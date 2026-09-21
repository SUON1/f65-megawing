MANDATORY D81 LOADABILITY GATE

Before creating, modifying, copying, renaming, packaging, mounting, testing, or releasing any D81, read and obey the repository-root file 00_D81_LOADABILITY_GATE.md.

The work must fail closed. A D81 may not be called final, test-ready, loadable, or delivered for physical testing until the exact artifact passes every applicable state in this order:

UNVERIFIED
-> HOST_STRUCTURALLY_VERIFIED
-> HOST_CONTENT_VERIFIED
-> XEMU_BOOT_VERIFIED
-> SD_COPY_VERIFIED
-> SD_CONTIGUITY_VERIFIED
-> PHYSICAL_CHOOSER_VERIFIED
-> TEST_ELIGIBLE

Never build a new test carrier by copying an existing D81 and reopening the copy in a second c1541 session to append files. Fresh-format the image and populate all files in one pinned-tool construction session.

ERROR CODE FF at the MEGA65 chooser is a hard chooser/attach-stage failure. Retire that tested copy and diagnose D81 construction, exact copied bytes, SD physical allocation, safe ejection, and platform identity before assigning a replacement. Do not patch, append to, rename, or re-test the failed copy and do not blame the program inside it.

A matching hash of the SD-card copy is necessary but not sufficient. The MEGA65 Freezer requires a disk-image file to occupy one contiguous FAT32 extent. A fragmented file can hash perfectly and still fail to mount with ERROR CODE FF. Do not submit a copied image to the physical chooser until an independent extent check reports exactly one extent.

# R0-F T04 successor emulator and exact-carrier execution

Date: 2026-09-20 to 2026-09-21

Status: **READY FOR REVIEW - PROVENANCE REMEDIATION COMPLETE**

## Build Intent

First reproduce the exact reviewed T03 target, then establish the first runtime
evidence for the same frozen architecture. Rebuild and identity-gate the PRG,
apply only bounded entry corrections exposed by direct execution, run clean
direct-PRG diagnostics using fresh disposable storage fixtures, construct one
fresh canonical D81 in one pinned-tool session, independently validate its
filesystem and extracted contents, and run two independent writable copies in
each admitted NTSC and PAL Xemu mode. Independently validate every result and
saved payload, and prove bounded missing/invalid input and corrupt-reducer
lockouts.

The canonical image contains only `AUTOBOOT.C65`, the corrected exact successor
PRG and the deterministic `TOKEN` input. `AUTOBOOT.C65` embeds a 107-byte
carrier-only bootstrap that runs at physical `$1000-$106A`, selects KERNAL bank
0, loads the unchanged on-disk successor bytes at their PRG address, and jumps
to the linked `_start`. It is made read-only after host admission and is never
mounted writable. Every carrier run starts from a newly copied image whose
pre-run hash equals the canonical hash. Post-run images are preserved as local
evidence and never reused.

## Frozen target and hardware boundary

- Reviewed T03 input reproduced before runtime work: 21,489 bytes, SHA-256
  `43074a4322b9a2ec35428e966d9f64ab30655c8f0f27516317e7e3f9e417264a`.
- Corrected T04 runtime PRG: 21,481 bytes, SHA-256
  `d0979c56c373f8885e4741670141ebf22c0a2e9ef8a84f6a931eaef05592d9df`.
- Registers/clobbers: the existing one-way entry still owns A/X/Y/Z, B, status,
  MAP, CPU port and I/O normalization. It now performs the official all-zero
  MAP clear before direct-page CPU-port access.
- CPU and physical memory: unchanged T02/T03 ranges, including guarded Attic
  `$08020000-$0802161F`, resident `$2001-$BFFF`, software stack
  `$C000-$CFFF`, and untouched `$058000-$05FFFF` reserve.
- MAP/base page: unchanged resulting canonical MAP, B=`2`, CPU port `$35` and
  vectors. Entry ordering now establishes that view before linked high-BSS is
  consumed.
- DMA: inherited synchronous application DMA; it must be empty before KERNAL
  ownership. KERNAL storage ownership remains exclusive.
- Timing/deadline: unchanged 100 Hz release and 21-stage order; storage occurs
  between ticks 33 and 34.
- IRQ/NMI: unchanged quiesce/restore sequence and global sticky-NMI lockout.

The direct diagnostic required two bounded target corrections: canonical entry
now precedes lifecycle/high-BSS initialization, and the platform entry uses one
all-zero MAP operation before selecting B=0 and touching `$01`/I/O. No generated
target contract, public ABI, memory ownership, stage order, production storage
ABI or measured value changed.

## Required order

1. Rebuild the complete T03 regression and reject any PRG identity drift.
2. Compile the independent runtime/SAVE oracle.
3. Create a fresh diagnostic D81 per direct-PRG run and run one clean NTSC and
   one clean PAL diagnostic. These fixtures are not the canonical carrier.
4. Exercise fresh missing-token and invalid-token fixtures and prove lockout;
   corrupt retained host inputs and prove the independent oracle rejects them.
5. Fresh-format and populate the canonical D81 exactly once, in one pinned
   `c1541` invocation; structurally validate it and extract/compare every file.
6. Mark the canonical bytes read-only. Never mount that path in Xemu.
7. For NTSC runs 1-2 and PAL runs 1-2, create a fresh byte-identical writable
   copy named exactly `R0FSUCC10.D81` in its run directory, verify its pre-run
   hash, execute it, retain the mutated image, validate the post-run filesystem,
   extract `RSSTATE`, and independently validate the target result and exact
   SAVE payload.
8. Recheck the canonical hash after all runs, retain the non-carrier evidence
   under `docs/evidence/r0f/successor/2026-09-21/`, and leave all D81 images in
   ignored local build storage because repository static CI prohibits new
   tracked D81 artifacts.
9. Freeze all reproducing source/tooling in a first commit, rebuild and repeat
   every runtime tier from that clean commit, then commit corrected evidence in
   a second commit. Stop before PR, merge, SD or physical work.

## Evidence and non-claims

T04 may establish host structure/content and Xemu runtime evidence only. It
does not establish FAT32 transfer, one-extent SD allocation, safe eject,
physical chooser loadability, physical MEGA65 behavior, measured limits,
founder acceptance or full R0-F acceptance. The canonical state after a
successful T04 is `XEMU_BOOT_VERIFIED`, not `TEST_ELIGIBLE`.

## Provenance remediation

Founder review accepted the observed runtime behavior but withdrew the Gate-3
claim because the tested copies were mounted as `run.D81` and the evidence
named the pre-T04 baseline commit. Those runs remain historical diagnostics.
They do not establish the final `XEMU_BOOT_VERIFIED` state.

The correction freezes the exact T04 source first. All accepted evidence is
then rebuilt from that clean commit, and every exact-carrier disposable copy
retains the release basename `R0FSUCC10.D81`. Any PRG or canonical D81 identity
drift stops the task rather than creating a replacement identity.
