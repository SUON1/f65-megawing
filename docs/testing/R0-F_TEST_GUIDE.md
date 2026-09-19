# R0-F Test Guide

## Current combined experiment: CF001 / F65BLK02

Use `docs/reports/R0-F_COMBINED_HANDOFF.md` for the exact hash, actual gate state,
one-command guarded delivery and hardware checklist. The card has not been
written merely because the local D81 exists. CF001 combines reset-only ROM
recovery, nominal-clock comparison calibration, synthetic workload, rendering,
real DMA/IRQ/PCM/matrix edges and raw capture. Full R0-F acceptance remains open.
The combined release manifest is authoritative; previous instructions below
apply only to their historical variants.

Hardware sequence after verified fill/eject: mount F65BLK02, load R0F-PROOF,
RUN, tap/release A three times during the colored display, note audio, capture
summary and raw pages 01–0E, then reset. Do not press RESTORE while acquiring.
See the full handoff for fault/identity checks and instructions if chooser FF
appears. There are no runtime disk writes.

## Previous development test: PF001 (not for SD delivery)

The owner selected full R0 closure and approved additive platform development.
The earlier bounded-proxy procedure below is retained for its existing carriers;
it is not the full combined workload or a scope waiver.

```sh
python3 tools/diagnostics/r0f_platform_build.py build
python3 tools/diagnostics/r0f_platform_build.py xemu
```

These commands qualify the standalone platform development PRG: native
ASan/UBSan checks, pinned target build/static checks, then two normal-speed
direct-PRG Xemu boots and independent Java result validation. Do not add
`-sleepless`: the pinned Xemu advances PCM in its real-time SDL audio callback.
This is not exact-D81 loadability, physical audio evidence or calibrated timing.
Handoff and remaining integration dependencies: `docs/reports/R0-F_PLATFORM_HANDOFF.md`.
No physical test is requested for this primitive-only PRG.

For the eventual full combined carrier, use the existing native **F65BLK02.D81**
destination only after verifying blank contents, correct size and one physical
extent. The read-only observation of F65BLK01 was 688128 bytes, not a valid
819200-byte D81; do not overwrite or repair it. Fresh-format/populate the local
F65BLK02.D81 in one pinned c1541 session and test that exact filename/hash in
Xemu before in-place SD delivery. The native blank is a destination slot, never
a local construction template. Both blanks remain untouched.

CF001 delivery now independently verifies the exact untouched blank; the fill
helper compares pre/post device and extent objects before eject and rolls back
on a mismatch. Matching hashes, exactly one
extent and successful safe eject are still mandatory. The root D81 gate
supersedes any historical procedure below.

## Retained bounded-carrier scope

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

Current measurement build: **F65R0F4.D81** in `build/r0f/cia-timing-safe/`.
Use `F65_R0F_VARIANT=cia-timing sh tools/build/r0f.sh ACTION`, where ACTION is
`host-test`, `build`, `audit`, `package`, or `xemu`. Package refuses an existing
identity. See `docs/reports/R0-F_CIA_TIMING_HANDOFF.md` for actual run results and
the exact hash; the F1/F2 instructions below are historical.

This diagnostic takes exclusive CIA1 timer ownership and requires RESET after
completion. Do not press RESTORE/Freezer during acquisition. It stops timers
on completion/fault; does not return to BASIC. An acquisition-complete screen
does not mean deadlines passed or R0-F is accepted. All displayed measurements
are hexadecimal raw CIA counts. Capture the entire final screen and machine
identity; do not interpret counts as microseconds. No SD transfer was performed
for this build. Resolve the previously reported Finder/eject failure before
the next physical transfer; F2 safe eject is NOT VERIFIED.

Current successor (2026-09-17): F65R0F2.D81 under `build/r0f/startup-fix/`
has passed bounded static/host gates and two fresh Xemu boots after the startup
fix. See `docs/reports/R0-F_STARTUP_FIX_HANDOFF.md` for exact hash, command,
environment-retry record, and pending native-slot SD/hardware procedure. The
older Step 3 failure and F65R0F1 results below are retained as history.

Step 3 review (2026-09-16): run `sh tools/build/r0f.sh audit` for current native,
compile/link, ledger and startup checks. Expected current result is exit 2:
`R0F-STATIC-STARTUP-001`. Resolve the startup B/KERNAL contract conflict before
advancing to packaging. The existing carrier's prior two-boot Xemu, SD transfer,
and owner-reported hardware loading remain recorded observations; this audit
does not request another SD transfer. See `docs/reports/R0-F_STEP3_AUDIT.md`.

The first bounded proxy is implemented. Run `sh tools/build/r0f.sh host-test`
for native C sanitizer checks, including five functional cases and phase-timeout
injection; `build` compiles the target and emits map/symbols/disassembly.
`package` fresh-builds the uniquely assigned F65R0F1.D81 and automatically runs
independent structural plus extracted-content checks. It refuses an existing
filename; do not delete an image to bypass that refusal. `xemu` requires the
pinned emulator, owner ROM (`F65_MEGA65_ROM`), and initialized emulator SD image
(`F65_MEGA65_SD_IMAGE`), and runs two fresh processes with disposable SD copies.

Native checks, target build and D81 host gates passed on 2026-09-05. Two clean Xemu boots subsequently passed using the owner's located runtime.
That exact carrier subsequently passed the native-slot SD transfer workflow and
was owner-reported loaded on hardware. Step 3's startup finding blocks further
advancement; earlier loading is not complete platform-ABI verification.
The full physical measurement program remains pending. Exact evidence and
limitations: `docs/reports/R0-F_BUILD_HANDOFF.md`.
