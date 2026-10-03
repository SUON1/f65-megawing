# Work in Progress

This is the sole routine active-work record, not project history or design
authority. Its status is one of ACTIVE, BLOCKED, READY FOR REVIEW or NONE.

## Current status

- **Status:** `BLOCKED`
- **Active task:** Group 1 terminal-preparation failure after P06. Owner
  authorized continued work on 2026-10-02. Branch
  `codex/r0f-group1-resume-clock`; remote main freshly verified at
  `c27d89787d1d5c4472e24262e0181c47943d46be`.
- **Build Intent:** Isolate terminal $6B using fresh copies of qualified P06,
  retaining all integrity predicates and original capacities. Initial bound:
  30 minutes/two target variants. Require fit/host before focused NTSC, PAL
  and exact-carrier gates. No additional SD/hardware delivery, publication,
  Group 2 implementation or acceptance is included.
- **Current result:** Both diagnostic variants fail resident fit: 42 and
  238 bytes over. Neither was executed or packaged. The second variant's
  native ASan/UBSan owner/capture/CRC checks and 83 codec rejects pass; this
  is host analysis only. The two-target-variant bound has been reached.
- **Handoff:** [Terminal diagnostic report](docs/reports/R0-F_GROUP1_TERMINAL_DIAGNOSTIC.md)
  and [preserved attempts](docs/evidence/r0f/group1/2026-10-02-terminal-diagnostic/README.md).
  The private return-code prototype is not an admitted implementation.
- **Physical evidence:** P06 reached `6B/0A/0C80/1F/00`: tick 3200 and all
  five resumed-service advancement bits, then terminal preparation failed.
  [Returned-card checks](docs/evidence/r0f/group1/2026-10-02-p06-physical/returned/README.md)
  pass structure, original payloads and actual tick-1600 SAVE. No G1Txx trace
  or terminal result exists. Exact inner terminal cause remains unknown.
  Explicit photo filename/video/platform confirmation remains unrecorded.
- **Preserved qualified source:**
  `build/r0f/group1/resume-recovery/clock-03-execution/source-inputs/`.
  PRG SHA-256 `9654d336deefe8dae0bd3b26986e00fbea45b8f3dcd8cfe0b1c73ac3f479ef7e`.
  P06 is retired after physical failure; P05 and earlier carriers also remain
  untouched. Do not rebuild root source and assume it reproduces P06.
- **Contract impact:** Prototype changes ordinary terminal C/private return
  semantics only. No generated/public ABI, capacity, reserve, MAP/base-page,
  DMA, register or IRQ/NMI policy changes. Both layouts exceed the resident
  bound and are therefore unqualified. Root target source remains unchanged.
- **Next action:** A new bounded continuation should test a smaller private
  terminal breadcrumb while preserving boolean interfaces and every guard.
  Measure full fit first; no savings are assumed. Do not run either failed
  PRG, repeat the P06 installer or retest P06. Group 2 has not started.
- **Preservation:** Prior 522-file resume packet and both physical manifests
  still match. CURRENT_STATE and historical freezes remain unchanged.
  Unrelated backup/mirror tools, reports and older physical directories remain
  untouched. No commit/push/PR/merge, new Xemu, SD write or hardware run occurred.

The former 994-line WIP remains in the original physical closeout packet.
The pre-terminal handoff WIP is retained in the new diagnostic packet.
