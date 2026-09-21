# Work in Progress

This is the sole routine active-work record. It is not a project history or
design authority. Its operational status is exactly one of: `ACTIVE`,
`BLOCKED`, `READY FOR REVIEW`, or `NONE`.

It records the current task, branch, Build Intent summary or link, governing
authority, authorized area, blocker if any, validation/evidence state, and exact
next action. If no substantive work is active, status is `NONE`.

Completed work leaves this file. Durable project changes belong in
`CURRENT_STATE.md` only when they change enduring project reality.

## Current status

- **Status:** `READY FOR REVIEW`
- **Task:** R0 Closeout T01 - re-baseline remaining R0-F closure against the
  reorganized repository.
- **Branch:** `codex/r0f-closeout-t01-rebaseline`
- **Build Intent:** Reconcile current Main v1.6 / Gameplay v1 / Runtime v1 and
  subsystem authority with retained R0 evidence; define the minimum successor
  combined proof without beginning its implementation.
- **Governing authority:** `spec/manifests/spec-corpus.json` current authority
  order; Main Concept v1.6; Gameplay v1; Runtime v1 candidate; current Physics,
  Graphics, Audio, Radar/Sensors/Tracks and AI papers; retained R0 decisions,
  contracts, ledgers and evidence for their stated scope.
- **Authorized area:** Documentation/control records only. No target source,
  generated interface, memory ledger, D81, evidence artifact, specification,
  dependency or toolchain change.
- **Validation state:** Founder-approved minor corrections applied. Tracked
  JSON, Python and shell syntax; R0A configuration validation; all present
  specification-manifest hashes; changed Markdown local links and whitespace;
  tracked-artifact guard; branch ancestry; changed-path scope; and
  `git diff --check` pass. Target, Xemu, D81, SD and physical MEGA65 tiers were
  not run.
- **Exact next action:** Founder verifies the corrected T01 packet and may then
  separately authorize commit/push. Do not start T02 or perform D81 work.
