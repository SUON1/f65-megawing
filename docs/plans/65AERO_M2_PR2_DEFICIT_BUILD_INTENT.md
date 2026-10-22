# M2 PR2 resident-deficit recovery — bounded transform experiment

**READY FOR REVIEW — planning only; S1–S6 await founder approval.**

Prepared from verified main `b3406ed8b9e141b50ca7ea7d3b5edd169c1ae310`,
[PR #22](https://github.com/SUON1/f65-megawing/pull/22).
Fetched origin/main, local main and the clean main worktree agree;
[exact-main static CI](https://github.com/SUON1/f65-megawing/actions/runs/39711685106)
is successful. Planning branch: `codex/65aero-m2-pr2-deficit-intent`.
This document proposes one future experiment; it authorizes no implementation.

## Objective and current evidence

Reduce the remaining resident deficit through one compact, fixed-sequence
transform-construction experiment, with exact numerical behavior and unchanged
memory limits. Establish the actual saving before choosing another target.

The accepted [Q46 publication](../reports/M2_PR2_Q46_PUBLICATION.md) integrates
the private limb helper and its rotation call-site. The full renderer/cache/
dispatch implementation remains outside main's active source tree; its committed
snapshots and failures are evidence, not accepted runtime code. Consequently,
11,718 bytes is the deficit of the retained full-development composition,
not a fresh full-renderer measurement of main.

The [recorded comparison](../evidence/flight-demo/2026-10-21-m2-q46-limb16/comparison.json)
and [link report](../evidence/flight-demo/2026-10-21-m2-q46-limb16/relink/build.json)
establish:

| Resident component | Bytes |
|---|---:|
| Text | 32,933 |
| Read-only data | 1,505 |
| Initialized data | 2 |
| BSS | 1,611 |
| Compiler scratch in `.noinit` | 216 |
| BASIC header / alignment gaps | 22 / 4 |
| Total | **36,293** |
| Allowed span `$2001–$7FFF` | **24,575** |
| Deficit; end exclusive | **11,718; `$ADC6`** |

Retained target SHA-256:
`1d4605236b408b1273fee14c915ae85e1779c6b9bc752dbbb1b9f0a0f15940a9`.
All addresses above the ceiling describe a failed artifact, not admitted memory.

The [symbol listing](../evidence/flight-demo/2026-10-21-m2-q46-limb16/relink/RENDER.symbols)
identifies the main individual costs:

| Symbol | Own code bytes | Implication |
|---|---:|---|
| `m2_transform` | 3,112 | Largest individual routine; repeated wide expression/call setup is a bounded structural target. |
| `m2_project_prepared` | 1,959 | Transformation, six-plane clipping and projection must retain their numerical behavior. |
| `interpolate_delta` | 1,605 | General clipping arithmetic remains necessary; the Q46 replacement did not remove it. |
| `overlay` / `telemetry` | 1,104 / 1,020 | Required anchors, labels, counters and missing-state output remain charged. |
| `m2_multiply_q46` | 1,054 | Accepted exact implementation is frozen for this experiment. |
| `m2_registration_matches_prepared` | 1,025 | Private owner checks remain required in the reconstructed reference. |
| `plane_distance` / `m2_raster_begin` | 946 / 945 | Precision and cursor bounds remain protected. |
| `__udivdi3` / `__muldi3` | 855 / 296 | Shared runtime code is still reachable and cannot simply be subtracted. |

These are individual symbol sizes, excluding callees; they are not subsystem
totals or promised savings. Eliminating all 3,112 transform bytes would still
leave 8,606 bytes of the current deficit before secondary layout effects.
The proposed replacement must itself occupy code/data. It cannot plausibly
close the whole gap alone. Anchor/cache wrappers alone are also insufficient:
`anchor` and `cache_segment` occupy 439 and 437 own bytes respectively.

## Governing authority and inspected contracts

Retain the hierarchy and approved D/F decisions in the
[PR2 intent](65AERO_M2_PR2_BUILD_INTENT.md),
[renderer-admission intent](65AERO_M2_PR2_RENDERER_ADMISSION_BUILD_INTENT.md)
and [entry plan](65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md): Main v1.8,
Gameplay v1.2, Runtime v1.2 approved candidate (NOT FINAL), Graphics v2.1 and
Physics v4.1 with their incorporated bases, as pinned by the
[corpus](../../spec/manifests/spec-corpus.json). No amendment is proposed.

Inspected contracts include [PR1 numerical/public layouts](../../interfaces/m2_pr1.json),
[full composition](../../interfaces/m2_full.json),
[full memory ledger](../../memory/m2-full-ledger.json),
[geometry](../../src/graphics/m2_geometry.c),
[accepted helper](../../src/graphics/m2_q46_private.h), the retained renderer/
cache/dispatch source and builder, and the Q46 arithmetic/carry/stack evidence.
The [workflow](../DEVELOPMENT_WORKFLOW.md),
[programming principles](../PROGRAMMING_PRINCIPLES.md) and
[C standard](../CODE_STYLE_C.md) govern any later approved implementation.

## Exact founder decisions

| ID | Decision requested | Recommendation |
|---|---|---|
| S1 | May the next build reconstruct the failed complete-development reference from main plus retained snapshots? | **Yes, in a fresh isolated experiment branch.** Restore only the 16 paths pinned in the reconstruction manifest; verify all 79 recorded input hashes. Keep main's accepted limb helper/tests. This is experiment setup, not acceptance of the unmerged renderer/cache work. First reproduce the resident bill and function sizes with the locked toolchain/recipe; stop on an unexplained mismatch. |
| S2 | What optimization is authorized? | **One compact transform-construction candidate only.** Replace repeated Q46 expression/call setup in `m2_transform` with one fixed bounded operand/operation sequence, using private constant descriptors or loops. Preserve the same 14 rounded Q46 products, including the two rounded intermediate products, the same signed additions/subtractions and final nine coefficients. Do not change the Q46 helper, clipping, anchor/cache algorithms, platform code or compiler flags. |
| S3 | May precision, validation, interfaces or memory rules change to obtain fit? | **No.** Preserve Q46/Q24/Q16 semantics, all camera/fixture bounds, public signatures/layouts and failure/output behavior. Preserve temporary-result publication so supported aliasing is unchanged. Charge any private descriptor table, compiler scratch and padding. Retain `$8000` resident ceiling, 4 KiB software-stack envelope, existing hardware-stack/base-page bands and zero reserve use. No bank relocation, memory-limit increase, assembly or generated-contract change. |
| S4 | What constitutes success and when must work stop? | **Measure one reference and one candidate composed relink.** A smaller fully charged resident span is a bounded size result; full fit still requires every section within the existing span. Report saving/regression and remaining deficit immediately after candidate relink, then stop implementation regardless of outcome. No second candidate or follow-on optimization. The known reference fit failure is the authorized starting observation, not a waived final gate. |
| S5 | What proof and compiler/ABI evidence are required? | **Host/oracle/sanitizer and compile/link/static only.** Prove exact transform equality for all 5,270,760 legal yaw/pitch/roll combinations against the retained expression implementation; retain an independent unbounded-integer oracle for signs, staged rounding, cancellation and extrema. Rerun Q46/carry, 3,857 Decimal and 841 clipping regressions plus renderer identity/image checks. Account for actual code, rodata, BSS, scratch and stack/callees; retain compiler/flags. Structural work bounds do not admit cycle WCET or the 100 Hz dispatcher. |
| S6 | What remains frozen, and what later authority is granted? | **Preserve every historical artifact and unrelated local path.** Keep all 17 cached segments, four protected anchors, deterministic labels, telemetry, generation cancellation/invalidation, workspace lifetimes and deadline guards. No Xemu, D81, SD, physical testing, runtime/display acceptance, publication or later milestone. Return to READY FOR REVIEW with measured results, or stop and report the first unexpected failed prerequisite. |

Suggested approval text:

> Approve S1–S6 as recommended. Authorize reconstruction of the pinned failed
> composition and one compact transform-construction experiment from verified
> main, preserving exact arithmetic, memory limits, evidence and unrelated paths.
> Run the specified host/oracle and target compile/link/static checks. Report
> immediately after the candidate relink and stop at READY FOR REVIEW or an
> unexpected failed prerequisite. No further optimization, Xemu, D81, SD,
> physical testing, commit, push, PR or merge.

## Reconstruction and bounded execution sequence after approval

1. Reverify main and its exact CI; create a fresh experiment branch/worktree.
   Use the [proposed reconstruction manifest](65AERO_M2_PR2_DEFICIT_RECONSTRUCTION.json).
   Sixty-three inputs already match main; 16 have exact committed snapshot
   sources. Verify all 79 hashes from the linked build report before compiling.
   Do not overlay entire evidence directories: predecessor snapshots also
   contain the superseded Q46 helper/tests, which must not replace main's code.
   Preserve the original mutable development checkout byte-for-byte.
2. Reproduce the complete early renderer reference using its locked compiler,
   opaque backend, source list and flags. Normalize fresh output paths only;
   retain commands, source/tool hashes, map, symbols and disassembly. Verify
   resident sections, function sizes, owners and cache layout against the record.
   A differing PRG hash must be explained by demonstrated path-only metadata
   differences or the task stops; do not silently accept a new reference.
   The historical fit FAIL is expected. No active display adapter is present.
3. Implement only the S2 candidate and its focused tests. A private fixed
   operation sequence may share call/assignment machinery; it must not regroup
   products, fuse rounding stages, add overflow-prone intermediate expressions
   or write partial public results. Tables are private Graphics implementation,
   not duplicated public layouts. No attempt to infer anchors from clipped
   endpoints, remove registration checks or reclaim the 289-byte cache.
4. Before candidate relink, pass exhaustive old/new matrix comparison, the
   independent arithmetic oracle and existing host regressions. Camera position
   does not affect a valid rotation matrix, but accepted/rejected position bounds,
   null/output-preservation and supported alias cases must be covered separately.
   Retain all failures; do not weaken an oracle or error tolerance to proceed.
5. Perform the single candidate composed target relink with the identical recipe.
   Immediately report own function bytes, newly introduced tables, all sections,
   actual owner allocations, compiler scratch, padding, total resident span,
   end/ceiling, remaining deficit and exact artifact hashes. Include conservative
   execution-work and reachable stack analysis, identifying unsupported paths.
   If fit still fails, stop; no full adapter/service/display gate may follow.

Required commands carried forward include `python3 -B tools/flight_demo/m2/build.py`
and, after approved reconstruction, `python3 -B tools/flight_demo/m2_full/renderer_build.py`.
The latter's nonzero result for the expected reference fit failure is retained
explicitly; no ignore-failure convention applies to other checks. Use fresh
command records for focused matrix and existing Q46 equivalence/carry suites.
No host, target or reconstruction command is run during this planning task.

## Ownership, memory and hardware impact

Graphics owns the future private matrix-building sequence and any descriptor
table. Environment remains fixture owner, Diagnostics owns requested camera,
Input owns semantic edges, Presentation owns snapshot publication and Platform
owns hardware. Generated/public records and their versions remain unchanged.

The reconstructed renderer's 289-byte cache continues sharing the 320-byte text
workspace only after synchronous HUD/footer transfer has ended its text lifetime.
Do not move matrix scratch into that union or other owners' memory. Keep every
cancellation/failure invalidation path. Display backing remains 320×200 at 2×
within 720×480 NTSC or 720×572 PAL reference outputs; display allocations and
mapping-admission obligations are unchanged.

Planning changes have no register/clobber, CPU-visible/physical memory,
MAP/base-page, DMA, timing, IRQ/NMI or persistent-state effects. A future pure-C
candidate can change emitted compiler clobbers, static scratch, stack and work
costs; these must be measured, not assumed unchanged from the Q46 helper's
13-to-9-byte closure result. There are no new hardware accesses or handlers.
Full integrated ABI/stack and service admission remain open. Unknown service
bounds continue granting no renderer work; compile/link cannot enable execution.

## Completion and next boundary

This planning handoff is READY FOR REVIEW when the main/CI pin, reconstruction
hashes, cost figures, local links, whitespace and preservation checks pass.
Only this intent, its proposed reconstruction manifest and planning WIP change.
Implementation awaits explicit approval of S1–S6.

After a future approved experiment, report both the bounded size result and the
separate full-fit/runtime status. Even positive savings do not close M2 PR2 or
authorize another experiment. If one compact transform does not establish a
credible path toward the remaining deficit, the next decision should be a
separate architecture/fit review of the remaining composition, with no implied
precision reduction, reserve use or memory expansion.
