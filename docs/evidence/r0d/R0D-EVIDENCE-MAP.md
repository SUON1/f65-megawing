# R0-D Evidence Map

Status: **D3 Xemu gate PASS.** `F65R0D.D81` and `F65R0D2.D81` remain invalid
after chooser `ERROR CODE FF`. D3 is `XEMU_BOOT_VERIFIED`; physical chooser
verification is the next gate.

| Test ID | Host | Target build | Xemu | Physical | Scope |
|---|---|---|---|---|---|
| R0D-FIX-001 | PASS | fixture identity only | PASS — D3 two clean boots | Awaiting chooser | 530,000-clock historical comparison fixture |
| R0D-TICK-001 | PASS | static/observable | PASS — D3 two clean boots | Awaiting chooser | 100 Hz, 21-stage and stage-16 next-tick contract |
| R0D-CLK-001 | PASS | result block | PASS — D3 two clean boots | Awaiting chooser | protected/rolling-clock counters |
| R0D-WORLD-001 | PASS | result block | PASS — D3 two clean boots | Awaiting chooser | generation/source/world-age counters |
| R0D-RENDER-001 | PASS | result block | PASS — D3 two clean boots | Awaiting chooser | non-render pool/DMA high-water counters |
| R0D-AUDIO-001 | PASS | result block | PASS — D3 two clean boots | Awaiting chooser | service, channel and P0/P1 counters |
| R0D-SNAP-001 | PASS | result block | PASS — D3 two clean boots | Awaiting chooser | extraction/publication/lag/drop/ownership |
| R0D-IO-001 | PASS | result block | PASS — D3 two clean boots | Awaiting chooser | DMA/input/storage timing counters |
| R0D-AI-001 | PASS | result block | PASS — D3 two clean boots | Awaiting chooser | stage-16 owner/held-intent/causality hooks |
| R0D-MEM-001 | PASS | PASS | PASS — D3 two clean boots | Awaiting chooser | reserve remains zero; map accounting is retained |
| R0D-TARGET-STATIC-001 | PASS | PASS | PASS — D3 two clean boots | Awaiting chooser | forbidden-range/operation static guard |
| R0D-D81-STRUCT-001 | PASS — D3 | `HOST_STRUCTURALLY_VERIFIED` | PASS — D3 post-run recheck | Awaiting chooser | raw geometry, BAM, directory, chain, and ownership validation |
| R0D-D81-CONTENT-001 | PASS — D3 | `HOST_CONTENT_VERIFIED` | PASS — D3 post-run recheck | Awaiting chooser | c1541 extraction and payload SHA-256 validation |

`F65R0D.D81` is **INVALID — DO NOT USE** after physical chooser `ERROR CODE
FF`; its transfer hash was not captured. `F65R0D2.D81` is also **INVALID — DO
NOT USE** after physical chooser `ERROR CODE FF`; its copied SD-card SHA-256
matched `51dd4ad5a0fe402eccbac81b1ec0e44d12f5ab2294a9f01b1e7452711fa52643`.
Both artifacts are permanently retired. No R0-D physical function result is
claimed.

`F65R0D3.D81`, SHA-256
`107c6a356b932e9ade875c24539d75b1b0a0078122a6a3910f524570aafec5ef`, is a
fresh one-session D81 built with `toolchain/vice-clean/bin/c1541` SHA-256
`73235289aca30a7e2e8067e521bf604743156cc1d7499c888a3894d6e46fcb3c`.
Construction/listing/extraction all had zero stderr and no forbidden warning or
error markers. It awaits commit/publication, then explicit Xemu authorization.

Xemu used the pinned `20260129235930` build and ROM SHA-256
`af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0`.
Two clean PRG boots of source commit `c5a12d9` produced the same screen SHA-256
`cd424a2b51109d891a3c3388f0da114042462ddab43f543d912bcdff41e8bcf2` and
result-block SHA-256
`24f8e8dac28e79d9615bbae9fb58b716e92cf55b515e66483769721cf14587f7`.
