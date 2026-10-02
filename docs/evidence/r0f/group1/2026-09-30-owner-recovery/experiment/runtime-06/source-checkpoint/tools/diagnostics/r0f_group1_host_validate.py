#!/usr/bin/env python3
"""Exercise actual target C and compare lineage with the independent host oracle."""
import json
import re
from pathlib import Path
import subprocess

import r0f_group1_contract as contract
import r0f_group1_reduce as reducer


def main():
    contract.generate()
    output = contract.ROOT / "build/r0f/group1/integration"
    output.mkdir(parents=True, exist_ok=True)
    executable = output / "workload-host-test"
    command = ["/usr/bin/clang", "-std=c11", "-Wall", "-Wextra", "-Wconversion",
               "-Werror", "-fsanitize=address,undefined", "-DR0FG1_INTEGRATION",
               "-Iinterfaces/generated", "-Isrc/diagnostics/r0f",
               "src/diagnostics/r0f/combined_model.c",
               "src/diagnostics/r0f/group1_workload.c",
               "src/diagnostics/r0f/successor_lifecycle.c",
               "tools/diagnostics/r0f_group1_workload_host_test.c", "-o", str(executable)]
    subprocess.run(command, cwd=contract.ROOT, check=True)
    text = subprocess.check_output([executable], text=True)
    ticks = (1600, 3200)
    expected = reducer.golden(ticks)
    actual = re.findall(r"lineage (\d+) ([0-9A-F]{8})", text)
    if actual != [(str(tick), value) for tick, value in zip(ticks, expected)]:
        raise ValueError("independent model lineage mismatch")
    sidecar, runs = reducer.sidecar_golden(ticks[-1])
    if f"sidecar {sidecar:08X} {' '.join(map(str, runs))}" not in text:
        raise ValueError("independent sidecar lineage mismatch")
    (output / "host-validation.json").write_text(json.dumps({
        "result": "PASS", "command": command, "output": text,
        "independentLineage": expected, "independentSidecar": f"{sidecar:08X}",
        "scope": "stage order, stage-2 input latch, held-intent causality, complete fixture lineage, streaming CRC",
    }, indent=2) + "\n")
    print(text, end="")


if __name__ == "__main__":
    main()
