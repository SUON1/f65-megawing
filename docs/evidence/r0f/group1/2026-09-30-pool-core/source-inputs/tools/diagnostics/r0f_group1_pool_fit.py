#!/usr/bin/env python3
"""Static lower-bound pool fit probe; never execute or replace the baseline."""
import argparse
import json
import re
import subprocess
from pathlib import Path

import r0f_group1_pool_build as pool
import r0f_platform_build as platform


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    output = args.out.resolve()
    output.relative_to(pool.ROOT / "build/r0f/group1/pool-core")
    baseline = pool.preserved_baseline()
    qualification = json.loads((pool.OUT / "validation.json").read_text())
    if (qualification["result"] != "PASS"
            or any(platform.sha(pool.ROOT / name) != digest
                   for name, digest in qualification["inputs"].items())):
        raise ValueError("pool qualification source drift")
    output.mkdir(parents=True, exist_ok=False)
    command = list(baseline["commands"][0])
    prg = output / "FIT-ONLY.prg"
    mapping = output / "FIT-ONLY.map"
    for index, value in enumerate(command):
        if value.startswith("-Wl,-Map,"):
            command[index] = "-Wl,-Map," + str(mapping)
        elif value == "-o":
            command[index + 1] = str(prg)
    command += [pool.SOURCE, "tools/diagnostics/r0f_group1_pool_shape.c",
                "-Wl,--undefined=r0fg1_pool_init",
                "-Wl,--undefined=r0fg1_pool_sample",
                "-Wl,--undefined=r0fg1_pool_shape"]
    result = subprocess.run(command, cwd=pool.ROOT, capture_output=True,
                            text=True, timeout=60)
    (output / "compiler-output.txt").write_text(result.stdout + result.stderr)
    if result.returncode:
        raise ValueError("fit-probe compile failed; retain output, not fit evidence")
    sections = {}
    for line in mapping.read_text().splitlines():
        match = re.match(r"\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+(\.[\w.]+)$", line)
        if match:
            sections[match[3]] = {"start": int(match[1], 16), "bytes": int(match[2], 16)}
    allocated = [sections[name] for name in (".r0fs_protected", ".text", ".rodata", ".data", ".bss", ".noinit")]
    end = max(row["start"] + row["bytes"] for row in allocated)
    # An unexecuted link artifact is not admitted merely because clang exits 0.
    report = {
        "scope": "Static lower bound: retained observer API and eight-state array, no owner hooks or telemetry",
        "command": command, "compileExit": result.returncode,
        "residentEndExclusive": end, "residentLimitExclusive": 0xc000,
        "residentGrowthBytes": end - baseline["residentEndExclusive"],
        "overflowBytes": max(0, end - 0xc000),
        "targetStateBytes": qualification["targetStateBytes"], "sections": sections,
        "fit": "FAIL" if end > 0xc000 else "PASS_STATIC_LOWER_BOUND_ONLY",
        "admitted": False, "executed": False,
        "prgSha256": platform.sha(prg),
        "baselinePrgSha256": baseline["prgSha256"],
        "inputs": {**baseline["inputs"], **qualification["inputs"],
                   "tools/diagnostics/r0f_group1_pool_fit.py": platform.sha(Path(__file__))},
        "xemu": "NOT RUN", "sd": "NOT RUN", "physical": "NOT RUN",
    }
    (output / "fit.json").write_text(json.dumps(report, indent=2) + "\n")
    pool.preserved_baseline()
    print(f"Static pool fit {report['fit']}: end ${end:04X}, growth "
          f"{report['residentGrowthBytes']} bytes, over by {report['overflowBytes']}; never executed")


if __name__ == "__main__":
    main()
