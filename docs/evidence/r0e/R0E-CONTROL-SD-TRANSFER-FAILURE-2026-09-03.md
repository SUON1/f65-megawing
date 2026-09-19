# R0-E Control Requalification Transfer Failure — 2026-09-03

```text
CONTROL_IDENTITY: F65R0E.D81
CONTROL_SHA256: 8cb76830489095a92a266c884e168efacfd6cb8e7d4db456300a3fbf67cc623b
CONTROL_BYTES: 819200
SOURCE: /private/tmp/r0e-evidence-worktree/build/r0e/artifacts/F65R0E.D81
TRANSFER_HELPER: tools/diagnostics/d81_sd_transfer.sh
STAGING_PATH: /Volumes/MEGA65FDISK/SF65R0E.TMP
STAGING_COPY_SHA256: 8cb76830489095a92a266c884e168efacfd6cb8e7d4db456300a3fbf67cc623b
SD_FILESYSTEM: MS-DOS FAT32
SD_DEVICE_IDENTIFIER: disk4s1
SD_EXTENT_COUNT: 5
SD_CONTIGUITY_RESULT: FAIL
FINAL_PATH: /Volumes/MEGA65FDISK/F65R0E.D81
FINAL_FILE_CREATED: NO
STAGING_CLEANUP: PASS
SAFE_EJECT: NOT ATTEMPTED
PHYSICAL_CHOOSER: NOT ATTEMPTED
```

The transfer helper correctly stopped before the final name, safe eject, or
MEGA65 chooser. Its temporary staging file was then removed. The copied bytes
were exact, but FAT32 allocated them in five physical extents: 622,592 bytes,
131,072 bytes, 4,096 bytes, 20,480 bytes, and 40,960 bytes.

This is a delivery-medium allocation failure, not a D81-construction or
MEGA65-hardware finding. No payload was rebuilt, and no physical result is
claimed. A new physical control pass requires a contiguous 819,200-byte FAT32
region, obtained through an explicitly authorized dedicated-media preparation
or MEGA65 Ethernet transfer.
