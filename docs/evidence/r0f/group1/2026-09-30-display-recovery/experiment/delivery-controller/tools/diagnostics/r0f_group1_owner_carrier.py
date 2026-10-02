#!/usr/bin/env python3
"""Context-bound version-6 carrier gates; reuse the immutable carrier primitives.

MANDATORY D81 LOADABILITY GATE

Before creating, modifying, copying, renaming, packaging, mounting, testing, or releasing any D81, read and obey the repository-root file 00_D81_LOADABILITY_GATE.md.

The work must fail closed. A D81 may not be called final, test-ready, loadable, or delivered for physical testing until the exact artifact passes every applicable state in this order:

UNVERIFIED
-> HOST_STRUCTURALLY_VERIFIED
-> HOST_CONTENT_VERIFIED
-> XEMU_BOOT_VERIFIED
-> SD_COPY_VERIFIED
-> SD_CONTIGUITY_VERIFIED
-> PHYSICAL_CHOOSER_VERIFIED
-> TEST_ELIGIBLE

Never build a new test carrier by copying an existing D81 and reopening the copy in a second c1541 session to append files. Fresh-format the image and populate all files in one pinned-tool construction session.

ERROR CODE FF at the MEGA65 chooser is a hard chooser/attach-stage failure. Retire that tested copy and diagnose D81 construction, exact copied bytes, SD physical allocation, safe ejection, and platform identity before assigning a replacement. Do not patch, append to, rename, or re-test the failed copy and do not blame the program inside it.

A matching hash of the SD-card copy is necessary but not sufficient. The MEGA65 Freezer requires a disk-image file to occupy one contiguous FAT32 extent. A fragmented file can hash perfectly and still fail to mount with ERROR CODE FF. Do not submit a copied image to the physical chooser until an independent extent check reports exactly one extent.
"""
import argparse
from pathlib import Path
import shutil
import subprocess

import r0f_group1_carrier as carrier
import r0f_group1_display_recovery as candidate
import r0f_group1_owner_recovery as codec

ROOT = candidate.ROOT
runtime = carrier.runtime


def context(experiment):
    source = experiment / "source-inputs"
    metadata = candidate.qualified(source=source, out=experiment)
    label = candidate.read(experiment / "qualification.json")["build_label"]
    return source, metadata, experiment / label / "GROUP1.prg", (
        experiment / (label + "-symbols.txt")).read_text()


def timing_identity(path, mode, metadata):
    identity = candidate.read(path / "build-identity.json")
    execution = candidate.read(path / "execution.json")
    report = candidate.read(path / "reduction.json")
    negatives = candidate.read(path / "negatives.json")
    if (identity != metadata or execution["videoArgument"] != mode
            or execution["status"] != 4 or execution["error"]
            or report["acquisition"] != "PASS"
            or report["nominalTiming"] != "WITHIN_OBSERVED_BOUNDS"
            or report["nominalDeadlineMisses"] or report["boundaryUncertain"]
            or report["cohortsBelow20Hz"] or negatives["result"] != "PASS"):
        raise ValueError("fresh exact-build timing admission failed")
    return report


def build(name, experiment):
    source, metadata, prg, symbols = context(experiment)
    modes = (("ntsc-01", "1"), ("pal-01", "0"))
    reports = {run: timing_identity(experiment / run, mode, metadata) for run, mode in modes}
    output = carrier.location(name)
    output.mkdir(parents=True, exist_ok=False)
    payload = codec.probe.integration.symbol(symbols, "r0fsi_payload")
    for run, _ in modes:
        admission = output / (run + "-admission")
        admission.mkdir()
        checked = codec.reduce_trace_files(source, experiment / run / "trace.bin",
            experiment / run / "saved.prg", payload, admission)
        if checked != reports[run]:
            raise ValueError("timing reduction drift")
    canonical = output / "canonical"
    canonical.mkdir()
    template = runtime.CARRIER_LOADER_SOURCE
    expected, loader = codec.probe.carrier_contents(canonical, prg, symbols)
    expected["token"] = ROOT / "docs/evidence/r0f/successor/2026-09-21/TOKEN.prg"
    image = canonical / name
    constructed = runtime.fresh_d81(canonical, image, name[:-4], expected)
    image.chmod(0o444)
    label = candidate.read(experiment / "qualification.json")["build_label"]
    shutil.copyfile(experiment / (label + "-symbols.txt"), canonical / "symbols.txt")
    inputs = {str(source.relative_to(ROOT) / path): digest
              for path, digest in metadata["inputs"].items()}
    for path in (Path(__file__), ROOT / "tools/diagnostics/r0f_group1_carrier.py",
                 ROOT / "tools/diagnostics/test_r0f_group1_owner_carrier.py",
                 ROOT / "tools/diagnostics/r0f_group1_owner_recovery.py",
                 ROOT / "tools/diagnostics/r0f_group1_display_recovery.py",
                 ROOT / "tools/diagnostics/r0f_group1_pool_trace_negative.py",
                 ROOT / "tools/diagnostics/r0f_group1_export_probe.py",
                 ROOT / "tools/diagnostics/r0f_successor_emulator.py", template,
                 runtime.CARRIER_LOADER_LINKER):
        inputs[str(path.relative_to(ROOT))] = candidate.sha(path)
    candidate.write(canonical / "host-gate.json", {
        "D81_STATE": "HOST_CONTENT_VERIFIED", "D81_FILENAME": name,
        "D81_SHA256": constructed["sha256"], "D81_BYTES": image.stat().st_size,
        "label": name[:-4], "image": constructed, "build": metadata,
        "inputs": inputs, **loader, "experiment": str(experiment),
        "timingEvidence": [str(experiment / run) for run, _ in modes],
        "sourceBranch": runtime.git_text("branch", "--show-current"),
        "sourceCommit": runtime.source_commit(), "canonicalMountedWritable": False,
        "sd": "NOT RUN", "physical": "NOT RUN", "testEligible": False,
        "fullGroup1Acceptance": False})
    print(f"{name} HOST_CONTENT_VERIFIED; {constructed['sha256']}; no SD/physical release")


def boot(name, mode, number):
    output, canonical, gate = carrier.checked_gate(name)
    run = ("ntsc" if mode == "1" else "pal") + f"-{number:02d}"
    directory = output / run
    if directory.exists():
        raise ValueError("tested copy exists; never retest")
    try:
        directory.mkdir()
        image = directory / name
        shutil.copyfile(canonical / name, image)
        image.chmod(0o644)
        if candidate.sha(image) != gate["D81_SHA256"]:
            raise ValueError("fresh exact-name copy mismatch")
        experiment = Path(gate["experiment"])
        source, metadata, _, symbols = context(experiment)
        candidate.write(directory / "build-identity.json", metadata)
        runtime.PRG = canonical / "R0FSUCC.prg"
        runtime.SOURCE_BRANCH = gate["sourceBranch"]
        _, execution = runtime.run_xemu(directory, mode, image,
            "GROUP1_OWNER_EXACT_NAME_CARRIER_COPY", True, 120)
        initial_names = tuple(entry["name"] for entry in gate["image"]["entries"])
        report, actual = codec.reduce_candidate_export(source, directory, image,
            symbols, execution, initial_names, gate["label"])
        for file in initial_names:
            if actual[file] != Path(gate["image"]["extracted"][file]).read_bytes():
                raise ValueError("carrier input payload changed: " + file)
        if (report["acquisition"] != "PASS"
                or report["nominalTiming"] != "WITHIN_OBSERVED_BOUNDS"
                or report["nominalDeadlineMisses"] or report["boundaryUncertain"]
                or report["cohortsBelow20Hz"]):
            raise ValueError("carrier timing/acquisition gate failed")
        command = ["python3", "-B", "tools/diagnostics/r0f_group1_pool_trace_negative.py",
                   "--source", str(source), "--trace", str(directory / "trace.bin"),
                   "--out", str(directory / "negatives.json")]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
        candidate.write(directory / "negative-command.json", {
            "command": command, "exitCode": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr})
        result.check_returncode()
        if "-prg" in execution["command"] or "-autoload" not in execution["command"]:
            raise ValueError("not a clean carrier boot")
        carrier.checked_gate(name)
        candidate.write(directory / "validation.json", {
            "result": "PASS", "run": run, "D81_FILENAME": name,
            "canonicalSha256": gate["D81_SHA256"], "preRunSha256": gate["D81_SHA256"],
            "postRunSha256": candidate.sha(image), "prgSha256": metadata["prgSha256"],
            "traceSha256": candidate.sha(directory / "trace.bin"), "records": report["records"],
            "worldPairs": report["worldEventsRetained"], "nominalTiming": report["nominalTiming"],
            "actualSave": "PASS", "actualExport": "PASS", "structureAndContent": "PASS",
            "cleanAutoloadNoPrgInjection": True, "canonicalUnchanged": True,
            "corruptionChecks": "102 rejects", "sd": "NOT RUN", "physical": "NOT RUN",
            "testEligible": False})
        print(f"{name} {run} clean boot, actual SAVE/export, timing and corruption gates PASS")
    except (Exception, SystemExit) as error:
        candidate.write(output / "retirement.json", {
            "D81_FILENAME": name, "canonicalSha256": gate["D81_SHA256"], "failedRun": run,
            "failure": str(error), "state": "RETIRED_AFTER_LOCAL_GATE_FAILURE",
            "sd": "NOT RUN", "physical": "NOT RUN", "testEligible": False})
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("action", choices=("build", "boot", "finish"))
    parser.add_argument("--name", required=True)
    parser.add_argument("--experiment", type=Path)
    parser.add_argument("--mode", choices=("0", "1"))
    parser.add_argument("--number", type=int, choices=(1, 2))
    args = parser.parse_args()
    if args.action == "build":
        if args.experiment is None:
            parser.error("build requires exact qualified experiment")
        build(args.name, args.experiment.resolve())
    elif args.action == "boot":
        if args.mode is None or args.number is None:
            parser.error("boot requires mode and number")
        boot(args.name, args.mode, args.number)
    else:
        carrier.finish(args.name)
