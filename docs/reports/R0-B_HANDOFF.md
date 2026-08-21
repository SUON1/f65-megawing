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
| Isolated VIC-IV `$D054` `CHR16|FCLRHI` latch and exact restore | `R0B-FCM-SAFE-XEMU-001` PASS | PASS: no `$D02F`, pointer, DMA, MAP, or IRQ path; text sentinel retained | NOT RUN | physical capture of exact `F65-R0B-FCM-SAFE.d81` required; not visible FCM |
| Deterministic 10,000-case edge fixture | PASS | target fixture PASS | NOT RUN | no CIA/input-latency conclusion |
| Presentation priority model / SID proxy configuration | PASS | target model PASS; dummy audio | AWAITING OWNER | no timing/PCM conclusion |
| Final composite FCM/presentation candidate | `R0B-FINAL-STATIC-001` PASS | `R0B-FINAL-XEMU-001` PASS: reversible `$D031/$D054`, full matrix B pointer selection/restore, active-palette round trip, HUD, FCM proxy card, and timed SID writes | NOT RUN | the single remaining R0-B hardware capture |

## Present evidence and debug output

- Contract and generated bindings: `interfaces/r0b_proof_contract.json` and
  `interfaces/generated/`.
- Host result: `build/r0b/reports/r0b-host-oracle.json`.
- Target build inspection: map, symbols, disassembly in `build/r0b/reports/`.
- Xemu result block and screen dump: `build/r0b/reports/R0B-XEMU.*`.
- Isolated FCM-safe Xemu capture: `build/r0b/reports/R0B-FCM-SAFE-XEMU.*` and `r0b-fcm-safe-xemu-evidence.json`.
- Final composite Xemu capture: `build/r0b/reports/R0B-FINAL-XEMU.*`.
- Final hardware artifact and instructions:
  `build/r0b/artifacts/F65-R0B-FINAL.d81` and
  `docs/testing/R0-B_FINAL_COMPOSITE_TEST_GUIDE.md`.
- Scope findings: `docs/evidence/r0b/`.

## Still open before any R0-B gate claim

- One physical run of the final composite D81, with one real key event during
  the displayed input window and one readable status-plus-`$1800` capture.
  This is required to convert the Xemu environment and real-input deferrals
  into physical evidence.
- Owner review of that capture against
  `docs/testing/R0-B_FINAL_COMPOSITE_TEST_GUIDE.md`. No R0-B gate is closed
  by this handoff.

The candidate intentionally does **not** prove raster-atomic presentation,
audible latency/preemption, PCM/DMA playback, graphics-DMA contention,
ten-minute stability, RRB/affine behavior, or production renderer/input/audio
selection. Those are outside this bounded R0-B proof unless separately
authorized. The timed 512-write SID service satisfies the stated
representative-audio-service measurement; PCM/DMA is documented as deferred,
not silently counted as a pass.

No entry selects a production display mode, renderer, controls, audio format,
quality tier, palette, or cockpit art.
