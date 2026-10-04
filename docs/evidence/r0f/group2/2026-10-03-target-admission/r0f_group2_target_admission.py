#!/usr/bin/env python3
"""One fresh compile-only P09-derived queue probe. Never executes target output."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from r0f_successor_integration import section_inventory

ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / 'docs/evidence/r0f/group1/2026-10-03-audio-readback'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    baseline = json.loads((PACKET / 'experiment/build.json').read_text())
    source = Path(baseline['sourceRoot'])
    # The retained packet indexes large local-only inputs at this frozen root.
    for name, digest in baseline['inputs'].items():
        if sha(source / name) != digest:
            raise ValueError('Frozen source mismatch: ' + name)
    parent = ROOT / 'build/r0f/group2/target-admission'
    parent.mkdir(parents=True, exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix='queue-', dir=parent))
    copied = out / 'source-inputs'
    shutil.copytree(source, copied)
    probe = Path('tools/diagnostics/r0f_group2_queue_probe.c')
    shutil.copyfile(ROOT / probe, copied / probe)
    integration = copied / 'src/diagnostics/r0f/successor_integration.c'
    content = integration.read_text()
    needle = '    r0fc_reset(&model);\n'
    if content.count(needle) != 1:
        raise ValueError('Ambiguous admission insertion')
    content = content.replace(needle, needle +
        '    group2_admission_result = r0fg2_queue_probe(&model);\n')
    content = content.replace('static r0fc_model model;',
        'static r0fc_model model;\n'
        'extern uint8_t r0fg2_queue_probe(r0fc_model *model);\n'
        'static volatile uint8_t group2_admission_result;')
    integration.write_text(content)
    report = {'result': 'FAIL', 'targetExecuted': False, 'carrier': 'NOT BUILT',
              'physical': 'NOT RUN', 'scope': 'G2-Q minimal admission only',
              'baselinePrgSha256': baseline['prgSha256'], 'commands': []}

    def run(label, command):
        result = subprocess.run(command, cwd=copied, text=True,
                                capture_output=True, timeout=60)
        (out / (label + '.txt')).write_text(result.stdout + result.stderr)
        report['commands'].append({'command': command, 'exitCode': result.returncode})
        result.check_returncode()

    try:
        command = baseline['command'].copy()
        compiler = Path(command[0])
        lock = json.loads((ROOT / 'toolchain/f65_toolchain.lock.json').read_text())
        if sha(compiler) != lock['llvm_mos']['compiler_sha256']:
            raise ValueError('Pinned compiler mismatch')
        native = out / 'probe-host'
        run('host-compile', ['/usr/bin/clang', '-std=c11', '-Wall', '-Wextra',
            '-Werror', '-fsanitize=address,undefined', '-fno-sanitize-recover=all',
            '-Iinterfaces/generated', '-Isrc/diagnostics/r0f',
            'src/diagnostics/r0f/combined_model.c',
            'src/diagnostics/r0f/successor_lifecycle.c', str(probe),
            str(ROOT / 'tools/diagnostics/r0f_group2_queue_probe_host_test.c'),
            '-o', str(native)])
        run('host-run', [str(native)])
        prg = out / 'ADMISSION.prg'
        mapping = out / 'ADMISSION.map'
        command[command.index('-o') + 1] = str(prg)
        command = ['-Wl,-Map,' + str(mapping) if item.startswith('-Wl,-Map,')
                   else item for item in command]
        command.append(str(probe))
        run('target-compile', command)
        sections = section_inventory(mapping.read_text())
        end = max(sections[name]['start'] + sections[name]['bytes'] for name in
                  ('.r0fs_protected', '.text', '.rodata', '.data', '.bss', '.noinit'))
        report.update(sections=sections, residentEndExclusive=end,
                      residentFreeBytes=0xc000-end,
                      addedBytes=end-baseline['residentEndExclusive'],
                      result='FIT_PASS_NOT_EXECUTABLE' if end <= 0xc000 else 'FIT_FAIL')
        run('sizes', [str(compiler.parent / 'llvm-nm'), '--print-size', '--size-sort',
                      str(prg) + '.elf'])
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        report['error'] = str(error)
    finally:
        report['inputs'] = {str(p.relative_to(copied)): sha(p)
                            for p in sorted(copied.rglob('*')) if p.is_file()}
        report['frozenInputsUnchanged'] = all(
            sha(source / name) == digest for name, digest in baseline['inputs'].items())
        (out / 'admission.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps({key: report.get(key) for key in
              ('result', 'residentFreeBytes', 'addedBytes', 'error')}))
        print(out)
    return 0 if report['result'] == 'FIT_PASS_NOT_EXECUTABLE' else 1


if __name__ == '__main__':
    raise SystemExit(main())
