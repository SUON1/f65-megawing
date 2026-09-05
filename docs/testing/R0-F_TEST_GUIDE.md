# R0-F Test Guide

R0-F is a bounded physical-MEGA65 evidence phase corresponding to the accepted
R0-E functional-proxy configuration. It is not production gameplay, a
measured-limits decision, or Phase 1 authorization.

## Preconditions

1. Review the R0-F admission, ownership, execution plan, interface/ledger
   impact, and stage control records.
2. Preserve the R0-E non-claims and identify the exact R0-E source/configuration
   being rebuilt; never use `F65R0EG.D81` or another D81 as a template.
3. Pin and record physical platform identity before measurement: MEGA65
   model/revision/serial or board identity where available, core, ROM, HYPPO,
   Freezer/SD Essentials, video/output/mode, clock, storage/media, input, and
   capture-tool identity.
4. Do not run physical functional testing before a new R0-F carrier reaches
   `PHYSICAL_CHOOSER_VERIFIED`.

## D81 procedure

Use a new, unique uppercase FAT 8.3 filename absent from the system card.
Fresh-format the D81 and write all source-built payloads in one pinned
`toolchain/vice-clean/bin/c1541` session. Require 819,200 bytes; independent
geometry/BAM/directory/chain/ownership/free-block validation; and
source-versus-extracted payload hashes.

Run two clean Xemu boots of exactly those bytes and that filename using pinned
Xemu/ROM identity. Retain screen, result-block, and artifact hashes. If Xemu is
unavailable, report `NOT VERIFIED` and do not transfer the image to hardware.

On the MEGA65 system card, the owner creates a fresh matching root slot with
`NEW D81 DD IMAGE`. After safe power-down and card movement, run only:

```sh
sudo tools/diagnostics/d81_sd_fill_mega65_slot.sh SOURCE.D81 /Volumes/MEGA65FDISK EXPECTED_SHA256
```

The helper must report the exact final hash, one raw FAT32 extent before and
after its in-place write at the same offset/length, and safe eject. Do not use
Finder, `cp`, a blank/reformatted system card, or an existing tested slot.

At the chooser, select the exact recorded filename, confirm a readable
directory and stable identity banner, and retain a photo. `ERROR CODE FF` is
a chooser/attach-stage failure: retire that tested copy, preserve its identity,
inspect its exact bytes, allocation, safe-eject record, and platform identity,
and do not patch, rename, append to, or retry it. `FF` itself is not proof of
fragmentation; current Freezer source maps `0x8B` to `IMAGE FRAGMENTED`.

## Runtime evidence

The admitted implementation must report mechanism, units, calibration, wrap
handling, sample count, phase-bin coverage, result encoding, and physical
capture for the independent 100 Hz simulation/display phase sweep. Retain
rolling-window/deadline evidence plus input/audio latency, snapshot ownership
and high-water, deterministic fault/shedding, reserve, and storage
inactivity/behavior results.

No threshold is a pass criterion unless an approved source defines it. Otherwise
record the observation for owner measured-limits review. Until a platform
wrapper is separately admitted and executed, report
`DMA_HARDWARE_PROBE_NOT_EXECUTED` and `IRQ_MEASUREMENT_NOT_EXECUTED`.

## Current test state

The first bounded proxy is implemented. Run `sh tools/build/r0f.sh host-test`
for native C sanitizer checks, including five functional cases and phase-timeout
injection; `build` compiles the target and emits map/symbols/disassembly.
`package` fresh-builds the uniquely assigned F65R0F1.D81 and automatically runs
independent structural plus extracted-content checks. It refuses an existing
filename; do not delete an image to bypass that refusal. `xemu` requires the
pinned emulator, owner ROM (`F65_MEGA65_ROM`), and initialized emulator SD image
(`F65_MEGA65_SD_IMAGE`), and runs two fresh processes with disposable SD copies.

Native checks, target build and D81 host gates passed on 2026-09-05. Two clean Xemu boots subsequently passed using the owner's located runtime.
The exact carrier may proceed to the gated native-slot SD transfer workflow;
no plain copy and no physical testing before the remaining gates.
The full physical measurement program remains pending. Exact evidence and
limitations: `docs/reports/R0-F_BUILD_HANDOFF.md`.
