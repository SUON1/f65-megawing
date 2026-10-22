"""Run only approved host regressions and static disassembly replay."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent


def main():
    commands = []
    checks = [
        ([sys.executable, '-B', '-m', 'unittest', 'discover', '-s',
          'tests/flight_demo/m2', '-p', 'test_*.py', '-v'], 'regressions.txt'),
        ([sys.executable, '-B', str(PACKET / 'replay.py')], 'replay.txt'),
    ]
    for argv, name in checks:
        assert not (PACKET / name).exists(), 'retain existing run; never overwrite'
        result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
        (PACKET / name).write_text(result.stdout + result.stderr)
        commands.append(dict(argv=argv, exit=result.returncode, log=name))
        (PACKET / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
        print(name, 'exit', result.returncode, flush=True)
        print(result.stdout + result.stderr, flush=True)
        if result.returncode:
            raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
