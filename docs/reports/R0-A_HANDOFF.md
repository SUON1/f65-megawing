# R0-A Engineering Handoff — Static Base-Page Proof; Runtime Pending

## What exists

- Exact approved R0 control records and candidate/historical corpus are synchronized and hash-pinned.
- R0-A task admission, ownership scope, agent record, ExecPlan, acceptance registry, canonical proof-only interface registry, platform ABI registry, memory ledger, Java generator/oracle, host validator, and root build commands exist.
- LLVM-MOS v23.1.0, Temurin 21.0.12+8, KickAssembler 5.25, and candidate Xemu identities are locked from inspected artifacts.
- `src/r0a/main.c` and `src/platform/r0a_platform_45gs02.s` form a minimal compiled-C to low-level ABI discovery probe. It establishes `B=$02` after stock startup, preserves it for nested C calls, restores `B=$00` before stock finalization, and tests a physical `$0002-$0021` sentinel against B-relocated ABI use. The linked artifact emits a PRG, map, symbols, and disassembly under ignored `build/r0a/`.

## Results

`make r0a-bootstrap` and `make r0a-host-test` pass. The host suite reports `R0A-CFG-001`, `R0A-PTR-001`, and `R0A-RES-001` PASS.

The target probe verifies that the selected frontend accepts `-mcpu=mos45gs02`, defines its CPU macros, and emits MOS ELF carrying the 45GS02 machine flag. `R0A-BP-001` now passes static map/disassembly validation: logical `__rc0..__rc31` remain `$0002..$0021`, general LTO direct-page sections are empty, `B=$02` follows stock `.init.010`, and `B=$00` precedes stock `.fini.990`.

## Remaining blocker

The user-authorized base-page approach is now represented in source and static evidence; it does not relocate LLVM-MOS symbols. The 45GS02 B register makes logical `$02..$21` use physical `$0202..$0221`, while `-mlto-zp=0` excludes the stock general `$22..$8f` LTO allocation. Runtime behavior is still unverified.

`make r0a-build` retains a verified 80-track D81 containing `AUTOBOOT.C65` and `F65-R0A-PROOF`, along with its PRG/map/symbol/disassembly. `make r0a-xemu` runs the pinned `xmega65` binary against an owner-supplied ROM by path, hashes that ROM, mounts the D81 on drive 8, and retains screen/memory capture on exit. The supplied ROM hash is verified and Xemu reaches its MEGA65 boot path in virtual-SD mode. The first boot requires Xemu onboarding before `AUTOBOOT.C65` can run; this is a local emulator-state setup, not a compiler or upstream blocker. No Xemu PASS, hardware PASS, or R0-A implementation-complete claim exists.

See [R0A-TOOLCHAIN-BASE-PAGE-FINDING.md](../evidence/r0a/R0A-TOOLCHAIN-BASE-PAGE-FINDING.md) and the exact lock in [`toolchain/f65_toolchain.lock.json`](../../toolchain/f65_toolchain.lock.json).

## Required external action

Complete the one-time Xemu onboarding using either a persistent owner SD image (`F65_MEGA65_SD_IMAGE`) or GUI mode (`F65_XEMU_GUI=1`), then execute the sentinel and nested-C arithmetic test through `AUTOBOOT.C65` in Xemu and on physical MEGA65. KERNAL calls remain forbidden from ordinary C until a B-save/B=0/B-restore assembly thunk is separately proved.

## Physical hardware status

**AWAITING HUMAN HARDWARE TEST** — no exact D81 exists yet, so hardware execution must not begin.
