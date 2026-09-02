# R0-E Evidence Map

Status: **The historical carrier is `TEST_ELIGIBLE` for its bounded physical
functional-proxy scope. The R0-E2 raster-observation carrier failed the
physical chooser with `ERROR CODE FF` and is invalid. R0-E3 is a fresh,
unbuilt replacement using the physically proven numeric disk-ID convention.
R0-F timing/measurement remains required.**

| Test ID | Host | Target static | Xemu | Physical | Scope |
|---|---|---|---|---|---|
| R0E-TICK-001 | PASS | PASS | PASS — functional proxy | PASS — banner proxy | 100 Hz, 21-stage model; no timing measurement |
| R0E-SNAP-001 | PASS | contract/static | PASS — functional proxy | PASS — banner proxy | forced lag, complete snapshot ownership, no checksum change |
| R0E-RENDER-001 | PASS | contract/static | PASS — functional proxy | PASS — banner proxy | exact presentation-only shedding ladder |
| R0E-INPUT-001 | PASS | contract/static | PASS — target pressure proxy | PASS — banner proxy | scripted proxy edge pressure; no latency measurement |
| R0E-AUDIO-001 | PASS | contract/static | PASS — target pressure proxy | PASS — banner proxy | priority-0 service proxy; no latency measurement |
| R0E-RASTER-001 | PASS | PASS | PASS — R0-E2 only | blocked — R0-E2 carrier rejected | 16 requested raster-low-byte phase bins/case; 33-tick window; raw modulo-256 line delta only |
| R0E-FAULT-001 | PASS | contract/static | PASS — functional proxy | PASS — banner proxy | deterministic queue/pool/effect one-over fixture |
| R0E-DMA-001 | `DMA_HARDWARE_PROBE_NOT_EXECUTED` | PASS | `DMA_HARDWARE_PROBE_NOT_EXECUTED` | R0-F if admitted | no fabricated DMA result |
| R0E-STORAGE-001 | PASS | PASS | PASS — no storage service invoked | PASS — banner proxy | storage inactive during active proof timeline |
| R0E-D81-STRUCT-001 | PASS — R0-E2 | PASS | not applicable | FAIL — `ERROR CODE FF` | 819,200-byte geometry, BAM, chain, ownership validation did not establish physical chooser compatibility |
| R0E-D81-CONTENT-001 | PASS — R0-E2 | PASS | unchanged SHA-256 verified | FAIL — no readable chooser directory | pinned extraction and payload hashes did not establish physical chooser compatibility |

`F65R0E.D81` has SHA-256
`8cb76830489095a92a266c884e168efacfd6cb8e7d4db456300a3fbf67cc623b`, source
commit `ae2b0aee2ded09622c67fcea97062b45fd6ce9ce`, and state
`TEST_ELIGIBLE` for its bounded functional-proxy scope. Two clean Xemu boots produced the same screen SHA-256
`6df9b459ac895c7f787e5568a17aa75b8d6dc6e323cbedc3b728286cd9581e84` and
`$1900-$19FF` result-block SHA-256
`4bd6ed488108739cbab916035f557f1f7972ca3bd068fb082203a0e274cfadbf`.
Retained captures and machine-readable evidence are under `xemu/`.

The host oracle exercised 1,000 proof ticks per case. Forced lag produced 798
deterministic skipped publications with unchanged checksum `393387319`; this
is host-proxy evidence, not a measured platform limit. The historical exact SD copy hash,
physical chooser directory, and running banner prove carrier loadability and
the displayed functional proxy on the MEGA65. They do not create a timing,
DMA, IRQ, phase-sweep, pinned-platform, or measured-limit claim; see
`R0E-D81-PHYSICAL-RELEASE.md`.

The in-progress successor observes only a read-only VIC-II-compatible raster
low-byte delta through the LLVM-MOS header. Its q50/q95/maximum fields rank raw
bytes only and are not elapsed-time p50/p95/worst results. It is not a
CPU-cycle, latency, DMA, IRQ, physical-MEGA65, or measured-limit result. A rebuilt D81 has no
standing from the historical carrier and must pass the complete fail-closed D81
chain again.
