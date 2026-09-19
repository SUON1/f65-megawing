# R0-A Engineering Handoff — Complete

## What exists

- Exact approved R0 control records and candidate/historical corpus are synchronized and hash-pinned.
- R0-A task admission, ownership scope, agent record, ExecPlan, acceptance registry, canonical proof-only interface registry, platform ABI registry, memory ledger, Java generator/oracle, host validator, and root build commands exist.
- LLVM-MOS v23.1.0, Temurin 21.0.12+8, KickAssembler 5.25, and candidate Xemu identities are locked from inspected artifacts.
- `src/r0a/main.c` and `src/platform/r0a_platform_45gs02.s` form a minimal compiled-C to low-level ABI discovery probe. It establishes `B=$02` after stock startup, preserves it for nested C calls, restores `B=$00` before stock finalization, and tests a physical `$0002-$0021` sentinel against B-relocated ABI use. The linked artifact emits a PRG, map, symbols, and disassembly under ignored `build/r0a/`.

## Results

`make r0a-bootstrap` and `make r0a-host-test` pass. The host suite reports `R0A-CFG-001`, `R0A-PTR-001`, and `R0A-RES-001` PASS.

The target probe verifies that the selected frontend accepts `-mcpu=mos45gs02`, defines its CPU macros, and emits MOS ELF carrying the 45GS02 machine flag. `R0A-BP-001` now passes static map/disassembly validation: logical `__rc0..__rc31` remain `$0002..$0021`, general LTO direct-page sections are empty, `B=$02` follows stock `.init.010`, and `B=$00` precedes stock `.fini.990`.

## Completion evidence

The user-authorized base-page approach is represented in source and static evidence; it does not relocate LLVM-MOS symbols. The 45GS02 B register makes logical `$02..$21` use physical `$0202..$0221`, while `-mlto-zp=0` excludes the stock general `$22..$8f` LTO allocation. Xemu and physical-hardware behavior are verified.

`make r0a-build` retains a verified 80-track D81 containing lower-byte PETSCII `autoboot.c65` and `f65-r0a-proof`, along with its PRG/map/symbol/disassembly. `make r0a-xemu` runs the pinned `xmega65` binary against the owner-supplied ROM, mounts the D81 on drive 8, captures screen/memory output, and validates the target result block. `R0A-XEMU-001` passes: direct PRG and D81 `AUTOBOOT.C65` execution both produce `R0A1 01 01 5A 02 01 04 57`, including `R0A-BP-001 PASS`. The owner then ran the corrected D81 on physical MEGA65 and captured `R0-A TEST RUN COMPLETE`, `R0A-BP-001 PASS`, and `R0A-PTR-001 PASS`. R0-A is complete.

See [R0A-TOOLCHAIN-BASE-PAGE-FINDING.md](../evidence/r0a/R0A-TOOLCHAIN-BASE-PAGE-FINDING.md) and the exact lock in [`toolchain/f65_toolchain.lock.json`](../../toolchain/f65_toolchain.lock.json).

## Follow-on constraint

KERNAL calls remain forbidden from ordinary C until a B-save/B=`$00`/B-restore assembly thunk is separately proved.

## Physical hardware status

**PASS — 2026-08-20.** The owner-operated physical MEGA65 capture shows the two required R0-A PASS markers. The captured setup identifies MEGA65 BASIC ROM v920413.
