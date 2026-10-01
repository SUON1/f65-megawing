# Group 1 isolated presentation policy checkpoint - 2026-09-30

Historical isolated checkpoint. Subsequent integration, fit, fresh timing and
local carrier work are recorded in
[the presentation integration report](R0-F_GROUP1_PRESENTATION_INTEGRATION.md).
The original evidence freeze and its program/input hashes remain unchanged.

The hardware-independent presentation kernel passes host sanitizers, an
independent boundary corpus and pinned LLVM-MOS target-object compilation.
It is not linked into the acquisition: the passing six-order PRG remains
`c249f4e4da972cdc0c5d0958a1a3a148387eb1ad4de602404c6b79fb7c79492b`,
with its complete NTSC/PAL evidence preserved. Group 1 is not hardware-ready.

## Authority and scope

The approved [Build Intent](../plans/R0-F_GROUP1_BUILD_INTENT.md) and
[measurement matrix](../plans/R0-F_GROUP1_MEASUREMENT_MATRIX.md), Main Concept
v1.6 sections 10/17, Graphics v2.1 sections 2.6/3.1/6.4/7 and candidate Runtime
v1 sections 8/14 govern. Graphics specifies atomic complete-world/registration/
view composition, presentation-only occlusion, bounded priority anchors and
stable per-attempt LOD. It does not freeze production thresholds or capacities.

This checkpoint adds only a private policy fixture, not a second renderer or
a production WorldRegistrationRecord. The [private configuration](../../interfaces/r0f_group1_presentation_contract.json)
owns the diagnostic capacities and thresholds; its generated header is not
hand-maintained. Native C structures are not serialized or public ABI layouts.

## Implemented and tested slice

- A generation binds source tick, view, tier, buffer identity and horizon once.
  Requests during unfinished work leave both the bound attempt and the old
  displayed registration unchanged. Only a complete matching pair can become
  ready; a superseded view cannot swap. Composition follows the complete pair.
- A four-entry diagnostic anchor pool ranks essential/selected cues before
  decorative cues, with stable handle tie-breaking. Overflow is counted;
  duplicate/invalid anchors and counter overflow reject. Exercised occupancy
  is tracked from actual insertion, not reported from capacity alone.
- A four-column diagnostic envelope carries the bound identity. Independent
  fragment enumeration checks front/behind, visible/clipped/hidden, ridge-zero,
  maximum-coordinate and missing/stale-envelope cases. This presentation-only
  fixture has no authoritative world-query or collision dependency.
- Two diagnostic size tiers use separate enter/exit thresholds and bind one
  chosen tier per attempt. Full 16-bit size input coverage and threshold
  oscillation checks establish size hysteresis; angle-bin behavior is deferred.
- Incomplete/mismatched publication, displayed-buffer reuse, non-forward
  generation, regressing source tick, invalid view/tier/buffer and counter
  overflow reject. Cancel retains the previous complete display.

## Validation and exact commands

```sh
python3 -B tools/diagnostics/r0f_group1_presentation_build.py
git diff --check
```

The build command compiles and executes the actual new C with ASan/UBSan,
`-Wall -Wextra -Wconversion -Werror`, runs four private-contract tests and
compiles with pinned `mos-mega65-clang -mcpu=mos45gs02 -Oz -fno-lto`.
All commands exit 0. The independent corpus includes 720 anchor permutations,
2592 enumerated occlusion cases, 131072 LOD comparisons, stale/unfinished view
and common-identity mutations, and overflow rejection. Host native state is
138 bytes; that is not a target-linked memory or stack measurement.

The build verifies the existing PRG and all 74 build inputs before and after
qualification. New outputs are separate under `build/r0f/group1/presentation-core/`;
no prior source, trace contract, PRG, retained evidence or carrier is rebuilt.
The [evidence freeze](../evidence/r0f/group1/2026-09-30-presentation-core/README.md)
retains exact source, generated parameters, host output, object and validation
identities. The qualification report records each compiler/test command.

## Contract/hardware impact and next action

The kernel has no hardware registers, new CPU-visible/physical allocation,
MAP/base-page operation, DMA, timer read, IRQ or NMI effect. C ABI clobbers are
compiler-managed. Caller-owned private state is bounded; target linked charge
and dynamic stack remain unmeasured. Deadlines and acquisition instrumentation
are unchanged because this kernel is not yet linked. A single-owner logical C
commit is not an instruction-atomic VIC-IV publication claim.

Next integrate and encode the bounded presentation observations with the
actual incremental display path, then independently reduce them. The current
resident envelope has only 616 bytes free: prove target fit without borrowing
any reserve, and repeat changed-build host/static/NTSC/PAL timing validation.
Complete the applicable geometry/audio/sensor pool observations, integrated
near-capacity trace, operator summary and exact-name boot gates afterward.
Directional angle-bin hysteresis, camera/projection and terrain/carrier visual
registration are not established by this small kernel. Whole-ISR cost, entry
latency and physical SI uncertainty remain open. No SD write, physical run,
commit, push, Group 1 acceptance or R0-F acceptance occurred.
