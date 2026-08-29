# R0-C D81 Loadability Audit and Recovery Plan

**Status:** current `F65-R0C-MEDIA.D81` is not certified loadable on the physical MEGA65. A chooser-level `ERROR CODE FF` is a hard failure; no BASIC or R0-C result is valid until the carrier passes the load gate.

## Symptom

The physical MEGA65 disk-image chooser reports `ERROR CODE FF` for the current `F65-R0C-MEDIA.D81`. Older R0-C/R0-B images in the same chooser load. The failure occurs before the R0-C BASIC program starts, so it is a disk-image/carrier, transfer, or device-selection failure—not a runtime result from `media_fixture.bas`.

## Repository and artifact identity

The audit was performed on branch `codex/r0-c-development`, with a clean tree and origin `https://github.com/SUON1/f65-megawing.git`.

Relevant history:

- `623256a` (`fix(r0c): isolate media fixture d81`) introduced a separate media carrier by copying a control D81 and then opening it in a second `c1541 -attach` session to append `R0C-MEDIA.C65`.
- `a2306a1` (`fix(r0c): derive media carrier from physical control layout`) retained that split-carrier/second-session construction as the active build path.
- `26ea67a` (`fix(r0c): reissue device-nine media fixture`) changed only the BASIC media fixture and its validator. It did **not** change D81 construction. It cannot explain a chooser failure that occurs before BASIC executes.

Current host artifacts are all 819,200 bytes:

| Artifact | SHA-256 |
| --- | --- |
| `F65-R0C-MEDIA.D81` | `e0d4600994cd7eb69870ea935974db0175868017e115222521965c7fc70d113` |
| `F65-R0C-CONTROL.D81` | `90c539529d3be603fd7af7b526d2fb9988d6f90106133b3ba580db6c29c63103` |
| `R0CMEDIA.D81` | `70232dbdb9cc044611f306a256e046ff6c6fbd5fc98500673276f79c44352aef` |
| `R0CFINAL.D81` | `d28a2d15429939db4f1b9aca2ecbc135f7dc9df45a5eef04dd25f46dba05e4ef` |

The host VICE `c1541` report recognizes the current media image as an 80-track D81 and lists its files. The control and media images first differ at byte 391937 (one-based); that is the expected appended-fixture region, but it also identifies the exact mutation boundary to inspect.

## Exact change to remove first

The first changed mechanism correlated with the bad physical carrier is **not** the selector BASIC. It is the second-session append introduced by `623256a` and retained by `a2306a1`:

```text
copy CONTROL.D81 -> MEDIA.D81
c1541 -attach MEDIA.D81 -write R0C-MEDIA.C65 r0c-media
```

This creates a carrier through two independent filesystem-edit sessions. The recovery build will format a fresh D81 and write every required file in one pinned `c1541` session. The `cp` plus second `-attach` append is removed from the load-critical path. The BASIC fixture remains unchanged until the carrier itself is proven loadable.

This is a defensible regression finding, not an overclaim of the physical root cause. Repository evidence alone cannot distinguish an on-disk DOS/BAM defect from a damaged or mis-copied SD-card file. The procedure below isolates both.

## Deterministic load-safe build procedure

1. Preserve the current images and hashes; never overwrite the owner’s ROM, source media, or an unrelated save disk.
2. Format a **new** D81 with the pinned repository VICE `c1541`.
3. In that same process/session, write only short PETSCII-safe names: `AUTOBOOT.C65`, `R0C-FINAL`, `R0CPROOF`, and `R0C-MEDIA`. Do not use Unicode, punctuation, or long host names as on-disk names.
4. Close the image cleanly, reopen it with `c1541`, list the directory, and extract/read back every file. Compare exact byte counts and SHA-256 values with the source files.
5. Inspect the raw D81 directory/BAM and confirm the directory chain and free-block count are internally consistent. A nominal 819,200-byte file is not proof of filesystem capacity.
6. Mount the new image in Xemu on the same drive number used by the physical procedure (device 9 for the sacrificial media fixture). Xemu must mount it and the chooser-equivalent load path must reach the program banner.
7. Copy the **verified** D81 to the sacrificial SD card without renaming it on the target. Hash the source and destination when the host permits; safely eject the card.
8. On the MEGA65, perform the chooser-only gate first. If it shows `ERROR CODE FF`, stop and return the card/image; do not run the fixture. If it loads, then and only then run the R0-C media fixture and capture the status screen and result block.

## Commands for the recovery build and load gate

Run from the repository root:

```bash
cd /Users/slice/Documents/Codex/f65-megawing
git status --short --branch
git log --oneline --decorate -8
shasum -a 256 build/r0c/artifacts/F65-R0C-MEDIA.D81
stat -f '%z bytes  %N' build/r0c/artifacts/F65-R0C-MEDIA.D81
```

After the one-session rebuild, use the repository’s pinned `c1541` binary to perform a fresh `-format`, all `-write` operations, a clean `-list`, and file extraction/readback. The build log must retain the exact command line, tool identity, directory listing, source/readback sizes, and hashes. Then run the normal Xemu target command from the checked-in R0-C guide using the newly generated image; do not substitute the old `F65-R0C-MEDIA.D81`.

## Acceptance criteria

The replacement D81 is load-safe only when all of these are true:

- `c1541` recognizes it as a valid 80-track D81 and lists all required files.
- Every extracted file matches the source bytes and expected PETSCII-safe name.
- Xemu mounts it and reaches the R0-C banner without a disk error.
- The physical chooser loads it without `ERROR CODE FF`.
- The physical fixture then reports its own PASS/FAIL/DEFERRED results; a chooser load alone does not close R0-C.

Any failed criterion invalidates the image and triggers a fresh-format rebuild. Do not “repair” the failed image in place, because that would make the byte identity and causal diagnosis ambiguous.

## What this audit does and does not conclude

It concludes that the first build-system change to remove is the split-carrier second-session append. It does not conclude that the D81 filesystem is definitely corrupt, nor that the SD card is definitely at fault. The one-session fresh-format build, readback, Xemu mount, and physical chooser gate are the required evidence to separate those possibilities.

Until that gate passes, the current media image remains a failed test artifact and no R0-C media result should be promoted to acceptance evidence.
# Loadability correction checkpoint (2026-08-28)

The failed copy-and-append carrier is retired. A fresh candidate was formatted
and populated in one pinned `c1541` invocation, then passed raw D81 chain,
filesystem listing, extraction, and source-byte comparison checks. The current
candidate is `build/r0c/artifacts/F65-R0C-MEDIA.D81`, exactly 819200 bytes,
SHA-256 `e01eb41cff0158e7b609a365ecc72b78b3ce825ddca06a42a32f8954f4c7e8d0`.
It boots its proof program from device 8; its fixture performs writes only to
the separate sacrificial device 9. Physical chooser verification is still
awaiting the owner.
