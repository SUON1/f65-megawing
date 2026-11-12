"""CC-D1--CC-D6: conditional host model, never a target service grant.

The old executable and the corrected source have deliberately separate roots.
All cost-profile numbers used by tests are synthetic. The CLI only consumes
sealed/source identities and emits unknown costs, constraints and a refusal.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess

from fixed_schedule_preflight import (
    REFERENCES, REFERENCE_REVISION, checked_file, clock_sample, inputs,
    integer, source_witnesses, stable_reads, state_after_updates,
)
from fixed_preflight import TARGET

ROOT = Path(__file__).resolve().parents[3]
BASE = "fcba7cf4f742a216fba1a6954a4e74b7c9d59ec8"
OLD_BASE = "5c78bf7d00aadda0e63ce800e27fe3e142c651c0"
IDENTITY = "65AERO-M2-FIXED-KERNEL-PREFLIGHT-3"
MASK = 0xffffffff
MODULUS = 65535 ** 2
PACKETS = {
    "2026-11-11-m2-fixed-kernel-preflight": "77641f1f0aed3d8c993d713e7932350d6d824468ce99e736037bdd4cfb15da72",
    "2026-11-11-m2-fixed-kernel-cost-correction": "84d469cfaab7c362126c6a28a8d504ada24a1c012826d138ee7b88c3f1c3ce77",
    "2026-11-11-m2-platform-clock": "0b0abb69eebb774bbba81203cb9f7b8a990b634c8b1e2968e28af091cc89e593",
    "2026-11-11-m2-platform-clock-p2": "59c17610191f1079b7ac076978d70e06b2f70ace1d745eb4ad4f1eeb9742bb3e",
}
MODES = {"PAL": (624, 1296, 112), "NTSC": (526, 1287, 64)}
DEMAND = {"products": 377, "divisions": 198, "quotient_digits": 396,
          "tiles": 640, "display_bytes": 45840}
UNKNOWNS = {
    "frame_poll_gap": "CPU cycles: every calibration frame-counter observation gap",
    "frame_read_to_sample": "CPU cycles: frame read through successful corrected sample, retries/IRQ included",
    "clock_gap": "native counts: all changed-image successful sample gaps, including initialization/failure paths",
    "batch_excess": "CPU cycles per scanline: normal-mode instruction-batch overshoot upper bound",
    "product": "CPU cycles: complete exact signed/carry/round/overflow product, all wrappers",
    "division": "CPU cycles: complete normalization, two quotient digits, correction, finish and wrappers",
    "frame_rest": "CPU cycles: all nonarithmetic foreground work, dispatch/clocks/guards, geometry control, horizon, maps, 640 tiles, text, 45840-byte transfer and setup; excludes tick/IRQ/wait",
    "atomic": "CPU cycles: largest indivisible foreground operation, including call/return",
    "tick": "CPU cycles: full ordered 21-stage tick and input/release work, corrected clock and observation latency; excludes IRQ",
    "fragment": "CPU cycles per release: TOTAL unusable guard/atomic tail, no-grant polling and observation staleness, at least atomic + guard/idle tail",
    "irq": "CPU cycles: complete interrupt entry/handler/return under pinned arrival envelope",
    "poll": "CPU cycles: complete unsuccessful commit loop including clock/fault/guard/return and retries; excludes separately charged tick/IRQ/fragment",
    "publication": "CPU cycles: first raster high read through selector/readback, first enable, matching record, calls and IRQ; no yielding",
    "capture_gap": "CPU cycles: previous commit through next logical capture, including scheduling/IRQ/input",
    "input_age": "CPU cycles: persistent input change through its authoritative sampled pose, including tick/IRQ/observation",
    "clock_resident_extra": "bytes: additional clock state/code/padding/scratch/alignment, minimum 10 logical bytes",
    "stack": "bytes: changed whole-program HW/SW stack, compiler helpers, IRQ/NMI/fault paths",
}


def ceildiv(a, b):
    return -(-a // b)


def regular_tree_path(path):
    """Do not accept a same-hash alias through any symlink component."""
    path = Path(path).absolute()
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError(f"symlinked input: {path}")
    return path


def sealed_packet(directory, digest):
    regular_tree_path(directory)
    seal = json.loads(checked_file(directory / "seal.json", digest))
    actual = {str(p.relative_to(directory)) for p in directory.rglob("*") if p.is_file()}
    if actual != set(seal) | {"seal.json"}:
        raise ValueError("sealed packet inventory changed")
    for name, expected in seal.items():
        path = regular_tree_path(directory / name)
        if not path.is_relative_to(directory.absolute()):
            raise ValueError("packet path escaped its root")
        checked_file(path, expected["sha256"], expected["bytes"])
    return len(seal)


def frozen_inputs(old_root, corrected_root, references):
    for root in (old_root, corrected_root, references):
        regular_tree_path(root)
    if old_root.resolve() == corrected_root.resolve():
        raise ValueError("old-image and corrected-source roots must be distinct")
    # The old verifier runs against its original source, never relaxed pins.
    old, target_ids, refs = inputs(old_root, references)
    # Harden inherited inputs against symlinks and extra target packet members.
    target_dir = old_root / TARGET
    sealed_packet(target_dir, old["target_seal_sha256"])
    for name in target_ids:
        regular_tree_path(old_root / name)
    for name in REFERENCES:
        regular_tree_path(references / name)
    packet_counts = {name: sealed_packet(corrected_root / "docs/evidence/flight-demo" / name, digest)
                     for name, digest in PACKETS.items()}
    # Git objects provide the immutable corrected-source identity; WIP and new
    # host files are not mistaken for constituents of the historical PRG.
    corrected_ids = {}
    names = set(target_ids) | {"src/platform/m1/clock_private.h"}
    for name in sorted(names):
        original = subprocess.check_output(["git", "show", f"{BASE}:{name}"], cwd=ROOT)
        digest = sha256(original).hexdigest()
        checked_file(regular_tree_path(corrected_root / name), digest, len(original))
        corrected_ids[name] = {"bytes": len(original), "sha256": digest}
    p2 = json.loads((corrected_root / "docs/evidence/flight-demo/2026-11-11-m2-platform-clock-p2/run-1.stdout").read_text())
    if p2["normalization"]["admitted_feedback_cap"] != 12:
        raise ValueError("old cap-six normalization credit refused")
    return old, target_ids, corrected_ids, refs, packet_counts


def witnesses(root, refs):
    compact = lambda text: "".join(text.split())
    texts = {name: compact((root / name).read_text()) for name in (
        "src/platform/m1/clock_private.h", "src/platform/m1/m1_platform.c",
        "src/platform/m2_rebuild/platform.c", "src/graphics/m2_rebuild.c",
        "src/diagnostics/m2_rebuild/main.c", "src/diagnostics/r0f/combined_model.c")}
    clock, adapter, platform, graphics, main, ratio = texts.values()
    vic, cpu, emulator = (compact(refs[n]) for n in (
        "targets/mega65/vic4.c", "xemu/cpu65.c", "targets/mega65/mega65.c"))
    checks = {
        "modulo_converter": all(s in clock for s in (
            "UINT32_C(0xfffe0001)", "(upper<<16u)-upper+(65535u-a)",
            "(M1_CLOCK_MODULUS-clock->phase)+phase", "clock->elapsed+=delta;")),
        "sticky_fault_and_half_range": all(s in clock for s in (
            "clock->fault||sample_fault", "delta>=M1_CLOCK_HALF_RANGE", "a==0u||b==0u")),
        "seventeen_samples_and_ratio": all(s in adapter for s in (
            "frames<17u&&polls++<4000000ul", "(uint8_t)(next-previous)!=1u",
            "elapsed=now-start;", "elapsed/16u,cycles,16u")),
        "ratio_remainder_carry": all(s in ratio for s in ("t+=r;", "if(t>=d)", "while(shift--)")),
        "raster_then_selector_readback": all(s in platform for s in (
            "line<4u||line>(uint16_t)(top-16u)", "CFREG(REG_SCREEN_BANK)=bank;",
            "CFREG(REG_SCREEN_BANK)!=bank||m1_platform_fault()")),
        "record_latch_and_uncertain_fault": all(s in graphics for s in (
            "fail(renderer,6u);", "renderer->front=renderer->destination;",
            "renderer->shown=1u;", "renderer->phase=M2RB_BEGIN;")),
        "q16_release_carry": all(s in main for s in (
            "period>>16u", "period&65535u", "next>>16u")),
        "one_cia_update_after_cpu_batch": all(s in emulator for s in (
            "cycles-=cpu_cycles_per_scanline;", "cia_tick(&cia1,32);", "vic4_render_scanline()")),
        "multi_operation_batch": ("while(all_cycles<run_for_cycles)" in cpu
                                  and "cpu_cycles_per_step=cpu_cycles_per_scanline;" in emulator),
        "physical_raster_updated_after_increment": "ycounter++;" in vic and "SET_PHYSICAL_RASTER(ycounter)" in vic,
        "selector_dependent_fetch": "SCREEN_ADDR" in vic and "CHARGEN_Y_START" in vic and "BORDER_Y_TOP" in vic,
    }
    if not all(checks.values()):
        raise ValueError("unsupported source shape: " + ", ".join(k for k, v in checks.items() if not v))
    return checks


class Clock:
    """Host mathematical model of the pinned private converter, no MMIO."""
    def __init__(self):
        self.phase = None
        self.elapsed = 0
        self.fault = False

    def sample(self, raw, fault=False):
        if self.fault or fault:
            self.fault = True
            return self.elapsed
        integer(raw, 0, MASK, "raw timestamp")
        counters = (~raw) & MASK
        a, b = counters & 65535, counters >> 16
        if not a or not b:
            self.fault = True
            return self.elapsed
        phase = (65535 - b) * 65535 + 65535 - a
        if self.phase is not None:
            delta = (phase - self.phase) % MODULUS
            if delta >= 1 << 31:
                self.fault = True
                return self.elapsed
            self.elapsed = (self.elapsed + delta) & MASK
        self.phase = phase
        return self.elapsed


def calibrated_period(mode, offsets):
    """Conservative finite phase domain under the explicit <one-line sample
    and <one-frame observation constraints. All 17 offsets are retained.
    One-frame observation plus one-line sample latency admits u in [0,R].
    The resulting endpoint difference covers every k in [-R,R].
    """
    if mode not in MODES or len(offsets) != 17:
        raise ValueError("unsupported calibration phase partition")
    rasters, line, _ = MODES[mode]
    for offset in offsets:
        integer(offset, 0, rasters, "sample offset in CIA updates")
    times = [i * rasters + offset for i, offset in enumerate(offsets)]
    if any(b < a for a, b in zip(times, times[1:])):
        raise ValueError("decreasing calibration samples")
    elapsed = (times[-1] - times[0]) * 32
    if not 16000 <= elapsed <= 1600000:
        raise ValueError("calibration acceptance failed")
    return (405000 * (elapsed // 16) * 65536) // (rasters * line)


def release(origin, fraction, period, ticks):
    integer(origin, 0, MASK, "release origin")
    integer(fraction, 0, 65535, "Q16 fraction")
    integer(period, 1, MASK, "Q16 period")
    integer(ticks, 0, MASK, "tick count")
    return (origin + (fraction + ticks * period) // 65536) & MASK


def phase_envelope(mode):
    rasters, line, top = MODES[mode]
    # Monotone integer floors over the whole endpoint domain. Intermediates
    # cannot make the extrema worse. Fraction and CIA-lattice rounding are
    # independently bounded below; there is no favorable phase reset.
    periods = [405000 * (32 * rasters + 2 * k) * 65536 // (rasters * line)
               for k in range(-rasters, rasters + 1)]
    minimum_lines = (min(periods) // 65536) // 32
    return {"offset_domain_updates": [0, rasters], "endpoint_classes": len(periods),
            "period_q16_min": min(periods), "period_q16_max": max(periods),
            "minimum_due_separation_lines": minimum_lines,
            "minimum_due_separation_CPU_cycles": minimum_lines * line,
            "safe_interior_raster_interval": [5, top - 16],
            "minimum_interior_CPU_cycles": (top - 21) * line,
            "minimum_prefetch_complete_lines": 14,
            "coverage": "integer interval enclosure of every offset, Q16 carry and 32-count lattice phase"}


def response_bound(work, tick_period, tick, fragment, irq, line, horizon):
    """Busy interval, including carry-in; all integer CPU-cycle units.

    F charges the TOTAL lost guard/atomic slack per release interval, not one
    poll. At most 1+ceil(t/T) ticks and 1+ceil(t/L) IRQs can interfere. This
    overcounts simultaneous endpoints. A stable upper bound is sufficient;
    failure of this deliberately conservative construction is not a measured
    or inevitable deadline miss.
    """
    for name, value in locals().copy().items():
        integer(value, 0 if name in ("fragment", "irq") else 1, 1 << 50, name)
    bound = work
    while bound <= horizon:
        new = work + (1 + ceildiv(bound, tick_period)) * (tick + fragment)
        new += (1 + ceildiv(bound, line)) * irq
        if new <= bound:
            return bound
        bound = new
    raise ValueError("conditional response bound exceeds horizon; not an inevitable execution failure")


def conditional_schedule(mode, costs, *, units="CPU cycles", tiles=640):
    """Evaluate sufficient constraints ONLY for an explicit synthetic profile.

    This API is a regression aid. The CLI never accepts costs or emits grants.
    It cannot substitute a proposed payload sketch for a complete linked WCET.
    """
    names = set(UNKNOWNS) - {"clock_gap", "clock_resident_extra", "stack"}
    if units != "CPU cycles" or set(costs) != names or tiles != 640:
        raise ValueError("wrong units, missing costs or unproved workload credit")
    for name, value in costs.items():
        integer(value, 1, 1 << 40, name)  # Unknown and zero never mean free work.
    rasters, line, _ = MODES[mode]
    p = phase_envelope(mode)
    t = p["minimum_due_separation_CPU_cycles"]
    if costs["frame_poll_gap"] >= rasters * line or costs["frame_read_to_sample"] >= line:
        raise ValueError("unproved calibration observation/phase envelope")
    if costs["publication"] >= line:
        raise ValueError("whole-publication one-line constraint failed")
    if costs["fragment"] <= costs["atomic"]:
        raise ValueError("fragment must charge atomic plus guard/idle tail")
    # Tick includes successful observation latency. Charge one pending IRQ and
    # every possible new IRQ; no tick work may run into the next due event.
    tick_response = costs["tick"]
    while tick_response < t:
        new = costs["tick"] + (1 + ceildiv(tick_response, line)) * costs["irq"]
        if new <= tick_response:
            break
        tick_response = new
    if tick_response >= t:
        raise ValueError("tick observation/work and IRQ cannot fit before the next due event")
    work = 377 * costs["product"] + 198 * costs["division"] + costs["frame_rest"]
    ready = response_bound(work, t, costs["tick"], costs["fragment"], costs["irq"], line, 2025000)
    gap = response_bound(costs["poll"], t, costs["tick"], costs["fragment"], costs["irq"], line, t - 1)
    interior = p["minimum_interior_CPU_cycles"]
    if gap >= interior:
        raise ValueError("poll-response gap cannot guarantee an interior-window sample")
    frame_upper = rasters * (line + costs["batch_excess"])
    # First poll can miss, then a later eligible poll can be G late. Ticks and
    # IRQ work inside this elapsed wait are already included, never added again.
    wait = frame_upper - interior + 2 * gap + costs["publication"]
    age = ready + wait
    cadence = costs["capture_gap"] + age
    pose_age = costs["input_age"] + 2 * age + costs["capture_gap"]
    if age > 2025000 or cadence > 2025000 or pose_age > 4050000:
        raise ValueError("conditional frame/cadence/persistent-pose constraint failed")
    return {"status": "CONDITIONAL ONLY: synthetic costs, no executable admission",
            "ready_upper_CPU_cycles": ready, "poll_response_upper_CPU_cycles": gap,
            "publication_wait_elapsed_upper_CPU_cycles": wait,
            "capture_age_upper_CPU_cycles": age, "intercommit_upper_CPU_cycles": cadence,
            "persistent_pose_age_upper_CPU_cycles": pose_age,
            "tick_response_upper_CPU_cycles": tick_response, "execution_authorized": False}


def analyze(old_root, corrected_root, references):
    old, target_ids, corrected_ids, refs, counts = frozen_inputs(old_root, corrected_root, references)
    raw_witnesses = source_witnesses(old_root, refs)
    corrected_witnesses = witnesses(corrected_root, refs)
    return {
        "identity": IDENTITY, "status": "BLOCKED: mandatory changed-image costs UNPROVEN",
        "historical_image_source_commit": OLD_BASE, "corrected_source_commit": BASE,
        "prg_sha256": old["prg_sha256"], "target_seal_sha256": old["target_seal_sha256"],
        "old_target_input_count": len(target_ids), "corrected_source_inputs": corrected_ids,
        "packet_members": counts, "reference_revision": REFERENCE_REVISION,
        "reference_sha256": REFERENCES, "raw_source_witnesses": raw_witnesses,
        "corrected_source_witnesses": corrected_witnesses,
        "clock_semantics": "PASS at source-model tier; accepted PC/P2 host evidence retained; no changed-image proof",
        "calibration_phase_model": {mode: phase_envelope(mode) for mode in MODES},
        "conditional_window": "source ordering established; whole first-high-read through matching record including IRQ must be <1287 NTSC /1296 PAL CPU cycles",
        "conditional_schedule": {
            "status": "sufficient interval constraints only; no numeric candidate allowance",
            "W": "377*C_product + 198*C_division + W_frame_rest (includes full 640 tiles/45840 bytes)",
            "R": "least upper fixed point W+(1+ceil(R/T))*(C_tick+F)+(1+ceil(R/L))*I",
            "G": "same response bound for complete failed-poll cost, including carry-in ticks, fragments and IRQs",
            "requirements": ["finite R; G<T and G<U; F>atomic with total guard/idle tail charged",
                             "tick observation/work plus IRQ fits before next minimum due event",
                             "H=R_frame*(L+batch_excess); U=(top-21)*L",
                             "V=H-U+2G+C_publication; no additional tick reservation inside V",
                             "A=R+V; A<=2025000; B+A<=2025000",
                             "input_age+2*A+B<=4050000; no reset of phase between generations"],
        },
        "model_conditions": [
            "pinned normal 40.5MHz CPU multi-op mode; no DMA, trace, single-step or hypervisor debugging",
            "frame-counter observation gap <one frame; frame read through successful clock sample <one line",
            "bounded batch overshoot and raw sampler window <one line, including IRQ",
            "every successful changed-image clock gap <2^31 native counts, never inferred just from small delta",
            "at most one IRQ per physical line plus one pending; no successful continuation through NMI fault",
            "foreground/guard native-count grants include 32*(ceil(C/L)+1) endpoint envelope and all wrapper/staleness cost",
            "FK-D4 capture policy is a successor obligation, unimplemented in historical executable",
            "normal publication returns without yield; preactivation failure retains old frame; uncertain selector is terminal/reset with displayed identity UNPROVEN",
            "cell-exclusive tiles/complete maps; 80-byte bitmap,24-byte delta; synchronous retired 64-byte Platform buffer reuse, including failure/cancellation",
        ],
        "retained_demand": DEMAND,
        "unknown_costs": {k: {"value": None, "units_and_scope": v} for k, v in UNKNOWNS.items()},
        "first_unresolved_gate": "changed-image observation/calibration/clock and batch envelopes; no target costs measured",
        "actual_complete_cost_admission": "UNPROVEN", "actual_phase_schedule": "NOT REACHED",
        "remaining_cost_allowance_cycles": None, "launch_budget": None, "service_budgets": None,
        "historical_resident": {"bytes": 29426, "ceiling": 28671, "deficit": 755, "scratch": 87, "reserve": 0},
        "historical_cold_lower_bound": {"cycles": 2323776, "ceiling": 2025000, "deficit": 298776},
        "conditional_replacement_bytes": {"retirement": 6935, "gross": 6180, "after_margin_and_data": 5820,
                                          "current_expression": "5820-C_clock", "upper_before_other_clock_charges": 5810},
        "resident_admission": "UNPROVEN / NOT BUILT", "stack_admission": "UNPROVEN / NOT BUILT",
        "target_links": 0, "runtime_executions": 0, "execution_authorized": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old-root", type=Path, required=True)
    parser.add_argument("--corrected-root", type=Path, default=ROOT)
    parser.add_argument("--references", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = analyze(args.old_root, args.corrected_root, args.references)
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        result = {"identity": IDENTITY, "status": "INPUT REFUSED", "error": str(error),
                  "execution_authorized": False}
    print(json.dumps(result, indent=2))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
