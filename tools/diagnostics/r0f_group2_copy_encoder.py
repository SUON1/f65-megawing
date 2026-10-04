#!/usr/bin/env python3
"""Measure the approved R2 encoder factoring on a fresh R1 copy."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from r0f_group2_scratch import PREFIX, function
from r0f_group2_target_admission import ROOT, sha, section_inventory

BASE = ROOT / 'build/r0f/group2/scratch/r1-j52fobh4'


def main():
    baseline = json.loads((BASE / 'result.json').read_text())
    source = BASE / 'source-inputs'
    for name, digest in baseline['inputs'].items():
        if sha(source / name) != digest:
            raise ValueError('R1 source mismatch: ' + name)
    parent = ROOT / 'build/r0f/group2/copy-encoder'
    parent.mkdir(parents=True, exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix='r2-', dir=parent))
    copied = out / 'source-inputs'
    shutil.copytree(source, copied)
    header = copied / PREFIX / 'group2_copy.h'
    header.write_text('''// Private synchronous foreground PF encoder; callers retain admission policy.
#ifndef R0FG2_COPY_H
#define R0FG2_COPY_H
#include <stdint.h>
uint8_t r0fg2_copy(uint32_t source, uint32_t destination, uint8_t bytes);
#endif
''')
    helper = '''// One PF request encoder. Ordinary C ABI; canonical B=2; no MAP/DMA.
// Foreground only. PF owns synchronous physical access and register restoration.
__attribute__((noinline))
uint8_t r0fg2_copy(uint32_t source, uint32_t destination, uint8_t bytes)
{
    for (uint8_t index = 0u; index < 4u; index++)
    {
        r0f_pf_copy_request[index] = (uint8_t)(source >> (index * 8u));
        r0f_pf_copy_request[4u + index] = (uint8_t)(destination >> (index * 8u));
    }
    r0f_pf_copy_request[8] = bytes;
    return r0f_pf_flat_copy();
}
'''
    platform_path = copied / PREFIX / 'combined_platform.c'
    platform = platform_path.read_text()
    old = function(platform, 'cfcopy').rstrip()
    new = old.replace('uint32_t a,b;uint8_t i;', 'uint32_t a,b;')
    begin = new.index('  for(i=0u;')
    end = new.index('if(!r0f_pf_flat_copy())')
    new = new[:begin] + '  ' + new[end:].replace('r0f_pf_flat_copy()', 'r0fg2_copy(a,b,n)', 1)
    platform = '#include "group2_copy.h"\n' + platform.replace(old, helper + new)
    platform_path.write_text(platform)
    integration_path = copied / PREFIX / 'successor_integration.c'
    integration = integration_path.read_text()
    old = function(integration, 'fixed_physical_copy').rstrip()
    new = '''static uint8_t fixed_physical_copy(uint32_t source, uint32_t destination,
                                   uint8_t length)
{
    return r0fg2_copy(source, destination, length);
}'''
    integration_path.write_text('#include "group2_copy.h"\n' + integration.replace(old, new))
    transport_path = copied / PREFIX / 'group1_transport.c'
    transport = transport_path.read_text()
    old = function(transport, 'transfer').rstrip()
    begin = old.index('    for (uint8_t index')
    new = old[:begin] + '''    return r0fg2_copy(write ? local : base + offset,
                      write ? base + offset : local, bytes);
}'''
    transport_path.write_text('#include "group2_copy.h"\n' + transport.replace(old, new))
    # Reuse R1's actual-owner tests, replacing only the three changed definitions.
    definitions = (BASE / 'host-review-67eoxd_e/actual_owners.h').read_text()
    for name, text in [('cfcopy', platform), ('fixed_physical_copy', integration_path.read_text()),
                       ('transfer', transport_path.read_text())]:
        definitions = definitions.replace(function(definitions, name), function(text, name))
    (out / 'actual_owners.h').write_text(helper + definitions)
    shutil.copyfile(ROOT / 'tools/diagnostics/r0f_group2_scratch_host_test.c', out / 'host_test.c')
    shutil.copyfile(Path(__file__), out / 'runner.py')
    report = {'result': 'FAIL', 'baseline': str(BASE), 'commands': [], 'targetExecuted': False}

    def run(label, command):
        result = subprocess.run(command, cwd=copied, text=True, capture_output=True, timeout=60)
        (out / (label + '.txt')).write_text(result.stdout + result.stderr)
        report['commands'].append({'command': command, 'exitCode': result.returncode})
        result.check_returncode()

    try:
        run('host-compile', ['/usr/bin/clang', '-std=c11', '-Wall', '-Wextra', '-Werror',
            '-fsanitize=address,undefined', '-fno-sanitize-recover=all',
            '-Iinterfaces/generated', '-I' + PREFIX, '-I' + str(out), str(out / 'host_test.c'),
            PREFIX + 'combined_model.c', PREFIX + 'successor_lifecycle.c',
            PREFIX + 'group1_export.c', '-o', str(out / 'host')])
        run('host-run', [str(out / 'host')])
        command = next(c['command'].copy() for c in baseline['commands']
                       if 'mos-mega65-clang' in c['command'][0])
        compiler = Path(command[0])
        lock = json.loads((ROOT / 'toolchain/f65_toolchain.lock.json').read_text())
        if sha(compiler) != lock['llvm_mos']['compiler_sha256']:
            raise ValueError('Compiler mismatch')
        prg, mapping = out / 'R2.prg', out / 'R2.map'
        command[command.index('-o') + 1] = str(prg)
        command = ['-Wl,-Map,' + str(mapping) if c.startswith('-Wl,-Map,') else c for c in command]
        run('target-compile', command)
        sections = section_inventory(mapping.read_text())
        end = max(sections[k]['start'] + sections[k]['bytes'] for k in
                  ('.r0fs_protected', '.text', '.rodata', '.data', '.bss', '.noinit'))
        report.update(sections=sections, residentEndExclusive=end, residentFreeBytes=0xc000-end,
                      recoveredBytes=baseline['residentEndExclusive']-end, prgSha256=sha(prg))
        for key in ('.bss', '.data', '.rodata', '.noinit'):
            if sections[key]['bytes'] != baseline['sections'][key]['bytes']:
                raise ValueError('Allocation changed: ' + key)
        if sections['.r0fs_protected'] != baseline['sections']['.r0fs_protected']:
            raise ValueError('Protected region changed')
        run('sizes', [str(compiler.parent / 'llvm-nm'), '--print-size', '--size-sort', str(prg)+'.elf'])
        run('disassembly', [str(compiler.parent / 'llvm-objdump'), '-d', str(prg)+'.elf'])
        report['result'] = 'FIT_PASS_NOT_EXECUTABLE' if end <= 0xc000 and report['recoveredBytes'] >= 0 else 'FIT_FAIL'
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        report['error'] = str(error)
    finally:
        report['inputs'] = {str(p.relative_to(copied)): sha(p) for p in sorted(copied.rglob('*')) if p.is_file()}
        report['changedInputs'] = [k for k,v in report['inputs'].items() if baseline['inputs'].get(k) != v]
        report['baselineUnchanged'] = all(sha(source / k) == v for k,v in baseline['inputs'].items())
        expected = {PREFIX + name for name in ('combined_platform.c', 'successor_integration.c', 'group1_transport.c', 'group2_copy.h')}
        if not report['baselineUnchanged'] or set(report['changedInputs']) != expected:
            report.update(result='FAIL', error='Unexpected source delta')
        (out / 'result.json').write_text(json.dumps(report, indent=2)+'\n')
        print(json.dumps({k:report.get(k) for k in ('result','residentFreeBytes','recoveredBytes','error')}))
        print(out)
    return 0 if report['result'] == 'FIT_PASS_NOT_EXECUTABLE' else 1


if __name__ == '__main__':
    raise SystemExit(main())
