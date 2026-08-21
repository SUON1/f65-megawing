# R0-B Engineering Handoff — In Progress

This record is deliberately partial. R0-B is **not implementation complete**
and has not passed owner hardware review.

## Current branch and upstream

- Branch: `codex/r0-b-development`.
- Consumed R0-A commit: `1ab5b62928d0e725c8dcf48e8a17783a525503b6`.
- R0-A D81: `40d95171389e3825793216ed54176084a87bad5bac630b942955c8b90668b3b4`.
- R0-A ABI/toolchain/interface identities are retained in
  `docs/plans/R0-B_EXEC_PLAN.md`.

## Built so far

| Candidate or proof | Host | Xemu | Hardware | Status |
|---|---|---|---|---|
| Two FCM accounting candidates | PASS | N/A | NOT RUN | candidate accounting only |
| Semantic palette / grayout role map | PASS | screen marker | NOT RUN | no readability decision |
| VIC-IV `$D054` FCM-related latch and restore | documented | PASS | AWAITING OWNER | no visible FCM conclusion |
| Deterministic 10,000-case edge fixture | PASS | target fixture PASS | NOT RUN | no CIA/input-latency conclusion |
| Presentation priority model / SID proxy configuration | PASS | target model PASS; dummy audio | AWAITING OWNER | no timing/PCM conclusion |

## Present evidence and debug output

- Contract and generated bindings: `interfaces/r0b_proof_contract.json` and
  `interfaces/generated/`.
- Host result: `build/r0b/reports/r0b-host-oracle.json`.
- Target build inspection: map, symbols, disassembly in `build/r0b/reports/`.
- Xemu result block and screen dump: `build/r0b/reports/R0B-XEMU.*`.
- Scope findings: `docs/evidence/r0b/`.

## Still open

- Visible FCM character/pointer-table operation, clear/span/face operations,
  complete-buffer presentation, swap/raster and tearing proof.
- Renderer tiers, cockpit/HUD/MFD proxy, day/dusk/night and grayout captures.
- Hardware input sample path and calibrated latency.
- SID service cadence, audible latency/preemption, PCM/DMA, graphics-DMA
  contention, ten-minute stability.
- RRB/affine disposition, integrated test, code/stack/cycle distributions,
  acceptance matrix closure, full hardware guide and owner review.

No entry selects a production display mode, renderer, controls, audio format,
quality tier, palette, or cockpit art.
