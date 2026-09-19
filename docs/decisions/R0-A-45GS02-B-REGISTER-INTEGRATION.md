# R0-A 45GS02 B-Register Integration Decision

**Status:** User-authorized R0 integration; static proof passing; runtime proof pending
**Date:** 2026-08-20
**Scope:** R0-A proof harness only; no production gameplay or public production ABI change

## Decision

Pin R0-A to LLVM-MOS SDK v23.1.0 (`7e47e7d`). Retain the stock MEGA65 linker symbols: `__rc0..__rc31` remain logical direct-page offsets `$0002..$0021`; do not relocate them to literal `$0202..$0221`.

Set 45GS02 `B=$02` in `.init.011`, after the stock MEGA65 `.init.010` writes to physical CPU-port locations `$0000/$0001`. Keep B at `$02` through C execution, and restore `B=$00` in `.fini.989`, before stock `.fini.990` restores the ROM mapping. R0-A overrides the stock `-mlto-zp=110` with `-mlto-zp=0`, so the general compiler-managed logical `$0022..$008f` range is not allocated.

The required runtime proof seeds a patterned sentinel at physical `$0002..$0021` with forced 16-bit addressing, confirms `TBA==$02` from C, runs nested 16/32-bit C arithmetic, then confirms the physical sentinel is unchanged. KERNAL calls require a separate B-save/B=`$00`/B-restore assembly thunk and are not admitted by this decision.

## Static evidence gate

`make r0a-build` records a PRG, ELF, map, symbol table, and disassembly, then runs `R0A-BP-001`. The gate requires logical ABI symbols `$0002..$0021`, empty general `.zp.data`/`.zp.bss`, ordered `.init.010 → .init.011 → main`, ordered `.fini.989 → .fini.990`, `TAB` transitions, physical sentinel opcodes, and nested-C direct-page operands.

The build intentionally returns status 2 after this gate until a D81 construction/auto-boot path is verified. Static evidence is not Xemu or hardware execution evidence.
