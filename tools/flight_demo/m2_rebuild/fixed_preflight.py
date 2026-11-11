"""Read-only, exact-image tick analysis for the FK preflight; never a grant.

Visit ceilings are source/control-flow witnesses for the pinned old executable.
Sum both sides of every branch, including terminal paths: this intentionally
overbounds execution. No instruction emulator, compiler or linker is invoked.
"""
import argparse
from functools import lru_cache
from graphlib import TopologicalSorter
from hashlib import sha256
import json
from pathlib import Path
import subprocess

from service_costs import InstructionTiming
from wide_static import PRG_SHA, TARGET_SEAL_SHA

ROOT = Path(__file__).resolve().parents[3]
TARGET = Path("docs/evidence/flight-demo/2026-11-09-m2-exact-wide/target")

# Each listed interval overrides the default visit ceiling. End is exclusive.
# The linked single producer queues at most one command for the immediately
# following tick. Stage 3 drains it; the future-command checksum/shift loops
# therefore have zero iterations. We still charge their instructions twice.
# The stage dispatcher is visited 22 times, and its increment 21 times.
VISITS = {
    "m1_tick": (2, [(0x48cd, 0x4908, 22), (0x4b76, 0x4b7e, 21)]),
    "m1_publish": (1, [(0x4c82, 0x4c9c, 4)]),
    "m2rb_camera_edges": (1, [(0x4f3e, 0x5056, 4), (0x508d, 0x5157, 4)]),
    "m2_camera_valid": (1, [(0x41b1, 0x4218, 4)]),
    "m2rb_platform_keys": (1, [(0x79ad, 0x79d6, 14)]),
    "m1_platform_now": (1, [(0x6c76, 0x6cd2, 33)]),
    "__mulhi3": (1, [(0x81e8, 0x8203, 16)]),
}

# Removing these *actual cycle* edges must make each function acyclic.
# Caps arise from the source invariants above, not from edge direction alone.
FEEDBACK = {
    "m1_tick": {(0x4b7b, 0x48cd), (0x4b6a, 0x4b27), (0x4b41, 0x4b20),
                (0x497d, 0x4934), (0x4936, 0x4908), (0x4aa1, 0x4a0e)},
    "m1_publish": {(0x4c9a, 0x4c82)},
    "m2rb_camera_edges": {(0x503b, 0x4f3e), (0x50ed, 0x50ef)},
    "m2_camera_valid": {(0x4215, 0x41b1)},
    "m2rb_platform_keys": {(0x79d4, 0x79ad)},
    "m1_platform_now": {(a, 0x6c76) for a in
                        (0x6ca5, 0x6cab, 0x6cb5, 0x6cbe, 0x6ccd)},
    "__mulhi3": {(0x81fd, 0x81e8), (0x8201, 0x81e8)},
    "memcpy": {(0x7d96, 0x7d87), (0x7d99, 0x7d87)},
    "memcmp": {(0x7db9, 0x7da5), (0x7dbd, 0x7da5)},
    "__ashlhi3": {(0x7e01, 0x7dfb)},
}
CALL_LENGTHS = {
    0x4921: 6, 0x4867: 6, 0x4ce7: 13, 0x4f2b: 22, 0x5202: 22,
    0x45a6: 18, 0x45d4: 4, 0x79c3: 12,
}
ACYCLIC = {
    "m1_input_sample", "m1_command", "m1_extract", "m2rb_camera_init",
    "m2rb_camera_equal", "clamp", "m2rb_input_edges", "m1_platform_key",
    "m1_platform_fault", "r0f_pf_irq", "r0f_pf_nmi",
}
SOURCES = [
    "src/core/m1_runtime.c", "src/input/m1_input.c",
    "src/presentation/m1_snapshot.c", "src/diagnostics/m2_rebuild/main.c",
    "src/diagnostics/m2_rebuild/camera.c", "src/input/m2_rebuild_input.c",
    "src/platform/m1/m1_platform.c", "src/platform/m2_rebuild/platform.c",
    "src/diagnostics/r0f/combined_platform.c",
    "src/graphics/m2_record_private.c", "src/platform/r0f/qualification_45gs02.s",
]


def check_identity(root):
    target = root / TARGET
    raw = (target / "seal.json").read_bytes()
    if sha256(raw).hexdigest() != TARGET_SEAL_SHA:
        raise ValueError("target seal identity changed")
    seal = json.loads(raw)
    for name, expected in seal.items():
        data = (target / name).read_bytes()
        if len(data) != expected["bytes"] or sha256(data).hexdigest() != expected["sha256"]:
            raise ValueError(f"sealed target member changed: {name}")
    result = json.loads((target / "result.json").read_text())
    for name in SOURCES:
        if sha256((root / name).read_bytes()).hexdigest() != result["inputs"][name]:
            raise ValueError(f"source invariant identity changed: {name}")
    # Pin every target source/generated input, including headers and inline
    # geometry helpers, not only the files explaining the loop witnesses.
    sources = {name: digest for name, digest in result["inputs"].items()
               if name.startswith(("src/", "interfaces/generated/"))}
    for name, digest in sources.items():
        if sha256((root / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f"target input identity changed: {name}")
    return sources


class TickBounds(InstructionTiming):
    def check_producers(self):
        expected = {"m1_input_sample": {0x7c9b}, "m1_tick": {0x7c9e},
                    "m1_command": {0x4bff}}
        for name, calls in expected.items():
            actual = {at for at in self.instructions if self.callee(at) == self.names[name]}
            if actual != calls:
                raise ValueError(f"single producer/tick call graph changed: {name}")

    def graph(self, entry):
        graph = {}
        pending = [entry]
        while pending:
            at = pending.pop()
            if at in graph:
                continue
            graph[at] = self.edges(at)
            pending.extend(target for target, _ in graph[at])
        return graph

    @staticmethod
    def check_cycles(graph, feedback):
        edges = {(at, target) for at, successors in graph.items() for target, _ in successors}
        if not feedback <= edges:
            raise ValueError("missing feedback witness")
        tuple(TopologicalSorter({at: {target for target, _ in successors
                                     if (at, target) not in feedback}
                                 for at, successors in graph.items()}).static_order())

    @lru_cache(maxsize=None)
    def bound(self, name, length=None):
        if name not in VISITS and name not in ACYCLIC and name not in ("memcpy", "memcmp", "__ashlhi3"):
            raise ValueError(f"unreviewed tick dependency: {name}")
        graph = self.graph(self.names[name])
        self.check_cycles(graph, FEEDBACK.get(name, set()))
        default, intervals = VISITS.get(name, (1, []))
        if name in ("memcpy", "memcmp", "__ashlhi3"):
            if length is None or not 0 <= length <= 22:
                raise ValueError("missing/invalid operand-derived SDK limit")
            # Overcount prologue, exit and both branches for every byte/shift.
            default = length + 1
        total = 0
        for at, edges in graph.items():
            visits = next((cap for low, high, cap in intervals if low <= at < high), default)
            cost = self.cycles(at) + max((extra for _, extra in edges), default=0)
            callee = self.callee(at)
            if callee is not None:
                names = [key for key, value in self.names.items() if value == callee]
                if len(names) != 1:
                    raise ValueError("ambiguous linked callee")
                cost += self.bound(names[0], CALL_LENGTHS.get(at))
            total += visits * cost
        return total

    def tick_iteration(self):
        self.check_producers()
        # Current iteration's fault or due-tick path, plus the tick-600 copy.
        # Exclude only the not-due edge. Stop at loop re-entry or terminal entry.
        root = 0x7bbe
        graph = {}
        pending = [root]
        while pending:
            at = pending.pop()
            if at in graph:
                continue
            terminal = self.callee(at) == self.names["stop"]
            graph[at] = () if terminal else tuple(
                (target, extra) for target, extra in self.edges(at)
                if target != root and (at, target) != (0x7bfe, 0x7c03))
            pending.extend(target for target, _ in graph[at])
        self.check_cycles(graph, set())
        own, callees = 0, {}
        for at, edges in graph.items():
            own += self.cycles(at) + max((extra for _, extra in edges), default=0)
            callee = self.callee(at)
            if callee is None:
                continue
            name = next(name for name, value in self.names.items() if value == callee)
            # stop records the reason, then loops forever. Only the bounded
            # transition to terminal is charged, never a claim of return.
            cost = self.cycles(callee) if name == "stop" else self.bound(name)
            callees[f"{at:04x}:{name}"] = cost
        irq = self.bound("r0f_pf_irq") + 7
        nmi = self.bound("r0f_pf_nmi") + 7
        total = own + sum(callees.values()) + 2 * irq + nmi
        return {"own_instructions": own, "calls": callees,
                "irq_including_entry": irq, "nmi_including_entry": nmi,
                "interrupt_envelope": "two raster IRQs and one terminal NMI",
                "iteration_cpu_cycles_upper": total,
                "interval_cpu_cycles": 405000,
                "cpu_slack_before_dispatch": 405000 - total,
                "scope": "pinned old image CPU work; not a native-clock or frame admission"}


def analyze(root, references):
    sources = check_identity(root)
    target = root / TARGET
    timing = references / "xemu/cpu65_mega65_timings.h"
    model = TickBounds((target / "UNADMITTED.prg").read_bytes(),
                       (target / "UNADMITTED.disassembly").read_text(),
                       (target / "UNADMITTED.symbols").read_text(),
                       timing.read_bytes(), PRG_SHA)
    selected = {
        "m2_command_service", "bind", "operand", "m2w_i32", "m2w_negate",
        "m2w_add", "m2w_double", "m2w_compare", "m2w_positive", "m2w_narrow",
        "magnitude", "m2l_multiply", "m2l_divide", "m2l_service", "normalize",
        "multiply_part", "divide_digit", "finish", "subtract_product",
        "math_transact", "math_ready", "m2rb_math_product", "m2rb_math_q24",
        "m2_commands", "m2_command_constants",
    }
    sizes = {row.split()[3]: int(row.split()[1], 16)
             for row in (target / "UNADMITTED.symbols").read_text().splitlines()
             if len(row.split()) == 4 and row.split()[3] in selected}
    if set(sizes) != selected or sum(sizes.values()) != 6935:
        raise ValueError("selected replacement footprint changed")
    tick = model.tick_iteration()
    return {"identity": "65AERO-M2-FIXED-KERNEL-PREFLIGHT-1",
            "prg_sha256": PRG_SHA, "target_seal_sha256": TARGET_SEAL_SHA,
            "source_invariants": sources, "timing_sha256": sha256(timing.read_bytes()).hexdigest(),
            "selected_linked_symbols_bytes": sizes,
            "tick": tick, "cost_gate": design_budget(model, references, tick),
            "target_links": 0, "runtime_executions": 0}


def design_budget(model, references, tick):
    """Evaluate a partial instruction sketch, NOT a linked bound or lower bound.

    Independent maximum demand counts and a full PAL wait are deliberately
    separable. Their sum cannot prove that any real frame takes this long.
    It does show that this conservative preflight construction has not closed.
    Missing work remains explicitly unknown, rather than charged as zero.
    """
    revision = "40dfef0d1d5f56be2469492715c12bdb32c75b67"
    reference_hashes = {}
    for name in ("targets/mega65/io_mapper.c", "xemu/cpu65_mega65_timings.h",
                 "targets/mega65/mega65.c", "targets/mega65/vic4.h"):
        original = subprocess.check_output(["git", "show", f"{revision}:{name}"], cwd=references)
        if original != (references / name).read_bytes():
            raise ValueError(f"pinned reference changed: {name}")
        reference_hashes[name] = sha256(original).hexdigest()
    # Ordinary absolute resident reads/writes. No new direct-page scratch is
    # assumed. Poll charges use the pinned emulator's always-ready $D70F;
    # the eight-poll timeout is a separate terminal path, not multiplied into
    # every operation of a successful frame.
    read, write, add = (model.base[op] for op in (0xad, 0x8d, 0x6d))
    move = read + write
    accumulate = read + add + write
    carry = read + model.base[0x69] + write
    ready = read + model.base[0x29] + model.base[0xf0] + 3
    # Four partial products in an order that reuses one hardware operand:
    # LL, HL, HH, LH. 20 operand bytes, not 32; output fused with accumulation.
    # Low 8 bytes, two cross products of 6 bytes, high 4 bytes, four propagated
    # carry bytes and explicit initial clearing of the top four product bytes.
    product = (20 * move + 8 * move + 12 * accumulate + 4 * accumulate
               + 4 * carry + 4 * (model.base[0xa9] + write) + 4 * ready)
    # One radix-24 estimate and two products: normalized high divisor for
    # estimation, low32 then high16 divisor for exact subtraction. This omits
    # correction, sign, rounding and ownership checks: they are still unknown.
    digit = (8 * move + 4 * move + 8 * move + 8 * accumulate + carry
             + 4 * move + 5 * accumulate + 3 * ready)
    # A concrete fixed-width normalization sketch: byte relocation then at
    # most seven ASL/ROL passes over the 18-byte dividend and six-byte divisor.
    # Count only the 24 memory shifts, not relocation, loop control or clearing.
    normalization = 7 * 24 * model.base[0x2e]
    # New bounded near-to-physical copy sketch, unrolled up to 64 bytes.
    # This already gives credit for replacing the old 13-cycle far read.
    copy_byte = read + model.base[0xea] + model.prefix[0x92] + model.base[0x1b]
    divisions = 9 * 6 * 3 + 9 * 2 * 2
    products = 14 + 3 + 9 * 2 * 3 * 3 + divisions
    byte_demand = 2000 + 550 * 64 + 9 * 320
    rows = {
        "377_full_product_payload_and_ready_checks": products * product,
        "396_quotient_digit_payload_and_ready_checks": divisions * 2 * digit,
        "198_normalization_shift_payloads": divisions * normalization,
        "40080_display_bytes_payload_only": byte_demand * copy_byte,
        "six_tick_reservations_including_possible_carry_in": 6 * tick["iteration_cpu_cycles_upper"],
        "one_full_PAL_frame_wait_reservation": 808704,
    }
    subtotal = sum(rows.values())
    return {
        "status": "FAIL TO ESTABLISH ADMISSION / UNPROVEN",
        "first_unresolved_gate": "complete-cost preflight before implementation",
        "kind": "partial conservative separable design budget; not a measured or unavoidable frame cost",
        "reference_revision": revision, "reference_sha256": reference_hashes,
        "sketch_unit_cycles": {"product_payload": product, "digit_payload": digit,
                               "normalization_shifts": normalization, "copy_byte": copy_byte},
        "rows": rows, "partial_budget_cycles": subtotal,
        "frame_cycles": 2025000, "partial_budget_excess": subtotal - 2025000,
        "conditional_demand_credit": "550-tile joint bound still requires raster proof; allocation bound is 640",
        "unknown_additional_costs": [
            "normalization byte relocation and controls; sign, correction, rounding, overflow",
            "rotation/clip control, DELTA packing, plane distances and exact horizon scan",
            "tile background construction, raster traversal, text formatting, map bookkeeping",
            "Platform acquisition/fault checks, wrappers, request staging and restoration",
            "continuation dispatch, guards, native-count conversion and phase-aligned publication proof",
            "complete encoded code, constants, compiler scratch, stacks and alignment",
        ],
        "resident": {"old_bytes": 29426, "ceiling": 28671, "old_deficit": 755,
                     "selected_replaceable_bytes": 6935, "replacement_allowance": 6180,
                     "allowance_after_256_margin_and_104_new_data": 5820,
                     "actual_successor_fit": "NOT BUILT / UNPROVEN", "reserve_used": 0},
        "decision": "STOP; no renderer source change and no target link",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--references", type=Path, required=True)
    args = parser.parse_args()
    result = analyze(ROOT, args.references)
    print(json.dumps(result, indent=2))
    # Successful calculation is not successful admission. Unknown mandatory
    # work cannot silently return a passing gate status to an invoking script.
    raise SystemExit(2)
