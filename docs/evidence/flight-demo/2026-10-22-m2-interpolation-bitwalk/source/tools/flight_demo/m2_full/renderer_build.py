"""Early real-renderer size gate with opaque backend; never execute target code.

Reuse the PR1 pure-source and host runtime inventory. This is not full-target
admission: display adapter, activation and static service gates follow only
when this early link fits. Preserve every attempt and command, including failure.
"""
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/flight_demo/m2'))
LEGACY = runpy.run_path(str(ROOT / 'tools/flight_demo/m2/build.py'))
TOOLS = LEGACY['TOOLS']
SOURCES = LEGACY['PURE'] + LEGACY['M1'] + [
    'src/graphics/m2_renderer.c', 'src/graphics/m2_font.c',
    'src/input/m2_camera_input.c', 'src/diagnostics/m2/camera.c',
    'src/diagnostics/m2/dispatch.c']
INCLUDES = LEGACY['INCLUDES'] + ['src/diagnostics/m2', 'src/platform/m1',
                               'src/diagnostics/r0f']
PLATFORM = ['src/platform/m1/m1_platform.c',
            'src/diagnostics/r0f/combined_platform.c',
            'src/diagnostics/r0f/combined_model.c',
            'src/platform/r0f/qualification_45gs02.s',
            'src/platform/r0f/combined_45gs02.s', 'src/platform/r0a_platform_45gs02.s']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build():
    out = ROOT / ('build/flight-demo/m2-renderer-' + str(time.time_ns()))
    out.mkdir(parents=True)
    report = {'output': str(out), 'base': subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], text=True).strip(), 'commands': [],
        'execution_admitted': False, 'target_executed': False,
        'full_target_fit': 'UNPROVEN: opaque backend; not actual display adapter',
        'runtime_display_admission': 'NOT REACHED'}

    def run(args, name):
        command = list(map(str, args))
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        (out / name).write_text(result.stdout + result.stderr)
        report['commands'].append({'argv': command, 'exit': result.returncode, 'log': name})
        if result.returncode:
            raise RuntimeError('check failed: ' + name)
        return result.stdout

    try:
        lock = json.loads((ROOT / 'toolchain/f65_toolchain.lock.json').read_text())['llvm_mos']
        for tool, key in [('mos-mega65-clang', 'compiler_sha256'),
                          ('llvm-objdump', 'objdump_sha256')]:
            assert sha(TOOLS / tool) == lock[key]
        report['tool_hashes'] = {name: sha(path) for name, path in [
            ('compiler', TOOLS / 'mos-mega65-clang'), ('objdump', TOOLS / 'llvm-objdump'),
            ('nm', TOOLS / 'llvm-nm'), ('host_clang', Path('/usr/bin/clang'))]}
        flags = ['-Wall', '-Wextra', '-Wconversion', '-Werror']
        includes = ['-I' + p for p in INCLUDES]
        run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s',
             'tests/flight_demo/m2_full', '-p', 'test_*.py', '-v'], 'contracts.txt')
        run(['/usr/bin/clang', '-std=c11', *flags, '-fsanitize=address,undefined',
             *includes, *SOURCES, 'tests/flight_demo/m2_full/renderer_host.c',
             '-o', out / 'host'], 'host-compile.txt')
        run([out / 'host', out], 'host.txt')
        report['host'] = 'PASS'
        target_flags = ['-mcpu=mos45gs02', '-mlto-zp=0', '-DM2_TARGET_LAYOUT_CHECK=1', '-Oz',
                        '-fno-inline-functions', '-fno-jump-tables', *flags, *includes]
        # The opaque non-LTO object cannot consume an LTO zero-page option.
        backend_flags = [flag for flag in target_flags if flag != '-mlto-zp=0']
        run([TOOLS / 'mos-mega65-clang', *backend_flags, '-fno-lto', '-c',
             'tests/flight_demo/m2_full/fit_backend.c', '-o', out / 'backend.o'],
            'backend-compile.txt')
        target = out / 'RENDER.prg'
        run([TOOLS / 'mos-mega65-clang', *target_flags, *SOURCES, *PLATFORM,
             'tests/flight_demo/m2_full/fit_root.c', out / 'backend.o',
             '-Wl,-T,src/platform/r0f/startup.ld', '-Wl,-Map,' + str(out / 'RENDER.map'),
             '-o', target], 'target-compile.txt')
        run([TOOLS / 'llvm-objdump', '-d', str(target) + '.elf'], 'RENDER.disassembly')
        symbols = run([TOOLS / 'llvm-nm', '-S', str(target) + '.elf'], 'RENDER.symbols')
        mapping = (out / 'RENDER.map').read_text()
        sections = {}
        for name in ['.text', '.rodata', '.data', '.bss', '.noinit']:
            match = re.search(r'^\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+'
                              + re.escape(name) + '$', mapping, re.M)
            assert match, name
            start, size = [int(value, 16) for value in match.groups()]
            sections[name] = {'start': start, 'bytes': size}
        end = max(s['start'] + s['bytes'] for s in sections.values())
        ledger = json.loads((ROOT / 'memory/m2-full-ledger.json').read_text())
        low, ceiling = ledger['resident']
        fits = all(low <= s['start'] and s['start'] + s['bytes'] <= ceiling
                   for s in sections.values())
        owner_names = ['core', 'snapshots', 'input', 'requested', 'previous_camera_keys',
                       'renderer', 'glyphs']
        owners = {}
        for line in symbols.splitlines():
            parts = line.split()
            if len(parts) == 4 and parts[2].lower() in ['b', 'd', 'r'] and (
                    parts[3] in owner_names or parts[3].startswith(('m2_fit_', 'input.'))):
                owners[parts[3]] = {'start': int(parts[0], 16), 'bytes': int(parts[1], 16)}
        required_owners = set(owner_names) - {'input'}
        assert required_owners <= set(owners), owners
        assert 'input' in owners or 'input.0' in owners, owners
        report.update({'sections': sections, 'owners': owners, 'resident_end': end,
                       'ceiling': ceiling, 'excess_bytes': max(0, end - ceiling),
                       'early_renderer_fit': 'PASS intermediate only' if fits else 'FAIL',
                       'target_sha256': sha(target), 'reserve_allocation': 0,
                       'owner_notes': 'input may scalarize; unobserved stage array may eliminate; all allocated sections charged',
                       'service_bounds': 'UNPROVEN; opaque backend bounds default zero, no target work admitted',
                       'stack': 'UNPROVEN: resident noinit charged once; dynamic/ABI gate not reached'})
    except Exception as error:
        report['error'] = str(error)
    finally:
        paths = set(SOURCES + PLATFORM + [
            'tests/flight_demo/m2_full/renderer_host.c', 'tests/flight_demo/m2_full/fit_root.c',
            'tests/flight_demo/m2_full/fit_backend.c', 'tests/flight_demo/m2_full/renderer_cases.json',
            'tests/flight_demo/m2_full/test_contract.py', 'src/platform/r0f/startup.ld',
            'tests/flight_demo/m2_full/q46_equivalence.c', 'tests/flight_demo/m2_full/q46_binding.c',
            'tests/flight_demo/m2_full/q46_oracle.py',
            'tools/flight_demo/m2_full/renderer_build.py', 'tools/flight_demo/m2_full/generate.py',
            'tools/flight_demo/m2/build.py', 'toolchain/f65_toolchain.lock.json',
            'interfaces/m2_full.json', 'interfaces/m2_pr1.json', 'memory/m2-full-ledger.json'])
        for directory in INCLUDES:
            paths.update(str(p.relative_to(ROOT)) for p in (ROOT / directory).glob('*.h'))
        report['inputs'] = {p: sha(ROOT / p) for p in sorted(paths)}
        (out / 'build.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps({k: report[k] for k in ['output', 'error', 'host', 'early_renderer_fit',
                                                'resident_end', 'excess_bytes'] if k in report}))
    return 0 if report.get('early_renderer_fit', '').startswith('PASS') else 1


if __name__ == '__main__':
    raise SystemExit(build())
