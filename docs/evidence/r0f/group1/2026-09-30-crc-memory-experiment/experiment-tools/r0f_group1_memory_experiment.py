#!/usr/bin/env python3
"""One isolated CRC-size experiment; keep the passing source/build untouched."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

import r0f_group1_export_probe as probe
import r0f_group1_integration as integration
import r0f_group1_pool_build as pool
import r0f_group1_reduce as reducer
import r0f_group1_run as acquisition

ROOT = probe.ROOT
OUT = ROOT / "build/r0f/group1/crc-recovery/nibble-01"
SOURCE_ROOT = OUT / "source-inputs"
WORKLOAD_TEST = "tools/diagnostics/r0f_group1_workload_host_test.c"
CHANGED = {
    "src/diagnostics/r0f/successor_lifecycle.c",
    "tools/diagnostics/r0f_group1_contract.py",
    "interfaces/generated/r0f_group1_crc_table.inc",
}


def write_report(path, value):
    probe.emulator.write_json(path, value)


def checked_baseline():
    metadata = pool.preserved_baseline()
    qualification = probe.emulator.read_json(pool.OUT / "validation.json")
    if qualification["result"] != "PASS" or any(
            probe.emulator.sha256(ROOT / name) != digest
            for name, digest in qualification["inputs"].items()):
        raise ValueError("pool qualification drift")
    return metadata, qualification


def prepare():
    baseline, qualification = checked_baseline()
    OUT.mkdir(parents=True, exist_ok=False)
    inputs = {**baseline["inputs"], **qualification["inputs"]}
    inputs[WORKLOAD_TEST] = probe.emulator.sha256(ROOT / WORKLOAD_TEST)
    for name in sorted(inputs):
        target = SOURCE_ROOT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    baseline_dir = OUT / "baseline"
    baseline_dir.mkdir()
    for name in ("GROUP1.prg", "GROUP1.prg.elf", "GROUP1.map",
                 "symbols.txt", "disassembly.txt", "build.json"):
        shutil.copyfile(ROOT / "build/r0f/group1/integration" / name,
                        baseline_dir / name)
    write_report(OUT / "preparation.json", {
        "baseline": baseline, "originalInputs": inputs,
        "poolQualification": qualification,
        "carrierSha256": probe.emulator.sha256(
            ROOT / "build/r0f/group1/carriers/R0FG1P02/canonical/R0FG1P02.D81"),
        "allowedExperimentalChanges": sorted(CHANGED),
    })
    print("Copied exact passing inputs/build; canonical source and carrier untouched")


def checked_snapshot():
    baseline, _ = checked_baseline()
    prepared = probe.emulator.read_json(OUT / "preparation.json")
    if prepared["baseline"] != baseline:
        raise ValueError("baseline metadata drift")
    changes = {name for name, digest in prepared["originalInputs"].items()
               if probe.emulator.sha256(SOURCE_ROOT / name) != digest}
    if changes != CHANGED:
        raise ValueError(f"unexpected snapshot changes: {sorted(changes)}")
    if probe.emulator.sha256(
            ROOT / "build/r0f/group1/carriers/R0FG1P02/canonical/R0FG1P02.D81"
    ) != prepared["carrierSha256"]:
        raise ValueError("preserved carrier drift")
    return prepared


def execute(command, name, cwd=SOURCE_ROOT):
    result = subprocess.run(list(map(str, command)), cwd=cwd,
                            capture_output=True, text=True, timeout=60)
    (OUT / (name + ".txt")).write_text(result.stdout + result.stderr)
    result.check_returncode()
    return result.stdout + result.stderr


def require_ntsc_gate(reduction, execution):
    if (reduction.get("acquisition") != "PASS"
            or reduction.get("nominalTiming") != "WITHIN_OBSERVED_BOUNDS"
            or reduction.get("records") != reducer.C["EPOCHS"] * reducer.C["PHASES"] * reducer.C["TICKS_PER_PHASE"]
            or execution.get("videoArgument") != "1"
            or execution.get("videoMode") != "NTSC"
            or execution.get("status") != 4 or execution.get("error") != 0):
        raise ValueError("focused complete NTSC gate missing")


def build():
    prepared = checked_snapshot()
    baseline = prepared["baseline"]
    compiler = Path(baseline["commands"][0][0])
    lock = probe.emulator.read_json(ROOT / "toolchain/f65_toolchain.lock.json")
    pool.platform.pin(compiler, lock["llvm_mos"]["compiler_sha256"])
    builds = {}
    for label, extra in (
            ("runtime", []),
            ("pool-fit", [pool.SOURCE, "tools/diagnostics/r0f_group1_pool_shape.c",
                          "-Wl,--undefined=r0fg1_pool_init",
                          "-Wl,--undefined=r0fg1_pool_sample",
                          "-Wl,--undefined=r0fg1_pool_shape"])):
        output = OUT / label
        output.mkdir(exist_ok=False)
        command = list(baseline["commands"][0])
        prg = output / "GROUP1.prg"
        mapping = output / "GROUP1.map"
        for index, value in enumerate(command):
            if value.startswith("-Wl,-Map,"):
                command[index] = "-Wl,-Map," + str(mapping)
            elif value == "-o":
                command[index + 1] = str(prg)
        command += extra
        execute(command, label + "-compiler")
        elf = Path(str(prg) + ".elf")
        symbols = execute([compiler.parent / "llvm-nm", elf], label + "-symbols")
        disassembly = execute([compiler.parent / "llvm-objdump", "-d",
                               "--print-imm-hex", elf], label + "-disassembly")
        (output / "symbols.txt").write_text(symbols)
        (output / "disassembly.txt").write_text(disassembly)
        sections = probe.integration.section_inventory(mapping.read_text())
        end = max(sections[name]["start"] + sections[name]["bytes"]
                  for name in (".r0fs_protected", ".text", ".rodata",
                               ".data", ".bss", ".noinit"))
        integration.validate_irq(disassembly)
        probe.validate_terminal(disassembly, symbols)
        if sections[".r0fs_protected"] != baseline["sections"][".r0fs_protected"]:
            raise ValueError("protected range changed")
        inputs = {name: probe.emulator.sha256(SOURCE_ROOT / name)
                  for name in prepared["originalInputs"]}
        report = {
            "scope": "isolated nibble CRC experiment; no pool owner hooks",
            "command": command, "sourceRoot": str(SOURCE_ROOT),
            "inputs": inputs, "sections": sections,
            "prgSha256": probe.emulator.sha256(prg),
            "prgBytes": prg.stat().st_size,
            "symbolsSha256": probe.emulator.sha256(output / "symbols.txt"),
            "residentEndExclusive": end, "residentFreeBytes": 0xc000 - end,
            "residentRecoveredBytes": baseline["residentEndExclusive"] - end,
            "fit": "PASS" if end <= 0xc000 else "FAIL",
            "targetStatic": "PASS", "executed": False,
            "xemu": "NOT RUN", "sd": "NOT RUN", "physical": "NOT RUN",
        }
        write_report(output / "build.json", report)
        builds[label] = report
    write_report(OUT / "fit.json", builds)
    checked_snapshot()
    print("Resident free bytes:", {name: row["residentFreeBytes"]
                                    for name, row in builds.items()})


def host():
    checked_snapshot()
    command = ["/usr/bin/clang", "-std=c11", "-Wall", "-Wextra",
               "-Wconversion", "-Werror", "-fsanitize=address,undefined",
               "-DR0FG1_INTEGRATION", "-Iinterfaces/generated",
               "-Isrc/diagnostics/r0f", "src/diagnostics/r0f/combined_model.c",
               "src/diagnostics/r0f/group1_workload.c",
               "src/diagnostics/r0f/successor_lifecycle.c", WORKLOAD_TEST,
               "-o", OUT / "workload-host-test"]
    execute(command, "host-compiler")
    actual = execute([OUT / "workload-host-test"], "host-output")
    expected = reducer.golden((1600, 3200))
    sidecar, runs = reducer.sidecar_golden(3200)
    for tick, lineage in zip((1600, 3200), expected):
        if f"lineage {tick} {lineage}" not in actual:
            raise ValueError("independent lineage mismatch")
    if f"sidecar {sidecar:08X} {' '.join(map(str, runs))}" not in actual:
        raise ValueError("independent sidecar mismatch")
    if "1025 streaming CRC lengths PASS" not in actual:
        raise ValueError("CRC host cases incomplete")
    crc_command = ["/usr/bin/clang", "-std=c11", "-Wall", "-Wextra",
                   "-Wconversion", "-Werror", "-fsanitize=address,undefined",
                   "-DR0FG1_INTEGRATION", "-Iinterfaces/generated",
                   "-Isrc/diagnostics/r0f", "src/diagnostics/r0f/successor_lifecycle.c",
                   ROOT / "tools/diagnostics/r0f_group1_crc_host_test.c",
                   "-o", OUT / "crc-host-test"]
    execute(crc_command, "crc-host-compiler")
    crc_actual = execute([OUT / "crc-host-test"], "crc-host-output")
    write_report(OUT / "host.json", {
        "result": "PASS", "command": list(map(str, command)),
        "crcCommand": list(map(str, crc_command)), "crcOutput": crc_actual,
        "crcTestSha256": probe.emulator.sha256(
            ROOT / "tools/diagnostics/r0f_group1_crc_host_test.c"),
        "snapshotInputs": {
            name: probe.emulator.sha256(SOURCE_ROOT / name)
            for name in probe.emulator.read_json(OUT / "preparation.json")["originalInputs"]
        },
        "output": actual, "independentLineage": expected,
    })
    print(actual, end="")
    print(crc_actual, end="")


def adapter_fit():
    checked_snapshot()
    runtime = probe.emulator.read_json(OUT / "ntsc-03/reduction.json")
    execution = probe.emulator.read_json(OUT / "ntsc-03/execution.json")
    require_ntsc_gate(runtime, execution)
    cold = probe.emulator.read_json(OUT / "pool-fit/build.json")
    output = OUT / "adapter-fit"
    output.mkdir(exist_ok=False)
    source = ROOT / "tools/diagnostics/r0f_group1_pool_adapter_probe.c"
    command = list(cold["command"])
    prg, mapping = output / "FIT-ONLY.prg", output / "FIT-ONLY.map"
    for index, value in enumerate(command):
        if value.startswith("-Wl,-Map,"):
            command[index] = "-Wl,-Map," + str(mapping)
        elif value == "-o":
            command[index + 1] = str(prg)
    command += [str(source), "-Wl,--undefined=r0fg1_pool_probe_begin",
                "-Wl,--undefined=r0fg1_pool_probe_sample",
                "-Wl,--undefined=r0fg1_pool_probe_encode"]
    execute(command, "adapter-fit-compiler")
    sections = probe.integration.section_inventory(mapping.read_text())
    end = max(sections[name]["start"] + sections[name]["bytes"]
              for name in (".r0fs_protected", ".text", ".rodata", ".data", ".bss", ".noinit"))
    write_report(output / "fit.json", {
        "scope": "cold candidate initialization/sample/field-wise export adapter; not real owner hooks or admitted trace",
        "command": command, "sections": sections,
        "residentEndExclusive": end, "residentFreeBytes": 0xc000 - end,
        "adapterGrowthBytes": end - cold["residentEndExclusive"],
        "overflowBytes": max(0, end - 0xc000),
        "fit": "PASS_STATIC_ONLY" if end <= 0xc000 else "FAIL",
        "prgSha256": probe.emulator.sha256(prg),
        "sourceSha256": probe.emulator.sha256(source),
        "source": str(source), "snapshotInputs": cold["inputs"],
        "executed": False, "admitted": False, "actualOwnerHooks": "NOT RUN",
        "xemu": "NOT RUN", "sd": "NOT RUN", "physical": "NOT RUN",
    })
    checked_snapshot()
    print(f"Cold adapter fit: end ${end:04X}, free {0xc000 - end}, never executed")


def run(attempt):
    checked_snapshot()
    fit = probe.emulator.read_json(OUT / "fit.json")
    if any(row["fit"] != "PASS" for row in fit.values()):
        raise ValueError("both runtime and dormant pool fit must pass before execution")
    host_report = probe.emulator.read_json(OUT / "host.json")
    if host_report["result"] != "PASS":
        raise ValueError("host gate missing")
    for report in (*fit.values(), host_report):
        inputs = report.get("snapshotInputs", report.get("inputs"))
        if any(probe.emulator.sha256(SOURCE_ROOT / name) != digest
               for name, digest in inputs.items()):
            raise ValueError("qualified experimental source drift")
    if probe.emulator.sha256(ROOT / "tools/diagnostics/r0f_group1_crc_host_test.c") != host_report["crcTestSha256"]:
        raise ValueError("qualified CRC host test drift")
    if not 1 <= attempt <= 99:
        raise ValueError("attempt identity outside bounded range")
    output = OUT / f"ntsc-{attempt:02d}"
    output.mkdir(exist_ok=False)
    metadata = fit["runtime"]
    prg = OUT / "runtime/GROUP1.prg"
    symbols = (OUT / "runtime/symbols.txt").read_text()
    if probe.emulator.sha256(prg) != metadata["prgSha256"]:
        raise ValueError("experimental PRG drift")
    write_report(output / "build-identity.json", metadata)
    probe.emulator.PRG = prg
    probe.emulator.SOURCE_BRANCH = probe.emulator.git_text("branch", "--show-current")
    image = output / "G1DEV01.D81"
    token = ROOT / "docs/evidence/r0f/successor/2026-09-21/TOKEN.prg"
    probe.emulator.fresh_d81(output, image, "G1 TIMING DEV", {"token": token})
    _, execution = probe.emulator.run_xemu(output, "1", image,
                                          "GROUP1_CRC_EXPERIMENT", False, 120)
    report, _ = acquisition.reduce_export(output, image, symbols, execution)
    require_ntsc_gate(report, probe.emulator.read_json(output / "execution.json"))
    checked_snapshot()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "build", "host", "run", "adapter-fit"))
    parser.add_argument("--attempt", type=int, default=3,
                        help="Fresh NTSC fixture identity; never overwrites a prior attempt")
    arguments = parser.parse_args()
    if arguments.action == "run":
        run(arguments.attempt)
    else:
        {"prepare": prepare, "build": build, "host": host,
         "adapter-fit": adapter_fit}[arguments.action]()
