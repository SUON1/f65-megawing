"""Preserve and inspect existing artifacts after the I5 failed gate. No builds."""
import difflib
import hashlib
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent
BUILD = ROOT / 'build/flight-demo'
STANDALONE = BUILD / 'm2-pr1-1792683066367533000'
HOST = BUILD / 'm2-interpolation-candidate-1792683066372990000'
DIRECT = BUILD / 'interpolation-comparison'
PROJECTION = BUILD / 'interpolation-projection-checks-1792683066366257000'
OLD = ROOT / 'docs/evidence/flight-demo/2026-10-21-m2-projection-forward-guard'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, data):
    (PACKET / name).write_text(json.dumps(data, indent=2) + '\n')


def elf_account(path):
    data = path.read_bytes()
    assert data[:7] == b'\x7fELF\x01\x01\x01'
    header = struct.unpack_from('<16sHHIIIIIHHHHHH', data)
    offset, size, count, strings = header[6], header[11], header[12], header[13]
    sections = [struct.unpack_from('<IIIIIIIIII', data, offset + i * size)
                for i in range(count)]
    names = data[sections[strings][4]:sections[strings][4] + sections[strings][5]]
    allocated = {}
    for section in sections:
        if section[2] & 2:
            name = names[section[0]:].split(b'\0', 1)[0].decode()
            allocated[name] = dict(start=section[3], bytes=section[5], type=section[1])
    nonempty = [s for s in allocated.values() if s['bytes']]
    low = min(s['start'] for s in nonempty)
    end = max(s['start'] + s['bytes'] for s in nonempty)
    assert low == 8193
    return dict(allocated=allocated, resident_bytes=end-low, resident_end=end,
                gaps=end-low-sum(s['bytes'] for s in nonempty),
                ceiling=32768, deficit=max(0, end-32768),
                reserve_allocation=0)


def main():
    for source, target in [(DIRECT, '01-direct'), (PROJECTION, '02-projection'),
                           (STANDALONE, '03-standalone'), (HOST, '04-renderer-host')]:
        destination = PACKET / target
        destination.mkdir(exist_ok=True)
        for path in source.iterdir():
            if path.is_file() and (path.suffix in {'.txt', '.json', '.map', '.symbols',
                                                 '.disassembly', '.ppm', '.h'}):
                shutil.copyfile(path, destination / path.name)
    # The frozen builder writes build.json only after its stack gate. Preserve
    # the real failure, and label recovered command metadata as reconstruction.
    assert not (STANDALONE / 'build.json').exists()
    failure = ('ValueError: unrecognized instruction: bit\n'
               'tools/flight_demo/m2/build.py:70 stack=check(disassembly)\n'
               'tools/flight_demo/m2/stack_check.py:82\n'
               'Wrapper exit 1; transcribed from the retained tool result.\n')
    (PACKET / '03-standalone/failure.txt').write_text(failure)
    previous = json.loads((OLD / '03-standalone/build.json').read_text())
    old_output = str(Path(previous['commands'][2][0]).parent)
    old_root = old_output.split('/build/flight-demo/')[0]
    logs = ['contract-tests.txt', 'host-build.txt', 'host.txt', 'oracle-build.txt',
            'oracle.json', 'clip-regressions.json', 'clip-vectors.txt',
            'clip-host-build.txt', 'clip-host.txt', 'target-build.txt',
            'M2.disassembly', 'M2.symbols']
    commands = []
    for argv, log in zip(previous['commands'], logs):
        assert (STANDALONE / log).is_file()
        commands.append(dict(argv=[p.replace(old_output, str(STANDALONE))
                                    .replace(old_root, str(ROOT)) for p in argv],
                             exit=0, log=log))
    save('03-standalone/recovered-command-record.json', dict(
        provenance='Reconstructed from unchanged builder and existing logs; not a builder-produced success report',
        wrapper=['python3', '-B', 'tools/flight_demo/m2/build.py'], wrapper_exit=1,
        commands=commands, stack_gate='FAIL unrecognized instruction: bit',
        later_static_checks='NOT REACHED'))
    fresh_reference = json.loads((PACKET / '00-reference/build.json').read_text())
    reference_output = Path(fresh_reference['output'])
    reference = elf_account(reference_output / 'RENDER.prg.elf')
    standalone = elf_account(STANDALONE / 'M2.prg.elf')
    before_end = max(s['start'] + s['bytes'] for s in previous['sections'].values())
    section_deltas = {name: standalone['allocated'][name]['bytes'] - section['bytes']
                      for name, section in previous['sections'].items()}
    standalone.update(comparison_baseline=str(OLD / '03-standalone/build.json'),
                      before_resident_bytes=before_end-8193,
                      resident_delta=standalone['resident_bytes']-(before_end-8193),
                      section_deltas=section_deltas,
                      stack='UNPROVEN; unchanged checker rejects BIT',
                      interpolation_symbol='Inlined into main; no separately sized helper',
                      shift_helper='__ashldi3 absent from standalone symbol table',
                      later_static_checks='Not reached by builder; ELF accounting here is read-only')
    assert '__ashldi3' not in (STANDALONE / 'M2.symbols').read_text()
    assert reference['resident_bytes'] == 34149 and reference['deficit'] == 9574
    assert standalone['resident_delta'] == -97
    inputs = fresh_reference['inputs']
    changed = [p for p, h in inputs.items() if sha(ROOT / p) != h]
    assert changed == ['src/graphics/m2_geometry.c'], changed
    old_source = (PACKET / 'reference_geometry.c').read_text()
    new_source = (ROOT / changed[0]).read_text()
    expected = old_source.replace('if (((magnitude >> (bit - 1u)) & 1u) != 0u)',
        'if ((magnitude & (UINT64_C(1) << 63u)) != 0u)')
    old_tail = '        }\n    }\n    if (remainder >= (divisor + 1u) / 2u)'
    new_tail = ('        }\n        // Unsigned wrap discards the bit already consumed by this step.\n'
                '        magnitude <<= 1u;\n    }\n    if (remainder >= (divisor + 1u) / 2u)')
    expected = expected.replace(old_tail, new_tail, 1)
    assert expected == new_source
    (PACKET / 'candidate.patch').write_text(''.join(difflib.unified_diff(
        old_source.splitlines(True), new_source.splitlines(True),
        fromfile='reference/src/graphics/m2_geometry.c',
        tofile='candidate/src/graphics/m2_geometry.c')))
    frozen = json.loads((PACKET / 'pre-edit-freeze.json').read_text())
    assert all(sha(ROOT / p) == h for p, h in frozen.items() if p != changed[0])
    save('source-freeze.json', dict(reference_inputs=inputs,
        candidate_inputs={p:sha(ROOT / p) for p in inputs}, differences=changed,
        exact_i2_edit='PASS', tests_and_q46_frozen='PASS',
        stack_checker_sha256=sha(ROOT / 'tools/flight_demo/m2/stack_check.py')))
    artifacts = {}
    for directory in [reference_output, DIRECT, PROJECTION, STANDALONE, HOST]:
        artifacts[str(directory)] = {p.name:dict(sha256=sha(p), bytes=p.stat().st_size)
                                     for p in sorted(directory.iterdir()) if p.is_file()}
    assert not any((HOST / n).exists() for n in ['RENDER.prg', 'RENDER.prg.elf', 'backend.o'])
    assert len(json.loads((HOST/'build.json').read_text())['commands']) == 3
    save('artifact-identities.json', artifacts)
    tool_hashes = fresh_reference['tool_hashes']
    save('comparison.json', dict(status='FAILED I5 prerequisite stack gate; implementation stopped',
        main=fresh_reference['base'], reference=reference,
        reference_interpolation_bytes=1605, reference_shift_helper_bytes=31,
        candidate_composed_relinks=0, candidate_composed_accounting=None,
        composed_savings='UNMEASURED; no candidate relink',
        last_verified_composed_deficit=9574, standalone=standalone,
        tool_hashes=tool_hashes, target_execution='NOT RUN'))
    # Preserve reconstructed production and new test sources without changing
    # or copying back into any earlier checkout.
    paths = {r['destination'] for r in json.loads((PACKET/'reconstruction.json').read_text())['restorations']}
    paths.update(['tests/flight_demo/m2_full/interpolation_corpus.py',
                  'tests/flight_demo/m2_full/interpolation_equivalence.c'])
    for relative in sorted(paths):
        destination = PACKET / 'source' / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, destination)
    print(json.dumps(dict(reference=reference, standalone=standalone), indent=2))


if __name__ == '__main__':
    main()
