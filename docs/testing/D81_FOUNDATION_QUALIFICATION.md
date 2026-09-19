# D81 Foundation Qualification

This is a host-side forensic gate for a chooser `ERROR CODE FF`. It does not
replace the SD-copy or physical-chooser gates in `00_D81_LOADABILITY_GATE.md`.

## Fixed controls

- Control image: `F65R0E.D81`, SHA-256
  `8cb76830489095a92a266c884e168efacfd6cb8e7d4db456300a3fbf67cc623b`.
- This control is the retained R0-E physical chooser pass. It remains untouched.
- E2, E3, and E4 are failed identities and are comparison inputs only.

## Required investigation order

1. Run `tools/diagnostics/d81_foundation_compare.py` against the control and
   every failed image. Retain its JSON output.
2. Record the exact SD-copy SHA-256 and FAT32 extent result for each failed
   identity. This is an integrity discriminator, not a claim that the card or
   MEGA65 hardware is faulty.
3. Reconstruct the physical-pass control using its recorded builder, command,
   payloads, label, ID, and write order. It must pass every host/Xemu/physical
   gate before any R0-E payload change is introduced.
4. The reconstruction must reproduce the control hash byte-for-byte. A different
   result is a construction-path failure, even when its D81 parser result is
   otherwise valid.
5. Introduce one difference at a time and retain the comparison report for each:
   payload bytes, evidence file, disk label/ID, directory entry order, builder,
   and delivery method are separate changes.
6. Require two fresh physical chooser passes from the qualified construction
   route before another R0 feature carrier is admitted.

No D81 is called mountable based only on this comparator. The physical chooser
is the final authority for mountability.

## Existing system-card delivery

A blank or reformatted card is not required and must not be proposed as the
normal remedy: the MEGA65 system card contains required parent files. If a
normal direct copy fails the single-extent gate and Ethernet is unavailable,
create a fresh uniquely named slot at the SD root with the MEGA65 Freezer's
`NEW D81 DD IMAGE` command. The official Freezer allocates the 819,200-byte D81
as a contiguous FAT32 file.

After safely powering down and moving the card to macOS, fill that exact slot
without truncation:

```sh
sudo tools/diagnostics/d81_sd_fill_mega65_slot.sh \
  build/r0e/artifacts/F65R0EF.D81 \
  /Volumes/MEGA65FDISK \
  ca85f73ffba93ea290078a60b372406dc6ab58eddacdf0765f7589cea039c40f
```

The helper fails before writing unless the untouched slot already has the
right name, size, root location, and one physical extent. It backs up the slot,
replaces exactly 819,200 bytes in place, rechecks the candidate hash and the
same one-extent allocation, and safely ejects. A failure after writing starts
triggers an in-place rollback. No other SD file is changed.

In current official Freezer source, error `0x8B` has the explicit text
`IMAGE FRAGMENTED`. A displayed `ERROR CODE FF` remains a chooser/attach-stage
failure, but `FF` alone does not identify fragmentation; record the copied hash,
extent result, and platform identities before drawing a cause conclusion.
