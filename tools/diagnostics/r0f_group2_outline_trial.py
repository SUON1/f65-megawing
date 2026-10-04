#!/usr/bin/env python3
"""One approved compile-only outlining experiment on the retained admission."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from r0f_group2_target_admission import ROOT, sha, section_inventory

BASE = ROOT / 'build/r0f/group2/target-admission/queue-ceu0y7ys'
CHOICES = {
    'frame-wait': ('src/diagnostics/r0f/combined_platform.c',
                   'uint32_t cfframe_wait(void)'),
    'ratio': ('src/diagnostics/r0f/combined_model.c',
              'uint32_t cfratio(uint32_t a,uint32_t b,uint32_t d,uint8_t shift)'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('helper', choices=CHOICES)
    args = parser.parse_args()
    baseline = json.loads((BASE / 'admission.json').read_text())
    source = BASE / 'source-inputs'
    for name, expected in baseline['inputs'].items():
        if sha(source / name) != expected:
            raise ValueError('Admission input mismatch: ' + name)
    parent = ROOT / 'build/r0f/group2/outline'
    parent.mkdir(parents=True, exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix=args.helper + '-', dir=parent))
    copied = out / 'source-inputs'
    shutil.copytree(source, copied)
    name, signature = CHOICES[args.helper]
    path = copied / name
    original = path.read_text()
    if original.count(signature) != 1:
        raise ValueError('Ambiguous function signature')
    replacement = '__attribute__((noinline)) ' + signature
    path.write_text(original.replace(signature, replacement, 1))
    assert path.read_text().replace(replacement, signature, 1) == original
    report = {'result': 'FAIL', 'helper': args.helper, 'baseline': str(BASE),
              'bodyUnchanged': True, 'targetExecuted': False, 'commands': [],
              'xemu': 'NOT RUN', 'physical': 'NOT RUN', 'carrier': 'NOT BUILT',
              'runnerSha256': sha(Path(__file__).resolve())}

    def run(label, command):
        result = subprocess.run(command, cwd=copied, text=True,
                                capture_output=True, timeout=60)
        (out / (label + '.txt')).write_text(result.stdout + result.stderr)
        report['commands'].append({'command': command, 'exitCode': result.returncode})
        result.check_returncode()

    try:
        command = next(item['command'].copy() for item in baseline['commands']
                       if 'mos-mega65-clang' in item['command'][0])
        compiler = Path(command[0])
        lock = json.loads((ROOT / 'toolchain/f65_toolchain.lock.json').read_text())
        if sha(compiler) != lock['llvm_mos']['compiler_sha256']:
            raise ValueError('Compiler identity mismatch')
        prg = out / 'ADMISSION.prg'
        mapping = out / 'ADMISSION.map'
        command[command.index('-o') + 1] = str(prg)
        command = ['-Wl,-Map,' + str(mapping) if item.startswith('-Wl,-Map,')
                   else item for item in command]
        run('compile', command)
        sections = section_inventory(mapping.read_text())
        end = max(sections[key]['start'] + sections[key]['bytes'] for key in
                  ('.r0fs_protected', '.text', '.rodata', '.data', '.bss', '.noinit'))
        if sections['.r0fs_protected'] != baseline['sections']['.r0fs_protected']:
            raise ValueError('Protected section changed')
        for key in ('.bss', '.data', '.noinit'):
            if sections[key]['bytes'] != baseline['sections'][key]['bytes']:
                raise ValueError('State allocation changed: ' + key)
        run('sizes', [str(compiler.parent / 'llvm-nm'), '--print-size', '--size-sort',
                      str(prg) + '.elf'])
        run('disassembly', [str(compiler.parent / 'llvm-objdump'), '-d',
                            '--print-imm-hex', str(prg) + '.elf'])
        report.update(sections=sections, residentEndExclusive=end,
                      residentFreeBytes=0xc000-end,
                      recoveredBytes=baseline['residentEndExclusive']-end,
                      prgSha256=sha(prg),
                      result='FIT_PASS_NOT_EXECUTABLE' if end <= 0xc000 else 'FIT_FAIL')
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        report['error'] = str(error)
    finally:
        report['inputs'] = {str(p.relative_to(copied)): sha(p)
                            for p in sorted(copied.rglob('*')) if p.is_file()}
        report['changedInputs'] = [key for key, value in report['inputs'].items()
                                   if baseline['inputs'].get(key) != value]
        report['baselineUnchanged'] = all(sha(source / key) == value
                                          for key, value in baseline['inputs'].items())
        if report['changedInputs'] != [name] or not report['baselineUnchanged']:
            report['result'] = 'FAIL'
            report['error'] = 'Unexpected source or baseline change'
        (out / 'trial.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps({key: report.get(key) for key in
                         ('result', 'residentFreeBytes', 'recoveredBytes', 'error')}))
        print(out)
    return 0 if report['result'] == 'FIT_PASS_NOT_EXECUTABLE' else 1


if __name__ == '__main__':
    raise SystemExit(main())
