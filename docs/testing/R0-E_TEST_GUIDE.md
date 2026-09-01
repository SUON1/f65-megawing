# R0-E Test Guide

Stage 1 runs host and target-static validation only. It must not run Xemu.

The candidate carrier is `F65R0E.D81`, label `F65 R0-E`, ID `65`, with `AUTOBOOT.C65 -> R0E-PROOF`. Before any later Xemu run, compare the published source commit, D81 SHA-256, payload hashes, c1541 identity, Xemu identity, and ROM identity. Run normal, forced lag, shedding, one-over queue/pool/effect, input pressure, priority-0 audio pressure, storage-inactive, and any admitted DMA/IRQ cases. DMA is currently `DMA_HARDWARE_PROBE_NOT_EXECUTED`.

R0-F, not R0-E, performs SD copy plus `sync`, copied-file hashing, physical chooser selection, and captures. A chooser `ERROR CODE FF` invalidates the carrier before program execution.
