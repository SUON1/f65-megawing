# R0-A Engineering Handoff — Interim Blocked State

## What exists

- Exact approved R0 control records and candidate/historical corpus are synchronized and hash-pinned.
- R0-A task admission, ownership scope, agent record, ExecPlan, acceptance registry, canonical proof-only interface registry, platform ABI registry, memory ledger, Java generator/oracle, host validator, and root build commands exist.
- LLVM-MOS v23.1.0, Temurin 21.0.12+8, KickAssembler 5.25, and candidate Xemu identities are locked from inspected artifacts.
- `src/r0a/main.c` and `src/platform/r0a_platform_45gs02.s` form a minimal compiled-C to low-level ABI discovery probe. The linked artifact emits a PRG, map, symbols, and disassembly under ignored `build/r0a/`.

## Results

`make r0a-bootstrap` and `make r0a-host-test` pass. The host suite reports `R0A-CFG-001`, `R0A-PTR-001`, and `R0A-RES-001` PASS.

The target probe verifies that the selected frontend accepts `-mcpu=mos45gs02`, defines its CPU macros, and emits MOS ELF carrying the 45GS02 machine flag. Retained generated-C disassembly also establishes the one-byte C-to-low-level probe's observed A-register argument/return behavior for this exact release.

## Blocking finding

The same retained map/disassembly shows that the default `mos-mega65-clang` startup assigns compiler imaginary registers to `$0002–$008f`. F-65 requires the canonical game base page `$0200–$02FF`. No verified compiler/startup/link path has been found that establishes the required 45GS02 base page while preserving LLVM-MOS ABI state.

Consequently the probe is an ABI-discovery artifact only. `make r0a-build` intentionally stops after retaining the PRG/map/symbol/disassembly with a D81 packaging blocker; `make r0a-xemu` and `make r0a-verify` remain blocked. No D81, Xemu PASS, hardware PASS, or R0-A implementation-complete claim exists.

See [R0A-TOOLCHAIN-BASE-PAGE-FINDING.md](../evidence/r0a/R0A-TOOLCHAIN-BASE-PAGE-FINDING.md) and the exact lock in [`toolchain/f65_toolchain.lock.json`](../../toolchain/f65_toolchain.lock.json).

## Required external action

Provide or approve an evidence-backed LLVM-MOS/45GS02 base-page relocation and startup path, including its public ABI, generated disassembly, and safe return contract. Once it is available, rerun the target probe, then establish an independently verified D81 construction/boot route before Xemu and physical-MEGA65 testing.

## Physical hardware status

**AWAITING HUMAN HARDWARE TEST** — no exact D81 exists yet, so hardware execution must not begin.
