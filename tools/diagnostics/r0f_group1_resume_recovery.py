#!/usr/bin/env python3
"""Bounded copied-source P05 resume correction; local fit/host/Xemu only.

Before D81 actions read 00_D81_LOADABILITY_GATE.md and docs/D81_WORKFLOW.md.
The capacity controller instance below has explicit experiment paths; imported
historical controllers and their qualified inputs are never modified.
"""
import argparse
import importlib.util
import shutil
import subprocess
from pathlib import Path

import r0f_group1_owner_integration as builder
import r0f_group1_owner_recovery as runner

ROOT = builder.ROOT
OUT = ROOT / "build/r0f/group1/resume-recovery/clock-03"
SOURCE = OUT / "source-inputs"
FROZEN = ROOT / "docs/evidence/r0f/group1/2026-10-01-capacity-summary"
BASELINE = FROZEN / "experiment/runtime-01"
PATCH = Path(__file__).with_name("r0f_group1_resume_clock.patch")
RESUME_HOST = "resume-host-02"
read, sha, write = builder.read, builder.sha, builder.write


def preserve():
    manifest = read(FROZEN / "sha256.json")["files"]
    for name, digest in manifest.items():
        if sha(FROZEN / name) != digest:
            raise ValueError("P05 frozen evidence drift: " + name)
    fit = read(BASELINE / "build.json")
    if sha(BASELINE / "GROUP1.prg") != fit["prgSha256"]:
        raise ValueError("P05 PRG drift")
    if builder.inputs(BASELINE / "source-checkpoint") != fit["inputs"]:
        raise ValueError("P05 source identity mismatch")
    return fit


def controller():
    spec = importlib.util.spec_from_file_location("resume_capacity_controller",
        ROOT / "tools/diagnostics/r0f_group1_capacity_summary.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.OUT, module.SOURCE = OUT, SOURCE
    return module


def carrier_controller():
    spec = importlib.util.spec_from_file_location("resume_carrier_controller",
        ROOT / "tools/diagnostics/r0f_group1_capacity_carrier.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.candidate = controller()
    return module


def prepare():
    fit = preserve()
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copytree(BASELINE / "source-checkpoint", SOURCE)
    command = ["patch", "--batch", "--fuzz=0", "-p1", "-i", str(PATCH)]
    result = subprocess.run(command, cwd=SOURCE, text=True, capture_output=True)
    write(OUT / "preparation.json", {"baseline": str(BASELINE),
        "baselinePrgSha256": fit["prgSha256"], "patchSha256": sha(PATCH),
        "command": command, "exitCode": result.returncode,
        "stdout": result.stdout, "stderr": result.stderr})
    result.check_returncode()
    changed = [name for name, digest in builder.inputs(SOURCE).items()
               if fit["inputs"].get(name) != digest]
    if changed != ["src/diagnostics/r0f/successor_integration.c"]:
        raise ValueError("unexpected target changes: " + repr(changed))
    print("P05 snapshot copied; one target source changed; predecessors preserved")


def build():
    baseline = preserve()
    preparation = read(OUT / "preparation.json")
    if preparation["exitCode"] or preparation["patchSha256"] != sha(PATCH):
        raise ValueError("successful exact-patch preparation must precede build")
    builder.build("runtime-01", source=SOURCE, out=OUT, predecessor=baseline,
                  terminal_validator=controller().snapshot_probe().validate_terminal)
    shutil.copytree(SOURCE, OUT / "runtime-01/source-checkpoint")
    if read(OUT / "runtime-01/build.json")["fit"] != "PASS":
        raise ValueError("resident fit failed; candidate must not execute")


def host():
    controller().host("host-01", "runtime-01")
    resume_host()


def resume_host():
    command = ["python3", "-B", str(ROOT / "tools/diagnostics/r0f_group1_resume_validate.py"),
               "--source", str(SOURCE), "--baseline", str(BASELINE / "source-checkpoint"),
               "--out", str(OUT / RESUME_HOST)]
    builder.execute(command, RESUME_HOST + "-controller", source=ROOT, out=OUT)


def qualify():
    report = read(OUT / RESUME_HOST / "validation.json")
    if report["result"] != "PASS" or report["sourceSha256"] != sha(
            SOURCE / "src/diagnostics/r0f/successor_integration.c"):
        raise ValueError("resume ordering/fault gate missing or stale")
    controller().qualify("runtime-01", "host-01")


def run(mode, image_name):
    qualify_existing()
    runner.run(mode, source=SOURCE, out=OUT, image_name=image_name,
               run_identity="GROUP1_POST_STORAGE_CLOCK_RECOVERY",
               build_label="runtime-01", host_label="host-01")
    capacity = controller()
    capacity.prior.negative(mode, source=SOURCE, out=OUT)
    folder = OUT / (mode + "-01")
    capacity.capacity_check(folder / "trace.bin", folder / "capacity.json", "runtime-01")
    capacity.operator_check(folder)


def qualify_existing():
    preserve()
    runner.qualified(source=SOURCE, out=OUT, build_label="runtime-01", host_label="host-01")
    report = read(OUT / RESUME_HOST / "validation.json")
    if report["result"] != "PASS" or report["sourceSha256"] != sha(
            SOURCE / "src/diagnostics/r0f/successor_integration.c"):
        raise ValueError("resume host identity drift")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "build", "host", "resume-host", "qualify", "ntsc", "pal",
                                           "negative-export", "carrier-build", "carrier-boot", "carrier-finish"))
    parser.add_argument("--name")
    parser.add_argument("--experiment", type=Path, default=OUT)
    parser.add_argument("--image-name", default="G1RES02.D81")
    parser.add_argument("--mode", choices=("0", "1"))
    parser.add_argument("--number", type=int, choices=(1, 2))
    args = parser.parse_args()
    OUT = args.experiment.resolve()
    SOURCE = OUT / "source-inputs"
    action = args.action
    if action in ("ntsc", "pal"):
        run(action, args.image_name)
    elif action == "negative-export":
        qualify_existing()
        controller().negative_export()
    elif action.startswith("carrier-"):
        qualify_existing()
        if args.name is None:
            parser.error("carrier action requires an exact fresh name")
        carrier = carrier_controller()
        if action == "carrier-build":
            carrier.build(args.name)
            # Bind this adapter and its resume-specific gate to the existing
            # fail-closed controller pin checks before any exact-name boot.
            path = carrier.previous.carrier.location(args.name) / "capacity-admission.json"
            admission = read(path)
            for name in ("r0f_group1_resume_recovery.py", "r0f_group1_resume_validate.py",
                         "r0f_group1_resume_host_test.c", "r0f_group1_resume_clock.patch"):
                file = ROOT / "tools/diagnostics" / name
                admission["controllerInputs"][str(file.relative_to(ROOT))] = sha(file)
            admission["resumeHostSha256"] = sha(OUT / RESUME_HOST / "validation.json")
            write(path, admission)
        elif action == "carrier-finish":
            carrier.finish(args.name)
        else:
            if args.mode is None or args.number is None:
                parser.error("carrier boot requires mode and fresh-copy number")
            carrier.boot(args.name, args.mode, args.number)
    else:
        {"prepare": prepare, "build": build, "host": host,
         "resume-host": resume_host, "qualify": qualify}[action]()
