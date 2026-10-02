#!/usr/bin/env python3
"""Compare actual C scene encoding with an independent rank/enumeration oracle."""
import subprocess
import sys

import r0f_group1_presentation_contract as contract
import r0f_group1_reduce as reducer
import r0f_successor_emulator as runtime


def main():
    contract.generate()
    output = contract.ROOT / "build/r0f/group1/scene"
    output.mkdir(parents=True, exist_ok=True)
    flags = ["-Wall", "-Wextra", "-Wconversion", "-Werror",
             "-Isrc/diagnostics/r0f", "-Iinterfaces/generated"]
    commands = []

    def run(arguments):
        commands.append(list(map(str, arguments)))
        result = subprocess.run(commands[-1], cwd=contract.ROOT, text=True,
                                capture_output=True)
        result.check_returncode()
        return result.stdout + result.stderr

    sources = ["src/diagnostics/r0f/group1_presentation.c",
               "src/diagnostics/r0f/group1_scene.c"]
    test = "tools/diagnostics/r0f_group1_scene_host_test.c"
    executable = output / "scene-host-test"
    run(["/usr/bin/clang", "-std=c11", *flags, "-fsanitize=address,undefined",
         *sources, test, "-o", executable])
    actual = run([executable])
    (output / "scene-host-test.txt").write_text(actual)
    rows = actual.splitlines()
    if len(rows) != 3201 or rows[-1] != "Scene owner cancellation/coherence PASS":
        raise ValueError("scene test shape")
    tier = 0
    for tick, row in enumerate(rows[:-1], 1):
        tier = reducer.scene_tier(tier, tick)
        expected, _ = reducer.scene_expected(tick, tick,
            (tick >> reducer.P["VIEW_TICK_SHIFT"]) & 1, tier, tick & 1)
        if bytes.fromhex(row) != expected:
            raise ValueError(f"independent scene mismatch at tick {tick}")
    tests = run([sys.executable, "-B", "-m", "unittest", "discover",
                 "-s", "tools/diagnostics", "-p", "test_r0f_group1*contract.py", "-v"])
    (output / "contract-tests.txt").write_text(tests)
    # Retain the isolated kernel's exhaustive negative/boundary corpus too.
    pure = output / "presentation-host-test"
    run(["/usr/bin/clang", "-std=c11", *flags, "-fsanitize=address,undefined",
         sources[0], "tools/diagnostics/r0f_group1_presentation_host_test.c",
         "-o", pure])
    pure_text = run([pure])
    (output / "presentation-host-test.txt").write_text(pure_text)
    inputs = [*sources, test, "src/diagnostics/r0f/group1_scene.h",
              "src/diagnostics/r0f/group1_presentation.h",
              "interfaces/r0f_group1_presentation_contract.json",
              "interfaces/generated/r0f_group1_presentation.h",
              "tools/diagnostics/r0f_group1_scene_validate.py",
              "tools/diagnostics/r0f_group1_reduce.py"]
    runtime.write_json(output / "validation.json", {
        "result": "PASS", "commands": commands,
        "independentSceneComparisons": 3200,
        "hostSanitizers": "PASS", "purePresentationBoundaryCorpus": pure_text,
        "inputs": {name: runtime.sha256(contract.ROOT / name) for name in inputs},
        "targetMemoryTiming": "NOT RUN", "physical": "NOT RUN",
    })
    print("3200 independent scene encodings, cancellation, exhaustive kernel corpus and contract tests PASS")


if __name__ == "__main__":
    main()
