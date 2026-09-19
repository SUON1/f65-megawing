# R0-B Stage 2 Evidence Harness — Build, Xemu, and Hardware Capture

Status: R0-B proof only. This harness does not select a production display
mode, renderer, control path, audio path, or gameplay implementation. A PASS
in this document is evidence for the named bounded fixture only; it is not
R0-B gate closure.

## Artifact and identity

The build emits `build/r0b/artifacts/F65-R0B-PROOF.d81` and its sibling PRG.
The matching SHA-256 files in that directory are the exact artifact identity.
The resident result block is at `$1800`, is 96 bytes, and begins `R0B2`.

Within the result block:

- bytes 0–47 are the identity header: contract SHA-256, LLVM-MOS SDK 23.1.0,
  base-page B value 2, `-mlto-zp=0`, revision 2, and block size;
- bytes 48–58 are the eleven PASS/FAIL/DEFERRED statuses;
- bytes 59–69 are their reason codes;
- bytes 70–73 are the input and SID service elapsed raster-line values;
- bytes 74–77 are complete-buffer and previous-buffer hashes; and
- byte 83 is the checksum of bytes 0–82.

The harness itself declares environment `0` (target binary). The runner record
pins whether that exact block came from the Xemu baseline or an owner hardware
capture; it prevents the binary from guessing which machine it is on.

## Build and host oracle

From the repository root:

```sh
make r0b-build
```

Expected host lines include `R0B-PRES-001 PASS`, `R0B-IN-003 PASS`, and
`R0B-AUD-001 PASS`. The host timings are wall-clock nanoseconds for the host
models; they are not target measurements.

## Xemu baseline

Use the owner ROM only from its approved local path; do not copy it into the
repository:

```sh
F65_MEGA65_ROM='/Users/slice/Documents/Codex/2026-08-15/1-refined-prompt-you-are-the/MEGA65.ROM' make r0b-xemu
```

The Xemu validator produces:

- `build/r0b/reports/R0B-XEMU.screen.txt`;
- `build/r0b/reports/R0B-XEMU.memory.bin`; and
- `build/r0b/reports/r0b-xemu-evidence.json`.

Expected target markers include `R0B-PRES-001 COMPLETE+PREV PASS`,
`R0B-HUD-001 COCKPIT/MFD PASS`, `R0B-REN-001 WIRE PROXY PASS`, and nonzero
`R0B-IN-003 EDGE RASTER` and `R0B-AUD-001 SID RASTER` values. The latest
pinned Xemu capture reports 157 and 12 raster lines respectively. The input
value may vary with starting raster phase; timing is an observation, not a
threshold or a hardware equivalence claim.

## Example verified Xemu result

The latest Xemu capture has the following relevant status lines:

```text
R0B-FCM-SAFE-001 DEFERRED
R0B-PRES-001 COMPLETE+PREV PASS
R0B-HUD-001 COCKPIT/MFD PASS
R0B-REN-001 WIRE PROXY PASS
R0B-IN-003 EDGE RASTER:     157
R0B-AUD-001 SID RASTER:      12
R0B-HW-001 OWNER CAPTURE REQUIRED
R0B-BLD-001 PASS; GATE NOT CLOSED
```

The result block at `$1800` begins as follows (hex); the last byte is checksum
`46`:

```text
52 30 42 32 02 00 01 02 C2 3B E9 9C 1B 73 29 2C
E6 C7 14 F7 91 DD 96 DF E3 0B C2 3C 18 B4 75 AA
E9 BA BB 93 EC C2 6C B7 17 01 00 00 02 00 60 00
03 01 03 01 03 01 01 03 01 01 03 01 00 02 00 01
00 00 03 00 00 05 9D 00 0C 00 E6 98 E6 0C 01 02
03 03 03 46
```

## Physical MEGA65 capture path

1. Run `make r0b-build` and copy the exact `F65-R0B-PROOF.d81` to the SD card
   without unpacking or renaming files inside it.
2. At the BASIC prompt mount it as drive 8 and type `BOOT`.
3. Photograph the complete screen after the harness stops. It must remain
   readable in normal text mode and show `R0B-BLD-001 PASS; GATE NOT CLOSED`.
4. Record the D81 SHA-256, MEGA65 model/core/system-file identity, PAL/NTSC,
   display connection, and the two raster-line values. Retain a byte dump of
   `$1800`–`$185f` when a monitor/debugger path is available.
5. A reset, unreadable screen, zero timing value, checksum mismatch, or any
   `FAIL` result is a failed capture. Preserve it; do not retry the unsafe FCM
   control-register method from this disk.

The physical capture can clear only `R0B-HW-001` from `OWNER CAPTURE REQUIRED`.
It cannot clear the independent FCM-register, hardware-flip, physical-input,
or DMA/PCM deferrals.
