#!/usr/bin/env python3
"""Isolated foreground bounds-helper recovery from the qualified nibble CRC."""
import argparse
import shutil
import subprocess
from pathlib import Path

import r0f_group1_memory_experiment as previous

ROOT = previous.ROOT
OUT = ROOT / "build/r0f/group1/foreground-recovery/shared-bounds-01"
SOURCE = OUT / "source-inputs"
CHANGED = "src/diagnostics/r0f/combined_model.c"
EXTRA = (
    "tools/diagnostics/r0f_combined_host_test.c",
    "tools/diagnostics/r0f_group1_pool_adapter_probe.c",
    "tools/diagnostics/r0f_group1_pool_adapter_host_test.c",
    "tools/diagnostics/r0f_group1_crc_host_test.c",
)
read = previous.probe.emulator.read_json
sha = previous.probe.emulator.sha256
write = previous.write_report


def preserve():
    previous.checked_snapshot()
    freeze = ROOT / "docs/evidence/r0f/group1/2026-09-30-crc-memory-experiment"
    manifest = read(freeze / "sha256.json")
    for name, digest in manifest["files"].items():
        if sha(freeze / name) != digest:
            raise ValueError("predecessor evidence drift: " + name)
    prior = read(previous.OUT / "fit.json")["runtime"]
    if sha(previous.OUT / "runtime/GROUP1.prg") != prior["prgSha256"]:
        raise ValueError("qualified nibble PRG drift")
    previous.require_ntsc_gate(read(previous.OUT / "ntsc-03/reduction.json"),
                               read(previous.OUT / "ntsc-03/execution.json"))
    return prior


def prepare():
    prior = preserve()
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copytree(previous.SOURCE_ROOT, SOURCE)
    for name in EXTRA:
        shutil.copyfile(ROOT / name, SOURCE / name)
    inputs = {**prior["inputs"], **{name: sha(SOURCE / name) for name in EXTRA}}
    write(OUT / "preparation.json", {"predecessor": prior, "inputs": inputs,
          "allowedChange": CHANGED, "controllerSha256": sha(Path(__file__))})
    print("Prepared separate shared-bounds source snapshot")


def checked():
    prior = preserve()
    preparation = read(OUT / "preparation.json")
    if prior != preparation["predecessor"]:
        raise ValueError("predecessor metadata drift")
    changes = [name for name, digest in preparation["inputs"].items()
               if sha(SOURCE / name) != digest]
    if changes != [CHANGED]:
        raise ValueError("unexpected experimental changes: " + repr(changes))
    return preparation, {name: sha(SOURCE / name)
                         for name in preparation["inputs"]}


def execute(command, log, cwd=SOURCE):
    result = subprocess.run(list(map(str, command)), cwd=cwd, text=True,
                            capture_output=True, timeout=60)
    with (OUT / (log + ".txt")).open("x") as stream:
        stream.write(result.stdout + result.stderr)
    result.check_returncode()
    return result.stdout + result.stderr


def host():
    _, inputs = checked()
    original = read(previous.OUT / "host.json")
    reports = []
    for label, original_command in (("workload", original["command"]),
                                    ("crc", original["crcCommand"])):
        command = [str(SOURCE / Path(item).relative_to(ROOT))
                   if str(item).startswith(str(ROOT / "tools/")) else str(item)
                   for item in original_command]
        binary = OUT / (label + "-host-test")
        command[command.index("-o") + 1] = str(binary)
        execute(command, label + "-host-compiler")
        output = execute([binary], label + "-host-output")
        if label == "workload" and output != original["output"]:
            raise ValueError("workload/independent lineage changed")
        if label == "crc" and output != original["crcOutput"]:
            raise ValueError("independent CRC corpus changed")
        reports.append({"command": command, "output": output})
    command = ["/usr/bin/clang", "-std=c11", "-Wall", "-Wextra", "-Werror",
               "-fsanitize=address,undefined", "-Iinterfaces/generated",
               "-Isrc/diagnostics/r0f", "src/diagnostics/r0f/combined_model.c",
               "tools/diagnostics/r0f_combined_host_test.c",
               "-o", str(OUT / "bounds-host-test")]
    execute(command, "bounds-host-compiler")
    output = execute([OUT / "bounds-host-test"], "bounds-host-output")
    if "range/DMA boundary tests PASS" not in output:
        raise ValueError("range/DMA host gate missing")
    reports.append({"command": command, "output": output,
                    "scope": "shared helper logic; Group 1 outlining checked in target disassembly"})
    write(OUT / "host.json", {"result": "PASS", "inputs": inputs, "checks": reports})
    print("ASan/UBSan workload, CRC and existing range/DMA corpus PASS")


def build():
    preparation, inputs = checked()
    prior = preparation["predecessor"]
    compiler = Path(prior["command"][0])
    lock = read(ROOT / "toolchain/f65_toolchain.lock.json")
    previous.pool.platform.pin(compiler, lock["llvm_mos"]["compiler_sha256"])
    reports = {}
    for label, extra in (("runtime", []), ("adapter-fit", [
            previous.pool.SOURCE, "tools/diagnostics/r0f_group1_pool_shape.c",
            "tools/diagnostics/r0f_group1_pool_adapter_probe.c",
            "-Wl,--undefined=r0fg1_pool_init", "-Wl,--undefined=r0fg1_pool_sample",
            "-Wl,--undefined=r0fg1_pool_shape", "-Wl,--undefined=r0fg1_pool_probe_begin",
            "-Wl,--undefined=r0fg1_pool_probe_sample", "-Wl,--undefined=r0fg1_pool_probe_encode"])):
        directory = OUT / label
        directory.mkdir(exist_ok=False)
        prg, mapping = directory / "GROUP1.prg", directory / "GROUP1.map"
        command = list(prior["command"])
        command[command.index("-o") + 1] = str(prg)
        command = ["-Wl,-Map," + str(mapping) if item.startswith("-Wl,-Map,")
                   else item for item in command] + extra
        execute(command, label + "-compiler")
        elf = Path(str(prg) + ".elf")
        symbols = execute([compiler.parent / "llvm-nm", elf], label + "-symbols")
        sizes = execute([compiler.parent / "llvm-nm", "--print-size", "--size-sort", elf], label + "-sizes")
        disassembly = execute([compiler.parent / "llvm-objdump", "-d", "--print-imm-hex", elf], label + "-disassembly")
        sections = previous.probe.integration.section_inventory(mapping.read_text())
        end = max(sections[name]["start"] + sections[name]["bytes"] for name in
                  (".r0fs_protected", ".text", ".rodata", ".data", ".bss", ".noinit"))
        previous.integration.validate_irq(disassembly)
        previous.probe.validate_terminal(disassembly, symbols)
        if sections[".r0fs_protected"] != prior["sections"][".r0fs_protected"]:
            raise ValueError("protected resident range changed")
        if " t inside\n" not in symbols or "<inside>" not in disassembly:
            raise ValueError("shared bounds helper was not retained")
        report = {"scope": "one shared foreground bounds helper; no actual pool hooks",
                  "command": command, "inputs": inputs, "sections": sections,
                  "sourceRoot": str(SOURCE), "prgSha256": sha(prg),
                  "prgBytes": prg.stat().st_size, "residentEndExclusive": end,
                  "residentFreeBytes": 0xc000 - end,
                  "recoveredVersusNibbleRuntime": prior["residentEndExclusive"] - end,
                  "fit": "PASS" if end <= 0xc000 else "FAIL", "targetStatic": "PASS",
                  "executed": False, "actualPoolObservations": False,
                  "sd": "NOT RUN", "physical": "NOT RUN"}
        write(directory / "build.json", report)
        reports[label] = report
    write(OUT / "fit.json", reports)
    checked()
    print({label: {"fit": report["fit"], "freeBytes": report["residentFreeBytes"]}
           for label, report in reports.items()})


def run():
    _, inputs = checked()
    fit, host_report = read(OUT / "fit.json"), read(OUT / "host.json")
    if any(report["fit"] != "PASS" for report in fit.values()) or host_report["result"] != "PASS":
        raise ValueError("fit and host gates must pass before acquisition")
    if any(report["inputs"] != inputs for report in (*fit.values(), host_report)):
        raise ValueError("qualified source drift")
    directory = OUT / "ntsc-01"
    directory.mkdir(exist_ok=False)
    prg = OUT / "runtime/GROUP1.prg"
    if sha(prg) != fit["runtime"]["prgSha256"]:
        raise ValueError("qualified PRG drift")
    write(directory / "build-identity.json", fit["runtime"])
    emulator = previous.probe.emulator
    emulator.PRG = prg
    emulator.SOURCE_BRANCH = emulator.git_text("branch", "--show-current")
    image = directory / "G1DEV01.D81"
    emulator.fresh_d81(directory, image, "G1 TIMING DEV", {
        "token": ROOT / "docs/evidence/r0f/successor/2026-09-21/TOKEN.prg"})
    _, execution = emulator.run_xemu(directory, "1", image, "GROUP1_SHARED_BOUNDS", False, 120)
    report, _ = previous.acquisition.reduce_export(
        directory, image, (OUT / "runtime-symbols.txt").read_text(), execution)
    previous.require_ntsc_gate(report, read(directory / "execution.json"))
    checked()
    print("Complete focused NTSC export/reduction and nominal timing PASS")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "host", "build", "run"))
    {"prepare": prepare, "host": host, "build": build, "run": run}[parser.parse_args().action]()
