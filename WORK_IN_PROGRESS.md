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
- **Task:** Phase 9B — install minimal static-hygiene CI.
- **Branch:** `codex/ci-static-hygiene`.
- **Build Intent:** Add a portable, deterministic GitHub Actions safety net for
  incoming whitespace, tracked private/generated artifacts, and JSON, Python,
  and POSIX-shell syntax. Do not bootstrap toolchains, run target/emulator/
  hardware work, or modify product source, specifications, interfaces, ledgers,
  evidence, or build tooling.
- **Authorized area:** CI workflow and this active-work control record only.
- **Implemented:** `.github/workflows/ci.yml` provides read-only static CI for
  incoming whitespace, prohibited tracked artifacts, and JSON, Python, and
  POSIX-shell syntax.
- **Validation/evidence tier:** Documentation/static validation passed locally:
  all tracked JSON, Python, and shell files passed their syntax checks; the
  tracked-artifact guard passed; Ruby Psych parsed the workflow YAML; working-
  tree whitespace passed; and PR-style and push-style range checks passed in a
  disposable Git clone containing the task changes. Host-oracle, target, Xemu,
  D81, SD-transfer, physical-MEGA65, and human-acceptance evidence tiers are not
  applicable and were not run.
- **Next action:** Founder review of the focused uncommitted diff. Do not commit,
  push, open a Pull Request, or change GitHub settings before approval.
