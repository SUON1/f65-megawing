#!/usr/bin/env python3
"""Pinned MEGA65 FAT allocator with independent pre/post verification.

MANDATORY D81 LOADABILITY GATE
Read and obey 00_D81_LOADABILITY_GATE.md before any image or media operation.
No host formatting request can guarantee SD allocation. Never write a mounted
raw filesystem. Never overwrite an existing identity. A failed copy is retained
for diagnosis, never repaired or silently retried. Physical chooser proof is
still required after exact hash, one extent and safe eject pass.
"""

import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import struct
import subprocess
import tempfile

from d81_delivery import IMAGE_BYTES, require_name
from d81_fat32_audit import Fat32
from d81_foundation_compare import Image
from d81_sd_contiguity import disk_info

ROOT = Path(__file__).resolve().parents[2]
LOCK = ROOT / 'toolchain/d81_delivery.lock.json'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def record(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def pinned_tool():
    lock = json.loads(LOCK.read_text())
    tool = ROOT / lock['binary']
    if not tool.is_file() or sha(tool) != lock['binarySha256']:
        raise ValueError('missing/changed pinned allocator; see docs/D81_WORKFLOW.md')
    return tool


def qualification_identity():
    paths = [Path(__file__), LOCK,
             ROOT / 'tools/diagnostics/test_d81_direct_delivery.py',
             ROOT / 'tools/diagnostics/d81_fat32_audit.py',
             ROOT / 'tools/diagnostics/d81_delivery.py',
             ROOT / 'tools/diagnostics/d81_foundation_compare.py',
             ROOT / 'tools/diagnostics/d81_sd_contiguity.py', pinned_tool()]
    return {str(p.relative_to(ROOT)): sha(p) for p in paths}


def require_qualification(path):
    value = json.loads(path.read_text())
    if value.get('result') != 'PASS' or value.get('identity') != qualification_identity():
        raise ValueError('allocator qualification missing or stale; rerun fixture tests')


def verify_release(source, manifest):
    require_name(source.name)
    value = json.loads(manifest.read_text())
    if (value['D81_FILENAME'] != source.name
            or value['D81_BYTES'] != IMAGE_BYTES
            or value['D81_SHA256'] != sha(source)
            or value['D81_STATE'] != 'XEMU_BOOT_VERIFIED'
            or any(value[key] != 'PASS' for key in
                   ('HOST_STRUCTURAL_RESULT', 'HOST_CONTENT_RESULT', 'XEMU_RESULT'))):
        raise ValueError('source identity or host/Xemu release gate failed')
    runs = value['XEMU_EVIDENCE']
    if [r['run'] for r in runs] != ['ntsc-1', 'ntsc-2', 'pal-1', 'pal-2']:
        raise ValueError('missing four independent NTSC/PAL boots')
    if any(r['mountedD81Filename'] != source.name
           or r['preRunD81Sha256'] != value['D81_SHA256'] for r in runs):
        raise ValueError('Xemu filename/hash does not match source')
    Image(source)
    return value


@contextlib.contextmanager
def volume(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        yield Fat32(fd)
    finally:
        os.close(fd)


def root_blocks(vol):
    return {c: vol.read(vol.offset(c), vol.cluster) for c in vol.chain(vol.root)}


def free_run(vol, required):
    count = 0
    for c in range(2, vol.max_cluster + 1):
        # Upstream scans raw FAT entries, so require all 32 bits to be zero.
        count = count + 1 if struct.unpack_from('<I', vol.fat, c * 4)[0] == 0 else 0
        if count == required:
            return c - count + 1
    raise ValueError('no contiguous free run; no media write performed')


def info_sectors(vol, boot):
    """Return only verified FSInfo sectors that may have their hints updated.

    A backup boot pointer is not evidence that a backup FSInfo was populated.
    The observed card has valid primary FSInfo and an all-zero backup slot.
    Preserve that slot; never manufacture a backup or accept arbitrary junk.
    """
    reserved = struct.unpack_from('<H', boot, 14)[0]
    primary, backup = struct.unpack_from('<HH', boot, 48)
    candidates = [('primary', primary)]
    if backup not in (0, 65535):
        candidates.append(('backup', backup + primary))
    sectors = []
    for role, sector in candidates:
        if not 0 < sector < reserved:
            raise ValueError(f'unsupported {role} FSInfo sector {sector}, reserved={reserved}')
        data = vol.read(sector * 512, 512)
        if role == 'backup' and not any(data):
            continue
        if (struct.unpack_from('<I', data, 0)[0] != 0x41615252
                or struct.unpack_from('<I', data, 484)[0] != 0x61417272
                or struct.unpack_from('<I', data, 508)[0] != 0xaa550000):
            raise ValueError(f'invalid {role} FSInfo signature at sector {sector}')
        sectors.append(sector)
    return sectors


def refresh_free_count(path, before):
    """Upstream leaves advisory FSInfo counts unchanged; recompute from FAT."""
    with volume(path) as vol:
        free = sum((struct.unpack_from('<I', vol.fat, c * 4)[0] & 0x0fffffff) == 0
                   for c in range(2, vol.max_cluster + 1))
        updated = {}
        for sector in before['infoSectors']:
            data = bytearray(vol.read(sector * 512, 512))
            struct.pack_into('<II', data, 488, free, 0xffffffff)
            updated[sector] = bytes(data)
    fd = os.open(path, os.O_RDWR)
    try:
        for sector in before['infoSectors']:
            # Raw character devices require sector-aligned I/O. Preserve every
            # other byte rather than attempting an eight-byte unaligned write.
            if os.pwrite(fd, updated[sector], sector * 512) != 512:
                raise ValueError('short FSInfo write')
        os.fsync(fd)
    finally:
        os.close(fd)
    with volume(path) as vol:
        for sector in before['infoSectors']:
            if vol.read(sector * 512, 512) != updated[sector]:
                raise ValueError('FSInfo readback mismatch')


def preflight(path, filename):
    require_name(filename)
    stage = filename[:-4] + '.TMP'
    with volume(path) as vol:
        boot = vol.read(0, 512)
        if (boot[16] != 2 or vol.root != 2 or vol.cluster != 4096
                or struct.unpack_from('<H', boot, 40)[0] != 0):
            raise ValueError('qualified layout requires two mirrored FATs, root 2, 4KiB clusters, no FAT flags')
        blocks = root_blocks(vol)
        # Check aliases for ALL active entries, including directories. The
        # inspector also validates LFN chains for files; malformed names fail.
        # Proper 8+3 padding is necessary for names shorter than eight chars.
        forbidden = {(n.split('.')[0].ljust(8) + n.split('.')[1]).encode('ascii')
                     for n in (filename, stage)}
        empty_run = 0
        enough_slots = False
        for block in blocks.values():
            for at in range(0, len(block), 32):
                slot = block[at:at + 32]
                if slot[0] not in (0, 229) and slot[:11].upper() in forbidden:
                    raise ValueError('destination/staging identity already exists; no overwrite')
                empty_run = empty_run + 1 if slot[0] in (0, 229) else 0
                enough_slots |= empty_run >= 3
        if not enough_slots:
            raise ValueError('root directory lacks spare slots; directory growth is not permitted')
        for entry in vol.root_entries(include_directories=True):
            if entry['name'].upper() in (filename, stage):
                raise ValueError('long-name destination/staging collision')
        start = free_run(vol, (IMAGE_BYTES + vol.cluster - 1) // vol.cluster)
        return {'fat': vol.fat, 'root': blocks, 'boot': boot,
                'reserved': vol.read(0, struct.unpack_from('<H', boot, 14)[0] * 512),
                'infoSectors': info_sectors(vol, boot),
                'clusterBytes': vol.cluster, 'firstFreeRun': start}


def audit(path, name, digest, before):
    with volume(path) as vol:
        matches = [e for e in vol.root_entries() if e['name'] == name]
        if len(matches) != 1 or matches[0]['shortName'] != name:
            raise ValueError('missing exact FAT short-name entry')
        result = vol.inspect(matches[0])
        if (result['sha256'] != digest or result['bytes'] != IMAGE_BYTES
                or result['extentCount'] != 1):
            raise ValueError('raw content/length/one-extent verification failed')
        chain = vol.chain(result['firstCluster'])
        if chain != list(range(before['firstFreeRun'], before['firstFreeRun'] + len(chain))):
            raise ValueError('allocation differs from independently predicted free run')
        # Check the entire FAT, not only the new file's chain. Existing entries
        # and free space outside the candidate must remain exactly unchanged.
        masked = bytearray(vol.fat)
        for c in chain:
            if before['fat'][c * 4:c * 4 + 4] != bytes(4):
                raise ValueError('allocator used a previously occupied cluster')
            masked[c * 4:c * 4 + 4] = bytes(4)
        if bytes(masked) != before['fat']:
            raise ValueError('unexpected FAT modification outside candidate chain')
        if vol.read(0, 512) != before['boot']:
            raise ValueError('boot sector unexpectedly changed')
        reserved = bytearray(vol.read(0, len(before['reserved'])))
        for sector in before['infoSectors']:
            at = sector * 512 + 488
            reserved[at:at + 8] = before['reserved'][at:at + 8]
        if reserved != before['reserved']:
            raise ValueError('reserved metadata changed outside FSInfo hints')
        after = root_blocks(vol)
        if after.keys() != before['root'].keys():
            raise ValueError('root allocation changed')
        for c, old in before['root'].items():
            for at in range(0, len(old), 32):
                if old[at] not in (0, 229) and old[at:at + 32] != after[c][at:at + 32]:
                    raise ValueError('existing directory entry changed')
        return result


def invoke(tool, path, command, cwd, log):
    result = subprocess.run([str(tool), '-n', '-d', str(path), '-c', command],
                            cwd=cwd, capture_output=True, text=True, timeout=120)
    Path(log).write_text(result.stdout + result.stderr)
    # This upstream CLI may return zero even when a queued command fails.
    if result.returncode or re.search(r'\b(ERROR|FATAL)\b', result.stdout + result.stderr):
        raise ValueError('allocator failed; inspect ' + str(log))
    fd = os.open(path, os.O_RDWR)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def deliver(path, source, out, expected_sha=None):
    """Shared backend. Caller must provide a regular image or unmounted partition."""
    tool = pinned_tool()
    require_name(source.name)
    Image(source)
    digest = sha(source)
    if expected_sha is not None and digest != expected_sha:
        raise ValueError('source changed after release verification')
    before = preflight(path, source.name)
    out.mkdir(parents=True, exist_ok=False)
    # Preserve metadata before writing; no automatic restoration on failure.
    (out / 'fat-before.bin').write_bytes(before['fat'])
    (out / 'boot-before.bin').write_bytes(before['boot'])
    (out / 'reserved-before.bin').write_bytes(before['reserved'])
    for c, data in before['root'].items():
        (out / f'root-{c}-before.bin').write_bytes(data)
    record(out / 'preflight.json', {k: before[k] for k in ('clusterBytes', 'firstFreeRun')})
    stage = source.name[:-4] + '.TMP'
    with tempfile.TemporaryDirectory(prefix='f65-d81-', dir='/tmp') as temp:
        payload = Path(temp) / 'PAYLOAD.D81'
        shutil.copyfile(source, payload)
        if sha(payload) != digest:
            raise ValueError('source changed while staging locally')
        invoke(tool, path, 'put PAYLOAD.D81 ' + stage, temp, out / 'put.log')
        staged = audit(path, stage, digest, before)
        record(out / 'staging.json', staged)
        invoke(tool, path, 'rename ' + stage + ' ' + source.name, temp, out / 'rename.log')
        refresh_free_count(path, before)
        final = audit(path, source.name, digest, before)
        if final['extents'] != staged['extents']:
            raise ValueError('allocation changed at rename')
        record(out / 'final.json', final)
    return final


def install_sd(args):
    """Explicit real-card operation; never used by fixture tests."""
    release = verify_release(args.source, args.manifest)
    pinned_tool()
    require_qualification(args.qualification)
    if args.report.exists():
        raise ValueError('report directory already exists; no media write performed')
    if not args.confirm_raw_write:
        raise ValueError('explicit --confirm-raw-write acknowledgement is required')
    if os.geteuid() != 0:
        raise ValueError('local administrator authentication is required')
    mount = args.mount.resolve()
    for local in (args.source, args.manifest, args.report, args.qualification):
        if local.resolve().is_relative_to(mount):
            raise ValueError('source/evidence/report paths must be off the target card')
    if not os.path.ismount(mount):
        raise ValueError('intended card must initially be mounted')
    info = disk_info(mount)
    if (info.get('VolumeUUID') != args.volume_uuid
            or info.get('RemovableMedia') is not True
            or info.get('FilesystemType') != 'msdos'):
        raise ValueError('card UUID/removable/FAT32 identity mismatch')
    node = info['DeviceNode']
    if not re.fullmatch(r'/dev/disk[0-9]+s[0-9]+', node):
        raise ValueError('only the resolved FAT partition may be written')
    raw = node.replace('/dev/disk', '/dev/rdisk', 1)
    preflight(raw, args.source.name)
    # Never force unmount. Open files or a busy volume must stop the workflow.
    subprocess.run(['/usr/sbin/diskutil', 'unmount', node], check=True)
    fresh = disk_info(Path(node))
    if fresh.get('Mounted') or fresh.get('VolumeUUID') != args.volume_uuid:
        raise ValueError('partition did not unmount or changed identity')
    # Read-only check: never repair other files, cross-links or filesystem hints.
    subprocess.run(['/sbin/fsck_msdos', '-n', raw], check=True)
    try:
        result = deliver(Path(raw), args.source, args.report, release['D81_SHA256'])
    except BaseException:
        # Preserve failure state and leave unmounted to avoid further changes.
        raise
    subprocess.run(['/sbin/fsck_msdos', '-n', raw], check=True)
    # Re-mount for independent filesystem-level content comparison, then eject.
    subprocess.run(['/usr/sbin/diskutil', 'mount', node], check=True)
    final_info = disk_info(Path(node))
    if final_info.get('VolumeUUID') != args.volume_uuid:
        raise ValueError('card identity changed after remount')
    final_path = Path(final_info['MountPoint']) / args.source.name
    if sha(final_path) != result['sha256']:
        raise ValueError('mounted file differs from raw verified content')
    with volume(raw) as vol:
        entries = [e for e in vol.root_entries() if e['name'] == args.source.name]
        if len(entries) != 1 or vol.inspect(entries[0]) != result:
            raise ValueError('raw final content/allocation changed after remount')
    subprocess.run(['/usr/sbin/diskutil', 'eject', node], check=True)
    record(args.report / 'sd-release.json', {
        **release,
        'D81_FILENAME': args.source.name, 'D81_SHA256': result['sha256'],
        'D81_BYTES': IMAGE_BYTES, 'D81_STATE': 'AWAITING_PHYSICAL_CHOOSER_VERIFICATION',
        'SD_COPY_SHA256': result['sha256'], 'SD_FILESYSTEM': info['FilesystemType'],
        'SD_VOLUME_UUID': args.volume_uuid, 'SD_DEVICE_IDENTIFIER': info['DeviceIdentifier'],
        'SD_TRANSFER_METHOD': 'pinned MEGA65 allocator on unmounted FAT32 partition',
        'SD_CONTIGUITY_RESULT': 'PASS', 'SD_EXTENT_COUNT': 1,
        'SD_EXTENT_EVIDENCE': result['extents'], 'SD_SAFE_EJECT_RESULT': 'PASS',
        'PHYSICAL_CHOOSER_RESULT': 'AWAITING HUMAN', 'allocatorSha256': sha(pinned_tool())})
    print('SD copy, one extent, mounted hash and safe eject PASS; physical chooser pending')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    image = sub.add_parser('test-image', help='regular FAT32 partition image only')
    image.add_argument('image', type=Path)
    image.add_argument('source', type=Path)
    image.add_argument('--report', required=True, type=Path)
    sd = sub.add_parser('install-sd', help='explicit real-card installation')
    sd.add_argument('source', type=Path)
    sd.add_argument('--manifest', required=True, type=Path)
    sd.add_argument('--mount', required=True, type=Path)
    sd.add_argument('--volume-uuid', required=True)
    sd.add_argument('--report', required=True, type=Path)
    sd.add_argument('--qualification', required=True, type=Path)
    sd.add_argument('--confirm-raw-write', action='store_true')
    args = parser.parse_args()
    args.source = args.source.resolve()
    if args.command == 'test-image':
        path = args.image.resolve()
        if not stat.S_ISREG(path.stat().st_mode) or str(path).startswith('/Volumes/'):
            raise ValueError('test-image accepts local regular files only')
        print(json.dumps(deliver(path, args.source, args.report), indent=2))
    else:
        install_sd(args)


if __name__ == '__main__':
    main()
