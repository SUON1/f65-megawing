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
- **Task:** R0 Closeout T04 - founder-requested source/provenance remediation.
- **Branch:** `codex/r0f-successor-emulator-exact-carrier`
- **Build Intent:** Preserve the accepted T04 runtime behavior and frozen
  T02/T03 architecture while correcting the fail-closed evidence chain. First
  commit and push every reproducing target/loader/builder/validator/oracle
  source. Then rebuild from that clean commit, require the exact accepted PRG
  and D81 identities, mount every Gate-3 disposable copy with basename
  `R0FSUCC10.D81`, regenerate all direct/carrier/fault evidence with the source
  commit identity, and commit/push the corrected evidence separately.
- **Governing authority:** `spec/manifests/spec-corpus.json` current authority
  order; Main Concept v1.6; Gameplay v1; Runtime v1 candidate; T01 successor
  reconciliation; frozen T02 contracts/ledgers; reviewed T03 implementation,
  private integration contract/ledger and handoff; and
  `00_D81_LOADABILITY_GATE.md`. The verbatim mandatory D81 prompt header and
  execution order are retained in
  `docs/plans/R0-F_SUCCESSOR_EMULATOR_EXACT_CARRIER_EXECUTION.md`.
- **Authorized area:** Bounded successor entry corrections required by direct
  Xemu diagnosis; T04-only carrier bootstrap, host builder/validator/oracle
  tooling, canonical carrier and disposable Xemu-run artifacts, retained
  runtime evidence/manifests, WIP and focused handoff. No public ABI,
  high-level memory map, frozen range, 100 Hz/stage order, production
  StorageService, SD-card, physical hardware, measured-limit or R0-F
  acceptance change.
- **Validation state:** Founder review accepted T04 runtime behavior but
  withdrew the Gate-3 provenance claim: prior carrier copies were mounted as
  `run.D81`, and manifests identified the pre-T04 baseline commit. Those runs
  remain preserved historical diagnostics and are not final Gate-3 evidence.
  Live local `main`, `origin/main` and GitHub `main` were
  verified at `e3cf022c73e76679d85532795d9f79095fa8ead5` before branch creation.
  A fresh full T03 regression reproduced the reviewed PRG byte-for-byte:
  21,489 bytes, SHA-256
  `43074a4322b9a2ec35428e966d9f64ab30655c8f0f27516317e7e3f9e417264a`;
  resident use was 23,665 / 40,959, high-water `$7C72`, protected end `$2B0F`
  and reserve use zero. Direct execution exposed entry-order/MAP assumptions;
  the bounded corrections produced a 21,481-byte PRG with SHA-256
  `d0979c56c373f8885e4741670141ebf22c0a2e9ef8a84f6a931eaef05592d9df`,
  resident use 23,657 / 40,959, high-water `$7C6A`, protected end `$2B07`, no
  new physical allocation and zero reserve use. Direct NTSC/PAL and two fresh
  exact-carrier runs per mode pass with lineage `D9EEAB81` to `307A70D6`, full
  service mask `$1F`, independently verified SAVE payload and unchanged
  canonical hash. Canonical `R0FSUCC10.D81` is 819,200 bytes, SHA-256
  `3721dff9b84cfb7842cc154f6885861e0c7cbd3c3408c8ecec190bf6b405d461`,
  prior run is retained as historical diagnostic evidence. Source-freeze
  commit `20b2aab382d0590037443b6a352fbc77fda7aa42` was pushed before the clean
  rebuild. Corrected direct NTSC/PAL, two NTSC plus two PAL exact-carrier runs,
  and missing/invalid-token plus corrupted-result/SAVE reducer lockouts all
  pass from that commit. Every exact-carrier copy was mounted with basename
  `R0FSUCC10.D81`; every corrected manifest records the source-freeze commit.
  SD and physical tiers were not run and remain prohibited.
- **Exact next action:** Founder review of the separately committed and pushed
  corrected provenance/evidence set. Do not open or merge a PR, copy to SD,
  perform physical work, start T05 or freeze measured limits without separate
  authorization.
