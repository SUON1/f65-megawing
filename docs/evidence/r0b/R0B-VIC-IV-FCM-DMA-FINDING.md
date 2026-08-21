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

`src/platform/r0b/vic4_probe.c` is retained as source for a future isolated
probe. It unlocks VIC-IV I/O, saves `$D054`, sets those three bits, reads them
back, and restores the saved byte. It is not run by the owner-facing disk.

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
completion proof — current Xemu result is unresolved`. The prior register-latch
result is not DMA evidence.

## 2026-08-20 physical MEGA65 display disposition

The first owner hardware execution of the D81 that invoked the `$D054`
latch/read/restore sequence produced an audible SID tone but an unreadable
normal text display. R0-A used the same `$0800` text-output routine on this
machine successfully, so the state-changing `$D054` probe is the affected
difference. The run is a hardware **FAIL** for `R0B-FCM-REG-001`, not a
graphics result and not an FCM pass.

The replacement owner disk does not access `$D054`. It reports
`R0B-FCM-REG-001 DEFERRED` and is limited to a readable display baseline,
target deterministic input fixture, and SID tone observation. A future FCM
probe must be smallest-first, demonstrate that the original text display is
restored on physical hardware, and only then be considered for a visible FCM
test.

## Explicitly not yet proven

- FCM character-data placement and screen-table interpretation on the target.
- Display-store swap timing, raster boundary behavior, tearing, or incomplete
  store protection.
- DMA list lifetime, blocking distribution, or graphics/audio contention.
- RRB, affine, SID/PCM, CIA input, and raster/IRQ behavior.
