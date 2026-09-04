# R0-E5 Physical Runtime Evidence — 2026-09-04

```text
EVIDENCE_STATE: OWNER_ACCEPTED_BOUNDED_R0E_CLOSURE
D81_FILENAME: F65R0EG.D81
D81_SHA256: ca85f73ffba93ea290078a60b372406dc6ab58eddacdf0765f7589cea039c40f
D81_BYTES: 819200
DISK_LABEL: F65 R0-E
DISK_ID: 65
ENTRY_FILENAME: AUTOBOOT.C65 -> R0E-PROOF
SOURCE_BRANCH: codex/r0-e-development
SOURCE_COMMIT: 2559e18
HOST_STRUCTURAL_RESULT: PASS
HOST_CONTENT_RESULT: PASS
XEMU_RESULT: NOT RERUN FOR REV3 CARRIER
SD_COPY_SHA256: ca85f73ffba93ea290078a60b372406dc6ab58eddacdf0765f7589cea039c40f
SD_TRANSFER_METHOD: MEGA65-created contiguous root slot; guarded in-place fill
SD_CONTIGUITY_RESULT: PASS
SD_EXTENT_COUNT: 1
SD_SAFE_EJECT_RESULT: PASS
PHYSICAL_CHOOSER_RESULT: PASS
PHYSICAL_RUNTIME_RESULT: PASS
PHYSICAL_EVIDENCE: physical/F65R0EG-PHYSICAL-RUNTIME-2026-09-04.jpg
PHYSICAL_EVIDENCE_SHA256: ab813983ba1b8e4a01446648d922590c115fde0ef31f9aa5ebc5f2a87ce81087
```

The owner mounted and loaded `F65R0EG.D81` on the MEGA65. The captured result
screen identifies `R0E1 REV3` at `$1900-$19FF` and reports:

- 100 Hz / 21-stage model: `FUNCTIONAL PASS`.
- Snapshot ownership `FREE/PUB/READY/READ`: `PASS`.
- Normal, lag, shedding, one-over, and pressure cases: `PASS`.
- Raster phase observation: 16 bins per case, 33-tick window, raw raster-line
  delta modulo 256; normal raw q50/q95/max bytes `020/020/020`.

The screen also explicitly preserves the proof boundaries: input/audio are
target proxies with no latency claim; DMA hardware probe was not executed; the
raster value is not CPU cycles, latency, or a physical-limit result.

## Evaluation

The owner accepted this as closure of the bounded R0-E combined-load
functional-proxy and read-only raster-observation proof. It is not R0-F
closure, a measured-limits decision, a DMA or IRQ measurement, a pinned
platform-matrix result, or authorization for production implementation.

The exact Rev3 carrier was not rerun through Xemu because the pinned owner ROM
and Xemu environment were unavailable in this worktree. Therefore this record
does not relabel the D81 `TEST_ELIGIBLE` under the full D81 state machine; it
records the stronger physical runtime observation and the owner-directed
bounded R0-E closure without fabricating the missing Xemu gate.
