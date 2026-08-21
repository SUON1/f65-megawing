# R0-B Isolated FCM Safe/Restore — Physical MEGA65 Test

This is an R0-B proof artifact, not a game build and not a gate closure.
It is intentionally the only artifact to run before any hardware pointer-flip
or visible-FCM experiment.

## File to test

Build from the repository root:

```sh
make r0b-fcm-safe-build
```

Copy this exact disk image to the SD card without changing its contents:

`build/r0b/artifacts/F65-R0B-FCM-SAFE.d81`

Record the value in `build/r0b/artifacts/F65-R0B-FCM-SAFE.d81.sha256` before
testing.

### Boot compatibility isolation

The previous physical attempt stopped at `BOOT` with `MEGA65 ROM VERSION
ERROR`, before this harness executed. This replacement disk deliberately uses
the byte-identical 28-byte BASIC-65 launcher and filename alias
`f65-r0a-proof` that the owner already proved on physical MEGA65 for R0-A.
The alias is only a disk-loader compatibility control; its payload and the
on-screen banner remain `R0B-FCM-SAFE-002`.

Do not use the prior D81 hash. Confirm the newly generated hash before copying
this replacement image.

## Run

1. Mount the D81 as drive 8 on the MEGA65.
2. At the BASIC prompt type `BOOT` and press Return.
3. Wait for the resident status screen. Do not type any further commands.
4. Leave it on screen for at least 30 seconds.

## A successful physical capture must show

```text
R0B-FCM-SAFE-002 LOCAL TEST: PASS
PHYSICAL EVIDENCE: PENDING
C65 CONTEXT: PASS
D054 LATCH READBACK: PASS
D054 EXACT RESTORE: PASS
TEXT SENTINEL: PASS
GATE OPEN; FCM FRAME/SWAP NOT ENABLED
```

The twelve rows below `RESULT HEX $1800-$185F BELOW` are the complete 96-byte
`$1800-$185F` result block
in hexadecimal. Photograph those rows too; no monitor command is required.
Return that photo plus the D81 SHA-256, MEGA65 model/core/system-file identity,
PAL/NTSC, and display connection.

## Fail and stop conditions

Stop and retain a photo if `BOOT` again reports `MEGA65 ROM VERSION ERROR`, the
display becomes unreadable, the machine resets, any status says `FAIL` or
`DEFERRED/FAIL`, the result flags are not `$07`, or the sentinel fails. Do
**not** retry an old build or a build that writes `$D02F`.

A good physical result clears only the isolated restore admission test. It does
not close R0-B or approve a hardware flip, visible FCM, physical input path,
or PCM/DMA path.
