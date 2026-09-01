# R0-E Evidence Map

Status: **Stage 3 Xemu functional-proxy verification is complete for the published source. Physical R0-F evidence remains required.**

| Test ID | Host | Target static | Xemu | Physical | Scope |
|---|---|---|---|---|---|
| R0E-TICK-001 | PASS | PASS | PASS — functional proxy | R0-F | 100 Hz, 21-stage model; no timing measurement |
| R0E-SNAP-001 | PASS | contract/static | PASS — functional proxy | R0-F | forced lag, complete snapshot ownership, no checksum change |
| R0E-RENDER-001 | PASS | contract/static | PASS — functional proxy | R0-F | exact presentation-only shedding ladder |
| R0E-INPUT-001 | PASS | contract/static | PASS — target pressure proxy | R0-F | scripted proxy edge pressure; no latency measurement |
| R0E-AUDIO-001 | PASS | contract/static | PASS — target pressure proxy | R0-F | priority-0 service proxy; no latency measurement |
| R0E-FAULT-001 | PASS | contract/static | PASS — functional proxy | R0-F | deterministic queue/pool/effect one-over fixture |
| R0E-DMA-001 | `DMA_HARDWARE_PROBE_NOT_EXECUTED` | PASS | `DMA_HARDWARE_PROBE_NOT_EXECUTED` | R0-F if admitted | no fabricated DMA result |
| R0E-STORAGE-001 | PASS | PASS | PASS — no storage service invoked | R0-F | storage inactive during active proof timeline |
| R0E-D81-STRUCT-001 | PASS | PASS | not applicable | R0-F chooser | 819,200-byte geometry, BAM, chain, ownership validation |
| R0E-D81-CONTENT-001 | PASS | PASS | unchanged SHA-256 verified | R0-F chooser | pinned extraction and payload hashes |

Candidate `F65R0E.D81` has SHA-256
`8cb76830489095a92a266c884e168efacfd6cb8e7d4db456300a3fbf67cc623b`, source
commit `ae2b0aee2ded09622c67fcea97062b45fd6ce9ce`, and state
`XEMU_BOOT_VERIFIED`. Two clean Xemu boots produced the same screen SHA-256
`6df9b459ac895c7f787e5568a17aa75b8d6dc6e323cbedc3b728286cd9581e84` and
`$1900-$19FF` result-block SHA-256
`4bd6ed488108739cbab916035f557f1f7972ca3bd068fb082203a0e274cfadbf`.
Retained captures and machine-readable evidence are under `xemu/`.

The host oracle exercised 1,000 proof ticks per case. Forced lag produced 798
deterministic skipped publications with unchanged checksum `393387319`; this
is host-proxy evidence, not a measured platform limit. Xemu validates only the
functional proxy and carrier boot chain. It does not convert the result into a
timing, DMA, IRQ, physical chooser, or physical-hardware claim.
