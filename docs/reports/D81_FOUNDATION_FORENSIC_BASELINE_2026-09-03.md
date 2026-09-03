# D81 Foundation Forensic Baseline — 2026-09-03

## Scope

This investigation treats the SD card and MEGA65 hardware as controls. It
compares the exact successful R0-E carrier to the failed R0-E2, R0-E3, and
R0-E4 carrier images before another carrier is constructed.

## Exact artifacts

| Role | File | SHA-256 | Physical outcome |
|---|---|---|---|
| Control | `F65R0E.D81` | `8cb76830489095a92a266c884e168efacfd6cb8e7d4db456300a3fbf67cc623b` | PASS |
| Failed | `F65R0E2.D81` | `e1955eff6f474a77e1b1c889b16bf38a3443db9a0213e78b44bdb605b89337de` | chooser `FF` |
| Failed | `F65R0E3.D81` | `7f1e9c79476a6dd3e55d94e1bc9a7ab624e4448cf8c6531946a730d24350d445` | chooser `FF` |
| Failed | `F65R0E4.D81` | `a92c61800e44c0e84892cf3d38c5b0c701700b1055bf3882b11148680ec231ef` | chooser `FF` |

## Measured facts

- All four images are exactly 819,200 bytes and pass the independent raw D81
  parser: header pointer, BAM counts, allocated-sector ownership, directory
  links, file chains, block counts, terminal-sector lengths, and payload hashes.
- R0-E3 and R0-E4 differ in exactly one byte: track 40, sector 0, offset 12,
  the final `3`/`4` character of the disk label. Their BAMs, directory entries,
  file chains, payload bytes, and all other bytes are identical.
- R0-E2 and R0-E3 differ only in label/ID metadata and its replicated BAM
  identity fields. The disk-ID change did not repair mountability.
- The successful control and failed family use the same `AUTOBOOT.C65`, the
  same three directory names, the same file order, and the same contiguous
  track-39 in-image allocation order.
- The substantive image difference is the newer `R0E-PROOF` payload: the
  control contains 3,903 payload bytes in 16 blocks; E2/E3/E4 contain 5,258
  bytes in 21 blocks. Their associated evidence file also differs.

These are forensic observations, not a claim that a PRG payload itself can
cause the chooser to execute it. `ERROR CODE FF` still occurs before the entry
program runs. The remaining necessary discriminator is the exact E4 SD-copy
hash and allocation record, followed by a one-variable reconstruction of the
known-good control construction path.

## Reconstruction results

The retained control was extracted and freshly reconstructed with the pinned
`c1541`, the exact `F65 R0-E,65` format string, and the original write order.
The reconstructed image has the exact physical-pass SHA-256
`8cb76830489095a92a266c884e168efacfd6cb8e7d4db456300a3fbf67cc623b` and is
byte-for-byte identical to `F65R0E.D81`. The historical construction procedure
is therefore deterministic and preserved.

The first one-variable local image has also been built:

```text
F65R0E-PRG-DELTA.D81
SHA-256: ca85f73ffba93ea290078a60b372406dc6ab58eddacdf0765f7589cea039c40f
format/label/ID: F65 R0-E / 65 — unchanged from physical-pass control
AUTOBOOT.C65: unchanged from physical-pass control
R0E-EVID.txt: unchanged payload from physical-pass control
R0E-PROOF.prg: only changed input; 5,258 bytes / 21 D81 blocks
```

The larger PRG necessarily moves the unchanged evidence file from track 39,
sector 17 to track 39, sector 22. Its structural comparison passes; it has not
been presented to Xemu, copied to an SD card, or physically chooser-tested.

## Permanent control

`tools/diagnostics/d81_foundation_compare.py` is the retained, read-only
comparator. It reports raw D81 structural validity, payload identities, and
every byte-level difference grouped as header, BAM, directory, payload, or
unallocated region. `docs/testing/D81_FOUNDATION_QUALIFICATION.md` defines the
required one-variable reconstruction sequence. Neither tool substitutes for
the physical chooser gate.
