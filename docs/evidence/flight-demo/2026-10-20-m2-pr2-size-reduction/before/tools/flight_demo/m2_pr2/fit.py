"""Fresh compile-only integrated-fit preflight; never executes the target."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / 'toolchain/runtime/llvm-mos/bin'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    output = ROOT / ('build/flight-demo/m2-pr2-fit-' + str(time.time_ns()))
    output.mkdir(parents=True)
    lock = json.loads((ROOT / 'toolchain/f65_toolchain.lock.json').read_text())['llvm_mos']
    for tool, key in [('mos-mega65-clang', 'compiler_sha256'), ('llvm-objdump', 'objdump_sha256')]:
        assert sha(TOOLS / tool) == lock[key]
    sources = ['src/core/m1_runtime.c', 'src/input/m1_input.c',
               'src/presentation/m1_snapshot.c', 'src/environment/m2_fixture.c',
               'src/graphics/m2_geometry.c', 'interfaces/generated/m2_tables.c',
               'src/platform/m1/m1_platform.c', 'src/diagnostics/r0f/combined_platform.c',
               'src/diagnostics/r0f/combined_model.c',
               'src/platform/r0f/qualification_45gs02.s',
               'src/platform/r0f/combined_45gs02.s', 'src/platform/r0a_platform_45gs02.s',
               'tests/flight_demo/m2_pr2/fit.c']
    includes = ['interfaces/generated', 'src/core', 'src/input', 'src/presentation',
                'src/environment', 'src/graphics', 'src/platform/m1', 'src/diagnostics/r0f']
    commands = []

    def run(args, filename):
        command = list(map(str, args))
        commands.append(command)
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        (output / filename).write_text(result.stdout + result.stderr)
        return result

    target = output / 'FIT.prg'
    result = run([TOOLS / 'mos-mega65-clang', '-mcpu=mos45gs02', '-mlto-zp=0',
                  '-Os', '-fno-jump-tables', '-Wall', '-Wextra', '-Wconversion', '-Werror',
                  *['-I' + item for item in includes], *sources,
                  '-Wl,-T,src/platform/r0f/startup.ld',
                  '-Wl,-Map,' + str(output / 'FIT.map'), '-o', target], 'compile.txt')
    sections = {}
    if result.returncode == 0:
        for tool, filename in [('llvm-objdump', 'FIT.disassembly'), ('llvm-nm', 'FIT.symbols')]:
            arguments = ['-d'] if tool == 'llvm-objdump' else ['-S']
            assert run([TOOLS / tool, *arguments, str(target) + '.elf'], filename).returncode == 0
        mapping = (output / 'FIT.map').read_text()
        for name in ('.text', '.rodata', '.data', '.bss', '.noinit'):
            found = re.search(r'^\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+' + re.escape(name) + r'$', mapping, re.M)
            assert found, name
            start, size = [int(value, 16) for value in found.groups()]
            sections[name] = {'start': start, 'bytes': size}
    end = max((value['start'] + value['bytes'] for value in sections.values()), default=0)
    ledger = json.loads((ROOT / 'memory/m1-development-ledger.json').read_text())
    ceiling = ledger['ranges']['resident_end_exclusive']
    paths = set(sources + ['src/platform/r0f/startup.ld', 'toolchain/f65_toolchain.lock.json',
                          'tools/flight_demo/m2_pr2/fit.py', 'memory/m1-development-ledger.json',
                          'memory/m2-pr1-ledger.json', 'interfaces/m1_development.json',
                          'interfaces/m2_pr1.json'])
    for directory in includes:
        paths.update(str(path.relative_to(ROOT)) for path in (ROOT / directory).glob('*.h'))
    report = {'base': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
              'commands': commands, 'compile_exit': result.returncode,
              'sections': sections, 'resident_end': end, 'resident_ceiling': ceiling,
              'fit': 'PASS provisional reachability only' if sections and end <= ceiling else 'FAIL',
              'excess_bytes': max(0, end - ceiling),
              'inputs': {path: sha(ROOT / path) for path in sorted(paths)},
              'target_sha256': sha(target) if target.exists() else None,
              'execution_admitted': False, 'target_executed': False,
              'limitations': 'Not full renderer, scheduling, stack/ABI admission or scanout proof; current PR1 raster output scratch retained explicitly.'}
    (output / 'fit.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'output': str(output), 'fit': report['fit'], 'resident_end': hex(end),
                      'excess_bytes': report['excess_bytes'], 'compile_exit': result.returncode}))
    return 0 if sections and end <= ceiling else 1


if __name__ == '__main__':
    raise SystemExit(build())
