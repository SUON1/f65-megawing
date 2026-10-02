# R0-F Group 1 P04: bounded physical handoff

Owner approval on 2026-10-01: "Approved: separately approve SD delivery/carrier
checks and the bounded Group 1 hardware test."

This approves the unchanged candidate and the gates below. It does not add
target features, authorize another delivery route, merge, or establish full
Group 1/R0-F acceptance. The checkpoint was published as
`2d9a42e110cdd9066031e28e83662ce4fdec6219`; these handoff updates are local.

## Current disposition: stopped at SD allocation

The owner Finder copy and subsequent authenticated raw audit have completed.
The exact short name, 819200 bytes and canonical hash match, but the file
occupies **10 physical FAT32 extents**. The saved raw audit is
`build/r0f/group1/physical/R0FG1P04/sd-copy-01.json`, SHA-256
`ecab0a4e2cb67eff92c2b9ad1de998b787a643545d28f42df9dbe29ffb6b2a69`.
State: `INVALID_FOR_MEGA65_FREEZER_MOUNT` — **DO NOT USE THIS SD COPY**.
No chooser, physical run or safe-eject gate was performed by the agent.

P04 is retired from further delivery/test attempts; preserve the failed copy,
audit and unchanged host canonical. Do not delete, rename, overwrite or retry.
The preparations below are retained, not current instructions to test P04.
This failure is SD allocation, not evidence of incorrect PRG/D81 payloads or
a defective card. No program correction or target rebuild is indicated.

Recommended next route, pending explicit approval: a fresh `R0FG1P05.D81`
delivery identity with exactly the same PRG, repeated host/exact-name Xemu
carrier gates, then the pinned contiguous allocator used for CAP14. Its retained
16-test qualification matches current wrapper/test/inspector/lock/executable
hashes. Live clean filesystem, equal FATs, sufficient free run, no collisions,
metadata preservation and staged/final/mounted hash/one-extent checks remain
mandatory before safe eject. This recommendation does not authorize raw writes
or promise a pass. The separately authorized native-slot route is a fallback,
not a request for another blank-card trip now.

Subsequent owner reply "Begin" approved P05 preparation and the owner-run
allocator route. P05 later passed delivery and physical entry but failed
post-storage display resume; it is also retired. See
[campaign closeout](R0-F_GROUP1_CLOSEOUT.md) for the actual returned data and
remaining blocker. Its [delivery preparation](R0-F_GROUP1_P05_DELIVERY_PREPARATION.md)
is historical and must not be repeated.
That does not restore P04 eligibility or permit retrying its failed SD copy.

## Frozen identity and current state

- Candidate: `R0FG1P04.D81`, 819200 bytes; disk label `R0FG1P04`, ID `65`.
- Canonical path:
  `/Users/slice/Developer/f65-megawing/build/r0f/group1/carriers/R0FG1P04/canonical/R0FG1P04.D81`.
- D81 SHA-256:
  `2519af02741197fb8851dccc26ab1379591d5340f1cae3b68cb243844c3730d4`.
- Contained `R0FSUCC` PRG SHA-256:
  `c068cc532dc820845d8c0649b1c2ea7dfc0bda394b32f7c186088a04d0dc048b`.
- Entry: the existing `AUTOBOOT.C65` flow loads `R0FSUCC` on device 8 and
  enters at `$31A6`. Do not load a different/root rebuilt PRG.
- Branch: `codex/r0f-successor-physical-exact-carrier`.
- Original host-gate source base: `9e2ffdb4786e4794119933a5edd4b1cf79f653f0`.
  The later preservation commit captures the exact isolated candidate inputs;
  it does not change the candidate bytes or rewrite historical provenance.
- Historical canonical state: `XEMU_BOOT_VERIFIED`; its bytes remain unchanged.
  Failed SD copy state: `INVALID_FOR_MEGA65_FREEZER_MOUNT`; physical `NOT RUN`.
  It is not hardware-loadable or `TEST_ELIGIBLE`.

Read-only preflight rechecked the canonical hash, pinned candidate/controller
inputs, D81 structure and retained extracted payload hashes, plus capacity and
operator-screen admission for `ntsc-01`, `ntsc-02`, `pal-01`, `pal-02`. All pass.
No rebuild or new Xemu run was performed.

The mounted card is `/Volumes/MEGA65FDISK`, removable MS-DOS FAT32, VolumeUUID
`83FFC12E-67E1-307F-91AD-E584C2E01E87`; the destination filename was absent at
initial preflight and is now present as the retained failed copy. Device numbers
must be resolved again before raw audit or ejection,
especially after reinsertion. This identity check is not an allocation pass.

## Delivery gate: owner Finder copy, then audit

1. Owner copies the canonical file with Finder into the card's root as exactly
   `R0FG1P04.D81`. Never overwrite or rename an existing file. Do not open or
   modify its contents, create a replacement blank, or copy a runtime/Xemu disk
   that already contains trace files. Tell the agent when the copy is complete.
2. Leave the card in the Mac. The agent independently runs the existing
   `tools/diagnostics/d81_sd_contiguity.py` raw FAT32 root-only inspector with
   `--fat32-root-only` and the expected hash above, retaining a fresh local
   report. Require the exact uppercase short name, 819200 bytes, matching raw
   hash and exactly one extent. Administrator authentication, if needed,
   stays in the owner's local Terminal, never in chat.
3. Only after the audit passes, flush and safely eject the positively identified
   card, retaining the successful eject result. Until then, do not put it in
   the MEGA65. A Finder/hash pass alone is insufficient.

Any absent/ambiguous audit, wrong hash, unexpected name/alias or fragmentation
stops delivery. Preserve the failed copy and evidence; do not overwrite, rename
or retry it. Raw allocator or native-slot fallback requires a specific route
decision, not an automatic switch. Never mount the host canonical writable.

## Physical gate and one bounded run

After the SD gates and safe eject pass:

1. On the MEGA65, select exactly `R0FG1P04.D81`. Record successful chooser
   mounting and readable directory, then use the documented `AUTOBOOT.C65`
   flow. Photograph the selected filename/build identity or running diagnostic.
   Any chooser/entry error stops immediately; do not retest that failed copy.
   Only recorded chooser/entry success establishes `TEST_ELIGIBLE` for it.
2. Allow this unchanged program **one run**, using the existing focused
   **120-second allowance from entry**. It performs 3200 ticks, its one
   returning-storage transition, the resumed acquisition and terminal export.
   Use the current hardware video mode and record it; this approval does not
   require an additional physical NTSC/PAL sweep or interactive stress cases.
3. On completion, photograph the whole terminal screen. Expected export-only
   summary:

   ```text
   G1 EXPORT S:4 E:00 F:14
   4=OK 5=FAIL / E,F HEX
   REDUCE FOR TIMING
   NOT ACCEPTANCE
   RESET
   ```

   `F:14` is hexadecimal for twenty files; their decimal names are
   `G1T00` through `G1T19`. Green/`S:4` is completed export, not timing acceptance.
4. For `S:5`, nonzero export error, unexpected file count, lockout or no terminal
   summary within the allowance: record the exact screen and elapsed time,
   stop the test sequence, and do not restart or extend the run. Do not remove
   the card or power off during apparent disk activity; retain the state and
   request guidance if writes have not stopped.
5. Once disk activity has stopped, photograph before resetting/powering down,
   power down safely and return the card to the Mac. Do not rerun this disk:
   the trace/SAVE names now exist and must not be replaced.

## Returned evidence and decision

Preserve a new read-only host snapshot of the actual returned D81, with its
post-run hash; never replace the canonical. Independently check structure,
original payloads, actual `RSSTATE`, all twenty chunks, trace integrity,
capacity and nominal timing. Use the existing reducer and independent SAVE
oracle, not an emulator SAVE, synthesized trace or screenshot transcription.
The legitimate added files will change the returned D81 hash.

Review that physical result with the owner. Passing host/Xemu or an export
summary cannot substitute for the returned-byte reduction. Group 1/R0-F
acceptance remains a separate owner decision; Groups 2/3 are not included.

Authority: `AGENTS.md`, `CURRENT_STATE.md`, `WORK_IN_PROGRESS.md`, development
workflow, Group 1 Build Intent and export amendment, generated export/trace
contracts and memory ledger, root D81 loadability gate and D81 workflow.
These changes are documentation only: no new register/clobber, CPU-visible or
physical allocation, MAP/base-page, DMA, timing/deadline or IRQ/NMI effects.
Generated artifacts are unchanged. During the approved physical run the
existing terminal export writes only the admitted new SAVE/trace files inside
the copied D81 and cannot return to measured work.
