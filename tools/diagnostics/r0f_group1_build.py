#!/usr/bin/env python3
"""Validate pure Group 1 timing/export modules; no D81, emulator or SD work."""

import hashlib
import json
from pathlib import Path
import subprocess

import r0f_platform_build as platform
import r0f_group1_export_admission as admission


ROOT = platform.ROOT
OUT = ROOT / "build/r0f/group1"
SOURCES = [
    "src/diagnostics/r0f/group1_timing.c",
    "src/diagnostics/r0f/group1_timing.h",
    "tools/diagnostics/r0f_group1_timing_host_test.c",
    "tools/diagnostics/r0f_group1_build.py",
]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    admission.main()
    OUT.mkdir(parents=True, exist_ok=True)
    commands = []

    def run(arguments):
        command = list(map(str, arguments))
        commands.append(command)
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        if result.stderr:
            print(result.stderr, end="")
        if result.stdout:
            print(result.stdout, end="")
        result.check_returncode()
        return result.stdout

    compiler = platform.TOOLS / "mos-mega65-clang"
    platform.pin(compiler,
                 "cc557ae99a68ed36e098062b0f5376a878e94ac187b87446c8e603e4fb45a906")
    objects = {}
    inputs = list(SOURCES)
    for module in ("timing", "export"):
        source = f"src/diagnostics/r0f/group1_{module}.c"
        test = f"tools/diagnostics/r0f_group1_{module}_host_test.c"
        inputs.extend((source, source[:-1] + "h", test))
        executable = OUT / f"{module}-host-test"
        flags = ["-Wall", "-Wextra", "-Wconversion", "-Werror",
                 "-Isrc/diagnostics/r0f", "-Iinterfaces/generated"]
        run(["/usr/bin/clang", "-std=c11", *flags,
             "-fsanitize=address,undefined", source, test, "-o", executable])
        (OUT / f"{module}-host-test.txt").write_text(run([executable]))
        object_path = OUT / f"group1_{module}.o"
        run([compiler, "-mcpu=mos45gs02", "-Oz", "-fno-lto", *flags,
             "-c", source, "-o", object_path])
        objects[module] = digest(object_path)
    inputs.extend((str(admission.CONTRACT.relative_to(ROOT)),
                   "interfaces/generated/r0f_group1_export.h"))
    report = {
        "identity": "R0F-GROUP1-PURE-MODULES",
        "scope": "pure timing and export policy; not integrated Group 1",
        "inputs": {name: digest(ROOT / name) for name in sorted(set(inputs))},
        "commands": commands,
        "hostSanitizers": "PASS",
        "closedFormReleaseComparisons": 1000000,
        "targetObjectCompilation": "PASS",
        "targetObjectSha256": objects,
        "targetLinkAndAccounting": "NOT RUN",
        "group1Integration": "PENDING",
        "d81": "NOT RUN",
        "xemu": "NOT RUN",
        "sd": "NOT RUN",
        "physical": "NOT RUN",
    }
    (OUT / "timing-core-validation.json").write_text(
        json.dumps(report, indent=2) + "\n")
    print("Timing/export host/target-object PASS; Group 1 integration PENDING")


if __name__ == "__main__":
    main()
