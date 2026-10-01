#!/usr/bin/env python3
"""Independent raw trace reduction. Acquisition validity is separate from timing.

Only uses the declared wire layout and actual exported bytes. Does not call
or reproduce the target fixed-point accumulator to establish release times.
"""
import argparse
import binascii
import json
import math
from pathlib import Path

import r0f_group1_contract as contract
import r0f_successor_emulator as runtime

WIRE = json.loads(contract.PATH.read_text())
C, O, H = (WIRE[key] for key in ("constants", "recordOffsets", "headerOffsets"))
MASK = 0xffffffff


def number(data, offset, size=4):
    return int.from_bytes(data[offset:offset + size], "little")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def span(end, start):
    value = (end - start) & MASK
    require(value < 0x80000000, "ambiguous/reversed clock interval")
    return value


def distribution(values):
    if not values:
        return {"samples": 0, "p95": None, "max": None}
    ordered = sorted(values)
    return {"samples": len(values), "p95": ordered[math.ceil(len(values) * .95) - 1],
            "max": ordered[-1]}


def folded(hash_value, value):
    return (((hash_value << 5) | (hash_value >> 27)) & MASK) ^ value


def golden(ticks):
    """Host integer oracle for the retained instruction fixture, not target calls."""
    table = (3, 7, 2, 11, 5, 13, 1, 9, 4, 15, 6, 12, 8, 14, 10, 0)
    x, y, z = ([i * scale + base for i in range(123)] for scale, base in ((17, 3), (13, 5), (7, 257)))
    command, pending = [0] * 9, [0] * 9
    checkpoints = {}
    for tick in range(1, max(ticks) + 1):
        environment = (tick & 7) + table[tick & 15]
        command = pending[:]
        for stage in range(5, 11):
            for actor in range(9):
                v = (x[actor] + command[actor] + environment + stage) & 65535
                x[actor] = v ^ (y[actor] >> 3)
                y[actor] = (y[actor] + table[v & 15]) & 65535
                z[actor] = 257 + ((z[actor] + actor + stage) & 1023)
        for actor in range(9, 97):
            x[actor] = (x[actor] + table[(actor + tick) & 15]) & 65535
            y[actor] ^= x[actor] >> 2
            z[actor] = 257 + ((z[actor] + 3) & 1023)
        for event in range(64):
            y[event % 9] = (y[event % 9] + 1) & 65535
        for actor in range(113, 123):
            x[actor] = (x[actor] + x[(actor - 113) % 9]) & 65535
            y[actor] ^= tick
        pending = [(x[113 + actor] ^ tick) & 15 for actor in range(9)]
        for actor in range(97, 113):
            x[actor] = (x[actor] + environment + 1) & 65535
        if tick in ticks:
            value = folded(0x0065cf01, tick)
            for actor in range(123):
                for coordinate in (x, y, z):
                    value = folded(value, coordinate[actor])
            for actor in range(9):
                value = folded(folded(value, command[actor]), pending[actor])
            checkpoints[tick] = f"{value:08X}"
    return tuple(checkpoints[tick] for tick in ticks)


def sidecar_golden(ticks):
    full = [[0] * 6 for _ in range(C["SIX_DOF"])]
    reduced = [[0] * 3 for _ in range(C["KINEMATIC"])]
    tracks = [[0] * C["TRACKS_PER_DOMAIN"] for _ in range(C["DOMAINS"])]
    intent, pending, eligible = [0] * 9, [0] * 9, [0] * 9
    runs = [0] * 3
    for tick in range(1, ticks + 1):
        for actor in range(9):
            if eligible[actor] and tick >= eligible[actor]:
                require(tick == eligible[actor], "oracle held-intent causality")
                intent[actor], eligible[actor] = pending[actor], 0
        for actor, axes in enumerate(full):
            for axis in range(6):
                axes[axis] = (axes[axis] + intent[actor] + tick + axis + actor) & 65535
        for actor, axes in enumerate(reduced):
            for axis in range(3):
                axes[axis] = (axes[axis] + intent[actor + 6] + tick + axis) & 65535
        for domain, domain_tracks in enumerate(tracks):
            for track in range(len(domain_tracks)):
                domain_tracks[track] = (tick * (tick + 1) // 2 + tick * (domain * 37 + track + 1)) & 65535
        for tier, cadence in enumerate((2, 5, 10)):
            if tick % cadence == 0:
                runs[tier] += 1
                for actor in range(tier, 9, 3):
                    pending[actor] = tracks[0 if actor < 5 else 1][actor]
                    eligible[actor] = tick + 1
    value = 0x47315731
    for matrix in (full, reduced, tracks):
        for row in matrix:
            for item in row:
                value = folded(value, item)
    for actor in range(9):
        for row in (intent, pending, eligible):
            value = folded(value, row[actor])
    return value, runs


def reduce(trace, saved=None, payload_address=None):
    count = C["EPOCHS"] * C["PHASES"] * C["TICKS_PER_PHASE"]
    result_offset = C["HEADER_BYTES"] + count * C["RECORD_BYTES"]
    world_count = number(trace, H["WORLD_EVENTS"])
    world_offset = result_offset + C["RESULT_BYTES"]
    require(0 < world_count <= C["MAX_WORLD_EVENTS"], "world event capacity")
    require(len(trace) == world_offset + world_count * C["WORLD_EVENT_BYTES"] + 4, "trace length")
    require(trace[:4] == b"G1T2" and number(trace, H["VERSION"], 2) == C["VERSION"], "trace identity")
    require(number(trace, H["RECORDS"]) == count and number(trace, H["RECORD_BYTES"], 2) == C["RECORD_BYTES"], "record shape")
    require(number(trace, H["TRACE_BYTES"]) == len(trace), "declared length")
    require(binascii.crc32(trace[:-4]) & MASK == number(trace, len(trace) - 4), "trace CRC")
    ticks = (count // 2, count)
    result = trace[result_offset:result_offset + C["RESULT_BYTES"]]
    decoded = runtime.validate_success_result(result, ticks, golden(ticks))
    if saved is not None:
        require(payload_address is not None, "missing independently linked payload address")
        require(saved[:2] == payload_address.to_bytes(2, "little")
                and saved[2:] == runtime.expected_save(result)[2:], "actual SAVE")
    sidecar, runs = sidecar_golden(count)
    require(number(trace, H["SIDECAR_HASH"]) == sidecar, "sidecar lineage")
    require(number(trace, H["AI_CAUSALITY_ERRORS"], 2) == 0, "AI next-tick causality")
    require([number(trace, H["AI_RUNS"] + 2 * tier, 2) for tier in range(3)] == runs, "AI due-pattern counts")
    require(list(trace[H["TRACK_HIGH"]:H["TRACK_HIGH"] + 2]) == [24, 24], "domain track occupancy")
    require(trace[H["LIVE_SIX_DOF"]] == 6 and trace[H["LIVE_KINEMATIC"]] == 3, "aircraft fixture classes")
    period = number(trace, H["PERIOD_Q16"])
    require(65536 <= period <= MASK, "period")
    require(trace[H["REFERENCE"]] in (1, 2) and trace[H["BASE_PAGE"]] == 2, "reference/platform")
    read_max = number(trace, H["READ_MAX"])
    require(number(trace, H["READ_MIN"]) <= read_max, "read overhead range")
    require(0 < number(trace, H["HARDWARE_STACK"], 2) < 256
            and 0 < number(trace, H["SOFTWARE_STACK"], 2) < 4096, "stack bounds")
    for field in ("PRE_FRAME_SAMPLES", "POST_FRAME_SAMPLES"):
        require(all(1000 <= number(trace, H[field] + 4 * index) <= 100000 for index in range(16)), "frame calibration")
    raw = [trace[C["HEADER_BYTES"] + index * C["RECORD_BYTES"]:C["HEADER_BYTES"] + (index + 1) * C["RECORD_BYTES"]] for index in range(count)]
    world_events = []
    for index in range(world_count):
        offset = world_offset + index * C["WORLD_EVENT_BYTES"]
        event = {"epoch": trace[offset], "phase": trace[offset + 1],
                 "source": number(trace, offset + 2, 2), "time": number(trace, offset + 4)}
        require(event["epoch"] < C["EPOCHS"] and event["phase"] < C["PHASES"]
                and 0 < event["source"] <= (event["epoch"] + 1) * count // 2, "world event identity")
        if world_events:
            previous = world_events[-1]
            require(previous["epoch"] <= event["epoch"], "world epoch ordering")
            if previous["epoch"] == event["epoch"]:
                span(event["time"], previous["time"])
        world_events.append(event)
    captures = [number(row, O["PREVIOUS_CAPTURE_COUNTS"]) for row in raw[1:]] + [number(trace, H["FINAL_CAPTURE"])]
    require(max(captures) == number(trace, H["CAPTURE_MAX"]), "capture overhead maximum")
    stages = [[] for _ in range(21)]
    durations, publication, lateness, ages = [], [], [], []
    services = [[], [], []]
    epochs = []
    publications = {}
    last_world = 0
    last_publication_count = 0
    for epoch in range(C["EPOCHS"]):
        cohorts = []
        for phase in range(C["PHASES"]):
            first_index = (epoch * C["PHASES"] + phase) * C["TICKS_PER_PHASE"]
            cohort = raw[first_index:first_index + C["TICKS_PER_PHASE"]]
            first_release = number(cohort[0], O["RELEASE"])
            debts, execution, misses, uncertain, dma_jobs = [], [], 0, 0, 0
            for local, row in enumerate(cohort):
                index = first_index + local
                tick = index + 1
                require(number(row, O["TICK"], 2) == tick and row[O["EPOCH"]] == epoch and row[O["PHASE"]] == phase, "record sequence")
                require(row[O["FLAGS"]] == 0, "invalid acquisition flags")
                release, start, published, end = (number(row, O[key]) for key in ("RELEASE", "START", "PUBLICATION", "END"))
                require(release == (first_release + (local * period // 65536)) & MASK, "release drift/skipped tick")
                late = span(start, release)
                duration = span(end, start)
                pub_duration = span(published, start)
                require(pub_duration <= duration, "publication after end")
                stage_values = [number(row, O["STAGE_COUNTS"] + 2 * stage, 2) for stage in range(21)]
                require(sum(stage_values) <= pub_duration, "stage totals exceed publication span")
                for stage, value in enumerate(stage_values):
                    stages[stage].append(value)
                for service in range(3):
                    services[service].append(number(row, O["INPUT_COUNTS"] + 2 * service, 2))
                next_release = first_release + (local + 1) * period // 65536
                budget = (next_release - release) & MASK
                debt = late + duration + captures[index] - budget
                misses += debt > read_max
                uncertain += abs(debt) <= read_max
                debts.append(debt)
                execution.append(duration + captures[index])
                durations.append(duration + captures[index]); publication.append(pub_duration); lateness.append(late)
                dma_jobs += number(row, O["DMA_JOBS"], 2)
                require(1 <= row[O["SNAPSHOT_HIGH"]] <= 3 and row[O["QUEUE_HIGH"]] == 64, "pool high-water")
                require(number(row, O["READING_TICK"], 2) <= tick, "future snapshot read")
                source = number(row, O["WORLD_SOURCE_TICK"], 2)
                generation = number(row, O["WORLD_GENERATION"], 2)
                require(last_world <= generation and source <= tick, "world generation/source")
                require(generation <= world_count, "world generation exceeds event log")
                if generation:
                    event = world_events[generation - 1]
                    require(event["source"] == source and event["time"] == number(row, O["WORLD_SWAP_TIME"]), "world record/event disagreement")
                if generation != last_world:
                    require(source > 0, "world without source snapshot")
                    if world_events[generation - 1]["epoch"] == epoch:
                        span(end, number(row, O["WORLD_SWAP_TIME"]))
                last_world = generation
                published_count = number(row, O["PUBLISHED"], 2)
                require(published_count - last_publication_count in (0, 1), "publication count continuity")
                if published_count != last_publication_count:
                    publications[(epoch, tick)] = published
                last_publication_count = published_count
                if source and (epoch, source) in publications:
                    age = span(end, publications[(epoch, source)])
                    ages.append(age)
                require(published_count <= tick, "publication count")
            # Every overlapping 33-tick execution window; no windows across
            # deliberate phase pauses or the storage clock reset.
            windows = [sum(execution[index:index + 33]) for index in range(len(execution) - 32)]
            window_spans = [span(number(cohort[index + 32], O["END"]), number(cohort[index], O["RELEASE"]))
                            + captures[first_index + index + 32] for index in range(len(execution) - 32)]
            elapsed = span(number(cohort[-1], O["END"]), first_release) + captures[first_index + 99]
            completed = sum(event["epoch"] == epoch and ((event["time"] - first_release) & MASK) <= elapsed for event in world_events)
            nominal_seconds = elapsed * 65536 / period / 100
            cohorts.append({"phase": phase, "ticks": len(cohort), "nominalDeadlineMisses": misses,
                            "boundaryUncertain": uncertain, "maxDebtCounts": max(debts),
                            "rolling33ExecutionCounts": distribution(windows),
                            "rolling33ElapsedCounts": distribution(window_spans),
                            "completeWorlds": completed, "observedNominalSeconds": nominal_seconds,
                            "nominalWorldHz": completed / nominal_seconds,
                            "below20HzFloor": completed / nominal_seconds < 20,
                            "dmaJobs": dma_jobs,
                            "irqAdvances": (number(cohort[-1], O["IRQ_AFTER"], 2) - number(cohort[0], O["IRQ_BEFORE"], 2)) & 65535})
        require(all(row["dmaJobs"] > 0 and row["irqAdvances"] > 0 for row in cohorts), "missing per-cohort IRQ/DMA contention")
        epochs.append({"epoch": epoch, "cohorts": cohorts})
    completion_ages = []
    for index, event in enumerate(world_events):
        source = publications.get((event["epoch"], event["source"]))
        if source is None:
            # A complete pre-storage world may remain displayed after restart;
            # its old CIA epoch cannot provide a cross-storage SI age.
            require(event["epoch"] == 1 and event["source"] <= count // 2, "world uses unpublished snapshot")
            continue
        completion_ages.append(span(event["time"], source))
        if index + 1 < len(world_events) and world_events[index + 1]["epoch"] == event["epoch"]:
            ages.append(span(world_events[index + 1]["time"], source))
    misses = sum(cohort["nominalDeadlineMisses"] for epoch in epochs for cohort in epoch["cohorts"])
    low_cadence = sum(cohort["below20HzFloor"] for epoch in epochs for cohort in epoch["cohorts"])
    uncertain = sum(cohort["boundaryUncertain"] for epoch in epochs for cohort in epoch["cohorts"])
    return {"acquisition": "PASS", "scope": "instrumented bounded combined fixture",
            "nominalDeadlineMisses": misses, "cohortsBelow20Hz": low_cadence,
            "boundaryUncertain": uncertain,
            "nominalTiming": "FAIL" if misses or low_cadence else "INCONCLUSIVE" if uncertain else "WITHIN_OBSERVED_BOUNDS",
            "records": count, "epochs": epochs, "successor": decoded,
            "instrumentedExecutionCounts": distribution(durations),
            "publicationCounts": distribution(publication), "releaseLatenessCounts": distribution(lateness),
            "stages": [distribution(values) for values in stages],
            "services": dict(zip(("input", "audio", "display"), map(distribution, services))),
            "displayedWorldAgeCounts": distribution(ages),
            "worldEventsRetained": world_count,
            "worldCompletionAgeCounts": distribution(completion_ages),
            "captureMaximumCounts": max(captures), "readMaximumCounts": read_max,
            "hardwareStackHighWaterBytes": number(trace, H["HARDWARE_STACK"], 2),
            "softwareStackHighWaterBytes": number(trace, H["SOFTWARE_STACK"], 2),
            "audioServiceGapCounts": number(trace, H["AUDIO_SERVICE_GAP"]),
            "physicalSiUncertainty": "UNRESOLVED; nominal counter ratio only",
            "physical": "NOT RUN", "fullGroup1Acceptance": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path)
    parser.add_argument("--saved", type=Path)
    parser.add_argument("--payload-address", type=lambda value: int(value, 0))
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    report = reduce(args.trace.read_bytes(), args.saved.read_bytes() if args.saved else None, args.payload_address)
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    print("Group 1 acquisition/reduction PASS; nominal timing observations retained separately")
