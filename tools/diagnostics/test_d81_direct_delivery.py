#!/usr/bin/env python3
"""Exercise the pinned allocator on disposable, fragmented FAT32 images only."""
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import d81_direct_delivery as delivery

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'build/r0f/d81-workflow/R0FGIAG4/canonical/R0FGIAG4.D81'
SECTOR = 512
CLUSTER = 4096
FAT_BYTES = 520 * SECTOR
DATA = (32 + 1040) * SECTOR
CLUSTERS = 66000
ALLOCATIONS = []


def fixture(path, no_run=False):
    boot = bytearray(512)
    boot[:3] = b'\xeb\x58\x90'
    boot[3:11] = b'MSDOS5.0'
    struct.pack_into('<H', boot, 11, 512)
    boot[13] = 8
    struct.pack_into('<H', boot, 14, 32)
    boot[16] = 2
    boot[21] = 248
    struct.pack_into('<I', boot, 32, DATA // 512 + CLUSTERS * 8)
    struct.pack_into('<I', boot, 36, 520)
    struct.pack_into('<I', boot, 44, 2)
    struct.pack_into('<HH', boot, 48, 1, 6)
    boot[64] = 128
    boot[66] = 41
    boot[71:82] = b'FIXTURE    '
    boot[82:90] = b'FAT32   '
    boot[510:] = b'\x55\xaa'
    fsinfo = bytearray(512)
    struct.pack_into('<I', fsinfo, 0, 0x41615252)
    struct.pack_into('<III', fsinfo, 484, 0x61417272, 0xffffffff, 0xffffffff)
    struct.pack_into('<I', fsinfo, 508, 0xaa550000)
    fat = bytearray(FAT_BYTES)
    struct.pack_into('<III', fat, 0, 0x0ffffff8, 0xffffffff, 0x0fffffff)
    chain = list(range(3, CLUSTERS + 2 if no_run else 401, 2))
    for i, c in enumerate(chain):
        struct.pack_into('<I', fat, c * 4, chain[i + 1] if i + 1 < len(chain) else 0x0fffffff)
    directory = bytearray(CLUSTER)
    directory[:11] = b'CONTROL BIN'
    directory[11] = 32
    struct.pack_into('<H', directory, 26, chain[0])
    struct.pack_into('<I', directory, 28, len(chain) * CLUSTER)
    with path.open('wb') as out:
        out.truncate(DATA + CLUSTERS * CLUSTER)
        for offset, value in ((0, boot), (512, fsinfo), (3072, boot),
                              (3584, fsinfo), (32 * 512, fat),
                              ((32 + 520) * 512, fat), (DATA, directory)):
            out.seek(offset)
            out.write(value)
        for c in chain:
            out.seek(DATA + (c - 2) * CLUSTER)
            out.write(bytes([c % 251]) * CLUSTER)


def digest(path):
    with path.open('rb') as stream:
        value = hashlib.sha256()
        for data in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(data)
        return value.hexdigest()


class DirectDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='f65-allocator-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.image = self.root / 'partition.img'
        fixture(self.image)

    def test_three_allocations_preserve_every_unrelated_byte(self):
        for name in ('R0FGIAG4.D81', 'TEST0002.D81', 'TEST0003.D81'):
            source = self.root / name
            source.write_bytes(SOURCE.read_bytes())
            before = self.image.read_bytes()
            result = delivery.deliver(self.image, source, self.root / name[:-4])
            self.assertEqual(result['extentCount'], 1)
            self.assertEqual(result['sha256'], delivery.sha(SOURCE))
            # Only allocated payload, its FAT entries, and free root slots may change.
            after = bytearray(self.image.read_bytes())
            first = result['firstCluster']
            count = delivery.IMAGE_BYTES // CLUSTER
            for base in (32 * 512, (32 + 520) * 512):
                a, b = base + first * 4, base + (first + count) * 4
                after[a:b] = before[a:b]
            a = DATA + (first - 2) * CLUSTER
            after[a:a + delivery.IMAGE_BYTES] = before[a:a + delivery.IMAGE_BYTES]
            for sector in (1, 7):
                at = sector * 512 + 488
                after[at:at + 8] = before[at:at + 8]
            for offset in range(DATA, DATA + CLUSTER, 32):
                if before[offset] in (0, 229):
                    after[offset:offset + 32] = before[offset:offset + 32]
            self.assertEqual(hashlib.sha256(after).digest(), hashlib.sha256(before).digest())
            ALLOCATIONS.append({**result, 'unrelatedBytes': 'UNCHANGED'})
        with delivery.volume(self.image) as vol:
            self.assertEqual(len(list(vol.root_entries())), 4)
        checked = subprocess.run(['/sbin/fsck_msdos', '-n', str(self.image)],
                                 capture_output=True, text=True)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_no_run_is_read_only(self):
        fixture(self.image, no_run=True)
        before = digest(self.image)
        with self.assertRaisesRegex(ValueError, 'no contiguous free run'):
            delivery.preflight(self.image, 'R0FGIAG4.D81')
        self.assertEqual(before, digest(self.image))

    def test_alias_collision(self):
        with self.image.open('r+b') as out:
            out.seek(DATA)
            out.write(b'R0FGIAG4D81')
        with self.assertRaisesRegex(ValueError, 'already exists'):
            delivery.preflight(self.image, 'R0FGIAG4.D81')

    def test_mirror_mismatch(self):
        with self.image.open('r+b') as out:
            out.seek((32 + 520) * 512 + 5000)
            out.write(b'\x01')
        with self.assertRaisesRegex(ValueError, 'mirrored FATs differ'):
            delivery.preflight(self.image, 'R0FGIAG4.D81')

    def test_invalid_name(self):
        with self.assertRaises(ValueError):
            delivery.preflight(self.image, 'R0FSUCC10.D81')

    def test_full_directory(self):
        with self.image.open('r+b') as out:
            for i in range(CLUSTER // 32):
                out.seek(DATA + i * 32)
                out.write((f'F{i:07d}' + 'BIN').encode('ascii') + bytes([32]) + bytes(20))
        with self.assertRaisesRegex(ValueError, 'spare slots'):
            delivery.preflight(self.image, 'R0FGIAG4.D81')

    def test_release_identity(self):
        manifest = ROOT / 'docs/evidence/r0f/successor/2026-09-22-workflow/R0FGIAG4/release.json'
        delivery.verify_release(SOURCE, manifest)
        value = json.loads(manifest.read_text())
        value['D81_SHA256'] = '0' * 64
        bad = self.root / 'bad.json'
        bad.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, 'release gate failed'):
            delivery.verify_release(SOURCE, bad)

    def test_changed_allocator_rejected(self):
        lock = json.loads(delivery.LOCK.read_text())
        lock['binarySha256'] = '0' * 64
        bad = self.root / 'lock.json'
        bad.write_text(json.dumps(lock))
        with patch.object(delivery, 'LOCK', bad):
            with self.assertRaisesRegex(ValueError, 'pinned allocator'):
                delivery.pinned_tool()

    def test_stale_qualification(self):
        report = self.root / 'qualification.json'
        report.write_text(json.dumps({'result': 'PASS', 'identity': {}}))
        with self.assertRaisesRegex(ValueError, 'stale'):
            delivery.require_qualification(report)

    def test_source_drift_stops_before_write(self):
        before = digest(self.image)
        with self.assertRaisesRegex(ValueError, 'source changed'):
            delivery.deliver(self.image, SOURCE, self.root / 'out', '0' * 64)
        self.assertFalse((self.root / 'out').exists())
        self.assertEqual(before, digest(self.image))

    def test_zero_exit_with_error_is_not_success(self):
        fake = subprocess.CompletedProcess([], 0, 'ERROR: allocation failed', '')
        with patch.object(delivery.subprocess, 'run', return_value=fake):
            with self.assertRaisesRegex(ValueError, 'allocator failed'):
                delivery.invoke(delivery.pinned_tool(), self.image, 'unused',
                                self.root, self.root / 'failed.log')

    def test_fsinfo_uses_sector_aligned_io(self):
        before = delivery.preflight(self.image, 'R0FHOST2.D81')
        real_write = delivery.os.pwrite
        real_read = delivery.os.pread

        def aligned_write(fd, data, offset):
            self.assertEqual(offset % 512, 0)
            self.assertEqual(len(data) % 512, 0)
            return real_write(fd, data, offset)

        def aligned_read(fd, length, offset):
            self.assertEqual(offset % 512, 0)
            self.assertEqual(length % 512, 0)
            return real_read(fd, length, offset)

        with patch.object(delivery.os, 'pwrite', side_effect=aligned_write), \
                patch.object(delivery.os, 'pread', side_effect=aligned_read):
            delivery.refresh_free_count(self.image, before)

    def test_blank_backup_preserved_through_delivery(self):
        with self.image.open('r+b') as out:
            out.seek(7 * 512)
            out.write(bytes(512))
        before = delivery.preflight(self.image, SOURCE.name)
        self.assertEqual(before['infoSectors'], [1])
        result = delivery.deliver(self.image, SOURCE, self.root / 'blank-backup')
        self.assertEqual(result['sha256'], delivery.sha(SOURCE))
        self.assertEqual(result['extentCount'], 1)
        with self.image.open('rb') as stream:
            reserved = stream.read(32 * 512)
        self.assertEqual(reserved[7 * 512:8 * 512], bytes(512))
        normalized = bytearray(reserved)
        normalized[512 + 488:512 + 496] = before['reserved'][512 + 488:512 + 496]
        self.assertEqual(normalized, before['reserved'])
        checked = subprocess.run(['/sbin/fsck_msdos', '-n', str(self.image)],
                                 capture_output=True, text=True)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_blank_primary_still_rejected(self):
        with self.image.open('r+b') as out:
            out.seek(512)
            out.write(bytes(512))
        with self.assertRaisesRegex(ValueError, 'invalid primary FSInfo signature at sector 1'):
            delivery.preflight(self.image, SOURCE.name)

    def test_nonzero_invalid_backup_still_rejected(self):
        with self.image.open('r+b') as out:
            out.seek(7 * 512)
            out.write(b'bad' + bytes(509))
        with self.assertRaisesRegex(ValueError, 'invalid backup FSInfo signature at sector 7'):
            delivery.preflight(self.image, SOURCE.name)

    def test_backup_outside_reserved_rejected(self):
        with self.image.open('r+b') as out:
            out.seek(50)
            out.write(struct.pack('<H', 32))
        with self.assertRaisesRegex(ValueError, 'unsupported backup FSInfo sector 33'):
            delivery.preflight(self.image, SOURCE.name)


if __name__ == '__main__':
    report = None
    if '--qualification' in sys.argv:
        at = sys.argv.index('--qualification')
        report = Path(sys.argv[at + 1])
        del sys.argv[at:at + 2]
        if report.exists():
            raise SystemExit('refusing to overwrite qualification evidence')
    result = unittest.main(exit=False).result
    if report:
        report.parent.mkdir(parents=True, exist_ok=True)
        delivery.record(report, {'result': 'PASS' if result.wasSuccessful() else 'FAIL',
                                 'testsRun': result.testsRun,
                                 'identity': delivery.qualification_identity(),
                                 'allocations': ALLOCATIONS,
                                 'sourceSha256': delivery.sha(SOURCE),
                                 'scope': 'synthetic fragmented FAT32 partition; no SD writes'})
    raise SystemExit(0 if result.wasSuccessful() else 1)
