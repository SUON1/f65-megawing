# R0FHOST2 direct-allocation installation

## Authority and scope

After the owner-supplied GIAG4 audit established four extents with the exact
canonical hash, the owner explicitly authorized one new D81 using the direct
allocator, administrator authentication, existing files unchanged, verification
and safe ejection. No format, card repair, defragmentation, existing-file
overwrite or broader R0-F acceptance is authorized.

Inspected AGENTS.md, CURRENT_STATE.md, WIP, development workflow, D81 loadability
gate, direct-delivery workflow, builder, allocator, auditor and qualification
tests. New identity isolates the delivery attempt; it is not a claim that
rebuilding fixes fragmentation. Target C/ABI/registers/clobbers, CPU-visible
and physical memory, MAP/base-page, DMA, timing/deadlines and IRQ/NMI are
unchanged from T06.

## Candidate and pre-install observations

- New file: `R0FHOST2.D81`; 819200 bytes.
- Candidate SHA-256: `49e8c104e6def9f0557bd55ce1149b8e1d0fe111b3454e022e06642dcff5c2bd`.
- Target PRG SHA-256: `3ce9aeb1029676465d47755145ec31d6b30ab2ca0c8ae95dc88e9703dd99446b`, unchanged from GIAG4/T06.
- SD VolumeUUID: `83FFC12E-67E1-307F-91AD-E584C2E01E87`.
- Observed partition: `disk4s1`, removable FAT32, 4096-byte clusters. Re-resolve
  on installation; do not rely on this device number as permanent identity.
- Existing Alpha SHA-256: `40d95171389e3825793216ed54176084a87bad5bac630b942955c8b90668b3b4`.
- Existing failed GIAG4 SHA-256: `90a819f49c5b6cb3bf66f71317c1f40e3cae3f4059fb422b46b05589e86915fa`.
- Existing native blank DIAG3 SHA-256: `357078cd97a9aae0bf676ed844e5a01bfcafd32994309cf0d657f53e2a590018`.

## Pre-install safety correction

The FSInfo refresh originally used eight-byte unaligned reads/writes, which
the regular-file fixture did not exercise as raw-device I/O. Before SD access,
changed it to full 512-byte sector reads/writes and complete-sector readback,
preserving all non-counter bytes. Added an aligned-I/O regression test and
requalified the exact wrapper/test/dependency/binary identity.

Validation:

- `python3 -B tools/diagnostics/test_d81_direct_delivery.py --qualification build/r0f/d81-workflow/R0FHOST2/allocator-qualification.json`: 12 tests PASS.
- `python3 -B tools/diagnostics/test_d81_delivery.py`: 18 tests PASS.
- `python3 -B tools/diagnostics/r0a_validate.py .`: PASS.
- `git diff --check`: PASS.

The new qualification supersedes GIAG4's older qualification for the updated
wrapper. The fixture still uses the same-size GIAG4 source to test allocation;
HOST2's separate exact-name release manifest governs actual installation.

## Operation status

Host target build and structural/content checks PASS. Two NTSC plus two PAL
exact-name Xemu boots PASS; final PAL screen visually checked. The exact
release identity and new qualification were rechecked together. Evidence is
retained under `docs/evidence/r0f/successor/2026-09-22-workflow/R0FHOST2/`.

Initial `sudo -n` reported that local administrator authentication is required.
The approved installer was then invoked using `osascript` with administrator
privileges, requesting the standard macOS system dialog. It remains pending
local authentication at the initial checkpoint (SecurityAgent observed;
terminal session 1620).

After the owner authenticated, session 1620 exited with status 1:
`PermissionError: [Errno 1] Operation not permitted: '/dev/rdisk4s1'`.
The failure was in `preflight -> volume -> os.open(..., O_RDONLY)`, before
unmount, filesystem checking, metadata snapshots or writes. No SD file was
changed and no install report directory was created. Do not infer the precise
macOS privacy-policy cause from EPERM alone. Use the owner's Terminal for the
same approved installer; prior authenticated raw audits worked there. No
permission changes or gate bypass are authorized. SD verification/ejection
and physical chooser/runtime are NOT COMPLETE.

The subsequent owner-run Terminal attempt accessed the raw partition but
failed in `preflight -> info_sectors` with `invalid FSInfo signature`, before
unmount or SD writes. The current validator assumes both primary and inferred
backup FSInfo sectors have valid signatures; its generic error cannot locate
the failure. Added `d81_fsinfo_audit.py` for read-only sector evidence. Do not
infer card corruption, skip the gate, initialize sectors or change the FAT
from this exception alone. Installation remains blocked pending that evidence.

## FSInfo evidence and correction

Owner-authenticated `fsinfo-audit.json` establishes 568 reserved sectors,
valid primary FSInfo at sector 1, boot backup at sector 6, and an all-zero
sector 7. The validator incorrectly required an FSInfo backup at that inferred
location. The boot backup is not itself an FSInfo sector.

The narrow correction requires valid primary FSInfo, preserves a completely
blank inferred backup, and maintains an already-valid populated backup. A
nonzero invalid backup or out-of-range pointer still fails. No sector is
initialized or repaired. The reserved-region audit includes the untouched
blank backup, so any unexpected modification there is rejected.

Validation: 16 allocator tests PASS, including full real-tool fixture delivery
with blank backup preservation and `fsck_msdos -n`; invalid primary, nonzero
invalid backup and out-of-range backup cases remain rejected. A read-only
replay of the captured actual boot/sectors returns only sector 1 as writable
FSInfo. Candidate release verification and current qualification PASS.
HOST2 bytes and target program were not changed; no emulator rerun needed
for this host-only fix. No SD write occurred during correction.

Current qualification is `allocator-qualification-2.json` under the HOST2
build/evidence folders; the earlier qualification is superseded. Retained
`fsinfo-audit.json` contains the actual sector bytes. Retry only the already
approved Terminal install with the new qualification. The clean read-only
filesystem check, raw hash/one-extent checks and safe-eject gates remain in
force. This does not establish SD installation or physical success.

## 2026-09-23 clean-filesystem gate

The owner-run retry reached unmount and `fsck_msdos -n`. The read-only check
reported a cross-link at cluster 12417 in
`/A. MegaWing/F65BLK02.D81`, stated that its 819200-byte directory size has
at most 4096 reachable bytes, and found 623 orphan clusters. It exited 206.
The installer stopped at `install_sd`'s mandatory `check=True` filesystem
check, before `deliver`, staging, FAT allocation, renaming or any SD write.
No install evidence directory exists. The supplied command output shows the
intended `disk4s1` volume was unmounted first; it has not been remounted by
this installer.

The prior raw audit had already reported an underallocated `F65BLK02.D81`;
these warnings are additional filesystem-level observations, not proof that
unrelated working files are damaged or that the card needs reformatting.
Existing-file repair/deletion and a bypass of the clean-filesystem gate are
outside the authorized operation. The exact HOST2 D81 remains host/Xemu
verified only. No physical chooser gate has been run for it.

The retained native `R0FDIAG3.D81` blank was one extent at its last raw audit.
Using it would require a fresh same-name host candidate and would overwrite
that intentionally empty slot in place. That is a different action from the
owner's approval to add one new file while leaving existing files untouched.
Revalidate its current identity before any separately authorized fill.
