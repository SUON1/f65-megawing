#!/usr/bin/env python3
"""Isolated actual-owner candidate. No execution path until full fit qualifies."""
import argparse
import shutil
import subprocess
from pathlib import Path

import r0f_group1_foreground_experiment as previous

ROOT = previous.ROOT
OUT = ROOT / "build/r0f/group1/pool-integration/owner-01"
SOURCE = OUT / "source-inputs"
read, sha, write = previous.read, previous.sha, previous.write
MODULES = ("src/diagnostics/r0f/group1_pool.c",
           "src/diagnostics/r0f/group1_pool_owners.c",
           "src/diagnostics/r0f/group1_geometry_fixture.c")


def preserve():
    previous.checked()
    fit = read(previous.OUT / "fit.json")["runtime"]
    if sha(previous.OUT / "runtime/GROUP1.prg") != fit["prgSha256"]:
        raise ValueError("qualified foreground PRG drift")
    previous.previous.require_ntsc_gate(
        read(previous.OUT / "ntsc-01/reduction.json"),
        read(previous.OUT / "ntsc-01/execution.json"))
    freeze = ROOT / "docs/evidence/r0f/group1/2026-09-30-foreground-memory-experiment"
    for name, digest in read(freeze / "sha256.json")["files"].items():
        if sha(freeze / name) != digest:
            raise ValueError("foreground evidence drift: " + name)
    return fit


def inputs(source=SOURCE):
    return {str(path.relative_to(source)): sha(path)
            for path in sorted(source.rglob("*"))
            if path.is_file() and "__pycache__" not in path.parts}


def prepare():
    prior = preserve()
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copytree(previous.SOURCE, SOURCE)
    write(OUT / "preparation.json", {"predecessor": prior, "inputs": inputs()})
    print("Prepared exclusive actual-owner source snapshot")


def execute(command, label, *, source=SOURCE, out=OUT):
    result = subprocess.run(list(map(str, command)), cwd=source, text=True,
                            capture_output=True, timeout=60)
    with (out / (label + ".txt")).open("x") as stream:
        stream.write(result.stdout + result.stderr)
    result.check_returncode()
    return result.stdout + result.stderr


def build(label="runtime", *, source=SOURCE, out=OUT, predecessor=None,
          terminal_validator=None, allow_protected_growth=False):
    prior = preserve()
    if predecessor is not None:
        prior = predecessor
    directory = out / label
    directory.mkdir(exist_ok=False)
    prg, mapping = directory / "GROUP1.prg", directory / "GROUP1.map"
    command = list(prior["command"])
    compiler = Path(command[0])
    lock = read(ROOT / "toolchain/f65_toolchain.lock.json")
    previous.previous.pool.platform.pin(compiler, lock["llvm_mos"]["compiler_sha256"])
    command[command.index("-o") + 1] = str(prg)
    command = ["-Wl,-Map," + str(mapping) if item.startswith("-Wl,-Map,")
               else item for item in command]
    command += [module for module in MODULES if module not in command]
    execute(command, label + "-compiler", source=source, out=out)
    elf = Path(str(prg) + ".elf")
    symbols = execute([compiler.parent / "llvm-nm", elf], label + "-symbols", source=source, out=out)
    execute([compiler.parent / "llvm-nm", "--print-size", "--size-sort", elf], label + "-sizes", source=source, out=out)
    disassembly = execute([compiler.parent / "llvm-objdump", "-d", "--print-imm-hex", elf], label + "-disassembly", source=source, out=out)
    sections = previous.previous.probe.integration.section_inventory(mapping.read_text())
    end = max(sections[name]["start"] + sections[name]["bytes"] for name in
              (".r0fs_protected", ".text", ".rodata", ".data", ".bss", ".noinit"))
    previous.previous.integration.validate_irq(disassembly)
    (terminal_validator or previous.previous.probe.validate_terminal)(disassembly, symbols)
    protected = sections[".r0fs_protected"]
    if (protected["start"] + protected["bytes"] > 0x4000
            or (not allow_protected_growth
                and protected != prior["sections"][".r0fs_protected"])):
        raise ValueError("protected resident range changed")
    report = {"command": command, "sourceRoot": str(source), "inputs": inputs(source),
              "sections": sections, "prgSha256": sha(prg),
              "prgBytes": prg.stat().st_size, "residentEndExclusive": end,
              "residentFreeBytes": 0xc000 - end,
              "addedVersusPredecessor": end - prior["residentEndExclusive"],
              "fit": "PASS" if end <= 0xc000 else "FAIL",
              "irqTerminalProtectedStatic": "PASS", "executed": False,
              "hardware": "NOT RUN", "carrier": "NOT BUILT"}
    write(directory / "build.json", report)
    preserve()
    print({key: report[key] for key in ("fit", "residentFreeBytes", "addedVersusPredecessor")})


def closeout():
    prior = preserve()
    host = read(OUT / "host-final/validation.json")
    if host["result"] != "PASS" or host["inputs"] != inputs():
        raise ValueError("host qualification/source mismatch")
    build("runtime-checked")
    final = read(OUT / "runtime-checked/build.json")
    if final["prgSha256"] != read(OUT / "runtime-final/build.json")["prgSha256"]:
        raise ValueError("reviewed final target was not reproducible")

    def sizes(path):
        result = {}
        for line in path.read_text().splitlines():
            fields = line.split()
            if len(fields) == 4:
                result[fields[3]] = int(fields[1], 16)
        return result

    before = sizes(previous.OUT / "runtime-sizes.txt")
    after = sizes(OUT / "runtime-checked-sizes.txt")
    growth = sorted(
        ({"symbol": name, "before": before.get(name, 0), "after": size,
          "growth": size - before.get(name, 0)} for name, size in after.items()
         if size > before.get(name, 0)),
        key=lambda item: item["growth"], reverse=True)
    report = {
        "result": "BLOCKED_FULL_RESIDENT_FIT", "fullCandidate": final,
        "hostResult": host["result"], "hostEvidence": "host-final/validation.json",
        "hostGeometryComparisons": host["geometryCrcComparisons"],
        "hostSceneComparisons": host["sceneByteComparisons"],
        "hostCodecRejects": host["codecRejects"],
        "traceMaximumBytes": 327300, "admittedTraceBytes": 327680,
        "traceFreeBytes": 380,
        "sections": {name: {"before": prior["sections"][name]["bytes"],
                           "after": final["sections"][name]["bytes"],
                           "growth": final["sections"][name]["bytes"] - prior["sections"][name]["bytes"]}
                     for name in (".r0fs_protected", ".text", ".rodata", ".data", ".bss", ".noinit")},
        "symbolGrowth": growth,
        "attributionBoundary": "LTO inlines owner and encoding work into main/run_ticks/display_quantum; symbol changes are not exact per-module additive costs.",
        "firstLink": {"path": "runtime/build.json", "overBytes": 1342,
                      "boundary": "Preliminary link before independent pool readback CRC was added; never executed."},
        "preservedPredecessorPrg": prior["prgSha256"],
        "ownerCoverage": {
            "geometry": "Four actual bounded byte-record buffers, claim/populate/hash/release; not production rendering.",
            "tracks": "Actual initially populated scalar slots; original 24-slot/domain arithmetic and held-intent lineage unchanged.",
            "pcm": "Actual channel-0 on/off state; no four-channel contention claim.",
            "cache": "Actual invalidation and successful 255-byte refill; failed copy does not publish valid bytes.",
            "epoch": "Two cumulative checkpoints; no observer reset across returning storage."},
        "recommendedCorrection": [
            "Replace new 32-bit geometry remainder with proven bounded 16-bit arithmetic; the two newly linked 32-bit division/remainder helpers cost 694 bytes combined. Preserve exact values including u16 boundaries.",
            "Measure outlining/reuse at owner serialization and final CRC boundaries to reduce repeated encoding and LTO register pressure. Savings are not yet demonstrated.",
            "Rebuild full candidate and rerun native checks; only a fit pass permits focused NTSC, then PAL and a new carrier."],
        "notAuthorizedOrNotRun": ["Xemu owner integration", "fresh PAL", "new carrier",
            "SD writes", "physical MEGA65", "commit", "push", "full Group 1 acceptance"],
        "limitations": ["Integrated version-6 raw-trace reduction has no fresh captured trace.",
                        "Host audio tests mock registers, DMA/copy and time.",
                        "Target timing and stack changes remain unmeasured."]}
    write(OUT / "closeout.json", report)
    print("Retained failing full-fit candidate, host proof and measured size breakdown")


def freeze():
    preserve()
    close = read(OUT / "closeout.json")
    if close["fullCandidate"]["inputs"] != inputs():
        raise ValueError("candidate changed since closeout")
    evidence = ROOT / "docs/evidence/r0f/group1"
    preceding = read(evidence / "2026-09-30-foreground-memory-experiment/validation.json")
    names = [item["name"] for item in preceding["before"]["manifests"]]
    names.append("2026-09-30-foreground-memory-experiment")
    verified = []
    for name in names:
        manifest = evidence / name / "sha256.json"
        entries = read(manifest)["files"]
        for file, digest in entries.items():
            if sha(evidence / name / file) != digest:
                raise ValueError("older frozen evidence drift: " + name + "/" + file)
        verified.append({"name": name, "entries": len(entries), "sha256": sha(manifest)})
    if sum(item["entries"] for item in verified) != 2226:
        raise ValueError("unexpected older evidence inventory")
    for metadata in (
            ROOT / "build/r0f/group1/integration/build.json",
            ROOT / "build/r0f/group1/carriers/R0FG1P02/canonical/host-gate.json"):
        for file, digest in read(metadata)["inputs"].items():
            if sha(ROOT / file) != digest:
                raise ValueError("passing root input drift: " + file)
    older = read(evidence / "2026-09-30-crc-memory-experiment/validation.json")["before"]
    for file, digest in older["baselines"].items():
        if sha(ROOT / file) != digest:
            raise ValueError("baseline PRG drift: " + file)
    destination = evidence / "2026-09-30-owner-integration"
    destination.mkdir(exist_ok=False)
    shutil.copytree(OUT, destination / "experiment",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for name in ("AGENTS.md", "CURRENT_STATE.md", "WORK_IN_PROGRESS.md",
                 "docs/plans/R0-F_GROUP1_BUILD_INTENT.md", "docs/DEVELOPMENT_WORKFLOW.md",
                 "docs/PROGRAMMING_PRINCIPLES.md", "docs/CODE_STYLE_C.md",
                 "tools/diagnostics/r0f_group1_owner_integration.py"):
        target = destination / "checkpoint" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    write(destination / "validation.json", {
        "result": "HOST_PASS_TARGET_FIT_BLOCKED", "closeout": close,
        "priorFrozenManifests": verified, "priorEntriesVerified": 2226,
        "rootBuildInputsVerified": 93, "carrierInputsVerified": 95,
        "originalBaselinePrgs": older["baselines"],
        "executed": False, "SD": "NOT RUN", "physical": "NOT RUN"})
    files = {str(path.relative_to(destination)): sha(path)
             for path in sorted(destination.rglob("*")) if path.is_file()}
    write(destination / "sha256.json", {"algorithm": "sha256", "files": files})
    for name, digest in files.items():
        if sha(destination / name) != digest:
            raise ValueError("new evidence copy mismatch: " + name)
    preserve()
    print({"frozenFiles": len(files), "previousEntriesVerified": 2226,
           "manifestSha256": sha(destination / "sha256.json"),
           "fullResidentFit": "FAIL", "overBytes": 1809})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "build", "build-final", "closeout", "freeze"))
    {"prepare": prepare, "build": build, "build-final": lambda: build("runtime-final"),
     "closeout": closeout, "freeze": freeze}[parser.parse_args().action]()
