#!/usr/bin/env python3
"""Qualify the isolated presentation kernel; preserve the integrated baseline."""
import json
import subprocess
import sys

import r0f_group1_presentation_contract as contract
import r0f_platform_build as platform

ROOT = contract.ROOT
OUT = ROOT / "build/r0f/group1/presentation-core"
SOURCE = "src/diagnostics/r0f/group1_presentation.c"
TEST = "tools/diagnostics/r0f_group1_presentation_host_test.c"
INPUTS = [
    SOURCE, SOURCE[:-1] + "h", TEST,
    "interfaces/r0f_group1_presentation_contract.json",
    "interfaces/generated/r0f_group1_presentation.h",
    "tools/diagnostics/r0f_group1_presentation_contract.py",
    "tools/diagnostics/test_r0f_group1_presentation_contract.py",
    "tools/diagnostics/r0f_group1_presentation_build.py",
    "tools/diagnostics/r0f_platform_build.py",
    "docs/plans/R0-F_GROUP1_BUILD_INTENT.md",
    "docs/plans/R0-F_GROUP1_MEASUREMENT_MATRIX.md",
    "spec/core/F65_Main_Concept_v1.6_FINAL_HUMAN_REVIEWED.md",
    "spec/subsystems/F-65_Megawing_Graphics_White_Paper_v2.1.pdf",
]


def check_baseline(metadata, prg):
    if (platform.sha(prg) != metadata["prgSha256"]
            or any(platform.sha(ROOT / name) != digest
                   for name, digest in metadata["inputs"].items())):
        raise ValueError("integrated baseline drift")


def main():
    baseline = ROOT / "build/r0f/group1/integration"
    metadata = json.loads((baseline / "build.json").read_text())
    prg = baseline / "GROUP1.prg"
    check_baseline(metadata, prg)
    contract.generate()
    OUT.mkdir(parents=True, exist_ok=True)
    commands = []

    def run(arguments):
        command = list(map(str, arguments))
        commands.append(command)
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        print(result.stdout + result.stderr, end="")
        result.check_returncode()
        return result.stdout

    flags = ["-Wall", "-Wextra", "-Wconversion", "-Werror",
             "-Isrc/diagnostics/r0f", "-Iinterfaces/generated"]
    executable = OUT / "presentation-host-test"
    run(["/usr/bin/clang", "-std=c11", *flags, "-fsanitize=address,undefined",
         SOURCE, TEST, "-o", executable])
    host = run([executable])
    run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tools/diagnostics",
         "-p", "test_r0f_group1_presentation_contract.py", "-v"])
    compiler = platform.TOOLS / "mos-mega65-clang"
    platform.pin(compiler,
                 "cc557ae99a68ed36e098062b0f5376a878e94ac187b87446c8e603e4fb45a906")
    object_path = OUT / "group1_presentation.o"
    run([compiler, "-mcpu=mos45gs02", "-Oz", "-fno-lto", *flags,
         "-c", SOURCE, "-o", object_path])
    check_baseline(metadata, prg)
    report = {
        "identity": "R0FG1-PRESENTATION-CORE-1",
        "inputs": {name: platform.sha(ROOT / name) for name in INPUTS},
        "commands": commands,
        "hostOutput": host,
        "hostSanitizers": "PASS",
        "anchorPermutations": 720,
        "occlusionEnumerationCases": 2592,
        "lodComparisons": 131072,
        "contractTests": 4,
        "targetObjectCompilation": "PASS",
        "targetObjectSha256": platform.sha(object_path),
        "preservedIntegratedPrgSha256": metadata["prgSha256"],
        "preservedIntegratedInputCount": len(metadata["inputs"]),
        "targetLinkMemoryTiming": "NOT RUN",
        "group1IntegratedPresentation": "NOT RUN",
        "xemuForNewKernel": "NOT RUN",
        "sd": "NOT RUN",
        "physical": "NOT RUN",
        "fullGroup1Acceptance": False,
    }
    (OUT / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print("Isolated presentation host/target-object PASS; integrated PRG unchanged")


if __name__ == "__main__":
    main()
