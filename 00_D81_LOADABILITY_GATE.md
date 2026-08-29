# MANDATORY FIRST-READ — D81 Loadability Gate

**This file must exist at the repository root on every branch that creates, modifies, copies, renames, packages, mounts, tests, or releases a D81 image. Its Prompt Header must be included at the beginning of every prompt that can affect a D81.**

This is a fail-closed release contract. A D81 is not testable, releasable, or “final” merely because it was built, is 819,200 bytes, appears in a file chooser, or can be listed by `c1541`.

The purpose of this gate is to prevent an unverified or structurally damaged D81 from reaching the owner. A MEGA65 freeze-menu or file-chooser `ERROR CODE FF` is a **carrier-image failure**, occurring before the contained program runs. It invalidates the D81 and all test claims based on it.

## Prompt Header — copy this block verbatim

```text
MANDATORY D81 LOADABILITY GATE

Before creating, modifying, copying, renaming, packaging, mounting, testing, or releasing any D81, read and obey the repository-root file 00_D81_LOADABILITY_GATE.md.

The work must fail closed. A D81 may not be called final, test-ready, loadable, or delivered for physical testing until the exact artifact passes every applicable state in this order:

UNVERIFIED
-> HOST_STRUCTURALLY_VERIFIED
-> HOST_CONTENT_VERIFIED
-> XEMU_BOOT_VERIFIED
-> PHYSICAL_CHOOSER_VERIFIED
-> TEST_ELIGIBLE

Never build a new test carrier by copying an existing D81 and reopening the copy in a second c1541 session to append files. Fresh-format the image and populate all files in one pinned-tool construction session.

ERROR CODE FF at the MEGA65 chooser is a hard carrier failure. Discard that image identity, investigate, and fresh-build a new image. Do not patch, append to, or rename the failed image and do not blame the program inside it.
```

## Non-negotiable rules

1. **Fresh image only.** Create every candidate D81 from a newly formatted blank image using the pinned D81 tool.
2. **One construction session.** Add every directory entry and payload during one controlled `c1541` construction session.
3. **No copy-and-append.** The following pattern is prohibited:

   ```text
   copy CONTROL.D81 to NEW.D81
   reopen NEW.D81
   append another file
   ```

4. **Never repair a failed image in place.** A chooser failure, mount failure, BAM error, directory error, chain error, extraction mismatch, or hash mismatch permanently invalidates that artifact identity.
5. **PETSCII-safe disk names.** Use short, explicit, unique on-disk filenames compatible with the target filesystem. Host filenames and PETSCII/on-disk filenames must be recorded separately.
6. **No casual renaming.** The filename verified in Xemu must be the filename copied to the SD card and selected on hardware. If a rename is unavoidable, the renamed copy becomes a new artifact and must repeat all gates.
7. **Exact artifact identity.** Every released image must have a recorded byte length and SHA-256. Instructions, manifests, screenshots, and evidence must identify that exact hash.
8. **No inference from weak checks.** Image size, successful build exit, directory listing, or file-chooser visibility alone never proves loadability.
9. **Fail closed.** Missing tools, missing verification, ambiguous output, or an unavailable environment produces `NOT VERIFIED`, never PASS.
10. **Never call an unverified artifact “FINAL.”** Use `CANDIDATE` until it reaches `TEST_ELIGIBLE`.

## Required construction procedure

The build must perform these operations in order:

1. Remove only the previous generated candidate in the controlled build directory. Never use a user media image as a build input.
2. Invoke the pinned `c1541` identity recorded by the repository toolchain lock.
3. Fresh-format a new D81 with a deterministic disk label and ID.
4. In that same construction invocation/session, write every required file.
5. Close the image cleanly.
6. Record:
   - D81 host filename.
   - Disk label and ID.
   - On-disk PETSCII filenames.
   - Exact file byte lengths.
   - Whole-image byte length.
   - SHA-256 of every source payload.
   - SHA-256 of the completed D81.
   - Builder path, version, and hash when available.
   - Source commit and branch.
7. Treat any warning, duplicate name, truncation, allocation failure, or nonzero exit as a failed build.

## Mandatory verification pipeline

### Gate 1 — Host structural verification

The completed image must be closed, reopened read-only, and independently validated.

Required checks:

- Exact D81 size is 819,200 bytes.
- D81 geometry is valid.
- Header, directory, BAM, and free-block accounting are internally consistent.
- Every directory entry has a valid type, start track/sector, and block count.
- Every file chain is in range, terminates correctly, and contains no loop or cross-link.
- No allocated sector is simultaneously marked free.
- No sector is owned by more than one file or filesystem structure.
- Directory chains and BAM references remain in range.
- Free-block count recomputed from the BAM matches the reported count.

Passing `c1541 -list` is useful evidence but is not sufficient by itself.

### Gate 2 — Host content verification

Reopen the completed D81 and extract every file to a fresh temporary directory.

For every file:

- Compare extracted byte length to the source byte length.
- Compare extracted SHA-256 to the source SHA-256.
- Confirm the expected PETSCII/on-disk filename and file type.
- Confirm the boot or entry file is present under the documented name.

Any mismatch invalidates the entire D81.

### Gate 3 — Xemu boot verification

Use the exact completed D81 hash that will be delivered to the owner.

Required checks:

- Start Xemu with the pinned ROM, core/profile, and configuration.
- Mount the D81 using the same logical device path expected on hardware.
- Confirm the image mounts without an I/O or filesystem error.
- Load the documented entry file.
- Reach a stable, human-readable build-identification or test banner.
- Capture a screenshot and log identifying the D81 SHA-256 and source commit.
- Repeat from a clean emulator start at least once.

If Xemu cannot exercise the physical chooser path, record that limitation. Do not substitute Xemu success for the physical chooser gate.

### Gate 4 — SD transfer verification

- Copy the Xemu-verified image without altering its contents or filename.
- Flush writes and safely eject the SD card.
- When the host can remount or read the card, hash the copied file and require an exact match with the source D81.
- Record the destination filename and hash.
- Do not use Finder or another tool to modify the D81 contents after verification.

### Gate 5 — Physical chooser verification

On the intended MEGA65 hardware:

- Select the exact D81 filename and recorded hash.
- Confirm the chooser mounts it without `ERROR CODE FF` or any other error.
- Confirm the directory is readable.
- Load the documented entry file and reach its stable identity banner.
- Capture a clear photo showing the filename/build identity or the running test banner.

Only after this gate passes may the artifact state become `TEST_ELIGIBLE` and may functional hardware testing begin.

## Required release record

Every D81 delivered for testing must include a machine-readable or Markdown release record containing:

```text
D81_STATE: TEST_ELIGIBLE
D81_FILENAME:
D81_SHA256:
D81_BYTES: 819200
DISK_LABEL:
DISK_ID:
ENTRY_FILENAME:
SOURCE_BRANCH:
SOURCE_COMMIT:
BUILDER_IDENTITY:
STRUCTURAL_VALIDATOR_IDENTITY:
HOST_STRUCTURAL_RESULT: PASS
HOST_CONTENT_RESULT: PASS
XEMU_RESULT: PASS
XEMU_EVIDENCE:
SD_COPY_SHA256:
PHYSICAL_CHOOSER_RESULT: PASS
PHYSICAL_EVIDENCE:
```

No field may be silently omitted. Before physical chooser evidence exists, use:

```text
D81_STATE: AWAITING_PHYSICAL_CHOOSER_VERIFICATION
PHYSICAL_CHOOSER_RESULT: AWAITING HUMAN
```

Such an image is a candidate, not a final or test-eligible image.

## Failure handling

If any gate fails:

1. Stop testing that D81 immediately.
2. Preserve its filename, SHA-256, build log, and failure evidence for diagnosis.
3. Mark the artifact `INVALID — DO NOT USE` in the evidence record.
4. Identify whether the failure occurred during construction, verification, transfer, chooser mounting, or program execution.
5. For chooser `ERROR CODE FF`, classify the failure as D81 carrier/mount failure unless evidence proves otherwise; the contained BASIC/C/PRG program has not run yet.
6. Correct the generator or packaging process, not the failed image.
7. Fresh-format and rebuild a new D81 with a new artifact identity.
8. Repeat every gate from the beginning.

Never append to, patch, salvage, or rebrand the failed artifact as the correction.

## Branch acceptance rule

A branch that can emit D81 files is not ready to merge or hand off unless:

- This file exists unchanged at the repository root.
- The build has a non-interactive fresh-format D81 target.
- The build forbids copy-and-append construction.
- Structural and extraction/hash validators run automatically.
- A failed validation returns a nonzero status.
- Generated release records distinguish candidate, Xemu-verified, physical-verified, and test-eligible states.
- Documentation never labels a candidate D81 as final.

Any change to the D81 builder, tool version, filesystem writer, payload list, PETSCII names, boot file, disk label/ID, or post-build handling invalidates prior verification and triggers the full gate again.

## Incident provenance

This policy was created after a physical MEGA65 chooser reported `ERROR CODE FF` for an R0-C media D81. Repository review found that the media carrier had been produced by copying a completed control image and reopening the copy in a second `c1541` session to append another file. Later source edits could not explain a chooser-level failure because the chooser failed before the contained program executed.

The permanent corrective action is therefore process-level: fresh-format every candidate, populate it once, independently validate its filesystem, extract and hash every payload, boot the exact artifact in Xemu, verify the transferred copy, and require a physical chooser mount before calling it test-ready.

## Final rule

**No verified chain, no D81 release. No physical chooser mount, no hardware test claim. `ERROR CODE FF` means discard the artifact identity and rebuild from a fresh format.**

