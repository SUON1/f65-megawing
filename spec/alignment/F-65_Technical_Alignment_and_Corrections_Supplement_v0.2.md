# F-65 Technical Alignment and Corrections Supplement

## 1. Document Control

| Field | Value |
|---|---|
| Title | F-65 Technical Alignment and Corrections Supplement |
| Version | 0.2 |
| Status | **DRAFT — REQUIRES HUMAN REVIEW** |
| Date | 2026-08-17 |
| Authoring role | Critical Technical Program Manager and systems-design auditor |
| Intended filename | `F-65_Technical_Alignment_and_Corrections_Supplement_v0.2.md` |
| Change model | Controlled correction layer; source documents are not silently rewritten |
| Release effect | None until the required human approvals are recorded |

### 1.1 Documents reviewed

All three supplied documents were read in full. File hashes identify the exact review inputs; descriptive titles alone are not sufficient version control.

| Short name | Reviewed document and declared status | SHA-256 |
|---|---|---|
| Architecture | *F-65 Megawing Revision 1.4.1 — Architecture Invariants and Documentation Update*; Frozen architecture baseline | `c54f77c817b8263f8d03de3ed442c115ff06b0b622c1f14be122df8963079922` |
| Gameplay | *F-65 Megawing — Gameplay and Simulation Requirements Supplement*, Draft 0.2; Freeze candidate | `5db0344f8e7fd66143874310c3794a64391d4767229a90f5caee5e5e287d84e4` |
| Engine | *F-65 Megawing — Engine, Runtime, and Toolchain Design Supplement*, Draft 0.1; Architecture-review candidate | `63f0d2e136507485296bd3424e83e9db796b2bf612d81f3fe5ac2744297d27aa` |

Revision 1.4, which Revision 1.4.1 says it supersedes and completely retains, was not supplied. No referenced generated schemas, interface artifacts, R0 evidence bundles, mission packages, asset manifests, or diagrams were present in the review workspace.

### 1.2 Required approvers

Approval is proportional to materiality:

- **Individual approval** is required for corrections or decisions that change architecture, product behavior, scope, creative direction, platform support, resource limits, failure behavior, or acceptance thresholds.
- **Delegated batch approval** is permitted for mechanically verifiable documentation repairs, generated cross-references, and Minor/Advisory findings that do not change semantics. Each affected ID still records its disposition for traceability.
- Document-level approval follows closure of the Blockers and Critical findings required by the document’s intended authority. Silence is never approval.

The findings register is evidence and planning input, not the daily work queue. A finding blocks only the milestone named in its `Required closure gate` field.

| Role | Required approval scope |
|---|---|
| Product/creative owner | Player experience, campaign, benchmark intent, controls, scope, and all creative decisions |
| Architecture owner/technical lead | Authority hierarchy, runtime contracts, memory, timing, interfaces, and development gates |
| MEGA65 platform reviewer | Hardware facts, core/ROM identity, VIC-IV, DMAgic, audio, MAP, storage, and hardware evidence |
| Test/acceptance owner | Acceptance thresholds, evidence retention, release gates, and reference-machine configuration |
| Art/audio owner | Asset envelopes and quality bars; may be delegated after envelopes are approved |

### 1.3 Revision history

| Version | Date | Status | Change |
|---|---|---|---|
| 0.1 | 2026-08-17 | Draft — requires human review | Initial three-document audit, correction register, contracts, acceptance criteria, traceability, risks, and remediation plan |
| 0.2 | 2026-08-17 | Draft — requires human review | Calibrated the verdict by work horizon; added Authorized Work Now and milestone closure fields; reclassified phase-owned gaps; streamlined approval; made the F-117A benchmark non-blocking before representative release evaluation |

---

## 2. Purpose and Reading Order

> **Read this supplement before F-65 Revision 1.4.1, F-65 Gameplay, or F-65 Engine. It identifies corrections, precedence decisions, unresolved questions, and implementation constraints affecting those documents. A correction marked “Proposed” is not authoritative until human approval is recorded.**

This supplement is the controlled orientation and correction layer for the F-65 specification set. It does not reproduce the three sources and does not change them while its status is Draft. It distinguishes supported requirements, technical corrections, proposals, assumptions, unresolved product choices, and material that cannot yet drive implementation.

While its status is Draft, this document is a high-signal diagnostic and prioritization tool—not a new architectural parent. If it is later approved, only its explicitly approved, scoped corrections gain precedence; the existence or length of the register does not itself create a requirement or stop-work order.

> **The specification set is not ready for autonomous full-game production. It is ready for the explicitly bounded pre-R0 and R0-A work already authorized by Revision 1.4.1. Findings block only the milestone named in their closure gate.**

### 2.1 Required reading sequence

1. Read this correction supplement.
2. Review unresolved decisions and approval status.
3. Consult the applicable source sections.
4. Follow approved corrections where conflicts exist.
5. Trace the requirement to its interface, implementation task, and acceptance test.
6. Stop and escalate if a material contradiction remains unresolved.

### 2.2 Use by humans and AI engineers

- Humans review §4, §6, §7, and §15 first. Material corrections receive individual approval; mechanical and Minor/Advisory dispositions may be approved in delegated batches.
- AI engineers begin with §13 and §16, then follow the requirement inventory and traceability matrix in Appendix A.
- An implementation task is ready only when its governing requirement, interface, limits, data or assets, and deterministic acceptance method are all identified.
- `Confirmed` means the source documents already agree. It does not mean a draft source has been approved.
- `Technical correction` means the proposal follows from a cited platform fact or arithmetic. It still requires incorporation approval because it changes the project specification.
- `Planning assumption` permits estimation or prototype planning only. It cannot define release behavior.
- A correction marked `Proposed` must not be implemented as if approved.
- A proposed contract may be exercised in an explicitly authorized non-shipping proof or generator skeleton when its Draft identity and closure gate are recorded; successful proof evidence does not approve the contract or create shipping behavior.

### 2.3 Navigation for the mandated audit outputs

| Requested output | Location |
|---|---|
| Executive verdict, authority/version assessment, AI-readiness scorecard, critical findings | §§3–4 |
| Complete findings register | Appendix B |
| Cross-document traceability matrix and requirement inventory | Appendix A |
| MEGA65 feasibility assessment | §9 |
| F-117A benchmark matrix | §12 |
| Insertion-ready document corrections | §6 |
| Vertical slice | §14.2 |
| Prioritized remediation plan | §14 |
| Human decisions | §15 |
| Final readiness checklist | §16 |

---

## 3. Authority and Precedence Rules

### 3.1 Current authority assessment

The source set declares this hierarchy:

1. Revision 1.4.1 is the frozen architecture authority.
2. Gameplay Draft 0.2 becomes the player-facing authority only once approved.
3. Engine Draft 0.1 is subordinate to both and is only an architecture-review candidate.

That hierarchy is coherent in principle but incomplete in practice. Revision 1.4.1 describes itself as a documentation-only update that “retains the complete Revision 1.4 product and architecture,” yet Revision 1.4 was not supplied. Gameplay and Engine are not approved, while Engine depends on Gameplay. Therefore the three reviewed files do not yet form an approved, self-contained production baseline.

### 3.2 Precedence after this supplement is approved

When this document becomes **APPROVED — FIRST-READ AUTHORITY**, apply the following order narrowly, not globally:

1. An explicit `Approved` correction in this supplement governs only the passages, requirements, systems, and dependencies it names.
2. Uncorrected architecture requirements remain governed by Revision 1.4.1 and any supplied, hash-pinned material that it incorporates.
3. Uncorrected approved gameplay requirements remain governed by the approved Gameplay supplement.
4. Uncorrected approved implementation requirements remain governed by the approved Engine supplement.
5. A measured-limits revision may close an `R0-GATED` value only when it records test identity, hardware/core configuration, evidence, tolerance, and approver.
6. A later numbered and approved decision may supersede an earlier one only by naming the earlier requirement or correction ID.

`TARGET`, `TBD`, `R0-GATED`, examples, comments, host-model behavior, and current code cannot override a higher-level `MUST`. Code is evidence of an implementation, never evidence that an unresolved product choice has been approved.

### 3.3 Conflict protocol

An engineer who encounters a conflict must:

1. record the affected requirement IDs and exact source sections;
2. stop work on the behavior whose outcome would differ;
3. continue only independent, reversible work;
4. open or update a decision-log entry;
5. obtain the required human approval; and
6. update the correction, interface, task, and test trace together.

“Choose the parent,” “match the current code,” and “use the simplest behavior” are not valid resolutions when they change observable behavior, resource limits, determinism, or architecture.

### 3.4 External technical references

The Architecture document cites the [20 July 2026 MEGA65 Chipset Reference](https://files.mega65.org/files/m/mega65-chipset-reference_cnFcKB.pdf); the Engine document cites an older [3 April 2024 edition](https://files.mega65.org/files/m/mega65-chipset-reference_4hh2eE.pdf). The 2026 edition is the proposed technical-reference baseline, subject to the actual target core and ROM being pinned and tested. The [official documentation landing page](https://mega65.atlassian.net/wiki/spaces/MEGA65/pages/21331992/Documentation+-+Landing+Page) and [official file version list](https://files.mega65.org/php/readversionlistpublic.php) identify current publications, but mutable “latest” links must not replace recorded hashes in release evidence.

---

## 4. Executive Readiness Assessment

### 4.1 Verdict

**GO — proceed with documentation repair, host-side foundations, and the explicitly bounded pre-R0/R0-A work.**

**NO-GO — do not begin autonomous gameplay production or full-game implementation.** No gameplay assembly may merge until the source documents’ R0-F/measured-limits gate and every finding whose closure gate is at or before that work have been resolved.

> **The specification set is not ready for autonomous full-game production. It is ready for the explicitly bounded pre-R0 and R0-A work already authorized by Revision 1.4.1. Findings block only the milestone named in their closure gate.**

The concept is not rejected as technically infeasible. A 100 Hz deterministic flight-combat game with a software-rendered cockpit presentation is plausible on the MEGA65 if the measured display mode, renderer, DMA policy, and content envelopes satisfy R0. The current problem is that several load-bearing contracts either contradict physical timing, lack ownership/lifetime rules, depend on absent artifacts, or remain intentionally creative TBDs.

| Work horizon | Operational verdict | Governing condition |
|---|---|---|
| Documentation correction and host schema/oracle work | **GO** | Remains non-shipping and preserves explicit proposal/approval status |
| R0-A Memory Access ABI/platform proof | **GO** | Uses the bounded scope in §4.2; platform identity and evidence are recorded |
| R0-B–R0-F measurement work | **Conditional Go** | Prior R0 evidence and correction dependencies for each experiment are satisfied |
| Phase 1 integrated engine harness | **Conditional Go after R0-F** | Snapshot, event, interface, memory, timing, and platform contracts required by the harness are closed |
| Gameplay assembly and Technical Combat Slice | **No-Go now** | Source R0-F gate, Phase 1 gate, and slice-required product tables/controls must close first |
| Campaign/content production and release | **No-Go now** | Approved gameplay/engine baselines, campaign/assets, acceptance, and release gates required |

Severity is not a scheduling synonym. `Blocker` means the target outcome cannot be completed reliably if the issue remains; it does not prohibit independent work before the finding’s closure gate.

### 4.2 Authorized Work Now

The following work is authorized and should continue:

1. encode the physical-region, resident-code, allocation, and reserve ledgers in a generated schema;
2. define the initial machine-readable interfaces for `CoreRuntime`, `InputCommandFrame`, entity common headers, resource handles, and renderer proof records;
3. implement the interface generator and Java/assembly offset/size assertion path for that initial interface subset;
4. implement the machine-readable module status source, generated status board, ownership map, and diff-scope validator;
5. implement the JSON5 mission schema skeleton and conservative frozen-pool capacity analyzer using the Gameplay 0.2 combined-load case as its first non-shipping fixture;
6. pin the macOS KickAssembler/Java/Xemu toolchain and evidence identity, then prove a reproducible non-interactive build;
7. build the pure Memory Access ABI proof D81 with boot identity, symbols, listings, opcode/MAP/base-page/DMA/IRQ instrumentation, and hardware/Xemu evidence;
8. create non-shipping host models, golden-vector infrastructure, fault/evidence schemas, and synthetic fixtures needed by those tasks; and
9. repair documentation and maintain traceability without promoting unresolved product behavior.

This authorization does **not** include flight, radar, weapons, tactical AI, campaign, production-renderer, or shipping gameplay assembly. It does not authorize an agent to choose a shipping value for a `TBD`, `TARGET`, `R0-GATED`, creative, or unresolved semantic requirement.

### 4.3 Blockers and critical risks

| Priority | Finding and v0.2 severity | Consequence | Blocks current pre-R0/R0-A? | Required closure gate |
|---:|---|---|---|---|
| 1 | **FND-BLK-001 — Blocker:** incorporated Revision 1.4 corpus is absent | Preserved requirements cannot be proved complete | No independent proof work; blocks formal baseline/R0-A acceptance | Gate 0, before R0-A is accepted |
| 2 | **FND-BLK-003 — Blocker:** snapshot schema, storage, and lifetime are undefined | Integrated renderer can race, overwrite, stall, or exceed memory | No | Before snapshot/interface freeze and Phase 1 integration |
| 3 | **FND-CRT-001 — Critical:** exact six-frame/ten-tick assumption conflicts with hardware timing | Average ledger may approve a legal worst-phase deadline failure | The correction is needed by timing-harness design; measurements continue under corrected model | Correction before timing harness acceptance; numeric limits at R0-F |
| 4 | **FND-CRT-007 — Critical:** unified IRQ/DMA/MAP/Q/math platform ABI is absent | R0 proof may be emulator-specific, corrupt state, or miss deadlines | Yes—the R0-A work exists to close it | R0-A |

Current-milestone deliverable gaps such as the absent bootstrap artifacts and incomplete initial interface definitions remain important, but are classified as Major work to be completed **by** R0-A rather than reasons to stop R0-A.

### 4.4 Immediate human decisions

The first approval meeting should decide only the matters needed to control the current horizon:

1. whether Revision 1.4.1 will be declared a consolidated standalone baseline or Revision 1.4 will be supplied and hash-pinned (`DEC-001`);
2. whether Gameplay 0.2 and Engine 0.1 remain controlled living drafts until their consuming phases, with no shipping authority meanwhile (`DEC-002`);
3. the target hardware/core/ROM and PAL/NTSC support matrix (`DEC-003`);
4. approval of the independent-clock correction used by the R0 timing harness (`CORR-TIME-001`);
5. the R0-A evidence identity, delegated mechanical-review authority, and acceptance owner; and
6. the snapshot handoff architecture and maximum presentation-record size (`DEC-004`) early enough to close before Phase 1, without delaying independent R0-A work.

The F-117A identity, Midnight Spear creative definition, final controls, doctrine, and campaign content are not current-horizon decisions. They retain explicit later gates and must not delay R0-A.

The recommended next action is to record the current-horizon decisions, execute the authorized §4.2 work, and publish the R0-A evidence bundle. Later findings become blocking only when their closure gate is reached.

### 4.5 AI-readiness scorecard

Scores are 0–5: `0` absent or unusable, `1` concept only, `2` materially incomplete, `3` implementable prototype with decisions outstanding, `4` production-capable with local gaps, `5` approved and deterministically verifiable. “Feasibility” scores technical plausibility, not approval.

| Subsystem | Complete | Consistent | Feasible | Testable | Implementation ready | Principal deficit |
|---|---:|---:|---:|---:|---:|---|
| Authority and configuration control | 2 | 1 | 5 | 2 | 0 | Missing incorporated baseline; drafts not approved |
| Scheduler, determinism, tick order | 4 | 2 | 3 | 4 | 2 | Display/simulation phase math and pause semantics |
| Memory, MAP, DMA, base page | 4 | 3 | 4 | 4 | 3 | Snapshot/event storage and unified platform ABI |
| Toolchain and generated interfaces | 3 | 3 | 5 | 3 | 1 | Versions, commands, artifacts, CI evidence absent |
| Input and controls | 2 | 2 | 5 | 2 | 1 | Missing axes/actions, ranges, edge/hold behavior |
| Rendering and display | 3 | 4 | 3 | 4 | 2 | Mode/encoding/clear/overdraw not measured |
| Flight and actuators | 3 | 4 | 3 | 3 | 1 | Numeric formats and all feel coefficients TBD |
| Aircraft systems/damage | 3 | 4 | 4 | 3 | 2 | State encoding, transitions, and failure tables |
| Radar, RWR, tracks, identification | 3 | 3 | 4 | 3 | 2 | Exact cadence, quality schema, overflow presentation |
| Weapons, collision, damage | 3 | 3 | 4 | 3 | 2 | Guidance tables, event bounds, edge cases |
| Tactical AI/RIO/wingman | 3 | 4 | 4 | 3 | 2 | Doctrine data, schedule, damaged-RIO behavior |
| Missions and campaign | 2 | 4 | 4 | 2 | 1 | Vertical slice undefined; eight operations/endings TBD |
| Audio | 2 | 3 | 4 | 2 | 1 | Channel plan, sample envelope, latency evidence absent |
| Storage, packages, save/recovery | 2 | 3 | 4 | 2 | 1 | No disk layout, fit proof, transaction/failure contract |
| Assets and conversion | 2 | 4 | 4 | 2 | 1 | Formats named; inventory and per-class budgets absent |
| Replay, diagnostics, acceptance | 3 | 3 | 4 | 3 | 2 | Canonical serialization/checksum/evidence format absent |

The implementation-readiness column averages approximately **1.5/5 for full-game production**. It is a diagnostic, not a stop-work vote. The bounded R0-A work has a separate **GO** because it exists to create several missing proofs and artifacts; a finding becomes disqualifying only at its stated closure gate.

---

## 5. Corrected Project Baseline

This section states the coherent baseline that is either already confirmed by the sources or proposed for approval. Labels are normative.

### 5.1 Intended product and player experience

- **Confirmed:** F-65 is a retro-synthwave, cockpit-primary, single-player fleet-interceptor combat-flight simulation for MEGA65, with an inexpensive chase view.
- **Confirmed:** The aircraft is the fictional F-65A with two engines, ten missiles, cannon, fuel, electrical, hydraulic, radar, jammer, RWR, countermeasures, damage, an AI RIO, wingman, AIC, enemies, carrier/airfield operations, a vertical slice, ten operations, and two endings.
- **Confirmed:** Accessibility comes from four semantic control contexts and assisted automation without making the simulation consequence-free.
- **Confirmed:** Aviation-facing displays use nmi, knots, feet, pounds, pounds-force, pounds/hour, psi, and G; implementation units remain canonical SI/fixed-point values defined in the numeric registry.
- **Unresolved:** The current full product scope includes the ten-operation campaign and both endings, but the exact content boundary of the independently bootable **MVP D81** is not defined. The minimum engineering **vertical slice** is the smaller proof in §14.2 and must not be advertised as the release MVP unless the product owner explicitly chooses that boundary.
- **Unresolved:** Flight feel, digital-control shaping, campaign content after Operation 2, ending predicates, detailed doctrine, scoring, and asset/audio quality require human approval.

### 5.2 Platform and technical boundaries

- **Confirmed:** All production target game code is 45GS02 assembly. Java is permitted for host tools, compilers, reference models, test oracles, and asset conversion.
- **Confirmed:** The simulation is one deterministic 100 Hz fixed-step timeline with a frozen 21-stage update order. Physical entities do not use visibility-dependent or secondary integration clocks.
- **Confirmed:** Active authoritative state uses statically bounded pools in chip RAM. Attic RAM is cold/immutable during tactical use and must be staged for VIC-IV, SID/audio DMA, or other consumers that cannot address it.
- **Confirmed:** Only the Memory Access ABI owns MAP; base page begins at `$0200`; `$01=$35` remains canonical; no in-sortie code overlay or continuous tactical disk streaming is allowed.
- **Confirmed:** Rendering is software 3D without a Z-buffer, using deterministic presentation extraction, clipping/bucketing/painter-style ordering, and load shedding that never changes authoritative simulation.
- **Proposed technical correction:** Display cadence is asynchronous to 100 Hz. Budgets are expressed per simulation tick, per display service, and over enumerated worst-phase rolling windows; no document may assume an exact integer tick count per display-frame group unless the selected timing mode proves one.
- **Planning assumption:** Production MEGA65 hardware at 40.5 MHz with 384 KB chip RAM, 32 KB color RAM, and 8 MB Attic RAM is the initial target. This excludes configurations without the required Attic RAM until `DEC-003` says otherwise.

### 5.3 Quality benchmark

- **Proposed:** Absolute thresholds for responsiveness, frame consistency, readability, control latency, loading, stability, reliability, and task success are the primary quality requirements.
- **Deferred comparative target:** F-65 intends to exceed the experience of a selected F-117A comparison configuration in measurable categories, not by copying content or by claiming superiority without captures. This comparison is non-blocking for pre-R0, R0, and Phase 1.
- **Unresolved:** The benchmark title appears to be *F-117A Nighthawk: Stealth Fighter 2.0*, released for Amiga in 1993. Available catalog evidence identifies Amiga 500/2000, OCS/ECS, 1 MB, keyboard/mouse, and floppy as the minimum—not a native AGA/A1200 product. `DEC-006` must pin the exact disk revision, PAL/NTSC mode, A1200 configuration, and capture procedure before comparative claims are accepted. See §12.

### 5.4 Minimum viable game versus proof milestones

| Level | Purpose | Content status |
|---|---|---|
| R0-A | Prove toolchain, CPU/addressing/MAP/DMA/IRQ behavior, timing counters, display candidates, input, and hardware identity | Authorized by source baseline; no gameplay merge |
| R0-B–R0-F | Measure renderer, memory, audio/input latency, storage, and combined-load limits; publish measured-limits revision | Required before gameplay implementation |
| Phase 1 integrated harness | Prove all core engines together under deterministic synthetic peak load | Required architecture gate |
| Technical vertical slice | Prove player flight → radar → target → weapon → enemy reaction → outcome, with representative presentation | Proposed in §14.2; creative wrapper requires approval |
| Release MVP | Independently bootable D81 containing the approved minimum release experience | Confirmed product boundary; exact disk/package split unresolved |
| Full current scope | Ten operations and two endings, with multi-D81 campaign permitted | Confirmed scope; content incomplete |

### 5.5 Definition of “AI-ready” for this project

A subsystem is AI-ready only when all of the following are approved or mechanically generated from an approved source:

1. requirement IDs and priority;
2. authoritative owner of each mutable state field;
3. input/output records with byte layout, units, numeric format, range, rounding, and invalid values;
4. exact update stage and cadence;
5. memory and cycle budgets with measured evidence where gated;
6. queue/pool capacity and deterministic overflow/fault behavior;
7. asset or data schema and bounded inventory;
8. normal, boundary, fault, and replay examples;
9. host oracle or target acceptance test;
10. requirement → interface → module → test trace; and
11. human approval for product/creative choices.

Compilation, visual plausibility, or similarity to a host reference alone does not establish conformance.

---

## 6. Approved and Proposed Corrections Register

Every entry is initially `Proposed`. Replacement language is written for direct insertion into this supplement or the named source at its next controlled revision. Material corrections are approved individually. A delegated batch may change the disposition of multiple mechanical/Minor IDs, but its approval record must enumerate every included ID; it does not approve unrelated text.

The register is the traceability ledger, not the day-to-day work queue. Engineering work is scheduled from §4.2 and §14 using each finding’s closure gate.

### 6.1 Status legend and baseline disposition

| Disposition | Content in this Draft |
|---|---|
| Confirmed source requirements | 45GS02 assembly target; Java host tools; fixed 100 Hz active simulation and 21-stage order; static pools; memory/MAP invariants; presentation independence; R0 and Phase 1 gates; current ten-operation/two-ending product scope |
| Proposed technical corrections | `CORR-REF-001`, `CORR-TIME-001`, and the DMA/Attic consequences in `CORR-PLAT-001` |
| Other proposed corrections | Every other `CORR-*` row below; none is yet authoritative |
| Unresolved product/creative decisions | `DEC-006`–`DEC-015` as applicable, plus source flight/sensor/weapon/AI/carrier/campaign TBDs |
| Planning assumptions | Initial production-class 40.5 MHz/8 MB Attic target; 320×200×8-bit only as a display measurement candidate; extracted triple snapshot buffer as recommendation; proxy slice content |
| Proposed supersessions after approval | The exact six-NTSC-frame/ten-tick claim; Engine’s older unqualified chipset-reference citation; the claim that absent bootstrap files are “published”; ambiguous direct consumption of a full `SimulationSnapshot` where the approved `PresentationSnapshot` contract applies |
| Approval route | Individual for architecture/product/scope/creative/platform/resource/failure/acceptance semantics; delegated batch for mechanically verifiable documentation and generated-link repairs |
| Approved/rejected/deferred corrections | None at version 0.2 |
| Safe AI auto-remediation | Only entries explicitly marked “Yes” in the register, and only after their semantic/authority choice is approved |

| Correction | Status | Class | Principal destination | Auto-remediation after approval? |
|---|---|---|---|---|
| CORR-AUTH-001 | Proposed | Authority | Revision 1.4.1 front matter | Yes, if the incorporated corpus is supplied unchanged |
| CORR-AUTH-002 | Proposed | Authority | Gameplay §0; Engine §0 | No |
| CORR-REF-001 | Proposed | Technical correction | Architecture §2; Engine §§0, 18 | Yes |
| CORR-TIME-001 | Proposed | Technical correction | Architecture §§3.1, 6 | No |
| CORR-SNAP-001 | Proposed | Architecture | Architecture §3; Engine §§3, 4, 8, 14 | No |
| CORR-IFACE-001 | Proposed | Interface | Gameplay §18; Engine §14 | Yes for generation; no for semantic choices |
| CORR-NUM-001 | Proposed | Interface | Architecture §4; Engine §§6–7, 14 | No |
| CORR-INPUT-001 | Proposed | Missing requirement | Gameplay §5; Engine §11 | No |
| CORR-PAUSE-001 | Proposed | Contradiction | Gameplay §4; Architecture §3 | Yes |
| CORR-FAULT-001 | Proposed | Missing requirement | Architecture §§3, 5, 12; Engine §§3–5, 13, 15 | No |
| CORR-PLAT-001 | Proposed | Technical/interface | Architecture §2; Engine §§3–5 | No |
| CORR-MEM-001 | Proposed | Feasibility/interface | Architecture §§2, 5; Engine §4 | No |
| CORR-STORE-001 | Proposed | Missing requirement | Architecture §12; Gameplay §4; Engine §13 | No |
| CORR-TOOL-001 | Proposed | Missing requirement | Engine §§14, 17, 21 | Yes for manifest scaffolding |
| CORR-ASSET-001 | Proposed | Missing requirement | Engine §§8, 12, 14 | No |
| CORR-MISSION-001 | Proposed | Scope/testability | Architecture §§1, 15; Gameplay §16 | No |
| CORR-CAMP-001 | Proposed | Creative/scope | Gameplay §16 | No |
| CORR-RADAR-001 | Proposed | Interface/testability | Gameplay §§10, 18; Engine §9 | No |
| CORR-AUDIO-001 | Proposed | Feasibility/interface | Engine §12 | No |
| CORR-REPLAY-001 | Proposed | Testability | Architecture §10; Engine §15 | Yes after field set is approved |
| CORR-BENCH-001 | Proposed | Quality/acceptance | New benchmark section | No |
| CORR-TEST-001 | Proposed | Testability | All source acceptance sections | Yes for evidence schema |

### CORR-AUTH-001 — Make the architecture corpus self-contained

**Source defect:** Revision 1.4.1 front matter and §1 say the file supersedes Revision 1.4 and retains it completely, but Revision 1.4 is absent. A documentation-only delta cannot establish that all retained requirements are present. Affects `ENGINE-001`, `GAME-001`, and every dependent requirement.

**Proposed replacement:**

> **Architecture corpus rule.** This revision is authoritative only together with the incorporated files listed below by exact filename, version, and SHA-256. Either (a) publish Revision 1.4.1 as a consolidated document containing every still-active Revision 1.4 requirement, and state that no external Revision 1.4 text is incorporated, or (b) supply Revision 1.4 and an itemized 1.4→1.4.1 change manifest. Requirements not present in the hash-pinned corpus are not presumed. A missing incorporated file is a release and implementation blocker.

**Impact and validation:** Documentation/configuration only unless omitted requirements are discovered. A corpus-verification script shall hash every file and fail on absence or mismatch. Product and architecture owners must approve the chosen consolidation route. Supplying an unchanged missing file and recording its hash is safe for AI auto-remediation after that choice.

### CORR-AUTH-002 — Approve dependencies in order

**Source defect:** Gameplay Draft 0.2 is a freeze candidate; Engine Draft 0.1 is an architecture-review candidate and depends on Gameplay. Their normative `MUST`s are not approved requirements. Affects the whole gameplay/engine tree.

**Proposed replacement:**

> **Approval gate.** Gameplay 0.2 and Engine 0.1 remain non-authoritative planning inputs until their required corrections are incorporated and approval is recorded. Approve in this order: architecture corpus and corrections; Gameplay; Engine; measured-limits revision. Host proof work explicitly authorized by Revision 1.4.1 may continue. Production gameplay assembly and asset finalization may not rely on an unapproved candidate.

**Impact and validation:** Program gate only. The build manifest shall print the approved specification-set ID and refuse release labeling against Draft inputs. Human approval is required.

### CORR-REF-001 — Pin one platform evidence identity

**Source defect:** Architecture §2 uses the 20 July 2026 chipset reference while Engine uses a 3 April 2024 edition. Neither source records document hash, target core build, ROM, bitstream, machine model, or configuration. Affects `ENGINE-006`, `MEM-001`, `PERF-004`, `AUDIO-001`, `TOOL-003`.

**Proposed replacement:**

> **Platform evidence identity.** The normative documentation baseline is the 20 July 2026 MEGA65 Chipset Reference until superseded by an approved record. Each evidence bundle records: reference filename and SHA-256; MEGA65 model and serial class; core/bitstream identity; ROM identity; CPU speed; PAL/NTSC and 50/60/63 Hz selection; expansion memory; storage device/media; input devices; and Xemu version/configuration when applicable. A later manual does not retroactively change accepted behavior. Any difference between the pinned target and the reference is an explicit compatibility finding.

**Impact and validation:** Update citations and evidence metadata; run a hardware identity probe at boot and in the R0 report. Architecture/platform approval is required. Updating the stale citation and manifest after approval is safe for AI auto-remediation.

### CORR-TIME-001 — Replace the integer superperiod assumption

**Source defect:** Architecture §6.3 requires a “six-NTSC-frame superperiod containing exactly ten simulation ticks.” The official geometry gives `526 × 858 / 27 MHz ≈ 16.715111 ms` per NTSC frame; six frames are about `100.290667 ms`, or `10.029067` 10-ms ticks. Display and simulation phases therefore drift, and a two-frame interval can intersect three or four tick executions. Affects `PERF-001`–`PERF-004`, `RENDER-004`, `TEST-003`.

**Proposed replacement:**

> **Independent-clock admission rule.** The authoritative simulation period is 10,000 microseconds. Display service is driven by measured raster timing and is asynchronous to simulation. The scheduler shall not assume an integer display/simulation superperiod. Budgets shall be specified (1) per simulation tick, (2) per display service, and (3) over every relative phase in a measured rolling window long enough to expose the maximum tick/display/DMA overlap. The R0 harness shall enumerate or sweep initial phase, report worst and percentile service costs, and prove that no legal phase causes tick skip, unsafe tick debt, input loss, audio deadline failure, or snapshot overwrite. The former 530k/100k/585k/135k two-frame figures remain planning allocations only until converted into measured per-service and worst-window limits.

**Impact and validation:** Scheduler, instrumentation, renderer admission tests, and performance documentation change. Verify both PAL and NTSC target modes for at least ten minutes per load case plus forced phase sweep; physical hardware is mandatory. Human architecture approval is required.

### CORR-SNAP-001 — Define bounded simulation-to-render handoff

**Source defect:** Architecture §3.1 and Engine §§3.3/8 allow the renderer to retain an immutable older `SimulationSnapshot` while simulation publishes a newer one, but no schema, maximum size, buffer count, acquisition/release protocol, overwrite rule, or ledger allocation exists. Affects `ENGINE-004`, `MEM-005`, `RENDER-001`, `TEST-002`.

**Proposed replacement:**

> **Presentation snapshot contract.** Authoritative simulation state is never exposed directly to presentation. Tick stage 20 extracts a generated, bounded `PresentationSnapshot` containing only render/HUD/audio-facing values. The measured-limits revision shall state `PRESENTATION_SNAPSHOT_MAX_BYTES`, field schema/version, and buffer count. Buffers have states `FREE`, `PUBLISHING`, `READY`, and `READING`; simulation alone transitions `FREE→PUBLISHING→READY`, renderer alone transitions `READY→READING→FREE`. Publication is an atomic index/state change after the checksum. Simulation shall never mutate `READY` or `READING` storage. If no `FREE` buffer exists, authoritative simulation continues and publishes no new presentation snapshot; a diagnostic counter increments. Renderer uses its current snapshot or the newest complete `READY` snapshot and may discard older unread presentation snapshots. Presentation drop/coalescing cannot affect simulation or replay. Required storage is charged explicitly to the chip-RAM ledger and protected by canaries in debug builds.

**Impact and validation:** CoreRuntime, SimEngine extraction, RenderEngine, HUD/audio event presentation, memory schemas, replay metadata, and tests. Race tests shall force renderer delay beyond two display services and prove no authoritative mutation, overwrite, torn record, or simulation stall. The human architecture owner must choose the buffer count and maximum bytes; a three-buffer ring is recommended unless measurements justify another bounded design.

### CORR-IFACE-001 — Establish a canonical generated-record registry

**Source defect:** Gameplay §18 and Engine §14 list different names and coverage (`TrackQuality` versus `RadarTrackState`; `WeaponGuidanceState` versus `MissileGuidanceState`; several gameplay records have no engine owner). Affects nearly all cross-module requirements.

**Proposed replacement:**

> **Canonical interface registry.** `interfaces/f65_interfaces.json5` is the only source for public binary record names, stable numeric IDs, fields, offsets, sizes, alignment, units, numeric formats, valid ranges, enum values, sentinel values, owner, readers, production/consumption stage, and schema version. Gameplay prose may name a logical concept but shall map it to exactly one registry record. Java and assembly definitions, serializers, debuggers, and documentation tables are generated from the same registry. Hand-written duplicate layouts are prohibited. Renaming or reusing a numeric ID requires an approved migration entry. The initial registry must reconcile every record named in Gameplay §18 and Engine §14 before either document is approved.

**Impact and validation:** All public module interfaces and generated artifacts. CI compares generated output byte-for-byte and assembles Java/assembly offset probes. Semantic naming choices require architecture approval; mechanical regeneration afterward is safe for AI auto-remediation.

### CORR-NUM-001 — Complete the numeric and coordinate registry

**Source defect:** Architecture §4 defines NED and `WorldPosition`, but orientation, angular units, rates, forces, velocities, table domains, fixed-point widths, rounding, saturation, divide-by-zero, conversions, and frame-transform conventions remain undefined. Affects `FLIGHT-*`, `RADAR-*`, `COMBAT-*`, `RENDER-*`.

**Proposed replacement:**

> **Numeric registry.** Every authoritative scalar and vector field shall declare: physical meaning; frame; unit; signedness; storage width; integer/fraction bits; valid and representable range; invalid encoding; rounding mode; overflow/saturation rule; normalization rule; and host conversion. The registry shall define body attitude representation, angular rate, linear velocity, acceleration, force, moment, mass, range, bearing/elevation, time, and probability/RNG comparison. All frame transforms state handedness and axis order. Floating point is forbidden in target authoritative state. Divide-by-zero, out-of-domain table input, invalid normalization, and sector-boundary overflow enter the controlled invariant-fault path rather than relying on processor accident.

**Impact and validation:** Generated interfaces, host oracle, flight/sensor/weapons math, replay, debug formatting. Golden vectors cover extrema, sign changes, wrap, sector crossings, and every rounding boundary. Human architecture approval is required because precision choices consume memory and cycles.

### CORR-INPUT-001 — Complete semantic input and command-frame behavior

**Source defect:** Gameplay §5 requires contexts and many actions but omits or does not freeze primary pitch/roll/yaw demands, taxi steering, complete throttle semantics, view/glance commands, pause/menu navigation, device arbitration, ranges, edges, holds, and overflow behavior. Engine §11 names an `InputCommandFrame` without layout. Affects `INPUT-001`–`INPUT-004`, `FLIGHT-001`, `GAME-003`.

**Proposed replacement:**

> **Input contract.** Raw keyboard and joystick sampling produces one tick-stamped `InputCommandFrame` for each active simulation tick. It contains signed pitch, roll, yaw/taxi-steer demands; absolute or relative throttle command; context; trim; weapon trigger/release; target and radar actions; countermeasure/jammer actions; gear/flap/hook/brake/ADLC actions; view/glance; pause; and menu/navigation actions. The interface registry defines ranges, dead zones, calibration, axis inversion, quantization, held level versus rising/falling edge, repeat policy, mutually exclusive actions, device arbitration, and context legality. Menu/full-pause actions are consumed outside active simulation. No physical key code enters gameplay modules. If multiple raw samples precede a tick, axes use the latest calibrated value and all non-repeatable edges are OR-latched once; the latch clears only after frame consumption. Queue overflow raises a controlled input fault in test builds and an explicit diagnostic/recovery policy in release builds.

**Impact and validation:** InputEngine, settings, flight control, Deck/TFL/Normal/Combat mappings, replay, UI. Acceptance covers keyboard-only and at least one approved digital/analog joystick on Xemu and hardware. Product approval is required for the default mapping and digital shaping.

### CORR-PAUSE-001 — Separate paused wall time from active simulation time

**Source defect:** Gameplay §4 says full pause freezes simulation; Architecture §3 says ticks are exactly 100 Hz, monotonic, and never skipped. Without state-machine semantics, paused wall time can become tick debt or emit stale input edges. Affects `GAME-003`, `PERF-001`, `INPUT-003`, `TEST-002`.

**Proposed replacement:**

> **Pause semantics.** `SimulationTick` counts completed `ACTIVE_SORTIE` steps only. Entering `FULL_PAUSE` occurs at a completed tick boundary. While paused, the scheduler dispatches no simulation tick, accrues no tick debt, advances no simulation RNG or mission time, and publishes no authoritative snapshot. Presentation and pause-menu input may continue on wall/raster time. Gameplay input edges are cleared on entry and re-armed only after all controls return to neutral or their release state. Resume establishes a new wall-time deadline origin; the first active tick is exactly `previous SimulationTick + 1`. Replays encode pause/resume as out-of-band presentation/control events and reproduce identical active-tick checksums.

**Impact and validation:** Scheduler, input latches, mission time, audio policy, replay. Tests pause for arbitrary wall duration during held trigger/axis input and prove no debt, duplicate release, or checksum divergence. This is a low-risk logical reconciliation and is safe for AI auto-remediation after approval.

### CORR-FAULT-001 — Define deterministic failure and overflow behavior

**Source defect:** The sources name timing faults and capacities but do not unify behavior for invariant failure, event/input/track/callout overflow, pool exhaustion, corrupt resources, save/media failure, DMA timeout, or unexpected platform identity. Affects `ENGINE-005`, `MEM-004`, `RADAR-004`, `TOOL-004`, `TEST-005`.

**Proposed replacement:**

> **Fault contract.** Every bounded resource and external operation has a named fault code, detection point, authoritative/non-authoritative classification, release response, and captured diagnostic fields. An authoritative overflow or invariant breach shall never wrap, corrupt adjacent memory, depend on presentation order, or silently change simulation. In development it stops at a deterministic tick boundary and writes a fixed-size fault record. In release it enters the approved controlled-performance pause or abort-to-debrief path without writing a normal save. Presentation-only overflow uses its documented deterministic priority/drop rule and increments a counter. Storage/resource corruption is rejected before activation; the last known-good save remains recoverable. Unknown hardware identity blocks measured/release claims but may enter an explicitly labeled diagnostic mode.

**Impact and validation:** All queues/pools, resource loader, save system, diagnostics, scheduler. Fault injection must cover every code. Product approval is needed for player-facing abort/recovery messaging; architecture approval is needed for the technical path.

### CORR-PLAT-001 — Publish one 45GS02/IRQ/DMA/MAP platform ABI

**Source defect:** Architecture §2 defines MAP ownership and DMA safety, but neither source defines the timer/raster/audio/input interrupt plan, nesting/acknowledgment, maximum masked interval, DMA blocking protocol, Q-mode and extended-addressing clobbers, or hardware multiply/divide semantics. Affects `ENGINE-002`, `ENGINE-006`, `PERF-*`, `MEM-002`, `AUDIO-001`.

**Proposed replacement:**

> **Platform ABI.** A generated platform contract shall identify every interrupt source, priority, vector owner, acknowledgment sequence, allowed nesting, preserved registers including Q/A/X/Y/Z and base-page state, maximum masked duration, and work deferred to the scheduler. It shall define MAP entry/exit preconditions, reentrancy prohibition, canonical `$01`, base-page ownership, and debug assertions. DMA jobs shall declare source/destination reachability, length, overlap legality, list storage, blocking duration, completion detection, and whether audio arbitration applies. Ordinary DMA shall be budgeted as CPU-unavailable time where the pinned core blocks the CPU. Hardware multiply/divide and Q-mode/extended-address operations shall be used only through verified wrappers that define operands, result, signedness, divide-by-zero, latency, clobbers, and interrupt safety. R0-A compares wrapper results and timing against host and software reference implementations before choosing each backend.

**Impact and validation:** CoreRuntime, MemoryAccessABI, DMAManager, math library, audio, renderer, scheduler, test ROM. Hardware verification on every supported core/ROM identity is mandatory. Architecture/platform approval is required.

### CORR-MEM-001 — Replace paper-fit claims with generated peak proofs

**Source defect:** Engine §4 arithmetic fills the 32 KB simulation ledger exactly but record layouts are estimates, event-buffer maximum fan-out is not derived, and snapshot storage is not charged. Affects `MEM-003`–`MEM-005`, `COMBAT-004`, `ENGINE-004`.

**Proposed replacement:**

> **Memory admission.** All resident and active arrays are generated from approved schemas. The linker emits per-owner actual, limit, and reserve; CI fails on overlap or limit excess. A pool-capacity proof includes record size, alignment, canaries/debug overhead policy, worst simultaneous live count, and spawn/free ordering. Queue proofs enumerate the maximum legal producers per tick and their maximum fan-out. Snapshot buffers and fault records are first-class allocations. The 32 KB measured-limits reserve is not consumed by baseline features without a numbered architecture decision. “Fits on paper” is planning evidence only until generated layouts and adversarial peak tests pass.

**Impact and validation:** Linker map, schema generator, mission compiler, peak harness, all pools/queues. Architecture approval required.

### CORR-STORE-001 — Define disk, package, load, and save transactions

**Source defect:** Architecture §12, Gameplay §4, and Engine §13 require D81 boot/packages/saves but give no directory/partition plan, byte budget, package version/integrity, residency plan, load-time target, media errors, or atomic-save strategy. Affects `GAME-003`, `ENGINE-007`, `TOOL-002`, `TEST-006`.

**Proposed replacement:**

> **Storage contract.** The build emits a disk manifest containing every file, exact and allocated bytes, checksum, package/schema version, destination residency class, and load phase. A release gate proves the independently bootable MVP image fits the selected D81 filesystem including allocation overhead and required free/save space. Tactical packages are loaded and validated before the sortie; no tactical disk read is required. Each package has magic, version, declared length, section directory, per-section bounds, and integrity check. Save writes are transactional: write and verify a new generation, then atomically select it; retain the prior valid generation. Define behavior for absent, changed, write-protected, full, corrupt, or removed media and for power loss at every write boundary. Boot and transition timing are measured on Xemu and physical media/device configurations.

**Impact and validation:** Bootstrap, resource manager, mission compiler/package, save system, menus, D81 builder. Product approval is required for recovery UX and campaign disk split; architecture approval for format and transaction.

### CORR-TOOL-001 — Make the macOS toolchain reproducible

**Source defect:** Engine §§14/17/21 name KickAssembler, Java, Xemu, JSON5, and “published bootstrap artifacts,” but do not pin versions, commands, dependencies, paths, exit behavior, or artifacts; the claimed artifacts were not supplied. Affects `TOOL-001`–`TOOL-004`.

**Proposed replacement:**

> **Reproducible build contract.** The repository shall contain a checked-in toolchain manifest with KickAssembler version and hash/license location, JDK version, host dependency lock, Xemu version/configuration, required MEGA65 core/ROM identities, and deterministic locale/time-zone settings. One documented non-interactive command shall regenerate interfaces/assets/missions, assemble target binaries, construct D81 images, run host tests, launch or drive emulator smoke tests where supported, and write a machine-readable evidence index. Generated artifacts identify their generator and source hash and fail a clean-tree check if stale. No document may call an artifact “published” until its path exists in the reviewed repository and its validation command passes.

**Impact and validation:** Build scripts, CI, generated outputs, documentation. A clean checkout on a second macOS host must produce byte-identical deterministic artifacts except explicitly listed metadata. Architecture/tooling approval required; manifest scaffolding is safe for AI auto-remediation after approval.

### CORR-ASSET-001 — Add a bounded asset manifest

**Source defect:** Engine §14 names glTF/PNG/WAV sources, but there is no required asset inventory, dimensions, topology/LOD limits, palette roles, converted byte budgets, sample formats, or fallback behavior. Affects `RENDER-003`, `AUDIO-002`, `GAME-005`, `TOOL-002`.

**Proposed replacement:**

> **Asset manifest.** Every required visual/audio asset has a stable ID, owner, gameplay use, source file, license/provenance, source constraints, conversion recipe/version, palette role, LOD or sample-rate variants, converted size limit, residency class, preload group, fallback/proxy, and acceptance owner. Mesh classes declare maximum vertices/edges/faces after conversion and each LOD transition. Images declare pixel dimensions, bit depth/indexing, transparency, and palette policy. Audio declares channels, sample format/rate, loop/cut points, priority, maximum duration, and DMA channel policy. The converter rejects rather than truncates out-of-envelope assets. The aggregate manifest must fit the chip/Attic/D81 ledgers before final asset approval.

**Impact and validation:** Asset pipeline, renderer, audio, package builder, art/audio review. Human art/audio and architecture approval required.

### CORR-MISSION-001 — Define the technical vertical slice and Midnight Spear

**Source defect:** Architecture §§1/17 name “Midnight Spear,” but no start state, objective graph, entities, failure/success conditions, representative assets, duration, or acceptance threshold defines it. Gameplay §16 describes only Operations 1 and 2. Affects `GAME-001`, `GAME-004`, `TEST-007`.

**Proposed replacement:**

> **Vertical-slice identity.** `Midnight Spear` shall not authorize implementation until a mission brief record names its start state, map/terrain package, participating entities and loadouts, objective graph, allowed branches, success/failure/abort conditions, expected duration, required controls/views/displays/audio, AI doctrine set, asset manifest subset, performance load case, deterministic replay seed, and acceptance IDs. Until that creative definition is approved, §14.2 of the Technical Alignment Supplement defines a non-narrative **Technical Combat Slice** solely for engine validation. Passing that slice does not constitute completion of Midnight Spear or the release MVP.

**Impact and validation:** Mission authoring, content, assets, integrated tests. Product/creative approval required.

### CORR-CAMP-001 — Gate incomplete campaign content

**Source defect:** Gameplay §16 provides opening material for two operations, while the remaining eight, branch predicates, two endings, scoring/progression, failure persistence, and authored concurrency proofs are incomplete. Affects `GAME-004`, `GAME-006`, `TOOL-002`.

**Proposed replacement:**

> **Campaign content gate.** Full-production campaign implementation begins only from an approved ten-row campaign manifest. Each operation declares mission IDs, prerequisites, carried state, scoring/grade effects, retry/abort consequences, objective branches, ending predicates, required assets, peak entity proof, and acceptance playthroughs. The two endings shall be reached by explicit deterministic campaign-state predicates. Unwritten operations may use non-shipping compiler fixtures but may not be invented by an implementation agent or counted complete.

**Impact and validation:** Campaign state, saves, mission compiler, debrief, QA. Product/creative approval required.

### CORR-RADAR-001 — Separate sensor truth, semantic track, and display cadence

**Source defect:** Gameplay §§10/18 and Engine §9 describe truth, tracks, identification, overflow, and a roughly 10 Hz display target without one exact cadence/interface contract. Affects `RADAR-001`–`RADAR-004`, `RENDER-002`.

**Proposed replacement:**

> **Sensor cadence contract.** Physical truth advances only at 100 Hz tick stage 2. Each sensor declares a tick-indexed scan schedule and deterministic revisit/measurement order. Track prediction, association, quality, identification, aging, and overflow occur only at the named track stage and use the canonical record registry. Fire-control consumers read the completed semantic track set, never display state. Display pages sample semantic tracks at their approved presentation cadence; urgent cues may request immediate presentation without advancing sensor/track state. The registry defines quality states, age, confidence, covariance/error surrogate, source/fusion flags, lost/coast/deletion thresholds, capacity ordering, and tie breaks. A dropped display update cannot change detection, lock, guidance, AI knowledge, or replay.

**Impact and validation:** Sensor/TrackEngine, radar/RWR, fire control, AI knowledge, displays. Host scenarios cover threshold crossings, equal-priority capacity overflow, coast/reacquire, jamming, sector boundaries, and cadence independence. Product approval is required for display feel; architecture approval for semantics.

### CORR-AUDIO-001 — Bound audio DMA and content

**Source defect:** Engine §12 assigns SID plus four audio-DMA channels and a 12 KB cache without sample formats/rates/durations, channel arbitration, memory reachability, DMA contention, cut/loop behavior, or degraded policy. Affects `AUDIO-001`–`AUDIO-003`, `PERF-003`, `MEM-005`.

**Proposed replacement:**

> **Audio service contract.** The audio registry assigns SID voices and four PCM channels by category and defines priority, preemption, retrigger, ducking, loop/cut boundary, maximum service latency, and deterministic event-to-sound mapping. PCM assets reside in or are staged into audio-reachable chip RAM before playback. Each declares bit depth, signedness/encoding, sample rate, maximum length, alignment, and converted bytes. The measured-limits revision charges audio bus/DMA contention to worst-phase budgets and selects a maximum aggregate active rate. Overflow drops only presentation audio by the documented stable priority/order and records a counter; it cannot alter simulation/RIO decisions. Essential warnings have a tested fallback when PCM channels or assets are unavailable.

**Impact and validation:** AudioEngine, ResourceManager, DMA manager, asset converter, warnings. Measure event-to-audible latency, distortion, contention, and preemption on physical hardware. Product/audio and platform approval required.

### CORR-REPLAY-001 — Define canonical checksums and replay compatibility

**Source defect:** Architecture §10 and Engine §15 require checksums/replay but not field scope, serialization order, algorithm, cadence, version compatibility, input encoding, fault representation, or comparison evidence. Affects `TEST-001`, `TEST-002`, `ENGINE-005`.

**Proposed replacement:**

> **Replay/checksum contract.** The authoritative checksum stream is generated from a schema-versioned canonical serialization of approved simulation state after tick stage 19 and before presentation extraction. Fields, entity ordering, byte order, padding exclusion, RNG streams, free-list state, and mission/campaign state are explicit. The checksum algorithm and cadence are versioned. Replays contain specification/build/platform identities, initial state/package/seed, one semantic input frame per active tick, and out-of-band pause/control events. A loader rejects incompatible schema/build identities unless an approved migration exists. Presentation state, wall time, diagnostics counters that do not affect authority, and uninitialized padding are excluded. Host and target runs report the first divergent tick and field group.

**Impact and validation:** Replay, test harness, serializers, diagnostics. Golden replay tests run twice on host, Xemu, and hardware and compare the complete checksum stream. Mechanical generator work is safe for AI auto-remediation after the field set is approved.

### CORR-BENCH-001 — Defer and control the F-117A comparison

**Source defect:** The three sources do not define F-117A as a benchmark; the audit request adds it without pinning title/revision/platform. “Exceed” has no baseline captures or scoring rule. Affects `GAME-007`, `PERF-005`, `TEST-008`.

**Proposed replacement:**

> **Reference-experience benchmark.** Absolute F-65 quality thresholds are primary and govern pre-R0 through representative release evaluation. No R0 or Phase 1 task depends on F-117A access, identity, capture, or comparative outcome. Before any comparative claim is made, F-65 shall be compared with one legally obtained, exactly identified F-117A release running under a recorded Amiga 1200 configuration. The benchmark record states title, publisher, release/disk revision and hashes where lawful, PAL/NTSC, CPU/chipset/RAM, storage, display, input, emulator/hardware, and capture tools. Tests record the categories and methods in §12. F-65 passes a category only when it meets the category’s absolute threshold and, where objective comparison is possible, exceeds the measured reference value or documents a human preference decision. Historical features are facts only when cited; unmeasured comparisons are labeled `Aspirational`. No F-117A code, assets, mission text, maps, audio, UI art, or other protected expression may be copied.

**Impact and validation:** Product quality plan and later capture evidence only; no pre-R0, R0, Phase 1, or core implementation dependency. Product/legal/acceptance approval is required before comparative claims.

### CORR-TEST-001 — Standardize acceptance evidence

**Source defect:** Acceptance sections contain useful intentions but mix subjective statements, unspecified tolerances, host tests, emulator results, and hardware gates without a common evidence record. Affects all `TEST-*` requirements.

**Proposed replacement:**

> **Acceptance evidence.** Every acceptance ID states requirement IDs, build/spec/package hashes, environment identity, preconditions, inputs/seed, duration/sample count, measured variables and units, pass threshold/tolerance, oracle, expected and actual result, first divergence/fault, artifacts, executor, date, and human sign-off where subjective. Host tests prove model logic; Xemu tests prove routine integration; only physical-MEGA65 evidence may close a hardware/timing/DMA/audio/input/storage gate. “Runs,” “looks smooth,” “feels good,” and “assembles” are observations, not pass criteria. A failed mandatory criterion cannot be waived without a named decision and risk acceptance.

**Impact and validation:** Test tooling, reports, CI, approval workflow. Evidence-schema generation is safe for AI auto-remediation after approval; thresholds require the named human owners.

---

## 7. Cross-Document Conflict Register

This register contains the material contradictions found in the reviewed set. Missing detail without two incompatible claims is recorded in §8 and Appendix B instead.

| Conflict | Sources and affected requirements | Exact conflict and consequence | Proposed authority/resolution | Approver |
|---|---|---|---|---|
| CON-001 | Architecture front matter/§1; absent Rev 1.4; all requirements | 1.4.1 says it retains the complete 1.4 baseline, but the retained source is not in the review corpus. Treating a delta as consolidated can silently omit requirements. | `CORR-AUTH-001`; architecture corpus, then this supplement’s approved corrections | Product + architecture |
| CON-002 | Gameplay front matter/§0; Engine front matter/§0 | Both describe “binding” contracts while their status is respectively Freeze candidate and Architecture-review candidate; Gameplay itself says it binds only once approved. | Status controls. Neither is binding until `CORR-AUTH-002` approval is recorded. | Product + architecture |
| CON-003 | Architecture §2; Engine §8.1 | Two different chipset-reference editions are presented as pinned verification. Hardware semantics may differ. | `CORR-REF-001`; approved platform-evidence manifest controls, initially the 2026 edition. | Platform + architecture |
| CON-004 | Architecture §§3.1, 6.2–6.3; Engine §5 | Exactly 100 Hz is combined with an exact ten ticks per six NTSC frames. Official raster timing does not produce that integer ratio. | `CORR-TIME-001`; 10-ms simulation time and measured independent display time replace the superperiod assertion. | Architecture + platform |
| CON-005 | Architecture §3.1; Gameplay §4 | `SimulationTick` is monotonic at exactly 100 Hz, while full pause freezes simulation. Undefined paused wall time makes both impossible if deadlines continue. | `CORR-PAUSE-001`; exact 100 Hz applies only in `ACTIVE_SORTIE`; pause accrues no simulation debt. | Product + architecture |
| CON-006 | Architecture §3.2; Gameplay §18; Engine §§3.3, 8.1; Engine §4 ledger | One atomic snapshot is the presentation boundary, but Engine permits an older one to remain bound while newer ones publish without storage/lifetime. | `CORR-SNAP-001`; bounded extracted presentation snapshots with explicit state machine and ledger. | Architecture |
| CON-007 | Gameplay §18; Engine §14.3 | Gameplay requires `TrackQuality` and `WeaponGuidanceState`; Engine lists `RadarTrackState` and `MissileGuidanceState`, with no mapping and missing gameplay records. | `CORR-IFACE-001`; canonical registry selects one stable name/ID and maps logical concepts. | Product semantics + architecture ABI |
| CON-008 | Engine §§3.1, 3.2, 4.5, 8.1 | `CoreRuntime` exclusively owns DMA submission; later only `DMAManager` may submit. `ResourceManager` stages Attic data, but the module graph contains only `ResourceAndDiagnostics`. | Core owns validation/serialization and exposes a DMA service; resource residency is a separately named owner. Final names/entry points come from the registry. | Architecture |
| CON-009 | Architecture §6.4; Engine §§5, 8.1 | Renderer must never block protected services while waiting for DMA, yet ordinary DMA can block CPU service on the target; “awaiting” alone does not prevent an overlong submitted batch. | `CORR-PLAT-001`; each batch carries measured worst blocking time and is admitted only inside the protected-latency bound. | Platform + architecture |
| CON-010 | Engine §21.1; reviewed workspace | The Engine says bootstrap artifacts are published at concrete paths, but those artifacts are absent from the provided corpus/workspace. | `CORR-TOOL-001`; remove “published” until files exist and validate, or supply them with hashes. | Architecture/tooling |
| CON-011 | Architecture §12 resource residency; Engine §§3.2, 4.5 | Architecture says only the Resource Manager changes residency; Engine groups resources with diagnostics but also names a different unstated manager. State ownership and entry points disagree. | Registry shall define `ResourceManager` as the sole mutable residency owner; diagnostics are read-only consumers. | Architecture |
| CON-012 | Architecture §6.4; Gameplay §10; Engine §§5, 9 | Radar/system pages may run at lower rates with “immediate” critical updates, while semantic track updates are confined to a frozen tick stage. Without separation, “immediate” can be read as a second sensor update. | `CORR-RADAR-001`; only presentation is immediate; semantic state changes at scheduled 100 Hz stages. | Product + architecture |

### 7.1 Capacity statements that are not conflicts

Architecture pool maxima (for example 16 aircraft and 32 missiles) are hard allocation capacities. Gameplay’s combined-load case (9 aircraft, 16 missiles, 24 gun groups, 48 decoys, 8 dynamic mission entities, 8 objectives, and 64 presentation effects) is a simultaneous acceptance profile. The smaller numbers do not reduce the pools. Mission packages must pass both per-pool capacity and the combined scenario proof. This interpretation should be added to the mission-compiler contract to prevent an agent from shrinking arrays to the Gameplay profile or assuming that every pool maximum may occur simultaneously.

---

## 8. Missing Requirements and Clarifications

The following are the smallest additional specifications needed to prevent incompatible implementations. Where a correction already supplies insertion-ready language, this table points to it rather than duplicating it.

| Gap | Severity | Missing decision/specification | Minimum closure | Destination |
|---|---|---|---|---|
| GAP-001 | Blocker | Complete incorporated architecture corpus | File/version/hash manifest or consolidated 1.4.1 | `CORR-AUTH-001` |
| GAP-002 | Blocker, closes before Phase 1 | Snapshot schema, maximum bytes, buffers, lifetime | Generated presentation schema and acquisition state machine | `CORR-SNAP-001` |
| GAP-003 | Major / phased | Canonical public ABI | Initial R0-A registry subset, then each record before its consuming interface freezes | `CORR-IFACE-001` |
| GAP-004 | Major / Phase 2 | Numeric formats and frame transforms | Field-by-field numeric registry and golden boundaries before physics consumers | `CORR-NUM-001` |
| GAP-005 | Major / R0-B–Phase 2 | Complete input set and default bindings | Initial command-frame envelope now; full semantics and human-approved shaping at named gates | `CORR-INPUT-001` |
| GAP-006 | Critical | Interrupt, DMA, MAP, Q-mode, math ABI | Platform contract and R0 opcode/timing evidence | `CORR-PLAT-001` |
| GAP-007 | Major / R0-E–Phase 1 | Queue/event maximum fan-out | Producer×fan-out proof, capacity, stable ordering, fault | `CORR-MEM-001`, `CORR-FAULT-001` |
| GAP-008 | Major / R0-C | Disk/package/save behavior | Format, byte budget, integrity, transactions, failure UX | `CORR-STORE-001` |
| GAP-009 | Major / current deliverable | Reproducible toolchain | Version/hash manifest and one clean build/test command | `CORR-TOOL-001` |
| GAP-010 | Major / later product gate | Midnight Spear definition | Mission identity and acceptance manifest | `CORR-MISSION-001` |
| GAP-011 | Major / Phase 2 | Flight and control coefficients | Approved tables/ranges, host oracle, pilot acceptance | Gameplay §19 `FL-*`; `DEC-009` |
| GAP-012 | Major / Phase 3 | Radar/weapons/defense data | Approved tables and boundary scenario corpus | Gameplay §19 `RD/WP/GN/DF-*` |
| GAP-013 | Major / Phase 4 | AI/RIO doctrine and scheduling | Decision cadence, utility/tie rules, knowledge tests | Gameplay §19 `AI-01` |
| GAP-014 | Major | Display mode and pixel format | Width/height/stride/packing/pages/palette/swap timing | R0-B measured-limits revision |
| GAP-015 | Major | World/terrain binary formats | Tile scale, height encoding, continuity, query bounds | Engine §§6, 14 registry |
| GAP-016 | Major | Collision/contact tolerance | Shapes, swept-test precision, tie order, penetration recovery | Contact interface and golden cases |
| GAP-017 | Major | Radar display cadence | Semantic scan schedule versus visual refresh schedule | `CORR-RADAR-001` |
| GAP-018 | Major | Audio channel and asset plan | Registry, memory/cache envelope, contention budget | `CORR-AUDIO-001` |
| GAP-019 | Major | Asset inventory | Per-asset converted envelope and aggregate fit | `CORR-ASSET-001` |
| GAP-020 | Major | Replay/checksum format | Canonical serialization, version, first-difference report | `CORR-REPLAY-001` |
| GAP-021 | Major | Controlled fault behavior | Code catalog and player/developer recovery | `CORR-FAULT-001` |
| GAP-022 | Major | Save/campaign schema migration | Stable IDs, defaults, rejection/migration rules | Storage/save interface |
| GAP-023 | Major | Tutorial restart semantics | Initial seed/state, save side effects, grade/debrief effects | Gameplay §§4, 16; Mission contract |
| GAP-024 | Major | Damaged/unavailable RIO countermeasure path | Manual fallback, degraded automatic behavior, or intentional loss | `DEC-007` |
| GAP-025 | Major | Primary-view and chase-view controls | Complete mappings, transitions, camera collision/horizon policy | `CORR-INPUT-001`; render/view contract |
| GAP-026 | Major | Campaign operations 3–10 and endings | Ten-row manifest with deterministic predicates | `CORR-CAMP-001` |
| GAP-027 | Advisory / deferred | F-117A identity and measured baseline | Exact release/config/capture plus licensed access | `CORR-BENCH-001`, `DEC-006`; non-blocking until comparative claims |
| GAP-028 | Major | Minimum supported physical MEGA65 | Model/core/ROM/RAM/video/storage/input matrix | `CORR-REF-001`, `DEC-003` |
| GAP-029 | Major | Load/transition targets | Boot, title, sortie, debrief, disk-swap absolute thresholds | §11 `ACC-STO-001` and transition-specific extensions |
| GAP-030 | Major | Accessibility acceptance | Readability setup, remap persistence, color/flash/audibility options | Product/accessibility decision and tests |
| GAP-031 | Major | Mission compiler proof algorithm | Restricted graph model, branch/concurrency analysis, witness output | Mission compiler contract |
| GAP-032 | Major | Degraded rendering visibility policy | Minimum target/threat/HUD information at every shedding tier | Rendering and product acceptance |
| GAP-033 | Minor | Terminology drift | Stable glossary for world frame, local frames, snapshot, truth/track, MVP | Appendix D |
| GAP-034 | Minor | Module/file ownership | Module status board must map owner to actual paths and ABI IDs | Engine §16 generated ownership manifest |
| GAP-035 | Minor | Decision deadlines and stale TBDs | Gate, owner, due milestone, deferral consequence for each TBD | §15 and Appendix E |

### 8.1 Planning specifications that may be adopted without creative invention

The following defaults are proposed only to unblock measurements; they do not define release feel:

- Use deterministic proxy geometry, generated tones, and synthetic mission data for R0/Phase 1.
- Start the Technical Combat Slice airborne so carrier physics does not block proof of flight/radar/combat; test carrier contact separately before a narrative slice.
- Treat display stores as opaque 64 KB resources until R0-B selects encoding. A test candidate may use 320×200×8-bit because it fits in 64,000 bytes, but that does not freeze the release mode.
- Use stable handle/producer ordering whenever two legal operations otherwise tie; never depend on traversal order of a mutable free list unless that order is in the canonical state/checksum.
- Reject malformed authoring data at build time. Do not add target-side repair heuristics for packages that the host compiler controls.

---

## 9. Technical Feasibility Corrections

### 9.1 Feasibility conclusion

The product is **plausible but unproven** on the intended production MEGA65. The fixed pools, static memory ownership, incremental renderer, no Z-buffer, host-generated data, presentation shedding, and R0 hardware gate are appropriate. The principal risk is not raw nominal CPU throughput; it is simultaneous worst-phase timing after DMA/audio stalls, renderer memory bandwidth, 6DOF/sensor/AI load, and snapshot/event storage are measured together.

### 9.2 CPU and frame time

The pinned 2026 chipset reference describes NTSC timing as 526 lines × 858 pixel clocks at 27 MHz. This yields about 16.715111 ms (59.826105 Hz). At a 40.5 MHz CPU clock:

| Quantity | Bounded calculation | Meaning |
|---|---:|---|
| Nominal CPU clocks per 10-ms simulation tick | 405,000 | Upper wall-time supply before stalls/interrupt overhead |
| CPU clocks per two NTSC frames | 1,353,924 | Very close to the source 1,350,000 planning ledger |
| Six NTSC frames | 100.290667 ms | Not exactly 100 ms |
| Simulation intervals per six frames | 10.029067 | Relative phase drifts; cannot be fixed at ten |
| Average protected non-render allocation per tick | about 158,539 clocks | `530,000 / 3.343022` average tick intervals in two frames |
| Mandatory reserve in source ledger | 135,000 clocks | About 10% of the two-frame supply, before interpreting DMA wait |

The aggregate 1.35M-clock ledger is arithmetically credible as an average two-frame supply. It is not yet a safe deadline proof because:

- relative phase can place four tick executions across a selected two-frame service window;
- ordinary DMA may make the CPU unavailable during a job;
- audio DMA competes for memory/DMA opportunities;
- interrupt entry, raster service, input scanning, and buffer swaps need explicit charges;
- “clock” must mean the same measured counter across CPU execution, waits, DMA, and emulator reports; and
- worst legal entity/event fan-out is not represented by average synthetic work alone.

**Required prototype:** R0-A timing harness with a hardware counter calibration, controllable tick/raster phase, DMA lengths and address classes, audio on/off, MAP windows, IRQ load, and captured worst/p50/p95. R0-D then runs the generated combined-load fixture. Physical hardware closes the gate; Xemu is a regression aid.

### 9.3 Memory and banking

The source map matches the documented production-class memory regions: 384 KB chip RAM, 32 KB color RAM, and normally 8 MB Attic RAM. The design correctly prevents direct presentation/audio consumers from treating Attic as ordinary chip RAM. Risks remain:

- The 32 KB active-simulation ledger totals exactly 32,768 paper bytes, leaving no local slack for alignment, schema growth, snapshot buffers, debug guards, or underestimated events.
- The entity-array arithmetic is internally consistent (`19,328` bytes in Engine §4.3.1), but semantic sufficiency cannot be proven until record schemas exist.
- The 1 KB “checksum and snapshot assembly” allocation is not evidence that one or more complete presentation snapshots fit.
- The 2 KB deterministic event buffer has no producer/fan-out proof.
- Reclaiming `$020000–$03FFFF` for display storage removes the normal ROM mapping assumption; boot, hypervisor/FDC calls, recovery, and post-reclaim storage access require a verified sequence.
- Attic RAM is “normally” 8 MB, not a universally safe minimum across all development configurations. The support matrix must explicitly include or exclude smaller/no-Attic targets.

**Required prototypes:** generated linker/schema map; canary peak harness; every pool at its legal high-water; adversarial same-tick event generation; MAP/base-page/ROM-reclaim test; Attic-to-chip staging throughput and correctness; cold-resource/package residency proof.

### 9.4 VIC-IV and renderer

Two 64 KB display stores strongly constrain direct pixel formats. Examples:

| Candidate representation | Bytes | Fits one 64 KB store? |
|---|---:|---|
| 320×200, 8 bits/pixel | 64,000 | Yes, with 1,536 bytes spare |
| 640×200, 4 bits/pixel | 64,000 | Yes, before metadata |
| 720×480, 8 bits/pixel | 345,600 | No |
| 720×576, 8 bits/pixel | 414,720 | No |

VIC-IV’s ability to emit higher resolutions does not make a full high-resolution software framebuffer affordable in the assigned stores. Native high-resolution remains a future target exactly as Architecture §13 says; production must select a packed/tiled/character/FCM arrangement or lower render surface at R0.

A full 64 KB clear once per two NTSC frames is about 1.96 MB/s before span writes, cockpit/HUD composition, and DMA-list traffic. If visible drawing averages two additional complete-store equivalents, the display-write demand is roughly 5.9 MB/s; this is an estimate, not a measured bus budget. Near-plane clipping, painter failure cases, span/DMA-list capacities, and carrier geometry are credible but high-risk assembly work.

**Required prototype:** representative sky/ocean clear, terrain, carrier, 9-aircraft scene, effects, cockpit/HUD, and worst overdraw at each candidate mode. Measure CPU clocks, DMA blocking, bytes written, list occupancy, aborts, completed-world cadence, input/audio latency, and monitor stability. Accept no mode solely because a static screenshot renders.

### 9.5 DMAgic, MAP, Q-mode, multiplication, and division

The official chipset documentation states that ordinary DMA jobs block the CPU until completion and cannot be interrupted, while audio DMA consumes otherwise available memory/DMA opportunities. Therefore the source rule “renderer never blocks protected services while awaiting [DMA]” must include maximum submitted-job duration; asynchronous software organization cannot make an uninterruptible hardware job preemptible.

The MEGA65/45GS02 provides extended-addressing and Q-register facilities useful to this architecture. The audit brief also requires hardware multiplication and division to be evaluated, but the reviewed F-65 documents do not pin the availability or semantics of any arithmetic accelerator for the target core. It would be unsafe for independently generated assembly modules to assume or use any of these facilities directly.

**Required prototype:** for every wrapper, execute signed/unsigned normal and boundary vectors, illegal/divide-zero cases, IRQ entry during all legal windows, MAP/base-page changes, and cycle counts on the pinned core. Compare with a bit-exact Java oracle and a conservative software implementation. Select the hardware backend only when it is deterministic, faster in the complete call context, and compatible with interrupt ownership.

### 9.6 Numeric precision and physics

`WorldPosition` is unusually well bounded: signed N/E sectors plus 24-bit local 1/256-m offsets and 24-bit altitude. The rest of the physical state is not. Six-degree-of-freedom rotation and moments are especially sensitive to normalization drift, intermediate width, table interpolation, saturation, and unit conversion. A plausible-looking target build can still diverge from host truth after thousands of ticks.

**Required prototype:** use a high-precision host oracle, then a bit-exact target model. Golden suites must include zero/maximum airspeed, low/high altitude, ±G limits, quaternion/matrix or chosen attitude normalization, 180° boundaries, sector crossings, ground/deck contact, engine-out asymmetry, long-duration trim, missile high-rate turn, and overflow-inducing invalid inputs. Record tolerance per variable and tick horizon; “same general trajectory” is insufficient.

### 9.7 Input

Keyboard and joystick support are feasible, but latency and ambiguity depend on the exact scan/IRQ/display schedule and hardware adapters. Sampling “every display frame” followed by a 100 Hz command latch requires an edge-preserving bridge; otherwise a press and release between simulation ticks can vanish, or PAL/NTSC can alter commands.

**Required prototype:** timestamp raw transitions and consumed semantic frames under keyboard-only, approved joystick(s), simultaneous key combinations, held/rapid inputs, device hot/unplug where relevant, renderer/DMA peak load, pause/resume, PAL/NTSC, and Xemu/hardware. Measure transition-to-tick latency and prove identical recorded semantic commands for the same test stimulus within the approved device model.

### 9.8 Audio

Four PCM channels plus SID are feasible, but the 12 KB cache bounds content sharply. For illustration, 12 KB holds about 0.77 seconds of 8-bit mono at 16 kHz or 1.54 seconds at 8 kHz before metadata/multiple sounds; 4-bit encoding roughly doubles duration. Long voice lines cannot be assumed resident at that budget. Attic assets must be staged to audio-reachable chip RAM, and tactical disk streaming is forbidden.

**Required prototype:** warning tones, engine bed, missile/RWR cues, impacts, and representative RIO snippets using the proposed channel plan. Measure cache high-water, staging latency, preemption, event-to-audible latency, glitches, SID interaction, DMA contention, and degraded warning fallback on hardware.

### 9.9 Storage and loading

An unformatted D81 image is conventionally 819,200 bytes, but filesystem allocation and directory needs reduce usable payload. The sources set no aggregate package budget. An independently bootable MVP is feasible only after boot/runtime/assets/missions and required save space are counted. Multi-D81 campaign support increases transition and recovery requirements; it is not a substitute for a fit proof.

**Required prototype:** deterministic D81 builder; file/allocation manifest; cold boot through title and one sortie; resource integrity failures; campaign disk change; write-protect/full/removal/power-loss save injection; physical internal drive and any other supported storage. Report median/worst transition time and recovery result.

### 9.10 Emulator versus hardware risk matrix

| Area | Xemu use | Physical-hardware requirement |
|---|---|---|
| Deterministic math, schemas, replay | Fast regression and first-divergence diagnosis | Confirm target opcode/core behavior and long-run checksums |
| Raster/frame timing | Routine scheduling regression | Authoritative clocks, phase sweep, video-mode stability |
| DMAgic | Functional lists/range checks | Blocking/arbitration duration, overlap, audio contention |
| Audio | Event/channel logic | Audible latency, distortion, SID/PCM mix, DMA behavior |
| MAP/base page/ROM release | Functional smoke test | Hypervisor/core/ROM edge behavior and post-release I/O |
| Keyboard/joystick | Mapping regression | Matrix ghosting, adapter/device latency, simultaneous input |
| VIC-IV/display | Pixel/layout regression | Palette, raster, swap tearing, monitor compatibility |
| Storage/save | Fast corruption tests | Real drive/media timing, write protect/removal/power-loss behavior |
| Performance counters | Trend detection | Release budgets and reserves |

No Xemu-only result may close `R0-GATED`, hardware timing, input latency, audio quality, DMA, or physical storage acceptance.

---

## 10. Unified Interface Contracts

This section is a proposed minimum contract layer. It freezes no still-creative coefficient. Values marked `R0` or `Human` must be inserted into the generated registry before the consuming production module is ready.

### 10.1 Ownership and dependency graph

```text
CoreRuntime
├── PlatformABI / MemoryAccessABI / DMAService
├── InputEngine
├── EnvironmentEngine
├── ControlAndSystemsEngine
├── FlightDynamicsEngine
├── ContactEngine
├── WeaponAndDamageEngine
├── SensorAndTrackEngine
├── AIEngine
├── MissionEngine
├── PresentationExtractor
├── GraphicsEngine          [reads presentation only]
├── AudioEngine             [reads presentation/audio events only]
├── ResourceManager         [sole residency owner]
├── StorageService          [non-tactical transitions only]
└── Diagnostics             [read-only observation plus bounded fault records]
```

`DMAService` is a CoreRuntime service, not an independent mutable owner: callers submit validated requests; CoreRuntime alone serializes and starts hardware jobs. `ResourceManager` owns handles, residence state, and staging. `Diagnostics` may inspect counters and append bounded records but may not change resources or simulation. This resolves `CON-008` and `CON-011` if approved.

### 10.2 Universal ABI rules

| Property | Contract |
|---|---|
| Source | `interfaces/f65_interfaces.json5` plus generated memory/numeric registries |
| Byte order | Little-endian for multibyte target records unless a format explicitly declares otherwise |
| Packing/alignment | Explicit per field/record; no compiler-native padding is serialized or checksummed |
| Boolean | Named enum values; never interpret arbitrary nonzero bytes unless declared |
| Handles | Frozen `EntityHandle`, `ResourceHandle16`, and `FarPtr32`; generation and invalid/sentinel encodings remain explicit |
| Tick | Unsigned 32-bit active `SimulationTick`; every authoritative command/event includes origin/effective tick as applicable |
| Units | Canonical internal units from numeric registry; aviation display conversion occurs only in presentation |
| Ownership | Exactly one mutable owner per field/queue/pool; readers receive read-only views or copied records |
| Mapping | Public entry points begin/end canonical mapping, `$01=$35`, base page `$0200`; only `MemoryAccessABI` changes MAP/base page |
| Clobbers | Every assembly entry declares A/X/Y/Z/Q, flags, base-page scratch, mapping, and reentrancy/IRQ safety |
| Ordering | Stable numeric enum/handle/source/producer sequence; address or incidental iteration order is prohibited unless specified |
| Invalid input | Reject at boundary, saturate only where field contract says, otherwise emit the named invariant fault |
| Versioning | Schema version changes on layout/semantic change; serialized/package compatibility is explicit, never inferred |
| Instrumentation | Cycles/wall ticks, high-water, overflow/drop, saturation, and first fault are recorded per owner |

### 10.3 Frozen active-tick order and publication boundary

The Architecture’s 21 stages remain authoritative. Module calls and principal records are mapped as follows:

| Stage | Owner/action | Consumes | Produces/commits |
|---:|---|---|---|
| 1 | CoreRuntime increments active tick | Previous complete tick | `SimulationTick` |
| 2 | CoreRuntime/InputEngine latches | Edge-preserved raw-input accumulator | `InputCommandFrame[t]` |
| 3 | CoreRuntime dispatches commands | Player/AI/mission directives with effective tick | Ordered commands applied to owned requests |
| 4 | EnvironmentEngine | Mission environment, prior carrier state | Environment/carrier truth for tick |
| 5 | ControlAndSystemsEngine supply | Commands, damage, prior supplies | Fuel/electrical/engine/hydraulic supply state |
| 6 | ControlAndSystemsEngine laws | Commands, air/aircraft state, supply | `FlightControlFrame` |
| 7 | ControlAndSystemsEngine actuators | Control frame, authority/damage | `ControlSurfaceState` |
| 8 | FlightDynamicsEngine force evaluation | Actual surfaces, atmosphere, engine, class tables | Bounded forces/moments |
| 9 | FlightDynamicsEngine integration | Rigid/kinematic state, forces/moments | New aircraft motion truth |
| 10 | ContactEngine | Motion truth, terrain/deck/runway | Corrected contact state and ordered contact events |
| 11 | WeaponAndDamageEngine requests | Commands, stores, fire-control authorization | Pending spawns/ammunition changes |
| 12 | WeaponAndDamageEngine motion | Existing missiles/groups/decoys | New weapon truth |
| 13 | Contact/WeaponAndDamageEngine detection | Swept paths and candidate sets | Ordered collision/fuze/damage events |
| 14 | WeaponAndDamageEngine damage | Sorted damage events | Accumulated component/capability state |
| 15 | SensorAndTrackEngine | Post-motion/post-damage truth, environment | Observations, tracks, RWR/warnings |
| 16 | AIEngine | Sensor-limited blackboards, doctrine schedule | `AIIntentFrame` for tick ≥ `t+1` |
| 17 | MissionEngine | Completed tick facts/events | Objectives, score, tutorial/campaign events |
| 18 | CoreRuntime lifecycle | Pending spawn/despawn lists | Pool/free-list generations and live set |
| 19 | PresentationExtractor | Completed authoritative state | Cockpit/warning/audio event values |
| 20 | CoreRuntime/checksum | Canonical authoritative serialization | Checksum record for tick |
| 21 | CoreRuntime/PresentationExtractor | Complete extracted record | Atomic ready-state publication |

No presentation, audio playback, disk, debugger, or renderer callback may execute inside a module in stages 1–21. Protected asynchronous services communicate only through bounded queues or published records.

### 10.4 Subsystem contract matrix

| Contract | Owner | Inputs | Outputs/readers | Cadence/order | Capacity/budget | Error behavior |
|---|---|---|---|---|---|---|
| IC-CORE-001 Scheduler | CoreRuntime | Timer/raster evidence, mode state | Tick dispatch, deadlines, debt counters | 100 Hz in `ACTIVE_SORTIE`; no debt in pause | R0 worst-phase budget | Timing fault after approved debt threshold; no skipped/merged tick |
| IC-MEM-001 Mapping | MemoryAccessABI | Validated address/range/operation | Copied/mapped data; canonical map restored | Explicit non-nested call | Source windows/ledger; R0 latency | Range/mapping fault; never continue mapped incorrectly |
| IC-DMA-001 DMA | CoreRuntime DMAService | Immutable validated job + deadline class | Completion/fault record | Only admitted safe points; ordinary job treated as blocking | Per-job measured maximum; list pool fixed | Reject overlap/range; timeout/invariant fault; no partial presentation publish |
| IC-INPUT-001 Input | InputEngine | Keyboard/joystick samples, settings | One semantic command frame/tick; UI actions outside sim | Raw at approved scan cadence; latch stage 2 | Fixed edge accumulator/queue | Explicit overflow fault/recovery; no silent edge loss |
| IC-ENV-001 Environment | EnvironmentEngine | Mission tables, tick, position | Pure atmosphere/wind/gravity/terrain-query inputs | Truth stage 4; queries pure within tick | Table bytes and max query clocks R0/Phase 1 | Clamp only to declared domain; invalid query fault |
| IC-SYS-001 Controls/systems | ControlAndSystemsEngine | Commands, aircraft truth, damage, supplies | Control frame, surface state, system state | Stages 5–7 every tick | Player detailed state + common aircraft records | Saturation/degradation explicit; no hidden assistance in Manual |
| IC-FLT-001 Flight | FlightDynamicsEngine | Class, rigid/kinematic state, actual controls, environment | New motion truth, force diagnostic | Stages 8–9 every tick | 16 aircraft pool; module clock ceiling R0 | Numeric/contact fault; no NaN-like sentinel propagation |
| IC-CONTACT-001 Contact | ContactEngine | Swept motion, typed candidates, terrain/deck | Ordered contact/collision candidates | Stages 10 and 13 | Generated candidate/event maxima | Conservative rejection; capacity breach aborts tick via fault, not missed collision |
| IC-WPN-001 Weapons/damage | WeaponAndDamageEngine | Requests, tracks, weapon state, contact events | Spawns, trajectories, damage/capabilities | Stages 11–14 every tick | 32 missiles, 32 gun groups, 64 decoys; combined profile separately | Stable rejection when store/pool unavailable; event overflow fault |
| IC-RADAR-001 Sensors/tracks | SensorAndTrackEngine | Post-damage truth, environment, emissions, prior tracks | Track file, RWR/warnings, AI/fire-control views | Stage 15; sensor scan schedule tick-indexed | 32 truth, 24 tracks; stable capacity priority | Drop/coast/delete by declared tie rules; counters; no duplicate physical contact |
| IC-AI-001 AI/RIO | AIEngine | Sensor-limited blackboard, doctrine, mission authorization | Intent for future tick, RIO callout request | Stage 16 on declared schedules | RIO 4; doctrine/table and per-slot clock ceilings | Fallback intent on invalid option; no truth leakage; stable tie |
| IC-MSN-001 Mission | MissionEngine | Ordered events, live handles, graph/package | Objective/score/tutorial/campaign state, directives ≥ next tick | Stage 17 | 32 mission entities, 16 objectives; graph proof | Package invalid at load; runtime capacity fault, no graph repair |
| IC-LIFE-001 Entity lifecycle | CoreRuntime | Pending spawn/despawn | Live sets, generations, free lists | Stage 18 only | Frozen pools | No same-tick reuse; stale handle rejected/counted |
| IC-PRES-001 Snapshot | PresentationExtractor/CoreRuntime | Completed authoritative/presentation state | Immutable bounded snapshot to graphics/audio | Extract stage 19; checksum 20; publish 21 | Approved max bytes × buffer count | Skip new presentation publish if no free buffer; sim continues |
| IC-GFX-001 Graphics | GraphicsEngine | One acquired snapshot, immutable resources, mode/tier | Complete world store + current protected overlays | Async; HUD each display service; world incremental | 64 KB store A/B, 32 KB render work; 585k planning allocation | Abort incomplete frame and shed; never show partial store or alter sim |
| IC-AUD-001 Audio | AudioEngine | Published audio events, asset handles | SID/PCM playback, text fallback, diagnostics | Display/approved interrupt service | SID + four PCM; 12 KB current cache; R0 bandwidth | Stable presentation-only preemption/drop; essential-warning fallback |
| IC-RES-001 Resources | ResourceManager | Package manifest, handles, transition requests | Valid resident handles/staged chip data | Load/transition; approved staging points, not tactical disk | 32 KB staging plus ledgered destinations/Attic | Integrity/range/residency fault before use; no dangling handle |
| IC-STO-001 Storage/save | StorageService | Versioned package/save request | Verified package/save generation | Non-tactical state only | D81 manifest and measured transition budget | Transactional recovery; explicit absent/full/protect/corrupt/media-change result |
| IC-DIAG-001 Diagnostics/replay | Diagnostics | Read-only counters, fault/checksum records | Evidence/replay/trace | Outside authoritative mutation; bounded append | Fixed buffers; host capture policy | Diagnostic overflow flagged; cannot affect checksum/simulation |

### 10.5 Update-frequency registry

| State/service | Semantic frequency | Presentation/service frequency | Freeze status |
|---|---|---|---|
| Physical aircraft/missile/decoy/ship/surface truth | Every active 100 Hz tick | Not applicable | Confirmed |
| Environment/carrier truth | Every active tick at stage 4 | Display sampling only | Confirmed |
| Radar truth/track transitions/RWR | Stage 15 according to tick-indexed sensor schedules | Radar page target around 10 Hz; urgent cue next permitted display service | Semantic confirmed; exact schedules/display cadence TBD |
| AI/RIO/AIC decision | Scheduled slots at stage 16; output ≥ next tick | Callout playback independently queued | Schedule/doctrine TBD |
| Mission/objectives | Every active tick at stage 17 | UI/debrief as needed | Confirmed |
| Checksum/presentation extraction | Every completed tick unless checksum cadence is later approved | Latest complete snapshot | Proposed every-tick canonical stream for tests |
| Raw input | At least every display service or approved higher-rate source | UI immediate; gameplay latched next tick | R0-GATED |
| HUD/cockpit/critical warnings | Reads completed snapshot only | Every display service | Confirmed |
| World store | No semantic update | Incremental; 20 Hz is failure floor under approved load | Confirmed floor, R0 performance limits |
| Audio | Event generated at stage 19 | Every display service or approved audio interval | Confirmed principle; exact interval R0 |
| Storage | No active tactical reads/writes except approved failure logging mechanism | Boot/menus/transitions/debrief only | Confirmed |

### 10.6 Performance-budget registry required at R0

The current source figures remain planning envelopes. R0 must publish this table with numeric values and evidence; blank values block the named production module.

| Budget ID | Quantity | Current planning value | Required frozen value/evidence |
|---|---|---:|---|
| BUD-CPU-001 | Nominal CPU supply/tick at 40.5 MHz | 405,000 clocks | Calibrated effective counter and timer variance |
| BUD-CPU-002 | Protected non-render average/two NTSC frames | 530,000 clocks | Per-module/tick and worst-phase rolling ceiling |
| BUD-HUD-001 | Protected HUD/cockpit/display/two frames | 100,000 clocks | Per-display worst/p95 and mode-specific maximum |
| BUD-REN-001 | Incremental world render/two frames | 585,000 clocks | Per-work unit and rolling-window admission |
| BUD-RES-001 | Mandatory reserve/two frames | 135,000 clocks | Minimum reserve after all stalls and measured overhead |
| BUD-DMA-001 | Longest uninterruptible ordinary DMA job | Unset | Hardware worst case by address/length/competing audio |
| BUD-IRQ-001 | Longest masked interval and IRQ response | Unset | Hardware threshold for timer/input/audio/raster deadlines |
| BUD-SNAP-001 | Snapshot extraction+publish | Unset | Maximum clocks and bytes at combined peak |
| BUD-EVT-001 | Events per tick and sort/apply cost | 2 KB buffer only | Derived legal count, bytes, and adversarial maximum clocks |
| BUD-AUD-001 | Audio service/bus/cache | 12 KB cache; 4 channels | Aggregate rate, latency, contention, high-water |
| BUD-LOAD-001 | Boot/sortie/transition/load | Unset | Hardware p95/worst thresholds approved in §11 |

### 10.7 Storage and serialization envelope

Packages and saves are never raw memory dumps. Their host schema shall generate:

- magic and format ID;
- major/minor version and minimum compatible reader;
- total length and section table with non-overlapping bounds;
- specification/build/source identity as appropriate;
- stable entity/resource/mission field IDs, not target pointers;
- explicit byte order and numeric encoding;
- integrity value and optional per-section integrity;
- required/optional section flags;
- deterministic default or migration for every added field; and
- an error result for unknown required fields, invalid lengths, duplicate IDs, capacity excess, or incompatible version.

The target validates header, length arithmetic, section overlap, capacities, and integrity before committing any active state. A failed load leaves the prior state unchanged.

---

## 11. Unified Acceptance Criteria

These criteria convert the source intent into testable gates. `Confirmed` criteria restate a source invariant; `Proposed` criteria or numeric thresholds require approval. An unset human/R0 value is a failing readiness condition, not permission for the implementer to choose one.

### 11.1 Authority, build, and ABI

| Acceptance ID | Traces to | Test and pass criterion | Environment | Status |
|---|---|---|---|---|
| ACC-AUTH-001 | ENGINE-001, TOOL-004 | Corpus checker finds every incorporated filename/version/hash and no unlisted normative input; missing/mismatch exits nonzero | Clean checkout | Proposed |
| ACC-AUTH-002 | CORR-AUTH-002 | Build/evidence index prints spec-set status; a Draft set cannot produce an artifact labeled release/approved | Host CI | Proposed |
| ACC-BUILD-001 | TOOL-001 | Two clean supported macOS hosts run the documented command and produce byte-identical generated interfaces, resources, packages, assembly binaries, and D81 except explicitly excluded signed metadata | Host | Proposed |
| ACC-BUILD-002 | TOOL-001, TOOL-003 | KickAssembler/JDK/Xemu/tool hashes, commands, logs, symbols, listings, linker ledger, and evidence index are retained for the build | Host CI | Proposed |
| ACC-ABI-001 | ENGINE-003, MEM-002 | Generated Java and assembly size/offset/enum probes match every public record; handwritten duplicate-layout scan is empty | Host + assembler | Proposed |
| ACC-ABI-002 | MEM-002, ENGINE-006 | Every public entry-point test begins in canonical map/base page, exercises normal/error exits and declared IRQ condition, and ends with canonical map, `$01=$35`, preserved registers, and intact guards | Xemu + hardware | Confirmed intent; details Proposed |
| ACC-ABI-003 | ENGINE-006 | Each Q/extended-address/math wrapper matches all host golden vectors, declares cycles/clobbers, and produces its specified divide-zero/fault behavior | Xemu + pinned hardware | Proposed |

### 11.2 Determinism, timing, memory, and faults

| Acceptance ID | Traces to | Test and pass criterion | Environment | Status |
|---|---|---|---|---|
| ACC-DET-001 | PERF-001, TEST-001 | Two identical initial states, packages, seeds, and semantic input streams produce identical canonical checksum at every sampled active tick | Host bit-exact, Xemu, hardware | Confirmed |
| ACC-DET-002 | TEST-001, ENGINE-005 | First-difference injection changes a named field and the diagnostic identifies the first divergent tick and field group | Host + target | Proposed |
| ACC-DET-003 | ENGINE-005 | Event-order permutation fixture proves final state is invariant to producer call order and conforms to class/source/target/producer-sequence sorting, including mutual kill and same-tick damage | Host + target | Confirmed |
| ACC-TIME-001 | PERF-001, PERF-002 | Timer calibration demonstrates 10,000-µs active-tick period within the platform-approved tolerance; no tick is skipped, merged, or visibility-dependent | Hardware | Confirmed; tolerance R0 |
| ACC-TIME-002 | PERF-003, CORR-TIME-001 | PAL and NTSC phase sweep across combined legal load produces no tick skip, unsafe debt, input loss, audio deadline miss, partial display, or reserve breach; all worst/p50/p95 values are recorded | Hardware | Proposed technical correction |
| ACC-TIME-003 | PERF-002 | Injected debt of 1–8 follows the approved renderer-yield/debt policy; debt greater than 8 enters the controlled timing fault exactly once without corrupting/save-normalizing the sortie | Xemu + hardware | Confirmed threshold; recovery Proposed |
| ACC-PAUSE-001 | GAME-003, PERF-001 | Pause for 1 s, 1 min, and across `SimulationTick` deadline boundaries; tick/RNG/mission time/checksum remain unchanged, no debt accrues, and resume advances exactly one tick | Host + Xemu + hardware | Proposed |
| ACC-MEM-001 | MEM-001–MEM-005 | Generated link/schema report has no overlap, every owner ≤ approved limit, the 32 KB measured reserve intact, and all snapshot/event/fault buffers charged | Host build | Proposed |
| ACC-MEM-002 | MEM-003, COMBAT-004 | All pools/queues run at legal high-water with guards; stale handles, exhaustion, simultaneous frees/spawns, and event maxima produce specified outcomes with no guard modification | Host + target | Confirmed intent; generated proof Proposed |
| ACC-DMA-001 | ENGINE-006, PERF-003 | Range/overlap/address-class matrix rejects invalid jobs; valid jobs copy exactly; source/list mutation is detected; measured worst blocking stays within the approved deadline | Hardware | Proposed |
| ACC-FAULT-001 | ENGINE-005 | Every fault-code injection produces exactly its cataloged tick, record, state transition, player response, and recoverability; no adjacent memory or prior valid save changes | Host + target | Proposed |

### 11.3 Input, rendering, and presentation

| Acceptance ID | Traces to | Test and pass criterion | Environment | Status |
|---|---|---|---|---|
| ACC-IN-001 | INPUT-001–INPUT-004 | Every semantic action/axis has at least one keyboard and one approved joystick path where applicable; context legality and remapping persistence match the registry | Xemu + hardware | Proposed |
| ACC-IN-002 | INPUT-002, INPUT-003 | Press/release shorter than one tick, simultaneous legal controls, held controls, and pause/resume lose or duplicate zero edges across 10,000 scripted transitions | Host device model + hardware sample rig | Proposed |
| ACC-IN-003 | INPUT-002, PERF-005 | Raw transition to consumed semantic tick is ≤2 active ticks at p99 under peak renderer/DMA/audio load, with maximum and distribution recorded separately per device | Hardware | Proposed threshold; human approval |
| ACC-IN-004 | INPUT-004 | Keyboard-only novice can launch the Technical Combat Slice, fly, select/track/engage, pause, and exit without undocumented keys; qualified review confirms no binding collision | Hardware playtest | Proposed |
| ACC-REN-001 | RENDER-001, ENGINE-004 | Deliberately delay renderer beyond two display periods while publishing newer snapshots; every displayed world store uses one recorded snapshot tick, no buffer tears/overwrites, and simulation checksums remain identical | Xemu + hardware | Proposed |
| ACC-REN-002 | RENDER-001, RENDER-004 | Under approved combined load, world cadence never falls below the source 20 Hz failure floor; HUD/critical warnings update each display service; no incomplete store is shown | Hardware | Confirmed floor; load/mode R0 |
| ACC-REN-003 | RENDER-003, MEM-005 | Every legal scene/tier stays within visible/clip/face/bucket/edge/span/DMA capacities or deterministically aborts and sheds without workspace guard change | Host scene compiler + target | Confirmed intent |
| ACC-REN-004 | RENDER-002, GAME-005 | At the approved viewing distance/monitor, all critical HUD/radar/system symbols meet the approved pixel height, contrast/palette-role, update, and occlusion rubric in every lighting preset | Hardware capture + human review | Human values required |
| ACC-REN-005 | PERF-004 | Effect/camera/presentation tier permutations produce identical authoritative checksum streams | Host + Xemu + hardware | Confirmed |

### 11.4 Flight, contact, sensors, weapons, and AI

| Acceptance ID | Traces to | Test and pass criterion | Environment | Status |
|---|---|---|---|---|
| ACC-FLT-001 | FLIGHT-001–FLIGHT-004 | At least 1,000 approved maneuver vectors match the high-precision envelope and bit-exact target oracle within named per-state tolerance and horizon; no unexplained saturation/normalization fault | Host + target | Source-required; tables/tolerances Human/Phase 2 |
| ACC-FLT-002 | FLIGHT-002, INPUT-004 | Assisted and Manual are observably distinct; Manual introduces no undocumented limiter; +9/−3 G, target roll-rate, engine-out, stall/overspeed, and digital shaping meet approved envelope | Host + hardware pilot review | Human/Phase 2 |
| ACC-CON-001 | FLIGHT-004, COMBAT-004 | Swept collision/contact suite covers maximum legal relative speed, grazing/tangent, sector boundary, deck motion, runway/wire, ground penetration, and equal-time tie; no legal target tunnels | Host + target | Proposed |
| ACC-RAD-001 | RADAR-001–RADAR-003 | Approved aspect/RCS/range/clutter/jamming matrix produces exact detection, coast, quality, ID, lock/support, and deletion transitions at named ticks | Host oracle + target | Phase 3 values required |
| ACC-RAD-002 | RADAR-004 | Create more equal-priority candidates than 24 tracks; retained/dropped order matches registry for all input permutations, one physical contact is never duplicated by fusion, and overflow is presented/counted | Host + target | Proposed |
| ACC-RAD-003 | RADAR-003, RENDER-002 | Change display cadence/tier and force dropped display updates; semantic track/fire-control/AI/checksum streams remain identical | Host + target | Proposed |
| ACC-WPN-001 | COMBAT-001–COMBAT-003 | Each weapon mode runs normal, min/max range, support loss/reacquire, seeker autonomy, decoy/notch, fuze boundary, miss/expire, pool exhaustion, friendly/invalid target, and simultaneous damage vectors | Host oracle + target | Phase 3 tables required |
| ACC-WPN-002 | COMBAT-004 | Approved combined peak produces the derived maximum event set, stable order, no overflow, no same-tick slot reuse, and exact replay; one-beyond-capacity triggers named fault/rejection | Host + target | Proposed |
| ACC-AI-001 | GAME-002, RADAR-002 | AI/RIO/wingman receive only sensor-limited blackboards; hidden-truth mutation that does not change observations cannot change their next intent | Host doctrine tests | Confirmed intent |
| ACC-AI-002 | GAME-002 | Equal-utility/tie, missed schedule, damaged sensor/RIO, unavailable weapon, lost lead, and no-valid-action scenarios choose the declared deterministic fallback and next-tick timing | Host + target | Phase 4 doctrine required |

### 11.5 Mission, campaign, audio, storage, and experience

| Acceptance ID | Traces to | Test and pass criterion | Environment | Status |
|---|---|---|---|---|
| ACC-MSN-001 | GAME-004, TOOL-002 | Mission compiler rejects every fixture exceeding a pool/concurrency/event/asset/residency limit and emits a branch witness for each accepted peak | Host compiler | Proposed |
| ACC-MSN-002 | GAME-004, GAME-006 | Every operation/branch/objective/ending in approved manifest is reached by at least one deterministic replay and every impossible/invalid transition is rejected | Host + target | Human content required |
| ACC-MSN-003 | GAME-003 | Restart Sortie and tutorial restart restore the approved initial state/seed, do not duplicate campaign rewards or save side effects, and replay identically | Host + target | Proposed; product semantics required |
| ACC-AUD-001 | AUDIO-001–AUDIO-003 | Under combined load, essential warning event-to-audible/fallback latency is ≤100 ms at p99; channel arbitration matches stable priority; no audio choice changes simulation checksum | Hardware | Proposed threshold |
| ACC-AUD-002 | AUDIO-002, MEM-005 | All simultaneous approved sounds fit cache/channel/rate budgets or follow declared preemption; no tactical disk read and no read from inaccessible Attic address occurs | Build + hardware | Proposed |
| ACC-STO-001 | TOOL-002, GAME-003 | D81 manifest fits filesystem and free/save policy; clean physical boot reaches title in ≤15 s and preloaded slice launch in ≤30 s at p95 | Hardware/storage matrix | Proposed thresholds |
| ACC-STO-002 | GAME-003, ENGINE-007 | Save fault matrix (absent, write-protect, full, corrupt, removal, power loss at each boundary) always retains at least one loadable prior/new generation and reports exact result | Hardware + fault rig where safe | Proposed |
| ACC-STAB-001 | GAME-001, TEST-004 | 60-minute peak-load soak has zero crash, memory-guard change, invalid handle, authoritative overflow, checksum mismatch, partial frame, or unrecovered timing fault | Hardware | Proposed |
| ACC-EXP-001 | GAME-005, GAME-008 | First-time keyboard player completes approved basic-flight/radar/engagement tasks after the approved tutorial allowance; completion/error/time distributions meet values set by product owner | Hardware playtest, ≥ approved sample | Human thresholds required |
| ACC-EXP-002 | GAME-005, GAME-008 | Qualified flight-sim reviewers score handling, situational awareness, combat feedback, pacing, and usability using the locked rubric; no category is below its approved floor | Blind/versioned playtest | Human thresholds required |

### 11.6 Evidence hierarchy

1. Static schema/link/mission/asset proofs establish bounds, not runtime timing.
2. High-precision host models establish intended physical behavior.
3. Bit-exact host models establish target arithmetic expectations.
4. Xemu establishes repeatable integration behavior but not final physical timing.
5. Physical MEGA65 evidence establishes platform gates.
6. Human playtest establishes subjective feel, readability, accessibility, art/audio, and acceptance.

An acceptance item must use every environment named in its row. A more convenient lower evidence tier cannot substitute for a higher one.

---

## 12. F-117A Benchmark Interpretation — Deferred and Non-Blocking

### 12.1 Historical facts, assumptions, and scope

The three reviewed F-65 source documents do not name F-117A; they cite other flight-simulation inspirations. This comparison was introduced by the audit brief and is **deferred until a representative build and lawful, pinned baseline exist**. It has no pre-R0, R0, or Phase 1 dependency.

Absolute F-65 requirements in §11 govern responsiveness, frame consistency, readability, control latency, loading, audio feedback, stability, task success, and reliability. Those thresholds must be approved and met on their own merits. Comparative measurement may later raise a threshold or support a carefully scoped claim; absence or failure of the historical comparison cannot waive an absolute criterion and cannot stop early engineering work.

Documented catalog facts available for the likely title are limited:

- [OpenRetro identifies *F-117A Nighthawk: Stealth Fighter 2.0*](https://openretro.org/amiga/f-117a-nighthawk-stealth-fighter-2-0) as a MicroProse Amiga release from 1993 and catalogs its manuals/reference material.
- [MobyGames’ Amiga specifications](https://www.mobygames.com/game/655/f-117a-nighthawk-stealth-fighter-20/specs/) list Amiga 500/2000, 1 MB RAM, OCS/ECS, 3.5-inch floppy, and keyboard/mouse as minimums.
- An [original manual scan distributed with the commercial re-release](https://cdn.akamai.steamstatic.com/steam/apps/328920/manuals/Manual.pdf?t=1689356003) documents the game’s general simulation/mission/cockpit concepts, but it is not by itself proof of Amiga-specific timing or A1200 behavior.

Accordingly, this audit does **not** claim that the comparison title was designed natively for Amiga 1200 or AGA. “F-117A on the Amiga 1200” is treated as a requested execution configuration. The exact legal disk revision, PAL/NTSC, CPU/cache/chipset behavior, RAM, drive, display, input, and capture path remain `DEC-006`.

All current comparative results are **Unmeasured**. Feature recollection, online video, screenshots, reviews, and nostalgia are not baseline measurements. Facts below are limited to cited catalog/manual evidence; comparative F-65 targets are aspirational until approved and tested.

### 12.2 Benchmark protocol

1. Acquire the reference lawfully; record title/revision and non-distributable hashes where permitted.
2. Freeze one primary A1200 configuration and any secondary compatibility configuration.
3. Use the same display capture clock basis and input stimulus method where comparison is meaningful.
4. Record at least three representative conditions: free flight, radar/combat, and dense/transition workload.
5. Measure cold/warm loads separately; exclude operator disk-swap delay but report it separately.
6. Preserve raw frame timestamps, input event timestamps, audio, task logs, crashes, and tester rubric.
7. Evaluate F-65 against both an absolute threshold and the measured reference. If a category is inherently subjective, use a locked blind rubric and report sample size/confidence; do not convert preference into hardware fact.
8. Record platform strengths honestly. A higher nominal resolution or more colors does not pass if readability, cadence, or input response is worse.

### 12.3 Benchmark matrix

| Category | Historical/reference baseline status | Proposed F-65 absolute target | “Exceed” rule | Current document support / gap |
|---|---|---|---|---|
| Responsiveness | Unmeasured on pinned A1200 | Input transition→semantic tick p99 ≤20 ms; input→critical HUD response p99 ≤50 ms under approved peak | Lower p50/p95 latency and no worse maximum lost/duplicate-input count; zero lost legal edges | 100 Hz and protected input/HUD support intent; exact scan and phase behavior missing (`CORR-INPUT-001`, `CORR-TIME-001`) |
| Frame consistency | Unmeasured | World completed-frame cadence never below 20 Hz under approved load; no partial frame; record median/p95/max interval and hitch count >100 ms | Better p95 interval/hitch rate while maintaining semantic load | Strong incremental-render plan; mode and worst-phase evidence R0-gated |
| Visual clarity, resolution, color, animation | Catalog establishes OCS/ECS minimum, not captured quality | Approved VIC-IV mode; every critical cue meets locked contrast/pixel/occlusion rubric; zero palette-role violations; animation state changes visible by approved deadline | Blind task/error test and expert rubric superior, not merely more pixels/colors | Palette roles and double stores strong; asset/mode/readability specs missing |
| HUD/radar readability | Reference cockpit/manual concepts exist; measured legibility absent | ≥98% correct interpretation of required critical symbols by qualified testers under every lighting/damage tier; no critical cue hidden by shedding | Higher correct-answer rate or faster median interpretation, with absolute floor | HUD hierarchy described; glyph/layout/update thresholds R0/Human |
| Flight feel and accessibility | Reference measurement absent | Novice completes basic flight/engagement tutorial tasks at approved success floor; pilot scores Assisted and Manual above rubric floor; no undocumented assistance | Higher task success/preference without eliminating consequential systems | Rich behavior targets; coefficients and digital shaping TBD |
| Radar, targeting, weapons, combat depth | Manual/catalog can document available reference functions after identity is pinned; current comparison unmeasured | Organic/offboard/fused tracks, ID, lock/support/autonomy, radar/IR/gun engagements, RWR/jamming/decoys, deterministic damage all pass scenario matrix | More approved tactical decisions and higher situational-awareness score, with no truth cheating | Broad support; tables, cadence, record schemas, edge cases missing |
| Enemy behavior | Unmeasured | Sensor-limited deterministic doctrine; at least approved intercept, commit, defend, support, disengage, and fallback scenario behaviors; no forbidden truth access | Blind reviewers rate challenge/legibility/variety higher at matched difficulty, and AI passes knowledge tests | Architecture credible; doctrine/schedule/data TBD |
| Mission variety and pacing | Catalog/manual confirm mission-oriented play, not comparative count/quality | Ten approved operations, two endings, compiler-proven concurrency, declared objective/setting/threat/pacing tags, no broken branch | Approved content matrix has greater meaningful variety and blind pacing score | Scope fixed but only first two operations sketched; blocker for claim |
| Controls and usability | Catalog lists keyboard/mouse minimum | All gameplay/menu actions discoverable/remappable; keyboard and approved joystick paths; zero undocumented mandatory commands; pause/settings safe | Lower task time/error count and no worse learning burden | Context concept strong; complete axes/actions/defaults missing |
| Loading and transitions | Floppy baseline expected but unmeasured | Cold boot→title p95 ≤15 s; selected preloaded slice start p95 ≤30 s; non-disk tactical transitions ≤10 s; no tactical disk read | Faster measured transitions or materially fewer disruptive loads while passing absolute targets | D81 concept exists; layout/package/load budgets absent; thresholds Proposed |
| Audio feedback | Unmeasured | Critical warning event→audible/fallback p99 ≤100 ms; distinct approved cue-confusion rate ≤2%; stable priority/preemption | Faster/correcter threat recognition and higher feedback rubric | SID+four PCM plausible; channel/assets/cache/content undefined |
| Stability and reliability | Unmeasured | 20/20 clean boots; 60-min peak soak with zero crash/corruption/guard breach/authoritative overflow; recoverable save fault matrix | Lower failure rate with equal or longer test exposure; absolute zero critical fault gate remains | Determinism/guards intended; fault/storage protocols missing |
| Replayability | Reference mission/catalog content can be inventoried after pinning | Both endings reachable; all mission branches covered by deterministic replay; Free Flight plus campaign; replay reproduces checksum stream | Higher approved replay-interest rubric and greater tested meaningful branch/content coverage | Campaign/replay concepts exist; content and replay format incomplete |
| Overall player experience | No current controlled comparison | No benchmark category below its absolute floor; no Blocker/Critical release finding; qualified blind panel uses locked rubric | Proposed: ≥60% paired preference for F-65, with category reasons reported; product owner retains final acceptance | Cannot be evaluated before representative vertical slice/full campaign |

The numerical thresholds in this matrix are **Proposed**, not approved. Where the reference performs unusually well, “exceed” may require raising the F-65 threshold. Where hardware makes a relative result impractical, a documented product decision may replace the relative claim with a different MEGA65-strength target; it may not silently declare victory.

### 12.4 Copyright and clean-room boundary

The benchmark permits observation and measurement of externally visible behavior. F-65 shall not copy F-117A code, executable data, art, audio, maps, missions, narrative text, manual text, cockpit layout expression, or other protected content. Test reports should store derived measurements and original F-65 fixtures; reference captures and hashes remain access-controlled and are not shipped. Generic facts, aviation concepts, and independently designed mechanics still require ordinary provenance review.

---

## 13. AI Engineering Instructions

### 13.1 Autonomous decisions permitted after the governing gate is approved

The §4.2 pre-R0/R0-A tasks may proceed now within their explicit non-shipping boundaries. They do not need downstream flight, radar, AI, campaign, art, or benchmark decisions. An AI engineer may use clearly labeled proxy data and fixtures when the fixture cannot be mistaken for shipping behavior.

An AI engineer may autonomously:

- choose local assembly instruction sequences behind an approved ABI and measured cycle ceiling;
- factor private routines and private storage inside the module’s approved allocation;
- add assertions, instrumentation, fault injection, golden vectors, and non-shipping fixtures;
- implement generated bindings, schemas, converters, and mechanically derived documentation;
- repair a defect whose one-to-one expected behavior is already defined by an approved requirement and acceptance test;
- select among behaviorally identical optimizations using recorded target measurements;
- improve build diagnostics and reproducibility without changing artifact semantics; and
- update trace links, byte/cycle reports, and module status after verified work.
- apply a delegated batch of mechanically verifiable documentation/Minor corrections when the batch enumerates its IDs and approving delegate.

These permissions do not bypass human code review before release.

### 13.2 Decisions requiring human approval

AI engineers shall stop and escalate before changing:

- player-visible mechanics, difficulty, handling feel, control defaults, assistance, mission content, scoring, progression, endings, art, audio style, or accessibility policy;
- an architecture invariant, public record, update order/rate, state owner, memory region, pool capacity, reserve, fault/recovery behavior, or supported hardware configuration;
- an R0/measured threshold, benchmark pass rule, or evidence waiver;
- a source-document precedence/status, correction outcome, or requirement priority;
- use of an undocumented/changed hardware behavior;
- current product scope or any feature postponement that affects release; or
- copying/deriving from a reference work beyond approved observation and generic facts.

### 13.3 Task admission template

No production task enters `Ready` unless its ticket contains every applicable field below. A pre-R0/proof task may mark a downstream field `Not applicable until <closure gate>` with a reason; it does not need decisions that cannot affect its bounded output.

```text
Requirement IDs:
Approved correction/decision IDs:
Owning module and files:
Input/output interface versions:
State owner and update stage/cadence:
Memory/code/cycle/DMA budgets:
Data/asset/package IDs:
Normal and edge-case behavior:
Fault/overflow behavior:
Host oracle/golden vectors:
Target/Xemu/hardware acceptance IDs:
Expected evidence artifacts:
Human review required:
```

If any applicable line is material and unresolved, the task may remain an explicitly bounded prototype/specification task but not a conforming production implementation. Closure is evaluated against the task’s milestone, not against every future-project finding.

### 13.4 Traceability and change discipline

- Every public symbol/module header names the governing requirement and interface IDs; private helpers inherit from their owning public behavior.
- Every acceptance test names requirements; every requirement inventory row names at least one acceptance method before implementation readiness can exceed 2/5.
- A code change that alters a generated layout, cycle budget, queue high-water, data format, update timing, or observable behavior must update the interface/source/correction and tests in the same reviewed change set.
- Host oracle, bit-exact host model, assembly, replay schema, and documentation must share versioned generated constants.
- A test may not bless current code output as a golden result without an independent requirement/oracle review.
- Passing assembly/link is only `Build` evidence. Passing host vectors is only model evidence. Hardware-gated behavior requires hardware evidence.
- AI agents may not resolve a contradiction by majority vote among documents, by copying the first existing implementation, or by treating a `TBD/TARGET/R0-GATED` value as arbitrary.
- Changes to `CoreRuntime`, MemoryAccessABI, DMAService, canonical schemas, or the fixed tick order require architecture-owner review and the complete invariant suite.

### 13.5 Required engineering artifacts

Before gameplay production, the repository must contain and validate:

```text
spec/approved-spec-set.json
interfaces/f65_interfaces.json5
interfaces/f65_numeric_registry.json5
interfaces/f65_platform_abi.json5
memory/f65_memory_ledger.json5
assets/f65_asset_manifest.json5
missions/f65_mission_schema.json5
tests/f65_acceptance_catalog.json5
tests/f65_evidence_schema.json5
toolchain/f65_toolchain.lock.json
```

These are proposed logical paths, not claims that files currently exist. The Engine draft’s §21.1 paths were not present in this review. Actual paths may change with architecture approval, but one canonical source per artifact class is mandatory.

### 13.6 Code impact at time of audit

No production code or build repository was supplied in the workspace, so no code was modified and no concrete file-level patch is authorized. Once code exists, approved corrections are likely to affect `CoreRuntime`/scheduler, MemoryAccessABI, DMA service, generated interface bindings, InputEngine, PresentationExtractor/GraphicsEngine, SensorAndTrackEngine, AudioEngine, ResourceManager, StorageService, replay/diagnostics, mission compiler, asset converters, build/D81 scripts, and their tests. Appendix F maps corrections to those modules.

---

## 14. Prioritized Remediation Plan

Work is ordered by dependency and risk, not document order. Orders 0–2 may proceed in parallel where their outputs are independent; their exit criteria constrain milestone acceptance, not permission to start the other authorized §4.2 tasks. No later phase may reinterpret an earlier failed gate as a tuning issue.

### 14.1 Remediation sequence

| Order | Gate/work package | Required inputs | Deliverables | Exit criterion |
|---:|---|---|---|---|
| 0 | Authority and approval control | `DEC-001`, `DEC-002` | Complete hash-pinned corpus; correction statuses; approvers/delegates; spec-set manifest | `ACC-AUTH-001/002` pass before R0-A acceptance; does not prevent independent R0-A construction |
| 1 | Initial canonical-contract foundations | Frozen parent requirements plus proposed contracts clearly marked Draft | R0-A interface/platform/memory/evidence subset and generated stubs; downstream records remain gated | Initial subset reconciles and generation/offset probes pass; full registries close at consuming phases |
| 2 | R0-A platform proof | Target matrix `DEC-003`; toolchain manifest | Reproducible boot, symbols/listing, counter calibration, MAP/base-page/ROM/opcode/math/DMA/IRQ probes | Architecture R0-A plus `ACC-BUILD-001/002`, `ACC-ABI-002/003`, `ACC-DMA-001`, and `ACC-TIME-001` pass in their required environments |
| 3 | R0-B display/input/audio proof | Candidate modes, proxy assets, complete input registry | Mode captures, input latency/edge results, audio channel/cache/content envelope | Selected candidates and numeric measured limits approved |
| 4 | R0-C storage/resource proof | D81/package/save formats and proxy manifest | Boot/load/stage/save/fault evidence; disk and residence ledger | `ACC-STO-001/002`; no tactical disk dependency; recovery approved |
| 5 | R0-D/E combined performance proof | Generated pool/event/snapshot schemas, renderer fixture | Worst-phase CPU/DMA/render/memory/event/snapshot high-water; shedding ladder | `ACC-TIME-002`, `ACC-MEM-001/002`, and `ACC-REN-001–005`; mandatory reserve intact |
| 6 | R0-F measured-limits revision | All R0 evidence | Approved frozen mode, budgets, capacities, cadences, tool/platform IDs | Every R0-GATED value used by Phase 1 closed; gameplay merge gate opens |
| 7 | Phase 1 integrated engine harness | Approved interfaces and R0 limits | One deterministic combined service loop with proxy data and fault injection | Architecture Phase 1 suite, 60-min hardware soak, exact replay |
| 8 | Phase 2–3 model gates | Human-approved flight/systems/sensor/weapon tables | High-precision and bit-exact oracles, assembly modules, golden suites | `ACC-FLT-001/002`, `ACC-CON-001`, `ACC-RAD-001–003`, and `ACC-WPN-001/002`; qualified handling approval |
| 9 | Technical Combat Slice | Phase 1 plus minimum Phase 2–4 data | Scope in §14.2, capture/evidence, usability test | Every vertical-slice exit criterion passes on hardware |
| 10 | Midnight Spear/content production | `DEC-008`, asset/campaign manifests | Approved narrative vertical slice, then operations/assets/audio | `ACC-MSN-001–003` and human acceptance; comparative benchmark is not a gate |
| 11 | Release hardening | Complete campaign and all approvals | Reproducible release images, manuals/control reference, full absolute-quality regression; optional pinned comparative benchmark before any superiority claim | §16 checklist complete; code/content release review |

### 14.2 Minimum Technical Combat Slice

The slice proves the engineering chain without inventing Midnight Spear’s narrative.

**Scope:**

- deterministic airborne start over a proxy ocean/terrain arena; carrier takeoff/recovery and cold start are separate fixtures, not slice blockers;
- one player F-65A in approved Assisted mode, with Manual selectable for model evidence;
- keyboard and one approved joystick route for pitch, roll, yaw, throttle, context, target/radar, weapon, view, pause, and menu/exit;
- one sensor-limited AI wingman, two hostile aircraft with at least intercept/engage/defend/disengage states, and an optional fixed emitter/target only if required to prove RWR or surface query;
- organic radar search/detection, track quality/ID, priority/lock, fire-control cue, support, loss/reacquire, and display cadence separation;
- one representative radar-guided missile engagement, one cannon/gun-group engagement, countermeasure/defensive reaction, ordered damage, despawn/spawn lifecycle, and a deterministic success/failure outcome;
- cockpit/HUD/radar/system essentials, low-cost chase view, critical warning audio/text fallback, and proxy but budget-valid assets;
- one mission graph with start, engage, success, failure, abort, debrief, and restart; it is explicitly non-campaign;
- exact replay/checksum, fault injection, instrumentation, and evidence capture; and
- separate synthetic combined-load run at the Gameplay §3.1 profile. The playable encounter need not contain the full stress load at all times.

**Dependencies:** approved source corpus; R0-F limits; generated records/numeric/platform ABI; validated toolchain/D81; presentation snapshot; deterministic event proof; minimal approved flight/radar/weapon/AI tables; proxy asset manifest; human-approved controls and basic handling rubric.

**Performance and memory limits:** the slice must remain inside the approved R0 per-tick/per-display/rolling-window budgets, pool/queue maxima, 64 KB display-store format, chip/Attic/D81 manifests, audio aggregate rate/cache, maximum DMA batch, and full mandatory reserve. No temporary slice exception may consume the release reserve or bypass fault behavior.

**Exit criteria:**

1. One clean command produces host tools, target binary, packages, D81, symbols/listings, and evidence identity.
2. The slice completes from both keyboard and approved joystick on physical hardware with no undocumented control.
3. Flight/radar/weapon/AI outcomes pass their golden scenarios; no module reads forbidden state.
4. Replaying the same semantic input/seed twice on host, Xemu, and hardware yields the approved checksum stream or an approved, diagnosed platform-specific exception; presentation changes never alter it.
5. NTSC and every supported PAL mode pass worst-phase timing with no tick skip, unsafe debt, lost input/audio warning, partial frame, or reserve breach.
6. World cadence stays above the approved threshold and never below 20 Hz; HUD and critical warnings meet their independent deadlines.
7. Pool/event/snapshot/render workspace high-waters remain within generated bounds; forced exhaustion produces the named deterministic behavior.
8. Critical audio latency, storage/load, pause/resume/restart, save/recovery as included, and a 60-minute soak pass their acceptance IDs.
9. Product owner accepts the basic control/handling/combat/readability rubric; this does not approve final tuning or art.
10. Every result is linked requirement → interface → module/build → test → evidence, and all failures/waivers are closed by named decisions.

### 14.3 Defer until after the technical slice

- full cold-start choreography and nonessential cockpit interactions;
- production carrier deck choreography and final LSO grading, while retaining separate contact prototypes;
- campaign operations 3–10, endings, persistence polish, and narrative assets;
- final scenery density, native high-resolution mode, complex transparent effects, or texture experiments;
- broad voice library and final music mix beyond representative channel/cache proof;
- nonessential views, editor polish, and generalized modding;
- destructible static scenery, already excluded by the architecture; and
- any feature that consumes the 32 KB measured-limits reserve without a numbered approval.

---

## 15. Open Decisions for Human Review

Only material decisions are listed. Recommended choices are not approved defaults.

| Decision | Owner/deadline | Options and tradeoffs | Recommendation | Consequence of deferral |
|---|---|---|---|---|
| DEC-001 Architecture corpus | Product + architecture; before any spec approval | **A:** publish consolidated 1.4.1 (simplest first-read, requires completeness proof). **B:** supply 1.4 plus exact delta (preserves history, increases reading/config risk). | A, with old versions retained as history | All production requirements remain suspect; Blocker stays open |
| DEC-002 Draft approvals | Product + architecture; after Blocker corrections | **A:** revise 0.2/0.1 through approved corrections then approve. **B:** replace with new numbered consolidated docs. **C:** keep planning-only. | A for speed if owners confirm intent | Gameplay/engine assembly cannot be conforming production |
| DEC-003 Supported platform matrix | Platform + product; before R0-A | Production MEGA65 only; include devkits/no-Attic systems with degraded path; PAL+NTSC versus one mode first; named core/ROM/storage/input devices. More breadth multiplies hardware tests and fallbacks. | Production-class 40.5 MHz/8 MB Attic, named core/ROM, PAL and NTSC; exclude smaller targets initially | Memory/timing/reference results cannot be closed |
| DEC-004 Snapshot design | Architecture; before interface freeze | Full authoritative-state double/triple copy (simple concept, high bytes/copy cost); extracted presentation double buffer (smaller, may skip when held); extracted triple buffer (recommended resilience, more bytes). | Bounded extracted triple buffer, subject to R0 byte/cycle proof | Renderer and simulation cannot safely integrate |
| DEC-005 Display candidate/quality floor | Product + platform/art; R0-B | 320×200 8-bit direct candidate; packed/tiled higher-resolution candidate; multiple tiers. Higher resolution competes with fill rate/stores. | Benchmark at least two candidates; freeze the clearest one that passes worst-load 20 Hz floor and reserve | Renderer/assets/HUD cannot freeze |
| DEC-006 F-117A benchmark identity | Product + acceptance/legal; before any comparative capture or claim, not before R0/Phase 1 | Pin exact Amiga disk release on A1200 configuration; choose a different documented reference; or keep it non-normative inspiration. | Defer. If a comparative claim remains desirable near representative release evaluation, pin likely 1993 *F-117A Nighthawk 2.0* Amiga release and one A1200 PAL setup after lawful acquisition. | Comparative claim remains unavailable; no early engineering consequence |
| DEC-007 Countermeasure/RIO failure control | Product; before input/defense freeze | Automatic RIO only (simple, loss may remove defense); manual fallback (more controls/agency); hybrid emergency action (recommended). | One context-sensitive manual emergency dispense plus RIO automation; define damaged-state behavior | Input and defensive AI cannot be accepted |
| DEC-008 Midnight Spear definition | Creative/product; before narrative slice | Use Operation 2 CAP as slice; write a distinct mission; rename technical slice. Each affects content reuse and campaign pacing. | Keep Technical Combat Slice non-narrative, then define Midnight Spear as a distinct approved mission manifest | Named vertical slice cannot be implemented or accepted |
| DEC-009 Flight-feel authority | Product; before Phase 2 tuning | One designer; qualified pilot/sim panel; metric-only. Metrics alone miss feel, panels cost time. | Named product owner plus 3–5 qualified reviewers using locked rubric and oracle limits | AI must invent gains/feel or tuning stalls |
| DEC-010 Campaign/endings | Creative/product; before Phase 4 content production | Linear ten ops; limited deterministic branches; wider branching. Branch breadth expands content/save/test matrix. | Limited deterministic branches with explicit two-ending predicates | Eight missions, campaign state, scoring, saves remain incomplete |
| DEC-011 Audio/voice scope | Product/audio/platform; R0-B and content lock | Tones/SID/text only; short PCM RIO vocabulary; extensive voice. More PCM consumes cache/package/staging and preemption complexity. | Short high-priority PCM vocabulary plus text and SID fallback; measure before expansion | Asset/D81/cache/latency budgets cannot freeze |
| DEC-012 Save medium/recovery UX | Product + architecture; R0-C | Same MVP disk with reserved space; separate save disk; supported host storage. Transaction model and user friction differ. | Two-generation transactional save on supported writable medium; retain prior generation and clear recovery prompt | Campaign reliability and D81 fit cannot be approved |
| DEC-013 Default controls and digital shaping | Product/accessibility; R0-B/Phase 2 | Simulation-heavy mapping; context-optimized mapping; two presets. Digital shaping determines accessibility/feel. | Two named presets sharing one complete semantic action set; context-optimized default | Input implementation and novice tests remain blocked |
| DEC-014 Absolute F-65 quality thresholds | Product + acceptance; each value before its consuming R0/slice/release gate | Approve §11 absolute values; revise once from R0/physical evidence; or defer a player-facing value to its named human gate. Relative-only comparison is not an option. | Retain absolute floors and revise from F-65 evidence independently of F-117A; comparative evidence may only raise or contextualize them later | The affected F-65 quality gate cannot pass; unrelated R0-A work continues |
| DEC-015 MVP D81 content boundary | Product + architecture; before package/content lock | Midnight Spear plus minimum shell/free flight; full campaign on one image; campaign bootstrap with additional disks. More content raises fit/load/save risk; too little weakens “MVP.” | After DEC-008, define a self-contained polished Midnight Spear package with required title/settings/control reference and representative free-flight access; keep full campaign as current full scope unless fit evidence supports more | Disk/assets/save budget and the meaning of MVP remain ambiguous |

---

## 16. Final AI-Readiness Checklist

### 16.1 Current authorized R0-A horizon

Work may start now. R0-A is complete only when the applicable items are checked and linked to evidence:

- [ ] The task is within §4.2 and contains no gameplay implementation or shipping `TBD` decision.
- [ ] The ledger schema encodes all frozen regions, code/allocation ceilings, and reserve ownership used by the proof.
- [ ] The initial interface generator covers the approved R0-A subset and emits Java/assembly size/offset assertions.
- [ ] The module status/ownership source, generated board, and diff-scope validator exist and reproduce.
- [ ] The mission schema/capacity analyzer skeleton reports the approved combined-load fixture without claiming full mission-compiler soundness.
- [ ] Toolchain/platform/spec identities, commands, symbols, listings, and evidence index reproduce from a clean supported macOS environment.
- [ ] The independent-clock timing correction governs the profiler/harness; the obsolete exact ten-tick superperiod is not encoded.
- [ ] The Memory Access ABI proof D81 validates opcode, MAP/base-page, DMA, IRQ, canonical restoration, and error paths in Xemu and on the pinned physical hardware.
- [ ] The architecture-corpus disposition is recorded before R0-A is formally accepted, even though it did not prevent independent proof work.
- [ ] No result is represented as authorizing flight, radar, weapons, tactical AI, campaign, or production-renderer assembly.

### 16.2 Full-production checklist

Full autonomous production remains **No-Go** until every item whose closure gate is at or before the proposed work is checked and linked to evidence. Later-phase items remain visible but do not block earlier authorized work.

### Authority and decisions

- [ ] Complete hash-pinned architecture corpus supplied or consolidated (`DEC-001`, `ACC-AUTH-001`).
- [ ] Every Blocker/Critical correction required by the proposed work’s closure gate is `Approved`, `Rejected` with replacement, or `Superseded`; none is merely deferred past that gate.
- [ ] Gameplay and Engine baselines have approved versions and dependency order (`DEC-002`).
- [ ] Platform/core/ROM/video/storage/input support matrix is approved (`DEC-003`).
- [ ] Material creative decisions required by the next phase are approved; remaining TBDs have owners/gates and do not leak into implementation.

### Contracts and bounds

- [ ] Canonical interface, numeric, platform, memory, fault, replay, mission, asset, acceptance, and evidence registries validate and generate all bindings.
- [ ] Every mutable field/pool/queue has one owner, stage/cadence, unit/format, capacity, and error behavior.
- [ ] Snapshot buffer count/bytes/lifetime and memory charge pass delayed-render tests.
- [ ] Complete semantic input/action/default/remap/device behavior is approved.
- [ ] Event fan-out, pool/free-list ordering, and all overflow/drop/fault behavior are proved.
- [ ] Package, D81, residency, save transaction, migration, and media-failure contracts are approved.

### Platform and performance

- [ ] Reproducible toolchain and clean-build artifacts pass on a second supported macOS host.
- [ ] R0-A platform ABI/opcode/MAP/base-page/ROM/IRQ/DMA/timer proof passes Xemu and physical hardware.
- [ ] Independent 100 Hz/display-clock phase model replaces the integer superperiod assumption.
- [ ] R0-B–F measured-limits revision freezes display, per-service/rolling budgets, maximum DMA latency, input/audio cadence, and required reserve.
- [ ] Generated chip/Attic/display/audio/staging/D81 ledgers fit without consuming the frozen reserve.
- [ ] Phase 1 combined harness passes worst-phase peak load and 60-minute physical soak.

### Gameplay, content, and acceptance

- [ ] Flight/control/system, radar, weapon/defense, AI/RIO, carrier, fuel, and campaign tables needed by the phase are approved and have host/target vectors.
- [ ] Technical Combat Slice and Midnight Spear are separately identified; each has an approved mission/asset/test manifest.
- [ ] The independently bootable MVP D81 has an approved content, disk-split, and save-space boundary (`DEC-015`).
- [ ] Ten-operation/two-ending campaign manifest exists before full campaign production.
- [ ] F-117A identity, lawful access, baseline capture, and benchmark thresholds are approved before superiority claims.
- [ ] Every requirement traces to engine support, data/assets, implementation task, deterministic tests, and acceptance owner.
- [ ] Xemu-only evidence is not used to close hardware gates.
- [ ] Product/creative, art/audio, playtest, architecture/scope, code, and release approvals remain human decisions.

When these conditions are met, readiness may change to **Conditional Go** for the approved phase. A final **Go** requires the phase’s actual evidence, not only completed documentation.

---

## 17. Appendices

## Appendix A — Requirements Inventory and Traceability Matrix

### A.1 Requirement conventions

- Priority `P0` is architecture/safety/gate-critical; `P1` is required for the Technical Combat Slice or release core; `P2` is required for full current scope; `P3` is quality/future unless promoted.
- Authority `Frozen` means stated by Revision 1.4.1, subject to `CORR-AUTH-001`. `Draft-G` and `Draft-E` mean source-stated but not approved. `Proposed-S` means introduced or made precise by this Draft supplement.
- A source section is not sufficient authority when its document status is Draft.

### A.2 Stable requirements inventory

#### Product, gameplay, flight, combat, and radar

| ID | Requirement summary | Source / authority | Pri. | Dependencies | Owner/subsystem | Acceptance |
|---|---|---|---:|---|---|---|
| GAME-001 | Cockpit-primary retro-synthwave MEGA65 F-65A interceptor product; low-cost chase view; one bootable MVP D81 | Architecture §§1, 13 / Frozen | P1 | ENGINE-001, RENDER-002, TOOL-002 | Product; Graphics; Build | ACC-BUILD-001, ACC-REN-004, ACC-STO-001 |
| GAME-002 | RIO, wingman, AIC, and enemies use deterministic sensor-limited decisions and next-tick commands | Gameplay §14 / Draft-G; Engine §10 / Draft-E | P1 | RADAR-002, ENGINE-002, AI data | AIEngine | ACC-AI-001/002 |
| GAME-003 | Title/settings/three save slots/full pause/restart/no time acceleration/no mid-sortie save | Gameplay §4 / Draft-G | P1 | INPUT-003, ENGINE-007, TEST-006 | UI, Scheduler, StorageService | ACC-PAUSE-001, ACC-MSN-003, ACC-STO-002 |
| GAME-004 | Declarative bounded missions, Midnight Spear, ten-operation campaign, two endings | Architecture §1 / Frozen; Gameplay §16 / Draft-G; Engine §13 / Draft-E | P2 | TOOL-002, MEM-003/004, GAME-006 | MissionEngine, mission compiler, Product | ACC-MSN-001/002, ACC-STO-001 |
| GAME-005 | Presentation/accessibility includes cockpit/HUD/radar/status, warning hierarchy, visual effects, remapping/readability | Architecture §§1, 7–9 / Frozen; Gameplay §§9, 17 / Draft-G | P1 | RENDER-002, INPUT-004, AUDIO-003 | Graphics, Input, Audio, Product | ACC-REN-004, ACC-IN-004, ACC-EXP-001 |
| GAME-006 | Debrief, grade, scoring, progression, retry consequences, campaign persistence | Gameplay §§15–16, 18 / Draft-G | P2 | GAME-004, ENGINE-007 | MissionEngine, StorageService | ACC-MSN-002/003 |
| GAME-007 | Deferred comparative target: exceed a pinned F-117A experience in approved measurable categories without weakening absolute F-65 thresholds | Audit brief; Supplement §12 / Proposed-S | P3 | DEC-006, representative build, lawful baseline | Product, Acceptance | TEST-008; §12 matrix |
| GAME-008 | Subjective handling, usability, art/audio, pacing, and final acceptance remain human-owned | Audit brief; Supplement §13 / Proposed-S | P0 | Evidence rubrics | Product/creative/art/audio/test owners | ACC-EXP-001/002 and human sign-off |
| FLIGHT-001 | Player/common aircraft physical state updates on one 100 Hz path; player uses deterministic 6DOF | Gameplay §§2, 7 / Draft-G; Engine §7 / Draft-E | P1 | PERF-001, NUM registry, ENV | FlightDynamicsEngine | ACC-FLT-001, ACC-TIME-001 |
| FLIGHT-002 | Assisted and Manual laws, actuator authority/rates/damage, target handling envelope | Architecture §7 / Frozen; Gameplay §7 / Draft-G | P1 | INPUT-001, FLIGHT-001, human tables | ControlAndSystemsEngine | ACC-FLT-002 |
| FLIGHT-003 | Engines, throttle, sweep, weight/fuel/performance targets use approved tables | Gameplay §§7.4–7.5, 13 / Draft-G | P1 | FLIGHT-001, system/numeric schemas | ControlAndSystemsEngine; FlightDynamics | ACC-FLT-001/002 |
| FLIGHT-004 | Gear/flaps/ADLC, terrain/runway/deck/arrestment/contact are deterministic and swept/bounded | Gameplay §§7.6, 15 / Draft-G; Engine §§6–7 / Draft-E | P2; contact P1 | World/terrain data, ContactEngine | ContactEngine; ControlAndSystems | ACC-CON-001, ACC-FLT-001 |
| FLIGHT-005 | Electrical/fuel/engine/hydraulic/system damage state resolves before control/flight and degrades capability explicitly | Architecture §§3.2, 8 / Frozen; Gameplay §8 / Draft-G | P1 | COMBAT-004, numeric/interfaces | ControlAndSystemsEngine | ACC-FLT-002, ACC-WPN-002 |
| COMBAT-001 | Approved ten-missile/cannon loadout, release authorization, stores/ammunition and fire-control presentation | Architecture §1 / Frozen; Gameplay §§11.1–11.2 / Draft-G | P1 | RADAR-003, INPUT-001 | WeaponAndDamageEngine; Presentation | ACC-WPN-001, ACC-IN-001 |
| COMBAT-002 | Guided missiles use deterministic 3DOF 100 Hz physics, support/autonomy/seeker/fuze/expiry states | Gameplay §11.3 / Draft-G; Engine §7.4 / Draft-E | P1 | FLIGHT numeric, RADAR-003 | WeaponAndDamageEngine | ACC-WPN-001 |
| COMBAT-003 | Cannon uses grouped deterministic ballistics, lead sight, bounded ammunition/projectile groups | Gameplay §§11.2, 11.4 / Draft-G; Engine §7.4 / Draft-E | P1 | COMBAT-004, render cues | WeaponAndDamageEngine | ACC-WPN-001/002 |
| COMBAT-004 | Swept collision/fuze, ordered simultaneous events, accumulated damage, no same-tick slot reuse | Architecture §§3.3, 5 / Frozen; Engine §§6.3, 7.4 / Draft-E | P0 | MEM-003/004, ENGINE-002 | CoreRuntime, Contact, WeaponAndDamage | ACC-DET-003, ACC-CON-001, ACC-WPN-002 |
| COMBAT-005 | RWR/jammer/chaff/flare/notch/decoy defense and damaged-RIO behavior are explicit/deterministic | Gameplay §12 / Draft-G | P1 | RADAR-001/002, INPUT-001, DEC-007 | SensorAndTrack; AI/RIO; WeaponDamage | ACC-RAD-001, ACC-WPN-001, ACC-AI-002 |
| RADAR-001 | Radar/sensors derive deterministic observations from post-motion/post-damage truth, environment, aspect/RCS/clutter/jamming | Architecture §3.2 stage 15 / Frozen; Gameplay §10 / Draft-G | P1 | FLIGHT-001, ENV, numeric registry | SensorAndTrackEngine | ACC-RAD-001 |
| RADAR-002 | Organic/offboard/fused tracks and ID have one physical identity, quality/age/source, sensor-limited readers | Gameplay §§10, 18 / Draft-G; Engine §§9–10 / Draft-E | P1 | RADAR-001, IFACE registry | SensorAndTrackEngine | ACC-RAD-001/002, ACC-AI-001 |
| RADAR-003 | Fire control consumes completed semantic tracks; support/lock/weapon state is independent of display cadence | Gameplay §§10–11 / Draft-G; Supplement CORR-RADAR-001 / Proposed-S | P1 | RADAR-002, COMBAT-002 | SensorAndTrack; WeaponDamage | ACC-RAD-003, ACC-WPN-001 |
| RADAR-004 | Truth/track pools remain bounded (32/24), with stable priority/overflow and player presentation | Architecture §5.2 / Frozen; Gameplay §3.5 / Draft-G | P0 | MEM-003/004, IFACE registry | CoreRuntime; SensorAndTrack | ACC-RAD-002, ACC-MEM-002 |

#### Input, rendering, engine, performance, and memory

| ID | Requirement summary | Source / authority | Pri. | Dependencies | Owner/subsystem | Acceptance |
|---|---|---|---:|---|---|---|
| INPUT-001 | Device-independent semantic command frame covers all axes/actions and four contexts | Architecture §7 / Frozen; Gameplay §5 / Draft-G; CORR-INPUT-001 / Proposed-S | P1 | IFACE registry, human mapping | InputEngine | ACC-IN-001/002 |
| INPUT-002 | Raw keyboard/joystick sampling preserves edges and creates one tick-tagged frame per active tick | Engine §11 / Draft-E; CORR-INPUT-001 / Proposed-S | P0 | PERF-001, Platform ABI | InputEngine, CoreRuntime | ACC-IN-002/003 |
| INPUT-003 | Pause/menu input is out-of-band; pause accrues no active tick debt and resume re-arms controls | Gameplay §4 / Draft-G; CORR-PAUSE-001 / Proposed-S | P0 | ENGINE-002, INPUT-002 | Scheduler, Input, UI | ACC-PAUSE-001 |
| INPUT-004 | Keyboard/joystick defaults, remap/calibration/inversion/digital shaping and discoverability are approved | Gameplay §§5, 17 / Draft-G | P1 | DEC-013, GAME-005 | Input, Settings, Product | ACC-IN-001/004, ACC-EXP-001 |
| RENDER-001 | Incremental software 3D uses one immutable presentation snapshot, no Z-buffer, complete-store swaps only | Architecture §6.1 / Frozen; Engine §8 / Draft-E; CORR-SNAP-001 / Proposed-S | P0 | ENGINE-004, MEM-005 | GraphicsEngine | ACC-REN-001/002/003 |
| RENDER-002 | Cockpit/HUD/MFD/radar/critical warning layers read completed presentation and meet protected deadline/readability | Architecture §§1, 6.4, 9 / Frozen; Gameplay §§9–10 / Draft-G | P1 | GAME-005, RADAR-003 | GraphicsEngine | ACC-REN-002/004 |
| RENDER-003 | Compile-time LOD/impostors/bounds and deterministic shedding fit fixed workspaces and preserve gameplay | Engine §§5, 8.2, 14 / Draft-E | P1 | ASSET manifest, PERF-004 | Graphics, asset compiler | ACC-REN-003/005 |
| RENDER-004 | Two 64 KB display stores, selected mode/encoding and swap/raster behavior stay inside measured ledger | Architecture §§2.1, 6 / Frozen | P0 | R0-B, Platform ABI | Graphics, CoreRuntime | ACC-TIME-002, ACC-REN-002 |
| ENGINE-001 | Target production code is 45GS02 assembly; Java host tools/oracles; modular engine-first development | Architecture §§1, 14 / Frozen; Engine §§0, 16–17 / Draft-E | P0 | TOOL-001, authority corpus | Architecture/Build | ACC-AUTH-001, ACC-BUILD-001 |
| ENGINE-002 | CoreRuntime exclusively owns 100 Hz dispatcher, lifecycle, command/event order, DMA service, RNG/checksum, publication, debt | Architecture §§3, 5 / Frozen; Engine §3.1 / Draft-E | P0 | Platform ABI, MEM, PERF | CoreRuntime | ACC-DET-001/003, ACC-TIME-001/003 |
| ENGINE-003 | Modules have one state owner and communicate only via approved records/queues/handles; no cross-private access | Engine §§3, 14 / Draft-E | P0 | IFACE registry, code ownership | All modules | ACC-ABI-001/002 |
| ENGINE-004 | Presentation extraction/publication is atomic, bounded, immutable, and presentation lag/drop never affects simulation | Architecture §3.2 / Frozen; CORR-SNAP-001 / Proposed-S | P0 | MEM-005, RENDER-001 | CoreRuntime, PresentationExtractor | ACC-REN-001, ACC-DET-001 |
| ENGINE-005 | RNG, arithmetic, checksum, replay, diagnostics, and faults are deterministic/versioned and bounded | Architecture §§3.4–3.6, 10 / Frozen; Engine §15 / Draft-E | P0 | NUM, REPLAY, FAULT registries | CoreRuntime, Diagnostics | ACC-DET-001/002, ACC-FAULT-001 |
| ENGINE-006 | One platform ABI governs IRQ, MAP/base page, DMAgic, Q/extended addressing, hardware math, clobbers/timing | Architecture §2 / Frozen; CORR-PLAT-001 / Proposed-S | P0 | DEC-003, R0-A | CoreRuntime/PlatformABI | ACC-ABI-002/003, ACC-DMA-001 |
| ENGINE-007 | Resources/packages/save/storage are versioned, integrity-checked, bounded, transaction-safe, and non-tactical | Architecture §12 / Frozen; Engine §§4.5, 13 / Draft-E; CORR-STORE-001 / Proposed-S | P0 | MEM-005, TOOL-002 | ResourceManager, StorageService | ACC-STO-001/002 |
| PERF-001 | Active simulation fixed at exactly 100 Hz; results independent of PAL/NTSC/presentation | Architecture §3.1 / Frozen | P0 | ENGINE-002, Platform timer | CoreRuntime | ACC-TIME-001, ACC-DET-001 |
| PERF-002 | No tick skip/merge; renderer yields first; bounded debt and controlled fault | Architecture §§3.6, 6.4 / Frozen | P0 | PERF-003, ENGINE-005 | CoreRuntime, Graphics | ACC-TIME-002/003 |
| PERF-003 | CPU/HUD/render/reserve ledger is proven across independent-clock worst phases including DMA/audio/IRQ | Architecture §6 / Frozen corrected by CORR-TIME-001 / Proposed-S | P0 | R0-D/F, ENGINE-006 | All runtime modules | ACC-TIME-002, ACC-DMA-001 |
| PERF-004 | Presentation tier/camera/effects/cadence cannot affect authoritative state; world 20 Hz is failure floor | Architecture §§6.4, 15 / Frozen; Engine §5 / Draft-E | P0 | RENDER-003, ENGINE-004 | CoreRuntime, Graphics | ACC-REN-002/005 |
| PERF-005 | Input/HUD/audio/loading/frame consistency meet approved absolute F-65 quality thresholds | Supplement §11 / Proposed-S | P1/P2 | Owning R0 evidence and human approval; no F-117A dependency | Product, runtime services | ACC-IN-003, ACC-AUD-001, ACC-STO-001, ACC-REN-002/004 |
| MEM-001 | Canonical physical/CPU ownership map and 32 KB measured reserve are maintained | Architecture §2.1–2.2 / Frozen | P0 | DEC-003, linker ledger | CoreRuntime/Linker | ACC-MEM-001 |
| MEM-002 | Only MemoryAccessABI uses MAP/base-page relocation; canonical entry/exit and static call graph are proved | Architecture §§2.3, 2.6 / Frozen | P0 | ENGINE-006 | MemoryAccessABI | ACC-ABI-002 |
| MEM-003 | Static typed pools have frozen capacities/generations; no heap/growth/same-tick reuse/silent replacement | Architecture §5 / Frozen | P0 | IFACE/memory registry | CoreRuntime | ACC-MEM-002 |
| MEM-004 | Queues/events have generated worst-fan-out proof, stable order, high-water, and deterministic fault/drop | CORR-MEM-001/FAULT-001 / Proposed-S | P0 | COMBAT-004, RADAR-004 | CoreRuntime, producers | ACC-MEM-002, ACC-WPN-002 |
| MEM-005 | Attic is cold/immutable tactically and staged; snapshot/audio/render/resource storage charged to ledgers | Architecture §2 / Frozen; Engine §§4.4–4.5 / Draft-E | P0 | ENGINE-004/007, AUDIO-002 | ResourceManager, Linker | ACC-MEM-001, ACC-AUD-002 |

#### Audio, tools, and tests

| ID | Requirement summary | Source / authority | Pri. | Dependencies | Owner/subsystem | Acceptance |
|---|---|---|---:|---|---|---|
| AUDIO-001 | SID and four PCM channels use one priority/preemption/service contract and cannot affect simulation | Engine §12 / Draft-E; CORR-AUDIO-001 / Proposed-S | P1 | Platform ABI, PERF-003 | AudioEngine | ACC-AUD-001 |
| AUDIO-002 | PCM format/rate/duration/residency/cache/channel data are manifest-bounded and staged to reachable chip RAM | Engine §§4.4, 12, 14 / Draft-E | P1 | ASSET manifest, MEM-005 | AudioEngine, ResourceManager | ACC-AUD-002 |
| AUDIO-003 | Essential warnings meet approved latency/confusion target and have text/SID fallback | Gameplay §§12, 17 / Draft-G; Engine §12 / Draft-E | P1 | GAME-005, AUDIO-001 | AudioEngine, Graphics | ACC-AUD-001, ACC-EXP-001 |
| TOOL-001 | macOS KickAssembler/Java/Xemu workflow is pinned, reproducible, non-interactive, and emits evidence | Architecture §§10, 11, 17 / Frozen; Engine §§16–17, 21 / Draft-E | P0 | Authority/platform manifests | Build/tooling | ACC-BUILD-001/002 |
| TOOL-002 | Host compilers validate/generate mission, asset, interface, resource/package and D81 artifacts with bounds | Engine §§13–14 / Draft-E | P0 | MEM, ASSET/MISSION schemas | Host tools | ACC-ABI-001, ACC-MSN-001, ACC-STO-001 |
| TOOL-003 | Xemu is routine regression; physical MEGA65 is mandatory for hardware-sensitive closure | Architecture §§10–11, 14 / Frozen; Supplement §9.10 / Proposed-S | P0 | DEC-003, evidence schema | Test/platform | All hardware-marked acceptance IDs |
| TOOL-004 | Spec/build/package/core/tool identities and approval status are machine-readable and retained | `CORR-AUTH-001/002`, `CORR-REF-001`, `CORR-TOOL-001`, `CORR-TEST-001` / Proposed-S | P0 | TOOL-001 | Configuration management | ACC-AUTH-001/002, ACC-BUILD-002 |
| TEST-001 | High-precision and bit-exact host references plus target golden vectors prove deterministic math/state | Architecture §10 / Frozen | P0 | NUM/IFACE registries | Test/oracles | ACC-DET-001/002, ACC-FLT-001 |
| TEST-002 | Replay and snapshot/pause tests prove canonical state, publication isolation, and active-time semantics | Engine §15 / Draft-E; Supplement CORR-* / Proposed-S | P0 | ENGINE-004/005, INPUT-003 | Test/runtime | ACC-DET-001/002, ACC-REN-001, ACC-PAUSE-001 |
| TEST-003 | Performance harness records per-module clocks, phases, DMA/IRQ/audio, high-waters and reserve under legal peaks | Architecture §§6, 10 / Frozen; Engine §§5, 15 / Draft-E | P0 | R0, PERF/MEM | Test/platform | ACC-TIME-002, ACC-MEM-001 |
| TEST-004 | Long-run hardware soak demonstrates stability and reliability | Supplement §11 / Proposed-S | P1 | Phase 1/slice | Test/platform | ACC-STAB-001 |
| TEST-005 | Fault injection covers every invariant/overflow/resource/platform code and recovery | CORR-FAULT-001 / Proposed-S | P0 | Fault catalog | All owners/Test | ACC-FAULT-001 |
| TEST-006 | Storage/load/save/media failure and recovery are proven on physical devices | CORR-STORE-001 / Proposed-S | P1 | ENGINE-007, DEC-012 | Storage/Test | ACC-STO-001/002 |
| TEST-007 | Technical slice proves build→flight→radar→combat→AI→presentation→evidence vertical chain | Supplement §14.2 / Proposed-S | P1 | R0-F, Phase 1, approved data | Program/Product/Test | §14.2 exits |
| TEST-008 | Deferred pinned F-117A comparison uses absolute and relative measures without copying protected expression | Supplement §12 / Proposed-S | P3 | DEC-006, representative content; no R0/Phase 1 dependency | Product/Acceptance | §12 matrix |

### A.3 End-to-end cross-document traceability

`Broken` means at least one required link is absent or unapproved; it does not mean the underlying design intent is poor.

| Player experience | Gameplay rule / requirement | Engine capability | Data or asset requirement | Implementation task/module | Test / acceptance | Link status and finding |
|---|---|---|---|---|---|---|
| Immediate, predictable control | Four contexts, Assisted/Manual, complete actions (`INPUT-*`, `FLIGHT-002`) | Raw-to-semantic latch; control law→actuator | Mapping/shaping/calibration registry | InputEngine; ControlAndSystems | ACC-IN-001–004, ACC-FLT-002 | **Broken:** axes/actions/frame semantics and human shaping absent; FND-CRT-005 |
| Smooth, deterministic flight | 100 Hz 6DOF and aircraft envelope (`FLIGHT-001/003`) | Fixed-step flight, atmosphere, systems | Numeric formats; aero/engine/weight tables | Environment; FlightDynamics; Systems | ACC-FLT-001/002, ACC-TIME-001 | **Broken:** coefficients/formats/tolerances TBD; FND-CRT-004/009 |
| Safe pause and restart | Full pause/restart/no acceleration (`GAME-003`, `INPUT-003`) | Scheduler active/pause state; replay event | Initial-state/seed and input re-arm rules | CoreRuntime; UI; Mission | ACC-PAUSE-001, ACC-MSN-003 | **Broken but corrected in proposal:** FND-CRT-006 |
| Readable cockpit and HUD | Cockpit-primary, warning hierarchy (`GAME-005`, `RENDER-002`) | Protected overlay independent of world | Glyph/layout/palette/lighting asset manifest | GraphicsEngine; asset compiler | ACC-REN-002/004 | **Broken:** display/glyph/readability budgets R0/Human; FND-MAJ-009 |
| Stable world view | ≥20 Hz failure floor, complete frames (`RENDER-001/003/004`) | Incremental painter/span/DMA renderer | Mode, mesh LOD/impostor/envelope | GraphicsEngine; converters | ACC-TIME-002, ACC-REN-001–003 | **Broken:** timing model/mode/assets; FND-CRT-001, FND-MAJ-008 |
| Radar situational awareness | Search/detect/track/ID/fusion/overflow (`RADAR-001/002/004`) | Sensor/track stage 15; capacity policy | Sensor tables, scan schedule, canonical records | SensorAndTrack; display | ACC-RAD-001/002 | **Broken:** tables/cadence/ABI; FND-CRT-003/009 |
| Target and employ weapons | Priority/lock/support, missiles/gun (`RADAR-003`, `COMBAT-001–003`) | Fire-control track consumer; weapon physics/events | Guidance/fuze/ballistic/loadout/cue data | WeaponDamage; Graphics/Audio | ACC-WPN-001/002, ACC-RAD-003 | **Broken:** tables/event bounds/cue asset specs; FND-CRT-009/010 |
| Defend against threats | RWR/jammer/decoy/notch/RIO (`COMBAT-005`) | Sensor warnings; decoy scoring; AI RIO | Defense tables, cues, fallback control | SensorTrack; AI; WeaponDamage; Input | ACC-WPN-001, ACC-AI-002, ACC-AUD-001 | **Broken:** damaged-RIO/manual path and data unresolved; FND-MAJ-013 |
| Credible enemies/wingman | Sensor-limited deterministic doctrine (`GAME-002`) | Blackboard, scheduled utility/doctrine | Doctrine sets, schedule, tie/fallback cases | AIEngine | ACC-AI-001/002 | **Broken:** AI-01 TBD; FND-CRT-009 |
| Carrier/airfield operations | Catapult/deck/ADLC/wires/grade (`FLIGHT-004`, `GAME-006`) | Moving-frame contact, systems, mission grade | Carrier mesh/query/contact/LSO tables | Contact; Flight; Mission; Graphics | ACC-CON-001, ACC-FLT-001 | **Broken:** tables/assets/tolerances and slice role; FND-MAJ-014 |
| Meaningful missions/campaign | Midnight Spear, ten ops, two endings (`GAME-004/006`) | Declarative graph/compiler/runtime/save | Ten-row mission/campaign/asset manifest | Mission compiler/engine; Storage | ACC-MSN-001–003 | **Broken:** slice and 8 operations/endings absent; FND-MAJ-001/002 |
| Clear audio feedback | Warning/RIO/engine/combat cues (`AUDIO-*`) | SID+four PCM, priority, text fallback | Audio manifest/rates/cache/residency | AudioEngine; ResourceManager | ACC-AUD-001/002 | **Broken:** channel/content/budget contract; FND-MAJ-010 |
| Fast reliable flow | Boot/title/load/save/transition (`GAME-003`, `ENGINE-007`) | Package loader, ResourceManager, StorageService | D81/file/package/save manifest | Build; Storage; Resource | ACC-STO-001/002 | **Broken:** fit/load/failure/transaction absent; FND-CRT-008 |
| Stable/replayable experience | Determinism, checksums, both endings (`ENGINE-005`, `TEST-*`) | Replay/diagnostics and canonical serialization | Replay schema, seeds, campaign branches | CoreRuntime; Diagnostics; Test | ACC-DET-001/002, ACC-STAB-001 | **Broken:** canonical checksum/replay/content absent; FND-MAJ-011 |
| Deferred comparison with F-117A experience | Measured quality categories (`GAME-007`) | Instrumentation and representative build | Pinned legal reference/captures/rubric | Acceptance/Product | §12 matrix | **Deferred, non-blocking:** identity/baseline not approved; FND-MAJ-012. Absolute F-65 criteria remain active. |

### A.4 High-risk “looks functional but violates intent” checks

An AI-generated build can compile and look plausible while being wrong if it:

- updates offscreen AI/aircraft less often than 100 Hz;
- lets renderer traversal order or frame completion affect collision, sensor, or RNG results;
- reads mutable simulation arrays rather than one acquired presentation snapshot;
- maps or relocates base page inside a module for convenience;
- uses floating point or different rounding in target-authoritative calculations;
- loses short input edges or makes PAL/NTSC produce different command frames;
- updates radar semantics at display cadence or gives AI access to truth;
- immediately reuses a despawned slot or silently evicts a live entity;
- drops authoritative events when a fixed buffer fills;
- treats hardware DMA submission as nonblocking merely because software does not poll it;
- serializes raw memory/pointers/padding into saves or checksums;
- reads mission assets from disk during tactical play;
- consumes the measured-limits reserve to make an unmeasured feature fit;
- changes a `TBD` coefficient until a test passes current code rather than approved intent; or
- declares the benchmark passed from screenshots, nominal resolution, or subjective recollection.

## Appendix B — Complete Findings Register

Replacement text is provided directly in §6. A reference such as “Use `CORR-X`” incorporates that insertion-ready language into the finding. `Human: Yes` identifies the approval needed; `Auto: Yes after approval` means the remaining edit is low-risk and mechanically verifiable.

Finding IDs remain stable across revisions. Their `BLK`/`CRT` prefix records the v0.1 classification and is not silently renamed when v0.2 changes severity. The displayed severity is current. “Blocks current milestone?” refers to the authorized pre-R0/R0-A horizon; the closure gate determines when the finding becomes a hard stop.

### B.1 High-risk findings and reclassified v0.1 findings

| Finding | Type | Affected source / requirements | Exact problem, why it matters, and likely failure | Correction and proposed replacement | Validation / acceptance | Approval / auto | Blocks current milestone? | Required closure gate |
|---|---|---|---|---|---|---|---|---|
| **FND-BLK-001 — Blocker** | Documentation defect; AI-readiness gap | Architecture front matter, §1; all requirements, especially ENGINE-001/GAME-001 | Revision 1.4.1 says it retains a complete Revision 1.4, but 1.4 was not supplied. The reviewed file may be only a delta; engineers cannot distinguish omitted requirement from deliberate freedom. Likely failure: a coherent implementation violates a preserved but unseen constraint and requires architectural rework. | Use `CORR-AUTH-001`: consolidate 1.4.1 or supply/hash the incorporated 1.4 and delta. | ACC-AUTH-001; independent corpus review confirms every active requirement is present. | Human: Product + Architecture. Auto: Yes after chosen corpus is supplied. | **No for independent proof work; yes for formal acceptance** | Gate 0, before R0-A is accepted |
| **FND-BLK-002 — Major (reclassified from Blocker)** | Authority contradiction; scope risk | Gameplay front/§0; Engine front/§0; all Draft-G/E requirements | Both candidates use normative/binding language but are not approved, and Engine depends on Gameplay. Draft statements cannot authorize autonomous product behavior. Likely failure: code and assets freeze around choices later rejected by human owners. | Use `CORR-AUTH-002`: keep them controlled living drafts; prohibit release/gameplay production from Draft inputs and approve each before its consuming production phase. | ACC-AUTH-002; spec manifest and approval signatures. | Human: Product + Architecture. Auto: No. | No | Before Gameplay/Engine approval or any gameplay merge; no later than R0-F |
| **FND-BLK-003 — Blocker** | Contradiction; integration/performance risk | Architecture §§3.1–3.2; Gameplay §18; Engine §§3.3, 4.3, 8.1; ENGINE-004, MEM-005, RENDER-001 | Renderer may retain an old immutable snapshot while new ones publish, but schema, buffer count, storage, states, acquisition/release, and overwrite are absent. The 1 KB snapshot assembly allocation does not prove storage. Likely failure: torn/mixed frames, renderer/sim race, overwrite, simulation stall, or hidden memory overflow. | Use `CORR-SNAP-001`: bounded extracted presentation snapshots, explicit state machine, skip/coalesce presentation only, charge buffers to memory. | ACC-REN-001, ACC-MEM-001; forced multi-frame render delay and canaries. | Human: Architecture. Auto: No; design choice. | No | Before snapshot/interface freeze and Phase 1 integration |
| **FND-CRT-001 — Critical** | Technical correction; performance risk | Architecture §§3.1, 6.2–6.3; Engine §5; PERF-001–003 | “Six NTSC frames” are not exactly ten 100 Hz ticks using official geometry; phases drift and a chosen two-frame window can intersect four ticks. Likely failure: an average ledger passes while a legal phase causes tick debt, input/audio miss, or stutter on hardware. | Use `CORR-TIME-001`: independent clocks; per-tick/per-display and worst-phase rolling admission. | ACC-TIME-001/002 on physical PAL/NTSC targets with phase sweep. | Human: Architecture + Platform. Auto: No. | **Correction required by current harness design; does not stop unrelated work** | Corrected model before timing-harness acceptance; measured limits at R0-F |
| **FND-CRT-002 — Major (reclassified from Critical)** | Documentation defect; current-milestone deliverable gap | Engine §21.1; TOOL-001/004 | Engine says bootstrap artifacts are published, but no such repository files are present. Likely failure: agents hand-create incompatible schemas/builds while believing a canonical source exists. | Use `CORR-TOOL-001`; remove “published” or produce paths/artifacts/hashes and validation command as the authorized milestone work. | ACC-BUILD-001/002; clean checkout locates and regenerates all named artifacts. | Human: Architecture/tooling contract; Auto: artifacts after approval. | **Yes—this is work to perform, not a stop-work order** | R0-A |
| **FND-CRT-003 — Major (reclassified from Critical)** | Contradiction; integration risk | Gameplay §18; Engine §§3, 14.3; all module interfaces | Logical records differ in name/coverage (`TrackQuality`/`RadarTrackState`, `WeaponGuidanceState`/`MissileGuidanceState`); required gameplay states lack engine owners. Engine also conflicts on DMA/resource manager naming. Likely failure: binary-incompatible modules, duplicated state, wrong owner, or adapters that alter semantics. | Use `CORR-IFACE-001` plus §10.1: one canonical registry; reconcile the current initial subset now and each later record before its consuming interface freezes. | ACC-ABI-001/002; generated-offset and ownership/static-access checks. | Human: Product semantics + Architecture ABI. Auto: generation only after decisions. | **Initial subset only** | Initial generator at R0-A; complete relevant records before Phase 1 or their consuming phase |
| **FND-CRT-004 — Major (reclassified from Critical)** | Missing requirement; phase-gated AI-readiness gap | Architecture §4; Engine §§6–7, 14; FLIGHT/RADAR/COMBAT records | NED/WorldPosition are defined, but orientation, angles/rates, velocity, force/moment, ranges, interpolation, rounding, saturation, transform order, and invalid arithmetic are not. Likely failure: individually plausible modules disagree at boundaries or diverge slowly from host truth. | Use `CORR-NUM-001`: field-level numeric/frame registry with exception rules and golden extrema. Only fields consumed by the current interface subset must be defined now. | ACC-ABI-003, ACC-FLT-001, ACC-CON-001, ACC-RAD-001. | Human: Architecture; flight tolerances also Product. Auto: No. | No | Before Phase 2 numeric/flight interface freeze; earlier for any field consumed by Phase 1 |
| **FND-CRT-005 — Major (reclassified from Critical)** | Missing requirement; creative decision required | Gameplay §5; Engine §11; INPUT-001–004 | Durable action list omits/unfreezes core axes, taxi, full throttle, views, pause/menu navigation, edge/hold/repeat/device arbitration and command-frame layout. Likely failure: different agents invent incompatible controls, lose short edges, or make required taxi/view behavior inaccessible. | Use `CORR-INPUT-001`; define the initial record envelope now, complete semantics for input proof, and defer final defaults/shaping to human tuning. | ACC-IN-001–004 under peak load on keyboard and joystick. | Human: Product/accessibility for defaults/shaping; Architecture for frame. Auto: No. | **Initial record envelope only** | Initial ABI at R0-A; complete semantics R0-B/Phase 1; feel/defaults Phase 2 |
| **FND-CRT-006 — Major (reclassified from Critical)** | Contradiction; determinism risk | Architecture §3.1; Gameplay §4; PERF-001, INPUT-003 | Exact monotonic 100 Hz is not reconciled with full pause. If wall deadlines continue, pause creates debt; if ticks continue, simulation is not frozen. Held inputs also leak on resume. | Use `CORR-PAUSE-001`: active-time tick, no paused debt, boundary entry, edge re-arm, replay event. | ACC-PAUSE-001 and ACC-MSN-003. | Human: Product + Architecture. Auto: Yes after approval. | No | Before Phase 1 scheduler/replay integration |
| **FND-CRT-007 — Critical** | Missing requirement; performance/integration risk | Architecture §2; Engine §§3–5, 8, 12; ENGINE-006 | No unified IRQ priority/ack/nesting/masked-duration, DMA blocking/completion, Q/clobber, extended-address, or multiply/divide ABI exists. Core-versus-DMAManager ownership conflicts. Likely failure: corrupt registers/mapping, missed 100 Hz deadlines, uninterruptible batches, or emulator-only correctness. | Use `CORR-PLAT-001`: generated platform ABI and wrapper proofs on pinned core. | ACC-ABI-002/003, ACC-DMA-001, ACC-TIME-002. | Human: Architecture + Platform. Auto: No. | **Yes—the milestone exists to close it** | R0-A |
| **FND-CRT-008 — Major (reclassified from Critical)** | Missing requirement; phase-gated integration/reliability risk | Architecture §§1, 12; Gameplay §4; Engine §§4.5, 13; ENGINE-007/TOOL-002 | D81/package/resource/save requirements lack disk byte allocation, format/integrity, boot/reclaim sequence, residency fit, loading threshold, transactional save, migration and media failures. Likely failure: build works on host but does not fit/boot/load/save safely on physical media. | Use `CORR-STORE-001`: disk manifest, bounded packages, preload, transactional two-generation save, failure matrix. The R0-A proof D81 needs only its reproducible proof-specific manifest. | ACC-STO-001/002; hardware boot/load/fault tests. | Human: Architecture + Product recovery UX. Auto: No. | No, except proof-D81 reproducibility | R0-C before storage/resource integration; full save UX before campaign work |
| **FND-CRT-009 — Major (reclassified from Critical)** | Missing requirement; phase-gated creative decisions | Gameplay §§7, 10–16, 19; Engine §§6–10, 18; FLIGHT/RADAR/COMBAT/GAME-002/004 | Consequential coefficients/tables/doctrine/mission data are explicitly TBD: flight, control, ADLC, engine/fuel, radar, weapons, defense, carrier, AI, campaign. That is acceptable sequencing but not autonomous-production readiness. Likely failure: AI invents feel, difficulty, outcomes, campaign, or “goldens” current behavior. | Close each source TBD before its first shipping consumer; use `CORR-CAMP-001`, `CORR-MISSION-001`, and `CORR-RADAR-001` plus `DEC-008`–`DEC-010`. “TBD data may drive only clearly labeled fixtures, never shipping behavior.” | Applicable `ACC-FLT-*`, `ACC-RAD-*`, `ACC-WPN-*`, `ACC-AI-*`, `ACC-MSN-*`, and `ACC-EXP-*` groups. | Human: Product/creative; Architecture/test for encoding/evidence. Auto: No. | No | Before each consuming Phase 2–5 module; campaign content before Phase 4 production |
| **FND-CRT-010 — Major (reclassified from Critical)** | Performance/integration risk; testability gap | Architecture §§3.3, 5; Engine §§4.3–4.3.1; MEM-004, COMBAT-004 | The 2 KB event buffer and “worst legal tick event set” have no derivation across weapon requests, swept contacts, fuzes, damage fan-out, spawns, mission events, warnings, and presentation events. Likely failure: a legal peak silently drops damage/events or corrupts memory. | Use `CORR-MEM-001` and `CORR-FAULT-001`: enumerate producers/fan-out, generate capacity, test one-over, no silent authoritative drop. | ACC-MEM-002, ACC-WPN-002, ACC-FAULT-001. | Human: Architecture. Auto: No. | No | R0-E and before the Phase 1 combined harness |

### B.2 Major findings

| Finding | Type | Affected source / requirements | Exact problem, why it matters, and likely failure | Correction and proposed replacement | Validation / acceptance | Approval / auto | Blocks current milestone? | Required closure gate |
|---|---|---|---|---|---|---|---|---|
| **FND-MAJ-001 — Major** | Scope/testability gap | Architecture §§1, 17; Gameplay §16; GAME-004/TEST-007 | Midnight Spear is named as the vertical slice but has no mission identity, objectives, assets, load, start/end, duration, or tests. Likely failure: teams build different slices or count a harness as product completion. | Use `CORR-MISSION-001` and §14.2; separate Technical Combat Slice from narrative mission. | §14.2 exits; approved mission manifest for Midnight Spear. | Human: Product/creative. Auto: No. | No | Before Midnight Spear implementation/acceptance |
| **FND-MAJ-002 — Major** | Missing requirement; creative/scope risk | Gameplay §16; GAME-004/006 | Only opening two operations are sketched; remaining eight, ending predicates, progression/scoring/retry consequences and content assets are absent. Likely failure: campaign code hard-codes invented branches or late content breaks saves/budgets. | Use `CORR-CAMP-001`: ten-row approved campaign manifest. | ACC-MSN-001–003 and branch replay coverage. | Human: Product/creative. Auto: No. | No | Before Phase 4 campaign production |
| **FND-MAJ-003 — Major** | Missing requirement; reliability risk | Architecture §§3.6, 5, 12; Engine §§5, 13, 15; ENGINE-005 | “Controlled performance pause” and release invariant handling lack exact state transition/player result; external/resource/media failures are fragmented. Likely failure: debug stop becomes release hang, normal save captures corrupt state, or modules recover differently. | Use `CORR-FAULT-001`; one catalog with deterministic detection/recovery. | ACC-FAULT-001. | Human: Architecture + Product UX. Auto: No. | No; fault-schema scaffolding may proceed | Technical fault path before Phase 1; player-facing recovery before release |
| **FND-MAJ-004 — Major** | Performance/memory risk | Engine §4.3; MEM-003–005 | 32 KB active-simulation ledger is arithmetically exact but has no slack for alignment/schema changes/guards and does not prove 320-byte aircraft records support all common behavior. Likely failure: late schema growth consumes another owner/reserve or uses opaque packed hacks. | Use `CORR-MEM-001`; generated record/ledger proof. Add: “A record’s byte estimate is not frozen capacity until every required field maps to it.” | ACC-MEM-001/002; semantic field-to-byte audit. | Human: Architecture. Auto: No. | **Ledger subset is current work; semantic completeness is not** | Generated ledger at R0-A; full schema/peak proof at R0-E/Phase 1 |
| **FND-MAJ-005 — Major** | Testability/performance gap | Gameplay §3.3; Engine §13; GAME-004/TOOL-002 | Mission compiler must prove conservative concurrency but graph restrictions, branch merge/loop semantics, analysis algorithm, event fan-out, and witness format are undefined. Likely failure: unsound acceptance or overconservative rejection and late runtime overflow. | Proposed text: “Mission graphs are finite and statically bounded; loops declare max iterations/concurrency; compiler computes per-resource may-live maxima over legal branches and emits a witness path; unknown dynamic count is a build error.” | ACC-MSN-001 against hand-proven adversarial fixtures. | Human: Architecture/tooling. Auto: No. | **Skeleton only** | Schema/capacity skeleton at R0-A; sound complete analyzer before Phase 1 mission fixtures |
| **FND-MAJ-006 — Major** | Ambiguity; performance risk | Architecture §§2.1, 6, 13.1; Engine §8; RENDER-004 | Display-store size is frozen but pixel/glyph format, stride, visible dimensions, page/swap/raster mode and overlay composition are R0-gated. Likely failure if implementation assumes 8-bpp linear high-resolution or assets freeze prematurely. | Proposed text: “Display resources remain opaque until R0-B freezes mode descriptor `{width,height,stride,packing,planes,palette,stores,swap_line,overlay}` and measured limits.” | ACC-REN-002/004 and hardware capture/timing. | Human: Platform + Product/art. Auto: No. | No | R0-B display-mode selection |
| **FND-MAJ-007 — Major** | Performance risk | Architecture §6; Engine §8; RENDER-001/003 | Renderer plan is credible but clear/overdraw/DMA/list/clip costs are estimates; carrier/painter intersections and transparent effects are high risk. Likely failure: cadence below 20 Hz or repeated abort/shedding at legal scenes. | §9.4 prototype language; add per-stage cycle/byte/high-water counters and representative worst scenes before mode freeze. | ACC-REN-002/003, ACC-TIME-002. | Human: Architecture/platform for limits. Auto: No. | No | R0-D/F before production renderer/Phase 1 closure |
| **FND-MAJ-008 — Major** | Missing requirement; integration risk | Engine §§8, 12, 14; GAME-001/005 | Source formats exist but exhaustive asset IDs, LOD/topology/image/audio envelopes, license/provenance, residency and fallbacks do not. Likely failure: individually valid assets overflow RAM/D81/render/audio budgets or lack required gameplay cues. | Use `CORR-ASSET-001`. | Asset compiler rejection tests; aggregate MEM/D81 fit; art/audio acceptance. | Human: Art/audio + Architecture. Auto: No. | No; budget-valid proxy work permitted | Representative slice asset lock; complete manifest before content production |
| **FND-MAJ-009 — Major** | Testability/creative gap | Architecture §§6.4, 9; Gameplay §§9, 17; GAME-005/RENDER-002 | “Readable,” “clear,” “glanceable,” and visual warning behavior lack glyph sizes, contrast, occlusion, viewing conditions, task/error rubrics and degraded-tier minima. Likely failure: polished display is illegible on actual monitor or shedding hides threats. | Proposed text: “For every display tier, list mandatory cues and approved viewing/capture conditions; pass ACC-REN-004 and a task interpretation test before layout freeze.” | ACC-REN-004, ACC-EXP-001. | Human: Product/accessibility/art. Auto: No. | No | R0-B candidate selection for technical limits; final human rubric before slice acceptance |
| **FND-MAJ-010 — Major** | Missing requirement; performance risk | Engine §12; AUDIO-001–003 | SID/PCM ownership is conceptual; sample format/rate/duration, channel plan, 12 KB cache allocation, contention, latency and fallback are absent. Likely failure: audio glitches/misses deadlines, RIO content does not fit, or essential warnings are preempted. | Use `CORR-AUDIO-001` and `CORR-ASSET-001`. | ACC-AUD-001/002 on hardware. | Human: Audio/product + Platform. Auto: No. | No | R0-B audio proof; content plan before representative slice |
| **FND-MAJ-011 — Major** | Testability gap | Architecture §10; Engine §15; TEST-001/002 | Replay/checksum promises omit canonical field order/scope/padding/RNG/free-list, algorithm/cadence, compatibility and first-difference format. Likely failure: cross-build false mismatches or nondeterminism hidden outside checksum. | Use `CORR-REPLAY-001`. | ACC-DET-001/002. | Human: Architecture/test. Auto: Generator after approval. | No; schema scaffolding permitted | Before Phase 1 determinism acceptance |
| **FND-MAJ-012 — Advisory (reclassified from Major)** | Ambiguity; testability/benchmark gap | Audit benchmark requirement; GAME-007/TEST-008 | Exact F-117A title/revision and A1200 environment are unpinned; historical sources do not show native A1200/AGA minimum. Likely failure: unrepeatable comparison or unsupported marketing claim. | Use `CORR-BENCH-001`, §12, `DEC-006`; absolute F-65 thresholds remain primary. | Pinned baseline capture and category matrix. | Human: Product/acceptance/legal. Auto: No. | No—explicitly non-blocking for pre-R0, R0, and Phase 1 | Before any comparative claim or representative release benchmark |
| **FND-MAJ-013 — Major** | Missing requirement; creative decision required | Gameplay §§5, 12, 14; COMBAT-005/INPUT-001 | Manual decoy binding is optional/preferred while RIO automatic behavior is required; behavior when RIO/systems are damaged/unavailable is not defined. Likely failure: player loses defense without feedback/control or different implementations expose different agency. | `DEC-007`; proposed hybrid emergency action and explicit degraded state. | ACC-AI-002, ACC-WPN-001, ACC-IN-001. | Human: Product. Auto: No. | No | Before Phase 3 defense/input behavior freeze |
| **FND-MAJ-014 — Major** | Missing requirement; integration risk | Gameplay §§7.6, 15, 19; Engine §§6–7; FLIGHT-004 | Carrier/deck/wire/contact/LSO targets exist but geometry frames, tolerances, contact shapes, tie rules, table data and asset bounds remain TBD. Likely failure: visual deck and physical deck disagree, tunneling/bolter grades vary, or vertical slice is blocked. | Use numeric/contact registry; keep carrier out of Technical Combat Slice; close CV-01 before narrative carrier slice. | ACC-CON-001, ACC-FLT-001, carrier-specific grade vectors. | Human: Product/flight + Architecture. Auto: No. | No | Phase 2 carrier/contact gate before narrative carrier slice |
| **FND-MAJ-015 — Major** | AI-readiness/testability gap | Gameplay §§7.2–7.3, 17, 20.5; FLIGHT-002/INPUT-004 | Novice/pilot feel acceptance is subjective without reviewer qualifications, sample, tasks, rubric, version lock and rejection threshold. Likely failure: an agent tunes to its own heuristic or cherry-picks playtest comments. | `DEC-009/013`; proposed locked rubric and named product owner/panel. | ACC-FLT-002, ACC-EXP-001/002. | Human: Product. Auto: No. | No | Before Phase 2 tuning acceptance and slice handling approval |
| **FND-MAJ-016 — Major** | Missing requirement; reliability gap | Gameplay §§4, 16; GAME-003/006 | Restart Sortie/tutorial restart do not define RNG seed, mission/campaign mutations, rewards, save writes, debrief/grade or input state. Likely failure: reward duplication, different replay, or persistent failure state. | Proposed text: “Restart restores the manifest’s initial authoritative state/seed and clears uncommitted sortie effects; committed campaign state changes only at approved debrief transaction.” | ACC-MSN-003, ACC-PAUSE-001. | Human: Product + Architecture. Auto: No. | No | Before restart enters the Technical Slice; campaign effects before Phase 4 |
| **FND-MAJ-017 — Major** | Ambiguity; integration risk | Architecture §6.4; Gameplay §§10, 19; Engine §9; RADAR-001–003 | Sensor scan, track semantic update and display refresh/immediate critical cue cadences are not separated numerically. Likely failure: display settings alter detection or AI/fire control, or “immediate” creates unscheduled state updates. | Use `CORR-RADAR-001`. | ACC-RAD-001/003. | Human: Product display feel + Architecture semantics. Auto: No. | No | Phase 3 radar interface/behavior gate |
| **FND-MAJ-018 — Major** | Missing requirement; integration risk | Architecture §4.3; Gameplay §6; Engine §6; FLIGHT-004/RADAR-001 | World area target exists but terrain tile/query encodings, scale, continuity, water/ground material, height precision, LOS/contact bounds and sector-edge behavior are not defined. Likely failure: renderer, physics, radar and mission compiler use different terrain truths. | Proposed text: “One generated terrain schema owns height/material/feature/LOS/contact queries; renderer resources derive from it and cannot be authoritative.” | ACC-CON-001, ACC-RAD-001, sector-boundary vectors. | Human: Architecture; product for map content. Auto: No. | No | Before Phase 1 world/query integration |
| **FND-MAJ-019 — Major** | Ambiguity; compatibility risk | Architecture §2; Engine §4.5; MEM-005 | “Normally 8 MB Attic” is treated as available, but minimum machine/model configuration and fallback/exclusion are not declared. Likely failure: boot/runtime failure on a development configuration without required Attic memory. | Use `CORR-REF-001`, `DEC-003`; probe and reject unsupported configuration clearly. | Boot/memory probe across support matrix. | Human: Product/platform. Auto: No. | **Yes** | R0-A support matrix and identity probe |
| **FND-MAJ-020 — Major** | Testability gap; hardware risk | Architecture §§10–11, 14; Engine §§18–19; TOOL-003 | Sources correctly require hardware gates but do not enumerate which behaviors Xemu cannot close or the physical device/core matrix. Likely failure: emulator results silently become release evidence. | Use §9.10 and `CORR-TEST-001`; tag every acceptance environment. | Evidence linter rejects missing hardware identity for hardware-gated IDs. | Human: Platform/test. Auto: Yes after matrix approval. | **Yes for R0-A evidence identity** | R0-A, then each later hardware gate |
| **FND-MAJ-021 — Major** | Integration risk; architecture ambiguity | Engine §§3.1–3.2, 4.5, 8.1; ENGINE-003/006/007 | CoreRuntime, `DMAManager`, `ResourceManager`, and `ResourceAndDiagnostics` ownership names conflict; some are absent from module graph. Likely failure: direct DMA/resource mutations or circular service calls. | §10.1 resolution: Core-owned DMAService, sole ResourceManager, read-only Diagnostics; generate entry points. | Ownership/static-call-graph tests and ACC-ABI-002. | Human: Architecture. Auto: No. | **Initial platform/service ownership only** | R0-A for platform/DMA ownership; complete module graph before Phase 1 |
| **FND-MAJ-022 — Major** | Missing requirement; performance risk | Architecture §§2, 12; Engine §§4, 13; ENGINE-007 | Post-ROM-reclaim boot/hypervisor/FDC/storage transition and error recovery are not defined. Likely failure: display memory overwrites ROM while later code still relies on it, or physical disk I/O fails after boot. | Proposed text: “R0-C records the last ROM/hypervisor-dependent operation, release handshake, post-release I/O path, re-entry prohibition/recovery, and memory test before display-store ownership begins.” | Hardware boot/load/save across reclaimed region with guards. | Human: Platform/architecture. Auto: No. | No; R0-A may probe without freezing storage path | R0-C |
| **FND-MAJ-023 — Major** | Scope/integration risk | Architecture §1; Gameplay §§3, 16; GAME-001/004 | One bootable MVP D81 and multi-D81 campaign are both permitted, but “MVP” content boundary, campaign split, disk-swap state and save-space ownership are not defined. Likely failure: late package split changes transitions/assets or no writable space remains. | `CORR-STORE-001`, `DEC-012`, and `DEC-015`; add a release disk manifest with required content and swap protocol. | ACC-STO-001/002 and full campaign install/swap walkthrough. | Human: Product + Architecture. Auto: No. | No | Before representative content/package lock; final split before release build |
| **FND-MAJ-024 — Major** | Technical debt risk | Engine §§16–17; all phase TBDs | Engine-first gates are sound, but interfaces are allowed to freeze at disparate phases without a compatibility/migration policy; AI agents may add adapters and duplicate records to make progress. | Proposed text: “A phase may extend private data, but public ABI change requires registry version, impact matrix, migration, all dependent rebuild/tests, and architecture approval.” | ACC-ABI-001 and clean dependency graph each phase. | Human: Architecture. Auto: Yes for mechanical impact reports. | No; initial versioning scaffold may proceed | Before first public ABI freeze; enforced at every later interface change |

### B.3 Minor and Advisory findings

| Finding | Type | Affected source / requirements | Exact problem, likely failure | Correction / replacement | Validation | Approval / auto | Blocks current milestone? | Required closure gate |
|---|---|---|---|---|---|---|---|---|
| **FND-MIN-001 — Minor** | Documentation defect | All sources | No stable requirement IDs exist in source text, so prose changes cannot trace reliably to code/tests. Likely failure: stale citations and duplicate interpretation. | Adopt Appendix A IDs; insert them beside normative groups at next approved revision without renumbering. | Link checker: every public task/test references valid IDs. | Delegated documentation batch after ID map approval. | No | Before the affected source is promoted to Approved |
| **FND-MIN-002 — Minor** | Documentation defect | All front matter/decision logs | Source files lack exact publication date/hash/approver identity and approval scope. Likely failure: two agents use same title/version with different bytes. | Add document-control table equivalent to §1 and spec-set manifest. | ACC-AUTH-001/002. | Delegated documentation/configuration batch. | No | Before approved baseline/release labeling |
| **FND-MIN-003 — Minor** | Ambiguity | All sources | Terms such as snapshot, truth, observation, track, priority, physical entity, dynamic mission entity, MVP and vertical slice can be read differently. | Adopt Appendix D glossary; generated schema names control technical usage. | Documentation glossary/link lint. | Delegated batch after definitions receive owning-role approval. | No | Before each affected public interface/content brief freezes |
| **FND-MIN-004 — Minor** | Testability gap | Gameplay/Engine TBD registers | Entries name gates but often not one owner, due revision, evidence artifact path, or consequence of deferral. | Add owner/deadline/evidence/status/supersedes columns; use §15. | Decision-register linter. | Delegated program-management batch after assignments. | No | Before each TBD’s consuming gate |
| **FND-MIN-005 — Minor** | Documentation defect | Gameplay/Engine logical records | Normal-state descriptions dominate; invalid enum/sentinel, version mismatch, one-beyond-capacity and stale-handle examples are sparse. | Require at least one normal, min/max, invalid, transition, and overflow example per public record. | Generated example fixtures round-trip Java/target. | Delegated test/documentation batch after semantics. | No | Before each affected public record freezes |
| **FND-MIN-006 — Minor** | Maintainability risk | Engine §16 module discipline | “Sacred core” review requirement is clear but no actual file/path ownership manifest or static boundary rule exists. | Generate module→path→public entry→private region ownership; fail cross-private symbol references. | Link/map/static reference check. | Architecture contract; mechanical generation delegated. | **Yes—status/ownership board is authorized work** | Initial ownership manifest at R0-A; complete boundary check before Phase 1 |
| **FND-ADV-001 — Advisory** | Quality improvement | Benchmark work | Even lawful observation can encourage accidental visual/content imitation. | Maintain benchmark measurement notes separately from art/mission production; review provenance and use original F-65 fixtures. | Provenance audit before asset/content acceptance. | Product/legal/art. | No | Before comparative benchmark assets/captures inform production |
| **FND-ADV-002 — Advisory** | Tooling improvement | Engine §§3, 16 | Static call-graph/MAP checks will be fragile if based only on naming conventions. | Emit call edges and memory-owner annotations from assembly symbols; machine-check forbidden calls/ranges. | Intentionally invalid fixtures fail CI. | Architecture; mechanical tooling delegated after schema. | No; may be implemented opportunistically now | Before Phase 1 static architecture gate |
| **FND-ADV-003 — Advisory** | Test improvement | Input/audio/timing | End-to-end latency is hard to infer from software counters alone. | Build a repeatable GPIO/video/audio capture fixture or equivalent external timing method and document uncertainty. | Calibration against known pulse/source. | Platform/test. | No | Before R0-B latency claims; optional if equivalent calibrated method exists |
| **FND-ADV-004 — Advisory** | Scope protection | Architecture memory/timing ledgers | Reserves tend to be consumed by individually attractive features. | Require a numbered decision with measured before/after reserve and rollback for any reserve use; publish reserve trend. | CI reserve floor and change-impact report. | Architecture/product. | No | Before any allocation consumes a frozen reserve |

### B.4 Readiness accounting

| Severity | Count | Must close before full autonomous production? |
|---|---:|---|
| Blocker | 2 | Yes—all by their stated closure gates; neither stops independent earlier proof work |
| Critical | 2 | Yes—timing and platform ABI by their stated closure gates |
| Major | 32 | Only those whose closure gate is at or before the work being authorized; later phase/content items remain tracked without blocking earlier work |
| Minor | 6 | Track and schedule; no silent contradictions |
| Advisory | 5 | Recommended or deferred quality controls, not gate-blocking by themselves |

## Appendix C — Risk Register

Likelihood (`L`) and impact (`I`) are 1–5 before mitigation; exposure is `L×I`. Residual exposure must be rescored from evidence, not optimism.

| Risk | L | I | Exposure | Trigger / early evidence | Mitigation and contingency | Owner / closure gate |
|---|---:|---:|---:|---|---|---|
| RSK-001 Missing/ambiguous specification authority | 5 | 5 | 25 | Different corpus or draft status used by tasks | CORR-AUTH-001/002 and spec manifest; stop affected baseline acceptance/gameplay production if hash/status fails while independent bounded proof work continues | Product + Architecture / Gate 0 before R0-A acceptance |
| RSK-002 Independent timing phases exceed source ledger | 4 | 5 | 20 | Four-tick window, reserve breach, debt/audio/input miss | CORR-TIME-001, phase sweep; reduce display work/mode/content only by approved measured decision | Architecture + Platform / R0-F |
| RSK-003 Renderer cannot sustain clarity and ≥20 Hz under legal scene | 4 | 5 | 20 | High abort/shedding, overdraw/list overflow, unreadable tier | Prototype candidate modes/scenes early; simplify mode/geometry/effects while preserving HUD | Graphics + Product / R0-D/F |
| RSK-004 Active-state/snapshot/event memory exceeds chip ledger | 4 | 5 | 20 | Generated schema > owner limit, zero guard/slack, event peak overflow | Generated ledgers/fan-out; reduce record/data scope or approve architecture revision—not reserve creep | Architecture / R0-E |
| RSK-005 Snapshot lifetime corrupts or stalls presentation | 4 | 5 | 20 | Renderer holds buffer while publisher wraps; mixed ticks | CORR-SNAP-001, bounded ring and forced-lag test; skip presentation publication safely | Core/Graphics / interface gate |
| RSK-006 Hardware behavior diverges from Xemu | 4 | 5 | 20 | DMA/IRQ/MAP/audio/video/input result differs on device | Pin identities, hardware gate each behavior; keep conservative backend/mode fallback | Platform / every R0 hardware gate |
| RSK-007 Fixed-point 6DOF or missile math lacks accuracy/stability | 4 | 5 | 20 | Long-run drift, normalization saturation, host divergence | Numeric registry, high-precision then bit-exact oracle; revise precision/schema before content tuning | Flight/Weapons / Phase 2–3 |
| RSK-008 Storage image fits nominal bytes but not boot/save/recovery | 3 | 5 | 15 | D81 allocation overflow, no save space, ROM-reclaim I/O failure | Disk manifest, R0-C physical boot/save fault matrix; split campaign or choose approved save medium | Storage/Product / R0-C |
| RSK-009 Tactical AI/sensor/weapons load exceeds protected budget | 4 | 4 | 16 | Combined profile p95/worst exceeds per-tick/rolling ceiling | Table/schedule optimization behind identical semantics; reduce authored concurrency only through approved limits | Runtime leads / Phase 1, 3–4 |
| RSK-010 Toolchain/generation is non-reproducible | 4 | 4 | 16 | Dirty generated files, host-dependent bytes, missing artifacts | Lock versions/locale; clean second-host build; fail stale generation | Tooling / Gate 1–2 |
| RSK-011 Audio cache/content/DMA contention misses warnings | 3 | 4 | 12 | Preemption/glitch/latency > target; 12 KB overflow | Short vocabulary, SID/text fallback, staged PCM registry; reduce rate/content based on hardware evidence | Audio/Product / R0-B |
| RSK-012 Campaign/content scope arrives after architecture freeze | 5 | 4 | 20 | Operations 3–10 need new mechanics/entities/assets | Ten-row manifest before production; use existing bounded mechanics; architecture change requires scope review | Product/Creative / before Phase 4 |
| RSK-013 Multiple AI agents create incompatible local conventions | 5 | 4 | 20 | Duplicate structs, converters, unit transforms, private cross-access | Single generated registries, task admission template, trace/static checks | Architecture/TPM / Gate 1 onward |
| RSK-014 Benchmark claim is historically wrong or unmeasurable | 4 | 2 | 8 | No legal pinned release/config, incompatible captures | Defer comparison; use absolute F-65 targets; DEC-006 and lawful clean-room capture only before a claim | Product/Acceptance / before comparative claims, non-blocking otherwise |
| RSK-015 Asset quality/final size invalidates proxy-era budgets | 4 | 4 | 16 | Final mesh/audio exceeds proxy envelope or readability | Budget-valid proxies, per-class manifest limits, converters reject overage, early representative finals | Art/Audio + Architecture / slice/content lock |
| RSK-016 Reserve erosion and exception accumulation | 4 | 5 | 20 | “Temporary” bytes/clocks persist; reserve trend declines | Numbered approval, measured impact/rollback, CI floor; cut/defer feature if reserve cannot recover | Architecture/Product / all gates |
| RSK-017 Physical media/input device variability | 3 | 3 | 9 | Load/latency/failure outside primary device result | Supported-device matrix, p95/worst tests; explicitly reject/label unsupported devices | Platform/Product / R0-B/C |
| RSK-018 Human decisions arrive too late for AI sequence | 4 | 4 | 16 | Tasks blocked or implement planning assumptions as product | §15 deadlines, decision owner and escalation SLA; continue only independent proof work | TPM/Product / each phase entrance |

## Appendix D — Terminology Glossary

| Term | Controlled meaning |
|---|---|
| Active tick / `SimulationTick` | One completed 10-ms authoritative simulation step while in `ACTIVE_SORTIE`; paused wall time does not advance it under proposed correction |
| Architecture corpus | The exact hash-pinned files that jointly contain every authoritative architecture requirement |
| Attic RAM | Normally available extended MEGA65 RAM at the documented high address range; cold/immutable tactically here and staged for consumers without direct reach |
| Authoritative state | State that can affect future simulation, mission/campaign outcome, replay checksum, or player capability |
| Base page | 45GS02 relocated zero/base page, frozen by Architecture at `$0200`; relocation is MemoryAccessABI-only |
| Blocker | A defect that prevents its target outcome from being completed reliably; it stops work only when the affected work reaches the finding’s closure gate |
| Blocks current milestone? | Whether the finding prevents acceptance of the currently authorized pre-R0/R0-A horizon; “No” still requires later closure at the named gate |
| Closure gate | Latest milestone boundary at which a finding must be resolved before dependent work may be accepted or proceed |
| Combined-load profile | Gameplay §3.1 simultaneous acceptance scenario; it does not replace individual pool capacities |
| Command | Tick-tagged requested action applied at the frozen command stage; may be player, AI, mission, or authorized external source |
| Controlled performance pause | A deterministic fault/recovery state entered by the approved timing policy; exact player behavior must be cataloged |
| Correction | A scoped replacement tied to source/version/section and defect; authoritative only when status is Approved |
| Decision | A recorded human choice among materially different product, architecture, scope, or acceptance outcomes |
| Deterministic | Identical approved initial state, semantic command stream, packages, seeds, and arithmetic produce the same canonical authoritative checksum stream |
| Display service | Raster/display-cadence work such as input sample, overlay, swap, or audio service; asynchronous to 100 Hz simulation |
| DMAService | Proposed CoreRuntime-owned validation/serialization interface for DMAgic jobs; no module starts DMA directly |
| D81 | 819,200-byte disk-image container before filesystem allocation overhead; project payload capacity is lower and must be manifested |
| Dynamic mission entity | Bounded mission-runtime object that affects authoritative objectives/events but is not another physical entity pool |
| Entity handle | Frozen typed slot+generation identity; stale generation is invalid and freed slot cannot be reused before lifecycle commit |
| Event | Immutable tick-originated fact sorted by the frozen class/source/target/producer ordering before authoritative application |
| Evidence bundle | Machine-indexed test inputs, identities, measurements, results, artifacts, and sign-offs sufficient to reproduce an acceptance decision |
| Frozen | Approved source invariant; not synonymous with technically correct if a verified contradiction requires a numbered correction |
| Golden vector | Approved input/initial state and independently reviewed expected output/tolerance, not merely captured current code behavior |
| Host oracle | High-precision or bit-exact Java model used to define/test target behavior; it is subordinate to approved requirements |
| Immutable resource | Resource whose bytes/semantic identity cannot change while any consumer may use it |
| MVP | Minimum viable release product; distinct from R0 proof, Phase 1 harness, and Technical Combat Slice |
| Measured-limits reserve | Architecture-owned 32 KB chip range and timing reserve protected against routine feature allocation |
| Midnight Spear | Named product vertical slice whose narrative mission specification is currently unresolved; not the same as the proposed Technical Combat Slice |
| Observation | Sensor-derived measurement generated from truth and uncertainty/environment; it is not truth or a fused track |
| Presentation state | Derived, non-authoritative data used by graphics/audio/UI; dropping or delaying it cannot alter simulation |
| `PresentationSnapshot` | Proposed bounded immutable extraction published at a completed tick for presentation consumers; replaces ambiguous use of full `SimulationSnapshot` where approved |
| Planning assumption | Temporary value usable for estimates/prototypes only; never shipping authority |
| Pool capacity | Maximum allocated slots for one type; does not assert every pool maximum is legal simultaneously |
| R0-GATED | Value that cannot freeze until named physical-hardware measurement and measured-limits approval |
| Reserve | Bytes/clocks intentionally unallocated for uncertainty and stability; it is not a general feature budget |
| Resource handle | Stable ID resolved by ResourceManager; not a raw pointer and not evidence of current residency |
| RIO | AI radar intercept officer/player-support system; its knowledge, callouts, automation, damage and fallback are explicit gameplay state |
| Semantic input | Device-independent action/axis after calibration/context mapping, recorded per active tick for simulation/replay |
| Sensor truth | Physical/emission/environment state available to the sensor model, not automatically available to AI, player, or track consumers |
| Severity | Consequence if a finding remains unresolved at its consuming outcome; not a substitute for schedule or closure gate |
| Shedding | Fixed deterministic reduction of presentation work/quality; forbidden from changing authoritative workload or results |
| Snapshot publication | Atomic transition making a complete immutable presentation record available; never exposes partially assembled state |
| Source of truth | The highest approved requirement controlling the exact behavior in question, subject to explicit scoped corrections |
| Technical Combat Slice | Non-narrative integrated engineering proof defined in §14.2; not a release campaign mission |
| Track | Bounded estimated/fused contact record derived from observations with quality/age/source; not a duplicate physical entity |
| Vertical slice | End-to-end player-visible proof spanning relevant engine/data/content/tests; its exact named product scope requires approval |
| World frame | Frozen right-handed north/east/down coordinate convention plus specified sector/local position representation |
| Worst phase | Relative alignment of independent tick, raster/display, IRQ, DMA/audio and work-release events that maximizes a measured deadline/resource quantity |

## Appendix E — Decision Log

This log records audit conclusions and pending governance. It does not turn a proposal into approval.

| Log ID | Date | Status | Decision/proposal and rationale | Supersedes / evidence | Approver |
|---|---|---|---|---|---|
| LOG-001 | 2026-08-17 | Confirmed observation | Reviewed exactly the three hashes in §1.1; no production code or referenced generated artifacts were supplied | File hashes and workspace inspection | Auditor |
| LOG-002 | 2026-08-17 | Proposed in v0.1; calibrated in v0.2 | GO for bounded documentation/host/pre-R0/R0-A work; No-Go for autonomous gameplay/full production. Findings block only at their closure gates. | §4; stable findings with v0.2 severity/gates | Product + Architecture |
| LOG-003 | 2026-08-17 | Proposed technical correction | Replace exact six-frame/ten-tick reporting with independent-clock worst-phase accounting | Official 2026 chipset geometry; calculation in §9.2 | Architecture + Platform |
| LOG-004 | 2026-08-17 | Proposed | Use 20 July 2026 chipset reference as documentation baseline and pin actual core/ROM/hardware identity | CON-003, CORR-REF-001 | Platform + Architecture |
| LOG-005 | 2026-08-17 | Proposed | Use bounded extracted presentation snapshots with explicit lifetime; recommend triple buffer pending measurement | FND-BLK-003, DEC-004 | Architecture |
| LOG-006 | 2026-08-17 | Proposed; deferred in v0.2 | Treat the F-117A comparison as unmeasured, non-blocking through Phase 1, and likely *F-117A Nighthawk 2.0* Amiga (1993), not proven native A1200/AGA | §12 cited catalogs; DEC-006 | Product + Acceptance/legal |
| LOG-007 | 2026-08-17 | Confirmed action | Source documents and production code were not edited; v0.1 is preserved and this v0.2 is a separate Draft revision | Repair policy; workspace/source hashes | Auditor |
| LOG-008 | 2026-08-17 | Proposed | Separate non-narrative Technical Combat Slice from undefined Midnight Spear product slice | FND-MAJ-001, §14.2 | Product + Architecture |
| LOG-009 | 2026-08-17 | Revised in v0.2 | Individual approval applies to material architecture/product/scope/platform/resource/failure/acceptance decisions; enumerated mechanical/Minor repairs may receive delegated batch approval; silence never approves proposals | §1.2, §6 | All required approvers/delegates |
| LOG-010 | 2026-08-17 | Deferred pending human review | All `DEC-001`–`DEC-015` outcomes | §15 | Named owners |
| LOG-011 | 2026-08-17 | Proposed v0.2 classification | Preserve stable finding IDs but classify current severity as 2 Blocker, 2 Critical, 32 Major, 6 Minor, and 5 Advisory; add current-milestone and closure-gate fields | Appendix B; human-directed v0.2 calibration | Product + Architecture |

When a decision is made, add approver identity, date, selected option/replacement text, evidence IDs, affected corrections/requirements, and effective specification version. Rejected and superseded entries remain in history.

## Appendix F — Change-Impact Matrix

No concrete production paths were available. Module/artifact names below identify the minimum likely impact once a repository exists.

| Correction/decision | Source documents | Likely runtime modules | Host/data/build artifacts | Required test changes |
|---|---|---|---|---|
| CORR-AUTH-001/002 | All front matter/authority | None directly | Approved-spec manifest, corpus checker, release labels | ACC-AUTH-001/002 |
| CORR-REF-001 / DEC-003 | Architecture §2; Engine references/TBD | PlatformABI, boot diagnostics | Toolchain lock, evidence schema, support matrix | All hardware evidence identity; boot probe |
| CORR-TIME-001 | Architecture §§3, 6; Engine §5 | Scheduler/CoreRuntime, Graphics, Audio, Input, Diagnostics | Performance harness/report schema | ACC-TIME-001–003, all phase sweeps |
| CORR-SNAP-001 / DEC-004 | Architecture §3; Gameplay §18; Engine §§3, 4, 8 | CoreRuntime, PresentationExtractor, Graphics, Audio-facing extractor | Interface/memory registry, host snapshot model | ACC-REN-001, ACC-MEM-001, deterministic lag tests |
| CORR-IFACE-001 | Gameplay §18; Engine §§3, 14 | Every module with public records | `f65_interfaces.json5`, generators, Java/asm bindings | ACC-ABI-001/002 and dependent vectors |
| CORR-NUM-001 | Architecture §4; Engine §§6–7, 14 | Environment, Flight, Contact, Weapon, Sensor, Graphics transforms | Numeric registry, high-precision/bit-exact oracle | ACC-ABI-003, FLT/CON/RAD/WPN suites |
| CORR-INPUT-001 / DEC-013 | Gameplay §5; Engine §11 | InputEngine, CoreRuntime, UI, ControlSystems, replay | Input schema/settings/default maps/device fixture | ACC-IN-001–004, pause/replay |
| CORR-PAUSE-001 | Architecture §3; Gameplay §4 | Scheduler, Input, Mission time, Audio/UI, replay | State-machine specification | ACC-PAUSE-001, ACC-MSN-003 |
| CORR-FAULT-001 | All queues/pools/storage | CoreRuntime and every owner; UI/debrief | Fault catalog, evidence/trace decoder | ACC-FAULT-001 plus one-over fixtures |
| CORR-PLAT-001 | Architecture §2; Engine §§3–5, 8, 12 | PlatformABI, MemoryAccessABI, DMAService, IRQ, math wrappers | Opcode/timing ROM, platform schema | ACC-ABI-002/003, DMA/TIME tests |
| CORR-MEM-001 | Architecture §§2, 5; Engine §4 | Core pools, snapshots, events, all allocations | Memory registry, linker report, mission capacity proof | ACC-MEM-001/002, WPN-002 |
| CORR-STORE-001 / DEC-012 | Architecture §12; Gameplay §4; Engine §13 | Boot, ResourceManager, StorageService, UI/Campaign | Package/save schema, D81 builder/manifest | ACC-STO-001/002, mission restart tests |
| CORR-TOOL-001 | Engine §§14, 17, 21 | Build identity probe only | Toolchain lock, build/CI scripts, artifact index | ACC-BUILD-001/002 |
| CORR-ASSET-001 / DEC-005/011 | Engine §§8, 12, 14 | Graphics, Audio, ResourceManager | Asset manifest/converters/provenance/D81 | ACC-REN-003/004, AUD-002, aggregate fit |
| CORR-MISSION-001 / DEC-008 | Architecture §1; Gameplay §16 | MissionEngine, relevant runtime slice modules | Technical/narrative mission manifests and packages | TEST-007, ACC-MSN-001, §14.2 |
| CORR-CAMP-001 / DEC-010 | Gameplay §16 | Mission/Campaign, Storage, UI/debrief | Ten-row manifest, mission packages/assets | ACC-MSN-001–003, branch coverage |
| CORR-RADAR-001 | Gameplay §§10, 18; Engine §9 | SensorAndTrack, FireControl/Weapon, AI, Graphics | Sensor/track schemas and scenario corpus | ACC-RAD-001–003 |
| CORR-AUDIO-001 / DEC-011 | Engine §12 | AudioEngine, DMAService, ResourceManager, Graphics fallback | Audio registry/converter/cache ledger | ACC-AUD-001/002, TIME phase load |
| CORR-REPLAY-001 | Architecture §10; Engine §15 | CoreRuntime, Diagnostics, Input, Mission | Replay/checksum schemas and diff tools | ACC-DET-001/002 and all golden replays |
| CORR-BENCH-001 / DEC-006/014 | New supplement benchmark | Instrumentation only; representative game modules | Legal baseline record/capture/rubric | TEST-008 / §12 matrix |
| CORR-TEST-001 | All acceptance sections | Diagnostics/instrumentation hooks | Acceptance/evidence catalog, CI reports | Every acceptance ID |

### F.1 Change completion rule

A correction is not implemented merely because its source prose, schema, or code changed. Completion requires, in one traceable reviewed set:

1. approved correction and decision state;
2. source-document insertion or explicit approved supplement precedence;
3. regenerated interfaces/data and impact report;
4. code/tool/asset changes within approved scope;
5. host and target tests at required evidence tiers;
6. updated memory/cycle/storage/high-water reports;
7. no unexplained regression or reserve loss; and
8. human code/content/release review as applicable.

---

**End of F-65 Technical Alignment and Corrections Supplement v0.2 — DRAFT — REQUIRES HUMAN REVIEW**
