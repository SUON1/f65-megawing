# M2 PR2 full composition and static admission — proposed Build Intent

**READY FOR REVIEW — planning only; N1–N6 below are pending.**
Baseline: verified main `0d42a8ce271a98abbffada019c403e31e7590e5d`,
[PR #20](https://github.com/SUON1/f65-megawing/pull/20).
Fetched origin/main and local main agree;
[exact-main CI](https://github.com/SUON1/f65-megawing/actions/runs/39550981545)
passed. Branch: `codex/65aero-m2-pr2-admission-intent`.
No implementation or execution is authorized by this document.

## Objective and why now

Replace the reachability-only fit claim with an actual bounded PR2 composition:
canonical runway and camera, complete hidden world/telemetry image, immutable
registration bundle, resumable construction, and a narrowly owned platform
adapter. Establish full-composition memory and static runtime/display readiness
using host/oracle and target compile/link evidence. Stop before execution.

The current probe ends at `$7E85`, leaving **379 bytes** below `$8000`. That
measurement includes one fixed-camera probe, not a full renderer, font, input
handling or scanout path. Its 16-byte cursor saves workspace; it does not prove
that the next increment fits or meets deadlines. A fixed probe's compiler
specialization is not a substitute for linking variable runtime camera state.

## Authority and inherited decisions

- [Main v1.8](../../spec/core/F65_Main_Concept_v1.8_APPROVED_AMENDMENT.md),
  [Gameplay v1.2](../../spec/core/F65_Gameplay_v1.2_APPROVED_AMENDMENT.md),
  [Runtime v1.2 candidate](../../spec/core/F65_Runtime_v1.2_APPROVED_CANDIDATE_AMENDMENT.md)
  and incorporated bases: unchanged owner boundaries, 100 Hz/21-stage timeline,
  immutable snapshots, memory ownership and protected reserve. Runtime is NOT FINAL.
- [Graphics v2.1](../../spec/subsystems/F-65_Megawing_Graphics_White_Paper_v2.1.pdf)
  §§2.6, 4.2, 7.3–7.6: complete world/registration/composition pair, common horizon,
  camera isolation and protected anchors. [Physics v4.1](../../spec/subsystems/F65_Physics_v4.1_APPROVED_AMENDMENT.md)
  and incorporated v4.0 preserve canonical fixture/query geometry.
- [Entry plan](65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md), M2 and S/P/D/V/E
  obligations; [original M2 intent](65AERO_M2_REGISTERED_RUNWAY_CAMERA_BUILD_INTENT.md).
- [PR2 intent](65AERO_M2_PR2_BUILD_INTENT.md), approved D2–D7 and clarified D1;
  [fit report](../reports/M2_PR2_INTEGRATED_FIT.md) records the founder's explicit
  choice of **lower-resolution backing scaled within high-resolution output**.
- [Size-reduction handoff](../reports/M2_PR2_SIZE_REDUCTION.md),
  [PR1 generated contract](../../interfaces/m2_pr1.json),
  [M1 ledger](../../memory/m1-development-ledger.json),
  [PR1 ledger](../../memory/m2-pr1-ledger.json), and [workflow](../DEVELOPMENT_WORKFLOW.md).

Retain Q12 public positions, Q24 clipping, Q46 rotation, Q16 projected coordinates,
320×128 logical world projection, 0.5-pixel projection/one-pixel raster tolerances,
fixture/camera envelopes, semantic press edges and non-flight labelling. No
superseded plan/report is rewritten. This intent is a new proposed increment,
not retrospective approval of full PR2 or a production graphics profile.

## Exact founder decisions and recommendations

These identifiers are new; they do not reopen approved D1–D7.

| ID | Decision requested | Recommendation |
|---|---|---|
| N1 | What is the next bounded implementation deliverable? | **Approve full host composition plus the real target composition compiled/linked only**, in the gate order below. Include normal, slow/cancelled and failure-test variants. Stop at READY FOR REVIEW or the first failed admission gate; no automatic execution or publication. |
| N2 | How should the 379-byte margin constrain implementation? | **Keep all existing ceilings and owner ranges.** Permit bounded pure-C code sharing/prepared-transform reuse and removal of probe-only scaffolding, with measured relinks. Charge every actual state, font/table, staging byte, padding and stack contribution. Do not fit by dropping required behavior, allocating other-owner bands, consuming reserve or moving code into display slack. |
| N3 | Admit the prepared-camera and resumable renderer design below? | **Yes.** Prepare one validated immutable camera/transform per generation, preserve existing API behavior, and use the cursor for bounded work. Prove prepared and legacy paths against the independent oracle. Retain all 17 runway segments/four protected anchors and deterministic capacity-two optional labels. |
| N4 | What exact scaling/composition should the display contract target? | **Recommend integer 2× scaling of the 320×200 backing to 640×400**, centered in the requested 720×480 or 720×572 output reference canvas. That means offsets (40,40) or (40,86), with unchanged logical world projection. Source-ground and validate the actual timing/active-area mapping before hardware code; do not silently replace PAL 572 with 576 or assume the requested canvas is a supported native timing. Stop on unsupported/ambiguous mapping. |
| N5 | What counts as runtime/display admission in this slice? | **Static readiness only:** actual call-graph/stack/base-page/physical-access checks and a source-pinned register/scanout contract with fail-closed host tests. Require explicit unresolved execution checks in the handoff. Do not infer safe scanout, exercised high-water, nominal cadence or visual acceptance from compilation. |
| N6 | Which testing and publication boundaries apply? | **Host/oracle/sanitizers and target compile/link/static only.** No Xemu, D81, SD, physical testing, commit/push/PR/merge or later milestone. Any later direct-PRG PAL/NTSC execution needs separate authorization for the reviewed artifact and outstanding gates. |

Suggested approval text:

> Approve N1–N6 as recommended. Build the bounded M2 PR2 full composition and
> static-admission increment in gate order, preserving precision, required
> behavior, memory ownership and evidence. Run host/oracle and target
> compile/link/static checks only. Stop at READY FOR REVIEW or a failed gate;
> do not expand budgets or change the output mapping silently. No Xemu, D81,
> SD, physical testing or publication.

## Gate 1 — complete owner/state and resource contract

Before implementation, create a distinct generated PR2 development contract and
ledger. Reference existing generated PR1 records; do not hand-copy their layouts
or rewrite their historical identity. Document new bundle/state layout, validity,
generation/revision wrap handling and owner lifetime. Graphics owns transient
raster workspace; Environment remains the sole fixture/query owner. Diagnostics
owns the camera, InputEngine semantic edges, CoreRuntime authoritative tick and
checksum, Presentation copied values, and Platform all hardware/physical access.

The final ledger must include at least: displayed and in-construction registration
bundles and anchors, requested/captured camera, copied snapshot, projected-line
or cursor state, generation/cancellation counters, input edge state, font/table
bytes, tile staging, guard policy and compiler scratch. Report each object's
actual placement and lifetime; count shared bytes once only. If reuse is claimed,
prove lifetimes cannot overlap, including failure and cancellation paths.

Retain CPU resident `$2001–$7FFF`, hardware stack `$0100–$01FF`, base page
`$0200–$02FF`, software-stack envelope `$C000–$CFFF`, declared platform result
and initialization ranges, and the existing ROM-backup lifecycle. Preserve
initialization-only `$09E0–$0A14` writes and Attic backup `$08000000–$0801FFFF`.
No new allocation in the active-simulation/audio/workspace/staging owner bands;
no `$058000–$05FFFF` reserve draw. Stack envelope is not stack proof.

Retain the approved per-display-bank layout in `$020000` and `$030000`:
2,000-byte screen map, 48-byte alignment, 61,440-byte changing tiles, 64-byte
blank tile = **63,552 bytes each**. The final 1,984 bytes per bank stay unallocated.
Shared 2,000-byte Color RAM and global palette are initialized once then immutable.
No new DMA, RRB, sprite or mutable shared-color path. Font bytes must be charged
where actually resident; do not hide them in unallocated display slack.

Gate result: generated layout, owner ledger, invariant/rejection tests and a
clear complete-composition bill of materials. No final-fit PASS from estimates.

## Gate 2 — prepared geometry and full host renderer

Prepare the validated camera position and Q46 transform once per captured
generation. A prepared object must bind camera revision, fixture/projection and
composition identity, not accept an arbitrary caller-supplied matrix as valid.
Use a private validated owner object or a generated immutable contract; either
way reject stale/malformed contexts and preserve the old public API's failure
behavior. Do not rerun full transform validation at every pixel. Retain exact
rounding, clip ambiguity and finite-output rules; no reduced-width shortcut.

Implement resumable transform/clip/raster/background/HUD work. Reuse the existing
cursor; no reintroduced 320-element pixel array. Background classification must
agree with the existing camera ray/horizon convention, including fully sky or
ground and extreme pitch/roll. A recurrence/scanline optimization needs numeric
bounds and oracle evidence before use; do not silently move the horizon.

Render the complete 320×128 world and 320×64 telemetry, with an immutable blank
8-row footer. Show blue sky/green ground, all visible required runway marks,
registered corner cues, NON-FLIGHT, checksum/tick/generation/camera/source-age
and fault/cancellation counters. ALTITUDE and AIRSPEED remain NOT IMPLEMENTED;
camera height is labelled above test datum. Font, strings and conversion code
must be the actual target assets, not a host-only richer substitute.

Host memory backend exposes exactly two display stores and immutable shared
resources. A transfer writes only the hidden store. Copy/release one legal
snapshot; the renderer must not hold a Core snapshot throughout construction.
Cancellation or a new camera revision invalidates pending work; old complete
world, record and composition remain visible. Recheck identity/completion at
commit. Required anchors cannot be evicted by the two optional ranked labels.
A failed selector/readback is a fatal uncertain-activation state, not a claimed
rollback. Null/malformed input, overflow and revision exhaustion fail closed.

Freeze deterministic camera/control schedules and independent expected cases
before implementation tests. Verify per-tick replay identity against rendering
off/normal/slow/cancelled, with changed camera scripts and preserved original
600-tick checkpoint `DE675132`. Inject failures and cancellation at every
continuation/ready/commit state; test full-slot and held-reader behavior, rank
permutation/replacement and output/resource bounds. Host composed images are
host evidence only and never described as target screenshots.

## Gate 3 — actual integrated link, ABI and bounded service

Replace the fixed-camera reachability probe with the actual target composition
root. Keep runtime camera/input mutable and all required functionality reachable;
exclude probe digest code and old entry points, not required runtime behavior.
Link all normal/stress variants with pinned LLVM-MOS and reviewed `-Oz
-fno-inline-functions` policy. Preserve every attempt under a fresh output ID.
The largest variant must fit all ranges; report actual per-owner symbols,
section gaps, assets and compiler scratch. No sum of standalone maps or
specialized fixed-camera probe is accepted as full-composition fit.

Static ABI admission must trace from startup through the actual scheduler,
geometry helpers, physical copies, commits, faults and enabled interrupt context:
B=`$02`, canonical MAP state, correct direct-page pseudo-register usage, stack
adjustments, call/return preservation and the reset-only no-ROM-return boundary.
Check reachable calls, recursion, indirect targets, tail transfers and every
software-SP write. Reject unknown writes/targets or an incomplete model; do not
relabel an unsupported checker path PASS. Include nested helper stack cost,
interrupt/fault overhead and compiler static scratch separately. Verify upper
bounds against both stack envelopes; dynamic high-water remains unmeasured.

CoreRuntime keeps the exact 100 Hz/21-stage order. Render service runs only when
no tick is due and its conservative worst-case bound plus return margin fits
before the next release. At most one 64-byte physical transfer or eight raster
samples per service quantum; these caps are not timing proof. Expensive transform
and clip work must be resumable or have a justified bound, not hidden inside
one oversized quantum. Account for helper calls, memory access and platform
clock assumptions. Check debt/camera cancellation/faults between quanta.
If a safe conservative service bound cannot be established without execution,
mark that gate unresolved and stop before runtime admission; never borrow the
old R0 timing measurements as a new renderer budget.

No normal-world 20 Hz failure-floor waiver; 25/30 Hz remain targets. Static
analysis may establish infeasibility, but does not establish measured cadence,
source-age distributions or input latency. Slowed fault profiles do not count
as nominal cadence passes. Failure to fit or to preserve required service is a
stop with the map/analysis and a smallest follow-up proposal, not automatic
allocation/precision changes or an unbounded optimization campaign.

## Gate 4 — source-pinned display contract, compile only

The selected backing is unchanged. Proposed mapping for logical sample (x,y)
is a 2×2 output block with upper-left `(40+2x,40+2y)` in a 720×480 reference
canvas, or `(40+2x,86+2y)` in a 720×572 reference canvas. World occupies only
backing rows 0–127; telemetry and footer keep the same generation. Record pixel
aspect separately. These are requested composition coordinates, not a claim
about existing VIC timing, emulator capture size, overscan or monitor scaling.

Before changing hardware source, pin the applicable official register/core
reference and derive a complete PAL/NTSC mode table: timing vs active region,
scale/offset/border values, fetch geometry, screen stride/index encoding, Color
RAM attributes, palette roles/bank, reset/preconditions, exact masked writes
and readback semantics. Local SDK register names and historical FCM proofs are
references, not sufficient proof of new mode behavior. If the hardware cannot
express the requested mapping, return the discrepancy to the founder; do not
substitute 576, stretch the projection or treat screenshot cropping as hardware
implementation without a separately approved change.

Retain immutable screen maps referencing each store's own tiles. Initialize both
complete stores while display is safely disabled. Subsequent activation changes
only the screen-bank selector, guarded by fresh complete-generation identity.
Derive the PAL/NTSC raster window from actual fetch/latch semantics, with at least
two complete lines before first dependent fetch and a selector/readback path
bounded below one line. Do not infer safety from a frame-counter edge or from
one-byte write width alone. Host tests cover early/late/missed windows and
readback failure; no new raster IRQ workaround. An unproved window blocks
activation readiness even when compilation succeeds.

Expected hardware owner remains Platform: VIC mode/geometry controls, screen and
color pointers, palette and border/background; raster/frame observations and
inherited CIA clock; keyboard acquisition seam. The exact table must enumerate
all registers/masks, A/X/Y/Z/flags/base-page clobbers, CPU vs physical addresses,
restoration/reset behavior and timing effects before hardware edits. No new MAP,
DMA or IRQ/NMI handler/ownership. Pure Graphics never acquires hardware access.

## Validation and handoff boundary

Required implementation evidence (only after N1–N6 approval):

- Generated consistency, malformed-contract rejection and complete memory ledger.
- Original 3,857 independent oracle cases and 841 near/far cases, plus prepared-
  context equivalence, full-background/camera cases and composition/cancellation
  properties. Sanitizers, cursor state checks and deterministic replay.
- All target variants' compile/link/map/disassembly, actual owner accounting,
  call-graph/stack/ABI analysis, physical-access and service-bound admission.
- Pinned display mode table and host register/transaction model with explicit
  hardware uncertainties. No model is counted as real scanout evidence.

Handoff must classify each gate PASS, FAIL or UNPROVEN, name the exact artifacts,
and retain failures. A successful compile-only increment may be READY FOR REVIEW
while execution/visual gates remain UNPROVEN; it must not be called runtime-safe,
M2 complete, exercised timing/stack PASS or visually accepted. A failed prerequisite
stops dependent work, with independent completed evidence retained.

Later execution is separately authorized: exact-PRG PAL/NTSC startup, real
scanout atomicity, screenshot mapping/readability, controls, cancellation/faults,
stack high-water and nominal cadence/age/latency. Physical acceptance remains
its own gate. This intent authorizes none of those tests.

## Non-scope and planning completion

No native large framebuffer, production resolution freeze, aircraft/contact/FCS,
audio/storage, new assembly optimization, reserve draw, other-owner allocation,
full-harness PASS, Xemu, D81, SD, physical testing or publication. Preserve R0
proof source, all evidence and earlier generated identities. Further milestones
are outside this increment.

**This planning task:** new intent and WIP only. Registers/clobbers, CPU/physical
memory, MAP/base-page, DMA, timing/deadlines, IRQ/NMI, generated interfaces and
persistent state: no changes. Main was verified; 846 captured file fingerprints
and all 20 unrelated entries are preserved. Validation is links, whitespace,
scope, mapping arithmetic and preservation only; no build/generator or target
execution. Founder decisions N1–N6 remain pending.
