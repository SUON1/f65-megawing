#!/usr/bin/env python3
"""Qualify the copied P07 readiness diagnostic; no SD or hardware actions.

MANDATORY D81 LOADABILITY GATE
Read 00_D81_LOADABILITY_GATE.md and docs/D81_WORKFLOW.md before D81 actions.
The unchanged resume/capacity controllers retain all original gates.
"""
import argparse
from pathlib import Path

import r0f_group1_resume_recovery as recovery

ROOT = recovery.ROOT
OUT = ROOT / 'build/r0f/group1/terminal-recovery/readiness-compact-01'
PINS = ('r0f_group1_readiness.py', 'r0f_group1_readiness.patch',
        'r0f_group1_readiness_validate.py', 'r0f_group1_readiness_host_test.c',
        'r0f_group1_readiness_policy_test.c')


def checked(experiment):
    recovery.OUT = experiment
    recovery.SOURCE = experiment / 'source-inputs'
    recovery.qualify_existing()
    fit = recovery.read(experiment / 'runtime-01/build.json')
    gate = recovery.read(experiment / 'readiness-host-02/validation.json')
    if gate['result'] != 'PASS' or gate['prgSha256'] != fit['prgSha256']:
        raise ValueError('readiness gate missing or stale')
    for path, digest in gate['validatorInputs'].items():
        if recovery.sha(ROOT / path) != digest:
            raise ValueError('readiness validator input drift: ' + path)
    # P06 and all frozen observations stay intact; never use a retired image.
    for name in ('2026-10-02-resume-recovery', '2026-10-02-p06-physical',
                 '2026-10-02-p06-physical/returned', '2026-10-02-terminal-diagnostic',
                 '2026-10-02-terminal-status', '2026-10-03-p07-physical',
                 '2026-10-03-p07-physical/returned', '2026-10-03-readiness-diagnostic'):
        packet = ROOT / 'docs/evidence/r0f/group1' / name
        for relative, digest in recovery.read(packet / 'sha256.json')['files'].items():
            if recovery.sha(packet / relative) != digest:
                raise ValueError('predecessor evidence drift: ' + relative)
    return fit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('verify', 'ntsc', 'pal', 'negative-export',
        'carrier-build', 'carrier-boot', 'carrier-finish'))
    parser.add_argument('--experiment', type=Path, default=OUT)
    parser.add_argument('--name')
    parser.add_argument('--mode', choices=('0', '1'))
    parser.add_argument('--number', type=int, choices=(1, 2))
    args = parser.parse_args()
    fit = checked(args.experiment.resolve())
    if args.action == 'verify':
        print('Terminal diagnostic fit/host/input/preservation gates PASS: ' + fit['prgSha256'])
    elif args.action in ('ntsc', 'pal'):
        recovery.run(args.action, 'G1RDY01.D81')
    elif args.action == 'negative-export':
        recovery.controller().negative_export()
    else:
        if args.name is None:
            parser.error('carrier action requires fresh exact name')
        carrier = recovery.carrier_controller()
        if args.action == 'carrier-build':
            carrier.build(args.name)
            path = carrier.previous.carrier.location(args.name) / 'capacity-admission.json'
            admission = recovery.read(path)
            for name in PINS:
                source = Path(__file__).with_name(name)
                admission['controllerInputs'][str(source.relative_to(ROOT))] = recovery.sha(source)
            admission['readinessGateSha256'] = recovery.sha(
                recovery.OUT / 'readiness-host-02/validation.json')
            recovery.write(path, admission)
        elif args.action == 'carrier-finish':
            carrier.finish(args.name)
        else:
            if args.mode is None or args.number is None:
                parser.error('carrier boot requires mode and fresh-copy number')
            carrier.boot(args.name, args.mode, args.number)


if __name__ == '__main__':
    main()
