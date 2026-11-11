"""Focused host evidence for PC; never compile/link or execute a target image."""
from hashlib import sha256
import io
import json
import os
from pathlib import Path
import random
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
MASK = 2**32 - 1
MODULUS = 65535**2
OUTPUT = Path(tempfile.mkdtemp(prefix="f65-platform-clock-host-"))
COMMANDS = []


def advance(state, counts):
    """Independent event oracle: countdown to A expiries, then decrement B."""
    a, b = state
    while counts >= a:
        counts -= a
        a = 65535
        b -= 1
        if b == 0:
            b = 65535
    return a - counts, b


def encode(state):
    a, b = state
    return int.from_bytes(bytes([255 - (a & 255), 255 - (a >> 8),
                                 255 - (b & 255), 255 - (b >> 8)]), 'little')


def stable(state):
    a, b = state
    return [b >> 8, b & 255, b >> 8, a >> 8, a & 255, a >> 8, b & 255, b >> 8]


def run(args, stdin=""):
    index = len(COMMANDS)
    (OUTPUT / f"command-{index}.stdin").write_text(stdin)
    env = dict(os.environ, ASAN_OPTIONS="abort_on_error=1", UBSAN_OPTIONS="halt_on_error=1")
    completed = subprocess.run([str(a) for a in args], input=stdin, text=True,
                               capture_output=True, cwd=ROOT, env=env)
    (OUTPUT / f"command-{index}.stdout").write_text(completed.stdout)
    (OUTPUT / f"command-{index}.stderr").write_text(completed.stderr)
    COMMANDS.append({'argv': [str(a) for a in args], 'exit_code': completed.returncode})
    if completed.returncode:
        raise AssertionError(f"Host command failed ({completed.returncode}); retained at {OUTPUT}")
    return completed.stdout.splitlines()


def host(lines):
    return run([OUTPUT / 'clock-host'], '\n'.join(lines) + '\n')


class ClockTests(unittest.TestCase):
    def test_origin_duplicates_and_independent_event_timeline(self):
        rng = random.Random(650011)
        state = (65535, 65535)
        lines, expected = ['r'], ['RESET']
        total = 0
        lines.append(f's {encode(state)} 0')
        expected.append('0 0 2')
        increments = [0, 32, 65504, 32, 32] + [32 * rng.randrange(0, 60000000) for _ in range(250)]
        for step in increments:
            state = advance(state, step)
            total += step
            lines.append(f's {encode(state)} 0')
            expected.append(f'{total & MASK} 0 2')
        self.assertGreater(total, 10 * MODULUS)
        self.assertEqual(host(lines), expected)

    def test_published_upper_rollover_witness(self):
        self.assertEqual(advance((1, 1), 32), (65504, 65535))
        self.assertEqual(host(['r', f's {0xfffefffe} 0', f's {31} 0']),
                         ['RESET', '0 0 2', '32 0 2'])

    def test_numeric_half_range_edges_and_sticky_recovery(self):
        # +/-1 are pure arithmetic edges, not claims of 32-count reachability.
        lines, expected = [], []
        for step in (2**31 - 1, 2**31, 2**31 + 1):
            state = advance((65535, 65535), step)
            lines += ['r', 's 0 0', f's {encode(state)} 0', f's {encode(advance(state, 32))} 0']
            expected += ['RESET', '0 0 2', f'{step if step < 2**31 else 0} {int(step >= 2**31)} 2',
                         f'{step + 32 if step < 2**31 else 0} {int(step >= 2**31)} 2']
        lines += ['r', 's 32 0']
        expected += ['RESET', '0 0 2']
        self.assertEqual(host(lines), expected)

    def test_invalid_counts_faults_and_uninitialized_lifecycle(self):
        lines, expected = ['z', 's 32 0', 'r'], ['RESET', '0 1 0', 'RESET']
        for raw, flag in ((encode((0, 1)), 0), (encode((1, 0)), 0), (32, 1)):
            lines += ['r', 's 32 0', 's 64 0', f's {raw} {flag}', 's 96 0']
            expected += ['RESET', '0 0 2', '32 0 2', '32 1 2', '32 1 2']
        self.assertEqual(host(lines), expected)

    def test_full_period_alias_is_not_detectable(self):
        before = (12345, 54321)
        self.assertEqual(advance(before, MODULUS), before)
        self.assertEqual(host(['r', f's {encode(before)} 0', f's {encode(before)} 0']),
                         ['RESET', '0 0 2', '0 0 2'])

    def adapter_samples(self, frame_counts, origin=(1, 1)):
        result, state = [], origin
        for _ in range(18):
            result.append(encode(state))
            state = advance(state, frame_counts)
        return result

    def test_real_adapter_pal_ntsc_calibration_and_now_share_units(self):
        lines, expected = [], []
        for video, frame_counts, frame_cpu in ((0, 624 * 32, 808704), (128, 526 * 32, 676962)):
            samples = self.adapter_samples(frame_counts)
            lines.append(f'a {video} 0 ' + ' '.join(map(str, samples)))
            period = (405000 * frame_counts * 65536) // frame_cpu
            expected.append(f'1 {period} {17 * frame_counts} 0 18')
        self.assertEqual(host(lines), expected)

    def test_adapter_failure_paths_and_reset_only_recovery(self):
        values = self.adapter_samples(624 * 32)
        lines = [f'a 0 {scenario} ' + ' '.join(map(str, values))
                 for scenario in (1, 2, 3, 5, 6, 7, 9, 10, 11, 0)]
        results = [list(map(int, line.split())) for line in host(lines)]
        for row in results[:6]:
            self.assertEqual(row[:2], [0, 0])
            self.assertEqual(row[3], 1)
        period = 405000 * 624 * 32 * 65536 // 808704
        for row, calls in zip(results[6:9], (18, 17, 17)):
            self.assertEqual(row, [1, period, 16 * 624 * 32, 1, calls])
        self.assertEqual(results[9], [1, period, 17 * 624 * 32, 0, 18])

    def test_adapter_invalid_raw_and_elapsed_reject(self):
        cases = [self.adapter_samples(624 * 32), [encode((4000, 4000))] * 18]
        cases[0][0] = encode((0, 1))
        rows = host(['a 0 0 ' + ' '.join(map(str, values)) for values in cases])
        for row in rows:
            ok, period, _, fault, _ = map(int, row.split())
            self.assertEqual((ok, period, fault), (0, 0, 1))

    def test_frozen_sampler_interleavings_exclusion_and_attempt_cap(self):
        lines, expected = [], []
        torn = stable((1234, 5678))
        torn[2] ^= 1
        good = stable((4000, 5000))
        for state in ((1, 1), (31, 256), (32, 257), (65519, 2), (256, 1), (257, 65535)):
            after = advance(state, 32)
            for split in range(9):
                reads = stable(state)[:split] + stable(after)[split:]
                bh, bl, bh2, ah, al, ah2, bl2, bh3 = reads
                coherent = bh == bh2 == bh3 and bl == bl2 and ah == ah2 and not (ah == 255 and al >= 240)
                sequence = reads if coherent else reads + good
                lines.append(f'q {len(sequence)} ' + ' '.join(map(str, sequence)))
                if coherent:
                    pair = (ah * 256 + al, bh * 256 + bl)
                    self.assertIn(pair, (state, after))
                    expected.append(f'{encode(pair)} 0 8')
                else:
                    expected.append(f'{encode((4000, 5000))} 0 16')
        for a in range(65520, 65536):
            sequence = stable((a, 42)) + good
            lines.append('q 16 ' + ' '.join(map(str, sequence)))
            expected.append(f'{encode((4000, 5000))} 0 16')
        for sequence, row in ((torn * 31 + good, f'{encode((4000, 5000))} 0 256'),
                              (torn * 32, '0 3 256')):
            lines.append('q 256 ' + ' '.join(map(str, sequence)))
            expected.append(row)
        self.assertEqual(host(lines), expected)

    def test_actual_guard_and_extracted_release_carry(self):
        lines, expected = [], []
        for period in (405000 * 624 * 32 * 65536 // 808704,
                       405000 * 526 * 32 * 65536 // 676962):
            for ticks in (1, 21, 100, 65537):
                release = (MASK - 1024 + (ticks * period // 65536)) & MASK
                fraction = ticks * period % 65536
                for delta in (-1, 0, 1):
                    lines.append(f't {period} {MASK - 1024} {ticks} {(release + delta) & MASK}')
                    expected.append(f'{release} {fraction} {int(delta >= 0)}')
        for now in (1000, MASK - 50):
            for remaining, want in ((119, 0), (120, 0), (121, 100), (65536, 65515), (100000, 65535)):
                lines.append(f'g {now} {(now + remaining) & MASK} 100 20')
                expected.append(str(want))
            for operation, guard in ((0, 20), (100, 0), (65536, 20), (100, MASK)):
                lines.append(f'g {now} {(now + 1000) & MASK} {operation} {guard}')
                expected.append('0')
            lines.append(f'g {now} {(now + 2**31) & MASK} 100 20')
            expected.append('0')
        self.assertEqual(host(lines), expected)

    def test_state_payload_limit(self):
        size, payload = map(int, host(['m'])[0].split())
        self.assertEqual(payload, 10)
        self.assertEqual(size, 12)  # Host ABI only; target padding is unmeasured.


def main():
    paths = ['src/platform/m1/clock_private.h', 'src/platform/m1/m1_platform.c',
             'src/platform/m1/m1_platform.h', 'src/diagnostics/r0f/combined_platform.c',
             'src/diagnostics/r0f/combined_platform.h', 'src/diagnostics/r0f/combined_model.c',
             'src/diagnostics/r0f/combined_model.h', 'interfaces/generated/r0f_combined.h',
             'interfaces/generated/m1_development.h', 'src/platform/m2_rebuild/guard.c',
             'src/platform/m2_rebuild/guard.h', 'src/diagnostics/m2_rebuild/main.c',
             'tests/flight_demo/m2_rebuild/clock_host.c', str(Path(__file__).relative_to(ROOT))]
    sources = {p: {'bytes': len((ROOT / p).read_bytes()),
                   'sha256': sha256((ROOT / p).read_bytes()).hexdigest()} for p in paths}
    for path in paths:
        saved = OUTPUT / 'inputs' / path
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / path, saved)
    combined = (ROOT / 'src/diagnostics/r0f/combined_platform.c').read_text()
    sampler_source = combined[combined.index('uint32_t cfnow(void)'):combined.index('uint32_t cfframe_wait(void)')]
    (OUTPUT / 'sampler.inc').write_text(sampler_source)
    main_source = (ROOT / 'src/diagnostics/m2_rebuild/main.c').read_text()
    release = main_source[main_source.index('uint32_t next ='):main_source.index('if (core.tick == 600u)')]
    (OUTPUT / 'release.inc').write_text(release)
    due = re.search(r'if \(((?:\(uint32_t\))\(now - release\) < 0x80000000UL)\)', main_source)[1]
    (OUTPUT / 'due.inc').write_text('(' + due + ')\n')
    compiler = Path(shutil.which('clang')).resolve()
    version = run([compiler, '--version'])
    args = [compiler, '-std=c11', '-O1', '-Wall', '-Wextra', '-Werror', '-pedantic',
            '-fsanitize=address,undefined', '-fno-omit-frame-pointer',
            '-I' + str(OUTPUT), '-Iinterfaces/generated', '-Isrc/diagnostics/r0f',
            '-Isrc/platform/m1', '-Isrc/platform/m2_rebuild',
            'tests/flight_demo/m2_rebuild/clock_host.c',
            'src/diagnostics/r0f/combined_model.c', 'src/platform/m2_rebuild/guard.c',
            '-o', OUTPUT / 'clock-host']
    success = False
    stream = io.StringIO()
    try:
        run(args)
        result = unittest.TextTestRunner(stream=stream, verbosity=2, failfast=True).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(ClockTests))
        success = result.wasSuccessful()
        (OUTPUT / 'tests.txt').write_text(stream.getvalue())
        print(stream.getvalue(), end='')
    finally:
        report = {'status': 'PASS' if success else 'FAIL', 'sources': sources,
                  'compiler': str(compiler), 'compiler_sha256': sha256(compiler.read_bytes()).hexdigest(),
                  'compiler_version': version, 'commands': COMMANDS,
                  'output': str(OUTPUT), 'target_link_or_execution': False,
                  'host_state_bytes': 12, 'logical_payload_bytes': 10}
        (OUTPUT / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
        print('Retained host evidence:', OUTPUT)
    raise SystemExit(0 if success else 1)


if __name__ == '__main__':
    main()
