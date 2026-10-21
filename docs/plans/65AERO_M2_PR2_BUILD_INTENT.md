# M2 PR2 registered display/camera — proposed Build Intent

**READY FOR REVIEW — planning only. All D1–D7 decisions below are pending.**
Prepared from verified main `a9d3f796291f2941002b4d1f4c8fc48a9dba3c89`,
[M2 PR1 #19](https://github.com/SUON1/f65-megawing/pull/19).
Local main and fetched origin/main matched; [exact-main CI](https://github.com/SUON1/f65-megawing/actions/runs/39517357784)
completed successfully. Planning branch: `codex/65aero-m2-pr2-build-intent`.
This document proposes decisions; it does not grant implementation, execution or publication authority.

## Objective, why now and authority

Integrate the approved synthetic runway/camera mathematics into a complete,
registered non-flight display while retaining M1's authoritative 100 Hz,
21-stage timeline and replay identity. PR1 now supplies independently checked
geometry; PR2 must earn integrated memory, scheduling and display coherence.

Governing references, in hierarchy:

- [Main v1.8](../../spec/core/F65_Main_Concept_v1.8_APPROVED_AMENDMENT.md),
  [Gameplay v1.2](../../spec/core/F65_Gameplay_v1.2_APPROVED_AMENDMENT.md),
  [Runtime v1.2 candidate](../../spec/core/F65_Runtime_v1.2_APPROVED_CANDIDATE_AMENDMENT.md)
  and their incorporated bases. Runtime remains NOT FINAL. Base Runtime §§6.1–6.4
  govern ownership/reserve/physical access; §10.2 governs registration.
- [Graphics v2.1](../../spec/subsystems/F-65_Megawing_Graphics_White_Paper_v2.1.pdf)
  §§2.6, 4.2, 7.3–7.6: indivisible world/record/composition, common horizon,
  deterministic anchor priority and camera isolation. Production mode remains gated.
- [Physics v4.1](../../spec/subsystems/F65_Physics_v4.1_APPROVED_AMENDMENT.md)
  and incorporated v4.0: shared canonical NED geometry; no contact implementation here.
- [Entry plan](65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md), M2 row and
  obligations S/P/D/V/E; [original M2 intent](65AERO_M2_REGISTERED_RUNWAY_CAMERA_BUILD_INTENT.md),
  approved fixture, camera, projection and numeric tolerances.
- [PR1 correction](../reports/M2_PR1_CLIPPING_P2.md),
  [PR1 schema](../../interfaces/m2_pr1.json), [PR1 ledger](../../memory/m2-pr1-ledger.json),
  [M1 schema](../../interfaces/m1_development.json), [M1 ledger](../../memory/m1-development-ledger.json),
  [M1 correction](../reports/M1_P2_CORRECTIONS.md), [workflow](../DEVELOPMENT_WORKFLOW.md).

No specification amendment, production capacity admission or historical proof
reinterpretation is proposed. The retained R0-B FCM source is a design reference,
not proof that this new display configuration works.

## Exact founder decisions

| ID | Decision requested | Recommendation |
|---|---|---|
| D1 | Approve the PR2 display/composition profile in the next section? | **Yes:** development-only 40×25 full-color 8×8 character cells, 320×128 world, 320×64 telemetry and 320×8 blank footer. Retain PR1's logical projection unchanged. No RRB, sprites, extra views or production display selection. |
| D2 | Approve the exact display allocation and immutable shared-resource policy? | **Yes:** use the existing display-owner banks `$020000–$02FFFF` and `$030000–$03FFFF`; charge 63,552 bytes per bank as below, plus 2,000 bytes shared Color RAM. Palette and color attributes are immutable after initialization. All changing visible content belongs to the hidden generation. No reserve or other owner's memory. |
| D3 | Approve the complete-generation commit and failure policy? | **Yes:** one screen-bank selector write in a verified safe raster window; latch the matching immutable record only after successful activation. Recheck camera/composition and completion immediately before activation. Keep the last complete pair on cancellation, lateness or precommit failure; reset-only fault on uncertain hardware activation. No frame-counter-only atomicity claim. |
| D4 | Approve camera integration, registration cues and bounded shedding scope? | **Yes:** preserve the approved fixture/camera envelope and controls; add independent camera commands and displayed-record corner anchors. All 17 runway segments and four corner anchors are protected. At most two optional corner labels are selected deterministically, as described below. No authoritative camera state or physics. |
| D5 | Approve integrated-fit and service admission without enlarging budgets? | **Yes:** first build gate links the actual runtime/platform/math composition under `$8000`, B=`$02`, MAP clear; retain the 4 KiB software-stack envelope and zero reserve. Cache per-generation transform and use resumable bounded raster work, proved against the independent oracle. Stop if fit, ABI or service bounds fail. No automatic bank expansion, assembly rewrite or relaxed precision/cadence. |
| D6 | Approve the evidence sequence and next implementation boundary? | **Recommend host/oracle and target compile/link/static only for the next authorization**, stopping at READY FOR REVIEW. Direct-PRG PAL/NTSC Xemu is a separate later decision after fit and scanout-contract review. Until that proof, PR2 is not visually accepted and M2 remains incomplete. No Xemu is authorized by approval of this recommended sequence. |
| D7 | Approve the change/preservation boundary? | **Yes:** new PR2 development contract, ledger, renderer/platform adapter, integration tests and fresh evidence identities; narrowly scoped reuse/refactoring of live M1/PR1 seams only where needed. Preserve historical reports, generated prior-version records, retained R0 source and all unrelated paths. No publication or next milestone authority. |

Suggested next approval text:

> Approve D1–D7 as recommended in this M2 PR2 Build Intent. Authorize the staged
> PR2 implementation and host/oracle plus target compile/link/static checks only,
> beginning with the integrated-fit gate. Stop at READY FOR REVIEW, or report a
> failed gate without enlarging scope. Preserve historical evidence and unrelated
> paths. No Xemu, D81, SD, physical testing, commit, push, PR creation or merge.

## Display and resource decision

Use FCM with 16-bit screen entries, 40 cells per row, 80-byte row stride and
25 rows. Each cell references an 8×8 tile of palette indices. This is a
proposed development profile, not inherited FCM acceptance. World logical
sample `(x,y)` maps to display sample `(x,y)` for y=0…127. Telemetry occupies
y=128…191; footer y=192…199 is blank. The physical screenshot scale, crop,
PAL/NTSC border and aspect must later be measured and recorded; do not compare
screenshot pixels directly to the PR1 logical-pixel oracle or assume square
physical pixels. No projection rescaling or changed focal length.

For each display bank, offsets are:

| Offset (inclusive) | Bytes | Responsibility |
|---|---:|---|
| `$0000–$07CF` | 2,000 | 1,000 immutable 16-bit screen entries |
| `$07D0–$07FF` | 48 | Charged alignment gap; not scratch |
| `$0800–$F7FF` | 61,440 | 960 unique 64-byte tiles: 640 world + 320 telemetry |
| `$F800–$F83F` | 64 | One immutable blank tile referenced by all 40 footer cells |
| `$F840–$FFFF` | 1,984 | Unallocated display-owner slack; no implicit new use |

Bank A therefore occupies `$020000–$02F83F`, bank B `$030000–$03F83F`.
Total charged display space is **127,104 bytes**, including 96 bytes of alignment.
The two full bank reservations remain 131,072 bytes; slack is not resident-code
capacity. Screen entries contain their own bank's physical tile-address/64,
so changing only `$D062` changes the entire pixel resource graph. Generated
validation checks alignment, character-number encoding, bounds, footer aliasing
and absence of cross-store references. Screen maps remain immutable while live.

Shared Color RAM: `$0FF80000–$0FF807CF`, 2,000 bytes, initialized with the
FCM-compatible neutral attributes and then immutable. Exact attribute encoding
must be source-grounded and checked in the platform admission table before
hardware code is changed; no live per-cell color updates. Use one fixed palette
with explicit roles: black background, blue sky, green ground, white runway/text,
and yellow diagnostic anchors. Use nonzero pixel indices for all painted
samples to avoid relying on transparent-index semantics. Initialize/read back
palette bank and RGB values before first display eligibility; freeze them for
the entire run. Border is fixed except a declared fatal indicator.

Rasterize text into the hidden telemetry tiles using a small owned bitmap font.
Keep `NON-FLIGHT`, generation/source tick, checksum, camera revision/height above
test datum, source age and fault/rejection/cancellation counters readable. With
40 text columns, put `ALTITUDE: NOT IMPLEMENTED` left-aligned on one line and
`AIRSPEED: NOT IMPLEMENTED` right-aligned on another; do not substitute camera
height or camera movement for flight readings. All telemetry in a generation
is labelled as captured at its construction start; it may remain stale with the
old complete frame. No live overlay can corrupt the visible generation.

This choice avoids mutable shared glyphs/color/palette and stays inside the
existing display-owner banks. M1 character-only output cannot meet PR1's
pixel tolerances. RRB, multi-layer overlays and DMA would add unnecessary
contracts; none is proposed for this bounded wireframe runway increment.

## Complete-generation transaction and ownership

Environment remains sole runway/query owner. InputEngine emits semantic camera
edges separately from M1 authoritative input. Diagnostics owns camera state;
Graphics owns raster policy and immutable registration bundles; Presentation
supplies copied snapshot values; Platform alone accesses registers/physical RAM.

Capture one legal immutable snapshot, camera revision, fixture/projection/view/
tier/composition identity and destination generation. Release the source slot
after copying; never hold it throughout raster construction. Prepare a bounded
bundle containing the PR1 registration record and four projected corner anchors
with explicit visible/clipped status. Generate the new bundle layout rather
than hand-copying PR1 public layouts. Introduce a distinct PR2 schema/ledger;
retain the prior schemas and original generated records as versioned inputs.

All 17 canonical segments and the four spatial anchors are required when
visible. Optional labels for the four corners are ranked by declared priority
then stable corner ID; capacity is two. Tests offer the same candidates in
permuted orders, force a higher-ranked arrival after lower-ranked candidates,
and confirm the protected set cannot be evicted. Label omission never moves
or drops the runway/anchor geometry. This is bounded M2 ranking evidence,
not production object/LOD pressure acceptance.

Render exclusively into the hidden tiles. Completion covers world, telemetry,
anchors and the registration bundle. A new camera request invalidates unfinished
or ready-but-uncommitted work. Before activation, revalidate desired camera,
all identities, completion and destination. On a single-threaded dispatcher,
perform the platform commit and displayed-bundle publication without yielding;
no IRQ/NMI reader may observe an intermediate software publication.

Initialize both complete stores before enabling the display. For later commits,
keep `$D060/$D061` at zero and the relevant `$D063` address bits fixed; only
`$D062` changes between 2 and 3. A frame-counter transition alone is insufficient.
The platform contract must identify the actual PAL/NTSC pre-fetch raster window,
mode geometry and fetch/latch semantics from pinned documentation/source.
Require at least two complete raster lines of margin before the first dependent
fetch and a compiled selector/readback critical path bounded below one line in
both modes. Poll without blocking authoritative ticks; defer if outside the
window. This is a proposed admission criterion, not an already established
hardware fact. If the window or fetch semantics cannot be established, stop
before enabling scanout. No new raster IRQ is authorized as a workaround.

A precommit validation/copy failure leaves the old complete pair untouched and
records the rejected attempt. An uncertain selector write/readback is fatal:
do not claim rollback or continue with mismatched software identity. Preserve
the failure evidence and require reset. Wrap/exhaustion of revision/generation
identifiers also fails closed rather than aliasing a stale generation.

## Integrated fit and bounded service

Evidence now available is deliberately separate: M1 slow-render resident end
`$4938`; corrected PR1 standalone probe end `$7466` (2,970 bytes below `$8000`),
25 hardware-stack bytes, 16 dynamic software-stack bytes, 471 bytes compiler
static scratch and 119-byte registration. These are **not additive allocations
or an integrated fit proof**: toolchain runtime helpers may overlap, startup
contracts differ, and actual new owner state must be linked and charged.

**Gate A — before building the complete renderer:** link the actual M1 runtime,
input/snapshot, narrow Platform lifecycle and corrected M2 arithmetic through
an M2 integration entry point; exclude both old diagnostic mains and unused test
harness arrays. Use the pinned LLVM-MOS toolchain, existing reset-only B=`$02`,
MAP-clear seam and ROM-call exclusion, not PR1's unadmitted SDK runtime contract.
Check arithmetic helpers, compiler pseudo-register accesses and stack-relative
code in the resulting disassembly. Unknown clobbers or ABI behavior stop admission.

Retain CPU resident `$2001–$7FFF`, hardware stack `$0100–$01FF`, base page
`$0200–$02FF`, software stack `$C000–$CFFF`, and declared platform result/startup
ranges. Retain the source-pinned M1 ROM-backup lifecycle, including Attic backup
`$08000000–$0801FFFF` and initialization-only `$09E0–$0A14` writes. These are
inherited seam obligations, not new scratch. No allocation in other Runtime
owner bands, no MAP window extension and no `$058000–$05FFFF` reserve draw.

**Gate B — complete composition:** relink with actual camera/input state,
registration bundles, projected anchors/lines, resumable cursors, font/table
bytes, bounded tile staging, guard bytes and compiler scratch. Report all
sections, padding and per-owner symbols, plus call-graph hardware/dynamic
software-stack bounds (including platform and interrupt/fault context).
Do not count static `.noinit` scratch twice as dynamic stack. Reject overflow
before producing an execution-admitted artifact. Gates A/B are provisional
static evidence; exercised high-water still awaits separately authorized execution.

Use one transform per captured camera generation. Do not call the existing
camera-to-transform path once per ground pixel. Permit narrow pure Graphics
refactoring to accept a prepared transform and resumable raster state, with
old PR1 API behavior retained and all 3,857 original plus 841 near/far cases
rechecked against the unchanged independent oracle. An incremental horizon
classifier must match the PR1 ray convention and its full-sky/full-ground cases;
no lower-precision arithmetic or fixed horizontal split to save time.

Split background/line/HUD construction into bounded continuations. Initial
engineering caps: at most one 64-byte tile transfer or eight pixel samples per
service quantum; expensive transform/clip operations need separate measured or
conservatively bounded quanta. These are ceilings, not a throughput assertion.
Service only when no authoritative tick is due and the worst-case quantum plus
return margin fits before the next release; otherwise defer. Check tick debt,
cancellation and faults between quanta. No heap, recursion, unbounded busy wait,
whole-frame copy or synchronous 17-segment batch in the slack dispatcher.

100 Hz/21-stage ordering and the existing sustained 20 Hz normal-world failure
floor remain unchanged; 25/30 Hz remain targets. Deliberately slowed/cancelled
fault cases are labelled stress evidence, not nominal cadence passes. No new
maximum source-age number is invented here: report age/construction/camera
latency distributions; founder limit approval remains at its owning gate.
If the proposed CPU-copy profile cannot meet normal cadence and protected
service, retain the evidence and return for a revised Build Intent—do not add
DMA, lower precision, enlarge memory or waive cadence automatically.

## Hardware impact proposed for later implementation

Planning itself changes none of these. Before the first hardware source edit,
publish the exact masked register writes, old/new mode values and helper
clobbers in the PR2 platform contract and validator:

- Display mode/geometry: `$D011`, `$D016`, `$D018`, `$D031`, `$D054`, row stride
  `$D058/$D059` and applicable geometry controls. Preserve unrelated bits;
  unexpected inherited mode fails admission. R0-B used `$D031` bit 7 clear and
  `$D054` low bits set for its bounded FCM proof; that is reference, not a
  sufficient complete PR2 configuration. Any additional register must be
  justified/documented before use, never an exploratory write on a live target.
- Screen pointer `$D060–$D063`; color pointer `$D064/$D065`; palette selection
  `$D070` and required RGB entries in `$D100–$D3FF`; border/background
  `$D020/$D021`. Initialization only except the one-byte screen selector and
  fatal border indication. No RRB or sprite controls.
- Read-only raster/frame/video-standard observations and inherited CIA clock.
  Input uses the narrow keyboard row/bit seam (`$D614/$D613`); document the
  exact row mask and restore/select behavior. Propose W/S north, A/D east,
  R/F height, J/L yaw, I/K pitch, U/O roll, Home reset; retain Space for the M1
  command. Preserve one step per press edge, cancel opposing simultaneous
  commands, reset precedence and visible out-of-envelope rejection.
- CPU C ABI and physical-copy assembly clobbers must be checked against the
  actual linked helpers. No application-owned MAP/base-page changes. No new
  DMA descriptors/submission, IRQ/NMI handlers or interrupt masks. Retain
  existing platform fault/NMI detection and reset-only lifecycle; no ROM return.
- No persistent storage or serialized aircraft state. Replay/control traces and
  evidence files are host artifacts only. No physical timing acceptance claim.

## Validation, work scope and completion

The next authorized build, if D1–D7 are accepted, changes only PR2 contract/
generator/ledger, Graphics/Environment-facing integration, diagnostic camera,
Input/Presentation seams as needed, a narrow M2 Platform adapter, its entry point,
validators and tests. Preserve R0 implementations; reuse their declared narrow
primitives without pulling diagnostic policy into the new owners. Keep shared
logic shared and the oracle independent. Use fresh output paths; never rerun a
builder that overwrites a retained M1 or PR1 evidence identity.

Required host/static checks:

1. Exact generated bytes, address non-overlap, tile/index bounds, immutable
   shared resources, resource accounting and malformed-contract rejection.
2. Independent projection/raster/horizon comparison, all PR1 regressions,
   full/empty sky cases, near/far clipping and complete composed-frame checks.
3. Per-tick authoritative replay equality with graphics off/normal/slow/cancelled
   and differing camera scripts; retain checkpoint `DE675132` for the original
   600-tick authoritative stream. Press/hold/release and camera-limit tests.
4. Generation mismatch, stale ready frame, cancellation at every service state,
   failed transfer, unavailable commit window, failed selector, wrap and retry
   cases; visible bytes/record stay unchanged until a valid complete commit.
5. Snapshot held-reader/full-slot rejection and release behavior; ranked optional
   label permutation/overflow tests; required anchors survive pressure.
6. Target compile/link Gates A/B, map/symbol/disassembly, actual ABI and stack,
   bounded work and forbidden hardware-operation checks. ASan/UBSan host runs.

**Not authorized now or by recommended D6:** Xemu. A later explicit authorization
must pin PRG/schema/toolchain/emulator/ROM and run direct-PRG PAL/NTSC normal,
slow/cancelled, camera-change and safe failure cases. Capture actual complete
sky/green-ground/runway/telemetry screenshots, exact logical-to-screen mapping,
registration overlays from the displayed record, timing/stack high-water and
scanout coherence evidence. Inspect screenshots, not just counters. Host mocks
and a one-byte write alone cannot prove hardware atomicity. Any remaining
physical uncertainty remains named for its later owner gate; physical testing
is never inferred from emulator approval.

No aircraft/contact/FCS, audio, production graphics freeze, full-harness PASS,
D81, SD, physical testing, publication or M3 work. Build completion is a scoped
READY FOR REVIEW handoff or a failed-gate report. Visual M2 acceptance remains
open until the separately authorized execution and founder inspection.

Planning completion: only this plan and WIP change. Main is verified; all 20
unrelated entries and 790 captured preservation fingerprints remain unchanged.
Documentation/link/whitespace, allocation arithmetic and scope checks are the
only new validation tier. No generator, target compiler, emulator or hardware
execution was used for this planning task. Founder decisions remain pending.
