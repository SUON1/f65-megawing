# Group 1 service-phase diagnostic — 2026-09-30

Declared NTSC/PAL sampled service-phase/order coverage now passes complete local
export and reduction. The pre-acquisition stall is traced
and corrected. The first corrected six-order NTSC run was interrupted during
export at 60 seconds; a fresh run of the unchanged PRG with a 120-second
allowance completed. No candidate carrier, SD copy, or physical test resulted.

## Authority and intended observation

The approved [Group 1 Build Intent](../plans/R0-F_GROUP1_BUILD_INTENT.md),
[measurement matrix](../plans/R0-F_GROUP1_MEASUREMENT_MATRIX.md), Main Concept
v1.6 §§4.6 and 17.5–17.7, and successor admission row 93 govern. Sixteen
initial release offsets and rolling windows already pass locally. This work
tried to record input, audio, and display starts in sixteen nominal-period
bins before each release, in both storage epochs, and to exercise six service
orders. The masks would show sampled coverage only, not every legal relative
phase or external input/audio latency. No per-service budget, maximum world
age, or new product pass threshold was introduced.

## What happened

- The private version-4 trace/header, pure phase-bin arithmetic, generated
  layout and host boundary cases passed. The six-order target fit the
  unchanged resident envelope, with 562 bytes free.
- Fresh NTSC development runs reached tick 3200, but fault 107 blocked
  terminal export because the private IRQ interval probe flagged an invalid
  interval. Diagnostic code distinguished this from its bounded CIA-reader
  exhaustion: the later first-error code was 3, meaning a computed positive
  body interval above 65535 counts. The collected all-bin/order masks belong
  to failed acquisitions and were **not** promoted to coverage evidence.
- A narrower fixed-order phase-bin binary fit with 815 bytes free, but fresh
  NTSC runs timed out at 180 and 360 seconds before the first Group 1 record.
  They had no target fault or IRQ probe error. The screen retained a prior
  ROM-verification message; advancing IRQ counts show that screen alone does
  not locate the stall. No deadline or post-storage result was obtained.
- The earlier validated `ec259fc7...` PRG, run in a new disposable image on
  the same host, completed ticks 1600 to 3200 with fault 00 at the original
  180-second limit. Its result and CRC passed the independent host validator.
  The new binary therefore regressed. The control did not constitute a new
  carrier gate.

## Exact stall trace and correction

The retained fixed-order PRG `f5963ae5...` was traced without rebuilding it
through pinned Xemu's serial monitor. During the zero-epoch pre-calibration
IRQ, the relaxed `BEQ16` at `$3298` (`F3 86 00`) landed at `$3320`, one byte
before its intended `RTS` at `$3321`. The byte at `$3320` was the `$B0` high
address operand of the preceding store; with carry set it decoded as
`BCS +$60`, reached a `BRK` at `$3384`, and recursively entered the IRQ. That
prevented `cfcalibrate(0)` from returning. The nearby operand changes with BSS
placement, which explains why added checkpoints made the failure disappear.

This repository already records the pinned assembler's one-byte-early relaxed
16-bit branch defect in the RH001 wrapper. The Group 1 correction likewise
uses a short in-range inverse condition and immediate inactive-path `RTS`, and
the Group 1 static validator now rejects every 16-bit branch opcode inside the
IRQ probe. The normal corrected build differs from preserved `ec259fc7...` in
exactly three bytes: `F3 86 00` became `D0 01 60`.

For a layout-neutral proof, those same three bytes were changed in a copy of
the exact failing PRG. Corrected SHA-256
`cca0ecb91a2d5378333482ebf706b16b9d513eb01953511119b96298d178460a`
completed all 3200 records and 20-chunk export in under one minute with status
4, error/fault zero. Independent extraction, BAM/chain checking, actual SAVE
validation and a fixed-order version-4 reduction passed. All six phase masks
were `FFFF`; service-order masks remained `00` by construction, so six-order
coverage is not claimed. See
[`2026-09-30-preacquisition-long-branch`](../evidence/r0f/group1/2026-09-30-preacquisition-long-branch/README.md).

[The retained failure evidence](../evidence/r0f/group1/2026-09-30-service-order-irq-failure/README.md)
includes exact PRGs, development D81s, logs, screenshots, memory/results,
build-input hashes and the last six-order source. Its manifest records what
was frozen and the fixed-order source-freeze limitation. The first sandboxed
Xemu attempt failed before program execution and is kept separately in that
same evidence set.

## Focused six-order NTSC continuation

Owner then requested a rebuild from the corrected baseline and one focused
NTSC acquisition. The retained phase/service-order C and version-4 private
contract were reapplied while retaining the short IRQ branch. The static gate
still rejects long branches, and the reducer now requires every one of the
sixteen phase-bin bits rather than merely nonzero masks. Target SHA-256 is
`c249f4e4da972cdc0c5d0958a1a3a148387eb1ad4de602404c6b79fb7c79492b`,
37191 bytes, resident end `$BD98`, 616 bytes free within the unchanged envelope.

The single fresh NTSC direct-PRG run used `--timeout-seconds 60`. At termination
it had all 3200 records, target fault 0, IRQ error 0, all six phase masks `FFFF`
and both order masks `3F`. The earlier stall and IRQ-interval failure did not
recur in this acquisition. However, export was still status 3 with four closed
chunks, no error and open `G1T04`; the time limit interrupted transport.
Independent success-result and actual 34-byte SAVE checks passed, and the first
exported header equals frozen target state. The complete-image validator rejects
the open file, and the partial trace reducer rejects its length. No full CRC,
deadline, cadence or six-order coverage PASS follows from this incomplete run.
IRQ samples 916/912 again contain zero nonzero intervals, retaining the known
Xemu resolution boundary. See the
[frozen focused-run evidence](../evidence/r0f/group1/2026-09-30-six-order-corrected-ntsc/README.md).

Host sanitizers, phase/wrap cases, one million release comparisons, target
compile/link/static boundaries, seven contract tests and host lineage checks
pass. The IRQ guard rejects an injected long branch. A clearly synthetic
HOST-only fixture rejects 22 repaired/truncated corruption cases, including an
incomplete phase mask and missing order bits in either epoch. Ordinary successor
regressions pass with its original exact SHA. The evidence's `validation.json`
records commands and the incomplete run separately.

## Complete unchanged-PRG NTSC export

The owner authorized a fresh 120-second NTSC fixture using the same exact
`c249f4e4...` PRG. Before execution, the prior 108-file evidence manifest,
PRG/symbol identity and all 79 retained source/tooling inputs matched. No
rebuild, target-source or generated-contract change occurred. The interrupted
image was preserved and not reused.

The fresh run completed export status 4, error 0 and 20 closed chunks. All
315780 trace bytes and 3200 records passed independent pinned-tool extraction,
D81 structure/BAM/chain checking, actual SAVE, full CRC and reduction. Both
epochs have service-start phase masks `FFFF` and order masks `3F`. Nominal
timing is `WITHIN_OBSERVED_BOUNDS`: zero deadline misses, zero uncertain cases
and no cohort below the existing 20 Hz floor; 976 complete-world events were
retained. The complete actual trace also rejected all 22 corruption cases.
Result fault is 0, ticks are 1600/3200, lineage is `6B765FDB`/`607348BD`, and
result CRC is `18D750C5`. The raw trace SHA-256 is
`cf54688d281d058e25b4fc73778d39b20d28319e1c446b9b6f272b4ac90503e7`.
See the [complete NTSC evidence](../evidence/r0f/group1/2026-09-30-six-order-ntsc-120s/README.md)
for exact commands, execution, artifacts and manifest.

This closes the incomplete NTSC export result at the declared sampled scope.
PAL remains unrun, and aggregate masks do not prove every relative phase
combination or external input/audio latency. IRQ samples 912/919 still contain
no nonzero body-read interval; pinned-Xemu resolution, whole-ISR cost, entry
latency and physical SI uncertainty remain unresolved.

## Complete unchanged-PRG PAL export

Continuation used one fresh PAL fixture with a 120-second allowance and the
same `c249f4e4...` PRG. The preceding 169 frozen evidence files, all 79 active
source/tooling inputs and PRG/symbol identity matched before execution. No
rebuild or target/generated-contract change occurred.

Export completed with status 4, error 0 and 20 closed chunks. Independent
extraction, D81 structure/BAM/chains, actual SAVE, full CRC and reduction pass
for 314620 bytes and all 3200 ticks. Both epochs have phase masks `FFFF` and
order masks `3F`. Nominal timing is `WITHIN_OBSERVED_BOUNDS`, with zero misses,
zero uncertain cases and no cohort below 20 Hz. All 22 corruption cases reject
against the complete actual trace. There are 831 world events, fault 0,
ticks 1600/3200, lineage `6B765FDB`/`607348BD` and result CRC `435801C3`.
Trace SHA-256 is
`7f032d917a3202f89523e02a8c2deafae8b09e707878bc5b770958866bf452a1`.
See the [complete PAL evidence](../evidence/r0f/group1/2026-09-30-six-order-pal-120s/README.md).

Declared aggregate sampled coverage is now established locally in both modes.
IRQ samples 782/786 still have no nonzero body-read interval, retaining the
same emulator resolution/whole-ISR/entry-latency boundary. Neither this run
nor the preceding NTSC run is an exact-name release-carrier boot or physical
acceptance proof.

## Preserved corrected baseline and validation

The passing Group 1 control remains preserved as
`ec259fc7611d8bb5809d15f6c333f5b224df4c945a8e9ffca5b2402d8444cb30`:
36,473 bytes, resident end `$BAAB`, 1,365 bytes free, private trace version 3.
The corrected normal baseline is the same size and differs only at the three
branch bytes above; its SHA-256 is
`0d96a1b21eb36680b05689b659ac8c6f73cc2b61e647c060ab2f369c2bbfc244`.
The ordinary successor PRG remains byte-identical to
`cf605bd377ddcee2c72cdc4abfd20c3ae9eee350b7b78b36cbde8ff1adf8fc23`.
The development runner now accepts a bounded `--timeout-seconds` override;
its default remains 180 seconds. It changes no target bytes or carrier gate.

The preceding correction checkpoint ran the following commands from the
repository root before the six-order source was reapplied:

- `python3 -B tools/diagnostics/r0f_group1_integration.py` — PASS; exact
  corrected target SHA, IRQ/static boundaries and no long branch in the IRQ
  probe.
- `python3 -B tools/diagnostics/r0f_group1_host_validate.py` — PASS;
  3200-stage/input/held-intent and 1025 CRC-length checks.
- `python3 -B tools/diagnostics/r0f_group1_build.py` — PASS; host sanitizers,
  one million release comparisons and pinned target-object compilation.
- `python3 -B -m unittest discover -s tools/diagnostics -p test_r0f_group1_contract.py -v`
  — seven tests PASS.
- `python3 -B tools/diagnostics/test_r0f_group1_reduce.py build/r0f/group1/integration/irq-ntsc-07/trace.bin`
  — eighteen repaired/truncated corruption cases rejected.
- `python3 -B tools/diagnostics/r0f_successor_integration.py build` — PASS;
  ordinary PRG SHA above.
- `git diff --check`, scoped Python AST/JSON parsing and retained evidence
  manifest hash checks — PASS.

The preserved passing PRG has earlier NTSC/PAL 3200-tick actual trace/SAVE
evidence in [the IRQ/space checkpoint](R0-F_GROUP1_IRQ_SPACE.md). This
diagnostic did not repeat PAL, exact-name carrier boots, SD/physical execution,
or SI calibration. It did not resolve the previous zero-resolution Xemu IRQ
body intervals, whole-ISR cost, or entry latency.

## Hardware and next action

The reapplied phase code uses only existing CIA1 coherent reads, service
owners and resident header bytes; its instrumentation cost remains included
in target deadlines. The retained branch correction changes only the private
Group 1 zero-epoch IRQ fast-path branch encoding; it changes no register or
clobber ownership, CPU-visible or physical-memory allocation, MAP/base-page,
DMA or NMI behavior. Acquisition instrumentation remains timed as before. No
reserve or physical allocation changed.

The unchanged six-order PRG now passes complete local pre/post-storage export
and reduction in NTSC and PAL, with unresolved timer resolution reported
honestly. Do not reuse or alter the interrupted NTSC image.
View/registration/occlusion/LOD and applicable pool evidence remain open, as
do the integrated near-capacity trace, compact operator summary and exact-name
carrier gates. No Group 1 or R0-F acceptance claim follows from this attempt.
