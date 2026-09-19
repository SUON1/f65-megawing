# R0-B Isolated FCM Safe/Restore Evidence

Status: **Xemu PASS; later physical MEGA65 runtime PASS observed; evidence identity incomplete; R0-B gate remains open.**

## Exact source and artifact identity

- Official reference: [MEGA65 Chipset Reference v1.2](https://files.mega65.org/files/m/mega65-chipset-reference_cnFcKB.pdf), downloaded 2026-08-21.
- Downloaded PDF SHA-256: `59d7e865bb9782a53fb2f1d019d4d01c44decbad0d077ffd583461e984938270`.
- Toolchain: LLVM-MOS SDK 23.1.0, `-mcpu=mos45gs02 -mlto-zp=0`.
- ABI: base-page B=`$02`; stack `$0100-$01FF` under the existing R0-A startup/finalization wrappers.
- Result block: `$1800-$185F`, 96 bytes, generated `R0BResidentResult`, harness revision 3.
- Xemu: commit `40dfef0d1d5f56be2469492715c12bdb32c75b67`, model 03, PAL, dummy audio backend.

The generated artifact hashes are in `build/r0b/artifacts/F65-R0B-FCM-SAFE.*.sha256`.

## Physical boot packaging result

The owner-operated MEGA65 attempt on 2026-08-21 typed `BOOT` against the
earlier `F65-R0B-FCM-SAFE.d81`. BASIC returned `MEGA65 ROM VERSION ERROR` and
returned to `READY.` The status screen did not appear, so the binary did not
execute and this is **not** FCM, D054, text-restore, or runtime evidence.

The replacement artifact uses the exact 28-byte `AUTOBOOT.C65` sequence and
the `f65-r0a-proof` disk filename alias from the physically passed R0-A
launcher. Its payload remains the FCM-safe program and identifies itself on
screen as `R0B-FCM-SAFE-002`. The replacement needs a new physical `BOOT`
capture before any hardware conclusion can be made. Its screen says `LOCAL
TEST: PASS` and `PHYSICAL EVIDENCE: PENDING` deliberately: the screen records
the program's local assertions, while the owner capture supplies the separate
physical evidence.

## Physical runtime observation (2026-08-21)

The owner subsequently returned a readable MEGA65 photograph of the
replacement program after `BOOT`. It shows all local assertions as `PASS`:

- `R0B-FCM-SAFE-002 LOCAL TEST: PASS`;
- `C65 CONTEXT: PASS`;
- `D054 LATCH READBACK: PASS`;
- `D054 EXACT RESTORE: PASS`; and
- `TEXT SENTINEL: PASS`.

The on-screen result dump shows the expected header prefix `52 30 42 32 02
00 01 03` (`R0B2`, schema 2, local pass, revision 3) and the probe/sentinel
bytes at `$1854-$1855` as `07 01`. This clears the **isolated physical
safe-restore runtime observation**: the documented `$D054` operation could be
latched, read back, exactly restored, and followed by readable text on that
machine.

The owner did not yet provide the exact D81 SHA-256, MEGA65/core/system-file
identity, video standard, or display connection. Therefore this is retained as
an owner photograph with incomplete identity, not gate-closing physical
evidence. It does not prove visible FCM, FCM pointer-table swap, palette
behavior, DMA, input, or audio behavior.

## What the isolated binary does

`src/platform/r0b/fcm_restore_45gs02.s` is a bounded assembly wrapper. It:

1. Reads `$D018`; a missing C65-context indication returns a deferred result and performs no `$D054` write.
2. Reads and retains `$D054`.
3. Writes `$D054 | $05` (`CHR16|FCLRHI`), reads those two bits back, and immediately writes back the exact saved byte.
4. Checks the restored `$D054` byte and a prewritten text-memory sentinel.
5. Displays the status and a full hex dump of `$1800-$185F` across twelve rows of the normal 80-column text screen.

It contains no `$D02F` write, `$D031` write, screen/colour/character pointer
write, palette change, DMA submission, MAP operation, IRQ masking, or raster
handler. It does not assert visible FCM, active palette, presentation swap,
physical input, or audio DMA behavior.

## Xemu result

`R0B-FCM-SAFE-XEMU-001` passed with result flags `$07`:

| Flag | Meaning | Xemu result |
|---|---|---|
| bit 0 | C65 text context observed | PASS |
| bit 1 | `$D054` read-back contained `CHR16|FCLRHI` | PASS |
| bit 2 | `$D054` equalled its saved byte after restoration | PASS |
| byte 85 | text-memory sentinel after return | PASS (`$01`) |

The retained generated evidence is `build/r0b/reports/r0b-fcm-safe-xemu-evidence.json` and the matching screenshot, screen dump, and memory dump. This is emulator evidence only.

## Identity completion condition

To make the recorded physical observation fully reproducible, retain the
matching D81 SHA-256 plus the MEGA65 model/core/system-file identity,
PAL/NTSC, and display connection. The readable photograph and the on-screen
result block are already returned. A future repeat is not required merely to
obtain those identity details.

Any future physical visible-FCM test must return:

- one photograph showing all four `PASS` lines and the on-screen `$1800-$185F` dump;
- the D81 SHA-256 from the sibling `.sha256` file;
- machine/core/system-file identity, PAL/NTSC, and display connection; and
- confirmation that the normal text screen remains readable for at least 30 seconds.

Any unreadable text, missing PASS line, non-`$07` flag, failed sentinel, or
unexpected reset is a retained **FAIL**. It does not authorize a retry with a
`$D02F` key-write sequence.
