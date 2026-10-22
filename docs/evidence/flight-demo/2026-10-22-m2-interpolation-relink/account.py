"""Read-only resident, emitted closure, stack and instruction-work accounting."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import struct

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent
PRIOR = ROOT / 'docs/evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    (PACKET / name).write_text(json.dumps(value, indent=2) + '\n')


def symbols(path):
    return {parts[3]:dict(start=int(parts[0], 16), bytes=int(parts[1], 16), kind=parts[2])
            for line in path.read_text().splitlines() if len(parts := line.split()) == 4}


def elf(path):
    data = path.read_bytes()
    assert data[:7] == b'\x7fELF\x01\x01\x01'
    header = struct.unpack_from('<16sHHIIIIIHHHHHH', data)
    sections = [struct.unpack_from('<IIIIIIIIII', data, header[6] + i * header[11])
                for i in range(header[12])]
    strings = sections[header[13]]
    names = data[strings[4]:strings[4] + strings[5]]
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
        gaps=end-low-sum(s['bytes'] for s in nonempty), ceiling=32768,
        excess=max(0, end-32768), reserve_allocation=0)


def stack_result(checker, text):
    try:
        return dict(status='PASS', result=checker.check(text))
    except (ValueError, KeyError) as error:
        return dict(status='UNPROVEN', reason=str(error))


def closure(directory, checker, candidate):
    text = (directory / 'RENDER.disassembly').read_text()
    blocks = {m[2]: (int(m[1], 16), m[0]) for m in re.finditer(
        r'^([0-9a-f]+) <([^>]+)>:\n.*?(?=^[0-9a-f]+ <|\Z)', text, re.M | re.S)}
    needed = {'m2_project_prepared'}
    pending = list(needed)
    while pending:
        name = pending.pop()
        for callee in re.findall(r'\b(?:jsr|jmp|bra|bcc|bcs|beq|bne|bmi|bpl|bvc|bvs)'
                r'\s+\$[0-9a-f]+\s+<([^>+]+)(?:\+[^>]*)?>', blocks[name][1]):
            if callee != name and callee not in needed:
                needed.add(callee)
                pending.append(callee)
    expected = {'m2_project_prepared', 'm2_point_valid', 'to_camera', 'multiply_rotation',
        'm2_multiply_q46', '__mulsi3', '__memset', 'plane_distance', 'interpolate_delta',
        'project_axis', 'rounded_ratio', '__udivdi3', 'memcpy'}
    if not candidate:
        expected.add('__ashldi3')
    assert needed == expected, needed
    subset = '\n'.join(blocks[n][1] for n in sorted(needed, key=lambda n: blocks[n][0]))
    subset = subset.replace('<m2_project_prepared>:', '<main>:')
    inventory = {n:len(re.findall(r'^\s*[0-9a-f]+:\s+', blocks[n][1], re.M)) for n in sorted(needed)}
    # Frozen source loop bounds, identical method to the predecessor. These
    # uniformly overcount instruction visits, not CPU cycles or service WCET.
    q46 = inventory['m2_multiply_q46'] * 12 + 9 * inventory['__mulsi3'] * 17 + inventory['__memset'] * 13
    camera = inventory['to_camera'] * 16 + 9 * (inventory['multiply_rotation'] + q46)
    interpolation = inventory['interpolate_delta'] * (65 * 3)
    if not candidate:
        interpolation += 64 * inventory['__ashldi3'] * 65
    division = inventory['__udivdi3'] * 129
    projection = inventory['project_axis'] + inventory['rounded_ratio'] + division
    # Both sides already contain the accepted compact projection: two endpoint
    # copies plus final output, not the pre-correction nineteen-copy reference.
    contributions = dict(root=inventory['m2_project_prepared'] * 24,
        point_validation=2 * inventory['m2_point_valid'] * 4,
        two_endpoint_transforms=2 * camera, plane_distances=12 * inventory['plane_distance'],
        coordinate_interpolations=18 * interpolation, projected_coordinates=4 * projection,
        bounded_copies=3 * inventory['memcpy'] * 25)
    instructions = re.findall(r'^\s*[0-9a-f]+:\s+(?:[0-9a-f]{2} )+\s*(\w+)\s*(.*)$', subset, re.M)
    writes = [(op, arg) for op, arg in instructions if op in {
        'sta', 'stx', 'sty', 'stz', 'inc', 'dec', 'inw', 'dew', 'asl', 'lsr', 'rol', 'ror'}
        and re.match(r'^\$[23]\b', arg)]
    assert len(writes) == 4, writes
    return dict(stack=stack_result(checker, subset), closure=sorted(needed),
        instruction_inventory=inventory, software_stack_pointer_writes=writes,
        syntactic_root_software_frame_bytes=8,
        per_call_instruction_bounds=dict(q46=q46, to_camera=camera,
            interpolate_delta=interpolation, project_axis=projection),
        contributions=contributions, conservative_projection_instruction_bound=sum(contributions.values()),
        operation_maxima=dict(to_camera=2, q46_products=18, limb_products_32bit=162,
            plane_distances=12, interpolations=18, interpolation_bit_steps=1152,
            interpolation_subtraction_tests=2304, project_axis=4, wide_divisions=4, memcpy_calls=3),
        whole_probe_stack=stack_result(checker, text))


def main():
    preflight = json.loads((PACKET / 'preflight.json').read_text())
    out = Path(preflight['output'])
    report = json.loads((out / 'build.json').read_text())
    assert len(report['commands']) == 7 and all(c['exit'] == 0 for c in report['commands'])
    before_report = json.loads((PRIOR / '00-reference/build.json').read_text())
    reference_output = Path(before_report['output'])
    before = elf(reference_output / 'RENDER.prg.elf')
    after = elf(out / 'RENDER.prg.elf')
    assert before['resident_bytes'] == 34149 and after['resident_bytes'] == report['resident_bytes']
    assert after['resident_end'] == report['resident_end']
    a = symbols(PRIOR / '00-reference/RENDER.symbols')
    b = symbols(out / 'RENDER.symbols')
    deltas = {name:dict(before=a.get(name), after=b.get(name))
        for name in sorted(set(a) | set(b)) if name not in a or name not in b
        or a[name]['bytes'] != b[name]['bytes'] or a[name]['kind'] != b[name]['kind']}
    owners = {name:dict(before=a[name], after=b[name]) for name in before_report['owners']}
    assert all(v['before']['bytes'] == v['after']['bytes'] and v['before']['kind'] == v['after']['kind']
               for v in owners.values())
    spec = importlib.util.spec_from_file_location('account_stack', ROOT / 'tools/flight_demo/m2/stack_check.py')
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    assert sha(ROOT / 'tools/flight_demo/m2/stack_check.py') == '5e4e20d3ff19697a7d55d3ae27c61260f3200172d4a9ba75bee84fa9810ac826'
    static = dict(reference=closure(PRIOR / '00-reference', checker, False),
                  candidate=closure(out, checker, True),
                  checker_sha256=sha(ROOT / 'tools/flight_demo/m2/stack_check.py'),
                  limitations='Instruction-visit overbounds only; no cycles, runtime speed, wait states, '
                  'platform/IRQ/NMI overhead, whole-renderer admission or 100 Hz margins.')
    save('static-accounting.json', static)
    section_delta = {name:after['allocated'][name]['bytes'] - value['bytes']
                     for name, value in before['allocated'].items()}
    assert sum(section_delta.values()) + after['gaps'] - before['gaps'] == after['resident_bytes'] - before['resident_bytes']
    result = dict(before=before, after=after, resident_delta=after['resident_bytes']-before['resident_bytes'],
        savings=before['resident_bytes']-after['resident_bytes'], section_deltas=section_delta,
        bounded_size_gate='PASS' if after['resident_bytes'] < 34149 else 'FAIL',
        full_fit='PASS' if after['excess'] == 0 else 'FAIL', owner_accounting=owners,
        all_symbol_size_kind_changes=deltas,
        reference_prg_sha256=sha(reference_output / 'RENDER.prg'),
        reference_elf_sha256=sha(reference_output / 'RENDER.prg.elf'),
        candidate_prg_sha256=sha(out / 'RENDER.prg'), candidate_elf_sha256=sha(out / 'RENDER.prg.elf'),
        candidate_prg_bytes=(out / 'RENDER.prg').stat().st_size,
        candidate_elf_bytes=(out / 'RENDER.prg.elf').stat().st_size,
        tool_hashes=report['tool_hashes'], source_inputs=report['inputs'], composed_candidate_relinks=1,
        target_execution='NOT RUN', runtime_display_admission='NOT REACHED; full-fit FAIL')
    save('comparison.json', result)
    archive = PACKET / '01-candidate'
    archive.mkdir(exist_ok=True)
    for path in out.iterdir():
        if path.is_file() and path.suffix in {'.json', '.txt', '.map', '.symbols', '.disassembly'}:
            shutil.copyfile(path, archive / path.name)
    destination = PACKET / 'source/src/graphics/m2_geometry.c'
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / 'src/graphics/m2_geometry.c', destination)
    save('candidate-artifacts.json', {str(p):dict(sha256=sha(p), bytes=p.stat().st_size)
                                     for p in sorted(out.iterdir()) if p.is_file()})
    print(json.dumps(dict(before=before, after=after, savings=result['savings'],
        section_deltas=section_delta, bounded=result['bounded_size_gate'], full_fit=result['full_fit'],
        reference_stack=static['reference']['stack'], candidate_stack=static['candidate']['stack'],
        whole_probe_stack=static['candidate']['whole_probe_stack'],
        work_before=static['reference']['conservative_projection_instruction_bound'],
        work_after=static['candidate']['conservative_projection_instruction_bound'],
        candidate_elf_sha256=result['candidate_elf_sha256']), indent=2))


if __name__ == '__main__':
    main()
