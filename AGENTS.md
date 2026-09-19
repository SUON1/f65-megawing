# F-65 Repository Instructions

These instructions apply to every task in this repository.

## Before changing anything

1. Read [CURRENT_STATE.md](CURRENT_STATE.md) and [WORK_IN_PROGRESS.md](WORK_IN_PROGRESS.md).
2. Read [the development workflow](docs/DEVELOPMENT_WORKFLOW.md).
3. Inspect the applicable governing design documents, interfaces, memory ledgers, implementation, and validation tooling.
4. For C work, read [the C readability standard](docs/CODE_STYLE_C.md).
5. Before any D81-related task, read and obey [00_D81_LOADABILITY_GATE.md](00_D81_LOADABILITY_GATE.md).

State the inspected authority and contracts before the first edit. Identify affected registers/clobbers, CPU-visible and physical memory, MAP/base-page, DMA, timing/deadline, and IRQ/NMI effects; mark non-applicable items explicitly.

## Scope and authority discipline

- Follow the approved Build Intent; do not casually expand scope.
- Do not delete, rewrite, or mass-restyle uncertain legacy material, proof source, or retained evidence without explicit approval.
- Do not silently resolve design contradictions. Record the conflict, identify the owner, and stop when implementation would choose an outcome.
- Do not promote drafts, `TBD`, `TARGET`, `R0-GATED`, measured values, or planning assumptions by implementation convenience.
- Preserve subsystem ownership and generated-contract authority. Do not duplicate generated public layouts by hand.
- Navigation documents summarize state; they do not replace governing design documents, generated interfaces, or measured evidence.

## C and low-level work

LLVM-MOS C is the primary target implementation language. Use handwritten 45GS02 assembly only for justified platform-critical or measured work, behind the applicable narrow contract.

Generated and public interfaces govern layouts. Respect hardware ownership boundaries and understand register, memory, MAP/base-page, DMA, IRQ, and restoration effects before changing low-level code. C formatting and readability requirements are in [docs/CODE_STYLE_C.md](docs/CODE_STYLE_C.md), not duplicated here.

## Validation and handoff

Run validation appropriate to the task and report exact commands and results. Compile/link, host, Xemu, and physical evidence each establish only their own tier; Xemu never substitutes for physical MEGA65 evidence where physical proof is required.

Record changed paths, contract and hardware impact, generated-artifact status, evidence identity, tests run or not run, unresolved risks, and the recommended next action.

## Git

Use focused branches and review before merge. Do not routinely force-push or rewrite history for cosmetic cleanup. Keep commits focused and handoffs clear.

## Historical and evidence material

Preserve retained R0 proof source and evidence. Existing evidence-bearing code is not a repository-wide style-migration target merely because a newer C style guide exists.
