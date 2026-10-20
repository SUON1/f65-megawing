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
Any M2 work requires its own approved Build Intent. Carry remaining obligations to the exact
owner gates approved in the entry plan. Establish actual measured limits and
full integrated-harness acceptance at their gates; bounded program closeout
does not relabel historical evidence or approve production capacity.

## Project-truth debt

- The `spec/` corpus now distinguishes current authority, candidate Runtime v1, provenance, supporting references, and project-control records.
- Physics v4 supersedes v3.3 as current detailed authority. The original v3.3 artifact is retained without repair or re-rendering as provenance.
- Broader technical-document consolidation is deferred until after repository reorganization and the new development system are complete.
- `F65_OFFICIAL_RECORD.md` retains configuration and R0 history; `CODEX_PROGRESS.md` retains the historical development journal. Neither is the routine live project-status interface.
- The current GitHub repository visibility is public. The historical bootstrap entry in `F65_OFFICIAL_RECORD.md` retains the earlier private-repository state as provenance; any later visibility change requires deliberate Git/project-control housekeeping.
