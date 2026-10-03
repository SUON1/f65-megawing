# Work in Progress

This is the sole routine active-work record, not project history or design
authority. Status is ACTIVE, BLOCKED, READY FOR REVIEW or NONE.

## Current status

- **Status:** `READY FOR REVIEW`
- **Task / Build Intent:** Owner's “Continue” on 2026-10-03 authorizes the narrow
  P08 audio-stop readback correction and local qualification. Fresh copied P08
  source; mask only sample-valid/stopped status bits 2/3, preserving every
  channel enable/configuration bit check and all other integrity checks.
- **Authority:** [Group 1 Build Intent](docs/plans/R0-F_GROUP1_BUILD_INTENT.md),
  [export amendment](docs/plans/R0-F_GROUP1_EXPORT_AMENDMENT.md), generated export
  contract and ledger; programming/C standards and D81 gate/workflow inspected.
  Branch `codex/r0f-group1-resume-clock`; remote main freshly verified unchanged
  at `c27d89787d1d5c4472e24262e0181c47943d46be`.
- **Experiment:** `build/r0f/group1/terminal-recovery/audio-readback-01/`.
  One changed target file, `source-inputs/src/diagnostics/r0f/group1_transport.c`.
  First fit PASS: resident end $BFF5, 11 bytes free, seven bytes smaller than P08.
- **Hardware contract:** Official core reference commit
  `bc7a3ece8aaee3d4d9f5df09cd71c70b1225a827`, `src/vhdl/gs4510.vhdl`, shows
  sample-valid bit 2 readback is not written by control writes, and stopped
  bit 3 may be asserted by hardware. Neither permits playback with enable clear.
  Installed physical core and actual rejected register bytes remain unrecorded.
- **Impact:** Same four reads at $D720/$D730/$D740/$D750, all now evaluated.
  Existing stop writes unchanged; ordinary C clobbers. No new CPU-visible or
  physical allocations, MAP/base-page, DMA, acquisition timing/deadline or IRQ/NMI
  effects. Terminal predicate lies outside acquisition. Generated/public ABI,
  capacities, reserves and original returning-storage lifecycle unchanged.
- **Validation:** Fit/static, native host, 1,298 transport cases, 2,624,256
  policy comparisons and 47 Python tests pass. Focused NTSC/PAL actual trace/SAVE
  and nominal timing pass; filename collision preserves original bytes. Fresh
  R0FG1P09.D81 passes structure/content and all four exact-name boots (2 NTSC,
  2 PAL); 3200 records/20 chunks and actual SAVE per run. XEMU_BOOT_VERIFIED only. Initial cap: two fit experiments / 30 minutes, no open-ended size work.
- **Physical boundary:** P08 failed 75/0A/0C80/1F/00. Actual returned program and
  tick-1600 SAVE pass; no trace. [Preserved evidence](docs/evidence/r0f/group1/2026-10-03-p08-physical/README.md).
  P08/P07/P06/P05 and older tested identities remain retired. Do not rerun them.
- **Scope:** No card writes, unmount/eject, physical execution, publication or
  Group 2 implementation. Group 1/full R0-F acceptance remains pending.
- **Preservation:** Prior reports/freezes, root target source, CURRENT_STATE and
  unrelated files remain unchanged. New tooling reuses the existing gated pipeline.

- **Local handoff:** [Audio readback report](docs/reports/R0-F_GROUP1_AUDIO_READBACK.md)
  and [frozen evidence](docs/evidence/r0f/group1/2026-10-03-audio-readback/README.md).
  P09 canonical SHA-256
  `bd1b645630c93d0ef764f3b6167924c0962ad67ed528d4ac8172ff2d4f9c5959`;
  PRG 37509 bytes, SHA-256
  `acc735f280f9d4e86b3b2040e5b2bed987908331f7899a87f5382c6cd23cd4d8`.
- **Next action:** Owner-run qualified P09 delivery, live allocation/hash/eject
  gates, then physical chooser/entry and terminal result. Return actual card
  for trace/SAVE reduction. No physical fix or acceptance is claimed from Xemu.
