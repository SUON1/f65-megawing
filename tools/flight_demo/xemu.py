"""M1 direct-PRG validation with disposable in-memory virtual boot media.

No D81 or physical/file-backed SD image is opened, copied or created.
"""
import hashlib
import json
from pathlib import Path
import re
import signal
import shutil
import plistlib
import subprocess
import sys
import time

from build import OUT

ROOT = Path(__file__).resolve().parents[2]
XEMU = ROOT / 'toolchain/xemu/xmega65'
ROM = Path('/Users/slice/Documents/Codex/f65-megawing/MEGA65.ROM')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(variant, video):
    assert variant in ('interactive', 'replay', 'slow-render')
    assert video in (0, 1)
    build = json.loads((OUT / 'build.json').read_text())
    assert all(sha(ROOT / p) == h for p, h in build['inputs'].items())
    prg = OUT / variant / 'M1.prg'
    assert sha(prg) == build['targets'][variant]['sha256']
    lock = json.loads((ROOT / 'toolchain/f65_toolchain.lock.json').read_text())
    assert sha(XEMU) == lock['xemu']['binary_sha256']
    assert sha(ROM) == 'af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0'
    destination = OUT / f'xemu-{variant}-{video}-{time.time_ns()}'
    destination.mkdir()
    virtual = destination / 'empty-virtual-media'
    virtual.mkdir()
    # SDL macOS bundles use Contents/Resources as the base directory.
    bundle = destination / 'M1Xemu.app/Contents'
    executable = bundle / 'MacOS/xmega65'
    executable.parent.mkdir(parents=True)
    preferences = bundle / 'Resources/mega65'
    preferences.mkdir(parents=True)
    (preferences / 'prefdir-is-here.txt').write_text('M1 isolated validation\n')
    shutil.copy2(XEMU, executable)
    shutil.copy2(XEMU.parent / 'libSDL2-xemu.dylib', executable.parent)
    (bundle / 'Info.plist').write_bytes(plistlib.dumps({
        'CFBundleIdentifier': 'org.xemu.m1-validation', 'CFBundleName': 'M1 Xemu',
        'CFBundleExecutable': 'xmega65', 'CFBundlePackageType': 'APPL'}))
    # Read-only seed of emulator configuration, not SD content.
    seed = Path.home() / 'Library/Application Support/xemu-lgb/mega65/i2c.bin'
    shutil.copy2(seed, preferences / 'i2c.bin')
    command = [str(executable), '-skipconfigfile', '-fastboot',
               '-besure', '-videostd', str(video), '-rom', str(ROM), '-virtsd', '-sdimg', str(virtual),
               '-prg', str(prg), '-dumpscreen', str(destination / 'screen.txt'),
               '-dumpmem', str(destination / 'memory.bin'),
               '-screenshot', str(destination / 'screen.png')]
    with (destination / 'xemu.log').open('wb') as log:
        process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        print(destination, flush=True)
        try:
            process.wait(timeout=120)
        except subprocess.TimeoutExpired:
            process.send_signal(signal.SIGTERM)
            process.wait(timeout=10)
    report = {'command': command, 'exit': process.returncode, 'prg_sha256': sha(prg),
              'physical': 'NOT RUN', 'i2c_seed_sha256': sha(seed),
              'xemu_sha256': sha(executable),
              'sdl_sha256': sha(executable.parent / 'libSDL2-xemu.dylib'), 'tier': 'direct PRG, virtual in-memory media only',
              'status': 'INCOMPLETE'}
    memory_path = destination / 'memory.bin'
    if memory_path.exists():
        memory = memory_path.read_bytes()
        symbols = (OUT / variant / 'M1.symbols').read_text()
        values = {}
        for name in ['m1_status', 'm1_replay_checksum', 'm1_replay_tick', 'm1_debt_max', 'm1_display_age',
                     'm1_current_tick', 'm1_display_generation', 'm1_source_tick', 'm1_display_store']:
            match = re.search(r'^([0-9a-f]+) ([0-9a-f]+) \w ' + name + '$', symbols, re.M)
            assert match, name
            address, size = [int(x, 16) for x in match.groups()]
            values[name] = int.from_bytes(memory[address:address + size], 'little')
        report['values'] = values
        expected = 0x65a001
        commands = previous = 0
        for tick in range(1, 601):
            held = ((tick - 1) // 25) & 1 if variant != 'interactive' else 0
            commands += held != previous
            previous = held
            expected = (((expected << 5) | (expected >> 27)) & 0xffffffff) ^ tick ^ commands ^ held
        report['expected_checksum'] = expected
        header = (ROOT / 'interfaces/generated/r0f_combined.h').read_text()
        config = json.loads((ROOT / 'interfaces/m1_development.json').read_text())
        result_base = config['memory']['platform_result_start']
        report['stack_bytes'] = {}
        for kind in ('hardware', 'software'):
            offset = int(re.search(r'#define R0FC_O_' + kind.upper() + r'_STACK (\d+)u', header)[1])
            report['stack_bytes'][kind] = int.from_bytes(memory[result_base + offset:result_base + offset + 2], 'little')
        log_text = (destination / 'xemu.log').read_text(errors='replace')
        isolated = 'SDL preferences directory: ' + str(preferences) + '/' in log_text
        report['preferences_isolated'] = isolated
        report['status'] = 'PASS' if (process.returncode == 0 and isolated and values['m1_status'] == 2
            and values['m1_replay_tick'] == 600 and values['m1_replay_checksum'] == expected
            and values['m1_current_tick'] > 600 and values['m1_display_generation'] > 0
            and values['m1_source_tick'] > 0) else 'FAIL'
        report['artifacts'] = {p.name: sha(p) for p in destination.iterdir()
                               if p.is_file() and p.name != 'result.json'}
    (destination / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report), flush=True)
    return report['status'] == 'PASS'


if __name__ == '__main__':
    sys.exit(0 if run(sys.argv[1], int(sys.argv[2])) else 1)
