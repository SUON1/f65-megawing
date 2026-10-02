#!/usr/bin/env python3
"""Read-only FAT32 root audit including long-name/short-alias diagnosis.

Never writes the raw device. Reports allocation and hashes independently of
the mounted filesystem; long names are diagnostic only, never release names.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import struct

from d81_sd_contiguity import disk_info, merge_adjacent


class AllocationMismatch(ValueError):
    def __init__(self, entry, cluster_bytes, clusters):
        required = (entry['bytes'] + cluster_bytes - 1) // cluster_bytes
        self.details = {
            'clusterBytes': cluster_bytes, 'requiredClusters': required,
            'allocatedClusters': len(clusters),
            'allocatedBytes': len(clusters) * cluster_bytes,
            'allocationIssue': 'UNDERALLOCATED' if len(clusters) < required else 'OVERALLOCATED',
            'chain': clusters,
        }
        super().__init__(
            f"{entry['name']}: file size/chain allocation mismatch; "
            f"size={entry['bytes']} bytes, cluster={cluster_bytes} bytes, "
            f"required={required} clusters, allocated={len(clusters)} clusters")


class Fat32:
    def __init__(self, fd):
        self.fd = fd
        boot = self.read(0, 512)
        if boot[510:512] != b'\x55\xaa' or boot[82:90] != b'FAT32   ':
            raise ValueError('not a FAT32 boot record')
        self.sector = struct.unpack_from('<H', boot, 11)[0]
        spc = boot[13]
        reserved = struct.unpack_from('<H', boot, 14)[0]
        fats = boot[16]
        fat_sectors = struct.unpack_from('<I', boot, 36)[0]
        total = struct.unpack_from('<I', boot, 32)[0]
        flags = struct.unpack_from('<H', boot, 40)[0]
        self.root = struct.unpack_from('<I', boot, 44)[0]
        if self.sector != 512 or spc not in (1, 2, 4, 8, 16, 32, 64, 128) or fats not in (1, 2):
            raise ValueError('unsupported FAT32 geometry')
        self.cluster = self.sector * spc
        self.data = (reserved + fats * fat_sectors) * self.sector
        self.max_cluster = (total * self.sector - self.data) // self.cluster + 1
        active = (flags & 15) if flags & 128 else 0
        if active >= fats or self.max_cluster < 65525:
            raise ValueError('invalid FAT32 geometry')
        self.fat = self.read((reserved + active * fat_sectors) * self.sector, fat_sectors * self.sector)
        if len(self.fat) < (self.max_cluster + 1) * 4:
            raise ValueError('FAT too short')
        if not flags & 128:
            for index in range(1, fats):
                other = self.read((reserved + index * fat_sectors) * self.sector, len(self.fat))
                if other != self.fat:
                    raise ValueError('mirrored FATs differ')

    def read(self, offset, size):
        data = os.pread(self.fd, size, offset)
        if len(data) != size:
            raise ValueError('short raw read')
        return data

    def chain(self, first):
        result, seen = [], set()
        current = first
        while current < 0x0ffffff8:
            if not 2 <= current <= self.max_cluster or current in seen:
                raise ValueError('invalid or looping FAT chain')
            seen.add(current)
            result.append(current)
            current = struct.unpack_from('<I', self.fat, current * 4)[0] & 0x0fffffff
        return result

    def offset(self, cluster):
        return self.data + (cluster - 2) * self.cluster

    def root_entries(self, include_directories=False):
        pending = []
        for cluster in self.chain(self.root):
            data = self.read(self.offset(cluster), self.cluster)
            for index in range(0, len(data), 32):
                entry = data[index:index + 32]
                if entry[0] == 0:
                    return
                if entry[0] == 229:
                    pending = []
                    continue
                if entry[11] == 15:
                    pending.append(entry)
                    continue
                short_raw = entry[:11]
                short = short_raw[:8].decode('ascii').rstrip() + '.' + short_raw[8:].decode('ascii').rstrip()
                name = short
                if pending:
                    checksum = 0
                    for value in short_raw:
                        checksum = (((checksum & 1) << 7) + (checksum >> 1) + value) & 255
                    expected_order = list(range(len(pending), 0, -1))
                    if (not pending[0][0] & 64 or [p[0] & 31 for p in pending] != expected_order
                            or any(p[13] != checksum for p in pending)):
                        raise ValueError('invalid long-name sequence')
                    raw = b''.join(p[1:11] + p[14:26] + p[28:32] for p in reversed(pending))
                    name = raw.decode('utf-16le').split('\x00')[0].rstrip('\uffff')
                pending = []
                if entry[11] & 8 or (entry[11] & 16 and not include_directories):
                    continue
                first = struct.unpack_from('<H', entry, 26)[0] | (struct.unpack_from('<H', entry, 20)[0] << 16)
                yield {'name': name, 'shortName': short, 'attributes': entry[11],
                       'firstCluster': first, 'bytes': struct.unpack_from('<I', entry, 28)[0]}

    def inspect(self, entry):
        size = entry['bytes']
        clusters = self.chain(entry['firstCluster'])
        if len(clusters) != (size + self.cluster - 1) // self.cluster:
            raise AllocationMismatch(entry, self.cluster, clusters)
        digest, extents, logical = hashlib.sha256(), [], 0
        for cluster in clusters:
            length = min(self.cluster, size - logical)
            digest.update(self.read(self.offset(cluster), self.cluster)[:length])
            extents.append((logical, length, self.offset(cluster)))
            logical += length
        extents = merge_adjacent(extents)
        return {**entry, 'sha256': digest.hexdigest(), 'extentCount': len(extents),
                'extents': [{'logicalOffset': l, 'bytes': n, 'deviceOffset': d} for l, n, d in extents]}


def inspect_names(volume, names):
    """Preserve all requested forensic results; never turn an error into PASS."""
    entries = {e['name'].upper(): e for e in volume.root_entries()}
    results = []
    for name in names:
        entry = entries.get(name.upper())
        if entry is None:
            results.append({'name': name, 'state': 'ABSENT'})
            continue
        try:
            results.append(volume.inspect(entry))
        except (ValueError, OSError) as error:
            results.append({**entry, 'state': 'ERROR', 'error': str(error),
                            **getattr(error, 'details', {})})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mount', type=Path)
    parser.add_argument('names', nargs='+')
    parser.add_argument('--json', type=Path, required=True)
    args = parser.parse_args()
    info = disk_info(args.mount)
    if not os.path.ismount(args.mount) or info.get('RemovableMedia') is not True:
        raise ValueError('intended removable FAT32 root required')
    node = info['DeviceNode']
    if not node.startswith('/dev/disk'):
        raise ValueError('unexpected device')
    fd = os.open(node.replace('/dev/disk', '/dev/rdisk', 1), os.O_RDONLY)
    try:
        volume = Fat32(fd)
        result = inspect_names(volume, args.names)
    finally:
        os.close(fd)
    report = {'state': 'READ_ONLY_FORENSICS_NOT_RELEASE', 'device': info,
              'inspectorSha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'files': result}
    # diskutil fields may include plist-specific values; stringify only metadata.
    rendered = json.dumps(report, indent=2, default=str) + '\n'
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(rendered)
    print(json.dumps(result, indent=2))
    if any(entry.get('state') == 'ERROR' for entry in result):
        raise SystemExit(f'Audit failed; diagnostics saved to {args.json}. No transfer authorized.')


if __name__ == '__main__':
    main()
