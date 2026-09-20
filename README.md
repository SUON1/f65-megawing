# F-65 Megawing

F-65 Megawing is a cockpit-primary combat-flight simulator for the MEGA65.

LLVM-MOS C is the primary MEGA65 target language. Selective handwritten 45GS02 assembly is retained for platform-critical or measured low-level work. Java and Python provide host engineering, generators, oracles, and validation tooling; they are not the production MEGA65 game runtime.

## Current development state

`main` contains the integrated R0-A through current R0-F engineering lineage. Retained R0-A through R0-E proof history, substantial R0-F development, and bounded R0-F physical evidence are present.

R0-F is not silently declared complete: remaining closure and integration obligations, including the integrated no-restart lifecycle boundary and wider parent-scope coverage, remain open. Measured limits are not approved. The R0 proof and diagnostic code is not equivalent to a completed production 65Aero engine; formal Phase 1 integrated 65Aero implementation has not started.

## Where to start

1. Read [CURRENT_STATE.md](CURRENT_STATE.md).
2. Read [WORK_IN_PROGRESS.md](WORK_IN_PROGRESS.md).
3. Read [AGENTS.md](AGENTS.md).
4. Read [the development workflow](docs/DEVELOPMENT_WORKFLOW.md).
5. Read the applicable governing design documents, interfaces, ledgers, subsystem material, evidence, and validation tooling before changing anything.
6. For C work, read [the C style guide](docs/CODE_STYLE_C.md).

`CURRENT_STATE.md` is the durable integrated project record. `WORK_IN_PROGRESS.md`
is the active task record. [F65_OFFICIAL_RECORD.md](F65_OFFICIAL_RECORD.md)
retains configuration and R0 history; [CODEX_PROGRESS.md](CODEX_PROGRESS.md) is a
historical development journal. Normal work does not require reading either
historical record in full.

The routine control documents summarize state and process; they do not replace
the governing design documents, generated contracts, or evidence.

## Repository layout

- `spec/` — preserved specification corpus; its current authority hierarchy is recorded in `spec/manifests/spec-corpus.json`.
- `docs/` — workflow, decisions, plans, reports, testing material, and retained evidence.
- `src/` — R0 proof programs, diagnostics, and platform wrappers; much of this is evidence software, not a completed production engine.
- `interfaces/` and `memory/` — machine-readable contracts, generated bindings, and ownership ledgers.
- `tools/` — build, generator, diagnostic, validator, and host-oracle tooling.
- `tests/` — host, target, fixture, and retained-evidence tests.
- `assets/`, `missions/`, `toolchain/`, `build/`, and `dist/` — controlled assets, mission material, pinned tools, and generated output areas.

## Building and testing

Current build and validation entry points live under `tools/build/` and `tools/diagnostics/`; use the commands and evidence tier required by the applicable subsystem or handoff rather than assuming one universal command.

Before any D81-related work, read and obey [00_D81_LOADABILITY_GATE.md](00_D81_LOADABILITY_GATE.md).
