# R0-D Replacement D81 Physical Chooser Failure — 2026-08-30

Status: **INVALID — DO NOT USE**

The physical MEGA65 chooser displayed `ERROR CODE FF` while the owner selected
`F65R0D2.D81`. This occurred before the image directory, `AUTOBOOT.C65`, or
`R0D-CALIB` could run. It is a carrier/chooser-mount failure, not an R0-D
program result.

```text
D81_FILENAME: F65R0D2.D81
HOST_D81_SHA256: 51dd4ad5a0fe402eccbac81b1ec0e44d12f5ab2294a9f01b1e7452711fa52643
D81_BYTES: 819200
PREVIOUS_STATE: XEMU_BOOT_VERIFIED
SD_COPY_DESTINATION: /Volumes/MEGA65FDISK/F65R0D2.D81
SD_COPY_SHA256: 51dd4ad5a0fe402eccbac81b1ec0e44d12f5ab2294a9f01b1e7452711fa52643 — exact match
PHYSICAL_CHOOSER_RESULT: FAIL — ERROR CODE FF
FAILURE_PHOTO: docs/evidence/r0d/physical/F65R0D2-D81-CHOOSER-FF.jpg
FAILURE_PHOTO_SHA256: 877916ff5e9d4f82ab4412f198ea7847e0476b45316223887ec2b2d54024029c
CONSTRUCTION_LOG: docs/evidence/r0d/physical/F65R0D2.D81-create.txt
CONSTRUCTION_LOG_SHA256: 1f24ced45cb44a51d8343dd28e45e6e56d7f738933857a68303db07c1361f029
LISTING_LOG: docs/evidence/r0d/physical/F65R0D2.D81-list.txt
LISTING_LOG_SHA256: 08a861e53b093de2fa3ec527d1a9d0848e011cf9f82aacc3cb82b0471b6d44fe
DISPOSITION: INVALID — do not copy, mount, patch, append, rename, or reuse
```

The source carrier used a new filename, a fresh 80-track format, one pinned
VICE `c1541` format/write session, raw structural/content validation, and two
clean D81 Xemu boots. The card copy hash matched exactly. Its label/ID profile,
PETSCII naming, directory start, DOS version, and construction shape match the
retained physical-pass R0-A carrier. Those facts rule out transfer corruption
and the prior D1 header-profile hypothesis; they do not prove another cause.

No third R0-D D81 is authorized. The required next diagnostic is a same-card,
hash-verified physical chooser control using the retained physical-pass
`F65-R0C-MEDIA.D81` identity, SHA-256
`e01eb41cff0158e7b609a365ecc72b78b3ce825ddca06a42a32f8954f4c7e8d0`.
