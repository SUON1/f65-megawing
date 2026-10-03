# Work in Progress

This is the sole routine active-work record, not project history or design
authority. Its status is one of ACTIVE, BLOCKED, READY FOR REVIEW or NONE.

## Current status

- **Status:** `READY FOR REVIEW`
- **Active task:** Group 1 terminal-only status-byte diagnostic, explicitly
  authorized by the owner on 2026-10-02. Branch
  `codex/r0f-group1-resume-clock`; remote main verified at
  `c27d89787d1d5c4472e24262e0181c47943d46be`.
- **Build Intent:** Expose P06's terminal failure through an existing private
  status byte, keeping every integrity predicate and boolean interface.
  Fresh copied P06 source; initial two-variant/30-minute diagnostic bound.
  Fit/host before focused NTSC/PAL and exact-carrier gates. No new SD write,
  physical run, publication, Group 2 implementation or acceptance included.
- **Review handoff:** [Terminal-status report](docs/reports/R0-F_GROUP1_TERMINAL_STATUS.md)
  and [frozen evidence](docs/evidence/r0f/group1/2026-10-02-terminal-status/README.md).
- **Implementation:** Existing protected byte $2F98 marks terminal intervals
  6B DOS copy, 6C capture setup, 6D trace integrity, 6E transport validation,
  6F readiness. Terminal exporter then owns its existing status values.
  Four three-byte INC instructions save 16 bytes versus ordinary volatile C.
  No allocation, generated/public interface, capacity or reserve changes.
  INC changes N/Z and the named byte; compiler cc/memory clobbers declared.
  No general-register, MAP/base-page, hardware-register, DMA or IRQ/NMI changes.
- **Completed gates:** Second variant fits at $BFFE, 2 bytes free. Native
  sanitizer/owner/resume tests pass, 17 terminal transport cases pass, every
  capture/transport executable predicate matches P06 after removing marker
  calls, and 47 Group 1 Python tests pass. Focused NTSC/PAL, collision/no-
  overwrite case and four exact-name P07 boots pass. Each successful run
  exports 3200 records and 20 chunks with nominal timing within observed bounds.
- **Exact identity:** PRG 37518 bytes, SHA-256
  `35f51114c5016b0e29962e038c48d7f48b9e8abca2136bdb0fe889f4c7570bae`.
  Source: `build/r0f/group1/terminal-recovery/status-02/source-inputs/`.
  P07: `build/r0f/group1/carriers/R0FG1P07/canonical/R0FG1P07.D81`,
  819200 bytes, SHA-256
  `138644c5066288ba5e635cced33633c6f2c75902482566e9a6f24ccfe5e8daf3`.
  State `XEMU_BOOT_VERIFIED` only; no SD or physical qualification.
- **Physical boundary:** P06 reached tick 3200/mask 1F then failed 6B. Actual
  SAVE and original payloads pass; no trace exists. The inner cause remains
  unknown. P06, P05 and older tested identities stay retired and untouched.
  Photo filename/video/platform confirmations remain unrecorded. Group 2 has
  not started; Group 1 and full R0-F acceptance remain ungranted.
- **Next action:** Review the marker diagnostic and exact P07 identity; any
  owner-approved physical retest requires its own live SD/chooser gates.
  Do not rebuild root source, rerun either non-fitting diagnostic, retest P06
  or repeat its installer. Commit/push/PR/merge are separate and have not occurred.
- **Preservation:** The first new status variant fails fit by 14 bytes and was
  never executed; the previous return-code attempts remain preserved. Prior
  freezes, CURRENT_STATE and unrelated untracked work are unchanged. New work
  uses off-card build/evidence paths only.
