# R0-B VIC-IV / FCM / DMA Source Finding

Status: scoped technical source finding, not a production selection.

## Source identity

- MEGA65 Team, [Chipset Reference PDF](https://files.mega65.org/files/m/mega65-chipset-reference_4hh2eE.pdf), accessed 2026-08-20.
- Pinned LLVM-MOS SDK v23.1.0 header:
  `toolchain/runtime/llvm-mos/mos-platform/mega65/include/_vic4.h`.

## Behaviors admitted to the first target probe

The reference identifies FCM as an 8×8, 256-colour-per-character mode with
64 data bytes per character; FCM normally pairs with 16-bit character numbers
for more than 256 character identities. The relevant documented controls are
the `CHR16`, `FCLRLO`, and `FCLRHI` bits of VIC-IV control register C (`$D054`).

`src/platform/r0b/vic4_probe.c` does only this: unlocks VIC-IV I/O, saves
`$D054`, sets those three bits, reads them back, and restores the saved byte.
`R0B-FCM-REG-001` is therefore a register-latch/restoration proof, not a claim
that a visible FCM frame, pointer table, swap boundary, or raster behavior has
passed.

## DMA finding and boundary

The source documents F018B fill/copy list fields and says that a DMA job blocks
normal CPU execution until completion, while audio DMA continues. R0-B will use
only immutable, range-validated lists under its Core/Platform proof owner.
No DMA operation is admitted by this finding yet: the target must first prove
list byte layout, trigger format, range validation, completion observation, and
the canonical MAP/interrupt return state in a separate smallest test.

## 2026-08-20 Xemu experiment disposition

An R0-B-only enhanced F018B DMA candidate wrote an immutable list at a normal
resident address, requested contiguous writes only to the allocated FCM
pointer-table/store-A ranges, then attempted a DMA copy-back to the fixed
diagnostic block. Its copy-back did not match in the pinned Xemu run; the first
strided-table form also produced an Xemu modulo-mode warning. The experiment
was removed rather than retained as a hardware claim or used on a MEGA65.

Result: `NOT_APPLICABLE_UNTIL_GATE: independently verified F018B list and
completion proof — current Xemu result is unresolved`. The existing
`R0B-FCM-REG-001` register-latch evidence remains valid and is not DMA evidence.

## Explicitly not yet proven

- FCM character-data placement and screen-table interpretation on the target.
- Display-store swap timing, raster boundary behavior, tearing, or incomplete
  store protection.
- DMA list lifetime, blocking distribution, or graphics/audio contention.
- RRB, affine, SID/PCM, CIA input, and raster/IRQ behavior.
