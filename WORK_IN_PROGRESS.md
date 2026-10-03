# Work in Progress

This is the sole routine active-work record, not project history or design
authority. Status is ACTIVE, BLOCKED, READY FOR REVIEW or NONE.

## Current status

- **Status:** `READY FOR REVIEW`
- **Task:** P09 physical resume/export proof and returned-card analysis, following
  owner photo S4/E00/F14 and “Cards in.” on 2026-10-03.
- **Authority:** Original Group 1 Build Intent, export amendment and measurement
  matrix; owner-authorized narrow audio readback correction and actual card
  verification. No new requirements, acceptance thresholds or target changes.
- **Result:** Actual P09 program/original payloads, 34-byte returning SAVE and
  all 20 physical trace chunks pass independent extraction/structure checks.
  Frozen version-7 reduction passes 3200 records, both 1600-tick epochs, 955
  world pairs and all existing integrity checks. Nominal timing is
  WITHIN_OBSERVED_BOUNDS: zero misses, below-20-Hz cohorts or uncertain boundaries.
  Physical resume/export blocker resolved for this bounded P09 fixture.
- **Evidence:** [Physical proof](docs/evidence/r0f/group1/2026-10-03-p09-physical/README.md)
  and [local build report](docs/reports/R0-F_GROUP1_AUDIO_READBACK.md).
  Actual returned D81 SHA-256:
  `ccd989151603fcfbeb130436c7be705e9b6f18804ce52012e142bdad1199a8ea`.
  Actual trace SHA-256:
  `e83b0b526c6fe22bb66285a93a25b8107da7c5c112d06f8ceb77af4cf6cc66dd`.
- **Qualified source:** `build/r0f/group1/terminal-recovery/audio-readback-01/source-inputs/`.
  PRG 37509 bytes, SHA-256
  `acc735f280f9d4e86b3b2040e5b2bed987908331f7899a87f5382c6cd23cd4d8`.
  Resident end $BFF5, 11 bytes free. Root working target is an older variant.
- **Preservation:** P09 is a protected successful tested identity; do not rerun,
  overwrite, repair or rename. P08/P07/P06/P05 and all earlier evidence remain
  unchanged. Card UUID 83FFC12E-67E1-307F-91AD-E584C2E01E87 was read-only verified
  and left mounted unchanged. No build, Xemu, card write/eject or publication
  occurred during this analysis. CURRENT_STATE and generated contracts unchanged.
- **Impact:** Off-card evidence/WIP only; target registers/clobbers, allocations,
  MAP/base-page, DMA, timing/deadline and IRQ/NMI effects non-applicable.
- **Boundary:** Full Group 1/R0-F acceptance, measured-limit approval and Phase 1
  remain pending. Trace reference/video are 2/$87; fresh named core/ROM/HYPPO/
  Freezer identities and explicit photo filename confirmation are unrecorded.
  Existing SI, phase, pool, latency and production-coverage limits remain.
- **Next action:** Review the bounded physical proof, then continue original
  remaining R0-F Groups 2-3 under their applicable Build Intent and existing
  admission/matrix boundaries. No passing-test replay or new feature checklist.
- **Publication:** Owner authorized commit and push on 2026-10-03. Freshly
  fetched origin/main and starting HEAD are both
  c27d89787d1d5c4472e24262e0181c47943d46be. Publish on the existing
  codex/r0f-group1-resume-clock branch; PR/merge remain subsequent steps.
  Include ten recovery/physical packets, seven reports, seventeen diagnostic
  tools/patches and this WIP. CI adds exact hash pins for the preserved P06
  returned D81 and original loader listing; no evidence bytes are normalized.
  Unrelated SD backup/mirror work and older physical directories are excluded.
  Publication does not grant full Group 1/R0-F or measured-limit acceptance.
