# M2 banked renderer — proposed bounded Build Intent

28 October 2026. Identity: **65AERO-M2-BANK-INTENT-1**.
**BR-D1–BR-D6 APPROVED for design/budget investigation on 29 October 2026.**
RF-EX2 remains proposed. The current result is in the existing
[RF feasibility contract](65AERO_M2_RESIDENCY_FEASIBILITY.md#rf-ex2--current-source-design-and-budget-investigation).
The exact original planning version is archived in the new design packet.
Main: `b20f91cb8023ea02e33d5fec6870026023bd8fbf`, PR #28.
Fresh fetch and independent ls-remote agree; exact-main push
[CI 40767414470](https://github.com/SUON1/f65-megawing/actions/runs/40767414470)
completed/success. Planning branch `codex/65aero-m2-banked-renderer-intent`
is directly based on that commit. No implementation or relink is authorized.

## Objective and first gate

Prepare a source-pinned banked-renderer path for the integrated, mutable-camera
minimum renderer without relaxing numeric precision, the 24,575-byte resident
ceiling, stack envelopes, zero reserve or 100 Hz / 21-stage timeline.
This is the next Build Intent, not another replacement architecture paper.
The integrated [RF contracts](65AERO_M2_RESIDENCY_FEASIBILITY.md) remain intact.

**Capacity preflight FAIL for banking alone under RF-EX1.** The current deficit
is larger than the entire approved 8 KiB bank. This plan must not authorize an
implementation that assumes the historical 2,175-byte deficit still applies.
The recommended immediate next task is bounded contract/budget reconciliation,
not a speculative target build. Actual prototype authorization comes separately
only after its capacity, exact membership and service design are reviewable.

## Authority and reference identity

Inspected controlling material: repository instructions, CURRENT_STATE, WIP,
[workflow](../DEVELOPMENT_WORKFLOW.md), [manifest](../../spec/manifests/spec-corpus.json),
[Main v1.8](../../spec/core/F65_Main_Concept_v1.8_APPROVED_AMENDMENT.md) and its
[v1.7 base §§5.1–5.3](../../spec/core/F65_Main_Concept_v1.7_HUMAN_APPROVED.md),
[Runtime v1.2 candidate](../../spec/core/F65_Runtime_v1.2_APPROVED_CANDIDATE_AMENDMENT.md),
[Phase 1 owner/gate plan](65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md),
[M2 PR2 intent](65AERO_M2_PR2_BUILD_INTENT.md), approved RF-CODE-1/RF-MAP-1/
RF-BOOT-1 and RF-EX1, [Platform registry](../../interfaces/f65_platform_abi.json5),
[minimum profile](../../interfaces/m2_rebuild.json),
[ledger](../../memory/m2-rebuild-ledger.json),
[baseline intent](65AERO_M2_MINIMUM_REBUILD_BUILD_INTENT.md), and
[correction handoff](../reports/M2_MINIMUM_REBUILD_CORRECTIONS.md).
Graphics v2.1 §9 and Runtime's incorporated memory rules remain required
production authority as identified in the approved RF contract; no new exception
is inferred from those references. This checkpoint does not requalify hardware.

Measured reference: the sealed corrected target
[target-1793167696482111000](../evidence/flight-demo/2026-10-27-m2-min-rebuild-corrections/target-1793167696482111000/).
PRG SHA-256 `1873c76d7b13f438244d5c3f99d8c80bc951af47cda9fc5ba9a6fadbeb4eda51`.
It predates publication; application inputs are compared to main, not relinked.
The later SDK-path correction is host tooling only. Original failures and the
consumed one-relink claim remain unchanged. New experiments require new identity,
new evidence root and separate relink authorization, never reuse of that claim.

| Current actual allocation | Bytes |
| --- | ---: |
| BASIC prefix | 22 |
| Text | 29,711 |
| Alignment | 2 |
| Read-only data | 1,439 |
| Initialized data | 0 |
| BSS | 1,475 |
| Compiler static scratch | 190 |
| Total resident, physical [$002001,$00A048) | **32,839** |
| Resident acceptance ceiling [$002001,$008000) | **24,575** |
| Actual deficit | **8,264** |

Renderer workspace is 676 target bytes. It is already charged to BSS; do not
subtract it again or assume it can move. The PRG is 31,176 file bytes, which is
not resident usage. Hardware/software stacks remain 256/4,096-byte envelopes;
whole-program bounds remain UNPROVEN. All eight operation grants, guard grant
and launch enablement remain zero. Runtime startup, service and Xemu admission
are not inherited from another candidate.

## Capacity arithmetic and current code costs

For unchanged code sizes, let B be resident bytes genuinely removed into the
bank, S be separately proved additional resident savings, and H be all added
resident costs. Required: **B + S >= 8,264 + H**.
Bank body capacity is at most bank capacity minus the 16-byte signature and
any bank alignment, veneers, duplicated helpers or additional bank overhead.
Do not count bytes copied to the bank but retained resident as B.

RF-EX1 allows at most 8,176 body bytes. Even if every one displaced a resident
byte, S must be at least 88 + H. Retaining RF's 363-byte minimum additional
DATA gives **S >= 451 + R**, where R is all other resident overhead. The ideal
residual is 32,839 - 8,176 + 363 = 25,026, still 451 above the ceiling.
Any unfilled bank space or added bank overhead makes that requirement larger.
Compiler/code-size changes are not bounded by this simple relocation equation:
count any demonstrated net reduction separately, never assume it beforehand.

The historical 4,374 relocation / 2,199 headroom / 363 data / 1,836 other-cost
allowance is preserved for its original 26,750-byte candidate. It is not a
current budget. Applying only that 4,374-byte removal to today's reference
would leave 4,253 bytes over the limit after the 363 minimum, before R.
The previous nine resumable bodies and helper allowlist are not present as that
implementation in the new baseline; do not import unrecovered source or pretend
its source identity survived.

Read-only linked symbol sizes identify current review targets:

| Current symbol | Bytes |
| --- | ---: |
| m2_project_prepared | 1,900 |
| interpolate_delta | 1,257 |
| m2_multiply_q46 | 1,054 |
| m2_transform | 936 |
| plane_distance | 946 |
| to_camera | 651 |
| project_axis | 536 |
| m2_camera_valid | 531 |
| rounded_ratio | 255 |
| sine | 232 |
| Sum of these ten symbols | **8,298** |

This is a cost inventory, **not an admitted relocation closure**. Public wrappers,
shared callers, constants, helper dependencies, linker clones and ABI boundaries
must be classified. The ten bodies plus the signature already require 8,314
bytes. Moving all ten hypothetically leaves 329 bytes of deficit after the
363 minimum, before R. Merely making room for these symbols does not close fit.
Actual shared compiler helpers such as __udivdi3 and __muldi3 require a complete
caller audit; neither may be blindly moved, duplicated for free or granted new
bank permissions. RF's old helper allowlist must be reconciled by design review.
Current PREPARE invokes the integrated transform/registration; PROJECT invokes
one complete segment. Existing raster continuations do not prove these operations
meet a banked IRQ-masked service budget. No historical resumable implementation
or historical timing result is substituted.

## Exact founder decisions and recommendations

| ID | Exact decision requested | Recommendation |
| --- | --- | --- |
| BR-D1 | Adopt PR #28 and its exact corrected target as the reference; supersede use of the old 2,175-byte deficit for this task only? | **Approve.** Use 8,264 and preserve the old RF calculation as historical. Keep source/precision/public records and all failures unchanged. |
| BR-D2 | Retain RF-EX1 with an additional proved recovery requirement, or request a larger development-only bank design? | **Recommend a design-only RF-EX2 request for one 16 KiB bank**, specified below. Do not implement or activate it. The existing 8 KiB bank cannot solve this alone; keeping it requires separately scoped and measured S >= 451 + R even at ideal occupancy. No automatic optimization campaign or increased resident ceiling. |
| BR-D3 | Approve a bounded current-source closure/budget design replacing reliance on the historical nine bodies? | **Approve design only:** enumerate actual transform/project roles, exact current bodies and every shared/private helper; price bank and resident copies, wrapper/continuation data and all gateway/loader costs. Constants/font/cache stay resident. Stop if sufficient net recovery cannot be justified; do not widen membership to other owners or implement speculative arithmetic changes. |
| BR-D4 | Preserve the protected per-call gateway and reset-only boot safety requirements during that reconciliation? | **Approve.** Keep per-invocation signature verification, canonical restoration, non-reentrancy, fail-closed lockout, full boot leases and retirement; no cached-verification shortcut or weakened fault handling. Resolve descriptor offsets/private typed roles in the reviewed versioned design before generating code. |
| BR-D5 | Require complete memory, stack and service feasibility before execution, with exact stage boundaries? | **Approve.** Use the gates below; unknown timing/stack is UNPROVEN, never PASS. The next design task may specify bounded continuations but cannot implement them. A later separately approved prototype gets frozen host/oracle checks and one complete candidate relink, then stops at its first failed gate. |
| BR-D6 | Approve scope, preservation and handoff boundaries? | **Approve.** Immediate follow-on is contract/budget design only, stopping at READY FOR REVIEW. No relink, Xemu, D81, SD, physical testing or publication without separate authority. Reviewed contract adoption must be integrated before a new prototype branch. Source baseline and banked prototype remain separate increments. |

All six were approved for **design reconciliation only**, not banked
implementation. The original suggested disposition is retained below:

> Approve BR-D1–BR-D6 as recommended for design only. Finalize the existing RF
> feasibility contract against the current baseline, including the proposed
> RF-EX2 and complete current-code budget. Stop at READY FOR REVIEW or a failed
> gate. Preserve evidence and unrelated paths. No implementation, relink, Xemu,
> D81, SD, physical testing or publication.

## Proposed RF-EX2 review envelope — NOT APPROVED

This is an exact requested exception for review, not a change to RF-EX1 or
permanent production ownership. If declined, retain RF-EX1 and return a bounded
additional-recovery proposal; do not select that optimization automatically.

| Resource | Approved RF-EX1 design | Proposed RF-EX2 design-only request |
| --- | --- | --- |
| Immutable Graphics bank, physical | [$048000,$04A000), 8 KiB | [$048000,$04C000), 16 KiB |
| CPU execution alias | [$8000,$A000) | [$8000,$C000); never cover software stack at $C000 |
| Remaining Graphics workspace | [$04A000,$050000), 24 KiB | [$04C000,$050000), 16 KiB; prove simultaneous demand, including failures |
| Reset-only bank-0 landing lease | [$008000,$00A000) | [$008000,$00C000); lease begins at PRG load |
| Exclusive ResourceManager boot staging | [$050000,$052000) | [$050000,$054000); other resource users blocked for the full lease |
| Maximum PRG payload span / file bytes | 32,767 / 32,769 | 40,959 / 40,961, including holes and 2-byte load address |

The enlarged staging proposal overlaps $053000–$053FFF of the retained proof
audio-cache band. That is an **additional explicit boot-only exclusivity
exception**, not free memory. No audio/decode/DMA/resource lease may overlap;
if boot sequencing cannot prove this, reject RF-EX2. Runtime ResourceManager
ownership is restored after verified retirement. [$054000,$058000), including
the remaining audio/DMA/proof reservations, is excluded from staging. Protected
reserve [$058000,$060000) remains untouched, as do simulation, audio-state,
display, assets, Color RAM, base page/stacks/vectors/results and ROM backup.

RF-EX2 conflicts with the exact RF-EX1 ranges, its excluded ResourceManager
subrange, RF-CODE-1 workspace envelope and RF-BOOT-1 load/copy bounds. Main/Runtime
and Graphics workspace-only production allocation also requires the explicit
versioned exception. Finalize these changes together in the existing RF document,
including the current-source role/helper contract; do not silently amend the
production map, registry or generated ledgers. No new MAP register immediates
are admitted by address arithmetic; derive and independently verify exact linked
selection/restoration under Platform ownership before execution.

At 16 KiB, theoretical body capacity is 16,368 minus other bank overhead. With
S=0, total H could be at most 8,104 minus that overhead **only if** sufficient
current code actually relocates. After the old minimum DATA, the theoretical
allowance for R would be 7,741 minus bank overhead. This is a capacity ceiling,
not headroom, a forecast or a supplied overhead budget. The ten-symbol example
above still fails; a larger bank alone is not evidence of recovery.

The 363-byte data minimum remains a historical lower bound pending exact
current control/readback/continuation layout. No true cost is set to zero.
Charge gateway and verification, typed calls, result preservation, loader/CRC,
restoration/lockout, tables, padding, compiler scratch, clones and duplicated
helpers. Require actual whole-program peaks, not additive symbol guesses.

## Required prototype gates after separate design adoption and authorization

1. **Contracts and budget, before source implementation.** Integrate reviewed
   current-source RF revision/exception and private generated owner classes,
   descriptor/signature offsets and entry roles. Preserve public ABI and FULL
   profile. Supply a closed relocation/removal inventory and priced overhead
   budget satisfying resident, bank, load and workspace limits. At this checkpoint
   the current 8 KiB banking-only proposal FAILS; RF-EX2 feasibility is UNPROVEN.
2. **Host correctness and isolated failure proof.** Freeze independent 3,857-case
   geometry and 841 near/far oracles, numeric extrema/ties/overflow checks, camera,
   common horizon, generation cancellation, held snapshots, faults and per-tick
   replay. Test the gateway model with missing/wrong/unreadable/changed-between-
   calls signatures, repeated calls, incorrect spatial mapping, nested calls,
   unsafe restoration and boot partial-copy/CRC/lease failures. All model results
   remain host evidence only. Prepare the nine selected segments once per
   generation, preserve cache/cancellation and complete frame/record publication.
3. **One actual complete compile/link after host gates.** Use the unchanged
   pinned LLVM-MOS compiler/flags and absolute SDK inventory. Link real mutable
   camera, runtime, input, fonts, both bank/resident closures, protected gateway,
   loader, fault paths and compiler helpers. Retain raw/sealed image identities,
   source/tool inputs, map, VMA/LMA/run ranges, scratch and every failure. Prove
   resident <=24,575, adopted bank/load/workspace bounds, zero reserve, no owner
   collision and no hidden uninitialized allocation. Any descriptor sealing is
   separately specified and proves unchanged addresses/extents/outside bytes.
   Failed fit stops: no second link, automatic rewrite, new capacity or execution.
4. **Exact startup/ABI/stack/service static proof.** Recheck MAP/B/CPU port before
   dependent BSS accesses, independent raw entry/terminal control flow, the entire
   reachable boot/runtime/helper/IRQ/NMI/fault stack graph and bank call/return
   edges. Unsupported paths stay UNPROVEN. Private enter/leave preserves X/Y/Z/B,
   compiler pseudo-registers and both SPs; save result before A is clobbered.
   Restore both MAP selectors/masks/offsets, EOM, B=$02, Z=0, E=1, CPU-port $2F/$35,
   admitted I/O, vectors and P before yield/public calls. Charge all eight slots,
   begin/service/commit, guard/clock, 16 signature reads on every call, body/helper
   work, restoration, calls/returns and legal IRQ/NMI interference. Each admitted
   quantum fits before the authoritative tick with no skipped/merged ticks.
   Whole transform/segment work cannot be declared bounded merely because its
   loop count is finite. Stop at the exact offending operation; no average-time
   admission or fabricated nonzero grant. Launch remains disabled.
5. **Review, then separate execution authorization.** Even all static gates PASS
   does not prove actual bank execution/return or visual behavior. Later exact-PRG
   PAL/NTSC Xemu must observe actual bank execution and canonical return, repeated
   per-call verification, signature fault lockout, stack/state restoration,
   unchanged 100 Hz replay, sky/ground/runway, camera and honest telemetry.
   No Xemu is authorized by this plan or the recommended next decision.

Reset-only boot retains the RF four full N-byte copy/verification passes,
CRC-32/ISO-HDLC, resident descriptor/readback and verified landing zero/readback
before release/READY/first tick. For proposed N=16,384, 1–255-byte chunks require
260 chunks for those four passes (65 each), 65,536 copy bytes and 32,768 CRC
bytes; landing retirement additionally writes/reads all 16,384 landing bytes.
Include every failure lifetime and safe quiescence state. No DMA, reload,
retry/repair, ROM return or reuse of stale staging as an executable source.

## Scope, hardware effects and stopping point

This planning checkout changes only this Build Intent, WIP and a fresh static
planning receipt. Generated files, authority, source, target artifacts and
historical packets remain unchanged. Actual register/clobber, CPU/physical
memory, MAP/base-page, DMA, timing and IRQ/NMI effects: **none in this task**.
The proposed future effects are bounded above; they are not current permissions.
Persistent public/serialized layouts: unchanged. No banking code, arithmetic
optimization, new fonts/display design, physics or aircraft work is authorized.

The next design must establish whether the enlarged Graphics code/workspace
trade is acceptable for this development profile and future engine service
capacity. It grants no spare-memory or performance claim for M3/M4/FULL.
If the closed current-code budget or service design still fails, stop and report
one next separately scoped alternative. Do not begin a minor-optimization series.

Validation here is documentation/static/hash/preservation only: verify reference
seal and application identity, recompute arithmetic from retained sections and
symbols, check links/JSON/whitespace, exact branch ancestry and focused scope.
The [planning receipt](../evidence/flight-demo/2026-10-28-m2-banked-renderer-intent/planning.json)
records results. No host behavior tests, target tools, compile/link, Xemu, D81,
SD, physical test, commit, push, PR or merge is performed. Historical recovery
remains 22 previously verified / 15 unresolved; eight old checkouts remain
NOT VERIFIED at Git-worktree tier. No reconstruction or historical regrading.

**Completion: READY FOR REVIEW of this plan. Implementation admission is held
at the failed current capacity gate; RF-EX2 and the current-code budget require
founder disposition and reviewed adoption.**


## 29 October design result

The existing RF contract now records the itemized current closure and lifetimes.
Optimistic removal is8,625; separate363 data fails by2 before other overhead.
An explicit same-Platform cfworkspace readback lease can reduce incremental
reference data to108, leaving253 for every new resident code/data cost, all still
unpriced. This refines the earlier historical363 assumption; it is not fit PASS.
Current renderer arena demand is0/16,384; renderer676 stays resident. Contiguous
16 KiB staging conflicts with4 KiB of retained Audio cache and requires explicit
disposition before implementation. RF-EX2 is not approved merely by investigation.
No new target image, execution permission or generated allocation exists.


## Final P2 disposition — 29 October

The corrected source-pinned CRC helper is84 bytes and remains resident;
relocation8,625 and conditional pre-overhead allowance253 are unchanged.
Full protection/loader/stack/compiler/service costs remain unbounded, so final
fit is not established. Contiguous staging is BLOCKED BY MEMORY OWNERSHIP:
its4,096-byte Audio overlap has no authorized exclusive boot lifetime.
**Recommend REJECT OPTION A**. This supersedes the earlier suggested next cost
probe: no bank implementation, larger bank or optimization campaign follows.
See the revision5 existing RF contract and completed validation packet.
