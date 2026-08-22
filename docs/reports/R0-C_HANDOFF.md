# R0-C Handoff

Status: **R0-C implementation is not complete.** This handoff records the
bounded candidate delivered so far and its explicit blockers. It must be updated
after a complete implementation and final remote verification.

## What was built

- Canonical `r0c-0.1.0-proof` contract and generated C/Java constants.
- Deterministic Java proof-package generator, structural validator, capacity
  witness, one-over rejection matrix, and two-generation host fault model.
- Non-shipping technical fixture metadata for terrain/query, carrier proxy,
  aircraft LOD labels, effects, and palette roles.
- A D81 builder that reports a package SHA-256 plus exact and allocated bytes.
- A small LLVM-MOS diagnostic that exposes a 96-byte result block at `$1800`,
  validates a bounded handle, and proves deterministic CPU copy into an owned
  proof buffer.
- Xemu capture/validation for the target diagnostic.

## Honest scope boundary and blockers

The target buffer source is explicitly an **Attic-model**, not real Attic RAM.
No `MemoryAccessABI`, MAP, DMA, or physical Attic access service was added.
The package is not loaded through a target storage service. No post-ROM-reclaim
storage restoration mechanism is asserted because the required official-platform
evidence/wrapper has not been admitted. `DEC-012` is open; therefore no physical
save-medium/media-fault claim is made.

Consequently, this is neither `R0-C IMPLEMENTATION COMPLETE` nor `R0-C GATE
PASSED`.

## Built artifacts and evidence

Generated (ignored) artifacts are under `build/r0c/`:

- `R0CPROOF.PKG`, package manifest, capacity/memory/storage reports, and host evidence.
- `artifacts/F65-R0C-PROOF.prg` and `artifacts/R0CFINAL.D81`.
- `reports/R0C-XEMU.png`, screen dump, memory dump, and Xemu evidence.

See `docs/evidence/r0c/R0C-EVIDENCE-MAP.md` and
`docs/testing/R0-C_TEST_GUIDE.md`.

## Required next work

1. Obtain owner approval for DEC-012 using `R0-C_DEC-012_DECISION_PACKET.md`.
2. Admit/document an official safe target storage and Attic staging service, or
   issue an authoritative blocker for those paths.
3. Implement target package preload/no-disk instrumentation using that service.
4. Implement and test the approved two-generation medium adapter on sacrificial
   media, including post-ROM-reclaim handoff/restore.
5. Repeat host/Xemu evidence, then perform the exact physical procedure and seek
   human acceptance.
