# F-65 Technical Alignment and Read-First Supplement

## 1. Document Control

| Field | Value |
|---|---|
| Title | F-65 Technical Alignment and Read-First Supplement |
| Version | 1.0 |
| Status | **APPROVED — FIRST-READ AUTHORITY** |
| Date | 2026-08-20 |
| Authoring role | Senior technical program manager, architecture auditor, and configuration-control editor |
| Intended filename | `F-65_Technical_Alignment_and_Read_First_Supplement_v1.0.md` |
| Approved status | **APPROVED — FIRST-READ AUTHORITY** |
| Approved draft SHA-256 | `2eb72648e7e04644dd09115895020f358e7173994fb42df78209850193956b3f` |
| Approval record | `F-65_Specification_Approval_Record_2026-08-20_R0_Development.md` |
| Approval effect | Active from 2026-08-20 under the recorded scope and exclusions |
| Change model | Orientation, configuration control, disposition, navigation, and escalation; not an alternate architecture |
| Supersedes when approved | `F-65_Technical_Alignment_and_Corrections_Supplement_v0.2.md` as the operating alignment document |

> **READ THIS SUPPLEMENT BEFORE F-65 REVISION 1.5.1, F-65 GAMEPLAY 0.2, F-65 ENGINE 0.2, ARCHITECTURE DECISION AD-001, OR THE GRAPHICS WHITE PAPER. It is the approved first-read authority for orientation and configuration control. AD-001 is separately approved as R0-A–F development authority. Neither approval passes an R0 gate, approves measured limits, or promotes a parent candidate or unresolved value.**

Approval was recorded by affirmative human action against the approved-draft hash above. Publication, silence, a code build, or an AI statement cannot create or broaden that approval.

### 1.1 Required approvers

| Role | Approval scope |
|---|---|
| Product/creative owner | Product behavior, controls/feel, campaign, missions, content, accessibility, art/audio, and player acceptance |
| Architecture owner/technical lead | Precedence, runtime invariants, memory, timing, ownership, public interfaces, implementation admission, and gates |
| MEGA65 platform reviewer | Hardware/core/ROM support, LLVM-MOS/45GS02 feasibility, VIC-IV, DMA, MAP, IRQ, audio, storage, and physical evidence |
| Test/acceptance owner | Evidence tiers, acceptance thresholds, reproducibility, hardware closure, and release qualification |
| Configuration-control owner | Exact hashes, approval records, status transitions, supersession, and manifest integrity |

The recorded approval is document-wide within this supplement's control role and explicit exclusions. It does not flatten parent status or authorize any unresolved behavior.

### 1.2 Approval does not flatten parent status

Approval of this Read-First Supplement does **not** automatically approve:

- Revision 1.5.1 if it still has Architecture-freeze-candidate status;
- Engine Draft 0.2;
- Architecture Decision `AD-001` unless the approval record expressly identifies and approves its exact bytes;
- unresolved product decisions;
- Gameplay or Engine `TARGET`, `TBD`, or `R0-GATED` values;
- white-paper recommendations;
- unfinished Midnight Spear, campaign, ending, asset, or audio content; or
- any implementation, build, test result, acceptance waiver, or release.

## 2. Read This First

### 2.1 Current program statement

> **The specification set is not ready for autonomous full-game production. Under approved Architecture Decision AD-001, the complete R0-A through R0-F proof program is GO for development. Development authorization does not mark a gate passed: R0 acceptance remains dependency-ordered, evidence-based, and subject to physical-MEGA65 proof and the separately approved measured-limits revision. Findings block only the milestone named in their closure gate.**

This is the controlling orientation statement if this document is approved. It preserves useful work without permitting an AI engineer to convert a living draft, a measurement candidate, or an unwritten product decision into shipping behavior.

### 2.2 Required reading sequence

1. Read this supplement.
2. Check the approval/status record for this supplement and `AD-001`, then review §10, Human Decisions.
3. Read Revision 1.5.1 for the architecture, invariant, gate, and admission rule involved.
4. Read Gameplay 0.2 for the relevant player-visible or simulation behavior.
5. Read Engine 0.2 for candidate module, toolchain, schema, renderer, and implementation contracts.
6. Consult the graphics white paper only as supporting research under §16 of this supplement.
7. Trace the requirement to its owning interface, implementation task, gate, test, and evidence.
8. Stop and escalate when a material contradiction, unapproved value, or authority gap remains.

### 2.3 Controlled status vocabulary

| Label | Meaning |
|---|---|
| **Established by parent** | Explicitly stated by a governing source; still subject to that source's approval status |
| **Architecture candidate** | Revision 1.5.1 architecture text awaiting its recorded human approval |
| **Gameplay candidate / parent-adopted** | Gameplay 0.2 `MUST` adopted only as Revision 1.5.1 §1.2 provides; tuning classes retain their status |
| **Engine candidate** | Subordinate implementation contract awaiting architecture review/approval |
| **Read-First disposition** | Configuration/navigation status recorded here; cannot override a parent |
| **Supporting technical evidence** | Research useful for experiments; not product or architecture authority |
| **Planning assumption** | Reversible value for estimating or proof work; never shipping behavior |
| **R0-GATED** | Value frozen only by the named R0 evidence and measured-limits revision |
| **TARGET** | Intended target that may move through the source-defined evidence/approval process |
| **TBD** | Required value/table/content not yet selected; implementers may not choose it |
| **Human decision** | Material choice that requires the named human owner |
| **GO for development** | Construction, integration, execution, diagnosis, and evidence collection are authorized; no gate pass or production selection is implied |
| **Gate passed** | Complete required evidence has been reviewed and accepted by the named owner; development activity alone cannot create this status |

## 3. Specification Corpus and Hashes

### 3.1 Exact review inputs

| Logical role | Exact supplied filename | SHA-256 | Declared status | v1.0 authority classification |
|---|---|---|---|---|
| Supporting graphics research | `1-MEGA65_Flight_Simulation_3D_Graphics_White_Paper.pdf` | `7e3f775dc5624a543ea8cccbad786be7940ca48b7603b98dd94b5c5e6de64491` | Technical White Paper Rev 1.0; internally “Project Baseline — Flight Simulation” | **SUPPORTING TECHNICAL REFERENCE** |
| Candidate engine/toolchain design | `2-F-65-Engine-Runtime-and-Toolchain-Design-Supplement-Draft-0.2.md` | `dfd4bf0b557b4dae6382de502db42e4b2d269ceaf44bd67440bb6d047341454a` | Draft 0.2; Architecture-review candidate | **CANDIDATE NORMATIVE**, subordinate |
| Gameplay companion | `3-F-65-Megawing-Gameplay-and-Simulation-Requirements-Supplement.md` | `5db0344f8e7fd66143874310c3794a64391d4767229a90f5caee5e5e287d84e4` | Draft 0.2; Freeze candidate | **CANDIDATE / ADOPTED BY REVISION 1.5.1 RULES** |
| Current architecture candidate | `4-F-65-Megawing-Revision-1.5.1-Architecture-Invariants.md` | `46ba078cb397d257de6aeee66cff510c5e3243bca97767db1738d86d9ebd1fec` | Architecture-freeze candidate | **HIGHEST CURRENT ARCHITECTURE CANDIDATE** |
| Historical alignment audit | `5-F-65_Technical_Alignment_and_Corrections_Supplement_v0.2.md` | `fd8188f3787d902466a3d07b13c46e88f9afe32d7d5839945c4bc33143e0249b` | Draft — requires human review | **HISTORICAL/SUPERSEDED** after this document is approved |

The supplied historical v0.2 is byte-identical to the workspace file of the same logical name and hash. No divergent duplicate was found; duplicate path identity does not create an additional authority.

All five inputs were read completely. All nine white-paper pages were rendered and visually inspected. Filenames alone were not used as version evidence.

### 3.2 Approved R0 development-authorization control

The following document was created after the five-input audit and approved separately on 2026-08-20. It is not a sixth historical review input:

| Control artifact | SHA-256 | Current status | Authority classification |
|---|---|---|---|
| `F-65_Architecture_Decision_AD-001_R0_Program_Development_Authorization.md` | `a93726389cc4b7d0cf2b0c4e87e21237e165f377a542bcadafc564f1896f8385` | **APPROVED — R0-A–F DEVELOPMENT AUTHORITY** | **ACTIVE R0 DEVELOPMENT AUTHORIZATION**; controls only whether R0 proof work may be developed now |

### 3.3 Recommended future specification-set manifest

The future repository manifest should hash-pin this logical set without treating every member as equal:

| Manifest entry | Classification | Required status for conforming use |
|---|---|---|
| This Read-First Supplement v1.0 | **CONTROL / READ-FIRST** | Exact approved bytes and approval identity |
| Architecture Decision `AD-001` | **R0 DEVELOPMENT AUTHORIZATION** | Exact approved-draft hash and human approval identity recorded; active for bounded R0-A–F proof development |
| Revision 1.5.1 | **NORMATIVE ARCHITECTURE** | Approved/frozen status explicitly recorded; until then, candidate |
| Gameplay 0.2 | **NORMATIVE GAMEPLAY COMPANION** | Exact hash and adoption/approval effect recorded per Architecture §1.2 |
| Engine 0.2 | **CANDIDATE NORMATIVE ENGINE DESIGN** | Scope of architecture review/approval explicitly recorded |
| Graphics White Paper 1.0 | **SUPPORTING TECHNICAL REFERENCE** | Hash recorded; recommendations remain non-normative unless adopted elsewhere |
| Technical Alignment v0.2 | **HISTORICAL/SUPERSEDED** | Retained for audit trail, excluded from current precedence |

This document cannot embed a stable hash of itself without changing that hash. The approval record or external specification-set manifest must record the final approved file hash.

## 4. Authority and Precedence

### 4.1 Controlling sources by decision type

| Decision type | Controlling source | Limits |
|---|---|---|
| Architecture, determinism, ownership, memory, timing, simulation order, platform isolation, language policy, C/assembly boundary, admission, R0, Phase 1 | Revision 1.5.1 | It remains an Architecture-freeze candidate until human approval; do not call it Frozen prematurely |
| Player-visible behavior and simulation requirements | Gameplay 0.2 within Revision 1.5.1 | `MUST` adoption follows Architecture §1.2; `TARGET`, `TBD`, and `R0-GATED` are never silently promoted |
| Runtime decomposition, restricted target C, toolchain, C/ASM method, renderer proof, schemas, host tools/oracles, mission/compiler design, engineering gates | Engine 0.2 | Subordinate Architecture-review candidate; its `MUST` cannot create or override architecture |
| Orientation, hash/status control, historical disposition, open-decision navigation, task admission, STOP/ESCALATE | This Read-First Supplement | Cannot invent gameplay, tune values, override a parent, approve itself, or turn an Engine candidate into architecture |
| Whether bounded R0-A–F proof artifacts may be developed before their gates pass | Approved Architecture Decision `AD-001` | Development authorization only; cannot change invariants, waive dependencies, pass a gate, freeze limits, or authorize production gameplay |
| Graphics feasibility ideas and experimental candidates | Graphics White Paper 1.0 | Supporting only; its “Project Baseline” label has no F-65 precedence effect |
| Historical audit evidence | Technical Alignment v0.2 | No current implementation authority after v1.0 approval |

Revision 1.5.1's front matter controls its transition: until Revision 1.5.1 receives human approval, Revision 1.5 retains its existing candidate status and Revision 1.4.1 remains the last frozen architecture baseline. Approval of this Read-First document does not change that fact. It describes the 1.5.1/Engine 0.2 candidate set so authorized proof work can proceed without confusing candidate intent with frozen authority.

### 4.2 Gameplay's historical Revision 1.4.1 references

Gameplay 0.2 still names Revision 1.4.1. This is not, by itself, a current blocker. Revision 1.5.1 §1.2 says those references mean the corresponding preserved invariant in Revision 1.5.1. If residual wording actually differs, Revision 1.5.1 controls architecture and the difference must be recorded. Implementers may not infer that all historical references are defects or that Gameplay can override current architecture.

### 4.3 Conflict and escalation protocol

When two applicable statements produce different observable behavior, state ownership, memory layout, timing, data format, or acceptance result:

1. Record exact documents, hashes, sections, and requirement IDs.
2. Determine whether the authority hierarchy already resolves the difference.
3. Stop only the behavior whose result would differ.
4. Continue independent, reversible work that does not prejudge the outcome.
5. Record the owner and closure gate.
6. Obtain human approval when the authority model cannot resolve the issue.
7. Update the controlling requirement, interface, task, tests, evidence, and disposition together.

“Match current code,” “use the simplest option,” “follow the newest-looking prose,” and “the Engine says MUST” are not valid ways to override a higher source.

### 4.4 Fundamental evidence rules

**Code is implementation evidence. Code is not specification authority.**

A compiler output is not hardware proof. Xemu evidence is not physical-MEGA65 evidence where a hardware gate requires MEGA65 evidence. A white-paper recommendation is not an adopted renderer requirement. A passing build cannot select a `TBD`, approve a `TARGET`, or waive an R0 gate.

## 5. Current F-65 Baseline

### 5.1 Product

F-65 Megawing is a retro-synthwave, cockpit-primary, single-player fleet-interceptor combat-flight simulator for the MEGA65. The player aircraft is the F-65A.

Current governed scope includes consequential six-degree-of-freedom flight; Assisted and Manual laws; carrier and airfield operations; AI RIO; wingman; AIC; enemies; radar, RWR, jammer, and countermeasures; radar and infrared weapons plus cannon; fuel; electrical, hydraulic, and damage systems; the non-narrative Technical Combat Slice; separately authored Midnight Spear; a ten-operation campaign; two endings; an independently bootable MVP D81; and multi-D81 campaign packaging where approved.

This summary does not author still-unwritten missions, endings, doctrine, tables, thresholds, assets, narrative text, or tuning values.

### 5.2 Production implementation model

- LLVM-MOS C is the default production implementation for the MEGA65/45GS02 target.
- Handwritten 45GS02 assembly is selective, first-class target code for platform-critical work or measured offenders admitted under Revision 1.5.1 §1.4.
- Java remains the independent host-tool, generator, high-precision oracle, bit-exact model, asset/mission compiler, and test-infrastructure language unless a later approved decision changes a component.
- No C-versus-assembly quota exists.
- Final linked code, runtime/library support, constants, data, stack, cycles, DMA interaction, and hardware behavior—not source-language ideology—determine admission.

### 5.3 Core implementation guardrails

The controlling details remain in Revision 1.5.1. The minimum read-first guardrails are:

- exactly 100 Hz authoritative simulation during `ACTIVE_SORTIE`;
- the frozen 21-stage order;
- independent simulation and display clocks with no exact integer superperiod assumption;
- bounded extracted `PresentationSnapshot` ownership and complete-buffer presentation;
- fixed/static runtime capacities and no general deterministic-runtime heap;
- protected memory, code, stack, and reserve ownership;
- `MemoryAccessABI`, `FarPtr32`, `ResourceHandle16`, and platform-service discipline;
- no ordinary C pointer as arbitrary physical/far memory;
- Core/Platform ownership of MAP, DMA, IRQ, Q/extended-register, hardware-math, and protected hardware state;
- no target floating point in authoritative simulation;
- generated public/cross-language records and numeric contracts;
- deterministic replay/checksum and fault behavior;
- R0 physical-hardware proof and measured-limits revision; and
- the hard Phase 1 integrated-engine-harness gate.

## 6. Current Operational Readiness

### 6.1 Phase-specific verdict

Development authorization and gate acceptance are different states. The `AD-001` development authorization is active under its exact human approval record.

| Work horizon | Current development authorization | Acceptance status | Current condition |
|---|---|---|---|
| Documentation/configuration control | **GO** | Ongoing control activity | Continue review, disposition, hash control, schemas, and evidence planning under the recorded approval; later changes require their own status control |
| Codex Engineering Harness / host foundations | **GO** | Not a product gate | Bounded schemas, generators, validators, oracles, fixtures, reports, and evidence work may proceed under parent-defined scope and candidate labels |
| R0-A proof | **GO** | **NOT PASSED** | Construct and execute the non-gameplay toolchain/platform/memory proof; acceptance requires Gate 0 status, exact identities, Xemu and required physical evidence |
| R0-B proof | **GO** | **NOT PASSED** | Candidate graphics/display/cockpit/palette/input/audio work may proceed; pre-R0-A results remain provisional and require revalidation against the accepted identity |
| R0-C proof | **GO** | **NOT PASSED** | Production-shaped tools/scene/package/D81/residency/storage/save proofs may proceed; no proof package or medium becomes a production selection |
| R0-D proof | **GO** | **NOT PASSED** | The protected-workload fixture may be constructed and calibrated; acceptance depends on explicit upstream evidence identity |
| R0-E proof | **GO** | **NOT PASSED** | The combined-load Xemu harness may be developed; Xemu cannot close physical-hardware requirements |
| R0-F proof | **GO** | **NOT PASSED** | Physical-MEGA65 test software, capture procedure, and phase sweep may be developed and executed against the corresponding accepted configuration |
| Measured-limits revision | Preparation **GO** | **NOT APPROVED** | Draft only from traceable R0 evidence; values freeze only by separate human approval |
| Phase 1 integrated harness | **NO-GO now** | **NOT OPEN** | Requires R0-F and approved measured-limits revision plus Phase 1 interface/fault/snapshot inputs |
| Production gameplay implementation | **NO-GO now** | **NOT OPEN** | No production gameplay implementation in C or assembly may merge before R0-F/measured limits and the governing Phase 1 gate |
| Technical Combat Slice | **NO-GO now** | **NOT OPEN** | Requires Phase 1 plus minimum approved Phase 2–4 behavior/data and a non-narrative slice manifest |
| Midnight Spear | **NO-GO now** | **NOT OPEN** | Requires separately approved mission manifest and preceding technical evidence; it is not the Technical Combat Slice |
| Campaign/content production | **NO-GO now** | **NOT OPEN** | Requires approved authored-data manifests, campaign rules, assets, capacities, saves, and phase gates |
| MVP/release acceptance | **NO-GO now** | **NOT OPEN** | Requires approved content boundary, complete evidence, human acceptance, reproducible images, and release review |

Severity is independent of schedule. A severe Phase 4 content gap does not block R0 development; it blocks the milestone named in its closure gate.

### 6.2 Current principal risks

1. Candidate documents may be mistaken for approved shipping authority.
2. Exact LLVM-MOS/45GS02 ABI and toolchain behavior remains unverified until R0-A.
3. Snapshot payload size/count/location remains a measured memory/timing decision.
4. Renderer architecture, display mode, RRB use, and quality tier remain R0 choices.
5. Hardware behavior may differ from Xemu, especially for MAP, DMA, IRQ, video, audio, input, and storage.
6. Later gameplay tables and content remain human/phase gated and cannot be generated from taste or current code.

## 7. Authorized Work Now

Revision 1.5.1 §17 and Engine 0.2 §§17.1, 21, and 21.1 authorize the existing host/R0-A scope. Approved `AD-001` additionally authorizes development of the complete R0 proof program below.

### 7.1 Host foundations and R0-A

1. Generated physical-memory, allocation, code, stack, runtime-support, and reserve ledgers.
2. Initial machine-readable C, Java, and platform interface sources for the R0-A subset.
3. `CoreRuntime` foundational contracts required by proof work.
4. `InputCommandFrame` envelope and generated assertions required by the current interface subset.
5. Entity common headers and typed handle/resource-handle definitions.
6. `PresentationSnapshot` proof records without freezing measured payload size/count/location.
7. C/platform wrapper declarations, probes, and restoration contracts.
8. Module ownership/status source, generated status report, and diff-scope validation.
9. JSON5 mission-schema skeleton and conservative frozen-pool capacity-analyzer skeleton using the Gameplay peak as a non-shipping fixture.
10. LLVM-MOS frontend, target, CPU-selection, compiler, runtime/libc, warnings, ABI, stack, object/link, symbols/maps/listings/disassembly, and retained assembler verification.
11. Reproducible build identity and proof-D81 construction.
12. The Memory Access ABI proof with minimal compiled C, C-to-platform/assembly boundaries, MAP/base-page/DMA/IRQ/Q/stack restoration, and instrumentation.
13. Host golden-vector, deterministic fixture, evidence-index, and proof-report infrastructure.
14. Documentation repair and traceability maintenance that does not change parent semantics.

### 7.2 Additional R0-B–F development authorized by `AD-001`

1. R0-B graphics/display modes, cockpit/HUD/MFD composition, palette/swap behavior, complete-buffer presentation, bucket/painter tiers, bounded RRB/affine candidates, input latency/edge tests, and representative audio measurements.
2. R0-C production-shaped host tools, shared proof scene, converters, packages, D81 manifests, capacity witnesses, resource-residency/staging tests, and storage/save/media fault fixtures.
3. R0-D construction and calibration of the historical 530,000-clock protected non-render workload and per-service measurement fixtures.
4. R0-E independent-clock combined-load harnesses for snapshot, memory, renderer, input, audio, DMA/IRQ, storage, faults, reserves, and deterministic shedding in Xemu.
5. R0-F physical-MEGA65 test builds, capture procedures, corresponding phase sweeps, diagnosis, and evidence packaging.
6. Draft measured-limit reports and comparison tools that preserve candidate identities and do not freeze values before approval.

Construction may overlap. A downstream task must declare unresolved upstream dependencies and remain reversible; a result produced against an unpassed identity is provisional and must be rebuilt or revalidated after that identity passes.

Allowed work remains candidate or proof work until its governing approval and evidence gate closes.

### 7.3 Prohibited at the current horizon

- No production flight, radar, weapon, tactical-AI, campaign, Midnight Spear, or production-selected renderer implementation. Bounded R0 renderer candidates are authorized only as proof artifacts.
- No production gameplay implementation in C or assembly before its governing gate.
- No shipping value for a `TBD`, `TARGET`, `R0-GATED`, creative, or unresolved semantic item.
- No direct C physical-memory access outside approved abstractions.
- No unmeasured assembly optimization admitted by intuition.
- No memory-map, pool, reserve, ownership, tick-order, or public-ABI change without authorization.
- No bootstrap or proof artifact described as “published” until its reviewed path exists and validation succeeds.

## 8. R0 Program Orientation

### 8.1 R0-A identity proof

R0-A is a platform, toolchain, memory-access, and mixed-language proof. It is not gameplay, the renderer, the flight model, a vertical slice, or Midnight Spear.

Its evidence must cover, as governed by the parents:

- exact build and specification identity;
- LLVM-MOS/compiler/SDK/runtime/linker identity and target/CPU selection;
- C/assembly interoperability and the generated Platform ABI;
- stack behavior and high-water instrumentation;
- canonical MAP, `$01`, base-page, and return-state behavior;
- physical addressing, `FarPtr32`, resource-directory, and `MemoryAccessABI` behavior;
- DMA validation, blocking, completion, and IRQ-latency behavior;
- IRQ state and allowed windows;
- Q/extended-register and selected hardware-math behavior where applicable;
- generated layouts and cross-language assertions;
- reproducible D81, symbols, maps, listings/disassembly, and evidence index;
- Xemu regression; and
- physical-MEGA65 results for every hardware-required item.

Passing R0-A does not waive R0-B–F, the measured-limits revision, Phase 1, product decisions, or human review.

### 8.2 Full R0 development versus gate passage

Under approved `AD-001`, R0-A–F are all GO for proof development. Acceptance remains dependency-ordered:

1. R0-B–F outputs created before R0-A passes are provisional and must identify the candidate toolchain/platform/ABI used.
2. R0-D/E acceptance requires the applicable R0-B/C candidate identities and evidence inputs.
3. R0-F must correspond to an identified R0-E configuration and provide the required physical-MEGA65 evidence.
4. Failed or changed upstream evidence triggers rebuild or revalidation of dependent conclusions; independent tools and fixtures may continue.
5. Only a separately approved measured-limits revision may freeze the measured modes, counts, budgets, cadences, latencies, tiers, and reserve.

## 9. Gate and Milestone Map

Approved `AD-001` authorizes construction of every R0 proof. The fourth column therefore records the consequence of acceptance, not permission to begin construction.

| Gate | Purpose | Principal evidence | Acceptance consequence | Remains prohibited |
|---|---|---|---|---|
| Gate 0 — configuration control | Establish exact corpus, approval/status, owners, and task authority | Hash-pinned manifest; explicit Architecture/Gameplay/Engine/Read-First/`AD-001` status records | Formal use of the approved scope and R0 acceptance processing | Shipping behavior from candidates; silent promotion of tuning values |
| R0-A | Prove toolchain, mixed-language ABI, platform wrappers, memory access, and reproducible proof D81 | Identity lock; compiler/ABI probes; MAP/base-page/DMA/IRQ/Q/stack evidence; Xemu and hardware | Downstream R0 results may bind to the accepted identity rather than a provisional candidate | Gameplay, flight, radar, weapons, AI, campaign, production-selected renderer |
| R0-B | Measure graphics/display/cockpit/palette/input/audio candidates | Hardware captures, timing/latency, edge tests, complete-buffer proof | Viable candidates for later combined measurement | Production selection without R0-F/measured limits |
| R0-C | Prove tools, scene/package, D81, residency, storage/save path | Packages, manifests, capacity witnesses, boot/load/save/media evidence | Bounded package/resource/storage design for combined proof | Tactical disk reads; unresolved release UX/content |
| R0-D | Reproduce protected workload | 530,000-clock historical fixture plus calibrated per-service data | Comparable protected-load baseline | Treating average ledger as deadline proof |
| R0-E | Combine independent clocks, load, snapshot, renderer, input, audio, memory, and storage in Xemu | Phase-swept Xemu report, high-waters, faults, reserves | Candidate measured limits for hardware confirmation | Hardware closure from Xemu alone |
| R0-F | Confirm the corresponding physical-hardware behavior | Pinned MEGA65 phase sweep and complete identity | Measured-limits revision drafting | Gameplay merge before approved limits |
| Measured-limits revision | Freeze actual budgets, modes, counts, latencies, tiers, and reserve | Approved R0 evidence and selected values/tolerances | Phase 1 implementation within those limits | Values not supported by the approved evidence identity |
| Phase 1 integrated engine harness | Prove scheduler, pools, memory, input, audio, renderer, resources, snapshot, replay, faults together | Combined p95/worst, deterministic checksum, reserve, soak, PAL/NTSC equivalence | Phase 2 model implementation | Partial pass or isolated subsystem substitution |
| Technical Combat Slice | Prove the non-narrative end-to-end combat chain | Approved slice manifest, target/hardware evidence, replay, usability/readability review | Consideration of separately authored Midnight Spear | Rebranding the proof as campaign content |
| Midnight Spear | Prove the approved narrative mission | Separate manifest, authored assets/doctrine/objectives, capacity/replay/acceptance | Later approved campaign/content phases | Invented missions or implicit campaign rules |
| Campaign/content completion | Complete ten operations, two endings, assets, saves, and branch evidence | Ten-row manifest, branch replays, asset/D81 ledgers, human content approval | MVP/release candidate assembly | Unwritten operations/endings or unapproved asset scope |
| MVP/release acceptance | Qualify the approved product boundary | Reproducible images, full regression, physical evidence, human playtest/code/content/release approval | Human-authorized release | Any waiver not recorded as a named decision/risk acceptance |

No arbitrary dates are created here. Gate owners schedule work from dependency and evidence readiness.

## 10. Human Decision Register

### 10.1 Attention required now

Approval of this Read-First v1.0 and `AD-001` was recorded on 2026-08-20. The remaining immediate decisions are:

| Action | Owner | Required by | Recommendation | Consequence of deferral |
|---|---|---|---|---|
| `DEC-002` — specification approval state | Product + architecture | Gate 0 / before formal R0-A acceptance | Approve Revision 1.5.1 separately; record its Gameplay 0.2 adoption effect; complete or scope Engine 0.2 architecture review | Candidate prose cannot be represented as approved production authority |
| `DEC-003` — supported platform/evidence matrix | Platform + product | R0-A | Pin production MEGA65 model/memory, core/ROM/system files, CPU/video, storage, input, Xemu, and supported PAL/NTSC modes | R0-A hardware evidence cannot close or be compared reproducibly |

### 10.2 Current material decisions at later gates

Only decisions still requiring human action are retained. Recommendations are not defaults.

| ID | Current decision | Owner | Gate | Options/tradeoff | Recommendation | Consequence of deferral |
|---|---|---|---|---|---|---|
| `DEC-005` | Renderer/display candidate and quality floor, including whether to benchmark white-paper affine ground and RRB composition | Architecture + graphics/platform + product/art | R0-B–F / measured limits | Engine bucket/painter proof only; add affine-ground candidate; or integrate a measured affine terrain resource into a tier. More candidates cost R0 time but reduce premature lock-in. | Benchmark affine as a clearly separate R0 candidate if it can use the same scene/evidence; keep bucket/painter as the current Engine proof until an approved result changes it. | Renderer, display mode, RRB status, assets, and quality tier cannot freeze |
| `DEC-006` | F-117A comparative identity or abandonment | Product + acceptance/legal | Before any comparative claim; never an R0/Phase 1 dependency | Pin a lawful exact release/configuration; choose another reference; or keep all comparisons non-normative | Defer; use absolute F-65 thresholds first | No comparative claim is available; early engineering is unaffected |
| `DEC-007` | Countermeasure/RIO failure control | Product | Before Phase 3 defense/input freeze | RIO automatic only; manual fallback; hybrid emergency action | Define one explicit degraded/failure path after defensive-system design is testable | Player agency and damaged-RIO behavior remain nonconforming |
| `DEC-008` | Midnight Spear mission definition | Product/creative | Before Midnight Spear implementation | Adapt an approved campaign operation; create a distinct mission; or rename/reframe the narrative slice | Keep the Technical Combat Slice non-narrative; approve Midnight Spear separately | Midnight Spear cannot be implemented or accepted |
| `DEC-009` | Flight-feel acceptance authority | Product | Before Phase 2 tuning acceptance | Single owner; qualified review panel; metrics only | Named product owner plus a small qualified panel and locked rubric, bounded by oracle safety/envelope requirements | AI may build model infrastructure but cannot freeze feel |
| `DEC-010` | Campaign branching and ending predicates | Product/creative | Before Phase 4–5 campaign authoring | Linear; limited deterministic branches; wider branching | Limited deterministic branches with explicit predicates and capacity/save proof | Operations 3–10, two endings, and campaign saves cannot complete |
| `DEC-011` | Final PCM/voice scope | Product/audio/platform | Representative audio lock after R0-B/F | SID/text/tones only; short PCM vocabulary; extensive voice | Retain the parent hybrid rule; expand only inside measured cache/D81/latency limits | Final audio manifest and content budget remain open |
| `DEC-012` | Save medium and player recovery UX | Product + architecture/platform | Before R0-C acceptance/content lock | Same disk; separate save disk; supported host storage; differing friction and reliability | Use the parent two-generation transaction on an explicitly supported writable medium with clear recovery | Storage acceptance and campaign reliability cannot close |
| `DEC-013` | Default controls and digital shaping | Product/accessibility | R0-B/Phase 2 | Simulation-heavy; context-optimized; multiple presets | One complete semantic action set with a context-optimized default and at least one alternate preset if it fits UX | Input proof can measure mechanics, but production feel/defaults cannot freeze |
| `DEC-014` | Absolute F-65 quality thresholds | Product + acceptance | Each consuming R0/slice/release gate | Approve proposed thresholds, revise from F-65 evidence, or defer per category | Establish absolute thresholds from R0 and representative F-65 evidence; do not depend on F-117A | Affected quality gate cannot pass; unrelated earlier work continues |
| `DEC-015` | Independently bootable MVP D81 content boundary | Product + architecture | Before package/content lock | Narrative slice plus shell; larger campaign subset; campaign bootstrap with other disks | Decide after Midnight Spear and R0-C fit evidence; preserve full campaign scope separately | Disk/assets/save budget and “MVP” remain ambiguous |

`DEC-001` and `DEC-004` are not current product-choice rows: §19 records their migration. Snapshot count/bytes/location are now a measured R0 decision rather than a preselected architecture option.

## 11. Current Conflict Register

This register contains current material contradictions or terminology differences, not historical defects already resolved by Revision 1.5.1. A parent-resolved difference remains listed only when an implementer could still follow the stale words incorrectly.

| ID | Documents/sections | Incompatible statements | Why it matters | Governing resolution | Owner / gate |
|---|---|---|---|---|---|
| `CUR-CON-001` | Gameplay §§2.1, 18; Architecture §§3.2, 3.9; Engine §§3.3, 8.1 | Gameplay says presentation consumes an atomic `SimulationSnapshot`; current Architecture and Engine require a bounded extracted `PresentationSnapshot` and forbid presentation access to authoritative state | A literal Gameplay implementation could expose or retain mutable authoritative storage | Architecture controls: every presentation-facing historical `SimulationSnapshot` reference is interpreted as the current `PresentationSnapshot` boundary. Correct Gameplay wording in its next controlled revision. | Architecture + Gameplay documentation; before Phase 1 snapshot/interface freeze; does not block R0-A proof records |
| `CUR-CON-002` | White Paper §§9.3, 13; Architecture §§3.1, 6; Engine §§2.1, 5 | White paper permits a 20–30 Hz simulation tied to a raster-driven frame loop; F-65 requires exactly 100 Hz authoritative simulation with independent presentation timing | Following the paper would change physics, sensors, replay, and deadlines | Revision 1.5.1 controls. The 20–30 Hz simulation recommendation is **SUPERSEDED BY F-65 ARCHITECTURE** and may not be prototyped as an F-65 simulation option. | Architecture; resolved for all gates |
| `CUR-CON-003` | White Paper §§4, 12–13; Engine §§8, 17.2 | White paper treats affine ground + RRB + billboards as its primary renderer baseline; Engine 0.2 makes bucket/painter filled/reduced/wireframe the primary production proof and allows affine/scaled copies only as measured candidates/resources | Two teams could build incompatible R0 scenes, memory layouts, and evidence while both claim the renderer baseline | White paper is non-normative. Engine proof remains the current candidate. `DEC-005` decides whether affine ground is added as a separately measured R0 candidate or integrated into a tier; no silent substitution. | Architecture + graphics/platform; R0-B–F |
| `CUR-CON-004` | White Paper §§2.3–2.4, 5.2, 10.1; Architecture §§2.5, 12.1; Engine §§3, 4.5, 6.1 | White paper describes background/continuous Attic tile streaming and DMA as a primary engine; parents require sole `ResourceManager` residency ownership, Core `DMAService`, normalized addresses, measured blocking, immutable jobs, bounded staging, and no tactical disk reads | “Background” could be implemented as unbounded or directly owned DMA that violates protected deadlines | Only bounded Attic-to-chip staging through the approved services is admissible. Disk streaming is prohibited. Exact tile set and staging cadence are R0-GATED. | Platform + Resource/Graphics; R0-C–F |
| `CUR-CON-005` | White Paper title/§9/roadmap; Architecture §§1.4–1.6; Engine §§2.3–2.5, 16.4 | White paper is written for assembly-language implementation; current production model is C-primary with selective assembly | Treating the paper as code policy would reintroduce assembly-first design and bypass compiler/ABI evidence | Architecture controls. Assembly-specific guidance is supporting low-level research only and must enter through an admitted wrapper or measured offender. | Architecture/toolchain; resolved as policy, verified per R0-A task |

No current conflict was found between the parent 100 Hz order, memory ownership, resource handles, DMA ownership, snapshot state machine, Technical Combat Slice identity, or C-primary policy in Revision 1.5.1 and Engine 0.2. Engine's `ENG-CON-001`–`006` are exposed dependencies or former Draft 0.1 contradictions, not six new parent conflicts.

## 12. Residual Findings and Missing Requirements

### 12.1 Milestone-aware residual findings

Severity describes consequence if unresolved at the consuming milestone. `Blocks authorized R0 construction?` asks whether the issue prevents bounded proof development under approved `AD-001`; it does not ask whether the affected gate may pass.

| ID | Severity | Status | Authority | Subsystem | Affected milestone | Closure gate | Blocks authorized R0 construction? | AI-independent work permitted? | Owner | Acceptance evidence | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `RF-FND-001` | Blocker | Open candidate-status gate | Architecture §status/§1.2; Engine §0 | Configuration control | Formal R0-A acceptance and every production phase | Gate 0 | **No** for construction; **Yes** for formal acceptance | **Yes**, labeled candidate/proof work | Product + architecture + config | Exact approval/status manifest | Revision 1.5.1 is not Frozen; Engine 0.2 is not approved by this document |
| `RF-FND-002` | Critical | Open verification gate | Architecture §§1.6, 2.6, 11; Engine §§2.5, 14.4, 18 | Compiler/platform ABI | R0-A | R0-A | **No**; it is the proof question | **Yes**, probes and reversible tool work | Toolchain + platform | Hostile-state C/ASM probes; Xemu and hardware; retained maps/listings | Blocks R0-A acceptance and dependent conclusions, not construction |
| `RF-FND-003` | Major | Required deliverables absent from reviewed corpus | Engine §21.1 | Bootstrap artifacts | R0-A | R0-A | **No**; creation is authorized work | **Yes** | Tooling/config | Paths exist, hashes recorded, validation passes | Required to pass R0-A; not a stop-work order |
| `RF-FND-004` | Major | Measured remainder | Architecture §3.9; Engine §§4.4, 18 `MEM-02` | Presentation snapshot | R0-D–F / Phase 1 | Measured-limits revision | No | Yes: schema/probe records without frozen size | Core + Graphics + memory | Forced-lag state tests, generated bytes/cycles/location, hardware phase sweep | Semantics are closed; bytes/count/location are not. Three buffers are the initial benchmark candidate, not a frozen count. |
| `RF-FND-005` | Major | Phase-gated interface work | Architecture §§4.5, 10.4; Engine §§14.2–14.3, 18 | Generated interfaces/numerics | R0-A subset; Phase 1–4 consumers | Before each consumer freezes | No; use the approved subset and provisional versions | Yes, within approved logical records | Architecture + module owner | Cross-language asserts, invalid/boundary examples, version/impact report | Do not freeze later layouts merely to make the generator complete |
| `RF-FND-006` | Major | R0 choice | Architecture §§6, 13.1; Engine §§5, 8, 18 `REN-*`; `DEC-005` | Renderer/display | R0-B–F | Measured-limits revision | No | Yes: bounded candidates under `AD-001` | Graphics + platform + product/art | Same-scene cost, clarity, complete-buffer, input/audio, reserve, hardware evidence | Candidate construction is authorized; production selection remains open |
| `RF-FND-007` | Major | R0-A identity gap | Architecture §11; Engine §14.4/`TOOL-01` | Toolchain | R0-A | R0-A | No; verification is authorized work | Yes | Tooling | Verified lock, two-host reproduction as applicable, symbols/maps/listings/evidence index | Blocks R0-A pass; unknown values stay `UNVERIFIED` |
| `RF-FND-008` | Major | R0 measured values | Engine §18 `CPU-01`, `AUD-01`, `IN-01` | Timing/input/audio | R0-B–F | Measured-limits revision / Phase 1 | No | Yes: experiments with proxy assets | Platform + subsystem owners | Independent-phase p50/p95/worst, latency/edge/audio tests on hardware | No exact frame/tick superperiod |
| `RF-FND-009` | Major | Human/platform decision | Architecture §11; `DEC-003` | Support matrix | R0-A | Gate 0/R0-A | No; candidate-matrix probes may proceed | Yes: diagnostic probes | Platform + product | Boot identity and explicit supported/unsupported matrix | Blocks formal hardware closure, not construction |
| `RF-FND-010` | Major | Product remainder | Architecture §12.2; Engine §§13.5, 18 `ENG-CON-005`; `DEC-012` | Storage/save | R0-C/campaign | R0-C for medium; content lock for UX | No | Yes: format/fault fixtures | Product + storage/platform | D81/package manifest and physical media/fault matrix | Transaction semantics are defined; exact medium and recovery experience are not |
| `RF-FND-011` | Major | Human acceptance work | Gameplay §§7, 17, 20; `DEC-009/013/014` | Feel/readability/usability | R0-B, Phase 2, Technical Slice, release | Consuming human gate | No | Yes: instrumentation and non-tuned oracles | Product + acceptance | Locked rubric, named build, qualified review, absolute thresholds | AI cannot freeze feel or quality by optimizing a proxy metric |
| `RF-FND-012` | Major | Deferred authored tables | Gameplay §19 `FL-*`, `EN-01`, `FU-01`, `CV-01`; Engine §18 | Flight/systems/contact | Phase 2 | Phase 2 gates | No | Yes: oracle infrastructure and boundary schema | Product/flight + architecture | High-precision/bit-exact vectors and qualified pilot approval | No shipping coefficients may be invented |
| `RF-FND-013` | Major | Deferred authored tables | Gameplay §19 `RD/WP/GN/DF-*`; Engine §18 | Radar/weapons/defense | Phase 3 | Phase 3 gates | No | Yes: scenario harnesses/schemas | Product/combat + architecture | Sensor/trajectory/defense matrices and replay | Geometry/energy contracts are defined; tuning tables are not |
| `RF-FND-014` | Major | Deferred product data | Gameplay §§14, 16, 19 `AI/MS-01`; Engine §§10, 13, 18 | AI/missions/Midnight Spear | Phase 4 | Phase 4 / separate manifest | No | Yes: compilers and non-shipping fixtures | Product/creative + AI/mission | Sensor-limited traces, capacity witnesses, approved mission manifest | Technical Combat Slice is not Midnight Spear |
| `RF-FND-015` | Major | Deferred content | Architecture §12.3; Gameplay §16; `DEC-010/015` | Campaign/assets/release | Phase 5 | Campaign/content lock | No | Yes: schema/manifest tooling | Product/creative/art/audio | Ten-row manifest, ending predicates, asset/D81 fit, branch replays | No operations/endings/assets invented by implementation agents |
| `RF-FND-016` | Minor | Editorial conflict | `CUR-CON-001` | Snapshot terminology | Phase 1 docs/interfaces | Before Gameplay successor approval or Phase 1 freeze | No | Yes: mechanical edit after approval | Gameplay + config | Terminology/link check | Architecture already supplies behavior |
| `RF-FND-017` | Major | Residual platform/storage path | Architecture §2.1; Engine §§13.5, 18 | ROM reclaim and storage | R0-C | R0-C | No | Yes: diagnostic and R0-C proof work under `AD-001` | Platform + storage | Last ROM/hypervisor operation, handoff, post-reclaim I/O, guards, recovery evidence | Do not assume ROM routines remain callable after reclaimed display ownership |
| `RF-FND-018` | Major | Candidate-selection risk | `CUR-CON-003/004`; `DEC-005` | Renderer/resource staging | R0-B–F | Measured-limits revision | No | Yes, under an admitted `AD-001` proof task | Graphics + platform | Same identity/scene and full service contention evidence | White-paper methods may not become a parallel unbudgeted renderer |

### 12.2 Missing requirements by consuming milestone

| Gap ID | Missing item | Consuming milestone | Owner | Blocks authorized R0 construction? | Acceptable closure evidence |
|---|---|---|---|---|---|
| `MR-001` | Recorded approval/status manifest for Architecture 1.5.1, Gameplay adoption, Engine 0.2, and this document | Gate 0/formal R0-A acceptance | Configuration control + product/architecture | No construction; yes acceptance | Exact hashes, approvers, dates, scope, supersession |
| `MR-002` | Exact MEGA65/core/ROM/system/video/storage/input support matrix | R0-A | Platform + product | No; blocks formal R0-A closure | Boot identity, supported/unsupported results, approved matrix |
| `MR-003` | Verified LLVM-MOS frontend/target/CPU/ABI/stack/runtime/link/diagnostic tool identity | R0-A | Tooling/platform | No; producing it is authorized | Populated lock, probes, maps/symbols/listings/disassembly, evidence index |
| `MR-004` | Initial C/Java/platform registry subset and actual bootstrap artifacts | R0-A | Architecture/tooling | No; producing them is authorized | Generated assertions, existing reviewed paths, stale-output and diff-scope validation |
| `MR-005` | Snapshot maximum bytes/count/location/cost | R0-D–F/limits | Core/Graphics/memory | No | Generated ledger plus lag/phase/hardware evidence |
| `MR-006` | Display mode, viewport, RRB use, world tier, affine-candidate disposition, cadence and clarity floor | R0-B–F/limits | Graphics/platform/product | No | Same-scene captures/cycles/bytes/latency/reserve and human readability decision |
| `MR-007` | Per-tick/service/module/DMA/IRQ/audio/input worst-phase limits | R0-D–F/limits | Platform/runtime leads | No | Pinned Xemu plus hardware phase sweeps and approved reserve |
| `MR-008` | Resource tile dimensions/resident count/staging cadence and terrain presentation encoding | R0-C–F/Phase 1 | World/Resource/Graphics | No | Package/capacity report, query/presentation separation tests, staging measurements |
| `MR-009` | Save medium and player recovery UX | R0-C/content lock | Product/storage | No | Approved `DEC-012`, media fault matrix, transactional recovery |
| `MR-010` | Event/queue producer fan-out, exact capacities, and fault-code catalog | R0-E/Phase 1 | Core + every producer | No | Static proof, one-over fixtures, bounded records and deterministic response |
| `MR-011` | Exact Phase 1 public layouts, numeric fields, replay/checksum algorithm, and compatibility rules | Phase 1 | Architecture + module/test | No | Registry version, cross-language probes, golden replay and first-divergence report |
| `MR-012` | Flight, engine, fuel, atmosphere, actuator, carrier/contact coefficients | Phase 2 | Product/flight + architecture | No | Named tables/tolerances, high-precision/bit-exact vectors, pilot review |
| `MR-013` | Radar, track, RWR, jammer, missile, gun, countermeasure, and damage tables | Phase 3 | Product/combat + architecture | No | Scenario/trajectory boundary corpus and deterministic replay |
| `MR-014` | RIO/wingman/enemy/AIC doctrine, cadence, weights, fallback, and damaged-RIO behavior | Phase 4 | Product + AI | No | Sensor-limited trace corpus and `DEC-007` disposition |
| `MR-015` | Midnight Spear manifest | Phase 4 after Technical Slice | Product/creative | No | Approved start/packages/entities/objectives/branches/doctrine/assets/load/replay/acceptance manifest |
| `MR-016` | Operations 3–10, ending predicates, campaign scoring/progression and branch data | Phase 5 | Product/creative | No | Approved ten-row manifest and branch replays |
| `MR-017` | Final visual/audio asset inventory and provenance | Slice/content/release | Art/audio + architecture | No | Per-asset manifests, converter rejection, aggregate chip/Attic/D81 fit, human approval |
| `MR-018` | Absolute handling, readability, latency, loading, stability, and experience thresholds | Each R0/slice/release gate | Product + acceptance | No for R0-A | Approved threshold/evidence record for each consuming gate |

`NOT_APPLICABLE_UNTIL_GATE` is the correct status for a genuinely later requirement. It is not equivalent to `TBD`, `0`, empty, or implementer-selected.

## 13. Old Technical Alignment v0.2 Correction Disposition

Revision 1.5.1 §19 is the primary source for this table. “Closed” means the semantic defect was resolved at the proper parent level; it does not claim that implementation evidence exists.

| Correction | Current disposition | Governing basis | Remaining work / gate |
|---|---|---|---|
| `CORR-AUTH-001` | **CLOSED — adopted by Revision 1.5.1** | Architecture §1.2 makes 1.5.1 self-contained for architecture and hash-pins companions | Human approval/status manifest at Gate 0; no missing-Revision-1.4 blocker carried forward |
| `CORR-AUTH-002` | **PARTIALLY CLOSED** | Architecture §1.2 defines adoption/precedence; Engine §0 preserves candidate status | `DEC-002`: record Architecture/Gameplay/Engine approval scope before formal use |
| `CORR-REF-001` | **CLOSED — resolved by both** | Architecture §11 and Engine §§14.4/18 require complete evidence identity | Populate exact values and prove them at R0-A |
| `CORR-TIME-001` | **CLOSED — adopted by Revision 1.5.1** | Architecture §§3.1, 6.3; Engine §5 | Numeric ceilings and phase results at R0-D–F/limits |
| `CORR-SNAP-001` | **PARTIALLY CLOSED** | Architecture §§3.2, 3.9; Engine §§3.3, 8.1 | `MEM-02`: measured bytes, count, location, extraction cost at R0-D–F |
| `CORR-IFACE-001` | **PARTIALLY CLOSED** | Architecture §10.4; Engine §14.2 | Actual initial registry at R0-A; later exact layouts before consumers |
| `CORR-NUM-001` | **PARTIALLY CLOSED** | Architecture §4.5; Engine interfaces/oracle requirements | Exact formats/tables at Phase 1–3 consuming gates |
| `CORR-INPUT-001` | **PARTIALLY CLOSED** | Architecture §7; Engine §11 | Initial frame subset R0-A; bindings/gesture/shaping R0-B/Phase 1–2 |
| `CORR-PAUSE-001` | **CLOSED — adopted by Revision 1.5.1** | Architecture §3.8; Engine §§11, 19.2 | Implementation/evidence at Phase 1 |
| `CORR-FAULT-001` | **PARTIALLY CLOSED** | Architecture §§3.6, 3.10, 12.6; Engine §§15, 19 | Actual fault catalog Phase 1; player recovery wording by product gate |
| `CORR-PLAT-001` | **PARTIALLY CLOSED / C-ADAPTED** | Architecture §§1.6, 2; Engine §2.5 | Exact compiler/platform ABI and wrapper proof at R0-A; assembly-only prescription rejected |
| `CORR-MEM-001` | **PARTIALLY CLOSED** | Architecture §5.4; Engine §4 | Generated layouts, runtime/stack/fault/snapshot charges, combined evidence at R0-A–E/Phase 1 |
| `CORR-STORE-001` | **PARTIALLY CLOSED** | Architecture §12.2; Engine §§13.5, 19.5 | Exact medium/UX/load ceilings at R0-C/content lock |
| `CORR-TOOL-001` | **PARTIALLY CLOSED / C-ADAPTED** | Architecture §11; Engine §§14.4, 21 | Actual LLVM-MOS lock/build/evidence at R0-A; KickAssembler-only model obsolete |
| `CORR-ASSET-001` | **CLOSED AS CONTRACT; DEFERRED AS DATA** | Architecture §12.1; Engine §14.1 | Actual bounded inventory/provenance at slice/content gates |
| `CORR-MISSION-001` | **CLOSED AS ARCHITECTURE DISTINCTION** | Architecture §§1, 12.3, 14; Engine §§13, 17 | Separate approved Midnight Spear manifest remains Phase 4 product work |
| `CORR-CAMP-001` | **CLOSED AS GATE; DEFERRED AS CONTENT** | Architecture §12.3; Gameplay §16 | Ten-row manifest, operations 3–10, endings Phase 4–5 |
| `CORR-RADAR-001` | **CLOSED AS SEMANTIC SEPARATION** | Architecture §§1.3, 6.4, 12.4; Engine §9 | Exact sensor/display schedules and tables at Phase 3/R0 display gate |
| `CORR-AUDIO-001` | **PARTIALLY CLOSED** | Architecture §12.5; Engine §12 | R0 cache/rate/channel/latency/content measurements |
| `CORR-REPLAY-001` | **CLOSED AS CONTRACT** | Architecture §10.6; Engine §15 | Exact generated schema/algorithm and evidence at Phase 1 |
| `CORR-TEST-001` | **CLOSED AS CONTRACT** | Architecture §§12.6, 15; Engine §19 | Evidence produced at each gate; no evidence-tier substitution |
| `CORR-BENCH-001` | **REJECTED AS PRODUCT REQUIREMENT / INFORMATIONAL ONLY** | Architecture §19 explicitly does not adopt F-117A comparison | `DEC-006` only before a future comparative claim; never early gate |

## 14. C-Primary and Toolchain Alignment

### 14.1 Migration of assembly-first concepts

| Obsolete v0.2 concept | Current governing interpretation |
|---|---|
| “All production target game code is 45GS02 assembly” | LLVM-MOS C is the default target implementation; selective handwritten 45GS02 remains first-class when platform- or measurement-admitted |
| “Gameplay assembly” | **Production gameplay implementation in C or assembly**; no such implementation before its gate |
| “Production-renderer assembly” | **Production renderer target implementation**; language follows contract, platform need, and measured evidence |
| Java/assembly-only generated interfaces | Generate C and Java bindings; generate low-level offsets/macros only where an admitted low-level consumer exists |
| KickAssembler-only toolchain | LLVM-MOS compiler/SDK/runtime/linker are primary; retain and pin a low-level assembler only when actually required |
| Assembly byte accounting | Charge all linked code, constants, thunks, runtime/libc, wrappers, data, stack, DMA, and low-level bytes to owners |
| Every module eventually becomes assembly | C remains production when it satisfies behavior and budgets; no rewrite obligation or language quota exists |
| AI may choose assembly sequences as a routine local optimization | AI may implement admitted low-level work only behind an approved ABI and evidence contract; intuition alone is insufficient |
| R0-A proves only assembly/opcodes/platform | R0-A proves minimal compiled C, C/platform/assembly calls, ABI, stack, object/link flow, and low-level platform behavior |
| Module status records only assembly implementation | Record target language, C conformance, runtime/data/stack cost, low-level optimization status, common vectors, and accepted evidence |
| “Assembles” means accepted | Compile/assemble/link is only build evidence; oracle, ABI, budget, Xemu, hardware, and human evidence remain separate |

### 14.2 Admission rule for low-level code

Handwritten assembly is admitted only when Revision 1.5.1 §1.4 already identifies the operation as platform-critical or measurement identifies a concrete offender. The task must state the measured problem, approved ceiling, boundary, clobbers, stack/MAP/base-page/IRQ behavior, before/after code/data/cycle evidence, and unchanged common tests. Faster code that changes rounding, saturation, order, faults, ownership, reserve, or player behavior is rejected.

The exact LLVM-MOS frontend name, target/CPU flag, ABI, object format, stack, runtime/libc subset, interrupt support, warning flags, and assembler interoperability remain `UNVERIFIED` until R0-A records real evidence. This document deliberately does not fabricate them.

## 15. AI / Codex Engineering Rules

### 15.1 Codex may autonomously perform

- bounded implementation behind an approved interface and admitted milestone;
- generated schemas, C/Java/applicable-low-level bindings, and validators;
- host tests, deterministic fixtures, approved reference/oracle implementations, and golden-vector infrastructure;
- evidence collection, instrumentation, reproducible build work, and reports;
- behavior-preserving refactoring inside authorized paths and budgets;
- C implementation of an authorized target module;
- approved low-level implementation when the task explicitly admits assembly;
- measured optimization proposals with retained before/after evidence; and
- mechanical documentation/traceability updates that do not change semantics.

### 15.2 Codex must stop and escalate for

- architecture, ownership, tick-order, cadence, memory-map, pool, reserve, or public-ABI changes;
- new product behavior, gameplay invention, changed player-visible mechanics, difficulty, or scope;
- choosing production values for `TBD`, `TARGET`, or `R0-GATED` material;
- unverified compiler, ABI, platform, core, ROM, DMA, IRQ, MAP, Q, video, audio, storage, or input assumptions;
- direct C physical/far-memory access outside approved services;
- renderer architecture changes not already admitted as an R0 candidate;
- resource residency or tactical streaming outside parent rules;
- mission, campaign, ending, art, audio, controls, feel, or accessibility choices requiring human approval;
- acceptance waivers or substituting host/Xemu evidence for required hardware/human evidence; or
- any change outside the task's authorized paths or module ownership.

An AI may continue independent reversible work while a later decision is open, but must not encode a planning assumption into shipping behavior.

## 16. Graphics White Paper and Renderer Disposition

### 16.1 Authority statement

The *MEGA65 Flight Simulation 3D Graphics White Paper Rev 1.0* is a useful feasibility/reference document. Its internal status “Project Baseline — Flight Simulation” was not issued by the F-65 authority chain and does not make it an F-65 baseline.

It may inform R0 candidates. It may not override the 100 Hz authoritative simulation, C-primary production model, `MemoryAccessABI`, DMA ownership, `PresentationSnapshot`, deterministic state, resource-residency rules, R0 gates, or Engine 0.2 renderer contract.

### 16.2 Common ground

Revision 1.5.1, Engine 0.2, and the white paper agree on the value of horizon stability; complete-buffer presentation; sparse geometry; billboards/impostors; distance LOD; bounded working sets; no general per-pixel Z-buffer; VIC-IV/RRB/DMA opportunities subject to measurement; cockpit readability; frame-time instrumentation; emulation for routine work; and physical hardware validation.

### 16.3 Recommendation-by-recommendation disposition

| White-paper recommendation | Disposition | F-65 interpretation |
|---|---|---|
| Affine/Mode-7-style ground as primary technique | **CANDIDATE FOR R0 EXPERIMENT** | May be benchmarked under `DEC-005`; does not replace Engine's bucket/painter proof without approved measured evidence |
| RRB cockpit/instrument composition | **CANDIDATE FOR R0 EXPERIMENT** | Architecture protects cockpit/HUD/MFD layers but does not require RRB; exact raster/composition method is R0-GATED |
| VIC-IV FCM/NCM/SEAM use | **CANDIDATE FOR R0 EXPERIMENT** | Candidate mode/asset encodings only; selected resolution/packing/palette must fit the parent ledgers and evidence |
| DMA fractional stepping for ground rows | **CANDIDATE FOR R0 EXPERIMENT** | Allowed only through Core-owned `DMAService`, normalized addresses, immutable jobs, and measured blocking/latency admission |
| Continuous terrain/tile streaming | **REQUIRES HUMAN/ENGINE DECISION** | Bounded Attic-to-chip staging may be tested; unbounded background work and tactical disk streaming are prohibited |
| 8 MB Attic library | **CONSISTENT SUPPORTING EVIDENCE** with qualification | Immutable cold assets and staged consumers fit parent policy; actual supported-memory matrix and resource ledger remain R0-A/C decisions |
| Billboard traffic | **CONSISTENT SUPPORTING EVIDENCE** | Engine already requires measured impostors/LODs with explicit asset/list/transform/DMA cost |
| Very low-poly close objects | **CONSISTENT SUPPORTING EVIDENCE** | Fits sparse mesh and bounded local sorting; authored limits and scene cost remain R0-GATED |
| No hardware/per-pixel Z-buffer | **CONSISTENT SUPPORTING EVIDENCE** | Engine proof uses buckets/painter order and bounded local sorting |
| 320×200 or 640×200 starting resolutions | **CANDIDATE FOR R0 EXPERIMENT** | No resolution is frozen; parent display stores, protected services, readability, and reserve control selection |
| 20–40 FPS target bands; 15–25 FPS complex scene | **SUPERSEDED BY F-65 ARCHITECTURE** where below the floor | F-65's measured limits and 20 Hz world failure floor control. White-paper bands are not acceptance thresholds |
| Horizon updated every visual frame from attitude | **CONSISTENT SUPPORTING EVIDENCE** with boundary | Renderer derives horizon from a complete snapshot; it never reads mutable aircraft state directly |
| Raster-position timing and worst-frame logs | **CONSISTENT SUPPORTING EVIDENCE** | Must be combined with independent-clock phase sweeps, per-tick/service costs, DMA/audio/input, and reserve—not just frame averages |
| Assembly numeric/critical-path guidance | **SUPERSEDED BY F-65 ARCHITECTURE** as language policy | Fixed-point and measured hot paths remain relevant; C is default and low-level work follows Platform ABI/admission |
| 20–30 Hz simulation recommendation | **CONFLICTS WITH F-65 ARCHITECTURE** | Rejected for F-65. Authoritative simulation remains exactly 100 Hz |
| Raster-driven main loop | **CONFLICTS WITH F-65 ARCHITECTURE** if authoritative | Raster may drive display service only; CoreRuntime owns the independent 100 Hz simulation scheduler |
| Renderer-first six-phase development sequence | **NOT APPLICABLE TO CURRENT F-65 DESIGN** as program plan | May structure a renderer experiment, but Revision 1.5.1/Engine 0.2 gate order controls the project |
| Affine height modulation for ordinary terrain | **REQUIRES HUMAN/ENGINE DECISION** | Presentation may use it; authoritative terrain height/LOS/contact must remain the Engine query data, never the rendered approximation |
| RRB/sprite runway, clouds, buildings, traffic layers | **CANDIDATE FOR R0 EXPERIMENT** | Each resource consumes explicit palette, memory, list, DMA, asset, and timing budgets; no layer is “free” |

### 16.4 Current renderer orientation

The current parent-aligned orientation is:

- Engine 0.2's bounded bucket/painter filled pipeline, reduced-filled tier, and wireframe contingency remain the primary production proof candidates.
- Affine ground is retained as supporting research and a possible additional R0 candidate, not selected production architecture.
- RRB is optional/R0-GATED, not required.
- Terrain/query truth remains separate from presentation at every tier.
- Any Attic tile staging is bounded, resource-handle based, and owned by `ResourceManager`/`DMAService`; no tactical disk read is permitted.
- The same protected-load scene, snapshot, service contention, and evidence identity must be used when comparing candidates.
- No renderer candidate passes solely because a still image looks attractive or an isolated loop is fast.

## 17. Task Admission Contract

A task entering implementation must identify every applicable field. A genuinely later-phase field may be marked `NOT_APPLICABLE_UNTIL_GATE: <gate> — <reason>`. Empty fields, guessed values, and `TBD` used as a number are invalid.

```text
Requirement IDs:
Approved decision/correction IDs:
Authorization basis and current status:
Milestone/gate:
Proof/candidate/production classification:
Owning module:
Authorized paths:
Prohibited paths:
Input/output interface versions:
Mutable-state owner:
Update stage/cadence:
Implementation language:
Compiler/toolchain identity:
Upstream evidence identities:
Provisional assumptions:
Rebuild/revalidation triggers:
Memory/code/stack/cycle/DMA budgets:
Data/asset/package IDs:
Normal behavior:
Boundary behavior:
Fault/overflow behavior:
Host oracle/golden vectors:
Host tests:
Xemu tests:
Hardware acceptance IDs:
Expected evidence:
Human review required:
Exit criterion:
```

Additional admission rules:

- An R0 task is not required to define campaign content; use `NOT_APPLICABLE_UNTIL_GATE: Phase 4/5`.
- A C task must still identify public ABI, stack, memory, runtime support, deterministic widths, and protected platform access.
- An assembly task must state its architecture/platform or measured admission reason and all clobber/restoration evidence.
- An R0 experiment must identify whether it is a parent-required proof or an optional candidate and may not relabel its result as a production selection.
- An R0-B–F task begun before its dependencies pass must cite `AD-001`, list every provisional upstream identity, and define the rebuild or revalidation trigger.
- A task that lacks an applicable material field may remain a specification/prototype task, not conforming production implementation.

## 18. AI-Readiness Assessment

Scores are `0` absent, `1` concept only, `2` materially incomplete, `3` implementable at a bounded gate with decisions outstanding, `4` strong candidate contract with measured/approval work remaining, and `5` approved and deterministically verifiable. These are documentation/program scores, not claims that code exists.

### 18.1 Subsystem scorecard

| Subsystem | Complete | Consistent | Feasible | Testable | Current implementation readiness | Principal remaining gate |
|---|---:|---:|---:|---:|---:|---|
| Authority/configuration control | 4 | 5 | 5 | 4 | 3 | Human status/approval manifest at Gate 0 |
| Compiler/toolchain | 3 | 5 | 4 | 5 | 4 for R0-A work | Actual LLVM-MOS/SDK/runtime/link evidence |
| C/assembly ABI | 4 | 5 | 4 | 5 | 4 for probes; 2 for accepted runtime | R0-A hostile-state/hardware proof |
| Memory/MAP/DMA | 4 | 5 | 4 | 5 | 4 for R0-A | Generated ledgers and R0-A/E/F evidence |
| Scheduler/determinism | 5 | 5 | 4 | 5 | 3 | Phase 1 implementation after measured limits |
| PresentationSnapshot | 4 | 5 | 4 | 5 | 3 | Measured bytes/count/location/cost |
| Generated interfaces | 4 | 5 | 5 | 5 | 4 for R0-A subset | Actual artifacts; later record layouts by phase |
| Input | 4 | 5 | 5 | 5 | 3 | R0-B edge/latency and human shaping |
| Renderer/display | 4 | 4 | 3 | 5 | 2 | R0 candidate comparison and measured limits |
| Flight | 3 | 5 | 3 | 5 | 1 | Phase 2 tables/oracles/pilot approval |
| Aircraft systems | 3 | 5 | 4 | 4 | 2 | Phase 2 dependencies/tables/faults |
| Radar/RWR/tracks | 4 | 5 | 4 | 5 | 2 | Phase 3 tables/cadences/layouts |
| Weapons/damage | 4 | 5 | 4 | 5 | 2 | Phase 3 tables/event bounds/trajectories |
| AI/RIO/wingman/AIC | 3 | 5 | 4 | 4 | 2 | Phase 4 doctrine/traces/human behavior |
| Mission/compiler | 4 | 5 | 5 | 5 | 4 for skeleton; 2 for full runtime | R0-A skeleton, then sound analyzer/Phase 4 data |
| Campaign | 2 | 5 | 4 | 3 | 1 | Phase 4–5 authored manifest/content |
| Audio | 4 | 5 | 4 | 5 | 2 | R0 rate/cache/channel/latency and content |
| Storage/save | 4 | 5 | 4 | 5 | 2 | R0-C medium/recovery/physical evidence |
| Assets/conversion | 4 | 5 | 4 | 4 | 3 for schemas/proxies; 1 for final | R0 converters and later approved inventory |
| Replay/diagnostics | 4 | 5 | 5 | 5 | 3 | Generated schema and Phase 1 target evidence |
| Acceptance/evidence | 4 | 5 | 5 | 5 | 3 | Threshold owners plus actual gate artifacts |

The old approximately `1.5/5` full-game score is not reused. It mixed later creative gaps with current proof readiness and assumed an obsolete architecture. Current scores must be read with the consuming gate column.

### 18.2 Readiness by horizon

| Horizon | Documentation readiness | Implementation readiness | Verdict rationale |
|---|---:|---:|---|
| A. Documentation/configuration | 4/5 | 4/5 | Coherent candidate hierarchy and dispositions exist; exact human approvals/manifest remain |
| B. R0-A | 4/5 | 4/5 to begin, 0/5 accepted evidence | Scope/contracts are strong; the purpose is to generate the missing real toolchain/ABI/hardware proof |
| C. R0-B–F measurement | 4/5 | 4/5 to begin after `AD-001`; 0/5 accepted evidence | Full proof development is authorized by `AD-001`; candidates and measured values intentionally remain provisional until evidence passes |
| D. Phase 1 harness | 4/5 | 2/5 | Invariants and module graph are strong; R0 limits, exact Phase 1 layouts, event/fault catalogs, and implementation are absent |
| E. Gameplay production | 3/5 | 1/5 | Observable contracts are rich, but Phase 2–4 tables, controls/feel, and human approvals remain |
| F. Full campaign/release | 2/5 | 0/5 | Operations 3–10, endings, final assets/audio, MVP boundary, thresholds, and release evidence are incomplete |

A later-horizon low score never expands the authority of earlier work and never creates a stop order outside its closure gate.

## 19. Final Readiness Checklists

### 19.1 Before formal R0-A acceptance

- [x] This Read-First Supplement has an exact human approval record.
- [x] `AD-001` has an exact Product/Architecture-scope approval record; R0-A–F proof development is authorized.
- [ ] Revision 1.5.1 approval/status and Gameplay adoption effect are recorded.
- [ ] Engine 0.2 approval/review scope is recorded.
- [ ] Supported hardware/core/ROM/video/storage/input and Xemu identities are pinned.
- [ ] Initial memory/code/stack/runtime/reserve ledgers and interface/platform registries exist and validate.
- [ ] LLVM-MOS frontend/target/CPU, ABI, stack, runtime/libc, object/link, warnings, maps/symbols/listings/disassembly, and any assembler are verified rather than assumed.
- [ ] Minimal compiled C and C/platform/assembly interoperability are proved.
- [ ] `MemoryAccessABI`, MAP, base-page, DMA, IRQ, Q/extended-register, stack, and return state pass normal/error/hostile-state tests.
- [ ] One reproducible proof D81 and machine-readable evidence index exist.
- [ ] Xemu evidence and required physical-MEGA65 evidence are separately identified.
- [ ] No gameplay, production renderer, flight, radar, weapon, AI, campaign, or Midnight Spear behavior is present or implied.

### 19.2 Before Phase 1

- [ ] R0-A through R0-F have passed their evidence gates and the measured-limits revision is separately approved.
- [ ] Snapshot bytes/count/location/cost and lag rules fit the memory/timing ledgers.
- [ ] Display mode/tier/RRB/renderer selection and shedding thresholds are frozen from common evidence.
- [ ] Phase 1 interface/numeric/fault/replay/resource/storage records are generated and versioned.
- [ ] Queue/event fan-out and one-over fault behavior are proved.
- [ ] Input/audio/DMA/IRQ deadlines and reserve are hardware measured.
- [ ] Terrain/query truth and presentation resources have one schema boundary.
- [ ] The Phase 1 combined harness task is admitted with exact paths, budgets, tests, and evidence.

### 19.3 Before gameplay, content, and release

- [ ] Phase 1 integrated harness passes completely; partial pass is failure.
- [ ] Each Phase 2–4 module has approved tables, oracles, interfaces, target evidence, and human-owned product decisions.
- [ ] Technical Combat Slice and Midnight Spear have distinct approved manifests and evidence identities.
- [ ] No operation, ending, doctrine, control feel, art, audio, or acceptance value was invented by an implementation agent.
- [ ] Ten-operation campaign/two-ending manifest exists before full campaign production.
- [ ] Final asset/audio/package/save/D81 ledgers fit with reserve and provenance intact.
- [ ] Absolute F-65 quality criteria and human playtest rubrics pass.
- [ ] Comparative claims, if any, use a separately approved lawful baseline and never waive an absolute F-65 requirement.
- [ ] Release images reproduce and pass the full physical-hardware, content, code-review, and human-acceptance process.

## 20. Final Current Verdict

| Area | Verdict | Condition |
|---|---|---|
| Documentation/configuration work | **GO** | Continue under the recorded Read-First approval and exact status/hash control for every parent or successor |
| Codex Engineering Harness work | **GO** | Limit to parent-authorized schemas, generators, validators, oracles, fixtures, build/evidence work, and non-shipping proof support |
| R0-A–F proof development | **GO** | `AD-001` approval is recorded; construction, integration, execution, diagnosis, and evidence collection are authorized across the full R0 program, with provisional dependencies and revalidation triggers recorded |
| R0-A–F gate acceptance | **NO-GO UNTIL EVIDENCE PASSES** | Each gate remains unpassed until its dependency-ordered evidence is reviewed; R0-F requires corresponding physical-MEGA65 evidence |
| Measured-limits approval | **NO-GO UNTIL R0 EVIDENCE PASSES** | A draft may be prepared, but only separate human approval freezes modes, budgets, counts, cadences, latencies, tiers, and reserve |
| Phase 1 | **NO-GO** | Opens only after R0-F and approved measured limits plus complete Phase 1 contracts |
| Production gameplay | **NO-GO** | Opens only after parent R0/Phase 1 gates and the relevant Phase 2–4 product/data approvals |
| Technical Combat Slice | **NO-GO** | Requires Phase 1 and approved minimum flight/radar/weapon/AI/slice data |
| Midnight Spear | **NO-GO** | Requires a separate human-approved mission manifest and preceding technical evidence |
| Campaign/content | **NO-GO** | Requires approved operations, endings, doctrine, assets, saves, capacities, and Phase 4–5 gates |
| Release | **NO-GO** | Requires the approved MVP/full-content boundary, complete evidence, reproducibility, and human code/content/playtest/release approval |

No single full-project GO/NO-GO is used because it would either freeze valid early work or conceal later gates.

## 21. Traceability and Appendices

### Appendix A — Stable requirement navigation

Authority labels:

- `A-CAND`: Revision 1.5.1 Architecture-freeze candidate.
- `G-CAND`: Gameplay 0.2 under Architecture §1.2 adoption/precedence.
- `E-CAND`: Engine 0.2 Architecture-review candidate.
- `RF-CTRL`: this Read-First control/disposition layer after approval.
- `AD-AUTH`: Architecture Decision `AD-001` after its separate human approval; proof-development authority only.
- `WP-REF`: white-paper supporting reference only.

| ID | Current requirement summary | Controlling source | Owner | Gate / acceptance navigation |
|---|---|---|---|---|
| `GAME-001` | Cockpit-primary retro-synthwave F-65A MEGA65 product; bootable MVP D81 | A-CAND §1 | Product/Graphics/Build | R0 display/storage; human product acceptance |
| `GAME-002` | RIO, wingman, AIC, enemies are deterministic and sensor-limited | G-CAND §14; E-CAND §10 | AIEngine | Phase 4 traces and human behavior review |
| `GAME-003` | Title/settings/saves/full pause/restart/no acceleration/no mid-sortie save | G-CAND §4; A-CAND §3.8 | UI/Core/Storage | Phase 1 pause; R0-C storage; Phase 4 restart |
| `GAME-004` | Bounded missions; Technical Slice distinct from Midnight Spear; ten operations/two endings | A-CAND §§1, 12.3; G-CAND §16 | Mission/Product | Phase 4–5 manifests and replays |
| `GAME-005` | Cockpit/HUD/radar/status/warnings/readability/accessibility | A-CAND §§1, 9; G-CAND §§9, 17 | Graphics/Input/Audio/Product | R0-B/F and human rubric |
| `GAME-006` | Debrief, grades, progression, retry and campaign persistence | G-CAND §§15–16 | Mission/Storage/Product | Phase 4–5 |
| `GAME-007` | F-117A comparison is non-normative unless separately approved | A-CAND §19; RF-CTRL §§10, 16 | Product/Acceptance | Before comparative claim only |
| `GAME-008` | Feel, usability, art/audio, creative direction and final acceptance remain human-owned | RF-CTRL §15 | Human owners | Every consuming gate |
| `FLIGHT-001` | Player/combat aircraft use one 100 Hz table-driven 6DOF path | A-CAND §§1.3, 3; G-CAND §7; E-CAND §7 | FlightDynamics | Phase 2 vectors |
| `FLIGHT-002` | Assisted/Manual laws share actuator/hydraulic/aero pipeline | A-CAND §7; G-CAND §7 | Controls/Systems | Phase 2 oracle + pilot review |
| `FLIGHT-003` | Engines, throttle, sweep, fuel/mass/performance use approved tables | G-CAND §§7, 13 | Systems/Flight | Phase 2 |
| `FLIGHT-004` | Gear/flaps/ADLC/contact/carrier/runway behavior is physical and bounded | G-CAND §§7.6, 15; E-CAND §6–7 | Controls/Contact/Flight | Phase 2 contact/carrier |
| `FLIGHT-005` | Supply and damage state resolve before controls/flight and degrade capability explicitly | A-CAND §§3.2, 8 | Systems | Phase 1 schema; Phase 2/3 behavior |
| `COMBAT-001` | Ten-missile/cannon loadout, physical release, stores and fire-control presentation | A-CAND §1.3; G-CAND §11 | WeaponDamage/Presentation | Phase 3 |
| `COMBAT-002` | Missiles use deterministic 3DOF 100 Hz guidance/seeker/fuze physics | G-CAND §11.3; E-CAND §7.4 | WeaponDamage | Phase 3 golden trajectories |
| `COMBAT-003` | Cannon uses grouped ballistics, lead, bounded groups/ammunition | G-CAND §11.4; E-CAND §7.4 | WeaponDamage | Phase 3 |
| `COMBAT-004` | Swept contact/fuze, ordered events, accumulated damage, no same-tick slot reuse | A-CAND §§3.3, 5; E-CAND §§6.3, 7.4 | Core/Contact/WeaponDamage | Phase 1 event proof; Phase 3 damage |
| `COMBAT-005` | RWR/jammer/decoy/notch/RIO defense is deterministic and explicit | G-CAND §12 | Sensor/AI/Weapon/Input | Phase 3; `DEC-007` |
| `RADAR-001` | Sensors derive deterministic observations from post-motion/post-damage truth | A-CAND §§3.2, 12.4; E-CAND §9 | SensorTrack | Phase 3 |
| `RADAR-002` | Organic/offboard/fused tracks share one contact identity and sensor-limited readers | G-CAND §§10, 18; E-CAND §9 | SensorTrack | Phase 3 registry/scenarios |
| `RADAR-003` | Fire control reads semantic tracks; display cadence cannot alter sensor/track state | A-CAND §§1.3, 12.4; E-CAND §9 | Sensor/Weapon/Graphics | Phase 3 + R0 display |
| `RADAR-004` | Truth/track pools and priority overflow remain bounded and stable | A-CAND §5; G-CAND §3.5 | Core/SensorTrack | Phase 1/3 one-over tests |
| `INPUT-001` | Semantic command frame covers axes/actions/four contexts | A-CAND §7; E-CAND §11 | InputEngine | R0-A subset; R0-B/Phase 1 complete |
| `INPUT-002` | Raw sampling preserves every legal edge into one command frame per active tick | A-CAND §7; E-CAND §11 | Input/Core | R0-B/Phase 1 10,000 transitions |
| `INPUT-003` | Pause input is out-of-band; no paused debt; release/neutral re-arm | A-CAND §3.8; E-CAND §11 | Core/Input/UI | Phase 1 |
| `INPUT-004` | Defaults, device profiles, shaping and discoverability are human/R0 gated | G-CAND §5; E-CAND §18 `IN-01` | Product/Input | R0-B/Phase 2 |
| `RENDER-001` | Incremental complete-buffer renderer consumes one complete snapshot and no Z-buffer | A-CAND §§3.9, 6; E-CAND §8 | Graphics | R0-B–F/Phase 1 |
| `RENDER-002` | Cockpit/HUD/MFD/warnings have protected presentation service | A-CAND §6.4; G-CAND §§9–10 | Graphics | R0-B–F readability/timing |
| `RENDER-003` | LOD/impostors/shedding consume explicit bounded resources and never affect authority | E-CAND §§5, 8.2 | Graphics/Asset tools | R0-B–F |
| `RENDER-004` | Display stores and selected mode/packing/swap fit measured ledgers | A-CAND §§2.1, 6 | Graphics/Platform | Measured-limits revision |
| `ENGINE-001` | C-primary LLVM-MOS target; selective 45GS02 assembly; Java independent host tools | A-CAND §§1.4–1.6; E-CAND §§2.3–2.5 | Architecture/Tooling | R0-A and every target gate |
| `ENGINE-002` | Core owns tick, lifecycle, order, DMA service, RNG/checksum, snapshot publication and debt | A-CAND §§3, 5; E-CAND §3.1 | CoreRuntime | R0-A subset/Phase 1 |
| `ENGINE-003` | One mutable owner; communication through approved records/queues/handles | E-CAND §3 | All modules | Interface/static-boundary tests |
| `ENGINE-004` | Snapshot extraction/publication is bounded, immutable and nonblocking to simulation | A-CAND §§3.2, 3.9 | Core/Presentation/Graphics | R0-D–F/Phase 1 |
| `ENGINE-005` | RNG/arithmetic/fault/replay/checksum behavior is deterministic/versioned/bounded | A-CAND §§3.4–3.10, 10.6 | Core/Diagnostics | Phase 1 and later replays |
| `ENGINE-006` | One generated C/platform ABI governs MAP/DMA/IRQ/Q/math and wrappers | A-CAND §§1.6, 2; E-CAND §2.5 | Platform/Core | R0-A |
| `ENGINE-007` | Packages/resources/saves are bounded, versioned, integrity-checked and non-tactical | A-CAND §12; E-CAND §13 | Resource/Storage | R0-C/Phase 1/campaign |
| `PERF-001` | Active simulation is exactly 100 Hz and PAL/NTSC/presentation independent | A-CAND §3.1 | Core | R0/Phase 1 replay/timing |
| `PERF-002` | Ticks never skip/merge; renderer yields; excessive debt faults | A-CAND §§3.6, 6.4 | Core/Graphics | R0-D–F/Phase 1 |
| `PERF-003` | Budgets use per-tick/service/worst-phase admission including DMA/audio/IRQ | A-CAND §6; E-CAND §5 | All runtime | R0-D–F/limits |
| `PERF-004` | Presentation tier/camera/effects/cadence never affect checksums; 20 Hz world is failure floor | A-CAND §§6.4, 15 | Core/Graphics | R0/Phase 1 |
| `PERF-005` | Player-facing quality thresholds are absolute and human approved | RF-CTRL §§10, 18–20 | Product/Acceptance | Consuming R0/slice/release gate |
| `MEM-001` | Canonical physical/CPU map and 32 KB measured reserve remain protected | A-CAND §2 | Core/Linker | R0-A/E/F |
| `MEM-002` | Only `MemoryAccessABI` uses MAP/base-page relocation; public return restores canonical state | A-CAND §§2.3, 2.6 | MemoryAccessABI | R0-A |
| `MEM-003` | Fixed typed pools/generations; no heap/growth/same-tick reuse | A-CAND §5 | Core | Generated ledger and Phase 1 |
| `MEM-004` | Queues/events have static fan-out, stable order, high-water and deterministic fault/drop | A-CAND §§3.3, 3.10, 5.4 | Core/producers | R0-E/Phase 1 |
| `MEM-005` | Attic resources are immutable/staged; all snapshot/audio/render/resource bytes are charged | A-CAND §§2, 12.1; E-CAND §4 | Resource/Linker | R0-C–F |
| `AUDIO-001` | SID/PCM follow one protected priority/service contract and cannot change simulation | A-CAND §12.5; E-CAND §12 | Audio | R0-B–F/Phase 1 |
| `AUDIO-002` | Audio formats/rates/cache/residency/channel data are bounded and staged | E-CAND §§4.4, 12, 14 | Audio/Resource | R0-B–F |
| `AUDIO-003` | Essential warnings meet approved latency and always have text/tone fallback | G-CAND §§12, 17; E-CAND §12 | Audio/Graphics | R0-B–F/human review |
| `TOOL-001` | macOS LLVM-MOS/Java/Xemu/retained-assembler workflow is pinned and reproducible | A-CAND §11; E-CAND §14.4 | Tooling | R0-A/release |
| `TOOL-002` | Host tools generate/validate mission, asset, interface, package and D81 artifacts | E-CAND §§13–14 | Host tools | R0-A/C and later phases |
| `TOOL-003` | Xemu is routine regression; physical MEGA65 closes hardware-sensitive gates | A-CAND §§11, 14–15; E-CAND §19 | Platform/Test | Every hardware gate |
| `TOOL-004` | Spec/build/package/platform/tool identities and status are retained machine-readably | A-CAND §§1.2, 11; RF-CTRL §§1–4 | Configuration control | Gate 0/R0-A/release |
| `TEST-001` | Independent high-precision/bit-exact Java oracles precede target acceptance where applicable | A-CAND §10; E-CAND §16.3 | Test/oracles | Each module gate |
| `TEST-002` | Replay/snapshot/pause tests prove canonical state and presentation isolation | A-CAND §§3.8–3.9, 10.6 | Core/Test | Phase 1 |
| `TEST-003` | Performance evidence records phases, modules, DMA/IRQ/audio, high-waters and reserve | A-CAND §§6, 10.3 | Platform/Test | R0-D–F/Phase 1 |
| `TEST-004` | Long-run hardware soak proves stability | A-CAND §15; E-CAND §19 | Test/platform | Phase 1/slice/release |
| `TEST-005` | Fault injection covers every bounded resource and invariant | A-CAND §§3.10, 12.6 | All owners/Test | Phase 1 and consuming gates |
| `TEST-006` | Storage/load/save/media failure and recovery are physically proved | A-CAND §12.2; E-CAND §19.5 | Storage/Test | R0-C/campaign |
| `TEST-007` | Technical Combat Slice proves the end-to-end non-narrative chain | A-CAND §§12.3, 14 | Program/Product/Test | Phase 4 entrance |
| `TEST-008` | Any comparative benchmark is deferred, lawful, controlled, and non-normative | A-CAND §19; RF-CTRL §10 | Product/Acceptance | Before comparative claim only |

### Appendix B — End-to-end traceability status

| Player outcome | Rule IDs | Engine/data path | Current implementation task/gate | Acceptance | Status |
|---|---|---|---|---|---|
| Predictable controls | `INPUT-001–004`, `FLIGHT-002` | Raw sample → semantic frame → law → actuator | R0-A frame subset; R0-B/Phase 1 edge bridge; Phase 2 shaping | 10,000 edge corpus + human control rubric | **Contract coherent; measured/human links open** |
| Deterministic flight | `FLIGHT-001–005`, `PERF-001` | Environment/tables → controls/systems → 6DOF/contact | Phase 2 tables/oracles | Host precision + bit-exact target + pilot review | **Phase-gated** |
| Stable cockpit/world | `RENDER-001–004`, `ENGINE-004` | Complete snapshot → protected overlays + resumable world renderer | R0-B–F candidates/limits; Phase 1 integration | Complete-buffer, lag, clarity, cadence, reserve | **R0-gated** |
| Radar awareness | `RADAR-001–004` | Truth → observation → track → fire control/display | Phase 3 schemas/tables; R0 display | Detection/track/overflow/cadence scenarios | **Semantic chain complete; tables open** |
| Weapon employment | `COMBAT-001–004` | Track/command → release → 100 Hz motion → fuze/damage/lifecycle | Phase 3 | Golden trajectories, event bounds, replay | **Phase-gated** |
| Defensive combat | `COMBAT-005`, `GAME-002` | RWR/track → RIO doctrine → jammer/decoy → seeker result | Phase 3–4; `DEC-007` | Sensor-limited traces and geometry scenarios | **Product fallback open** |
| Credible AI | `GAME-002`, `RADAR-002` | Sensor-limited blackboard → bounded doctrine/utility → next-tick intent | Phase 4 | No-truth-leak and tie/fallback traces | **Doctrine data open** |
| Missions/campaign | `GAME-004/006`, `TOOL-002` | JSON5 → compiler/capacity witness → package → runtime/save/debrief | R0-A skeleton; Phase 4–5 content | Compiler rejection, branch replays, human content approval | **Tool foundation ready; content open** |
| Critical audio | `AUDIO-001–003` | Simulation/presentation event → priority service → SID/PCM/text fallback | R0-B–F/Phase 1 | Hardware latency/contention/preemption | **R0-gated** |
| Reliable flow/storage | `GAME-003`, `ENGINE-007` | Manifest/package → preload → transactional save/recovery | R0-C then campaign | Physical boot/load/save/media matrix | **Medium/UX open** |
| Reproducibility | `TOOL-001–004`, `TEST-001–006` | Approved contracts → generators/oracles → target → evidence index | R0-A onward | Hashes, first divergence, Xemu/hardware separation | **Strong candidate; evidence absent** |

### Appendix C — Historical v0.2 conflict disposition

| Old ID | v1.0 disposition | Basis / current remainder |
|---|---|---|
| `CON-001` | **CLOSED — adopted by Revision 1.5.1** | Architecture §1.2 is self-contained for invariants and hash-pins companions; do not revive the missing-Revision-1.4 blocker |
| `CON-002` | **PARTIALLY CLOSED** | Architecture §1.2 resolves adoption/precedence; actual candidate approvals remain `DEC-002` |
| `CON-003` | **CLOSED — resolved by both** | Current Architecture/Engine use the Revision 1.5.1 evidence identity model; exact binaries/core still R0-A work |
| `CON-004` | **CLOSED — adopted by Revision 1.5.1** | Independent clocks and phase sweeps replace exact six-frame/ten-tick assumption |
| `CON-005` | **CLOSED — adopted by Revision 1.5.1** | Full-pause semantics are explicit in Architecture §3.8 |
| `CON-006` | **PARTIALLY CLOSED** | Snapshot state/lifetime is resolved; measured payload/count/location remains `MEM-02` |
| `CON-007` | **PARTIALLY CLOSED** | Engine 0.2 uses Gameplay-facing logical names and requires registry mapping; exact layouts/migration remain phased |
| `CON-008` | **CLOSED — resolved by both** | Core-owned `DMAService`, sole `ResourceManager`, read-only `Diagnostics` are explicit |
| `CON-009` | **CLOSED AS CONTRACT** | DMA blocking duration and protected-deadline admission are explicit; hardware ceilings remain R0 |
| `CON-010` | **CLOSED AS DOCUMENTATION DEFECT** | Engine 0.2 §21.1 explicitly says required artifacts do not exist merely because named; creation remains R0-A work |
| `CON-011` | **CLOSED — resolved by both** | Resource ownership/module graph is explicit |
| `CON-012` | **CLOSED AS SEMANTIC SEPARATION** | Architecture/Engine separate sensor/track updates from urgent presentation; exact cadences remain gated |

Current conflicts are only those in §11; historical IDs do not create active duplicate findings.

### Appendix D — Complete historical v0.2 findings disposition

Stable IDs are preserved as audit history. Historical severity remains visible in the ID but does not determine current scheduling.

#### D.1 Former Blocker and Critical series

| Old finding | v1.0 disposition | Exact current remainder / controlling gate |
|---|---|---|
| `FND-BLK-001` | **CLOSED — adopted by Revision 1.5.1** | Self-contained architecture/corpus rule; Gate 0 approval manifest remains `RF-FND-001`, not a missing-1.4 blocker |
| `FND-BLK-002` | **PARTIALLY CLOSED** | Gameplay adoption is defined; Architecture and Engine candidate approvals remain `DEC-002` before formal acceptance/production |
| `FND-BLK-003` | **PARTIALLY CLOSED; RECLASSIFIED AS MEASURED MAJOR** | Snapshot semantics are fixed; payload bytes/count/location/cost close at R0-D–F/measured limits (`RF-FND-004`) |
| `FND-CRT-001` | **CLOSED — adopted by Revision 1.5.1** | Independent-clock model governs; R0 supplies measurements |
| `FND-CRT-002` | **CLOSED — resolved by Engine 0.2** | False “published” claim removed; actual bootstrap artifacts are current R0-A deliverables (`RF-FND-003`) |
| `FND-CRT-003` | **PARTIALLY CLOSED** | Logical names/owners reconciled; exact public layouts/mappings close before their consuming interfaces (`RF-FND-005`) |
| `FND-CRT-004` | **PARTIALLY CLOSED / DEFERRED TO NAMED GATES** | Numeric registry obligation is architectural; actual fields/formats close Phase 1–3 |
| `FND-CRT-005` | **PARTIALLY CLOSED / DEFERRED TO NAMED GATES** | Semantic input/edge contract is defined; frame subset R0-A, mechanics R0-B/Phase 1, shaping/defaults Phase 2 |
| `FND-CRT-006` | **CLOSED — adopted by Revision 1.5.1** | Active-time pause semantics explicit; implementation evidence Phase 1 |
| `FND-CRT-007` | **PARTIALLY CLOSED** | Platform ABI ownership/invariants now explicit; exact LLVM-MOS/stack/register/object/link/hardware behavior remains R0-A (`RF-FND-002`) |
| `FND-CRT-008` | **PARTIALLY CLOSED / DEFERRED TO R0-C** | Package/save/residency transactions defined; exact medium, recovery UX, fit and physical evidence remain |
| `FND-CRT-009` | **DEFERRED TO NAMED GATES** | Consequential tables/content remain correctly `TBD`/human-owned at Phases 2–5; not a current blocker |
| `FND-CRT-010` | **PARTIALLY CLOSED / DEFERRED TO R0-E–PHASE 1** | Fan-out/static proof and deterministic fault rules required; actual derived capacities/evidence remain `MR-010` |

#### D.2 Major series

| Old finding | v1.0 disposition | Exact current remainder / controlling gate |
|---|---|---|
| `FND-MAJ-001` | **CLOSED AS ARCHITECTURE DISTINCTION** | Technical Combat Slice and Midnight Spear are explicitly distinct; Midnight Spear manifest remains `DEC-008`, Phase 4 |
| `FND-MAJ-002` | **DEFERRED TO PHASE 4–5** | Operations 3–10, endings, progression/content remain human-authored (`MR-016`) |
| `FND-MAJ-003` | **PARTIALLY CLOSED** | Technical fault behavior is defined; exact catalog Phase 1 and player recovery wording later (`MR-010`) |
| `FND-MAJ-004` | **PARTIALLY CLOSED** | Engine 0.2 paper audit and unallocated reserve clarify fit; generated layouts/runtime/stack/snapshot proof remains R0-A–E/Phase 1 |
| `FND-MAJ-005` | **CLOSED AS CONTRACT** | Finite bounded graphs, may-live analysis and witness paths are explicit; analyzer skeleton is R0-A, full soundness before mission consumers |
| `FND-MAJ-006` | **DEFERRED TO R0-B–F** | Display mode/packing/viewport/swap/RRB remain legitimate measured choices (`MR-006`) |
| `FND-MAJ-007` | **DEFERRED TO R0-B–F** | Renderer performance/clarity remains measurement risk, not a documentation contradiction (`RF-FND-006/018`) |
| `FND-MAJ-008` | **CLOSED AS CONTRACT; DEFERRED AS DATA** | Asset manifest/converter requirements are explicit; actual inventory/provenance awaits slice/content |
| `FND-MAJ-009` | **STILL OPEN / DEFERRED TO R0-B AND HUMAN SLICE GATE** | Readability/quality thresholds and degraded-tier mandatory cues remain `DEC-014`/`MR-018` |
| `FND-MAJ-010` | **PARTIALLY CLOSED** | Audio ownership/priority/fallback is defined; rates/cache/channels/latency/content remain R0/human (`DEC-011`) |
| `FND-MAJ-011` | **CLOSED AS CONTRACT** | Canonical replay/checksum scope/order/version/first divergence are specified; generated implementation/evidence remains Phase 1 |
| `FND-MAJ-012` | **INFORMATIONAL ONLY** | F-117A is non-normative/deferred; exact identity needed only before a claim (`DEC-006`) |
| `FND-MAJ-013` | **STILL OPEN / DEFERRED TO PHASE 3** | Damaged/unavailable RIO and manual/emergency countermeasure agency requires `DEC-007` |
| `FND-MAJ-014` | **DEFERRED TO PHASE 2** | Carrier/contact constants/assets and LSO thresholds remain properly gated; Technical Slice need not include carrier |
| `FND-MAJ-015` | **STILL OPEN / DEFERRED TO PHASE 2 HUMAN GATE** | Flight-feel reviewer/rubric authority remains `DEC-009/013/014` |
| `FND-MAJ-016` | **PARTIALLY CLOSED** | Tutorial restart starts a new deterministic run; exact campaign mutation/reward/seed transaction remains before Phase 4 use |
| `FND-MAJ-017` | **CLOSED AS SEMANTIC SEPARATION** | Sensor/track/display independence is explicit; exact scan/display values remain Phase 3/R0-gated |
| `FND-MAJ-018` | **PARTIALLY CLOSED** | One authoritative world/query model is explicit; tile encodings/dimensions/staging/query formats remain R0/Phase 1 (`MR-008`) |
| `FND-MAJ-019` | **PARTIALLY CLOSED / DEFERRED TO R0-A** | Complete platform/memory identity is required; actual supported matrix remains `DEC-003` |
| `FND-MAJ-020` | **CLOSED AS EVIDENCE RULE; DEFERRED AS MATRIX** | Parents prohibit evidence-tier substitution; exact physical matrix/evidence remains R0-A and later gates |
| `FND-MAJ-021` | **CLOSED — resolved by both** | Core `DMAService`, `ResourceManager`, and read-only Diagnostics ownership are explicit |
| `FND-MAJ-022` | **STILL OPEN / DEFERRED TO R0-C** | Post-ROM-reclaim I/O/hypervisor/storage handoff needs physical proof (`RF-FND-017`) |
| `FND-MAJ-023` | **STILL OPEN / DEFERRED TO CONTENT LOCK** | MVP D81 boundary/save space/campaign split remains `DEC-015` plus R0-C evidence |
| `FND-MAJ-024` | **CLOSED AS CONTRACT** | Engine 0.2 requires registry versioning, impact, regeneration, dependent rebuild, and tests |

#### D.3 Minor and Advisory series

| Old finding | v1.0 disposition | Exact current remainder / controlling gate |
|---|---|---|
| `FND-MIN-001` | **PARTIALLY CLOSED** | Stable IDs are retained here; source-inline IDs remain optional documentation work before source promotion |
| `FND-MIN-002` | **PARTIALLY CLOSED** | Current hashes/status are explicit; final approver/date/scope must enter Gate 0 manifest |
| `FND-MIN-003` | **PARTIALLY CLOSED** | Glossary updated here; generated registries control technical meanings at interface gates |
| `FND-MIN-004` | **PARTIALLY CLOSED** | Parent registers name evidence/gates; this document supplies owners/deferral consequences; actual assignments remain maintained data |
| `FND-MIN-005` | **DEFERRED TO EACH RECORD GATE** | Normal/min/max/invalid/transition/overflow examples remain required before record freeze |
| `FND-MIN-006` | **CLOSED AS REQUIREMENT; DEFERRED AS ARTIFACT TO R0-A** | Engine requires machine-readable status/ownership/diff-scope; actual artifact remains `RF-FND-003` |
| `FND-ADV-001` | **INFORMATIONAL ONLY** | Preserve clean-room separation if comparative research is ever used |
| `FND-ADV-002` | **ADOPTED AS SUPPORTING TOOLING DIRECTION** | Static call/path/owner checks may proceed under R0-A/Phase 1 scope; update for C/object/link symbols, not assembly-only names |
| `FND-ADV-003` | **INFORMATIONAL / CANDIDATE FOR R0-B** | External calibrated latency capture is preferred when software counters cannot prove end-to-end latency |
| `FND-ADV-004` | **CLOSED — adopted by Revision 1.5.1** | Reserves are unallocated/protected and require numbered decisions to consume |

### Appendix E — Historical decision and missing-requirement disposition

#### E.1 Old `DEC-001`–`DEC-015`

| Old decision | v1.0 disposition | Migration / current owner and gate |
|---|---|---|
| `DEC-001` Architecture corpus | **CLOSED / SUPERSEDED** | Revision 1.5.1 §1.2 is self-contained for architecture and hash-pins companions. Do not ask for missing Revision 1.4. Human approval status moved to `DEC-002`. |
| `DEC-002` Draft approvals | **STILL OPEN; REWORDED** | Decide Architecture 1.5.1 approval, Gameplay adoption record, and Engine 0.2 review/approval scope. Product + architecture; Gate 0. |
| `DEC-003` Platform matrix | **STILL OPEN** | Pin exact hardware/core/ROM/system/video/storage/input/Xemu support. Platform + product; R0-A. |
| `DEC-004` Snapshot design | **PARTIALLY RESOLVED / MIGRATED TO MEASUREMENT** | Architecture fixes extracted-buffer semantics; byte count, buffer count, location and cost are `MEM-02` at R0-D–F. No current preselection decision. |
| `DEC-005` Display candidate/quality floor | **STILL OPEN; EXPANDED** | Includes display mode/tier/RRB and optional affine-ground candidate. Architecture/graphics/platform/product; R0-B–F. |
| `DEC-006` F-117A identity | **DEFERRED / INFORMATIONAL** | Needed only before a comparative claim. Product/acceptance/legal; no R0/Phase 1 consequence. |
| `DEC-007` Countermeasure/RIO failure control | **STILL OPEN** | Product; before Phase 3 defense/input freeze. |
| `DEC-008` Midnight Spear | **PARTIALLY RESOLVED; CONTENT OPEN** | Separation from Technical Combat Slice is closed; product/creative manifest remains before Midnight Spear. |
| `DEC-009` Flight-feel authority | **STILL OPEN** | Product owner/reviewer rubric before Phase 2 tuning acceptance. |
| `DEC-010` Campaign/endings | **STILL OPEN** | Product/creative; before Phase 4–5 content. |
| `DEC-011` Audio/voice scope | **PARTIALLY RESOLVED; CONTENT OPEN** | Hybrid SID/PCM/text fallback is architectural; final sample vocabulary/content remains after R0 measurements. |
| `DEC-012` Save medium/recovery UX | **PARTIALLY RESOLVED; PRODUCT CHOICE OPEN** | Two-generation transaction is defined; medium and player recovery remain before R0-C/content lock. |
| `DEC-013` Controls/digital shaping | **STILL OPEN** | Product/accessibility; R0-B/Phase 2. |
| `DEC-014` Absolute quality thresholds | **STILL OPEN, PER CONSUMING GATE** | Product/acceptance; F-65 evidence first, no F-117A dependency. |
| `DEC-015` MVP D81 content boundary | **STILL OPEN** | Product + architecture; after R0-C/Midnight Spear evidence and before package/content lock. |

#### E.2 Old `GAP-001`–`GAP-035`

| Old gap | v1.0 disposition | Current remainder / gate |
|---|---|---|
| `GAP-001` architecture corpus | **CLOSED** | Revision 1.5.1 self-contained/hash-pinned architecture model |
| `GAP-002` snapshot schema/lifetime | **PARTIALLY CLOSED** | Semantics fixed; bytes/count/location/cost at R0-D–F (`MR-005`) |
| `GAP-003` public ABI | **PARTIALLY CLOSED** | Canonical generated registry required; R0-A subset then each consumer (`MR-004/011`) |
| `GAP-004` numeric formats/transforms | **PARTIALLY CLOSED** | Registry requirements explicit; values Phase 1–3 (`MR-011–013`) |
| `GAP-005` input/defaults | **PARTIALLY CLOSED** | Frame/edge semantics explicit; bindings/shaping R0-B/Phase 2 (`DEC-013`) |
| `GAP-006` platform ABI | **PARTIALLY CLOSED** | Invariant/ownership explicit; exact compiler/hardware ABI R0-A (`MR-003/004`) |
| `GAP-007` event fan-out | **PARTIALLY CLOSED** | Static proof/fault requirements explicit; evidence R0-E/Phase 1 (`MR-010`) |
| `GAP-008` disk/package/save | **PARTIALLY CLOSED** | Architecture/format/transaction explicit; medium/fit/UX/evidence R0-C (`MR-009`) |
| `GAP-009` reproducible toolchain | **PARTIALLY CLOSED** | Exact lock/build requirements explicit; actual verification R0-A (`MR-003`) |
| `GAP-010` Midnight Spear | **PARTIALLY CLOSED** | Distinction fixed; manifest remains Phase 4 (`MR-015`) |
| `GAP-011` flight/control coefficients | **DEFERRED TO PHASE 2** | `MR-012` |
| `GAP-012` radar/weapons/defense data | **DEFERRED TO PHASE 3** | `MR-013` |
| `GAP-013` AI/RIO doctrine | **DEFERRED TO PHASE 4** | `MR-014` |
| `GAP-014` display mode/pixel format | **DEFERRED TO R0-B–F** | `MR-006` |
| `GAP-015` world/terrain formats | **PARTIALLY CLOSED** | Truth/presentation boundary explicit; dimensions/encodings/staging R0/Phase 1 (`MR-008`) |
| `GAP-016` collision/contact tolerances | **DEFERRED TO PHASE 2–3** | `MR-012/013` |
| `GAP-017` radar display cadence | **CLOSED AS SEPARATION; VALUES DEFERRED** | Sensor/display independence explicit; exact schedules Phase 3/R0 display |
| `GAP-018` audio plan | **PARTIALLY CLOSED** | Priority/fallback architecture explicit; rates/cache/content R0 (`DEC-011`) |
| `GAP-019` asset inventory | **CLOSED AS CONTRACT; DATA DEFERRED** | Actual inventory/provenance at slice/content (`MR-017`) |
| `GAP-020` replay/checksum | **CLOSED AS CONTRACT; IMPLEMENTATION DEFERRED** | Exact generated schema/algorithm/evidence Phase 1 (`MR-011`) |
| `GAP-021` fault behavior | **CLOSED AS CONTRACT; CATALOG DEFERRED** | Fault catalog/one-over evidence Phase 1 (`MR-010`) |
| `GAP-022` save/campaign migration | **PARTIALLY CLOSED** | Versioned chunks/migration rules exist conceptually; exact campaign schema Phase 4–5 |
| `GAP-023` tutorial restart | **PARTIALLY CLOSED** | New deterministic run fixed; campaign/reward/save effects before Phase 4 |
| `GAP-024` damaged RIO/countermeasure fallback | **STILL OPEN** | `DEC-007`, Phase 3 |
| `GAP-025` view controls/transitions | **PARTIALLY CLOSED** | Supported views explicit; exact bindings/layout R0-B/Phase 1–2 |
| `GAP-026` operations/endings | **DEFERRED TO PHASE 4–5** | `MR-016` |
| `GAP-027` F-117A identity | **INFORMATIONAL ONLY** | `DEC-006` before a claim, no project gate |
| `GAP-028` physical MEGA65 support | **STILL OPEN / R0-A** | `DEC-003`, `MR-002` |
| `GAP-029` load/transition targets | **PARTIALLY CLOSED** | Hardware measurement required; thresholds/medium at R0-C and release (`MR-009/018`) |
| `GAP-030` accessibility acceptance | **STILL OPEN / HUMAN GATED** | `DEC-013/014`, R0-B/slice/release |
| `GAP-031` mission compiler proof algorithm | **CLOSED AS CONTRACT** | Finite bounded graph/may-live/witness requirements explicit; implementation staged R0-A→Phase 4 |
| `GAP-032` degraded rendering visibility | **PARTIALLY CLOSED** | Shedding order fixed; mandatory cue/clarity floors remain `DEC-014`/R0-B |
| `GAP-033` terminology | **PARTIALLY CLOSED** | This document controls orientation; generated registries and Gameplay editorial correction remain |
| `GAP-034` module/file ownership | **CLOSED AS REQUIREMENT; ARTIFACT DUE R0-A** | Engine §16 status/ownership/diff-scope; actual paths/reports are `RF-FND-003` |
| `GAP-035` decision ownership/gates | **PARTIALLY CLOSED** | This document supplies current owners/gates; maintain machine-readable status as project data |

### Appendix F — Current risk register

Likelihood (`L`) and impact (`I`) are planning scores from 1–5. Exposure is `L×I`; evidence must rescore it.

| ID | Risk | L | I | Exposure | Mitigation | Owner / closure gate |
|---|---|---:|---:|---:|---|---|
| `RSK-101` | Candidate text is mistaken for approved production authority | 4 | 5 | 20 | Exact status/hash manifest, release-label guard, task admission | Config + product/architecture / Gate 0 |
| `RSK-102` | LLVM-MOS/45GS02 ABI, stack, runtime or object flow differs from assumption | 4 | 5 | 20 | Real probes, hostile-state wrapper tests, retained maps/listings, conservative fallbacks | Tooling/platform / R0-A |
| `RSK-103` | Xemu behavior masks a physical MAP/DMA/IRQ/video/audio/input/storage difference | 4 | 5 | 20 | Pin both identities; never substitute evidence tiers; hardware phase/fault tests | Platform/test / every R0 hardware gate |
| `RSK-104` | Snapshot payload/count/copy cost breaks memory/timing under renderer lag | 4 | 5 | 20 | Generated ledger, forced lag, skipped publication, phase sweep, reserve | Core/Graphics / R0-D–F |
| `RSK-105` | Renderer candidate fails clarity or 20 Hz floor under protected load | 4 | 5 | 20 | Same-scene candidates, complete-buffer rule, fixed shedding, human clarity rubric | Graphics/product/platform / R0-B–F |
| `RSK-106` | White-paper path becomes an unowned parallel renderer/resource architecture | 3 | 5 | 15 | Treat as explicit R0 candidate only; use same services, ledger, scene, evidence and `DEC-005` | Architecture/graphics / R0-B |
| `RSK-107` | Generated records, runtime support, stacks, faults/events exceed fixed ledgers | 4 | 5 | 20 | One owner ledger, compile/link assertions, producer fan-out, one-over fixtures | Architecture/Core / R0-A–E/Phase 1 |
| `RSK-108` | Attic/tile staging or DMA blocks protected services | 4 | 5 | 20 | Sole services, bounded resident set, normalized jobs, measured blocking and phase admission | Resource/platform / R0-C–F |
| `RSK-109` | AI agents invent later tables/content to keep implementation moving | 5 | 5 | 25 | Gate-aware tasks, `NOT_APPLICABLE_UNTIL_GATE`, stop/escalate, non-shipping fixtures | TPM/product/architecture / every Phase 2–5 entrance |
| `RSK-110` | Final assets/audio/D81/save scope invalidates proxy-era budgets | 4 | 4 | 16 | Budget-valid proxies, rejecting converters, early representative finals, aggregate manifests | Art/audio/product/architecture / slice/content lock |
| `RSK-111` | Human quality/feel decisions arrive after interfaces/content harden | 4 | 4 | 16 | `DEC-009/013/014` owners and gate deadlines; preserve reversible work only | Product/TPM / R0-B, Phase 2, slice |
| `RSK-112` | MVP/campaign/save medium is decided too late for packaging | 4 | 4 | 16 | R0-C storage proof, `DEC-012/015`, content/D81 manifest before lock | Product/storage/architecture / R0-C/content lock |

### Appendix G — v0.2 readiness-deficit migration

This table disposes the major subsystem deficits that supported the old approximately 1.5/5 full-game score. The current §18 scorecard replaces that number.

| v0.2 scorecard area | v1.0 disposition |
|---|---|
| Authority/configuration | Missing-Revision-1.4 defect **closed**; candidate approvals and manifest remain Gate 0 |
| Scheduler/determinism | Timing and pause contradictions **closed**; target/hardware proof remains R0/Phase 1 |
| Memory/MAP/DMA/base page | Ownership/ABI contract **substantially closed**; compiler/platform evidence and measured snapshot/event costs remain |
| Toolchain/generated interfaces | Assembly-first deficit **superseded**; LLVM-MOS/C/Java/platform generators and R0-A artifacts now clearly specified |
| Input/controls | Command/edge semantics **substantially closed**; exact bindings/shaping remain R0/human gated |
| Rendering/display | Still R0-GATED by design; white-paper alternative explicitly controlled rather than silently chosen |
| Flight/actuators | Architecture/interface path coherent; coefficients, precision and feel remain proper Phase 2 gaps |
| Aircraft systems/damage | State/dependency structure coherent; exact tables/transitions remain Phase 2–3 |
| Radar/RWR/tracks | Truth/observation/track/display separation **closed**; numeric tables/cadences remain Phase 3 |
| Weapons/collision/damage | Model/event/lifecycle contracts coherent; tables/fan-out/evidence remain Phase 1/3 |
| AI/RIO/wingman | Knowledge boundary and module strategy coherent; doctrine/product behavior remains Phase 4 |
| Missions/campaign | Compiler/Technical Slice separation **closed**; authored Midnight Spear/campaign data remains Phase 4–5 |
| Audio | Ownership/priority/fallback **closed**; measured rates/cache/latency and content remain R0/later human gate |
| Storage/packages/save | Format/residency/transaction **closed as contract**; medium/UX/fit/hardware evidence remains R0-C |
| Assets/conversion | Bounded manifest/converter contract **closed**; actual inventory/provenance remains content gated |
| Replay/diagnostics/acceptance | Canonical/evidence contracts **substantially closed**; generated schemas and actual evidence remain Phase 1 onward |

### Appendix H — Controlled terminology

| Term | Meaning |
|---|---|
| Active tick / `SimulationTick` | One completed 10 ms authoritative step during `ACTIVE_SORTIE`; paused wall time does not advance it |
| Architecture-freeze candidate | Architecture proposed for approval; not Frozen until the approval record says so |
| Authoritative state | State that can affect future simulation, mission/campaign outcome, player capability, or canonical checksum |
| C-primary | LLVM-MOS C is the default target implementation; selective assembly remains first-class under admission rules |
| Candidate normative | Intended to become binding within its authority if approved; not currently self-approving |
| Closure gate | Latest milestone at which a finding/decision must close before dependent acceptance/work proceeds |
| Codex Engineering Harness | Host/generator/validator/oracle/evidence/build infrastructure; not a playable game or authority source |
| Complete buffer | A world/presentation store whose required work/DMA completed and which is eligible for display; partial stores never display |
| Engine candidate | Subordinate implementation design that cannot create architecture merely by using `MUST` |
| Evidence identity | Exact specification, source, build, toolchain, platform, package, fixture, environment and test identity |
| Human decision | Material product, creative, architecture, scope, resource, platform, or acceptance choice made by the named human owner |
| Low-level target code | Handwritten 45GS02 assembly or platform-specific wrapper admitted by architecture/platform need or measured evidence |
| Measured-limits revision | Approved post-R0 source that freezes hardware-derived budgets, modes, counts, cadences, latencies and reserve |
| Midnight Spear | Separately authored product mission; never a synonym for the Technical Combat Slice |
| MVP D81 | Independently bootable minimum product disk whose exact content remains `DEC-015`; not R0-A or the Technical Slice by default |
| Planning assumption | Reversible proof/estimate value without production authority |
| PresentationSnapshot | Bounded versioned extraction acquired by presentation; authoritative state is never exposed directly |
| R0-A | Non-gameplay platform/toolchain/memory/mixed-language proof |
| Supporting technical reference | Research that may support an experiment but cannot override product or architecture |
| Technical Combat Slice | Non-narrative Phase 4 integration proof distinct from Midnight Spear and release MVP |
| Worst phase | Relative alignment of simulation, raster/display, IRQ, DMA/audio, input and work release that maximizes the relevant cost/latency |

### Appendix I — Change-impact navigation

No production repository/code was supplied or modified. When approved requirements eventually drive work, use this navigation rather than assuming filenames:

| Change class | Likely owners/artifacts | Required evidence impact |
|---|---|---|
| Approval/hash/status | Specification-set manifest, release label, evidence index | Corpus/status validation; no Draft mislabeled approved |
| Compiler/platform ABI | Platform wrappers, C declarations, low-level routines, toolchain lock | ABI probes, stack/clobber/MAP/base-page/IRQ/Q restoration, Xemu + hardware |
| Snapshot measured limit | Core, PresentationExtractor, Graphics/Audio consumers, memory ledger | Generated bytes/location, lag tests, extraction cycles, phase sweep |
| Renderer candidate | Graphics, asset converters, resource staging, display/platform layer | Same-scene cycles/bytes/DMA/latency/clarity/reserve/hardware captures |
| Public interface/numeric change | Canonical registries, C/Java/low-level bindings, all consumers | Version/impact report, regeneration, asserts, golden vectors, dependent rebuild |
| Memory/pool/event change | Owner ledger, linker report, mission analyzer, Core/producers | Static fan-out/capacity, one-over faults, combined high-water, reserve approval |
| Gameplay table/feel change | Java oracle, target module, scenario corpus, product rubric | Human approval, high-precision/bit-exact evidence, hardware/playtest as named |
| Mission/campaign/content | JSON5 source, compiler/package, assets, saves/debrief | Capacity witness, branch replay, D81/residency fit, creative acceptance |
| Storage/save change | Package/save schema, ResourceManager, StorageService, D81 manifest | Compatibility/migration, physical media fault matrix, prior-generation retention |

### Appendix J — Non-closed historical-item control crosswalk

Every historical item not semantically closed maps to a current control row below. This crosswalk supplies the owner, closure gate, present blocking scope, permitted independent work, and consequence of deferral without carrying the old finding forward as a duplicate requirement.

| Current control | Historical IDs covered | Exact remaining issue / authority | Owner / closure gate | Blocks authorized R0 construction? | Independent reversible AI work? | Consequence of deferral |
|---|---|---|---|---|---|---|
| Gate 0 status | `CORR-AUTH-002`, `CON-002`, `FND-BLK-002`, `DEC-002` | Architecture §1.2 and Engine §0 define precedence but the human approval record is absent | Product + architecture + config / Gate 0, before formal R0-A acceptance | No construction; yes formal acceptance/production | Yes, labeled candidate/proof work | No artifact may be represented as conforming to an approved current set |
| Snapshot measurement | `CORR-SNAP-001`, `CON-006`, `FND-BLK-003`, `DEC-004`, `GAP-002` | Architecture §3.9 fixes semantics; Engine `MEM-02` leaves bytes/count/location/cost measured | Core + Graphics + memory / R0-D–F and measured limits | No | Yes, proof schemas/lag harness without frozen size | Phase 1 cannot safely allocate or integrate presentation |
| Public interface registry | `CORR-IFACE-001`, `CON-007`, `FND-CRT-003`, `GAP-003`, `FND-MIN-005` | Architecture §10.4/Engine §14 require one generated source; exact later layouts/examples remain | Architecture + consuming module / R0-A subset, then before each consumer | No; use versioned proof subsets | Yes, only approved logical fields | Consumers otherwise create incompatible layouts or adapters |
| Numeric registry | `CORR-NUM-001`, `FND-CRT-004`, `GAP-004` | Architecture §4.5 fixes required metadata; exact formats/tables remain phase-gated | Architecture + model owner / before Phase 1–3 consumers | No | Yes, schema/oracle infrastructure | Physics/sensors/weapons could disagree or drift |
| Input mechanics and feel | `CORR-INPUT-001`, `FND-CRT-005`, `DEC-013`, `GAP-005`, `GAP-025` | Architecture §7/Engine §11 define semantic/edge rules; bindings/shaping/views remain R0/human | Input + product/accessibility / R0-A subset, R0-B/Phase 1, Phase 2 feel | No; R0 proof profiles remain provisional | Yes, registry/probes without final defaults | Input integration or human feel acceptance cannot close |
| Fault/event bounds | `CORR-FAULT-001`, `FND-CRT-010`, `FND-MAJ-003`, `GAP-007`, `GAP-021` | Architecture §§3.10, 12.6 require faults; exact producer fan-out/catalog/UX remain | Core + every producer; product for UX / R0-E–Phase 1, UX before release | No | Yes, fault schema/one-over fixtures | Legal load may overflow differently or faulted sorties may save/recover incorrectly |
| Platform ABI | `CORR-PLAT-001`, `FND-CRT-007`, `GAP-006` | Architecture §§1.6, 2 and Engine §2.5 define boundary; exact compiler/hardware behavior unverified | Platform + toolchain / R0-A | No; proving it is authorized | Yes, probes/wrappers within R0-A | Formal R0-A cannot pass; target state could corrupt |
| Memory proof | `CORR-MEM-001`, `FND-MAJ-004` | Architecture §5.4/Engine §4 require generated owner proof; real layouts/runtime/stack charges absent | Architecture/Core/tooling / R0-A–E and Phase 1 | No; provisional ledgers/fixtures are authorized | Yes | Late growth may consume another owner or reserve |
| Toolchain/bootstrap | `CORR-TOOL-001`, `FND-CRT-002`, `FND-MIN-006`, `GAP-009`, `GAP-034` | Architecture §11/Engine §§14.4, 21 require real lock/artifacts; reviewed paths do not yet exist | Tooling/config / R0-A | No; producing them is authorized | Yes, this is authorized work | R0-A identity/build/status evidence cannot close |
| Storage/save/media | `CORR-STORE-001`, `FND-CRT-008`, `FND-MAJ-022`, `DEC-012`, `GAP-008`, `GAP-022`, `GAP-029` | Architecture §12.2/Engine §13.5 define transaction; medium, post-ROM path, UX, limits remain | Storage/platform/product / R0-C, campaign/content lock | No | Yes, proof D81 and format/fault fixtures | Physical load/save/recovery and content packaging remain unqualified |
| Asset inventory | `FND-MAJ-008`, `GAP-019` | Architecture §12.1/Engine §14.1 define manifest; actual final assets/provenance remain | Art/audio + architecture / slice and content lock | No | Yes, schemas and budget-valid proxies | Final assets may break RAM/D81/timing/readability |
| Renderer/display | `FND-MAJ-006`, `FND-MAJ-007`, `DEC-005`, `GAP-014`, `GAP-032` | Architecture §6/Engine §§5, 8 plus white-paper disposition leave candidate/mode/clarity measured | Graphics/platform/product/art / R0-B–F and measured limits | No | Yes, admitted proof candidates under `AD-001` | Production mode/tier/assets/quality cannot freeze |
| Audio measured/content plan | `CORR-AUDIO-001`, `FND-MAJ-010`, `DEC-011`, `GAP-018` | Architecture §12.5/Engine §12 fix priority/fallback; rates/cache/channels/content remain | Audio/product/platform / R0-B–F, representative content lock | No | Yes, proxy tones/samples and instrumentation | Essential latency or content fit cannot be accepted |
| Flight/carrier/feel | `FND-CRT-009`, `FND-MAJ-014`, `FND-MAJ-015`, `DEC-009`, `GAP-011`, `GAP-016` | Gameplay §19/Engine §18 intentionally gate coefficients/contact/feel | Product/flight + architecture / Phase 2 | No | Yes, oracle/schema infrastructure | Shipping flight/contact behavior and slice handling cannot freeze |
| Radar/weapons/defense | `FND-MAJ-013`, `DEC-007`, `GAP-012`, `GAP-017`, `GAP-024` | Gameplay §§10–12, 19 gate tables and damaged-RIO agency; semantic cadence separation already fixed | Product/combat + architecture / Phase 3 | No | Yes, scenario harnesses/schemas | Combat outcomes or player defensive agency would be invented |
| AI doctrine | `GAP-013` | Gameplay §19/Engine §18 gate doctrine/cadence/weights | Product + AI / Phase 4 | No | Yes, trace harness/blackboard schema | AI behavior cannot be accepted or tuned legitimately |
| Restart/campaign transaction | `FND-MAJ-016`, `GAP-023` | Gameplay fixes new-run retry; exact seed/reward/save/debrief mutation remains | Product + Mission/Storage / before Technical Slice restart and Phase 4 campaign | No | Yes, state-machine fixtures without reward choice | Replays/rewards/saves may diverge or duplicate |
| Terrain/query format | `FND-MAJ-018`, `GAP-015` | Engine §6 separates authoritative queries from render LOD; exact encoding/dimensions/staging remain | World/Resource/Graphics + architecture / R0-C–F and Phase 1 | No | Yes, schema/candidate resources | Flight, radar, contact and graphics could use different terrain |
| Hardware support/evidence matrix | `FND-MAJ-019`, `FND-MAJ-020`, `DEC-003`, `GAP-028` | Architecture §11 requires identity; exact supported matrix remains | Platform + product/test / R0-A and each hardware gate | No; blocks formal hardware closure | Yes, diagnostics/probes | Results remain non-authoritative or fail on unsupported configurations |
| Midnight Spear | `DEC-008`, `GAP-010` | Architecture §12.3 separates it from Technical Slice; product manifest absent | Product/creative / Phase 4 after Technical Slice | No | Yes, non-narrative fixtures only | Named mission cannot be implemented/accepted |
| Campaign/endings/MVP | `FND-MAJ-002`, `FND-MAJ-023`, `DEC-010`, `DEC-015`, `GAP-026` | Architecture/Game scope fixed; authored operations/endings/MVP boundary absent | Product/creative + architecture / Phase 4–5/content lock | No | Yes, schemas/compilers/non-shipping fixtures | Campaign, D81 split, saves and release boundary cannot close |
| Quality/accessibility | `FND-MAJ-009`, `DEC-014`, `GAP-030` | Parent behavior exists; absolute readability/usability/latency/experience floors remain human-owned | Product/accessibility/acceptance / R0-B, slice, release | No | Yes, instrumentation and test-rubric scaffolds | The affected quality gate cannot pass |
| Configuration terminology | `FND-MIN-001`, `FND-MIN-002`, `FND-MIN-003`, `FND-MIN-004`, `GAP-033`, `GAP-035` | This Read-First supplies IDs/status/glossary/owners; source-inline and machine-readable maintenance remains | Configuration control + owning reviewers / source promotion and each consumer | No | Yes, mechanical updates after semantics | Stale references/status may misdirect tasks but do not authorize behavior |
| F-117A comparison | `DEC-006`, `GAP-027` | Architecture §19 rejects it as product requirement | Product/acceptance/legal / before comparative claim only | No | Yes, none required for early project | Only the comparative claim remains unavailable |

## 22. Revision History

| Version | Date | Status | Change |
|---|---|---|---|
| 0.1 | 2026-08-17 | Historical Draft | Initial audit/correction layer over Revision 1.4.1, Gameplay 0.2, and Engine 0.1 |
| 0.2 | 2026-08-17 | Historical Draft | Added milestone-aware verdict and authorized-work calibration; remained assembly-first |
| 1.0 | 2026-08-20 | Final Draft | Fresh audit against Revision 1.5.1, Engine 0.2, Gameplay 0.2, Technical Alignment v0.2, and Graphics White Paper 1.0; amended before approval to incorporate proposed `AD-001` and separate development authorization from gate passage |
| 1.0 | 2026-08-20 | **APPROVED — FIRST-READ AUTHORITY** | Human approval recorded against Final Draft SHA-256 `2eb72648…56b3f`; `AD-001` separately activated R0-A–F proof-development authority; mechanical status metadata added with no semantic expansion |

Approval date, human approval identity, approved-draft SHA-256, scope, and exclusions are recorded in `F-65_Specification_Approval_Record_2026-08-20_R0_Development.md`. Later semantic changes require a new revision and approval record.

---

**End of F-65 Technical Alignment and Read-First Supplement v1.0 — APPROVED — FIRST-READ AUTHORITY**
