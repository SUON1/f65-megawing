# R0-C Evidence Map

Status: **R0-C IMPLEMENTATION COMPLETE — owner-waived remaining physical media
fault matrix (2026-08-29). This is not a formal hardware-gate PASS.**
`R0CMEDIA.D81` and `ROCFINAL.D81` are retired after observed Freezer `FF`
mount failures. `F65-R0C-MEDIA.D81` is the sole current fixture candidate.

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
| R0C-SAVE-001 | Two-generation transaction/fault model and fixture | PASS | Fixture menu/boot PASS | Historical menu observation only | The historical carrier cannot be tied to the current candidate; no transaction pass is claimed. |
| R0C-MEDIA-001 | Absent/write-protected/full/corrupt/removed/interrupted-media faults | Fixture surface PASS | Fixture menu PASS | WAIVED BY OWNER | Physical fault matrix intentionally not executed after owner closure request; no PASS inferred. |

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

## Current corrected fixture identity

- Mount control: `F65-R0CFINAL.D81`
  - SHA-256: `ba72aa82387f7e65551e893a3274f1c7f26a813416652c4aeab73c6a8b7e7e38`
  - The owner mounted this three-file control successfully. It must not be
    modified and it does not contain `R0C-MEDIA`.
- D81: `build/r0c/artifacts/F65-R0C-MEDIA.D81`
  - SHA-256: `e0d4600994cd7eb69870ea935974db0175868017e115222521965c7fc70d113`
- Historical prior fixture hash `8826fc89706bcca0d9587f9bae80b5d12a8a1d35e3e0a92868c118e9ef204059` is retired after the DOS 62 / line-5110 defects described below.
  - Carrier directory: `AUTOBOOT`, `R0C-FINAL`, `R0CPROOF`, then appended
    `R0C-MEDIA`.
- Device-9 fixture: `R0C-MEDIA.C65`
  - SHA-256: `91ce42ca7d831ff6eeebc75d60c2b2eb01939dd453e46b68433f34147e66f366`
- Package SHA-256: `9b535b022c97a7b9eb52552ac07f7776c677f23a3c604b75f9541d43c114f19f`

`AUTOBOOT.C65` uses only `LOAD "R0C-FINAL",9,1`; it has no implicit or
device-8 fallback. The Xemu media test mounts this carrier at device 9 only,
starts a separate explicit `LOAD "R0C-MEDIA",9,1` boot entry, and captures the
readable menu. It does not execute a write, model removal, or replace physical
media evidence.

The fixture writes only `R0CG0`, `R0CG1`, and `R0CSEL` on device 9. It writes
the inactive generation with 512 checked payload records, rereads/verifies it,
and only then writes `R0CSEL`.
The controlled interruption action pauses after verification and before the
selector write. It is a DEC-012 sacrificial test fixture, not a production save
medium, disk split, recovery UX, or post-ROM-reclaim service.

## Physical carrier observations (2026-08-24/25)

The Freezer rejected both delivered `R0CMEDIA.D81` and replacement
`ROCFINAL.D81` with `ERROR CODE FF` when selected for the external-1565
managed drive. Those artifacts are retired. The owner supplied
`F65-R0CFINAL.D81`, which does mount but contains only `AUTOBOOT`, `R0C-FINAL`,
and `R0CPROOF`; it therefore cannot supply the fixture program. Its
`R0C-FINAL` and `R0CPROOF` bytes are the control for the correction above.

The corrected carrier preserves that package/proof layout and appends
`R0C-MEDIA` afterward. It also retains the explicit device-9 boot contract and
the PETSCII/ASCII input normalization that fixes the observed `I` unknown-action
defect. The D81 is a virtual floppy: device-9 writes mutate its sacrificial D81
sectors, whose backing file resides on the SD card; this does not access device
8. No physical mount, initialization, or fault action is claimed for the
corrected carrier yet.

`R0-C IMPLEMENTATION COMPLETE` is eligible only after the corrected
implementation, host/Xemu validation, guide, evidence, commits, and remote
verification are all recorded. `R0-C GATE PASSED` additionally requires
physical save/media evidence, a formally resolved ROM-reclaim condition, and
human acceptance.

## Owner waiver closure (2026-08-29)

The owner reports that the exact corrected carrier loads on physical hardware
without chooser `ERROR CODE FF` and reaches the fixture menu. The owner then
requested completion and waived further physical media-fault execution. The
physical result for `R0C-MEDIA-001` is therefore **WAIVED**, not PASS; no
initialization, recovery, corruption, removal, write-protection, full-media,
or interruption result is inferred from the menu observation.

Candidate closure: **R0-C IMPLEMENTATION COMPLETE — OWNER-WAIVED REMAINING
PHYSICAL MEDIA FAULT MATRIX**. `R0C-ROM-001` remains deferred and formal
`R0-C GATE PASSED` is not claimed.

Final carrier: `build/r0c/artifacts/F65-R0C-MEDIA.D81`
SHA-256: `e01eb41cff0158e7b609a365ecc72b78b3ce825ddca06a42a32f8954f4c7e8d0`
Source commit: `2ce0e35` (local, not pushed)
