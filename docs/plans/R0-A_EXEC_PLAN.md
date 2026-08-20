# R0-A Execution Plan

This is an evidence log and forward plan, not a record of private reasoning.

## Baseline

| Field | Value |
|---|---|
| Base commit | `0f650e7fed72933a2ff9d5eaa9a9bd5a70e92975` |
| Working branch | `codex/r0-a-development` |
| Gate | R0-A; development GO, acceptance NOT PASSED |
| Task record | `docs/plans/r0-a-task-admission.json` |
| Scope policy | `docs/plans/r0-a-ownership-map.json` |

## Stage log

### 0. Configuration control — complete

- Read the repository controls and exact external authority set in Read-First order.
- Verified every supplied publication hash and the approval-record hash.
- Verified the named repository and remote head: `main` was clean at `0f650e7` and remote `main` resolved to the same commit.
- Added unedited approved and candidate source copies, preserved historical sources, updated the corpus manifest, README, record, and repository instructions.
- Command results: JSON parsing, source hash checks, and `git diff --check` passed.
- Commit: `5a97d63 chore(spec): synchronize approved R0 authority records`.

### 1. Governance and host-foundation admission — in progress

- Create the agent record, this plan, task-admission record, ownership/diff-scope map, stable acceptance registry, and module-status source.
- Implement an independent Java-host oracle and deterministic fixtures after verifying a project-local JDK.

### 2. Toolchain establishment — pending

- Pin an inspected local LLVM-MOS SDK archive and extracted binary identity in `toolchain/f65_toolchain.lock.json`.
- Verify the MEGA65 frontend, CPU-selection mechanism, object format, compiler driver expansion, map/symbol/disassembly tools, and C/assembly interoperability. Unknown fields remain `UNVERIFIED`.

Finding on 2026-08-20: LLVM-MOS v23.1.0 verifies the MEGA65 frontend and `-mcpu=mos45gs02` object flags/macros. Its default MEGA65 startup/link flow assigns compiler imaginary registers to `$0002–$008f`; retained disassembly confirms C uses that range. The governing ABI requires base page `$0200–$02FF`. The selected release's compatible 45GS02 base-page/startup mechanism has not been verified, so target conformance, D81, Xemu, and hardware stages are blocked rather than inferred.

### 3. Generated contracts and diagnostics — pending

- Implement canonical registry sources and generators for the R0-A subset, memory ledger, evidence schema, capacity skeleton, scope validation, status board, and golden vectors.

### 4. Target proof and D81 — pending

- Implement the smallest compiled-C proof, only admitted platform wrappers, observable result record, reproducible D81 path, and Xemu capture harness.

### 5. Evidence and handoff — pending

- Run clean host/build/Xemu reproduction; retain evidence and create the hardware guide, acceptance matrix, and handoff.

## Revalidation triggers

Any controlling document/status, compiler/SDK/runtime, linker/assembler, generated interface, wrapper, source, D81, ROM/core/system configuration, or Xemu identity change invalidates dependent R0 results.

## Current blockers

- The required `$0200` 45GS02 base-page/startup path is not verified for the selected LLVM-MOS release. The default driver emits compiler imaginary-register accesses at `$0002–$008f`.
- No verified D81 construction and auto-boot path exists, so the D81, Xemu, evidence, and hardware stages cannot start.
- `DEC-002` and `DEC-003` are open; they do not block construction but prevent formal scope/platform closure.
- Physical MEGA65 evidence requires the project owner after the reproducible D81 exists.
