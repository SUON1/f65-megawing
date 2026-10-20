"""Build M1 only. No D81, SD, emulator or retained-proof output operations."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from generate import generate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'build/flight-demo/m1-p2'
TOOLS = ROOT / 'toolchain/runtime/llvm-mos/bin'
COMMON = ['src/core/m1_runtime.c', 'src/presentation/m1_snapshot.c',
          'src/input/m1_input.c', 'src/graphics/m1_graphics.c']
INCLUDES = ['interfaces/generated', 'src/core', 'src/presentation', 'src/input',
            'src/graphics', 'src/platform/m1', 'src/diagnostics/r0f']
PLATFORM = ['src/platform/m1/m1_platform.c', 'src/diagnostics/r0f/combined_platform.c',
            'src/diagnostics/r0f/combined_model.c', 'src/platform/r0f/qualification_45gs02.s',
            'src/platform/r0f/combined_45gs02.s', 'src/platform/r0a_platform_45gs02.s']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(args, **kwargs):
    return subprocess.run([str(x) for x in args], cwd=ROOT, check=True, **kwargs)


def build():
    generate()
    config = json.loads((ROOT / 'interfaces/m1_development.json').read_text())
    memory = config['memory']
    OUT.mkdir(parents=True, exist_ok=True)
    admission = run([sys.executable, '-B', '-m', 'unittest', 'discover',
                     '-s', 'tests/flight_demo', '-p', 'test_*.py', '-v'],
                    capture_output=True, text=True)
    admission_result = admission.stdout + admission.stderr
    (OUT / 'admission.txt').write_text(admission_result)
    print(admission_result, end='')
    includes = ['-I' + p for p in INCLUDES]
    warnings = ['-Wall', '-Wextra', '-Wconversion', '-Werror']
    run(['/usr/bin/clang', '-std=c11', *warnings, '-fsanitize=address,undefined',
         *includes, *COMMON, 'tests/flight_demo/m1_host.c', '-o', OUT / 'host'])
    result = run([OUT / 'host'], capture_output=True, text=True).stdout
    (OUT / 'host.txt').write_text(result)
    print(result, end='')
    lock = json.loads((ROOT / 'toolchain/f65_toolchain.lock.json').read_text())['llvm_mos']
    assert sha(TOOLS / 'mos-mega65-clang') == lock['compiler_sha256']
    assert sha(TOOLS / 'llvm-objdump') == lock['objdump_sha256']
    report = {'base': run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip(),
              'profile': config['identity'], 'host': result.strip(), 'physical': 'NOT RUN',
              'inputs': {}, 'targets': {}, 'admission': admission_result.strip()}
    for variant, replay, divisor in [('interactive', 0, 1), ('replay', 1, 1), ('slow-render', 1, 17)]:
        target = OUT / variant
        target.mkdir(exist_ok=True)
        prg = target / 'M1.prg'
        args = [TOOLS / 'mos-mega65-clang', '-mcpu=mos45gs02', '-mlto-zp=0', '-Os',
                *warnings, *includes, '-DM1_REPLAY=' + str(replay),
                '-DM1_RENDER_DIVISOR=' + str(divisor), *COMMON, *PLATFORM,
                'src/diagnostics/flight_demo/main.c', '-Wl,-T,src/platform/r0f/startup.ld',
                '-Wl,-Map,' + str(target / 'M1.map'), '-o', prg]
        run(args)
        elf = Path(str(prg) + '.elf')
        symbols = run([TOOLS / 'llvm-nm', '-S', elf], capture_output=True, text=True).stdout
        disassembly = run([TOOLS / 'llvm-objdump', '-d', elf], capture_output=True, text=True).stdout
        (target / 'M1.symbols').write_text(symbols)
        (target / 'M1.disassembly').write_text(disassembly)
        assert not re.search(r'\b(?:jsr|jmp)\s+\$[ef][0-9a-f]{3}\b', disassembly)
        assert 'r0f_pf_enter' in disassembly and 'f65_basepage_enter' in disassembly
        mapping = (target / 'M1.map').read_text()
        sections = {}
        for name in ('.text', '.rodata', '.data', '.bss', '.noinit'):
            match = re.search(r'^\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+' + re.escape(name) + r'$', mapping, re.M)
            assert match, name
            start, size = [int(x, 16) for x in match.groups()]
            assert not size or (start >= memory['resident_start'] and start + size <= memory['resident_end_exclusive']), (name, start, size)
            sections[name] = {'start': start, 'bytes': size}
        assert '__stack = ' + hex(memory['software_stack_end_exclusive']) in mapping
        report['targets'][variant] = {'sha256': sha(prg), 'bytes': prg.stat().st_size,
                                      'sections': sections, 'command': list(map(str, args)),
                                      'owner_symbols': {name: {'address': int(address, 16), 'bytes': int(size, 16)}
                                          for address, size, name in re.findall(r'^([0-9a-f]+) ([0-9a-f]+) [BbDd] (m1_\w+)$', symbols, re.M)}}
    additional = sorted(str(p.relative_to(ROOT)) for directory in INCLUDES
                        for p in (ROOT / directory).glob('*.h'))
    additional += sorted(str(p.relative_to(ROOT)) for p in (ROOT / 'tools/flight_demo').glob('*.py'))
    additional += sorted(str(p.relative_to(ROOT)) for p in (ROOT / 'tests/flight_demo').glob('*') if p.is_file())
    additional += ['toolchain/f65_toolchain.lock.json']
    for p in COMMON + PLATFORM + additional + ['src/diagnostics/flight_demo/main.c', 'interfaces/m1_development.json',
                                  'interfaces/generated/m1_development.h', 'memory/m1-development-ledger.json',
                                  'src/platform/r0f/startup.ld']:
        report['inputs'][p] = sha(ROOT / p)
    (OUT / 'build.json').write_text(json.dumps(report, indent=2) + '\n')
    print('M1 TARGET compile/link/static PASS (3 profiles); no execution claim')


if __name__ == '__main__':
    build()
