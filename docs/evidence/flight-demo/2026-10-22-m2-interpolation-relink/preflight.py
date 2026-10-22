"""Complete pending standalone static gates and prepare one fresh relink output.

No compiler, linker or target is invoked here. Earlier raw outputs remain exact.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import time

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent
PRIOR = ROOT / 'docs/evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk'
VERIFIER = ROOT / 'docs/evidence/flight-demo/2026-10-22-m2-bit-clv-verifier'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert not (PACKET / 'preflight.json').exists(), 'retain completed preflight'
    freeze = json.loads((PRIOR / 'source-freeze.json').read_text())
    assert all(sha(ROOT / p) == h for p, h in freeze['candidate_inputs'].items())
    assert len(freeze['candidate_inputs']) == 79
    for p, h in json.loads((PRIOR / 'pre-edit-freeze.json').read_text()).items():
        if p != 'src/graphics/m2_geometry.c':
            assert sha(ROOT / p) == h, p
    assert sha(ROOT / 'tools/flight_demo/m2/stack_check.py') == '5e4e20d3ff19697a7d55d3ae27c61260f3200172d4a9ba75bee84fa9810ac826'
    assert (ROOT / 'tests/flight_demo/m2/test_contract.py').read_bytes() == (
        VERIFIER / 'source/tests/flight_demo/m2/test_contract.py').read_bytes()
    for inventory in (ROOT / 'docs/evidence/flight-demo').glob('*/inventory.json'):
        assert all(sha(inventory.parent / p) == h
                   for p, h in json.loads(inventory.read_text()).items()), inventory
    reference = json.loads((PRIOR / '00-reference/build.json').read_text())
    tool_paths = dict(compiler=ROOT / 'toolchain/runtime/llvm-mos/bin/mos-mega65-clang',
        objdump=ROOT / 'toolchain/runtime/llvm-mos/bin/llvm-objdump',
        nm=ROOT / 'toolchain/runtime/llvm-mos/bin/llvm-nm', host_clang=Path('/usr/bin/clang'))
    assert {n:sha(p) for n, p in tool_paths.items()} == reference['tool_hashes']
    raw_identity = json.loads((PRIOR / 'artifact-identities.json').read_text())
    for directory, files in raw_identity.items():
        raw = Path(directory)
        assert {p.name for p in raw.iterdir() if p.is_file()} == set(files)
        assert all(sha(raw / p) == h['sha256'] and (raw / p).stat().st_size == h['bytes']
                   for p, h in files.items())
    standalone = ROOT / 'build/flight-demo/m2-pr1-1792683066367533000'
    disassembly = (standalone / 'M2.disassembly').read_text()
    symbols = (standalone / 'M2.symbols').read_text()
    mapping = (standalone / 'M2.map').read_text()
    schema = json.loads((ROOT / 'interfaces/m2_pr1.json').read_text())
    spec = importlib.util.spec_from_file_location('resumed_stack_check',
        ROOT / 'tools/flight_demo/m2/stack_check.py')
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    stack = checker.check(disassembly)
    assert stack == json.loads((VERIFIER / 'replay.json').read_text())[
        'replay']['interpolation']['after']['stack']
    # Exact static assertions after the failed line 70 in the unchanged builder.
    assert not re.search(r'\b(?:jsr|jmp)\s+\$[ef][0-9a-f]{3}\b', disassembly)
    assert not re.search(r'\b(?:cfentry|cfcopy|r0f_pf_enter|m1_platform_)', symbols)
    sections = {}
    for name in ('.text', '.rodata', '.data', '.bss', '.noinit'):
        match = re.search(r'^\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+'
                          + re.escape(name) + r'$', mapping, re.M)
        assert match, name
        start, size = [int(x, 16) for x in match.groups()]
        assert not size or schema['memory']['resident_start'] <= start < start + size <= schema['memory']['resident_end_exclusive']
        sections[name] = dict(start=start, bytes=size)
    assert '__stack = ' + hex(schema['memory']['software_stack_end_exclusive']) in mapping
    assert '(.noinit..Lstatic_stack)' in mapping
    stack['compiler_static_stack_bytes'] = sections['.noinit']['bytes']
    owners = {name:dict(address=int(addr, 16), bytes=int(size, 16))
              for addr, size, name in re.findall(
                  r'^([0-9a-f]+) ([0-9a-f]+) [BbDd] (m2_probe_\w+)$', symbols, re.M)}
    assert owners['m2_probe_pixels']['bytes'] == schema['constants']['raster_points'] * 4
    assert owners['m2_probe_record']['bytes'] > 0 and owners['m2_probe_surface']['bytes'] > 0
    static_result = dict(status='PASS remaining standalone static assertions',
        original_raw_output=str(standalone), target_sha256=sha(standalone / 'M2.prg'),
        stack=stack, sections=sections, owners=owners, target_execution='NOT RUN',
        source='Unchanged tools/flight_demo/m2/build.py assertions after line 70; no rebuild')
    (PACKET / 'standalone-static.json').write_text(json.dumps(static_result, indent=2) + '\n')
    old_host = ROOT / 'build/flight-demo/m2-interpolation-candidate-1792683066372990000'
    host = json.loads((old_host / 'build.json').read_text())
    assert len(host['commands']) == 3 and all(c['exit'] == 0 for c in host['commands'])
    assert host['host'] == 'PASS' and host['image_comparison'] == 'PASS five byte-identical'
    assert all(sha(ROOT / p) == h for p, h in host['inputs'].items())
    assert host['inputs'] == freeze['candidate_inputs']
    assert not any((old_host / p).exists() for p in ('RENDER.prg', 'RENDER.prg.elf', 'backend.o'))
    for i in range(5):
        assert sha(old_host / f'pose-{i}.ppm') == sha(PRIOR / '00-reference' / f'pose-{i}.ppm')
    out = ROOT / ('build/flight-demo/m2-interpolation-resumed-' + str(time.time_ns()))
    shutil.copytree(old_host, out)
    host['output'] = str(out)
    host['host_evidence_reused'] = dict(output=str(old_host),
        build_sha256=sha(old_host / 'build.json'),
        note='Copied exact host executable/logs/images. First three commands were run in original output, not rerun here.')
    (out / 'build.json').write_text(json.dumps(host, indent=2) + '\n')
    result = dict(status='PASS', output=str(out), source_inputs=host['inputs'],
        tool_hashes=reference['tool_hashes'], reused_host=host['host_evidence_reused'],
        original_raw_artifacts_preserved=sum(map(len, raw_identity.values())),
        candidate_composed_links_before=0, target_execution='NOT RUN')
    (PACKET / 'preflight.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(status='PASS pending static checks and exact pins',
        stack=stack, sections=sections, output=str(out)), indent=2))


if __name__ == '__main__':
    main()
