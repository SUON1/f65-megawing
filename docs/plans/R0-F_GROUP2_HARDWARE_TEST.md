# R0-F Group 2 — bounded physical export-collision test

**L3 physical terminal/returned-card observables PASS — operator record incomplete.**
Updated 2026-10-04 with the [physical acquisition](../evidence/r0f/group2/2026-10-04-l3-physical/README.md).
Owner confirms L3 selection/ordinary entry; safe eject and one-run/no-restart
remain unconfirmed, chooser photo absent, actual configuration UNKNOWN. Earlier
pre-run gates below are preserved; no new physical run is needed to fill record
gaps, and the earlier raw allocator proposal was not executed by the agent.
Control source/payload identities are unchanged. The original broader-suite
proof remains incomplete; the current work package is now closed under the
[owner-approved bounded disposition](../reports/R0-F_GROUP2_CLOSEOUT_REVIEW.md).
Operator gaps and missing proof carry into the upcoming review; no rerun.
This refines G2-L-EXPORT-COLLISION under the prospectively approved
[Group 2 Build Intent](R0-F_GROUP2_BUILD_INTENT.md). It does not recover a
historical Group 2 allocation, assign Group 3 or close the broader suite.

## Decision and controlling contracts

With an occupied first trace filename, does the actual terminal exporter
report failure, preserve all pre-existing payloads and leave no successful
trace export? This is a bounded failure/lockout observation after the combined
fixture, not physical timing or complete resumed-service proof.

The [generated export contract](../../interfaces/r0f_group1_export_contract.json),
[export amendment](R0-F_GROUP1_EXPORT_AMENDMENT.md),
[export memory ledger](../../memory/r0f-group1-export-memory-ledger.json),
[successor admission](../reports/R0-F_SUCCESSOR_ADMISSION_RECONCILIATION.md),
[D81 gate](../../00_D81_LOADABILITY_GATE.md) and
[delivery workflow](../D81_WORKFLOW.md) govern. Retain capsule consumption,
readiness/integrity checks, no replace syntax, no automatic retry and no return
from terminal ownership. No target implementation or generated layout changes
are made here. Registers/clobbers, CPU-visible/physical memory, MAP/base-page,
DMA, timing/deadline and IRQ/NMI effects are non-applicable for this refinement.

## Evidence located, missing proof and owner decision

| Classification | Concrete finding / disposition |
| --- | --- |
| Existing evidence located | Four retained L2 NTSC/PAL memory dumps distinguish first SAVE failure: secondary 1 after successful initialization, staged chunk 16384, remaining 327680, filename G1T00, S5/E03/F00 and consumed permit. See [read-only inspection](../evidence/r0f/group2/2026-10-03-export-collision/retained-save-path.json). No execution was repeated. |
| Existing evidence reused | Actual-owner R1/R2 host proof, normal control acquisitions and retained P09 nominal physical proof. Current eight-input CAP14 allocator qualification is reused. L3 has its own new host/four exact-name boots and returned-file check; L2 boots were not substituted or repeated. |
| Physical evidence now located | Owner confirms exact L3 selection/ordinary entry; readable terminal photo and actual returned-card structure/payload/SAVE checks pass. Safe eject/one-run confirmation and chooser photo remain record gaps; do not replay the carrier to fill them. L2's fragmented copy supplies no physical proof. |
| Additional physical proof not captured by this carrier | S5/E03/F00 and returned files do not uniquely distinguish OPEN/CLOSE initialization failure from first SAVE failure. They do not record DOS status-channel text, attempt count, the full lifecycle result or timing. A strict physical call-stage claim needs a separately qualified observation/instrumentation increment. |
| Delivery disposition | Owner-supplied L3 audit passes exact name/hash/size and one extent. The card was used and returned; no allocator write was executed by the agent. Safe ejection remains unconfirmed. No further delivery action or raw write is authorized by this record. |

The shared terminal error handler stores the failed KERNAL call's A register;
E:03 is hexadecimal, not a uniquely identified DOS error or a physical call
log. The retained Xemu state provides call-stage proof at that tier only.
No-retry control flow is established by the frozen owner implementation;
physical evidence establishes the terminal disposition and file effects.
Do not silently turn either into a measured physical retry count.

## Recorded release gates before the owner run

`R0FG2L2.D81` on SD is **INVALID — DO NOT USE**: exact bytes/hash/short name
pass, allocation fails with 39 extents. Preserve it, L1, P09 and older carriers.
Do not overwrite, repair, rename, recopy or test them. This is an allocation
failure; changing the program or repeatedly copying with Finder is not a fix.

`R0FG2L3.D81` began this procedure as **XEMU_BOOT_VERIFIED / NOT DELIVERED**. Its own
[qualification packet](../evidence/r0f/group2/2026-10-04-l3-carrier/README.md)
records 819200 bytes and SHA-256
`c3df1ceda3979cf6e49e7885b563555379c7d64557360bed0d288144085092e5`.
Canonical path:
`/Users/slice/Developer/f65-megawing/build/r0f/group2/control/trial-jnt4dplw/carrier-l3/canonical/R0FG2L3.D81`.
Its own canonical release.json records host/four exact-name PASS, not L2's hash
or boot records. Program remains R0FG2C1; disk identity is R0FG2L3.
Fresh construction and independent extraction retain these exact payloads:

| On-disk file | Bytes | SHA-256 |
| --- | ---: | --- |
| AUTOBOOT.C65 | 466 | 32ef6c98a4bc54c3107751e1300684d11ffe6435f55a7e9e467b428b83c2810f |
| R0FSUCC | 37284 | 46491ef275863dd89edd2af420092e7baff733b5b5e54064ea52cfcfbbb09f92 |
| TOKEN | 34 | 0e8d0ac2ce727ba51285be0173ea784b52b56fdc4729a1f7c0d2d7271005b572 |
| G1T00 | 34 | 0e8d0ac2ce727ba51285be0173ea784b52b56fdc4729a1f7c0d2d7271005b572 |

There is no pre-existing RSSTATE or other trace chunk. G1T00 is a harmless
occupied-name fixture, not a damaged trace or a destructive storage fault.

Fresh single-session construction, independent structure/extraction and two
NTSC/two PAL exact-name disk boots passed. The
[exact owner CLI proposal](../evidence/r0f/group2/2026-10-04-l3-carrier/OWNER_DELIVERY.md)
is prepared from that release, not executed. After the separate delivery
decision, use the
owner's existing CLI session; do not launch another user's Terminal or transfer
automatically. The installer must resolve the current removable FAT32 volume,
refuse destination/staging aliases, unmount without force, pass clean read-only
filesystem/matching-FAT/free-run checks, retain metadata off-card, verify staged
and final raw hash/one extent, mounted readback and safe eject. A raw write is
not power-loss transactional. Any failure stops; no automatic retry or repair.

Only a reviewed `sd-release.json` with matching release identity, exactly one
extent and safe-eject PASS permits the chooser/entry check. It does not confer
hardware-loadable, TEST_ELIGIBLE or runtime PASS before physical entry is seen.

## One owner run, two required photographs

1. Record the actual video mode and core/HYPPO/ROM/Freezer identities from the
   physical configuration where available. Unknown values remain UNKNOWN;
   never fill them from Xemu. Preserve the delivery report and exact D81 hash.
2. Select only the newly qualified exact filename. Photograph the chooser
   filename, confirm attach succeeds and the directory is readable, then run
   AUTOBOOT.C65 through the ordinary entry path. Record entry confirmation.
   An attach or entry failure stops the case before wider runtime testing.
3. Let one run finish without input, reset, reload or a second attempt.
   Photograph the full readable terminal screen and border. Expected:

   ```text
   G1 EXPORT S:5 E:03 F:00
   4=OK 5=FAIL / E,F HEX
   REDUCE FOR TIMING
   NOT ACCEPTANCE
   RESET
   ```

   The red border is expected for this deliberate rejection. Red alone is
   insufficient. S4/E00/F14 would fail this occupied-name case even if it looks
   like a nominal export success. G1 EXPORT remains the existing terminal text.
   A new elapsed-time acceptance threshold is not introduced; record observed
   elapsed time if available. Missing terminal output is incomplete evidence.
4. Retake an unreadable photograph of the same halted run if needed; do not
   restart it for a better photo. Record unexpected output exactly, then stop.
   A blank/unclear photograph does not by itself prove a target display defect.
5. After terminal capture, power down safely and return the card. Preserve the
   mutated D81 and its filename. Do not delete G1T00, inspect it by executing
   the program again, or remove any other card file.

Operator note: exact filename; chooser/attach/directory/entry observed;
actual video/configuration identities or UNKNOWN; terminal photo and result;
one run/no restart; card returned. Two clear photos plus this note avoid a
large trace transcription. Uncertain identity or missing configuration stays
an evidence gap rather than being inferred from a passing emulator run.

## Returned-card checks and bounded completion

Take a fresh host-only snapshot with the exact returned filename and record
its hash before inspection. Preserve actual photos, owner note and delivery
record together. The post-run image hash is expected to differ from canonical
because RSSTATE was added; original payloads must still match exactly.

Use the existing read-only
[returned-file checker](../../tools/diagnostics/r0f_group2_collision_return.py)
with that snapshot, L3's own verified canonical release and a fresh output
directory under `build/r0f/group2`. A read-only check of the new L3 PAL post-run
image passes; it remains emulator evidence, not a returned physical card.
Do not substitute the old L2 command/release or an emulator snapshot for the
future physical acquisition.

Required returned contents: exactly AUTOBOOT.C65, R0FSUCC, TOKEN, original
G1T00 and correct 34-byte RSSTATE. Independently validate directory/BAM/chains,
all four unchanged payloads, SAVE load address/checksum and absence of extra
trace files. The checker deliberately returns
`RETURNED_FILE_CHECKS_PASS_OPERATOR_PHOTO_PENDING`; combine it with identified
physical entry and readable operator evidence, never promote it alone.

Completion is only the observable occupied-name rejection/preservation subcase
for the recorded configuration. Unexpected status, changed payload, bad SAVE
or extra chunk fails; missing/uncertain evidence remains incomplete. Retain
each result without fixing/retrying its carrier. Physical SAVE-call provenance,
retry counting, full lifecycle/service state and timing are not established by
this card. The other G2-L cases and G2-Q/S/P/D/A remain open; full Group 2/R0-F
acceptance, measured limits and publication remain separate decisions.

The L3 owner run and actual returned-card checks have now occurred. Finish the
operator-record review without new execution; subsequent implementation work
remains live capture fit/schema/reducer and the other approved owner cases.
If strict physical SAVE
branch discrimination is required for closure, first specify a compact phase
observation under the existing owner/fit contracts; this plan does not add it
or replace the existing S5/E03/F00 expectation.
