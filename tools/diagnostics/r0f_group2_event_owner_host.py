#!/usr/bin/env python3
"""Run only the approved frozen event-owner host proof; never rebuild P09."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/evidence/r0f/group1/2026-10-03-audio-readback/source"
PINS = {
    "src/diagnostics/r0f/combined_model.c":
        "00fed181cd67df8293653b962c481cf7c14a68d3a3e3938f13d74fe78500cd9f",
    "src/diagnostics/r0f/combined_model.h":
        "0931d1e42914903d61d073be597910575a941171c6592b45d4a81649123113df",
    "interfaces/generated/r0f_combined.h":
        "a728d596e43163e28d1de7d2e17ee366b6df4970be8924bff9f64ca2e4a0d4f2",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parent = ROOT / "build/r0f/group2/event-owner"
    parent.mkdir(parents=True, exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix="host-", dir=parent))
    test = ROOT / "tools/diagnostics/r0f_group2_event_owner_host_test.c"
    compiler = Path("/usr/bin/clang")
    inputs = [SOURCE / name for name in PINS] + [test, Path(__file__).resolve()]
    before = {str(path.relative_to(ROOT)): digest(path) for path in inputs}
    report = {
        "result": "FAIL", "scope": "isolated actual r0fc_event/reset host API",
        "integrationMacro": False, "target": "NOT RUN", "xemu": "NOT RUN",
        "physical": "NOT RUN", "inputs": before, "commands": [],
        "compilerSha256": digest(compiler),
        "sourceCommit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "branch": subprocess.check_output(
            ["git", "branch", "--show-current"], cwd=ROOT, text=True).strip(),
    }
    environment = os.environ.copy()
    environment["ASAN_OPTIONS"] = "halt_on_error=1"
    environment["UBSAN_OPTIONS"] = "halt_on_error=1:print_stacktrace=1"
    report["sanitizers"] = {key: environment[key]
                            for key in ("ASAN_OPTIONS", "UBSAN_OPTIONS")}

    def run(name, command):
        result = subprocess.run(command, cwd=ROOT, env=environment,
                                text=True, capture_output=True, timeout=60)
        (output / f"{name}.txt").write_text(result.stdout + result.stderr)
        report["commands"].append({"command": command, "exitCode": result.returncode,
                                   "log": f"{name}.txt"})
        if result.returncode:
            raise RuntimeError(f"{name} failed: exit {result.returncode}")
        return result.stdout

    try:
        for name, expected in PINS.items():
            if digest(SOURCE / name) != expected:
                raise RuntimeError(f"Frozen input mismatch: {name}")
        run("compiler", [str(compiler), "--version"])
        executable = output / "event-owner"
        run("compile", [str(compiler), "-std=c11", "-Wall", "-Wextra", "-Werror",
                        "-fsanitize=address,undefined", "-fno-sanitize-recover=all",
                        "-g", "-I" + str(SOURCE / "interfaces/generated"),
                        "-I" + str(SOURCE / "src/diagnostics/r0f"),
                        str(SOURCE / "src/diagnostics/r0f/combined_model.c"),
                        str(test), "-o", str(executable)])
        report["executableSha256"] = digest(executable)
        result = run("run", [str(executable)])
        if "event-owner PASS:" not in result:
            raise RuntimeError("Missing test completion marker")
        after = {str(path.relative_to(ROOT)): digest(path) for path in inputs}
        report["inputsUnchanged"] = before == after
        if before != after:
            raise RuntimeError("Inputs changed during execution")
        report["result"] = "PASS"
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        report["error"] = str(error)
    finally:
        (output / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
        print(f"{report['result']}: {output / 'validation.json'}")
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
