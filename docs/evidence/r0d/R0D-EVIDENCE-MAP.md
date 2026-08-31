# R0-D Evidence Map

Status: **D81 Xemu boot verification complete; awaiting SD-copy and physical
chooser evidence.**

| Test ID | Host | Target build | Xemu | Physical | Scope |
|---|---|---|---|---|---|
| R0D-FIX-001 | PASS | fixture identity only | PASS — two clean D81 boots | Awaiting SD/chooser | 530,000-clock historical comparison fixture |
| R0D-TICK-001 | PASS | static/observable | PASS — two clean D81 boots | Awaiting SD/chooser | 100 Hz, 21-stage and stage-16 next-tick contract |
| R0D-CLK-001 | PASS | result block | PASS — two clean D81 boots | Awaiting SD/chooser | protected/rolling-clock counters |
| R0D-WORLD-001 | PASS | result block | PASS — two clean D81 boots | Awaiting SD/chooser | generation/source/world-age counters |
| R0D-RENDER-001 | PASS | result block | PASS — two clean D81 boots | Awaiting SD/chooser | non-render pool/DMA high-water counters |
| R0D-AUDIO-001 | PASS | result block | PASS — two clean D81 boots | Awaiting SD/chooser | service, channel and P0/P1 counters |
| R0D-SNAP-001 | PASS | result block | PASS — two clean D81 boots | Awaiting SD/chooser | extraction/publication/lag/drop/ownership |
| R0D-IO-001 | PASS | result block | PASS — two clean D81 boots | Awaiting SD/chooser | DMA/input/storage timing counters |
| R0D-AI-001 | PASS | result block | PASS — two clean D81 boots | Awaiting SD/chooser | stage-16 owner/held-intent/causality hooks |
| R0D-MEM-001 | PASS | PASS | PASS — two clean D81 boots | Awaiting SD/chooser | reserve remains zero; map accounting is retained |
| R0D-TARGET-STATIC-001 | PASS | PASS | PASS — two clean D81 boots | Awaiting SD/chooser | forbidden-range/operation static guard |
| R0D-D81-STRUCT-001 | PASS | `HOST_STRUCTURALLY_VERIFIED` | PASS | Awaiting physical chooser | raw geometry, BAM, directory, chain, and ownership validation |
| R0D-D81-CONTENT-001 | PASS | `HOST_CONTENT_VERIFIED` | PASS | Awaiting physical chooser | c1541 extraction and payload SHA-256 validation |

Candidate `F65R0D.D81` is 819,200 bytes, disk `F65 R0-D 530K` ID `D1`, and
SHA-256 `a1d11bfb2b18a92618d55b5f3051a44d019adbdf2ba70b7c6715049567638d48`.
It contains PETSCII-safe `AUTOBOOT.C65` and `R0D-CALIB`, created in one pinned
`c1541` format/write session. Its state is **XEMU_BOOT_VERIFIED**; it is a
candidate, not final or `TEST_ELIGIBLE`. Two clean D81 boots produced screen
SHA-256 `cd424a2b51109d891a3c3388f0da114042462ddab43f543d912bcdff41e8bcf2`
and result-block SHA-256
`24f8e8dac28e79d9615bbae9fb58b716e92cf55b515e66483769721cf14587f7`.
The failed D0 image SHA-256
`9bac7a0bc28b14618524be487fcd1aeee55dd6f78cb0312d0879401c20a6457f` is
invalid and must not be copied, mounted, or renamed.

Xemu used the pinned `20260129235930` build and ROM SHA-256
`af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0`.
Two clean PRG boots of source commit `c5a12d9` produced the same screen SHA-256
`cd424a2b51109d891a3c3388f0da114042462ddab43f543d912bcdff41e8bcf2` and
result-block SHA-256
`24f8e8dac28e79d9615bbae9fb58b716e92cf55b515e66483769721cf14587f7`.
