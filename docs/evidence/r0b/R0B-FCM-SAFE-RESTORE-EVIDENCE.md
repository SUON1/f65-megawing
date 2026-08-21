# R0-B Isolated FCM Safe/Restore Evidence

Status: **Xemu PASS; physical MEGA65 NOT RUN; R0-B gate remains open.**

## Exact source and artifact identity

- Official reference: [MEGA65 Chipset Reference v1.2](https://files.mega65.org/files/m/mega65-chipset-reference_cnFcKB.pdf), downloaded 2026-08-21.
- Downloaded PDF SHA-256: `59d7e865bb9782a53fb2f1d019d4d01c44decbad0d077ffd583461e984938270`.
- Toolchain: LLVM-MOS SDK 23.1.0, `-mcpu=mos45gs02 -mlto-zp=0`.
- ABI: base-page B=`$02`; stack `$0100-$01FF` under the existing R0-A startup/finalization wrappers.
- Result block: `$1800-$185F`, 96 bytes, generated `R0BResidentResult`, harness revision 3.
- Xemu: commit `40dfef0d1d5f56be2469492715c12bdb32c75b67`, model 03, PAL, dummy audio backend.

The generated artifact hashes are in `build/r0b/artifacts/F65-R0B-FCM-SAFE.*.sha256`.

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

## Physical clearing condition

The physical MEGA65 owner must run the exact hashed D81 and return:

- one photograph showing all four `PASS` lines and the on-screen `$1800-$185F` dump;
- the D81 SHA-256 from the sibling `.sha256` file;
- machine/core/system-file identity, PAL/NTSC, and display connection; and
- confirmation that the normal text screen remains readable for at least 30 seconds.

Any unreadable text, missing PASS line, non-`$07` flag, failed sentinel, or
unexpected reset is a retained **FAIL**. It does not authorize a retry with a
`$D02F` key-write sequence.
