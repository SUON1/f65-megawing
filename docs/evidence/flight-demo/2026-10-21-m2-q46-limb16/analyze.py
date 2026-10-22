"""Read-only accounting of retained linked artifacts; never execute a target.

Instruction bounds are structural overcounts, not CPU-cycle WCET admission.
Each whole routine's instruction inventory is multiplied by a safe maximum
visit count, then bounded callee costs are added at the call multiplicity.
"""
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tools/flight_demo/m2'))
from stack_check import check


def analyze(path, after):
    text = (path / 'RENDER.disassembly').read_text()
    blocks = {m[2]: (int(m[1], 16), m[0]) for m in re.finditer(
        r'^([0-9a-f]+) <([^>]+)>:\n.*?(?=^[0-9a-f]+ <|\Z)', text, re.M | re.S)}
    wanted = {'m2_multiply_q46'}
    pending = list(wanted)
    while pending:
        name = pending.pop()
        for callee in re.findall(r'\bjsr\s+\$[0-9a-f]+\s+<([^>+]+)(?:\+[^>]*)?>',
                                 blocks[name][1]):
            if callee not in wanted:
                wanted.add(callee)
                pending.append(callee)
    expected = {'m2_multiply_q46', '__mulsi3', '__memset'} if after else {
        'm2_multiply_q46', '__muldi3'}
    assert wanted == expected, wanted
    subset = '\n'.join(blocks[n][1] for n in sorted(wanted, key=lambda n: blocks[n][0]))
    subset = subset.replace('<m2_multiply_q46>:', '<main>:')
    stack = check(subset)
    inventory = {n: len(re.findall(r'^\s*[0-9a-f]+:\s+', blocks[n][1], re.M))
                 for n in wanted}
    if after:
        # Own inner-loop header: four visits per outer iteration, three outers.
        # Other own instructions execute at most nine/three/one times.
        # Each __mulsi3 operand is a zero-extended uint16; <=16 shift iterations.
        bound = inventory['m2_multiply_q46'] * 12 + 9 * inventory['__mulsi3'] * 17 \
            + inventory['__memset'] * 13
        formula = '526*12 + 9*64*17 + 15*13'
        assumptions = ['three extraction iterations', 'three rows x three product cells',
                       'inner guard visited at most 12 times', 'nine 16x16 products',
                       'one 12-byte zero-fill', 'library multiplication shifts one bit per iteration']
    else:
        # Own helper has no loops. All four __muldi3 operands are 23-bit low
        # limbs or <=2^23 high limbs, hence at most 24 significant bits.
        bound = inventory['m2_multiply_q46'] + 4 * inventory['__muldi3'] * 25
        formula = '562 + 4*150*25'
        assumptions = ['own helper acyclic', 'four __muldi3 calls',
                       'both factors per call have at most 24 significant bits',
                       'library multiplication shifts one bit per iteration']
    return {'helper_stack': stack, 'instruction_inventory': inventory,
            'conservative_instruction_bound': bound, 'formula': formula,
            'assumptions': assumptions,
            'cost_limitations': 'Counts include calls and bounded callee instructions, not cycle timings. Uniform inventory multipliers overcount paths; bound comparison does not establish a speed improvement/regression. No platform/interrupt/wait-state or dispatcher WCET admission.'}


before = ROOT / 'docs/evidence/flight-demo/2026-10-21-m2-generation-cache/02-fit-failure'
after = Path(__file__).resolve().parent / 'relink'
result = {'before': analyze(before, False), 'after': analyze(after, True),
          'stack_checker_sha256': hashlib.sha256((ROOT / 'tools/flight_demo/m2/stack_check.py').read_bytes()).hexdigest(),
          'hardware_stack_scope': 'helper entry return address plus reachable helper calls only; excludes callers and IRQ/NMI',
          'target_cycles': 'UNPROVEN; structural instruction bounds are not cycle bounds'}
print(json.dumps(result, indent=2))
