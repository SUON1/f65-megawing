# D81 native-blank examination — 2026-09-22

## Findings

The owner reports physical chooser `ERROR CODE FF` for `R0FDIAG2.D81` and
supplies a newly MEGA65-formatted blank. The actual on-card blank filename is
`R0FDIAG3.D81`, not the `F0FDIAG3` spelling in the message. Examination is
read-only on the card; no transfer, rename, overwrite, repair or eject was
performed. Local evidence copies were retained.

| Image | Bytes | Internal filesystem result | Files / free sectors |
| --- | ---: | --- | --- |
| Native `R0FDIAG3.D81` | 819200 | PASS | 0 / 3196 |
| Failed SD `R0FDIAG2.D81` | 819200 | PASS | 3 / 3106 |
| Previously run SD `R0FHOST1.D81` | 819200 | PASS | 4 / 3107 |
| Retained CF001 physical-pass control | 819200 | PASS | 3 / 3074 |

The native blank has a 40/3 directory pointer, a terminated empty directory,
consistent BAM counts, and precisely four allocated filesystem sectors.
All bytes outside track 40 are zero. Its label is `R0FDIAG3`, disk ID `F6`,
and header DOS identifier `1D`. SHA-256:
`357078cd97a9aae0bf676ed844e5a01bfcafd32994309cf0d657f53e2a590018`.

The failed SD copy exactly matches the canonical T06 source hash:
`912df16828f1c60127e4fcdd8d545dfca0c2ad8fe6a24a64ae01b4ac280df17d`.
All three contained PRG payload hashes match the build record. Its `3D`
header identifier and high-bit PETSCII label conventions also occur in the
previously working `R0FHOST1` image. These differences from the native blank
are therefore not sufficient evidence of the chooser failure's cause.

The SD `R0FHOST1` now includes the expected `RSSTATE` saved file. Its current
hash `2ad1c08b75efcae9e35438bf82da3ba23e59666ef8c2a7296c939aa56d55134d`
is a post-execution identity, not the pre-run `3721dff9...` identity.

## Proven weakness in the host allocation method

The live Mac is macOS 26.7, build `25G229`. `mount` reports the intended
`/dev/disk4s1` volume as `msdos` with `fskit`. Its volume UUID is
`83FFC12E-67E1-307F-91AD-E584C2E01E87`; diskutil reports about 26.4 GB free.
These findings do not diagnose card failure or shortage of total free space.

Apple's published FSKit FAT implementation explicitly ignores
`FSPreallocateFlagsContig`, calls allocation with `mustBeContig:false`, and
uses best effort. Source:
[FATVolume.m, lines 2185–2192](https://github.com/apple-oss-distributions/msdosfs/blob/c9f076c4e7c10b4bc3b0177d114aedf1bb8b9109/msdos_appex/FATVolume.m#L2185-L2192).
This published implementation is consistent with the previously observed
successful preallocation request followed by a 22-extent raw audit. It is not
a binary-source attestation for the installed driver build.

Our helper's claim that request acceptance demonstrated contiguous-allocation
support was incorrect. A one-extent success for an earlier file did not prove
repeatability. Diagnostic output and documentation now say allocation was
reported, with contiguity unverified until the raw FAT audit passes.

The old T06 wrapper also selected native-slot filling solely from the existence
of a matching filename. That is not sufficient provenance and would be unsafe
now that the matching image has failed. The wrapper is disabled before media
access, including with sudo. No replacement is released by this examination.

## Native implementation and remaining work

The official MEGA65 creator explicitly finds/allocates a contiguous FAT range
before formatting it. It also automatically attaches the new image; earlier
advice to create it without mounting was not literally achievable in that UI.
[Native creator, lines 339–365](https://github.com/MEGA65/mega65-freezemenu/blob/844754576a6f1a4e92e4c10614ea853719d56037/makedisk.c#L339-L365).

The initial raw audit required the owner's local sudo authentication. The
owner subsequently supplied it; the exact JSON is now retained alongside
the foundation evidence as `raw-audit.json`. It establishes:

| Exact name | SHA-256 prefix | Extents | Meaning |
| --- | --- | ---: | --- |
| R0FDIAG2.D81 | 912df16828f1c601 | 13 | Failed Finder copy; canonical bytes unchanged |
| R0FDIAG3.D81 | 357078cd97a9aae0 | 1 | Native blank, 819200 bytes |
| R0FHOST1.D81 | 2ad1c08b75efcae9 | 1 | Previously mounted/run carrier, post-run contents |

The old 22-extent record belongs to the removed staging file, not the Finder
copy. Both allocation measurements are now distinguished. No current extent
count is inferred merely from chooser FF or filename. The failed copy's bytes
are internally consistent but its allocation fails the MEGA65 delivery gate.

A repeatable host solution must actually reserve one contiguous FAT range,
not depend on FSKit honoring this flag. The subsequently approved workflow
qualifies a pinned official allocator on disposable fragmented FAT32 fixtures;
see `D81_WORKFLOW_R0FGIAG4_2026-09-22.md` for its bounded results.
Keep the native blank and failed image unchanged until their raw allocation
comparison is complete. The prior instruction to stop CLI transfers remains
in force; diagnostic CLI reads are separate and were explained as such.

## Evidence and checks

`tools/diagnostics/d81_foundation_compare.py` was run against retained
`docs/evidence/r0f/combined/F65BLK02.D81`, the native blank, the failed SD
image, the previously working SD carrier, and the original T04 canonical.
All passed its geometry/directory/file-chain/BAM ownership checks. The full
byte differences grouped by component are retained in
`docs/evidence/r0f/successor/2026-09-22-forensics/foundation.json`.

Local evidence identities:

- `foundation.json`: `08251ee776c6c33ffa9adae21b5317f801a22676a45566886d471ddff91b22c4`
- `R0FDIAG3-native-blank.D81`: `357078cd97a9aae0bf676ed844e5a01bfcafd32994309cf0d657f53e2a590018`
- `R0FDIAG2-chooser-ff.jpg`: `65b9d1bf2ea69a3462e3ca6de8c6822d90ff83ccfab20322b2934f5bd75f0518`

Target registers/clobbers, CPU/physical memory, MAP/base-page, DMA, deadlines,
IRQ/NMI and public contracts are not affected. No target rebuild or new Xemu
run is required for these diagnostic-message and retirement corrections.

Validation: all 18 `test_d81_delivery.py` tests PASS; `r0a_validate.py .` PASS;
shell syntax and `git diff --check` PASS. Invoking the retired T06 wrapper
returns exit 2 immediately. All three on-card hashes were rechecked and remain
unchanged after examination.
