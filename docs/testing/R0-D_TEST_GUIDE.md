# R0-D Test Guide

Stage 1 runs host generation, deterministic fixture tests, static target checks,
and a target build with map, symbols, and disassembly. The required host IDs
are `R0D-FIX-001`, `R0D-TICK-001`, `R0D-CLK-001`, `R0D-WORLD-001`,
`R0D-RENDER-001`, `R0D-AUDIO-001`, `R0D-SNAP-001`, `R0D-IO-001`,
`R0D-AI-001`, `R0D-MEM-001`, and `R0D-TARGET-STATIC-001`.

No Xemu command may be run in Stage 1. No R0-D D81 is required for this stage;
if later packaging creates one, it must be fresh-formatted and pass the full
repository D81 gate before mounting.

## Stage 4 — physical-MEGA65 procedure

Status: **AUTHORIZED; execution preflight blocked on the owner's already-proven
direct-PRG launch procedure.** Existing repository physical guides launch D81
carriers. R0-D has no D81, and this guide must not invent a MEGA65 loader
command or create a D81 workaround.

Use only `build/r0d/artifacts/F65-R0D-CALIBRATION.prg` with SHA-256
`ad4827da70d6f4a571817df2268bb3ca4e88d11a0f8aacfc11441abca2fd1677`. The
published evidence commit is `30549f061dea55b7d78291f7a9f62bdda9386bd8`; the
executable was built and Xemu-tested from `c5a12d936e07fa20e1ca43333042cb7a3fcaa57f`.

1. On the host, confirm the PRG SHA-256 above. Copy that exact file to the SD
   card without changing its contents; record the path and transfer method.
2. Record the MEGA65 model/revision, FPGA core version, ROM identity, video
   configuration, and SD-card identity. If the SD card can be mounted on the
   host afterward, re-hash the copied PRG and require the same SHA-256.
3. Provide the exact UI/tool/method that has already successfully launched a
   standalone PRG on this machine. Do not proceed on an assumed BASIC command,
   drive number, or launcher behavior.
4. Launch the exact copied PRG using that owner-proven method. Photograph or
   capture the complete result screen, including the title and all `R0D` lines.
5. Return the image/video plus the launch method, hardware identity, observed
   behavior, and copied-file hash. A blank screen, loader failure, or a screen
   that lacks the R0-D title is evidence to preserve, not a PASS.

Expected display identity: `R0-D PROTECTED-WORKLOAD CALIBRATION CANDIDATE`.
The hardware observation can confirm display and target behavior only; it does
not turn the historical 530,000-clock comparison fixture into a production
deadline or a measured-limit selection.

D81 loadability state is **NOT APPLICABLE**: no D81 is generated, copied,
mounted, or tested by R0-D. Consequently there is no chooser verification or
`TEST_ELIGIBLE` D81 claim for this phase.
