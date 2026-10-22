# Work in Progress

- **Status: READY FOR REVIEW — bounded BIT/CLV verifier fix and pinned replay complete.**
- **Branch/base:** `codex/65aero-m2-interpolation-experiment`, verified main `c6a41e0988a3e329f1b30f7d48c87d92e00b523b`; exact-main CI PASS.
- **Authority:** Current task prompt approves the read-only review's exact BIT/CLV verifier fix, required regressions and pinned-artifact replay. The [interpolation intent](docs/plans/65AERO_M2_PR2_INTERPOLATION_BUILD_INTENT.md) and failed experiment remain provenance; their unused composed relink is not resumed.
- **Scope:** Add BIT/CLV to ordinary stack-neutral instructions; preserve both branch successors and all rejection/limit rules. Add approved regressions and replay the previously passing standalone probe and failed interpolation probe, without relinking.
- **Preservation:** All prior checkouts/evidence and unrelated paths untouched. Precision, public/generated ABI, memory limits, cache/cancellation/lifetimes and deadline guards frozen.
- **Boundary:** No target source edits, compile/link, Xemu, D81, SD, physical testing, further optimization or publication.
- **Result:** 11 contract tests PASS (six added methods). Original checker reproduces the pinned interpolation failure; corrected checker passes both pinned standalone probes. Both bound 20 hardware bytes including entry return and zero dynamic software bytes; predecessor result is identical. All 57 raw outputs remain exact; zero relinks.
- **Accounting:** Interpolation standalone compiler scratch remains 487 resident bytes, separate from dynamic stack. Last composed reference remains 34,149 bytes with 9,574-byte deficit; composed candidate size/stack/timing remain unmeasured. No full-builder or runtime/display PASS claimed.
- **Handoff:** [Verifier result and limitations](docs/reports/M2_BIT_CLV_VERIFIER_FIX.md), [new evidence](docs/evidence/flight-demo/2026-10-22-m2-bit-clv-verifier/README.md). Review this bounded correction; no resumed build, relink or later stage is authorized. Prior failure/report/evidence and unrelated paths preserved.
