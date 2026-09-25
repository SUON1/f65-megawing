# F-65 Repository Instructions

These instructions apply to every task in this repository.

## Before work

1. Read [CURRENT_STATE.md](CURRENT_STATE.md) and [WORK_IN_PROGRESS.md](WORK_IN_PROGRESS.md).
2. Read [the development workflow](docs/DEVELOPMENT_WORKFLOW.md).
3. Inspect the applicable governing design documents, interfaces, memory ledgers, implementation, and validation tooling.
4. For C work, read [the C readability standard](docs/CODE_STYLE_C.md).
5. Before any D81-related task, read and obey [00_D81_LOADABILITY_GATE.md](00_D81_LOADABILITY_GATE.md).
6. For D81 construction or delivery, follow [the reproducible D81 workflow](docs/D81_WORKFLOW.md). Use exact uppercase FAT 8.3 names, fresh single-session construction, independent extraction/structure checks, and fresh exact-name Xemu copies. Never mount the canonical image writable.

## D81 engineering requirements

- Image construction and SD allocation are separate gates. A correct 819,200-byte image and matching hash do not guarantee a mountable SD file.
- Do not rely on macOS `F_PREALLOCATE` success as a contiguity guarantee: the observed FSKit FAT implementation ignores its contiguous flag. Do not claim the SD card is defective from candidate fragmentation.
- The host-created replacement workflow uses a hash-pinned official MEGA65 allocator, independently qualified on disposable fragmented FAT32 fixtures. Any raw-card write requires explicit owner authorization, an unmounted positively identified partition, clean read-only filesystem checks, bounded free-run preflight, no existing destination/alias, retained metadata, and staged/final raw hash/one-extent checks. See the workflow for the unverified physical boundary and qualification command.
- Never require repeated owner-created blank images as the normal build process. Never overwrite, repair, rename or retest a failed carrier. Retain failed identities and evidence.
- Respect owner-selected transfer boundaries. If the owner chooses Finder, provide the exact host path, do not transfer automatically, and require a read-only allocation audit after copying. Do not claim Finder guarantees one extent.
- Do not call a candidate hardware-loadable until its exact SD copy passes physical chooser and entry-load verification. Keep R0-F runtime acceptance separate; stop the wider test sequence until the carrier gate passes.

Do not routinely read all of [F65_OFFICIAL_RECORD.md](F65_OFFICIAL_RECORD.md)
or [CODEX_PROGRESS.md](CODEX_PROGRESS.md). Consult them when historical or
configuration context is actually needed.

State the inspected authority and contracts before the first edit. Identify affected registers/clobbers, CPU-visible and physical memory, MAP/base-page, DMA, timing/deadline, and IRQ/NMI effects; mark non-applicable items explicitly.

## Recovery and Build Intent

When resuming work, inspect `WORK_IN_PROGRESS.md`, the current branch and
`git status`, the current diff and recent commits, and the governing Build
Intent. Continue from repository state rather than reconstructing progress from
chat memory; do not restart merely because the conversation changed.

Substantive work requires an approved Build Intent before implementation. It
may be in the task prompt, summarized or linked from WIP, or stored as a
dedicated task record when complexity warrants it. A permanent file is not
required for every trivial change.

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

Provide a useful handoff with changed paths, contract and hardware impact,
validation run, evidence tiers not run, unresolved risks, and the recommended
next action. State generated-artifact status and evidence identity when
applicable.

## Git

Use focused branches and review before merge. Do not routinely force-push or rewrite history for cosmetic cleanup. Keep commits focused and handoffs clear.

## Historical and evidence material

Preserve retained R0 proof source and evidence. Existing evidence-bearing code is not a repository-wide style-migration target merely because a newer C style guide exists.
