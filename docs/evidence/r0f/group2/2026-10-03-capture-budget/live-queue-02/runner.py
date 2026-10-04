#!/usr/bin/env python3
"""Fresh live G2-Q variant with versioned case encoding and fit gates."""
import json
from pathlib import Path
import shutil

from r0f_group2_experiment import Experiment
from r0f_group2_scratch import function
from r0f_group2_target_admission import ROOT, sha

BASE = ROOT / 'build/r0f/group2/copy-encoder/r2-b4wd7lrc'
CAPTURE = 'src/diagnostics/r0f/group1_capture.c'
CONTRACT = 'interfaces/r0f_group2_capture_contract.json'
HEADER = 'interfaces/generated/r0f_group2_capture.h'
PROBE = 'tools/diagnostics/r0f_group2_queue_probe.c'
MODEL = 'src/diagnostics/r0f/combined_model.c'
INTEGRATION = 'src/diagnostics/r0f/successor_integration.c'


def configure(experiment):
    contract = {'id':'R0FG2-CASES-1', 'traceVersion':8, 'caseId':1, 'family':1,
        'subcase':1, 'blockBytes':352, 'headerBytes':28, 'recordBytes':40, 'slots':8,
        'observations':2, 'payloadBytes':12, 'unusedPattern':165,
        'checkMask':15, 'harnessFault':114,
        'payloadOffsets':{'TICK':0,'STATUS':2,'CHECKS':3,'BEFORE':4,'AFTER':8},
        'ticks':[1,1601], 'inputDigest':sha(BASE/'result.json'),
        'semantics':'Full queue stage 13; reject entity 0,9,255 with only sticky flag change; restore injected flag; whole-model CRC unchanged after all three rejections.'}
    (experiment.source/CONTRACT).write_text(json.dumps(contract,indent=2)+'\n')
    header = b'G2C1' + bytes([1,40,8,2]) + bytes.fromhex(contract['inputDigest'])[:16] + bytes([1,0,0,0])
    text = ('// Generated from private r0f_group2_capture_contract.json.\n'
        '#ifndef R0FG2_CAPTURE_H\n#define R0FG2_CAPTURE_H\n#include <stdint.h>\n')
    for name,value in [('HEADER_BYTES',28),('CRC_AT',348),('BLOCK_BYTES',352),
                       ('UNUSED',165),('OBSERVATIONS',2),('PAYLOAD_BYTES',12),('HARNESS_FAULT',114)]:
        text += f'#define R0FG2_{name} {value}u\n'
    for name,value in contract['payloadOffsets'].items():
        text += f'#define R0FG2_O_{name} {value}u\n'
    text += ('static const uint8_t r0fg2_identity[] = {'+','.join(map(str,header))+'};\n'
        'extern uint8_t r0fg2_queue_observed[R0FG2_OBSERVATIONS][R0FG2_PAYLOAD_BYTES];\n'
        'void r0fg2_queue_live(struct_unused *);\n#endif\n').replace('void r0fg2_queue_live(struct_unused *);\n','')
    (experiment.source/HEADER).write_text(text)
    shutil.copyfile(ROOT/'tools/diagnostics/r0f_group2_live_queue.c',experiment.source/PROBE)
    integration=experiment.source/INTEGRATION
    integration.write_text(integration.read_text().replace('extern uint8_t r0fg2_queue_probe(r0fc_model *model);\nstatic volatile uint8_t group2_admission_result;\n','').replace('    group2_admission_result = r0fg2_queue_probe(&model);\n',''))
    model=experiment.source/MODEL
    source=model.read_text().replace('extern void cfinput_tick(uint8_t state);','extern void cfinput_tick(uint8_t state);\nextern void r0fg2_queue_live(r0fc_model *model);')
    needle='for(i=0u;i<R0FC_QUEUE_CAPACITY;++i)(void)r0fc_event(m,(uint8_t)(i%9u));'
    if source.count(needle)!=1:raise ValueError('Queue pressure seam mismatch')
    source=source.replace(needle,needle+'\n#ifdef R0FG1_INTEGRATION\n      if(m->tick==1u||m->tick==1601u)r0fg2_queue_live(m);\n#endif')
    model.write_text(source)
    capture=experiment.source/CAPTURE
    original=capture.read_text()
    helper='// Version-8 case block; encode one bounded chunk with the existing workspace.\nstatic void case_record(uint8_t *out, uint8_t epoch)\n{\n    for (uint8_t index = 0u; index < 40u; index++) out[index] = 0u;\n    out[0] = epoch + 1u;\n    out[2] = 1u;\n    out[3] = 1u;\n    out[4] = epoch;\n    out[5] = 1u;\n    out[8] = r0fg2_queue_observed[epoch][R0FG2_O_TICK];\n    out[9] = r0fg2_queue_observed[epoch][R0FG2_O_TICK + 1u];\n    out[10] = R0FG2_PAYLOAD_BYTES;\n    out[14] = r0fg2_queue_observed[epoch][R0FG2_O_STATUS];\n    for (uint8_t index = 0u; index < R0FG2_PAYLOAD_BYTES; index++)\n    {\n        out[16u + index] = r0fg2_queue_observed[epoch][index];\n    }\n}\n\n'
    changed='#include "r0f_group2_capture.h"\n'+original.replace('uint8_t r0fg1_capture_finish(void)',helper+'uint8_t r0fg1_capture_finish(void)')
    begin=changed.index('    uint16_t tail_left =')
    end=changed.index('    put32(record, ~crc);',begin)
    tail='    uint16_t case_at = 0u;\n    uint32_t case_crc = 0xfffffffful;\n    uint16_t tail_left = (uint16_t)(R0FG1_TRACE_BYTES - 4u - offset);\n    while (tail_left)\n    {\n        uint8_t bytes = tail_left > sizeof(record) ? sizeof(record) : (uint8_t)tail_left;\n        uint8_t value = (uint8_t)offset;\n        if (case_at == 0u)\n        {\n            bytes = R0FG2_HEADER_BYTES;\n            for (uint8_t index = 0u; index < bytes; index++) record[index] = r0fg2_identity[index];\n        }\n        else if (case_at == 28u || case_at == 68u)\n        {\n            bytes = 40u;\n            case_record(record, case_at == 28u ? 0u : 1u);\n        }\n        else if (case_at < R0FG2_CRC_AT)\n        {\n            if (bytes > R0FG2_CRC_AT - case_at) bytes = (uint8_t)(R0FG2_CRC_AT - case_at);\n            for (uint8_t index = 0u; index < bytes; index++) record[index] = R0FG2_UNUSED;\n        }\n        else if (case_at == R0FG2_CRC_AT)\n        {\n            bytes = 4u;\n            put32(record, ~case_crc);\n        }\n        else\n        {\n            for (uint8_t index = 0u; index < bytes; index++)\n            {\n                record[index] = value++ ^ R0FG1_CAPACITY_PATTERN_XOR;\n            }\n        }\n        uint32_t expected = r0fs_crc32(record, bytes);\n        if (!r0fg1_trace_write(offset, record, bytes)\n            || !r0fg1_trace_read(offset, record, bytes)\n            || r0fs_crc32(record, bytes) != expected)\n        {\n            return 0u;\n        }\n        // Pattern bytes keep their original independent byte comparison too.\n        if (case_at >= R0FG2_BLOCK_BYTES)\n        {\n            value = (uint8_t)offset;\n            for (uint8_t index = 0u; index < bytes; index++)\n            {\n                if (record[index] != (uint8_t)(value++ ^ R0FG1_CAPACITY_PATTERN_XOR)) return 0u;\n            }\n        }\n        if (case_at < R0FG2_CRC_AT) case_crc = r0fs_crc32_update(case_crc, record, bytes);\n        crc = r0fs_crc32_update(crc, record, bytes);\n        offset += bytes;\n        case_at = (uint16_t)(case_at + bytes);\n        tail_left = (uint16_t)(tail_left - bytes);\n    }\n'
    changed=changed[:begin]+tail+changed[end:]
    capture.write_text(changed)
    # Update only this copied trace contract and its generated constants.
    trace_contract='interfaces/r0f_group1_trace_contract.json'
    trace=json.loads((experiment.source/trace_contract).read_text())
    trace['id']='R0FG2-TRACE-8';trace['constants']['VERSION']=8
    trace['group2Contract']=CONTRACT
    trace['encoding']+=' Version 8 inserts the generated 352-byte Group 2 case block after real world events and before the remaining capacity tail; all prior capacities and comparisons remain.'
    (experiment.source/trace_contract).write_text(json.dumps(trace,indent=2)+'\n')
    generated='interfaces/generated/r0f_group1_trace.h'
    p=experiment.source/generated;p.write_text(p.read_text().replace('#define R0FG1_VERSION 7u','#define R0FG1_VERSION 8u'))
    return contract, changed, [CAPTURE,CONTRACT,HEADER,PROBE,MODEL,INTEGRATION,trace_contract,generated]


def main():
    experiment=Experiment(BASE,'live-queue')
    contract,changed,allowed=configure(experiment)
    shutil.copyfile(Path(__file__),experiment.out/'runner.py')
    try:
        # Fit first: only a fitting complete variant proceeds to execution gates.
        experiment.fit()
    except Exception as error:
        experiment.report.update(result='FAIL',error=str(error))
    finally:
        experiment.finish(allowed)
    return 0 if experiment.report['result']=='FIT_PASS_NOT_EXECUTABLE' else 1

if __name__=='__main__':
    raise SystemExit(main())
