# F-65 Architecture Decision AD-001 — R0 Program Development Authorization

## Document Control

| Field | Value |
|---|---|
| Decision ID | `AD-001` |
| Version | 1.0 |
| Status | **APPROVED — R0-A–F DEVELOPMENT AUTHORITY** |
| Date | 2026-08-20 |
| Decision class | Program development authorization under architecture control |
| Parent architecture | F-65 Megawing Revision 1.5.1 — Architecture Invariants and Gameplay Alignment |
| Parent engine design | F-65 Engine Runtime and Toolchain Design Supplement Draft 0.2 |
| Required approvers | Product owner and Architecture owner/technical lead |
| Approved draft SHA-256 | `a93726389cc4b7d0cf2b0c4e87e21237e165f377a542bcadafc564f1896f8385` |
| Approval record | `F-65_Specification_Approval_Record_2026-08-20_R0_Development.md` |
| Approval effect | Active from 2026-08-20 under the recorded scope and exclusions |

This decision did not approve itself. Its external human approval is recorded against the exact Final Draft hash above. Publication, silence, implementation activity, compiler output, Xemu output, or an AI statement cannot create or broaden approval.

## Decision

Under the recorded human approval of `AD-001`, development of the complete R0-A through R0-F proof program is **GO**.

“GO for development” authorizes construction, integration, execution, diagnosis, and evidence collection for the bounded proof artifacts described by Revision 1.5.1 and Engine Draft 0.2. It does not mean that any R0 gate has passed, that any measured value is frozen, or that production gameplay is authorized.

R0-A through R0-F proof development may proceed concurrently where dependencies permit. Acceptance remains dependency-ordered and evidence-based. Work depending on an unpassed earlier result must identify that dependency, use a reversible candidate assumption, and remain provisional until the dependency passes.

## Reason

Revision 1.5.1 defines all of R0-A through R0-F but names R0-A as the smallest authorized next milestone. That wording prevents premature production work but can also be read as prohibiting useful preparation of later R0 experiments. Engine Draft 0.2 already defines production-shaped R0 proof candidates whose early construction reduces toolchain, renderer, memory, storage, timing, and hardware risk.

This decision broadens proof-development authorization without weakening any architecture invariant, evidence requirement, gate, reserve, or human approval obligation.

## Authorized R0 Development Scope

| Stage | Development authorized under approved `AD-001` | Evidence required before the stage may be recorded as passed |
|---|---|---|
| R0-A | Toolchain identity; generated interfaces and ledgers; minimal compiled-C boot/link path; C/platform/assembly ABI probes; `MemoryAccessABI`; MAP, base-page, DMA, IRQ, Q/extended-register, stack, profiler, D81, maps/symbols/listings, Xemu and hardware harnesses | Complete pinned identity and every Architecture 1.5.1/Engine 0.2 R0-A acceptance item, including required physical-MEGA65 evidence |
| R0-B | Candidate graphics/display modes, cockpit composition, HUD/MFD service, palette and swap behavior, renderer candidates, input latency/edge tests, representative audio and applicable RRB/affine experiments | Pinned candidate identity; complete-buffer proof; captures; timing, latency, edge, readability and representative-audio evidence on required environments |
| R0-C | Production-shaped host tools and scene; package/D81 manifests; converters; capacity witnesses; resource residency/staging; storage/save/media and post-ROM-reclaim proof fixtures | Reproducible package/D81 evidence, conservative fit witnesses, approved service ownership, physical storage/save fault evidence, and no tactical disk dependency |
| R0-D | Historical 530,000-clock protected non-render workload and calibrated per-service measurement fixture | Reproducible fixture identity and calibrated workload evidence compatible with the accepted platform/toolchain baseline |
| R0-E | Independent-clock combined-load harness covering snapshot, memory, renderer, input, audio, DMA/IRQ, storage, reserves, faults and shedding in Xemu | Complete phase-swept Xemu report with identities, p50/p95/worst/high-water evidence, fault results and candidate limits; no claim of hardware closure |
| R0-F | Physical-MEGA65 execution, capture, diagnosis and phase sweep corresponding to the accepted R0-E configuration | Pinned physical platform identity and corresponding hardware report satisfying the parent acceptance requirements |

Authorized renderer, audio, input, storage, scene, and workload implementations are proof candidates. They are not production selections and may use bounded proxy assets or synthetic data when the task admission contract identifies them as such.

## Dependency and Acceptance Rules

1. Construction may overlap; acceptance may not bypass dependencies.
2. R0-B through R0-F artifacts must record which R0-A toolchain, ABI, platform, and interface identities they use. Results produced before R0-A passes are provisional and must be rebuilt or revalidated against the accepted identity.
3. R0-D and R0-E acceptance requires the applicable R0-B/R0-C candidate identities and evidence inputs to be explicit and stable for that run.
4. R0-F must correspond to an identified R0-E configuration. Xemu output cannot substitute for the required physical-MEGA65 evidence.
5. Failure of an earlier gate invalidates only dependent conclusions. Independent fixtures, schemas, tools, and evidence infrastructure may continue when they do not presume the failed behavior.
6. No gate is marked `PASS`, `CLOSED`, or equivalent until its complete evidence is reviewed by the named acceptance owner.
7. The measured-limits revision remains a separate, human-approved post-R0 control document. R0 results alone do not freeze a `TARGET`, `TBD`, or `R0-GATED` value.

## Explicit Non-Authorization

`AD-001` does not authorize:

- production flight, aircraft-systems, radar, weapon, damage, tactical-AI, campaign, Midnight Spear, or other gameplay implementation in C or assembly;
- Phase 1 implementation or acceptance before R0-F passes and the measured-limits revision is approved;
- representing a proof renderer, display mode, RRB/affine experiment, asset, audio format, input profile, storage path, or snapshot layout as the production selection;
- changing the 100 Hz authoritative simulation, frozen stage order, ownership, public ABI, memory map, fixed-capacity rule, resource-residency rule, DMA ownership, presentation-snapshot semantics, or deterministic-state boundary;
- consuming the 32 KB measured-limits reserve or enlarging another owner’s allocation without the required numbered decision;
- bypassing `MemoryAccessABI`, Core/Platform services, generated public records, or C/assembly admission rules;
- selecting player-visible behavior, creative content, tuning, `TARGET`, `TBD`, or `R0-GATED` production values;
- treating successful compilation, host tests, or Xemu as physical-hardware proof; or
- waiving review, traceability, evidence identity, or acceptance requirements.

## Task and Evidence Control

Every R0-B–F task started before its predecessors pass must state:

- the gate and proof question;
- upstream identities and any provisional assumption;
- authorized and prohibited paths;
- interfaces and mutable-state owners;
- implementation language and exact toolchain identity;
- memory, code, stack, cycle, DMA and reserve budgets;
- normal, boundary, fault and overflow behavior;
- host, Xemu and physical-hardware evidence obligations;
- the condition that triggers rebuild or revalidation; and
- the human review and exit criterion.

`NOT_APPLICABLE_UNTIL_GATE` remains valid for genuinely later information. It may not conceal a fact needed to interpret the current proof.

## Authority and Relationship to Parent Documents

This is a narrow development-authorization decision. It does not rewrite Architecture 1.5.1, Gameplay 0.2, or Engine 0.2 and does not change any R0 or Phase 1 pass criterion.

If approved, `AD-001` controls only the question “May the team develop this R0 proof artifact now?” Architecture 1.5.1 controls invariants and gate requirements; Gameplay 0.2 controls adopted player-facing behavior; Engine 0.2 supplies subordinate candidate proof contracts. A conflict on behavior, ownership, budget, interface, or acceptance is resolved by those parent authorities, not by expanding this authorization.

Approval may be recorded while the parent documents retain candidate status. In that case, R0 development is authorized against their exact hash-pinned candidate identities, but formal gate acceptance and production use remain subject to Gate 0 and the parent approval record.

## Approval Record

This decision was activated by the external approval record. Its recorded entries are:

| Field | Required entry |
|---|---|
| Exact filename | `F-65_Architecture_Decision_AD-001_R0_Program_Development_Authorization.md` |
| Version | `1.0` |
| Approved draft SHA-256 | `a93726389cc4b7d0cf2b0c4e87e21237e165f377a542bcadafc564f1896f8385` |
| Human approver identity | Project user/human authority in the controlling conversation; personal name not supplied |
| Approval scopes | Product and Architecture authorization stated affirmatively by the human authority |
| Approval date | 2026-08-20 |
| Scope/exclusions | Full decision; exclusions are those stated in this document and the human approval statement |
| Effective status | `APPROVED — R0-A–F DEVELOPMENT AUTHORITY` |

Recorded approval statement (full record retained in the external approval file):

> Approved as authorization to develop the complete R0-A through R0-F proof program against the identified candidate specification corpus. This approval does not mark any R0 gate passed, approve measured limits, authorize Phase 1 or production gameplay, or waive physical-MEGA65 evidence and human acceptance.

## Revision History

| Version | Date | Status | Change |
|---|---|---|---|
| 1.0 | 2026-08-20 | Final Draft | Initial decision separating full R0 proof-development authorization from sequential evidence acceptance |
| 1.0 | 2026-08-20 | **Approved** | Human approval recorded against Final Draft SHA-256 `a9372638…f8385`; mechanical status metadata activated with no semantic change |
