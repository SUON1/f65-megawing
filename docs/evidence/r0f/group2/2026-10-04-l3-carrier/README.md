# R0FG2L3 — exact-name collision carrier qualification

2026-10-04. **XEMU_BOOT_VERIFIED; SD and physical NOT RUN.**
Owner authorized "Build the working R0FG2L3.D81". This is the bounded
G2-L-EXPORT-COLLISION subcase of the prospectively approved broader suite;
Group 2 remains unfinished. No commit or push occurred.

## Artifact and authority

Canonical, never mounted writable:
`/Users/slice/Developer/f65-megawing/build/r0f/group2/control/trial-jnt4dplw/carrier-l3/canonical/R0FG2L3.D81`.

- 819200 bytes; SHA-256
  `c3df1ceda3979cf6e49e7885b563555379c7d64557360bed0d288144085092e5`.
- Disk label R0FG2L3, ID 65; ordinary entry AUTOBOOT.C65 loads R0FSUCC.
- Unchanged program R0FG2C1, 37284 bytes, SHA-256
  `46491ef275863dd89edd2af420092e7baff733b5b5e54064ea52cfcfbbb09f92`.
- Original [release](release.json): host structure/content PASS; two NTSC and
  two PAL clean exact-name boots PASS; TEST_ELIGIBLE false, GROUP2_COMPLETE false.

[Build Intent](../../../../plans/R0-F_GROUP2_BUILD_INTENT.md),
[physical procedure](../../../../plans/R0-F_GROUP2_HARDWARE_TEST.md),
generated export contract/amendment/ledger, D81 gate and reproducible delivery
workflow govern. HEAD and freshly fetched origin/main remain
abd3a0803b96090654db5dbdda43ad42d7b29a5a on codex/r0f-group2-preparation.

## Reuse, construction and exact-case results

The complete 129-file control freeze, original combined PRG/link artifacts,
actual-owner host admission and normal NTSC/PAL acquisitions are reused from
[the control packet](../2026-10-03-export-collision/README.md); none were replayed.
Resident end remains $BD16, 746 bytes free; protected/static-stack sizes stay
4495/36. No combined-fixture recompile was required. The ordinary loader was
rebuilt during carrier preparation and is byte-identical to the qualified one.
Controller v5 changes only L3 name/directory selection and its new admission pin;
v4 and all previous evidence remain retained unchanged.

Fresh pinned c1541 construction formats and adds AUTOBOOT.C65, R0FSUCC, TOKEN
and harmless occupied-name G1T00 in one session. Independent structure and
extraction pass. All four payloads match L2 exactly. Whole-image comparison
finds only offset 399370 changing from ASCII 2 to 3 in the disk label. L3 is a
fresh construction, never a renamed or patched L2 image. This is identity
isolation; allocation is addressed separately by the delivery method.

Each exact-name boot uses a separate fresh writable D81 and disposable SD
image, ordinary autoload, no PRG injection, and independent logs/captures.
NTSC/PAL run concurrently as an independent pair for each repetition; these
collision boots make no timing/calibration claim. All four runs pass actual
S5/E03/F00, unchanged inputs, correct actual SAVE and the readable PNG glyph
comparison. The PAL image was also visually inspected. Retained memory checks
locate secondary 1 and first staged chunk: first SAVE failure after successful
initialization. The complete lifecycle result passes in Xemu memory only.

Commands run from the repository root:

```sh
/usr/bin/python3 -B tools/diagnostics/r0f_group2_control.py carrier-build --experiment build/r0f/group2/control/trial-jnt4dplw
/usr/bin/python3 -B tools/diagnostics/r0f_group2_control.py boot --experiment build/r0f/group2/control/trial-jnt4dplw --mode 1 --number 1
/usr/bin/python3 -B tools/diagnostics/r0f_group2_control.py boot --experiment build/r0f/group2/control/trial-jnt4dplw --mode 0 --number 1
/usr/bin/python3 -B tools/diagnostics/r0f_group2_control.py boot --experiment build/r0f/group2/control/trial-jnt4dplw --mode 1 --number 2
/usr/bin/python3 -B tools/diagnostics/r0f_group2_control.py boot --experiment build/r0f/group2/control/trial-jnt4dplw --mode 0 --number 2
/usr/bin/python3 -B tools/diagnostics/r0f_group2_control.py carrier-finish --experiment build/r0f/group2/control/trial-jnt4dplw
/usr/bin/python3 -B tools/diagnostics/r0f_group2_collision_return.py --image build/r0f/group2/control/trial-jnt4dplw/carrier-l3/pal-01/R0FG2L3.D81 --release build/r0f/group2/control/trial-jnt4dplw/carrier-l3/canonical/release.json --out build/r0f/group2/control/trial-jnt4dplw/carrier-l3/returned-file-check-01
```

All exit 0. The read-only checker passes the actual new PAL post-run image and
leaves physical photo evidence pending. Release/qualification identity checks
pass; retained allocator fixture qualification is reused without rerunning it.

## Physical boundary and next action

The deliberate expected terminal screen is **red**, G1 EXPORT S:5 E:03 F:00.
It proves no nominal export success. Physical completion requires identified
chooser/entry, readable photo and actual returned-card file/SAVE checks under
the one-run procedure. Photos/files alone do not distinguish KERNAL call stage,
DOS error text or attempt count. The 34-byte SAVE does not carry full lifecycle,
resumed-service or timing evidence. All other suite cases remain open.

The initial sandboxed metadata query could not identify the volume; a separate
read-only query confirms mounted removable FAT32 with the intended UUID. No L3
destination/staging name was observed and the failed L2 bytes/hash remain
unchanged. Raw aliases, allocation/filesystem health, safe eject and physical
gates remain unverified. The
[owner CLI delivery proposal](OWNER_DELIVERY.md) is concrete and unexecuted;
raw writes still require the owner's method decision. Do not send L3 to the
chooser before exact SD hash, one extent and safe eject pass.

Preserve failed L2 (39 extents), withheld L1, frozen P09 and historical/unrelated
SD work. No new target registers/clobbers, CPU-visible/physical allocations,
MAP/base-page, DMA, timing/deadline, IRQ/NMI or generated-contract change.
The bootstrap is freshly generated with identical bytes; public contracts,
capacities, reserves, integrity checks and thresholds remain unchanged.

SHA256SUMS covers this packet. Large D81/memory/disposable-SD originals remain
local and hash-identified in local-artifacts.json; no private ROM dump is packaged.
