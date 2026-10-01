# R0-F Group 1: combined workload, timing and storage resume

Owner approved the three-group campaign, then Group 1 preparation and "Build
it" on 2026-09-29. Local implementation and host/target/exact-carrier Xemu
validation are authorized. SD delivery, physical execution, publication and
full R0-F acceptance are not authorized by this build.

## Baseline and preservation

Continue `codex/r0f-successor-physical-exact-carrier` at
`9e2ffdb4786e4794119933a5edd4b1cf79f653f0`. Freshly fetched `origin/main` is
`ae2b397698cc7197d03349e57cd058b4fb9f3987`, an ancestor. Preserve all dirty
T09/T10/T11 work and retained CAP14, IRQ11 and failed-carrier evidence.
Prebuild dirty-file hashes and non-evidence file copies are retained locally
at `/private/tmp/f65-group1-prebuild-20260929/`; this is a recovery aid, not
the eventual source/evidence freeze.

## Approved coverage

One integrated normal-workload suite covers platform/reference identity,
calibration/overhead, representative combined workload, tick/stage/service
timing, phase alignment, rolling windows, IRQ/DMA interference, snapshot and
world-generation coherence, complete-world cadence/age, and exercised dynamic
high-water. It includes the first resumed tick and repeated relevant coverage
after the returning-storage transition. Groups 2 and 3 remain separate.

Main Concept v1.6 sections 4 and 17, Gameplay v1, candidate Runtime v1
sections 7-8 and 19, and the current successor admission reconciliation govern.
The T02/T03 generated contracts and memory ledgers govern platform ownership.
The C standard, development workflow and root D81 gate/workflow apply.

100 Hz and 21-stage order are invariants. The historical 530,000 clocks is
not a tick budget. World 25/30 Hz values are targets; the sustained 20 Hz
floor remains a requirement, with observation-window semantics documented
before evaluation. No per-service latency allowance or maximum world age
is invented. Nominal clock conversion is not traceable SI calibration.

## Integration admission issue: terminal export

The campaign proposed a post-acquisition trace SAVE so the owner need only
capture a compact summary and return the card. Current
`interfaces/r0f_successor_contract.json` instead mandates destruction of the
only pre-C KERNAL context before `SERVICES_RESUMED`. The lifecycle has one
forward storage transition; a second storage call is not admitted.

Do not retain the context past its lifetime, call the old storage trampoline
after invalidation, or silently turn this into a repeated-storage contract.
The owner approved the narrow private terminal-export amendment with "Make
the corrections" on 2026-09-29. Its contract and qualification are recorded
in `R0-F_GROUP1_EXPORT_AMENDMENT.md`. The separate capability is now being
implemented and validated before workload integration.
The earlier "Ready" response did not identify this constraint and was premature.

## Completion gates

- Exact requirement-to-case matrix and workload accounting, including all
  deferred/unexercised items, without relabeling the old synthetic workload
  as complete current-parent coverage.
- Versioned private evidence format, bounded capture and independently checked
  release/deadline/window reduction; zero reserve borrowing.
- Calibrated read/capture overhead, timer coherence/wrap handling and explicit
  physical uncertainty. Host boundary and corruption tests must fail closed.
- Target map/symbol/disassembly and stack/physical-lifetime checks.
- Fresh exact-name D81 with structure/content extraction, two NTSC and two PAL
  clean Xemu boots and independent actual-result/export reduction.
- Physical tier explicitly NOT RUN; no carrier is released merely because
  host arithmetic or a subset of workload checks passes.

## Hardware impact of initial measurement core

The initial module is pure bounded integer arithmetic: no hardware registers,
physical allocation, MAP/base-page changes, DMA or IRQ/NMI effects. C ABI
clobbers are ordinary compiler-managed caller-saved state. Future integration
must account for timestamp reads, telemetry storage, instrument overhead and
all platform changes before target editing. Public ABI remains unchanged.

## Initial validation checkpoint

`python3 -B tools/diagnostics/r0f_group1_build.py` passes one million release
comparisons against an independent 64-bit closed form, ASan/UBSan boundary and
wrap tests, and pinned LLVM-MOS target-object compilation. The first object
compile rejected an inapplicable link-only `-mlto-zp=0` flag; removing it from
this compile-only invocation resolved the error. No target linker flags or
predecessor build changed. Report: `build/r0f/group1/timing-core-validation.json`.

Full workload integration and its carrier gates remain NOT RUN. The separate
development export probe has linked and passed its target static checks;
its qualification does not close any Group 1 workload requirement.
The pure module is not a hardware clock, complete calibration or a validated
scheduler replacement. It does not alter the existing successor tick loop.
