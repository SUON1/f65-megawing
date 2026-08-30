# R0-D Evidence Map

Status: **Xemu evidence complete; physical testing is not authorized.**

| Test ID | Host | Target build | Xemu | Physical | Scope |
|---|---|---|---|---|---|
| R0D-FIX-001 | PASS | fixture identity only | PASS | Not run | 530,000-clock historical comparison fixture |
| R0D-TICK-001 | PASS | static/observable | PASS | Not run | 100 Hz, 21-stage and stage-16 next-tick contract |
| R0D-CLK-001 | PASS | result block | PASS | Not run | protected/rolling-clock counters |
| R0D-WORLD-001 | PASS | result block | PASS | Not run | generation/source/world-age counters |
| R0D-RENDER-001 | PASS | result block | PASS | Not run | non-render pool/DMA high-water counters |
| R0D-AUDIO-001 | PASS | result block | PASS | Not run | service, channel and P0/P1 counters |
| R0D-SNAP-001 | PASS | result block | PASS | Not run | extraction/publication/lag/drop/ownership |
| R0D-IO-001 | PASS | result block | PASS | Not run | DMA/input/storage timing counters |
| R0D-AI-001 | PASS | result block | PASS | Not run | stage-16 owner/held-intent/causality hooks |
| R0D-MEM-001 | PASS | PASS | PASS | Not run | reserve remains zero; map accounting is retained |
| R0D-TARGET-STATIC-001 | PASS | PASS | PASS | Not run | forbidden-range/operation static guard |

No D81 is emitted in Stage 1, so D81 state is **NOT APPLICABLE**. A future
candidate must start at `UNVERIFIED` and pass the complete loadability gate.

Xemu used the pinned `20260129235930` build and ROM SHA-256
`af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0`.
Two clean PRG boots of source commit `c5a12d9` produced the same screen SHA-256
`cd424a2b51109d891a3c3388f0da114042462ddab43f543d912bcdff41e8bcf2` and
result-block SHA-256
`24f8e8dac28e79d9615bbae9fb58b716e92cf55b515e66483769721cf14587f7`.
