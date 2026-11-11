"""PC gap verifier revision 2: correct normalization width; no executable grant.

Successor to the immutable 2026-11-11-m2-platform-clock/inspect_gap.py packet.
The coarse algorithm and all other bounds remain unchanged.
"""
from functools import lru_cache
from graphlib import TopologicalSorter
from pathlib import Path
from hashlib import sha256
import argparse
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/flight_demo/m2_rebuild'))
from fixed_preflight import check_identity, TickBounds
from service_costs import InstructionTiming
from wide_static import Bounds, PRG_SHA

# Source upper bounds on total loop feedback transfers per call. This deliberately
# includes extra visits and mutually exclusive branches; it is not a deadline.
CAPS = {
    'm1_acquire': 12, 'm2_camera_valid': 3, '__mulhi3': 16,
    'memcpy': 128, '__memset': 128, 'memcmp': 128,
    '__ashlhi3': 32, '__lshrhi3': 32, '__lshrqi3': 32, '__lshrsi3': 32,
    '__mulsi3': 32, '__modhi3': 0, '__umodhi3': 3 * 16,
    '__udivmodhi4': 4 * 16, '__udivmodsi4': 6 * 32,
    'm2_bundle_fields': 13 + 3 * 127, 'continuation': 8,
    'm2_fixture_segment': 3, 'm2_command_service': 12,
    'm2w_i32': 8, 'm2w_negate': 12, 'm2w_add': 8, 'm2w_double': 8,
    'm2w_compare': 8, 'm2w_narrow': 8,
    # Divisor count is 1..6; product count is 13 ($29B3): twelve feedbacks.
    'm2l_divide': 5 + 7 + 3, 'normalize': 12, 'remainder_ge': 6,
    'accumulate': 12, 'finish_multiply': 12 * 3 + 7, 'finish': 12 * 3 + 7,
    'm2rb_math_product': 4 + 4 + 8, 'math_transact': 4 + 4 + 8,
    'math_ready': 8, 'bind': 10 + 9, 'm2_point_valid': 6,
    'm2_raster_begin': 8, 'm2rb_text_row': 40 + 13, 'number': 8,
    'm2rb_glyph': 41 + 7 * (1 + 5), 'copy': 4,
    'r0f_pf_flat_copy': 8 + 64,
    'm2rb_platform_init': 32 * 3 + 4, 'initialize_store': 32 * 32 * 3 + 961,
    'm2rb_renderer_init': 32768,
    'm2rb_dispatch': 65535, 'cfnow': 32, 'm1_platform_now': 32,
    'cfratio': 32 + 16 + 6 * 32,
}


class Gap(InstructionTiming):
    graph = Bounds.graph

    def __init__(self, *args):
        super().__init__(*args)
        self.normalization = check_normalization(self)

    @lru_cache(None)
    def upper(self, entry):
        name = next(k for k, v in self.names.items() if v == entry)
        graph = self.graph(entry)
        # Identify real feedback edges, never branch direction alone.
        def reaches(start, end):
            todo, seen = [start], set()
            while todo:
                at = todo.pop()
                if at == end:
                    return True
                if at not in seen:
                    seen.add(at)
                    todo.extend(n for n, _ in graph[at])
            return False
        cuts = {(a, b) for a, edges in graph.items() for b, _ in edges
                if b <= a and reaches(b, a)}
        if cuts and name not in CAPS:
            raise ValueError(f'Unbounded dependency {name}: {cuts}')
        dag = {a: {b for b, _ in edges if (a, b) not in cuts}
               for a, edges in graph.items()}
        tuple(TopologicalSorter(dag).static_order())
        # Tarjan SCCs form an acyclic graph. Sum all instructions inside a
        # cyclic component times a conservative visit cap, then take the longest
        # component path. Calls after a loop are paid once, not per iteration.
        numbers, low, stack, live, components = {}, {}, [], set(), []
        def visit(at):
            numbers[at] = low[at] = len(numbers)
            stack.append(at)
            live.add(at)
            for nxt, _ in graph[at]:
                if nxt not in numbers:
                    visit(nxt)
                    low[at] = min(low[at], low[nxt])
                elif nxt in live:
                    low[at] = min(low[at], numbers[nxt])
            if low[at] == numbers[at]:
                component = []
                while True:
                    last = stack.pop()
                    live.remove(last)
                    component.append(last)
                    if last == at:
                        break
                components.append(component)
        visit(entry)
        owner = {at: i for i, members in enumerate(components) for at in members}
        cd = {i: {owner[b] for a in members for b, _ in graph[a] if owner[b] != i}
              for i, members in enumerate(components)}
        weights = {}
        cyclic_nodes = 0
        for i, members in enumerate(components):
            cyclic = len(members) > 1 or any(a == b for a in members for b, _ in graph[a])
            visits = CAPS.get(name, 0) + 1 if cyclic else 1
            cyclic_nodes += len(members) if cyclic else 0
            cost = 0
            for at in members:
                cost += self.cycles(at) + max((extra for _, extra in graph[at]), default=0)
                callee = self.callee(at)
                if callee is not None and callee != self.names['m2rb_text_row']:
                    cost += self.upper(callee)
            weights[i] = visits * cost
        lengths = {}
        for i in TopologicalSorter(cd).static_order():
            lengths[i] = weights[i] + max((lengths[n] for n in cd[i]), default=0)
        value = lengths[owner[entry]]
        self.results[name] = {'cpu_cycles': value,
                              'feedback': sorted([list(edge) for edge in cuts]),
                              'total_feedback_cap': CAPS.get(name, 0),
                              'cyclic_instruction_count': cyclic_nodes}
        return value


def check_normalization(model):
    """Pin the two source-proved call widths and their linked loop witness.

    The source-pinned positive divisor has used=1..6. The second call passes
    13 in A, and both calls enter count-1 countdown logic. A global cap of 12
    deliberately overbounds all divisor widths rather than specializing costs.
    """
    entry = model.names['normalize']
    calls = {at for at in model.instructions if model.callee(at) == entry}
    if entry != 0x2a0c or calls != {0x298f, 0x29b3}:
        raise ValueError('Normalization caller closure changed')
    expected = {
        0x29ab: ('lda', '#$d'), 0x29b3: ('jsr', '$2a0c'),
        0x2a44: ('dec', ''), 0x2a45: ('sta', '$19'),
        0x2a62: ('bra', '$2a93'), 0x2a85: ('dec', '$19'),
        0x2a93: ('lda', '$19'), 0x2a95: ('bne', '$2a64'),
    }
    if any(model.instructions.get(at, ())[:2] != shape for at, shape in expected.items()):
        raise ValueError('Normalization operand or countdown witness changed')
    widths = tuple(range(1, 7)) + (13,)
    required = max(widths) - 1
    if CAPS.get('normalize', -1) < required:
        raise ValueError('Normalization cap misses the 13-byte product call')
    return {'source_widths': list(widths), 'call_sites': [0x298f, 0x29b3],
            'required_feedback_cap': required, 'admitted_feedback_cap': CAPS['normalize'],
            'maximum_body_visits': required, 'maximum_guard_visits': required + 1}


def sampler():
    # A is exhaustive. For B only equality and a decrement are observed, so
    # these classes cover unchanged high byte, low-byte borrow and B reload.
    cases = accepted = rejected = 0
    for a in range(1, 65536):
        for b in (1, 2, 255, 256, 257, 65534, 65535):
            a2, b2 = a - 32, b
            if a2 <= 0:
                a2 += 65535
                b2 = b - 1 if b > 1 else 65535
            before = (b >> 8, b & 255, b >> 8, a >> 8, a & 255, a >> 8, b & 255, b >> 8)
            after = (b2 >> 8, b2 & 255, b2 >> 8, a2 >> 8, a2 & 255, a2 >> 8, b2 & 255, b2 >> 8)
            for split in range(9):
                bh, bl, bh2, ah, al, ah2, bl2, bh3 = before[:split] + after[split:]
                ok = bh == bh2 == bh3 and bl == bl2 and ah == ah2 and not (ah == 255 and al >= 240)
                cases += 1
                if ok:
                    accepted += 1
                    if ((ah << 8) | al, (bh << 8) | bl) not in ((a, b), (a2, b2)):
                        raise ValueError('Accepted torn counter pair')
                else:
                    rejected += 1
    return {'cases': cases, 'accepted_coherent': accepted, 'rejected': rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    options = parser.parse_args()
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=options.baseline).decode().strip()
    if head != '5c78bf7d00aadda0e63ce800e27fe3e142c651c0':
        raise ValueError('Preflight source baseline changed')
    sources = check_identity(options.baseline)
    refs = ROOT / 'docs/evidence/flight-demo/2026-11-11-m2-fixed-kernel-cost-correction/reference-identities.json'
    for name, expected in json.loads(refs.read_text())['files'].items():
        raw = (Path('/private/tmp/f65-m2-service-reference') / name).read_bytes()
        if {'bytes': len(raw), 'sha256': sha256(raw).hexdigest()} != expected:
            raise ValueError('Reference changed: ' + name)
    # Analyze the same sealed target whose source/metadata check_identity verified.
    target = options.baseline / 'docs/evidence/flight-demo/2026-11-09-m2-exact-wide/target'
    args = [(target / 'UNADMITTED.prg').read_bytes(),
            (target / 'UNADMITTED.disassembly').read_text(),
            (target / 'UNADMITTED.symbols').read_text(),
            Path('/private/tmp/f65-m2-service-reference/xemu/cpu65_mega65_timings.h').read_bytes(),
            PRG_SHA]
    model = Gap(*args)
    model.results = {}
    for name in ('begin', 'commit', 'continuation', 'coherent', 'm2rb_text_row',
                 'm2rb_platform_init', 'm2rb_renderer_init', 'm2rb_dispatch',
                 'cfnow', 'cfratio', 'm1_core_init', 'm2rb_camera_init', 'm2rb_guard'):
        model.upper(model.names[name])
    # Charge deferred text calls explicitly. One dispatch stops at COMMIT or
    # BEGIN/fault; tile_index increases once per COPY from 640 through 959.
    # TEXT constructs a row only at multiples of 40: at most eight calls.
    cost = lambda name: model.results[name]['cpu_cycles']
    dispatch = cost('m2rb_dispatch') + 8 * cost('m2rb_text_row')
    tick = TickBounds(*args).tick_iteration()
    # After clock start, at most 4,000,001 poll-condition visits, 17 samples
    # and one cfratio. Overcount every own adapter instruction per poll.
    calibration_graph = model.graph(0x62fd)
    calls = [model.callee(at) for at in calibration_graph if model.callee(at) is not None]
    if set(calls) != {model.names['cfnow'], model.names['cfratio']}:
        raise ValueError('Calibration closure changed')
    calibration_own = sum(model.cycles(at) + max((extra for _, extra in edges), default=0)
                          for at, edges in calibration_graph.items())
    calibration = calibration_own * 4000001 + 17 * cost('cfnow') + cost('cfratio')
    main_own = sum(model.cycles(at) + max((extra for _, extra in model.edges(at)), default=0)
                   for at in model.instructions if model.names['main'] <= at < model.names['memcpy'])
    initialization = (calibration + cost('m2rb_platform_init') + cost('m2rb_renderer_init')
                      + cost('m1_core_init') + cost('m2rb_camera_init') + main_own)
    runtime = dispatch + cost('m2rb_guard') + main_own + 2 * cost('cfnow')
    cpu = max(initialization, runtime, tick['iteration_cpu_cycles_upper'])
    # At most one conservatively costed raster interrupt per scanline is more than
    # the actual one-per-frame handler. One pending IRQ plus two partial-line
    # phases are included. NMI makes the proposed sampler fail closed, so no
    # successful-sample pair spans a nonterminal NMI path.
    irq = tick['irq_including_entry']
    lines = (cpu + irq + 1286) // (1287 - irq) + 2
    counts = 32 * lines + 64  # permit both endpoints' sampler staleness
    if counts >= 2**31:
        raise ValueError('Observation gap has no passing conservative envelope')
    window = sum(model.cycles(at) for at in model.instructions if 0x6c81 <= at < 0x6ca3)
    if window + irq >= 1287:
        raise ValueError('More than one CIA update may enter the eight reads')
    result = {
        'identity': '65AERO-M2-PLATFORM-CLOCK-GAP-2',
        'predecessor_seal_sha256': '0b0abb69eebb774bbba81203cb9f7b8a990b634c8b1e2968e28af091cc89e593',
        'normalization': model.normalization,
        'status': 'PASS: old caller/source preflight for host-only correction; no changed-image admission',
        'baseline': str(options.baseline), 'baseline_commit': head,
        'prg_sha256': PRG_SHA, 'source_count': len(sources), 'reference_count': 8,
        'eight_read_window_cycles': window, 'irq_cycles_including_entry': irq,
        'sampler': sampler(), 'bounds': model.results,
        'dispatch_cpu_cycles_including_eight_deferred_rows': dispatch,
        'calibration_whole_poll_envelope_cpu_cycles': calibration,
        'post_clock_initialization_cpu_cycles': initialization,
        'runtime_dispatch_interval_cpu_cycles': runtime,
        'old_tick_cpu_cycles': tick['iteration_cpu_cycles_upper'],
        'maximum_old_caller_cpu_cycles': cpu, 'native_counts_upper': counts,
        'strict_native_count_limit': 2**31, 'margin_native_counts': 2**31 - counts,
        'candidate_clock_target_cost': 'UNMEASURED; future exact-image gap, stack, size and deadline recheck required',
        'new_target_execution_or_link': False,
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
