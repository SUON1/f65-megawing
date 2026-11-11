# M2 Platform clock continuity — host checkpoint

**READY FOR REVIEW.** PC-D1–PC-D6 preflight passed for the bounded host-only
increment. The private Platform correction and 11 focused C host checks passed,
with address and undefined-behavior sanitizers. No target compiler, target linker
or runtime was invoked. This is not changed-image clock, timing or fit admission.

## Identity and scope

- Branch: `codex/65aero-m2-platform-clock`.
- Base: `5c78bf7d00aadda0e63ce800e27fe3e142c651c0`; fetched main remains
  `9570f0ab427121a4e8f042041a14c89aaaeff9e2`.
- Authority: founder approval of PC-D1–PC-D6 in the unchanged
  [intent snapshot](../plans/65AERO_M2_PLATFORM_CLOCK_CONTINUITY_INTENT.md).
- Candidate analysis identity: `65AERO-M2-PLATFORM-CLOCK-1`, not an adopted
  generated runtime profile. PR #34 and the planning checkout are unchanged.
- Evidence: [packet](../evidence/flight-demo/2026-11-11-m2-platform-clock/),
  [preflight](../evidence/flight-demo/2026-11-11-m2-platform-clock/preflight.json),
  [host result](../evidence/flight-demo/2026-11-11-m2-platform-clock/host-result.json).

The only modified existing implementation is
`src/platform/m1/m1_platform.c`. It uses the new private
`src/platform/m1/clock_private.h` for calibration and runtime reads and includes
its sticky fault in the existing Platform fault interface. No other owner gains
access to its state. The raw CF001 sampler, timer setup, public declarations,
generated interfaces, renderer, scheduler, guard and historical checks are unchanged.

## Correction

The converter decodes successful countdown pairs with periods of 65,535, computes
phase modulo 4,294,836,225, and accumulates elapsed counts modulo 2^32. It uses
32-bit shifts/addition/subtraction only: no division, 64-bit arithmetic, new MMIO
or math-register access. The first successful sample establishes zero elapsed.
Calibration and subsequent reads use this same accumulated domain.

The retained upper-timer witness moves from raw `0xfffefffe` to `0x0000001f`.
Its corrected elapsed delta is **32**, compared with the old binary difference
of **65,569**. Independent countdown-event fixtures cover repeated hardware
periods and independent uint32 output rollover, not just that one witness.

Zero A/B counters, sampler/NMI faults, use before initialization and observed
deltas at or above 2^31 latch failure. Subsequent calls retain the last valid
elapsed count until reset-only Platform initialization. Failed initialization
leaves period zero and the clock fault latched. There is no tick/frame reset,
new IRQ timekeeper, callback, reentrancy or heap allocation.

A completely missed hardware period remains undetectable from A/B alone. The
host suite explicitly demonstrates this alias; it does not call it a detectable
fault. The observation-gap obligation is mandatory.

## Preflight and observation-gap boundary

The preflight inspected the exact preserved executable, all 81 target source and
generated inputs and eight pinned emulator reference files at
`40dfef0d1d5f56be2469492715c12bdb32c75b67`. Its PRG SHA-256 is
`7fdcea61387c0e6b7ae92310725966ac6c0e29e82e8ba1c9a6be77335af76aad`.
The checker reads the unchanged published baseline explicitly; it does not make
the old checker accept the modified adapter.

The actual eight-read sampler window costs 55 pinned instruction cycles. A
conservative 105-cycle raster interrupt still leaves it below the shortest
1,287-cycle scanline. At most one 32-count CIA update can occur in that window.
All 65,535 positive A values, B byte-borrow/reload equivalence classes and all nine
update positions were checked: **4,128,705 cases**, comprising 4,012,577 coherent
acceptances and 116,128 rejections. The C host suite also compiles the exact
unchanged sampler text and checks torn reads, the top-sixteen exclusion and
success/failure at the 32-attempt boundary.

The coarse caller proof includes all positive service grants, not the current
zero grants. It forms control-flow components from the exact linked instructions,
checks cycle coverage, and charges bounded loop visits plus complete callees.
Mutually exclusive paths inside cyclic components are conservatively summed.
The detailed function bounds and feedback addresses are in the preflight JSON.

| Caller interval | Conservative old-image CPU cycles |
| --- | ---: |
| Entire bounded calibration, including all polling | 4,076,303,585 |
| Calibration through display/core/camera/renderer initialization | 4,295,191,412 |
| Renderer dispatch interval, including guard and clock calls | 26,920,964,465 |
| Previously proved ordered tick iteration | 39,126 |

These deliberately loose bounds answer the half-range question only. They are
not service grants, useful frame estimates or new tick measurements.

The principal finite-work witnesses are:

- Calibration: at most 4,000,001 condition visits, 17 successful samples and one
  bounded ratio calculation; reset/ROM work occurs before clock start.
- Initialization: each store has 32 screen batches of at most 32 cells and 961
  64-byte tile writes; two stores, 32 color copies and four palette entries.
  Copy operations have checked finite sizes; no initialization wait is unbounded.
- Dispatch: each continuation spends positive credit from a uint16 grant before
  work. There are at most 65,535 continuations per call. BEGIN and COMMIT are
  separate bounded calls. Fault/cancellation or reaching COMMIT ends the batch.
- Text: within one batch, monotonic tile indices 640–959 allow at most eight row
  constructions. Their full conservative costs are charged separately, rather
  than incorrectly repeating an entire row on every continuation.
- Geometry/arithmetic: one bounded command or limb unit per continuation; byte
  loops, normalization, SDK shifts/division, timeout polling, copy and raster
  loops have source/operand caps. The text descriptor, glyph and registration
  loops are included. No suspended division is treated as already completed.
- Main-loop due-release bookkeeping, guard, return paths and clock sampling are
  included. The existing single-producer tick proof is reused only for its exact
  old source/image. No complete-frame scheduling claim is inferred from it.

For the pinned emulator, the envelope allows one raster interrupt per scanline
(more than its actual one per frame), a pending interrupt, partial scanlines and
both sample endpoints' staleness. No concurrent DMA or second timer owner is
introduced. An NMI becomes a sticky sampled fault in this candidate, so a pair
of successful samples cannot span a continuing NMI-fault path. Terminal paths
do not resume the clock. Host pauses do not advance this CPU/CIA count model.

The resulting **old caller** gap is at most **728,824,896 native counts**, below
the strict **2,147,483,648** limit by **1,418,658,752**. This establishes the finite
caller prerequisite for the host-only correction without a run-duration cap.
The new converter adds straight-line scalar work, bounded raw sampling and
fault checks. Its generated code cost is **UNMEASURED**. An eventual changed
image must re-establish the gap including that cost, startup, stack, IRQ and
deadline effects; the old envelope is not transferred as an executable grant.
Physical CIA semantics and physical wait-state timing are outside this evidence.

## Host checks and accounting

`python3 -B tests/flight_demo/m2_rebuild/test_platform_clock.py` returned 0:
**11/11 PASS**, using Apple clang 21.0.0, C11, `-O1 -Wall -Wextra -Werror
-pedantic -fsanitize=address,undefined -fno-omit-frame-pointer`.
The host suite includes:

- Countdown-event arithmetic oracle, duplicates, A/B reloads, the published
  witness, repeated periods, uint32 rollover and below/at/above half-range edges.
- Real adapter with host fakes: PAL/NTSC calibration crossing the upper reload,
  shared units, invalid samples, polling exhaustion, frame jumps, physical-mode
  refusal, sampler/NMI faults before and during reads, sticky failure and reset.
- Exact raw sampler extraction, independent torn-read expectations and attempt
  exhaustion; the real guard and release/carry expressions extracted unchanged
  from the composition root, including strict equality and wrap behavior.

Private state is **10 logical bytes**: two uint32 fields and two byte flags.
The host ABI occupies **12 bytes** including padding. Target padding, code,
constants, compiler scratch, hardware/software stack and call costs are
**UNMEASURED**, not zero. The helper has no internal loop, recursion or dynamic
storage. Each raw sample remains bounded by 32 attempts of eight reads.

All host binaries, inputs, compiler arguments, stdout/stderr and test outcomes
were produced in a new temporary directory and retained in
[host-evidence.tar.gz](../evidence/flight-demo/2026-11-11-m2-platform-clock/host-evidence.tar.gz),
SHA-256 `4b57976560a6830073e9b31c92873b2ae1d6dac815ddbb249c25400a67c5f215`.
Both the `/usr/bin/clang` launcher and the selected Command Line Tools compiler
are identified. The exploratory coarse estimates are preserved separately;
they are not failed target measurements or admitted cycle grants.

## Preservation, impact and handoff

The final scope/preservation check records the exact paths and verifies all
16,610 published file identities in the baseline, 16,608 unchanged identities in
this candidate (excluding WIP and the adapter), six related checkouts and all
480 unrelated paths. The original target and failed FC packets remain unchanged.
The two unavailable historical checkouts remain **NOT VERIFIED at the
Git-worktree tier**; no missing metadata or evidence was reconstructed.

Generated artifacts are unchanged. Platform retains ownership inside the
existing CoreRuntime resident allocation; public ABI and physical owners do
not change. No MAP/base-page, CPU-port, ROM/I/O selection, DMA, math-register,
assembly register/clobber or IRQ/NMI-handler changes occur. Added C code/state
and stack/scratch effects require future target accounting. Production `$8000`,
development `$9000`, all other owners and zero protected reserve are preserved.

Historical failures remain independent and unchanged: **29,426 / 28,671 resident
bytes (755 over)** and **2,323,776 / 2,025,000 cold-frame cycles (298,776 over)**.
They do not measure this new clock source. Complete FC scheduling, publication
wait/commit safety and executable admission remain unresolved.

Review this focused clock/preflight/host increment next. Publication and any
later exact-image accounting or complete-cost analysis need separate authority.
No relink, runtime/Xemu, rendering/oracle campaign, banking, D81, SD, physical
testing, commit, push, PR update or merge was performed.
