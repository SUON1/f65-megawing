# R0-D Evidence Map

Status: **D81 correction in coding.** `F65R0D.D81` is invalid after chooser
`ERROR CODE FF`; replacement `F65R0D2.D81` is `HOST_CONTENT_VERIFIED` only.

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

`F65R0D.D81` is **INVALID — DO NOT USE** after physical chooser `ERROR CODE
FF`; its transfer hash was not captured. `F65R0D2.D81` is 819,200 bytes, disk
`F65 R0-D` ID `65`, SHA-256
`51dd4ad5a0fe402eccbac81b1ec0e44d12f5ab2294a9f01b1e7452711fa52643`, and is
**HOST_CONTENT_VERIFIED**. It has distinct filename/header identity and must
restart publication and Xemu gates. Do not copy or mount it yet.

Xemu used the pinned `20260129235930` build and ROM SHA-256
`af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0`.
Two clean PRG boots of source commit `c5a12d9` produced the same screen SHA-256
`cd424a2b51109d891a3c3388f0da114042462ddab43f543d912bcdff41e8bcf2` and
result-block SHA-256
`24f8e8dac28e79d9615bbae9fb58b716e92cf55b515e66483769721cf14587f7`.
