#!/usr/bin/env python3
"""Freeze qualified local capacity/summary evidence without SD or publication."""
import argparse
import shutil

import r0f_group1_capacity_summary as candidate
import r0f_group1_capacity_carrier as carrier

ROOT, OUT = candidate.ROOT, candidate.OUT
read, sha, write = candidate.read, candidate.sha, candidate.write


def audit():
    candidate.preserve()
    evidence = ROOT / "docs/evidence/r0f/group1"
    predecessor = evidence / "2026-09-30-display-recovery"
    names = [item["name"] for item in read(predecessor / "validation.json")["priorFrozenManifests"]]
    names.append(predecessor.name)
    verified = []
    for name in names:
        manifest = evidence / name / "sha256.json"
        entries = read(manifest)["files"]
        for file, digest in entries.items():
            if sha(evidence / name / file) != digest:
                raise ValueError("prior evidence drift: " + name + "/" + file)
        verified.append({"name": name, "entries": len(entries), "manifestSha256": sha(manifest)})
    if sum(item["entries"] for item in verified) != 5726:
        raise ValueError("unexpected preserved evidence inventory")
    inputs = []
    for name in ("build/r0f/group1/integration/build.json",
                 "build/r0f/group1/carriers/R0FG1P02/canonical/host-gate.json",
                 "build/r0f/group1/carriers/R0FG1P03/canonical/host-gate.json"):
        entries = read(ROOT / name)["inputs"]
        for file, digest in entries.items():
            if sha(ROOT / file) != digest:
                raise ValueError("passing root/carrier input drift: " + file)
        inputs.append({"metadata": name, "inputsVerified": len(entries)})
    baselines = read(evidence / "2026-09-30-crc-memory-experiment/validation.json")["before"]["baselines"]
    for name, digest in baselines.items():
        if sha(ROOT / name) != digest:
            raise ValueError("original PRG drift: " + name)
    return {"priorFrozenManifests": verified, "priorEntriesVerified": 5726,
            "passingInputsVerified": inputs, "originalBaselinePrgs": baselines}


def closeout():
    before = audit()
    fit = candidate.prior.qualified(source=candidate.SOURCE, out=OUT)
    name = "R0FG1P04.D81"
    carrier.finish(name)
    location, _, gate = carrier.checked(name)
    cases = {}
    for mode in ("ntsc", "pal"):
        folder = OUT / (mode + "-01")
        carrier.require_case(folder)
        carrier.require_screen(folder)
        cases[mode] = {key: read(folder / (key + ".json")) for key in
                      ("execution", "reduction", "negatives", "capacity", "operator-summary", "operator-screen-review")}
    trials = []
    for experiment in (OUT.with_name("integrated-01"), OUT):
        for path in sorted(experiment.glob("*/build.json")):
            data = read(path)
            if sha(path.parent / "GROUP1.prg") != data["prgSha256"]:
                raise ValueError("compile trial PRG drift")
            for file, digest in data["inputs"].items():
                if sha(path.parent / "source-checkpoint" / file) != digest:
                    raise ValueError("compile trial source drift")
            trials.append({"experiment": experiment.name, "label": path.parent.name,
                           "prgSha256": data["prgSha256"], "freeBytes": data["residentFreeBytes"],
                           "inputsVerified": len(data["inputs"])})
    write(OUT / "closeout.json", {
        "result": "PASS_LOCAL_INTEGRATED_CAPACITY_OPERATOR_SUMMARY", "build": fit,
        "focusedRuns": cases, "compileCheckpoints": trials,
        "host": read(OUT / read(OUT / "qualification.json")["host_label"] / "validation.json"),
        "expectedExportFailure": read(OUT / "export-failure-01/validation.json"),
        "carrier": {"name": name, "sha256": gate["D81_SHA256"], "state": "XEMU_BOOT_VERIFIED",
                    "inputs": len(gate["inputs"]), "controllerInputs": 5,
                    "fourBoots": [read(location / run / "validation.json") for run in
                                  ("ntsc-01", "ntsc-02", "pal-01", "pal-02")]},
        "preservation": before, "rootTests": 47,
        "boundary": "Full existing allocation export with separately checked non-timing tail; no invented tick/world/pool observations.",
        "SD": "NOT RUN", "physical": "NOT RUN", "commit": "NOT RUN", "push": "NOT RUN",
        "fullGroup1Acceptance": False})
    print("Qualified local slice and all four clean carrier gates PASS")


def freeze():
    close = read(OUT / "closeout.json")
    current = candidate.prior.qualified(source=candidate.SOURCE, out=OUT)
    if close["build"] != current:
        raise ValueError("closeout/source drift")
    before = audit()
    carrier.checked("R0FG1P04.D81")
    candidate.builder.execute(["git", "diff", "--check"], "final-diff-check", source=ROOT, out=OUT)
    destination = ROOT / "docs/evidence/r0f/group1/2026-10-01-capacity-summary"
    destination.mkdir(exist_ok=False)
    ignored = shutil.ignore_patterns("disposable-sd.img", "__pycache__", "*.pyc")
    shutil.copytree(OUT, destination / "experiment", ignore=ignored)
    shutil.copytree(OUT.with_name("integrated-01"), destination / "earlier-trials", ignore=ignored)
    shutil.copytree(ROOT / "build/r0f/group1/carriers/R0FG1P04",
                    destination / "carrier", ignore=ignored)
    for name in ("AGENTS.md", "CURRENT_STATE.md", "WORK_IN_PROGRESS.md",
                 "docs/DEVELOPMENT_WORKFLOW.md", "docs/PROGRAMMING_PRINCIPLES.md", "docs/CODE_STYLE_C.md",
                 "00_D81_LOADABILITY_GATE.md", "docs/D81_WORKFLOW.md",
                 "docs/plans/R0-F_GROUP1_BUILD_INTENT.md", "docs/plans/R0-F_GROUP1_EXPORT_AMENDMENT.md",
                 "docs/plans/R0-F_GROUP1_MEASUREMENT_MATRIX.md", "docs/reports/R0-F_GROUP1_CAPACITY_SUMMARY.md",
                 "tools/diagnostics/r0f_group1_capacity_summary.py",
                 "tools/diagnostics/r0f_group1_capacity_carrier.py",
                 "tools/diagnostics/r0f_group1_capacity_closeout.py",
                 "tools/diagnostics/r0f_group1_owner_integration.py",
                 "tools/diagnostics/test_r0f_group1_capacity_carrier.py",
                 "tools/diagnostics/test_r0f_group1_capacity_summary.py"):
        target = destination / "checkpoint" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    write(destination / "validation.json", {
        "result": close["result"], **before,
        "prgSha256": current["prgSha256"], "residentFreeBytes": current["residentFreeBytes"],
        "carrierState": "XEMU_BOOT_VERIFIED", "carrierSha256": close["carrier"]["sha256"],
        "excluded": "Disposable multi-gigabyte SD fixtures only; retained source/PRG/D81, memory, actual export, logs, screenshots and checks included.",
        "SD": "NOT RUN", "physical": "NOT RUN", "fullGroup1Acceptance": False})
    files = {str(path.relative_to(destination)): sha(path)
             for path in sorted(destination.rglob("*")) if path.is_file()}
    write(destination / "sha256.json", {"algorithm": "sha256", "files": files})
    for name, digest in files.items():
        if sha(destination / name) != digest:
            raise ValueError("new freeze drift: " + name)
    audit()
    carrier.checked("R0FG1P04.D81")
    print({"frozenEntries": len(files), "manifestSha256": sha(destination / "sha256.json"),
           "priorEntriesVerified": 5726})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("closeout", "freeze"))
    args = parser.parse_args()
    (closeout if args.action == "closeout" else freeze)()
