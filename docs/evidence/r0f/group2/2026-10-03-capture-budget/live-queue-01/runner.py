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
        'semantics':'Full queue stage 13; reject entity 0,9,255 with only sticky flag change; restore injected flag; model CRC unchanged.'}
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
    helper='''// Version-8 terminal encoding; all acquisition comparisons precede this.
static uint32_t case_crc;
static uint8_t case_tail_byte(uint16_t position, uint8_t absolute)
{
    static const uint8_t prefix[16] = {1u,0u,1u,1u,0u,1u,0u,0u,0u,0u,12u,0u,0u,0u,0u,0u};
    if (position < R0FG2_HEADER_BYTES)
    {
        return r0fg2_identity[position];
    }
    if (position < R0FG2_HEADER_BYTES + 2u * 40u)
    {
        uint8_t epoch = (uint8_t)((position - R0FG2_HEADER_BYTES) / 40u);
        uint8_t index = (uint8_t)((position - R0FG2_HEADER_BYTES) % 40u);
        const uint8_t *observed = r0fg2_queue_observed[epoch];
        if (index >= 16u)
        {
            return index < 28u ? observed[index - 16u] : 0u;
        }
        if (index == 0u) return epoch + 1u;
        if (index == 4u) return epoch;
        if (index == 8u || index == 9u) return observed[index - 8u];
        if (index == 14u) return observed[R0FG2_O_STATUS];
        return prefix[index];
    }
    if (position < R0FG2_CRC_AT) return R0FG2_UNUSED;
    if (position < R0FG2_BLOCK_BYTES)
    {
        return (uint8_t)(~case_crc >> ((position - R0FG2_CRC_AT) * 8u));
    }
    return absolute ^ R0FG1_CAPACITY_PATTERN_XOR;
}

'''
    changed='#include "r0f_group2_capture.h"\n'+original.replace('uint8_t r0fg1_capture_finish(void)',helper+'uint8_t r0fg1_capture_finish(void)')
    changed=changed.replace('    uint16_t tail_left =','    uint16_t case_at = 0u;\n    case_crc = 0xfffffffful;\n    uint16_t tail_left =',1)
    needle='        uint8_t value = (uint8_t)offset;'
    changed=changed.replace(needle,'''        if (case_at < R0FG2_CRC_AT && bytes > R0FG2_CRC_AT - case_at)
        {
            bytes = (uint8_t)(R0FG2_CRC_AT - case_at);
        }
'''+needle)
    changed=changed.replace('record[index] = value++ ^ R0FG1_CAPACITY_PATTERN_XOR;',
        'record[index] = case_tail_byte((uint16_t)(case_at + index), value++);')
    changed=changed.replace('(uint8_t)(value++ ^ R0FG1_CAPACITY_PATTERN_XOR)',
        'case_tail_byte((uint16_t)(case_at + index), value++)')
    # Update the case CRC after byte readback verification; never checksum a
    # damaged readback. Last four CRC bytes are emitted only in the next chunk.
    needle='        crc = r0fs_crc32_update(crc, record, bytes);\n        offset += bytes;'
    changed=changed.replace(needle,'''        if (case_at < R0FG2_CRC_AT)
        {
            case_crc = r0fs_crc32_update(case_crc, record, bytes);
        }
'''+needle+'\n        case_at = (uint16_t)(case_at + bytes);')
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
