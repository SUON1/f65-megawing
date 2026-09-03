# R0-E4 D81 Host Candidate — 2026-09-02

```text
D81_STATE: HOST_CONTENT_VERIFIED — NOT TEST_READY
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
PHYSICAL_CHOOSER_RESULT: NOT STARTED
```

`F65R0E4.D81` is a fresh carrier identity, not a renamed or modified failed
image. It must not be copied to the SD card until the exact hash completes two
clean Xemu boots. The missing local toolchain is a reproducibility/infrastructure
defect, not a reason to infer a target-code or MEGA65 hardware fault.
