# M2 Platform clock continuity — bounded Build Intent

Status: **READY FOR REVIEW — planning only; PC-D1–PC-D6 await founder approval.**

## Objective and recommendation

Prepare one development-only Platform correction for the accepted chained-timer
rollover failure. Preserve the existing bounded raw sampler and timer setup;
convert its readings into accumulated native elapsed counts behind the existing
Platform interface. Use that same corrected clock for calibration and runtime
reads. Validate a small C candidate with independent host arithmetic and fault
fixtures after approval. No target compile/link or runtime execution is included
in this proposed increment.

This closes a prerequisite for later scheduling analysis. It does not solve the
renderer fit/timing failures, complete the FC joint schedule, reactivate the FK
implementation/link grant, or admit an executable.

## Verified baseline and authority

- Fetched main: `9570f0ab427121a4e8f042041a14c89aaaeff9e2`.
- Published correction: `5c78bf7d00aadda0e63ce800e27fe3e142c651c0`;
  [PR #34](https://github.com/SUON1/f65-megawing/pull/34) is draft, NOT FOR MERGE,
  with passing static CI. Its parent is `6c0caa8d453bb647696ef85b5b31b35ef2310def`.
- Planning branch: `codex/65aero-m2-platform-clock-intent`, from `5c78bf7`.
  Published experimental ancestry is retained; it is not integrated main.
- Accepted [clock counterexample](../reports/M2_FIXED_KERNEL_COST_CORRECTION.md):
  32 supplied CIA ticks become 65,569 accepted binary timestamp counts at the
  first upper-timer reload. This is pinned-source evidence, not an observed run.
- Correction packet seal SHA-256:
  `84d469cfaab7c362126c6a28a8d504ada24a1c012826d138ee7b88c3f1c3ce77`.
  Retained PRG SHA-256:
  `7fdcea61387c0e6b7ae92310725966ac6c0e29e82e8ba1c9a6be77335af76aad`.

Governing authority: the [specification manifest](../../spec/manifests/spec-corpus.json),
Main v1.8 with incorporated Main v1.7 §§2.5, 3.3 and 4, Runtime v1.2 approved
candidate, [Phase 1 plan](65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md),
[FC intent](65AERO_M2_FIXED_KERNEL_COST_CORRECTION_INTENT.md),
[Platform registry](../../interfaces/f65_platform_abi.json5),
[development interface](../../interfaces/m1_development.json),
[M1 ledger](../../memory/m1-development-ledger.json),
[extended resident contract](../../interfaces/m2_extended_resident.json) and
[ledger](../../memory/m2-extended-resident-ledger.json). The existing
[display/commit contract](65AERO_M2_PR2_BUILD_INTENT.md) is unchanged.

## Exact founder decisions

| ID | Exact decision requested | Recommendation |
| --- | --- | --- |
| PC-D1 | Authorize one Platform clock candidate and host validation from published `5c78bf7`, leaving PR #34 and its source/evidence intact? | **Approve.** Use a separate `codex/65aero-m2-platform-clock` implementation branch and candidate analysis identity `65AERO-M2-PLATFORM-CLOCK-1`; copy this approved intent without changing the planning checkout. This is not a new adopted/generated runtime profile. |
| PC-D2 | Correct the private clock interpretation using the actual 65,535-count timer periods, accumulated elapsed counts and one calibration/read domain? | **Approve.** Retain `cfclock_begin()` and `cfnow()` unchanged; treat the latter as a raw coherent encoding inside Platform. Keep existing public signatures, unsigned 32-bit output and Q16 period format. Recalculate calibration from corrected samples; no inherited binary-clock ratio is a grant. |
| PC-D3 | Require an explicit observation-gap invariant and fail-closed lifecycle before claiming continuity? | **Approve as a hard prerequisite.** Establish less than `2^31` supplied CIA counts between successful samples on every nonterminal caller path. Reject observed deltas at or above that threshold, invalid samples and sticky faults. No duration cap, full-period-loss detection claim or new IRQ timekeeper may substitute for the proof. Stop if the prerequisite cannot be established within this scope. |
| PC-D4 | Authorize focused C host/sanitizer checks and independent sampler/arithmetic/calibration/deadline regressions only? | **Approve.** Preserve both historical failed preflights, use fresh temporary outputs and new source-pinned evidence, and report clock arithmetic separately from application timing/admission. No renderer/oracle campaign or complete-frame schedule implementation. |
| PC-D5 | Bound private state and retain all memory/performance obligations without a target link? | **Approve.** At most two 32-bit state values and two byte flags: 10 logical payload bytes before layout padding. Charge actual padding, code, constants, scratch, stacks and call cost at later exact-image admission. No workspace overlay, protected reserve, memory-limit increase or invented cycle estimate. New target size/cost remain UNMEASURED. |
| PC-D6 | What may follow the candidate checks? | **Stop at READY FOR REVIEW or the first unresolved mandatory gate.** No target compile/link, Xemu or other runtime testing, renderer changes, full FC scheduling, banking, D81, SD, physical testing, commit, push, PR update or merge. Those need separate authorization. |

## Smallest technical correction after approval

The [current adapter](../../src/platform/m1/m1_platform.c) calls `cfnow()` directly
both during calibration and in `m1_platform_now()`. Correcting only the latter
would mix clock domains. Both must use one Platform-owned converter, and
`m1_platform_fault()` must include its sticky failure state. Retain the 17-frame
calibration loop, existing bounded polling, Q16 ratio algorithm and CoreRuntime
release/fractional-carry logic. Test their interaction; do not silently repair a
separate calibration or scheduler defect in this increment.

Reuse the unchanged [CF001 sampler](../../src/diagnostics/r0f/combined_platform.c),
including its eight reads, consistency predicates, top-sixteen exclusion,
32-attempt ceiling and fault signal. It continues to own the existing CIA
accesses. Check its fault before consuming a returned value; zero returned on
failure is not a successful timestamp. No second sampler or timer programming
path is needed. Unchanged [IRQ/NMI handlers](../../src/platform/r0f/qualification_45gs02.s)
must not call or update the converter.

For the pinned emulator source at
`40dfef0d1d5f56be2469492715c12bdb32c75b67`, let `L=65,535` and
`P=L²=4,294,836,225` (`$FFFE0001`). Decode A and B from the complement of the
successful raw `cfnow()` encoding; both countdowns must be in `[1,L]`.
The elapsed phase within the chained-timer period is:

`phase = (L - B) × L + (L - A)`, in `[0,P-1]`.

Its multiplication can be expressed exactly as `(u << 16) - u`, with
`u=(uint32_t)(L-B)`. No 64-bit arithmetic, division, floating point or hardware
math-register access is required. The complete expression stays within uint32.
This is an arithmetic rationale, not a linked-size or execution-cost claim.

Use the first successful sample to set a private origin and return zero elapsed
counts. Thereafter compute elapsed delta modulo P, using an explicit wrap case,
then accumulate that delta modulo `2^32` for the existing public return value.
At the accepted witness, phase moves from `P-1` to `31`; delta is exactly **32**.
Since `2^32-P=131,071`, hardware-period rollover and public uint32 rollover are
different events. The accumulator must handle both, including repeated wraps.
Duplicate samples produce zero delta and no progress; they are legal within
one scanline. Reset the converter only with reset-only Platform initialization,
before calibration; never at a frame, camera change or tick boundary.

### Observation gap, failure and ownership

Modulo arithmetic cannot detect one or more completely missed periods: the
same A/B reading can recur. The gap condition in PC-D3 is therefore a caller
obligation, not something a small observed delta proves. Derive its conservative
source/control-flow basis for calibration polling, post-calibration display
initialization, each main-loop tick path, every admitted renderer dispatch path
and nonterminal fault return. Count whole atomic calls, not just loop iterations.
Terminal paths do not resume the clock. Do not use zero launch/service grants
as a vacuous proof for the intended enabled application.

Use the pinned emulator's scanline/CIA relationship when relating work to this
gap. No fixed host wall-time assumption is valid. A coarse observation-gap bound
does not prove the much tighter 10 ms tick or 50 ms frame deadline. Changed
compiler output still needs later exact-image verification; the old 39,126-cycle
tick bound cannot be assigned to a changed executable.

On a sampler fault, invalid range, unsupported lifecycle or ambiguous observed
delta, keep the last valid published count, latch failure and refuse further
progress until reset. Initialization must reject failure before accepting a
period. The existing main-loop fault check remains the terminal authority.
The state is private, mainline-only and non-reentrant; no heap, callback,
interrupt-masked extension, ISR writer, or persistent/serialized clock state.

This correction is restricted to the pinned emulator development adapter.
The existing physical-machine refusal remains. Do not infer a physical CIA's
reload semantics or compatibility with other Xemu revisions from this model.
The adapter is shared source: no prior M1 or M2 qualification automatically
applies to a newly built caller after the change.

## Focused proposed change surface

- `src/platform/m1/m1_platform.c`: reset, shared calibration/now conversion and
  private fault propagation only.
- One new private Platform header for the small pure state/conversion helper,
  allowing the exact C implementation to be tested without target I/O. No
  public header, generated layout or existing build-source list needs changing.
- One focused host test driver and C harness under
  `tests/flight_demo/m2_rebuild/`, plus the new handoff/evidence and WIP.

The host evidence must include every new helper/header and exact compiler
arguments. Keep old tools and old input hashes unchanged; do not make the
frozen FC verifier accept modified target source. Use a new clock-only result
under the candidate identity. Preserve original source archives and every
failed attempt. Do not invoke broad build drivers that relink or overwrite old
evidence. Candidate output paths must be fresh, outside all sealed packets.

## Required checks and stopping boundary

1. Verify published ancestry, original packet/target/reference hashes, exact
   caller closure and ownership before implementation. Establish the sampler
   and observation-gap assumptions explicitly; unresolved mandatory assumptions
   stop the work rather than becoming an unconditional clock PASS.
2. Independently compare the C converter with an event/countdown oracle of the
   pinned timer recurrence, not another copy of the conversion formula. Cover
   reset/first sample, duplicates, ordinary increments, A reload, B reload,
   the published witness, multiple timer periods and separate uint32 wrap.
3. Check consistent and torn eight-read interleavings, carry/borrow boundaries,
   the retained `$FFF0–$FFFF` exclusion and 32-attempt exhaustion. Verify invalid
   A/B, sampler/NMI faults, delta just below/at/above `2^31`, sticky lockout and
   reset. Distinguish pure numeric edges from reachable 32-count increments.
   Include full-period alias examples to demonstrate the gap limitation;
   do not claim those are detectable from timer values alone.
4. Exercise the actual adapter's calibration/now/fault wiring with host fakes.
   Cover PAL/NTSC sample sequences, corrected-unit period calculation, Q16 carry,
   due-release modulo comparison and the existing strict guard equality policy.
   Expected values come from independent integer timelines. Preserve 100 Hz,
   all 21 stages, no skipped/merged ticks, precision and public interfaces.
5. Run focused host C warnings and address/undefined-behavior sanitizers. Record
   commands, exit codes, host compiler/source identities, state sizes and bounded
   operation counts. Report any unsupported observation-gap or calibration
   uncertainty separately. Host success does not establish target cost or the
   full native-clock/publication-window admission gate.
6. Check source scope, links, syntax, whitespace and preservation. Return at
   READY FOR REVIEW or the first failed gate. Target compile/link, new resident
   measurement, whole-program stack/service proof and execution remain NOT RUN.
   The full FC schedule and renderer implementation remain deferred.

## Fixed limits and impact

Preserve Q12/Q24/Q46/Q16, nine runway segments, diagnostic camera/telemetry,
complete immutable frames, CoreRuntime 100 Hz/21 stages, 20 Hz presentation,
production end-exclusive `$8000`, development end-exclusive `$9000` and zero
protected-reserve use. Historical actual resident usage stays **29,426 / 28,671
bytes**, **755 bytes over**, compiler scratch 87. The independent historical
cold-frame lower bound stays **2,323,776 / 2,025,000 cycles**, **298,776 over**.
Neither value measures a future clock candidate. No new target saving or cost
is claimed; the 10-byte payload cap excludes padding/compiler overhead.

Planning changes are documentation only. For the proposed future correction:
Platform owns the private clock state inside the existing CoreRuntime resident
allocation; physical ownership and limits do not change. No new MMIO writes,
register/assembly clobber contract, CPU port, MAP/base-page, DMA, math-register,
IRQ/NMI or software/hardware stack allocation changes. C helper stack/scratch
and per-read timing effects remain to be measured before target admission.
Generated contracts remain unchanged. No runtime/production authority is added.

## Planning validation

Planning validation passed: exactly two changed paths, 14 local links,
whitespace, scalar arithmetic and eight pinned reference identities.
`git diff --check` returned 0. Read-only `python3 -B` inventory checks verified
all 16,610 published files and all 16,609 planning-baseline files outside WIP;
the 23 sealed correction-packet members plus seal and all five related checkout
identities match. The unchanged original preflight preservation checker returned
0 from its original checkout, verifying the 480 unrelated paths and six
available historical checkouts. Validation output is outside sealed evidence at
`/var/folders/bt/gybs30z52sx1jjjhm2h7_nj80000gq/T/f65-clock-plan-validation-bec8vbzl/`.

The two unavailable historical checkouts remain **NOT VERIFIED at the
Git-worktree tier**. No missing metadata or evidence was reconstructed. No
implementation, host engineering suite, target compile/link, runtime test,
generated-artifact change, commit, push or PR modification occurred. The new
plan and WIP are ready for founder review; PC-D1–PC-D6 remain unapproved.
