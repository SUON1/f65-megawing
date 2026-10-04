#!/usr/bin/env python3
"""Compile-only minimum empty-case capture admission; never constructs a carrier."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from r0f_group2_target_admission import ROOT, sha, section_inventory

BASE = ROOT / 'build/r0f/group2/copy-encoder/r2-b4wd7lrc'


def main():
    baseline = json.loads((BASE / 'result.json').read_text())
    source = BASE / 'source-inputs'
    assert all(sha(source / k) == v for k,v in baseline['inputs'].items())
    parent = ROOT / 'build/r0f/group2/capture-fit'
    parent.mkdir(parents=True, exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix='empty-', dir=parent))
    copied = out / 'source-inputs'
    shutil.copytree(source, copied)
    # Empty block is deliberately NOT a successful case record. A new format
    # version must be admitted with the full reducer before any execution.
    contract = {'id': 'R0FG2-CAPTURE-SKELETON-1', 'blockBytes': 352,
        'headerBytes': 28, 'slots': 8, 'recordBytes': 40, 'crcBytes': 4,
        'used': 0, 'unusedPattern': 165, 'workBytes': 92,
        'status': 'COMPILE_ONLY_NOT_AN_ADMITTED_TRACE_VERSION',
        'inputDigest': sha(BASE / 'result.json')}
    (copied / 'interfaces/r0f_group2_capture_skeleton.json').write_text(json.dumps(contract, indent=2)+'\n')
    header = list(b'G2C1') + [1,40,8,0] + list(bytes.fromhex(contract['inputDigest'])[:16]) + [0,0,0,0]
    text = ('// Generated from r0f_group2_capture_skeleton.json.\n'
        '#ifndef R0FG2_CAPTURE_H\n#define R0FG2_CAPTURE_H\n#include <stdint.h>\n'
        f'#define R0FG2_BLOCK_BYTES {contract["blockBytes"]}u\n'
        f'#define R0FG2_CRC_OFFSET {contract["blockBytes"]-contract["crcBytes"]}u\n'
        f'#define R0FG2_WORK_BYTES {contract["workBytes"]}u\n'
        f'#define R0FG2_UNUSED {contract["unusedPattern"]}u\n'
        'static const uint8_t r0fg2_case_header[] = {' + ','.join(map(str,header)) + '};\n'
        'uint8_t r0fg2_capture_empty(uint32_t *, uint32_t *, uint8_t *);\n#endif\n')
    (copied / 'interfaces/generated/r0f_group2_capture.h').write_text(text)
    relative = 'tools/diagnostics/r0f_group2_capture_skeleton.c'
    shutil.copyfile(ROOT / relative, copied / relative)
    capture = copied / 'src/diagnostics/r0f/group1_capture.c'
    original = capture.read_text()
    needle = '    uint16_t tail_left = (uint16_t)(R0FG1_TRACE_BYTES - 4u - offset);'
    assert original.count(needle) == 1
    capture.write_text('#include "r0f_group2_capture.h"\n' + original.replace(needle,
        '    if (!r0fg2_capture_empty(&offset, &crc, record))\n    {\n        return 0u;\n    }\n' + needle))
    shutil.copyfile(Path(__file__), out / 'runner.py')
    report = {'result':'FAIL','commands':[], 'baseline':str(BASE), 'targetExecuted':False}
    def run(label, command):
        result = subprocess.run(command,cwd=copied,text=True,capture_output=True,timeout=60)
        (out/(label+'.txt')).write_text(result.stdout+result.stderr)
        report['commands'].append({'command':command,'exitCode':result.returncode})
        result.check_returncode()
    try:
        command = next(c['command'].copy() for c in baseline['commands'] if 'mos-mega65-clang' in c['command'][0])
        compiler = Path(command[0])
        assert sha(compiler) == json.loads((ROOT/'toolchain/f65_toolchain.lock.json').read_text())['llvm_mos']['compiler_sha256']
        prg,mapping=out/'EMPTY.prg',out/'EMPTY.map'
        command[command.index('-o')+1]=str(prg)
        command=['-Wl,-Map,'+str(mapping) if c.startswith('-Wl,-Map,') else c for c in command]+[relative]
        run('target-compile',command)
        sections=section_inventory(mapping.read_text())
        end=max(sections[k]['start']+sections[k]['bytes'] for k in ('.r0fs_protected','.text','.rodata','.data','.bss','.noinit'))
        report.update(sections=sections,residentEndExclusive=end,residentFreeBytes=0xc000-end,
                      addedBytes=end-baseline['residentEndExclusive'],prgSha256=sha(prg))
        run('sizes',[str(compiler.parent/'llvm-nm'),'--print-size','--size-sort',str(prg)+'.elf'])
        report['result']='FIT_PASS_NOT_EXECUTABLE' if end<=0xc000 else 'FIT_FAIL'
    except (OSError,subprocess.SubprocessError) as error:
        report['error']=str(error)
    finally:
        report['inputs']={str(p.relative_to(copied)):sha(p) for p in sorted(copied.rglob('*')) if p.is_file()}
        report['baselineUnchanged']=all(sha(source/k)==v for k,v in baseline['inputs'].items())
        report['changedInputs']=[k for k,v in report['inputs'].items() if baseline['inputs'].get(k)!=v]
        (out/'result.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:report.get(k) for k in ('result','residentFreeBytes','addedBytes','error')}));print(out)
    return 0 if report['result']=='FIT_PASS_NOT_EXECUTABLE' else 1

if __name__=='__main__':
    raise SystemExit(main())
