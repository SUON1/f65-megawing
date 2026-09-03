# R0-E Evidence Map

Status: **The historical carrier is `TEST_ELIGIBLE` for its bounded physical
functional-proxy scope. The R0-E2 and R0-E3 raster-observation carriers failed
the physical chooser with `ERROR CODE FF` and are invalid. R0-E3 disproved the
disk-ID hypothesis. The release gate omitted mandatory SD FAT32 contiguity;
R0-E3 was measured at five extents. The retained successful R0-E carrier
measured at one extent on the same card, clearing card-wide and hardware
causes. `F65R0E4.D81` is admitted as a new candidate and may proceed only
through the corrected per-artifact transfer gate.
R0-F timing/measurement remains required.**

| Test ID | Host | Target static | Xemu | Physical | Scope |
|---|---|---|---|---|---|
| R0E-TICK-001 | PASS | PASS | PASS — functional proxy | PASS — banner proxy | 100 Hz, 21-stage model; no timing measurement |
| R0E-SNAP-001 | PASS | contract/static | PASS — functional proxy | PASS — banner proxy | forced lag, complete snapshot ownership, no checksum change |
| R0E-RENDER-001 | PASS | contract/static | PASS — functional proxy | PASS — banner proxy | exact presentation-only shedding ladder |
| R0E-INPUT-001 | PASS | contract/static | PASS — target pressure proxy | PASS — banner proxy | scripted proxy edge pressure; no latency measurement |
| R0E-AUDIO-001 | PASS | contract/static | PASS — target pressure proxy | PASS — banner proxy | priority-0 service proxy; no latency measurement |
| R0E-RASTER-001 | PASS | PASS | PASS — R0-E2/R0-E3 | blocked — both carriers rejected | 16 requested raster-low-byte phase bins/case; 33-tick window; raw modulo-256 line delta only |
| R0E-FAULT-001 | PASS | contract/static | PASS — functional proxy | PASS — banner proxy | deterministic queue/pool/effect one-over fixture |
| R0E-DMA-001 | `DMA_HARDWARE_PROBE_NOT_EXECUTED` | PASS | `DMA_HARDWARE_PROBE_NOT_EXECUTED` | R0-F if admitted | no fabricated DMA result |
| R0E-STORAGE-001 | PASS | PASS | PASS — no storage service invoked | PASS — banner proxy | storage inactive during active proof timeline |
| R0E-D81-STRUCT-001 | PASS — R0-E2/R0-E3 | PASS | not applicable | FAIL — `ERROR CODE FF` | 819,200-byte geometry, BAM, chain, ownership validation did not establish SD-file contiguity |
| R0E-D81-CONTENT-001 | PASS — R0-E2/R0-E3 | PASS | unchanged SHA-256 verified | FAIL — no readable chooser directory | matching logical bytes do not establish contiguous FAT32 allocation |
| R0E-SD-CONTIG-001 | omitted by prior gate | new host extent inspector | R0-E3: 5 extents; retained F65R0E control: 1 extent | R0-E3 FAIL — chooser `ERROR CODE FF`; control PASS | exactly one physical extent is mandatory before chooser testing |

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
