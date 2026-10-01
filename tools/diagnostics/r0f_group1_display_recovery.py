#!/usr/bin/env python3
"""Isolated complete-frame throughput correction; unchanged workload and gates."""
import argparse
import shutil

import r0f_group1_owner_recovery as previous

ROOT = previous.ROOT
OUT = ROOT / "build/r0f/group1/display-recovery/completion-01"
SOURCE = OUT / "source-inputs"
read, sha, write = previous.read, previous.sha, previous.write


def preserve():
    prior = previous.qualified()
    evidence = ROOT / "docs/evidence/r0f/group1/2026-09-30-owner-recovery"
    for name, digest in read(evidence / "sha256.json")["files"].items():
        if sha(evidence / name) != digest:
            raise ValueError("owner recovery evidence drift: " + name)
    return prior


def prepare(*, source=SOURCE, out=OUT, predecessor=None):
    prior = preserve()
    predecessor_source = previous.SOURCE
    if predecessor is not None:
        predecessor_source = predecessor / "source-inputs"
        prior = previous.qualified(source=predecessor_source, out=predecessor,
                                   **read(predecessor / "qualification.json"))
    out.mkdir(parents=True, exist_ok=False)
    shutil.copytree(predecessor_source, source)
    write(out / "preparation.json", {"predecessor": prior,
                                    "predecessorExperiment": str(predecessor) if predecessor else None})
    print("Prepared exclusive display correction from preserved owner candidate")


def build(label, *, source=SOURCE, out=OUT):
    preserve()
    prior = read(out / "preparation.json")["predecessor"]
    previous.previous.build(label, source=source, out=out, predecessor=prior)
    shutil.copytree(source, out / label / "source-checkpoint")


def host(label, *, source=SOURCE, out=OUT):
    preserve()
    previous.host(label, source=source, out=out,
                  reference_display=previous.SOURCE / "src/diagnostics/r0f/successor_integration.c")


def qualified(*, source=SOURCE, out=OUT):
    preserve()
    labels = read(out / "qualification.json")
    return previous.qualified(source=source, out=out, **labels)


def qualify(build_label, host_label, *, source=SOURCE, out=OUT):
    labels = {"build_label": build_label, "host_label": host_label}
    fit = previous.qualified(source=source, out=out, **labels)
    write(out / "qualification.json", labels)
    print({"qualifiedPrg": fit["prgSha256"], "freeBytes": fit["residentFreeBytes"]})


def run(mode, *, source=SOURCE, out=OUT):
    qualified(source=source, out=out)
    image_name = "G1DSP01.D81" if out.name == "completion-01" else "G1DSP02.D81"
    previous.run(mode, source=source, out=out, image_name=image_name,
                 run_identity="GROUP1_DISPLAY_COMPLETION_DEVELOPMENT",
                 **read(out / "qualification.json"))


def negative(mode, *, source=SOURCE, out=OUT):
    qualified(source=source, out=out)
    output = out / (mode + "-01")
    previous.previous.execute([
        "python3", "-B", "tools/diagnostics/r0f_group1_pool_trace_negative.py",
        "--source", source, "--trace", output / "trace.bin",
        "--out", output / "negatives.json"], mode + "-negative-controller",
        source=ROOT, out=out)
    print(mode.upper() + " actual-trace corruption rejection PASS")


def closeout(*, source=SOURCE, out=OUT):
    fit = qualified(source=source, out=out)
    runs = {}
    for mode in ("ntsc", "pal"):
        folder = out / (mode + "-01")
        if folder.exists():
            runs[mode] = {name: read(folder / (name + ".json"))
                          for name in ("execution", "reduction", "negatives")
                          if (folder / (name + ".json")).exists()}
    passed = len(runs) == 2 and all(
        run.get("reduction", {}).get("acquisition") == "PASS"
        and run["reduction"]["nominalTiming"] == "WITHIN_OBSERVED_BOUNDS"
        and run.get("negatives", {}).get("result") == "PASS"
        for run in runs.values())
    failed = any(run.get("reduction", {}).get("nominalTiming") == "FAIL"
                 for run in runs.values())
    write(out / "closeout.json", {
        "result": "PASS_FIT_HOST_FOCUSED_NTSC_PAL" if passed else
                  "FIT_HOST_PASS_NTSC_TIMING_FAILED" if failed else "GATES_INCOMPLETE",
        "build": fit,
        "host": read(out / read(out / "qualification.json")["host_label"] / "validation.json"),
        "runs": runs,
        "correction": ["Finish after final successful scene copy, with snapshot CRC and registration checks retained.",
                       "Choose the next backbuffer after any swap, never clear the just-published front store.",
                       "RAM CRC calls use the existing qualified compact algorithm." if out.name == "ram-crc-02"
                       else "Completion correction alone did not close the resumed 20 Hz floor."],
        "unchanged": ["scene encoding and nine copies", "15 bounded 4096-byte clears",
                      "view cancellation policy", "frame-boundary publication", "all capacities and integrity checks",
                      "generated contracts", "resident/physical memory envelopes", "100 Hz and 21-stage order"],
        "SD": "NOT RUN", "physical": "NOT RUN", "commit": "NOT RUN", "push": "NOT RUN",
        "fullGroup1Acceptance": False})
    print("Retained display correction and measured gates")


def freeze(*, source=SOURCE, out=OUT):
    qualified(source=source, out=out)
    evidence = ROOT / "docs/evidence/r0f/group1"
    prior = evidence / "2026-09-30-owner-recovery"
    names = [item["name"] for item in read(prior / "validation.json")["priorFrozenManifests"]]
    names.append(prior.name)
    verified = []
    for name in names:
        entries = read(evidence / name / "sha256.json")["files"]
        for file, digest in entries.items():
            if sha(evidence / name / file) != digest:
                raise ValueError("frozen evidence drift: " + name + "/" + file)
        verified.append({"name": name, "entries": len(entries),
                         "manifestSha256": sha(evidence / name / "sha256.json")})
    if sum(item["entries"] for item in verified) != 4498:
        raise ValueError("prior inventory changed")
    for metadata in ("build/r0f/group1/integration/build.json",
                     "build/r0f/group1/carriers/R0FG1P02/canonical/host-gate.json"):
        for file, digest in read(ROOT / metadata)["inputs"].items():
            if sha(ROOT / file) != digest:
                raise ValueError("passing source input drift: " + file)
    previous.previous.execute(["python3", "-B", "-m", "unittest", "discover",
        "-s", "tools/diagnostics", "-p", "test_r0f_group1_*.py", "-v"],
        "root-suite", source=ROOT, out=out)
    previous.previous.execute(["git", "diff", "--check"], "diff-check", source=ROOT, out=out)
    destination = evidence / "2026-09-30-display-recovery"
    destination.mkdir(exist_ok=False)
    shutil.copytree(out, destination / "experiment",
                   ignore=shutil.ignore_patterns("disposable-sd.img", "__pycache__", "*.pyc"))
    predecessor = read(out / "preparation.json").get("predecessorExperiment")
    if predecessor:
        shutil.copytree(predecessor, destination / "earlier-trial",
                       ignore=shutil.ignore_patterns("disposable-sd.img", "__pycache__", "*.pyc"))
    for name in ("AGENTS.md", "CURRENT_STATE.md", "WORK_IN_PROGRESS.md",
                 "docs/plans/R0-F_GROUP1_BUILD_INTENT.md", "docs/DEVELOPMENT_WORKFLOW.md",
                 "docs/PROGRAMMING_PRINCIPLES.md", "docs/CODE_STYLE_C.md",
                 "00_D81_LOADABILITY_GATE.md", "docs/D81_WORKFLOW.md",
                 "tools/diagnostics/r0f_group1_owner_recovery.py",
                 "tools/diagnostics/r0f_group1_display_recovery.py"):
        target = destination / "checkpoint" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    write(destination / "validation.json", {
        "result": read(out / "closeout.json")["result"],
        "priorFrozenManifests": verified, "priorEntriesVerified": 4498,
        "rootInputsVerified": 93, "carrierInputsVerified": 95,
        "SD": "NOT RUN", "physical": "NOT RUN"})
    files = {str(path.relative_to(destination)): sha(path)
             for path in sorted(destination.rglob("*")) if path.is_file()}
    write(destination / "sha256.json", {"algorithm": "sha256", "files": files})
    for name, digest in files.items():
        if sha(destination / name) != digest:
            raise ValueError("freeze copy mismatch: " + name)
    preserve()
    print({"frozenFiles": len(files), "priorEntriesVerified": 4498,
           "manifestSha256": sha(destination / "sha256.json")})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "build", "host", "qualify", "ntsc", "pal",
                                           "negative-ntsc", "negative-pal", "closeout", "freeze"))
    parser.add_argument("--label", default="runtime-02")
    parser.add_argument("--build-label", default="runtime-02")
    parser.add_argument("--host-label", default="host-02")
    parser.add_argument("--variant", choices=("completion-01", "ram-crc-02"), default="completion-01")
    parser.add_argument("--predecessor", type=type(OUT))
    args = parser.parse_args()
    action = args.action
    output = OUT.parent / args.variant
    context = {"out": output, "source": output / "source-inputs"}
    if action in ("ntsc", "pal"):
        run(action, **context)
    elif action.startswith("negative-"):
        negative(action.removeprefix("negative-"), **context)
    elif action in ("build", "host"):
        {"build": build, "host": host}[action](args.label, **context)
    elif action == "qualify":
        qualify(args.build_label, args.host_label, **context)
    elif action == "prepare":
        prepare(predecessor=args.predecessor, **context)
    else:
        {"closeout": closeout, "freeze": freeze}[action](**context)
