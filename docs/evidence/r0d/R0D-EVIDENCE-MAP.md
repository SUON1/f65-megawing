# R0-D Evidence Map

Status: **Stage-1 host/build evidence pending final review.** No Xemu or
physical result is claimed.

| Test ID | Host | Target build | Xemu | Physical | Scope |
|---|---|---|---|---|---|
| R0D-FIX-001 | PASS | fixture identity only | Not run | Not run | 530,000-clock historical comparison fixture |
| R0D-TICK-001 | PASS | static/observable | Not run | Not run | 100 Hz, 21-stage and stage-16 next-tick contract |
| R0D-CLK-001 | PASS | result block | Not run | Not run | protected/rolling-clock counters |
| R0D-WORLD-001 | PASS | result block | Not run | Not run | generation/source/world-age counters |
| R0D-RENDER-001 | PASS | result block | Not run | Not run | non-render pool/DMA high-water counters |
| R0D-AUDIO-001 | PASS | result block | Not run | Not run | service, channel and P0/P1 counters |
| R0D-SNAP-001 | PASS | result block | Not run | Not run | extraction/publication/lag/drop/ownership |
| R0D-IO-001 | PASS | result block | Not run | Not run | DMA/input/storage timing counters |
| R0D-AI-001 | PASS | result block | Not run | Not run | stage-16 owner/held-intent/causality hooks |
| R0D-MEM-001 | PASS | PASS | Not run | Not run | reserve remains zero; map accounting is retained |
| R0D-TARGET-STATIC-001 | PASS | PASS | Not run | Not run | forbidden-range/operation static guard |

No D81 is emitted in Stage 1, so D81 state is **NOT APPLICABLE**. A future
candidate must start at `UNVERIFIED` and pass the complete loadability gate.
