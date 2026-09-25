# F-65 Development Workflow

## Purpose

F-65 development uses small, reviewable tasks with explicit authority,
validation, and founder acceptance. The workflow applies to human and
AI-assisted work. It does not change specification precedence, approve candidate
material, waive an engineering gate, or replace the governing design documents,
generated contracts, or evidence.

`CURRENT_STATE.md` records durable project reality. `WORK_IN_PROGRESS.md`
records the one active task. Historical R0 plans, reports, decisions, approvals,
and evidence remain authoritative for their stated scope but are not a general
task workflow.

## D81 construction and delivery

The root [D81 loadability gate](../00_D81_LOADABILITY_GATE.md) and
[reproducible D81 workflow](D81_WORKFLOW.md) govern every image change.
Fresh image construction, exact-name emulator proof, SD allocation and physical
chooser proof are separate requirements. Host copy/preallocation success must
never substitute for an independently measured single FAT32 extent. The new
direct allocator remains host-fixture-qualified until its first physical test;
document that limitation instead of promoting fixture results to hardware PASS.

## Normal lifecycle

```text
DISCUSS / DESIGN
        ↓
BUILD INTENT APPROVED
        ↓
VERIFY MAIN
        ↓
CREATE FOCUSED TASK BRANCH
        ↓
IMPLEMENT + UPDATE WIP
        ↓
VALIDATE AT REQUIRED EVIDENCE TIER
        ↓
READY FOR REVIEW
        ↓
FOUNDER REVIEW / ACCEPTANCE
        ↓
COMMIT + PUSH
        ↓
PULL REQUEST
        ↓
MERGE
        ↓
CLOSEOUT
```

Do not turn every lifecycle step into a formal status field. WIP uses only
`ACTIVE`, `BLOCKED`, `READY FOR REVIEW`, and `NONE`.

## 1. Build Intent

Before substantive work, establish an approved Build Intent. It identifies the
objective, why now, governing authority, scope and non-scope, owner/subsystem,
contract and hardware impact, required validation, founder-owned decisions, and
completion condition. Use [the Build Intent template](templates/BUILD_INTENT.md)
when useful.

The Build Intent may be in the approved task prompt, summarized or linked from
WIP, or retained as a dedicated task record when complexity warrants it. A
trivial typo or mechanical maintenance change does not require a permanent
Build Intent file when the approved task is already explicit.

Do not turn a draft, proposal, `TBD`, `TARGET`, `R0-GATED` value, or planning
assumption into shipping behavior. Stop and escalate material contradictions or
missing authority rather than choosing a convenient interpretation.

## 2. Verify the baseline and create a task branch

Normal new work starts from verified current `main`. Inspect the current
project-truth documents, repository instructions, applicable specifications,
interfaces, memory ledgers, implementation, evidence, and validation tooling
before editing. Record expected register/clobber, memory, MAP/base-page, DMA,
timing, and IRQ/NMI impact, including items that are not applicable.

Use one focused branch for one coherent task. Preferred naming is:

```text
codex/<area>-<short-description>
```

Examples:

```text
codex/runtime-command-queue
codex/physics-phase1-interface
codex/radar-track-schema
codex/audio-priority-runtime
codex/docs-runtime-freeze
```

Do not require numbered ticket identifiers. Keep unrelated cleanup, refactoring,
specification changes, and repository housekeeping out of the task.

## 3. Implement and maintain WIP

Make the smallest coherent change that satisfies the Build Intent. Preserve
generated-file ownership and use generated contracts instead of duplicating
layouts or constants. Do not change architecture, public ABI, memory ownership,
timing order, capacities, reserves, or another module's private state merely to
simplify implementation.

During substantive work, WIP identifies the current task and exact next action.
Update it when work becomes blocked or ready for review. Do not accumulate
completed-task history in WIP.

For C work, follow [`CODE_STYLE_C.md`](CODE_STYLE_C.md). Existing
evidence-bearing R0 code is not a style-migration target unless a task explicitly
authorizes that work.

## 4. Validate at the required evidence tier

Run the checks appropriate to the change and report exact commands and actual
results.

### Documentation/static

Examples include link, JSON/schema, whitespace/diff, and generated-consistency
checks.

### Host

Examples include host tests, Java or Python oracles, sanitizers, and fixtures.

### Target

Examples include LLVM-MOS compile/link, map, symbol, listing, disassembly, and
static target-contract validation.

### Xemu

Emulator execution and deterministic artifact checks.

### Physical MEGA65

Hardware-sensitive behavior and physical artifact verification.

### Human acceptance

Founder-owned observations, approvals, handling, visual/audio decisions,
waivers, and gate acceptance.

Passing a lower evidence tier never implies a higher tier passed. If a required
tier is unavailable, report it as not run and do not claim it passed.
Documentation-only changes still receive link/path checks, whitespace checks,
and diff review.

## 5. Founder review, commit, and push

When implementation and validation are complete, set WIP to `READY FOR REVIEW`.
Present the focused diff, validation results, architecture or contract impact,
evidence identity, limitations, and unresolved risks to the founder. Founder
review owns product decisions, approvals, waivers, measured-limit acceptance,
and other decisions reserved by project authority.

Apply in-scope review corrections on the same task branch. Split materially
different work into another Build Intent and branch. After founder acceptance,
confirm the diff contains only intended files, commit one coherent change, and
push the branch unless the approved task explicitly requires another checkpoint
pattern. R0 evidence work may retain its specialized checkpoint process.

## 6. Pull Request and merge

Open a focused Pull Request against `main`. It should summarize the Build
Intent, changed scope, applicable authority, validation and evidence, known
limits, and required human decisions or acceptance.

Opening a Pull Request does not authorize merging it. Use the merge strategy
appropriate to the task: squash is acceptable for ordinary focused work whose
intermediate commits have no durable evidentiary value; preserve multi-commit
history or use a merge commit when engineering or evidence provenance materially
depends on those commits. Never rewrite evidence-bearing history merely for
cosmetic cleanliness.

## 7. Closeout and recovery

After merge, remove completed task state from WIP. Update `CURRENT_STATE.md`
only when merged work changes durable project reality. Update specification,
interface, memory, or evidence records only when the merged work actually
changes them. Do not manufacture a separate closeout artifact for every trivial
task.

When resuming interrupted work, inspect WIP, the current branch and `git
status`, the current diff and recent commits, and the governing Build Intent.
Continue from repository state rather than reconstructing progress from chat
memory; do not restart merely because the conversation changed.

## Handoff

Every useful handoff identifies changed paths, contract and hardware impact,
validation run, evidence tiers not run, unresolved risks, and the recommended
next action. State generated-artifact status and evidence identity when
applicable.
