#!/usr/bin/env python3
"""Isolated full-allocation export and terminal summary; local gates only.

Before D81 work read 00_D81_LOADABILITY_GATE.md and docs/D81_WORKFLOW.md.
No SD access, physical execution, commit, push or acceptance promotion.
"""
import argparse
import importlib.util
import shutil
from pathlib import Path

import r0f_group1_display_recovery as prior
import r0f_group1_owner_integration as builder

ROOT = prior.ROOT
OUT = ROOT / "build/r0f/group1/capacity-summary/integrated-02"
SOURCE = OUT / "source-inputs"
PREDECESSOR = ROOT / "build/r0f/group1/display-recovery/ram-crc-02"
read, sha, write = prior.read, prior.sha, prior.write


def preserve():
    metadata = prior.qualified(source=PREDECESSOR / "source-inputs", out=PREDECESSOR)
    gate = ROOT / "build/r0f/group1/carriers/R0FG1P03/canonical/host-gate.json"
    carrier = read(gate)
    image = gate.parent / carrier["D81_FILENAME"]
    if sha(image) != carrier["D81_SHA256"]:
        raise ValueError("passing P03 canonical drift")
    for name, digest in carrier["inputs"].items():
        if sha(ROOT / name) != digest:
            raise ValueError("passing P03 input drift: " + name)
    return metadata


def snapshot_probe():
    spec = importlib.util.spec_from_file_location("capacity_terminal_probe",
        SOURCE / "tools/diagnostics/r0f_group1_export_probe.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(label):
    builder.build(label, source=SOURCE, out=OUT, predecessor=preserve(),
                  terminal_validator=snapshot_probe().validate_terminal,
                  allow_protected_growth=True)
    shutil.copytree(SOURCE, OUT / label / "source-checkpoint")


def capacity_check(trace, output, build_label):
    builder.execute(["python3", "-B", "tools/diagnostics/r0f_group1_capacity_check.py",
        "--trace", trace, "--out", output,
        "--disassembly", OUT / (build_label + "-disassembly.txt"),
        "--symbols", OUT / (build_label + "-symbols.txt"),
        "--support-tools", ROOT / "tools/diagnostics"],
        str(output.relative_to(ROOT)).replace("/", "-") + "-controller",
        source=SOURCE, out=OUT)


def host(label, build_label):
    preserve()
    fit = read(OUT / build_label / "build.json")
    if fit["fit"] != "PASS" or fit["inputs"] != builder.inputs(SOURCE):
        raise ValueError("exact-input fit must precede host admission")
    prior.host(label, source=SOURCE, out=OUT)
    capacity_check(PREDECESSOR / "ntsc-01/trace.bin", OUT / label / "capacity.json", build_label)


def qualify(build_label, host_label):
    preserve()
    if read(OUT / host_label / "capacity.json")["result"] != "PASS":
        raise ValueError("capacity/summary host gate incomplete")
    prior.qualify(build_label, host_label, source=SOURCE, out=OUT)


def operator_check(directory, *, expected_failure=False):
    labels = read(OUT / "qualification.json")
    symbols = (OUT / (labels["build_label"] + "-symbols.txt")).read_text()
    symbol = prior.previous.probe.integration.symbol
    memory = (directory / "memory.bin").read_bytes()
    start = symbol(symbols, "r0fg1_operator_text")
    end = symbol(symbols, "r0fg1_operator_text_end")
    text = memory[start:end]
    values = {name: memory[symbol(symbols, "r0fg1_export_" + name)]
              for name in ("status", "error", "files")}
    if expected_failure:
        valid = values["status"] == 5 and values["error"] != 0 and values["files"] == 0
    else:
        valid = values == {"status": 4, "error": 0, "files": 20}
    expected = (b"\x93" + f"G1 EXPORT S:{values['status']} E:{values['error']:02X} F:{values['files']:02X}\r".encode("ascii")
                + b"4=OK 5=FAIL / E,F HEX\r"
                b"REDUCE FOR TIMING\rNOT ACCEPTANCE\rRESET\r\0")
    if not valid or text != expected:
        raise ValueError("operator summary does not match actual completed export")
    write(directory / "operator-summary.json", {
        "result": "PASS_EXPECTED_EXPORT_FAILURE" if expected_failure else "PASS_PROTECTED_TEXT", **values,
        "text": text[1:-1].decode("ascii").replace("\r", "\n"),
        "screenReview": "REQUIRED", "scope": "Export outcome, not timing acceptance"})


def negative_export():
    # A pre-existing first trace filename must reject, never replace/retry.
    fit = prior.qualified(source=SOURCE, out=OUT)
    output = OUT / "export-failure-01"
    output.mkdir(exist_ok=False)
    write(output / "build-identity.json", fit)
    labels = read(OUT / "qualification.json")
    prg = output / "GROUP1.prg"
    shutil.copyfile(OUT / labels["build_label"] / "GROUP1.prg", prg)
    probe = prior.previous.probe
    probe.emulator.PRG = prg
    probe.emulator.SOURCE_BRANCH = probe.emulator.git_text("branch", "--show-current")
    image = output / "G1FAIL01.D81"
    token = ROOT / "docs/evidence/r0f/successor/2026-09-21/TOKEN.prg"
    probe.emulator.fresh_d81(output, image, "G1 CAP FAILURE", {"token": token, "g1t00": token})
    _, execution = probe.emulator.run_xemu(output, "1", image,
        "GROUP1_UNCHANGED_PRG_EXPORT_NAME_COLLISION", False, 120)
    write(output / "execution.json", execution)
    finish_negative_export()


def finish_negative_export():
    # Reduce an already finished fixture read-only; never relaunch or retest it.
    output = OUT / "export-failure-01"
    fit = read(output / "build-identity.json")
    prg = output / "GROUP1.prg"
    if sha(prg) != fit["prgSha256"]:
        raise ValueError("negative fixture PRG identity drift")
    probe = prior.previous.probe
    operator_check(output, expected_failure=True)
    if read(output / "operator-summary.json")["error"] != 3:
        raise ValueError("not the pinned KERNAL filename-collision error")
    image = output / "G1FAIL01.D81"
    token = ROOT / "docs/evidence/r0f/successor/2026-09-21/TOKEN.prg"
    actual = probe.extract_actual(image, output, ["token", "g1t00", "rsstate"], "G1 CAP FAILURE")
    if actual["token"] != token.read_bytes() or actual["g1t00"] != token.read_bytes():
        raise ValueError("failed export replaced a pre-existing payload")
    import r0f_group1_reduce as core_oracle
    result = (output / "result.bin").read_bytes()
    probe.emulator.validate_success_result(result, (1600, 3200), core_oracle.golden((1600, 3200)))
    labels = read(OUT / "qualification.json")
    symbols = (OUT / (labels["build_label"] + "-symbols.txt")).read_text()
    probe.validate_saved(actual["rsstate"], result, symbols)
    write(output / "validation.json", {
        "result": "PASS_EXPECTED_EXPORT_FAILURE", "prgSha256": sha(prg),
        "firstTraceFilenameCollision": "REJECTED", "filesExported": 0,
        "preExistingFilesUnchanged": True, "structureAndContent": "PASS",
        "actualReturningSave": "PASS", "originalSuccessorResult": "PASS",
        "scope": "Fail-closed terminal error output, not a timing acquisition proof",
        "retry": "NONE", "SD": "NOT RUN", "physical": "NOT RUN"})
    preserve()
    print("Actual unchanged-PRG export collision rejected, old bytes preserved, failure summary PASS")


def run(mode):
    preserve()
    labels = read(OUT / "qualification.json")
    prior.previous.run(mode, source=SOURCE, out=OUT, image_name="G1CAP02.D81",
        run_identity="GROUP1_INTEGRATED_CAPACITY_SUMMARY_DEVELOPMENT", **labels)
    folder = OUT / (mode + "-01")
    prior.negative(mode, source=SOURCE, out=OUT)
    capacity_check(folder / "trace.bin", folder / "capacity.json", labels["build_label"])
    operator_check(folder)
    preserve()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("build", "host", "qualify", "run", "negative-export", "negative-check", "operator", "capacity"))
    parser.add_argument("--label")
    parser.add_argument("--build-label", default="runtime-01")
    parser.add_argument("--host-label", default="host-01")
    parser.add_argument("--mode", choices=("ntsc", "pal"))
    parser.add_argument("--directory", type=Path)
    args = parser.parse_args()
    if args.action == "build":
        if not args.label:
            parser.error("build requires a fresh label")
        build(args.label)
    elif args.action == "host":
        host(args.host_label, args.build_label)
    elif args.action == "qualify":
        qualify(args.build_label, args.host_label)
    elif args.action == "run":
        if not args.mode:
            parser.error("run requires a video mode")
        run(args.mode)
    elif args.action == "negative-export":
        negative_export()
    elif args.action == "negative-check":
        finish_negative_export()
    else:
        if args.directory is None:
            parser.error("operator/capacity require the actual run directory")
        if args.action == "operator":
            operator_check(args.directory.resolve())
        else:
            labels = read(OUT / "qualification.json")
            capacity_check(args.directory.resolve() / "trace.bin",
                           args.directory.resolve() / "capacity.json", labels["build_label"])
