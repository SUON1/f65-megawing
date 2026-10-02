#!/usr/bin/env python3
"""Qualify integrated lockout with disposable PRG fault derivatives.

MANDATORY D81 LOADABILITY GATE: read 00_D81_LOADABILITY_GATE.md first.
Each run fresh-formats a token-only image; never touches SD or an existing disk.
Patches are exact-byte checked, recorded and confined to a new local PRG.
"""
import argparse
from pathlib import Path

import r0f_group1_export_probe as probe


def run(case, output):
    runtime = probe.emulator
    build = probe.ROOT / "build/r0f/group1/integration"
    metadata = runtime.read_json(build / "build.json")
    source = build / "GROUP1.prg"
    symbols = (build / "symbols.txt").read_text()
    if runtime.sha256(source) != metadata["prgSha256"] or any(
            runtime.sha256(probe.ROOT / name) != digest
            for name, digest in metadata["inputs"].items()):
        raise ValueError("source/build drift")
    original = source.read_bytes()
    load = int.from_bytes(original[:2], "little")

    def offset(symbol):
        return probe.integration.symbol(symbols, symbol) - load + 2

    if case == "capsule-guard":
        begin, end = map(offset, ("r0fg1_export_capture", "r0fg1_export_capture_end"))
        # Guard seed followed by LDZ #0 in both leading/trailing capture loops.
        guard = runtime.read_json(probe.ROOT / "interfaces/r0f_group1_export_contract.json")["constants"]["GUARD_VALUE"]
        signature = bytes((0xa9, guard, 0xa3, 0))
        fragment = original[begin:end]
        if fragment.count(signature) != 2:
            raise ValueError("capsule seed instruction identity")
        patch_offset = begin + fragment.index(signature) + 1
        replacement = bytes((guard ^ 1,))
        description = "Corrupt leading capsule guard during pre-C capture; validator unchanged"
    else:
        patch_offset = offset("r0fg1_irq_begin")
        if original[patch_offset] != 0xd8:  # CLD at the checked probe entry.
            raise ValueError("IRQ probe entry identity")
        flag = "r0f_pf_nmi_seen" if case == "nmi-sticky" else "r0fg1_irq_error"
        address = probe.integration.symbol(symbols, flag)
        replacement = bytes((0xa9, 1, 0x8d, address & 255, address >> 8, 0x60))
        description = "Set " + flag + " on the first acquired IRQ; simulated sticky fault, not an injected electrical NMI"
    patched = bytearray(original)
    old = original[patch_offset:patch_offset + len(replacement)]
    patched[patch_offset:patch_offset + len(replacement)] = replacement
    output.mkdir(parents=True, exist_ok=False)
    runtime.write_json(output / "injection.json", {
        "case": case, "description": description, "address": load + patch_offset - 2,
        "oldHex": old.hex(), "newHex": replacement.hex(), "source": metadata,
    })
    runtime.PRG = output / "NEGATIVE.prg"
    runtime.PRG.write_bytes(patched)
    runtime.SOURCE_BRANCH = runtime.git_text("branch", "--show-current")
    image = output / "G1NEG01.D81"
    token = runtime.ROOT / "docs/evidence/r0f/successor/2026-09-21/TOKEN.prg"
    initial = runtime.fresh_d81(output, image, "G1 NEGATIVE", {"token": token})
    result, environment = runtime.run_xemu(output, "1", image,
                                            "GROUP1_NEGATIVE", False,
                                            180 if case == "irq-read-error" else 60)
    decoded = runtime.decode_result(result)
    memory = (output / "memory.bin").read_bytes()
    status = {name: memory[probe.integration.symbol(symbols, "r0fg1_export_" + name)]
              for name in ("permit", "status", "files")}
    expected_faults = {"capsule-guard": (107,), "nmi-sticky": (90, 91), "irq-read-error": (107,)}
    if (decoded["fault"] not in expected_faults[case] or decoded["lifecycle"] != 10
            or any(status.values())
            or decoded["resultCrc32"] != decoded["independentCrc32"]
            or (case == "nmi-sticky" and decoded["nmiSticky"] != 1)):
        raise ValueError(f"expected lockout absent: {decoded}, export={status}")
    if case == "irq-read-error":
        wire = runtime.read_json(probe.ROOT / "interfaces/r0f_group1_trace_contract.json")["constants"]
        count = wire["EPOCHS"] * wire["PHASES"] * wire["TICKS_PER_PHASE"]
        if (decoded["tickAfter"] != count
                or memory[probe.integration.symbol(symbols, "r0fg1_irq_error")] != 1):
            raise ValueError("IRQ negative did not reach the intended capture rejection")
    actual = probe.extract_actual(image, output,
                                 ["token", "rsstate"] if case == "irq-read-error" else ["token"],
                                 "G1 NEGATIVE")
    if actual["token"] != token.read_bytes():
        raise ValueError("negative fixture token changed")
    if case == "irq-read-error":
        payload = probe.integration.symbol(symbols, "r0fsi_payload").to_bytes(2, "little")
        if actual["rsstate"] != payload + runtime.expected_save(result)[2:]:
            raise ValueError("returning storage SAVE mismatch in negative run")
    if case != "irq-read-error" and runtime.sha256(image) != initial["sha256"]:
        raise ValueError("pre-storage negative mutated disk")
    runtime.write_json(output / "validation.json", {
        "result": "PASS", "case": case, "target": decoded, "export": status,
        "sourcePrgSha256": metadata["prgSha256"], "injectedPrgSha256": runtime.sha256(runtime.PRG),
        "environment": environment, "physical": "NOT RUN",
        "tier": "DIRECT_PRG_DEVELOPMENT_FAULT_INJECTION",
    })
    print(f"Integrated {case} lockout and zero export PASS")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True, choices=("capsule-guard", "nmi-sticky", "irq-read-error"))
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    run(args.case, args.out.resolve())
