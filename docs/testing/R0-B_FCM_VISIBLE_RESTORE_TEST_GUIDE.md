# R0-B Isolated Visible FCM Card / Restore — Test Guide

This is a bounded R0-B proof artifact. It is not a production display mode,
renderer, palette selection, or hardware pointer-table swap.

## Preconditions

The isolated FCM safe/restore test has a physical readable PASS observation.
This next artifact begins with a read-only runtime-context capture. Do not copy
the visible-card image to a physical MEGA65 until a separate `$D031`
save/set/readback/restore proof passes in Xemu and on the owner hardware.

## What it changes

After read-only precondition checks, the binary may temporarily change only
`$D054` by OR-ing documented FCM bits `$07` (`CHR16|FCLRHI|FCLRLO`). It writes
the currently visible default C65 `$0800` text matrix and an aligned 64-byte
proof character, presents a checker card for a nominal dwell, restores the
screen and character bytes exactly, then restores the exact saved `$D054`.

It does **not** write `$D02F`, `$D031`, `$D058/$D059`, `$D060-$D06A`, `$D070`,
palette registers, DMA, MAP, IRQ state, or a raster handler.

## Current Xemu context capture

With the owner ROM SHA-256
`af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0`,
the current Xemu capture reports:

```text
$D018 = $24  (C65 context admitted)
$D031 = $E0  (80-column state; 40-pair transition not yet proven)
$D054 = $40  (observed only; no write performed)
$D060-$D063 = $00,$08,$00,$00  (runtime screen matrix is $0800)
```

The result is correctly `DEFERRED`, not a failure of Xemu or the ROM. It
clears the false `$0800` assumption and leaves the single next condition
explicit: prove exact `$D031` save/set/readback/restore before any FCM-card
presentation attempt.

## Build and Xemu verification

From the repository root:

```sh
make r0b-fcm-visible-build
F65_MEGA65_ROM=/absolute/path/to/MEGA65.ROM make r0b-fcm-visible-xemu
```

The Xemu screenshot is written to:

`build/r0b/reports/R0B-FCM-VISIBLE-XEMU.png`

Expected terminal result for the present context-capture stage:

```text
R0B-FCM-VIS-XEMU-001 DEFERRED: runtime display context captured; no D054 write performed
```

## Physical visible-card test — blocked pending the D031 proof

Copy this exact disk image:

`build/r0b/artifacts/F65-R0B-FCM-VISIBLE.d81`

Do not run this visible-card image on physical hardware yet. The older physical
capture correctly showed `$D031` incompatible with this image's 40-pair
precondition. The next physical artifact must be the narrower D031
save/set/readback/restore proof; it will have its own D81, checksum, and test
guide.

After that proof passes, record the sibling `.sha256` file, mount the visible
card image as drive 8, type `BOOT`, and capture the brief card phase and final
restored result screen. That final screen must say:

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
