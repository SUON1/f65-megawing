# R0-E4 D81 Host Candidate — 2026-09-02

```text
D81_STATE: INVALID — PHYSICAL CHOOSER FF ON 2026-09-03
D81_FILENAME: F65R0E4.D81
D81_SHA256: a92c61800e44c0e84892cf3d38c5b0c701700b1055bf3882b11148680ec231ef
D81_BYTES: 819200
DISK_LABEL: F65 R0-E4
DISK_ID: 65
SOURCE_BRANCH: codex/r0-e-development
SOURCE_COMMIT: 7d845e5
CONSTRUCTION: fresh format plus AUTOBOOT.C65, F65-R0E-PROOF.prg, and R0E-EVID.txt in one clean c1541 session
BUILDER: toolchain/vice-clean/bin/c1541 (locked identity verified by the structural gate)
PAYLOAD_PROVENANCE: retained R0-E3 host/Xemu-validated payload set; payload PRG SHA-256 a40f6d7acccea3b85aacb0c098440b8392ec4647a8a84f2a5905eccb34463c22
HOST_STRUCTURAL_RESULT: PASS
HOST_CONTENT_RESULT: PASS
XEMU_RESULT: NOT VERIFIED — pinned Java/LLVM-MOS/Xemu binaries are absent from this checkout
SD_COPY_RESULT: NOT STARTED
SD_CONTIGUITY_RESULT: NOT STARTED
PHYSICAL_CHOOSER_RESULT: FAIL — ERROR CODE FF; see R0E4-D81-FAILURE-2026-09-03.md
```

`F65R0E4.D81` is now retired after its physical chooser failure. Its prior
host-content record remains preserved for the forensic comparison; it is not
evidence that the carrier was eligible for physical delivery.
