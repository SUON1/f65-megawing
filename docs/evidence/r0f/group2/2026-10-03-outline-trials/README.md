# Group 2 outlining trials — no space recovered

Owner “Build it” approved the two bounded compile-only experiments proposed in
[the target admission](../2026-10-03-target-admission/README.md).
Both were run separately against fresh copies of that exact retained admission.
Only the named function's `noinline` attribute changes in each source tree.
Bodies, integrity checks, capacities, reserve policy and linker regions remain.

Commands from repository root:

```sh
python3 -B tools/diagnostics/r0f_group2_outline_trial.py frame-wait
python3 -B tools/diagnostics/r0f_group2_outline_trial.py ratio
```

| Trial | Resident end | Over $C000 | Recovery against admission |
| --- | --- | --- | --- |
| Retained minimal queue admission | $C16F | 367 bytes | — |
| `cfframe_wait` noinline | $C16F | 367 bytes | 0 bytes |
| `cfratio` noinline | $C366 | 870 bytes | -503 bytes |

Both target compiler commands exited 0. Both controllers exited 1. The first
records FIT_FAIL; the second rejects changed `.noinit` before populating its
fit fields. The unmodified raw second report is retained. Independent parsing
of its retained linker map supplies the size figures in [summary.json](summary.json):
500 bytes additional text and 3 bytes additional compiler static stack
(`.noinit..Lstatic_stack`, 36 -> 39). This is not growth in application pools.
Protected content remains 4495 bytes in both trials. No trial is executable.

The first trial's size and disassembly logs are retained. The second stopped
at its state-allocation guard, so no size/disassembly command was run for it;
its map and compiler output remain available. Trial reports bind every copied
input and verify the retained admission source stayed unchanged. The runner,
source deltas, reports, maps and logs are hashed in `sha256.json`. Full copied
sources and binaries remain at the paths recorded in the summary.

No new host equivalence suite was run: neither structural candidate passed
admission, and function bodies were verified byte-identical after removing the
single attribute. Earlier host PASS remains its own evidence, not qualification
of new target timing or calling conventions. No target program, Xemu, D81,
SD or physical run occurred. P09 and historical evidence are unchanged.

## Disposition

Reject both outlining remedies; the authorized two-trial budget is exhausted.
Do not stack these attributes or try more compiler switches without a reviewed
new remedy. Group 2 remains blocked even at its minimal admission, before the
remaining fault cases and capture code are included. No commit or push.

The next useful work is a source/disassembly size-attribution design for shared
cold calibration/setup code and a concrete combined-suite capture/fit budget.
This must identify removable duplication while retaining every required check
and workload; no savings are established by this report. A resulting bounded
implementation remedy needs review under the Build Intent. Do not substitute
a standalone hardware test, borrow reserves, widen the resident envelope or
invent overlays to avoid the combined-load requirement.

Hardware effects of the trials: ordinary compiler-managed C call/stack changes
only; no new register access, MAP/base-page operation, physical allocation,
DMA or IRQ/NMI policy. Dynamic stack and timing were not executed or qualified.
No generated/public contract or acceptance threshold changed.
