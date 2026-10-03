# R0-F Group 1 post-storage resume recovery — 2026-10-02

Owner authorized local implementation with "Build it" after the integrated
[P05 closeout](R0-F_GROUP1_CLOSEOUT.md). This is the bounded carry-forward
correction, under the original Group 1 Build Intent. Physical P05 causality
and resumed-workload acceptance remain open. P05 stays retired.

## Source and correction

Baseline main is `c27d89787d1d5c4472e24262e0181c47943d46be`, verified against
GitHub with passing static CI before editing. Work is on
`codex/r0f-group1-resume-clock`. The immutable P05 version-7 snapshot is the
input; the earlier root target source is not replaced. The reproducible
change is [the exact-source patch](../../tools/diagnostics/r0f_group1_resume_clock.patch),
applied by [the recovery controller](../../tools/diagnostics/r0f_group1_resume_recovery.py).

Only the copied `src/diagnostics/r0f/successor_integration.c` changes:

- Restart the existing CIA clock before display-resume DMA reads timestamps.
- Every display rejection records a cause. State rejection records 93; copy,
  DMA and clock failures retain their existing inner code through lockout.
- Keep raster-line selection after display configuration and audio restart
  after clock/display preparation.

The second changed candidate is 37505 bytes, SHA-256
`9654d336deefe8dae0bd3b26986e00fbea45b8f3dcd8cfe0b1c73ac3f479ef7e`.
Resident end exclusive is `$BFF1`, with 15 bytes free. Protected placement,
public/generated interfaces and capacities are unchanged.

## Contract and IRQ review

Inspected AGENTS, current state/WIP, development workflow, C/programming
standards, Group 1 Build Intent, measurement matrix, export amendment,
successor lifecycle/integration contracts and memory ledgers, D81 gate/workflow,
and frozen implementation/validation tooling.

Clock initialization writes the existing CIA1 `$DC04-$DC07` and `$DC0E/$DC0F`
registers and starts the existing raster IRQ path. At its new call site,
KERNAL/application context, CPU port `$35`, B=2 and canonical MAP/vectors have
been restored; the one-use context is invalidated and ROM reclaim complete.
The handler preserves A/X/Y/Z/B and interrupted P, has no C/display/audio/DMA
calls, and accesses only its existing resident state. Acquisition epoch is
zero across the boundary, so these early IRQs add no cohort timing samples.
The resumed IRQ-count baseline is still captured after storage_transition
returns. The handler and NMI policy are unchanged.

Display fetch stays suspended during all 15 synchronous 4096-byte clears.
Existing staging, ROM/display stores and DMA list are reused; no CPU-visible
or physical allocation is added. MAP/base-page behavior is unchanged. C
clobbers remain compiler-managed. Restart precedes resumed tick 1601 and
does not advance model time. No deadline, cadence, capacity, reserve or
acceptance threshold changes.

The generated target disassembly confirms the resumed clock call at `$4F7B`,
after reclaim, before staging at `$4FB5` and application DMA at `$4FE5`.
Raster selection remains after display configuration. The existing clock
initializer programs the timers before its IRQ-start call at `$9267`.

## Bounded experiments and validation

The initial bound was 30 minutes/two targeted experiments. Two target variants
were compiled. The first moved the clock and used a fallback expression;
it exceeded resident space by 3 bytes and was never executed. The second
records the state fault at its rejecting branch and directly propagates the
cause; it fits, saving 12 bytes relative to P05. No further target variant
is part of this task.

An earlier malformed patch caused an unchanged baseline compile during setup.
Its logs and output remain in `clock-01`; it is not changed-build evidence.
Preparation now gates build execution. `clock-02` retains the non-fitting
first experiment, and `clock-03` retains the qualified second experiment.

Fresh fit/static and native owner/scene/workload/audio checks pass, including
ASan/UBSan. The new native test extracts the actual post-restore suffix,
display preparation, clock initializer, coherent reader and DMA wrapper.
It models physical registers/copies explicitly: the old code masks a
stopped-at-FFFF CIA reader failure (3) as 93; the correction completes all
15 clears and retains injected state/copy/DMA/clock failures. Restoration,
NMI and IRQ-fault precedence checks pass. This demonstrates an ordering
hazard and correction under the model, not the unseen physical P05 subfault.
The first extraction attempt selected a forward declaration; its failed
compile is retained, and the definition-aware extraction passes.

`python3 -B -m unittest discover -s tools/diagnostics -p 'test_r0f_group1_*.py' -v`
passes all 47 tests. Generated outputs remain identical to the version-7
source inputs. No root target or generated interface is edited.

The first focused Xemu launch failed in the macOS sandbox before producing
a memory capture. That `G1RES01.D81` fixture and log are retained and not
reused. `clock-03-execution` is a byte-verified copy of the same qualified
source/build for a fresh launch outside the sandbox, using `G1RES02.D81`.
This changes the host execution environment, not the target experiment.

Focused NTSC and PAL both pass: 3200 records, 955/807 complete world pairs,
zero nominal deadline misses, zero uncertain boundaries and zero cohorts
below the existing 20 Hz floor. Each exports the complete 327680-byte allocation
in 20 chunks; independent version-7 reduction, capacity corruption checks,
actual returning SAVE and operator-summary checks pass. A fresh exact-PRG
filename-collision fixture preserves the existing bytes and displays
`S:5 E:03 F:00`; successful runs display `S:4 E:00 F:14` (hex file count).
The actual screenshots were inspected.

Fresh `R0FG1P06.D81` construction and independent structure/content gates pass.
Canonical size is 819200 bytes, SHA-256
`4f046112e8343c211ab5cc81caec2a85aa85e7d323e6c8a23019d513d4b592bf`.
The canonical image is read-only. Two NTSC and two PAL clean exact-name
autoload boots pass, each with 3200 records, actual SAVE, 20 exported chunks,
independent reduction, nominal timing, corruption/capacity checks and verified
operator screen. The carrier is `XEMU_BOOT_VERIFIED`, not SD-verified or
physically test-eligible. Its host path is
`build/r0f/group1/carriers/R0FG1P06/canonical/R0FG1P06.D81`.

During screen review, the indexed NTSC PNG appeared blank in one viewer
rendering. The sequence was paused and the already-started first PAL process
was sent SIGTERM. Independent PNG decoding established that the original
NTSC images are byte-identical and contain the complete expected text; a
pixel-preserving RGB inspection confirmed it. The initial failed visual
assessment is retained with its superseding review. No target/carrier fault
was established and no existing image was retested. The first PAL capture
already contained complete acquisition/export and passed all data gates;
its PNG is byte-identical to the directly reviewed focused PAL image.
The final required PAL copy is a separate clean boot.

Fresh preservation audit: all 7511 entries across the twelve prior campaign
freezes and all 333 physical-closeout entries match. Original baseline PRGs
and root/P02/P03 passing input sets match. No old evidence is rewritten.

## Commands and local identities

The following controller actions ran in order with `python3 -B
tools/diagnostics/r0f_group1_resume_recovery.py`: `prepare`, `build`, `host`,
`resume-host`, `qualify`, `ntsc`, `pal`, `negative-export`, `carrier-build`,
individual `carrier-boot` actions and `carrier-finish`. The retained records distinguish the
setup failures, rejected first variant and qualified second variant.

The qualified execution context is
`--experiment build/r0f/group1/resume-recovery/clock-03-execution`.
Focused boots use `--image-name G1RES02.D81`. Carrier actions use
`--name R0FG1P06.D81`; mode 1 is NTSC and mode 0 is PAL, each with fresh
copy numbers 1 and 2. These are historical commands, not instructions to
retest the existing images. Every output directory is exclusive.

The zero-context patch is independently replayed into a temporary copy of
the immutable baseline and produces exactly the qualified source bytes.
Its representation was normalized after compilation to avoid whitespace-only
patch context; this does not change source or PRG identity. Original preparation
records and the replay record retain both patch identities.

The initial two target experiments completed within eight minutes. Remaining
elapsed time is prescribed qualification of the second variant, with no
additional diagnostic target variants. Fifteen free resident bytes remain
a tight fit, not general expansion headroom.

## Remaining physical boundary

No SD access or physical execution is included. A later physical attempt
requires a fresh, independently verified SD identity and owner authorization.
The recorded physical P05 failure is unchanged; local checks cannot identify
its hidden subfault or grant Group 1/R0-F acceptance. Full R0-F, measured-limit
approval and Phase 1 retain their existing boundaries.

## Review handoff

Status: **READY FOR REVIEW — local correction qualified; physical proof open**.
Review [the evidence packet](../evidence/r0f/group1/2026-10-02-resume-recovery/README.md),
the source patch, recovery controller and native boundary validator/test.
WIP records this task; CURRENT_STATE remains the integrated checkpoint state.
The source change is confined to the new copied experiment. The root target,
generated contracts, historical evidence and unrelated untracked work are unchanged.

The packet preserves the qualified PRG, changed source, reports, extracted
actual data and screenshots. Raw D81s, disposable SD fixtures and verbatim
whitespace-bearing tool output remain in ignored build paths, with relevant
raw file identities recorded. No existing CI exception manifest is expanded.
Publication would need to choose and review any additional raw evidence to
track; no commit, push, PR or merge occurred here.

Recommended next action: review the local correction and evidence, then
separately authorize P06 SD/hardware delivery through the existing exact-copy
and one-extent gates if accepted. Physical first-fault identity and resumed
workload success must come from that new run. P05 must never be reused.
