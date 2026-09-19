# F-65 Development Workflow

## Purpose

F-65 development uses small, reviewable tasks with explicit authority, validation, and human acceptance. The workflow applies to human and AI-assisted work and does not change specification precedence, approve candidate material, or waive any engineering gate.

```text
ChatGPT discussion / design
        ↓
Build Intent
        ↓
focused Codex task
        ↓
task branch
        ↓
implementation
        ↓
validation
        ↓
founder review
        ↓
commit / push
        ↓
GitHub Pull Request
        ↓
merge to main
        ↓
closeout / project-truth update if needed
```

## 1. Discuss and define the Build Intent

Start by stating the outcome, why it is needed now, and what is explicitly out of scope. Identify the governing approved documents, candidate documents, interfaces, memory ownership, evidence tier, and human decisions involved.

Do not turn a draft, proposal, `TBD`, `TARGET`, `R0-GATED` value, or planning assumption into shipping behavior. Stop and escalate material contradictions or missing authority rather than choosing a convenient interpretation.

## 2. Create a focused task and branch

Give Codex one bounded objective with acceptance criteria and prohibited changes. Use a task-specific branch created from the verified current `main`. Keep unrelated cleanup, refactoring, specification changes, and repository housekeeping out of the task.

Before editing, inspect the current project-truth documents, repository instructions, governing specifications, affected interfaces and memory ledgers, relevant implementation, and applicable validation tooling. Record expected register, memory, MAP/base-page, DMA, timing, and IRQ/NMI impact, including items that are not applicable.

## 3. Implement within ownership boundaries

Make the smallest coherent change that satisfies the Build Intent. Preserve generated-file ownership and use generated contracts instead of duplicating layouts or constants. Do not change architecture, public ABI, memory ownership, timing order, capacities, reserves, or another module's private state merely to simplify implementation.

For C work, follow [`CODE_STYLE_C.md`](CODE_STYLE_C.md). Existing evidence-bearing R0 code is not a style-migration target unless a task explicitly authorizes that work.

## 4. Validate at the required evidence tier

Run the checks appropriate to the change and report the exact commands and actual results. Depending on scope, validation may include:

- focused static or schema checks;
- host unit, oracle, sanitizer, and negative tests;
- target compile, link, map, symbols, listing, or disassembly checks;
- D81 structural and content gates;
- Xemu execution; and
- physical MEGA65 evidence and human observation.

One evidence tier does not substitute for another. If a required tier is unavailable, report it as not run and do not claim it passed. Documentation-only changes should still receive link/path checks, whitespace checks, and a diff review.

## 5. Founder review

Present the focused diff, validation results, architecture or contract impact, evidence identity, limitations, and unresolved risks to the founder. Human review owns product decisions, approvals, waivers, measured-limit acceptance, and other decisions reserved by project authority.

Address review feedback on the same task branch when it remains in scope. Split materially different work into another Build Intent and branch.

## 6. Commit, push, and open a Pull Request

After review readiness:

1. Confirm the diff contains only intended files.
2. Confirm generated artifacts are current or explicitly not applicable.
3. Commit one coherent change with a specific imperative message.
4. Push the task branch and configure upstream tracking.
5. Open a focused GitHub Pull Request against `main`.

The Pull Request should explain the Build Intent, why now, scope boundaries, changed areas, acceptance criteria, checks and actual results, documentation/configuration/deployment effects, architecture deviations, known limitations, and recommended next action.

Opening a Pull Request does not authorize merging it. Merge only after the required review and approval. Preserve the requested history strategy; do not silently squash or rebase work that requires a merge commit.

## 7. Merge and close out

After approval, merge to `main` using the authorized method and verify the resulting branch state. Then update project truth only where the merged work actually changes it. Examples include the official record, decision log, memory ledger, interface registry, evidence index, or milestone closeout.

Do not promote a gate, status, measurement, or candidate specification merely because code merged. Close historical branches, delete branches, or change repository settings only under an explicit housekeeping task.

## Handoff checklist

Every coding-task handoff should identify:

- inspected authority, specifications, interfaces, ledgers, and relevant code;
- changed paths and their responsibilities;
- register/clobber, memory, MAP/base-page, DMA, timing, and IRQ/NMI impact;
- generated-artifact status;
- exact validation commands and results;
- evidence identity and evidence tiers not run;
- architecture or contract deviations, or explicitly none; and
- unresolved risks and the recommended next action.
