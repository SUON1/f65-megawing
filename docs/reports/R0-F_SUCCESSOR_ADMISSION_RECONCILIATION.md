# R0-F successor admission and current-authority reconciliation

Date: 2026-09-20
Status: **READY FOR HUMAN REVIEW - IMPLEMENTATION NOT STARTED**

## Purpose and boundary

This packet re-baselines the remaining R0-F closure work against the
reorganized repository. It does not reopen R0-A/B/C/D, revoke bounded R0-E or
R0-F evidence, freeze a measured value, approve Runtime v1 as final, authorize
Phase 1, or implement/package/run a successor carrier.

The closure judgment is:

> Full R0-F remains open. A successor combined proof must join CF001's active
> combined workload to RH001's same-run returning KERNAL/storage lifecycle,
> close the missing current-parent measurement coverage, and carry one exact
> identified configuration through Xemu, physical MEGA65 evidence, and named
> owner acceptance. The predecessor evidence remains valid only for its stated
> bounded scope and is not to be repeated merely because the repository moved.

## 1. Current authority

The current design order is the exact order in
`spec/manifests/spec-corpus.json`:

1. Main Concept v1.6 - active master product/architecture authority.
2. Gameplay and Simulation Supplement v1 - active player-facing authority.
3. 65Aero Engine Runtime and Technical Supplement v1 - current approved
   candidate implementation architecture, **not final**.
4. Physics v3.3.
5. Graphics v2.1.
6. Audio v1.0.
7. Radar / Sensors / Track v1.0.
8. AI Behavior and Decision Architecture v1.0.

Main v1.6 §§4.1-4.6, 5, 15 and 17; Gameplay v1 §§9.7, 21.2-21.7 and 22.7;
Runtime v1 §§19.1-19.4 and its R0-gated register; and the subsystem papers'
explicit R0/Phase-1 sections govern this reconciliation. Physics v3.3's actual
coefficient model, Radar/Sensors/Tracks Phase-3 tables, and AI Phase-4 tuning
remain later-phase work; they contribute fixture shapes, ownership and
measurement hooks only where the R0 proof consumes them.

AD-001, the R0 development approval, RH001 owner decision, generated/private
contracts, ledgers, handoffs and evidence records control the exact scope and
identity of historical proof claims. Older Read-First, Architecture 1.5.1,
Gameplay 0.2 and Engine 0.2 material is provenance only unless an immutable
artifact identifies it as the historical source of a retained obligation.

## 2. Retained evidence

| Milestone / evidence | Current disposition | Exact boundary retained |
|---|---|---|
| R0-A | Retain closed bounded platform/toolchain/MemoryAccessABI evidence. | No claim that later private proof wrappers are production ABI. |
| R0-B | Retain bounded graphics/display/cockpit/palette/swap/input-edge and representative audio evidence. | No retrofit for Graphics v2.1 or Audio v1.0 additions; no successor combined-load latency claim. |
| R0-C | Retain the bounded package/resource/residency/storage proof and recorded owner disposition. | Current program disposition is R0-C COMPLETE under Main v1.6. Historical evidence remains truthful and retains the recorded owner waiver; no historical record is retroactively relabeled as a formal PASS. Remaining returning `StorageService` implementation is carried forward and does not reopen Charlie. |
| R0-D | Retain the accepted calibration-proof scope and historical 530,000-clock protected-workload baseline. | It is not a complete current-parent renderer/audio/input/timing limit. |
| R0-E | Retain the bounded functional-proxy and raster-observation scope, including its accepted carrier route. | It is not the current-parent combined measurement gate and has no DMA/IRQ or external latency promotion. |
| CF001 / `F65BLK02.D81` | Retain exact carrier, SD integrity/one extent/eject, Xemu and physical result/raw reductions, ROM restoration, four real key edges, owner-reported audio, 2,640 samples and 80 windows. | Reset-only; synthetic fixture; nominal counter-ratio rather than traceable SI time; no external input/audio latency, full parent phase/window coverage, returning storage lifecycle, measured limits or R0-F acceptance. |
| RH001 | Retain 16,842,752 host cases and clean NTSC/PAL Xemu LOAD/SAVE/reload continuation from tick 33 to 34 with ROM, KERNAL/DOS context, application stack/base-page and state restoration. | Standalone, not co-resident with CF001, not physical, no active display/audio/IRQ/DMA resumption, no production storage ABI and no R0-F acceptance. |

The exact retained CF001 identity is `F65BLK02.D81`, SHA-256
`b13853a7ddaf3bf26dfcaceb7e4466ab2d58702b96bfcbe9ae62c7db56ed3d82`.
The RH001 PRG identity remains
`b856ad29b0ac06939083dd54140136d438037ce41c3f49f00163d6b2c52efcc9`.
These identities are predecessor evidence inputs, not the future successor
carrier identity.

## 3. Remaining requirement-to-evidence matrix

`X` and `HW` mean successor Xemu and physical-MEGA65 evidence. `Human` means
explicit owner acceptance of that row is required for full R0-F acceptance.

| Requirement | Classification | Current source; historical origin | Existing evidence | Exact non-claim / successor requirement | X | HW | Human |
|---|---|---|---|---|:---:|:---:|:---:|
| Platform/toolchain and canonical MemoryAccessABI baseline | `SATISFIED — RETAIN EVIDENCE` | Main §§2.2, 5.2-5.3, 17.2; R0-A | R0-A handoff/contracts | Do not reopen; successor must use, not redefine, the ABI. | No | No | No |
| R0-B display/input/audio candidates | `SATISFIED FOR BOUNDED PREDECESSOR SCOPE` | Main §17.3; Graphics §16.1; Audio §19 | R0-B handoff/evidence | Retain only what R0-B tested; current combined behavior is covered below. | No | No | No |
| R0-C current-program disposition | `SATISFIED — RETAIN EVIDENCE` | Main §§5.6, 17.4; `CURRENT_STATE.md`; historical R0-C records | R0-C is COMPLETE for the Revision 1.6 program baseline; bounded evidence retains the recorded owner waiver | No historical record is retroactively relabeled as a formal PASS. Remaining returning `StorageService` implementation is carried forward and does not reopen Charlie. | No | No | No |
| R0-D calibration baseline | `SATISFIED FOR BOUNDED PREDECESSOR SCOPE` | Main §17.5; Runtime §19.1 | R0-D handoff/evidence | Preserve 530,000-clock reference; do not call it a current full workload limit. | No | No | No |
| R0-E combined proxy | `SATISFIED FOR BOUNDED PREDECESSOR SCOPE` | Main §17.6; Runtime §19.2; AD-001 | R0-E handoff/evidence | Functional proxy only; not the required successor E-to-F chain. | No | No | No |
| CF001 bounded combined physical experiment | `SATISFIED FOR BOUNDED PREDECESSOR SCOPE` | Runtime §§19.2-19.3; historical full-closure plan | CF001 exact-D81 Xemu/physical evidence | Retain exact counters and non-claims; no repeat solely for reorganization. | No | No | No |
| RH001 returning lifecycle | `SATISFIED FOR BOUNDED PREDECESSOR SCOPE` | Owner no-restart decision; Main §§5.6, 14.5; RH001 decision | Host plus NTSC/PAL Xemu | Same-run continuation proved only for standalone retained C model. | No | No | No |
| Combined CF001 + RH001 same-run lifecycle | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Runtime §§19.2-19.3; owner RH001 decision | Separate CF001 and RH001 evidence | One run must quiesce, restore ROM/KERNAL/storage, perform checked I/O, restore application state, and resume the active combined workload without reset/reload. | Yes | Yes | Yes |
| Linked/physical memory fit and ownership | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Main §5.1; Runtime §§19.1-19.2; current ledgers | Separate generated accounting | Generated successor ledger/map must prove all lifetimes, overlaps and high-water with zero measured-reserve consumption. | Yes | Yes | Yes |
| MAP, base page, hardware/application stacks, ports, vectors and ROM protection restoration | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Main §§5.2-5.3; PlatformABI/MemoryAccessABI; RH001 decision | CF001 ROM restore; RH001 standalone context restore | Prove canonical B=2/port `$35`/MAP/vector exit, full application continuation and failure lockout in the combined image. | Yes | Yes | Yes |
| Returning storage path | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Main §§5.6, 14.5; Runtime §19.2; owner decision | RH001 checked LOAD/SAVE/reload | Private R0 proof boundary is sufficient; production `StorageService` ABI is not required here. Include deterministic storage failures and no false resume success. | Yes | Yes | Yes |
| Production StorageService/public storage ABI | `PHASE 1 - NOT AN R0-F REQUIREMENT` | Main §§5.6, 18.2; Runtime Phase 1 | None claimed | Do not freeze production API, filenames, campaign-save layout or timing from the private R0 wrapper. | No | No | No |
| IRQ/DMA exclusion during storage and resumed contention afterward | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Main §§3.3, 5.4, 17.6; Runtime §19.2 | CF001 active IRQ/DMA; RH001 quiescent storage | Enter only with application DMA complete/empty and IRQ masked; restore service/vector state, then prove resumed IRQ/DMA activity and bounded contention. | Yes | Yes | Yes |
| PCM/SID protected audio service and contention | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Main §§4.6, 11, 17.5-17.7; Gameplay §21.6; Audio §§19-21 | R0-B bounded audio; CF001 service/preemption and owner-reported sound | Exercise representative P0/P1 versus lower-priority contention, resume logical/hardware service after storage, measure event-to-service and worst protected gaps. Production content/format remains unfrozen. | Yes | Yes | Yes |
| Input edge semantics and latency | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Main §§4.6, 17.5-17.7; Runtime §§19.1-19.3 | R0-B bounded input; CF001 matrix edges/four physical A edges | Use semantic/context edge corpus, press/hold/release and deterministic queue behavior; measure external-to-observed/consumed latency under combined load. No production binding choice. | Yes | Yes | Yes |
| Snapshot publication/consumption, complete-buffer and registration coherence | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Main §§4.2, 4.6, 10.4-10.5, 17.5-17.7; Gameplay §§9.4, 9.7; Graphics §§2.5, 7, 16 | CF001 three synthetic snapshots/complete-buffer swaps | Prove ownership transitions, source tick, drops/supersession, immutable read, atomic world-registration pair and no partial display under lag/storage/resume. | Yes | Yes | Yes |
| Representative renderer/protected-presentation combined load | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Main §§4.6, 10, 17.6; Gameplay §§9.7, 21.2-21.3; Graphics §§12, 14, 16 | R0-B candidates; R0-E/CF001 synthetic work | Use bounded proxy content but represent required nine-aircraft/combined entity pressure, cockpit/HUD, occlusion/registration/LOD, pool pressure and deterministic shedding. No production art or Phase-2/3/4 model is required. | Yes | Yes | Yes |
| Exact 100 Hz release, 21-stage order, phase and rolling-window behavior | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Main §§4.1-4.6, 17.5-17.7; Runtime §§19.1-19.3 | CF001 16 phases/33-tick cohorts, nominal comparison | Prove calibrated release/deadline behavior across legal relative phases and rolling windows without changing order or slipping/merging ticks. | Yes | Yes | Yes |
| Completed-world cadence and displayed-world age | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Main §4.6; Gameplay §§9.7, 21.2-21.3; Graphics §§2.5, 12, 16 | CF001 small-scene cadence/lag | Measure source-snapshot age, complete-frame cadence, view latency and p95/worst under representative load; enforce the existing 20 Hz failure floor. Candidate maximum age remains unfrozen. | Yes | Yes | Yes |
| Calibrated reference, overhead and uncertainty | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Runtime §§19.1-19.3; R0 full-closure plan RC-1 | Raw CIA/count-ratio observations | Identify the clock/reference chain; quantify read/capture instrumentation overhead, resolution, wrap/coherence and physical uncertainty. Nominal 40.5 MHz is not traceable SI calibration. | Yes | Yes | Yes |
| Code/data/static/dynamic stack and reserve high-water | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Main §§5.1, 15.3, 17.8; Runtime §§19.1, 19.4 | Maps/accounting and bounded canaries | Record linked bytes plus worst exercised hardware/software stack, pools/queues/staging/DMA lists; prove `$058000-$05FFFF` unchanged and unused. | Yes | Yes | Yes |
| Deterministic overflow, fault, starvation and shedding | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Main §§4.6, 15.2, 17.6; Runtime §19.2; Graphics §§8, 14, 16; Audio §§17, 20 | R0-E/CF001 bounded injected faults | Cover one-over, queue/pool exhaustion, snapshot starvation, storage error/lockout, optional resource absence and protected-service preservation with observable deterministic disposition. | Yes | Yes | Yes |
| PAL/NTSC successor regression | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Runtime §§19.2-19.3 and §22.7; exact configuration rule | CF001 and RH001 PAL/NTSC Xemu | Run the successor in both Xemu modes; physical evidence may use the explicitly identified supported owner configuration. Do not infer complete production equivalence from one hardware mode. | Yes | One identified mode | Yes |
| Full production PAL/NTSC equivalence | `PHASE 1 - NOT AN R0-F REQUIREMENT` | Runtime §§20.4-20.5, 22.7 | None claimed | Later integrated runtime must preserve authoritative equivalence; R0-F supplies inherited measurements only. | No | No | No |
| Exact D81/carrier and evidence identity | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Main §15.3; Runtime §19.3; development workflow | Predecessor exact carriers | Fresh successor PRG/D81 hashes, inputs, toolchain, ROM/Xemu, maps/symbols/disassembly, construction, SD hash/extent/eject and physical platform/configuration chain. | Yes | Yes | Yes |
| Named owner acceptance | `MUST BE CARRIED INTO SUCCESSOR COMBINED PROOF` | Main §§15.3, 17.7; AD-001 and workflow | Development approval only | Evidence review and explicit full R0-F acceptance; mergeability or passing lower tiers is not acceptance. | No | No | Yes |
| R0-supported numeric/capacity limits | `MEASURED-LIMIT CLOSURE AFTER R0-F` | Main §17.8; Runtime §19.4; Graphics §16.5; Audio §20 | Candidate observations only | Freeze only values supported by accepted evidence; no automatic promotion of every observed maximum. | No | No | Yes |
| Production generated interfaces and complete Phase-1 ledger closure | `PHASE 1 - NOT AN R0-F REQUIREMENT` | Main §18; Runtime §§20.1-20.5 | Proof-only generated contracts | Successor may add private generated proof records/ledger entries only; it must not freeze production layouts. | No | No | No |
| Physics coefficients/FCS tuning, radar tables, AI doctrine and production gameplay/content | `LATER PHASE - NOT AN R0-F REQUIREMENT` | Main §§18-21; Physics v3.3; Radar/Sensors/Tracks v1.0; AI v1.0 | Bounded proxy/interface evidence only | Preserve interface shapes/owners and representative costs; do not invent later-phase data to close R0. | No | No | No |

No row currently requires `CONTRADICTION / HUMAN DECISION REQUIRED`. The
owner's no-restart decision is settled. Main v1.6's placement of production
StorageService closure in Phase 1 is compatible with qualifying a private
same-run storage lifecycle inside R0-F; the successor must not promote that
private wrapper into a public production ABI.

## 4. Successor combined-harness scope

The minimum successor fixture is a single private R0 combined image that:

1. starts from canonical R0 platform state and preserves a pre-C opaque KERNAL
   context before C/base-page initialization;
2. runs an admitted representative combined workload with an exact 100 Hz
   release, the 21 ordered stages, bounded later-phase proxies, immutable
   snapshots, protected cockpit/HUD, complete-buffer rendering, semantic input,
   SID/PCM, IRQ and DMA service;
3. collects calibrated per-stage/protected-service, phase, rolling-window,
   world-age/cadence, latency, pool/queue, stack, memory and reserve evidence;
4. at a declared tick boundary, completes outstanding application DMA, freezes
   publication at a complete snapshot, saves logical service state, masks IRQs,
   stops/quiesces presentation and audio hardware, restores/verifies ROM, and
   enters the RH001 returning KERNAL/storage path;
5. performs checked LOAD/SAVE/reload plus deterministic error/lockout cases;
6. restores application low memory, DOS overlay, base page, hardware stack/SP,
   MAP/MB selectors, port, vectors, timers, IRQ, display and audio state;
7. resumes the same model/checksum/tick lineage and active display/audio/input/
   IRQ/DMA scheduling without startup, reset or application reload; and
8. publishes a versioned result/raw capture independently reducible by host and
   Java oracles.

Synthetic/proxy content remains permitted for Phase-2 physics, Phase-3 sensors/
weapons and Phase-4 AI, but its simultaneous counts, ownership, causality,
memory pressure and protected-service cost must represent the parent R0
acceptance load. Production gameplay, art, coefficient tables and final public
schemas are explicitly outside this harness.

State that must survive the storage transition includes at least: simulation
tick/release phase; deterministic model/RNG/checksum state; command/event and
input-edge state; snapshot ownership/source ticks; world-generation,
registration and renderer cursor/destination state; audio scheduler/priority/
voice/PCM logical state; timer/IRQ/vector configuration and counters; DMA queue
empty/completion state; result accumulators; storage/fault state; stack/base-page
state; and the reserve sentinel.

## 5. CF001/RH001 integration analysis

### Fixed conflict

CF001's linked resident image ends at `$7F71`, leaving 143 bytes below the
enforced `$8000` ceiling. RH001's pre-C opaque `$0000-$15FF` KERNAL snapshot is
5,632 bytes and is currently linked `.noinit`. The linked images therefore
cannot be concatenated.

| Allocation / service | Current conflict | Disposition for successor admission |
|---|---|---|
| `$2001-$7FFF` linked image | Both variants independently occupy the same ceiling; RH001 snapshot alone exceeds CF001 free space. | Keep one linked program and move the opaque pre-C snapshot out of linked resident storage. Reconcile code/BSS/static stack in a generated successor map. |
| `$0300-$1FFF` low memory | CF001 raw capture/hot/result data overlaps KERNAL/application low-memory preservation. | Treat low memory as lifecycle-owned during storage. Move persistent measurement/raw capture to a generated physical/Attic allocation before handoff; restore application bytes before resume. |
| `$050000-$051FFF` resource staging | CF001 DMA staging overlaps RH001's `$050000-$051CFF` low-memory backup. | Reuse only after CF001 application DMA is complete and staging contents are no longer live; record mutually exclusive lifetime in the ledger. |
| `$01D000-$01EFFF` shared transient | RH001 uses it for the application DOS-overlay backup. | Retain exclusive lifecycle use; no renderer/resource scratch may remain live during the storage phase. |
| `$053000-$0530FE` PCM cache | CF001 sample is live outside the storage phase. | Preserve/re-stage immutable sample and logical scheduler state; do not reuse this range for context storage while audio resume is required. |
| `$054000-$055FFF` | RH001 opaque DOS entry context; CF001 does not allocate it. | Admit as lifecycle-only resource-staging ownership for the transition. |
| `$056000-$056010` | CF001 immutable DMA list. | Preserve; no KERNAL snapshot overlap. Application DMA is quiescent before transition. |
| `$020000-$03FFFF` | CF001 reclaimed ROM/display stores. | Restore and verify ROM before KERNAL entry; unavailable as application scratch during the call. |
| `$058000-$05FFFF` | Protected measured-limits reserve. | Read/CRC only. Never use it to solve integration fit. |
| Attic `$08000000-$0801FFFF` | Existing immutable ROM backup. | Preserve unchanged. A new private opaque-context allocation elsewhere in the existing Attic resource tier remains the preferred T02 admission hypothesis, subject to current Attic policy, generated ledger/range validation and an early protected CPU-copy path. T01 selects no exact address. |

### Recommended bounded approach

The preferred T02 admission hypothesis is to capture the 5,632-byte KERNAL
context in an explicitly generated private Attic resource immediately on entry,
before C startup changes low memory. This state is private R0 proof-platform
transition state, not authoritative simulation or gameplay state. No simulation
decision consumes it, and it exists only across the quiesced same-run platform/
storage transition. Access is exclusively through the protected platform /
MemoryAccessABI path; ordinary C receives no arbitrary Attic pointer. The
hypothesis uses no measured-limits reserve.

T02 must prove that this temporary use is compatible with Main/Runtime Attic
ownership, residency and access rules before implementation proceeds. If that
proof requires changing Main v1.6, a public ABI, high-level memory ownership or
Runtime architecture, stop and escalate rather than silently creating an
exception. T01 does not choose an exact Attic address. Exact address, alignment,
guard bytes, integrity fields and copy mechanics remain T02 admission outputs.

The successor may then reuse CF001 resource staging for RH001 low-memory backup
only after application DMA is complete and services are quiescent. RH001's
existing DOS-context and shared-transient allocations remain lifetime-exclusive.
Measurement capture that must survive the transition must be moved out of low
memory through a generated private record rather than silently growing the
linked image.

This approach requires a new private successor contract/header, linker/map
accounting and memory ledger. It does **not** require a change to Main v1.6,
public PlatformABI/MemoryAccessABI semantics, the high-level chip-memory map,
100 Hz timing, 21-stage ordering, CoreRuntime ownership, or reserve policy.

## 6. Evidence plan

| Tier | Required successor evidence | Exit boundary |
|---|---|---|
| Host | Native sanitizer tests and independent oracle for normal/boundary/one-over/corruption; lifecycle state machine; deterministic repeat/checksum; semantic input; snapshots; storage errors/lockout; phase/window reduction; generated-record validation. | Proves software model/contracts only. |
| Target/static | Compile/link; map/symbols/disassembly; startup-before-C snapshot order; branch-encoding and ROM-call allowlists; public/private ABI checks; linked/physical ownership and overlap/lifetime proof; code/data/static/dynamic-stack instrumentation; register/MAP/base-page/vector restore paths. | Proves built-image structure, not execution. |
| Xemu | Fresh direct-PRG development followed by the exact fresh D81; at least two clean boots per admitted mode; NTSC and PAL; full combined workload before/after storage; raw captures and independent reduction; injected deterministic failure cases that do not require destructive media behavior. | Establishes emulator behavior only. |
| Exact D81 / delivery | One-session construction, structure/BAM/directory/chain/allocation and extracted-payload checks; immutable hashes; exact mounted image in Xemu; guarded SD copy with matching pre/post hash, one extent and safe eject. | Establishes carrier identity/delivery, not hardware behavior. |
| Physical MEGA65 | Exact identified D81 and hardware/core/ROM/HYPPO/Freezer/video/storage/input/capture configuration; calibrated phase/window/raw capture; lifecycle continuation; active service resumption; input/audio/DMA/IRQ/snapshot/world-age/memory/stack/reserve evidence; independent reduction. | Establishes only the recorded physical configuration and exercised cases. |
| Human acceptance | Review every matrix row, non-claim, evidence identity and uncertainty; explicit named full R0-F acceptance or row-specific rejection/waiver. | Required before any R0-F pass or measured-limit freeze. |

No D81 is authorized by this reconciliation task. The root D81 gate must be
read and obeyed in the successor task before any D81 operation.

## 7. Measured-limits handoff

After successful owner-accepted R0-F, a separate measured-limits action may
freeze only evidence-supported values: protected-service and per-stage/
combined-workload ceilings; input/warning/audio service latency; renderer tier,
complete-world cadence and displayed-world age; DMA batch/latency; selected
VIC-IV/RRB composition; audio channel/cache/staging limits; code/data/static and
dynamic stack/reserve margins; and measured resource/presentation/work-queue
capacities.

It must not freeze Phase-2 physics coefficients/FCS tuning, Phase-3 radar/IR/
seeker/link data, Phase-4 AI doctrine/cadences, production mission/gameplay
content, campaign-save schemas, a public StorageService ABI, or production
record layouts not actually required and measured by the accepted proof.

## 8. Exact next implementation task

**Task:** R0-F successor memory/lifecycle contract and static admission
**Proposed branch:** `codex/r0f-successor-memory-lifecycle-admission`

Inputs:

- this reviewed reconciliation;
- CF001 and RH001 source/contracts/generated headers/maps/ledgers/accounting;
- current PlatformABI/MemoryAccessABI and high-level memory ownership;
- current generator/build/static-validation tooling.

Outputs:

- one private successor contract and generated header;
- a generated lifetime-aware memory ledger with the early opaque-context
  allocation, persistent capture allocation, every overlap/exclusion, guard and
  reserve rule;
- linker/startup skeleton proving pre-C capture ordering and resident fit;
- host/static tests for copy integrity, lifecycle admission, overlap, restoration
  and failure lockout;
- a handoff identifying exact later workload-integration work.

Completion condition: host and target/static gates prove that the successor
layout and lifecycle can contain both predecessor responsibilities without
public ABI/high-level-memory/tick-order/reserve changes. No D81, Xemu, SD or
physical run belongs to that first implementation task. Any failure to fit
without reserve use or any required public-architecture change is reported as
a contradiction for human decision rather than designed around silently.

## Task impact

This packet changes documentation only. Registers/clobbers, CPU-visible and
physical memory, MAP/base-page, stacks, DMA, timing/deadlines, IRQ/NMI, public
interfaces, generated artifacts, source, D81s and retained evidence are
unchanged.
