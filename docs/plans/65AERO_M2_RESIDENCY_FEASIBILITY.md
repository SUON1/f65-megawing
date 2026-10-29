# M2 recovery exit and residency feasibility

29 October 2026. Identity: **65AERO-M2-RESIDENCY-FEASIBILITY-1**, revision 5 (RF-EX2 P2 correction and final disposition).
**READY FOR REVIEW — RECOMMEND REJECT OPTION A.**
**RF-EX2: BLOCKED BY MEMORY OWNERSHIP; complete resident/service budget UNPROVEN.**

BR-D1–BR-D6 are approved for design/budget investigation only. The new
[RF-EX2 investigation](#rf-ex2--current-source-design-and-budget-investigation)
below records the current result. Sections preceding it retain revision 3
RF-EX1 approval and historical calculation; they do not admit RF-EX2. The exact
pre-investigation documents are archived in the new evidence packet. Statements
there about the then-missing source apply to 27 October, before PR #28.

This is the approved, versioned M2 development design. The incomplete historical
packet remains unadopted; no banked implementation or active allocation is made.

## Baseline and disposition

GitHub main was freshly fetched and independently checked with ls-remote:
`af3b0913c4b73eb6b8add638fb88bdbbae158036`.
Its exact push [CI run 40259907202](https://github.com/SUON1/f65-megawing/actions/runs/40259907202)
is completed/success. The initially clean new branch is
`codex/65aero-m2-residency-feasibility`, based directly on that commit in a
durable Developer checkout. The original dirty checkout was not switched,
reset, cleaned or repurposed. No damaged checkout supplies the source baseline.

The founder's Recovery Exit directive is the Build Intent: end recovery as a
prerequisite; prepare a small current contract; reconcile the budget; prototype
only if legal and fully costed; stop at a required decision or failed gate.
The founder now approves RF-D1, RF-D2, RF-D3 and RF-EX1 as reviewed for
controlled M2 development design and publication. Source-baseline import and
bank implementation remain separate increments. The exact reviewed revision
and its successful checks are retained without rewriting their results.
“Cost” clarification concerns model tokens and money, not target byte or safety
limits. No further APFS, snapshot, Trash or historical-worktree search occurred.

The former 37-member adoption packet remains **incomplete and unadopted**:
22 members were previously SHA-256 verified; 15 were not verified recoverable.
Its retained inventory SHA-256 is
`1e932efe541468afce20081b9654186b457c458b24d70df992a6c911b2233447`.
Those are historical findings, not a new full-packet preservation PASS.
Eight historical checkouts remain **NOT VERIFIED at the Git-worktree tier**;
available byte-level findings do not establish ancestry. No missing files,
metadata, logs, timestamps or test results were reconstructed. The old
MAP-2/BOOT-2/CODEBANK-2 drafts inform this proposal only. Their exact informing
identities are recorded in the [calculation](../evidence/flight-demo/2026-10-27-m2-residency-feasibility/accounting.json);
no private journal or recovered packet contents are copied into this checkpoint.

## Approved development disposition and exact placement exception

On 27 October the founder approved RF-D1–RF-D3 and RF-EX1 as reviewed,
restricted to this versioned M2 development profile. The
[publication approval record](../evidence/flight-demo/2026-10-27-m2-residency-feasibility/publication.json)
binds that disposition to the exact reviewed revision. This approves the
design exception; actual placement, implementation and runtime admission still
require their own measured gates. Production ownership and public ABI do not change.

| Direction | Recorded disposition | Remaining boundary |
| --- | --- | --- |
| RF-D1 — Graphics code bank | APPROVED DEVELOPMENT DESIGN | RF-EX1 is the precise development-only exception; no physical allocation is activated here. |
| RF-D2 — protected gateway | APPROVED DEVELOPMENT DESIGN | Every invocation must verify its signature; exact linked ABI, MAP, stack and timing evidence remains mandatory. |
| RF-D3 — reset-only loading | APPROVED DEVELOPMENT DESIGN | Load-time and boot-only leases require exclusive ownership, verified retirement and actual resource evidence before use. |

Inspected authority: [manifest](../../spec/manifests/spec-corpus.json);
[Main v1.8](../../spec/core/F65_Main_Concept_v1.8_APPROVED_AMENDMENT.md) and
incorporated v1.7 §§5.1–5.3;
[Runtime v1.2 candidate](../../spec/core/F65_Runtime_v1.2_APPROVED_CANDIDATE_AMENDMENT.md)
and its incorporated base §§6.1–6.6;
[Graphics v2.1](../../spec/subsystems/F-65_Megawing_Graphics_White_Paper_v2.1.pdf)
§9 (pp. 11–12); [Phase 1 plan](65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md);
[M2 geometry intent](65AERO_M2_REGISTERED_RUNWAY_CAMERA_BUILD_INTENT.md);
[M2 PR2 intent](65AERO_M2_PR2_BUILD_INTENT.md);
[full ledger](../../memory/m2-full-ledger.json),
[PR1 ledger](../../memory/m2-pr1-ledger.json),
[Platform registry](../../interfaces/f65_platform_abi.json5) and
[published evidence](../reports/M2_GUARD_EVIDENCE_PUBLICATION.md).
Current authority and active generated allocations remain unchanged.

**RF-EX1 — APPROVED M2 DEVELOPMENT DESIGN EXCEPTION; NOT AN ACTIVE ALLOCATION:**

> For this separately admitted M2 minimum development profile only, permit the
> closed Graphics transform/project code bank in physical [$048000,$04A000),
> replacing workspace-only use of those 8192 bytes for the admitted lifetime.
> Retain [$04A000,$050000) as the remaining 24576-byte Graphics workspace.
> Permit only the private bounded Platform gateway and its closed C/helper
> calls while that bank is mapped at CPU [$8000,$A000). Grant a one-use bank-0
> [$008000,$00A000) payload landing lease from PRG load time and exclusive
> ResourceManager [$050000,$052000) boot staging under Platform execution.
> Keep all other owner bands, resident/stack limits, public ABI, FULL profile,
> protected reserve, 100 Hz clock and 21-stage order unchanged. This grants no
> permanent production allocation or general bank service.

Main's incorporated §5.1 and Runtime's incorporated §6.1 currently assign the
whole [$048000,$050000) to renderer workspace. Graphics §9 binds it to
vertices/buckets/spans/occlusion/staging and places renderer code under the
shared resident ceiling. The integrated PR2 intent separately forbids automatic
bank expansion. RF-EX1 is the explicit, founder-approved exception for this
M2 development design only. It does not edit those production authority bytes
or derive admission from disjoint byte arithmetic. The registry is unchanged;
its historical wrappers and allowlists gain no new executable permission here.

Only this exact versioned profile exception is approved. No permanent
production allocation, public ABI or live gateway is introduced. Implementation
is not authorized in this publication task. The source-complete unbanked
development checkpoint may retain a failing fit result with runtime enablement
disabled. The old RL approvals and historical drafts remain historical.

## RF-CODE-1 — proposed ownership and lifetime contract

Keep the nine-segment minimum selection [0,1,2,3,4,5,7,11,15] from the unchanged
17-segment Environment fixture. Retain sky/ground on the common camera horizon,
a controllable diagnostic camera, numeric telemetry, ALTITUDE and AIRSPEED
NOT IMPLEMENTED, and NON-FLIGHT DIAGNOSTIC. No omitted registered HUD cues,
ranked labels, physics, fake motion, weapons or AI are enabled.

The run bank is one immutable Graphics allocation, physical [$048000,$04A000).
It is an alias at CPU [$8000,$A000) only inside a protected scope.
Platform alone loads/selects/restores it. No nested bank, reload or runtime
writer is permitted. Only transform-step and project-step roles enter it.
Keep their begin functions, public wrappers, constants/tables/font, cached
geometry, continuations, input/result objects and compiler scratch resident.
Keep existing numerical precision and independent oracle tolerances.

The reference nine-body membership is in accounting.json. Its resident helper
closure is limited to __memset, __modhi3, __mulsi3, __umodhi3,
m2_min_bytes_any/clear/copy and m2_min_word_add/compare/half/increment/left/
negate/negative/subtract. Link reachability must prove the actual closure.
No guessed indirect entry, unlisted helper, literal pool, ROM call, MMIO,
callback, DMA, clock read or yield is allowed inside the scope.
Both entry offsets must identify their exact linked instruction boundaries
after the header, within the actual image length. A range check alone is
insufficient.

No bank pointer escapes. Prepared geometry is built once per captured
generation, retained across bounded continuations and invalidated on cancellation
or camera/generation change. Check coherence before entry and after canonical
exit. Immutable snapshots and complete-frame publication remain unchanged.
Bank code/data and resident lifetimes are charged separately; no borrowed
stack, display slack, Color RAM, ROM backup or protected reserve is allowed.


### Exclusions and lifetime ledger

All ranges here are half-open physical byte ranges unless explicitly called
CPU windows. The CPU window is an alias, not another 8192-byte allocation.

| Excluded allocation | Physical range / policy |
| --- | --- |
| Authoritative simulation, entity/system/sensor/AI state | [$010000,$018000); no bank, boot lease, descriptor or scratch allocation |
| Audio state, mission-hot queues and handoffs | [$018000,$01C000); untouched |
| Display controls and shared scratch | [$01C000,$020000); no borrowing |
| Display stores A and B | [$020000,$030000), [$030000,$040000); no code, landing or staging; all slack remains display-owned |
| Cockpit/HUD/MFD/sprite/palette assets | [$040000,$048000); no borrowing |
| Remaining Graphics workspace | [$04A000,$050000); no bank aliases or runtime bank writes; actual simultaneous workspace demand must fit these 24576 bytes |
| Other ResourceManager/audio/decode/DMA users | [$052000,$058000) excluded entirely; [$050000,$052000) exclusive during boot only |
| Protected measured-limits reserve | [$058000,$060000); zero draw |
| Color RAM | [$0FF80000,$0FF88000); presentation only, no bank/data substitution |
| Attic / protected ROM backup | no new Attic allocation; preserve [$08000000,$08020000) backup and its lifecycle |
| Low-memory stacks/base page/results/vectors | no bank/lease overlap; hardware [$0100,$0200), base page [$0200,$0300), software [$C000,$D000), resident vectors and declared result bands remain protected |

The existing proof registry's audio cache [$053000,$056000), DMA lists
[$056000,$057000) and proof-reserved [$057000,$058000) remain excluded.
These are retained proof-specific boundaries, not new production allocations.
The entire parent ResourceManager band remains [$050000,$058000);
no assumption that its first 8 KiB is free is made. An exclusive boot witness
must reject every audio, decode, DMA-list or resource lease conflicting with
[$050000,$052000), including one not listed in the old proof subledger.

The run-bank reservation begins at load/initialization and lasts through reset.
Partial boot contents are invalid and quarantined on failure. READY makes the
verified run image logically immutable; it is not hardware write protection.
Neither a frame cancellation nor a fault releases its physical bytes to another
owner. The 24 KiB remaining workspace is a proposed envelope, not a measurement
that the current or future renderer fits.

### Boot lease phases

| Phase | Landing / staging / bank eligibility |
| --- | --- |
| PRG load and early startup | Landing owned from load time, before C/ResourceManager; no bank execution or first authoritative release |
| Boot copy/verify | Landing, exclusive staging and run bank charged separately; resident loader/readback/descriptor/controls stay charged; READY false |
| Successful retirement | Verify run identity/CRC/entries; clear and read back all landing bytes; restore canonical mapping; release staging lease; only then READY and first tick release |
| Normal operation | Landing lease retired; bank-0 landing is not runtime capacity. Staging may be reused by its owner and its stale bytes confer no bank-call rights. Run bank is immutable until reset |
| Any failed phase | READY false; partial bank and leases quarantined; canonical lockout or resident terminal sink; no general operation, reload, fallback or retry before reset |

All lease state changes are owned by the protected loader, with ResourceManager
as the logical staging/landing lease owner. This does not assert that an
operational production ResourceManager already exists. Staging release is not
a claimed wipe. Every full-program witness must account failed-boot lifetimes,
not overlay loader/readback storage with later state by assumption.

## RF-MAP-1 — proposed per-invocation gateway contract

Require canonical entry, exact READY identity, retired boot leases, valid near
spans, no active mapping, no sticky fault and sufficient admitted deadline slack.
Platform alone owns the gateway, expected identity and mapping state.

For **every bank-call invocation**, including an already selected/loaded bank:

1. Validate entry conditions and save the declared context in owned resident
   storage. Save original P and mask IRQs before the first mutable MAP operation.
2. Perform any required bank selection/MAP/EOM.
3. Through volatile reads and an admitted compiler barrier, read and compare the
   expected 16-byte bank signature in the selected execution window.
4. Only a successful verification for this invocation permits the typed bank
   entry. A prior successful verification never authorizes a later call.
5. On missing, incorrect, changed or unreadable signature, execute no banked
   instruction. Restore canonical state, invalidate eligibility, set a sticky
   fault and lock out future dispatch until reset. If safe restoration cannot
   be established, remain in a protected resident terminal sink; do not return
   through an uncertain mapping.

Verification belongs to the protected gateway, never Graphics callers.
The existing informing wire format is retained as a proposal: 16 bytes consisting
of ASCII 65M2RUN2 and the first eight bytes of the expected build ID. This
checkpoint invents no new signature format or public ABI. A matching signature
is identity checking, not whole-bank integrity, hardware write protection or
proof of the physical address selected. Same-build stale staging aliases need
independent spatial/MAP qualification. If readable mapping or a safe read cannot
be established, admission is UNPROVEN; do not pretend an unreadable bus always
raises a detectable exception.

Private enter/leave helpers take no arguments, return status in A, preserve
X/Y/Z/B, logical compiler pseudo-registers $02–$21 and both stack pointers.
A aliases Q's low byte, so independent Q preservation is not asserted.
Banked C bodies use the pinned ordinary C ABI; no guessed assembly parameter
ABI is introduced. Preserve the body result before leave clobbers A.
Insufficient pre-entry slack may defer without body work; permanent identity,
range, signature or restoration failure may never masquerade as continuing or
completed work.

Restore zero MAP masks/offsets and both megabyte selectors, finish EOM, restore
B=$02, Z=0, E=1, CPU-port DDR=$2F/data=$35, admitted ROM/I/O state (including
D030=$44 where required), page-1 hardware stack, $C000–$CFFF software stack,
resident vectors and original P before public return/yield or clock work.
The proposed offset $040000 and block-4 selection parameters A=$00, X=$00,
Y=$00, Z=$14 remain derived design values, not executed qualification.

One scope contains at most one bounded body quantum plus entry, per-call
verification and restoration. IRQ masking is charged for that entire interval.
The unmaskable NMI path must remain resident, never touch MAP/bank/DMA/C state,
preserve return to the same mapping and retain sticky interference. Include its
legal races and fault exits in the exact control-flow proof. A nested call
cannot clear an outer token or return into an unmapped caller.


The gateway is **non-reentrant**: it owns one busy token and admits one body
quantum only. Canonical busy/reentry rejection before mapping cannot mutate an
outer operation. An illegal nested call while mapped takes the resident terminal
path without clearing the outer token or returning into its bank. No callback,
public service or IRQ/NMI path may initiate another bank call. Cached “loaded”
or “verified” flags never bypass the 16 current signature reads.

If selection is unnecessary, verification is still mandatory immediately
before the banked transfer. No authorized writer may alter the run image,
expected descriptor or entry identity between check and execution.
Unreadable/unsafe spans reject before dereference; if actual target readability
or mapping cannot be proved, runtime admission remains UNPROVEN. There is no
assumed bus exception or fabricated readback mechanism.

A signature failure after mapping uses resident code only: suppress the body,
restore canonical state, set sticky bank/Platform fault and prevent future
entries until reset. If restoration is uncertain, do not issue a public call,
reenable IRQs or RTS through an uncertain context; remain in the protected
resident terminal sink. A numeric/body failure may not become DONE because
leave succeeded. NMI interference remains sticky and is checked at all admitted
entry/exit/READY boundaries; the exact race proof is still required.

For every slot, its admitted bound must include pre-entry guard/clock,
selection, all 16 signature reads/comparisons and barriers, body/helper quantum,
typed result handling, canonical restoration, pending IRQ/NMI and return margin.
The bound must fit before the next authoritative release. There is no unbounded
retry, signature scan, copy loop or wait while mapped. Zero/unknown costs deny
entry; boot work completes before the 100 Hz timeline starts. These are required
bounds, not supplied cycle measurements.

## RF-BOOT-1 — proposed load and content contract

Use one reset-loaded self-contained uncompressed PRG at $2001.
Distinguish bank payload LMA [$008000,$00A000), CPU VMA [$8000,$A000) and
physical run destination [$048000,$04A000). The landing lease begins at load
time, before C or an operational ResourceManager. It is not runtime capacity.
The maximum bank-0 load span [$2001,$A000) is 32767 bytes, including all file
holes/padding; the PRG maximum is 32769 bytes including its two-byte load address.
BSS/noinit initialization may not overwrite the landing payload.

Before BSS/data/compiler-dependent access, prove canonical MAP/megabyte/B/Z,
CPU port/ROM/I/O, page-1 stack and interrupt policy from actual entry disassembly
and an independent control-flow check. Main's M1 startup cannot substitute for
the missing corrected minimum-renderer startup. Loader, descriptor, scratch,
vectors and both stacks must be outside the landing/mapped window.

After C initialization and the admitted Platform/ROM-backup/clock lifecycle,
but before first tick release, validate the pinned source/tool/command identity,
descriptor, exact length, entry roles and CRC-32/ISO-HDLC. Retain the informing
64-byte descriptor and 16-byte signature format; exact wire offsets require
the new adoption's single generated source, not handwritten public duplicates.
Require 16 < N <= 8192 and distinct role offsets 16 <= offset < N, each bound to
its exact linked instruction boundary. Expected identity comes from the pinned
resident descriptor, never from the unverified bank authorizing itself.

Use the exclusive [$050000,$052000) staging lease, checked full spans and
1–255-byte CPU-copy chunks. Four N-byte passes are landing→staging,
staging→resident readback/CRC, staging→run bank and run bank→readback/CRC.
At N=8192 this is 132 chunks, 32768 copied bytes and 16384 CRC-processed bytes.
Separately zero/read back all 8192 landing bytes before retiring the lease.
Only then release staging and publish READY after sticky-fault checks.
Stale staging bytes confer no runtime access. No retry, fallback or repair.

A new typed fixed-class facade must prove the unchanged backend's mailbox,
base-page, copy-span, stack and interference requirements; neither cfcopy nor
a historical wrapper gains new permissions by implication. No DMA submission
is introduced. Preserve protected ROM backup [$08000000,$08020000).
Boot failure leaves READY false, prevents bank execution and enters canonical
lockout or the resident terminal sink. Reset is the recovery boundary.

Pin every consumed source/generator/header/tool/SDK/linker input and exact flags.
Use the existing [LLVM-MOS lock](../../toolchain/f65_toolchain.lock.json);
do not change compiler or ABI flags. Any future post-link descriptor sealing
must prove unchanged outside bytes, addresses and extents and retain raw/sealed
identities; the earlier one-link descriptor protocol may inform that separately
reviewed recipe. No artifact is generated or sealed as a target here.
Runtime CRC identifies current bytes; it does not prove arbitrary transport
delivered fresh bytes. Direct-PRG length/structure and later transport acceptance
remain distinct.

## One reconciled feasibility calculation

The [published candidate record](../evidence/flight-demo/2026-10-25-m2-guard-evidence-publication/record.json)
identifies the historical diagnostic by PRG SHA-256
`10c6b083bd37392b8177d3211035a76c599894aa46bb11ff4a18851e97dab6e1`
and runtime inventory
`d5fce59c011225643d27d884454c7b7982e7a99dfbd4e1af598a4a4fb200a245`.
It reports resident 26750, limit 24575, deficit 2175, compiler scratch 77 and
reserve zero. These are that exact historical candidate's reported results,
not measurements of current main. Main contains no minimum executable,
resumable minimum functions or active bank implementation. No relink was done.

| Reference calculation | Bytes |
| --- | ---: |
| Historical resident | 26750 |
| Reference selected nine bodies | 4374 |
| Conditional resident after removing all nine bodies | 22376 |
| Resident ceiling | 24575 |
| Conditional gross headroom | 2199 |
| Minimum new descriptor/readback/control data | 363 |
| Conditional resident including that minimum | 22739 |
| Remaining allowance for ALL other resident costs | 1836 |
| Reference bank bodies plus 16-byte header | 4390 |
| Remaining 8192-byte bank capacity before other bank costs | 3802 |

**The 2199 figure is headroom after the original deficit, not gross code
recovery. The 363 figure is minimum DATA, not total banking overhead.**
4374−2175=2199; 2199−363=1836. If 2199 were instead gross removal,
26750−2199+363=24914: still 339 bytes oversized before code costs.
That interpretation is not the one in the hash-verified informing ledger.

Let R be all additional resident costs beyond the 363-byte data minimum and
the assumed removal of all nine reference bodies. Conditional fit requires
R ≤ 1836. R includes gateway and per-call signature code, typed trampolines,
normal restoration, boot/copy/CRC loader, additional fault/lockout code,
extra constants, padding, compiler scratch changes, unavoidable duplication
and changed code generation. Do not assume any of these is zero. The
[accounting input](../evidence/flight-demo/2026-10-27-m2-residency-feasibility/accounting.json)
lists each unpriced term. Added stack use is separately bounded inside the
existing 256/4096-byte envelopes and charged to actual owner peaks.

P2 per-call signature verification is now mandatory; its resident code,
additional storage if any, stack and timing increments are **unmeasured**.
The 363-byte minimum is retained; the true overhead is 363 + R, not 363.
No numeric signature surcharge is fabricated and no 1836-byte fit is claimed.
The older nine-body figures were independently matched to their sealed draft
identities, not remeasured against a surviving executable/map. Changed LTO,
retained clones/helpers or padding can invalidate the removal assumption.

At maximum load, [$2001,$A000) is 32767 bank-0 component bytes, plus
8192 staging and 8192 run bank = 49151. Do not add the resident span again.
At runtime, resident-plus-bank envelopes total 32767. Both figures exclude
separately charged stack/base-page/vectors/results/displays/Color RAM/ROM backup
and other live owners. Neither is a complete machine high-water or permission
to use those excluded resources.

**Feasibility: arithmetic has a conditional 1836-byte allowance; complete
banked fit and service remain UNPROVEN. Implementation is NOT ADMITTED.**
There is no measured banked recovery, complete predicted overhead or executable
source identity on main to justify admitting the conditional prototype.
RF-D1–RF-D3 and RF-EX1 are approved development design only. Actual placement,
linked fit, stack, gateway and service evidence remain UNPROVEN. These gates
remain prerequisites; this publication starts no implementation or optimization.

## Implications for future 65Aero engine work

This direction is a private M2 development profile, not a permanent engine
bank allocator. Any later production adoption needs its own reviewed authority
and complete generated physical/CPU/lifetime ledger.

- Graphics keeps ownership of all relocated code, resident wrappers/constants,
  geometry/cache and remaining workspace. Banked bytes remain charged; relocation
  does not waive the shared code/service accounting or establish a new production
  code ceiling. Every later Graphics/FULL profile must prove the actual remaining
  24 KiB workspace or explicitly replace this provisional strategy.
- Platform/CoreRuntime remains sole MAP/base-page/CPU-port/interrupt owner.
  A private bank gateway is not a new public engine ABI, ResourceManager API,
  general overlay scheduler or permission for other owners to call banked code.
- ResourceManager retains the whole resource band. Boot staging excludes
  simultaneous audio, decode and DMA leases; after successful release, normal
  resource services may reuse it. No future runtime service may rely on stale
  staging bytes or keep an undeclared lease.
- The resident gateway, startup, loader, fault/restoration code, vectors,
  descriptor, state, scratch and stacks must fit their actual owner allocations.
  No hidden cold/hot duplication, future-owner subsidy or reserve use is allowed.
- CoreRuntime continues exact 100 Hz / 21-stage order and deterministic replay.
  Bank transitions enter the actual service ledger for all eight renderer slots.
  Geometry remains prepared once per generation with cancellation and complete
  publication; banking creates no alternate simulation or presentation clock.
- Future M3 aircraft data and M4 flight code are separate increments. They inherit
  no claim of spare code/state/workspace or service time from this estimate.
  Their combined memory, stacks, immutable-table lifetimes and active runtime
  services need fresh admission before enablement.
- ROM/storage transitions, resets and any future dynamic resource lifecycle must
  quiesce bank use and establish their own canonical state/ownership contract.
  This profile authorizes no ROM return, hot reload, general DMA or runtime bank
  replacement. Reset-only recovery is not a returning production service.

## Stack, service, ABI and next step

The historical unbanked diagnostic reports hardware stack 50/256 including
IRQ/NMI, software 127/4096, separate trap 3 and static scratch 77. These remain
reported historical bounds only. New gateway frames, saved P/registers, helper
closure, boot failures, IRQ/NMI and terminal paths require whole-program proof;
no average, guessed increment or inherited PASS admits a banked build.

All eight exact linked dispatch slots, begin/service/commit, guard/clock,
calls/returns, signature reads, restoration, pending IRQ and NMI must be
bounded again. The published unbanked quiet-plus-largest-slot value is 9794
against clock period >9892 in its pinned Xemu profile. Those values provide no
automatic bank-call timing allowance. Unknown/zero budgets refuse dispatch;
no skipped/merged ticks or change to 100 Hz / 21-stage order is allowed.

The founder authorizes committing/pushing this approved design checkpoint,
opening a focused PR and merging only after required CI passes, the PR matches
the approved scope and no review findings remain. Verify integrated main and
leave WIP at NONE before starting the next engineering branch. Source baseline
and banking implementation remain separate reviewable increments.

The next separate engineering increment establishes a source-complete,
reproducible minimum renderer from integrated Git code, retaining approved
nine-segment behavior, precision and a new source identity. It may retain a
failing resident-fit gate as evidence, but must not be enabled or described as
an admitted runtime build. Missing former source is not represented as recovered.
Review, publish, merge and verify that source checkpoint separately. The old
37-member packet is not a prerequisite for either increment.

Only after the source baseline and reviewed banking contracts are integrated,
the approved development exception is represented in its generated profile
and a complete budget is defensible,
may one separately authorized banked-renderer prototype begin. It must prove
complete linked-image fit, actual execution/return, per-invocation signature
checks, canonical MAP/B/stack restoration, zero reserve, bounded transition and
graphics cost, unchanged 100 Hz simulation and deterministic replay. A failed
memory or service gate stops that prototype; recommend a compatible alternative
without implementing it automatically. None of this starts in the design task.

If banking is declined or cannot meet the complete budget, the bounded
configuration alternative to evaluate is a simpler immutable-glyph numeric HUD
in place of custom pixel-font composition, preserving all required telemetry,
camera, nine segments and complete-generation coherence. This requires a fresh
display/resource decision and measurement; no 2175-byte saving is asserted,
and it is not implemented here. Do not reduce precision, omit required scene
content, freeze the camera or borrow another owner's memory as a fallback.

Before direct-PRG Xemu: integrate the reviewed source/contracts, link the entire
mutable-camera executable, prove resident ≤24575, bank ≤8192, no owner overlap
or reserve use, early startup, complete stacks, physical mapping/signature
fault cases and all service bounds. Then obtain exact executable execution
authorization and run PAL/NTSC visuals/camera/tick/fault checks. No old diagnostic
PASS authorizes a new banked image or full M2/Graphics acceptance.

## Validation and handoff

Run the local read-only calculation check from this checkout:

```text
python3 -B docs/evidence/flight-demo/2026-10-27-m2-residency-feasibility/validate.py
git diff --check
```

The check verifies pinned Git inputs, manifest bytes, reference arithmetic,
approved development ownership/exclusion rules, honest unknown costs and
fail-closed budget preconditions. A successful schema check establishes no
actual allocation, executable fit or runtime admission.
It is **design/static verification only**. Signature negative cases (missing,
incorrect, unreadable and changed between successive calls) are mandatory
future implementation tests; none is represented as an executed bank call.
[Retained reviewed-finalization result](../evidence/flight-demo/2026-10-27-m2-residency-feasibility/finalization-validation.json)
records revision 2 checks and source-preservation identities without regrading.
The [publication record](../evidence/flight-demo/2026-10-27-m2-residency-feasibility/publication.json)
records current approval and applicable static checks. The
[reviewed revision archive](../evidence/flight-demo/2026-10-27-m2-residency-feasibility/reviewed-revision-2.tar.gz)
preserves the four files whose approval/navigation status changed. The
[prior validation result](../evidence/flight-demo/2026-10-27-m2-residency-feasibility/validation.json)
is retained unchanged. The
[pre-finalization archive](../evidence/flight-demo/2026-10-27-m2-residency-feasibility/checkpoint-before-conditional.tar.gz)
contains all five exact prior checkpoint files; validation reads it in memory,
without extraction or execution. The 15 unresolved historical members and their
original sealed SHA-256 identities are recorded in accounting.json; the 22-member
historical verification is retained without claiming a newly recovered packet.

Publication changes this existing contract/handoff, accounting/checker,
approval record, reviewed archive and current-state/WIP navigation. All earlier
validation records and archives stay byte-identical. No new architecture paper
is created.
Current authority, public ABI, active generators/ledgers and engine source
are unchanged. Generated target-artifact status: **not generated**.
Registers/clobbers, CPU-visible/physical allocation, live MAP/B, DMA, clock/
deadlines and IRQ/NMI: **no runtime changes** in this checkpoint; proposed
impacts are specified above and await adoption/proof.

This publication runs documentation/static/schema/preservation/Git checks only.
No target compile/relink, host geometry rerun, Xemu, D81, SD or physical test
is authorized. Prior accepted results remain unchanged; updated approval
metadata receives its own static checks. No renderer or banking source is
part of this design publication. Actual linked fit, stack, gateway and service
performance remain UNPROVEN.

## RF-EX2 — current-source design and budget investigation

29 October 2026. **Design investigation authorized; RF-EX2 exception and
implementation remain pending founder acceptance.** This section is the current
16 KiB proposal; it does not alter production authority, RF-EX1's historical
approval, old accounting/checkers or any generated interface/allocation.

Main remains `b20f91cb8023ea02e33d5fec6870026023bd8fbf`; fresh fetch/ls-remote
agree. The integrated source-complete profile is `65AERO-M2-MIN-REBUILD-1`.
The retained corrected target PRG SHA-256 is
`1873c76d7b13f438244d5c3f99d8c80bc951af47cda9fc5ba9a6fadbeb4eda51`.
Its application inputs match current Git source. No target tool or relink ran.

### Decision packet

| Founder question | Current answer |
| --- | --- |
| Does the arrangement comply with every other current contract? | **No, as written.** CPU window geometry is permitted by Main §5.2, but code/workspace partition, current role/helper permissions, landing and staging require explicit amendments. The staging proposal overlaps a retained Audio reservation. No other-owner borrowing is granted by this investigation. |
| Does the legal closure plausibly recover the deficit plus protection costs? | **Not established.** Optimistic current role removal is 8,625 bytes. Distinct new data gives a 2-byte deficit before all new code. Proposed reuse gives only a 253-byte allowance for every remaining incremental resident cost, whose upper bound is unknown. No conservative fit PASS. |
| Does the current renderer fit the remaining Graphics arena? | **Yes for the unchanged current renderer's physical-arena use: 0 / 16,384 bytes.** Its 676-byte renderer object, other resident data, 190-byte compiler scratch and dynamic stacks are separately charged. This is not whole-program fit or proof of future continuation/stack requirements. |
| Are boot, gateway and stack ownership coherent? | **Conditionally in the proposed design; not admitted.** Typed classes, an exclusive existing-buffer lease, safe new linked placement, hardware quiescence and staging conflict disposition are mandatory. Whole-program stacks and IRQ/NMI races remain UNPROVEN. |
| What remains unproven until implementation? | Actual new code/data/alignment/scratch and duplication, linked VMA/LMA/entries, all stack/failure paths, actual mapping/signature reads, gateway return/restoration and all eight service bounds. Execution and visuals need later separate authorization. |
| What exact implementation should follow? | **None for this candidate. Recommend REJECT OPTION A.** Current authority does not grant staging exclusivity, and all mandatory overhead cannot be bounded inside the 253-byte conditional allowance. Terminate this banking candidate after founder disposition; do not start the previously suggested cost probe, another bank design or micro-optimization round automatically. |

### Exact placement, mapping and permissions

All ranges are half-open; inclusive founder ranges end one byte earlier.

| Allocation | Proposed range | Owner and lifetime |
| --- | --- | --- |
| Run code bank | physical [$048000,$04C000), 16,384 bytes | Graphics; Platform sole loader/mapper; reserved from load through reset, immutable after READY, quarantined on failure |
| CPU alias | [$8000,$C000) | Protected Platform scope only; an alias, not another physical allocation |
| Remaining Graphics arena | [$04C000,$050000), 16,384 bytes | Graphics; no bank or staging alias, no claim for FULL profile capacity |
| Payload landing | bank-0 [$008000,$00C000) | Reset-load lease begins before C; full zero/readback retirement before READY/first tick |
| Proposed whole-image staging | [$050000,$054000) | ResourceManager logical owner, Platform executor; exclusive boot lease only; **conflicting audio reservation prevents unconditional approval** |
| Hardware / base page / software stacks | [$0100,$0200) / [$0200,$0300) / [$C000,$D000) | Unchanged; CPU alias stops at $C000 and may never include it |

The derived MAP setting uses blocks 4 and 5, upper offset $040000:
MAPLO=$0000, MAPH=$3400, ordinary MAP register inputs A/X/Y/Z=$00/$00/$00/$34.
Physical addresses equal CPU+$040000 with both megabyte selectors zero:
$8000→$048000, $9FFF→$049FFF, $A000→$04A000, $BFFF→$04BFFF.
Blocks 6/7 are not selected: software stack and I/O/vectors remain outside the
window. Restore both megabyte selectors and MAP masks/offsets to zero and EOM
before canonical public exit. The selector-token operation and normal MAP must
remain distinct; this is a design derivation, not assembled/executed proof.

The pinned official [MAP encoding reference](https://github.com/MEGA65/mega65-user-guide/blob/4a259350c29206b52b278c1e0312ca1e2afc6918/memory.tex)
explains the two masks/offsets and X/A/Z/Y input ordering. Its
[banking-priority appendix](https://github.com/MEGA65/mega65-user-guide/blob/4a259350c29206b52b278c1e0312ca1e2afc6918/appendix-memorymap.tex)
states MAP overrides the ROM banking mechanisms for selected blocks. Older
manual/wiki text differs on priority; qualification must bind the actual core
and check spatial mapping, not assume old prose proves the selected physical
bank. Canonical $D030=$44 and CPU-port DDR/data=$2F/$35 remain unchanged on exit.
ROM/I/O settings outside the selected blocks still matter. No hardware readback
of arbitrary current MAP state is assumed.

The current image cannot be overlaid with this payload. Its resident union
[$2001,$A048) overlaps landing by **8,264 bytes**; current main, buffers, tables,
BSS and compiler scratch include addresses above $8000. A later complete link
must place every resident object/helper/vector/loader below $8000, preserve
stack/result bands and place payload LMA separately. BSS/data initialization
must not touch landing. Maximum payload load span [$2001,$C000) is 40,959
bytes; file maximum is 40,961 including the two-byte load address and all holes.
No existing target is modified or enabled by this layout proposal.

Current `cfcopy`/`r0fc_range` admits the old proof staging class only; the
Graphics display writer admits display classes only. Neither gains new rights.
RF-EX2 needs a private generated fixed-class boot facade for landing, staging,
run bank and resident readback, checked full spans and 1–255-byte transfers.
No raw arbitrary pointer, general bank API, caller-written MAP or DMA is allowed.
Actual caller/buffer addresses are validated before a mapping change.

### Architecture conflicts and exclusions

Proposed RF-EX2 wording for founder review:

> For this separately admitted M2 development profile only, permit immutable
> Graphics transform/project code in physical [$048000,$04C000), scoped by the
> protected Platform gateway at CPU [$8000,$C000). Retain [$04C000,$050000) as
> Graphics workspace. Permit reset-load landing [$008000,$00C000). A proposed
> exclusive ResourceManager staging lease [$050000,$054000) is conditional on
> explicit disposition of the retained audio-cache overlap and verified absence
> of all conflicting activity. No exception is effective before that disposition.
> Keep all other owners, public ABI, resident/stack limits, FULL profile, reserve,
> 100 Hz clock and 21-stage order unchanged. No permanent allocation or general
> runtime bank/reload service is granted.

This changes Main/Runtime/Graphics workspace-only use for the versioned profile,
RF-EX1's smaller partition, RF-CODE-1 roles/helper list and RF-BOOT-1 whole-image
load/staging bounds. It does not silently replace production ownership.
The proposed staging intersects the retained audio-cache [$053000,$056000)
in [$053000,$054000): **4,096 bytes**. Under the current no-other-owner-borrowing
boundary this is a real design conflict, not a disjointness PASS. Founder may
explicitly approve boot-only exclusivity after a lease/quiescence proof, or
require a separate design using the existing 8 KiB staging in two phases. That
alternative changes RF-BOOT's whole-image protocol and is not adopted here.

All simulation [$010000,$018000), audio state [$018000,$01C000), display-control/
shared scratch [$01C000,$020000), display stores [$020000,$040000), assets
[$040000,$048000), Color RAM, result [$1900,$2000), base page/stacks/vectors and
ROM backup [$08000000,$08020000) stay excluded. [$054000,$058000), including
remaining audio cache, DMA lists [$056000,$057000) and proof-reserved
[$057000,$058000), stays excluded from staging. Protected reserve
[$058000,$060000) has **zero consumption**.

Actual boot sequence is startup normalization → C initialization → disabled
launch guard → m1_platform_begin (cfentry, cfrom_begin, cfclock_begin and clock
calibration) → display initialization → renderer/core initialization → release
loop. cfclock_begin enables a resident IRQ. A later loader scheduled after
successful m1_platform_begin must account for it or quiesce/restart it explicitly.
There are no baseline calls starting audio or DMA, but inherited hardware
quiescence is not established by that absence. Require audio/DMA inactivity and
all conflicting leases denied before granting staging. All boot validation,
copy/CRC, landing retirement, canonical restore and release precede first tick.

At maximum N=16,384, the four existing copy/readback passes require 260 chunks,
65,536 copied bytes and 32,768 CRC-processed bytes; landing retirement separately
writes and reads all 16,384 landing bytes. No DMA, retry, fallback repair or
runtime reload. Failure leaves READY false, leases/bank quarantined, canonical
lockout or protected resident terminal sink, with reset as recovery boundary.

### Current relocation closure and resident costs

The retained disassembly's direct JSR/JMP graph rooted at m2_transform and
m2_project_prepared contains 18 unique code symbols totaling **9,736 bytes**.
Every cross-symbol direct edge resolves to an exact symbol boundary; no indirect
JSR/JMP occurs in that closure. This does not prove whole-program control flow,
stack bounds or new relocation correctness.

| Potential relocated role body/private helper | Current linked bytes |
| --- | ---: |
| m2_transform | 936 |
| sine | 232 |
| multiply_rotation | 3 |
| m2_multiply_q46 | 1,054 |
| m2_project_prepared | 1,900 |
| to_camera | 651 |
| plane_distance | 946 |
| interpolate_delta | 1,257 |
| project_axis | 536 |
| rounded_ratio | 255 |
| __udivdi3 | 855 |
| Optimistic unique removal B | **8,625** |

These bodies currently implement monolithic transform/segment work. Public
signatures must keep resident wrappers; new private resumable roles are not
already implemented. Allowing current helpers/callees requires explicit RF-CODE
review: the old helper allowlist omits __udivdi3, memcpy, m2_camera_valid and
Environment's m2_point_valid. Owner boundaries remain: Environment code stays
resident and the gateway does not grant Environment a new bank role.

| Closure code retained resident | Bytes | Reason |
| --- | ---: | --- |
| m2_camera_valid | 531 | Resident begin and camera-input callers |
| m2_point_valid | 119 | Environment ownership |
| __modhi3 / __umodhi3 | 110 / 166 | Shared resident camera-input path |
| __mulsi3 | 121 | Resident camera and fixture users |
| memcpy / __memset | 36 / 28 | Core, snapshots, Platform, startup, fixture and renderer callers |
| Retained closure total | **1,111** | No duplicate removal credit |

__udivdi3 has only rounded_ratio as linked caller and is a candidate for a
private bank copy with the original removed; loss of that condition forces
resident retention or explicitly charged duplication. __muldi3 (296 bytes) is
outside the role closure and stays with resident ground classification (700).
Resident constants include sine table 728, transform products 56, glyph rows
287 and glyph characters 42 bytes. Resident adapters include m2_prepare 26,
prepare 227, project 174, begin 233 and dispatch 244. None is free relocation.

Dependency paths are transform→camera validation/sine/multiply/memcpy;
sine→mod→unsigned mod; multiply→Q46→memset/mulsi; projection→Environment point
validation/memcpy/to_camera/plane distance/interpolation/project axis;
to_camera→multiply; axis→rounded_ratio→udivdi3. The machine-readable receipt
retains edges and caller classification. Relocation must fix all code/table
references at actual linked addresses; copied old bytes are not an executable
bank image. Existing compiler scratch remains resident and must be safe under
non-reentrancy and handler rules.

### Workspace and proposed existing-buffer lifetime

The current renderer never allocates or accesses the physical Graphics arena:
**actual unchanged arena demand is 0 / 16,384 bytes**. No success, cancellation,
held-snapshot or fault path releases or aliases resident storage into that band.
The 676-byte persistent renderer allocation is prepared context95 + cached
lines144 + two bundles254 + snapshot13 + raster cursor16 + counters28 + indexes4
+ visibility9 + tile64 + text40 + flags9. Both publication bundles coexist.
This remains resident for the entire run, including failure. Platform buffer64,
block255, cfworkspace255, mailbox9 and state are already charged in 1,475 BSS
bytes. Static compiler scratch190 is separate. Geometry locals belong to
compiler-assigned stack/scratch, not an uncharged arena; whole-program dynamic
stack use remains UNPROVEN. No assertion is made about FULL renderer demand or
new continuation/save-state allocations.

The historical additional-data estimate was descriptor64 + readback255 +
controls44 =363. It is not necessarily 363 incremental bytes for this baseline.
A proposed explicit Platform lease can reuse existing cfworkspace255 as readback
strictly after successful m1_platform_begin and before first tick. Its only
users in this linked composition are ROM verification/restoration; normal render and IRQ/NMI paths
do not use it, and cfrom_restore is not linked. ROM CRC/validity is retained
elsewhere. Loader entry is denied on failed Platform init or pending ROM work.
No returning ROM/storage/reload path is permitted; loader failure is terminal
until reset, so it cannot reenter ROM verification with a leased buffer. Normal
operation never reads this buffer as bank authority. This is same-owner reuse,
not another owner's scratch, and is not a 255-byte subtraction from baseline
resident usage. A new link must relocate this buffer from its old $9ACF address
to below $8000. Runtime immutable expected descriptor/signature state may not
alias the boot readback buffer. The 44 control bytes are an allowance, not a
proven adequate gateway-save/continuation layout; extras must be charged.

### Conservative budget and failed admission

Baseline resident is **32,839**, ceiling **24,575**, deficit **8,264**, reserve0.
8 KiB minus signature16 provides at most8,176 body bytes: deficit88 before any
new resident cost. The historical 4,374/2,199/363/1,836 figures remain historical.

| Current-source design scenario | Resident before unpriced R | Margin |
| --- | ---: | ---: |
| Maximum current role removal B=8,625 | 24,214 | +361 for ALL new costs |
| Distinct descriptor64 + new readback255 + controls44 | 24,577 | **-2** |
| Proposed existing-readback lease; descriptor64 + controls44 incremental | 24,322 | **+253 before every other resident cost** |

Bank minimum is 8,625+signature16=8,641, leaving7,743 bank bytes before alignment,
entry thunks, duplicated helpers or changed code generation. Spare bank bytes
cannot pay for resident gateway/loader code under the current role restriction.
R includes every byte of entry/precondition/signature verification; typed
wrappers and result preservation; context save, canonical restore and nested
lockout; loader range/lease checks, CRC/readback/retirement and boot quiescence;
normal/fault/terminal handling; new continuations, descriptor/control excess;
alignment/veneer/constants, compiler scratch and changed code generation.
All R components have **unknown upper bounds**, not zero. Code already retained
(cfcopy463, cfphysical_crc445, crc_byte84, r0f_pf_flat_copy, range checks) may
provide mechanisms but not free new permissions or validated new range logic.
New facade/glue costs remain R. Stack increments and every service cost are
also unknown, separately constrained inside unchanged stack/deadline envelopes.

Thus a conservative complete banked budget cannot be closed. Distinct-buffer
scenario FAILS by at least2+R. Reuse scenario requires R<=253 with all terms
bounded and all contracts accepted; that is **UNPROVEN**, not plausible fit
established from symbol sums. No code-size/cycle upper bounds are fabricated.
No banked prototype or execution is admitted. R cannot be bounded from the
retained unbanked link, so no conservative final numeric allowance exists after
all mandatory costs. The 253-byte figure is only the pre-overhead ceiling.
The current recommendation is REJECT OPTION A, not a cost-probe authorization.

### Protected gateway and acceptance requirements

RF-MAP-1 safety remains mandatory for every invocation: after selection and
before transferring to bank code, 16 volatile signature reads against the
resident expected identity and a compiler barrier. Prior success never grants
a later call. Missing/wrong/changed/unreadable or unprovable mapping suppresses
the body, restores canonical state, marks sticky fault and locks out until reset.
If restore is uncertain, stay in the resident terminal sink; do not unmask IRQs,
call a public service or return through an uncertain context. Signature checking
is identity only, not CRC integrity, physical-location proof or hardware write
protection. No writer may change the image/descriptor between check and entry.

Platform alone owns MAP, B, CPU port, both stacks, saved P, busy token and the
gateway. Preserve X/Y/Z/B, both stack pointers and logical compiler $02–$21
pseudo-registers around enter/leave; A is the status/result clobber and overlaps Q.
Preserve body result before leave clobbers A; numeric failure cannot become DONE.
No independent Q preservation is promised. Restore zero MAP/megabyte selectors,
EOM, B=$02, Z=0, E=1, CPU-port $2F/$35, admitted ROM/I/O and resident vectors
before public return/yield/clock and restore original P at the safe boundary.
One call owns one body quantum. Reentry before mapping cannot clear an outer
token; nested entry while mapped goes to resident terminal lockout, never into
unmapped caller code. IRQ masking spans selection, signature/body and restoration.
Resident NMI does no C/MAP/DMA/bank work, preserves interrupted mapping and makes
interference sticky. All NMI races and pending IRQs must enter the eventual
whole-program proof. Finite monolithic loops are not service admission.

Charge all eight slot bounds, guard/clock overhead, calls/returns, per-call
verification, helper/body work, restore, pending IRQ/NMI and return margin.
No guessed cycle number, merged/skipped tick or altered 100 Hz/21-stage order.
Keep launch and grants zero until actual stack/service safety is established.
Generated descriptor64/signature16 formats are not reconstructed from missing
historical files: exact current offsets, typed entry boundaries and controls
remain a required versioned design deliverable before a prototype link.

### Validation, scope and handoff

Run the new design checker (arithmetic/ownership/lifetimes/graph/schema only):

```text
python3 -B docs/evidence/flight-demo/2026-10-29-m2-rf-ex2-design/validate.py
git diff --check
```

[Accounting and decision receipt](../evidence/flight-demo/2026-10-29-m2-rf-ex2-design/accounting.json)
records actual-source closure, explicit unknown costs, ownership conflict,
conditional lease, reference identities and pending decisions. The checker
rejects unknown-cost admission, stale signature authorization, unsafe lifetime
reuse, owner overlap, incorrect mapping/window/stack boundaries and stale
arithmetic; synthetic cases are design model checks, never executed bank calls.
Earlier planning receipts and every historical packet remain unchanged.
The prior three design/navigation files are archived before modification.

Source, public/generated contracts, active ledgers and target artifacts remain
unchanged. Actual register/clobber, memory, MAP/B, DMA, timing and IRQ/NMI effects
are **none in this design task**. Proposed effects above require reviewed adoption
and actual implementation evidence. No host geometry/renderer tests, target
compile/link, Xemu, D81, SD, physical test or publication is performed. Historical
recovery stays22 previously verified/15 unresolved; eight old Git-worktree tiers
remain NOT VERIFIED. No metadata or files are reconstructed.

Status: **READY FOR REVIEW — recommend REJECT OPTION A**. RF-EX2 is
**BLOCKED BY MEMORY OWNERSHIP**, with resident/stack/service admission UNPROVEN.
No implementation follows automatically. Founder acceptance and separate
publication authorization remain required before commit/push/PR/CI/merge.
Historical failed and successful evidence remains unchanged.


### P2 corrections and mandatory final disposition

The CRC symbol is `$77F1`, size **$54 = 84 bytes**, in both the exact retained
map and symbols. Its direct caller is `cfphysical_crc` (445 bytes), whose caller
is resident `cfrom_begin` (546 bytes), reached from `m1_platform_begin`.
Its source is the pinned `combined_platform.c` CRC-32/ISO-HDLC byte loop.
`crc_byte` is not in the transform/project closure. It must remain resident for
boot ROM-backup verification; moving a duplicate into a bank removes **zero**
resident CRC bytes and adds 84 bank bytes plus any new calling glue. Bank-loader
CRC work may reuse the resident mechanism only through an explicitly legal
facade; no new permissions or cost-free glue follow. The correction is +26
bytes to the descriptive helper inventory, **not** +26 to resident usage: all
84 were already charged in 32,839. Removal8,625, gross allowance361,
separate-data deficit2 and reuse allowance253 are therefore unchanged after
independent graph/map/symbol recomputation. No standalone compilation was used.

Staging `[$050000,$054000)` is proposed ResourceManager boot storage. The
registry separately prohibits `[$053000,$056000)` as Audio cache, overlapping
`[$053000,$054000)` by **4,096 bytes**. Audio's reservation has no current
load-time/boot retirement boundary granting these bytes to this loader. Current
RF-EX1 only proposes staging through `$052000` and does not amend that Audio
reservation. The absence of linked audio-start/DMA calls proves neither lease
authority nor inherited hardware quiescence. There is no operational lease
manager/witness in this candidate establishing exclusive use before Audio
ownership begins. Therefore staging exclusivity is **NOT PROVEN UNDER CURRENT
AUTHORITY**, and RF-EX2 is **BLOCKED BY MEMORY OWNERSHIP**. No Audio owner is
moved, borrowed or silently rescheduled; no new exception or alternate staging
protocol is adopted in this correction.

Final mandatory-cost ledger: the baseline already includes compiler scratch190,
CRC84 and the existing readback buffer255. Descriptor64 + logical-control44
is a conditional108 increment only if the proposed same-owner boot lease is
accepted and valid; actual save/continuation layout can require more. New
signature checks on every invocation, typed gateway/wrappers, mapping and
canonical restore, loader/CRC/range/retirement glue, normal/fault/terminal paths,
context/continuation data, alignment/duplication and compiler scratch changes
all lack proven size upper bounds. Added hardware/software stack and per-call
service/IRQ/NMI bounds are also unknown. The full residual is **253 - R bytes**
under the optimistic reuse scenario, with R unknown; it is not253 available
bytes after protection. No cost is assigned zero to close that equation.

**Recommendation: REJECT OPTION A for the current baseline and contracts.**
The correction does not mathematically prove every possible banking design
impossible. It establishes that this candidate has an unresolved owner conflict
and no credible bounded complete fit/service case. Terminate it rather than
start implementation or another micro-optimization sequence. No larger bank,
new owner allocation or next experiment is proposed automatically.

The completed [validation receipt](../evidence/flight-demo/2026-10-29-m2-rf-ex2-design/validation.json)
records actual command argv/cwd, exits, outputs and SHA-256 identities. New
[accounting](../evidence/flight-demo/2026-10-29-m2-rf-ex2-design/accounting.json)
and the read-only checker establish documentation/design consistency only.
They do not mark failed feasibility gates PASS. The packet preserves the exact
16,060-file reviewed inventory, archives all three authorized edited preimages,
and compares the other16,057 files unchanged, including every old evidence file.
The original480 unrelated path bytes, status and diff are independently checked.
The final seal covers the new packet; the older pre-design archive is untouched.
No target tools, renderer tests, relink, Xemu, media/hardware or publication ran.
