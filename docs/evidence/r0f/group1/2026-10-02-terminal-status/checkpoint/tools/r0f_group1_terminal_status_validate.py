#!/usr/bin/env python3
"""Verify terminal markers without changing the candidate or relaxing guards."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from r0f_group1_resume_validate import function

ROOT = Path(__file__).resolve().parents[2]


def validate(experiment):
    source = experiment / 'source-inputs'
    baseline = ROOT / 'build/r0f/group1/resume-recovery/clock-03-execution/source-inputs'
    out = experiment / 'terminal-status-host'
    out.mkdir(exist_ok=False)
    # Remove only observational marker calls/comments. Executable predicates
    # and boolean returns must be exactly the qualified P06 token stream.
    tokens = lambda text: re.sub(r'//[^\n]*', '', text).split()
    for name in ('group1_capture.c', 'group1_transport.c'):
        relative = Path('src/diagnostics/r0f') / name
        current = (source / relative).read_text().replace('    r0fg1_terminal_checkpoint();\n', '')
        assert tokens(current) == tokens((baseline / relative).read_text()), name
    disassembly = (experiment / 'runtime-01-disassembly.txt').read_text()
    symbols = (experiment / 'runtime-01-symbols.txt').read_text()
    address = int(re.search(r'^(\w+) \w r0fg1_export_status$', symbols, re.M)[1], 16)
    assert len(re.findall(r'\binc\s+\$' + f'{address:x}' + r'\b', disassembly)) == 4
    prg = (experiment / 'runtime-01/GROUP1.prg').read_bytes()
    load = int.from_bytes(prg[:2], 'little')
    assert prg[2 + address - load] == 0x6b
    text = (source / 'src/diagnostics/r0f/group1_transport.c').read_text()
    (out / 'terminal_transport_under_test.inc').write_text(
        function(text, 'static uint8_t validate_capsule(')
        + function(text, 'uint8_t r0fg1_transport_prepare('))
    executable = out / 'transport-host'
    command = ['/usr/bin/clang', '-std=c11', '-Wall', '-Wextra', '-Wconversion', '-Werror',
        '-fsanitize=address,undefined', '-DR0FG1_INTEGRATION', '-I' + str(out),
        '-I' + str(source / 'interfaces/generated'), '-I' + str(source / 'src/diagnostics/r0f'),
        str(ROOT / 'tools/diagnostics/r0f_group1_terminal_status_host_test.c'),
        str(source / 'src/diagnostics/r0f/group1_export.c'),
        str(source / 'src/diagnostics/r0f/successor_lifecycle.c'), '-o', str(executable)]
    commands = []
    for label, argv in [('compile', command), ('run', [str(executable)])]:
        result = subprocess.run(argv, capture_output=True, text=True, timeout=60)
        (out / (label + '.txt')).write_text(result.stdout + result.stderr)
        commands.append({'command': argv, 'exitCode': result.returncode})
        result.check_returncode()
    report = {'result': 'PASS', 'commands': commands, 'guardTokenEquivalence': 'PASS',
        'targetAbsoluteIncrements': 4, 'initialMarker': '6B', 'prgSha256': hashlib.sha256(prg).hexdigest(),
        'physicalCause': 'UNKNOWN', 'hardwareEdges': 'MOCKED', 'sdWrites': False}
    (out / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Terminal guard equivalence, emitted INC markers and 17 sanitizer transport cases PASS')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('experiment', type=Path)
    args = parser.parse_args()
    validate(args.experiment.resolve())
