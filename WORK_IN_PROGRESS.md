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
- **Task:** R0 Closeout T02 - successor memory/lifecycle contract and static
  admission.
- **Branch:** `codex/r0f-successor-memory-lifecycle-admission`
- **Build Intent:** Prove statically that one successor R0-F harness can combine
  CF001 and RH001 responsibilities within current memory ownership,
  PlatformABI / MemoryAccessABI rules and reserve policy, without building the
  full successor workload.
- **Governing authority:** `spec/manifests/spec-corpus.json` current authority
  order; Main Concept v1.6; Gameplay v1; Runtime v1 candidate; current Physics,
  Graphics, Audio, Radar/Sensors/Tracks and AI papers; retained R0 decisions,
  contracts, ledgers and evidence for their stated scope.
- **Authorized area:** One private successor machine-readable contract and
  generated constants; lifetime-aware ledger; pre-C/startup/linker skeleton;
  host lifecycle and integrity tests; compile/link/map/symbol/disassembly
  validators; and focused T02 handoff. No full workload, public ABI, high-level
  map, timing/stage-order, D81, Xemu, SD, hardware or production StorageService
  change.
- **Validation state:** Founder-approved static-ledger correction applied.
  `$010000-$011FFF` has exclusive application ownership outside the exact
  `KERNAL_ACTIVE` / `STORAGE_COMPLETE` / `KERNAL_CONTEXT_RESTORED` overlay;
  application restoration precedes `SERVICES_RESUMED`, and authoritative
  simulation does not advance during KERNAL ownership. Exhaustive range-pair
  validation passes and rejects three negative cases: undeclared overlap,
  concurrent incompatible lifetimes and missing DOS/application exclusion.
  The complete T02 build passes generated-binding, native ASan/UBSan, fresh
  CF001/RH001 predecessor, LLVM-MOS compile/link, protected code/data linker,
  map/symbol/disassembly and conservative fit checks. Post-correction charge
  remains 40,023 / 40,959 resident bytes with 936 bytes margin, 5,664 guarded
  Attic transition bytes and zero measured-reserve bytes. JSON/Python syntax,
  generated reproducibility, Markdown links, whitespace/diff and changed-path
  scope checks pass. D81, Xemu, SD and physical MEGA65 tiers were not run.
- **Exact next action:** Founder reviews the corrected T02 ledger, exhaustive
  validator, protected resident rule, generated accounting and handoff. Do not
  commit, push, open a PR, start T03 or perform D81/Xemu/hardware work before
  separate authorization.
