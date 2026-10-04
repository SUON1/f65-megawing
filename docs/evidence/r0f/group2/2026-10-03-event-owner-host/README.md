# Group 2 first slice: event-owner host proof

Status: **PASS at host tier; READY FOR REVIEW**, 2026-10-03.
Owner approved the revised first slice, then “Built it” authorized implementation.
The [Build Intent](../../../../plans/R0-F_GROUP2_BUILD_INTENT.md) governs;
Main Concept §15.2 requires observable deterministic rejection without unrelated
mutation. This does not recover the historical Group 2 allocation or define Group 3.

Command, from repository root:

```sh
python3 -B tools/diagnostics/r0f_group2_event_owner_host.py
```

[Validation](validation.json) records exact compiler/link/run commands, compiler
identity, source/test/runner hashes, executable hash and unchanged-input result.
[Output](run.txt): 71 accepted and 17 rejected calls; ASan/UBSan and strict
`-Wall -Wextra -Werror` compilation pass. The frozen P09 `combined_model.c`,
model header and generated combined contract header are compiled directly,
without `R0FG1_INTEGRATION`. The tested event function has no integration-macro
branch. Existing passing Group 1 suites were not rerun.

The focused test checks generated-capacity fill and queue order; first valid
one-over and repeated rejection across nine legal IDs; invalid IDs 9/255 at
empty and partially occupied queues; the rejection flag; all other model bytes
and a separate peer; and reset followed by successful enqueue. Fully initialized
objects and byte copies preserve padding for whole-object comparisons.
This is actual owner behavior, not observer or manifest-validation evidence.

Changes: the new C test and Python runner under `tools/diagnostics/`, the Build
Intent, compact WIP and this new packet. The runner creates a fresh output
folder per run and rejects mismatched frozen source/header identities. Native
binary remains in the ignored output folder identified in validation.json.
Source commit describes the base; input hashes identify uncommitted test code.

No target source, generated artifact, capacity, threshold, reserve or memory
ledger changed. Target registers/clobbers, CPU-visible/physical memory,
MAP/base-page, DMA, timing and IRQ/NMI effects are non-applicable. No target
build, Xemu, carrier, SD or physical execution occurred. P09 and historical
source/evidence remain untouched; 11 resident bytes are not expansion headroom.

This closes only the named host assertions. It does not prove integrated
pressure, timing, physical fault behavior or full Group 2/R0-F acceptance.
Review this slice next. Further case allocation, audio-policy investigation,
owner changes, target work, publication and acceptance remain separate.
