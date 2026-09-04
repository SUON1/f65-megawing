# R0-F New-Chat Startup Prompt

Copy the complete prompt below into a new Codex chat opened on the
`codex/r0-f-development` branch.

````text
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

Begin R0-F development on branch `codex/r0-f-development`, created from the closed R0-E commit `97ead74605217df365e17eeb8d38a1d391372688`.

Goal: execute the approved AD-001 R0-F scope—physical MEGA65 execution, capture, diagnosis, and phase sweep corresponding to the accepted R0-E configuration. Produce a pinned physical-platform identity and corresponding hardware report suitable for measured-limits revision drafting. Do not freeze measured limits, select production values, open Phase 1, or implement gameplay.

Read completely before editing:

1. `AGENTS.md` and `F65_OFFICIAL_RECORD.md`.
2. `00_D81_LOADABILITY_GATE.md`.
3. Approved Read-First v1.0, AD-001, and the active approval record.
4. Both architecture files under `spec/architecture/`, plus current `memory/` and `interfaces/` contracts.
5. `docs/evidence/r0e/R0E5-D81-PHYSICAL-RUNTIME-2026-09-04.md`.
6. `docs/evidence/r0e/R0E-EVIDENCE-MAP.md` and `docs/plans/R0-E_EXEC_PLAN.md`.
7. `docs/reports/D81_MEGA65_NATIVE_SLOT_DELIVERY_2026-09-03.md` and `docs/testing/D81_FOUNDATION_QUALIFICATION.md`.
8. Relevant R0-A through R0-D handoffs and evidence identities consumed by R0-E.

R0-E input identity:

- Closure: owner-accepted bounded combined-load functional-proxy and read-only physical raster-observation proof.
- Accepted physical carrier: `F65R0EG.D81`.
- SHA-256: `ca85f73ffba93ea290078a60b372406dc6ab58eddacdf0765f7589cea039c40f`.
- Result identity: `R0E1 REV3`, `$1900-$19FF`.
- Physical observations: 100 Hz / 21-stage functional pass; snapshot ownership pass; normal/lag/shedding/one-over/pressure pass; 16 raster phase bins per case; 33-tick window; normal raw q50/q95/max bytes `020/020/020`.
- Non-claims to preserve: not CPU cycles, not input/audio latency, not elapsed-time p50/p95/worst, not a physical limit, no DMA hardware probe, no IRQ measurement, and no pinned platform identity.
- The exact Rev3 carrier did not receive a fresh Xemu rerun. R0-F must not inherit or fabricate that gate result.

First create R0-F-owned admission, ownership, execution-plan, test-guide, evidence-map, interface/ledger impact, and stage-control records. Reconcile them with the official record without editing preserved specifications or promoting draft requirements. Before implementation, state all affected 45GS02 registers/clobbers, CPU-visible and physical memory, MAP/base-page state, DMA behavior, timing/deadline effects, IRQ/NMI behavior, and exact validation commands; mark every non-applicable item explicitly.

The R0-F plan must identify, without inventing values:

- Exact R0-E source/configuration being confirmed.
- MEGA65 hardware revision and serial/board identity where available.
- Core, ROM, HYPPO, Freezer/SD Essentials, video standard/mode, clock setting, and storage identity.
- Physical measurement mechanism, units, calibration, wrap handling, sample counts, phase-bin coverage, and result encoding.
- Independent 100 Hz simulation/display phase sweep and required rolling-window/deadline evidence derived from the governing documents.
- Input/audio latency evidence, snapshot and high-water evidence, deterministic faults/shedding, reserve proof, and storage inactivity/behavior required by the admitted scope.
- Any DMA/IRQ instrumentation as a separately justified platform wrapper with explicit registers, ownership, save/restore behavior, clobbers, and failure handling. If it is not implemented and executed, retain `DMA_HARDWARE_PROBE_NOT_EXECUTED` or the equivalent exact non-claim.
- Pass/fail thresholds only when an approved source defines them. Otherwise report measured observations for human measured-limits review.

D81 construction and delivery are mandatory parts of R0-F, but do not begin by copying an old image:

1. Never use `F65R0EG.D81` or another D81 as a template or payload source. Rebuild from source payloads.
2. Choose a new, unique uppercase FAT 8.3 filename that is absent from the system card. Retire each failed tested identity permanently.
3. Fresh-format the D81 and write all payloads in one invocation of the pinned `toolchain/vice-clean/bin/c1541`; reject stderr, warnings, duplicates, truncation, allocation errors, and nonzero exit.
4. Validate exact 819,200-byte geometry, BAM, directory, sector ownership, file chains, free-block accounting, and source-versus-extracted payload hashes.
5. Run two clean Xemu boots of the exact completed D81 bytes and filename with pinned Xemu/ROM identity. Capture screen, result block, and hashes. If unavailable, stop at `NOT VERIFIED`; do not send the D81 to hardware.
6. On the MEGA65 system card, create a fresh matching root slot with Freezer `NEW D81 DD IMAGE`. A blank/reformatted system card is not an acceptable requirement.
7. Return the card to macOS without Finder-copying, replacing, truncating, or renaming the slot.
8. Fill the slot only with:
   `sudo tools/diagnostics/d81_sd_fill_mega65_slot.sh SOURCE.D81 /Volumes/MEGA65FDISK EXPECTED_SHA256`
9. Require one raw FAT32 extent before and after the in-place write, identical device offset/length, exact final SHA-256, and successful safe eject.
10. Only then request physical chooser and runtime evidence for that exact filename/hash.

Why this delivery method is mandatory: normal `cp`/Finder replacement produced exact hashes but 5, 13, and 15 FAT32 extents and chooser failures. The successful route used the MEGA65 Freezer's own contiguous 819,200-byte allocator, then replaced only the slot bytes using `dd conv=notrunc`; `F65R0EG.D81` remained one extent at the same device offset before and after fill and mounted successfully. Do not recommend a blank card or blame the SD card/MEGA65 hardware.

Current official Freezer source maps `0x8B` to `IMAGE FRAGMENTED`; `ERROR CODE FF` is a generic/legacy chooser-stage failure and does not, by itself, prove fragmentation. Diagnose with exact hash, raw FAT extent evidence, D81 structure/content, and platform identity.

Work autonomously through safe host-side admission, implementation, and verification. Stop for user action only when owner ROM access, administrator authentication, SD-card movement, MEGA65 operation, platform identity, or physical capture is genuinely required. Keep the user updated, commit focused changes, push `codex/r0-f-development`, and never mark R0-F passed until the complete physical evidence is reviewed and explicitly accepted by the owner.
````
