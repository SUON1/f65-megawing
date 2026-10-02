#!/usr/bin/env python3
"""Regression tests for the filename incident, allocation and raw FAT audit."""

import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from d81_delivery import contiguous_copy, require_name, rename_exclusive, IMAGE_BYTES
from d81_fat32_audit import AllocationMismatch, Fat32, inspect_names
import r0f_successor_emulator as runtime


def fake_transfer_tool():
    """Test-only OS boundary for executing the real transfer shell control flow.

    This never accesses a disk device. Allocation/FAT/eject are simulated, not
    physical evidence. The production helper has no mock or bypass option.
    """
    command = Path(sys.argv[0]).name
    arguments = sys.argv[1:]
    scenario = os.environ['D81_TEST_FAILURE']
    log = Path(os.environ['D81_TEST_LOG'])
    def record(phase):
        with log.open('a') as stream:
            stream.write(phase + '\n')
        if scenario == phase:
            raise SystemExit(2)
    if command == 'id':
        print('0')
    elif command == 'diskutil':
        record('eject')
    elif arguments[0] == '-':
        code = sys.stdin.read()
        if len(arguments) > 2:
            record('preflight')
        else:
            # Execute the actual post-eject report update from the helper.
            record('release')
            sys.argv = arguments
            exec(compile(code, '<helper-report-update>', 'exec'), {'__name__': '__main__'})
    elif arguments[0].endswith('d81_delivery.py'):
        action = arguments[1]
        if action == 'name':
            require_name(arguments[2])
        elif action == 'contiguous-copy':
            record('allocate')
            source, stage = map(Path, arguments[2:4])
            with stage.open('xb') as stream:
                stream.write(source.read_bytes())
        elif action == 'rename-exclusive':
            record('rename')
            rename_exclusive(Path(arguments[2]), Path(arguments[3]))
        else:
            raise AssertionError(action)
    elif arguments[0].endswith('d81_sd_contiguity.py'):
        phase = 'staging-audit' if arguments[1].endswith('.TMP') else 'final-audit'
        record(phase)
        report = Path(arguments[arguments.index('--json') + 1])
        report.write_text(json.dumps({'SD_EXTENT_COUNT': 1, 'SD_CONTIGUITY_RESULT': 'PASS'}))
    else:
        raise AssertionError(arguments)


@unittest.skipUnless(os.uname().sysname == 'Darwin', 'macOS shell/stat/rename semantics')
class TransferWorkflowTests(unittest.TestCase):
    def run_transfer(self, failure='', existing=False):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            diagnostic = root / 'tools/diagnostics'
            diagnostic.mkdir(parents=True)
            script = diagnostic / 'd81_sd_transfer.sh'
            production = Path(__file__).with_name(script.name).read_text()
            # Replace only the absolute eject executable inside this isolated
            # test copy. No configurable production escape hatch is added.
            script.write_text(production.replace('/usr/sbin/diskutil', 'diskutil'))
            binaries = root / 'bin'
            binaries.mkdir()
            shim = (f'#!{sys.executable}\nimport sys\n'
                    f'sys.path.insert(0, {str(Path(__file__).parent)!r})\n'
                    'from test_d81_delivery import fake_transfer_tool\n'
                    'fake_transfer_tool()\n')
            for name in ('python3', 'id', 'diskutil'):
                path = binaries / name
                path.write_text(shim)
                path.chmod(0o755)
            mount = root / 'card'
            mount.mkdir()
            source = root / 'R0FHOST1.D81'
            source.write_bytes(b'x' * IMAGE_BYTES)
            target = mount / source.name
            if existing:
                target.write_bytes(b'preserve existing')
            log = root / 'calls.txt'
            env = {**os.environ, 'PATH': str(binaries) + ':/usr/bin:/bin',
                   'D81_TEST_FAILURE': failure, 'D81_TEST_LOG': str(log),
                   'PYTHONDONTWRITEBYTECODE': '1'}
            result = subprocess.run(['/bin/sh', str(script), str(source), str(mount),
                                     hashlib.sha256(source.read_bytes()).hexdigest()],
                                    capture_output=True, text=True, env=env, timeout=30)
            calls = log.read_text().splitlines() if log.exists() else []
            report = root / 'build/d81-sd-transfer/R0FHOST1.D81.final.json'
            return (result, calls, target.read_bytes() if target.exists() else None,
                    list(mount.glob('*.TMP')), json.loads(report.read_text()) if report.exists() else {})

    def test_success_requires_ordered_gates_and_eject(self):
        result, calls, target, stages, report = self.run_transfer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls, ['preflight', 'allocate', 'staging-audit', 'rename', 'final-audit', 'eject', 'release'])
        self.assertEqual(target, b'x' * IMAGE_BYTES)
        self.assertEqual(stages, [])
        self.assertEqual(report['SD_SAFE_EJECT_RESULT'], 'PASS')
        self.assertEqual(report['PHYSICAL_CHOOSER_RESULT'], 'AWAITING HUMAN')

    def test_failure_at_each_boundary_never_releases(self):
        phases = ['preflight', 'allocate', 'staging-audit', 'rename', 'final-audit', 'eject']
        for index, phase in enumerate(phases):
            with self.subTest(phase=phase):
                result, calls, target, stages, report = self.run_transfer(phase)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(calls, phases[:index + 1])
                self.assertNotIn('D81 SD TRANSFER PASS', result.stdout)
                self.assertNotIn('SD_SAFE_EJECT_RESULT', report)
                self.assertEqual(stages, [])
                self.assertEqual(target, b'x' * IMAGE_BYTES if index >= 4 else None)

    def test_existing_identity_never_touched(self):
        result, calls, target, stages, report = self.run_transfer(existing=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(calls, [])
        self.assertEqual(target, b'preserve existing')
        self.assertEqual(stages, [])


class DeliveryTests(unittest.TestCase):
    def test_names(self):
        for name in (
                'R0FSUC10.D81', 'R0FHOST1.D81', 'R0FDIAG1.D81',
                'R0FDIAG2.D81', 'A.D81'):
            self.assertEqual(require_name(name), name)
        for name in ('R0FSUCC10.D81', 'r0fsuc10.d81', '../A.D81', 'A B.D81', 'A.D81\n', 'Ａ.D81'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                require_name(name)

    def test_builder_rejects_before_construction(self):
        with patch.object(runtime, 'c154') as tool:
            with self.assertRaises(ValueError):
                runtime.fresh_d81(Path('/absent'), Path('/absent/R0FSUCC10.D81'), 'TEST', {})
            tool.assert_not_called()

    def test_contiguous_request_and_exact_write(self):
        with tempfile.TemporaryDirectory() as temp:
            source, stage = Path(temp) / 'A.D81', Path(temp) / 'STAGE.TMP'
            source.write_bytes(bytes(range(256)) * 3200)
            def allocate(fd, command, request):
                self.assertEqual(command, 42)
                self.assertEqual(struct.unpack('@Iiqqq', request), (6, 3, 0, IMAGE_BYTES, 0))
                return struct.pack('@Iiqqq', 6, 3, 0, IMAGE_BYTES, IMAGE_BYTES)
            with patch('d81_delivery.fcntl.fcntl', side_effect=allocate):
                contiguous_copy(source, stage)
            self.assertEqual(source.read_bytes(), stage.read_bytes())
            with self.assertRaises(FileExistsError):
                contiguous_copy(source, stage)
            self.assertEqual(source.read_bytes(), stage.read_bytes())

    def test_failed_allocation_cleans_only_new_stage(self):
        with tempfile.TemporaryDirectory() as temp:
            source, stage = Path(temp) / 'A.D81', Path(temp) / 'STAGE.TMP'
            source.write_bytes(b'x' * IMAGE_BYTES)
            for response in (OSError('unsupported'), struct.pack('@Iiqqq', 6, 3, 0, IMAGE_BYTES, 4096)):
                options = {'side_effect': response} if isinstance(response, Exception) else {'return_value': response}
                with patch('d81_delivery.fcntl.fcntl', **options), self.assertRaises((OSError, ValueError)):
                    contiguous_copy(source, stage)
                self.assertFalse(stage.exists())
                self.assertEqual(source.stat().st_size, IMAGE_BYTES)

    def test_source_drift_stops_before_destination_creation(self):
        with tempfile.TemporaryDirectory() as temp:
            source, stage = Path(temp) / 'A.D81', Path(temp) / 'STAGE.TMP'
            source.write_bytes(b'x' * IMAGE_BYTES)
            with patch('d81_delivery.fcntl.fcntl') as allocate:
                with self.assertRaisesRegex(ValueError, 'source changed'):
                    contiguous_copy(source, stage, '0' * 64)
                allocate.assert_not_called()
            self.assertFalse(stage.exists())

    def test_partial_writes_complete_and_zero_write_cleans_stage(self):
        with tempfile.TemporaryDirectory() as temp:
            source, stage = Path(temp) / 'A.D81', Path(temp) / 'STAGE.TMP'
            source.write_bytes(b'x' * IMAGE_BYTES)
            real_write = os.write
            def partial(fd, data):
                return real_write(fd, data[:1024])
            allocated = struct.pack('@Iiqqq', 6, 3, 0, IMAGE_BYTES, IMAGE_BYTES)
            with patch('d81_delivery.fcntl.fcntl', return_value=allocated):
                with patch('d81_delivery.os.write', side_effect=partial):
                    contiguous_copy(source, stage, hashlib.sha256(source.read_bytes()).hexdigest())
                self.assertEqual(stage.read_bytes(), source.read_bytes())
                stage.unlink()
                with patch('d81_delivery.os.write', return_value=0):
                    with self.assertRaisesRegex(OSError, 'short staging write'):
                        contiguous_copy(source, stage)
                self.assertFalse(stage.exists())

    @unittest.skipUnless(os.uname().sysname == 'Darwin', 'Darwin atomic rename')
    def test_exclusive_rename_never_replaces(self):
        with tempfile.TemporaryDirectory() as temp:
            source, target = Path(temp) / 'STAGE.TMP', Path(temp) / 'A.D81'
            source.write_bytes(b'new')
            target.write_bytes(b'old')
            with self.assertRaises(FileExistsError):
                rename_exclusive(source, target)
            self.assertEqual(source.read_bytes(), b'new')
            self.assertEqual(target.read_bytes(), b'old')
            target.unlink()
            rename_exclusive(source, target)
            self.assertEqual(target.read_bytes(), b'new')
            self.assertFalse(source.exists())


class FatTests(unittest.TestCase):
    def setUp(self):
        self.file = tempfile.TemporaryFile()
        self.fd = self.file.fileno()
        self.fat_sectors = 520
        self.data_offset = (32 + 2 * self.fat_sectors) * 512
        self.file.truncate(self.data_offset + 66000 * 512)
        boot = bytearray(512)
        boot[510:512] = b'\x55\xaa'
        boot[82:90] = b'FAT32   '
        struct.pack_into('<H', boot, 11, 512)
        boot[13], boot[16] = 1, 2
        struct.pack_into('<H', boot, 14, 32)
        struct.pack_into('<I', boot, 32, self.data_offset // 512 + 66000)
        struct.pack_into('<I', boot, 36, self.fat_sectors)
        struct.pack_into('<I', boot, 44, 2)
        os.pwrite(self.fd, boot, 0)
        self.fat = bytearray(self.fat_sectors * 512)
        self.set_chain({2: 0x0fffffff, 3: 4, 4: 0x0fffffff})
        entry = bytearray(32)
        entry[:11] = b'R0FSUC10D81'
        entry[11] = 32
        struct.pack_into('<H', entry, 26, 3)
        struct.pack_into('<I', entry, 28, 1024)
        os.pwrite(self.fd, entry, self.data_offset)
        os.pwrite(self.fd, b'x' * 1024, self.data_offset + 512)

    def tearDown(self):
        self.file.close()

    def set_chain(self, values):
        for cluster, next_cluster in values.items():
            struct.pack_into('<I', self.fat, cluster * 4, next_cluster)
        for i in range(2):
            os.pwrite(self.fd, self.fat, (32 + i * self.fat_sectors) * 512)

    def test_contiguous_raw_content(self):
        volume = Fat32(self.fd)
        result = volume.inspect(next(volume.root_entries()))
        self.assertEqual(result['shortName'], 'R0FSUC10.D81')
        self.assertEqual(result['extentCount'], 1)
        self.assertEqual(result['sha256'], hashlib.sha256(b'x' * 1024).hexdigest())

    def test_fragmentation(self):
        self.set_chain({3: 5, 5: 0x0fffffff})
        volume = Fat32(self.fd)
        self.assertEqual(volume.inspect(next(volume.root_entries()))['extentCount'], 2)

    def test_full_d81_same_hash_one_extent_versus_nine(self):
        # Match the card's 4096-byte clusters and full 819200-byte image size.
        boot = bytearray(os.pread(self.fd, 512, 0))
        boot[13] = 8
        struct.pack_into('<I', boot, 32, self.data_offset // 512 + 66000 * 8)
        os.pwrite(self.fd, boot, 0)
        self.file.truncate(self.data_offset + 66000 * 4096)
        entry = bytearray(os.pread(self.fd, 32, self.data_offset))
        struct.pack_into('<I', entry, 28, IMAGE_BYTES)
        os.pwrite(self.fd, bytes(4096), self.data_offset)
        os.pwrite(self.fd, entry, self.data_offset)
        digest = hashlib.sha256(b'x' * IMAGE_BYTES).hexdigest()
        for lengths in ([200], [147, 2, 1, 1, 1, 1, 1, 6, 40]):
            with self.subTest(extents=len(lengths)):
                clusters, start = [], 3
                for length in lengths:
                    clusters.extend(range(start, start + length))
                    start += length + 10
                self.fat = bytearray(len(self.fat))
                chain = dict(zip(clusters, clusters[1:] + [0x0fffffff]))
                self.set_chain({2: 0x0fffffff, **chain})
                for cluster in clusters:
                    os.pwrite(self.fd, b'x' * 4096, self.data_offset + (cluster - 2) * 4096)
                volume = Fat32(self.fd)
                result = volume.inspect(next(volume.root_entries()))
                self.assertEqual(result['sha256'], digest)
                self.assertEqual(result['extentCount'], len(lengths))
                self.assertEqual(sum(e['bytes'] for e in result['extents']), IMAGE_BYTES)

    def test_chain_corruption_and_wrong_length(self):
        for value in (0, 1, 3, 0x0ffffff7, 0x0fffffff):
            with self.subTest(value=value):
                self.set_chain({3: value})
                volume = Fat32(self.fd)
                with self.assertRaises(ValueError):
                    volume.inspect(next(volume.root_entries()))

    def test_mirror_mismatch(self):
        os.pwrite(self.fd, b'xxxx', 32 * 512 + 12)
        with self.assertRaises(ValueError):
            Fat32(self.fd)

    def test_allocation_mismatch_reports_counts_and_keeps_strict_gate(self):
        for chain, allocated, issue in (({3: 0x0fffffff}, 1, 'UNDERALLOCATED'),
                                        ({3: 4, 4: 5, 5: 0x0fffffff}, 3, 'OVERALLOCATED')):
            with self.subTest(issue=issue):
                self.set_chain(chain)
                volume = Fat32(self.fd)
                with self.assertRaises(AllocationMismatch) as raised:
                    volume.inspect(next(volume.root_entries()))
                self.assertIn('R0FSUC10.D81', str(raised.exception))
                self.assertEqual(raised.exception.details['requiredClusters'], 2)
                self.assertEqual(raised.exception.details['allocatedClusters'], allocated)
                self.assertEqual(raised.exception.details['allocationIssue'], issue)

    def test_forensics_continues_after_bad_file(self):
        entry = bytearray(os.pread(self.fd, 32, self.data_offset))
        entry[:11] = b'GOOD    D81'
        struct.pack_into('<H', entry, 26, 6)
        os.pwrite(self.fd, entry, self.data_offset + 32)
        self.set_chain({3: 0x0fffffff, 6: 7, 7: 0x0fffffff})
        results = inspect_names(Fat32(self.fd), ['R0FSUC10.D81', 'GOOD.D81', 'MISSING.D81'])
        self.assertEqual(results[0]['state'], 'ERROR')
        self.assertEqual(results[0]['chain'], [3])
        self.assertEqual(results[1]['extentCount'], 1)
        self.assertEqual(results[2]['state'], 'ABSENT')

    def test_long_name_diagnosis_and_checksum(self):
        short = b'R0FSUC~1D81'
        checksum = 0
        for value in short:
            checksum = (((checksum & 1) << 7) + (checksum >> 1) + value) & 255
        raw = ('R0FSUCC10.D81\x00').encode('utf-16le').ljust(52, b'\xff')
        directory = bytearray(512)
        for offset, ordinal in ((0, 2), (32, 1)):
            part = raw[(ordinal - 1) * 26:ordinal * 26]
            directory[offset] = ordinal | (64 if ordinal == 2 else 0)
            directory[offset + 11] = 15
            directory[offset + 13] = checksum
            directory[offset + 1:offset + 11] = part[:10]
            directory[offset + 14:offset + 26] = part[10:22]
            directory[offset + 28:offset + 32] = part[22:]
        entry = bytearray(os.pread(self.fd, 32, self.data_offset))
        entry[:11] = short
        directory[64:96] = entry
        os.pwrite(self.fd, directory, self.data_offset)
        result = next(Fat32(self.fd).root_entries())
        self.assertEqual(result['name'], 'R0FSUCC10.D81')
        self.assertEqual(result['shortName'], 'R0FSUC~1.D81')
        directory[13] ^= 1
        os.pwrite(self.fd, directory, self.data_offset)
        with self.assertRaises(ValueError):
            list(Fat32(self.fd).root_entries())


if __name__ == '__main__':
    unittest.main()
