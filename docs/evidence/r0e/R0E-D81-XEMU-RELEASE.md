# R0-E Xemu Release Record

```text
D81_STATE: XEMU_BOOT_VERIFIED
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
XEMU_EVIDENCE: docs/evidence/r0e/xemu/r0e-xemu-evidence.json
SD_COPY_SHA256: AWAITING R0-F / HUMAN
PHYSICAL_CHOOSER_RESULT: AWAITING R0-F / HUMAN
PHYSICAL_EVIDENCE: AWAITING R0-F / HUMAN
```

Both clean headless Xemu starts mounted the exact D81 at drive 8, auto-loaded
`AUTOBOOT.C65 -> R0E-PROOF`, and reached the stable functional-proxy banner.
Their screen SHA-256 is
`6df9b459ac895c7f787e5568a17aa75b8d6dc6e323cbedc3b728286cd9581e84`; their
`$1900-$19FF` result-block SHA-256 is
`4bd6ed488108739cbab916035f557f1f7972ca3bd068fb082203a0e274cfadbf`.

The pinned Xemu was `20260129235930` at source commit
`40dfef0d1d5f56be2469492715c12bdb32c75b67`; the owner ROM SHA-256 was
`af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0`.
The D81 SHA-256 remained the recorded host-gated value after both boots.

This validates a bounded functional proxy only. Timing is `NOT_MEASURED`, DMA
is `DMA_HARDWARE_PROBE_NOT_EXECUTED`, and no IRQ result is claimed. Xemu cannot
verify the MEGA65 physical chooser, phase-swept timing, or physical hardware;
this carrier is not `PHYSICAL_CHOOSER_VERIFIED` or `TEST_ELIGIBLE`.
