# M2 fixed-kernel complete-cost correction — bounded Build Intent

Status: **READY FOR REVIEW — planning only; FC-D1–FC-D5 await founder approval.**

## Recommendation and boundary

Authorize one **host-only accounting correction**: distinguish processor work
from elapsed publication delay and evaluate them on the same bounded timeline.
Keep the fixed-kernel design, workload ceilings and all unknown costs explicit.
This corrects the next proof method; it does not regrade the accepted failed
preflight or promise that the renderer can meet 50 ms.

The deliverable would be a phase-aware schedule, a remaining-cost allowance and
an honest gate result. No renderer rewrite, kernel optimization, target link or
execution follows automatically, even if the accounting checks pass. Completing
missing kernel cost proofs would require a separately bounded task if they
cannot be established from the existing inspected material.

## Verified starting point and authority

- Published checkpoint: `6c0caa8d453bb647696ef85b5b31b35ef2310def`.
- Fetched main: `9570f0ab427121a4e8f042041a14c89aaaeff9e2`.
- [PR #33](https://github.com/SUON1/f65-megawing/pull/33) is draft,
  **FAILED PREFLIGHT — NOT FOR MERGE**. Its experimental ancestry is not main
  admission. PR #32 remains separate historical failed evidence.
- Planning branch: `codex/65aero-m2-fixed-kernel-cost-intent`, in
  `/private/tmp/f65-m2-fixed-kernel-cost-intent`, from the exact published head.
  Only this document and this worktree's WIP may change.
- Original [packet](../evidence/flight-demo/2026-11-11-m2-fixed-kernel-preflight/README.md)
  seal SHA-256:
  `77641f1f0aed3d8c993d713e7932350d6d824468ce99e736037bdd4cfb15da72`.

The approved [FK-D1–FK-D8 intent](65AERO_M2_FIXED_KERNEL_BUILD_INTENT.md),
[Phase 1 plan](65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md),
[display/commit contract](65AERO_M2_PR2_BUILD_INTENT.md),
[extended resident contract](../../interfaces/m2_extended_resident.json),
[resident ledger](../../memory/m2-extended-resident-ledger.json) and
[current specification manifest](../../spec/manifests/spec-corpus.json) govern.
The [accepted preflight report](../reports/M2_FIXED_KERNEL_PREFLIGHT.md) supplies
the stated evidence tier and limitations. This plan requests no new architecture
exception. FK-D4's captured-camera rule remains approved but unimplemented in
the old executable; model it only as a proposed successor rule, never as current
behavior of that image.

## What needs correction

The current `design_budget()` in
[fixed_preflight.py](../../tools/flight_demo/m2_rebuild/fixed_preflight.py)
intentionally adds independent maxima and always refuses admission. That is a
valid conservative stop, not a demonstrated timing defect in the renderer.

| Retained accounting | Cycles | Meaning |
| --- | ---: | --- |
| Product, quotient-digit, normalization and copy payload sketches | 1,233,452 | Incomplete instruction sketches; not complete operation upper bounds |
| Six tick reservations | 234,756 | 6 × 39,126; includes possible carry-in |
| Full PAL-frame wait reservation | 808,704 | Phase delay, not additional renderer processor work |
| Separable subtotal | 2,276,912 | 251,912 above the 2,025,000-cycle nominal frame budget |

Ticks may execute during the publication wait. Adding their time again can
overstate elapsed duration; simply deleting a tick or subtracting a whole wait
can understate it. A tick, failed raster read or delayed polling can also cause
the commit window to be missed and add another frame. Neither possibility is
resolved by the existing scalar sum. Removing one tick alone still leaves
212,786 cycles unclosed, before missing costs.

The current [Platform commit](../../src/platform/m2_rebuild/platform.c) accepts
sampled physical raster lines 4 through `top - 16`: PAL 4–96 with `top=112`,
NTSC 4–48 with `top=64`. These are source predicates, **not admitted safe
windows**. The governing contract still requires the actual fetch semantics,
two complete lines of prefetch margin and a selector/readback critical path
shorter than one line. An inconsistent raster sample defers; it is not success.

The [main loop](../../src/diagnostics/m2_rebuild/main.c) prioritizes due ticks
and uses a Q16 native-clock period with fractional carry. The
[guard](../../src/platform/m2_rebuild/guard.c) requires strictly more remaining
time than operation plus guard costs. The
[clock calibration](../../src/platform/m1/m1_platform.c) depends on the pinned
emulator's scanline accounting. Therefore nominal CPU cycles, native CIA
counts, raster phase and host wall time must not be treated as interchangeable.

## Exact founder decisions

| ID | Decision requested | Recommendation |
| --- | --- | --- |
| FC-D1 | Authorize a separate host-only successor to the published cost preflight, with no target changes? | **Approve.** Add a small schedule/accounting verifier and focused host regressions from `6c0caa8`; preserve the original verifier, report and packet unchanged. Use analysis identity `65AERO-M2-FIXED-KERNEL-PREFLIGHT-2`, not a generated runtime profile. |
| FC-D2 | Replace the independent full-wait-plus-ticks sum with a source-pinned joint schedule covering PAL and NTSC? | **Approve.** Account for actual commit-window eligibility, tick interference, polling, guards and clock uncertainty across all legal phases. No favorable phase alignment, skipped tick, widened window or delayed capture is assumed. |
| FC-D3 | Keep the existing workload ceilings and require explicit proof for every demand credit? | **Approve.** Retain 377 products, 198 divisions and 396 quotient digits. Retain the 550-tile case only as conditional; use the 640-slot fallback for an unconditional demand case unless its tighter raster bound is independently proved from existing code. No geometry or raster optimization in this task. |
| FC-D4 | Permit only substantiated complete costs to close the gate, with unknown entries blocking admission? | **Approve.** Separate linked bounds, incomplete instruction sketches and unknown costs. Report a residual allowance; never fill missing costs with zero or an invented allowance. Keep resident fit independent and unproven. |
| FC-D5 | What happens after the corrected accounting is checked? | **Stop at READY FOR REVIEW or the first unresolved mandatory proof.** Do not reactivate FK-D7's conditional rewrite/link sequence. No implementation of renderer changes, relink, runtime, Xemu, banking, D81, SD, physical work, commit, push, PR update or merge without separate authorization. |

## Smallest proposed implementation scope after approval

Keep the existing verifier and its 11 accepted regressions intact. A companion
`tools/flight_demo/m2_rebuild/fixed_schedule_preflight.py` may consume its sealed
result and reuse its pinned identity/tick checks. Add only its focused test file,
one correction report, WIP and a fresh evidence directory. Do not edit old seals,
source archives, `src/`, `interfaces/`, `memory/`, CI policy or accepted reports.

### 1. Establish the time and publication model first

Read and hash-check the pinned source revision
`40dfef0d1d5f56be2469492715c12bdb32c75b67`, including `mega65.c`, `vic4.c`,
`vic4.h`, `io_mapper.c` and the instruction timing table, together with the
current application clock/guard/commit source and sealed linked image.
Use the available source checkout read-only; do not launch Xemu.

Derive conservative conversions and uncertainty for scanline-truncated CIA
updates, coherent clock/raster sampling, Q16 fractional release carry, guard
rounding and 32-bit wrap. Keep the old 39,126-cycle tick bound restricted to its
pinned composition; it is not a native-clock grant for a future image. If a
required conversion or window property cannot be established, report that
specific missing proof and stop before a purported frame result.

### 2. Put processor work and waiting on one timeline

Represent construction, due-tick service, guard-limited yielding, commit polling
and successful selector/readback plus record publication as distinct events.
Charge bounded calls, returns, scheduler/guard/poll overhead and interrupts.
Include the main loop's no-grant path and repeated unsuccessful commit polls;
neither is a zero-cost sleep or permission to block the authoritative tick.
The retained tick bound already includes two raster IRQs and a terminal NMI;
identify that coverage and separately bound interrupts during renderer/wait
work. Do not remove inherited conservative charges without a proof.

Ticks occurring inside an elapsed waiting interval occupy that interval, rather
than automatically extending its end. Conversely, service that prevents entry
within the remaining commit window must advance to the next eligible window.
There is no free overlap of two CPU operations. Include any unusable slack
caused by the next atomic operation being too large for the guard's grant.

Cover arbitrary capture/raster/tick phases, fractional carry and timer wrap.
Prove that any finite phase partition covers the full domain; a sample sweep or
a nominal five-tick assumption is insufficient. Repeated generations require
an invariant on possible completion and next-begin phases, not an assumed
reset of phase after every frame. Charge begin/return delay when assessing
inter-commit cadence. Do not insert a wait before capture to make its age look
smaller. Cold and continuously changing cameras remain required cases under
the proposed FK-D4 rule; persistent-pose latency remains at most 100 ms, with
capture-to-commit at most 50 ms and scanout latency reported separately.

Fault, explicit cancellation, identity invalidation and exhaustion preserve the
last complete frame and follow bounded failure/terminal handling. A faulted or
cancelled frame is not a successful 20 Hz publication. No infinite external
fault/cancellation stream is relabeled a normal cadence guarantee.

### 3. Report the complete-cost boundary honestly

Keep these categories separate:

- **Known old-image bound:** the pinned tick analysis, with its exact scope.
- **Conditional payload sketch:** product 592, quotient digit 445,
  normalization shift payload 1,176 and copy byte 15 cycles. These omit costs
  and cannot be used as complete WCET grants.
- **Unknown completion costs:** normalization relocation/control; sign,
  quotient correction, rounding and overflow; delta packing, rotation/clip
  control, plane distances and horizon; tile painting, line traversal, text
  formatting and maps; Platform checks/restoration and compiler wrappers;
  dispatch, polling, native-clock conversion and full commit paths.

Retain each unknown as an explicit blocking entry. Determine, where provable,
how much additional construction and atomic-service work each phase case can
tolerate. A positive residual is an allowance for missing proof, not evidence
that the missing code fits it. Unknowns must not produce a successful complete
cost gate or a zero exit status implying admission.

The 550-tile case transfers 40,080 bytes. The allocation-safe 640-tile fallback
transfers 45,840 bytes: 2,000 + 640×64 + 2,880. At the same incomplete copy
payload rate it adds 86,400 cycles, making the old separable subtotal 2,363,312
and its excess 338,312. This is a sensitivity calculation only. Tightening
workload counts, assuming cache hits or redesigning the copy/arithmetic kernels
is outside this correction.

Retain the independent actual resident failure: 29,426 / 28,671 bytes, 755
over; compiler scratch 87 bytes; zero reserve. The old cold-frame lower-bound
failure remains 2,323,776 / 2,025,000 cycles, 298,776 over. Hypothetical selected
retirement remains 6,935 bytes; replacement allowance 6,180, or 5,820 after the
256-byte margin and 104 bytes of proposed new data. No new saving, encoded-size
closure, stack proof or actual fit follows from a scheduling calculation.

## Required future regressions and stop rules

Run the new host-only tests in temporary directories. Preserve success and
failure output in a new packet; never direct regression output into old evidence.
Required cases are:

- Tick fully inside a wait, partly overlapping it, and carrying in at capture;
  prove against an independent simple time-line calculation that no work is lost
  and the same elapsed interval is not charged twice.
- Completion before, exactly at and just after both edges of each commit window;
  tick/IRQ interference or stale/inconsistent raster reads causing a missed
  window; bounded retries must never be an instantaneous successful commit.
- PAL and NTSC; every admitted phase class; Q16 fractional carry, clock wrap,
  uncertainty and strict guard equality; oversized atomic operations must fail.
- Cold/moving consecutive generations and persistent-pose age; explicit
  cancellation and fault before/during activation; no mismatched record or
  successful-publication credit after failure.
- Changed source/reference/image hashes, missing or malformed costs, wrong
  units, unsupported phase/edge, unproved 550-tile credit and truncated tables
  must fail closed. Positive residual with unknown costs must remain UNPROVEN.
- Original packet/source inventories unchanged after both passing and failing
  tests; 480 unrelated paths and historical checkout preservation rechecked.

Report separately: accounting-verifier correctness, native-clock/window proof,
complete-cost admission, residual unknown work, resident/stack admission and
execution authorization. Passing host fixtures alone closes only verifier
correctness. If full proof remains unavailable, name the first exact missing
operation or assumption and stop; do not launch another optimization campaign.

## Ownership, hardware impact and planning validation

This plan and the proposed host-only correction change no registers/clobbers,
CPU-visible or physical memory, MAP/B, CPU ports, DMA, IRQ/NMI ownership or
target behavior. Platform retains math/display I/O ownership; CoreRuntime keeps
100 Hz and all 21 stages. Graphics owns captures/cache/composition, Presentation
owns snapshots and Diagnostics owns requested camera. Precision, public ABI,
nine runway segments, diagnostic telemetry, both NOT IMPLEMENTED labels,
complete-frame publication, production `$8000`, development `$9000` and zero
reserve remain fixed. Generated contracts and all target grants stay unchanged.

Planning validation passed: two-file scope, 14 local document links, whitespace,
all stated arithmetic and five pinned reference-file identities. All 16,582
files in the published checkout match the starting inventory; all 16,581
baseline files outside this new worktree's WIP match here. The 20 sealed packet
members and six pinned source identities match in their original checkpoint.
The original preflight, planning and failed-experiment checkout identities are
unchanged. All 480 unrelated paths and six available historical checkouts match.
`git diff --check` and the published packet's `check_scope.py` both returned 0;
the latter ran in its original checkout, with output outside sealed evidence.
Inline read-only Python checked links, hashes and scalar arithmetic without
invoking the engineering preflight. No new schema or generated artifact changed.

These are documentation, arithmetic, Git scope and preservation checks only.
No preflight replay, host rendering campaign, target build
or runtime test is required for preparing this intent. The original packet's
WIP identity belongs to `6c0caa8`; only the new planning worktree gets a new WIP.
Two unavailable historical checkouts remain **NOT VERIFIED at the Git-worktree
tier**. Available hash evidence is retained separately; no metadata is rebuilt.

The next permitted action is founder disposition of FC-D1–FC-D5. This planning
checkpoint does not authorize executing those proposed corrections.
