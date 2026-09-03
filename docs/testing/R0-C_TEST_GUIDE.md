# R0-C Physical Test Guide

Status: **ARCHIVED — R0-C candidate complete by owner waiver; no further physical fault testing requested.**
`DEC-012` authorizes a sacrificial writable D81 only for this fixture. It does
not choose a production medium, campaign disk split, or recovery UX.

## Corrected fixture revision (2026-08-26)

The current carrier is a fresh one-session rebuild. SHA-256:
`e01eb41cff0158e7b609a365ecc72b78b3ce825ddca06a42a32f8954f4c7e8d0`.

This supersedes `8826fc89706bcca0d9587f9bae80b5d12a8a1d35e3e0a92868c118e9ef204059`; retire that carrier for further physical media testing. This revision accepts a blank sacrificial device-9 medium: initialization does not issue a scratch-file probe or DOS-status probe before creating `R0CG0`, `R0CG1`, and `R0CSEL`. Selector I/O is split into distinct BASIC statements. On missing/corrupt media it reports a controlled fixture failure/recovery result or returns to the menu; it must not reproduce the prior `?UNDEFINED STATEMENT ERROR IN 5110`. The carrier at device 8 is never modified.

## Exact artifact and device roles

- Copy only `build/r0c/artifacts/F65-R0C-MEDIA.D81` with SHA-256
`e01eb41cff0158e7b609a365ecc72b78b3ce825ddca06a42a32f8954f4c7e8d0`.
  Its outer SD-card filename must remain exactly `F65-R0C-MEDIA.D81`. Its
  directory shows `AUTOBOOT`, `R0C-FINAL`, `R0CPROOF`, and `R0C-MEDIA`, all
  written during one fresh-format c1541 session. Any future direct-card copy
  must use `tools/diagnostics/d81_sd_transfer.sh` and record both its matching
  hash and exactly one FAT32 physical extent before chooser testing.
- `F65-R0CFINAL.D81` (SHA-256 `ba72aa82387f7e65551e893a3274f1c7f26a813416652c4aeab73c6a8b7e7e38`)
  is the known mountable three-file control. Do not overwrite or modify it.
- The prior `R0CMEDIA.D81` and `ROCFINAL.D81` deliveries were physically
  rejected by the Freezer with `ERROR CODE FF`; both are retired and must not
  be used for this procedure.
- The corrected physical carrier is a fresh, hash-verified `F65-R0C-MEDIA.D81`
  mounted on unit 8. Device 8 is the read-only proof carrier for this test.
- Device 9: one separate fresh, writable, recoverable sacrificial D81. This is
  the sole fixture medium and is the only medium modified by the BASIC test.
- The second managed drive in the MEGA65 Freezer can be assigned either unit 9
  or unit 11. It **must display `UNIT #9`** before this fixture is loaded. If
  it displays `UNIT #11`, press `9` once at the main Freezer screen to toggle
  it to unit 9, then press `1` to select the D81 for that second managed drive.
  A D81 mounted while this display says `UNIT #11` correctly produces `DEVICE
  NOT PRESENT` for `LOAD ...,9,1`; that is a mount configuration error, not a
  program result.
- The proof carrier is explicitly device 8: `LOAD "R0C-FINAL",8,1`. The media
  harness is explicitly loaded from device 8 with `LOAD "R0C-MEDIA",8,1`,
  then all fixture I/O is explicitly device 9. No automatic device detection
  exists.
- The media program is loaded from the proof carrier at device 8:

```basic
LOAD "R0C-MEDIA",8,1
RUN
```

Record the MEGA65 revision, FPGA core/hash, ROM SHA-256, system-files identity,
video mode, storage configuration, D81 hash, and a full-screen photo for every
case. Use a new hash-verified device-9 copy when a case consumes or corrupts
media.

## Safety convention

The fixture has no tactical or post-ROM-reclaim activity. Its only disk calls
are BASIC/DOS calls addressed to device 9. A menu prompt is idle, but a write,
verify, selector, or fill action is active until the program returns to the
menu or displays its explicit removal message. Each candidate generation has
512 payload records and an end marker, so verification checks the complete
candidate before the selector write.

| Screen state | Is removing device 9 safe? |
|---|---|
| Menu showing `I=INITIALIZE ... Q=QUIT`, before entering an action | Yes; no media I/O is active. |
| `PRESS Y`, `PRESS F`, or a corruption target prompt | Yes; no media I/O is active. |
| `WRITE`, `VERIFY`, `SELECTOR`, or `FILL` action in progress | No. Do not remove it. |
| `SAFE TO REMOVE DEVICE 9 NOW: NO MEDIA I/O IS ACTIVE.` | Yes; this is the controlled selector-interruption point. |
| `MEDIA OPERATION FAILED ...` or a returned menu | Yes; no operation is in flight. |

Before each action below, verify the screen is in the named safe state. Never
remove media to create a fault unless the step explicitly says it is safe. For
a power-interruption case, power cycling is the injected fault; it is not
represented as safe media removal.

## Mandatory device-9 mount precheck

This precheck is non-destructive and must pass before any save or fault action.

1. Hold `RESTORE` for one second and release it to open the main Freezer menu.
   **Do not remove any media.** No removal is needed for this step.
2. Read the lower-right second-managed-drive line. If it says `UNIT #11`, press
   `9` exactly once. Expected: the line changes to `UNIT #9`. If it does not,
   stop and photograph that screen; do not run a fixture command.
3. Press `1`, select the hash-verified `F65-R0C-MEDIA.D81` carrier for unit 8,
   and press `RETURN`. **Do not remove media while the image browser is open
   or while it mounts.** The retired `R0CMEDIA.D81` is excluded after its
   observed `FF` mount rejection.
4. Mount a separate fresh sacrificial D81 as unit 9. Press `F3` to resume
   BASIC, then run the explicit device-8 command shown above. Once the fixture
   menu is visible and idle, removal of device 9 is safe only for a deliberately
   instructed fault case.

## Baseline and normal two-generation transaction

1. At the menu, mount the hash-verified sacrificial copy as device 9.
   Removal safe: **yes**, until an action is entered.
2. With both devices mounted, load and run `R0C-MEDIA` from device 8. Choose `I`, then press `Y` at the
   confirmation line. Removal safe: **no** after `Y` until the program returns.
   Expected:
   `INITIALIZE PASS: G0=1 AND G1=2 VERIFIED; SELECTOR=G1`.
3. At the returned menu, choose `W` twice, waiting for the menu after each
   write. Removal safe: **no** for each write. Expected on each: candidate
   write, `VERIFY PASS`, `SELECTOR PASS`, and `WRITE PASS`.
4. At the menu, choose `R`. Removal safe: **no** while it reads; safe once it
   returns. Expected: `RECOVERY PASS: SELECTOR CHOSE G0` or `G1` with the
   selected generation. Photograph this result.

## Physical media-fault matrix

Run every case from an initialized fresh device-9 copy unless the case says to
retain its immediately preceding state.

1. **Absent — R0C-MEDIA-001.** At the menu, remove device 9. Removal safe:
   **yes**. With it absent, choose `W`. Expected: `MEDIA OPERATION FAILED ON
   DEVICE 9 - NO PASS CLAIM.` Reinsert the same sacrificial medium before the
   next action; then choose `R` and photograph the retained prior generation.

2. **Write-protected — R0C-MEDIA-001.** At the menu, enable write protection
   only on the sacrificial device-9 copy. Removal safe: **yes** while changing
   this state, because no I/O is active. Choose `W`; removal safe: **no** while
   it runs. Expected: a device-9 failure and no successful selector claim.
   Disable protection only after it returns, then choose `R` and photograph the
   retained generation.

3. **Full — R0C-MEDIA-001.** Initialize a fresh device-9 copy, then choose
   `F` and press `F` at the confirmation line. Removal safe: **no** after the
   second `F`; allow the fixture to
   stop on the drive-full failure. Once it returns, choose `W`. Expected: a
   device-9 failure and no successful selector claim. Photograph the failure;
   discard this consumed copy and use a new one for the next case.

4. **Corrupt selector — R0C-MEDIA-001.** Initialize, choose `C`, then `S`.
   Removal safe: **no** during the corruption write; safe after it returns.
   Choose `R`. Expected: `RECOVERY PASS: SELECTOR INVALID; HIGHEST VERIFIED`
   generation. Photograph both the corruption completion and recovery screen.

5. **Corrupt selected generation — R0C-MEDIA-001.** Initialize (the selector
   starts on G1), choose `C`, then `1`. Removal safe: **no** during the
   corruption write; safe after it returns. Choose `R`. Expected: selector is
   rejected against the corrupt generation and recovery selects verified G0.
   Photograph the recovery screen.

6. **Removed between verify and selector — R0C-MEDIA-001.** Initialize, then
   choose `X`. Do not remove media during its candidate write/verify. When it
   shows `SAFE TO REMOVE DEVICE 9 NOW: NO MEDIA I/O IS ACTIVE.`, removal safe:
   **yes**. Remove device 9, press `C`, and record the expected failure.
   Reinsert the same medium, then choose `R`. Expected: the previously selected
   generation remains selected; the verified but unselected candidate is not a
   successful commit.

7. **Power interruption during candidate write — R0C-MEDIA-001.** Initialize
   a fresh copy and choose `W`. Removal safe: **no** once `W` begins. Inject the
   planned power interruption only during this write attempt; do not remove the
   media. Restore power, remount the same device-9 copy, reload `R0C-MEDIA`, and
   choose `R`. Expected: no new successful selector claim; record whether the
   fixture reaches the retained generation or reports a device-9 read failure.
   The latter is evidence of an unresolved recovery defect, not a pass.

8. **Power interruption after verified candidate / before selector —
   R0C-MEDIA-001.** Use the `X` action and stop power only at its explicit safe
   removal message, before pressing `C`. Removal safe: **yes** at that
   message; power interruption is still the injected fault. Restore power,
   remount device 9, reload the fixture, and choose `R`. Expected: the prior
   selector/generation is retained.

For every case, retain the original D81 hash, the post-case D81 hash if it can
be safely copied, photographs, exact action sequence, and observed text. A
failure is valuable evidence but does not turn into a PASS without the specified
recovery result. Do not attempt ROM reclaim, storage restoration, device-8
access, or gameplay testing.
