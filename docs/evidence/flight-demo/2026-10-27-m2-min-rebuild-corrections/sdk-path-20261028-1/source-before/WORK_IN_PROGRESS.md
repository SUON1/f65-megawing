# Work in Progress

- **Status: READY FOR REVIEW.**
- **Task:** Minimum-renderer P1 and both P2 corrections, packet `65AERO-M2-MIN-REBUILD-CORRECTIONS-1`; same private profile, branch `codex/65aero-m2-minimum-renderer-baseline`, base `b044440fa98c2dfc91ec590668049610afc98a1e`.
- **Authority:** Founder authorizes these three fixes, affected checks and one target relink. [Original Build Intent](docs/plans/65AERO_M2_MINIMUM_REBUILD_BUILD_INTENT.md); [correction handoff](docs/reports/M2_MINIMUM_REBUILD_CORRECTIONS.md).
- **Result:** Terminal handler uses raw-verified absolute JMP; `AGE AT TEXT` uses the candidate snapshot; full SDK identities verified before/after linking. Host/sanitizer, 27 contract/startup/SDK tests, frozen geometry/near-far oracles, policy checks and one complete target compile/link PASS.
- **Fit:** FAIL retained: 32,839 / 24,575 resident bytes, deficit 8,264 (44 fewer than prior). Compiler scratch 190, renderer workspace 676, reserve zero. Precision, public records, clock, stage order and limits unchanged.
- **Admission:** Linked prefix/terminal closure checked only; runtime startup, whole-program stack and service remain UNPROVEN. Launch, eight operation bounds and guard remain zero. Xemu/display NOT RUN/NOT OBSERVED; no banking.
- **Preservation:** [Correction evidence](docs/evidence/flight-demo/2026-10-27-m2-min-rebuild-corrections/) retains the exact reviewed source archive, all original failures and the new target identity. Old packet remains unchanged; historical 22/15 recovery and eight unverified Git-worktree tiers remain unchanged.
- **Next:** Founder review. No automatic optimization, banking, target execution or publication.
- **Boundary:** No commit, push, PR, merge, Xemu, D81, SD or physical testing performed.
