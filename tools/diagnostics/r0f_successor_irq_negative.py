#!/usr/bin/env python3
"""Exercise T09 IRQ fail-closed behavior in disposable development fixtures.

MANDATORY D81 LOADABILITY GATE: read 00_D81_LOADABILITY_GATE.md before use.
Fresh token-only D81; never an SD candidate. The injected PRG is a local test
derivative, not a modification to any canonical or previously tested image.
"""

import argparse
import binascii
import json
from pathlib import Path
import re

import r0f_successor_emulator as runtime


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--good-run", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    if args.out.exists():
        raise ValueError("refusing to replace negative-test evidence")
    accounting = json.loads(runtime.ACCOUNTING.read_text())
    original = runtime.PRG.read_bytes()
    if (runtime.sha256(runtime.PRG) != accounting["prgSha256"]
            or any(runtime.sha256(runtime.ROOT / path) != digest
                   for path, digest in accounting["inputs"].items())):
        raise ValueError("target/source identity drift")
    disassembly = runtime.PRG.with_suffix(".disassembly").read_text()
    routine = disassembly.split("<r0f_pf_start_irq>:", 1)[1]
    routine = routine.split("<r0f_pf_stop_irq>:", 1)[0]
    matches = re.findall(r"^\s*([0-9a-f]+): 58\s+cli\s*$", routine, re.M)
    if len(matches) != 1:
        raise ValueError("expected one CLI in checked IRQ restart")
    address = int(matches[0], 16)
    load_address = int.from_bytes(original[:2], "little")
    offset = address - load_address + 2
    if original[offset] != 0x58:
        raise ValueError("IRQ restart byte mismatch")

    args.out.mkdir(parents=True)
    runtime.OUT = args.out.resolve()
    runtime.SOURCE_BRANCH = runtime.git_text("branch", "--show-current")
    classes = runtime.OUT / "classes"
    classes.mkdir()
    runtime.checked_run([
        runtime.platform_build.JAVA / "javac", "-Xlint:all", "-Werror",
        "-d", classes, runtime.ROOT / runtime.ORACLE_SOURCE,
    ])
    good = (args.good_run / "result.bin").read_bytes()
    saved = (args.good_run / "saved.prg").resolve()
    runtime.validate_success_result(good)
    runtime.java_oracle(args.good_run / "result.bin", saved)
    reducer_tests = []
    for name, before, after, should_pass in (
            ("forged-mask-without-irq", 123, 123, False),
            ("counter-rollover", 65535, 0, True)):
        result = bytearray(good)
        result[60:62] = before.to_bytes(2, "little")
        result[62:64] = after.to_bytes(2, "little")
        result[508:] = (binascii.crc32(result[:508]) & 0xFFFFFFFF).to_bytes(4, "little")
        path = runtime.OUT / (name + ".bin")
        path.write_bytes(result)
        try:
            runtime.validate_success_result(result)
            python_pass = True
        except ValueError:
            python_pass = False
        java = runtime.java_oracle(path, saved, check=False)
        if python_pass != should_pass or (java.returncode == 0) != should_pass:
            raise ValueError("reducer verdict mismatch: " + name)
        reducer_tests.append({"case": name, "expectedPass": should_pass,
                              "pythonPass": python_pass,
                              "javaReturnCode": java.returncode,
                              "javaStderr": java.stderr})

    directory = runtime.OUT / "no-raster-irq"
    directory.mkdir()
    mutated = bytearray(original)
    mutated[offset] = 0x78  # SEI, solely in this disposable PRG derivative.
    runtime.PRG = directory / "IRQ-OFF.prg"
    runtime.PRG.write_bytes(mutated)
    token = directory / "TOKEN.prg"
    token.write_bytes(runtime.token_bytes())
    image = directory / "IRQNEG10.D81"
    initial = runtime.fresh_d81(directory, image, "R0F IRQ NEG", {"token": token})
    result, environment = runtime.run_xemu(
        directory, "1", image, "DIRECT_PRG_FAULT", False)
    decoded = runtime.decode_result(result)
    if (decoded["fault"] != 101 or decoded["lifecycle"] != 10
            or decoded["tickAfter"] != 66 or decoded["resumedServiceMask"] != 0x17
            or decoded["irqBefore"] != decoded["irqAfter"]
            or decoded["stage"] == 127
            or decoded["resultCrc32"] != decoded["independentCrc32"]):
        raise ValueError("disabled IRQ did not produce exact fault-65 lockout")
    post = runtime.check_disk(
        image, {"token": token.read_bytes(), "rsstate": runtime.expected_save(result)},
        "R0F IRQ NEG", runtime.CANONICAL_ID, directory / "post-extracted")
    runtime.write_json(runtime.OUT / "summary.json", {
        "result": "PASS", "tier": "DEVELOPMENT_FAULT_INJECTION_NOT_CARRIER",
        "sourcePrgSha256": accounting["prgSha256"],
        "injectedPrgSha256": runtime.sha256(runtime.PRG),
        "injection": {"address": address, "old": "58 CLI", "new": "78 SEI"},
        "initialD81Sha256": initial["sha256"],
        "postRunD81Sha256": post["sha256"],
        "target": decoded, "environment": environment,
        "reducerTests": reducer_tests, "physical": "NOT RUN",
    })
    print("T09 disabled-IRQ fault 65 and independent reducer checks PASS")


if __name__ == "__main__":
    main()
