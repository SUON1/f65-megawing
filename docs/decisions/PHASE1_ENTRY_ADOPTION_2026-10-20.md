# Bounded Phase 0 closeout and Phase 1 entry adoption

20 October 2026. **FOUNDER APPROVED; local adoption prepared, not integrated.**

## Exact authority

The founder approved:

> Approve bounded Phase 0 program closeout and the named obligation reassignments in the entry plan. Approve amendments A1–A6 and authorize their versioned adoption. After adoption is integrated into verified main, authorize the M1 Build Intent, including direct-PRG PAL/NTSC Xemu validation, stopping at READY FOR REVIEW. Preserve all historical evidence and unrelated local paths. No D81, SD or physical testing is authorized.

The [entry plan](../plans/65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md)
contains the approved row definitions, evidence limitations, A1–A6 wording and
M1 Build Intent. Approval closes the Phase 0 work program for the limited
development profile. It does not declare full R0-E/F technical PASS, approve
measured limits, finalize Runtime or grant aircraft/demo acceptance.

## Approved obligation destinations

All evidence tiers, failure behavior and limitations in the plan's matrix remain
part of each assignment:

| Plan row | Approved destination |
| --- | --- |
| Q / G2-Q | CoreRuntime M1 queue rejection/preservation; M6 combined physical pressure; storage crossing when enabled |
| S / G2-S | M1 immutable ownership/starvation, M2 Xemu visibility, M6 physical combined load |
| P / G2-P | M2 ranking/supersession, M6 enabled-load shedding; full production pressure at Graphics acceptance |
| D / G2-D | M1 safe publication, M2 safe Xemu failure cases, M6 physical failure evidence |
| A / G2-A | AudioEngine before first audio enablement and before M6 if enabled; fault 21/22 caller reachability/lockout remains required |
| L / G2-L | StorageService before a feature depends on returning storage; refusal/restoration/lockout and physical evidence remain required |
| C / I / T / V | Instrument calibration, IRQ/input, phase/window and world-age/cadence from M1; close applicable evidence and approved limits before M6 acceptance |
| M | Actual owner/code/stack/reserve accounting each increment; block non-fitting slices; M6 exercised physical high-water and full ledger at integrated-harness gate |
| R | Full integrated-harness and later enabled subsystem combined-load acceptance |
| E | Retain bounded P09/L3 provenance limitations without inventing missing facts or replaying historical carriers; new configuration evidence at the new implementation's gates |
| G | Entry-contract change approved by this decision and A1–A6; M1 still waits for integration into verified main |
| H | Pre-entry tool availability check completed; M1 records its pinned JDK selection and generated development seam |

No unnamed obligation is waived. Reassignment does not mean the required test
passed. P09 nominal audio restart is not G2-A fault continuation. No new Group 3
or replay of the failed live-capture draft is assigned.

## Versioned adoption

The exact [manifest](../../spec/manifests/spec-corpus.json) identifies:

- [Main v1.8](../../spec/core/F65_Main_Concept_v1.8_APPROVED_AMENDMENT.md): unchanged Main v1.7 plus A1–A3.
- [Gameplay v1.2](../../spec/core/F65_Gameplay_v1.2_APPROVED_AMENDMENT.md): unchanged Gameplay v1.1 plus A4.
- [Runtime v1.2 candidate](../../spec/core/F65_Runtime_v1.2_APPROVED_CANDIDATE_AMENDMENT.md): unchanged v1.1/base-PDF composition plus A5/R7; NOT FINAL.
- [Physics v4.1](../../spec/subsystems/F65_Physics_v4.1_APPROVED_AMENDMENT.md): unchanged Physics v4.0 mechanics plus A6 sequencing.

These are controlled amendments, not lossy transcriptions. Predecessor bytes,
PDF reading copies, evidence and original approval records remain unchanged.
The Physics v4.0 reading PDF covers the incorporated base only; it does not
render the new sequencing amendment. No replacement PDF is generated.
Current-parent references resolve through the coordinated successor family;
historical references remain historical. Other subsystem identities are unchanged.

## Execution and publication boundary

Prepared on `codex/r0-phase1-entry-closeout`, baseline
`44f6c46bfb76a050f88bc343a354220cbf5782ea`. Fresh fetch and live GitHub main
verification on 20 October matched that baseline. Continue the existing planning
branch; do not discard its reviewed work or unrelated untracked paths.

M1 is authorized conditionally, including direct-PRG PAL/NTSC Xemu validation
and a READY FOR REVIEW stop. The prerequisite is adoption integrated into
verified main. That condition is not yet satisfied. No repeat authorization
for that same M1 scope is needed once the condition is satisfied.

Commit, push, PR and merge have not been authorized by this decision. Complete
the local adoption and its static checks, then stop at READY FOR REVIEW.
No D81, SD or physical testing is authorized. Later M2–M6 implementation,
aircraft-data/envelope decisions, measured-limit approval and qualified handling
acceptance remain separate.

## Impact and validation

Document identity and phase-entry/sequencing rules change. Registers/clobbers,
CPU-visible/physical memory, MAP/base-page, DMA, timing/deadlines, IRQ/NMI,
generated binary interfaces, capacities and protected reserve: not applicable /
unchanged. No source or target implementation is changed.

Validation: `python3 /tmp/f65_validate_entry_adoption.py` passed all 24
predecessor corpus hashes, all 28 present manifest hashes and dependency graphs,
verbatim A1–A6 comparison, 64 local links and tracked/new-file whitespace.
`python3 -B tools/diagnostics/r0a_validate.py .` passed corpus/configuration
validation. Final diff scope is five tracked files and six new Markdown files
(including the existing task plan); the 20 unrelated untracked status entries
remain. Previous planning compiler/oracle preflight is dated evidence, not a
rerun in this adoption. No execution-tier tests or hosted CI were run.

## Subsequent publication and continuation authorization

The founder subsequently instructed: “Commit and push the adoption, open a PR,
and merge after checks pass. Preserve all unrelated paths. Then verify main and
start the authorized M1 Build Intent, stopping at READY FOR REVIEW.”
This supersedes the earlier publication hold for this adoption only. Merge is
conditional on passing checks; M1 still starts only after verified integration.
D81, SD and physical testing remain prohibited.
