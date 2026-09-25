# D81 delivery recovery

2026-09-22 correction: the preallocation capability claim below was too strong.
Apple's FSKit FAT code ignores the contiguous flag. The 22-extent staging audit
disproves a reliable one-extent guarantee from this method. See
[the native-blank examination](D81_NATIVE_COMPARISON_2026-09-22.md).

Status: **Host fixes and two exact-name Xemu candidates verified; SD delivery
blocked on local administrator authentication and missing native slot.**

## Authorization and boundary

The owner's 2026-09-21 instruction prioritizes reliable D81 creation and
delivery, authorizes fresh candidate files, and requests filling the freshly
MEGA65-formatted `R0FSUC10.D81`. This replaces the original T05 frozen host
filename constraint. It does not change the target payload, public ABI,
memory ownership, MAP/base-page, DMA, 100 Hz/21-stage model, IRQ/NMI handling,
measured limits or founder acceptance. Registers/clobbers and target timing
effects are not applicable to these host-only changes.

Integrated baseline: `ae2b397698cc7197d03349e57cd058b4fb9f3987`.
Frozen target source: `20b2aab382d0590037443b6a352fbc77fda7aa42`.
Target: 21,481 bytes, SHA-256
`d0979c56c373f8885e4741670141ebf22c0a2e9ef8a84f6a931eaef05592d9df`.
Governing inputs: root D81 gate; development workflow; T04 exact-carrier
handoff, source and retained payload/evidence records; current T05 scope plus
the owner's carrier-recovery amendment. Retained T04 evidence is unchanged.

## Findings and repairs

- Builder name validation was missing. Shared validation now rejects long,
  lowercase, non-ASCII and malformed release names before c1541 is invoked.
  The original T04 historical default intentionally fails this validation;
  the recovery command below owns the newly authorized compliant identities.
- Transfer previously used ordinary `cp`, which did not request contiguous
  allocation. It now requests `F_PREALLOCATE` with `F_ALLOCATECONTIG` and
  `F_ALLOCATEALL`, without a caller-side fallback. The filesystem may still
  return fragmented allocation. A live
  temporary non-D81 probe on the intended FAT32 card allocated all 819,200
  bytes successfully, then removed only its own probe. This proves request
  acceptance only, not support for contiguous allocation, completed SD
  transfer, or physical mountability.
- Transfer now checks the mount, filesystem, removable-media identity and raw
  read privilege before creating a staging file. It no longer requires
  Homebrew `rg` in an administrator shell's PATH.
- Final rename uses Darwin `renamex_np(RENAME_EXCL)` to reject an existing
  destination atomically. Post-rename failures retain the final file for
  diagnosis; they do not delete an uncertain final identity.
- Root release auditing now reads the FAT directly, checks mirrored tables,
  exact short-name identity, cluster bounds/loops/length and the content hash
  reconstructed from raw clusters. Long-name decoding is available only for
  forensic analysis; it does not admit a long release name.
- Both transfer routes record safe-eject PASS only after `diskutil eject`
  succeeds. They then report awaiting human chooser verification.

The allocation API constants/layout were checked against the installed macOS
SDK `sys/fcntl.h`; exclusive rename against `sys/stdio.h`. The card uses
macOS's FSKit `msdos` filesystem. Official
[MEGA65 Tools](https://github.com/MEGA65/mega65-tools/tree/23186dd68d8549386421db261c228fd0710224f2)
also supports direct-card mode and contiguous cluster allocation. That source
was inspected as an alternative; it was not used to modify this card.

## Candidates and evidence

Both fresh c1541 constructions have 819,200 bytes and SHA-256
`3721dff9b84cfb7842cc154f6885861e0c7cbd3c3408c8ecec190bf6b405d461`.
Host filenames are distinct; internal disk label `R0F SUCC T04`, ID `65`, and
all three T04 payloads are unchanged. Matching bytes do not reuse old Gate-3
claims: each new basename completed two clean NTSC and two clean PAL boots.

| Candidate | Purpose | Current gate |
|---|---|---|
| `R0FSUC10.D81` | Fill the owner's fresh native slot | XEMU_BOOT_VERIFIED |
| `R0FHOST1.D81` | Fresh host-allocated transfer | XEMU_BOOT_VERIFIED |

Local images: `build/r0f/successor-t05-recovery/<stem>/<filename>`.
Retained non-D81 evidence:
`docs/evidence/r0f/successor/2026-09-21-recovery/<stem>/`.
Raw incident photographs and interpretation are in that directory's
`incident/REVIEW.md`. The failed SD image is retired and untouched.

Every accepted emulator run passes Python reduction, the independent Java
oracle, post-run structure/content validation and extracted SAVE comparison.
Canonical images remain read-only and unmounted; only fresh disposable copies
receive the diagnostic's SAVE. Working-tree tooling hashes and the frozen
target source identity are explicitly distinguished in each release record.
Initial sandbox-denied emulator starts remain local failed-environment logs;
they were not counted as passes.

## Repeatable commands and validation

Fresh construction and exact-name Xemu checks (refuses overwrite):

```sh
python3 -B tools/diagnostics/r0f_successor_carrier_recovery.py R0FSUC10.D81
python3 -B tools/diagnostics/r0f_successor_carrier_recovery.py R0FHOST1.D81
```

This run used `--host-only`, then `--resume-xemu` for each, retaining fresh
attempt directories after the initial sandbox restriction.

Completed checks:

- `python3 -B tools/diagnostics/test_d81_delivery.py`: 10 tests PASS.
- Both construction commands: host structure/content and frozen bytes PASS.
- Both emulator commands: four exact-name runs each PASS.
- `python3 -B tools/diagnostics/r0a_validate.py .`: corpus/reserve/scope PASS.
- Shell syntax and `git diff --check`: PASS.
- Live `allocation-probe /Volumes/MEGA65FDISK/F65ALLOC.TMP`: contiguous/all
  allocation of 819,200 bytes completed; probe removed.

The raw audit command opened a local administrator request that did not
complete. `sudo -n /bin/sh tools/diagnostics/r0f_recovery_sd.sh` returned
`sudo: a password is required`; no delivery occurred. The read-only OS extent
API also required the raw-device fallback, which lacked permission.

## Latest audit failure and next diagnostic

The owner subsequently authenticated and ran the recovery helper. Its initial
read-only audit raised `file size/chain allocation mismatch` before either
transfer. The diagnostic failed to record which file or the chain counts;
this does not yet establish filesystem corruption or explain chooser FF.

The audit now preserves per-file errors and continues examining the other
requested files, saves the report, then returns nonzero if any file failed.
Allocation mismatch records include logical size, cluster size, required and
actual cluster counts, and the complete chain. Neither underallocation nor
overallocation is accepted by the release validator. The strict validator
still raises; only forensic reporting catches and records that error.
`/usr/bin/python3 -B tools/diagnostics/test_d81_delivery.py`: 12 tests PASS,
including under/overallocation rejection and continuing diagnostics after a
bad file. `git diff --check`: PASS. No target or candidate bytes changed.

Run this read-only diagnostic before retrying transfer:

```sh
sudo /usr/bin/python3 -B /Users/slice/Developer/f65-megawing/tools/diagnostics/d81_fat32_audit.py /Volumes/MEGA65FDISK R0FSUCC10.D81 R0FSUC10.D81 F65BLK02.D81 --json /Users/slice/Developer/f65-megawing/build/r0f/successor-t05-recovery/sd-diagnostic.json
```

It writes only the local JSON report, never the SD card. A nonzero exit with
`Audit failed; diagnostics saved` is intentional when an allocation error
remains. Inspect that report before authorizing the next media operation.

## Transfer command after resolving the audit blocker

### Continued authorized creation/delivery repair

The owner reaffirmed host-created delivery, without card repair/reformatting
or a required manually created blank. Read-only comparison with the retained
CF001 builder and `physical/2026-09-18/sd-fill.log` establishes that the
successful historical path was one fresh c1541 construction session followed
by a native contiguous-slot fill. Its retained post-fill record reports one
819,200-byte extent at partition byte offset 108,425,216. This is historical
evidence, not a statement about the current on-card control's allocation.

The successor uses the same pinned c1541 hash and fresh single-session
construction pattern. The demonstrated delivery regressions are the illegal
nine-character host stem and the fragmented copied file; internal-image
corruption has not been established. Do not claim card-wide damage either.

The fresh host route replaces plain `cp` with OS contiguous/all preallocation,
then writes the already hash-checked bytes. It rechecks the source hash in the
writer before creating the destination, validates raw volume geometry/FAT
mirrors/root names before allocation, and requires staged/final raw content
hash plus one complete extent. Rename is exclusive. Signals return nonzero;
eject failure cannot produce a delivery PASS. A post-rename failure retains
that exact candidate as not released for diagnosis, never silently reuses it.

The recovery pre-audit now selects the retired failed file and the potential
native slot only. The unrelated `F65BLK02.D81` anomaly is preserved in
`sd-diagnostic.json`, but that file is neither a release input nor a verified
current control. Removing it from the batch does not relax geometry, FAT
mirror, candidate chain length, raw hash, one-extent or safe-eject gates.
No writes, repair or renaming of existing working/failed files are authorized.

The recovery builder's runtime revalidation now first reconstructs the full
image from the frozen payloads, validates/extracts it and requires equality
with the immutable candidate. Repeated attempts retain previous evidence;
current delivery-tool hashes are recorded and checked by recovery preflight.

Host validation: `python3 -B tools/diagnostics/test_d81_delivery.py` passes
18 tests. Added coverage includes a full-size 4-KiB-cluster FAT fixture with
one versus nine extents but identical hashes; source drift before allocation;
partial/zero writes; and execution of the transfer shell's actual control flow
with simulated OS boundaries. The latter covers successful ordered gates,
preflight/allocation/staging-audit/rename/final-audit/eject failures, preservation
of existing final names, staging cleanup and no premature release. These are
host simulations, not SD or hardware proof. Python parsing, shell syntax,
`git diff --check` and `r0a_validate.py .` pass.

Administrator check for this continuation still returns `sudo: a password is
required`; SD delivery has not occurred. Local authentication is required for
the command below. The repeated Xemu checks have now finished: two NTSC and
two PAL runs PASS in `R0FHOST1/attempt-2`, including Python/Java result reduction,
SAVE extraction and screen identity checks. Fresh reconstruction and canonical
identity remain `3721dff9b84cfb7842cc154f6885861e0c7cbd3c3408c8ecec190bf6b405d461`.
Evidence is retained under
`docs/evidence/r0f/successor/2026-09-21-recovery/R0FHOST1/attempt-2/`.
The real recovery manifest-preflight code also passes against the actual local
manifests/images with mocked device identity; this is a host check only.

The frozen target's visible banner still says `CF001 / F65BLK02` and includes
old host/static disclaimers. NTSC-1 and PAL-2 screenshots were visually checked
in this continuation. The carrier name is `R0FHOST1.D81`, established by the
mount command and manifest; no target strings or executable bytes were changed.

One command in the owner's local Terminal:

```sh
sudo /bin/sh /Users/slice/Developer/f65-megawing/tools/diagnostics/r0f_recovery_sd.sh
```

It verifies the inspected card UUID and both Gate-3 manifests, audits the failed
copy, fills the native slot only if present and blank, then delivers the fresh
host candidate through contiguous preallocation, staged/final raw FAT and hash
checks, and safe eject. Existing final identities are never overwritten.
Missing `R0FSUC10.D81` is reported explicitly; it does not prevent the separate
host candidate from being attempted. Extent reports are under
`build/d81-sd-transfer/`; raw incident audit under
`build/r0f/successor-t05-recovery/sd-before.json`.

This command reached its privileged read-only audit but stopped there; no
candidate transfer ran. The native-slot branch also awaits confirmation
that formatting actually completed, since no matching root file is visible.

Do not claim either new image physically loadable until the owner verifies
chooser attachment, readable directory and entry loading. Full R0-F remains
open; a successful carrier mount alone would not close it. No commit, push,
PR, merge, measured-limit freeze or Phase 1 work occurred.

## Physical result received

The owner ran the repaired host-created `R0FHOST1.D81` delivery. The transfer
log reports the exact expected SHA-256, one 819,200-byte FAT32 extent at device
offset 111,132,672 and safe eject. On MEGA65 the image attached and executed,
so the corrected carrier has passed the physical chooser/entry-load boundary
that previously produced `ERROR CODE FF`.

The runtime itself failed closed. The owner observed brief graphics and sound;
Photo 1 shows immutable-ROM verification, and Photo 2 shows `SUCCESSOR LOCKOUT
- NO ACCEPTANCE`, fault `58`, lifecycle `0A`, tick `0042`, result CRC32
`20452538`. Fault `0x58` is decimal 88, assigned only by the aggregate final
completion test. Tick 66 proves both timed workload halves completed, but the
screen cannot distinguish reserve-integrity failure from a missing required
resumed-service bit or another value in that final predicate. No physical
runtime PASS or R0-F acceptance is claimed.

The unmodified photos, SD reports, hashes and evidence interpretation are in
`docs/evidence/r0f/successor/2026-09-21-recovery/R0FHOST1/physical-1/`.
A new instrumented target would be a separate diagnostic revision and is not
authorized by the current no-target-source-change scope.
