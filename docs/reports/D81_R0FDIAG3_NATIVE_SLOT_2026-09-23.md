# R0FDIAG3 native-slot delivery — 2026-09-23

## Scope and owner decision

The authorized task is to place a fresh exact-name T06 diagnostic in the
previously MEGA65-formatted, never-tested `R0FDIAG3.D81` root blank. The owner
approved changing only that blank after verification. No repair, deletion,
reformat, raw FAT metadata allocation, or change to another card file was
authorized.

The separate `R0FHOST2.D81` direct allocator stopped before writing because
read-only `fsck_msdos -n` reported a preexisting cross-link/underallocation in
`/A. MegaWing/F65BLK02.D81` and orphan clusters. Do not bypass its clean-card
gate. The mounted native blank route changes the pre-existing file's data in
place and has separate allocation and content gates.

## Current evidence

| Item | Identity or result |
| --- | --- |
| Native blank before fill | `R0FDIAG3.D81`, 819200 bytes, SHA-256 `357078cd97a9aae0bf676ed844e5a01bfcafd32994309cf0d657f53e2a590018` |
| Native blank structure | Empty D81, independently compared in `D81_NATIVE_COMPARISON_2026-09-22.md` |
| Native blank current raw FAT audit | PASS, one extent, 819200 bytes at device offset 114716672 |
| New canonical image | `build/r0f/d81-workflow/R0FDIAG3/canonical/R0FDIAG3.D81`, 819200 bytes, SHA-256 `30508cb424e526b09f9f923e3ae4e35e449d89a5ec239f769b7da8a8cb2e1d60` |
| Target PRG | SHA-256 `3ce9aeb1029676465d47755145ec31d6b30ab2ca0c8ae95dc88e9703dd99446b` |
| Host gates | Structure and independent content extraction PASS |
| Xemu gate | Two NTSC and two PAL exact-name fresh-copy boots PASS |
| SD fill | PASS; postimage hash matches canonical, same single extent at offset 114716672, safe eject PASS |
| Physical chooser and entry load | PASS for exact `R0FDIAG3.D81`, confirmed by owner; diagnostic screen reached |
| R0-F runtime | FAIL: successor lockout `FAULT 57` (hex), `STATE 0A`, `TICK 0021` |

The first Xemu attempt failed before memory capture because the app sandbox
denied Xemu's config-template write. Its log is retained as
`failed-xemu-environment/xemu.log`. Four new disposable same-name copies then
passed; no failed image was modified, renamed or retested. The canonical D81
remained read-only and unchanged.

## Delivery gate

The owner-terminal command is recorded in `docs/D81_WORKFLOW.md`. The helper
requires the exact source and known blank SHA-256. It rechecks the source,
current blank bytes, exact FAT short name and single-extent chain, backs up the
blank off-card, writes exactly 819200 bytes without truncation, compares the
final hash and unchanged allocation, and safely ejects. An unavailable raw
audit or any mismatch stops. The owner ran this command in Terminal. The saved
pre/post raw audit reports independently show the same exact FAT32 short name,
removable `disk4s1`, one-extent allocation and 819200-byte size. The preimage
was the verified native blank hash; the postimage is the canonical hash. The
helper reported `safe_eject=PASS`. Evidence is retained at
`build/d81-sd-transfer/R0FDIAG3.D81.slot-pre.json`,
`build/d81-sd-transfer/R0FDIAG3.D81.slot-post.json`, and the host-side
`slot-backups/R0FDIAG3.D81.<blank-sha>.D81` backup. The backup is root-owned;
its bytes were checked by the helper, but this app could not independently
read that root-only file afterward.

The SD copy, contiguity and safe-eject gates are passed for this exact
`R0FDIAG3.D81` identity. The owner confirmed that selecting that exact file
on the MEGA65 reached the diagnostic screen in the retained photo. This
establishes physical chooser/entry loadability for this carrier, not a passing
R0-F runtime or wider acceptance. It also validates the MEGA65-native blank
fill route for this instance; the separate host-created direct allocator
remains blocked by its clean-filesystem preflight and has not been proven on
this physical card.

## Owner-supplied physical screen

The photo received after the test is retained as
`docs/evidence/r0f/successor/2026-09-23-r0fdiag3-physical/photo-1.jpg`,
SHA-256 `ed11efdaedecf8bb4bc0dc026bb5d7715ad8ab8fea3ab1d77c162e919147da37`.
It visibly shows `SUCCESSOR LOCKOUT - NO ACCEPTANCE`, `FAULT 57` (hex),
`STATE 0A`, `TICK 0021`, `MASK 00`, `NMI 00`, and equal reserve-before/after
CRCs (`3C7D60D8`). The screen itself does not display the selected SD
filename; the owner explicitly confirmed that it followed selection of
`R0FDIAG3.D81`. The photograph and confirmation bind this physical observation
to the exact carrier whose SD hash and allocation passed the preceding gates.

`0x57` is decimal `87`, the caller's lockout code when `run_ticks(33)` fails
after storage. Tick `0x21` is 33, exactly the pre-storage count; no first
post-storage tick completed. This is a runtime failure, not chooser `FF` or
evidence of a malformed D81. The caller unconditionally writes fault 87 on
the failed return, so a more specific fault raised within
`run_authoritative_tick()` may be obscured. The display does not establish
which inner condition caused the failure. Do not run broader R0-F acceptance
or infer a card-wide fault from this screen.
