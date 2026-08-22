# R0-C Physical Test Guide

Status: **draft — do not treat this as authorization to run storage/media faults until DEC-012 is approved.**

## Exact candidate

- D81: `build/r0c/artifacts/R0CFINAL.D81`
- Package: `build/r0c/R0CPROOF.PKG`
- Commit: record the final pushed R0-C commit in the handoff before a physical run.
- Required identity: LLVM-MOS/JDK/Xemu identities in `toolchain/f65_toolchain.lock.json` and the build manifest.
- Video: record PAL/NTSC actually used. Hardware revision, FPGA core/hash, ROM SHA-256, system-files identity, storage device, and media configuration must be photographed or logged with the result.

## Safe test sequence

1. Verify the D81 SHA-256 against the final handoff; transfer a copy only.
2. Mount/boot it normally. `AUTOBOOT.C65` loads `R0C-FINAL` using PETSCII-safe on-disk names.
3. Photograph the whole result screen and capture the visible `$1800-$185f` block if shown by a diagnostic monitor.
4. Expected target lines: `R0C-ID-001` through `R0C-NODISK-001` PASS; `R0C-ROM-001` DEFERRED; `R0C-SAVE-001` identifies DEC-012 as open; `R0C-MEDIA-001` awaits a human media plan.
5. Do **not** remove media during any future write transaction. This candidate has no admitted physical save transaction.

## Deferred physical sequence

After the owner approves DEC-012, use a sacrificial writable medium only. The
future exact procedure must cover normal/repeated writes, changed/removed and
write-protected media, full media, corrupt selector/generation, and interruption
at each transaction stage. It must also state the last storage operation before
ROM reclaim, the restoration path, MAP, `$01`, base page, IRQ/vector state, and
post-reclaim storage behavior. Those details are intentionally absent because no
authoritative platform wrapper has been admitted.

Expected duration for the current read-only diagnostic: under one minute. Return
the full-screen photo, the exact D81 hash, ROM/core/system-files identity, and the
raw result-block bytes. Evidence is matched to the final commit/package/D81 hash.
