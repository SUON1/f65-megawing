# Group 1 display-throughput recovery — 2026-09-30

The isolated owner-observation candidate now passes memory fit, host checks
and fresh focused NTSC/PAL timing. A new local carrier passes all four clean
exact-name NTSC/PAL boots. No SD write, physical run, commit, push or acceptance
promotion.

## Authority and correction

The approved [Group 1 Build Intent](../plans/R0-F_GROUP1_BUILD_INTENT.md),
[measurement protocol](../plans/R0-F_GROUP1_MEASUREMENT_MATRIX.md), private
presentation version 3, pool version 2 and trace version 6 govern. The
unchanged 100 Hz/21-stage workload, 20 Hz floor, first resumed cohort,
capacities, memory envelopes and all integrity checks remain controlling.

The retained `ee3b59a1...` acquisition was valid but resumed phase 0 measured
19.0756 Hz. A busy view change coincided with an approximately 100 ms gap;
the first resumed world was prompt. The evidence supported insufficient
display/cancellation headroom, not another pre-acquisition stall.

The exact old display function, compiled with mocked hardware edges, confirms
two avoidable owner-path issues:

- After the ninth successful scene copy, readiness required another
  completion-only service quantum. The correction verifies the held snapshot
  CRC and matching registration immediately after that synchronous copy.
  Publication still waits for a subsequent observed frame boundary.
- A swap changed `display_front` but the next clear used the destination
  calculated before that swap. The correction switches that destination to
  the current backbuffer, avoiding a clear of the just-published front store.

These corrections alone improve total world count but do not close resumed
phase 0. The second isolated variant replaces only the three display-owner
CRC calls on ordinary RAM buffers with the already-qualified compact
CRC32/ISO-HDLC implementation. Volatile register/low-memory checks retain
their existing path. No CRC comparison, nine-copy workload, 15-clear
workload, snapshot hold or superseded-view cancellation is removed.

## Preserved trials and target fit

| Candidate | Resident free bytes | Focused NTSC | Execution max CIA counts |
| --- | ---: | --- | ---: |
| Retained owner recovery `ee3b59a1...` | 66 | FAIL: resumed phase 0, 19.0756 Hz | 8128 |
| Completion/backbuffer correction `941fac20...` | 80 | FAIL: resumed phase 0, 19.0738 Hz | 8033 |
| RAM-CRC correction `523d0369...` | 37 | PASS: minimum cohort 28.1116 Hz | 7328 |

The first compile-only spelling of the completion correction added 223 bytes
and failed fit by 157 bytes. It remains retained with its full source
checkpoint and was never executed. Equivalent simpler control flow saves
14 bytes versus the predecessor and passes fit. Its first host-controller
attempt failed because the baseline binary path collided with an include
directory; the corrected exclusive rerun passes. This host-tool failure is
not a target result.

Qualified PRG:
`build/r0f/group1/display-recovery/ram-crc-02/runtime-01/GROUP1.prg`.
SHA-256: `523d0369f88957b4bdf33cd15441954ebdf033685e097513411456791634f65d`.
37483 bytes; resident end exclusive `$BFDB`; 37 bytes remain before `$C000`.
Protected resident section remains `$2017-$30B1`, 4250 bytes. Text 32668,
constant data 518, initialized data 23, BSS 3405 and noinit 36 bytes. No
software-stack, physical-memory, resource-reserve or measured-reserve borrowing.
All generated contracts and bindings remain unchanged.

## Validation

The actual display function passes host ASan/UBSan checks for both buffers,
frame-gated publication, all 26 unfinished/ready cancellation boundaries,
final-copy failure/retry, synchronous-DMA failure/retry and snapshot corruption.
The retained old function reproduces both issues independently of the fix.
The full owner suite still passes workload/AI lineage, 3200 independent scene
byte comparisons, 65536 generation equivalence cases, 248832 observer-state
equivalence cases, exact mocked audio/export owner checks, CRC boundary
coverage, 83 synthetic codec rejects and generated-contract checks. The
repository suite passes 43 tests, including new fail-closed carrier admission.

| Fresh focused run | Export | Worlds | Minimum cohort Hz | Execution max/p95 | HW/SW stack bytes |
| --- | --- | ---: | ---: | --- | --- |
| NTSC | 19 closed chunks, 310580 trace bytes | 955 | 28.1116 | 7328 / 6784 | 67 / 124 |
| PAL | 19 closed chunks, 308212 trace bytes | 807 | 23.1109 | 7264 / 6528 | 62 / 124 |

Both runs retain all 3200 records, actual SAVE, independently extracted
version-6 traces, both phase masks `FFFF` and order masks `3F`, zero nominal
deadline misses, zero uncertain boundaries and zero below-20-Hz cohorts.
NTSC resumed phase 0 rises to 28 worlds in 0.99524 nominal seconds, 28.1339 Hz.
Each actual trace rejects all 102 raw/repaired-CRC corruption cases. Actual
owner observations continue across storage; this does not claim unexercised
four-channel PCM contention or production pool sizing.

Exact commands are retained in build/host/execution/reducer JSON and logs.
Main invocations from the repository root:

```sh
python3 -B tools/diagnostics/r0f_group1_display_recovery.py build --label runtime-02
python3 -B tools/diagnostics/r0f_group1_display_recovery.py host --label host-02
python3 -B tools/diagnostics/r0f_group1_display_recovery.py qualify
python3 -B tools/diagnostics/r0f_group1_display_recovery.py ntsc
python3 -B tools/diagnostics/r0f_group1_display_recovery.py negative-ntsc
python3 -B tools/diagnostics/r0f_group1_display_recovery.py build --variant ram-crc-02 --label runtime-01
python3 -B tools/diagnostics/r0f_group1_display_recovery.py host --variant ram-crc-02 --label host-01
python3 -B tools/diagnostics/r0f_group1_display_recovery.py qualify --variant ram-crc-02 --build-label runtime-01 --host-label host-01
python3 -B tools/diagnostics/r0f_group1_display_recovery.py ntsc --variant ram-crc-02
python3 -B tools/diagnostics/r0f_group1_display_recovery.py negative-ntsc --variant ram-crc-02
python3 -B tools/diagnostics/r0f_group1_display_recovery.py pal --variant ram-crc-02
python3 -B tools/diagnostics/r0f_group1_display_recovery.py negative-pal --variant ram-crc-02
python3 -B -m unittest discover -s tools/diagnostics -p 'test_r0f_group1_*.py' -v
```

## Hardware and remaining boundary

Ordinary compiler-managed C clobbers; no added assembly, IRQ/NMI, MAP or
base-page operation. Existing `$D7FA` frame reads and `$D060-$D062` publication
remain owner-controlled. The two existing physical stores `$020000-$03FFFF`
and staging/DMA ownership remain unchanged. Each service call still makes at
most one bounded DMA/copy job; the last-copy completion work is measured.
Original returning storage, immutable terminal capsule and no-return export
lifetimes remain unchanged.

37 free resident bytes is a real constraint, not comfortable expansion room.
The integrated near-capacity trace case and compact operator summary remain
open. Sampled phases do not prove every relative phase combination; Xemu's
zero-resolution IRQ-body intervals do not establish whole-ISR cost or entry
latency. Physical SI uncertainty, real scanout/PCM and physical carrier/runtime
evidence remain unestablished. No hardware-ready or full Group 1 claim follows.

## New local carrier and freeze

`build/r0f/group1/carriers/R0FG1P03/canonical/R0FG1P03.D81` is 819200 bytes,
SHA-256 `d1f60b4b56c9eff5b2e1b7d216794789d4817730e411f37af64e5897576194ef`.
It was fresh-formatted and populated in one pinned construction session,
independently extracted and checked, then made read-only. The canonical was
never mounted writable. All four clean exact-name copies pass actual SAVE,
version-6 export/reduction, nominal timing and 102 corruption rejects; both
NTSC copies retain 955 worlds, both PAL copies 807. Each copy's post-run
mutation remains separate. Canonical state is **XEMU_BOOT_VERIFIED only**.
SD byte/allocation/chooser, physical runtime and test eligibility are NOT RUN.

```sh
python3 -B tools/diagnostics/r0f_group1_owner_carrier.py build --name R0FG1P03.D81 --experiment /Users/slice/Developer/f65-megawing/build/r0f/group1/display-recovery/ram-crc-02
python3 -B tools/diagnostics/r0f_group1_owner_carrier.py boot --name R0FG1P03.D81 --mode 1 --number 1
python3 -B tools/diagnostics/r0f_group1_owner_carrier.py boot --name R0FG1P03.D81 --mode 1 --number 2
python3 -B tools/diagnostics/r0f_group1_owner_carrier.py boot --name R0FG1P03.D81 --mode 0 --number 1
python3 -B tools/diagnostics/r0f_group1_owner_carrier.py boot --name R0FG1P03.D81 --mode 0 --number 2
python3 -B tools/diagnostics/r0f_group1_owner_carrier.py finish --name R0FG1P03.D81
python3 -B tools/diagnostics/r0f_group1_display_closeout.py
```

The context-bound carrier adapter reuses the pinned constructor, loader,
structure/extraction checks, independent snapshot reducer and existing
carrier identity/four-boot finishing gates. It leaves the original version-5
carrier tools/inputs untouched. The new carrier pins 133 source/controller
inputs; the previous passing build's 93 and `R0FG1P02`'s 95 inputs are checked
unchanged. Original `ec259fc7...`, later passing/failed PRGs and prior carriers
remain retained. Separate freeze:
[`2026-09-30-display-recovery`](../evidence/r0f/group1/2026-09-30-display-recovery/validation.json).
It includes both timing experiments, compile-only rejection, host evidence,
actual traces/SAVEs and all four carrier copies; multi-gigabyte disposable SD
fixtures stay in build with their execution hashes. Ten previous freezes,
4498 files, are reaudited before copying; no historical evidence is rewritten.

Next close the integrated near-capacity trace and compact operator summary
under the same fit/host-first discipline. Hardware is not yet proposed.
