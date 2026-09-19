# R0-D Replacement D81 Release Record

```text
D81_STATE: INVALID — DO NOT USE
D81_FILENAME: F65R0D2.D81
D81_SHA256: 51dd4ad5a0fe402eccbac81b1ec0e44d12f5ab2294a9f01b1e7452711fa52643
D81_BYTES: 819200
DISK_LABEL: F65 R0-D
DISK_ID: 65
ENTRY_FILENAME: AUTOBOOT.C65 -> R0D-CALIB
SOURCE_BRANCH: codex/r0-d-development
SOURCE_COMMIT: 3dd5b33ba117557e8c40957db9c1999ccbba3594
BUILDER_IDENTITY: VICE c1541 3.10; SHA-256 597907f1cad64d74f33f3631fb23a9d9b0e66445069333d4025e92f8f03b4e3c
STRUCTURAL_VALIDATOR_IDENTITY: tools/diagnostics/r0d_d81_loadability_gate.py
HOST_STRUCTURAL_RESULT: PASS
HOST_CONTENT_RESULT: PASS
XEMU_RESULT: PASS — two clean D81 boots
XEMU_EVIDENCE: build/r0d/reports/R0D2-D81-XEMU-boot{1,2}.{log,screen.txt,memory.bin,png}; screen SHA-256 cd424a2b51109d891a3c3388f0da114042462ddab43f543d912bcdff41e8bcf2; result-block SHA-256 24f8e8dac28e79d9615bbae9fb58b716e92cf55b515e66483769721cf14587f7
SD_COPY_SHA256: 51dd4ad5a0fe402eccbac81b1ec0e44d12f5ab2294a9f01b1e7452711fa52643 — exact match on /Volumes/MEGA65FDISK/F65R0D2.D81
PHYSICAL_CHOOSER_RESULT: FAIL — ERROR CODE FF
PHYSICAL_EVIDENCE: docs/evidence/r0d/physical/F65R0D2-D81-CHOOSER-FF.jpg; SHA-256 877916ff5e9d4f82ab4412f198ea7847e0476b45316223887ec2b2d54024029c
```

`F65R0D.D81` and `F65R0D2.D81` are both invalid after physical chooser FF and
are not inputs to any future carrier. D2's copied-file hash matched its host
identity, so transfer corruption is not the explanation for its failure. It
is not final, loadable, or `TEST_ELIGIBLE`.
