#!/usr/bin/env python3
"""Admit empty capture through the existing verified tail traversal."""
import json
from pathlib import Path
import shutil
import zlib

from r0f_group2_experiment import Experiment
from r0f_group2_scratch import function
from r0f_group2_target_admission import ROOT, sha

BASE = ROOT / 'build/r0f/group2/copy-encoder/r2-b4wd7lrc'
CAPTURE = 'src/diagnostics/r0f/group1_capture.c'
CONTRACT = 'interfaces/r0f_group2_capture_skeleton.json'
HEADER = 'interfaces/generated/r0f_group2_capture.h'


def main():
    experiment = Experiment(BASE, 'integrated-capture')
    contract = {'id': 'R0FG2-EMPTY-CAPTURE-2', 'blockBytes': 352,
                'headerBytes': 28, 'slots': 8, 'recordBytes': 40, 'crcBytes': 4,
                'unusedPattern': 165, 'used': 0, 'inputDigest': sha(BASE / 'result.json'),
                'status': 'COMPILE_ONLY_NOT_AN_ADMITTED_TRACE_VERSION'}
    header = b'G2C1' + bytes([1,40,8,0]) + bytes.fromhex(contract['inputDigest'])[:16] + bytes(4)
    block = header + bytes([contract['unusedPattern']]) * (contract['slots'] * contract['recordBytes'])
    crc = zlib.crc32(block).to_bytes(4, 'little')
    text = ('// Generated empty skeleton; no successful observation implied.\n'
            '#ifndef R0FG2_CAPTURE_H\n#define R0FG2_CAPTURE_H\n#include <stdint.h>\n'
            f'#define R0FG2_HEADER_BYTES {len(header)}u\n'
            f'#define R0FG2_CRC_AT {len(block)}u\n'
            f'#define R0FG2_BLOCK_BYTES {len(block)+len(crc)}u\n'
            f'#define R0FG2_UNUSED {contract["unusedPattern"]}u\n'
            'static const uint8_t r0fg2_empty_identity[] = {'
            + ','.join(map(str,header+crc)) + '};\n#endif\n')
    (experiment.source / CONTRACT).write_text(json.dumps(contract, indent=2)+'\n')
    (experiment.source / HEADER).write_text(text)
    capture = experiment.source / CAPTURE
    original = capture.read_text()
    helper = '''// Case encoding shares the existing tail traversal and byte readback check.
// CRC is generated for an empty immutable block only; no live case is claimed.
static uint8_t case_tail_byte(uint16_t position, uint8_t absolute)
{
    if (position < R0FG2_HEADER_BYTES)
    {
        return r0fg2_empty_identity[position];
    }
    if (position < R0FG2_CRC_AT)
    {
        return R0FG2_UNUSED;
    }
    if (position < R0FG2_BLOCK_BYTES)
    {
        return r0fg2_empty_identity[R0FG2_HEADER_BYTES + position - R0FG2_CRC_AT];
    }
    return absolute ^ R0FG1_CAPACITY_PATTERN_XOR;
}

'''
    needle = 'uint8_t r0fg1_capture_finish(void)'
    if original.count(needle) != 1:
        raise ValueError('Capture finish definition mismatch')
    changed = '#include "r0f_group2_capture.h"\n' + original.replace(needle, helper + needle)
    changed = changed.replace('    uint16_t tail_left =', '    uint16_t case_at = 0u;\n    uint16_t tail_left =', 1)
    changed = changed.replace('record[index] = value++ ^ R0FG1_CAPACITY_PATTERN_XOR;',
        'record[index] = case_tail_byte((uint16_t)(case_at + index), value++);')
    changed = changed.replace('(uint8_t)(value++ ^ R0FG1_CAPACITY_PATTERN_XOR)',
        'case_tail_byte((uint16_t)(case_at + index), value++)')
    changed = changed.replace('        tail_left = (uint16_t)(tail_left - bytes);',
        '        case_at = (uint16_t)(case_at + bytes);\n        tail_left = (uint16_t)(tail_left - bytes);')
    capture.write_text(changed)
    # Execute the exact helper and tail statements on the host before target fit.
    begin = changed.index('    uint16_t case_at =')
    end = changed.index('    put32(record, ~crc);', begin)
    host = (experiment.out / 'tail_under_test.h')
    host.write_text(function(changed, 'case_tail_byte') +
        'static uint8_t encode_tail(uint32_t offset)\n{\n    uint32_t crc = 0xfffffffful;\n'
        + changed[begin:end] + '    host_outer_crc = ~crc;\n    return 1u;\n}\n')
    shutil.copyfile(ROOT / 'tools/diagnostics/r0f_group2_tail_host_test.c', experiment.out / 'host_test.c')
    shutil.copyfile(Path(__file__), experiment.out / 'runner.py')
    try:
        experiment.run('host-compile', ['/usr/bin/clang','-std=c11','-Wall','-Wextra','-Werror',
            '-fsanitize=address,undefined','-fno-sanitize-recover=all',
            '-Iinterfaces/generated','-Isrc/diagnostics/r0f','-I'+str(experiment.out),
            str(experiment.out/'host_test.c'), 'src/diagnostics/r0f/successor_lifecycle.c',
            '-o',str(experiment.out/'host')])
        experiment.run('host-run',[str(experiment.out/'host')])
        experiment.fit()
    except Exception as error:
        experiment.report.update(result='FAIL', error=str(error))
    finally:
        experiment.finish([CAPTURE,CONTRACT,HEADER])
    return 0 if experiment.report['result']=='FIT_PASS_NOT_EXECUTABLE' else 1


if __name__ == '__main__':
    raise SystemExit(main())
