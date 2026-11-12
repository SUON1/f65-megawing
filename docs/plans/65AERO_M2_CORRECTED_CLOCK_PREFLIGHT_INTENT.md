# M2 fixed-kernel complete-cost preflight with corrected Platform clock

Status: **READY FOR REVIEW — planning only; CC-D1–CC-D6 await founder approval.**

## Recommendation and bounded deliverable

Authorize one host-only successor to the stopped complete-cost preflight. Use
the accepted Platform clock semantics to establish the remaining calibration,
native-count/raster and publication-window model, then derive a phase-aware
schedule and explicit missing-cost limits where those prerequisites permit.
Produce one source-pinned result, independent regressions and a clear first
unresolved obligation. Do not implement the fixed kernels or tile renderer.

The corrected clock's target code/call/stack costs are still **UNMEASURED**.
A numeric executable-admission claim is already blocked. The useful work in
this proposal is a bounded conditional proof: establish which complete costs
a later executable would have to satisfy. Unknown costs block admission.
This is not permission to bypass that gate or repeat size optimization.

## Verified baseline and authority

- Published corrected source: `fcba7cf4f742a216fba1a6954a4e74b7c9d59ec8`.
  [PR #35](https://github.com/SUON1/f65-megawing/pull/35) remains draft,
  **NOT FOR MERGE**; static CI run `43123374216` passed. Its experimental
  ancestry remains unadmitted and is not integrated main.
- Fetched main: `9570f0ab427121a4e8f042041a14c89aaaeff9e2`.
- Planning branch: `codex/65aero-m2-corrected-clock-preflight-intent`, from
  the published clock commit. Only this intent and its WIP may change.
- Historical executable root: `/private/tmp/f65-m2-fixed-kernel-cost-correction`,
  at `5c78bf7d00aadda0e63ce800e27fe3e142c651c0`; PRG SHA-256
  `7fdcea61387c0e6b7ae92310725966ac6c0e29e82e8ba1c9a6be77335af76aad`.
- Clock packet seal:
  `0b0abb69eebb774bbba81203cb9f7b8a990b634c8b1e2968e28af091cc89e593`.
  Normalization P2 packet seal:
  `59c17610191f1079b7ac076978d70e06b2f70ace1d745eb4ad4f1eeb9742bb3e`.

Authority: the [specification manifest](../../spec/manifests/spec-corpus.json),
Main v1.8/Runtime v1.2 candidate, [Phase 1 plan](65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md),
approved [FK intent](65AERO_M2_FIXED_KERNEL_BUILD_INTENT.md),
[FC intent](65AERO_M2_FIXED_KERNEL_COST_CORRECTION_INTENT.md),
[clock intent](65AERO_M2_PLATFORM_CLOCK_CONTINUITY_INTENT.md),
[display/commit contract](65AERO_M2_PR2_BUILD_INTENT.md),
[extended resident contract](../../interfaces/m2_extended_resident.json) and
[ledger](../../memory/m2-extended-resident-ledger.json). No new architecture
exception is requested. FK-D4 is approved successor captured-camera policy,
not behavior already implemented in the historical image.

## Exact founder decisions

| ID | Decision requested | Recommendation |
| --- | --- | --- |
| CC-D1 | Authorize one host-only successor from the published clock source, preserving earlier checkers and evidence? | **Approve.** After approval use a separate `codex/65aero-m2-corrected-clock-preflight` branch from `fcba7cf` and analysis identity `65AERO-M2-FIXED-KERNEL-PREFLIGHT-3`. Keep historical target and corrected-source roots separate. This is not a runtime profile or main integration. |
| CC-D2 | Require corrected-clock calibration, observation uncertainty and publication-window semantics before schedule credit? | **Approve.** Consume accepted clock/P2 evidence; prove remaining phase/rounding/window obligations with pinned sources and independent host models. No invented target cost, ideal calibration assumption or widened window. |
| CC-D3 | Allow a conditional joint schedule accounting for simulation work during publication waits? | **Approve.** Cover all admitted PAL/NTSC phase classes, strict guards, atomic fragmentation, retries and consecutive generations. Report sufficient cost constraints, not an executable grant. Stop dependent analysis if required semantic/window proof is unavailable. |
| CC-D4 | Retain full workload, complete-frame and camera-age requirements? | **Approve.** Keep 377 products, 198 divisions, 396 quotient digits and unconditional 640-tile demand. No unproved 550-tile, cache-hit, cancellation or favorable-phase credit. Preserve 100 Hz/21 stages, 20 Hz, capture-to-commit at most 50 ms and persistent-pose publication at most 100 ms under FK-D4. |
| CC-D5 | Charge missing costs and corrected-clock resident overhead explicitly, with separate gate results? | **Approve.** Missing clock/kernel/Platform/compiler costs remain typed unknowns; positive residual never means PASS. Preserve historical failures. Reduce the old replacement allowance by the additional clock charge; no assumed savings, margin consumption, reserve use or larger ceiling. |
| CC-D6 | What follows this bounded host analysis? | **Stop at READY FOR REVIEW or the first unresolved mandatory model gate.** Record executable-admission blockers separately even if the conditional model succeeds. No automatic FK implementation, target compile/relink, runtime/Xemu, optimization, banking, D81, SD, physical testing, commit, push, PR change or merge. |

## Ordered work after approval

### 1. Preserve distinct source and image identities

Leave [FC2](../reports/M2_FIXED_KERNEL_COST_CORRECTION.md),
[the clock report](../reports/M2_PLATFORM_CLOCK_CONTINUITY.md) and
[the P2 report](../reports/M2_PLATFORM_CLOCK_GAP_P2.md) unchanged. Verify seals,
source archives and original target/reference identities before analysis.
The old checker pins 81 inputs including old `m1_platform.c`; do not relax pins
to make it accept corrected source. Use the old root for its disassembly and
linked bounds; pin current clock helper, adapter, main, guard and commit source
separately to `fcba7cf`. Every bound names its source/image, units and tier.

The old 39,126-cycle tick and 728,824,896-native-count gap are not corrected-image
grants. P2 normalization/divide bounds 14,191/63,084 apply only to that old image.
Do not substitute them for the proposed fixed-kernel implementation costs.

### 2. Establish source-model semantics before phase accounting

Use the eight pinned emulator references at
`40dfef0d1d5f56be2469492715c12bdb32c75b67`, read-only. Reuse accepted clock
semantics: latch 65,535, period 4,294,836,225, separate uint32 accumulator wrap,
sticky faults and a required successful-sample gap strictly below `2^31` native
counts. A full missed hardware period remains undetectable. Preserve the
32-attempt raw sampler; a small observed delta does not prove the caller gap.

Extend coverage for actual 17-sample calibration, all admitted frame/sample
offsets, `elapsed / 16` truncation, `cfratio` rounding, Q16 fractional carry,
timer/public wrap and strict guard equality. Derive CPU-cycle/native-count
relationships from the pinned 32-count scanline updates, endpoint staleness,
IRQs and polling latency. Host time, CPU cycles, raster and native counts are
distinct units. Unmeasured converter/wrapper costs remain named parameters
with explicit sufficient inequalities, never default zeros.

Current commit predicates accept NTSC lines 4–48 and PAL lines 4–96; these are
not admitted windows. Trace coherent/stale raster samples, first enable,
selector/readback, matching record publication and first dependent display
fetch. Establish two complete lines of prefetch margin and selector/readback
completion shorter than one line as cost obligations. Include IRQ placement,
readback/fault failure and missed-window advancement. If fetch/order semantics
cannot be established, stop before assigning a usable window or frame allowance.
No Platform edit, new IRQ, interrupt masking or invented hardware guarantee.

### 3. Build one complete conditional event model

Model capture, preparation, atomic renderer units, due ticks, guard/no-grant
paths, unsuccessful commit polls, activation/record publication and next begin
on one timeline. CPU operations cannot overlap. Ticks serviced during waiting
are not also charged outside that elapsed interval; work that misses a window
must advance publication to the next eligible window. Charge calls/returns,
clock/fault checks, scheduler/guard overhead, interrupts and unusable atomic
slack. No skipped/merged tick or catch-up debt counts as deadline success.

Prove coverage of a finite phase partition or interval model, rather than
sampling favorable alignments. Cover Q16 state and repeated generations without
phase resets. Charge begin/return delay in inter-commit cadence. Include cold
and continuously changing cameras without cache credit, modeling FK-D4 only as
successor semantics. Do not delay capture to improve apparent age. Report
scanout latency separately. Pre-activation cancellation, invalidation,
exhaustion or fault retains the old complete frame. An uncertain selector/write
readback requires terminal failure and reset, with displayed identity unproven;
never claim rollback or that the old generation remains live. Neither outcome
receives successful publication or cadence credit.

The cost inventory includes arithmetic/sign/carry/rounding/overflow; transforms,
clipping, planes and horizon; maps/tiles/raster/text; Platform checks/restoration;
compiler wrappers/scratch/stacks; dispatch/input/ticks/clocks/guards/IRQs and
commit. Every entry is a pinned bound, proved symbolic demand or unknown.
Existing 592/445/1,176/15-cycle payload sketches are neither complete WCETs nor
proven whole-operation lower bounds. They cannot establish grants or inevitable
failure from the historical separable sum.

Report constraints on every missing whole-operation and atomic cost, including
clock calls in ticks, renderer loops and waits. Do not emit a single spendable
allowance that omits required terms. Positive conditional allowance with unknown
entries leaves complete-cost admission **UNPROVEN**. Stop at the first missing
semantic proof; later gates stay **NOT REACHED**. Known unknown costs may remain
symbolic only in this explicitly conditional model and still block admission.

## Frozen workload, lifetime and resident accounting

- Unconditional display demand: `2,000 + 640 × 64 + 2,880 = 45,840` bytes.
  Historical 550-tile/40,080-byte demand stays conditional, without default
  credit. No tighter workload proof or renderer optimization is in scope.
- Preserve cell-exclusive mixed tiles, complete 1,000-entry maps, 80-byte bitmap
  and 24-byte delta buffer. Existing 64-byte Platform buffer reuse is synchronous
  and only after initialization retirement, nonoverlapping on success, fault
  and cancellation. The schedule must retain these lifetimes.
- Historical actual resident: `29,426 / 28,671`, **755 bytes over**, scratch 87,
  reserve zero. Historical cold lower bound: `2,323,776 / 2,025,000`,
  **298,776 cycles over**. Neither measures the corrected source.
- Historical hypothetical retirement 6,935; replacement allowance 6,180;
  after 256 margin and 104 proposed data bytes: **5,820**. Keep those figures
  historical. Current conditional allowance is `5,820 - C_clock`, where
  `C_clock` charges additional clock state, code, padding, scratch and alignment
  without assumed retirement credit. The 10 logical state bytes alone reduce
  its upper ceiling to **5,810**, before all other clock costs. Host size 12 is
  not a target-layout claim. No measured fit follows.
- Stack maxima remain separate. Preserve production `$8000`, development
  `$9000`, owner allocations and zero protected reserve.

## Proposed scope, regressions and stopping results

Add one companion `tools/flight_demo/m2_rebuild/corrected_clock_preflight.py`,
focused Python tests, one report, WIP and a fresh evidence packet. Preserve all
target code, historical tools/tests, interfaces, ledgers, CI policy and grants.
No target compiler/linker is needed. Reuse accepted clock evidence; do not rerun
accepted rendering or C host campaigns merely to prepare this successor.

Independent event/countdown and simple timeline oracles must cover calibration
offsets/truncation, A/B and public wrap, sampler rejection/lockout, tick carry-in,
full/partial wait overlap, both window edges/misses, IRQ interference, strict
guard equality, oversized atomic operations, polling cost, consecutive cold/
moving generations, persistent-pose age, fault/cancellation/exhaustion and frame/
record coherence. Negative fixtures reject changed/missing/symlinked inputs,
wrong roots/units, missing costs, truncated/unsupported phase partitions, old
cap-six credit, unproved 550-tile credit and positive-residual attempts to turn
unknowns into PASS. Fixtures and outputs use temporary directories, never sealed
packets. Recheck protected inventories after successful and failing runs.

Report input integrity, clock/calibration source-model correctness, conditional
gap/window proof, conditional schedule/cost constraints, actual complete-cost
admission, resident/stack admission and execution authorization separately.
Regressions may return zero; candidate admission with mandatory unknowns must
remain nonzero/UNPROVEN with no launch/service budget emitted. Preserve the first
failure and stop; do not automatically implement a correction or redesign.

## Planning impact and validation

Register/clobber, CPU-visible/physical-memory, MAP/B, CPU-port, DMA, IRQ/NMI and
target deadline effects are not applicable to this planning task or host model.
Platform retains I/O/time; CoreRuntime retains 100 Hz/21 stages; Graphics owns
composition/capture, Presentation snapshots and Diagnostics requested camera.
Exact Q12/Q24/Q46/Q16 precision, nine segments, required telemetry and both
NOT IMPLEMENTED labels remain fixed. Generated contracts remain unchanged.

Planning checks passed: two-file scope/ancestry, 12 local links, whitespace,
stated scalar arithmetic, three JSON contracts and eight pinned reference files.
All 16,654 published identities and 16,653 planning-tree identities outside WIP
match. All four packets (20/23/13/16 members plus seals), seven related checkouts
and 480 unrelated paths remain preserved. Checks used read-only Python and
`git diff --check`; the historical preservation checker ran unchanged in its
original checkout, with output outside sealed evidence. No new schema or
generated artifact changed. Independent planning review checked the clock,
budget and uncertain-activation boundaries.

No engineering preflight, target build or runtime test is performed. Two
unavailable historical checkouts remain **NOT VERIFIED at the Git-worktree
tier**; available hashes are separate evidence. No metadata is reconstructed.

Next: founder disposition of CC-D1–CC-D6. This planning document does not
authorize its proposed host implementation, publication or further engineering.
