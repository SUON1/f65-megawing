# R0-E Test Guide

Stage 1 runs host and target-static validation only. The source must be
committed and published under the stage-control procedure before `xemu` is run.

The raster-observation candidate carrier is `F65R0E3.D81`, label `F65 R0-E3`, ID `65`, with `AUTOBOOT.C65 -> R0E-PROOF`. `F65R0E2.D81` is invalid after a physical chooser `ERROR CODE FF`; do not copy, rename, or retest it. `F65R0E.D81` remains historical functional-proxy evidence only. Before any later Xemu run, compare the published source commit, D81 SHA-256, payload hashes, c1541 identity, Xemu identity, and ROM identity. Run normal, forced lag, shedding, one-over queue/pool/effect, input pressure, priority-0 audio pressure, storage-inactive, and any admitted DMA/IRQ cases. DMA is currently `DMA_HARDWARE_PROBE_NOT_EXECUTED`.

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

R0-F, not R0-E, performs SD copy plus `sync`, copied-file hashing, physical chooser selection, and captures. A chooser `ERROR CODE FF` invalidates the carrier before program execution. A source or payload change creates a new D81 identity; it must repeat the complete D81 chain before any new physical observation.
