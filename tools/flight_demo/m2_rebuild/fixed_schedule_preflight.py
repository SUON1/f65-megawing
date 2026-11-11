"""FC-D1--FC-D5 host preflight: fail at the first native-clock prerequisite.

No target instructions are executed. The arithmetic model below describes the
pinned CIA source, not a replacement clock implementation. A source-derived
counterexample stops analysis before publication-window or frame scheduling.
The original fixed_preflight module and all retained results remain unchanged.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path

from fixed_preflight import check_identity


ROOT = Path(__file__).resolve().parents[3]
BASE = "6c0caa8d453bb647696ef85b5b31b35ef2310def"
IDENTITY = "65AERO-M2-FIXED-KERNEL-PREFLIGHT-2"
OLD = Path("docs/evidence/flight-demo/2026-11-11-m2-fixed-kernel-preflight")
OLD_SEAL_SHA = "77641f1f0aed3d8c993d713e7932350d6d824468ce99e736037bdd4cfb15da72"
REFERENCE_REVISION = "40dfef0d1d5f56be2469492715c12bdb32c75b67"
REFERENCES = {
    "targets/mega65/mega65.c": "b6550e3263d82a2b59b452c7f3d400f56544ab8be36c4b46cdcc087bfc67621e",
    "targets/mega65/vic4.c": "7abafaf98dde6c8a3b5ad582b811dd1a9071e0ff2f47bbc2a767b6372b878928",
    "targets/mega65/vic4.h": "15147c924d88ae1d4c01a407bb12097d5d9b076e34eb6eba9a4f982db200272f",
    "targets/mega65/io_mapper.c": "ab5dc491ed0b2c41ac4e3c8ed6413ee1db3d9191cf75dfa6b9094adb91bcdfd0",
    "targets/mega65/xemu-target.h": "ab0f7ad422e7601eacc63e8ad29f837b78ecc22b856900c1da7fbfb6ceecaca7",
    "xemu/cpu65.c": "2f138d3da13583b8f21669fe09d802296fdf211e98826d46e16d5b546e1cfc14",
    "xemu/cpu65_mega65_timings.h": "6bb84846f83975acbdff5f16e39ebe7b5e08390cb68ed0cab2a85df311b4af58",
    "xemu/cia6526.c": "ce7429739fbd4e76784ab18061086b250f0b990252a21bce9f9c32879ce5ca21",
}
LATCH = 65535
PULSES_PER_UPDATE = 32
MASK32 = (1 << 32) - 1


def integer(value, low, high, name):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"invalid {name}")
    return value


def checked_file(path, digest, size=None):
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"missing or non-regular input: {path}")
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != digest or (size is not None and len(raw) != size):
        raise ValueError(f"input identity changed: {path}")
    return raw


def inputs(root, references):
    seal = json.loads(checked_file(root / OLD / "seal.json", OLD_SEAL_SHA))
    actual = {p.name for p in (root / OLD).iterdir()}
    if actual != set(seal) | {"seal.json"}:
        raise ValueError("original packet inventory changed")
    for name, expected in seal.items():
        checked_file(root / OLD / name, expected["sha256"], expected["bytes"])
    source_ids = json.loads((root / OLD / "source-identities.json").read_text())
    # WIP is navigation for this new task. Its historical identity is retained
    # in the sealed packet and Git at BASE, not asserted against current WIP.
    for name, expected in source_ids.items():
        if name != "WORK_IN_PROGRESS.md":
            checked_file(root / name, expected["sha256"], expected["bytes"])
    target_inputs = check_identity(root)  # All 12 target members and 81 inputs.
    ref_sources = {name: checked_file(references / name, digest).decode()
                   for name, digest in REFERENCES.items()}
    old = json.loads((root / OLD / "preflight-final.json").read_text())
    if old["identity"] != "65AERO-M2-FIXED-KERNEL-PREFLIGHT-1":
        raise ValueError("wrong predecessor identity")
    return old, target_inputs, ref_sources


def source_witnesses(root, references):
    """Explain the pinned semantics; unknown source shapes are not accepted."""
    cia = "".join(references["xemu/cia6526.c"].split())
    main = "".join(references["targets/mega65/mega65.c"].split())
    platform = "".join((root / "src/diagnostics/r0f/combined_platform.c").read_text().split())
    witnesses = {
        "timer_a_decrements_by_supplied_ticks": "cia->TCA-=ticks;" in cia,
        "timer_a_underflow_at_zero": "if(cia->TCA<=0)" in cia,
        "timer_a_adds_latch_not_latch_plus_one": "cia->TCA+=cia->TLAL|(cia->TLAH<<8);" in cia,
        "timer_b_counts_a_underflows": "if(timer_a_underflow)cia->TCB--;" in cia,
        "timer_b_underflow_at_zero": "if(cia->TCB<=0)" in cia,
        "timer_b_adds_latch_not_latch_plus_one": "cia->TCB+=cia->TLBL|(cia->TLBH<<8);" in cia,
        "both_latches_ffff": all(f"CFREG(0x{r:04x}u)=255u;" in platform
                                 for r in (0xdc04, 0xdc05, 0xdc06, 0xdc07)),
        "linked_timer_force_load_and_start": "CFREG(0xdc0fu)=0x51u;CFREG(0xdc0eu)=0x11u;" in platform,
        "cia1_ticks_32_per_scanline_update": "cia_tick(&cia1,32);" in main,
        "binary_composite_timestamp": "return~((uint32_t)bh<<24u|(uint32_t)bl<<16u|(uint16_t)ah<<8u|al);" in platform,
        "coherent_sampler_and_reload_exclusion": "bh==bh2&&bh==bh3&&bl==bl2&&ah==ah2&&!(ah==255u&&al>=240u)" in platform,
    }
    if not all(witnesses.values()):
        raise ValueError("unsupported clock source witness: "
                         + ", ".join(k for k, v in witnesses.items() if not v))
    return witnesses


def state_after_updates(updates):
    """Closed form, derived from the pinned <=0/reload recurrence.

    For x supplied pulses, k=floor(x/L) A underflows have occurred and
    A=L-(x mod L). B similarly counts k modulo L. L=65535, not 65536.
    Positive remainders represent the reloaded value at exact boundaries.
    """
    integer(updates, 0, MASK32, "CIA update count")
    underflows, remainder = divmod(updates * PULSES_PER_UPDATE, LATCH)
    return LATCH - remainder, LATCH - underflows % LATCH


def clock_sample(reads):
    """The existing cfnow acceptance predicate for one eight-read attempt."""
    if len(reads) != 8:
        raise ValueError("clock sample must contain eight register reads")
    for value in reads:
        integer(value, 0, 255, "clock register byte")
    bh, bl, bh2, ah, al, ah2, bl2, bh3 = reads
    if bh != bh2 or bh != bh3 or bl != bl2 or ah != ah2 or (ah == 255 and al >= 240):
        return None
    return (~(bh << 24 | bl << 16 | ah << 8 | al)) & MASK32


def stable_reads(a, b):
    integer(a, 1, LATCH, "timer A")
    integer(b, 1, LATCH, "timer B")
    bh, bl, ah, al = b >> 8, b & 255, a >> 8, a & 255
    return (bh, bl, bh, ah, al, ah, bl, bh)


def native_clock_gate():
    # L^2 = 32*n + 1, so the state immediately before B's first reload is
    # exactly A=B=1. It is reachable from force-loaded A=B=L without faults.
    before_update, remainder = divmod(LATCH * LATCH, PULSES_PER_UPDATE)
    if remainder != 1:
        raise ValueError("unsupported rollover arithmetic")
    before = state_after_updates(before_update)
    after = state_after_updates(before_update + 1)
    before_reads, after_reads = stable_reads(*before), stable_reads(*after)
    before_stamp, after_stamp = clock_sample(before_reads), clock_sample(after_reads)
    if before_stamp is None or after_stamp is None:
        raise ValueError("rollover witness rejected by the actual sampler")
    delta = (after_stamp - before_stamp) & MASK32
    if delta != 65569 or before != (1, 1) or after != (65504, 65535):
        raise ValueError("rollover witness changed")
    return {
        "status": "FAIL: binary native-clock continuity at upper-timer reload",
        "evidence_tier": "source-pinned host arithmetic counterexample; not observed target execution",
        "cia_updates_before": before_update, "cia_updates_after": before_update + 1,
        "supplied_CIA_pulses": PULSES_PER_UPDATE,
        "before": {"A": before[0], "B": before[1], "reads": before_reads, "cfnow": before_stamp},
        "after": {"A": after[0], "B": after[1], "reads": after_reads, "cfnow": after_stamp},
        "uint32_timestamp_delta": delta, "excess_encoded_counts": delta - PULSES_PER_UPDATE,
        "sampler_accepts_both": True,
        "modes": ["PAL", "NTSC"],
        "reason": "Both modes advance CIA1 by 32 per scanline update. The existing binary composite jumps by 65569; unsigned wrap subtraction does not remove it. No approved duration cap excludes this reachable state.",
    }


def analyze(root, references):
    old, target_inputs, sources = inputs(root, references)
    witnesses = source_witnesses(root, sources)
    gate = native_clock_gate()
    # FC-D5: do not proceed to a frame result after this mandatory failure.
    return {
        "identity": IDENTITY, "baseline": BASE,
        "status": "BLOCKED AT FIRST MANDATORY GATE",
        "old_packet_seal_sha256": OLD_SEAL_SHA,
        "prg_sha256": old["prg_sha256"], "target_seal_sha256": old["target_seal_sha256"],
        "target_input_count": len(target_inputs),
        "reference_revision": REFERENCE_REVISION, "reference_sha256": REFERENCES,
        "source_witnesses": witnesses, "native_clock": gate,
        "publication_window_proof": "NOT REACHED",
        "phase_schedule": "NOT REACHED; no favorable phase or overlap credit assigned",
        "complete_cost_admission": "UNPROVEN",
        "remaining_cost_allowance_cycles": None,
        "resident": old["cost_gate"]["resident"],
        "old_tick_CPU_bound": old["tick"],
        "retained_demand": {"products": 377, "divisions": 198, "quotient_digits": 396,
                            "unconditional_tile_slots": 640, "conditional_unproved_tiles": 550},
        "unknown_costs": old["cost_gate"]["unknown_additional_costs"],
        "execution_authorized": False, "target_links": 0, "runtime_executions": 0,
        "not_reached_regressions": ["joint tick/wait overlap and commit-window phases",
                                    "guard/atomic-service schedule and Q16 release phases",
                                    "cold/moving generations, cancellation and publication ages"],
        "decision": "STOP. Review a bounded Platform-owned clock continuity correction before resuming scheduling proof. No clock implementation or target link in this task.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--references", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        result = analyze(args.root, args.references)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"identity": IDENTITY, "status": "INPUT REFUSED",
                          "error": str(error), "execution_authorized": False}, indent=2))
        return 2
    print(json.dumps(result, indent=2))
    return 2  # Neither complete costs nor execution have been admitted.


if __name__ == "__main__":
    raise SystemExit(main())
