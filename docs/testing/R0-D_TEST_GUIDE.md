# R0-D Test Guide

Stage 1 runs host generation, deterministic fixture tests, static target checks,
and a target build with map, symbols, and disassembly. The required host IDs
are `R0D-FIX-001`, `R0D-TICK-001`, `R0D-CLK-001`, `R0D-WORLD-001`,
`R0D-RENDER-001`, `R0D-AUDIO-001`, `R0D-SNAP-001`, `R0D-IO-001`,
`R0D-AI-001`, `R0D-MEM-001`, and `R0D-TARGET-STATIC-001`.

No Xemu command may be run in Stage 1. R0-D is delivered as a D81 containing
the PRG. Its builder fresh-formats the image and writes all payloads in one
pinned `c1541` session, then requires independent structural and content
validation before it can be mounted.

## Stage 4 — physical-MEGA65 procedure

Status: **STOP — both R0-D D81 identities are invalid after physical chooser
`ERROR CODE FF`.** D2 completed publication, two-clean-boot Xemu, and an exact
SD-copy hash check before its chooser failure. Do not copy, mount, rename, or
retry either R0-D image.

`F65R0D.D81` and `F65R0D2.D81` are **INVALID — DO NOT USE**. There is no
current R0-D physical candidate or functional test procedure.

## Required non-destructive diagnostic control

Do not construct or test another R0-D D81. On the same SD card and in the same
chooser workflow, use the retained known-good `F65-R0C-MEDIA.D81` only after
its copied-file hash is verified as
`e01eb41cff0158e7b609a365ecc72b78b3ce825ddca06a42a32f8954f4c7e8d0`.

1. Run `shasum -a 256 "/Volumes/MEGA65FDISK/F65-R0C-MEDIA.D81"`. If the file
   is absent or the hash differs, stop and report that result; do not select it.
2. In the same MEGA65 chooser/unit configuration that rejected D2, select that
   exact existing R0-C image and photograph the result. Do not alter the image
   or its directory.
3. If it mounts, photograph its readable directory or R0-C identity. If it
   displays `ERROR CODE FF`, photograph that failure. Do not run an R0-D
   program in either outcome.

A passing control isolates the failure to an as-yet-unidentified difference in
the R0-D carrier; a failing control shifts diagnosis to the current chooser,
unit/configuration, or SD environment. Either result is required before a new
R0-D construction change can be admitted.

No R0-D D81 is `XEMU_BOOT_VERIFIED`, `PHYSICAL_CHOOSER_VERIFIED`, or
`TEST_ELIGIBLE` for continued use. The historical 530,000-clock fixture is not
a production deadline or measured-limit selection.
