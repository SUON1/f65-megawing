#!/usr/bin/env python3
"""Run a fresh development-only Group 1 image and retain actual exported bytes.

00_D81_LOADABILITY_GATE.md applies. No physical SD access or carrier release.
"""
import argparse
from pathlib import Path

import r0f_group1_export_probe as probe
import r0f_group1_contract as contract
import r0f_group1_reduce as reducer


def run(output, mode):
    build_dir = probe.ROOT / "build/r0f/group1/integration"
    metadata = probe.emulator.read_json(build_dir / "build.json")
    prg = build_dir / "GROUP1.prg"
    symbols = (build_dir / "symbols.txt").read_text()
    if (probe.emulator.sha256(prg) != metadata["prgSha256"]
            or any(probe.emulator.sha256(probe.ROOT / name) != digest
                   for name, digest in metadata["inputs"].items())):
        raise ValueError("build/source drift")
    output.mkdir(parents=True, exist_ok=False)
    probe.emulator.write_json(output / "build-identity.json", metadata)
    frozen_prg = output / "GROUP1.prg"
    frozen_prg.write_bytes(prg.read_bytes())
    probe.emulator.PRG = frozen_prg
    probe.emulator.SOURCE_BRANCH = probe.emulator.git_text("branch", "--show-current")
    image = output / "G1DEV01.D81"
    token = probe.ROOT / "docs/evidence/r0f/successor/2026-09-21/TOKEN.prg"
    probe.emulator.fresh_d81(output, image, "G1 TIMING DEV", {"token": token})
    _, execution = probe.emulator.run_xemu(output, mode, image,
                                           "GROUP1_DEVELOPMENT", False, 180)
    memory = (output / "memory.bin").read_bytes()
    values = {name: memory[probe.integration.symbol(symbols, "r0fg1_export_" + name)]
              for name in ("status", "files", "error")}
    probe.emulator.write_json(output / "execution.json", {**execution, **values})
    if values["status"] != 4:
        raise ValueError(f"export incomplete: {values}; see memory, screen and log")
    wire = probe.emulator.read_json(contract.PATH)["constants"]
    length_address = probe.integration.symbol(symbols, "r0fg1_export_bytes")
    length = int.from_bytes(memory[length_address:length_address + 4], "little")
    base_length = wire["HEADER_BYTES"] + wire["EPOCHS"] * wire["PHASES"] * wire["TICKS_PER_PHASE"] * wire["RECORD_BYTES"] + wire["RESULT_BYTES"] + 4
    if not base_length <= length <= base_length + wire["MAX_WORLD_EVENTS"] * wire["WORLD_EVENT_BYTES"]:
        raise ValueError("export length outside admitted wire bounds")
    chunks = (length + 16383) // 16384
    if values["files"] != chunks:
        raise ValueError("export chunk count")
    names = [f"g1t{index:02d}" for index in range(chunks)]
    actual = probe.extract_actual(image, output, ["token", "rsstate", *names], "G1 TIMING DEV")
    trace = bytearray()
    for index, name in enumerate(names):
        data = actual[name]
        size = min(16384, length - index * 16384)
        if data[:2] != b"\x00\x40" or len(data) != size + 2:
            raise ValueError("chunk framing/length")
        trace.extend(data[2:])
    (output / "trace.bin").write_bytes(trace)
    (output / "saved.prg").write_bytes(actual["rsstate"])
    payload_address = probe.integration.symbol(symbols, "r0fsi_payload")
    report = reducer.reduce(trace, actual["rsstate"], payload_address)
    probe.emulator.write_json(output / "reduction.json", report)
    print(f"Actual trace validated: {len(trace)} bytes, {report['records']} ticks; "
          f"nominal timing {report['nominalTiming']}, "
          f"misses={report['nominalDeadlineMisses']}, low-cadence cohorts={report['cohortsBelow20Hz']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--mode", choices=("0", "1"), required=True)
    args = parser.parse_args()
    run(args.out.resolve(), args.mode)
