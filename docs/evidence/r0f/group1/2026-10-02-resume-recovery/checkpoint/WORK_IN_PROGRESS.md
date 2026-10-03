# Work in Progress

This is the sole routine active-work record, not project history or design
authority. Its status is one of ACTIVE, BLOCKED, READY FOR REVIEW or NONE.

## Current status

- **Status:** `READY FOR REVIEW`
- **Active task:** Bounded Group 1 post-storage display-resume correction,
  owner authorized by "Build it" on 2026-10-02. Branch
  `codex/r0f-group1-resume-clock`, baseline `c27d89787d1d5c4472e24262e0181c47943d46be`;
  current remote main and baseline static CI verified.
- **Review handoff:** [Resume recovery](docs/reports/R0-F_GROUP1_RESUME_RECOVERY.md)
  and [local evidence packet](docs/evidence/r0f/group1/2026-10-02-resume-recovery/README.md).
  Original [P05 closeout](docs/reports/R0-F_GROUP1_CLOSEOUT.md) remains the
  physical authority: `5D` at tick 1600; no Group 1/R0-F acceptance.
- **Build Intent:** Under the original [Build Intent](docs/plans/R0-F_GROUP1_BUILD_INTENT.md)
  and closeout carry-forward, copy the immutable version-7 P05 source into
  `build/r0f/group1/resume-recovery/clock-03/source-inputs/`. Restart the existing
  CIA clock before display-clear DMA, preserve first-fault identity, and verify
  restoration/IRQ ordering. Initial diagnostic cap: 30 minutes/two targeted
  experiments from 2026-10-02 15:30 PDT. Require fit/host before focused NTSC,
  then PAL and fresh exact-carrier gates. Completion is a reviewable local
  correction or a retained bounded blocker with evidence. Physical causality
  and resumed-workload proof remain outstanding until a separately authorized
  hardware test. No feature/capacity/threshold change, SD/hardware delivery,
  commit/push/PR/merge or acceptance is included. P05 remains retired.
- **Contract impact:** CIA1 clock initialization and its existing raster IRQ
  start occur after canonical restore/context invalidation/ROM reclaim and
  before display DMA. Handler has no display/DMA/audio dependency; acquisition
  is inactive. Raster selection remains after display setup. C ABI clobbers
  remain compiler-managed; existing VIC/CIA/DMA registers and memory ranges
  only. No new allocation, MAP/base-page, handler, NMI or deadline change.
- **Completed local gates:** Second target variant fits at `$BFF1` (15 bytes
  free); native ASan/UBSan ordering/fault and owner tests pass; 47 Group 1
  tests pass. Focused NTSC/PAL and four fresh P06 clean boots pass, 3200 records
  and 20 chunks each. P06 is `XEMU_BOOT_VERIFIED` only. Two target variants
  completed within eight minutes; subsequent work qualified that same PRG.
- **Exact live source:** `build/r0f/group1/resume-recovery/clock-03-execution/source-inputs/`.
  PRG SHA-256 `9654d336deefe8dae0bd3b26986e00fbea45b8f3dcd8cfe0b1c73ac3f479ef7e`.
  Target change is reproducible from the immutable P05 snapshot and
  `tools/diagnostics/r0f_group1_resume_clock.patch`; do not rebuild root source
  and assume it produces P06.
- **Next action:** Owner review, then separately authorized SD/hardware delivery
  if accepted. Physical subfault and resumed-workload proof remain open.
  P05 stays retired. Commit/push/PR/merge have not occurred.
- **Local preservation:** Unrelated backup/mirror tools, reports and older
  physical directories remain untracked and untouched. The original passing
  `ec259fc7...` baseline and all frozen evidence remain unchanged.

The former 994-line WIP is retained byte-for-byte at
`docs/evidence/r0f/group1/2026-10-01-physical-closeout/WIP-before-closeout.md`.
Use it only for historical recovery, not routine startup.
