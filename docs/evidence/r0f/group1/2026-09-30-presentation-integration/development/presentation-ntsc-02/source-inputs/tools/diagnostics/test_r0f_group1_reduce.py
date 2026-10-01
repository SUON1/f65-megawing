#!/usr/bin/env python3
"""Reject plausible-looking corrupt raw evidence, even with a repaired outer CRC."""
import argparse
import binascii
from pathlib import Path

import r0f_group1_reduce as reducer


def validate_negatives(trace):
    reducer.reduce(trace)
    cases = []
    start = reducer.C["HEADER_BYTES"]
    offsets = reducer.O
    irq_count = reducer.H["IRQ_SUMMARIES"] + reducer.WIRE["irqOffsets"]["COUNT"]
    irq_total = reducer.H["IRQ_SUMMARIES"] + reducer.WIRE["irqOffsets"]["TOTAL"]
    world_offset = start + reducer.C["EPOCHS"] * reducer.C["PHASES"] * reducer.C["TICKS_PER_PHASE"] * reducer.C["RECORD_BYTES"] + reducer.C["RESULT_BYTES"]
    for name, mutate in (
        ("truncated", lambda data: data.pop()),
        ("crc", lambda data: data.__setitem__(start + 40, data[start + 40] ^ 1)),
        ("tick-order", lambda data: data.__setitem__(start, 2)),
        ("epoch", lambda data: data.__setitem__(start + offsets["EPOCH"], 1)),
        ("phase", lambda data: data.__setitem__(start + offsets["PHASE"], 1)),
        ("release-drift", lambda data: data.__setitem__(start + reducer.C["RECORD_BYTES"] + offsets["RELEASE"], data[start + reducer.C["RECORD_BYTES"] + offsets["RELEASE"]] ^ 1)),
        ("stage-overflow", lambda data: data.__setitem__(slice(start + 20, start + 62), b"\xff" * 42)),
        ("snapshot-overflow", lambda data: data.__setitem__(start + offsets["SNAPSHOT_HIGH"], 4)),
        ("future-world", lambda data: data.__setitem__(slice(start + offsets["WORLD_SOURCE_TICK"], start + offsets["WORLD_SOURCE_TICK"] + 2), b"\xff\xff")),
        ("capture-cost", lambda data: data.__setitem__(reducer.H["CAPTURE_MAX"], data[reducer.H["CAPTURE_MAX"]] ^ 1)),
        ("ai-causality", lambda data: data.__setitem__(reducer.H["AI_CAUSALITY_ERRORS"], 1)),
        ("domain-state", lambda data: data.__setitem__(reducer.H["SIDECAR_HASH"], data[reducer.H["SIDECAR_HASH"]] ^ 1)),
        ("world-capacity", lambda data: data.__setitem__(slice(reducer.H["WORLD_EVENTS"], reducer.H["WORLD_EVENTS"] + 4), (reducer.C["MAX_WORLD_EVENTS"] + 1).to_bytes(4, "little"))),
        ("world-source", lambda data: data.__setitem__(slice(world_offset + 2, world_offset + 4), b"\xff\xff")),
        ("world-event-time", lambda data: data.__setitem__(slice(world_offset + 4, world_offset + 8), ((reducer.number(data, world_offset + 4) + 0x80000000) & reducer.MASK).to_bytes(4, "little"))),
        ("presentation-view", lambda data: data.__setitem__(world_offset + reducer.W["KEY_FLAGS"], data[world_offset + reducer.W["KEY_FLAGS"]] ^ 1)),
        ("presentation-tier", lambda data: data.__setitem__(world_offset + reducer.W["KEY_FLAGS"], data[world_offset + reducer.W["KEY_FLAGS"]] ^ 2)),
        ("presentation-buffer", lambda data: data.__setitem__(world_offset + reducer.W["KEY_FLAGS"], data[world_offset + reducer.W["KEY_FLAGS"]] ^ 4)),
        ("presentation-anchor", lambda data: data.__setitem__(world_offset + reducer.W["ANCHOR_MASK"], 0x0f)),
        ("presentation-registration", lambda data: data.__setitem__(world_offset + reducer.W["REGISTRATION_CRC"], data[world_offset + reducer.W["REGISTRATION_CRC"]] ^ 1)),
        ("presentation-high-water", lambda data: data.__setitem__(reducer.H["ANCHOR_HIGH"], 3)),
        ("presentation-cancel", lambda data: data.__setitem__(slice(reducer.H["VIEW_CANCELS"], reducer.H["VIEW_CANCELS"] + 2), b"\x00\x00")),
        ("irq-error", lambda data: data.__setitem__(reducer.H["IRQ_ERROR"], 1)),
        ("irq-empty", lambda data: data.__setitem__(slice(irq_count, irq_count + 2), b"\x00\x00")),
        ("irq-total", lambda data: data.__setitem__(slice(irq_total, irq_total + 4), b"\xff" * 4)),
        ("service-phase-empty", lambda data: data.__setitem__(slice(reducer.H["SERVICE_PHASE_MASKS"], reducer.H["SERVICE_PHASE_MASKS"] + 2), b"\x00\x00")),
        ("service-phase-incomplete", lambda data: data.__setitem__(slice(reducer.H["SERVICE_PHASE_MASKS"], reducer.H["SERVICE_PHASE_MASKS"] + 2), b"\xfe\xff")),
        ("service-order-missing", lambda data: data.__setitem__(reducer.H["SERVICE_ORDER_MASKS"], 0x1f)),
        ("service-post-order-missing", lambda data: data.__setitem__(reducer.H["SERVICE_ORDER_MASKS"] + 1, 0x1f)),
    ):
        corrupted = bytearray(trace)
        mutate(corrupted)
        if name not in ("crc", "truncated"):
            corrupted[-4:] = (binascii.crc32(corrupted[:-4]) & 0xffffffff).to_bytes(4, "little")
        try:
            reducer.reduce(corrupted)
        except ValueError:
            cases.append(name)
        else:
            raise AssertionError("accepted corrupt evidence: " + name)
    # A nominal miss is a valid observation, not malformed evidence and never
    # a timing PASS. Keep the captured first failing run as the regression.
    print(f"Independent reducer rejected {len(cases)} corruption cases: {', '.join(cases)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path)
    args = parser.parse_args()
    validate_negatives(args.trace.read_bytes())
