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

Finding on 2026-08-20: LLVM-MOS SDK v23.1.0 (`7e47e7d`) retains logical compiler ABI registers at `$0002–$0021`; the stock driver also requests 110 general LTO direct-page bytes. The user-authorized R0-A remedy retains those logical ABI symbols, adds a 45GS02 `B=$02` transition in `.init.011` after stock `.init.010`, disables general LTO direct-page allocation with `-mlto-zp=0`, and restores `B=$00` in `.fini.989` before stock `.fini.990`. Static map/disassembly validation is passing; Xemu and hardware runtime validation remain pending.

### 3. Generated contracts and diagnostics — pending

- Implement canonical registry sources and generators for the R0-A subset, memory ledger, evidence schema, capacity skeleton, scope validation, status board, and golden vectors.

### 4. Target proof and D81 — pending

- Implement the smallest compiled-C proof, only admitted platform wrappers, observable result record, reproducible D81 path, and Xemu capture harness.

### 5. Evidence and handoff — pending

- Run clean host/build/Xemu reproduction; retain evidence and create the hardware guide, acceptance matrix, and handoff.

## Revalidation triggers

Any controlling document/status, compiler/SDK/runtime, linker/assembler, generated interface, wrapper, source, D81, ROM/core/system configuration, or Xemu identity change invalidates dependent R0 results.

## Current blockers

- VICE 3.10 `c1541` reproducibly formats and verifies an 80-track D81 containing a BASIC-65 `AUTOBOOT.C65` and the proof PRG; the D81 has passed its Xemu boot/run result.
- The version-pinned `xmega65` binary, initialized local SD image, and owner-supplied ROM execute the D81/autoload/capture runner. `R0A-XEMU-001` verifies the expected target result block and screen markers. The B-register sentinel proof still requires physical-MEGA65 execution; Xemu is not a runtime hardware PASS.
- `DEC-002` and `DEC-003` are open; they do not block construction but prevent formal scope/platform closure.
- Physical MEGA65 evidence requires the project owner after the reproducible D81 exists.
