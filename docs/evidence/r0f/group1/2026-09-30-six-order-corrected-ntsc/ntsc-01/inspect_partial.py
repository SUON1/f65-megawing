#!/usr/bin/env python3
"""Inspect this terminated run; never promote its partial trace to a PASS."""
import json
from pathlib import Path
import sys

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "tools/diagnostics"))
import r0f_group1_contract as contract
import r0f_group1_reduce as reducer
import r0f_group1_export_probe as probe


def main():
    output = Path(__file__).resolve().parent
    symbols = (output / "symbols.txt").read_text()
    build = probe.emulator.read_json(output / "build-identity.json")
    if (probe.emulator.sha256(output / "symbols.txt") != build["symbolsSha256"]
            or probe.emulator.sha256(contract.PATH)
            != build["inputs"][str(contract.PATH.relative_to(ROOT))]):
        raise ValueError("symbol/contract drift")
    memory = (output / "memory.bin").read_bytes()
    wire = json.loads(contract.PATH.read_text())
    offsets = wire["headerOffsets"]

    def read_symbol(name, size):
        address = probe.integration.symbol(symbols, name)
        return int.from_bytes(memory[address:address + size], "little")

    header_address = probe.integration.symbol(symbols, "header")
    header = memory[header_address:header_address + wire["constants"]["HEADER_BYTES"]]
    number = lambda offset, size=4: int.from_bytes(header[offset:offset + size], "little")
    ticks = (1600, 3200)
    result = (output / "result.bin").read_bytes()
    decoded = probe.emulator.validate_success_result(result, ticks, reducer.golden(ticks))
    extraction = output / "partial-extracted"
    extraction.mkdir(exist_ok=True)
    actual = {}
    for name in ("token", "rsstate", "g1t00", "g1t01", "g1t02", "g1t03"):
        path = extraction / name
        if not path.exists():
            probe.emulator.c154([output / "G1DEV01.D81", "-read", name, path])
        actual[name] = path.read_bytes()
    payload_address = probe.integration.symbol(symbols, "r0fsi_payload")
    if (actual["rsstate"][:2] != payload_address.to_bytes(2, "little")
            or actual["rsstate"][2:] != probe.emulator.expected_save(result)[2:]):
        raise ValueError("actual SAVE mismatch")
    for name in ("g1t00", "g1t01", "g1t02", "g1t03"):
        if len(actual[name]) != 16386 or actual[name][:2] != b"\x00\x40":
            raise ValueError("closed chunk length/framing mismatch: " + name)
    if actual["g1t00"][2:258] != header:
        raise ValueError("exported header differs from frozen target header")
    try:
        probe.emulator.Image(output / "G1DEV01.D81")
    except (ValueError, SystemExit) as error:
        structure_error = str(error)
    else:
        raise ValueError("partial image unexpectedly passed complete-image validation")
    prefix = b"".join(actual[f"g1t{index:02d}"][2:] for index in range(4))
    try:
        reducer.reduce(prefix, actual["rsstate"], payload_address)
    except ValueError as error:
        reduction_error = str(error)
    else:
        raise ValueError("partial trace unexpectedly accepted")
    report = {
        "scope": "one focused NTSC acquisition; export interrupted at 60 seconds",
        "targetFault": read_symbol("cffault", 1),
        "records": read_symbol("records", 2),
        "irqError": read_symbol("r0fg1_irq_error", 1),
        "exportStatus": read_symbol("r0fg1_export_status", 1),
        "exportFilesCompleted": read_symbol("r0fg1_export_files", 1),
        "exportError": read_symbol("r0fg1_export_error", 1),
        "traceBytesDeclared": read_symbol("r0fg1_export_bytes", 4),
        "exportBytesRemainingAtChunkBoundary": read_symbol("r0fg1_export_remaining", 4),
        "servicePhaseMasks": [[f"{number(offsets['SERVICE_PHASE_MASKS'] + (epoch * 3 + service) * 2, 2):04X}"
                               for service in range(3)] for epoch in range(2)],
        "serviceOrderMasks": [f"{header[offsets['SERVICE_ORDER_MASKS'] + epoch]:02X}" for epoch in range(2)],
        "irqSummaries": [{"count": number(offsets["IRQ_SUMMARIES"] + epoch * 8, 2),
                          "totalCounts": number(offsets["IRQ_SUMMARIES"] + epoch * 8 + 2),
                          "maxCounts": number(offsets["IRQ_SUMMARIES"] + epoch * 8 + 6, 2)}
                         for epoch in range(2)],
        "result": decoded,
        "actualSaveValidation": "PASS",
        "closedChunkFraming": "PASS",
        "exportedHeaderEqualsFrozenHeader": "PASS",
        "completeImageValidation": "REJECTED: " + structure_error,
        "partialTraceReduction": "REJECTED: " + reduction_error,
        "fullTraceReduction": "NOT RUN: incomplete export",
        "phaseCoverageAcceptance": False,
        "physical": "NOT RUN",
        "fullGroup1Acceptance": False,
    }
    probe.emulator.write_json(output / "inspection.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
