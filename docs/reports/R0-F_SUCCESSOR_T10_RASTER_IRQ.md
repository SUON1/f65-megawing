# R0-F T10: interior raster IRQ and physical failure follow-up

## Latest physical disposition — 2026-09-28

IRQ11 subsequently passed physical entry and the bounded runtime summary:
00/09/0042/1F/00, IRQ 0015 -> 0029, equal reserve CRCs. The owner-selected
Finder copy after MEGA65-native clean setup passed raw exact hash/one extent
and safe eject. See [retained observation](../evidence/r0f/successor/2026-09-28-r0firq11-physical/README.md).
Do not rerun the historical blank-fill commands below. Preserve IRQ11.
Complete result reduction remains pending; T11 adds a post-run capture viewer.
No full R0-F acceptance or universal hardware-fix claim follows from one run.

## Authority and scope

The owner's continuing Fault 65 correction request and new never-tested
`R0FIRQ11.D81` native blank authorize this narrow successor correction and
fresh local carrier build. No commit/push, failed-carrier rewrite, filesystem
repair, public ABI change or R0-F acceptance. Base `9e2ffdb4786e4794119933a5edd4b1cf79f653f0`
on `codex/r0f-successor-physical-exact-carrier`; fetched origin/main remains
`ae2b397`, the integrated predecessor. Preserve the existing dirty T09 work.

Inspected contracts: PF001 qualification, CF001 combined implementation,
T02 successor admission and T03 integration contracts/ledgers, T09 handoff,
repository development/C standards and the D81 gate/workflow. Per-input
hashes identify the local build; this is not a published source freeze.

## Physical result and supported diagnosis

IRQ10 loaded but failed: fault `65`, state `0A`, tick `0042`, mask `17`,
NMI `00`, reserve before/after `3C7D60D8`, result CRC `E96A691D`.
IRQ counts are `0000 -> 0000`; IEC output/clear are `00/00`, reclaim
features `2B`. The returned feature bit 6 is clear. The T09 IEC hypothesis
did not resolve the failure and is not supported at this sampled transition.
Retain its guard/tests but do not describe it as the proven physical cause.

The pinned official core `b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f`
has a concrete mismatch with our line-zero setup:

- `viciv.vhdl` writes to D011/D012 select logical raster comparison.
- Its NTSC setup selects first logical raster 7. The counter resets to
  `vicii_first_raster` each frame, increments and saturates at the maximum.
  The only counter assignments in this source are increment and frame reset.
- Raster comparison requires equality on a changed counter, with optional
  one-line delay. Neither line 0 nor delayed line 1 need be visited.
- The pinned Xemu `vic4.c` instead resets logical raster to zero and computes
  it from `ycounter >> 1`. Its passing line-zero result misses this case.

Primary source:
[VIC-IV](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/vhdl/viciv.vhdl).
Retained local source: `build/r0f/combined/references/viciv.vhdl` and
`xemu-vic4.c`. SHA-256 respectively
`81aa438fa0c2d5b6e040ba5f24db2401ed0c18e140138d355cbe3ce037f5091b`
and `7abafaf98dde6c8a3b5ad582b811dd1a9071e0ff2f47bbc2a767b6372b878928`.
This proves a source-level setup defect, not the installed
hardware's exact cause: its D06F and live CPU/VIC states were not captured
by IRQ10. The next physical diagnostic must confirm or refute the inference.

## Change and hardware effects

Only the successor selects logical line 128 after initial display setup and
after the resumed clock start. Line 128 is above every six-bit first-raster
value (0-63) and below both supported maxima, even with one-line delay.
Preserve D011 bits 0-6, clear its compare MSB, write D012=128. The existing
PF001 enable/acknowledge/vector/handler and CF001 programs are unchanged.
No artificial IRQ count, acceptance waiver, timer-source change or PAL/NTSC
mode switch. The existing post-storage real count advancement remains required.

Private result bytes 100-107 retain CPU P, D019, D01A, D06F, D079, D07A,
and CPU-visible FFFE/FFFF after the resumed interval and before cleanup.
These are sequential reads, not an atomic snapshot. FF means not reached;
D079/D07A may not expose comparison state in the pinned emulator. CPU P
uses a three-instruction PHP/PLA/RTS C-return shim: A and N/Z clobbered,
XYZ/B/MAP and I/D/C preserved, balanced hardware stack, no SEI or CLI.
It is application text, never executed during the MAP-hidden storage window.
Existing protected mailbox addresses stay fixed. No new physical allocation,
reserve write, DMA, NMI handler change or 100 Hz deadline/stage change.

Diagnostics remain private generated-contract fields in the existing
512-byte result. Final screen identifies R0FIRQ11 and displays these samples.
Reading D019/D01A is non-acknowledging; CIA interrupt-status registers are
not read. A racing IRQ can change pending status between observations.

## Verification / delivery status

New host cases exercise the actual C selector against all D011
values and source-derived reachability over every first-raster value, delay
and video maximum, including reproducing the old unreachable zero case.
This bounded model is not FPGA simulation or physical proof. Target/static,
fresh development and exact-carrier Xemu, negative disabled-IRQ regression,
image checks and current input identities must pass before delivery.

Completed local checks:

- `python3 -B tools/diagnostics/r0f_successor_integration.py build`: PASS,
  525,587 IRQ tests, 1,527,538 integration checks, CF001 regressions and
  16,842,752 RH001 checks. Generated contracts, protected storage range,
  IRQ preservation, symbol addresses and target ordering PASS.
- Development runner `r0f_successor_post_storage_probe.main()` with OUT
  `build/r0f/successor-raster-line-probe-1`, NAME `R0FDEV11.D81`, LABEL
  `R0F RASTER T10`: NTSC and PAL PASS. Both `00/09/0042/1F/00`, actual
  resumed IRQ counts advance. Direct-PRG evidence only, not carrier proof.
- `python3 -B tools/diagnostics/r0f_successor_irq_negative.py --good-run
  build/r0f/successor-raster-line-probe-1/ntsc --out
  build/r0f/successor-raster-negative-1`: PASS. CLI-to-SEI derivative still
  produces `65/0A/0042/17/00`, no count advancement. Its new CPU sample is
  `35` (I=1), contrasting passing sample `31` (I=0). Python and Java reducers
  reject a forged pass mask with no IRQ advancement; rollover still passes.
- `python3 -B tools/diagnostics/test_d81_delivery.py`: 18 tests PASS.
- `python3 -B tools/diagnostics/r0a_validate.py .`: PASS.
- Tracked/non-ignored JSON/Python syntax and `git diff --check`: PASS.

Development and negative evidence retained in
`docs/evidence/r0f/successor/2026-09-26-raster-irq/`. No existing evidence
files or canonical images were reused as writable test inputs. One initial
compile placed the three-byte status shim in protected text and the target
identity gate correctly rejected the shifted storage payload address before
emulation. It is now application text, restoring the existing `$29C4`
payload and `$2B07` protected end. This did not produce a delivery image.

Target: 22,803 bytes, SHA-256
`a7420418b8fa60e0fe8f83847dabae3a905a0b2920569b64592b5e689e999a95`.
Resident usage 24,982, margin 15,977, high-water exclusive `$8197`.
No new physical allocations or reserve consumption.

Exact carrier command completed PASS:
`python3 -B tools/diagnostics/r0f_successor_physical_diagnostic.py all --name R0FIRQ11.D81`.
Fresh single-session structure/extraction gates PASS. Canonical image:
`build/r0f/d81-workflow/R0FIRQ11/canonical/R0FIRQ11.D81`, 819,200 bytes,
SHA-256 `e7889a59f95a68d3b167880398881f4d17b628b0cd2c1b269f8e4b701797e5fa`.
Four fresh exact-name Xemu runs PASS; state **XEMU_BOOT_VERIFIED only**.
All show `00/09/0042/1F/00` and matching reserve CRCs. NTSC counts are
35->51 and 35->52; PAL counts are 36->48 twice. Result CRCs respectively
`3328CA5F`, `4F3F2B2E`, `CEE81C2F`, `2A3FA7DF`. The canonical remains
read-only and byte-identical; no writable test mounted it. Retained release,
accounting and four independent result/SAVE/screen records:
`docs/evidence/r0f/successor/2026-09-22-workflow/R0FIRQ11/`.

At the 2026-09-26 checkpoint the new SD blank had not been written. Initial read-only content reads were
stuck in OS I/O despite visible metadata. Do not infer defective media or
bypass its empty-image/hash/one-extent gates. All prior failed identities
remain unchanged. Physical fix and full R0-F acceptance remain unproven.

The owner was asked to eject normally and reconnect; if normal eject fails,
leave the card connected and report it. No forced unmount or repair is
authorized. Only our two stalled read-only Python checks were sent TERM;
the uninterruptible I/O had not returned at the checkpoint. Do not issue
an SD fill instruction with an invented/unverified blank hash. Once normal
reads work, finish blank verification and the existing native-slot workflow.
The exact canonical hash above must be used; no Finder replacement.

### 2026-09-28: readable blank verified; privileged fill pending

Owner reports mounted. Fresh read-only inspection confirms the intended
removable FAT32 volume UUID `83FFC12E-67E1-307F-91AD-E584C2E01E87`.
`Image("/Volumes/MEGA65FDISK/R0FIRQ11.D81")` passes geometry/BAM/chain
checks with zero entries, 3,196 free blocks and 819,200 bytes. Label R0FIRQ11,
ID C9, SHA-256 `3acd72a0d993eb7eb48734714e49f6055629493ddd69bfe20c766a7d19bc6f49`.
Retained in the IRQ11 evidence directory as `native-blank-2026-09-28.json`.
Current source inputs and canonical bytes still match retained accounting
and the XEMU_BOOT_VERIFIED release. No rebuild, code change or SD write.

The owner must authenticate locally for the remaining raw allocation check
and fill. This command refuses a changed blank or failed one-extent check
before writing, retains a host backup, fills only the exact same-name slot,
verifies candidate bytes and unchanged allocation, then safely ejects:

```sh
cd /Users/slice/Developer/f65-megawing
sudo tools/diagnostics/d81_sd_fill_mega65_slot.sh \
  build/r0f/d81-workflow/R0FIRQ11/canonical/R0FIRQ11.D81 \
  /Volumes/MEGA65FDISK \
  e7889a59f95a68d3b167880398881f4d17b628b0cd2c1b269f8e4b701797e5fa \
  3acd72a0d993eb7eb48734714e49f6055629493ddd69bfe20c766a7d19bc6f49
```

Do not repeat after a successful fill or physical test. Await the actual
helper output before claiming SD contiguity, safe eject or physical readiness.

### 2026-09-28: FAT-copy disagreement blocks fill

The owner ran the above command. It stopped in `d81_sd_contiguity.py` when
`Fat32.__init__` raised `ValueError('mirrored FATs differ')`. In the existing
helper this preflight precedes backup/fill and `slot_modified=1`. Neither
IRQ11 slot-pre nor slot-post report exists. A subsequent independent mounted
`Image` inspection confirms the same blank hash, size, empty directory and
3,196 free blocks. No candidate data was written by this attempt. Do not
repeat the fill command until the disagreement is understood and gates pass.

The error alone does not identify which FAT words differ, which copy reflects
the intended allocation, whether reads raced a metadata update, or whether
the inspector is rejecting non-allocation differences. It does not prove
physical media damage. Do not waive the check or choose a FAT arbitrarily.

Read-only diagnostic scope under the continuing failure investigation:
`tools/diagnostics/d81_fat_mirror_diagnostic.py` opens only the currently
identified removable partition with O_RDONLY. It bounds boot/FAT reads,
compares two successive pairs, classifies differing entries by location and
bit differences, and reports at most 32 examples per pair. It does not read
user file contents, unmount, flush, repair, select an authoritative FAT, or
grant any release state. Its output is exclusive-create, off removable
volumes. Two matching reads are observations, not an atomic/offline audit.
Target registers/clobbers, CPU/physical memory, MAP/base-page, DMA, timing
and IRQ/NMI effects are not applicable: target code/images are unchanged.
Existing `Fat32` and slot-fill safety logic are unchanged.

`python3 -B tools/diagnostics/test_d81_fat_mirror_diagnostic.py`: eight
synthetic host tests PASS (equality, differing scopes/bits, sample bound,
length validation, real local fixture reads, changing snapshots, bad geometry,
partition bounds and short reads). Actual SD table comparison requires the
owner's local sudo authentication; agent O_RDONLY access was denied.

```sh
cd /Users/slice/Developer/f65-megawing
sudo /usr/bin/python3 -B tools/diagnostics/d81_fat_mirror_diagnostic.py \
  /Volumes/MEGA65FDISK \
  --json build/r0f/d81-workflow/R0FIRQ11/fat-mirrors-1.json
```

This command only reads the SD and saves diagnostic JSON on the Mac. No
repair, new blank, alternate transfer, or physical test is currently requested.
