# F-65 Repository Instructions

These instructions apply to every task in this repository.

## Before changing code or contracts

1. Read `F65_OFFICIAL_RECORD.md` first.
2. Read the frozen architecture source under `spec/architecture/` completely, including its memory map and MemoryAccessABI requirements.
3. Read the current files under `memory/`, the calling conventions and public contracts under `interfaces/`, and every relevant subsystem specification/document before editing. If an expected contract does not yet exist, state that explicitly; do not invent it.
4. Before the first edit, state which files, requirements, interfaces, memory-map entries, and contracts were inspected.
5. Identify the affected 45GS02 registers and clobbers, CPU-visible and physical memory ranges, MAP/base-page state, DMA behavior, timing/deadline effects, IRQ/NMI behavior, and validation commands. Mark non-applicable items explicitly.

## Authority and scope

- Read the approved Read-First supplement and current approval record before applying candidate Architecture 1.5.1, Gameplay 0.2, or Engine 0.2. `AD-001` authorizes bounded R0 proof development; it does not pass a gate or approve a candidate parent document.
- C compiled with LLVM-MOS is the primary target language. Handwritten 45GS02 is limited to documented platform wrappers, interrupt/startup paths, or a measured and admitted compiler gap. Target changes must compile/link, generate maps/symbols/listings or disassembly, and have Xemu plus physical-evidence obligations recorded.

- Never treat Draft, Proposed, `TBD`, `TARGET`, `R0-GATED`, recommendation, or planning-assumption text as approved shipping behavior.
- Never modify architecture, CoreRuntime, public ABI, memory ownership, tick order, pool capacities, reserves, or another module's private state merely to simplify implementation.
- Never modify preserved source specifications unless the user explicitly tasks that source-document change.
- Prefer generated machine-readable contracts and constants over duplicated handwritten layouts.
- Stop and report a material contradiction or undocumented hardware dependency instead of choosing an interpretation.
- Never invent unverified MEGA65/45GS02/VIC-IV/DMAgic behavior. Mark uncertainty, consult the pinned official project references, and require measured evidence where specified.
- Keep gameplay and production-engine implementation outside R0-A until the governing gates open.

## Verification and handoff

- Assemble the affected target and run the applicable host, Xemu, and physical-target tests after changes. If a required tier is unavailable, report that fact and do not claim it passed.
- R0-A source must expose observable proof results and machine-readable evidence, preserve canonical MAP/base-page/IRQ state on every public exit, and account for C runtime, wrappers, code, data, stack, DMA, and reserve use in the generated ledgers.
- Run all relevant validation before committing and list the exact commands and results in the handoff.
- Update the memory map or append a decision-log entry whenever a shared memory, ABI, ownership, timing, IRQ, DMA, serialization, or lifecycle contract changes.
- Include inspected files/contracts, changed paths, register/memory/timing impact, generated-artifact status, tests, evidence identity, and unresolved risks in every coding-task handoff.
