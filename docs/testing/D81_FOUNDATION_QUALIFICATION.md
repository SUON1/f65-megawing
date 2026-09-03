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
4. Introduce one difference at a time and retain the comparison report for each:
   payload bytes, evidence file, disk label/ID, directory entry order, builder,
   and delivery method are separate changes.
5. Require two fresh physical chooser passes from the qualified construction
   route before another R0 feature carrier is admitted.

No D81 is called mountable based only on this comparator. The physical chooser
is the final authority for mountability.
