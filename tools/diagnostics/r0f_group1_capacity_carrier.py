#!/usr/bin/env python3
"""Version-7 capacity/summary admission around the preserved carrier workflow.

Before any D81 action read 00_D81_LOADABILITY_GATE.md and docs/D81_WORKFLOW.md.
Fresh uppercase exact-name construction; never mount canonical writable.
Local host/Xemu tiers only. No SD write or physical-test eligibility.
"""
import argparse
from pathlib import Path

import r0f_group1_owner_carrier as previous
import r0f_group1_capacity_summary as candidate

ROOT = candidate.ROOT
read, sha, write = candidate.read, candidate.sha, candidate.write


def require_case(folder):
    capacity = read(folder / "capacity.json")
    operator = read(folder / "operator-summary.json")
    reduction = read(folder / "reduction.json")
    if (capacity["result"] != "PASS"
            or capacity["scope"] != "ACTUAL_EXPORTED_VERSION_7"
            or len(capacity["capacityRejections"]) != 12
            or capacity["capacity"] != reduction["capacityCase"]
            or reduction["capacityCase"]["result"] != "PASS"
            or reduction["capacityCase"]["allocationBytes"] != 327680
            or not reduction["capacityCase"]["outsideAcquisitionTiming"]
            or operator["result"] != "PASS_PROTECTED_TEXT"
            or operator["status"] != 4 or operator["error"] or operator["files"] != 20):
        raise ValueError("full-capacity actual export/operator admission failed")


def build(name):
    candidate.preserve()
    for mode in ("ntsc", "pal"):
        require_case(candidate.OUT / (mode + "-01"))
        require_screen(candidate.OUT / (mode + "-01"))
    failed = candidate.OUT / "export-failure-01"
    rejection = read(failed / "validation.json")
    operator = read(failed / "operator-summary.json")
    labels = read(candidate.OUT / "qualification.json")
    fit = read(candidate.OUT / labels["build_label"] / "build.json")
    if (rejection["result"] != "PASS_EXPECTED_EXPORT_FAILURE"
            or rejection["prgSha256"] != fit["prgSha256"]
            or not rejection["preExistingFilesUnchanged"]
            or rejection["actualReturningSave"] != "PASS"
            or operator["status"] != 5 or operator["error"] != 3 or operator["files"] != 0):
        raise ValueError("exact-PRG failed-export/no-overwrite gate missing")
    require_screen(failed)
    previous.build(name, candidate.OUT)
    output = previous.carrier.location(name)
    inputs = {str(path.relative_to(ROOT)): sha(path) for path in (
        Path(__file__), ROOT / "tools/diagnostics/r0f_group1_capacity_summary.py",
        ROOT / "tools/diagnostics/r0f_group1_owner_integration.py",
        ROOT / "tools/diagnostics/test_r0f_group1_capacity_carrier.py",
        ROOT / "tools/diagnostics/test_r0f_group1_capacity_summary.py")}
    write(output / "capacity-admission.json", {
        "result": "PASS", "controllerInputs": inputs,
        "prgSha256": read(output / "canonical/host-gate.json")["build"]["prgSha256"],
        "traceVersion": 7, "allocationBytes": 327680, "chunks": 20,
        "tail": "Non-timing pattern after real events; not fabricated workload",
        "sd": "NOT RUN", "physical": "NOT RUN", "testEligible": False})


def checked(name):
    candidate.preserve()
    output, canonical, gate = previous.carrier.checked_gate(name)
    admission = read(output / "capacity-admission.json")
    if admission["result"] != "PASS" or admission["prgSha256"] != gate["build"]["prgSha256"]:
        raise ValueError("capacity/carrier identity drift")
    for path, digest in admission["controllerInputs"].items():
        if sha(ROOT / path) != digest:
            raise ValueError("capacity controller input drift: " + path)
    return output, canonical, gate


def boot(name, mode, number):
    output, _, gate = checked(name)
    run = ("ntsc" if mode == "1" else "pal") + f"-{number:02d}"
    directory = output / run
    try:
        previous.boot(name, mode, number)
        labels = read(candidate.OUT / "qualification.json")
        candidate.capacity_check(directory / "trace.bin", directory / "capacity.json", labels["build_label"])
        candidate.operator_check(directory)
        require_case(directory)
        checked(name)
    except (Exception, SystemExit) as error:
        if not (output / "retirement.json").exists():
            write(output / "retirement.json", {
                "D81_FILENAME": name, "canonicalSha256": gate["D81_SHA256"],
                "failedRun": run, "failure": str(error),
                "state": "RETIRED_AFTER_LOCAL_GATE_FAILURE", "sd": "NOT RUN",
                "physical": "NOT RUN", "testEligible": False})
        raise


def finish(name):
    output, _, _ = checked(name)
    for mode in ("ntsc", "pal"):
        for number in (1, 2):
            directory = output / f"{mode}-{number:02d}"
            require_case(directory)
            require_screen(directory)
    previous.carrier.finish(name)


def require_screen(directory):
    review = read(directory / "operator-screen-review.json")
    if review["result"] != "PASS" or review["screenSha256"] != sha(directory / "screen.png"):
        raise ValueError("actual operator screen review missing/drifted")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("build", "boot", "finish"))
    parser.add_argument("--name", required=True)
    parser.add_argument("--mode", choices=("0", "1"))
    parser.add_argument("--number", type=int, choices=(1, 2))
    args = parser.parse_args()
    if args.action == "build":
        build(args.name)
    elif args.action == "boot":
        if args.mode is None or args.number is None:
            parser.error("boot requires video mode and fresh copy number")
        boot(args.name, args.mode, args.number)
    else:
        finish(args.name)
