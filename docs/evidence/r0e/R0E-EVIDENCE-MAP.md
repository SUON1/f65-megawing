# R0-E Evidence Map

Status: **The exact carrier is `TEST_ELIGIBLE` for its bounded physical
functional-proxy scope. R0-F timing/measurement evidence remains required.**

| Test ID | Host | Target static | Xemu | Physical | Scope |
|---|---|---|---|---|---|
| R0E-TICK-001 | PASS | PASS | PASS — functional proxy | PASS — banner proxy | 100 Hz, 21-stage model; no timing measurement |
| R0E-SNAP-001 | PASS | contract/static | PASS — functional proxy | PASS — banner proxy | forced lag, complete snapshot ownership, no checksum change |
| R0E-RENDER-001 | PASS | contract/static | PASS — functional proxy | PASS — banner proxy | exact presentation-only shedding ladder |
| R0E-INPUT-001 | PASS | contract/static | PASS — target pressure proxy | PASS — banner proxy | scripted proxy edge pressure; no latency measurement |
| R0E-AUDIO-001 | PASS | contract/static | PASS — target pressure proxy | PASS — banner proxy | priority-0 service proxy; no latency measurement |
| R0E-FAULT-001 | PASS | contract/static | PASS — functional proxy | PASS — banner proxy | deterministic queue/pool/effect one-over fixture |
| R0E-DMA-001 | `DMA_HARDWARE_PROBE_NOT_EXECUTED` | PASS | `DMA_HARDWARE_PROBE_NOT_EXECUTED` | R0-F if admitted | no fabricated DMA result |
| R0E-STORAGE-001 | PASS | PASS | PASS — no storage service invoked | PASS — banner proxy | storage inactive during active proof timeline |
| R0E-D81-STRUCT-001 | PASS | PASS | not applicable | PASS — exact SD hash and chooser | 819,200-byte geometry, BAM, chain, ownership validation |
| R0E-D81-CONTENT-001 | PASS | PASS | unchanged SHA-256 verified | PASS — readable chooser directory | pinned extraction and payload hashes |

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
is host-proxy evidence, not a measured platform limit. The exact SD copy hash,
physical chooser directory, and running banner prove carrier loadability and
the displayed functional proxy on the MEGA65. They do not create a timing,
DMA, IRQ, phase-sweep, pinned-platform, or measured-limit claim; see
`R0E-D81-PHYSICAL-RELEASE.md`.
