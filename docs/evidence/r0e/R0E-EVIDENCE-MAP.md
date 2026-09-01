# R0-E Evidence Map

Status: **Stage 1 source/host validation complete; Xemu is not authorized or executed.**

| Test ID | Host | Target static | Xemu | Physical | Scope |
|---|---|---|---|---|---|
| R0E-TICK-001 | PASS | PASS | AWAITING STAGE 3 | R0-F | 100 Hz, 21-stage, independent clocks |
| R0E-SNAP-001 | PASS | contract/static | AWAITING STAGE 3 | R0-F | forced lag, complete snapshot ownership, no checksum change |
| R0E-RENDER-001 | PASS | contract/static | AWAITING STAGE 3 | R0-F | exact presentation-only shedding ladder |
| R0E-INPUT-001 | PASS | contract/static | AWAITING STAGE 3 | R0-F | scripted legal edge preservation |
| R0E-AUDIO-001 | PASS | contract/static | AWAITING STAGE 3 | R0-F | priority-0 service opportunity under proxy load |
| R0E-FAULT-001 | PASS | contract/static | AWAITING STAGE 3 | R0-F | deterministic queue/pool/effect one-over fixture |
| R0E-DMA-001 | `DMA_HARDWARE_PROBE_NOT_EXECUTED` | PASS | AWAITING admitted wrapper | R0-F if admitted | no fabricated DMA result |
| R0E-STORAGE-001 | PASS | PASS | AWAITING STAGE 3 | R0-F | storage inactive during active proof timeline |
| R0E-D81-STRUCT-001 | PASS | PASS | not applicable | R0-F chooser | 819,200-byte geometry, BAM, chain, ownership validation |
| R0E-D81-CONTENT-001 | PASS | PASS | recheck required after Stage 3 | R0-F chooser | pinned extraction and payload hashes |

Stage 1 candidate: `F65R0E.D81`, SHA-256
`612a7bf0877132677e40ba75b15458cfa9160618b79200be300242ea222ee138`, disk
`F65 R0-E`/ID `65`, entry `AUTOBOOT.C65 -> R0E-PROOF`. Its state is
`HOST_CONTENT_VERIFIED`, not Xemu-verified, final, physical-verified, or test-eligible.

The host oracle exercised 1,000 proof ticks per case. Forced lag produced 798
deterministic skipped publications with unchanged checksum `393387319`; this
is host-proxy evidence, not a measured platform limit. No Xemu command has run.
