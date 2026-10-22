# M2 PR2 resident-deficit recovery — bounded interpolation bit-consumption experiment

**READY FOR REVIEW — planning only; I1–I6 await founder approval.**

Verified main `c6a41e0988a3e329f1b30f7d48c87d92e00b523b`,
[PR #24](https://github.com/SUON1/f65-megawing/pull/24), matches fetched
origin/main, GitHub main and the clean main worktree.
[Exact-main static CI](https://github.com/SUON1/f65-megawing/actions/runs/39724644712)
passes. Planning branch: `codex/65aero-m2-pr2-interpolation-intent`.
This task prepares a proposal; no implementation, source reconstruction, host
test suite, target compile/link or publication is authorized or performed.

## Objective and feasibility boundary

Measure one pure-C change to the private `interpolate_delta` bit traversal:
consume the magnitude's existing 64 bits from high to low using a fixed
unsigned one-bit shift, instead of recomputing a variable bit selection in each
iteration. Preserve the exact quotient/remainder recurrence and rounding.
The experiment targets code and conservative work cost, with no precision or
memory-limit change and no promised saving.

Main integrates the accepted Q46, transform and corrected prepared projection.
The [publication scope](../reports/M2_PR2_PROJECTION_PUBLICATION.md) keeps the
full renderer/cache/dispatch composition outside its active source tree.
Consequently **9,574 bytes** describes the
[retained composed artifact](../evidence/flight-demo/2026-10-21-m2-projection-forward-guard/04-candidate/build.json),
not a fresh complete renderer built from main.

| Retained resident accounting | Bytes |
|---|---:|
| Text | 30,747 |
| Read-only data | 1,561 |
| Initialized data / BSS | 2 / 1,611 |
| Compiler scratch `.noinit` | 200 |
| BASIC header / alignment gaps | 22 / 6 |
| **Total resident span** | **34,149** |
| Allowed span `$2001–$7FFF` | 24,575 |
| **Deficit; end exclusive** | **9,574; `$A566`** |

Reference PRG SHA-256:
`72fd75a63771794a0f1936f92289cac612db149317781ab5646756a8045aa94d`.
Above-ceiling placement remains a failed-fit diagnostic, not admitted memory.

The [actual symbol listing](../evidence/flight-demo/2026-10-21-m2-projection-forward-guard/04-candidate/RENDER.symbols)
and disassembly show the remaining costs:

| Symbol | Own code bytes | Proposed treatment |
|---|---:|---|
| `m2_project_prepared` | 1,900 | Freeze accepted compaction and local-forward guard. |
| `interpolate_delta` | **1,605** | One bit-consumption candidate only. |
| `__ashldi3` | **31** | Currently called only by interpolation; report actual reachability after relink. |
| `overlay` / `telemetry` | 1,104 / 1,020 | Freeze required anchors, labels and counters. |
| `m2_multiply_q46` / `m2_transform` | 1,054 / 985 | Freeze accepted arithmetic and staged transform. |
| `m2_registration_matches_prepared` | 1,025 | Freeze reconstructed owner checks. |
| `plane_distance` / `project_axis` / `to_camera` | 946 / 536 / 651 | Freeze numerical helper bodies. |

The emitted interpolation selects a bit by constructing a variable shifted
mask through `__ashldi3`. It calls that helper once per bit step. Its shift
counts span 63 down to zero: **2,016 one-bit shift-body iterations per complete
interpolation**, before caller/callee setup, guards and the unchanged ratio
work. The proposed fixed walk needs 64 unsigned one-bit magnitude advances.
These counts explain a structural opportunity; they are not CPU cycles or a
measured speedup. Compiler output must establish the actual effect.

The 1,636 combined own code bytes of interpolation and its current shift callee
are much smaller than the 9,574-byte deficit, and a replacement still needs
code. This is one partial recovery experiment, not a credible claim to close
full fit by itself. Its result must return for review. Further arithmetic,
anchor/cache, owner-wrapper or architecture work requires a separate decision;
no automatic chain of experiments is authorized.

## Inspected authority and contracts

Retain the approved hierarchy carried by the
[PR2 intent](65AERO_M2_PR2_BUILD_INTENT.md),
[renderer-admission intent](65AERO_M2_PR2_RENDERER_ADMISSION_BUILD_INTENT.md),
[projection intent](65AERO_M2_PR2_PROJECTION_BUILD_INTENT.md) and
[entry plan](65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md): Main v1.8,
Gameplay v1.2, Runtime v1.2 approved candidate (NOT FINAL), Graphics v2.1 and
Physics v4.1 with incorporated bases, pinned by the
[corpus](../../spec/manifests/spec-corpus.json). No design amendment is proposed.

Inspected implementation/contracts: [geometry](../../src/graphics/m2_geometry.c),
[PR1 numeric/public schema](../../interfaces/m2_pr1.json),
[full composition schema](../../interfaces/m2_full.json),
[memory ledger](../../memory/m2-full-ledger.json), retained renderer/cache/
dispatch, builder, independent Decimal/clipping oracles, exact projection
comparison and corrected projection stack/work evidence. Generated layouts,
Q46/Q24/Q16 scales and all camera/fixture bounds remain controlling.
The [development workflow](../DEVELOPMENT_WORKFLOW.md),
[programming principles](../PROGRAMMING_PRINCIPLES.md) and
[C standard](../CODE_STYLE_C.md) govern any later implementation.

## Exact founder decisions

| ID | Decision requested | Recommendation |
|---|---|---|
| I1 | Which baseline and reconstruction may a future build use? | **One fresh isolated experiment from reverified main.** Resolve all 79 recorded inputs using the 16 exact restorations in the new manifest; reproduce the 34,149-byte reference and exact PRG, section, owner, tool and recipe identities first. Use the corrected projection snapshot. Preserve all old checkouts. Known reference fit FAIL is the starting observation; an unexplained mismatch stops work. |
| I2 | What implementation change is permitted? | **One candidate inside `interpolate_delta` only.** Test the current unsigned magnitude's high bit, then advance that magnitude left by one unsigned bit per iteration. Retain all 64 iterations, their order, quotient/remainder updates, two subtraction tests, final rounding and signed result. Freeze every other production function, including the accepted local-forward guard. No new arithmetic kernel, table, assembly or persistent state. |
| I3 | May numerical, interface or memory rules change? | **No.** Preserve the existing valid private ratio domain, exact outputs, signed behavior, tie handling and narrowing; keep all public/generated interfaces, Q46/Q24/Q16 precision and world bounds. Preserve `$8000` resident ceiling, 4 KiB software-stack envelope, existing hardware-stack/base-page/display bands and zero reserve. Charge every code/data/padding/scratch/helper effect. |
| I4 | What equivalence evidence is required? | **Inductive bit/state proof plus the fixed direct-helper corpus below**, comparing original and candidate and an independent unbounded-integer oracle under sanitizers. Also rerun the frozen 799,886 projection cases +34 contract checks, 3,857 Decimal cases, 841 near/far regressions, renderer cancellation/failure checks and five byte-identical images. Keep accepted Q46/transform proofs and source identities pinned; no oracle or tolerance changes. |
| I5 | What size, compiler and stop gates apply? | **One reference and one candidate composed relink, unchanged toolchain/flags.** Run the standard standalone host/oracle/target static checks before the candidate composed relink. Immediately report all resident sections, own/helper code, padding, scratch, stack/work status and remaining deficit, then stop implementation. A candidate must use fewer than 34,149 resident bytes to pass bounded size; full fit remains separate. No second candidate. Unexpected prerequisites fail closed. |
| I6 | What remains preserved and what later authority follows? | **Preserve all history, evidence and unrelated paths; grant no later stage.** Freeze all 17 cached segments, four anchors, labels/telemetry, generation cancellation/invalidation, workspace lifetimes and deadline guards. No runtime/display admission, Xemu, D81, SD, physical testing, publication or later optimization. Return READY FOR REVIEW with exact measurements or a failed gate. |

Suggested approval:

> Approve I1–I6 as recommended. Build the single bounded interpolation
> bit-consumption experiment from verified main. Preserve exact arithmetic,
> memory limits, evidence and unrelated paths. Run the frozen and specified
> direct-helper checks plus host/oracle and target compile/link/static checks.
> Report immediately after the candidate relink and stop at READY FOR REVIEW
> or a failed gate. No further optimization, Xemu, D81, SD, physical testing,
> commit, push, PR or merge.

## Exact candidate semantics and proof obligation

Let `M` be the original valid unsigned magnitude and `k` the completed bit-step
count. At the start of step `k`, require
`working_magnitude = (M * 2^k) mod 2^64`.
Its high bit is exactly bit `63-k` of `M`, matching the original variable
selection. Advance the magnitude with unsigned `<< 1` after the existing
two-subtraction loop, once each step, including the last. Discarded high bits
are already consumed; the final magnitude is unused. Do not shift signed
`delta` or use a shift by 64. The original `delta` remains intact for the final
sign restoration. No extra magnitude copy or new workspace is required.

Since the selected bit is equal at every step, identical initial quotient and
remainder produce identical additions, comparisons, subtractions and quotient
increments by induction. Keep the final threshold `(divisor + 1) / 2`, sign
restoration, and return type unchanged. Preserve numerator 0/equal-denominator,
zero delta, exact ties and carries across every byte/word boundary. Do not
replace the general ratio, alter evaluation stages, skip leading zeros, shorten
the 64-step loop or infer a smaller magnitude width from current fixtures.

Existing valid arithmetic domain is `delta` from `-INT64_MAX` through
`INT64_MAX`, `1 <= denominator <= floor((2^48-1)/3)`, and
`0 <= numerator <= denominator`. This is a conservative valid arithmetic test
envelope, not expanded world/fixture admission. The actual clipping inputs remain
under their existing geometric bounds. `INT64_MIN`, zero/negative denominators,
and invalid ratios are outside this private contract; do not invoke signed
negation UB or invent new invalid-input return semantics. The legacy magnitude
conversion is unchanged by this candidate.

## Fixed direct-helper corpus and independent oracle

Before any production edit, retain the exact reference helper/source and freeze
the generator, input serialization, Python version, seed and corpus hash.
The following set definitions have planning-verified cardinalities:

1. Let `L = 2^63-1`. Delta set is `{0, -L, L}` union both signs of
   `2^k-1`, `2^k`, `2^k+1`, for `k=0..62`, retaining magnitudes in `[0,L]`,
   deduplicated and sorted: **373 deltas**.
2. Let `D = floor((2^48-1)/3) = 93824992236885`. Denominator set is
   `{1,2,3,4,5,D-1,D}` union `2^k-1`, `2^k`, `2^k+1`, for `k=0..46`,
   retaining values in `[1,D]`, deduplicated and sorted: **139 denominators**.
3. For each denominator `d`, use distinct sorted numerators from
   `{0,1,d//2-1,d//2,(d+1)//2,d//2+1,d-1,d}`, retaining `[0,d]`.
   Cross these with all deltas, iterating delta then denominator then numerator:
   **357,334 structured cases**. This covers binary boundaries, valid signed
   extrema, ratio endpoints and below/tie/above-half cases.
4. Add **100,000 seeded cases**, Python `random.Random(650018)`. Per case draw
   inclusive `randint(-L,L)` delta, then `randint(1,D)` denominator, then
   `randint(0,denominator)` numerator. No rejection, retry or deduplication;
   structured cases consume no RNG draws. Total direct-helper corpus is
   **457,334 cases**.

For each case compare original/candidate exact signed output and an independent
Python unbounded-integer oracle:
`sign(delta) * ((abs(delta)*numerator + denominator//2)//denominator)`.
The oracle must not call the C reference or reproduce its bit recurrence.
Validate bit-order/state induction over all 64 positions, including sign-boundary
magnitude advances and carry/borrow boundaries. Preserve all failures. Any
test-only binding must not introduce public ABI/layout copies or target hooks.

Rerun the unchanged projection corpus SHA-256
`92c334a7812dabafe70ccef7ab8703db424c15ef1f312c56fd314bf36f90a8d5`,
its output-preservation/alias checks, independent Decimal and near/far suites,
renderer identity/cache/generation/cancellation/failure checks and five exact
host-image comparisons. The projection comparator shares frozen helpers, so
direct-helper reference separation and independent integer/Decimal oracles are
mandatory for this helper change. No reliance on raster hashes alone.

## Gate order and accounting after approval

1. Reverify main/CI; create a fresh experiment branch/worktree. Use the
   [proposed reconstruction manifest](65AERO_M2_PR2_INTERPOLATION_RECONSTRUCTION.json).
   Sixty-three inputs already match main; 16 require exact committed snapshots.
   Geometry must come from the corrected projection snapshot, preserving all
   accepted Q46/transform/projection work plus the experimental owner comparison.
   Do not overlay older packets or copy mutable working sources. This is
   reconstruction scaffolding, not acceptance of the restored renderer.
2. Verify all 79 hashes and locked compiler tools before any build. Reproduce
   the reference with the identical opaque backend, source list and full flags
   (`-mcpu=mos45gs02`, `-mlto-zp=0`, `-Oz`, `-fno-inline-functions`,
   `-fno-jump-tables` and existing layout/warning flags). Normalize checkout tool
   and output paths only. Independently verify owner symbol kinds where the
   builder omits them. Exact PRG/section/owner mismatch is a stop. The known
   reference fit FAIL is explicitly retained; no other failure is tolerated.
3. Freeze direct-helper reference/corpus identities, implement only I2, and pass
   I4. Run `python3 -B tools/flight_demo/m2/build.py` and the reconstructed renderer
   host/image phases. Separate host and target phases using the exact recorded
   recipe, as in the preceding experiment; do not run an early candidate relink
   before required checks or run duplicate composed links.
4. Perform the single candidate composed relink. Immediately report
   interpolation and shift-helper bytes/reachability; every allocated ELF
   section including BASIC, gaps and `.noinit`; owner objects; total span,
   end/ceiling and deficit; compiler/command/source and raw PRG/ELF identities.
   Shared compiler scratch is charged once, separately from dynamic stacks.
   The 31-byte shift helper is not a promised saving or removable by assumption.
   Report any secondary specialization or helper costs across the whole link.
5. Stop implementation regardless of outcome. Complete read-only reachable
   stack and conservative instruction-work accounting, including tail transfers.
   Report unsupported paths; do not relax the stack checker to claim PASS.
   Bounded size passes only below 34,149 fully charged bytes. Full fit requires
   all resident sections inside `$2001–$7FFF`. Neither partial saving nor full
   fit grants adapter/service/display execution authority. Preserve the result
   and return for review; no next candidate follows automatically.

The existing composed stack proof rejects `bit` in frozen interpolation and is
UNPROVEN; the 8-byte syntactic software frame and 200-byte resident scratch are
not a whole-renderer stack bound. The accepted standalone probe's 20-byte
hardware stack, zero dynamic software bytes and 497-byte scratch are a separate
tier. A future candidate may change these emitted effects and must account for
them honestly. CPU-cycle WCET, platform/IRQ/NMI overhead and 100 Hz margins
remain unresolved; unknown service budgets stay zero and deadline guards stay
fail-closed. A lower structural work count is not runtime admission.

## Ownership, preservation and planning completion

Graphics owns the helper's temporary scalar arithmetic. Environment remains
fixture owner, Diagnostics requested-camera owner, Input semantic-edge owner,
Presentation snapshot owner and Platform hardware owner. No new state, tables,
continuation phases, memory reuse, MAP operation, platform seam or handler is
proposed. The 289-byte geometry cache/320-byte HUD workspace lifetimes and all
cancellation/failure invalidation paths remain unchanged. Backing/output mapping
and display admission obligations remain unchanged.

Planning has no register/clobber, CPU-visible/physical-memory allocation,
MAP/base-page, DMA, timing/deadline, IRQ/NMI or persistent-state effects; all are
not applicable. A future pure-C candidate can change compiler register saves,
static scratch, stack and instruction cost; actual output must account for it.
No precision reduction, reserve use, bank relocation or memory-limit increase.

Planning completion requires current main/CI, all virtual reconstruction pins,
reference cost/call-count figures, fixed cohort cardinalities, local links,
JSON/whitespace and preservation checks. Only this intent, its proposed manifest
and WIP change. Preserve every predecessor packet/report/source and all unrelated
entries and working paths. No implementation, source restoration, host test
suite, target build, Xemu, D81, SD, physical testing, commit, push, PR or merge
occurs during this planning task. Stop READY FOR REVIEW, pending I1–I6.
