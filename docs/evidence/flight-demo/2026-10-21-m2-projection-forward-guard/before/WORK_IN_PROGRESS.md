# Work in Progress

- **Status: READY FOR REVIEW — bounded size gate FAILED; implementation stopped.**
- **Branch/base:** `codex/65aero-m2-projection-experiment`, verified main `9dae245314ddd41cceaa7c6c3e7fce90c564138e`; exact-main CI PASS.
- **Authority:** [Approved bounded projection intent](docs/plans/65AERO_M2_PR2_PROJECTION_BUILD_INTENT.md), as approved by the founder on 21 October. The retained planning file is unchanged provenance; this task approval supersedes its pending status.
- **Scope:** Reconstruct the 79-input reference; one candidate confined to `m2_project_prepared`; fixed comparison/oracle/renderer and target checks. Stop after candidate relink and read-only accounting.
- **Boundary:** Preserve all other checkouts, evidence, unrelated entries, precision, memory limits, ownership, renderer/cache/dispatch and generated contracts. No Xemu, D81, SD, physical testing or publication.
- **Result:** [Projection experiment](docs/reports/M2_PR2_PROJECTION_EXPERIMENT.md): own projection code -96 bytes, text +328, scratch -16; resident 34,221 → 34,533 (+312); remaining deficit 9,958 bytes, end `$A6E6`. One reference and one candidate composed relink.
- **Checks:** 799,886 exact ASan/UBSan comparisons +34 contract checks; 3,857 Decimal cases; 841 near/far cases; renderer/cancellation/fault checks and five identical images; standalone target/static PASS. Composed stack proof remains UNPROVEN because unchanged checker rejects `bit` in frozen interpolation. Full-fit/runtime/display gates not reached.
- **Preservation:** Original 15,731 paths and prior transform 15,536 paths unchanged; 20 unrelated entries and 12 historical inventories verified; generated files/ledgers unchanged.
- **Next:** Founder review of the failed experiment. No second candidate, optimization, target execution or publication authorized.
