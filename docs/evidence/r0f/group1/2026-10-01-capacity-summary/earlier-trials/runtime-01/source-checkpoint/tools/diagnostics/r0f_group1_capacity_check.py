#!/usr/bin/env python3
"""Independent capacity-tail and protected terminal checks; synthetic vs actual explicit."""
import argparse
import binascii
import json
import re
from pathlib import Path

import r0f_group1_reduce as reducer
import r0f_group1_export_probe as terminal


def capacity_negatives(data):
    report = reducer.reduce(data)
    c = reducer.C
    world = c["HEADER_BYTES"] + report["records"] * c["RECORD_BYTES"]
    world += c["RESULT_BYTES"] + c["EPOCHS"] * c["POOL_EPOCH_BYTES"]
    tail = world + report["worldEventsRetained"] * c["WORLD_EVENT_BYTES"]
    positions = {"tail-first": tail, "tail-page": (tail + 255) & ~255,
                 "tail-chunk": (tail + 16383) & ~16383, "tail-last": len(data) - 5}
    cases = [(name, lambda value, at=at: value.__setitem__(at, value[at] ^ 1))
             for name, at in positions.items() if at < len(data) - 4]
    cases += [
        ("tail-zero", lambda value: value.__setitem__(slice(tail, -4), bytes(len(value) - 4 - tail))),
        ("tail-shift", lambda value: value.__setitem__(slice(tail, -4), bytes(((at + 1) & 255) ^ c["CAPACITY_PATTERN_XOR"] for at in range(tail, len(value) - 4)))),
        ("extra-byte", lambda value: value.insert(-4, 0)),
        ("truncated-tail", lambda value: value.__delitem__(tail)),
        ("short-declaration", lambda value: value.__setitem__(slice(reducer.H["TRACE_BYTES"], reducer.H["TRACE_BYTES"] + 4), (len(value) - 1).to_bytes(4, "little"))),
        ("version-six", lambda value: value.__setitem__(4, 6)),
        ("fake-extra-world", lambda value: value.__setitem__(slice(reducer.H["WORLD_EVENTS"], reducer.H["WORLD_EVENTS"] + 4), (report["worldEventsRetained"] + 1).to_bytes(4, "little"))),
        ("dropped-world", lambda value: value.__setitem__(slice(reducer.H["WORLD_EVENTS"], reducer.H["WORLD_EVENTS"] + 4), (report["worldEventsRetained"] - 1).to_bytes(4, "little"))),
    ]
    rejected = []
    for name, mutate in cases:
        corrupted = bytearray(data)
        mutate(corrupted)
        corrupted[-4:] = binascii.crc32(corrupted[:-4]).to_bytes(4, "little")
        try:
            reducer.reduce(corrupted)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError("accepted repaired-CRC capacity corruption: " + name)
    return report["capacityCase"], rejected


def terminal_negatives(disassembly, symbols):
    terminal.validate_terminal(disassembly, symbols)
    def changed(section, instruction):
        start = terminal.integration.symbol(symbols, section)
        return re.sub(rf"(?m)^\s*{start:x}: .*", f"{start:x}: 60 {instruction}", disassembly, count=1)
    cases = {
        "return-to-c": changed("r0fg1_terminal_export", "rts"),
        "summary-return": changed("r0fg1_terminal_summary", "rts"),
        "hex-application-memory": changed("r0fg1_terminal_summary_hex", "lda $8000"),
        "hex-rom-call": changed("r0fg1_terminal_summary_hex", "jsr $ffe4"),
        "unknown-screen-call": disassembly.replace("jsr\t$ffd2", "jsr\t$ffe4"),
    }
    rejected = []
    for name, corrupt in cases.items():
        if corrupt == disassembly:
            raise AssertionError("negative mutation did not change disassembly: " + name)
        try:
            terminal.validate_terminal(corrupt, symbols)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError("accepted terminal contract corruption: " + name)
    return rejected


def main(trace, out, disassembly, symbols):
    original = trace.read_bytes()
    data = bytearray(original)
    synthetic = data[:4] == b"G1T6"
    if synthetic:
        # Reuse real predecessor semantics only as a labelled codec fixture.
        # Conversion is NOT a captured version-7 trace or fresh timing proof.
        data = data[:-4]
        data.extend((at & 255) ^ reducer.C["CAPACITY_PATTERN_XOR"]
                    for at in range(len(data), reducer.EXPORT["constants"]["TRACE_CAPACITY"] - 4))
        data[:4] = b"G1T7"
        data[4:6] = (7).to_bytes(2, "little")
        at = reducer.H["TRACE_BYTES"]
        data[at:at + 4] = (len(data) + 4).to_bytes(4, "little")
        data.extend(binascii.crc32(data).to_bytes(4, "little"))
    capacity, corruptions = capacity_negatives(data)
    boundaries = terminal_negatives(disassembly.read_text(), symbols.read_text())
    with out.open("x") as stream:
        json.dump({"result": "PASS", "trace": str(trace),
            "scope": "SYNTHETIC_CODEC_ONLY" if synthetic else "ACTUAL_EXPORTED_VERSION_7",
            "capacity": capacity, "capacityRejections": corruptions,
            "outerCrcRepairedForCapacityCases": True,
            "terminalStaticRejections": boundaries,
            "physical": "NOT RUN"}, stream, indent=2)
        stream.write("\n")
    print(f"Capacity/terminal checks PASS: {len(corruptions)} repaired-CRC and {len(boundaries)} static rejects; synthetic={synthetic}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("trace", "out", "disassembly", "symbols"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    main(args.trace, args.out, args.disassembly, args.symbols)
