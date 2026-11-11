"""Qualify an exact extended-profile link read-only; never starts Xemu."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time

import linked_admission
import stack_admission
import startup_check

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "docs/evidence/flight-demo/2026-10-30-m2-extended-resident"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qualify(packet, references):
    out = EVIDENCE / ("qualification-" + str(time.time_ns()))
    out.mkdir(exist_ok=False)
    report = {"identity": "65AERO-M2-EXTRES-1", "tier": "linked static admission",
              "target": str(packet.relative_to(ROOT)), "target_executed": False,
              "Xemu": "NOT RUN", "status": "BLOCKED", "commands": []}
    run = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s",
                          "tests/flight_demo/m2_rebuild", "-p", "test_*admission.py", "-v"],
                         cwd=ROOT, text=True, capture_output=True)
    (out / "verifier-regressions.txt").write_text(run.stdout + run.stderr)
    report["commands"].append({"argv": run.args, "exit": run.returncode,
                               "log": "verifier-regressions.txt"})
    if run.returncode:
        raise RuntimeError("verifier regressions failed")
    program = out / "staging-ranges"
    for command, log in [
        (["/usr/bin/clang", "-std=c11", "-Wall", "-Wextra", "-Wconversion", "-Werror",
          "-fsanitize=address,undefined", "-Iinterfaces/generated", "-Isrc/diagnostics/r0f",
          "src/diagnostics/r0f/combined_model.c", "tests/flight_demo/m2_rebuild/residency_ranges.c",
          "-o", str(program)], "staging-compile.txt"),
        ([str(program)], "staging-ranges.txt")]:
        completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        (out / log).write_text(completed.stdout + completed.stderr)
        report["commands"].append({"argv": command, "exit": completed.returncode, "log": log})
        if completed.returncode:
            raise RuntimeError(log + " failed")
    result = json.loads((packet / "result.json").read_text())
    prg = (packet / "UNADMITTED.prg").read_bytes()
    elf = (packet / "UNADMITTED.prg.elf").read_bytes()
    disassembly = (packet / "UNADMITTED.disassembly").read_text()
    symbols = (packet / "UNADMITTED.symbols").read_text()
    report["target_prg_sha256"] = sha(packet / "UNADMITTED.prg")
    report["target_seal_sha256"] = sha(packet / "seal.json")
    report["toolchain"] = result["toolchain"]
    parent = json.loads((ROOT / "docs/evidence/flight-demo/2026-10-30-m2-final-unbanked-fit/target-1793382249042750000/result.json").read_text())
    # This qualification is for the frozen renderer and new startup contract,
    # not a reusable admission of an arbitrary future rendering implementation.
    rendering = [name for name in result["inputs"] if name.endswith(".c") and name.startswith("src/")]
    for name in rendering:
        if result["inputs"][name] != parent["inputs"][name]:
            raise ValueError("unreviewed rendering/runtime implementation changed: " + name)
    if result["toolchain"]["flags"] != parent["toolchain"]["flags"] \
       or result["toolchain"]["sdk_identity_digest"] != parent["toolchain"]["sdk_identity_digest"]:
        raise ValueError("frozen compiler or flags changed")
    report["frozen_application"] = {"status": "PASS", "unchanged_C_inputs": len(rendering),
        "reference": "aed5bfb exact archived target inputs; new Platform startup is separately decoded"}
    for name, identity in json.loads((packet / "seal.json").read_text()).items():
        path = packet / name
        if sha(path) != identity["sha256"] or path.stat().st_size != identity["bytes"]:
            raise ValueError("sealed target identity changed: " + name)
    for name, digest in result["inputs"].items():
        if (name.startswith("src/") or name.startswith("interfaces/") or name.startswith("memory/")) \
           and sha(ROOT / name) != digest:
            raise ValueError("tested application/contract changed: " + name)
    stages = [
        ("load", lambda: linked_admission.check_load(prg, elf, result)),
        ("canonical_prefix", lambda: startup_check.check(disassembly, symbols, prg)),
        ("initialization", lambda: linked_admission.check_initialization(prg, disassembly, symbols)),
        ("application_mapping", lambda: linked_admission.check_application_mapping(disassembly, symbols)),
        ("application_stack", lambda: stack_admission.check(disassembly, symbols))]
    for name, check in stages:
        try:
            report[name] = check()
        except (ValueError, KeyError, AssertionError) as error:
            report[name] = {"status": "FAIL", "reason": str(error)}
            report["first_unresolved_gate"] = name
            break
    if "application_stack" in report and report["application_stack"]["status"] == "PASS":
        timing_path = references / "xemu/cpu65_mega65_timings.h"
        text = timing_path.read_text()
        blob = hashlib.sha1(b"blob " + str(len(timing_path.read_bytes())).encode() + b"\0" + timing_path.read_bytes()).hexdigest()
        if blob != "03ead4f0ce7d08e3812b1ca405ad60a62f2803a7":
            raise ValueError("timing primary source identity differs")
        timings = list(map(int, re.search(r"#define TIMINGS_65GS_FAST\s*\{([^}]+)\}", text)[1].split(",")))
        if len(timings) != 256:
            raise ValueError("timing table malformed")
        try:
            report["renderer_service"] = linked_admission.service_lower_bound(prg, disassembly, symbols, timings)
        except (ValueError, KeyError, AssertionError) as error:
            report["renderer_service"] = {"status": "UNPROVEN", "reason": str(error)}
        report["timing_source"] = {"sha256": sha(timing_path), "git_blob": blob,
            "url": "https://github.com/lgblgblgb/xemu/blob/40dfef0d1d5f56be2469492715c12bdb32c75b67/xemu/cpu65_mega65_timings.h"}
        report["first_unresolved_gate"] = "whole-program privileged trap/entry proof remains UNPROVEN; renderer cadence independently FAILS"
    report["runtime_overall"] = "NOT ADMITTED; launch and all eight operation/guard grants remain zero"
    report["evidence_limits"] = {"whole_program_stack": "UNPROVEN until exact privileged trap stack/restoration and entry/NMI conditions close",
        "startup_execution": "UNPROVEN; static prefix/initialization is not observed fresh-entry/Hypervisor behavior",
        "display_and_physical_address_execution": "NOT RUN", "emulator_visuals": "NOT OBSERVED",
        "physical": "NOT RUN", "reserve_used": 0}
    report["checker_inputs"] = {str(path.relative_to(ROOT)): sha(path)
        for path in [Path(__file__), Path(linked_admission.__file__), Path(stack_admission.__file__),
                     Path(startup_check.__file__), *sorted((ROOT / "tests/flight_demo/m2_rebuild").glob("test_*admission.py"))]}
    report["checker_inputs"]["tests/flight_demo/m2_rebuild/residency_ranges.c"] = sha(ROOT / "tests/flight_demo/m2_rebuild/residency_ranges.c")
    report["checker_inputs"]["src/diagnostics/r0f/combined_model.c"] = sha(ROOT / "src/diagnostics/r0f/combined_model.c")
    (out / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    (out / "seal.json").write_text(json.dumps({p.name: {"bytes": p.stat().st_size, "sha256": sha(p)}
                                              for p in out.iterdir()}, indent=2) + "\n")
    print(json.dumps({"output": str(out), "status": report["status"],
                      "startup": report.get("initialization"), "stack": report.get("application_stack"),
                      "service": report.get("renderer_service"),
                      "first_unresolved_gate": report.get("first_unresolved_gate")}))
    return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--references", type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(qualify(args.packet.resolve(), args.references.resolve()))
