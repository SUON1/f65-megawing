#!/usr/bin/env python3
"""Bounded arithmetic/shared-encoding recovery, no capacity or integrity change."""
import argparse
import importlib.util
import shutil
import subprocess

import r0f_group1_owner_integration as previous
import r0f_group1_export_probe as probe

ROOT = previous.ROOT
OUT = ROOT / "build/r0f/group1/pool-recovery/arithmetic-codec-01"
SOURCE = OUT / "source-inputs"
read, sha, write = previous.read, previous.sha, previous.write


def preserve():
    previous.preserve()
    freeze = ROOT / "docs/evidence/r0f/group1/2026-09-30-owner-integration"
    for name, digest in read(freeze / "sha256.json")["files"].items():
        if sha(freeze / name) != digest:
            raise ValueError("owner evidence drift: " + name)
    prior = read(previous.OUT / "runtime-checked/build.json")
    if sha(previous.OUT / "runtime-checked/GROUP1.prg") != prior["prgSha256"]:
        raise ValueError("original owner candidate drift")
    if previous.inputs() != prior["inputs"]:
        raise ValueError("original owner source drift")
    return prior


def prepare():
    prior = preserve()
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copytree(previous.SOURCE, SOURCE)
    write(OUT / "preparation.json", {"predecessor": prior})
    print("Prepared exclusive arithmetic/codec recovery snapshot")


def build(label):
    previous.build(label, source=SOURCE, out=OUT, predecessor=preserve())
    shutil.copytree(SOURCE, OUT / label / "source-checkpoint")


def host(label, *, source=SOURCE, out=OUT, reference_display=None):
    preserve()
    command = ["python3", "-B", "tools/diagnostics/r0f_group1_owners_validate.py",
               str(out / label), "--reference-pool",
               str(previous.SOURCE / "src/diagnostics/r0f/group1_pool.c")]
    if reference_display is not None:
        command += ["--reference-display", str(reference_display)]
    result = subprocess.run(command, cwd=source, text=True, capture_output=True, timeout=60)
    with (out / (label + "-controller.txt")).open("x") as stream:
        stream.write(result.stdout + result.stderr)
    result.check_returncode()
    write(out / (label + "-command.json"), {"command": command, "cwd": str(source),
                                           "exitCode": result.returncode})
    print(result.stdout.strip())
    preserve()


def qualified(*, source=SOURCE, out=OUT, build_label="runtime-final", host_label="host-final"):
    preserve()
    current = previous.inputs(source)
    fit = read(out / build_label / "build.json")
    host_result = read(out / host_label / "validation.json")
    if (fit["fit"] != "PASS" or fit["residentFreeBytes"] < 0
            or host_result["result"] != "PASS"
            or fit["inputs"] != current or host_result["inputs"] != current
            or sha(out / build_label / "GROUP1.prg") != fit["prgSha256"]):
        raise ValueError("complete fit, host and exact-input gates must pass")
    return fit


def run(mode, *, source=SOURCE, out=OUT, image_name="G1OWN01.D81",
        run_identity="GROUP1_OWNER_RECOVERY_DEVELOPMENT",
        build_label="runtime-final", host_label="host-final"):
    # Development-only, fresh single-session fixture; never a released carrier.
    # 00_D81_LOADABILITY_GATE.md and docs/D81_WORKFLOW.md govern this operation.
    fit = qualified(source=source, out=out, build_label=build_label, host_label=host_label)
    if mode == "pal":
        ntsc = read(out / "ntsc-01/reduction.json")
        execution = read(out / "ntsc-01/execution.json")
        previous.previous.previous.require_ntsc_gate(ntsc, execution)
    output = out / (mode + "-01")
    output.mkdir(exist_ok=False)
    write(output / "build-identity.json", fit)
    frozen_prg = output / "GROUP1.prg"
    shutil.copyfile(out / build_label / "GROUP1.prg", frozen_prg)
    if sha(frozen_prg) != fit["prgSha256"]:
        raise ValueError("run PRG copy mismatch")
    probe.emulator.PRG = frozen_prg
    probe.emulator.SOURCE_BRANCH = probe.emulator.git_text("branch", "--show-current")
    image = output / image_name
    probe.emulator.fresh_d81(output, image, "G1 TIMING DEV", {
        "token": ROOT / "docs/evidence/r0f/successor/2026-09-21/TOKEN.prg"})
    _, execution = probe.emulator.run_xemu(output, "1" if mode == "ntsc" else "0",
        image, run_identity, False, 120)
    spec = importlib.util.spec_from_file_location("owner_trace_extraction",
        source / "tools/diagnostics/r0f_group1_run.py")
    acquisition = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(acquisition)
    # Explicit codec injection keeps root version-5 inputs immutable; the
    # independent version-6 reducer runs in its own snapshot import context.
    def reduce_trace(trace, saved, payload):
        if (output / "trace.bin").read_bytes() != trace or (output / "saved.prg").read_bytes() != saved:
            raise ValueError("extracted trace/SAVE identity mismatch")
        command = ["python3", "-B", str(source / "tools/diagnostics/r0f_group1_reduce.py"),
                   str(output / "trace.bin"), "--saved", str(output / "saved.prg"),
                   "--payload-address", hex(payload), "--out", str(output / "independent-reduction.json")]
        result = subprocess.run(command, cwd=source, text=True, capture_output=True, timeout=60)
        write(output / "reducer-command.json", {"command": command, "exitCode": result.returncode,
                                                "stdout": result.stdout, "stderr": result.stderr})
        result.check_returncode()
        return read(output / "independent-reduction.json")
    wire = read(source / "interfaces/r0f_group1_trace_contract.json")["constants"]
    report, _ = acquisition.reduce_export(output, image,
        (out / (build_label + "-symbols.txt")).read_text(), execution,
        wire=wire, reduce_trace=reduce_trace)
    if report["acquisition"] != "PASS" or report["nominalTiming"] != "WITHIN_OBSERVED_BOUNDS":
        raise ValueError("fresh timing gate failed")
    if mode == "ntsc":
        previous.previous.previous.require_ntsc_gate(report, read(output / "execution.json"))
    qualified(source=source, out=out, build_label=build_label, host_label=host_label)
    print(mode.upper() + " complete acquisition, actual SAVE/export and nominal timing PASS")


def closeout():
    fit = qualified()
    prior = preserve()
    runs = {}
    for mode in ("ntsc", "pal"):
        folder = OUT / (mode + "-01")
        if folder.exists():
            runs[mode] = {name: read(folder / (name + ".json"))
                          for name in ("execution", "reduction", "negatives")
                          if (folder / (name + ".json")).exists()}
    complete = len(runs) == 2 and all(
        run.get("reduction", {}).get("acquisition") == "PASS"
        and run["reduction"]["nominalTiming"] == "WITHIN_OBSERVED_BOUNDS"
        and run.get("negatives", {}).get("result") == "PASS"
        for run in runs.values())
    trials = []
    for number in range(1, 14):
        label = f"runtime-{number:02}"
        report = read(OUT / label / "build.json")
        for name, digest in report["inputs"].items():
            if sha(OUT / label / "source-checkpoint" / name) != digest:
                raise ValueError("trial checkpoint drift: " + label + "/" + name)
        trials.append({"label": label, "freeBytes": report["residentFreeBytes"],
                       "prgSha256": report["prgSha256"], "executed": False})
    timing_failed = any(run.get("reduction", {}).get("nominalTiming") == "FAIL"
                        for run in runs.values())
    report = {
        "result": "PASS_FIT_HOST_FOCUSED_NTSC_PAL" if complete else
                  "FIT_HOST_PASS_NTSC_TIMING_FAILED" if timing_failed else
                  "FIT_HOST_PASS_XEMU_GATE_INCOMPLETE",
        "build": fit, "runs": runs, "staticTrials": trials,
        "recoveredResidentBytes": prior["residentEndExclusive"] - fit["residentEndExclusive"],
        "sectionChanges": {name: fit["sections"][name]["bytes"] - prior["sections"][name]["bytes"]
                           for name in (".r0fs_protected", ".text", ".rodata", ".data", ".bss", ".noinit")},
        "host": read(OUT / "host-final/validation.json"),
        "retainedChanges": [
            "Wide geometry remainder replaced by reduce-before-add bounded u16 arithmetic; same demands/data for all u16 generation values.",
            "Sequential CRC region traversal reuses one region accumulator; record region uses whole-record units, others bounded u16 byte counts, all trace addresses remain u32.",
            "Pool invariant factored into equivalent full/non-full branches; pinned LTO specialization preserves source rejection rules.",
            "Checkpoint encoding retains its own function boundary outside the captured tick."],
        "unchanged": ["all generated contracts and layouts", "all pool capacities",
                      "all backing buffers and observer state", "three acquisition/readback CRC comparisons",
                      "whole-trace CRC and export residue", "protected resident region", "memory envelope",
                      "MAP/base-page and IRQ/NMI implementation", "100 Hz/21-stage/deadline requirements"],
        "trialBoundary": "13 compile-only source checkpoints plus the exact final build; only the final qualified identity is executed. Larger/rejected trials retained.",
        "newCarrier": "NOT BUILT", "SD": "NOT RUN", "physical": "NOT RUN",
        "commit": "NOT RUN", "push": "NOT RUN", "fullGroup1Acceptance": False,
        "limitation": "66 resident bytes free; emulator counters are not physical SI/whole-ISR or hardware proof."}
    if timing_failed:
        run = runs["ntsc"]["reduction"]
        wire = read(SOURCE / "interfaces/r0f_group1_trace_contract.json")
        constants, header, record, world = (wire[name] for name in
            ("constants", "headerOffsets", "recordOffsets", "worldOffsets"))
        data = (OUT / "ntsc-01/trace.bin").read_bytes()
        def value(offset, width=4):
            return int.from_bytes(data[offset:offset + width], "little")
        start = constants["HEADER_BYTES"] + 1600 * constants["RECORD_BYTES"]
        first_release = value(start + record["RELEASE"])
        period = value(header["PERIOD_Q16"]) / 65536
        events_start = constants["HEADER_BYTES"] + 3200 * constants["RECORD_BYTES"] + constants["RESULT_BYTES"] + constants["EPOCHS"] * constants["POOL_EPOCH_BYTES"]
        events = []
        for index in range(run["worldEventsRetained"]):
            base = events_start + index * constants["WORLD_EVENT_BYTES"]
            if value(base + world["EPOCH"], 1) == 1 and value(base + world["PHASE"], 1) == 0:
                events.append({
                    "generation": index + 1, "sourceTick": value(base + world["SOURCE_TICK"], 2),
                    "requestTick": value(base + world["REQUEST_TICK"], 2),
                    "view": value(base + world["KEY_FLAGS"], 1) & 1,
                    "swapAfterReleaseTicks": ((value(base + world["SWAP_TIME"]) - first_release) & 0xffffffff) / period})
        report["failingCohort"] = run["epochs"][1]["cohorts"][0]
        report["resumedPhaseZeroEvents"] = events
        report["diagnosis"] = (
            "First resumed world arrives after 2.95 tick periods; subsequent swaps are about five "
            "tick periods apart. A request change at tick 1664 lies in the near-ten-period gap "
            "between generations 468 and 469. Source ticks jump 1653 to 1663, matching the "
            "existing busy-at-view-change cancellation path. This supports a cadence/cancellation "
            "headroom failure, not a stalled acquisition or late first resumed world. No per-quantum "
            "target instrumentation was added; the precise instruction/frame-edge mechanism remains open.")
        report["nextAction"] = (
            "Narrow display-throughput correction around the view-change cancellation under the same "
            "workload/capacities. Preserve this failed trace; repeat full fit/host then fresh NTSC. "
            "Do not add a grace period, drop the resumed cohort, relax 20 Hz or run PAL yet.")
    write(OUT / "closeout.json", report)
    print(report["result"])


def freeze():
    qualified()
    report = read(OUT / "closeout.json")
    evidence = ROOT / "docs/evidence/r0f/group1"
    owner = evidence / "2026-09-30-owner-integration"
    names = [item["name"] for item in read(owner / "validation.json")["priorFrozenManifests"]]
    names.append(owner.name)
    verified = []
    for name in names:
        entries = read(evidence / name / "sha256.json")["files"]
        for file, digest in entries.items():
            if sha(evidence / name / file) != digest:
                raise ValueError("older frozen evidence drift: " + name + "/" + file)
        verified.append({"name": name, "entries": len(entries),
                         "manifestSha256": sha(evidence / name / "sha256.json")})
    if sum(item["entries"] for item in verified) != 2429:
        raise ValueError("older evidence inventory changed")
    for metadata in ("build/r0f/group1/integration/build.json",
                     "build/r0f/group1/carriers/R0FG1P02/canonical/host-gate.json"):
        for file, digest in read(ROOT / metadata)["inputs"].items():
            if sha(ROOT / file) != digest:
                raise ValueError("passing root/carrier input drift: " + file)
    previous.execute(["python3", "-B", "-m", "unittest", "discover",
                      "-s", "tools/diagnostics", "-p", "test_r0f_group1_*.py", "-v"],
                     "root-suite", source=ROOT, out=OUT)
    previous.execute(["git", "diff", "--check"], "diff-check", source=ROOT, out=OUT)
    destination = evidence / "2026-09-30-owner-recovery"
    destination.mkdir(exist_ok=False)
    shutil.copytree(OUT, destination / "experiment",
        ignore=shutil.ignore_patterns("disposable-sd.img", "__pycache__", "*.pyc"))
    for name in ("AGENTS.md", "CURRENT_STATE.md", "WORK_IN_PROGRESS.md",
                 "docs/plans/R0-F_GROUP1_BUILD_INTENT.md", "docs/DEVELOPMENT_WORKFLOW.md",
                 "docs/PROGRAMMING_PRINCIPLES.md", "docs/CODE_STYLE_C.md",
                 "00_D81_LOADABILITY_GATE.md", "docs/D81_WORKFLOW.md",
                 "tools/diagnostics/r0f_group1_owner_integration.py",
                 "tools/diagnostics/r0f_group1_owner_recovery.py",
                 "tools/diagnostics/r0f_group1_pool_trace_negative.py"):
        target = destination / "checkpoint" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    write(destination / "validation.json", {
        "result": report["result"], "priorFrozenManifests": verified,
        "priorEntriesVerified": 2429, "rootBuildInputsVerified": 93, "carrierInputsVerified": 95,
        "prgSha256": report["build"]["prgSha256"],
        "excluded": "Disposable multi-gigabyte emulator images remain in build; execution reports retain hashes.",
        "SD": "NOT RUN", "physical": "NOT RUN", "carrier": "NOT BUILT"})
    files = {str(path.relative_to(destination)): sha(path)
             for path in sorted(destination.rglob("*")) if path.is_file()}
    write(destination / "sha256.json", {"algorithm": "sha256", "files": files})
    for name, digest in files.items():
        if sha(destination / name) != digest:
            raise ValueError("new evidence copy mismatch: " + name)
    preserve()
    print({"frozenFiles": len(files), "priorEntriesVerified": 2429,
           "manifestSha256": sha(destination / "sha256.json")})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "build", "host", "ntsc", "pal", "closeout", "freeze"))
    parser.add_argument("--label", default="runtime-01")
    args = parser.parse_args()
    if args.action == "prepare":
        prepare()
    elif args.action == "build":
        build(args.label)
    elif args.action == "host":
        host(args.label)
    elif args.action in ("ntsc", "pal"):
        run(args.action)
    else:
        {"closeout": closeout, "freeze": freeze}[args.action]()
