# R0-E Evidence Map

Status: **R0-E is closed for the owner-accepted bounded combined-load
functional-proxy and read-only raster-observation scope. `F65R0EG.D81` passed
the physical chooser and loaded its Rev3 result screen after an exact-hash,
one-extent FAT32 transfer. R0-E2, R0-E3, R0-E4, and R0-EF are retired failed
delivery identities. The successful delivery method is a MEGA65-created,
contiguous root slot filled in place; it preserves the system card and its FAT
chain. R0-F timing/DMA/IRQ measurement and platform identity remain separate.**

| Test ID | Host | Target static | Xemu | Physical | Scope |
|---|---|---|---|---|---|
| R0E-TICK-001 | PASS | PASS | PASS — functional proxy | PASS — banner proxy | 100 Hz, 21-stage model; no timing measurement |
| R0E-SNAP-001 | PASS | contract/static | PASS — functional proxy | PASS — banner proxy | forced lag, complete snapshot ownership, no checksum change |
| R0E-RENDER-001 | PASS | contract/static | PASS — functional proxy | PASS — banner proxy | exact presentation-only shedding ladder |
| R0E-INPUT-001 | PASS | contract/static | PASS — target pressure proxy | PASS — banner proxy | scripted proxy edge pressure; no latency measurement |
| R0E-AUDIO-001 | PASS | contract/static | PASS — target pressure proxy | PASS — banner proxy | priority-0 service proxy; no latency measurement |
| R0E-RASTER-001 | PASS | PASS | PASS — host raster observation | PASS — Rev3 result screen | 16 bins/case; 33-tick window; normal raw q50/q95/max bytes 020/020/020; raw modulo-256 line delta only |
| R0E-FAULT-001 | PASS | contract/static | PASS — functional proxy | PASS — banner proxy | deterministic queue/pool/effect one-over fixture |
| R0E-DMA-001 | `DMA_HARDWARE_PROBE_NOT_EXECUTED` | PASS | `DMA_HARDWARE_PROBE_NOT_EXECUTED` | R0-F if admitted | no fabricated DMA result |
| R0E-STORAGE-001 | PASS | PASS | PASS — no storage service invoked | PASS — banner proxy | storage inactive during active proof timeline |
| R0E-D81-STRUCT-001 | PASS — F65R0EG | PASS | not rerun for Rev3 carrier | PASS — mounted and loaded | fresh 819,200-byte D81, structural/content readback; physical runtime photo retained |
| R0E-D81-CONTENT-001 | PASS — F65R0EG | PASS | not rerun for Rev3 carrier | PASS — exact SD hash and runtime banner | matching logical bytes plus one extent established the accepted carrier route |
| R0E-SD-CONTIG-001 | MEGA65 slot allocator | raw FAT32 inspector | F65R0EG: one extent before and after fill | PASS — chooser mount and runtime | exact 819,200-byte one extent at device offset 103182336; safe eject PASS |

`F65R0E.D81` remains the retained historical physical-pass control. The
accepted Rev3 physical carrier is `F65R0EG.D81`, SHA-256
`ca85f73ffba93ea290078a60b372406dc6ab58eddacdf0765f7589cea039c40f`, source
commit `2559e18`. Its one-extent transfer, safe eject, chooser mount, and
runtime screen are recorded in `R0E5-D81-PHYSICAL-RUNTIME-2026-09-04.md`.
The historical Xemu carrier produced the same screen SHA-256
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

The Rev3 physical screen observes only a read-only VIC-II-compatible raster
low-byte delta through the LLVM-MOS header. Its q50/q95/maximum fields rank raw
bytes only and are not elapsed-time p50/p95/worst results. It is not a
CPU-cycle, latency, DMA, IRQ, or measured-limit result. Future D81 work must
use the retained MEGA65-native slot procedure and pass the complete fail-closed
chain again.
