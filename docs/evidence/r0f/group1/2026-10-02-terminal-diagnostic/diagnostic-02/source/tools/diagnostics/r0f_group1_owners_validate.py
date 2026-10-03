#!/usr/bin/env python3
"""Native candidate owner checks, independent codec/scene oracle; no target run."""
import argparse
import binascii
import json
import subprocess
from pathlib import Path

import r0f_group1_reduce as reducer
import r0f_group1_contract as trace_contract
import r0f_group1_pool_contract as pool_contract
import r0f_group1_presentation_contract as scene_contract
import r0f_successor_emulator as runtime

ROOT = trace_contract.ROOT
OWNER = ["src/diagnostics/r0f/group1_pool.c", "src/diagnostics/r0f/group1_pool_owners.c"]
GEOMETRY = ["src/diagnostics/r0f/group1_geometry_fixture.c", "src/diagnostics/r0f/successor_lifecycle.c"]
FLAGS = ["/usr/bin/clang", "-std=c11", "-Wall", "-Wextra", "-Wconversion", "-Werror",
         "-fsanitize=address,undefined", "-DR0FG1_INTEGRATION",
         "-Iinterfaces/generated", "-Isrc/diagnostics/r0f"]


def main(out, reference_pool=None, reference_display=None):
    out.mkdir(exist_ok=False)
    commands = []

    def run(command, name):
        result = subprocess.run(list(map(str, command)), cwd=ROOT,
                                text=True, capture_output=True, timeout=60)
        (out / (name + ".txt")).write_text(result.stdout + result.stderr)
        commands.append({"command": list(map(str, command)), "exitCode": result.returncode})
        result.check_returncode()
        return result.stdout

    def native(name, sources, flags=(), arguments=()):
        binary = out / name
        run([*FLAGS, *flags, *sources, "-o", binary], name + "-compiler")
        return run([binary, *arguments], name + "-output")

    expected_generated = {path: runtime.sha256(ROOT / path) for path in (
        "interfaces/generated/r0f_group1_trace.h", "interfaces/generated/r0f_group1_trace.inc",
        "interfaces/generated/r0f_group1_pool.h", "interfaces/generated/r0f_group1_presentation.h",
        "interfaces/generated/r0f_group1_crc_table.inc")}
    trace_contract.generate()
    pool_contract.generate()
    scene_contract.generate()
    assert all(runtime.sha256(ROOT / path) == digest for path, digest in expected_generated.items())
    workload = native("workload", ["src/diagnostics/r0f/combined_model.c",
        "src/diagnostics/r0f/group1_workload.c", "src/diagnostics/r0f/successor_lifecycle.c",
        *OWNER, "tools/diagnostics/r0f_group1_workload_host_test.c"])
    golden = reducer.golden((1600, 3200))
    sidecar, runs = reducer.sidecar_golden(3200)
    assert workload == (f"lineage 1600 {golden[0]}\nlineage 3200 {golden[1]}\n"
                        f"sidecar {sidecar:08X} {' '.join(map(str, runs))}\n"
                        "Stage/input/AI causality and 1025 streaming CRC lengths PASS\n")
    geometry = native("owners", [*OWNER, *GEOMETRY, "tools/diagnostics/r0f_group1_owners_host_test.c"])
    owners = list(reducer.POOL["pools"])
    capacity = [pool["capacity"] for pool in reducer.POOL["pools"].values()]
    samples, full, peak = [1] * 8, [0] * 8, [0] * 8
    comparisons = 0
    for line in geometry.splitlines():
        fields = line.split()
        if fields[0] == "geometry":
            generation, source = map(int, fields[1:3])
            scene, _ = reducer.scene_expected(generation, source, 0, 0, 0)
            assert int(fields[3], 16) == reducer.number(scene, reducer.S["GEOMETRY_CRC"])
            for owner in range(4):
                demand = (generation + owner * reducer.POOL["fixtureParameters"]["OFFSET_STRIDE"]) % (capacity[owner] + 1)
                samples[owner] += 2
                full[owner] += demand == capacity[owner]
                peak[owner] = max(peak[owner], demand)
            comparisons += 1
        elif fields[0] in ("initial", "checkpoint"):
            data = bytes.fromhex(fields[1])
            expected = b"".join(value.to_bytes(2, "little") for owner in range(8)
                                for value in (capacity[owner], peak[owner], samples[owner], full[owner]))
            assert data == expected, fields[0]
    assert comparisons == 3201 and geometry.endswith("owner bounds, first fault, overflow and immutable peers PASS\n")
    scene = native("scene", [*OWNER, *GEOMETRY, "src/diagnostics/r0f/group1_presentation.c",
        "src/diagnostics/r0f/group1_scene.c", "tools/diagnostics/r0f_group1_scene_host_test.c"])
    rows = scene.splitlines()
    assert len(rows) == 3201 and rows[-1] == "Scene owner cancellation/coherence PASS"
    tier = 0
    for tick, row in enumerate(rows[:-1], 1):
        tier = reducer.scene_tier(tier, tick)
        expected, _ = reducer.scene_expected(tick, tick, (tick >> 7) & 1, tier, tick & 1)
        assert bytes.fromhex(row) == expected
    # Test exact owner functions with mocked edges, not a reimplementation.
    platform = (ROOT / "src/diagnostics/r0f/combined_platform.c").read_text()
    audio = platform[platform.index("void cfaudio_stop(void)"):platform.index("void cfinput(void)")]
    (out / "audio_owner_under_test.inc").write_text(audio)
    native("audio", [*OWNER, "tools/diagnostics/r0f_group1_audio_owner_host_test.c"], ["-I" + str(out)])
    capture = (ROOT / "src/diagnostics/r0f/group1_capture.c").read_text()
    helpers = capture[capture.index("static void put16("):capture.index("static uint16_t get16(")]
    checkpoint = capture[capture.index("void r0fg1_phase_end("):capture.index("void r0fg1_tick_open(")]
    finish = capture[capture.index("uint8_t r0fg1_capture_finish_fault("):]
    (out / "capture_owner_under_test.inc").write_text(helpers + checkpoint + finish)
    native("capture", [*OWNER, "src/diagnostics/r0f/successor_lifecycle.c",
        "tools/diagnostics/r0f_group1_capture_owner_host_test.c"], ["-I" + str(out)])
    display = (ROOT / "src/diagnostics/r0f/successor_integration.c").read_text()
    begin = display.index("#ifdef R0FG1_INTEGRATION\nstatic void display_quantum_work(void)")
    end = display.index("\n#ifdef R0FG1_INTEGRATION\nvoid r0fg1_display_metrics", begin)
    (out / "display_owner_under_test.inc").write_text(display[begin:end])
    model = (ROOT / "src/diagnostics/r0f/combined_model.c").read_text()
    begin = model.index("uint8_t r0fc_acquire(")
    end = model.index("\n#ifdef R0FG1_INTEGRATION", begin)
    (out / "snapshot_owner_under_test.inc").write_text(model[begin:end])
    native("display", [*OWNER, *GEOMETRY, "src/diagnostics/r0f/group1_presentation.c",
        "src/diagnostics/r0f/group1_scene.c", "tools/diagnostics/r0f_group1_display_owner_host_test.c"],
        ["-I" + str(out)])
    if reference_display is not None:
        baseline = out / "display-baseline-inputs"
        baseline.mkdir()
        display = reference_display.read_text()
        begin = display.index("#ifdef R0FG1_INTEGRATION\nstatic void display_quantum_work(void)")
        end = display.index("\n#ifdef R0FG1_INTEGRATION\nvoid r0fg1_display_metrics", begin)
        (baseline / "display_owner_under_test.inc").write_text(display[begin:end])
        native("display-baseline", [*OWNER, *GEOMETRY,
            "src/diagnostics/r0f/group1_presentation.c", "src/diagnostics/r0f/group1_scene.c",
            "tools/diagnostics/r0f_group1_display_owner_host_test.c"],
            ["-I" + str(baseline), "-I" + str(out)], ["--baseline"])
    native("pool-core", ["src/diagnostics/r0f/group1_pool.c",
                         "tools/diagnostics/r0f_group1_pool_host_test.c"])
    native("crc", ["src/diagnostics/r0f/successor_lifecycle.c",
                   "tools/diagnostics/r0f_group1_crc_host_test.c"])
    if reference_pool is not None:
        original = out / "reference-pool.o"
        run([*FLAGS, "-Dr0fg1_pool_init=reference_init",
             "-Dr0fg1_pool_sample=reference_sample", "-c", reference_pool,
             "-o", original], "reference-pool-compiler")
        native("recovery-equivalence", [*OWNER, *GEOMETRY, str(original),
            "tools/diagnostics/r0f_group1_recovery_equivalence_test.c"])
    # Synthetic codec boundaries only; never represented as captured evidence.
    data = bytearray(b"".join(value.to_bytes(2, "little") for epoch in range(2)
        for cap in capacity for value in (cap, cap, 101 + epoch, 1 + epoch)))
    reducer.pool_checkpoints(data)
    rejects = 0
    for epoch in range(2):
        for owner in range(8):
            for offset, bad in ((0, capacity[owner] + 1), (2, capacity[owner] + 1),
                                (4, 0), (6, 65535), (6, 0)):
                corrupted = data[:]
                at = epoch * 64 + owner * 8 + offset
                corrupted[at:at + 2] = bad.to_bytes(2, "little")
                try:
                    reducer.pool_checkpoints(corrupted)
                except ValueError:
                    rejects += 1
                else:
                    raise AssertionError("pool decoder accepted corrupted field")
    for mutated in (data[:-1], data + b"\0", data[:64] * 2):
        try:
            reducer.pool_checkpoints(mutated)
        except ValueError:
            rejects += 1
        else:
            raise AssertionError("pool decoder accepted truncation/reset")
    run(["python3", "-B", "-m", "unittest", "discover", "-s", "tools/diagnostics",
         "-p", "test_r0f_group1*contract.py", "-v"], "contracts")
    runtime.write_json(out / "validation.json", {
        "result": "PASS", "commands": commands, "geometryCrcComparisons": comparisons,
        "sceneByteComparisons": 3200, "codecRejects": rejects,
        "displayOwner": "Actual function, physical-edge mocks; 26 cancellation boundaries, copy/DMA retries and snapshot CRC failure PASS",
        "displayReferenceSha256": runtime.sha256(reference_display) if reference_display else None,
        "trackCheckpointCounts": [[1625, 1601], [3225, 3201]],
        "scope": "Native actual-owner functions and independent field/scene oracles only",
        "recoveryEquivalence": {"observerStates": 248832, "generations": 65536,
            "referencePoolSha256": runtime.sha256(reference_pool)} if reference_pool else None,
        "integratedTraceReduction": "NOT RUN", "audioHardware": "NOT RUN",
        "targetTiming": "NOT RUN",
        "inputs": {str(path.relative_to(ROOT)): runtime.sha256(path)
                   for path in sorted(ROOT.rglob("*")) if path.is_file()
                   and "__pycache__" not in path.parts}})
    print("Host owner/scene/workload/audio checks PASS; 83 codec rejects; no target execution")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path)
    parser.add_argument("--reference-pool", type=Path)
    parser.add_argument("--reference-display", type=Path)
    args = parser.parse_args()
    main(args.out, args.reference_pool, args.reference_display)
