# R0-D D3 Physical Release Record

```text
D81_STATE: TEST_ELIGIBLE
D81_FILENAME: F65R0D3.D81
D81_SHA256: 107c6a356b932e9ade875c24539d75b1b0a0078122a6a3910f524570aafec5ef
D81_BYTES: 819200
DISK_LABEL: F65 R0-D3
DISK_ID: 65
ENTRY_FILENAME: AUTOBOOT.C65 -> R0D-CALIB
SOURCE_BRANCH: codex/r0-d-development
SOURCE_COMMIT: dfd8bb16c65fb14d5e2cac3074819c2d796ddaf3
BUILDER_IDENTITY: toolchain/vice-clean/bin/c1541, SHA-256 73235289aca30a7e2e8067e521bf604743156cc1d7499c888a3894d6e46fcb3c
STRUCTURAL_VALIDATOR_IDENTITY: tools/diagnostics/r0d_d81_loadability_gate.py
HOST_STRUCTURAL_RESULT: PASS
HOST_CONTENT_RESULT: PASS
XEMU_RESULT: PASS — two clean drive-8 AUTOBOOT runs
XEMU_EVIDENCE: docs/evidence/r0d/R0D-D81-D3-XEMU-RELEASE.md
SD_COPY_SHA256: 107c6a356b932e9ade875c24539d75b1b0a0078122a6a3910f524570aafec5ef — exact match at /Volumes/MEGA65FDISK/F65R0D3.D81
PHYSICAL_CHOOSER_RESULT: PASS
PHYSICAL_EVIDENCE: docs/evidence/r0d/physical/F65R0D3-PHYSICAL-DIRECTORY.jpg; docs/evidence/r0d/physical/F65R0D3-PHYSICAL-CALIBRATION.jpg
```

The owner copied the unchanged D3 file to `MEGA65FDISK`, ran `sync`, and
returned the exact expected SHA-256. The physical chooser then showed the
readable `F65 R0-D3` directory with `AUTOBOOT.C65` and `R0D-CALIB`; the next
photo shows the R0-D calibration screen running on the MEGA65.

This establishes the D81 loadability chain for this exact artifact through
`TEST_ELIGIBLE`. It does not select measured limits, prove production timing,
or close a later R0-E/R0-F gate.
