#!/usr/bin/env python3
"""Local exact-name Group 1 carrier gates. No SD/physical release.

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

import r0f_group1_run as acquisition

runtime = acquisition.probe.emulator
ROOT = acquisition.probe.ROOT


def location(name):
    runtime.require_name(name)
    return ROOT / "build/r0f/group1/carriers" / name[:-4]


def checked_timing(path, mode, metadata, symbols):
    report = runtime.read_json(path / "reduction.json")
    identity = runtime.read_json(path / "build-identity.json")
    execution = runtime.read_json(path / "execution.json")
    if (identity["prgSha256"] != metadata["prgSha256"]
            or execution["videoArgument"] != mode
            or execution["status"] != 4 or execution["error"]
            or report["nominalTiming"] != "WITHIN_OBSERVED_BOUNDS"):
        raise ValueError("fresh exact-build timing admission failed")
    payload = acquisition.probe.integration.symbol(symbols, "r0fsi_payload")
    checked = acquisition.reducer.reduce((path / "trace.bin").read_bytes(),
        (path / "saved.prg").read_bytes(), payload)
    if checked != report:
        raise ValueError("timing reduction drift")


def build(name, ntsc, pal):
    metadata, prg, symbols = acquisition.checked_build()
    checked_timing(ntsc, "1", metadata, symbols)
    checked_timing(pal, "0", metadata, symbols)
    output = location(name)
    output.mkdir(parents=True, exist_ok=False)
    canonical = output / "canonical"
    canonical.mkdir()
    template = runtime.CARRIER_LOADER_SOURCE
    expected, loader = acquisition.probe.carrier_contents(canonical, prg, symbols)
    token = ROOT / "docs/evidence/r0f/successor/2026-09-21/TOKEN.prg"
    expected["token"] = token
    image = canonical / name
    constructed = runtime.fresh_d81(canonical, image, name[:-4], expected)
    image.chmod(0o444)
    shutil.copyfile(ROOT / "build/r0f/group1/integration/symbols.txt", canonical / "symbols.txt")
    inputs = {**metadata["inputs"], **{path: runtime.sha256(ROOT / path) for path in (
        "tools/diagnostics/r0f_group1_carrier.py",
        "tools/diagnostics/test_r0f_group1_carrier.py",
        "tools/diagnostics/r0f_successor_emulator.py",
        str(template.relative_to(ROOT)),
        str(runtime.CARRIER_LOADER_LINKER.relative_to(ROOT)),
    )}}
    runtime.write_json(canonical / "host-gate.json", {
        "D81_STATE": "HOST_CONTENT_VERIFIED", "D81_FILENAME": name,
        "D81_SHA256": constructed["sha256"], "D81_BYTES": image.stat().st_size,
        "label": name[:-4], "image": constructed, "build": metadata,
        "inputs": inputs, **loader,
        "timingEvidence": [str(ntsc), str(pal)],
        "sourceBranch": runtime.git_text("branch", "--show-current"),
        "sourceCommit": runtime.source_commit(),
        "canonicalMountedWritable": False,
        "sd": "NOT RUN", "physical": "NOT RUN", "testEligible": False,
        "fullGroup1Acceptance": False,
    })
    print(f"{name} HOST_CONTENT_VERIFIED; SHA-256 {constructed['sha256']}; no SD/physical release")


def checked_gate(name):
    output = location(name)
    if (output / "retirement.json").exists():
        raise ValueError("failed carrier identity retired; build a fresh name, never retest")
    canonical = output / "canonical"
    gate = runtime.read_json(canonical / "host-gate.json")
    if (runtime.sha256(canonical / name) != gate["D81_SHA256"]
            or any(runtime.sha256(ROOT / path) != digest
                   for path, digest in gate["inputs"].items())):
        raise ValueError("canonical/source drift")
    return output, canonical, gate


def _boot(name, mode, number):
    output, canonical, gate = checked_gate(name)
    run = ("ntsc" if mode == "1" else "pal") + f"-{number:02d}"
    directory = output / run
    directory.mkdir(exist_ok=False)
    image = directory / name
    shutil.copyfile(canonical / name, image)
    image.chmod(0o644)
    if runtime.sha256(image) != gate["D81_SHA256"]:
        raise ValueError("fresh exact-name copy identity")
    runtime.SOURCE_BRANCH = gate["sourceBranch"]
    _, execution = runtime.run_xemu(directory, mode, image,
        "GROUP1_EXACT_NAME_CARRIER_COPY", True, 120)
    symbols = (canonical / "symbols.txt").read_text()
    initial_names = tuple(entry["name"] for entry in gate["image"]["entries"])
    report, actual = acquisition.reduce_export(directory, image, symbols, execution,
        initial_names, gate["label"])
    for file in initial_names:
        expected = Path(gate["image"]["extracted"][file]).read_bytes()
        if actual[file] != expected:
            raise ValueError("carrier input payload changed: " + file)
    if report["nominalTiming"] != "WITHIN_OBSERVED_BOUNDS":
        raise ValueError("carrier nominal timing failed; retain copy and stop")
    checked_gate(name)
    command = execution["command"]
    if "-prg" in command or "-autoload" not in command:
        raise ValueError("not a clean carrier boot")
    runtime.write_json(directory / "validation.json", {
        "result": "PASS", "run": run, "D81_FILENAME": name,
        "canonicalSha256": gate["D81_SHA256"], "preRunSha256": gate["D81_SHA256"],
        "postRunSha256": runtime.sha256(image),
        "prgSha256": gate["build"]["prgSha256"],
        "traceSha256": runtime.sha256(directory / "trace.bin"),
        "records": report["records"], "worldPairs": report["worldEventsRetained"],
        "nominalTiming": report["nominalTiming"],
        "actualSave": "PASS", "actualExport": "PASS", "structureAndContent": "PASS",
        "cleanAutoloadNoPrgInjection": True, "canonicalUnchanged": True,
        "sd": "NOT RUN", "physical": "NOT RUN", "testEligible": False,
    })
    print(f"Exact-name {name} {run} boot/export/reduction PASS")


def boot(name, mode, number):
    output, _, gate = checked_gate(name)
    run = ("ntsc" if mode == "1" else "pal") + f"-{number:02d}"
    if (output / run).exists():
        raise ValueError("tested copy identity already exists; never retest")
    try:
        _boot(name, mode, number)
    except (Exception, SystemExit) as error:
        runtime.write_json(output / "retirement.json", {
            "D81_FILENAME": name, "canonicalSha256": gate["D81_SHA256"],
            "failedRun": run, "failure": str(error),
            "state": "RETIRED_AFTER_LOCAL_GATE_FAILURE", "sd": "NOT RUN",
            "physical": "NOT RUN", "testEligible": False,
        })
        raise


def finish(name):
    output, canonical, gate = checked_gate(name)
    runs = []
    for run in ("ntsc-01", "ntsc-02", "pal-01", "pal-02"):
        result = runtime.read_json(output / run / "validation.json")
        if (result["result"] != "PASS" or result["canonicalSha256"] != gate["D81_SHA256"]
                or result["prgSha256"] != gate["build"]["prgSha256"]):
            raise ValueError("four fresh exact-carrier successes required")
        runs.append(result)
    gate["D81_STATE"] = "XEMU_BOOT_VERIFIED"
    gate["XEMU_EVIDENCE"] = runs
    runtime.write_json(canonical / "host-gate.json", gate)
    runtime.write_json(output / "carrier-summary.json", {
        "D81_STATE": "XEMU_BOOT_VERIFIED", "D81_FILENAME": name,
        "D81_SHA256": gate["D81_SHA256"], "prgSha256": gate["build"]["prgSha256"],
        "runs": runs, "canonicalUnchanged": True,
        "sd": "NOT RUN", "physical": "NOT RUN", "testEligible": False,
        "fullGroup1Acceptance": False,
    })
    print(f"{name} XEMU_BOOT_VERIFIED only; SD/physical/acceptance remain NOT RUN")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=("build", "boot", "finish"))
    parser.add_argument("--name", required=True)
    parser.add_argument("--ntsc", type=Path)
    parser.add_argument("--pal", type=Path)
    parser.add_argument("--mode", choices=("0", "1"))
    parser.add_argument("--number", type=int, choices=(1, 2))
    args = parser.parse_args()
    if args.command == "build":
        if not args.ntsc or not args.pal:
            parser.error("build requires --ntsc and --pal complete timing evidence")
        build(args.name, args.ntsc.resolve(), args.pal.resolve())
    elif args.command == "boot":
        if args.mode is None or args.number is None:
            parser.error("boot requires --mode and --number")
        boot(args.name, args.mode, args.number)
    else:
        finish(args.name)
