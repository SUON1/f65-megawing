# Group 2 first physical subcase — export collision

2026-10-03. Approved prospectively within the broader fault/pressure suite;
historical Group 2 allocation remains unrecovered. No Group 3 scope is inferred.
Hardware precedes publication; no commit or push has occurred.

2026-10-04 continuation: owner authorized fresh L3 construction; its separate
[qualification packet](../2026-10-04-l3-carrier/README.md) now records host/four
exact-name Xemu PASS with unchanged payloads. L2's invalid SD copy and all
records below remain preserved. Earlier replacement-not-created statements
describe the handoff before that authorization; raw SD delivery is still pending.

**Case: G2-L-EXPORT-COLLISION.** Does the actual terminal exporter reject the
existing first chunk name without overwrite, additional trace files or retry?
The governing no-overwrite/terminal-lifetime contracts and current Build Intent
define the expected result. The fresh disk contains `G1T00` with the harmless
34-byte TOKEN fixture. This exercises the real SAVE error path after the full
combined workload, without destructive media operations or new target injection.

## Candidate identity and current gate

Canonical host path:
`/Users/slice/Developer/f65-megawing/build/r0f/group2/control/trial-jnt4dplw/carrier-l2/canonical/R0FG2L2.D81`.

- Image: **819200 bytes**, SHA-256
  `3a2a90c21e10fb7c753ef48d3e6307f45c98aeab26de55694f4709a1d795a134`.
- Disk label `R0FG2L2`, ID `65`; entry `AUTOBOOT.C65`, loading exact `R0FSUCC`.
- Program: 37284 bytes, SHA-256
  `46491ef275863dd89edd2af420092e7baff733b5b5e54064ea52cfcfbbb09f92`.
- Program banner `R0FG2C1` identifies the normal control; `R0FG2L2` identifies
  this disk fixture. The final existing terminal text still begins `G1 EXPORT`.
- Host structure/content PASS. **Two NTSC and two PAL exact-name disk boots PASS**;
  [release.json](carrier-l2/canonical/release.json) records `XEMU_BOOT_VERIFIED`.
  The original release is preserved. The owner's subsequent Finder SD copy
  passes exact bytes/hash/short name but **fails contiguity: 39 extents**.
  That SD copy is **INVALID — DO NOT USE**. Safe eject, physical chooser/entry
  and runtime are NOT RUN. This is not TEST_ELIGIBLE or Group 2 complete.

Branch `codex/r0f-group2-preparation`, HEAD/fetched main
`abd3a0803b96090654db5dbdda43ad42d7b29a5a`; source changes are uncommitted.
`build/result.json` identifies the complete frozen copied input; it preserves the
compile-time disposition. Later run records establish their separate tiers.

## Reused and new evidence

R1/R2 actual owner definitions are matched exactly to the retained sanitizer
tests: 1484 poisoned scratch handoffs and 256 independent nine-byte encoder cases.
The changed control removes the startup-only queue probe, retaining the full
fixture, CRC/guard checks, capacities and thresholds. End $BD16, 746 bytes free;
protected allocation and compiler static stack remain 4495 and 36 bytes.
New NTSC/PAL normal-control traces validate all 3200 records, twenty chunks,
actual SAVE, capacity/reserve checks and zero nominal deadline/floor/boundary
failures. Those are Xemu results, not new physical timing proof.

New direct collision observation passes: actual state 5/error 3/files 0,
unchanged TOKEN/G1T00, valid returning SAVE and complete lifecycle result in
Xemu memory. Exact carrier boots additionally verify ordinary loader/entry
and preservation of AUTOBOOT/R0FSUCC. No PRG injection is used in these boots.
Actual screenshots are decoded and compared to the retained readable collision
glyph pattern, translating position only for PAL/NTSC; blank or changed glyphs
fail. Dumped text and protected status are checked separately.

L1 was mistakenly stopped after a misread preview. Its PNG is exactly the same
as the retained passing collision screenshot and contains 3194 white text pixels.
`carrier/observer-correction.json` preserves that finding alongside the initial
stop record. L1 remains withheld and is not retested, repaired or renamed.
Fresh L2 repeats the applicable gates with the corrected pixel check; no target
code or D81 contents were changed to address an unproven display defect.
The earlier sandbox/config-file launch failure is retained separately as a
pre-execution environment failure. Its disk/source identity is never reused.

The returned-file checker has one actual-byte positive case and nine focused
changed/missing/extra-payload negatives. This validates the checker, not owner
fault behavior; actual Xemu execution supplies that lower-tier proof. A complete
read-only extraction of L2's new post-run NTSC image also passes the checker,
leaving physical chooser/photo evidence explicitly pending.

## SD allocation failure and proposed recovery

The owner executed the read-only raw audit in the `hs_admin` CLI session.
[Original audit](sd-finder-01/raw-audit-owner.json) and
[derived failure record](sd-finder-01/allocation-failure.json) retain exact
819200-byte/hash/short-name PASS and all 39 extents. Independent coverage checks
confirm every logical byte is accounted for without overlapping physical ranges;
mounted and canonical hashes still match. The failed layer is SD allocation,
not D81 payload construction or evidence that the card is defective. Earlier
authentication/permission attempts and the pending record remain as history.
Preserve `R0FG2L2.D81` on the card unchanged; do not recopy, overwrite, rename,
repair or send it to the chooser. No SD write or new hardware run occurred.

**Proposed, awaiting owner authorization:** use fresh identity `R0FG2L3.D81`
with identical program/bootstrap/TOKEN/G1T00 payloads, fresh single-session
construction and all host/four exact-name Xemu gates. Correct allocation with
the pinned official contiguous allocator, executed by the owner in their CLI
session. A new identity isolates the failed copy; it is not a payload fix.
The CAP14 retained fixture qualification matches all eight current tool/lock
hashes and is reusable without rerunning passing fixtures. This route has one
bounded CAP14 physical success, as recorded in the current D81 workflow.

The live installer must re-identify the removable FAT32 partition/VolumeUUID,
refuse destination/staging aliases, unmount without force, pass clean read-only
filesystem/matching-FAT/actual free-run checks, retain metadata off-card and
verify staged/final raw hash and one extent, mounted readback and safe eject.
It writes data and FAT metadata and is not power-loss transactional. Raw writes
and the fresh identity require the specific owner decision in the D81 workflow
and gate; neither is authorized or executed by this record. No replacement
has been created. Do not repeat Finder copying or require another native blank.

## Planned hardware procedure — withheld for failed L2

The [refined physical test](../../../../plans/R0-F_GROUP2_HARDWARE_TEST.md)
is the current review plan. It separates the delivery decision, minimum physical
capture, actual returned-card checks and call-stage evidence limitation.

The following L2 procedure describes the qualified case before the allocation
failure. **Do not execute it for L2.** Reissue it with the exact new artifact
identity only after owner-authorized recovery passes every delivery gate.

1. Use the exact canonical path above for the owner's Finder copy to the MEGA65
   FAT32 root. Preserve P09, L1 and all older files. Do not overwrite an existing
   `R0FG2L2.D81`. No automatic CLI/raw-card transfer is authorized.
2. Before chooser testing, independently audit the copied hash, exact uppercase
   short name, 819200 bytes and **one FAT32 extent**, then safely eject. The
   repository's read-only raw audit is `tools/diagnostics/d81_fat32_audit.py`;
   positively identify the currently mounted partition before using it. A Finder
   copy alone does not pass delivery. Multiple/unknown extents stop the sequence.
3. On MEGA65, choose exactly `R0FG2L2.D81`. Capture filename/chooser evidence,
   confirm no attach error, read the directory, and load `AUTOBOOT.C65`. A chooser
   failure stops here and retires that tested copy; do not rerun or repair it.
4. Let this single run finish. Expected final screen is red with:
   `G1 EXPORT S:5 E:03 F:00`, `4=OK 5=FAIL / E,F HEX`, `REDUCE FOR TIMING`,
   `NOT ACCEPTANCE`, `RESET`. Photograph the screen and record the actual video
   mode/core/HYPPO/ROM/Freezer identities. S5/E03/F00 is the deliberate collision,
   not a nominal export success. Any other result stops the case.
5. Power down safely and return the card. Preserve the mutated image unchanged.
   Read-only validation must show exactly the original AUTOBOOT/R0FSUCC/TOKEN/
   G1T00 plus `RSSTATE`, unchanged four input payloads, correct 34-byte SAVE,
   valid BAM/chains and no additional trace chunks. Do not remove G1T00 to retry.

The host checker command, after a verified release exists, is:

```sh
python3 -B tools/diagnostics/r0f_group2_collision_return.py \
  --image /PATH/TO/RETURNED/R0FG2L2.D81 \
  --release build/r0f/group2/control/trial-jnt4dplw/carrier-l2/canonical/release.json \
  --out build/r0f/group2/physical-collision-return-01
```

It reads the image only and creates fresh host evidence. Its PASS deliberately
leaves chooser/operator-photo confirmation pending. The SAVE encodes only the
pre-storage checksum fixture; it does not contain the full lifecycle result or
timing trace. Physical timing and complete resumed-service proof are not supplied
by this collision card. Retained P09 nominal results keep their original bounds.

[Read-only inspection of the four retained Xemu dumps](retained-save-path.json)
locates first SAVE failure: secondary 1, first staged chunk, full remaining
bytes and consumed permit distinguish it from initialization failure. Physical
S5/E03/F00 alone exposes neither that phase state nor DOS status-channel text.
No new execution was needed to locate this existing emulator evidence.

## Remaining work and impact

No new target register/clobber, resident state, physical-memory, MAP/base-page,
DMA, timing or IRQ/NMI effects are added for this disk stimulus. R1/R2 already
change private scratch ownership and call costs; their new control was qualified
at host/fit/Xemu tiers. Public/generated ABI, trace-v7, capacities/reserves and
all existing checks/acceptance thresholds remain unchanged. The private scratch
header was generated in the frozen copy; the v8 capture drafts are not executed.

This case closes only export-collision physical behavior after its required
photo/card evidence passes. G2-Q/S/P/D/A and other G2-L cases still need their
declared evidence/dispositions; the live queue capture still exceeds resident
fit by 511 bytes. Policy conflicts require an owner decision. Delivery choice,
full-suite review, measured limits, R0-F acceptance and publication stay separate.

`SHA256SUMS` covers the retained packet. Large D81/memory/SD originals stay in the
local experiment with identities in `local-artifacts.json`; canonical images
are never mounted writable. No P09 or historical proof was executed or changed.
