"""Read-only emitted projection closure and loose instruction-work accounting.

No target executes. The existing stack checker remains fail-closed, unchanged.
Instruction visit bounds overcount alternative paths; they are not cycle WCET.
"""
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools/flight_demo/m2'))
from stack_check import check


def analyze(directory, candidate):
    text = (directory / 'RENDER.disassembly').read_text()
    blocks = {m[2]: (int(m[1], 16), m[0]) for m in re.finditer(
        r'^([0-9a-f]+) <([^>]+)>:\n.*?(?=^[0-9a-f]+ <|\Z)', text, re.M | re.S)}
    needed = {'m2_project_prepared'}
    pending = list(needed)
    while pending:
        name = pending.pop()
        for callee in re.findall(
                r'\b(?:jsr|jmp|bra|bcc|bcs|beq|bne|bmi|bpl|bvc|bvs)'
                r'\s+\$[0-9a-f]+\s+<([^>+]+)(?:\+[^>]*)?>', blocks[name][1]):
            if callee != name and callee not in needed:
                needed.add(callee)
                pending.append(callee)
    subset = '\n'.join(blocks[n][1] for n in sorted(needed, key=lambda n: blocks[n][0]))
    subset = subset.replace('<m2_project_prepared>:', '<main>:')
    try:
        stack = {'status': 'PASS', 'result': check(subset)}
    except (ValueError, KeyError) as error:
        stack = {'status': 'UNPROVEN', 'reason': str(error)}
    inventory = {n: len(re.findall(r'^\s*[0-9a-f]+:\s+', blocks[n][1], re.M))
                 for n in sorted(needed)}
    expected = {'m2_project_prepared', 'm2_point_valid', 'to_camera',
                'multiply_rotation', 'm2_multiply_q46', '__mulsi3', '__memset',
                'plane_distance', 'interpolate_delta', '__ashldi3',
                'project_axis', 'rounded_ratio', '__udivdi3', 'memcpy'}
    if candidate:
        expected.add('__divdi3')
    assert needed == expected, needed
    # Frozen Q46 loop: own maximum per-instruction visits 12, nine limb
    # products (each __mulsi3 <=16 restoring steps plus guard), 12-byte zero.
    q46 = inventory['m2_multiply_q46'] * 12 \
        + 9 * inventory['__mulsi3'] * 17 + inventory['__memset'] * 13
    # to_camera: three rows, three axes; 16 uniformly overcounts each local
    # instruction including the inner-loop guards. Nine rounded products.
    camera = inventory['to_camera'] * 16 + 9 * (inventory['multiply_rotation'] + q46)
    # Interpolation: 64 bit steps, two subtractions each, with loop guards.
    # 65*3 uniformly overcounts local visits. Each bit calls __ashldi3 once,
    # with shift 0..63; 65 overcounts its shift-loop and entry/exit visits.
    interpolation = inventory['interpolate_delta'] * (65 * 3) \
        + 64 * inventory['__ashldi3'] * 65
    # Unsigned 64-bit division: at most 64 alignment and 64 restoring shifts.
    # 129 uniformly overcounts each instruction. Signed wrapper is acyclic.
    division = inventory['__udivdi3'] * 129 + inventory.get('__divdi3', 0)
    projection = inventory['project_axis'] + inventory['rounded_ratio'] + division
    # Root: six planes and three coordinate updates, guards included: no own
    # instruction visited >6*4 times. Two validation loops have 3 axes + guard.
    # Original copies <=3*6 ClipPoints + final line; candidate <=2 + final.
    # Every copy <=24 bytes. 25 uniformly overcounts each memcpy instruction.
    copies = 3 if candidate else 19
    contributions = {
        'root': inventory['m2_project_prepared'] * 24,
        'point_validation': 2 * inventory['m2_point_valid'] * 4,
        'two_endpoint_transforms': 2 * camera,
        'plane_distances': 12 * inventory['plane_distance'],
        'coordinate_interpolations': 18 * interpolation,
        'projected_coordinates': 4 * projection,
        'bounded_copies': copies * inventory['memcpy'] * 25}
    instructions = re.findall(
        r'^\s*[0-9a-f]+:\s+(?:[0-9a-f]{2} )+\s*(\w+)\s*(.*)$', subset, re.M)
    sp_writes = [(op, operand) for op, operand in instructions
                 if op in {'sta', 'stx', 'sty', 'stz', 'inc', 'dec', 'inw', 'dew',
                           'asl', 'lsr', 'rol', 'ror'}
                 and re.match(r'^\$[23]\b', operand)]
    # Record SP writes even if the checker cannot complete the full proof.
    # Each root has a syntactic 8-byte constant allocation and deallocation.
    assert len(sp_writes) == 4, sp_writes
    return dict(stack=stack, software_stack_pointer_writes=sp_writes,
                closure=sorted(needed), instruction_inventory=inventory,
                per_call_bounds=dict(q46=q46, to_camera=camera,
                                     interpolate_delta=interpolation,
                                     project_axis=projection),
                contributions=contributions,
                conservative_projection_instruction_bound=sum(contributions.values()),
                source_operation_maxima=dict(point_validation=2, to_camera=2,
                    q46_products=18, limb_products_32bit=162, plane_distance=12,
                    interpolate_delta=18, interpolation_bit_steps=1152,
                    interpolation_subtraction_tests=2304, project_axis=4,
                    wide_divisions=4, memcpy_calls=copies))


if __name__ == '__main__':
    result = dict(before=analyze(PACKET / '00-reference', False),
                  after=analyze(PACKET / '04-candidate', True),
                  stack_checker_sha256=hashlib.sha256(
                      (ROOT / 'tools/flight_demo/m2/stack_check.py').read_bytes()).hexdigest(),
                  limitations='Structural instruction overbounds only; no cycles, speed, '
                      'wait states, platform/IRQ/NMI or dispatcher admission. Stack checker '
                      'rejects BIT in frozen interpolation in both artifacts; no integrated '
                      'hardware-stack bound claimed. Both roots syntactically allocate '
                      'and free an 8-byte software frame; no other closure SP writes. '
                      'Resident scratch charged separately.')
    print(json.dumps(result, indent=2))
