# D81 `ERROR CODE FF` Cross-Incident Root-Cause Audit — 2026-09-02

## Finding

The repository's D81 gate omitted a required property of the file after it was
copied to the MEGA65 SD card: the D81 must occupy one contiguous FAT32 physical
extent. The prior process checked logical bytes with SHA-256 but did not inspect
the FAT allocation chain. A fragmented copy can therefore match the source hash
exactly while remaining impossible for the Freezer to mount.

Official MEGA65 sources state this requirement directly:

- The [MEGA65 Freezer repository](https://github.com/MEGA65/mega65-freezemenu#copying-to-the-sd-card)
  warns that the SD-card copy process must avoid fragmented files.
- The [MEGA65 Welcome Guide, “A note about file fragmentation”](https://dansanderson.com/mega65/welcome/singlehtml/index.html#a-note-about-file-fragmentation)
  states that a fragmented disk image will not mount and that Ethernet transfer
  does not create fragmented files.

## Evidence pattern

- R0-C and R0-D established that `ERROR CODE FF` occurs before the contained
  program executes.
- R0-D2 and R0-E2/R0-E3 passed internal D81 structure/content checks and Xemu.
- R0-D2, R0-E2, and R0-E3 had exact matching hashes after direct SD-card copies,
  yet the physical chooser returned `FF`.
- Changing the disk label/ID from R0-E2 to R0-E3 did not change the outcome.
- Older files already resident on the same card remained chooser-readable.

These facts reject payload code, D81 logical byte corruption, and label/ID as
adequate explanations. They are consistent with—and the official platform
documentation predicts—fragmented FAT32 allocation of newly copied files.

The specific R0-E3 allocation was read from the card on 2026-09-02: the exact
819,200-byte file with the expected SHA-256 occupies **five physical FAT32
extents**. This conclusively identifies SD FAT32 fragmentation as the chooser
`FF` cause for R0-E3.

The retained historical R0-E carrier was then measured on the same mounted
card: `A. MegaWing/F65R0E.D81`, with its expected SHA-256, occupies exactly one
819,200-byte FAT32 extent and passed the extent gate. This control clears an
SD-card-wide defect and MEGA65 hardware as explanations. The correction is a
per-artifact transfer/allocation gate, not reformatting or other card-wide work.

## Corrective action

The repository gate now adds distinct `SD_COPY_VERIFIED` and
`SD_CONTIGUITY_VERIFIED` states. Direct-card releases must use a non-D81 staging
name, verify source/copy hashes, require exactly one physical extent, rename in
place, re-verify, and safely eject. Plain `cp` + `sync` + `shasum` no longer
authorizes physical chooser testing.

The retained same-card control is now verified. No R0-E4 carrier may be copied
until its own direct-to-card transfer passes source/copy hashing, one-extent
verification before and after rename, and safe ejection. The five-extent result
applies to R0-E3 only; it does not diagnose a card-wide or hardware failure.
