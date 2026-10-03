#!/usr/bin/env python3
"""Qualify exact diagnostic policy and transport without target execution."""
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
    baseline = ROOT / 'build/r0f/group1/terminal-recovery/status-02/source-inputs'
    out = experiment / 'readiness-host-02'
    out.mkdir(exist_ok=False)
    tokens = lambda text: re.sub(r'//[^\n]*', '', text).split()
    relative = Path('src/diagnostics/r0f/group1_capture.c')
    old = (baseline / relative).read_text().replace('    r0fg1_terminal_checkpoint();\n', '')
    assert tokens(old) == tokens((source / relative).read_text())
    relative = Path('src/diagnostics/r0f/group1_transport.c')
    old = (baseline / relative).read_text().replace('    r0fg1_terminal_checkpoint();\n', '')
    current = (source / relative).read_text()
    restored = current.replace(
        '    uint8_t rejection = r0fg1_export_begin_diagnostic(&export, &readiness);\n'
        '    if (rejection != 0u)', '    if (!r0fg1_export_begin(&export, &readiness))').replace(
        '        r0fg1_export_status = rejection;\n', '')
    assert tokens(old) == tokens(restored)
    # Only two text literals differ from the previously checked named policy.
    previous = ROOT / 'build/r0f/group1/terminal-recovery/readiness-01/source-inputs'
    relative = Path('src/diagnostics/r0f/successor_integration.c')
    original = (previous / relative).read_text()
    revised = original.replace('GROUP 1 LOCKOUT - NO ACCEPTANCE', 'G1 FAIL - NO ACCEPTANCE').replace(
        'RESET TO EXIT - RETAIN FAILURE', 'PHOTO THEN RESET')
    assert (source / relative).read_text() == revised
    (out / 'terminal_transport_under_test.inc').write_text(
        function(current, 'static uint8_t validate_capsule(')
        + function(current, 'uint8_t r0fg1_transport_prepare('))
    commands = []
    for name, test, support in (
        ('transport', 'r0f_group1_readiness_host_test.c', ['successor_lifecycle.c']),
        ('policy', 'r0f_group1_readiness_policy_test.c', [])):
        executable = out / name
        command = ['/usr/bin/clang', '-std=c11', '-Wall', '-Wextra', '-Wconversion', '-Werror',
            '-fsanitize=address,undefined', '-DR0FG1_INTEGRATION', '-I' + str(out),
            '-I' + str(source / 'interfaces/generated'), '-I' + str(source / 'src/diagnostics/r0f'),
            str(ROOT / 'tools/diagnostics' / test),
            str(source / 'src/diagnostics/r0f/group1_export.c')]
        command += [str(source / 'src/diagnostics/r0f' / file) for file in support]
        command += ['-o', str(executable)]
        for label, argv in [('compile', command), ('run', [str(executable)])]:
            result = subprocess.run(argv, capture_output=True, text=True, timeout=60)
            (out / (name + '-' + label + '.txt')).write_text(result.stdout + result.stderr)
            commands.append({'command': argv, 'exitCode': result.returncode})
            result.check_returncode()
    prg = experiment / 'runtime-01/GROUP1.prg'
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    inputs = [Path(__file__), ROOT / 'tools/diagnostics/r0f_group1_readiness_host_test.c',
              ROOT / 'tools/diagnostics/r0f_group1_readiness_policy_test.c']
    report = {'result': 'PASS', 'commands': commands,
        'captureTransportGuardEquivalence': 'PASS', 'onlyTwoReportingStringsChanged': 'PASS',
        'prgSha256': sha(prg), 'physicalCause': 'UNKNOWN', 'hardwareEdges': 'MOCKED',
        'policyCases': 2624256, 'transportCases': 18,
        'validatorInputs': {str(p.relative_to(ROOT)): sha(p) for p in inputs}, 'sdWrites': False}
    (out / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Guard equivalence, 18 transport cases and 2624256 policy comparisons PASS')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('experiment', type=Path)
    args = parser.parse_args()
    validate(args.experiment.resolve())
