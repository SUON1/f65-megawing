#!/usr/bin/env python3
"""Freeze qualified display recovery and its local-only exact-name carrier."""
import shutil

import r0f_group1_owner_carrier as delivery

ROOT = delivery.ROOT
EXPERIMENT = ROOT / "build/r0f/group1/display-recovery/ram-crc-02"
NAME = "R0FG1P03.D81"


def main():
    source, metadata, _, _ = delivery.context(EXPERIMENT)
    output, _, gate = delivery.carrier.checked_gate(NAME)
    summary = delivery.candidate.read(output / "carrier-summary.json")
    if summary["D81_STATE"] != "XEMU_BOOT_VERIFIED" or summary["prgSha256"] != metadata["prgSha256"]:
        raise ValueError("four fresh exact-name carrier gates must pass")
    if (EXPERIMENT / "carrier-closeout.json").exists():
        raise ValueError("closeout already exists; never rewrite frozen results")
    runs = {}
    for run in ("ntsc-01", "ntsc-02", "pal-01", "pal-02"):
        report = delivery.candidate.read(output / run / "reduction.json")
        execution = delivery.candidate.read(output / run / "execution.json")
        negatives = delivery.candidate.read(output / run / "negatives.json")
        if (report["acquisition"] != "PASS" or report["nominalTiming"] != "WITHIN_OBSERVED_BOUNDS"
                or negatives["result"] != "PASS" or execution["status"] != 4 or execution["error"]):
            raise ValueError("carrier result drift: " + run)
        runs[run] = {
            "records": report["records"], "worldPairs": report["worldEventsRetained"],
            "executionCounts": report["instrumentedExecutionCounts"],
            "minimumCohortHz": min(cohort["nominalWorldHz"]
                for epoch in report["epochs"] for cohort in epoch["cohorts"]),
            "corruptionRejects": negatives["existingCases"] + negatives["poolCases"],
            "traceSha256": delivery.candidate.sha(output / run / "trace.bin")}
    delivery.candidate.closeout(source=source, out=EXPERIMENT)
    delivery.candidate.write(EXPERIMENT / "carrier-closeout.json", {
        "result": "PASS_FIT_HOST_FOCUSED_TIMING_FOUR_EXACT_NAME_BOOTS",
        "D81_STATE": summary["D81_STATE"], "D81_FILENAME": NAME,
        "D81_SHA256": gate["D81_SHA256"], "prgSha256": metadata["prgSha256"],
        "carrierInputsVerified": len(gate["inputs"]), "runs": runs,
        "canonicalMountedWritable": False, "SD": "NOT RUN", "physical": "NOT RUN",
        "commit": "NOT RUN", "push": "NOT RUN", "fullGroup1Acceptance": False,
        "remaining": ["Integrated near-capacity trace", "Compact operator summary",
                      "Physical SI/whole-ISR/real scanout and PCM boundaries", "Physical carrier/runtime gates"]})
    shutil.copytree(output, EXPERIMENT / "new-local-carrier",
                   ignore=shutil.ignore_patterns("disposable-sd.img", "__pycache__", "*.pyc"))
    checkpoint = EXPERIMENT / "delivery-controller"
    checkpoint.mkdir()
    for name, digest in gate["inputs"].items():
        path = ROOT / name
        if not path.is_relative_to(source):
            target = checkpoint / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
            if delivery.candidate.sha(target) != digest:
                raise ValueError("controller checkpoint drift: " + name)
    for name in ("tools/diagnostics/r0f_group1_display_closeout.py",
                 "docs/reports/R0-F_GROUP1_DISPLAY_THROUGHPUT_RECOVERY.md"):
        target = checkpoint / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    delivery.candidate.freeze(source=source, out=EXPERIMENT)
    delivery.carrier.checked_gate(NAME)
    print("Preserved predecessors, both timing trials and four local-only carrier boots")


if __name__ == "__main__":
    main()
