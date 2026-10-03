# Work in Progress

This is the sole routine active-work record, not project history or design
authority. Status is ACTIVE, BLOCKED, READY FOR REVIEW or NONE.

## Current status

- **Status:** `BLOCKED`
- **Active task:** P07 terminal readiness subfault diagnostic, owner-authorized
  by “Execute” on 2026-10-03. Branch `codex/r0f-group1-resume-clock`; freshly
  verified remote main `c27d89787d1d5c4472e24262e0181c47943d46be`.
- **Build Intent:** Fresh copied P07 source, report the first failed readiness
  predicate using the existing status byte. Preserve every integrity check and
  boolean policy interface; two attempts/30-minute initial cap. Fit/host before
  focused NTSC/PAL and exact-carrier gates. No SD write, physical execution,
  publication, Group 2 work or acceptance included.
- **Result:** Two variants compile/link and pass protected IRQ/terminal static
  checks, but fail fit: readiness-01 ends $C012 (18 over); readiness-02 ends
  $C02C (44 over). Neither executed; no new D81 exists. Both preserved.
  Separate pure-policy differential tests pass 2,624,256 comparisons per
  variant under ASan/UBSan. No full host admission or emulator run occurred.
- **Handoff:** [Readiness diagnostic report](docs/reports/R0-F_GROUP1_READINESS_DIAGNOSTIC.md)
  and [frozen packet](docs/evidence/r0f/group1/2026-10-03-readiness-diagnostic/README.md).
- **Impact:** New pure private diagnostic API; original boolean wrapper retains
  semantics. Existing $2F98 status byte only; ordinary C clobbers. No hardware
  accesses added, physical allocation, MAP/base-page, DMA, deadline, IRQ/NMI,
  generated/public ABI, capacity or reserve changes.
- **Physical boundary:** P07 photograph shows 6F/0A/0C80/1F/00. Final readiness
  rejected after whole-trace CRC/freeze. Actual returned P07 original payloads
  and tick-1600 SAVE pass; no trace exists. Individual rejecting predicate is
  unknown. [P07 returned verification](docs/evidence/r0f/group1/2026-10-03-p07-physical/returned/README.md).
  Exact photo filename/PAL-NTSC confirmation remains unrecorded. Card remains
  mounted unchanged. P07/P06/P05 and older tested identities remain retired.
- **Next action:** Size-focused review of terminal reporting; the smaller new
  variant needs at least 18 bytes recovered with all integrity checks and
  reserves intact. Two-attempt initial cap reached; no third experiment run.
  No new physical carrier is ready. Group 1/full R0-F acceptance and Group 2
  progression remain pending. Do not rerun installers or tested carriers.
- **Preservation:** Original source/canonical PRGs, freezes, CURRENT_STATE,
  generated contracts and unrelated work unchanged. No commit/push/PR/merge.
