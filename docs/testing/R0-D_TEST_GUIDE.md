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

Status: **D81 XEMU_BOOT_VERIFIED; ready for SD-copy and physical chooser
verification.** The earlier direct-PRG route is superseded.

Use only `build/r0d/artifacts/F65R0D.D81`, 819,200 bytes, SHA-256
`a1d11bfb2b18a92618d55b5f3051a44d019adbdf2ba70b7c6715049567638d48`. It has
disk label `F65 R0-D 530K`, ID `D1`, and contains `AUTOBOOT.C65` plus
`R0D-CALIB` (the PRG SHA-256 is
`ad4827da70d6f4a571817df2268bb3ca4e88d11a0f8aacfc11441abca2fd1677`).

1. On the host, confirm the D81 SHA-256 above. Copy that exact filename to the
   SD card without changing its contents; record the path and transfer method.
   If possible, remount the SD card on the host and require an identical hash.
2. Record the MEGA65 model/revision, FPGA core version, ROM identity, video
   configuration, and SD-card identity. If the SD card can be mounted on the
   host afterward, re-hash the copied D81 and require the same SHA-256.
3. Mount the exact D81 on MEGA65 drive 8 using the established disk-image
   workflow. Confirm a readable directory and no chooser error. `ERROR CODE FF`
   invalidates this D81 identity before program execution; preserve the photo,
   stop, and do not patch or rename the image.
4. At the BASIC prompt, type `BOOT`. `AUTOBOOT.C65` loads `R0D-CALIB` from
   device 8. Photograph the complete result screen, including the title and all
   `R0D` lines.
5. Return the image/video plus mount result, hardware identity, copied-file
   hash, and observed behavior. A mount/loader failure or a screen that lacks
   the R0-D title is evidence to preserve, not a PASS.

Expected display identity: `R0-D PROTECTED-WORKLOAD CALIBRATION CANDIDATE`.
The hardware observation can confirm display and target behavior only; it does
not turn the historical 530,000-clock comparison fixture into a production
deadline or a measured-limit selection.

D81 state is **XEMU_BOOT_VERIFIED** only. It must proceed through SD-copy hash
verification and physical chooser PASS before it can become `TEST_ELIGIBLE`.
