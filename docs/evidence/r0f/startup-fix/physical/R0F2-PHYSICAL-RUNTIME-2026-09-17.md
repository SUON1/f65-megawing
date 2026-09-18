# F65R0F2 physical runtime observation — 2026-09-17

State: **PHYSICAL FUNCTIONAL/RUNTIME SCREEN OBSERVED; FULL R0-F OPEN**.

The owner supplied a photograph in the controlling conversation after the
guarded SD transfer. Visually inspected and retained unchanged as
`F65R0F2-runtime-2026-09-17.jpg` (137536 bytes), SHA-256
`900ae12dd595d50c2713a0634cd60662c2d35bd681221803cd2f4102f23869a7`.

Visible results:

- `BUILD: F65R0F2 STARTUP FIX`.
- `UNPACED 100HZ / 21-STAGE MODEL: FUNCTIONAL PASS`.
- `RASTER ACQUISITION: ALL 80 SAMPLES VALID`.
- Snapshot synchronous proxy, synthetic input/audio, unresolved modulo wraps,
  no DMA hardware probe, no IRQ measurement, and no physical-limit pass are
  explicitly labeled on screen.

This is physical startup/runtime evidence for the corrected bounded proxy.
The photo does not show the chooser directory, platform versions, raw result
bytes, card hash, or safe-eject completion. It is associated with the exact
carrier through the owner's transfer report and visible build identity, not
by extracting a cryptographic identity from the photo.

## SD evidence

Retained `F65R0F2.D81.slot-pre.json` and `.slot-post.json` match the owner-pasted
audit output. Both describe 819200 bytes at the same single FAT32 extent:
device offset 101085184, logical offset 0, partition disk4s1,
mount /Volumes/MEGA65FDISK, removable MS-DOS FAT32.

Pre-fill blank SHA-256:
`a79acc91b88861485a10aa33f6c44b1886ee94e03c91683ba19554dfe4c976ca`.
Post-fill SHA-256:
`24fabf16d8c85e7767f7caf23183c67995886ce96d126d2085eb387aff548297`, matching
the two-clean-boot Xemu carrier. Hash and unchanged single-extent checks PASS.
The supplied output ends before the safe-eject result; safe eject remains
**NOT CONFIRMED**. Successful runtime is not substituted for that missing log.
No complete `TEST_ELIGIBLE` release-chain claim is made.

## Remaining scope

This records successful physical execution of the startup fix; it does not
establish complete ABI preservation, calibrated elapsed time, independent-clock
deadlines, actual input/audio latency, stack/snapshot high-water, DMA/IRQ
measurements, full platform identity, or owner acceptance of R0-F. The full R0
gate and measured-limits revision remain open. No code, ABI, registers, memory,
MAP, DMA, IRQ/NMI or timing behavior changed in this evidence-only update.
