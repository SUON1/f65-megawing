# Codex Progress — F65 R0-D protected-workload calibration

## Original objective

Implement the bounded R0-D protected-workload and calibration proof defined by
the supplied human-reviewed F65 Main Concept v1.6. R0-D owns the reproducible
historical 530,000-clock non-render workload and instrumentation foundation
needed by R0-E and R0-F. The owner additionally clarified that this proof is
delivered in a D81 containing the PRG. The proof remains limited to the
admitted R0-D scope.

## Current status

- Current phase: R0-D; production stage: CODING (physical chooser correction).
- Authorization: the physical chooser failure returns the carrier internally
  to Stage 1. Existing Xemu authorization resumes only after the replacement
  has passed Stage 1 and Stage 2; no replacement physical attempt is authorized
  until its ordered gates have completed.
- Repository branch: `codex/r0-d-development`.
- Local / last remotely verified commit before this correction:
  `33ce4342a73a90c7dc1c199bf89c714ce8d072f3`.
- Remote verification: `git ls-remote` returned `33ce434` for
  `origin/codex/r0-d-development` before the physical result.
- Working tree was clean before preserving the returned physical failure and
  beginning this correction.
- D81: `F65R0D.D81`, SHA-256
  `a1d11bfb2b18a92618d55b5f3051a44d019adbdf2ba70b7c6715049567638d48`, is
  **INVALID — DO NOT USE** after physical chooser `ERROR CODE FF`. Its
  SD-copy hash was not captured, so the failed transferred byte identity is
  unknown. The replacement begins `UNVERIFIED` with a distinct filename.
- R0-C is complete by owner waiver of its remaining physical media-fault matrix.
  R0-D direct-PRG and failed-D81 Xemu evidence are preserved but are invalid
  for a replacement carrier. No physical R0-D program result exists.
- Current work: preserve the failure, correct the D81 header-profile host gate,
  and fresh-build a distinct carrier using the retained physical-accepted
  R0-A/R0-C profile. The label/ID difference is a compatibility hypothesis,
  not a proven root cause.

## Completed work

- Verified the required repository, branch, baseline commit, clean status,
  history, origin remote, and all required sentinel files.
- Read root `AGENTS.md`, the prior checkpoint, official record, D81 gate, R0-C
  handoff/plan/admission/ownership/evidence, toolchain lock, R0-C build path,
  interfaces, memory ledger, and public platform ABI registry.
- Recorded supplied current-document SHA-256 values:
  - Main Concept v1.6:
    `e7d8ed40ce630d82e707e2a9c7f29995fac6f4281849c2c7ef5261d420c2c425`
  - Gameplay and Simulation Supplement v1:
    `b675daa213c02e4b642fd8f8dd439c74f72808488c548a6af14fc8400487645a`
  - 65Aero Runtime and Technical Supplement v1 candidate:
    `bcb50a96ca6aadfd45637c48c4a80a10d8ce61b1e2461ba03448b4f06497d260`
- Created the R0-D admission, ownership map, ExecPlan, agent record, counter
  contract, memory ledger, test guide, evidence map, handoff, generated C/Java
  bindings, host fixture, static validators, build script, and target diagnostic.
- Implemented `R0D-PW-530K-001`: a deterministic 21-stage, 100 Hz historical
  comparison fixture with exactly 530,000 declared protected-work clocks. It is
  explicitly not a production timing budget or measured-limit selection.
- Built target observability at `$1860-$18DF`; the target touches no protected
  staging, audio, DMA-list, reserve, or measured-limits range.
- Committed the complete Stage-1 implementation as
  `2bcb54e046e9cdcd8f03b7daaa12141a474c6af0`
  (`feat(r0d): add protected workload calibration harness`).
- Verified the VS Code publication with `git ls-remote --heads origin
  refs/heads/codex/r0-d-development`, which returned
  `5c2ff556968281092eb972e6c31e4492d9bdffda`.
- Reverified the exact published `c5a12d9` branch/HEAD/clean state before Xemu
  admission. The pinned Xemu reports version `20260129235930` at source commit
  `40dfef0d1d5f56be2469492715c12bdb32c75b67`.

## Files changed

- R0-D source, documentation, generated bindings, validation scripts, and build
  tooling listed in `docs/plans/r0-d-ownership-map.json`: committed locally in
  `2bcb54e`, `62ffb16`, and `5c2ff55`; published through VS Code; no further
  Stage-1 source changes expected.
- `CODEX_PROGRESS.md`: durable R0-D checkpoint and published Xemu evidence
  record through `30549f`; this physical-preflight update is pending its local
  documentation commit; further updates are expected after owner evidence.
- `docs/testing/R0-D_TEST_GUIDE.md` and `docs/evidence/r0d/R0D-EVIDENCE-MAP.md`:
  source-owned Stage-4 procedure/evidence-state records, pending this physical
  preflight documentation commit; further edits expected after owner evidence.
- `src/r0d/autoboot.bas`, `tools/build/r0d.sh`, and
  `tools/diagnostics/r0d_d81_loadability_gate.py`: new R0-D-owned D81 carrier,
  one-session builder, and independent structural/content validator; committed
  in `13ebdf9`; the D1 candidate was freshly regenerated from that commit.
- `docs/evidence/r0d/physical/F65R0D-D81-CHOOSER-FF.jpg` and
  `docs/evidence/r0d/R0D-D81-FAILURE-2026-08-30.md`: retained physical failure
  evidence and its disposition; pending this correction commit.

## Decisions and architecture

- The explicit R0-D task prompt and supplied v1.6 documents control this task.
  The preserved R0-C record and older candidate corpus remain historical.
- R0-D will add separate proof-only contracts, generated bindings, ledgers,
  diagnostics, host evidence, target observability, and a fresh D81 path.
- No change is authorized to CoreRuntime ownership, 100 Hz/21-stage order,
  public production ABI, fixed capacities, MAP/base-page/stack rules,
  MemoryAccessABI, protected reserves, or R0-C sources/evidence.
- Existing relevant ranges are stack `$0100-$01ff`, base page `$0200-$02ff`,
  R0-C result `$1800-$185f`, display `$020000-$03ffff`, workspace
  `$048000-$04ffff`, staging `$050000-$052fff`, audio `$053000-$055fff`, DMA
  lists `$056000-$056fff`, reserve `$057000-$057fff`, and untouched measured
  limits reserve `$058000-$05ffff`. R0-D counters must not consume them.

## Validation performed

- Git root/branch/HEAD/status/diff/history/remote checks: PASS.
- Required sentinel checks: PASS.
- Baseline containment check: PASS for local R0-C/R0-D and
  `origin/codex/r0-c-development`.
- SHA-256 calculations for all three supplied current documents: PASS.
- `sh tools/build/r0d.sh bootstrap`: PASS; pinned LLVM-MOS 24.0.0git / MOS
  45GS02 target and Temurin 21.0.12 runtime available.
- `sh tools/build/r0d.sh host-test`: PASS; all R0-D host fixture/counter tests
  pass and emit `build/r0d/evidence/r0d-host-evidence.json`.
- `make r0d-verify`: PASS; generated binding freshness and static target guard
  pass.
- `make r0d-build`: PASS; LLVM-MOS links the target and emits map, symbols,
  disassembly, build-accounting report, and PRG SHA-256
  `ad4827da70d6f4a571817df2268bb3ca4e88d11a0f8aacfc11441abca2fd1677`.
- `git diff --check`: PASS.
- No R0-D D81 is required or emitted in Stage 1. D81 host validation is not
  applicable; no D81 is to be mounted for this PRG-based Xemu path.
- Xemu: PASS. The supplied 131,072-byte ROM matched SHA-256
  `af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0`.
  Two clean PRG boots produced matching screen and result-block hashes.

## Known problems or unresolved issues

- Implementation defects: the R0-D D81 host gate omitted validation of the
  physical-accepted disk header label/ID profile.
- Tooling: no active host-tooling defect. Python bytecode compilation cannot
  use the macOS cache in this sandbox, so source syntax was checked in-memory.
- Unverified behavior: physical R0-D timing/behavior and all hardware behavior.
- Authority discrepancy: repository status reflects predecessor candidates;
  supplied human authorization adopts v1.6 for R0-D.
- Missing evidence: a replacement D81, its host/Xemu evidence, SD-copy hash,
  physical chooser, physical display/result, and hardware environment evidence.
- Human decisions: R0-GATED/TARGET/TBD values remain unselected.
- Later gates: replacement Stage-1 build, Stage-2 publication, replacement
  Xemu evidence, SD-copy verification, and physical chooser/evidence review.

## Remaining work

- [x] Verify repository, baseline, sentinels, R0-C evidence, and inputs.
- [x] Read the D81 gate and record supplied-document hashes.
- [x] Establish the R0-D admission checkpoint.
- [x] Create R0-D task-admission, ExecPlan, ownership, agent, test, evidence,
  and handoff records.
- [x] Implement deterministic 530,000-clock workload and R0-D counters.
- [x] Implement host/static/build validation and target observability.
- [x] Complete diff review, commit, and report Stage-1 results.
- [x] Publish the Stage-1 branch through VS Code and verify its GitHub commit.
- [x] Publish the Xemu evidence commit through VS Code and verify it remotely.
- [x] Run two clean Xemu boots and capture deterministic evidence.
- [x] Receive owner clarification that R0-D requires a D81 carrier containing
  the PRG; read the D81 gate before any carrier action.
- [x] Add fresh one-session D81 builder, independent structural/content checks,
  and release manifest.
- [x] Build and host-verify the R0-D D81 candidate.
- [x] Commit the D81 implementation locally (`13ebdf9`).
- [x] Publish the D81 implementation and coding checkpoint through VS Code;
  remote `fa108a8` verified.
- [ ] Publish this push-verification checkpoint through VS Code.
- [x] Re-run two-clean-boot Xemu tests on the failed D81 identity.
- [x] Preserve physical chooser `ERROR CODE FF` evidence and invalidate the
  failed D81 identity.
- [ ] Correct the header-profile gate and fresh-build a distinct D81 carrier.
- [ ] Publish the replacement through VS Code, then re-run two-clean-boot Xemu.
- [ ] Require SD-copy hash and physical chooser PASS before functional evidence.

## Exact resume point

Run the corrected D81 builder to create `F65R0D2.D81` from a new fresh format;
confirm raw header `F65 R0-D` / `65`, run the full host gate, and update all
records with its identity. Do not mount/copy the replacement until it completes
Stage 1 and Stage 2. Do not retry `F65R0D.D81`.

## Checkpoint log

2026-08-30T09:00:00-07:00 — stage: CODING; branch:
`codex/r0-d-development`; local HEAD:
`d02be340834563a5d76c03243f73d27cdca004e3`; remote verification: baseline is
advertised by `origin/codex/r0-c-development`, no R0-D publication; completed:
reconciled repository/sentinels/R0-C evidence, read the D81 gate, and recorded
the supplied-document hashes; validation: Git and sentinel checks PASS;
artifacts: no R0-D artifact; unresolved: v1.6 is not yet represented in the
historical official record and all R0-D evidence is pending; next: create R0-D
admission, plan, ownership, and proof contracts; authorization: Stage-1 coding
only, no Xemu or hardware.

2026-08-30T09:25:00-07:00 — stage: CODING; branch:
`codex/r0-d-development`; local HEAD:
`d02be340834563a5d76c03243f73d27cdca004e3`; remote verification: no R0-D
publication; completed: R0-D proof-only contracts, generator, host fixture,
target diagnostic, static/map accounting, and Stage-1 records; validation:
bootstrap, host tests, verify, target build, map/symbol/disassembly review, and
`git diff --check` PASS; artifacts: PRG SHA-256
`ad4827da70d6f4a571817df2268bb3ca4e88d11a0f8aacfc11441abca2fd1677`, no
D81; unresolved: Xemu/hardware evidence and actual protected-work timing are
not claimed; next: review diff and commit Stage-1 work; authorization: Stage-1
only, no publication, Xemu, or hardware.

2026-08-30T09:35:00-07:00 — stage: CODING; branch:
`codex/r0-d-development`; local HEAD:
`2bcb54e046e9cdcd8f03b7daaa12141a474c6af0`; remote verification: no R0-D
publication; completed: staged full diff review and committed Stage-1 R0-D
implementation; validation: final host tests, generated-binding verify, static
target validation, target build, map accounting, and diff check PASS; artifacts:
PRG SHA-256 `ad4827da70d6f4a571817df2268bb3ca4e88d11a0f8aacfc11441abca2fd1677`,
no D81; unresolved: this post-commit checkpoint requires commit, Xemu/hardware
remain unrun, and actual hardware timing is unmeasured; next: commit checkpoint
then await VS Code publication authorization; authorization: Stage-1 only, no
publication, Xemu, or hardware.

2026-08-30T09:50:00-07:00 — stage: CODING COMPLETE reconciliation; branch:
`codex/r0-d-development`; local HEAD:
`62ffb16efbf448bea72e894269061101d5ff1ab9`; remote verification: no R0-D
publication; completed: final Stage-1 verification rerun and checkpoint/Git
reconciliation; validation: host test, generated-binding verify, static target
validation, target build, build-accounting and diff check PASS; artifacts: PRG
SHA-256 `ad4827da70d6f4a571817df2268bb3ca4e88d11a0f8aacfc11441abca2fd1677`,
no D81; discrepancy corrected: the prior checkpoint lagged the already-created
Stage-1 documentation commit; next: commit this reconciliation and await
explicit VS Code publication authorization; authorization: coding complete,
publication/Xemu/hardware not authorized.

2026-08-30T10:05:00-07:00 — stage: PUSH VIA VS CODE; branch:
`codex/r0-d-development`; local HEAD:
`5c2ff556968281092eb972e6c31e4492d9bdffda`; remote verification: PASS,
`git ls-remote` returned that exact commit for
`refs/heads/codex/r0-d-development`; completed: owner published Stage-1 work
through VS Code and remote identity was verified; validation: clean worktree
and remote branch match; artifacts: unchanged PRG SHA-256
`ad4827da70d6f4a571817df2268bb3ca4e88d11a0f8aacfc11441abca2fd1677`, no
D81; unresolved: this publication checkpoint needs commit/push, Xemu/hardware
are unrun; next: commit/push this checkpoint and verify remote; authorization:
publication checkpoint only, no Xemu or hardware.

2026-08-30T10:20:00-07:00 — stage: XEMU TESTING admission; branch:
`codex/r0-d-development`; local/remote HEAD:
`c5a12d936e07fa20e1ca43333042cb7a3fcaa57f`; remote verification: PASS;
completed: reverified branch, remote identity, clean state, D81 non-applicability,
and pinned Xemu identity; validation: Xemu version check PASS; artifacts:
unchanged PRG SHA-256 `ad4827da70d6f4a571817df2268bb3ca4e88d11a0f8aacfc11441abca2fd1677`,
no D81; unresolved: `F65_MEGA65_ROM` is unavailable, so no emulator start or
Xemu result exists; next: configure the owner-ROM path and run two clean boots;
authorization: Xemu only, no physical testing.

2026-08-30T10:35:00-07:00 — stage: XEMU TESTING; branch:
`codex/r0-d-development`; source commit under test:
`c5a12d936e07fa20e1ca43333042cb7a3fcaa57f`; completed: ROM identity verified,
two clean PRG boots, screen/result-block validation, and determinism comparison;
validation: PASS; artifacts: PRG SHA-256
`ad4827da70d6f4a571817df2268bb3ca4e88d11a0f8aacfc11441abca2fd1677`,
result-block SHA-256 `24f8e8dac28e79d9615bbae9fb58b716e92cf55b515e66483769721cf14587f7`,
no D81; unresolved: Xemu evidence commit requires publication and physical
hardware remains unauthorized; next: commit/publish Xemu evidence; authorization:
Xemu complete, no physical testing.

2026-08-30T17:10:43-07:00 — stage: HARDWARE TESTING preflight; branch:
`codex/r0-d-development`; local/last remotely verified HEAD:
`30549f061dea55b7d78291f7a9f62bdda9386bd8`; remote verification: PASS before
physical admission; completed: physical authorization received and the exact
published PRG was re-hashed; validation: PRG SHA-256 remains
`ad4827da70d6f4a571817df2268bb3ca4e88d11a0f8aacfc11441abca2fd1677`, no D81
exists and no D81 operation occurred; artifacts: source evidence commit
`30549f`, executable source commit `c5a12d9`, direct PRG only; unresolved: no
approved physical launch procedure for a standalone PRG exists in the retained
evidence; next: obtain the owner's already-proven direct-PRG launch method,
then capture physical evidence; authorization: Stage-4 physical testing,
bounded to R0-D and with no D81 workaround.

2026-08-30T17:12:20-07:00 — stage: HARDWARE TESTING preflight guide; branch:
`codex/r0-d-development`; local HEAD before this documentation commit:
`30549f061dea55b7d78291f7a9f62bdda9386bd8`; remote verification: that commit
remains the last verified published identity; completed: updated the R0-D test
guide, evidence map, handoff, and durable checkpoint with the exact direct-PRG
copy/hash/capture requirements; validation: `git diff --check` PASS and PRG
SHA-256 recheck PASS (`ad4827da70d6f4a571817df2268bb3ca4e88d11a0f8aacfc11441abca2fd1677`);
artifacts: no D81 and no D81 gate state entered; unresolved: the physical PRG
launcher is still unspecified by controlled evidence; next: commit this guide,
then await the owner-proven launch method and returned hardware capture;
authorization: Stage-4 physical testing, no unverified loader behavior.

2026-08-30T17:59:38-07:00 — stage: CODING (D81 carrier correction); branch:
`codex/r0-d-development`; local HEAD:
`b081e7c847f822c5d3e3e2bb254330172c7e795a`; last remotely verified commit:
`30549f061dea55b7d78291f7a9f62bdda9386bd8`; completed: reconciled the owner
clarification that R0-D is delivered as a D81 containing its PRG, re-read the
mandatory D81 gate, and inspected the retained R0-A/R0-C `AUTOBOOT.C65` and
one-session `c1541` conventions; validation: clean worktree and branch/remote
identity verified, no R0-D D81 created or mounted; artifacts: prior direct PRG
SHA-256 `ad4827da70d6f4a571817df2268bb3ca4e88d11a0f8aacfc11441abca2fd1677`,
no candidate D81 yet; unresolved: fresh builder, structural/content validator,
and D81 identity are pending; next: implement the R0-D-owned D81 path without
copy/append; authorization: Stage-1 coding for the D81 correction, existing
Xemu/physical authorization applies only after required preceding gates.

2026-08-30T18:00:00-07:00 — stage: CODING D81 host-gate diagnosis; branch:
`codex/r0-d-development`; local HEAD:
`b081e7c847f822c5d3e3e2bb254330172c7e795a`; remote verification: last
verified `30549f061dea55b7d78291f7a9f62bdda9386bd8`; completed: created the
first fresh, one-session `F65R0D.D81` candidate and ran its host gate;
validation: build/static checks PASS, but `R0D-D81-STRUCT-001` correctly FAILed
on a validator directory-block-count parsing defect; failed artifact:
`F65R0D.D81`, 819200 bytes, SHA-256
`9bac7a0bc28b14618524be487fcd1aeee55dd6f78cb0312d0879401c20a6457f`, recorded
in `build/r0d/reports/F65R0D.D81-create.txt` and `F65R0D.D81-list.txt`; no
Xemu, SD transfer, chooser, or hardware test occurred; unresolved: validator
offset correction requires a fresh rebuild, and the failed identity is invalid
and must not be used; next: correct the validator and fresh-format a new
candidate; authorization: Stage-1 D81 coding only.

2026-08-30T18:05:00-07:00 — stage: CODING D81 host-gate diagnosis; branch:
`codex/r0-d-development`; local HEAD:
`b081e7c847f822c5d3e3e2bb254330172c7e795a`; remote verification: unchanged
at `30549f061dea55b7d78291f7a9f62bdda9386bd8`; completed: retained the second
host-gate failure evidence and identified the raw D81 BAM fact: track 40 has
36 free sectors with only `40/0..3` allocated, so unused directory sectors are
not permanently reserved; validation: prior candidate hash remains
`9bac7a0bc28b14618524be487fcd1aeee55dd6f78cb0312d0879401c20a6457f` and is
invalid — do not use; artifacts: controlled construction log retained; unresolved:
correct the validator's system-sector model and ensure the new fresh image has
a distinct disk ID/hash; next: fresh-format the D1 carrier and rerun all host
gates; authorization: Stage-1 D81 coding only.

2026-08-30T18:06:24-07:00 — stage: CODING D81 host verification; branch:
`codex/r0-d-development`; local HEAD before the D81 implementation commit:
`b081e7c847f822c5d3e3e2bb254330172c7e795a`; remote verification: last
verified `30549f061dea55b7d78291f7a9f62bdda9386bd8`; completed: fresh-formatted
the D1 carrier and wrote `AUTOBOOT.C65` plus `R0D-CALIB` in one pinned c1541
session, then ran raw geometry/BAM/directory/chain/ownership checks and c1541
extraction/hash checks; validation: `make r0d-build r0d-verify` PASS,
`git diff --check` PASS; artifacts: `F65R0D.D81`, 819200 bytes, SHA-256
`a1d11bfb2b18a92618d55b5f3051a44d019adbdf2ba70b7c6715049567638d48`, state
`HOST_CONTENT_VERIFIED`; unresolved: this candidate must be rebuilt after the
source commit to stamp its builder identity, then published and revalidated in
Xemu; next: review/commit the D81 source and documentation; authorization:
Stage-1 coding only, no Xemu mount or physical copy.

2026-08-30T18:10:00-07:00 — stage: CODING COMPLETE; branch:
`codex/r0-d-development`; carrier source commit:
`13ebdf977a192ff65e1d34f450824a7b4eff5ef6`; last remotely verified commit:
`30549f061dea55b7d78291f7a9f62bdda9386bd8`; completed: committed the fresh
one-session D81 builder, `AUTOBOOT.C65`, raw structural/content validator, and
R0-D record changes, then rebuilt the exact committed carrier; validation:
`make r0d-build r0d-verify` PASS, builder c1541 hash matched the lock, raw
geometry/BAM/directory/file-chain/ownership PASS, and c1541 extraction/hash
PASS; artifacts: `F65R0D.D81`, 819200 bytes, D1, SHA-256
`a1d11bfb2b18a92618d55b5f3051a44d019adbdf2ba70b7c6715049567638d48`, state
`HOST_CONTENT_VERIFIED`, payload `R0D-CALIB` SHA-256
`ad4827da70d6f4a571817df2268bb3ca4e88d11a0f8aacfc11441abca2fd1677`;
unresolved: publication, D81-specific Xemu, SD transfer, and physical chooser
are unrun; next: commit this checkpoint and hand off for VS Code push;
authorization: Coding complete, no D81 mount/Xemu/physical action until the
source publication stage is verified.

2026-08-30T18:15:00-07:00 — stage: PUSH VIA VS CODE verification; branch:
`codex/r0-d-development`; local/remote HEAD:
`fa108a819385b66ac4e77d8d39572bf3433b2005`; remote verification: PASS,
`git ls-remote --heads origin refs/heads/codex/r0-d-development` returned the
same commit; completed: owner confirmed the VS Code push, and branch/clean
state plus exact D81 SHA-256 were reverified; validation: `F65R0D.D81`
SHA-256 remains `a1d11bfb2b18a92618d55b5f3051a44d019adbdf2ba70b7c6715049567638d48`,
state `HOST_CONTENT_VERIFIED`; unresolved: this required publication checkpoint
needs commit and final VS Code sync, then D81-specific Xemu is pending; next:
commit/publish this checkpoint and reverify remote; authorization: source
published, Xemu authorization retained but not yet exercised on the D81.

2026-08-30T19:20:00-07:00 — stage: XEMU TESTING boot 1; branch:
`codex/r0-d-development`; local/remote HEAD:
`d5acdce4b9cb94b137002de32a00e8b65a5d9a1b`; remote verification: PASS;
completed: reran the host structural/content D81 gate and booted the exact D81
from a clean Xemu start at drive 8 with `-autoload`; validation: banner/result
block PASS, D81 hash unchanged; artifacts: D81 SHA-256
`a1d11bfb2b18a92618d55b5f3051a44d019adbdf2ba70b7c6715049567638d48`, screen
SHA-256 `cd424a2b51109d891a3c3388f0da114042462ddab43f543d912bcdff41e8bcf2`,
result-block SHA-256 `24f8e8dac28e79d9615bbae9fb58b716e92cf55b515e66483769721cf14587f7`;
unresolved: second clean boot required; next: clean boot 2; authorization:
Stage-3 Xemu only.

2026-08-30T19:22:42-07:00 — stage: XEMU TESTING complete; branch:
`codex/r0-d-development`; local/remote HEAD:
`d5acdce4b9cb94b137002de32a00e8b65a5d9a1b`; remote verification: PASS;
completed: second clean D81 boot, deterministic comparison, and post-mount D81
hash verification; validation: both screen/result-block hashes and screenshot
SHA-256 `a1217395a3d60788d4df449f02cec9642913f5d107122dad6504542131f200f8`
match, D81 remains unchanged; artifacts: D81 state `XEMU_BOOT_VERIFIED`, logs,
screens, memory dumps, and screenshots at `build/r0d/reports/R0D-D81-XEMU-boot*`;
unresolved: evidence documentation must be committed/published, then SD-copy
and physical chooser evidence are pending; next: commit/publish Xemu evidence;
authorization: Xemu complete, physical authorization awaits the ordered gates.

2026-08-30T19:35:00-07:00 — stage: HARDWARE TESTING failure / CODING return;
branch: `codex/r0-d-development`; local/last remotely verified HEAD:
`33ce4342a73a90c7dc1c199bf89c714ce8d072f3`; remote verification: PASS before
physical selection; completed: preserved owner photo showing selected
`F65R0D.D81` with chooser `ERROR CODE FF`; validation: physical chooser FAIL,
no directory/program execution claim, and source D81 hash was
`a1d11bfb2b18a92618d55b5f3051a44d019adbdf2ba70b7c6715049567638d48` but the
SD-copy hash was not captured; artifacts: failure photo SHA-256
`e5e2ba6b54490229e9e29c0afd01807820ac00fb3992a858d8989bfa1409bf09`, failed
D81 identity INVALID — DO NOT USE; unresolved: construction versus transfer is
not separable without copied-file hash, and the host gate omitted the accepted
header profile assertion; next: correct the validator and fresh-build a unique
replacement; authorization: return to Stage-1 correction, no reuse/mount of
the failed identity.

2026-08-30T19:45:00-07:00 — stage: CODING replacement D81 host gate; branch:
`codex/r0-d-development`; local HEAD before replacement commit:
`33ce4342a73a90c7dc1c199bf89c714ce8d072f3`; remote verification: unchanged
at `33ce434`; completed: corrected the missing physical-profile header check,
created distinct `F65R0D2.D81` through a fresh one-session format/write, and
ran the complete host gate; validation: `make r0d-build r0d-verify` PASS, raw
header label `F65 R0-D` / ID `65` PASS, structural/content extraction/hash PASS;
artifacts: `F65R0D2.D81`, 819200 bytes, SHA-256
`51dd4ad5a0fe402eccbac81b1ec0e44d12f5ab2294a9f01b1e7452711fa52643`, state
`HOST_CONTENT_VERIFIED`; unresolved: this new identity needs commit, VS Code
publication, and replacement Xemu gates; next: commit the failure record and
replacement builder; authorization: Stage-1 correction only, no replacement
mount/transfer/physical selection.

## Historical R0-C checkpoint (preserved)

### Original objective

Resume the existing F-65 R0-C work without restarting it, identify and correct the D81 carrier-loadability failure that produced MEGA65 chooser error code FF, and establish a durable repository-root loadability gate for every future branch and prompt. Build and validate a fresh D81 through the approved one-session construction path. Close the candidate by explicit owner waiver of further physical fault testing, without mislabeling that waiver as a formal hardware gate pass.

## Current status

- Repository: `/Users/slice/Documents/Codex/f65-megawing`
- Branch: `codex/r0-c-development`
- HEAD at resume: `d631c9d935632e1813399ae8a13f6e131d0506a6`
- Remote: `https://github.com/SUON1/f65-megawing.git`
- Working tree was clean at resume.
- The branch contains the prior D81 loadability audit. The root gate and corrected fresh-build validation are now complete in this continuation.
- The physical chooser failure is treated as a hard carrier failure, not as a program/runtime failure.
- Owner requested R0-C completion on 2026-08-29 and waived further media-fault execution after confirming the corrected carrier loads without `ERROR CODE FF` and reaches the fixture menu.

## Completed work

- R0-B is recorded as closed in the prior accepted history; R0-C remains a proof candidate and is not formally gate-passed.
- DEC-012 was approved for the R0-C media-fault fixture only: sacrificial writable media, with no production save-medium selection.
- The narrow Attic CPU-copy contract was admitted; the ROM-reclaim/storage handoff contract remains deferred.
- Prior R0-C host/Xemu/static proof work and physical evidence remain preserved.
- Prior commit `26ea67a` reissued the device-nine media fixture, and commit `d631c9d` documented the D81 loadability audit.
- The incident audit identified `tools/build/r0c.sh` as copying `F65-R0C-CONTROL.D81` to `F65-R0C-MEDIA.D81` and reopening the copy in a second `c1541` session to append a file. That is prohibited by the loadability gate and is the leading cause of chooser error FF.

## Files changed

- This checkpoint: `CODEX_PROGRESS.md` (created in this continuation).
- Prior committed changes include the R0-C build scripts, media fixture, diagnostics, evidence, and D81 loadability audit. No prior R0-C source is being discarded or rewritten.
- Continuation changes are limited to the root D81 gate, the fresh one-session D81 build path, matching validators/tests, and their documentation/evidence.

## Decisions and architecture

- The proof carrier selected in the MEGA65 chooser is mounted at device 8. Its bootstrap must load its resident proof program from device 8.
- The sacrificial writable media fixture is mounted at device 9 and is probed only after its bootstrap is loaded from the selected device-8 carrier.
- Every candidate D81 must be freshly formatted and populated in one pinned `c1541` construction session. No copy-and-append workflow is allowed.
- PETSCII-safe on-disk names and the exact artifact identity must be retained; host filenames and PETSCII directory names are not interchangeable.
- A failed image identity is discarded. It is never repaired, renamed, appended to, or released.
- Required state progression is `UNVERIFIED -> HOST_STRUCTURALLY_VERIFIED -> HOST_CONTENT_VERIFIED -> XEMU_BOOT_VERIFIED -> PHYSICAL_CHOOSER_VERIFIED -> TEST_ELIGIBLE`.

## Validation performed

- Verified repository root, branch, clean status, HEAD, remote, and recent history in the actual source repository.
- Inspected the D81 loadability gate source supplied by the owner.
- Inspected the current `tools/build/r0c.sh` construction path and confirmed the prohibited copy/reopen/append sequence.
- Inspected the pinned VICE `c1541` path in the toolchain lock.
- Physical evidence supplied by the owner shows the chooser listing and error code FF for the bad image; earlier carriers load successfully.

## Known problems or unresolved issues

- `tools/build/r0c.sh` currently creates the media image by copying an existing D81 and appending in a second `c1541` session.
- The media bootstrap and host validators still describe the old device-9 boot arrangement instead of selecting the carrier at device 8 and probing the sacrificial fixture at device 9.
- The current media validator expects the old mixed carrier/fixture directory layout.
- Physical chooser verification was reported by the owner as successful; the remaining physical fault matrix is owner-waived and is not claimed as PASS.

## Remaining work checklist

- [x] Add the exact repository-root `00_D81_LOADABILITY_GATE.md` and wire its mandatory prompt header into `AGENTS.md`.
- [x] Correct `media_boot.bas` and its host assertions so the selected carrier boots from device 8 while the fixture probes device 9.
- [x] Replace the copy-and-append D81 build with one fresh-format, one-session construction of the physical-test carrier.
- [x] Update media/D81/Xemu validators and manifests to the corrected carrier identity and layout.
- [x] Add host structural/content extraction validation for geometry, BAM, directory chains, file chains, crosslinks, exact lengths, and source hashes.
- [x] Build the fresh artifact with the pinned toolchain and record its exact hash and identity.
- [x] Run host/static validation and repeat the Xemu-capable load test with the owner ROM.
- [x] Append the resulting evidence and exact resume state here before stopping.
- [x] Provide the owner the exact new file path, hash, and physical chooser test instruction; do not push without new explicit authorization.

## Exact resume point

The R0-C candidate is complete by owner waiver. The exact fresh carrier is `build/r0c/artifacts/F65-R0C-MEDIA.D81`, SHA-256 `e01eb41cff0158e7b609a365ecc72b78b3ce825ddca06a42a32f8954f4c7e8d0`; package SHA-256 is `9b535b022c97a7b9eb52552ac07f7776c677f23a3c604b75f9541d43c114f19f`. Host/static and Xemu are PASS. Physical chooser/loadability is owner-reported PASS; the remaining fault matrix is WAIVED, not PASS. R0C-ROM-001 remains deferred.

## Checkpoint entries

### 2026-08-28 — initial continuation checkpoint

- Confirmed the real repository is `/Users/slice/Documents/Codex/f65-megawing`, branch `codex/r0-c-development`, HEAD `d631c9d935632e1813399ae8a13f6e131d0506a6`, with a clean working tree.
- Resumed at the exact D81 loadability defect identified by the prior audit: copied D81 plus second-session append.
- No substantive source changes made yet in this continuation.

### 2026-08-28 — fresh carrier correction and validation

- Added the repository-root `00_D81_LOADABILITY_GATE.md` and wired the mandatory rule into `AGENTS.md`.
- Corrected both BASIC boot paths to load the selected carrier from device 8 while the media fixture owns only device 9 operations.
- Replaced the prohibited copy/reopen/append sequence in `tools/build/r0c.sh` with fresh-format, one-session `c1541` construction.
- Added fail-closed raw D81 chain plus c1541 extraction validation and gate evidence.
- Rebuilt twice with the pinned Java/LLVM-MOS/VICE toolchain; both builds produced identical D81 hash `e01eb41cff0158e7b609a365ecc72b78b3ce825ddca06a42a32f8954f4c7e8d0`.
- Host/static result: PASS. Xemu result: PASS with `MEGA65.ROM`; media screen shows the fixture menu. Physical chooser remains awaiting owner verification.

### 2026-08-28 — documentation and syntax checkpoint

- Updated `docs/testing/R0-C_TEST_GUIDE.md` and the D81 audit with the fresh hash and corrected device roles so the owner will not be directed to the retired carrier or the old copy-and-append path.
- Python validator syntax, shell syntax, and `git diff --check` pass. Generated build outputs remain controlled/ignored artifacts; source changes are the files shown above.

### 2026-08-28 — local handoff checkpoint

- Committed the loadability correction as `ddd37b2` (`fix(r0c): enforce fresh d81 loadability gate`).
- Working tree is clean and the branch is one commit ahead of origin; no push was performed.
- Exact artifact for owner verification remains `build/r0c/artifacts/F65-R0C-MEDIA.D81` with SHA-256 `e01eb41cff0158e7b609a365ecc72b78b3ce825ddca06a42a32f8954f4c7e8d0`.
- Stop point: owner must verify the hash after SD transfer and perform the physical chooser test. A physical result is not inferred from host/Xemu PASS.

### 2026-08-28 — physical chooser result received

- Owner reports the exact copied carrier loads without chooser `ERROR CODE FF`.
- This closes the physical chooser/loadability observation for the carrier only; it does not close the media fault matrix or formal R0-C gate.
- Next test: mount a separate sacrificial writable D81 on device 9, initialize both generations, then recover and photograph the result.

### 2026-08-28 — physical fixture menu reached

- Owner photos show the corrected carrier boots without `ERROR CODE FF` and the R0-C media fixture menu is visible.
- Device roles are visibly correct: the harness is loaded from device 8 and states that only device 9 is probed.
- Initialization is awaiting the confirmation key: the captured screen still says `PRESS Y TO CONTINUE`; no initialization PASS is claimed yet.

### 2026-08-29 — owner closure waiver

- Owner requested that all R0-C records be updated and the candidate called complete.
- Closure status: `R0-C IMPLEMENTATION COMPLETE — OWNER-WAIVED REMAINING PHYSICAL MEDIA FAULT MATRIX`.
- The corrected carrier's physical chooser/loadability result is accepted as owner-reported PASS; no claim is made for unexecuted save/media fault cases, ROM reclaim, or formal `R0-C GATE PASSED`.

### 2026-08-29 — R0-C records reconciled

- Updated the official record, task admission, execution plan, agent record, handoff, evidence map, blockers, D81 audit, platform/ROM reports, and test guide.
- Local closure commit: `f476a8b` (`docs(r0c): close candidate by owner waiver`).
- Branch remains unpushed and clean after this checkpoint commit; no formal hardware-gate PASS is claimed.
