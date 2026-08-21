# R0-B Isolated Visible FCM Card / Restore — Test Guide

This is a bounded R0-B proof artifact. It is not a production display mode,
renderer, palette selection, or hardware pointer-table swap.

## Preconditions

The isolated FCM safe/restore test has a physical readable PASS observation.
This next artifact still requires an **Xemu PASS first**. Do not copy it to a
physical MEGA65 until `make r0b-fcm-visible-xemu` passes using the owner ROM.

## What it changes

After read-only precondition checks, the binary temporarily changes only
`$D054` by OR-ing documented FCM bits `$07` (`CHR16|FCLRHI|FCLRLO`). It writes
the currently visible default C65 `$0800` text matrix and an aligned 64-byte
proof character, presents a checker card for a nominal dwell, restores the
screen and character bytes exactly, then restores the exact saved `$D054`.

It does **not** write `$D02F`, `$D031`, `$D058/$D059`, `$D060-$D06A`, `$D070`,
palette registers, DMA, MAP, IRQ state, or a raster handler.

## Build and Xemu verification

From the repository root:

```sh
make r0b-fcm-visible-build
F65_MEGA65_ROM=/absolute/path/to/MEGA65.ROM make r0b-fcm-visible-xemu
```

The Xemu screenshot is written to:

`build/r0b/reports/R0B-FCM-VISIBLE-XEMU.png`

Expected terminal result:

```text
R0B-FCM-VIS-XEMU-001 PASS: default C65 FCM card and exact restoration in Xemu
```

## Physical test — only after Xemu passes

Copy this exact disk image:

`build/r0b/artifacts/F65-R0B-FCM-VISIBLE.d81`

Record the sibling `.sha256` file, mount it as drive 8, type `BOOT`, and do
not issue other commands. Capture both the brief FCM checker-card phase and
the final restored result screen. The final screen must say:

```text
R0B-FCM-VIS-001 LOCAL TEST: PASS
C65 CONTEXT: PASS
D031 40-PAIR PRECONDITION: PASS
D060 DEFAULT $0800 PRECONDITION: PASS
D054 FCLRLO/HI+CHR16 LATCH: PASS
FCM 64-BYTE CARD ALIGNMENT: PASS
D054 EXACT RESTORE: PASS
SCREEN BYTES EXACT RESTORE: PASS
FCM CARD BYTES EXACT RESTORE: PASS
```

The `$1800-$185F` hex dump must also be photographed. Any unreadable text,
reset, missing card phase, missing PASS line, or failed result is a retained
FAIL; stop without attempting a pointer-table swap.
