# R0-F Evidence Map

Status: **ADMITTED — NO R0-F EXECUTION OR PHYSICAL EVIDENCE YET.**

| Evidence ID | Required evidence | Current state | Non-claim / blocker |
|---|---|---|---|
| R0F-IDENTITY-001 | Complete pinned MEGA65/core/ROM/HYPPO/Freezer/video/clock/storage/input/capture identity | `AWAITING_PHYSICAL_CAPTURE` | No platform identity may be inferred from R0-E. |
| R0F-CONFIG-001 | Exact R0-E source/configuration reconstruction identity | `PLANNED` | R0-E source `2559e18`; Rev3 carrier is evidence only, never a template. |
| R0F-D81-STRUCT-001 | Fresh one-session R0-F D81 structural validation | `NOT VERIFIED` | No filename or carrier exists. |
| R0F-D81-CONTENT-001 | Source/extracted payload hashes | `NOT VERIFIED` | No payload set exists. |
| R0F-XEMU-001 | Two clean boots of exact R0-F filename/hash with pinned Xemu/ROM | `NOT VERIFIED` | R0-E Rev3 Xemu result cannot be inherited. |
| R0F-SD-001 | Exact SD-copy hash and safe eject | `NOT VERIFIED` | Requires owner/admin/card action. |
| R0F-SD-CONTIG-001 | One raw FAT32 extent before/after slot fill, same offset/length | `NOT VERIFIED` | Hash alone is insufficient. |
| R0F-CHOOSER-001 | Physical chooser directory and stable identity banner | `AWAITING HUMAN` | Must follow every prior D81 state. |
| R0F-PHASE-001 | Independent 100 Hz simulation/display phase sweep and rolling-window/deadline evidence | `NOT IMPLEMENTED` | No elapsed-time or limit claim. |
| R0F-INPUT-001 | Physical input-latency evidence | `NOT IMPLEMENTED` | R0-E proxy result is not latency evidence. |
| R0F-AUDIO-001 | Physical audio-latency/service evidence | `NOT IMPLEMENTED` | R0-E proxy result is not latency evidence. |
| R0F-SNAPSHOT-001 | Snapshot ownership, age, drops, and high-water evidence | `NOT IMPLEMENTED` | No production snapshot sizing is selected. |
| R0F-FAULT-001 | Deterministic faults, shedding, and reserve proof | `NOT IMPLEMENTED` | No reserve use is authorized. |
| R0F-STORAGE-001 | Storage inactivity/behavior evidence | `NOT IMPLEMENTED` | No production storage decision is selected. |
| R0F-DMA-001 | Separately admitted DMA wrapper and hardware observation | `DMA_HARDWARE_PROBE_NOT_EXECUTED` | No DMA behavior is inferred. |
| R0F-IRQ-001 | Separately admitted IRQ wrapper and hardware observation | `IRQ_MEASUREMENT_NOT_EXECUTED` | No IRQ behavior is inferred. |
| R0F-OWNER-001 | Owner review and explicit R0-F acceptance | `AWAITING HUMAN` | R0-F cannot be passed without it. |

All threshold-free evidence is observation-only for a later measured-limits
revision. This map does not freeze a value or open Phase 1.
