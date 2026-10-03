#!/usr/bin/env python3
"""Native extracted resume boundary with explicit hardware mocks, never hardware proof."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def function(text, signature):
    start = text.index(signature)
    opening = text.index("{", start)
    while ";" in text[start:opening]:
        start = text.index(signature, start + len(signature))
        opening = text.index("{", start)
    depth = 1
    end = opening + 1
    while depth:
        depth += (text[end] == "{") - (text[end] == "}")
        end += 1
    return text[start:end] + "\n"


def validate(source, baseline, out):
    out.mkdir(parents=True, exist_ok=False)
    commands = []
    for name, root in (("baseline", baseline), ("candidate", source)):
        directory = out / name
        directory.mkdir()
        integration = (root / "src/diagnostics/r0f/successor_integration.c").read_text()
        platform = (root / "src/diagnostics/r0f/combined_platform.c").read_text()
        pieces = [function(platform, signature) for signature in (
            "uint8_t cfclock_begin(void)", "uint32_t cfnow(void)",
            "uint8_t cfdma(uint32_t")]
        pieces += [function(integration, signature) for signature in (
            "static uint8_t application_dma(", "static uint8_t display_seed_staging(",
            "static uint8_t display_resume(", "static void lockout(",
            "static uint8_t transition(")]
        storage = function(integration, "static uint8_t storage_transition(")
        # Exercise the actual post-restore suffix, with restored local values.
        suffix = storage[storage.index("    r0fs_context_invalidate();"):]
        pieces.append("static uint8_t resume_boundary(void)\n{\n"
            "    uint16_t tick_before = 1600u;\n"
            "    uint32_t checksum_before = 0x6b765fdbul;\n"
            "    uint32_t low_before = 1u, low_after = 1u;\n"
            "    uint32_t dos_before = 2u, dos_after = 2u;\n" + suffix)
        (directory / "resume_under_test.inc").write_text("\n".join(pieces))
        executable = directory / "resume-host"
        command = ["/usr/bin/clang", "-std=c11", "-Wall", "-Wextra", "-Werror",
            "-fsanitize=address,undefined", "-DR0FG1_INTEGRATION",
            "-DTEST_BASELINE=" + str(int(name == "baseline")),
            "-I" + str(directory), "-I" + str(root / "interfaces/generated"),
            "-I" + str(root / "src/diagnostics/r0f"),
            str(Path(__file__).with_name("r0f_group1_resume_host_test.c")),
            str(root / "src/diagnostics/r0f/successor_lifecycle.c"), "-o", str(executable)]
        for label, argv in (("compile", command), ("run", [str(executable)])):
            result = subprocess.run(argv, text=True, capture_output=True, timeout=60)
            (directory / (label + ".txt")).write_text(result.stdout + result.stderr)
            commands.append({"command": argv, "exitCode": result.returncode})
            result.check_returncode()
    path = source / "src/diagnostics/r0f/successor_integration.c"
    report = {"result": "PASS", "sourceSha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "commands": commands,
        "baseline": "Stopped-at-FFFF CIA mock produces inner 3 masked as 93",
        "candidate": "Clock precedes 15 clears; state/copy/DMA/clock faults retained; restoration, NMI and IRQ override reject",
        "scope": "Extracted actual resume/display/clock/DMA functions; mocked physical edges",
        "physicalCauseConfirmed": False}
    (out / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print("Resume ordering and first-fault native ASan/UBSan checks PASS")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    validate(args.source.resolve(), args.baseline.resolve(), args.out.resolve())
