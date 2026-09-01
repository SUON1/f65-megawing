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

## Current D81 candidate and later gates

`F65R0D.D81` and `F65R0D2.D81` are **INVALID — DO NOT USE** after physical
chooser `ERROR CODE FF`. Do not copy, mount, rename, or retry either image.

The corrected fresh candidate is `build/r0d/artifacts/F65R0D3.D81`, SHA-256
`107c6a356b932e9ade875c24539d75b1b0a0078122a6a3910f524570aafec5ef`. It was
formatted once as `F65 R0-D3`, ID `65`, with `AUTOBOOT.C65` and `R0D-CALIB`
written in that same c1541 session. Structural and extraction/hash gates pass;
its present state is `HOST_CONTENT_VERIFIED` only.

D3 is now `XEMU_BOOT_VERIFIED` from two clean drive-8 AUTOBOOT runs. Physical
MEGA65 work still requires separate explicit authorization.

## Stage 4 — physical-MEGA65 procedure

Use only `F65R0D3.D81`, unchanged, SHA-256
`107c6a356b932e9ade875c24539d75b1b0a0078122a6a3910f524570aafec5ef`.

1. Copy it to the MEGA65 SD volume under the exact same filename, flush writes,
   and hash the copied file. Stop if its hash differs.
2. In the MEGA65 chooser, select exactly `F65R0D3.D81`. A chooser `ERROR CODE
   FF` permanently invalidates this D3 identity; photograph it and do not try
   to repair, rename, or reuse the image.
3. On chooser success, photograph the readable directory showing `AUTOBOOT.C65`
   and `R0D-CALIB`, then load the entry and capture the calibration screen.
4. Confirm the screen begins `R0-D PROTECTED-WORKLOAD CALIBRATION CANDIDATE`.

Only the successful chooser-directory check promotes D3 to
`PHYSICAL_CHOOSER_VERIFIED`. Only then may functional hardware testing begin;
it is not `TEST_ELIGIBLE` beforehand.

The owner returned the exact SD-copy SHA-256 and the physical directory plus
calibration photos. D3 is `TEST_ELIGIBLE` for its admitted R0-D proof scope;
that result does not replace R0-F or authorize later production phases.

The historical 530,000-clock fixture is not a production deadline or
measured-limit selection.
