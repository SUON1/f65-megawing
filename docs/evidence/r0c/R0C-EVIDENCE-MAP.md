# R0-C Evidence Map

Status: **implementation evidence in progress; this is not an R0-C closure record.**

| Test ID | Proof | Host | Xemu | Physical | Evidence / limitation |
|---|---|---|---|---|---|
| R0C-ID-001 | Pinned proof identity and 96-byte `$1800` result block | PASS | PASS | Awaiting | `build/r0c/evidence/r0c-*-evidence.json` |
| R0C-PKG-001 | Explicit-LE, bounded package header/directory/integrity | PASS | PASS (target identity) | Awaiting | `R0CPROOF.PKG`; host mutation corpus |
| R0C-CAP-001 | Exact combined witness and every one-over rejection | PASS | PASS (target identity) | Awaiting | `r0c-capacity-report.json` |
| R0C-RES-001 | Handle sentinel/range validation | PASS | PASS | Awaiting | Target has a bounded proof directory |
| R0C-STG-001 | Deterministic CPU copy into owned proof buffer | PASS | PASS | Awaiting | **Attic-model only**; not a physical Attic RAM service proof |
| R0C-NODISK-001 | No tactical disk function linked into target diagnostic | PASS | PASS | Awaiting | Static guard; not a loaded-package tactical run |
| R0C-ROM-001 | Post-ROM-reclaim storage handoff | Deferred | Deferred | Awaiting | No admitted authoritative restoration/storage wrapper |
| R0C-SAVE-001 | Two-generation transaction/fault model | PASS | Deferred | Awaiting | Host model passes; DEC-012 is open |
| R0C-MEDIA-001 | Removal/change/write-protect/full-media faults | Deferred | Deferred | Awaiting | Requires DEC-012 and sacrificial physical medium |

Inherited R0-B physical platform evidence remains accepted at commit
`18cac27f1d0de9b50123ccfd4148ad40a3ecec4c`; it is not substituted for any
R0-C storage, package, or save evidence.
