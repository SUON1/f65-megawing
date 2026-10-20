# M2 registered runway/camera — proposed Build Intent

Status: READY FOR REVIEW — planning only; no M2 implementation or execution authorized.
Prepared from verified main `2acd30c21a4be0996cd1a2dd3ce74da6deb6c84d` (M1 PR #18).
Local main and fetched origin/main agree; [exact-main CI](https://github.com/SUON1/f65-megawing/actions/runs/39500308794) passed. Planning branch: `codex/65aero-m2-build-intent`.

## 1. Objective and authority

Extend the non-flight foundation with one synthetic, canonically defined runway, a movable diagnostic camera, and a complete displayed world paired with its exact registration record. Demonstrate geometric registration and camera/render independence without claiming flight, contact, physical display qualification or production limits.

Governing references:

- [Entry plan §6, M2 row and shared geometry](65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md#6-minimum-architecture-and-executable-milestones): PR1 pure transform/clipping/registration plus oracle; PR2 bounded renderer/camera integration. Geometry and tolerances need founder approval.
- [Main v1.8](../../spec/core/F65_Main_Concept_v1.8_APPROVED_AMENDMENT.md) and incorporated v1.7: progressive development profile, unchanged owner boundaries and tick order.
- [Gameplay v1.2 §21.10](../../spec/core/F65_Gameplay_v1.2_APPROVED_AMENDMENT.md): visibly non-flight; absent flight states marked NOT IMPLEMENTED.
- [Runtime v1.2 candidate](../../spec/core/F65_Runtime_v1.2_APPROVED_CANDIDATE_AMENDMENT.md), incorporated Runtime v1 §§10.2 and generated-interface requirements: canonical environment geometry and displayed-generation registration; candidate remains NOT FINAL.
- [Graphics v2.1](../../spec/subsystems/F-65_Megawing_Graphics_White_Paper_v2.1.pdf) §§2.6, 4.2, 7.3, 7.5–7.6: complete world/record/view pair, shared horizon, camera isolation; production resolution/composition and measured limits remain gated under current controlling parents.
- [Physics v4.1](../../spec/subsystems/F65_Physics_v4.1_APPROVED_AMENDMENT.md), incorporated v4.0 §§2.3, 10: NED and canonical geometry, visual/query registration. M2 does not implement contact.
- [M1 correction handoff](../reports/M1_P2_CORRECTIONS.md), [development schema](../../interfaces/m1_development.json), [ledger](../../memory/m1-development-ledger.json), [workflow](../DEVELOPMENT_WORKFLOW.md).

No governing document is amended by this plan. All new numeric choices below are **proposed test-only values**, not existing requirements, measured capabilities or production defaults.

## 2. Findings from the integrated seam

M1 has an 80×25 character renderer, two 2000-byte screen stores, row-static colors, a one-key input sample and a snapshot containing tick/commands/checksum/fault only. It has no runway query, projection, camera identity, pixel raster or generated world-registration record. Its fixed profile deliberately rejects configuration drift. Replacing literals or relabelling character cells as pixels would not implement M2.

M1 swaps screen-bank selection; shared color RAM is not generation-buffered. A moving horizon/runway cannot mutate visible colors during an incomplete frame. Before PR2 writes target display code, its concrete development display contract must show how every visible dependent resource (pixels/glyphs, color, palette and composition) remains stable until the matching complete generation becomes eligible. Do not infer that the existing swap automatically provides that guarantee.

The M1 slow-render image ends at `$4938`, under its `$8000` resident ceiling; BSS+noinit is 820 bytes and emulator stack maxima are 31/28 bytes. These are M1 observations, not an M2 allocation or timing budget. M2 must earn its own map, bounded work and high-water evidence. Preserve the M1 reports, packets and raw outputs unchanged.

## 3. Exact founder decisions and recommendations

All six decisions are pending. They can be approved together as the bounded recommendation below; none is inferred from this planning request.

| ID | Decision requested | Recommendation and consequence |
|---|---|---|
| D1 | Approve the M2 non-flight objective and two-slice sequence? | **Yes. Authorize only PR1 implementation next**, stopping at READY FOR REVIEW. PR2 is prepared here but starts only after PR1 review and a concrete display/resource contract. No automatic commit, push, merge or next milestone. This follows the entry plan and avoids approving an uninspected hardware mode. |
| D2 | Admit the exact synthetic runway fixture in §4? | **Yes: `M2-RWY-TEST-1`**, 6000 ft × 150 ft, flat local NED datum, endpoints and markings below. This is test geometry shared by Environment and Graphics, not a real airport or aircraft datum. Later contact must consume this revision or explicitly version a replacement. |
| D3 | Admit the diagnostic camera and control envelope in §5? | **Yes: `M2-CAMERA-TEST-1`**, independent presentation-only position/orientation, reset pose and discrete controls below. Retain ALTITUDE/AIRSPEED NOT IMPLEMENTED; show camera height separately as test data. No chase/cockpit aircraft behavior is implied. |
| D4 | Approve the registration acceptance bars in §6? | **Yes:** exact fixture identity and generation coherence; at most 0.5 logical pixel numeric projection error, at most 1 logical pixel raster-boundary error, and no partial or mismatched display. These are proposed pass/fail criteria, not an assertion that M2 already meets them. If unattainable, return measured evidence; do not loosen them silently. |
| D5 | Admit a bounded development projection/raster profile without freezing production graphics? | **Yes for PR1's logical 320×128, square-sample, 90° horizontal-FOV profile.** Defer selection of the physical VIC-IV mode, viewport placement and store/color layout to the PR2 contract review. Target compile/link of the math is included in PR1; a logical host raster is not target-visible acceptance. |
| D6 | Which execution and evidence tiers may the next slice use? | **PR1: host tests, independent oracle, generated checks and target compile/link only.** No emulator execution now. At PR2 admission, separately authorize direct-PRG PAL/NTSC Xemu for camera/render proof, then stop at READY FOR REVIEW. No D81, SD or physical testing in either proposed slice; no publication authority is included. |

Recommended approval text:

> Approve D1–D6 as recommended in this plan, including the specified test-only fixture, camera envelope and registration criteria. Authorize M2 PR1 pure geometry/projection/registration implementation, host/oracle checks and target compile/link, stopping at READY FOR REVIEW. Do not start PR2 or run Xemu until its concrete display/resource contract is reviewed and separately authorized. Preserve all historical evidence and unrelated paths. No D81, SD or physical testing; no commit, push or merge.

## 4. Proposed fixture: M2-RWY-TEST-1

Use one versioned authoring source, then generated C/host bindings; no duplicate hand-authored runway corners in Graphics. Environment owns the read-only fixture/query. Units are feet; NED axes follow Physics §2.3. Datum `(N,E,D)=(0,0,0)` is the runway center, on a synthetic flat plane; its elevation is zero **relative to this local datum**, not MSL or a geodetic claim.

- Centerline endpoints: `(-3000,0,0)` and `(3000,0,0)`; northbound heading 000°.
- Four rectangle corners: `(-3000,-75,0)`, `(-3000,75,0)`, `(3000,75,0)`, `(3000,-75,0)`.
- Threshold markings: full-width lines at N = -2900 and +2900 ft.
- Centerline markings: eleven 100-ft segments centered at N = -2500, -2000, …, +2500 ft, E = 0. These are synthetic registration marks, not compliant airport markings.
- Geometry is planar and stationary. Surface query returns datum identity, plane elevation, and rectangle membership, not friction, tire forces, collision impulses, gear or physical contact.
- No carrier, curved Earth, terrain tiles, airport asset loader, runway number text or resource streaming.

The generated fixture manifest pins source bytes, units, datum, revision and bounded geometry counts. Missing/unknown revision, non-finite input, invalid dimensions or inconsistent units reject admission; never fall back to a different runway.

## 5. Proposed camera and projection profile

Camera axes are +X forward, +Y right, +Z down. Camera-to-NED attitude uses a Hamilton scalar-first quaternion or a generated equivalent rotation derived from that declared convention. Positive yaw turns right, positive pitch looks up, positive roll lowers the right side. World-to-camera uses the inverse transform; no flight state is created.

- Reset: N=-4500 ft, E=0, D=-300 ft; yaw=0°, pitch=-5°, roll=0°.
- Position envelope: N ∈ [-12000,12000] ft, E ∈ [-6000,6000] ft, height above fixture plane ∈ [10,3000] ft (D = -height).
- Orientation: yaw wraps modulo 360°; pitch and roll each bounded to [-60°,60°]. These are camera test limits, not aircraft limits.
- Camera commands: ±25 ft north/east, ±10 ft height, ±1° yaw/pitch/roll, and reset; one step per semantic press edge. Held keys do not accelerate. Opposing commands cancel within one sampled input batch; reset takes precedence. Out-of-envelope steps reject visibly and leave the camera unchanged. Keyboard mapping is an implementation detail documented before target execution.
- Projection: 320×128 logical samples with centers at integer coordinates; principal point `(159.5,63.5)`, focal scales `fx=fy=160`; nominal horizontal field of view 90°. Clip to x ∈ [-0.5,319.5], y ∈ [-0.5,127.5]. Near forward distance 10 ft; far forward distance 40000 ft. Clip before perspective divide; nonpositive/invalid depth never reaches division. Screen x increases right, screen y down.
- Sky/ground split derives from the same camera/projection as the runway. Pitch/roll and off-center views must not leave a fixed horizontal M1 color boundary. Ground-plane horizon singularities and a fully sky/ground viewport have defined bounded results.

InputEngine emits diagnostic camera commands separately from authoritative M1 commands. Diagnostics owns camera state; commands acquire a monotonic camera revision. Capture one camera revision, fixture revision, projection revision and immutable snapshot for each render attempt. Camera motion never changes simulation tick order, authoritative commands or checksum. “Camera height: … FT ABOVE TEST DATUM” is separate from the flight altitude field. World-registered anchors use the displayed record, never the latest camera.

## 6. Proposed acceptance criteria

Before implementation tests, freeze cases and the independent oracle equations. Host reference uses high-precision arithmetic independent of target transform/clipping/raster functions; shared fixture inputs and schema are allowed. Include general points within the envelope, not only the rectangle's four corners.

1. **World registration:** query and rendering consume identical generated datum, endpoints, width and revision. Exactly representable fixture coordinates match exactly; transformed values follow the documented numeric error budget. No second geometry owner.
2. **Projection:** target numeric output within 0.5 logical pixel per axis of the oracle after clipping for visible anchors. Rasterized edges/line samples within 1 logical pixel per axis of the independently rasterized reference, including rounding. Logical pixels are distinct from screenshot pixels; PR2 must declare its scale/aspect mapping before screenshot comparison.
3. **Clip ambiguity:** clip classification agrees with the oracle outside a 1/1024-ft distance band around near/far planes. Within that band either classification is allowed only with bounded finite output and edge error still ≤1 logical pixel; viewport-boundary rounding gets the same 1-pixel rule. Zero divisions, wraparound, writes outside the destination, or unbounded loops are failures.
4. **Generation identity:** exact equality of destination generation, source tick, camera/view revision, fixture revision, projection revision and composition identity. The world store and its immutable registration record become eligible together. Zero stale-view commits after a newer camera request invalidates an in-progress attempt. Keep the old complete pair visible until a matching new pair is ready; no forced partial swap.
5. **Reproducibility:** identical authoritative input produces identical per-tick checksums with rendering disabled, normal, slowed and cancelled, and with different camera scripts. Camera changes may alter only presentation identities/results. Preserve M1's original 600-tick replay checkpoint where the authoritative input stream is unchanged.
6. **Geometry cases:** reset; ±east offsets; northbound/southbound views; positive/negative pitch, yaw and roll; horizon outside viewport; near/far-plane crossings; camera behind/alongside the runway; all viewport edges; degenerate/clipped-to-empty primitives; extreme envelope poses; rapid reset/view requests during build and immediately before commit.
7. **Resource/deadline behavior:** fixed maximum vertices/clipped vertices/spans/work units are generated and tested. Overflow rejects or cancels the attempt with an observable fault and preserves the last complete pair. No reserve borrowing, unbounded catch-up renderer, hidden tick drops or 100 Hz/21-stage changes. Measure displayed age, view-request-to-first-complete latency and cancellation counts; do not invent a production age/cadence limit from M1. After commands cease, a valid in-envelope view must complete within the generated worst-case work-unit bound under available renderer service; starvation is not a passing “stable old frame.”

The founder's later interactive observation must see a runway rectangle and marks moving coherently with the labelled camera, readable counters, complete sky/green ground, and no mixed camera/frame composition. Automated geometry and screenshot checks do not substitute for that observation or physical qualification.

## 7. Proposed implementation sequence and ownership

### PR1 — pure geometry/projection/registration foundation

After D1–D6 approval, reverify main and create a focused implementation branch. Read programming/C standards and exact generated/platform contracts. Implement bounded pure C transform, clipping and registration construction plus an independent host oracle. Define a new development-scoped M2 schema/ledger and generated bindings; do not bypass M1 admission or silently alter its identity. Use one source for parameters, reject unsupported configurations before generation, and preserve historical outputs.

Expected areas (paths are proposals, not created by this plan): `src/environment/` fixture/query; `src/graphics/` pure camera/projection/clipping; `interfaces/` M2 source/generated records; `memory/` M2 owner ledger; `tests/flight_demo/` oracle vectors/negative tests; `tools/flight_demo/` bounded generation/build support. Reuse existing runtime/publication APIs through narrow dependencies; avoid copying the entire M1 build or platform implementation.

The registration contract must specify lifetime and complete-pair eligibility, including camera revision and composition identity. No final production WorldRegistrationRecord ABI is hand-authored. Target compile/link exercises the pure functions and rejects overflow of admitted resident/stack ranges. A host diagnostic image may verify projection/raster math but is explicitly not an emulator screenshot. No target executable run in PR1.

Completion: host/oracle/negative checks, sanitizer checks, generated byte consistency and target compile/link/map/disassembly pass; fixture and source/tool hashes recorded; bounds and stack assumptions documented. Prepare PR2's exact display format, allocations, buffer/color/palette coherence, input mapping and register-clobber contract. Stop at READY FOR REVIEW. If a viable PR2 display seam cannot be demonstrated, record the named conflict and alternatives; do not select an unsafe seam or broaden to production graphics.

### PR2 — bounded rendering and camera integration (not yet authorized)

Start from reviewed/integrated PR1 and separately authorized concrete display contract. Integrate complete sky/ground, projected rectangle/marks and protected numeric overlay, with bounded yield/cancel and atomic matching world/registration/composition publication. Add read-only generation/camera/source-age/latency/fault counters and bounded diagnostic controls. A new camera request invalidates obsolete work without changing the still-displayed record. Static global palette is acceptable only if generation invariance is demonstrated; generation-dependent color data needs the same eligibility contract as the image.

Under separate direct-PRG authorization, run PAL/NTSC deterministic replay and normal/slow rendering, plus a camera-change/cancellation sequence and visual inspection. Record exact PRG, schema, toolchain, emulator/ROM identities, input trace, maps and screenshots. Use fresh output/evidence identities (`build/flight-demo/<m2-identity>/`, `docs/evidence/flight-demo/<m2-identity>/`); do not overwrite M1. Retain failed attempts honestly; exclude ROM-bearing dumps from publication. Stop at READY FOR REVIEW; publication and merge remain separate.

## 8. Contract and hardware impact

**This planning change:** documents/WIP only. Registers/clobbers, CPU/physical memory, MAP/base-page, DMA, timing/deadlines, IRQ/NMI, serialized state and generated artifacts: no changes.

**PR1 proposal:** pure C and generated development records; linked CPU-visible code/state/stack accounted with actual maps. No hardware register access, new assembly, MAP/base-page operation, DMA, IRQ/NMI handler, disk or persistent state. Fixed-point representation and intermediate widths are selected against the oracle, not assumed from M1's counters. No new physical allocation is approved by this plan.

**PR2 proposal:** Graphics owns scene/raster policy; Environment owns geometry; Platform alone owns device registers, input acquisition, copies and scanout activation. The existing B=`$02`, cleared MAP/EOM, reset-only seam and local IRQ/NMI ownership remain constraints. A changed display mode or input acquisition needs exact affected registers/clobbers, physical/CPU ranges, scanout-safe commit window and restoration effects documented before editing it. No DMA submission or new IRQ/NMI work is proposed. The protected `$058000–$05FFFF` reserve remains untouched. Existing M1 allocations are reference bounds, not free space automatically granted to M2. Reuse of unchanged R0 primitives retains declared startup writes and source pins.

## 9. Non-scope, stops and planning completion

No aircraft motion, aerodynamic data, FCS, gear/contact forces, takeoff/landing, cockpit/chase simulation, combat, audio, runtime storage, RRB/production graphics freeze, physical timing/cadence acceptance, full-harness PASS, D81, SD or physical testing. Do not change retained R0 proof source or public ABI. A required owner/contract contradiction, inability to fit admitted resources, or inability to preserve complete-pair display is a stop with evidence, not permission to lower acceptance bars.

Planning completion is this reviewable intent and pending D1–D6 decisions, with only this plan and WIP changed. Main remains verified; the 20 unrelated untracked entries, historical M1/R0 evidence and old outputs remain preserved. No implementation, generator, compiler, emulator or hardware test has been run for M2. Documentation links, whitespace, scope and preservation checks are the validation tier for this task.
