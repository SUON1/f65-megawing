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

Do not transfer or mount D3 yet. Stage 2 requires its source commit to be
published through VS Code. Stage 3 then requires explicit Xemu authorization
and two clean D3 boots. Only after published Xemu PASS may the physical guide be
used: copy the unchanged filename, hash the SD copy, select it in the chooser,
confirm a readable directory with no `ERROR CODE FF`, and capture the running
identity. The artifact is not `TEST_ELIGIBLE` until that physical chooser gate
passes.

The historical 530,000-clock fixture is not a production deadline or
measured-limit selection.
