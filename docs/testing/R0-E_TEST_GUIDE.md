# R0-E Test Guide

Stage 1 runs host and target-static validation only. The source must be
committed and published under the stage-control procedure before `xemu` is run.

R0-E is closed for its owner-accepted bounded combined-load functional-proxy
and read-only raster-observation scope. `F65R0EG.D81`, SHA-256
`ca85f73ffba93ea290078a60b372406dc6ab58eddacdf0765f7589cea039c40f`, passed
the MEGA65 physical chooser and loaded the Rev3 result screen after a verified
one-extent SD delivery. `F65R0E2.D81`, `F65R0E3.D81`, `F65R0E4.D81`, and
`F65R0EF.D81` remain failed identities; do not copy, rename, or retest them.
DMA remains `DMA_HARDWARE_PROBE_NOT_EXECUTED`.

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

For R0-F and later carrier work, use the MEGA65-native slot procedure in
`docs/reports/D81_MEGA65_NATIVE_SLOT_DELIVERY_2026-09-03.md`: create a unique
matching `NEW D81 DD IMAGE` slot on the MEGA65, then fill it in place with
`d81_sd_fill_mega65_slot.sh`. Do not use Finder or a normal host copy to create
or replace the D81 file. A chooser `ERROR CODE FF` invalidates that tested copy
before program execution. A source or payload change creates a new D81 identity
and repeats the complete D81 chain.
