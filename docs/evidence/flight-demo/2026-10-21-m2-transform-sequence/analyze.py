"""Read-only transform-closure stack and conservative instruction accounting.

Uniform per-routine visit bounds overcount mutually exclusive paths. These are
instruction-work bounds, never cycle WCET, actual speed or runtime admission.
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
    needed = {'m2_transform'}
    pending = list(needed)
    while pending:
        name = pending.pop()
        # Include tail jumps and cross-routine branches, not only JSR calls.
        for callee in re.findall(
                r'\b(?:jsr|jmp|bra|bcc|bcs|beq|bne|bmi|bpl|bvc|bvs)'
                r'\s+\$[0-9a-f]+\s+<([^>+]+)(?:\+[^>]*)?>', blocks[name][1]):
            if callee != name and callee not in needed:
                needed.add(callee)
                pending.append(callee)
    expected = {'m2_transform', 'm2_camera_valid', 'sine', '__modhi3', '__umodhi3',
                'multiply_rotation', 'm2_multiply_q46', '__memset', '__mulsi3'}
    if candidate:
        expected.add('memcpy')
    assert needed == expected, needed
    subset = '\n'.join(blocks[n][1] for n in sorted(needed, key=lambda n: blocks[n][0]))
    subset = subset.replace('<m2_transform>:', '<main>:')
    stack = check(subset)
    inventory = {name: len(re.findall(r'^\s*[0-9a-f]+:\s+', blocks[name][1], re.M))
                 for name in needed}
    assert inventory['m2_transform'] == (506 if candidate else 1345)
    assert {name: inventory[name] for name in expected - {'m2_transform', 'memcpy'}} == {
        'm2_camera_valid': 278, 'sine': 124, '__modhi3': 60, '__umodhi3': 91,
        'multiply_rotation': 1, 'm2_multiply_q46': 526, '__memset': 15, '__mulsi3': 64}
    q46 = inventory['m2_multiply_q46'] * 12 + 9 * inventory['__mulsi3'] * 17 \
        + inventory['__memset'] * 13
    # Sine's own control flow and signed remainder wrapper are acyclic. The
    # unsigned 16-bit remainder has <=16 alignment and <=16 restoring shifts;
    # 33 safely bounds any one instruction including guards. Divisor is 360.
    sine = inventory['sine'] + inventory['__modhi3'] + inventory['__umodhi3'] * 33
    # Old transform is acyclic, including its inlined result stores. Candidate
    # has six sine iterations and fourteen product iterations; maximum guard
    # visits 15, with no nested local copy loop. Its final memcpy is 72 bytes.
    own = inventory['m2_transform'] * (15 if candidate else 1)
    copy = inventory['memcpy'] * 73 if candidate else 0
    bound = own + inventory['m2_camera_valid'] \
        + 6 * sine + 14 * (inventory['multiply_rotation'] + q46) + copy
    return {'stack': stack, 'closure': sorted(needed), 'instruction_inventory': inventory,
            'q46_callee_instruction_bound': q46, 'sine_callee_instruction_bound': sine,
            'own_instruction_bound': own, 'final_copy_instruction_bound': copy,
            'conservative_transform_instruction_bound': bound,
            'formula': ('506*15 + 278 + 6*(124+60+91*33) + 14*(1+16299) + 22*73'
                        if candidate else
                        '1345 + 278 + 6*(124+60+91*33) + 14*(1+16299)'),
            'call_multiplicities': {'validation': 1, 'sine': 6, 'Q46': 14,
                                    'memcpy_72_bytes': 1 if candidate else 0}}


before = analyze(PACKET / '00-reference', False)
after = analyze(PACKET / '04-candidate', True)
result = {'before': before, 'after': after,
          'scope': 'transform entry return and reachable callees; excludes callers and IRQ/NMI',
          'compiler_scratch': '216 resident bytes in each composed link; charged once',
          'limitations': 'Loose structural instruction bounds; no actual speed or CPU-cycle '
                         'WCET comparison. No wait-state, platform, interrupt or scheduler admission.',
          'stack_checker_sha256': hashlib.sha256(
              (ROOT / 'tools/flight_demo/m2/stack_check.py').read_bytes()).hexdigest()}
print(json.dumps(result, indent=2))
