# D81 MEGA65-Native Slot Delivery

## Decision

Use a fresh D81 slot allocated by the MEGA65 Freezer itself when the existing
system SD card must be preserved, Ethernet is unavailable, and normal macOS
copy allocation does not pass the one-extent gate. This replaces the incorrect
blank-card recommendation and does not attribute the defect to the card or the
MEGA65 hardware.

## Official-source basis

Official `mega65-freezemenu` source commit
`844754576a6f1a4e92e4c10614ea853719d56037` was inspected locally.

- `makedisk.c` accepts an eight-character name for `NEW D81 DD IMAGE`, appends
  `.D81`, and calls `fat32_create_contiguous_file()` with
  `80 * 10 * 2 * 512`, exactly 819,200 bytes.
- `fdisk_fat32.c` documents that this routine creates a contiguous file, scans
  for enough consecutive free clusters, and writes the FAT chain.
- `freeze_diskchooser.c` maps error `0x8B` to `IMAGE FRAGMENTED`. Error `0xFF`
  is not that mapping; it reaches the generic error display, while an older
  commented table describes it as `NO SUCH TRAP / EOF`.

Consequently, a chooser `FF` proves that attach failed before the contained
program ran, but it does not independently prove fragmentation. Exact-byte and
FAT-chain evidence must localize the fault.

## Controlled procedure

1. Fresh-build and host-verify a candidate whose uppercase FAT 8.3 host name is
   the final authorized name.
2. On the MEGA65, create a never-tested root slot with `NEW D81 DD IMAGE` using
   the same stem.
3. Move the safely powered-down card to macOS.
4. Run `tools/diagnostics/d81_sd_fill_mega65_slot.sh` under `sudo`.
5. The helper proves the preimage is one extent, takes a verified host backup,
   writes exactly 819,200 bytes with `conv=notrunc`, proves the final hash and
   one-extent allocation, and safely ejects.
6. Only then select that exact name in the physical chooser.

The procedure neither resizes nor replaces the FAT directory entry, so the
Freezer-created cluster chain remains intact. It never modifies system/parent
files. If a post-write check fails, the helper restores the slot's original
bytes in place and leaves the card mounted for inspection.

## R0-E candidate identity

```text
HOST_FILENAME: F65R0EF.D81
D81_BYTES: 819200
D81_SHA256: ca85f73ffba93ea290078a60b372406dc6ab58eddacdf0765f7589cea039c40f
DISK_LABEL: F65 R0-E
DISK_ID: 65
ENTRY_FILES: AUTOBOOT.C65, R0E-PROOF, R0E-EVID
BUILDER: toolchain/vice-clean/bin/c1541
BUILDER_SHA256: 73235289aca30a7e2e8067e521bf604743156cc1d7499c888a3894d6e46fcb3c
D81_STATE: HOST_CONTENT_VERIFIED; AWAITING XEMU/SD/PHYSICAL GATES
```

The filename is new because prior E2/E3/E4 tested copies are retired. The D81
bytes reproduce the already recorded R0-E one-variable PRG-delta candidate;
only the host filename changes to match the new MEGA65-created slot.
