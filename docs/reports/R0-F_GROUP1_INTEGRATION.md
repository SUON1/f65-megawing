# Group 1 workload and timing integration — 2026-09-29

The workload/timing recorder is integrated and locally validated through the
post-storage interval. This is a bounded Group 1 checkpoint, not a hardware-ready
disk or full Group 1/R0-F completion. The original dirty tree and CAP14 evidence
were preserved; no SD writes, commits or pushes occurred.

## Implementation and protocol

[The measurement matrix](../plans/R0-F_GROUP1_MEASUREMENT_MATRIX.md) records
governing requirements, exact cases, nominal thresholds, measurement boundaries
and remaining coverage. One model advances through 3200 ticks and a returning
storage transition at tick 1600. Every tick retains 21 stage durations;
release/start/publication/end timestamps; service, IRQ/DMA and snapshot/world
observations; and capture overhead. Independent reduction checks the fractional
release schedule, including the first resumed tick, and overlapping 33-tick
windows within each declared phase cohort.

The workload adds bounded six-full-shape/three-reduced-shape aircraft work,
two independent 24-track domains and next-tick held intentions to the retained
combined fixture. These are R0 instruction/data fixtures, not production
physics, sensor tables or AI doctrine. Diagnostic due patterns do not freeze
production cadences.

New `group1_capture`, `group1_workload` and `group1_transport` modules separate
measurement/encoding, workload and bounded physical transport. The generated
trace contract owns offsets and capacities. Existing model/platform/lifecycle
files contain opt-in integration hooks; the ordinary predecessor variant is
unchanged at binary level. Builder configuration is passed explicitly, and
the probe and integrated builds share the target compiler/static-check path.

## Results

The same final 37,394-byte PRG passed development Xemu acquisition/reduction in
NTSC and PAL. Each produced 3200 records with zero nominal deadline misses,
zero uncertain deadline boundaries and no measured cohort below 20 Hz.
Nominal complete-world cadence was 29.06–30.12 Hz in NTSC and 24.11–25.12 Hz in
PAL. Actual SAVE bytes, deterministic model lineage, sidecar state and all
976/831 world-swap events passed independent Python checks.

The first run exposed 32 nominal misses. Its bit-at-a-time capture CRC cost
reached 2273 CIA counts. A generated 1024-byte lookup table reduced the final
observed maximum to 673 counts in NTSC and 705 in PAL, with independent
streaming CRC equivalence tests. Thresholds and workload counts were unchanged.
Version 2 also adds a bounded event log after finding that two world swaps can
occur between tick records at a phase boundary; no event is silently discarded.
All failed/superseded development directories remain intact.

The retained ordinary predecessor PRG still has SHA-256
`cf605bd377ddcee2c72cdc4abfd20c3ae9eee350b7b78b36cbde8ff1adf8fc23`.
The final integrated PRG is
`bd6f75d4eb5829d76640bf81ed307cf55b64b00db950a6a822dce981ef93c516`.
Complete evidence and frozen source inputs are in
[the evidence checkpoint](../evidence/r0f/group1/2026-09-29-workload-timing/README.md).

## Validation commands and outcomes

- `python3 -B tools/diagnostics/r0f_group1_host_validate.py` — PASS under
  ASan/UBSan: 3200 stage/input/held-intent cases, independent model and sidecar
  lineage, 1025 streaming CRC lengths. Checkpoints are `6B765FDB` at tick 1600,
  `607348BD` at 3200; sidecar hash `71A7DF9E`.
- `python3 -B tools/diagnostics/r0f_group1_build.py` — PASS: pure timing/export
  tests, one million release comparisons and pinned target-object builds.
- `python3 -B -m unittest discover -s tools/diagnostics -p test_r0f_group1_contract.py -v`
  — five tests PASS for wire geometry, capacity and field overlaps.
- `python3 -B -m unittest discover -s tools/diagnostics -p test_r0f_group1_export_admission.py -v`
  — eight lifetime/ownership/geometry tests PASS.
- `python3 -B tools/diagnostics/r0f_successor_integration.py build` — PASS:
  predecessor host/Java, IRQ, capture, CF001/RH001 and target/static regressions.
  Its source-pattern check was updated to follow the explicit retained tick-count
  alias; it still checks the same post-storage IRQ observation ordering.
- `python3 -B tools/diagnostics/r0f_group1_integration.py` — PASS: generated
  contract, pinned target link, map, pre-C order, protected/staging bounds,
  terminal no-return and ROM-call allowlist checks.
- `python3 -B tools/diagnostics/r0f_group1_run.py --out build/r0f/group1/integration/ntsc-04 --mode 1`
  and the corresponding `pal-02 --mode 0` command — PASS. Fresh disposable
  images, pinned Xemu/ROM, actual 20-file export extraction, independent
  structure/BAM/content validation, result/SAVE/trace reduction. Direct PRG
  execution only; these are not exact-carrier gate results.
- `python3 -B tools/diagnostics/test_r0f_group1_reduce.py build/r0f/group1/integration/ntsc-04/trace.bin`
  and the PAL equivalent — fifteen corruption cases rejected, including
  repaired outer CRCs with semantically impossible evidence.
- `python3 -B tools/diagnostics/r0a_validate.py .`, scoped Python/JSON parsing
  and `git diff --check` — PASS. Pre-existing retained evidence hashes match.

## Hardware and fit

CIA reads, clock restart, IRQ ownership, synchronous DMA and original storage
restoration retain their admitted wrappers. No new MAP operation, IRQ/NMI
handler or physical allocation was introduced. All new state is either linked
resident data or inside the previously admitted trace range. Reserve use is
zero. Generated trace/CRC bindings are current.

The final resident end is `$BE29`, leaving **471 bytes** below `$C000`.
Protected export code/data remains below `$4000`. Exercised stack high-water
was 72 hardware bytes and 88 software bytes in both final runs. These values
describe the exercised path, not universal maxima. Further instrumentation
must recover resident space within the contract or receive a separate admission;
it cannot silently borrow reserves or extend into the software stack.

## Remaining Group 1 work

Before calling Group 1 hardware-ready: recover space for remaining IRQ-body/
latency and independent-service phase measurements; complete the declared
view/registration/occlusion/LOD and applicable pool observations; qualify
integrated capsule/NMI/full-capacity negatives; provide the compact operator
summary; and run the fresh exact-name carrier gates. The matrix explicitly
marks these open rows. Physical SI uncertainty also remains unresolved.
Groups 2 and 3, physical tests and named owner acceptance remain separate.
