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

**Approved successor adoption pending integration:** on 20 October the founder
approved bounded Phase 0 program closeout, named obligation reassignments and
A1–A6. The local manifest identifies Main v1.8, Gameplay v1.2, Runtime v1.2
candidate and Physics v4.1, each composed from its unchanged predecessor plus
the approved amendment. See the [decision](docs/decisions/PHASE1_ENTRY_ADOPTION_2026-10-20.md).
M1 is authorized after adoption is integrated into verified main; implementation
has not started. The integrated baseline below remains the 4 October family
until merge; WIP tracks the local adoption.

Founder directed coordinated Physics v4 adoption on 4 October 2026. The current specification set contains that adoption. See [adoption authority](docs/decisions/PHYSICS_V4_ADOPTION_2026-10-04.md) and the exact [corpus manifest](spec/manifests/spec-corpus.json).

1. Main Concept v1.7 - master product and architecture authority.
2. Gameplay v1.1 - player-facing authority.
3. Runtime v1.1 approved candidate amendment - NOT FINAL; base v1 PDF plus amendment, pending independent freeze closure.
4. Physics v4.0 - current detailed physical model and aircraft-data engineering baseline.
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
it does not mark missing proof PASS. Phase 1 M1 entry is authorized conditionally
on adoption integrated into verified main. Formal Phase 1 implementation has
not started.

## What currently exists in code

- R0 proof programs and diagnostics under `src/r0a/`, `src/r0b/`, `src/r0c/`, `src/r0d/`, `src/r0e/`, and `src/r0f/`.
- R0 diagnostic models and narrow platform wrappers under `src/diagnostics/` and `src/platform/`.
- Generated interfaces and machine-readable contracts under `interfaces/`; ownership ledgers under `memory/`.
- Java/Python host tooling, builders, validators, and oracles under `tools/`.
- Retained evidence, handoffs, decisions, and plans under `docs/`.
- Placeholder or future production-module areas, not a completed 65Aero engine.

## Durable technical sequence

Integrate and verify the approved entry adoption, then execute the authorized
M1 visible-foundation Build Intent. Carry remaining obligations to the exact
owner gates approved in the entry plan. Establish actual measured limits and
full integrated-harness acceptance at their gates; bounded program closeout
does not relabel historical evidence or approve production capacity.

## Project-truth debt

- The `spec/` corpus now distinguishes current authority, candidate Runtime v1, provenance, supporting references, and project-control records.
- Physics v4 supersedes v3.3 as current detailed authority. The original v3.3 artifact is retained without repair or re-rendering as provenance.
- Broader technical-document consolidation is deferred until after repository reorganization and the new development system are complete.
- `F65_OFFICIAL_RECORD.md` retains configuration and R0 history; `CODEX_PROGRESS.md` retains the historical development journal. Neither is the routine live project-status interface.
- The current GitHub repository visibility is public. The historical bootstrap entry in `F65_OFFICIAL_RECORD.md` retains the earlier private-repository state as provenance; any later visibility change requires deliberate Git/project-control housekeeping.
