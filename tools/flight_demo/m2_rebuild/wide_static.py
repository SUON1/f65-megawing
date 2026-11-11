"""Review the exact linked opt-in arithmetic candidate without executing it."""
import argparse
from collections import defaultdict
from functools import lru_cache
from graphlib import TopologicalSorter
from hashlib import sha256
import json
from pathlib import Path
import re

from linked_admission import check_application_mapping, check_initialization, elf_sections
from service_costs import InstructionTiming
from stack_admission import Graph, WRITES, check as stack_check, stack_effects
from wide_validate import ROOT, seal

PRG_SHA = "7fdcea61387c0e6b7ae92310725966ac6c0e29e82e8ba1c9a6be77335af76aad"
TARGET_SEAL_SHA = "e906a9472db26272268137773be4c0dd220bb264bd9ff10f1f2b88ef0bce518a"
FAST_HZ = 40_500_000
IRQ_ENTRY = 7
CLIP_DIVISIONS = 9 * 6 * 3
PERSPECTIVE_DIVISIONS = 9 * 2 * 2

# The exact link turns loops into the following return edges. Counts are
# taken-edge caps, grouped when the compiler emits alternate loop entries.
FIXED_LOOPS = [
    (8, "wide signed comparison: eight equal-byte advances", [(0x2735, 0x2701)]),
    (5, "at most five leading zero divisor bytes", [(0x296e, 0x2962)]),
    (7, "at most seven shifts of the nonzero top divisor byte", [(0x2978, 0x2974)]),
    (3, "at most three leading zero quotient windows", [(0x29f6, 0x29d1)]),
    (6, "remainder comparison: six equal-byte advances", [(0x2b15, 0x2af4)]),
    (12, "result carry and signed narrowing: twelve bytes",
     [(0x2f77, 0x2f16), (0x2f86, 0x2f1c), (0x2f8b, 0x2f32)]),
    (7, "signed-minimum validation: seven low zero bytes", [(0x2ffa, 0x2fee)]),
    (10, "bind ten private Graphics registers", [(0x3d94, 0x3d68)]),
    (9, "bind nine prepared rotation elements", [(0x3de9, 0x3dc5)]),
    (8, "signed addition: eight bytes", [(0x26d7, 0x269a)]),
    (32, "coherent clock sample: at most 32 failed attempts",
     [(at, 0x6c76) for at in (0x6ca5, 0x6cab, 0x6cb5, 0x6cbe, 0x6ccd)]),
    (4, "write four operand pairs", [(0x7a70, 0x7a45)]),
    (4, "read four quotient bytes", [(0x7aae, 0x7a98)]),
    (8, "read eight product bytes", [(0x7ac8, 0x7ab4)]),
    (8, "at most eight busy status reads", [(0x7b15, 0x7b0d)]),
]
PARAMETER_LOOPS = [
    ("byte negation", [(0x268d, 0x2671)]),
    ("normalization after reading the top byte", [(0x2a95, 0x2a64)]),
    ("add/subtract width", [(0x2eba, 0x2e81)]),
    ("SDK copy after first byte", [(0x7d96, 0x7d87), (0x7d99, 0x7d87)]),
    ("SDK fill after first byte", [(0x7dec, 0x7ddf), (0x7df0, 0x7ddf)]),
    ("SDK shift after first bit", [(0x7e01, 0x7dfb), (0x7e1f, 0x7e19)]),
]
CALL_LIMITS = {
    0x2883: 17, 0x28fc: 5, 0x2915: 6, 0x277c: 7,
    0x298f: 5, 0x29a0: 5, 0x29b3: 12, 0x29c4: 11,
    0x2a50: 6, 0x2a76: 6, 0x2aab: 4, 0x2ba5: 6,
    0x2c44: 3, 0x2c78: 3, 0x2cdb: 12, 0x2dca: 9,
    0x2de9: 3, 0x2e22: 9, 0x2e3e: 3, 0x2f38: 6, 0x2fae: 8,
    0x3076: 9, 0x30bb: 5, 0x34b6: 7, 0x7af8: 7,
}
RESTRICTED_EDGES = {
    "raw_multiply": [(0x2b30, 0x2b60)],
    "raw_finish": [(0x2d03, 0x2d11), (0x2d09, 0x2d1b)],
    "divide_more": [(0x2b30, 0x2b32), (0x2b7d, 0x2b86)],
    "divide_last": [(0x2b30, 0x2b32), (0x2b7d, 0x2b7f)],
    "division_finish": [(0x7e15, 0x7e17)],
    "product_result": [(0x7a80, 0x7a82), (0x7a92, 0x7a94)],
    "quotient_result": [(0x7a80, 0x7a8f), (0x7a92, 0x7ab0)],
}


class Bounds(InstructionTiming):
    def graph(self, entry, cuts=(), stop=None):
        graph = {}
        pending = [entry]
        while pending:
            at = pending.pop()
            if at in graph:
                continue
            graph[at] = () if at == stop else tuple(
                (next_at, extra) for next_at, extra in self.edges(at) if (at, next_at) not in cuts)
            pending.extend(next_at for next_at, _ in graph[at])
        return graph

    @lru_cache(maxsize=None)
    def upper(self, entry, limit=None, variant=None, through=None):
        graph = self.graph(entry, RESTRICTED_EDGES.get(variant, ()), stop=through)
        if through is not None:
            predecessors = defaultdict(set)
            for at, edges in graph.items():
                for target, _ in edges:
                    predecessors[target].add(at)
            retained = {through}
            pending = [through]
            while pending:
                for parent in predecessors[pending.pop()] - retained:
                    retained.add(parent)
                    pending.append(parent)
            if entry not in retained:
                raise ValueError("callsite is unreachable")
            graph = {at: tuple((target, extra) for target, extra in graph[at] if target in retained)
                     for at in retained}
        edges = {(at, target) for at, successors in graph.items() for target, _ in successors}
        groups = []
        for cap, _, group in FIXED_LOOPS:
            if edges.intersection(group):
                groups.append((cap, group))
        for reason, group in PARAMETER_LOOPS:
            if edges.intersection(group):
                if limit is None:
                    raise ValueError(f"missing linked loop cap for {reason} at ${entry:04x}")
                groups.append((limit, group))
        groups_by_edge = {edge: index for index, (_, group) in enumerate(groups) for edge in group}
        # A changed or missing loop witness must leave a cycle here and fail.
        tuple(TopologicalSorter({at: {target for target, _ in successors
                                    if (at, target) not in groups_by_edge}
                                for at, successors in graph.items()}).static_order())
        return self.longest(graph, entry, groups, groups_by_edge, variant, through)

    def longest(self, graph, entry, groups, groups_by_edge, variant, stop):
        weights = {}
        for at in graph:
            # through marks the JSR instruction. Charge that instruction but
            # let the caller add the appropriate operand-conditioned callee.
            weights[at] = self.cycles(at)
            callee = self.callee(at)
            if callee is None or at == stop:
                continue
            subvariant = {0x2b5a: "raw_finish", 0x2bc0: "division_finish",
                          0x7b31: "quotient_result"}.get(at)
            if at == 0x2f38 and variant == "division_finish":
                subvariant = "division_finish"
            if callee == self.names["m2rb_math_product"]:
                subvariant = "product_result"
            if subvariant == "raw_finish" and variant != "raw_multiply":
                raise ValueError("raw product assumption outside clip numerator")
            weights[at] += self.upper(callee, CALL_LIMITS.get(at), subvariant)

        # Counters only increase. The expanded graph is a finite DAG. A path
        # that tries to exceed a cap is infeasible, including on a fault edge.
        root = (entry, (0,) * len(groups))
        states = {}
        pending = [root]
        while pending:
            state = pending.pop()
            if state in states:
                continue
            at, counts = state
            successors = []
            for target, extra in graph[at]:
                index = groups_by_edge.get((at, target))
                updated = counts
                if index is not None:
                    if counts[index] == groups[index][0]:
                        continue
                    updated = counts[:index] + (counts[index] + 1,) + counts[index + 1:]
                successors.append(((target, updated), extra))
            states[state] = successors
            pending.extend(successor for successor, _ in successors)
        order = TopologicalSorter({state: {s for s, _ in successors}
                                   for state, successors in states.items()}).static_order()
        values = {}
        for state in order:
            at = state[0]
            if not graph[at]:
                if at != stop and self.instructions[at][0] not in ("rts", "rti"):
                    raise ValueError(f"non-return terminal at ${at:04x}")
                values[state] = weights[at]
            else:
                choices = [values[s] + extra for s, extra in states[state] if values[s] is not None]
                values[state] = weights[at] + max(choices) if choices else None
        if values[root] is None:
            raise ValueError("no bounded return")
        return values[root]

    def command_overhead(self, callsite):
        if not self.callee(callsite):
            raise ValueError("expected a numeric JSR")
        start = self.names["m2_command_service"]
        tail = callsite + len(self.instructions[callsite][2])
        return self.base[0x20] + self.upper(start, through=callsite) + self.upper(tail)


def ownership(model):
    instructions, names = model.instructions, model.names
    effects = stack_effects(instructions, names)
    foreground = Graph(instructions, effects)
    foreground.walk(names["__do_init_stack"])
    irq = Graph(instructions)
    irq.walk(names["r0f_pf_irq"], "interrupt")
    irq.walk(names["r0f_pf_nmi"], "interrupt")
    if irq.call_edges or foreground.reachable & irq.reachable:
        raise ValueError("foreground and interrupt control flow are not exclusive")
    prefix = {at for at in instructions if names["m2rb_startup"] <= at < names["__do_init_stack"]}
    live = foreground.reachable | irq.reachable | prefix
    absolute = set()
    constructions = set()
    far = set()
    dma = set()
    for at in live:
        op, operand, _ = instructions[at]
        match = re.fullmatch(r"\$([0-9a-f]+)(?:,([xyz]))?", operand)
        if match:
            first = int(match[1], 16)
            last = first + (255 if match[2] else 0)
            if first <= 0xd70f <= last or first <= 0xd7bf and last >= 0xd768:
                absolute.add(at)
            if op in WRITES and first <= 0xd70e and last >= 0xd700:
                dma.add(at)
        if operand == "#$d7":
            constructions.add(at)
        if "[" in operand:
            far.add(at)
    if absolute != {0x7a32, 0x7b10} or constructions != {0x7a51, 0x7a65, 0x7aa0, 0x7abc}:
        raise ValueError("unreviewed linked math register address or construction")
    if dma or far != {0x21b9, 0x21bc} or (absolute | constructions) & irq.reachable:
        raise ValueError("unreviewed DMA, physical pointer or interrupt access")
    if {(a, b) for a, b in foreground.call_edges if b == names["r0f_pf_flat_copy"]} \
            != {(0x673f, 0x219c), (0x73e9, 0x219c)}:
        raise ValueError("unreviewed physical-copy caller")
    # Match the actual pointer constructions, which are indirect instructions
    # in this link. Y ranges over [0,4), X over [0,4) or [0,8), and Z is zero
    # under the startup / PF001 ABI. No other register parameter enters them.
    sequences = {
        0x7a49: "98 18 69 70 85 08 a9 00 69 d7 85 09 a5 0a 92 08",
        0x7a5d: "98 18 69 74 85 08 a9 00 69 d7 85 09 a5 0a 92 08",
        0x7a98: "8a 18 69 69 85 04 a9 00 69 d7 85 05 b2 04",
        0x7ab4: "8a 18 69 78 85 04 a9 00 69 d7 85 05 b2 04",
    }
    for start, expected in sequences.items():
        cursor = start
        raw = b""
        while len(raw) < len(bytes.fromhex(expected)):
            code = instructions[cursor][2]
            raw += code
            cursor += len(code)
        if raw != bytes.fromhex(expected):
            raise ValueError("math register pointer loop changed")
    destinations = {names[name] for name in
                    ("m2rb_math_product", "m2rb_math_q24", "math_transact", "math_ready")}
    calls = {(a, b) for a, b in foreground.call_edges if b in destinations}
    if calls != {(0x2c93, 0x79e7), (0x3055, 0x79e7), (0x3094, 0x79e7),
                 (0x2d51, 0x7b1d), (0x7b31, 0x79ec), (0x7a72, 0x7b0b)}:
        raise ValueError("math call ownership changed")
    entry = names["math_transact"]
    data_accesses = {0x7a57, 0x7a6b, 0x7aa4, 0x7ac0}
    if data_accesses.intersection(model.graph(entry, stop=0x7a3e)):
        raise ValueError("math access can bypass owner acquisition")
    if {0x7aa4, 0x7ac0}.intersection(model.graph(entry, cuts=[(0x7a76, 0x7a78)])):
        raise ValueError("math output read can bypass readiness")
    owner = names["math_owner"]
    owner_uses = {at for at in live if instructions[at][1] == f"${owner:x}"}
    if owner_uses != {0x79ec, 0x7a3e, 0x7a88, 0x7aca, 0x7b05}:
        raise ValueError("unexpected owner-byte access")
    return {
        "status": "PASS: linked application scope",
        "reachable_instruction_counts": {"foreground_and_prefix": len(foreground.reachable | prefix),
                                          "irq_and_nmi": len(irq.reachable)},
        "cpu_status": "D70F", "cpu_operand_and_result_window": "D768-D77F",
        "physical_status": "FFD370F", "physical_operand_and_result_window": "FFD3768-FFD377F",
        "indexed_or_indirect_bus_sites": sorted(data_accesses), "absolute_status_sites": sorted(absolute),
        "calls": sorted(calls), "long_indirect_sites": sorted(far), "owner_byte": owner,
        "conditions": ["Canonical MEGA65 I/O, unchanged MAP/B and Z=0 for C entry.",
                       "Private pointers derive from linked RAM/stack objects or reviewed I/O classes.",
                       "The two PF001 far accesses use the checked CF001 copy and M2 store/color ranges.",
                       "The reset-only privileged trap precedes arithmetic. External concurrent masters are outside this proof."],
    }


def cycle_report(model):
    names = model.names
    setup_multiply = model.upper(names["m2l_multiply"])
    setup_divide = model.upper(names["m2l_divide"])
    multiply = model.upper(names["m2l_service"], variant="raw_multiply")
    more = model.upper(names["m2l_service"], variant="divide_more")
    last = model.upper(names["m2l_service"], variant="divide_last")
    outer_jsr = model.base[0x20]
    product = model.upper(names["m2rb_math_product"], variant="product_result") + outer_jsr
    quotient = model.upper(names["m2rb_math_q24"]) + outer_jsr
    numerator = setup_multiply + 4 * multiply + 5 * outer_jsr
    division = setup_divide + more + last + 3 * outer_jsr
    adapter = {"multiply_setup": model.command_overhead(0x3912),
               "divide_setup": model.command_overhead(0x3559),
               "service": model.command_overhead(0x3512)}
    command = numerator + division - 8 * outer_jsr + adapter["multiply_setup"] \
        + adapter["divide_setup"] + 6 * adapter["service"]
    irq = model.upper(names["r0f_pf_irq"]) + IRQ_ENTRY
    nmi = model.upper(names["r0f_pf_nmi"]) + IRQ_ENTRY
    count = CLIP_DIVISIONS + PERSPECTIVE_DIVISIONS
    return {
        "scope": "Conservative fast-mode instruction-cycle bounds from raw linked code. Includes eight-poll timeout, calls and returns.",
        "clock_hz": FAST_HZ, "multiply_gateway_cycles": product, "estimate_gateway_cycles": quotient,
        "callee_bounds_with_return": {"product_setup": setup_multiply, "raw_product_step": multiply,
                                      "divide_setup": setup_divide, "divide_nonfinal_digit": more,
                                      "divide_final_digit": last},
        "standalone_including_outer_calls": {"raw_numerator": numerator, "two_digit_divide": division,
                                             "numerator_and_division": numerator + division},
        "linked_command_overhead_excluding_arithmetic_callees": adapter,
        "clip_or_perspective_numerator_and_divide_cycles_with_commands": command,
        "largest_single_arithmetic_command_cycles": max(
            setup_multiply + adapter["multiply_setup"], setup_divide + adapter["divide_setup"],
            max(multiply, more, last) + adapter["service"]),
        "linked_irq_cycles_including_entry": irq, "linked_nmi_cycles_including_entry": nmi,
        "guard_and_one_clock_sample_including_calls": model.upper(names["m2rb_guard"])
        + model.upper(names["cfnow"]) + 2 * outer_jsr,
        "clip_interpolations": CLIP_DIVISIONS, "perspective_divisions": PERSPECTIVE_DIVISIONS,
        "clip_interpolations_only_cycles_without_products_or_commands": CLIP_DIVISIONS * division,
        "frame_envelope_for_divisions_only": count * division,
        "frame_envelope_for_products_divisions_and_commands": count * command,
        "numeric_planning_cycles_per_frame": 800_000,
        "excluded_from_frame_envelopes": "Geometry transforms, DELTA, scheduler/dispatch, IRQ/NMI, display and commit.",
        "physical_wall_clock": "UNPROVEN: FPGA and bus wait-state latency are separate from the capped instruction path.",
    }


def check_sealed_target(target):
    seal_bytes = (target / "seal.json").read_bytes()
    if sha256(seal_bytes).hexdigest() != TARGET_SEAL_SHA:
        raise ValueError("target seal identity changed")
    members = json.loads(seal_bytes)
    actual = {str(path.relative_to(target)) for path in target.rglob("*")
              if path.is_file() and path != target / "seal.json"}
    if actual != set(members):
        raise ValueError("sealed target inventory changed")
    for name, identity in members.items():
        raw = (target / name).read_bytes()
        if len(raw) != identity["bytes"] or sha256(raw).hexdigest() != identity["sha256"]:
            raise ValueError("sealed target member changed: " + name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--timings", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    check_sealed_target(args.target)
    prg = (args.target / "UNADMITTED.prg").read_bytes()
    disassembly = (args.target / "UNADMITTED.disassembly").read_text()
    symbols = (args.target / "UNADMITTED.symbols").read_text()
    model = Bounds(prg, disassembly, symbols, args.timings.read_bytes(), PRG_SHA)
    report = {"prg_sha256": PRG_SHA, "target_seal_sha256": TARGET_SEAL_SHA,
              "ownership": ownership(model), "cycles": cycle_report(model),
              "stack": stack_check(disassembly, symbols),
              "initialization": check_initialization(prg, disassembly, symbols),
              "mapping": check_application_mapping(disassembly, symbols),
              "resident_fit": "FAIL", "target_executed": False}
    sections = elf_sections((args.target / "UNADMITTED.prg.elf").read_bytes())
    contract = json.loads((ROOT / "interfaces/m2_extended_resident.json").read_text())
    start, ceiling = contract["development_resident"]
    end = max(section["address"] + section["bytes"] for section in sections.values())
    report["resident"] = {"required": end - start, "limit": ceiling - start,
                          "deficit": end - ceiling, "reserve": 0,
                          "bss": sections[".bss"]["bytes"], "scratch": sections[".noinit"]["bytes"],
                          "payload": len(prg) - 2, "excess_resident_range": [ceiling, end]}
    if end <= ceiling or end >= contract["software_stack"][0]:
        raise ValueError("unexpected allocation for the failed-fit image")
    if not sections[".bss"]["address"] <= model.names["math_owner"] < sections[".noinit"]["address"]:
        raise ValueError("math owner is not reset by the linked BSS initialization")
    args.output.mkdir()
    (args.output / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    seal(args.output)
    print(json.dumps(report["cycles"], indent=2))


if __name__ == "__main__":
    main()
