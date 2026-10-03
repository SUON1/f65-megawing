#!/usr/bin/env python3
"""P08 audio readback correction through the unchanged qualified carrier gates.

MANDATORY D81 LOADABILITY GATE: read 00_D81_LOADABILITY_GATE.md and
 docs/D81_WORKFLOW.md. No SD or physical actions are provided here.
"""
import r0f_group1_readiness as predecessor
import r0f_group1_audio_readback_validate as validation

OUT = predecessor.ROOT / 'build/r0f/group1/terminal-recovery/audio-readback-01'
previous_checked = predecessor.checked


def checked(experiment):
    fit = previous_checked(experiment)
    for name in ('2026-10-03-readiness-compact', '2026-10-03-p08-physical'):
        packet = predecessor.ROOT / 'docs/evidence/r0f/group1' / name
        for path, digest in predecessor.recovery.read(packet / 'sha256.json')['files'].items():
            if predecessor.recovery.sha(packet / path) != digest:
                raise ValueError('P08 preservation drift: ' + path)
    return fit


if __name__ == '__main__':
    predecessor.OUT = OUT
    predecessor.PINS = validation.PINS
    predecessor.checked = checked
    predecessor.main()
