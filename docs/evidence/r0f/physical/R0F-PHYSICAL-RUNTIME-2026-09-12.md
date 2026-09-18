# R0-F Physical Runtime Evidence — 2026-09-12

```text
EVIDENCE_STATE: OWNER_REPORTED_HARDWARE_RUNTIME_OBSERVED
D81_FILENAME: F65R0F1.D81
D81_SHA256: 9b539a14f08d671195ef71e54bbacb3eacd5258634f7a29396bf00a068cddd89
D81_BYTES: 819200
DISK_LABEL: F65 R0-F1
DISK_ID: 65
ENTRY_FILENAME: AUTOBOOT.C65 -> R0F-PROOF
SOURCE_BRANCH: codex/r0-f-development
SOURCE_COMMIT: 744920d
HOST_STRUCTURAL_RESULT: PASS
HOST_CONTENT_RESULT: PASS
XEMU_RESULT: PASS (exact same D81 bytes, two clean boots)
SD_COPY_SHA256: 9b539a14f08d671195ef71e54bbacb3eacd5258634f7a29396bf00a068cddd89
SD_TRANSFER_METHOD: MEGA65-created contiguous root slot with guarded in-place fill
SD_PRE_TRANSFER_JSON: build/d81-sd-transfer/F65R0F1.D81.slot-pre.json
SD_POST_TRANSFER_JSON: build/d81-sd-transfer/F65R0F1.D81.slot-post.json
SD_CONTIGUITY_RESULT: PASS
SD_EXTENT_COUNT: 1
SD_SAFE_EJECT_RESULT: PASS
PHYSICAL_CHOOSER_RESULT: OWNER_REPORTED_PASS
PHYSICAL_RUNTIME_RESULT: OWNER_REPORTED_PASS
PHYSICAL_EVIDENCE: user-provided photo attachment (conversation artifact only; not currently stored in repo path)
PHYSICAL_EVIDENCE_SHA256: unavailable_local
```

The owner reported loading and running `F65R0F1.D81` on MEGA65 hardware after SD
transfer. The captured runtime text included:

- `R0-F COMBINED-LOAD FUNCTIONAL PROXY`
- `UNPACED 100HZ / 21-STAGE MODEL: FUNCTIONAL PASS`
- `SNAPSHOT: SYNCHRONOUS HANDOFF PROXY ONLY`
- `NORMAL / LAG / SHED / SYNTHETIC FAULT / PRESSURE`
- `INPUT/AUDIO ARE TARGET PROXIES; NO LATENCY CLAIM`
- `16 BINS/CASE, 33-TICK WINDOW; $1900-$19FF R0F1 REV1`
- `RASTER ACQUISITION: ALL 80 SAMPLES VALID`
- `IRQ: NOT MEASURED. NO REAL INPUT/AUDIO LATENCY.`
- `DMA: HARDWARE PROBE NOT EXECUTED`
- `RAW MOD256 BYTES IN PHASE ORDER; WRAPS UNRESOLVED`

## Evaluation

This is an owner-reported hardware pass for the bounded functional-proxy runtime
screen and confirms that the exact carrier can be mounted and run in this phase.
It does not close R0-F measured-limits obligations and does not replace missing
DMA, IRQ, timing, audio/input latency, or full platform-identity measurements.
