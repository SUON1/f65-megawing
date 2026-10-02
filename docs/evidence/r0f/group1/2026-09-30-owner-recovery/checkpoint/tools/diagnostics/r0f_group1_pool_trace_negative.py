#!/usr/bin/env python3
"""Independent corruption checks against a supplied version-6 source snapshot."""
import argparse
import binascii
import json
import sys
from pathlib import Path


def main(source, trace_path, output):
    if output.exists():
        raise ValueError("refusing to overwrite negative-test evidence")
    sys.path.insert(0, str(source / "tools/diagnostics"))
    import r0f_group1_reduce as reducer
    import test_r0f_group1_reduce as existing
    data = trace_path.read_bytes()
    existing.validate_negatives(data)
    constants = reducer.C
    pool_start = constants["HEADER_BYTES"] + constants["EPOCHS"] * constants["PHASES"] * constants["TICKS_PER_PHASE"] * constants["RECORD_BYTES"] + constants["RESULT_BYTES"]
    cases = []
    for epoch in range(constants["EPOCHS"]):
        for owner, (name, pool) in enumerate(reducer.POOL["pools"].items()):
            for field, bad in (("CAPACITY", pool["capacity"] + 1),
                               ("PEAK", pool["capacity"] + 1),
                               ("SAMPLES", 0), ("FULL_SAMPLES", 65535)):
                at = pool_start + epoch * constants["POOL_EPOCH_BYTES"] + owner * reducer.POOL["wire"]["RECORD_BYTES"] + reducer.POOL["wireOffsets"][field]
                cases.append((f"{epoch}/{name}/{field}", at, bad))
    for owner, name in enumerate(reducer.POOL["pools"]):
        at = pool_start + owner * reducer.POOL["wire"]["RECORD_BYTES"] + reducer.POOL["wireOffsets"]["SAMPLES"]
        cases.append(("no-post-storage-samples/" + name,
                      at + constants["POOL_EPOCH_BYTES"], reducer.number(data, at, 2)))
    for name, at, bad in cases:
        corrupted = bytearray(data)
        corrupted[at:at + 2] = bad.to_bytes(2, "little")
        corrupted[-4:] = (binascii.crc32(corrupted[:-4]) & 0xffffffff).to_bytes(4, "little")
        try:
            reducer.reduce(corrupted)
        except ValueError:
            continue
        raise AssertionError("accepted repaired-CRC corruption: " + name)
    with output.open("x") as stream:
        json.dump({"result": "PASS", "trace": str(trace_path),
                   "existingCases": 30, "poolCases": len(cases),
                   "poolRejections": [case[0] for case in cases],
                   "outerCrcRepairedForPoolCases": True}, stream, indent=2)
        stream.write("\n")
    print(f"Actual version-6 trace: 30 existing and {len(cases)} pool corruption cases rejected")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--trace", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    main(args.source.resolve(), args.trace.resolve(), args.out.resolve())
