# L3 physical export-collision observation

2026-10-04. **Observable rejection/preservation PASS; operator record incomplete.
Group 2 remains unfinished.**

Owner confirms selecting R0FG2L3.D81, using ordinary AUTOBOOT.C65 and returning
the card to the Mac. The original terminal photo visibly supplies red border
and `G1 EXPORT S:5 E:03 F:00`. Actual returned-card checks pass: exactly the four
unchanged inputs plus correct 34-byte RSSTATE, no extra chunks, valid D81
directory/BAM/chains. See [combined result](result.json),
[operator confirmation](operator-note.json) and [checker result](validation.json).

## Exact acquisition and reuse

Pre-run canonical: 819200 bytes, SHA-256
`c3df1ceda3979cf6e49e7885b563555379c7d64557360bed0d288144085092e5`.
Owner's raw audit passes exact name/short name, bytes/hash and one full extent;
its supplied array is retained here. The complete pre-run inspector/device
report was not supplied. No new allocator or SD writer was used by the agent.

Live returned volume was identified as removable MS-DOS FAT32, UUID
`83FFC12E-67E1-307F-91AD-E584C2E01E87`, device /dev/disk4s1 at acquisition only.
Fresh snapshot from `/Volumes/MEGA65FDISK/R0FG2L3.D81` is 819200 bytes, SHA-256
`966f32869d0906a7660bcf0eb427c40feeecc7fe3209e2ff8b426902b7637ef1`.
Source before/after and new read-only host snapshot are byte-identical. The
snapshot remains local at the exact path in [local-artifacts.json](local-artifacts.json).
This hash also matches the retained PAL postimage, but this acquisition came
from the positively identified returned SD file; no emulator image was substituted.

The [acquisition](acquisition.json) and [volume metadata](volume-identity.plist)
retain provenance. [Disk check](post-disk.json), actual extracted payloads and
original photo are preserved in this packet. The original photo observation
and its pending fields are preserved as recorded earlier; subsequent owner
confirmation and new checks live in this packet, without rewriting history.

The read-only checker verifies canonical release/frozen linked inputs, compares
pinned-tool extraction with independent structure/content checks, compares all
four inputs, and independently derives the expected SAVE address/checksum.
[Command](check-command.json) exited 0:

```sh
/usr/bin/python3 -B tools/diagnostics/r0f_group2_collision_return.py --image build/r0f/group2/control/trial-jnt4dplw/carrier-l3/physical-return-01/snapshot/R0FG2L3.D81 --release build/r0f/group2/control/trial-jnt4dplw/carrier-l3/canonical/release.json --out build/r0f/group2/control/trial-jnt4dplw/carrier-l3/physical-return-01/checks
```

The checker's unmodified `RETURNED_FILE_CHECKS_PASS_OPERATOR_PHOTO_PENDING`
result intentionally does not inspect photos. Photo/owner evidence is combined
separately in result.json. Do not rerun this command into its existing output.
Retained normal/P09/host/Xemu proof is reused; no target compile or execution
was repeated during acquisition/checking.

## Remaining record and proof boundaries

Safe ejection before testing and one-run/no-reset/reload remain unconfirmed.
No chooser photograph was supplied; directory readability was not separately
recorded. Actual video/core/HYPPO/ROM/Freezer identities remain UNKNOWN. Pending
operator confirmation was requested; do not infer it or rerun a carrier to fill
these gaps. Formal bounded-case closure and the complete release chain remain
pending review; TEST_ELIGIBLE is not asserted.

This proves the observed rejection and preservation effects for this run. E:03
does not uniquely identify the failed KERNAL call or DOS error; physical attempt
count is not measured. The SAVE is the pre-storage checksum fixture, not full
512-byte lifecycle/service-state or timing proof. Other G2-L and G2-Q/S/P/D/A
cases, live capture fit/schema/reducer, acceptance and measured limits remain
open. Historical Group 2 allocation remains unrecovered; Group 3 is unassigned.
No commit or push occurred.

[Build Intent](../../../../plans/R0-F_GROUP2_BUILD_INTENT.md),
[hardware procedure](../../../../plans/R0-F_GROUP2_HARDWARE_TEST.md), generated
export contract/amendment/ledger and D81 gate/workflow govern. Evidence-only
changes have non-applicable register/clobber, CPU-visible/physical memory,
MAP/base-page, DMA, timing/deadline and IRQ/NMI effects. No generated authority,
capacity, reserve, integrity check or threshold changed. P09, failed L2 and
historical/unrelated SD work remain untouched. SHA256SUMS covers this packet;
the large immutable returned D81 remains local and hash-identified.
