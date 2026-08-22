# R0-B Isolated `$D031` 40-Column Transition / Restore — Test Guide

This is a bounded R0-B safety proof, not an FCM presentation, display-pointer
swap, palette test, renderer, or game feature.

## What it does

In C65 text context only, the wrapper saves `$D031`, writes that saved byte
with H640 (bit 7) clear, compares the latch read-back to the intended byte,
then restores the original byte and verifies that exact restoration. A text
sentinel at `$0800` is checked after the restore.

The static target admission check rejects accesses to `$D02F`, `$D054`,
`$D058/$D059`, `$D060-$D064`, `$D068`, `$D070`, palette registers, DMA, MAP,
and IRQ controls. It uses no production rendering or flight/game code.

## Xemu gate

Run from the repository root, using the already configured owner ROM:

```sh
F65_MEGA65_ROM='/Users/slice/Documents/Codex/f65-megawing/MEGA65.ROM' \
  F65_XEMU_RUN_SECONDS=25 make r0b-d031-safe-xemu
```

Expected terminal result:

```text
R0B-D031-SAFE-XEMU-001 PASS: isolated D031 transition/restore and text sentinel in Xemu
```

The screenshot and result evidence are written to:

- `build/r0b/reports/R0B-D031-SAFE-XEMU.png`
- `build/r0b/reports/r0b-d031-safe-xemu-evidence.json`

## Physical test — only after the Xemu PASS

Copy this exact image to the MEGA65 media:

`build/r0b/artifacts/F65-R0B-D031-SAFE.d81`

Record its companion SHA-256 file:

`build/r0b/artifacts/F65-R0B-D031-SAFE.d81.sha256`

Mount as drive 8 and type `BOOT`. The expected screen lines are:

```text
R0B-D031-SAFE-001 LOCAL TEST: PASS
C65 CONTEXT: PASS
D031 40-COL READBACK: PASS
D031 EXACT RESTORE: PASS
TEXT SENTINEL: PASS
```

Photograph the status and `$1800-$185F` dump. If any line is not `PASS`, the
screen becomes unreadable, or the machine resets, stop: do not run the FCM
visible-card or pointer/swap test. Those later tests remain gated on this
physical result.
