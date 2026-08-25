# R0-C Evidence Map

Status: **R0-C IMPLEMENTATION COMPLETE; this is not an R0-C closure record.**
Commit `a1a9a26c97ff45bdea7a430fd34ffb8c0442577c` is verified on the requested
origin branch. `R0CMEDIA.D81` is a fixture-artifact
filename only, never a gate-closure label.

| Test ID | Proof | Host | Xemu | Physical | Evidence / limitation |
|---|---|---|---|---|---|
| R0C-ID-001 | Pinned proof identity and 96-byte `$1800` result block | PASS | PASS | PASS | Owner observed the direct device-9 load/run screen. |
| R0C-PKG-001 | Explicit-LE, bounded package header/directory/integrity | PASS | PASS (target identity) | PASS | Physical screen observation is recorded; package mutation corpus remains host evidence. |
| R0C-CAP-001 | Exact combined witness and every one-over rejection | PASS | PASS (target identity) | PASS | Physical screen observation; one-over matrix remains host evidence. |
| R0C-RES-001 | Handle sentinel/range validation | PASS | PASS | PASS | Direct device-9 proof screen. |
| R0C-STG-001 | Real bounded CPU copy into owned proof buffer | PASS | PASS | PASS | Direct device-9 proof screen; no storage operation is in this diagnostic. |
| R0C-ATTIC-001 | ABI/range/rollback | PASS | PASS | PASS | Direct device-9 proof screen. |
| R0C-NODISK-001 | No tactical disk function linked into target diagnostic | PASS | PASS | PASS | Static guard plus direct device-9 proof screen. |
| R0C-ROM-001 | Post-ROM-reclaim storage handoff | Deferred | Deferred | Deferred | No officially documented reversible restore contract is admitted. |
| R0C-SAVE-001 | Two-generation transaction/fault model and fixture | PASS | Fixture menu/boot PASS | Awaiting | Host model and D81 fixture exist; no physical transaction pass is claimed. |
| R0C-MEDIA-001 | Absent/write-protected/full/corrupt/removed/interrupted-media faults | Fixture surface PASS | Fixture menu PASS | Awaiting | Requires the exact sacrificial device-9 matrix in the test guide. |

## Recorded physical proof observation

The owner reported a physical MEGA65 screen PASS for `R0C-ID-001`,
`R0C-PKG-001`, `R0C-CAP-001`, `R0C-RES-001`, `R0C-STG-001`,
`R0C-ATTIC-001`, and `R0C-NODISK-001`, run directly from sacrificial device 9:

```basic
LOAD "R0C-FINAL",9,1
RUN
```

Device 8 is the owner's F0C-final SD and was neither mounted nor modified for
that proof. The R0-C proof PRG remains SHA-256
`285965bcfcfe36826f9f1f8bcf36ad488f3e0c2c6b42c3dfa6859232affcb6bd`.

## Current reproducible fixture identity

- D81: `build/r0c/artifacts/R0CMEDIA.D81`
  - SHA-256: `70232dbdb9cc044611f306a256e046ff6c6fbd5fc98500673276f79c44352aef`
  - Media-only directory: `AUTOBOOT` and `R0C-MEDIA` only; no proof PRG or
    package is present.
- Device-9 fixture: `R0C-MEDIA.C65`
  - SHA-256: `0bdddae9363327dc286c5a7e18f5e0ed76e81ddeaacc90b9f48ce2a858fb37cb`
- Package SHA-256: `9b535b022c97a7b9eb52552ac07f7776c677f23a3c604b75f9541d43c114f19f`

The media-only D81's `AUTOBOOT.C65` uses only `LOAD "R0C-MEDIA",9,1`; it has
no implicit or device-8 fallback. The separate proof boot entry uses only
`LOAD "R0C-FINAL",9,1`. The Xemu media test mounts the media D81 at device 9
only, starts its `AUTOBOOT`, and captures the readable menu. It does not
execute a write, model removal, or replace physical media evidence.

The fixture writes only `R0CG0`, `R0CG1`, and `R0CSEL` on device 9. It writes
the inactive generation with 512 checked payload records, rereads/verifies it,
and only then writes `R0CSEL`.
The controlled interruption action pauses after verification and before the
selector write. It is a DEC-012 sacrificial test fixture, not a production save
medium, disk split, recovery UX, or post-ROM-reclaim service.

`R0-C IMPLEMENTATION COMPLETE` is eligible only after the implementation,
host/Xemu validation, guide, evidence, commits, and remote verification are all
recorded. `R0-C GATE PASSED` additionally requires physical save/media evidence,
a formally resolved ROM-reclaim condition, and human acceptance.
