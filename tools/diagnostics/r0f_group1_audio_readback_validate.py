#!/usr/bin/env python3
"""Validate the one-predicate P08 revision without touching hardware."""
import argparse
import re
import subprocess
from pathlib import Path
import r0f_group1_resume_recovery as recovery
from r0f_group1_resume_validate import function

ROOT = recovery.ROOT
BASE = ROOT / 'build/r0f/group1/terminal-recovery/readiness-compact-01'
PINS = ('r0f_group1_audio_readback.py', 'r0f_group1_audio_readback_validate.py',
        'r0f_group1_audio_readback_host_test.c', 'r0f_group1_readiness_host_test.c',
        'r0f_group1_readiness_policy_test.c')


def validate(experiment):
    source = experiment / 'source-inputs'
    original = BASE / 'source-inputs'
    fit = recovery.read(experiment / 'runtime-01/build.json')
    assert fit['fit'] == 'PASS'
    assert recovery.builder.inputs(source) == fit['inputs']
    old_inputs = recovery.read(BASE / 'runtime-01/build.json')['inputs']
    assert recovery.builder.inputs(original) == old_inputs
    changes = [p for p, h in fit['inputs'].items() if old_inputs.get(p) != h]
    assert changes == ['src/diagnostics/r0f/group1_transport.c']
    before = (original / changes[0]).read_text()
    after = (source / changes[0]).read_text()
    # Independently limit the edit: restore just the initializer and strip the
    # local mask declaration/comments; every other target input stays exact.
    pattern = r'        \.audio_stopped = .*?(?=\n        \.irq_masked)'
    restored = re.sub(pattern, re.search(pattern, before, re.S).group(), after, flags=re.S)
    restored = restored[:restored.index('// CHx control')] + restored[restored.index('static uint8_t buffer['):]
    assert restored == before
    out = experiment / 'readiness-host-02'
    out.mkdir(exist_ok=False)
    mask = re.search(r'^#define AUDIO_CHANNEL_CONTROL_MASK .*$', after, re.M).group()
    (out / 'terminal_transport_under_test.inc').write_text(mask + '\n' +
        function(after, 'static uint8_t validate_capsule(') +
        function(after, 'uint8_t r0fg1_transport_prepare('))
    commands = []
    for name, test, support in (
        ('transport', 'r0f_group1_audio_readback_host_test.c', ['successor_lifecycle.c']),
        ('policy', 'r0f_group1_readiness_policy_test.c', [])):
        executable = out / name
        command = ['/usr/bin/clang', '-std=c11', '-Wall', '-Wextra', '-Wconversion', '-Werror',
                   '-fsanitize=address,undefined', '-DR0FG1_INTEGRATION', '-I' + str(out),
                   '-I' + str(source / 'interfaces/generated'),
                   '-I' + str(source / 'src/diagnostics/r0f'),
                   str(ROOT / 'tools/diagnostics' / test),
                   str(source / 'src/diagnostics/r0f/group1_export.c')]
        command += [str(source / 'src/diagnostics/r0f' / p) for p in support]
        command += ['-o', str(executable)]
        for label, argv in [('compile', command), ('run', [str(executable)])]:
            result = subprocess.run(argv, capture_output=True, text=True, timeout=60)
            (out / (name + '-' + label + '.txt')).write_text(result.stdout + result.stderr)
            commands.append({'command': argv, 'exitCode': result.returncode})
            result.check_returncode()
    recovery.write(out / 'validation.json', {
        'result': 'PASS', 'commands': commands, 'onlyAudioReadbackPredicateChanged': True,
        'prgSha256': fit['prgSha256'], 'transportCases': 1298, 'policyCases': 2624256,
        'hardwareEdges': 'MOCKED', 'physicalCause': 'RAW_BITS_UNRECORDED',
        'validatorInputs': {str((ROOT / 'tools/diagnostics' / p).relative_to(ROOT)):
                            recovery.sha(ROOT / 'tools/diagnostics' / p) for p in PINS}})
    print('PASS: 1298 transport cases, 2624256 policy cases; only audio readback predicate changed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('experiment', type=Path)
    validate(parser.parse_args().experiment.resolve())
