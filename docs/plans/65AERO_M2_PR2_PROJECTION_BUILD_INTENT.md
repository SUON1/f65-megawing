# M2 PR2 resident-deficit recovery — bounded prepared-projection experiment

**READY FOR REVIEW — planning only; P1–P6 await founder approval.**

Verified main `9dae245314ddd41cceaa7c6c3e7fce90c564138e`,
[PR #23](https://github.com/SUON1/f65-megawing/pull/23), matches local main and
fetched origin/main. The clean main worktree and
[exact-main static CI](https://github.com/SUON1/f65-megawing/actions/runs/39715650122)
were verified. Planning branch: `codex/65aero-m2-pr2-projection-intent`.
No implementation, source reconstruction, host suite or target build is
authorized or performed by this planning task.

## Objective, baseline and feasibility limit

Measure one pure-C compaction of `m2_project_prepared`: replace duplicate
endpoint copies and repeated call/output setup with bounded endpoint/axis loops
and indexed private working points. Preserve exact clipping and projection.
This is one partial size-recovery experiment, not a commitment to close the
remaining 9,646-byte deficit or a full M2 PR2 admission attempt.

Main integrates the accepted Q46 helper and transform sequence. The complete
renderer/cache/dispatch composition remains outside its active source tree.
The [publication scope](../reports/M2_PR2_TRANSFORM_PUBLICATION.md) distinguishes
accepted functions from restored experimental scaffolding. The current deficit
belongs to the [retained composed artifact](../evidence/flight-demo/2026-10-21-m2-transform-sequence/04-candidate/build.json),
not a newly built complete renderer from main.

| Retained resident accounting | Bytes |
|---|---:|
| Text | 30,806 |
| Read-only data, including accepted 56-byte transform table | 1,561 |
| Initialized data / BSS | 2 / 1,611 |
| Compiler resident scratch | 216 |
| BASIC header / alignment gaps | 22 / 3 |
| Total resident span | **34,221** |
| Allowed span `$2001–$7FFF` | **24,575** |
| Remaining deficit; end exclusive | **9,646; `$A5AE`** |

Reference PRG SHA-256:
`98822933724ec7b373622445723fb18be2ebac7ca74947e9a046f8b41acb9c51`.
The reference has failed resident admission; its above-ceiling addresses are
diagnostic placement, not authorized allocations.

The [actual symbol listing](../evidence/flight-demo/2026-10-21-m2-transform-sequence/04-candidate/RENDER.symbols)
shows the next costs:

| Routine | Own code bytes | Proposed treatment |
|---|---:|---|
| `m2_project_prepared` | **1,959** | One control/data-flow compaction candidate. |
| `interpolate_delta` | 1,605 | Freeze exact general clipping arithmetic. |
| `overlay` | 1,104 | Retain required anchors and labels. |
| `m2_multiply_q46` | 1,054 | Freeze accepted helper. |
| `m2_camera_command` | 1,042 | Retain camera behavior and envelope. |
| `m2_registration_matches_prepared` | 1,025 | Retain experimental owner validation. |
| `telemetry` | 1,020 | Retain counters and missing-state output. |
| `m2_transform` | 985 | Freeze accepted transform sequence. |
| `plane_distance` / `project_axis` / `to_camera` | 946 / 536 / 651 | Freeze numerical helper bodies. |

These are symbol sizes excluding callees, not subsystem totals or savings
estimates. Removing every one of the projection routine's 1,959 bytes would
still leave 7,687 bytes before secondary effects; a replacement needs code and
working storage itself. No saving is promised. Further work requires review of
the measured result, not an automatic chain of small optimizations. A credible
whole-composition fit path remains an open architecture/engineering question.

## Governing authority and inspected contracts

The [PR2 intent](65AERO_M2_PR2_BUILD_INTENT.md),
[renderer-admission intent](65AERO_M2_PR2_RENDERER_ADMISSION_BUILD_INTENT.md),
[prior transform intent](65AERO_M2_PR2_DEFICIT_BUILD_INTENT.md) and
[entry plan](65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md) carry forward
the approved Main v1.8, Gameplay v1.2, Runtime v1.2 candidate (NOT FINAL),
Graphics v2.1 and Physics v4.1 authority with incorporated bases. The
[corpus](../../spec/manifests/spec-corpus.json) remains controlling.

Inspected implementation/contracts: [geometry](../../src/graphics/m2_geometry.c),
[PR1 numeric/public schema](../../interfaces/m2_pr1.json),
[full composition schema](../../interfaces/m2_full.json),
[full memory ledger](../../memory/m2-full-ledger.json), retained full renderer,
cache/dispatch, builder, clipping regressions and transform experiment evidence.
Public/generated interfaces and the existing Q46/Q24/Q16 rules are frozen.
The [development workflow](../DEVELOPMENT_WORKFLOW.md),
[programming principles](../PROGRAMMING_PRINCIPLES.md) and
[C standard](../CODE_STYLE_C.md) apply to any later approved implementation.

## Exact founder decisions

| ID | Decision requested | Recommendation |
|---|---|---|
| P1 | Reconstruct which reference, and where? | **Approve one isolated experiment branch from reverified main.** Restore only the 16 paths in the new manifest and verify all 79 recorded inputs. Preserve main's accepted transform and Q46 implementations. Reproduce the exact 34,221-byte reference, sections, owners, tool/recipe and PRG identity before a candidate. Stop on unexplained mismatch. The known reference fit failure is the starting observation. |
| P2 | What implementation change is authorized? | **One prepared-projection compaction candidate, confined to `m2_project_prepared`.** Use two indexed private `ClipPoint` work records and bounded loops to share endpoint transformation, plane-distance evaluation and projected-output setup. Update only the outside endpoint during clipping. Freeze every called arithmetic helper, public guard, clipping-plane sequence and rounding step. No interpolation rewrite, new arithmetic kernel or anchor/cache refactoring. |
| P3 | Which behavior and resource rules may change? | **None of the governing rules.** Preserve endpoint order; exact `-1/0/1` results; failure-output preservation; same-pointer degenerate segments; current supported alias behavior; all camera/fixture bounds; Q46/Q24/Q16 precision; generated/public layouts and signatures. Keep the `$8000` resident ceiling, 4 KiB software-stack envelope, hardware-stack/base-page bands and zero reserve. All changed compiler scratch, local lifetimes, code, padding and tables are charged. |
| P4 | What evidence is required before relink? | **Exact old/new host comparison on the fixed corpus below**, ASan/UBSan, independent Decimal geometry and all 841 near/far regressions. Rerun renderer identity/cancellation/failure checks and require five byte-identical images. Hash-pin the unchanged accepted arithmetic/transform sources and retained proofs. No tolerance change or validation bypass to make a case pass. |
| P5 | How is the target result admitted and bounded? | **One reference and one candidate composed relink, unchanged compiler and flags.** Also run the standard standalone host/oracle/target static checks. Report actual function/section/resident bytes, remaining deficit, compiler scratch, reachable stack and conservative work immediately after candidate relink, then stop implementation. Positive net resident saving is a bounded result; full fit still requires every resident section within the existing ceiling. No second candidate or automatic optimization. |
| P6 | What remains frozen and what later authority is granted? | **Preserve evidence and unrelated paths; grant no later stage.** Keep 17 cached segments, four protected anchors, labels/telemetry, generation cancellation/invalidation, workspace lifetimes and fail-closed deadline guards. No full adapter/runtime/display acceptance, Xemu, D81, SD, physical testing, publication or later milestone. Return READY FOR REVIEW with the measured result or report the first unexpected failed prerequisite. |

Suggested approval:

> Approve P1–P6 as recommended. Build the single bounded prepared-projection
> compaction experiment from verified main, beginning with exact reference
> reconstruction. Preserve arithmetic, behavior, memory limits, evidence and
> unrelated paths. Run the specified host/oracle and target compile/link/static
> checks; report immediately after the candidate relink and stop at READY FOR
> REVIEW or a failed gate. No second optimization, Xemu, D81, SD, physical testing,
> commit, push, PR or merge.

## Concrete candidate constraints

The current routine creates two transformed endpoints, computes both signed
distances before clipping a plane, copies inside/outside records, interpolates
three coordinates and emits four projected coordinates. Candidate sharing may
change private storage/control flow only:

- Preserve the correspondence of working endpoint 0 to `first` and endpoint 1
  to `last`. Complete both transformations before any caller output write.
- For each of the six planes, calculate both distances from the current endpoints
  before modifying either. Preserve the both-outside and sign-crossing decisions.
  Select the inside and outside indices only in the crossing branch.
- Keep numerator and denominator fixed across all three coordinate updates.
  Each updated outside coordinate must use that coordinate's prior outside
  value and the unchanged inside endpoint. Preserve the inside-origin formula
  `inside + interpolate_delta(outside - inside, numerator, denominator)`.
  Retain plane order, near/far handling and the final positive-forward check.
- Preserve `project_axis` calls with the correct component, forward coordinate
  and width/height. Build a local `M2Line` and publish only after success. Do not
  treat public struct fields as an undocumented flat coordinate array.
- Keep `to_camera`, `plane_distance`, `interpolate_delta`, `project_axis`,
  `rounded_ratio`, the Q46 helper, transform sequence and raster cursor unchanged.
  No new persistent state, cache entries, continuation phases or hardware seam.

## Fixed host comparison and independent checks

Before editing, retain the reference function/source and freeze corpus generation
and seed. Host tests may share frozen helpers for exact old/new comparison;
the independent Decimal quaternion/parametric clipping oracle remains separate.
Compare return status and all output coordinate fields, not just raster hashes.

1. **599,760 canonical cases:** 360 yaw values, pitch and roll each in
   `[-60,-30,-1,0,1,30,60]`, all 17 fixture segments and both endpoint orders.
   Use the legal camera position `(-4500,0,-300)` feet. Count is
   `360 × 7 × 7 × 17 × 2`.
2. **200,000 seeded cases:** Python `random.Random(650017)`; generate 100,000 legal camera and
   world-endpoint pairs using integer public Q12 coordinates across the complete
   declared bounds, legal integer angles and nonzero revisions. Test both orders.
   Per pair, draw camera north, east and down; yaw; pitch; roll; revision; first
   north/east/down; then last north/east/down, in that order. Use inclusive
   `randint` bounds from the generated contract (revision 1 through `2^32-1`),
   with no rejection, retry or deduplication. Canonical/analytic cases consume
   no RNG draws. Record Python version, generator source and exact input identity
   before running the candidate.
3. **126 analytic plane/degenerate cases:** identity camera at `(0,0,-10)` feet.
   For each of six planes, construct two distinct legal boundary points, perturb
   each by `-1,0,+1` public Q12 coordinate units normal to that plane, and test all
   nine side-pairs in both orders (`6 × 9 × 2 = 108`). Also test each plane's
   first boundary point at those three offsets as a same-pointer degenerate
   segment (`6 × 3 = 18`). Near/far use forward 10/40,000 feet with tangential
   east coordinates 0/1 foot; left/right use forward 100/110 feet and east
   `±forward`; top/bottom use forward 100/110 feet and translated down
   `±2*forward/5`. Apply the camera offset to obtain world points. Perturb forward,
   east or down respectively; oracle calculations determine inside/outside signs.
4. Add contract checks for null/unready context, null/invalid endpoints, null
   output, representable bounds, unchanged output on every unsuccessful path,
   and supported alias cases. Reject malformed-input expectations outside the
   private prepared-context contract rather than inventing new semantics.
5. Pass all existing **3,857 Decimal** and **841 near/far** cases, error limits
   and raster checks, plus renderer cache/generation/cancellation/failure tests.
   Require all five completed host images to match the reconstructed reference.

The fixed exact-comparison corpus contains **799,760 canonical/seeded cases plus
126 analytic cases**; contract checks are additional. Existing signed arithmetic,
carry and exhaustive transform proof identities remain pinned because their
implementations and toolchain are frozen. Host passing does not establish target
execution or timing correctness.

## Gate order, accounting and stop

After explicit approval, create a fresh isolated experiment checkout and use the
[proposed reconstruction manifest](65AERO_M2_PR2_PROJECTION_RECONSTRUCTION.json).
Sixty-three reference inputs already match main; sixteen require exact retained
snapshot copies. The geometry source must come from the transform-sequence
snapshot, not an earlier version that would undo the accepted matrix change.
Do not copy from mutable development worktrees or overlay entire old packets.

Verify all 79 hashes and locked tool identities before the reference build.
Reproduce the source list, opaque non-LTO backend, `-mcpu=mos45gs02`,
`-mlto-zp=0`, `-Oz`, `-fno-inline-functions`, `-fno-jump-tables` and warnings.
Fresh output paths are the only recipe normalization. An unexplained PRG hash,
size/owner or section mismatch is a stop. The expected reference fit FAIL at
`$A5AE` is recorded explicitly; no other failure is implicitly tolerated.

Implement only P2 and its focused tests, then pass P4 before the candidate
composed relink. Required existing commands include
`python3 -B tools/flight_demo/m2/build.py` and the approved reconstructed renderer
recipe in `tools/flight_demo/m2_full/renderer_build.py`; preserve all logs and
exit results. Host phases/image comparison may be separated from target phases
using the exact recorded command recipe, as in the previous experiment.

Immediately after the one candidate relink, report own projection code bytes,
all allocated sections including header/gaps/`.noinit`, owner objects, total span,
end/ceiling and remaining deficit. Include compiler/command/source hashes and
raw PRG/ELF identities. All introduced working storage or runtime helper effects
must be charged; resident scratch is counted once, separately from dynamic stack.
Distinguish the standalone probe's memory/stack from the composed artifact.

Complete read-only reachable stack and conservative instruction-work accounting
for the projection closure, including all helper/tail-call work. State unknown
paths; do not infer a whole-renderer stack bound from a function closure or the
previous transform's 15-byte result. Cycle WCET, platform/interrupt overhead and
100 Hz dispatcher margins remain unproven; unknown service budgets stay zero.

Stop implementation after this relink regardless of saving or regression.
If resident fit still fails, no full adapter, service or display gate follows.
Nonpositive net saving is a failed bounded size result. Positive partial savings
remain separate from full-fit/runtime acceptance. Preserve every outcome and
return its exact accounting for review; no next candidate is implied.

## Ownership, hardware impact and handoff

Graphics owns temporary clipping/projection state; Environment remains fixture
owner, Diagnostics owns requested camera, Input owns semantic edges, Presentation
owns snapshots and Platform owns registers/physical memory. Public/generated
interfaces and all versions remain unchanged. Matrix scratch must not be moved
into the 289-byte cache/320-byte HUD workspace or another owner's band.

Planning changes have no register/clobber, CPU-visible/physical-memory,
MAP/base-page, DMA, timing/deadline, IRQ/NMI or persistent-state effects. A future
pure-C candidate may alter compiler register saves, stack/scratch lifetimes and
work cost; these require actual emitted-code accounting. No new hardware accesses,
handlers, assembly, memory limits or reserve use are proposed. Display allocations,
320×200 backing at 2× within the approved PAL/NTSC reference outputs, and every
runtime/display admission obligation remain unchanged.

This planning task is complete when main/CI, reconstruction pins, retained cost
figures, case counts, links, whitespace and preservation checks pass. Changes
are confined to this intent, its proposed reconstruction manifest and WIP.
Historical evidence and original working paths remain untouched. No source
restoration, implementation, host/target build, Xemu, D81, SD, physical testing,
commit, push, PR or merge occurs in this planning task.
