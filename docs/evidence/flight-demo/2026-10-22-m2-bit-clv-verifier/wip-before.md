# Work in Progress

- **Status: FAILED GATE — stopped for review; no composed candidate relink.**
- **Branch/base:** `codex/65aero-m2-interpolation-experiment`, verified main `c6a41e0988a3e329f1b30f7d48c87d92e00b523b`; exact-main CI PASS.
- **Authority:** [Approved bounded interpolation intent](docs/plans/65AERO_M2_PR2_INTERPOLATION_BUILD_INTENT.md), as approved on 22 October. Retained planning status is provenance; the current prompt supplies implementation authority.
- **Scope:** Reconstruct exact 34,149-byte reference; freeze direct-helper corpus/reference; one bit-consumption candidate inside interpolate_delta; required checks and one candidate composed relink, then stop implementation and report read-only accounting.
- **Preservation:** All prior checkouts/evidence and unrelated paths untouched. Precision, public/generated ABI, memory limits, cache/cancellation/lifetimes and deadline guards frozen.
- **Boundary:** No Xemu, D81, SD, physical testing, further optimization or publication.
- **Result:** Exact 34,149-byte reference reproduced; sole I2 edit implemented. Direct 457,334-case and frozen 799,886-case comparisons, Decimal/near-far checks, renderer host/cancellation and five exact images PASS. Standalone compile/link completed, then required stack checker failed on emitted `BIT`; I5 stops before composed candidate relink. No checker change or retry.
- **Accounting:** Standalone probe 17,151 → 17,054 resident bytes (−97), scratch 497 → 487; dynamic stacks UNPROVEN. Composed candidate savings/fit UNMEASURED; last verified composed deficit remains 9,574 bytes.
- **Handoff:** [Result and next-review recommendation](docs/reports/M2_PR2_INTERPOLATION_BITWALK_EXPERIMENT.md), [evidence](docs/evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk/README.md). Separate verifier review/authority required before resuming the unused composed relink. No further implementation, builds or publication in this task.
