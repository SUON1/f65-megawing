# CODEX Progress

## Original objective

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
