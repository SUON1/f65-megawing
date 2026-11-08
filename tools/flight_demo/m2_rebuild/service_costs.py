"""Static costs for the sealed SERVICE1 link. No execution or grant assignment."""
from functools import lru_cache
from graphlib import TopologicalSorter
import hashlib
from heapq import heappop, heappush
import re

from linked_admission import image_bytes
from stack_admission import BRANCHES, branch_targets, parse

CPU_HZ = 40_500_000
ROLES = ('begin', 'prepare', 'project', 'background', 'copy_tile', 'line', 'text', 'commit')
PRG_SHA = '567a7b0425598ffc049d4b82bcd8bdd82c09d7aef6bcd8523ac1063cdda4fbdd'
TIMING_SHA = '6bb84846f83975acbdff5f16e39ebe7b5e08390cb68ed0cab2a85df311b4af58'


class Costs:
    def __init__(self, prg, disassembly, symbols, timings):
        if hashlib.sha256(prg).hexdigest() != PRG_SHA:
            raise ValueError('loop witnesses and limits apply only to the sealed SERVICE1 image')
        if hashlib.sha256(timings).hexdigest() != TIMING_SHA:
            raise ValueError('pinned Xemu timing table changed')
        self.instructions, self.names = parse(disassembly, symbols)
        branch_targets(self.instructions)
        for address, (_, _, raw) in self.instructions.items():
            if image_bytes(prg, address, len(raw)) != raw:
                raise ValueError(f'instruction/PRG mismatch at ${address:04x}')
        source = timings.decode()
        self.base = list(map(int, re.search(r'#define TIMINGS_65GS_FAST\s*\{([^}]+)\}', source)[1].split(',')))
        if len(self.base) != 256:
            raise ValueError('malformed timing table')
        self.prefix = {op: int(re.search(rf'#define MEGA_FOP_NOP_{op:02X}_CYCLES\s+(\d+)', source)[1])
                       for op in (0xb2, 0x92)}

    def cycles(self, address):
        _, _, raw = self.instructions[address]
        if raw[0] == 0xea and len(raw) > 1:
            return self.base[0xea] + self.prefix[raw[1]]
        if raw.startswith(b'\x42\x42'):
            raise ValueError('unsupported Q prefix')
        return self.base[raw[0]]

    def edges(self, address):
        op, operand, raw = self.instructions[address]
        if op in ('rts', 'rti'):
            return ()
        if op in BRANCHES or op in ('bra', 'jmp'):
            target = int(operand[1:], 16)
            # Xemu _BRA adds a page penalty relative to the operand address;
            # ultra-mode conditional short branches add two, long branches one.
            extra = 0
            if op != 'jmp' and len(raw) == 2:
                extra = (2 if op in BRANCHES else 0) + ((address + 1) >> 8 != target >> 8)
            elif op in BRANCHES:
                extra = 1
            taken = ((target, int(extra)),)
            return taken + (((address + len(raw), 0),) if op in BRANCHES else ())
        return ((address + len(raw), 0),)

    def callee(self, address):
        op, operand, _ = self.instructions[address]
        return int(operand[1:], 16) if op == 'jsr' else None

    @lru_cache(maxsize=None)
    def minimum(self, start, end=None, exclude=frozenset(), cuts=frozenset(),
                omit_calls=frozenset()):
        """Shortest linked path, permitting infeasible branches for a safe lower bound."""
        seen = set()
        queue = [(0, start)]
        while queue:
            cost, address = heappop(queue)
            if address == end:
                return cost
            if address in seen:
                continue
            seen.add(address)
            callee = self.callee(address)
            cycles = 0 if address in exclude else self.cycles(address)
            if callee is not None and callee not in omit_calls:
                cycles += self.minimum(callee, exclude=exclude)
            edges = self.edges(address)
            if not edges and end is None:
                return cost + cycles
            for target, extra in edges:
                if (address, target) not in cuts:
                    heappush(queue, (cost + cycles + extra, target))
        raise ValueError(f'no path from ${start:04x} to {end}')

    @lru_cache(maxsize=None)
    def upper(self, entry, loop_cap=0, omit_calls=frozenset(), stop_at=frozenset(),
              forced_cuts=frozenset()):
        """Overbound each acyclic path between explicitly bounded loop returns."""
        graph = {}
        pending = [entry]
        while pending:
            address = pending.pop()
            if address in graph:
                continue
            graph[address] = self.edges(address) if address not in stop_at else ()
            pending.extend(target for target, _ in graph[address])

        def reaches(start, end):
            pending = [start]
            seen = set()
            while pending:
                address = pending.pop()
                if address == end:
                    return True
                if address not in seen:
                    seen.add(address)
                    pending.extend(target for target, _ in graph[address]
                                   if (address, target) not in forced_cuts)
            return False

        cuts = {(address, target) for address, edges in graph.items() for target, _ in edges
                if (address, target) not in forced_cuts and target <= address and reaches(target, address)}
        if cuts and not loop_cap:
            raise ValueError(f'unbounded linked loop at ${entry:04x}: {sorted(cuts)}')

        longest = {}
        dag = {a: {b for b, _ in edges if (a, b) not in cuts | forced_cuts}
               for a, edges in graph.items()}
        for address in TopologicalSorter(dag).static_order():
            if address in stop_at:
                longest[address] = 0
                continue
            cycles = self.cycles(address)
            callee = self.callee(address)
            if callee is not None and callee not in omit_calls:
                cycles += self.upper(callee, CALL_CAPS.get(address, CAPS.get(callee, 0)))
            longest[address] = cycles + max(
                (extra + (longest[target] if target in dag[address] else 0)
                 for target, extra in graph[address]), default=0)
        return longest[entry] + loop_cap * max((longest[target] for _, target in cuts), default=0)


# Total feedback transfers per *invocation*, rounded up for alternative
# machine branches. All addresses and shapes are pinned by PRG_SHA above.
# Nested counts are products where required. The fallback memory/shift bounds
# use the actual machine count widths. The callsite caps below tighten those
# limits for the pinned runtime closure. These are CPU-only envelopes.
CAPS = {
    0x219c: 8 + 255,                     # request staging and byte transfer
    0x22f0: 6, 0x2367: 3,                # three-axis fixture loops
    0x2636: 8, 0x2667: 255, 0x2690: 8, 0x26db: 8, 0x26f0: 8, 0x27af: 8,
    0x297f: 6 + 7, 0x2b3e: 12 * 3 + 7, 0x2c7d: 7, 0x2ca5: 6,
    0x2d23: 12, 0x3935: 10 + 9 + 3,      # DELTA shift and bind port loops
    0x3d0d: 3, 0x3e01: 8,                # camera axes, raster endpoints
    0x41cc: 13 + 3 * 127,                 # 13 descriptors, 127 bytes total
    0x445b: 2 * 21 + 28 + 4 * 8,          # stages, <=28 shifts, <=8 commands per phase
    0x485b: 3, 0x48f0: 4 * 3,             # three immutable snapshot slots
    0x4adc: 6 * 3,                        # position and angle edges
    0x54e9: 8,                            # one scanline of eight tile pixels
    0x5970: 40 + 13, 0x5a17: 8 * 2, 0x5c48: 41 + 7 * (1 + 5),
    0x6100: 32, 0x6855: 32,              # coherent CIA sampler
    0x6e9d: 4, 0x7578: 13,               # physical request and keyboard rows
    0x780d: 65535, 0x7831: 65535, 0x786c: 65535,
    0x7888: 255, 0x7893: 255, 0x78a6: 255, 0x78b1: 255, 0x78c4: 255,
    0x78db: 3 * 16, 0x7981: 4 * 16, 0x7ac7: 6 * 32,  # shift and quotient loops
    0x7c79: 16, 0x7cab: 32,                # shift-and-add multiplication
}


# Pinned callsites that pass smaller bounds to SDK and arithmetic helpers.
# The byte counts are constants in the linked callers (A:X for memcpy/memcmp,
# X:$06 for __memset). The $4504 copy loads its constant length from $19.
# Runtime copy accepts at most 64 bytes. Shift widths follow the linked mask,
# shift modulo, digit, four-byte address or keyboard/glyph loop at each site.
CALL_CAPS = {
    0x23ab: 12, 0x23bc: 12, 0x2617: 12, 0x2630: 12, 0x277c: 8,
    0x2883: 12, 0x28fc: 6, 0x2915: 6, 0x2966: 19,
    0x2a70: 7, 0x2ad4: 7, 0x2bb6: 7, 0x2c2c: 8,
    0x3099: 8, 0x3222: 8, 0x3231: 8, 0x33a0: 8, 0x382e: 16,
    0x3bc3: 8, 0x3bd4: 8, 0x3c51: 12, 0x3c68: 12,
    0x4189: 18, 0x41b7: 4, 0x4268: 48,
    0x444a: 6, 0x4504: 6, 0x48ca: 13, 0x4b0e: 22, 0x4de5: 22,
    0x5135: 13, 0x5198: 22, 0x522d: 9, 0x531b: 9,
    0x5988: 40, 0x5a9d: 4, 0x5c8e: 64, 0x5ccc: 4,
    0x6f98: 24, 0x6fb0: 24, 0x6fcc: 8 + 64, 0x75a6: 12,
}


def measure(prg, disassembly, symbols, timing_source, host_log):
    model = Costs(prg, disassembly, symbols, timing_source)
    names = model.names
    fields = image_bytes(prg, names['m2_bundle_fields.fields'], 13 * 4)
    if sum(fields[3::4]) != 127:
        raise ValueError('linked registration field-byte accounting changed')
    row = re.search(r'^FRAME WORK ((?:\d+ ){8})DIVBITS (\d+) MULROWS (\d+) PIXELS (\d+)$', host_log, re.M)
    if row is None:
        raise ValueError('complete default frame witness missing')
    work = list(map(int, row[1].split()))
    divbits, mulrows, pixels = map(int, row.groups()[1:])
    if work != [1, 585, 5868, 5120, 960, 115, 320, 1] or (divbits, mulrows, pixels) != (3456, 1290, 96):
        raise ValueError('default frame witness changed')

    # The two loops alone are a disjoint lower bound. The byte loop executes
    # once for every successful COPY or LINE byte, the remainder loop once per
    # division bit (also a second time for rounding, excluded here).
    copy_body = {a for a in model.instructions if 0x21b9 <= a <= 0x21c1}
    remainder_body = {a for a in model.instructions if 0x2c83 <= a <= 0x2ca2}
    copy_byte = sum(model.cycles(a) for a in copy_body)
    div_bit = 7 * sum(model.cycles(a) for a in remainder_body)
    required_bytes = 64 * work[4] + pixels
    mandatory_copy = required_bytes * copy_byte
    mandatory_div = divbits * div_bit

    # The painter starts with Y=0, increments Y once after every pixel store
    # and cannot exit until Y=8. Split at its loop header, so the lower bound
    # counts all eight pixels and the actual compiler divide call in the setup.
    paint_prefix = model.minimum(names['background'], end=0x55af)
    pixel = model.minimum(0x55af, end=0x55ae, cuts=frozenset({(0x55b1, 0x55e4)}))
    pixel += model.cycles(0x55ae)
    paint_suffix = model.cycles(0x55af) + model.cycles(0x55b1) + model.minimum(0x55e4)
    paint_row = paint_prefix + 8 * pixel + paint_suffix

    # Camera equality loop fast path skips its high-count decrement. The
    # equal-byte path is mandatory for both memcmp calls (18 and 4 bytes).
    comparison = 0x783a
    equal_body = [a for a in model.instructions if 0x783a <= a <= 0x7852 and a != 0x784c]
    equal_byte = sum(model.cycles(a) for a in equal_body)
    checked_equal = 22 * equal_byte
    caller = frozenset({names['memcmp']})
    # On equality the eight-bit count starts positive; X stays zero, BNE at
    # $784a skips DEX, and $7852 repeats for every byte except the last.
    memcmp_fixed = (sum(model.cycles(a) for a in (0x7831, 0x7833, 0x7834, 0x7836, 0x7838,
                                                   0x7854, 0x7856, 0x7857, 0x7869, 0x786a, 0x786b)))
    memcmp_equal = sum(memcmp_fixed + length * (equal_byte + 2) + (length - 1) * 2
                       for length in (18, 4))
    minimum_camera = (model.minimum(names['m2_camera_same'], end=0x4189)
                      + model.minimum(0x4189, end=0x41b7, omit_calls=caller)
                      + model.minimum(0x41b7, end=0x41c7, omit_calls=caller)
                      + model.minimum(0x41c7) + memcmp_equal)
    omitted = frozenset(copy_body | remainder_body)
    roles = {}
    for role, count in zip(ROLES, work):
        at = names[role]
        minimum = paint_row if role == 'background' else model.minimum(at, exclude=omitted)
        roles[role] = {'address': at, 'successful_frame_calls': count,
                       'minimum_cycles_excluding_separate_copy_and_divider_body': minimum,
                       'maximum_cpu_cycles_with_rts': model.upper(at, CAPS.get(at, 0)),
                       'minimum_total_cycles_excluding_separate_loops': count * minimum}
    frame_core = sum(role['minimum_total_cycles_excluding_separate_loops'] for role in roles.values()) + mandatory_copy + mandatory_div

    irq = model.upper(names['r0f_pf_irq']) + 7
    nmi = model.upper(names['r0f_pf_nmi']) + 7
    helpers = {name: model.upper(names[name], CAPS.get(names[name], 0))
               for name in ('m1_platform_now', 'm2rb_guard', 'coherent', 'm2rb_io_fault', 'm2rb_io_commit',
                            'm1_tick', 'm2rb_platform_keys', 'm2rb_input_edges', 'm2rb_camera_edges',
                            'm1_platform_key', 'm1_input_sample')}
    role_calls = frozenset(names[name] for name in ROLES)
    dispatch = names['m2rb_dispatch']
    # The exact dispatch loop body begins at $503e. The back edge to that
    # header occurs only after another positive cost has been subtracted.
    loop_header = 0x503e
    loop_exits = frozenset({0x4fc2, 0x4f9f, 0x4fd8})
    repeat = frozenset({(0x5039, loop_header)})
    prefix = model.upper(dispatch, omit_calls=role_calls, stop_at=frozenset({loop_header}))
    exit_cost = max(model.upper(a) for a in loop_exits)
    continuation_overhead = model.upper(names['continuation'], stop_at=role_calls)
    step = model.upper(loop_header, omit_calls=frozenset({names['continuation']}),
                       stop_at=loop_exits, forced_cuts=repeat) + continuation_overhead
    # One outer scheduler iteration. Stop at the next clock read or reset-only
    # terminal fault; the dispatch body and its charged operations are separate.
    terminal_calls = frozenset(a for a in model.instructions if model.callee(a) == names['stop'])
    scheduler = model.upper(0x7653, omit_calls=frozenset({dispatch}),
                            stop_at=terminal_calls | {0x771e},
                            forced_cuts=frozenset({(0x7701, 0x7653), (0x771b, 0x7653)}))
    tick = model.upper(0x771e, stop_at=terminal_calls | {0x7653})
    allowance = CPU_HZ // 20
    return {
        'status': 'FAIL' if frame_core > allowance else 'UNPROVEN',
        'scope': 'pinned Xemu fast-mode instruction cycles, not execution or physical timing',
        'clock_hz': CPU_HZ, 'maximum_frame_cycles_at_20hz': allowance,
        'maximum_tick_cycles_at_100hz': CPU_HZ // 100,
        'roles': roles, 'helper_cpu_cycle_upper_bounds_with_returns': helpers,
        'hardware_interrupt_cpu_cycle_upper_bounds_including_entry': {'irq': irq, 'nmi': nmi},
        'outer_call_jsr_cycles': model.base[0x20], 'rts_cycles': model.base[0x60],
        'camera': {'equal_byte_cycles_minimum': equal_byte, 'byte_count': 22,
                   'full_equal_call_cycles_minimum': minimum_camera,
                   'full_equal_call_cpu_cycle_upper_bound': model.upper(names['m2_camera_same']),
                   'two_equal_byte_loops_per_ordinary_batch_minimum': 2 * checked_equal,
                   'memcmp_loop': comparison, 'ordinary_batches': 'two full checks; COMMIT checks three'},
        'copy': {'loop': min(copy_body), 'cycles_per_byte_minimum': copy_byte,
                 'required_bytes': required_bytes, 'frame_cycles_minimum': mandatory_copy},
        'division': {'loop': min(remainder_body), 'cycles_per_bit_minimum': div_bit,
                     'required_bits': divbits, 'frame_cycles_minimum': mandatory_div},
        'background': {'one_row_prefix_cycles_minimum': paint_prefix, 'one_pixel_cycles_minimum': pixel,
                       'one_row_suffix_cycles_minimum': paint_suffix, 'one_row_cycles_minimum': paint_row},
        'minimum_copy_plus_divider_cycles': mandatory_copy + mandatory_div,
        'minimum_complete_frame_cycles': frame_core,
        'minimum_complete_frame_ms': frame_core * 1000 / CPU_HZ,
        'optimistic_complete_frame_hz': CPU_HZ / frame_core,
        'frame_excludes': ['renderer dispatch/batch and coherence overhead', '100 Hz release, input and tick work',
                           'guard, clock, interrupts and publication-window waiting'],
        'batch_upper': {'fixed_dispatch_cycles_with_rts': prefix + exit_cost,
                        'per_ordinary_step_overhead_cycles': step,
                        'scheduler_cycles_including_clock_guard_dispatch_jsr': scheduler,
                        'two_raster_irqs_and_one_nmi_cycles': 2 * irq + nmi,
                        'fixed_cycles_with_interrupt_envelope': prefix + exit_cost + scheduler + 2 * irq + nmi,
                        'tick_path_after_release_decision_cpu_cycles': tick,
                        'tick_iteration_upper_including_clock_and_interrupts': tick + scheduler + 2 * irq + nmi,
                        'operation_cpu_cost': 'sum of admitted role bounds, including each continuation dispatch and iteration charge',
                        'additional_fixed_cost': 'clock sampling, main pre-dispatch/return, IRQ/NMI and timestamp uncertainty',
                        'whole_wall_time': 'UNPROVEN: native-count conversion, IRQ arrival and display-window timing require qualification'},
        'launch_and_native_count_grants': 'zero; CPU cycle envelopes do not authorize a nonzero budget',
    }
