# R0-E Test Guide

Stage 1 runs host and target-static validation only. The source must be
committed and published under the stage-control procedure before `xemu` is run.

There is no current raster-observation carrier. `F65R0E2.D81` and `F65R0E3.D81` are invalid after physical chooser `ERROR CODE FF`; do not copy, rename, or retest them. R0-E3 disproved the disk-ID hypothesis. Its direct SD copy had matching bytes, but the prior gate omitted the MEGA65 requirement that a disk-image file occupy one contiguous FAT32 extent. `F65R0E.D81` remains historical functional-proxy evidence only. Do not create R0-E4 until the failed R0-E3 SD file has been inspected read-only with `tools/diagnostics/d81_sd_contiguity.py`. Every future direct-card transfer must use `tools/diagnostics/d81_sd_transfer.sh`, record a matching hash, one physical extent, and successful safe eject before the physical chooser. DMA remains `DMA_HARDWARE_PROBE_NOT_EXECUTED`.

`tools/build/r0e.sh xemu` requires the owner ROM, runs two clean Xemu boots of
the exact host-gated D81, and validates screen plus `$1900-$19FF` result data.
In addition to the functional proxy, it requires 16 read-only raster-low-byte
phase observations per case, each covering a 33-tick proxy window. Results are
raw raster-line deltas modulo 256: they are neither CPU cycles nor input/audio
latency, and they cannot exclude a 256-line wrap. The recorded q50/q95/maximum
fields rank raw byte values only; they are not elapsed-time p50/p95/worst
claims. Xemu validates the target
record only; it is not physical-MEGA65 timing evidence. DMA remains
`DMA_HARDWARE_PROBE_NOT_EXECUTED`.

R0-F, not R0-E, performs the gated SD transfer, copied-file hashing, physical
extent verification, safe eject, physical chooser selection, and captures. A
chooser `ERROR CODE FF` invalidates the carrier before program execution. A
source or payload change creates a new D81 identity; it must repeat the complete
D81 chain before any new physical observation.
