# Physics v4 coordinated revision package

Status: READY FOR REVIEW - NOT ADOPTED. Date: 4 October 2026.

## Approved Build Intent

The founder accepted the cross-repository review/design direction, then explicitly requested "Make the revisions." Prepare the six identified Physics corrections and coordinated parent/AI review drafts. Preserve every admitted source and historical evidence identity. Return local review artifacts; do not commit, push, open a PR, update the active manifest, or declare adoption.

Baseline: `c6ff0cd429bdd233b182e416d1e8a75f91c2ae49`, independently matched to live main before edits. Work is isolated because the primary checkout contains unrelated untracked work. Authority: Main v1.6 > Gameplay v1 > Runtime v1 approved candidate > Physics v3.3. Their bytes and the manifest remain unchanged.

## Review artifacts

- [Physics v4.0 R1](F65_Flight_Physics_and_Simulation_Engineering_v4.0_R1_REVIEW_DRAFT.md): canonical revised source; generated PDF under `output/pdf/`.
- [Main v1.7 draft](F65_Main_Concept_v1.7_REVIEW_DRAFT.md): full successor text; narrowly changed current physics references and draft control.
- [Gameplay v1.1 draft](F65_Gameplay_and_Simulation_Supplement_v1.1_REVIEW_DRAFT.md): full successor text; current physics reference and proposed parent control.
- [Runtime v1.1 amendment](F65_Runtime_v1.1_AMENDMENT_REVIEW_DRAFT.md): exact base-plus-amendment successor, preserving the canonical PDF.
- [AI v1.1 amendment](F65_AI_Behavior_v1.1_AMENDMENT_REVIEW_DRAFT.md): exact base-plus-amendment successor for §27.2 and current-contract annotation.
- `review-identities.json`: review-package identities only; not a specification manifest or approval record.

The Runtime/AI amendments are insertion-ready controlled revisions, not replacement full PDFs. Their unchanged bases remain required parts of the proposed successor. Numbering is proposed, not reserved or approved.

## Correction trace

| Review finding | Revised location |
|---|---|
| Engine moment double-count ambiguity | Physics §6.2 |
| Sampling age, override and initialization | Physics §1.3.1; Runtime R3-R4 |
| Closed coefficient conventions | Physics §6.1; Runtime R2/R5 |
| CG/datum continuity | Physics §4.4.1; Runtime R4 |
| Qualified-pilot acceptance | Physics §14.5; Runtime R5 |
| Complete controlled migration | Physics §15.2; this package and AI amendment |

## Contract and hardware impact

Documentation proposals only. Registers/clobbers, CPU-visible/physical allocation, MAP/base-page, DMA, target timing/deadline and IRQ/NMI changes: not applicable. Runtime sampling/state semantics are proposed for later generated contracts; no interface bytes or ledger entries change. No production aircraft data, gains, table dimensions, formats or budgets are selected. P09 and later bounded evidence do not supply production headroom.

## Adoption held for founder review

After acceptance, deliberately select the successor identities, update current authority references in the corpus manifest, CURRENT_STATE and the current table in F65_OFFICIAL_RECORD, and preserve v3.3 as provenance. Do not rewrite historical source appendices or frozen evidence. Other white papers, README and AGENTS require changes only for actual dependencies. Runtime remains a candidate until its independent finalization conditions are satisfied. Publication and merge remain separate decisions.

## Validation

See VALIDATION.md for actual checks, reading-copy generation and limits. No target build, Xemu, physical flight test, handling acceptance or production performance evidence is implied by this documentation delivery.
