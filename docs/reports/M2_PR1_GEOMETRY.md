# M2 PR1 geometry, projection and registration

**READY FOR REVIEW.** Local, uncommitted implementation on `codex/65aero-m2-pr1-geometry`, based on verified main `2acd30c21a4be0996cd1a2dd3ce74da6deb6c84d` (M1 PR #18). The founder approved D1–D6 of the [M2 intent](../plans/65AERO_M2_REGISTERED_RUNWAY_CAMERA_BUILD_INTENT.md) and explicitly authorized PR1 host/oracle and target compile/link only. The original planning document is preserved as written; its pending-decision wording is historical, superseded for PR1 by that approval. PR2 remains unauthorized.

## Delivered ownership and contracts

- [M2 source schema](../../interfaces/m2_pr1.json), [generator](../../tools/flight_demo/m2/generate.py), [generated records](../../interfaces/generated/m2_pr1.h), [rotation table](../../interfaces/generated/m2_tables.c), and [owner ledger](../../memory/m2-pr1-ledger.json): development identity `65AERO-M2-PR1-1`. Admission pins the exact reviewed source before writing; schema, capacity, unit, frame, revision, memory or layout drift fails closed. This is intentionally a fixed profile, not a configurable production ABI. Header/table/ledger regeneration is byte-identical.
- [Environment fixture](../../src/environment/m2_fixture.c): sole owner of `M2-RWY-TEST-1`; four edges, two threshold lines and eleven centerline segments. Read-only footprint/elevation query shares the same generated geometry and revision. Membership means horizontal runway footprint, not contact with a surface or a physical force.
- [Graphics math](../../src/graphics/m2_geometry.c): valid diagnostic camera envelope; NED-to-camera rotation; bounded six-plane segment clipping before divide; logical projection; bounded Bresenham samples; common-camera horizon ray classification; immutable registration construction and complete-pair eligibility predicate.
- [Host tests](../../tests/flight_demo/m2/host.c), [independent oracle](../../tests/flight_demo/m2/oracle.py), [frozen oracle description](../../tests/flight_demo/m2/ORACLE.md), and [contract tests](../../tests/flight_demo/m2/test_contract.py): numeric, negative, replay-independence and generation-identity proof. No existing M1/R0 source was edited.
- [Build driver](../../tools/flight_demo/m2/build.py) and [static stack checker](../../tools/flight_demo/m2/stack_check.py): fresh outputs per invocation, pinned compiler/objdump, no emulator or media entry point. The [target probe](../../tests/flight_demo/m2/target.c) consumes all output bytes so LTO cannot discard the raster/registration/query work being charged.

Camera angles are integer degrees, matching the admitted one-degree diagnostic steps. Position is signed Q12 feet, rotation signed Q30, screen coordinates signed Q16 logical pixels; multiplication/division uses int64 intermediates. Inputs outside the declared camera envelope or the arithmetic world-coordinate bound ±65536 ft reject. The latter is a pure arithmetic input limit, not terrain extent or a new camera envelope. All admitted runway/camera cases fit it. No float, heap allocation or recursion is used by the target math.

A transformed coordinate is bounded by the norm of the largest admitted world-minus-camera vector, below 126000 ft (about 516 million Q12 units). The largest clipping plane normal has norm sqrt(29); even the conservative product of two endpoint differences and a plane distance stays below 3×10^18, below INT64_MAX. Rotation dot products and projection products are smaller. Rounding is explicit and symmetric before narrowing. No negative signed shifts or implementation-defined packed layout are used. Generated records are C in-memory development records, not serialized wire bytes; native and target padding may differ, and record equality is fieldwise.

Clipping has six iterations and at most three coordinate interpolations per plane. A line yields at most 320 samples; the fixture has 17 lines, hence at most 5440 line samples. A clipped line still has two endpoints. There is no polygon fill or target raster service in this increment. Capacity/invalid-input failures preserve output buffers/counts; clipped-empty results leave the caller's output untouched.

## Validation and exact evidence

Command: `python3 -B tools/flight_demo/m2/build.py`.

Final output: `build/flight-demo/m2-pr1-1792534579771485000/`. All earlier preflight outputs remain local. The [review packet](../evidence/flight-demo/2026-10-20-m2-pr1/README.md) retains exact commands, input hashes, reports, map, symbols and disassembly.

| Check | Actual result |
|---|---|
| Four contract tests | PASS, including mutations of every constant/memory field and identity/unit/frame/layout, temporary regeneration, and fail-closed stack-CFG fixtures |
| Native ASan/UBSan | PASS: malformed/negative/capacity/registration cases and 600 per-tick M1 checksum comparisons with absent, normal and intermittent/stale geometry work; checkpoint `DE675132` |
| Independent 60-digit Decimal oracle | PASS: 3857 segment cases, 1278 visible segments and 119736 raster samples; includes 1000 near-camera cases in addition to general/fixture/clip cases |
| Maximum projection endpoint error | 0.0331513833 logical pixel, below approved 0.5 limit |
| Raster comparison | Bidirectional Chebyshev distance ≤1 logical pixel against independent DDA; PASS |
| Horizon | Common quaternion ray classification agrees at sampled viewport points across the frozen camera cases |
| LLVM-MOS compile/link/map/disassembly | PASS; no calls into retained R0 diagnostic/platform functions or ROM entry addresses |
| Static stack | Checked direct-call CFG: 22 hardware bytes including main's entry return; compiler static scratch 275 bytes; no dynamic software-stack pointer adjustments in this linked probe |
| Preservation/source identity | 25 current build-input hashes verified; 521 baseline file fingerprints match, including original plan and M1 outputs/evidence; 20 unrelated untracked entries preserved |

The oracle computes quaternion rotations with independently converged Decimal trigonometry and clips via parametric interval intersection; it does not read the generated C sine table or call C to obtain expected projections. Fixture data/layout are shared intentionally. Near-camera tests were added to amplify divide-boundary error; they did not relax the frozen acceptance bars. Logical raster samples are not screenshots or target-visible evidence.

### Linked accounting

| Section | Bytes | Start |
|---|---:|---:|
| Text/runtime support | 17480 | `$2017` |
| Read-only data, including sine table | 1449 | `$645F` |
| Initialized data | 22 | `$6A08` |
| BSS, including 1280-byte probe raster output | 1420 | `$6A1E` |
| Compiler static scratch (.noinit) | 275 | `$6FAA` |

Resident end is `$70BD`, below `$8000`, leaving 3907 bytes in this standalone envelope. PRG is 18975 bytes, SHA-256 `62f85fda019146ec64c1f7236a1d58441b22a87cf3a4504074f3332558bb656a`. The target registration object is 83 bytes. The 275-byte compiler scratch is charged in resident memory, not counted again as dynamic software-stack usage. No protected reserve is allocated. No exercised target stack high-water or timing result is claimed.

The probe uses the existing SDK linker/startup only for static reachability and accounting, with `-fno-jump-tables` to make its stack-control-flow analysis enumerable. SDK startup includes processor-port/`$D030` setup and logical register storage `$0002–$0021`; it is **not** the B=`$02`/MAP-cleared M1 runtime adapter and is not admitted for execution. The generated ledger explicitly records that distinction. Pure M2 code contains no register access, MAP/base-page changes, DMA, IRQ/NMI code or persistent-state writes. No new assembly was added.

## Registration lifetime and limits of the proof

A record copies camera pose/revision, transform, source tick, generation, fixture/projection/composition revisions, view/tier and destination-store identity. Eligibility requires complete status exactly 1, matching supported identities, an internally consistent transform, and the currently requested camera revision. Pending record and displayed record must be separate caller-owned values. Once a completed pair becomes displayed, both its image and record remain immutable until replaced together.

The pure predicate rejects incomplete, stale or mismatched pairs; it does not implement interrupt exclusion, scanout activation, a renderer queue or an atomic hardware swap. Caller must recheck the wanted camera revision at the eventual commit boundary. Camera controls, held-key behavior, revision allocation/wrap policy, display-age and completion-latency measurements, and runtime cancellation/service scheduling belong to PR2. This is not a claim that the actual visible renderer already prevents mixed frames or meets a latency bound. M1 CoreRuntime/Input/Presentation and their authoritative checksum code are unchanged.

## PR2 display contract: named unresolved seam, not implementation

**Owner: Platform with Graphics.** M1 exposes an 80×25 character-screen bank swap and shared row-static color RAM. That seam cannot establish a generation-atomic 320×128 pixel world with a moving horizon and runway. It is unsafe to draw into currently visible glyph/color resources or switch composition before the matching complete record. PR1 proves the math; PR2 target display admission remains unresolved.

A concrete resource candidate for review is two 320×128 8-bit logical images (40960 bytes each), fitting as proposed cold pixel payloads at `$020000–$029FFF` and `$030000–$039FFF` within the existing development display-bank regions. These are **proposed payload bounds only**, not new allocations or a claim that VIC-IV can scan that representation. Screen maps, glyph interpretation, palette/color ownership and scanout selection are not accounted by those byte counts. Production mode selection remains gated.

Two alternatives need a separately reviewed register/resource contract before PR2 target edits:

1. A VIC-IV mode using immutable per-generation pixel/glyph resources and screen maps, with static global palette/color only if it can represent every required scene color without generation-dependent visible writes. Prove that the selected scanout resource identity and registration/composition identity change at one legal boundary.
2. A deliberately smaller presentation profile that can preserve complete-pair eligibility behind a simpler seam. Any change to the approved logical viewport/tolerances goes back to the founder; it is not an implementation fallback.

Do not select either from host images. The next contract must name exact mode, registers and clobbers, screen/color/glyph addresses and lengths, image scaling/aspect mapping, old/new resource lifetimes, bounded scanout-safe activation, input mapping, and reset-only restoration assumptions. It must also supply an integrated map: this PR1 probe's 3907 spare resident bytes do **not** show that M1 plus M2 fits. Wide arithmetic and repeated transforms may be costly; no throughput promise has been inferred from compile success. A bounded integration contract and any needed optimization must retain the independent error tests.

## Stop and recommendation

Review PR1 source ownership, generated identity, oracle independence and linked accounting. PR1 is complete at its permitted evidence tier. Keep PR2 blocked on the named display/resource and integrated-fit contract; no new approval is requested or presumed in this handoff. No commit, push, PR creation or merge performed. No PR2, target execution, Xemu, D81, SD or physical testing performed.
