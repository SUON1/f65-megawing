# R0-D D3 Xemu Release Record

```text
D81_STATE: TEST_ELIGIBLE — superseded by R0D-D81-D3-PHYSICAL-RELEASE.md
D81_FILENAME: F65R0D3.D81
D81_SHA256: 107c6a356b932e9ade875c24539d75b1b0a0078122a6a3910f524570aafec5ef
D81_BYTES: 819200
DISK_LABEL: F65 R0-D3
DISK_ID: 65
ENTRY_FILENAME: AUTOBOOT.C65 -> R0D-CALIB
SOURCE_BRANCH: codex/r0-d-development
SOURCE_COMMIT: 48b3647fea18cfd7cb80d4f4ab3f242b096c3b38
BUILDER_IDENTITY: toolchain/vice-clean/bin/c1541, SHA-256 73235289aca30a7e2e8067e521bf604743156cc1d7499c888a3894d6e46fcb3c
STRUCTURAL_VALIDATOR_IDENTITY: tools/diagnostics/r0d_d81_loadability_gate.py
HOST_STRUCTURAL_RESULT: PASS
HOST_CONTENT_RESULT: PASS
XEMU_RESULT: PASS — two clean drive-8 AUTOBOOT runs
XEMU_EVIDENCE: docs/evidence/r0d/xemu/r0d3-d81-xemu-evidence.json
SD_COPY_SHA256: 107c6a356b932e9ade875c24539d75b1b0a0078122a6a3910f524570aafec5ef — exact match at /Volumes/MEGA65FDISK/F65R0D3.D81
PHYSICAL_CHOOSER_RESULT: PASS
PHYSICAL_EVIDENCE: docs/evidence/r0d/physical/F65R0D3-PHYSICAL-DIRECTORY.jpg (SHA-256 569bb7b4bfce67529a7f3e0b652421f9b66df99eb295ab4376c2cb75e2955b91); docs/evidence/r0d/physical/F65R0D3-PHYSICAL-CALIBRATION.jpg (SHA-256 80675aa04d16681c7de216322e6910745d437eac5e45197c9e3a38cdb472ade9)
```

Both clean Xemu starts mounted the exact D81 at drive 8, auto-loaded its entry,
and reached the stable calibration screen. The screen SHA-256 was
`cd424a2b51109d891a3c3388f0da114042462ddab43f543d912bcdff41e8bcf2` for both
boots. The `$1860-$18DF` result-block SHA-256 was
`24f8e8dac28e79d9615bbae9fb58b716e92cf55b515e66483769721cf14587f7` for both
boots.

The pinned Xemu was `20260129235930`, source commit
`40dfef0d1d5f56be2469492715c12bdb32c75b67`, with the owner ROM SHA-256
`af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0`.
The post-run host structural/content gate also passed with the unchanged D81
SHA-256 above.

Xemu cannot verify the MEGA65 physical chooser. This image is not
`PHYSICAL_CHOOSER_VERIFIED` or `TEST_ELIGIBLE`.

The owner then returned the mandatory SD-copy SHA-256, which matches the exact
D3 artifact. The physical directory and calibration-screen evidence now promote
this artifact to `TEST_ELIGIBLE`; see
`docs/evidence/r0d/R0D-D81-D3-PHYSICAL-RELEASE.md`.
