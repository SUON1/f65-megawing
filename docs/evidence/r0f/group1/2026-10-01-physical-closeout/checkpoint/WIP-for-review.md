# Work in Progress

This is the sole routine active-work record, not project history or design
authority. Its status is one of ACTIVE, BLOCKED, READY FOR REVIEW or NONE.

## Current status

- **Status:** `READY FOR REVIEW`
- **Task:** Review/publication preparation for Group 1 campaign closeout.
- **Branch:** `codex/r0f-successor-physical-exact-carrier`.
- **Existing published checkpoint:** `2d9a42e110cdd9066031e28e83662ce4fdec6219`.
- **Owner intent:** Analyze the returned data, close this work unit and retain
  a compact handoff; publication/merge precede a new chat for remaining R0-F.
  No new implementation, SD write or hardware run is part of closeout.
- **Outcome:** Development campaign closed as a preserved checkpoint **with a
  physical blocker**, not a Group 1/R0-F PASS. Local fit/host/four exact-name
  Xemu runs pass. P05 SD hash, one extent, safe eject and physical entry pass.
  The physical run fails `5D/0A/0640/00/00` at display resume after tick 1600.
  Actual returned `RSSTATE` passes the independent tick-1600 golden; no trace
  chunks exist, so physical timing is unavailable.
- **Exact target:** PRG `c068cc532dc820845d8c0649b1c2ea7dfc0bda394b32f7c186088a04d0dc048b`,
  37517 bytes, resident end `$BFFD`, 3 free bytes. Root source is an earlier
  variant; the qualified version-7 source is the published isolated snapshot
  identified in the closeout report. Generated contracts are unchanged.
- **Retained failure:** P05 `046198fc...5ee4ff` and returned disk
  `9816043f...f4197d` are preserved. P05 is retired, INVALID — DO NOT USE;
  no rerun, repair, rename or overwrite. P04's ten-extent failure and the
  original `ec259fc7...` baseline remain unchanged.
- **Authority/evidence/handoff:** [Group 1 closeout](docs/reports/R0-F_GROUP1_CLOSEOUT.md)
  and [physical packet](docs/evidence/r0f/group1/2026-10-01-physical-closeout/README.md).
  Governing [Build Intent](docs/plans/R0-F_GROUP1_BUILD_INTENT.md) remains;
  this closeout does not waive its resumed-workload requirement.
- **Validation:** 47 fresh host tests; twelve prior freezes/7511 entries,
  original PRGs and P05 inputs match; four existing version-7 Xemu traces
  independently re-reduce. Actual returned structure/payload/SAVE checks pass.
  No new target build, Xemu launch or physical test. Hardware/ABI impact none.
- **Next:** Owner review, then separately authorized focused commit/push/PR and
  merge with fresh branch/remote/CI review. Leave unrelated dirty local backup,
  mirror tools/reports and older physical directories unstaged and intact.
  After merge, move to a fresh chat using the closeout handoff. First remaining
  R0-F task is the physical display-resume subfault/clock-order diagnostic;
  Groups 2/3, existing measurement boundaries and owner acceptance remain.
  No additional target feature is prescribed and no acceptance follows a merge.

The former 994-line WIP is retained byte-for-byte at
`docs/evidence/r0f/group1/2026-10-01-physical-closeout/WIP-before-closeout.md`.
Use it only for historical recovery, not routine startup.
