#!/usr/bin/env python3
"""Qualify owner-fed pool observations without modifying the integrated PRG."""
import json
import re
import subprocess
import sys

import r0f_group1_pool_contract as contract
import r0f_platform_build as platform

ROOT = contract.ROOT
OUT = ROOT / "build/r0f/group1/pool-core"
SOURCE = "src/diagnostics/r0f/group1_pool.c"
TEST = "tools/diagnostics/r0f_group1_pool_host_test.c"
INPUTS = [SOURCE, SOURCE[:-1] + "h", TEST,
          "tools/diagnostics/r0f_group1_pool_shape.c",
          "tools/diagnostics/r0f_group1_pool_build.py",
          "tools/diagnostics/r0f_group1_pool_contract.py",
          "tools/diagnostics/test_r0f_group1_pool_contract.py",
          "interfaces/r0f_group1_pool_contract.json",
          "interfaces/generated/r0f_group1_pool.h",
          "interfaces/r0f_group1_trace_contract.json",
          "interfaces/generated/r0f_group1_trace.h",
          "toolchain/f65_toolchain.lock.json",
          "tools/diagnostics/r0f_platform_build.py",
          "docs/plans/R0-F_GROUP1_BUILD_INTENT.md",
          "spec/core/F65_Main_Concept_v1.6_FINAL_HUMAN_REVIEWED.md"]


def preserved_baseline():
    baseline = ROOT / "build/r0f/group1/integration"
    metadata = json.loads((baseline / "build.json").read_text())
    if (platform.sha(baseline / "GROUP1.prg") != metadata["prgSha256"]
            or any(platform.sha(ROOT / name) != digest
                   for name, digest in metadata["inputs"].items())):
        raise ValueError("passing integrated baseline drift")
    return metadata


def main():
    baseline = preserved_baseline()
    wire = contract.generate()
    trace = json.loads((ROOT / "interfaces/r0f_group1_trace_contract.json").read_text())
    c = trace["constants"]
    ticks = c["EPOCHS"] * c["PHASES"] * c["TICKS_PER_PHASE"]
    OUT.mkdir(parents=True, exist_ok=True)
    commands = []

    def run(arguments):
        command = list(map(str, arguments))
        commands.append(command)
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                timeout=60)
        if result.returncode:
            print(result.stdout + result.stderr, end="")
        result.check_returncode()
        return result.stdout + result.stderr

    flags = ["-Wall", "-Wextra", "-Wconversion", "-Werror",
             "-Isrc/diagnostics/r0f", "-Iinterfaces/generated"]
    executable = OUT / "pool-host-test"
    run(["/usr/bin/clang", "-std=c11", "-UNDEBUG", *flags,
         "-fsanitize=address,undefined", SOURCE, TEST, "-o", executable])
    actual = run([executable])
    (OUT / "host-observations.txt").write_text(actual)
    rows = actual.splitlines()
    boundary = re.fullmatch(r"Boundary PASS: (\d+) transitions; two 65535-sample counter limits", rows[0])
    if not boundary or len(rows) != ticks * len(wire["pools"]) + 1:
        raise ValueError("incomplete owner observation corpus")
    capacities = [pool["capacity"] for pool in wire["pools"].values()]
    peaks = [0] * len(capacities)
    full_samples = [0] * len(capacities)
    zero_samples = [0] * len(capacities)
    for index, row in enumerate(rows[1:]):
        tick, pool = index // len(capacities) + 1, index % len(capacities)
        occupancy = (tick + pool * wire["fixtureParameters"]["OFFSET_STRIDE"]) % (capacities[pool] + 1)
        peaks[pool] = max(peaks[pool], occupancy)
        full_samples[pool] += occupancy == capacities[pool]
        zero_samples[pool] += occupancy == 0
        expected = [tick, pool, occupancy, peaks[pool], tick, full_samples[pool]]
        if row.split()[0] != "ROW" or list(map(int, row.split()[1:])) != expected:
            raise ValueError(f"independent observation mismatch at tick {tick}, owner {pool}")
    if peaks != capacities or not all(full_samples) or not all(zero_samples):
        raise ValueError("missing empty/full pool pressure")
    tests = run([sys.executable, "-B", "-m", "unittest", "discover", "-s",
                 "tools/diagnostics", "-p", "test_r0f_group1_pool_contract.py", "-v"])
    (OUT / "contract-tests.txt").write_text(tests)
    lock = json.loads((ROOT / "toolchain/f65_toolchain.lock.json").read_text())
    compiler = platform.TOOLS / lock["llvm_mos"]["compiler"]
    platform.pin(compiler, lock["llvm_mos"]["compiler_sha256"])
    for source, name in [(SOURCE, "group1_pool"),
                         ("tools/diagnostics/r0f_group1_pool_shape.c", "pool-shape")]:
        run([compiler, "-mcpu=mos45gs02", "-Oz", "-fno-lto", *flags,
             "-c", source, "-o", OUT / (name + ".o")])
    sizes = run([platform.TOOLS / "llvm-nm", "-S", OUT / "pool-shape.o"])
    (OUT / "target-shape-symbols.txt").write_text(sizes)
    shape = re.search(r"^[0-9a-f]+\s+([0-9a-f]+)\s+B\s+r0fg1_pool_shape$", sizes, re.M)
    if not shape:
        raise ValueError("missing target observer size")
    target_bytes = int(shape[1], 16)
    if target_bytes % len(capacities):
        raise ValueError("inconsistent target state size")
    preserved_baseline()
    report = {
        "identity": wire["id"], "result": "PASS", "commands": commands,
        "inputs": {name: platform.sha(ROOT / name) for name in INPUTS},
        "hostSanitizers": "PASS", "transitionCases": int(boundary[1]),
        "independentSamples": ticks * len(capacities), "hostTicks": ticks,
        "emptyFullPressure": "PASS", "peerIsolation": "PASS",
        "counterBoundarySequences": 2, "contractTests": 5,
        "capacities": capacities, "peaks": peaks, "fullSamples": full_samples,
        "zeroSamples": zero_samples, "targetObjectCompilation": "PASS",
        "targetStateBytes": target_bytes,
        "targetObjectSha256": platform.sha(OUT / "group1_pool.o"),
        "preservedIntegratedPrgSha256": baseline["prgSha256"],
        "preservedIntegratedInputCount": len(baseline["inputs"]),
        "baselineResidentFreeBytes": baseline["residentFreeBytes"],
        "stateAloneExceedsBaselineSlack": target_bytes > baseline["residentFreeBytes"],
        "targetLinkMemoryTiming": "NOT RUN", "integratedPoolOwnerHooks": "NOT RUN",
        "newXemu": "NOT RUN", "sd": "NOT RUN", "physical": "NOT RUN",
        "fullGroup1Acceptance": False,
        "boundary": "Pure observation kernel and synthetic host occupancy only; not allocation, renderer geometry, audio scheduling/cache, real sensors or target runtime high-water proof",
    }
    (OUT / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"Pool observation PASS: {report['transitionCases']} transitions, "
          f"{report['independentSamples']} independent samples, five contract tests; "
          f"target state {target_bytes} bytes, baseline slack {baseline['residentFreeBytes']} bytes")


if __name__ == "__main__":
    main()
