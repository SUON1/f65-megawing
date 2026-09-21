# Current Project State

This records durable integrated project state. It is not a design authority,
contract, acceptance record, historical journal, or task log. Active task
status belongs in [WORK_IN_PROGRESS.md](WORK_IN_PROGRESS.md). Completed work is
recorded here only when it changes enduring project reality.

## Current baseline

- Integrated branch: `main`.
- Target platform: MEGA65.
- Implementation model: LLVM-MOS C is primary target code; selective 45GS02 assembly serves justified platform-critical or measured low-level work; Java and Python are host tooling languages.

The intended human-reviewed design hierarchy is:

1. F65 Main Concept v1.6 — master product and architecture authority.
2. F65 Gameplay and Simulation Supplement v1 — player-facing requirements authority.
3. F65 65Aero Engine Runtime and Technical Supplement v1 — `APPROVED CANDIDATE DESIGN - NOT FINAL`; the current implementation-architecture companion. Generated interface, ABI, memory-ledger, test, and evidence freeze closure remains required before FINAL status.
4. Flight Physics and Simulation Engineering White Paper v3.3.
5. Graphics Engineering White Paper v2.1.
6. Audio, Sound Effects and Music Engineering White Paper v1.0.
7. Radar / Sensors / Track Engineering White Paper v1.0.
8. AI Behavior and Decision Architecture White Paper v1.0.

This checkout now contains Main Concept v1.6, Gameplay v1, Runtime v1 candidate, Physics v3.3, Graphics v2.1, Audio v1.0, Radar/Sensors/Track v1.0, AI Behavior/Decision v1.0, and the supporting Product Story reference. The earlier Read-First, Architecture 1.5.1, and Draft 0.2 family remains at its existing paths as provenance only.

## Engineering state

R0-A and R0-B are closed bounded proof milestones; R0-D is closed for its
accepted calibration-proof scope. Under current Main Concept v1.6 authority,
R0-C is COMPLETE for the Revision 1.6 program baseline. Its retained historical
evidence remains truthful: the recorded owner disposition was a waiver rather
than a formal historical gate PASS, and no historical record is retroactively
relabeled. Remaining returning `StorageService` implementation is carried
forward and does not reopen Charlie. R0-E is closed only for its bounded
functional-proxy and raster-observation scope.

R0-F contains substantial bounded development and physical evidence. CF001 demonstrated a reset-only combined diagnostic with ROM backup/recovery, synthetic workload, IRQ/DMA/display/PCM/input activity, physical capture reduction, and retained SD integrity evidence. RH001 separately demonstrates a same-run ROM/storage lifecycle continuation in NTSC/PAL Xemu.

Full R0-F remains open. The CF001 and RH001 proofs are not co-resident; the documented MemoryAccessABI-compatible integration boundary, remaining parent-scope workload/phase/latency/IRQ coverage, complete evidence review, and named owner acceptance remain outstanding. Measured limits are not approved. Formal Phase 1 integrated 65Aero implementation has not started.

## What currently exists in code

- R0 proof programs and diagnostics under `src/r0a/`, `src/r0b/`, `src/r0c/`, `src/r0d/`, `src/r0e/`, and `src/r0f/`.
- R0 diagnostic models and narrow platform wrappers under `src/diagnostics/` and `src/platform/`.
- Generated interfaces and machine-readable contracts under `interfaces/`; ownership ledgers under `memory/`.
- Java/Python host tooling, builders, validators, and oracles under `tools/`.
- Retained evidence, handoffs, decisions, and plans under `docs/`.
- Placeholder or future production-module areas, not a completed 65Aero engine.

## Durable technical sequence

Complete and reconcile the remaining R0-F closure work without relabeling bounded evidence as full acceptance. Then establish measured limits through the applicable evidence and approval process. The integrated 65Aero Phase 1 harness follows only when its governing gates and contracts are ready.

## Project-truth debt

- The `spec/` corpus now distinguishes current authority, candidate Runtime v1, provenance, supporting references, and project-control records.
- Physics v3.3 is retained exactly as supplied. Its known formatting, glyph, and parent-reference debt, including modernization or re-rendering, is deferred until after repository reorganization and the new development system are complete.
- Broader technical-document consolidation is deferred until after repository reorganization and the new development system are complete.
- `F65_OFFICIAL_RECORD.md` retains configuration and R0 history; `CODEX_PROGRESS.md` retains the historical development journal. Neither is the routine live project-status interface.
- The current GitHub repository visibility is public. The historical bootstrap entry in `F65_OFFICIAL_RECORD.md` retains the earlier private-repository state as provenance; any later visibility change requires deliberate Git/project-control housekeeping.
