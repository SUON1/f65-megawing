# Current Project State

This records durable integrated project state. It is not a design authority,
contract, acceptance record, historical journal, or task log. Active task
status belongs in [WORK_IN_PROGRESS.md](WORK_IN_PROGRESS.md). Completed work is
recorded here only when it changes enduring project reality.

## Current baseline

- Integrated branch: `main`.
- Target platform: MEGA65.
- Implementation model: LLVM-MOS C is primary target code; selective 45GS02 assembly serves justified platform-critical or measured low-level work; Java and Python are host tooling languages.

## Current specification baseline

**Integrated Phase 1 entry adoption:** [PR #17](https://github.com/SUON1/f65-megawing/pull/17)
merged on 20 October as `df1347b663c960e307870268f0b08ceaa6988d5c`.
The founder approved bounded Phase 0 program closeout, named obligation
reassignments and amendments A1–A6. Historical specifications and evidence remain
unchanged; full R0-F technical PASS and measured limits are not implied.
See the [decision](docs/decisions/PHASE1_ENTRY_ADOPTION_2026-10-20.md) and
[corpus manifest](spec/manifests/spec-corpus.json). The M1 visible foundation supplies a development-only non-flight executable;
see the [M1 correction handoff](docs/reports/M1_P2_CORRECTIONS.md).

1. Main Concept v1.8 - predecessor v1.7 plus approved A1–A3.
2. Gameplay v1.2 - predecessor v1.1 plus approved A4.
3. Runtime v1.2 candidate - predecessor v1.1 candidate plus A5; NOT FINAL.
4. Physics v4.1 - predecessor v4.0 plus approved A6.
5. Graphics v2.1.
6. Audio v1.0.
7. SensorAndTrack v1.0.
8. AI Behavior v1.1 - base v1.0 PDF plus narrow amendment.

Physics v3.3 and superseded standalone parent identities remain unchanged provenance. Incorporated Runtime/AI base PDFs remain required dependencies of their successors. Historical evidence retains original authority references. Original R1 drafts remain a dated review package, not current authority.

## Engineering state

R0-A and R0-B are closed bounded proof milestones; R0-D is closed for its
accepted calibration-proof scope. Under the retained Main Concept v1.6 program disposition,
R0-C is COMPLETE for the Revision 1.6 program baseline. Its retained historical
evidence remains truthful: the recorded owner disposition was a waiver rather
than a formal historical gate PASS, and no historical record is retroactively
relabeled. Remaining returning `StorageService` implementation is carried
forward and does not reopen Charlie. R0-E is closed only for its bounded
functional-proxy and raster-observation scope.

R0-F contains substantial bounded development and physical evidence. CF001 demonstrated a reset-only combined diagnostic with ROM backup/recovery, synthetic workload, IRQ/DMA/display/PCM/input activity, physical capture reduction, and retained SD integrity evidence. RH001 separately demonstrates a same-run ROM/storage lifecycle continuation in NTSC/PAL Xemu.

The original Group 1 development checkpoint is integrated through
[PR #10](https://github.com/SUON1/f65-megawing/pull/10). Its preserved P05 failure
and campaign history remain in the [original closeout](docs/reports/R0-F_GROUP1_CLOSEOUT.md).
The subsequent physical recovery and evidence are now integrated through
[PR #12](https://github.com/SUON1/f65-megawing/pull/12), merge
`7e4a3c81dc9122433c4ce36ba616bdfe4cc1b98b`, with evidence history preserved.

P09 resolves the bounded physical resume/export blocker: the actual returned
card supplies all 3200 records, both storage-separated epochs, the correct
returning SAVE and twenty trace chunks. Independent version-7 reduction
validates 955 world pairs, all five resumed services and integrity checks.
Nominal timing is WITHIN_OBSERVED_BOUNDS, with zero deadline misses, below-20-Hz
cohorts or uncertain boundaries. See the
[physical proof](docs/evidence/r0f/group1/2026-10-03-p09-physical/README.md).

The qualified source is the [frozen P09 snapshot](docs/evidence/r0f/group1/2026-10-03-audio-readback/README.md),
not the earlier root working target. P09 is preserved as a successfully tested
identity; P08/P07/P06/P05 and earlier failures remain unchanged. Do not repair,
rename, overwrite or rerun any tested carrier.

The Group 2 work package is integrated through
[PR #14](https://github.com/SUON1/f65-megawing/pull/14), merge
`23a38eb0984dbef487dc5641c9130de7ddf01f0f`, under the owner's approved
[bounded closeout](docs/reports/R0-F_GROUP2_CLOSEOUT_REVIEW.md). Retained results
include actual event-owner queue host proof, located historical snapshot proof,
private resident-size experiments and L3 physical export-collision/returned-card
preservation and SAVE checks. Each retains its stated tier and limitations.

The broader six-case suite is not marked PASS. Missing combined-load/tier proof,
audio continuation, live capture fit/schema/reducer and L3 operator/configuration
gaps retain their historical evidence limitations. Their new owner-gate
destinations were approved in the 20 October entry decision.
The historical Group 2 allocation was not recovered; its grouping was approved
prospectively. Group 3 is not defined or assigned by this closeout. Missing
successor proof is not marked PASS; the approved row-specific reassignment
changes when and where its obligations must be closed.

Full Group 1/R0-F technical acceptance and measured limits remain unapproved.
The 20 October founder decision closes the bounded Phase 0 work program and
assigns remaining obligations to their named implementation/acceptance gates;
it does not mark missing proof PASS. Phase 1 M1 implementation followed verification of integrated adoption.
The development-only foundation includes generated contracts, ordered runtime,
semantic input, immutable snapshots and complete sky/ground rendering. Host,
target-build and PAL/NTSC direct-PRG Xemu checks pass; physical acceptance,
flight behavior and full-harness acceptance remain outside this increment.

## What currently exists in code

- R0 proof programs and diagnostics under `src/r0a/`, `src/r0b/`, `src/r0c/`, `src/r0d/`, `src/r0e/`, and `src/r0f/`.
- R0 diagnostic models and narrow platform wrappers under `src/diagnostics/` and `src/platform/`.
- Generated interfaces and machine-readable contracts under `interfaces/`; ownership ledgers under `memory/`.
- Java/Python host tooling, builders, validators, and oracles under `tools/`.
- Retained evidence, handoffs, decisions, and plans under `docs/`.
- Placeholder or future production-module areas, not a completed 65Aero engine.

## Durable technical sequence

M1 visible-foundation implementation and its three P2 corrections are complete.
M2 PR1 implements the approved bounded runway/camera geometry, independent
oracle and registration contracts, including the near/far clipping correction.
Host/oracle and target compile/link checks pass; generated development identity
is `65AERO-M2-PR1-2`. See the [correction handoff](docs/reports/M2_PR1_CLIPPING_P2.md)
for exact evidence and memory accounting. The bounded PR2 size-reduction increment adds a private streaming raster cursor
and a size-focused integrated probe. Its provisional resident extent is `$7E85`
(379 bytes below `$8000`); precision and memory limits are unchanged. See the
[size-reduction handoff](docs/reports/M2_PR2_SIZE_REDUCTION.md). The founder
approved this increment only, not complete PR2 runtime/display admission.
The subsequent bounded prepared-context/overrun increment preserves the public
geometry API and adds private captured camera/transform reuse. Its initial
`$8014` failed gate is retained; removing the redundant registration temporary
restores the regression probe to `$7FDC`, 36 bytes below `$8000`, with precision
and memory ceilings unchanged. The founder approved this bounded correction
and publication. See the [overrun correction](docs/reports/M2_PR2_FIT_OVERRUN_FIX.md).
The founder subsequently approved the bounded Q46 limb experiment and corrected
report for publication. The private arithmetic helper and rotation call-site are
integrated separately from the unmerged full renderer/cache development work.
The retained experiment saves 101 resident bytes in that failed composition,
which still exceeds its unchanged resident ceiling by 11,718 bytes. See the
[publication scope](docs/reports/M2_PR2_Q46_PUBLICATION.md) and
[exact experiment](docs/reports/M2_PR2_Q46_LIMB16_EXPERIMENT.md).
The founder also approved the bounded transform-sequence experiment for
publication. Its exact matrix-building function is integrated independently of
the unmerged renderer/cache work. In the retained complete-development
composition it saves another 2,072 resident bytes, leaving a 9,646-byte deficit
under the unchanged memory limit. See the
[transform publication scope](docs/reports/M2_PR2_TRANSFORM_PUBLICATION.md) and
[experiment evidence](docs/reports/M2_PR2_TRANSFORM_SEQUENCE_EXPERIMENT.md).
The founder also approved the bounded prepared-projection correction for
publication. Its exact projection function is integrated independently of the
unmerged renderer/cache/dispatch scaffolding. The retained failed projection
experiment and corrected artifact remain unchanged: the correction saves 72
resident bytes against the 34,221-byte reference, leaving a 9,574-byte deficit.
See the [projection publication scope](docs/reports/M2_PR2_PROJECTION_PUBLICATION.md)
and [correction evidence](docs/reports/M2_PR2_PROJECTION_FORWARD_GUARD.md).
The founder also approved the bounded interpolation bit-consumption result and
the required BIT/CLV host-verifier coverage correction for publication. The
private interpolation helper and focused regressions are integrated separately
from the unmerged renderer/cache/dispatch scaffold. The retained composition
saves 385 resident bytes, leaving a 9,189-byte deficit under the unchanged
ceiling. Projection-closure stack bounds pass at 24 hardware / 8 dynamic software
bytes; whole-program proof remains unsupported at CLD. See the
[interpolation publication scope](docs/reports/M2_PR2_INTERPOLATION_PUBLICATION.md)
and [exact relink evidence](docs/reports/M2_PR2_INTERPOLATION_RELINK_RESULT.md).
The founder separately accepted the P2 guard-test evidence-isolation correction
for its reported host-test scope. Main records its exact patch and sealed host
evidence only; the minimum-renderer implementation and its prerequisites remain
outside the active main tree. The preserved development candidate's startup,
stack, service and diagnostic PAL/NTSC results retain their limited evidence
meaning; its 2,175-byte resident deficit remains unresolved. See the
[publication scope and next blocker](docs/reports/M2_GUARD_EVIDENCE_PUBLICATION.md).


The founder approved RF-D1, RF-D2, RF-D3 and RF-EX1 for the versioned M2
controlled-development design. The [residency contract](docs/plans/65AERO_M2_RESIDENCY_FEASIBILITY.md)
records the exact development-only code-bank exception, gateway verification
on every call and reset-only loading/retirement requirements. No permanent
production map, public ABI, protected-reserve use or active bank allocation is
introduced. Actual fit, stack, gateway and service performance remain UNPROVEN.
The source-complete minimum-renderer baseline and subsequent banked prototype
are separate reviewable increments; the old incomplete adoption packet is not
a prerequisite and is not claimed recovered or adopted.

Full-renderer fit, integrated stack/timing and high-resolution output mapping
remain open; no M2 target execution is claimed. Carry remaining obligations to the exact
owner gates approved in the entry plan. Establish actual measured limits and
full integrated-harness acceptance at their gates; bounded program closeout
does not relabel historical evidence or approve production capacity.

The founder approved the new `65AERO-M2-MIN-REBUILD-1` source baseline and
its startup, telemetry provenance and SDK identity/path corrections for
publication. This is a new reproducible development baseline, not recovered
historical source. See the [correction handoff](docs/reports/M2_MINIMUM_REBUILD_CORRECTIONS.md).
The retained complete target link uses 32,839 resident bytes against 24,575,
a failed fit by 8,264 bytes, with zero reserve use. Runtime startup, whole-program
stack and service remain UNPROVEN; launch and service grants stay zero.
The source baseline includes no banking or Xemu admission. Historical failures
and incomplete recovery limitations remain preserved.

## Project-truth debt

- The `spec/` corpus now distinguishes current authority, candidate Runtime v1, provenance, supporting references, and project-control records.
- Physics v4 supersedes v3.3 as current detailed authority. The original v3.3 artifact is retained without repair or re-rendering as provenance.
- Broader technical-document consolidation is deferred until after repository reorganization and the new development system are complete.
- `F65_OFFICIAL_RECORD.md` retains configuration and R0 history; `CODEX_PROGRESS.md` retains the historical development journal. Neither is the routine live project-status interface.
- The current GitHub repository visibility is public. The historical bootstrap entry in `F65_OFFICIAL_RECORD.md` retains the earlier private-repository state as provenance; any later visibility change requires deliberate Git/project-control housekeeping.
