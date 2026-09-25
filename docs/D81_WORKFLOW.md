# Reproducible D81 construction and delivery

## Current delivery amendment

As of 2026-09-23, `R0FDIAG3.D81` has a physical chooser/entry-load PASS via
the owner-authorized MEGA65-native blank-fill route, but its R0-F diagnostic
locked out at fault `0x57`. The direct host allocator remains blocked by its
mandatory read-only filesystem check of an unrelated pre-existing FAT error;
do not bypass it or infer that other card files are bad. The next local
diagnostic carrier is `R0FDBG07.D81`, SHA-256
`c780d79a0e24ff00f10fbb7f3829ec943783c8b2d4413417ba389d900edcc775`,
at `XEMU_BOOT_VERIFIED` only. It is not yet an SD or physical result. See the
T07 first-fault report and WIP before any further delivery.

The GIAG4 physical copy failed: exact hash, **four measured FAT extents**.
Do not copy, install or retest GIAG4. Its commands and evidence below describe
the historical workflow qualification, not the current delivery instruction.
The owner subsequently authorized one historical direct-allocator installation
attempt, preserving every existing file. Its identity was `R0FHOST2.D81`, with
the same T06 target PRG and new exact-name host/Xemu evidence. That one-time
authorization did not carry forward to `R0FDBG07.D81`; the installation stopped
at the mandatory read-only filesystem check and did not deliver a new SD file.

Historical `R0FHOST2.D81` paths:

- Source: `build/r0f/d81-workflow/R0FHOST2/canonical/R0FHOST2.D81`.
- Release: `docs/evidence/r0f/successor/2026-09-22-workflow/R0FHOST2/release.json`.
- Qualification: `build/r0f/d81-workflow/R0FHOST2/allocator-qualification-2.json`.
- Install report: `build/r0f/d81-workflow/R0FHOST2/sd-install-1/`.

The direct allocator uses whole-sector aligned FSInfo I/O. Its 16-test
qualification supersedes earlier qualifications for that attempted
installation. Primary FSInfo must be valid. An all-zero inferred backup FSInfo
sector is preserved unchanged, not initialized or repaired; valid populated
backups are maintained.
Nonzero invalid backups, invalid primary signatures and out-of-range pointers
still stop installation. The observed card has valid primary sector 1 and
blank sector 7. The read-only filesystem and all allocation gates still apply.
No physical pass is implied; consult WIP and the actual install report before
hardware testing. Administrator authentication and all safety gates remain
required; neither a filesystem repair nor an overwrite is authorized.

Authority: [mandatory loadability gate](../00_D81_LOADABILITY_GATE.md).
Approved scope: owner's 2026-09-22 workflow recovery and `R0FGIAG4.D81` build.
This does not approve broader R0-F implementation or acceptance.

## Why the old workflow failed

There are two filesystems: the Commodore filesystem **inside** the D81 and the
FAT32 filesystem that stores the D81 **on the SD card**. Both must work.
The failed `R0FDIAG2.D81` SD copy has the exact host-verified bytes but 13 physical
extents. The native blank has one; the host-created `R0FHOST1.D81` that mounted
on hardware also has one. This is not evidence that the SD card is defective.

The observed macOS FSKit FAT implementation explicitly ignores the contiguous
preallocation flag and uses `mustBeContig:false`:
[Apple FATVolume.m, pinned source](https://github.com/apple-oss-distributions/msdosfs/blob/c9f076c4e7c10b4bc3b0177d114aedf1bb8b9109/msdos_appex/FATVolume.m#L2185-L2192).
Successful `F_PREALLOCATE` therefore never established a reliable allocator.
Changing D81 header bytes cannot choose the FAT clusters used by Finder.

## 1. Construct a unique canonical image

Choose the exact uppercase FAT 8.3 identity before building. For this request
the spelling is **R0FGIAG4.D81**, not R0FDIAG4.D81. Never reuse a failed identity.

From the repository root, the reproducible build command is:

```sh
python3 -B tools/diagnostics/r0f_successor_physical_diagnostic.py all --name R0FGIAG4.D81
```

This command has already completed for this identity. It intentionally refuses
to overwrite existing build/evidence directories. Future candidates require
their separately approved unique basename, not deletion of these results.

The builder rebuilds the unchanged T06 payload, freshly formats and populates
the image in one pinned `c1541` invocation, independently checks sectors/BAM/
chains and every extracted payload, then boots fresh exact-name copies twice
in NTSC and twice in PAL. It keeps post-run mutations separate. Never run the
canonical writable image. Working-tree input hashes are retained; this is not
a claim that the uncommitted diagnostic source is a published source freeze.

Historical `R0FGIAG4.D81` canonical file (failed SD allocation; do not retest):

```text
build/r0f/d81-workflow/R0FGIAG4/canonical/R0FGIAG4.D81
819200 bytes
SHA256 90a819f49c5b6cb3bf66f71317c1f40e3cae3f4059fb422b46b05589e86915fa
```

Release manifest and four independent runs:
`docs/evidence/r0f/successor/2026-09-22-workflow/R0FGIAG4/`.
Its host/Xemu state was `XEMU_BOOT_VERIFIED`; its later physical SD copy
failed the one-extent gate. It is not the current candidate.

## 2. Qualify host-created allocation without touching the card

The replacement uses the official MEGA65 host tool's contiguous FAT allocator,
not the ignored host preallocation flag. `toolchain/d81_delivery.lock.json`
pins the official archive, source commit, executable hash and local location.
The wrapper rejects any changed executable before writing.

The pinned archive is presently installed under `build/tools/`. For setup on
another Mac, fetch the lock's exact URL, verify `archiveSha256` **before**
extracting to `build/tools/`, and verify `binarySha256` after extraction. The
official development-release URL can disappear; a missing or changed download
is a blocker, not permission to use a newer binary. Retain the checked archive
or use a separately reviewed pin update and repeat qualification.

Run the real pinned executable against disposable local FAT32 partition images:

```sh
python3 -B tools/diagnostics/test_d81_direct_delivery.py --qualification build/r0f/d81-workflow/R0FGIAG4/allocator-qualification-2.json
python3 -B tools/diagnostics/test_d81_delivery.py
```

The qualification report is immutable: use a new report pathname for a rerun.
Tests create fragmented occupied chains and holes, allocate three new carriers,
and compare the entire partition byte-for-byte outside the new data, its FAT
entries, free root slots and advisory FSInfo fields. Existing files must stay
unchanged. macOS `fsck_msdos -n` independently checks the completed fixture.
Negative tests cover no free contiguous run, name collision, full root, divergent
FAT mirrors, bad 8.3 name, release-hash mismatch, changed tool and stale evidence.
Qualification is bound to the exact wrapper, inspector, test, lock and binary.
No test opens an SD device.

## 3. Delivery choice and authority

**Current owner preference: no automatic CLI transfer without a specific
exception.** The earlier one-time direct-allocator approval did not authorize
other future card writes. Provide the canonical host path. If the owner copies
with Finder, that operation is permitted but leaves the SD gates unverified.
Read-only raw audit must then establish the same hash, exact short name,
819,200 bytes and one extent; safely eject before the chooser test. If Finder
creates several extents, stop. Do not repeatedly retry, blame image content,
or send another unqualified file to hardware.

### Separately authorized direct allocator route

This route eliminates repeated MEGA65 blank creation. It is **host-fixture
qualified, not yet proven on the physical card**. It writes FAT metadata and
data directly and is not power-loss transactional. Obtain specific approval
before using it; the commands below are engineering reference, not an
instruction to override the owner's transfer preference.

Resolve the mounted removable FAT32 partition and its VolumeUUID using
`diskutil info -plist /Volumes/MEGA65FDISK`; never hardcode a remembered disk
number. After approval and local administrator authentication:

```sh
sudo python3 -B tools/diagnostics/d81_direct_delivery.py install-sd \
  build/r0f/d81-workflow/R0FGIAG4/canonical/R0FGIAG4.D81 \
  --manifest docs/evidence/r0f/successor/2026-09-22-workflow/R0FGIAG4/release.json \
  --mount /Volumes/MEGA65FDISK \
  --volume-uuid UUID_FROM_CURRENT_DISKUTIL_OUTPUT \
  --qualification build/r0f/d81-workflow/R0FGIAG4/allocator-qualification-2.json \
  --report build/r0f/d81-workflow/R0FGIAG4/sd-install-1 \
  --confirm-raw-write
```

Safety contract:

- Require the exact release identity, passing fixture qualification, removable
  FAT32 VolumeUUID and partition-only device. All source/evidence stays off-card.
- Refuse final/staging names and aliases that already exist. Require root
  cluster 2, 4KiB clusters, two equal FATs and spare root slots; other layouts
  are unsupported until separately qualified.
- Find a sufficient **actual free run**, bounded by volume geometry, before
  calling the upstream allocator. No available run means no write.
- Unmount without force. Recheck identity/unmounted state; run read-only
  `fsck_msdos -n`. Any existing filesystem error stops this method; it does not
  authorize repair of other files or prove card-wide failure.
- Preserve FAT, root and reserved-sector metadata locally before writing.
  The pinned official tool stages to `.TMP`; raw audit proves the hash,
  predicted allocation, one extent and unchanged existing FAT/root entries.
- Rename to the exact `.D81` without rewriting content. Recompute advisory
  FSInfo free count/unknown next hint (the upstream tool leaves these stale).
  Reaudit and run read-only filesystem checking. Remount, independently compare
  the mounted hash and raw allocation, and safely eject.
- Any failure stops. Retain staging and evidence; do not auto-repair, auto-retry
  or restore raw metadata on an uncertain filesystem. If failure occurs while
  unmounted, leave it unmounted and report the precise failure. Metadata
  snapshots are diagnostic evidence, not a complete card backup.

The older preallocation transfer wrapper is not the default. Native slot-fill
remains a separately authorized fallback, not a required normal build step.
Neither fallback bypasses raw allocation checks or physical proof.

### Separately authorized MEGA65-native blank route

Use only a never-tested, MEGA65-formatted root-level blank whose uppercase FAT
8.3 name exactly matches a fresh host candidate. Verify its size, empty D81
structure and SHA-256 before filling; record that blank hash. The helper must
recheck the same hash and independently audit a single FAT32 extent before any
write. It makes a host-side backup, changes only the existing file's 819,200
data bytes in place, verifies the candidate hash and unchanged allocation,
then safely ejects. A preflight failure makes no SD write. Do not use it to
repair a failed or previously tested carrier, and do not use a different name.

```sh
sudo tools/diagnostics/d81_sd_fill_mega65_slot.sh \
  build/r0f/d81-workflow/R0FDIAG3/canonical/R0FDIAG3.D81 \
  /Volumes/MEGA65FDISK \
  30508cb424e526b09f9f923e3ae4e35e449d89a5ec239f769b7da8a8cb2e1d60 \
  357078cd97a9aae0bf676ed844e5a01bfcafd32994309cf0d657f53e2a590018
```

This is the historical command for the one specifically authorized
`R0FDIAG3.D81` native blank. Its slot was filled, safely ejected and physically
tested. **Do not rerun this command or overwrite that tested carrier.**
The separate direct allocator cannot be used while its clean-filesystem check
fails, but that does not itself disqualify a verified existing native slot.

## 4. Physical carrier test, then R0-F

After SD gates and safe eject pass, select the exact verified filename in the MEGA65 chooser.
Require no chooser error and a readable directory. Run `AUTOBOOT.C65` (or the
documented autoboot flow) and photograph the stable diagnostic screen.
The first target is successful mount/load, not completion of R0-F.

The emulator's final diagnostic values are `FAULT 00`, `STATE 09`, `TICK 0042`,
`MASK 1F`, `NMI 00`, with matching reserve-before/after CRCs. Result CRC is
run-dependent. Brief graphics/audio are not acceptance evidence. Record the
actual physical values; do not infer them from Xemu. Any nonzero fault is a
runtime diagnostic failure distinct from chooser failure.

Only recorded physical chooser/entry evidence advances this exact carrier to
`TEST_ELIGIBLE`. Broader R0-F testing and acceptance remain separate.
