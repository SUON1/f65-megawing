# L3 owner CLI delivery proposal — not executed

The new [release](release.json) passes host and four exact-name Xemu gates.
The owner authorized constructing L3; the raw allocation method remains a
separate owner decision under the [D81 workflow](../../../../D81_WORKFLOW.md).
This command is prepared for review. **Running it performs a real card write**;
do not run it as a read-only audit. No automatic transfer or Terminal launch.

Use the owner's CLI session after choosing this route and inserting the intended
card, mounted at /Volumes/MEGA65FDISK. Its expected UUID below matches the
retained owner L2 audit and the current read-only mounted-volume inspection.
The installer resolves the live partition again and rejects a different UUID,
non-removable/non-FAT32 volume or missing mount. No L3 final/staging name was
observed through the mounted filesystem; raw aliases, filesystem health and
free run remain unverified. No remembered device number is used by the command.

```sh
sudo /usr/bin/python3 -B \
  /Users/slice/Developer/f65-megawing/tools/diagnostics/d81_direct_delivery.py install-sd \
  /Users/slice/Developer/f65-megawing/build/r0f/group2/control/trial-jnt4dplw/carrier-l3/canonical/R0FG2L3.D81 \
  --manifest /Users/slice/Developer/f65-megawing/build/r0f/group2/control/trial-jnt4dplw/carrier-l3/canonical/release.json \
  --mount /Volumes/MEGA65FDISK \
  --volume-uuid 83FFC12E-67E1-307F-91AD-E584C2E01E87 \
  --qualification /Users/slice/Developer/f65-megawing/docs/evidence/r0f/successor/2026-09-22-workflow/R0FCAP14/allocator-qualification-1.json \
  --report /Users/slice/Developer/f65-megawing/build/r0f/group2/control/trial-jnt4dplw/carrier-l3/sd-install-01 \
  --confirm-raw-write
```

The report directory must be fresh. The pinned wrapper independently requires
the exact release/hash, unchanged eight-input allocator qualification, no final
or staging alias, clean read-only filesystem checks, matching FATs, sufficient
actual contiguous free clusters and spare root slots. It unmounts without force,
preserves allocation metadata off-card, stages R0FG2L3.TMP, verifies staged/final
hash and one extent, reads back after mounting and safely ejects. Only L3 and
its required allocation metadata are added. Preserve L2/P09/all existing files.
The raw write is not power-loss transactional; keep the card connected during
an authorized installation. Any failure stops; retain evidence/staging and do
not retry, repair, reformat or roll back automatically.

An installer PASS still leaves physical chooser verification pending. Review
sd-install-01/sd-release.json for the exact L3 hash, one extent and safe-eject
PASS before following the [one-run physical procedure](../../../../plans/R0-F_GROUP2_HARDWARE_TEST.md).
Select R0FG2L3.D81, confirm directory/ordinary AUTOBOOT entry, photograph the
expected red S5/E03/F00 result and return the card. Do not remove G1T00 or rerun.
SD delivery, physical proof, full Group 2/R0-F acceptance and publication remain
separate; no commit/push is authorized by this proposal.
