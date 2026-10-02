#!/usr/bin/env python3
"""Read-only FAT32 reserved-sector evidence; never installs or repairs anything."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct

from d81_sd_contiguity import disk_info


def inspect(fd):
    def sector(number):
        data = os.pread(fd, 512, number * 512)
        if len(data) != 512:
            raise ValueError('short sector read')
        return data

    boot = sector(0)
    if (boot[510:] != b'\x55\xaa' or boot[82:90] != b'FAT32   '
            or struct.unpack_from('<H', boot, 11)[0] != 512):
        raise ValueError('unsupported boot geometry')
    reserved = struct.unpack_from('<H', boot, 14)[0]
    primary, backup = struct.unpack_from('<HH', boot, 48)
    requested = [('primaryFSInfo', primary)]
    if backup not in (0, 65535):
        requested += [('backupBoot', backup), ('presumedBackupFSInfo', backup + primary)]
    result = {'reservedSectors': reserved, 'primaryFSInfoSector': primary,
              'backupBootSector': backup, 'bootHex': boot.hex(), 'sectors': []}
    for role, number in requested:
        entry = {'role': role, 'sector': number}
        if not 0 < number < reserved:
            entry['state'] = 'OUTSIDE_RESERVED_OR_ABSENT'
        else:
            data = sector(number)
            signatures = [struct.unpack_from('<I', data, offset)[0]
                          for offset in (0, 484, 508)]
            entry.update({
                'state': 'READ', 'sha256': hashlib.sha256(data).hexdigest(),
                'allZero': not any(data), 'hex': data.hex(),
                'signatures': [f'{value:08X}' for value in signatures],
                'validFSInfoSignatures': signatures == [0x41615252, 0x61417272, 0xaa550000],
                'freeCount': struct.unpack_from('<I', data, 488)[0],
                'nextFree': struct.unpack_from('<I', data, 492)[0]})
        result['sectors'].append(entry)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mount', type=Path)
    parser.add_argument('--json', required=True, type=Path)
    args = parser.parse_args()
    info = disk_info(args.mount)
    if (not os.path.ismount(args.mount) or info.get('RemovableMedia') is not True
            or info.get('FilesystemType') != 'msdos'):
        raise ValueError('mounted removable FAT32 volume required')
    node = info['DeviceNode']
    if not re.fullmatch(r'/dev/disk[0-9]+s[0-9]+', node):
        raise ValueError('partition device required')
    if args.json.resolve().is_relative_to(args.mount.resolve()):
        raise ValueError('diagnostic output must stay off the SD card')
    fd = os.open(node.replace('/dev/disk', '/dev/rdisk', 1), os.O_RDONLY)
    try:
        result = inspect(fd)
    finally:
        os.close(fd)
    result.update({'state': 'READ_ONLY_DIAGNOSTIC_NOT_RELEASE',
                   'device': node, 'volumeUUID': info.get('VolumeUUID')})
    args.json.parent.mkdir(parents=True, exist_ok=True)
    with args.json.open('x') as out:
        json.dump(result, out, indent=2)
        out.write('\n')
    # Preserve complete sectors locally; keep the paste-back output readable.
    result.pop('bootHex')
    for entry in result['sectors']:
        entry.pop('hex', None)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
