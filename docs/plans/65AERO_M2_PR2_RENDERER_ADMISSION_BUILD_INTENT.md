# M2 PR2 complete-renderer fit and static admission — Build Intent

**READY FOR REVIEW — planning only; F1–F6 below await founder approval.**
Verified main: `8ee5214ea9c63b86e92ca9bc4fa0779115dbd57f`,
[PR #21](https://github.com/SUON1/f65-megawing/pull/21).
Fetched origin/main and local main agree; [exact-main CI](https://github.com/SUON1/f65-megawing/actions/runs/39623256426)
is successful. Planning branch: `codex/65aero-m2-pr2-renderer-admission-intent`.
This document proposes implementation; the present task authorizes planning only.

## Starting point and authority

The founder approved N1–N6 in the [prior full-composition intent](65AERO_M2_PR2_FULL_COMPOSITION_ADMISSION_INTENT.md),
then accepted and published the bounded prepared-context/overrun increment.
That historical intent and its original pending wording remain unchanged.
This successor scopes resumption from integrated code; it does not restart the
contract/prepared-context work or reinterpret the earlier approval as permission
to execute or publish the next implementation.

The [overrun handoff](../reports/M2_PR2_FIT_OVERRUN_FIX.md) and its retained
failed/corrected packets establish a regression probe ending at `$7FDC` with
36 bytes below `$8000`. The probe has a fixed camera, digest scaffolding and
legacy wrapper calls. It is not the complete renderer or a capacity estimate.
The 52-byte text reduction plus four alignment bytes are already integrated.
No further saving is assumed.

Governing authority remains Main v1.8, Gameplay v1.2, Runtime v1.2 approved
candidate (NOT FINAL), Graphics v2.1 and Physics v4.1 with their incorporated
bases, as pinned in the [corpus](../../spec/manifests/spec-corpus.json).
The prior intent's authority links, ownership, numeric constraints and detailed
acceptance requirements remain applicable. Approved D1 clarification and D2–D7
are carried forward, not reopened. Consult the [PR2 intent](65AERO_M2_PR2_BUILD_INTENT.md)
and [entry plan](65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md).

Inspected implementation/contracts: [prepared context](../../src/graphics/m2_prepared_private.h),
[geometry](../../src/graphics/m2_geometry.c), [cursor](../../src/graphics/m2_raster_private.h),
[current probe](../../tests/flight_demo/m2_pr2/fit.c), [platform](../../src/platform/m1/m1_platform.c),
[full contract](../../interfaces/m2_full.json), [generated header](../../interfaces/generated/m2_full.h),
[generator](../../tools/flight_demo/m2_full/generate.py), [full ledger](../../memory/m2-full-ledger.json)
and [M1 ledger](../../memory/m1-development-ledger.json).

## Exact founder decisions

| ID | Decision | Recommendation |
|---|---|---|
| F1 | Resume which implementation after PR #21? | Approve the complete shared host/target renderer and actual mutable-camera target root, compiled/linked only. Reuse integrated contracts, prepared geometry and cursor. Include actual font, telemetry, controls, cancellation/fault paths and normal/stress variants. A smaller probe is not the deliverable. |
| F2 | How should fit be established with only 36 probe bytes spare? | Preserve every ceiling and precision rule. Permit bounded pure-C sharing, existing prepared-context reuse and exclusion of probe-only digest/scaffolding from the new root. Measure early with real assets/state. Stop at the first failed fit/admission gate with retained evidence and a smallest follow-up proposal; no automatic optimization campaign, budget increase or feature deletion. |
| F3 | How should complete composition and accounting be enforced? | Retain `65AERO-M2-FULL-1` and its generated parent records. Implement the complete immutable world/registration/anchor/label bundle and every owner object; derive an actual symbol/lifetime bill from the link. Keep historical generated contracts and evidence unchanged. A required public-layout/resource change is a separate decision, not generator-hash editing for convenience. |
| F4 | What display profile and mapping decision applies? | Retain 320×200 backing at integer 2×, centered in 720×480 or 720×572 reference canvases at (40,40)/(40,86). Before hardware edits, derive a source-pinned PAL/NTSC register/fetch/latch contract. Unsupported or ambiguous mapping stops display implementation; no silent PAL 576 substitution, cropping workaround or native large framebuffer. |
| F5 | What does runtime/display admission mean here? | Static readiness only, with separate fit, ABI/stack, service-bound and display-contract outcomes. Trace actual scheduler/platform paths and fail closed on unknown bounds. Compilation or host models do not establish runtime safety, scanout, cadence, visual acceptance or exercised stack high-water. |
| F6 | What validation and stopping authority is granted? | After approval, run host/oracle/sanitizers, target compile/link and static analysis only. Stop at READY FOR REVIEW or the first failed/unproven prerequisite. No Xemu, D81, SD, physical testing, commit/push/PR/merge or later milestone. |

Suggested approval:

> Approve F1–F6 as recommended. Build the bounded M2 PR2 complete renderer and
> static-admission increment from verified main, preserving precision, memory
> limits, required behavior, evidence and unrelated paths. Run host/oracle and
> target compile/link/static checks only. Stop at READY FOR REVIEW or the first
> failed or unproven prerequisite. No Xemu, D81, SD, physical testing or publication.

## Gate order and concrete deliverables

### 1. Complete resource model and shared renderer; measure fit early

Continue the private immutable prepared-camera lifetime and 16-byte cursor;
retain public API failure/output behavior and registration alias correctness.
Keep Q12 positions, Q24 clipping, Q46 rotation, Q16 projection, original camera/
fixture bounds, 0.5-pixel projection and one-pixel raster tolerances. Oracle
calculations stay independent of production geometry. No arithmetic narrowing,
new recurrence approximation or removed clipping plane is authorized to fit.

Build one renderer used by the host backend and target root. Include all 17
runway segments, four protected anchors, deterministic capacity-two optional
labels, complete 320×128 world, 320×64 telemetry and blank eight-row footer.
Use the actual owned 8×8 font, strings and conversion routines on both paths.
Show NON-FLIGHT, checksum/tick/generation/camera/source-age/fault/cancellation
values; altitude left and airspeed right remain NOT IMPLEMENTED with validity
and reference/units handled per Gameplay. Camera height is above test datum,
never flight altitude. Label policies and semantic press edges remain inherited.

Copy and release a valid snapshot before construction. Capture one camera and
transform per generation. Prepare hidden storage only; cancellation/staleness
leaves the previous complete pair visible. Check all identities/completion before
commit; failed activation readback enters fatal uncertain-activation state.
Generation/revision exhaustion fails closed. Inner PR1 registration composition
revision remains 1; the outer full bundle requires revision 2. Validate both
at their owning boundaries, without treating the old pair predicate alone as
proof that the full bundle is complete.

Charge both bundles, prepared context, requested/captured camera, copied snapshot,
cursor/line, tile[64], text[320], counters, input-edge state, font/tables, platform
state and all compiler scratch. The current generated ledger names owner classes;
it does not prove their final byte bill. Produce an additive measured report,
not a rewrite of historical measured evidence. Charge alignment and static
scratch once; distinguish hardware stack, dynamic software stack and resident
compiler scratch. Any workspace reuse needs a non-overlap lifetime proof through
normal, failure, cancellation and interrupt contexts.

Preserve resident `$2001–$7FFF`, base page `$0200–$02FF`, hardware stack
`$0100–$01FF`, software envelope `$C000–$CFFF`, platform result `$1900–$1FFF`,
initialization-only `$09E0–$0A14` writes and Attic ROM backup
`$08000000–$0801FFFF`. No other-owner allocation or `$058000–$05FFFF` reserve draw.
Each display at `$020000`/`$030000` retains 2,000 map bytes + 48 alignment +
61,440 changing tile bytes + 64 blank bytes = 63,552; its last 1,984 bytes stay
unallocated. Shared 2,000-byte Color RAM and palette become immutable after init.
No font/code hiding in display slack, new DMA, sprites or RRB path.

Create a separate real composition root; preserve the historical probe and its
checks. Keep camera/input runtime-variable so LTO cannot specialize the required
behavior away. Link actual state/assets early, using pinned LLVM-MOS and existing
`-Oz -fno-inline-functions -fno-jump-tables` policy. Retain every attempt under a
fresh output identity. If an early complete-renderer link exceeds a ceiling,
stop before dependent admission work. A link with a host/stub platform backend
is intermediate evidence only: final full-fit PASS requires the real platform
adapter, activation and fault paths, and the largest normal/stress variant.

### 2. Establish the display contract before implementing its adapter

Read and pin applicable official VIC/core register sources and their versions.
Distinguish requested output coordinates from actual timing, active area,
fetch region and pixel aspect. Derive exact scale/offset/border, screen/Color RAM
pointers, map stride/index encoding, palette bank, preconditions, masks and
readback semantics for PAL and NTSC. Local register names and older screenshots
are not proof of the requested mode. Do not issue hardware writes during this
compile-only increment.

Derive activation from real fetch/latch semantics: at least two complete lines
before first dependent fetch and selector/readback bounded below one line.
A frame edge alone is insufficient. The host transaction model must reject early,
late, missed and stale commits and handle readback failure. Initialize both
complete stores with display disabled; subsequent activation changes only the
approved screen selector. If the mapping/window cannot be justified, retain
source evidence, mark UNPROVEN and stop; no placeholder is admitted as working
hardware. Once justified, compile the narrow adapter and repeat actual full fit.

### 3. Admit static runtime and ABI only for the actual composed artifact

Trace startup, scheduler, prepared geometry, copies, selector, faults and enabled
interrupt paths. Check B=`$02`, canonical MAP state, direct-page pseudo-register
usage, call/return preservation, tail/indirect targets, recursion and every
software-SP write. Preserve reset-only/no-ROM-return behavior. Include nested
helper and interrupt/fault overhead in each stack bound; reject incomplete
analysis rather than reporting envelope allocation as proof.

Keep exact 100 Hz/21-stage CoreRuntime order. Render only when no tick is due
and a conservative service bound plus return margin fits before the next release.
At most one 64-byte physical transfer or eight raster samples per quantum;
these are work caps, not timing proof. Bound or split transform, clipping, text,
initialization and commit work as applicable. Account for actual helpers, memory
and clock assumptions, and check debt/camera/fault state between quanta.
No borrowed R0 timings, normal-world 20 Hz failure-floor waiver or promotion of
25/30 Hz targets to measurements. If static timing cannot establish a safe
bound without execution, mark it UNPROVEN and stop before runtime admission.

## Validation, ownership and handoff

Before implementation, read programming principles and C style. Keep owners:
CoreRuntime authoritative tick/checksum; Input semantic edges; Presentation
copied values; Diagnostics requested camera; Environment canonical fixture/query;
Graphics pure composition/workspace; Platform hardware/physical access.
No new dependency on R0 diagnostic policy is authorized. Existing narrow lifecycle
seams remain inherited, with their actual linked costs accounted.

Required implementation checks (not run during this planning task):

- Generated consistency and malformed-contract rejection; measured owner ledger.
- Existing 3,857 independent oracle and 841 near/far cases; prepared/legacy
  equivalence, alias/output preservation, cursor bounds and ASan/UBSan.
- Deterministic camera schedules and independent expected images frozen before
  renderer tests; full sky/ground, extreme pitch/roll, runway/anchor registration,
  label ranking/capacity, readable actual-font telemetry and NOT IMPLEMENTED labels.
- Normal/slow/cancelled/fault rendering versus render-off per-tick replay,
  including original 600-tick `DE675132`; held/full snapshot slots and injected
  cancellation/failures at every construction/ready/commit state.
- Every target variant's compile/link/map/symbol/disassembly and exact input/tool/
  artifact hashes; actual ABI/stack/service analysis and host register-model tests.

Handoff lists separate PASS/FAIL/UNPROVEN outcomes for renderer correctness,
complete-target fit, ABI/stack, service bounds and display readiness. Preserve
all failed identities. Host images are host evidence, never target screenshots.
State exact changed paths, commands, ranges, generated status and unresolved
execution tests. READY FOR REVIEW is possible for a completed compile-only
increment with explicitly deferred execution proof; an unproven required static
prerequisite is a gate stop, not a successful admission. Recommend only the next
bounded decision; do not start execution or publication automatically.

Potential future hardware edits are Platform-owned VIC geometry/pointers/palette/
border and inherited clock/input seams. Exact A/X/Y/Z/flags/base-page clobbers,
register masks, CPU versus physical addresses, restoration and deadline effects
must be enumerated before those edits. No new MAP, DMA or IRQ/NMI ownership.

## Planning-only completion

This task changes this intent and WIP only. Registers/clobbers, CPU-visible and
physical memory, MAP/base-page, DMA, timing/deadlines, IRQ/NMI, generated records,
source code and persistent state: no changes. No generator, build, host test or
target execution is needed to prepare this document. Validate links, arithmetic,
whitespace, diff scope and preservation. No Xemu, D81, SD or physical testing.
No commit, push, PR or merge. Founder decisions F1–F6 remain pending.
