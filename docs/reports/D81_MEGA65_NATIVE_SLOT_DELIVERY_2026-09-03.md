# D81 MEGA65-Native Slot Delivery

## Decision

Use a fresh D81 slot allocated by the MEGA65 Freezer itself when the existing
system SD card must be preserved, Ethernet is unavailable, and normal macOS
copy allocation does not pass the one-extent gate. This replaces the incorrect
blank-card recommendation and does not attribute the defect to the card or the
MEGA65 hardware.

## Official-source basis

Official `mega65-freezemenu` source commit
`844754576a6f1a4e92e4c10614ea853719d56037` was inspected locally.

- `makedisk.c` accepts an eight-character name for `NEW D81 DD IMAGE`, appends
  `.D81`, and calls `fat32_create_contiguous_file()` with
  `80 * 10 * 2 * 512`, exactly 819,200 bytes.
- `fdisk_fat32.c` documents that this routine creates a contiguous file, scans
  for enough consecutive free clusters, and writes the FAT chain.
- `freeze_diskchooser.c` maps error `0x8B` to `IMAGE FRAGMENTED`. Error `0xFF`
  is not that mapping; it reaches the generic error display, while an older
  commented table describes it as `NO SUCH TRAP / EOF`.

Consequently, a chooser `FF` proves that attach failed before the contained
program ran, but it does not independently prove fragmentation. Exact-byte and
FAT-chain evidence must localize the fault.

## Controlled procedure

1. Fresh-build and host-verify a candidate whose uppercase FAT 8.3 host name is
   the final authorized name.
2. On the MEGA65, create a never-tested root slot with `NEW D81 DD IMAGE` using
   the same stem.
3. Move the safely powered-down card to macOS.
4. Run `tools/diagnostics/d81_sd_fill_mega65_slot.sh` under `sudo`.
5. The helper proves the preimage is one extent, takes a verified host backup,
   writes exactly 819,200 bytes with `conv=notrunc`, proves the final hash and
   one-extent allocation, and safely ejects.
6. Only then select that exact name in the physical chooser.

The procedure neither resizes nor replaces the FAT directory entry, so the
Freezer-created cluster chain remains intact. It never modifies system/parent
files. If a post-write check fails, the helper restores the slot's original
bytes in place and leaves the card mounted for inspection.

## R0-E candidate identity

```text
HOST_FILENAME: F65R0EF.D81
D81_BYTES: 819200
D81_SHA256: ca85f73ffba93ea290078a60b372406dc6ab58eddacdf0765f7589cea039c40f
DISK_LABEL: F65 R0-E
DISK_ID: 65
ENTRY_FILES: AUTOBOOT.C65, R0E-PROOF, R0E-EVID
BUILDER: toolchain/vice-clean/bin/c1541
BUILDER_SHA256: 73235289aca30a7e2e8067e521bf604743156cc1d7499c888a3894d6e46fcb3c
D81_STATE: HOST_CONTENT_VERIFIED; AWAITING XEMU/SD/PHYSICAL GATES
```

The filename is new because prior E2/E3/E4 tested copies are retired. The D81
bytes reproduce the already recorded R0-E one-variable PRG-delta candidate;
only the host filename changes to match the new MEGA65-created slot.

## Physical SD transfer result — 2026-09-04

`F65R0EF.D81` was rejected before testing because the raw FAT32 audit measured
13 extents. Its bytes matched the candidate, but it had been delivered through
a file-replacement path rather than the required untouched-slot transaction.
That tested copy is retired.

The replacement identity `F65R0EG.D81` was freshly constructed in one pinned
`c1541` session with the same deterministic D81 bytes, then delivered through
the MEGA65-native slot procedure. The owner created the empty slot with
`NEW D81 DD IMAGE` and ran the guarded slot-fill helper. Recorded results:

```text
D81_STATE: AWAITING_PHYSICAL_CHOOSER_VERIFICATION
D81_FILENAME: F65R0EG.D81
D81_SHA256: ca85f73ffba93ea290078a60b372406dc6ab58eddacdf0765f7589cea039c40f
D81_BYTES: 819200
DISK_LABEL: F65 R0-E
DISK_ID: 65
ENTRY_FILENAME: AUTOBOOT.C65
SOURCE_BRANCH: codex/r0-e-development
SOURCE_COMMIT: 702700f
BUILDER_IDENTITY: toolchain/vice-clean/bin/c1541
BUILDER_SHA256: 73235289aca30a7e2e8067e521bf604743156cc1d7499c888a3894d6e46fcb3c
HOST_STRUCTURAL_RESULT: PASS
HOST_CONTENT_RESULT: PASS
XEMU_RESULT: NOT RUN FOR THIS EXACT FILENAME
XEMU_EVIDENCE: NONE; exact artifact physical chooser test remains gated
SD_COPY_SHA256: ca85f73ffba93ea290078a60b372406dc6ab58eddacdf0765f7589cea039c40f
SD_FILESYSTEM: MS-DOS FAT32
SD_DEVICE_IDENTIFIER: disk4s1
SD_TRANSFER_METHOD: MEGA65-created contiguous slot; guarded dd conv=notrunc fill
SD_CONTIGUITY_RESULT: PASS
SD_EXTENT_COUNT: 1
SD_EXTENT_EVIDENCE: logical 0, bytes 819200, device offset 103182336
SD_ALLOCATION_PRESERVED: PASS; same device offset before and after fill
SD_SAFE_EJECT_RESULT: PASS
PHYSICAL_CHOOSER_RESULT: AWAITING HUMAN
```

The pre-fill slot hash was
`1e743a99b1806271413e8a49951683b3edb8ff8b35ee8e0f8b6753ebccdb5b01`.
Both the pre-fill and post-fill raw FAT32 audits reported one 819,200-byte
extent at device offset `103182336`. The final hash matched the host candidate,
and `diskutil` successfully ejected `/Volumes/MEGA65FDISK`. This is direct
evidence that the in-place fill preserved the Freezer-created allocation.

## Physical chooser and runtime result — 2026-09-04

The owner mounted and loaded `F65R0EG.D81` successfully on the intended
MEGA65. The physical photo retained at
`docs/evidence/r0e/physical/F65R0EG-PHYSICAL-RUNTIME-2026-09-04.jpg`
(SHA-256 `ab813983ba1b8e4a01446648d922590c115fde0ef31f9aa5ebc5f2a87ce81087`)
shows the Rev3 R0-E result screen. It is the physical confirmation that the
MEGA65-created-slot delivery route succeeds where normal host file replacement
produced fragmented, unmountable D81 files.

### Standard delivery recipe for R0-F and later proof carriers

1. Fresh-format the candidate and write every payload in one pinned `c1541`
   session; never copy-and-append a D81.
2. Run structural and extraction/hash validation on the completed host D81.
3. On the MEGA65 system card, use `NEW D81 DD IMAGE` to create a *new unique*
   uppercase 8.3 root slot matching the candidate filename.
4. Return the card to macOS without Finder-copying or replacing that slot.
5. Run `sudo tools/diagnostics/d81_sd_fill_mega65_slot.sh SOURCE.D81
   /Volumes/MEGA65FDISK SHA256`.
6. Proceed only when its pre-fill and post-fill raw FAT32 audits both report
   one extent, the final hash matches, and safe eject reports PASS.

The helper is deliberately fail-closed: it backs up the new Freezer-created
slot, writes exactly 819,200 bytes with `conv=notrunc`, and restores the slot
if any post-write validation fails. It never modifies the system-card parent
files. `F65R0EF.D81` is retained only as a failed 13-extent delivery identity;
do not reuse it.
