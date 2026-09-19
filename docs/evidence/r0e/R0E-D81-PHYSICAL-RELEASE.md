# R0-E D81 Physical Release Record

```text
D81_STATE: TEST_ELIGIBLE
D81_FILENAME: F65R0E.D81
D81_SHA256: 8cb76830489095a92a266c884e168efacfd6cb8e7d4db456300a3fbf67cc623b
D81_BYTES: 819200
DISK_LABEL: F65 R0-E
DISK_ID: 65
ENTRY_FILENAME: AUTOBOOT.C65 -> R0E-PROOF
SOURCE_BRANCH: codex/r0-e-development
SOURCE_COMMIT: ae2b0aee2ded09622c67fcea97062b45fd6ce9ce
BUILDER_IDENTITY: toolchain/vice-clean/bin/c1541, SHA-256 73235289aca30a7e2e8067e521bf604743156cc1d7499c888a3894d6e46fcb3c
STRUCTURAL_VALIDATOR_IDENTITY: tools/diagnostics/r0e_d81_loadability_gate.py
HOST_STRUCTURAL_RESULT: PASS
HOST_CONTENT_RESULT: PASS
XEMU_RESULT: PASS — two clean drive-8 AUTOBOOT functional-proxy runs
XEMU_EVIDENCE: docs/evidence/r0e/R0E-D81-XEMU-RELEASE.md
SD_COPY_SHA256: 8cb76830489095a92a266c884e168efacfd6cb8e7d4db456300a3fbf67cc623b — exact match at /Volumes/MEGA65FDISK/F65R0E.D81
PHYSICAL_CHOOSER_RESULT: PASS
PHYSICAL_EVIDENCE: docs/evidence/r0e/physical/F65R0E-PHYSICAL-CHOOSER.jpg; docs/evidence/r0e/physical/F65R0E-PHYSICAL-BANNER.jpg
```

The owner copied the unchanged D81 to `MEGA65FDISK`, ran `sync`, and returned
the exact expected SHA-256. The chooser photo shows `F65R0E.D81` selected with
a readable directory containing `AUTOBOOT.C65`, `R0E-PROOF`, and `R0E-EVID`,
without a chooser error. The banner photo shows the R0-E functional-proxy
program running on the MEGA65 with its displayed proxy cases reporting `PASS`.

Photo SHA-256 identities:

- `F65R0E-PHYSICAL-CHOOSER.jpg`:
  `202ab9ebc980c48e4e976f3b1a97e30f28119f642629c620547ae773e23d194f`
- `F65R0E-PHYSICAL-BANNER.jpg`:
  `eb1cd541827aa795579d357914979a48d41a9ed4f3f0202f2628dc3c4a97175f`

This completes the D81 carrier chain through `TEST_ELIGIBLE` for the bounded
R0-E functional-proxy scope. It does not record a pinned MEGA65 core/ROM
identity, timing measurement, DMA execution, IRQ result, phase sweep, measured
limit, R0-E closure, or R0-F closure.
