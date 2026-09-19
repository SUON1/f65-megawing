# R0-A Toolchain Base-Page Finding

## Status

**STATIC REMEDIATION IMPLEMENTED — runtime proof remains pending.**

## Governing requirement

Architecture 1.5.1 §2.2 requires every public routine to assume and restore the relocated game base page at `$0200–$02FF`. Sections 1.6 and 2.6 require the C/platform boundary and its public entry/exit state to be proved, not presumed. Engine 0.2 §§2.4–2.5 and `ABI-01` make compiler stack/register/base-page behavior an R0-A verification deliverable.

## Observed evidence

The inspected LLVM-MOS SDK v23.1.0 (`7e47e7d`) `mos-mega65-clang` driver accepts `-mcpu=mos45gs02`, defines `__mos45gs02__`, and emits a MOS ELF object with the `mos45gs02` flag. The stock MEGA65 configuration supplies `-mlto-zp=110`; R0-A explicitly overrides it with `-mlto-zp=0`.

The linked R0-A map assigns `__rc0..__rc31` to logical `$0002..$0021`, with zero-sized `.zp.data` and `.zp.bss`. Its ordered startup shows stock `.init.010`, then `f65_basepage_enter` in `.init.011` (`LDA #$02`, `TAB`), followed by compiler ABI accesses with 8-bit offsets. Ordered finalization shows `f65_basepage_leave` in `.fini.989` (`LDA #$00`, `TAB`) before stock `.fini.990`. The sentinel assembly uses forced 16-bit physical `$0002,Y` instructions, so its 32-byte pattern is outside the B-relocated ABI window.

## Impact and disposition

This static proof removes the unresolved startup/link-path blocker. It is not an R0-A proof D81, has not run under Xemu, and is not accepted as a target runtime PASS. The `R0A-BP-001` target validator checks the logical register map, zero general LTO direct-page allocation, init/fini order, B transitions, physical sentinel opcodes, and nested-C direct-page operands.

The next action is an independently verified D81 construction/auto-boot path, followed by Xemu execution of the sentinel and nested C arithmetic test, then physical MEGA65 execution before `R0A-BP-001` can report runtime PASS.
