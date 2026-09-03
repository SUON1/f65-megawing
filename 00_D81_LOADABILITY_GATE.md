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
-> SD_COPY_VERIFIED
-> SD_CONTIGUITY_VERIFIED
-> PHYSICAL_CHOOSER_VERIFIED
-> TEST_ELIGIBLE

Never build a new test carrier by copying an existing D81 and reopening the copy in a second c1541 session to append files. Fresh-format the image and populate all files in one pinned-tool construction session.

ERROR CODE FF at the MEGA65 chooser is a hard carrier failure. Retire that image identity and diagnose D81 construction, SD physical allocation, safe ejection, and platform identity before assigning a replacement. Do not patch, append to, rename, or re-test the failed image and do not blame the program inside it.

A matching hash of the SD-card copy is necessary but not sufficient. The MEGA65 Freezer requires a disk-image file to occupy one contiguous FAT32 extent. A fragmented file can hash perfectly and still fail to mount with ERROR CODE FF. Do not submit a copied image to the physical chooser until an independent extent check reports exactly one extent.
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
11. **One contiguous SD extent is mandatory.** The copied D81 must occupy exactly one physical extent on the FAT32 data partition. Logical file size and SHA-256 do not prove this.
12. **No plain-copy release procedure.** A bare `cp`, Finder copy, or equivalent followed only by `sync` and `shasum` is not an admissible transfer gate. Use the repository transfer helper or another recorded process that stages, hashes, verifies one extent, renames without rewriting, re-verifies, and safely ejects.
13. **Do not churn identities while the SD layout is unknown.** Repeatedly adding replacement D81 files to a fragmented card can repeat or worsen the condition. After a matching-hash chooser `FF`, inspect the failed SD file's extent map before building another D81.

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

### Gate 4 — SD byte-transfer verification

- Require the intended MEGA65 data partition and record its filesystem type. For the removable-card workflow it must be FAT32/MS-DOS FAT32; do not silently target APFS, exFAT, another volume, or a similarly named mount point. A built-in SD reader can report `Internal: true` while the volume is still removable; require `RemovableMedia: true`, not `Internal: false`.
- Refuse to overwrite an existing final filename. A failed D81 identity is never reused.
- Copy first to a non-D81 staging filename in the same root directory, flush writes, and require an exact SHA-256 match with the Xemu-verified source.
- Independently inspect the staging file's physical allocation and require exactly one contiguous extent covering all 819,200 logical bytes. `shasum`, `stat`, `c1541`, and Xemu cannot establish this.
- Rename the verified staging file to the exact documented final filename within the same directory, without rewriting its bytes. Recheck both SHA-256 and physical extent count after the rename.
- Flush writes and use the operating system's safe-eject operation. Record successful ejection.
- Prefer MEGA65 Ethernet file transfer when available; official MEGA65 guidance states that it does not create fragmented files. For direct card access, use `tools/diagnostics/d81_sd_transfer.sh` or an equivalently evidenced procedure.
- If one contiguous extent cannot be proven, set `SD_CONTIGUITY_RESULT: NOT VERIFIED` and stop. Do not present the image to the physical chooser.
- Do not use Finder or another tool to modify the D81 contents after verification.

### Gate 5 — SD physical-contiguity verification

- The exact final SD path must report one physical extent for the entire D81.
- Record the extent inspector identity, filesystem type, mount/device identity, extent count, logical byte count, and extent evidence.
- Treat a zero/unknown extent length, an unsupported host/filesystem, multiple extents, or an unavailable inspector as `NOT VERIFIED`, never PASS.
- A matching copied-file SHA-256 with more than one extent is `INVALID FOR MEGA65 FREEZER MOUNT` even though its bytes are intact.

### Gate 6 — Physical chooser verification

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
SD_FILESYSTEM:
SD_TRANSFER_METHOD:
SD_CONTIGUITY_RESULT: PASS
SD_EXTENT_COUNT: 1
SD_EXTENT_EVIDENCE:
SD_SAFE_EJECT_RESULT: PASS
PHYSICAL_CHOOSER_RESULT: PASS
PHYSICAL_EVIDENCE:
```

No field may be silently omitted. Before physical chooser evidence exists, use:

```text
D81_STATE: AWAITING_PHYSICAL_CHOOSER_VERIFICATION
SD_COPY_SHA256:
SD_CONTIGUITY_RESULT: PASS
SD_EXTENT_COUNT: 1
SD_SAFE_EJECT_RESULT: PASS
PHYSICAL_CHOOSER_RESULT: AWAITING HUMAN
```

Such an image is a candidate, not a final or test-eligible image.

## Failure handling

If any gate fails:

1. Stop testing that D81 immediately.
2. Preserve its filename, SHA-256, build log, and failure evidence for diagnosis.
3. Mark the artifact `INVALID — DO NOT USE` in the evidence record.
4. Identify whether the failure occurred during construction, verification, SD byte transfer, SD physical allocation, safe ejection, chooser mounting, or program execution.
5. For chooser `ERROR CODE FF`, classify the failure as carrier/mount failure unless evidence proves otherwise; the contained BASIC/C/PRG program has not run yet.
6. If the SD hash matched, remount the card read-only or without modifying the failed file and inspect its physical extent map. A multi-extent result diagnoses an SD allocation/fragmentation failure; do not blame or rebuild the D81 payload.
7. If the failed SD file was one contiguous extent, run a retained known-good same-card chooser control and record the MEGA65 core, HYPPO, Freezer/SD Essentials, and ROM identities before changing the D81 builder.
8. Correct the proven failing layer. Do not issue another D81 merely because the prior identity failed.
9. Only when D81 construction/content is implicated, fresh-format and rebuild a new D81 with a new artifact identity.
10. Repeat every applicable gate from the beginning.

Never append to, patch, salvage, or rebrand the failed artifact as the correction.

## Branch acceptance rule

A branch that can emit D81 files is not ready to merge or hand off unless:

- This file exists unchanged at the repository root.
- The build has a non-interactive fresh-format D81 target.
- The build forbids copy-and-append construction.
- Structural and extraction/hash validators run automatically.
- A failed validation returns a nonzero status.
- Generated release records distinguish candidate, Xemu-verified, physical-verified, and test-eligible states.
- The physical-transfer instructions require a matching hash, exactly one FAT32 extent, and safe ejection; `cp` plus `sync` plus `shasum` alone is rejected.
- A checked-in, fail-closed extent validator or an explicitly pinned equivalent is named in the release procedure.
- Documentation never labels a candidate D81 as final.

Any change to the D81 builder, tool version, filesystem writer, payload list, PETSCII names, boot file, disk label/ID, or post-build handling invalidates prior verification and triggers the full gate again.

## Incident provenance

This policy was created after a physical MEGA65 chooser reported `ERROR CODE FF` for an R0-C media D81. Repository review found that the media carrier had been produced by copying a completed control image and reopening the copy in a second `c1541` session to append another file. Later source edits could not explain a chooser-level failure because the chooser failed before the contained program executed.

The initial corrective action addressed internal D81 construction: fresh-format every candidate, populate it once, independently validate its filesystem, extract and hash every payload, and boot the exact artifact in Xemu. Later R0-D and R0-E incidents proved that those checks plus a matching SD-copy hash can still yield chooser `ERROR CODE FF`.

The missing layer was FAT32 physical allocation. Official MEGA65 documentation states that fragmented disk-image files cannot be mounted because the mounting mechanism requires a pointer to one contiguous SD-card region. Therefore every direct-to-card release must also prove a single physical extent and safe ejection. See the MEGA65 Freezer repository's “Copying to the SD Card” warning and the MEGA65 Welcome Guide section “A note about file fragmentation.”

## Final rule

**No verified chain, no D81 release. No single-extent SD proof, no physical chooser test. No physical chooser mount, no hardware test claim. `ERROR CODE FF` means retire the artifact identity and diagnose the failing layer before creating any replacement.**
