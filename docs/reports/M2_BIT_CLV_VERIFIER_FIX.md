# M2 BIT/CLV verifier coverage correction

**READY FOR REVIEW — approved bounded verifier work complete; no relink.**

The founder approved the BIT/CLV checker fix, required regressions and replay of
pinned artifacts in the current task prompt. This continues on
`codex/65aero-m2-interpolation-experiment`, HEAD
`c6a41e0988a3e329f1b30f7d48c87d92e00b523b`, in
`/private/tmp/f65-m2-interpolation-experiment`. It does not resume the unused
composed candidate relink or authorize target changes or publication.

## Problem and exact change

The interpolation probe compiled and linked but its required static stack
checker rejected `BIT $5ab0` at `$463c`. A second reachable instruction, `CLV`
at `$46e2`, was also absent from the checker. The compiler uses a read of the
SDK's `$FF` `__set_v` constant to set V and `CLV` to clear it before a shared
`BVS` path. Both instructions change flags, fall through and have zero hardware
or software stack effect.

The only functional verifier change adds `bit` and `clv` to the existing
ordinary-instruction set in
[stack_check.py](../../tools/flight_demo/m2/stack_check.py), with an explanatory
comment. It does not simulate flag values or prune branches. Conditional
successors, call/return traversal, join-depth consistency, unknown/indirect
transfer rejection, recursion/growth-loop rejection, software-pointer write
rules and the hardware/software envelope checks are unchanged.

[test_contract.py](../../tests/flight_demo/m2/test_contract.py) adds six test
methods. Its pre-existing local fixture helpers were lifted unchanged in
meaning to module scope and shared with the new fixtures; original assertions
remain. No target source, public/generated interface, oracle, numeric tolerance,
compiler flag or memory ledger was edited. No architecture deviation.

## Validation actually run

`python3 -B docs/evidence/flight-demo/2026-10-22-m2-bit-clv-verifier/run_checks.py`
completed with exit 0. Its exact subprocess argv, exit codes and logs are
retained in [commands.json](../evidence/flight-demo/2026-10-22-m2-bit-clv-verifier/commands.json).

1. `python3 -B -m unittest discover -s tests/flight_demo/m2 -p 'test_*.py' -v`
   — **11 tests PASS**, including the five existing tests and six new methods:
   - stack neutrality for absolute BIT and CLV, separately/together, plus
     immediate/indexed BIT and reads of logical `$2`/`$3`;
   - balanced BVS/BVC/BMI/BPL/BEQ/BNE diamonds and rejection of imbalance on
     either successor, even when CLV establishes a known V value;
   - unchanged nested call and software-frame accounting: 6 hardware bytes
     including entry return and 16 dynamic software bytes in the fixture;
   - unknown instructions, indirect transfers, recursion, unbalanced returns,
     stack underflow and unauthorized direct/indexed software-pointer writes
     still reject, with assertions on the specific failure reason;
   - stack-growth loops reject through either BVS/BVC branch;
   - hardware 255 bytes passes / 256 rejects, software 4,096 passes / 4,097
     rejects. No limit or reserve was enlarged.
2. `python3 -B docs/evidence/flight-demo/2026-10-22-m2-bit-clv-verifier/replay.py`
   — **PASS**, without invoking a compiler, linker, disassembler or target.
   Original checker and new checker were both applied to the exact retained
   text. The original checker reproduces the original interpolation failure.
   The new checker passes both pinned standalone probes.

| Pinned standalone artifact | Original checker | Corrected checker | HW bytes including entry return | Dynamic SW bytes | Checked call entries |
|---|---|---|---:|---:|---:|
| Corrected-projection predecessor | PASS | PASS, identical result | 20 | 0 | 12 |
| Interpolation candidate | FAIL: unrecognized `bit` | PASS | 20 | 0 | 11 |

The pinned predecessor disassembly SHA-256 is
`4e547d315061d7445edab574b471814f08dd3373e1fb67a08ecb0f0e3fd2b0b2`;
the interpolation disassembly SHA-256 is
`446b837320606cfbd21a9619ed0cedbddea64c6711b1dbd71269a5cca4bb6fef`.
The replay also pins the predecessor build record, verifies the exact approved
two-token checker delta and verifies all **57 raw output files** across the five
existing build directories, including binaries, corpora, maps and images.
Neither file sets nor bytes changed.

Original checker SHA-256:
`4d344f815d246859b621caac01f2c9e27f1501ecec32c7f9491d7f2e427522ef`.
Corrected checker SHA-256:
`5e4e20d3ff19697a7d55d3ae27c61260f3200172d4a9ba75bee84fa9810ac826`.
The [replay record](../evidence/flight-demo/2026-10-22-m2-bit-clv-verifier/replay.json)
and [regression log](../evidence/flight-demo/2026-10-22-m2-bit-clv-verifier/regressions.txt)
contain actual results, not a replacement historical build report.

## Contract, hardware and memory impact

This is host verifier/test work. Target CPU register/flag clobbers, hardware
register access, CPU-visible/physical allocation, MAP/base-page setup, DMA,
timing/deadline behavior and IRQ/NMI effects are **not applicable to this change**.
No target executable was produced or run. Graphics arithmetic, Q46/Q24/Q16
precision, ownership, cache generations/cancellation and dispatch guards remain
byte-identical to the state before this fix. Public/generated ABI is unchanged.
The ledger still reserves resident `$2001–$7FFF`, hardware stack `$0100–$01FF`,
software stack `$C000–$CFFF`, existing base-page/display bands and zero reserve.

The new 20/0 result is a static bound for the pinned direct-call standalone
probe only. It excludes IRQ/NMI, platform integration and executed high-water.
Compiler static scratch remains **487 resident bytes** for the interpolation
probe, separate from zero dynamic software stack. The predecessor has 497
resident scratch bytes. The retained resident spans remain 17,054 and 17,151
bytes respectively; this task changed **zero target bytes** and measured no
new size saving.

The composed candidate still has no link artifact. Its size, scratch, owners,
stack and timing remain unmeasured. The last verified composition remains
34,149 resident bytes with a **9,574-byte deficit**, ending at `$A566` against
the unchanged `$8000` ceiling. Neither the standalone replay nor this checker
change establishes full-renderer fit, whole-renderer stack safety, cycle WCET,
100 Hz margin or runtime/display admission. The historical standalone builder's
later static assertions were not rerun; its original failure report remains
truthful. No new full-builder PASS is claimed.

## Preservation and handoff

The previous interpolation report, packet, original failure, reference checker,
source snapshots and raw target identities remain intact. All **16 pre-existing
flight-evidence inventories** and four prior checkout snapshots verify exact.
The **20 unrelated entries** remain intact. All pre-existing paths in this
experiment retain their bytes except the explicitly approved checker, tests
and WIP. All 43 generated/interface and memory files match HEAD. Only a new
report and a new evidence packet were added for this task.

The [evidence packet](../evidence/flight-demo/2026-10-22-m2-bit-clv-verifier/README.md)
retains the before snapshot, original checker/tests/WIP, corrected source
snapshots, pinned replay program/results, exact command logs, preservation audit
and SHA-256 inventory. Its preservation audit also checks scope, local links,
JSON and whitespace. No archived inventory was amended.

Recommended next action: review this bounded verifier correction and its
static replay results. Any resumed composed relink, full-builder validation,
further size optimization, publication or target execution requires separate
authority. No Xemu, D81, SD or physical testing occurred. Stop READY FOR REVIEW.
