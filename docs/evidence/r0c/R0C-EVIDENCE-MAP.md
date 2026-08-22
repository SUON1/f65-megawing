# R0-C Evidence Map

Status: **implementation evidence in progress; this is not an R0-C closure record.**

| Test ID | Proof | Host | Xemu | Physical | Evidence / limitation |
|---|---|---|---|---|---|
| R0C-ID-001 | Pinned proof identity and 96-byte `$1800` result block | PASS | PASS | Awaiting | `build/r0c/evidence/r0c-*-evidence.json` |
| R0C-PKG-001 | Explicit-LE, bounded package header/directory/integrity | PASS | PASS (target identity) | Awaiting | `R0CPROOF.PKG`; host mutation corpus |
| R0C-CAP-001 | Exact combined witness and every one-over rejection | PASS | PASS (target identity) | Awaiting | `r0c-capacity-report.json` |
| R0C-RES-001 | Handle sentinel/range validation | PASS | PASS | Awaiting | Target has a bounded proof directory |
| R0C-STG-001 | Real bounded CPU copy into owned proof buffer | PASS | PASS | Awaiting | Physical ABI/clobber measurement remains pending |
| R0C-NODISK-001 | No tactical disk function linked into target diagnostic | PASS | PASS | Awaiting | Static guard; not a loaded-package tactical run |
| R0C-ROM-001 | Post-ROM-reclaim storage handoff | Deferred | Deferred | Awaiting | No admitted authoritative restoration/storage wrapper |
| R0C-SAVE-001 | Two-generation transaction/fault model | PASS | Deferred | Awaiting | Host model passes; DEC-012 approved for sacrificial fixture only |

## Attic wrapper update (append-only)

`R0C-PLAT-ATTIC-001` is now implemented as the admitted private, zero-argument
45GS02 bounded CPU-copy proof helper in `src/platform/r0c_attic_45gs02.s`.
The helper exercises real flat Attic source `$08000000`, copies six bytes into
the owned `$050000` staging window, and is validated by the R0-C result block.
Host and XEMU evidence are PASS; physical ABI/clobber evidence remains pending.
ROM-reclaim remains deferred and is not part of this wrapper.
| R0C-MEDIA-001 | Removal/change/write-protect/full-media faults | Deferred | Deferred | Awaiting | Sacrificial D81 approved; requires admitted target adapter and physical fault evidence |

Inherited R0-B physical platform evidence remains accepted at commit
`18cac27f1d0de9b50123ccfd4148ad40a3ecec4c`; it is not substituted for any
R0-C storage, package, or save evidence.

Candidate package SHA-256:
`9b535b022c97a7b9eb52552ac07f7776c677f23a3c604b75f9541d43c114f19f`.

Candidate D81 SHA-256:
`ba72aa82387f7e65551e893a3274f1c7f26a813416652c4aeab73c6a8b7e7e38`.

Authority/decision blocker detail is recorded in
`docs/reports/R0-C_AUTHORITY_BLOCKERS.md`.
