# P06 physical resumed-workload proof — 2026-10-02

Status: SD delivery PASS; reported physical runtime FAIL at tick 3200.
P06 is INVALID — DO NOT USE. See the [physical observation](../evidence/r0f/group1/2026-10-02-p06-physical/README.md).
[Returned-card analysis](../evidence/r0f/group1/2026-10-02-p06-physical/returned/README.md)
passes structure, original payloads and actual tick-1600 SAVE; no G1Txx files
exist. Explicit photo-filename/video-mode confirmation remains pending.
Do not repeat the installer. The preparation instructions below are historical.
The owner requested physical resumed-workload proof after the qualified
[resume correction](R0-F_GROUP1_RESUME_RECOVERY.md). This advances that exact
candidate to one physical attempt. Group 1's physical blocker remains open;
Group 2 has not started and acceptance is not implied.

## Confirmed SD delivery

The owner ran the prepared installer once. Its retained
[log](../../build/r0f/group1/carriers/R0FG1P06/sd-install-01.log),
[staging audit](../../build/r0f/group1/carriers/R0FG1P06/sd-install-01/staging.json),
[final audit](../../build/r0f/group1/carriers/R0FG1P06/sd-install-01/final.json) and
[SD release](../../build/r0f/group1/carriers/R0FG1P06/sd-install-01/sd-release.json)
confirm the expected P06 hash and one 819200-byte extent at device offset
63926272. Exact short filename is `R0FG1P06.D81`; volume UUID matches.
Pre/post read-only filesystem checks completed, mounted verification passed,
and safe eject passed. File count rose 185 to 186 and free space fell by
800 KiB / 200 clusters, consistent with the image; raw audits independently
establish contiguity. Canonical bytes remain unchanged.

Current state is `AWAITING_PHYSICAL_CHOOSER_VERIFICATION`. The run instructions below are historical; do not repeat them. The new photos show final tick 3200 and service mask 1F, but terminal
preparation failed with 6B; independent workload proof remains incomplete. No further card operation was performed during this review.

## Authority and scope

Inspected AGENTS, CURRENT_STATE, WIP, development workflow, the Group 1 Build
Intent, measurement matrix, export amendment, recovery report and frozen
source/evidence, root D81 gate, D81 workflow and pinned allocator implementation.
Remote main remains `c27d89787d1d5c4472e24262e0181c47943d46be`.

Prepare the release manifest and owner-run installer, verify the unchanged
qualified inputs, then collect actual chooser/entry and resumed-workload data.
The owner-run route preserves the workflow's transfer preference. Its raw FAT
allocation requires local administrator authentication and all live checks.
No target build, Xemu rerun, feature/capacity/threshold change or publication
is included. P05 and every tested predecessor remain untouched.

This preparation changes off-card records only. Registers/clobbers,
CPU-visible/physical allocations, MAP/base-page, DMA, timing/deadlines and
IRQ/NMI effects are non-applicable to these edits. Physical execution exercises
the unchanged P06 contracts described in the recovery report. Generated
interfaces remain unchanged.

## Exact candidate and preparation checks

- `R0FG1P06.D81`: 819200 bytes, SHA-256
  `4f046112e8343c211ab5cc81caec2a85aa85e7d323e6c8a23019d513d4b592bf`.
- Contained PRG: 37505 bytes, SHA-256
  `9654d336deefe8dae0bd3b26986e00fbea45b8f3dcd8cfe0b1c73ac3f479ef7e`.
- State: `XEMU_BOOT_VERIFIED`; four retained exact-name boots pass.
- Fresh read-only checks: canonical structure/content, qualified copied-source
  and controller input hashes, four retained disk hashes and allocator
  qualification identity PASS. No emulator rerun was needed.
- An initial input audit resolved copied build paths against the older root
  tree and rejected its different generated table. Resolving them against the
  recorded isolated source root passed; no source or generated output changed.
- Mounted card: removable MS-DOS FAT32, UUID
  `83FFC12E-67E1-307F-91AD-E584C2E01E87`, currently `disk4s1`,
  `/Volumes/MEGA65FDISK`, 4096-byte allocation units. Mounted directory has no
  P06 final/staging filename. Device identity is re-resolved by the installer.
- Raw alias/free-run, clean filesystem, SD hash/extent and safe-eject checks
  remain live installer gates; the mounted directory check does not replace them.
- Source is the uncommitted copied-source correction, identified by the frozen
  recovery packet and exact input hashes. Baseline commit alone does not
  reproduce P06. The local publication step remains separate.

The manifest is
[`release.json`](../../build/r0f/group1/carriers/R0FG1P06/release.json).
The canonical image has not been mounted writable or copied to the card.

## Owner installation

Run once in Terminal:

```sh
sudo /bin/bash /Users/slice/Developer/f65-megawing/build/r0f/group1/carriers/R0FG1P06/install-p06.sh
```

The [script](../../build/r0f/group1/carriers/R0FG1P06/install-p06.sh) invokes the
unchanged pinned allocator, rejects existing final/staging identities and
prior attempts, unmounts without force, requires clean read-only filesystem
checks, retains metadata, verifies staged/final/mounted hashes and one extent,
then safely ejects. Output is retained in `sd-install-01.log` beside the script;
raw evidence is retained in `sd-install-01/`. Do not repeat after any failure.
Do not use Finder to copy this candidate or create another blank image.

Proceed to hardware only after the installer ends with:
`SD copy, one extent, mounted hash and safe eject PASS; physical chooser pending`.
Any failure stops the sequence; preserve the output for review.

## One physical run and return

1. Put the safely ejected card in the MEGA65. Record the current PAL/NTSC mode
   and available core, ROM, HYPPO and Freezer versions, preferably with a photo.
   Missing identities remain unrecorded; do not substitute Xemu identities.
2. Select exactly `R0FG1P06.D81` on device 8. Record chooser success and entry
   via `AUTOBOOT.C65` / its normal autoboot flow. A chooser error stops the run;
   photograph it and retain the carrier without repair or retry.
3. Let the diagnostic finish. The expected completed-export screen is
   `G1 EXPORT S:4 E:00 F:14` (hexadecimal 14 means 20 chunks). Photograph the
   entire screen and confirm the selected filename. This screen reports export
   completion; independent trace reduction still determines workload/timing.
4. If it faults or stops progressing, photograph all displayed fault/state/
   tick/mask/NMI fields and report elapsed time. Do not reset and rerun P06.
5. Once the terminal screen is stable and disk activity has stopped, power
   down and return the card to the Mac. Leave the image untouched for read-only
   snapshot/extraction. No second PAL/NTSC physical run is requested on P06.

## Actual proof to close the blocker

Read the returned card into a host-only immutable snapshot and compare again.
Independently parse chains/BAM and extract with pinned c1541; verify original
payloads unchanged. Validate actual `RSSTATE` against the independent tick-1600
model and reconstruct the actual `G1Txx` exports with the matching version-7
reducer. Require the complete 3200-record capture, post-storage ticks 1601–3200,
resumed service/IRQ/model lineage, actual terminal result and export integrity.
Apply the existing timing predicates and report physical calibration limits
separately. Never substitute emulator bytes for physical results.

A failure or missing export remains a physical blocker with its exact evidence.
A passing resumed workload closes this blocker, then reconcile the original
Group 1 admission/matrix requirements before advancing the approved Groups 2–3
campaign. Do not invent additional production features. Owner acceptance,
measured-limit approval and full R0-F acceptance remain separate decisions.
