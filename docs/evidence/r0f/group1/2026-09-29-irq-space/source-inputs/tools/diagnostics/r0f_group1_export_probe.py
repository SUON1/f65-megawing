#!/usr/bin/env python3
"""Build a development-only terminal-export probe, never a delivery artifact.

Read 00_D81_LOADABILITY_GATE.md before invoking the run command. Each local
probe uses a fresh token-only image in an exclusive output directory. It is
not an exact-carrier gate, SD operation, or Group 1 workload qualification.
"""

import argparse
import binascii
import json
from pathlib import Path
import re

import r0f_group1_export_admission as admission
import r0f_successor_emulator as emulator
import r0f_successor_integration as integration


ROOT = integration.ROOT
OUT = ROOT / "build/r0f/group1/export-probe"
PRG = OUT / "EXPORT-PROBE.prg"
EXTRA_SOURCES = [
    "src/diagnostics/r0f/group1_export.c",
    "src/diagnostics/r0f/group1_transport.c",
    "src/diagnostics/r0f/group1_export_probe.c",
    "src/platform/r0f/group1_export_capture_45gs02.s",
    "src/platform/r0f/group1_terminal_export_45gs02.s",
]


def build(defines=("-DR0FG1_EXPORT_QUALIFICATION",), scope="terminal export development probe; not Group 1 workload",
          out=OUT, prg_name="EXPORT-PROBE.prg", extra_sources=None, source_replacements=None):
    prg = out / prg_name
    sources = EXTRA_SOURCES if extra_sources is None else extra_sources
    admission.main()
    out.mkdir(parents=True, exist_ok=True)
    mapping = prg.with_suffix(".map")
    replacements = source_replacements or {}
    target_sources = [replacements.get(name, name) for name in integration.TARGET_SOURCES]
    integration.compile_target(target_sources + sources,
                               prg, mapping, defines)
    elf = Path(str(prg) + ".elf")
    symbols = integration.run([integration.platform_build.TOOLS / "llvm-nm", elf],
                              capture_output=True, text=True).stdout
    (out / "symbols.txt").write_text(symbols)
    sections = integration.section_inventory(mapping.read_text())
    protected = sections[".r0fs_protected"]
    if protected["start"] + protected["bytes"] > 0x4000:
        raise ValueError("terminal exporter overlaps staging")
    for name in (".text", ".rodata", ".data", ".bss", ".noinit"):
        section = sections[name]
        if section["start"] + section["bytes"] > 0xc000:
            raise ValueError("probe exceeds resident envelope: " + name)
    if not (integration.symbol(symbols, "r0fs_pre_c_capture")
            < integration.symbol(symbols, "r0fg1_export_capture")
            < integration.symbol(symbols, "f65_basepage_enter")
            < integration.symbol(symbols, "__do_zero_bss")):
        raise ValueError("export capture must precede C initialization")
    disassembly = integration.run([
        integration.platform_build.TOOLS / "llvm-objdump", "-d", "--print-imm-hex", elf,
    ], capture_output=True, text=True).stdout
    (out / "disassembly.txt").write_text(disassembly)
    terminal = disassembly.split("<r0fg1_terminal_export>:", 1)[1].split(
        "<r0fg1_terminal_export_end>:", 1)[0]
    if re.search(r"\brts\b|\brti\b", terminal):
        raise ValueError("terminal path must not return")
    if re.search(r"\$[89ab][0-9a-f]{3}\b", terminal):
        raise ValueError("terminal path references mapped application memory")
    calls = re.findall(r"\bjsr\s+\$([0-9a-f]+)", terminal)
    if set(calls) != {"ff87", "ff84", "ff8a", "ff81", "ffcc", "ff90",
                      "ff6b", "ffba", "ffbd", "ffd8"}:
        raise ValueError("terminal ROM call allowlist")
    inputs = set(integration.TARGET_SOURCES + target_sources + sources)
    for directory, patterns in (
            ("src/diagnostics/r0f", ("*.h",)),
            ("src/platform/r0f", ("*.inc", "*.ld")),
            ("interfaces/generated", ("*.h", "*.inc")),
            ("interfaces", ("r0f*contract.json",)),
            ("memory", ("r0f*ledger.json",))):
        for pattern in patterns:
            inputs.update(str(path.relative_to(ROOT))
                          for path in (ROOT / directory).glob(pattern))
    inputs.update(("tools/diagnostics/r0f_group1_export_probe.py",
                   "tools/diagnostics/r0f_group1_export_admission.py",
                   "tools/diagnostics/r0f_successor_integration.py"))
    report = {
        "scope": scope,
        "prgBytes": prg.stat().st_size, "prgSha256": emulator.sha256(prg),
        "symbolsSha256": emulator.sha256(out / "symbols.txt"),
        "inputs": {name: emulator.sha256(ROOT / name) for name in sorted(inputs)},
        "sections": sections, "targetStatic": "PASS",
        "xemu": "NOT RUN", "sd": "NOT RUN", "physical": "NOT RUN",
    }
    emulator.write_json(out / "build.json", report)
    print(json.dumps(report, indent=2))


def extract_actual(image, output, names, label="G1 EXP PROBE"):
    """Compare pinned-tool extraction with the independent chain/BAM parser."""
    actual = {}
    extraction = output / "actual"
    extraction.mkdir()
    for name in names:
        path = extraction / name
        emulator.c154([image, "-read", name, path])
        actual[name] = path.read_bytes()
    post = emulator.check_disk(image, actual, label, "65",
                               output / "post-extracted")
    emulator.write_json(output / "post-disk.json", post)
    return actual


def run_probe(output, mode, case):
    build_report = emulator.read_json(OUT / "build.json")
    if (emulator.sha256(PRG) != build_report["prgSha256"]
            or emulator.sha256(OUT / "symbols.txt") != build_report["symbolsSha256"]
            or any(emulator.sha256(ROOT / name) != digest
                   for name, digest in build_report["inputs"].items())):
        raise ValueError("probe artifact drift: rebuild before running")
    output.mkdir(parents=True, exist_ok=False)
    emulator.write_json(output / "build-identity.json", build_report)
    emulator.PRG = PRG
    emulator.SOURCE_BRANCH = emulator.git_text("branch", "--show-current")
    token = ROOT / "docs/evidence/r0f/successor/2026-09-21/TOKEN.prg"
    image = output / "G1EXP01.D81"
    contents = {"token": token}
    marker = b"\x00\x40EXISTING TRACE MUST SURVIVE"
    if case == "existing":
        marker_path = output / "existing.prg"
        marker_path.write_bytes(marker)
        contents["g1t00"] = marker_path
    emulator.fresh_d81(output, image, "G1 EXP PROBE", contents)
    _, execution = emulator.run_xemu(output, mode, image, "DEVELOPMENT_EXPORT_PROBE", False)
    memory = (output / "memory.bin").read_bytes()
    symbols = (OUT / "symbols.txt").read_text()
    status = memory[integration.symbol(symbols, "r0fg1_export_status")]
    files = memory[integration.symbol(symbols, "r0fg1_export_files")]
    error = memory[integration.symbol(symbols, "r0fg1_export_error")]
    if case == "existing":
        actual = extract_actual(image, output, ("token", "g1t00", "rsstate"))
        if status != 5 or files != 0 or actual["g1t00"] != marker:
            raise ValueError(f"existing-file rejection status={status}, files={files}, error={error}")
        emulator.write_json(output / "export-validation.json", {
            "scope": "existing-file rejection only", "result": "PASS",
            "status": status, "files": files, "error": error,
            "existingFileUnchanged": True, "execution": execution,
            "prgSha256": build_report["prgSha256"], "physical": "NOT RUN",
        })
        print("Terminal export existing-file rejection PASS: preserved, no retry/resume")
        return
    if status != 4 or files != 3:
        raise ValueError(f"terminal export status={status}, files={files}, error={error}")
    # Extract actual post-run files using pinned tooling and independent structure checks.
    actual = extract_actual(image, output,
                            ("token", "rsstate", "g1t00", "g1t01", "g1t02"))
    chunks = []
    for index, length in enumerate((16384, 16384, 257)):
        data = actual[f"g1t{index:02d}"]
        if len(data) != length + 2 or data[:2] != b"\x00\x40":
            raise ValueError("export chunk framing")
        chunks.append(data[2:])
    trace = b"".join(chunks)
    result = trace[:512]
    decoded = emulator.validate_success_result(result)
    if trace[512:] != bytes((position ^ (position >> 8) ^ 0x71) & 255
                            for position in range(512, 33025)):
        raise ValueError("exported trace differs from deterministic input")
    saved = actual["rsstate"]
    expected_payload = emulator.expected_save(result)[2:]
    if (saved[:2] != integration.symbol(symbols, "r0fsi_payload").to_bytes(2, "little")
            or saved[2:] != expected_payload):
        raise ValueError("actual first storage result")
    (output / "exported-result.bin").write_bytes(result)
    (output / "exported-trace.bin").write_bytes(trace)
    emulator.write_json(output / "export-validation.json", {
        "scope": "export qualification only", "result": "PASS",
        "actualFiles": 3, "traceBytes": len(trace),
        "traceCrc32": f"{binascii.crc32(trace) & 0xffffffff:08X}",
        "successorResult": decoded, "execution": execution,
        "prgSha256": build_report["prgSha256"],
        "physical": "NOT RUN", "fullGroup1": "NOT RUN",
    })
    print("Terminal export probe PASS: actual result/SAVE and 33025 exported bytes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "run"))
    parser.add_argument("--out", type=Path)
    parser.add_argument("--mode", choices=("0", "1"), default="1")
    parser.add_argument("--case", choices=("normal", "existing"), default="normal")
    args = parser.parse_args()
    if args.command == "build":
        build()
    elif args.out is None:
        parser.error("run requires a new --out directory")
    else:
        run_probe(args.out.resolve(), args.mode, args.case)
