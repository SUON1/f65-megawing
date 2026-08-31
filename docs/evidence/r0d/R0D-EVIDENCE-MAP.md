# R0-D Evidence Map

Status: **D81 diagnostic hold.** `F65R0D.D81` and `F65R0D2.D81` are invalid
after chooser `ERROR CODE FF`. D2's SD-copy SHA-256 matched exactly; no third
R0-D image is authorized without a specific evidence-backed correction.

| Test ID | Host | Target build | Xemu | Physical | Scope |
|---|---|---|---|---|---|
| R0D-FIX-001 | PASS | fixture identity only | PASS — D2 two clean boots | Blocked — D2 carrier FF | 530,000-clock historical comparison fixture |
| R0D-TICK-001 | PASS | static/observable | PASS — D2 two clean boots | Blocked — D2 carrier FF | 100 Hz, 21-stage and stage-16 next-tick contract |
| R0D-CLK-001 | PASS | result block | PASS — D2 two clean boots | Blocked — D2 carrier FF | protected/rolling-clock counters |
| R0D-WORLD-001 | PASS | result block | PASS — D2 two clean boots | Blocked — D2 carrier FF | generation/source/world-age counters |
| R0D-RENDER-001 | PASS | result block | PASS — D2 two clean boots | Blocked — D2 carrier FF | non-render pool/DMA high-water counters |
| R0D-AUDIO-001 | PASS | result block | PASS — D2 two clean boots | Blocked — D2 carrier FF | service, channel and P0/P1 counters |
| R0D-SNAP-001 | PASS | result block | PASS — D2 two clean boots | Blocked — D2 carrier FF | extraction/publication/lag/drop/ownership |
| R0D-IO-001 | PASS | result block | PASS — D2 two clean boots | Blocked — D2 carrier FF | DMA/input/storage timing counters |
| R0D-AI-001 | PASS | result block | PASS — D2 two clean boots | Blocked — D2 carrier FF | stage-16 owner/held-intent/causality hooks |
| R0D-MEM-001 | PASS | PASS | PASS — D2 two clean boots | Blocked — D2 carrier FF | reserve remains zero; map accounting is retained |
| R0D-TARGET-STATIC-001 | PASS | PASS | PASS — D2 two clean boots | Blocked — D2 carrier FF | forbidden-range/operation static guard |
| R0D-D81-STRUCT-001 | PASS | `HOST_STRUCTURALLY_VERIFIED` | PASS — D2 | FAIL — chooser FF | raw geometry, BAM, directory, chain, and ownership validation |
| R0D-D81-CONTENT-001 | PASS | `HOST_CONTENT_VERIFIED` | PASS — D2 | FAIL — chooser FF | c1541 extraction and payload SHA-256 validation |

`F65R0D.D81` is **INVALID — DO NOT USE** after physical chooser `ERROR CODE
FF`; its transfer hash was not captured. `F65R0D2.D81` is also **INVALID — DO
NOT USE** after physical chooser `ERROR CODE FF`; its copied SD-card SHA-256
matched `51dd4ad5a0fe402eccbac81b1ec0e44d12f5ab2294a9f01b1e7452711fa52643`.
Both artifacts are permanently retired. No R0-D physical function result is
claimed.

Xemu used the pinned `20260129235930` build and ROM SHA-256
`af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0`.
Two clean PRG boots of source commit `c5a12d9` produced the same screen SHA-256
`cd424a2b51109d891a3c3388f0da114042462ddab43f543d912bcdff41e8bcf2` and
result-block SHA-256
`24f8e8dac28e79d9615bbae9fb58b716e92cf55b515e66483769721cf14587f7`.
