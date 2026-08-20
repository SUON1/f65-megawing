# R0-A Toolchain Base-Page Finding

## Status

**BLOCKED — no conforming target proof is claimed.**

## Governing requirement

Architecture 1.5.1 §2.2 requires every public routine to assume and restore the relocated game base page at `$0200–$02FF`. Sections 1.6 and 2.6 require the C/platform boundary and its public entry/exit state to be proved, not presumed. Engine 0.2 §§2.4–2.5 and `ABI-01` make compiler stack/register/base-page behavior an R0-A verification deliverable.

## Observed evidence

The inspected LLVM-MOS v23.1.0 `mos-mega65-clang` driver accepts `-mcpu=mos45gs02`, defines `__mos45gs02__`, and emits a relocatable MOS ELF object with the `mos45gs02` flag. The default driver configuration also supplies `-mlto-zp=110`.

The retained preliminary C/assembly probe map assigns `__rc0` to `$0002`; the disassembly uses `$02–$09` for compiler imaginary registers. The probe's minimal startup does not show a verified 45GS02 base-page setup. It therefore cannot be labeled as conforming to the F-65 canonical base-page contract.

## Impact and disposition

The preliminary PRG is an ABI-discovery artifact only. It is not an R0-A proof D81, is not run under Xemu, and is not accepted as a target PASS. No target implementation that relies on this startup is advanced.

The smallest required next action is a documented, reproducible compiler/linker/startup path that sets and restores the 45GS02 base page at `$0200` while preserving the selected LLVM-MOS ABI. That path must be demonstrated in disassembly and then tested in Xemu and on physical MEGA65 before the affected R0-A tests can report PASS.
