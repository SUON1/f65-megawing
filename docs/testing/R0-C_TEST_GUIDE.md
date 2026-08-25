# R0-C Physical Test Guide

Status: **physical media/save evidence requested; not an R0-C closure guide.**
`DEC-012` authorizes a sacrificial writable D81 only for this fixture. It does
not choose a production medium, campaign disk split, or recovery UX.

## Exact artifact and device roles

- Copy only `build/r0c/artifacts/R0CMEDIA.D81` with SHA-256
  `fa2ebf7c96014f583efc3b4b3ef2d3946bb34b304f12188a0871a913102fff52`.
  Its outer SD-card filename is uppercase 8.3 and must remain exactly
  `R0CMEDIA.D81`. Do not select the superseded `R0CFINAL.D81` copy.
- Device 8: owner's F0C-final SD. **Do not mount, read, write, swap, or fault
  test it.**
- Device 9: one fresh, writable, recoverable copy of the D81 above. This is the
  sole fixture medium.
- The boot file is explicitly device 9: `LOAD "R0C-FINAL",9,1`. No automatic
  device detection exists.
- The media program is explicitly device 9:

```basic
LOAD "R0C-MEDIA",9,1
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

Before each action below, verify the screen is in the named safe state and that
device 8 has not been selected. Never remove media to create a fault unless the
step explicitly says it is safe. For a power-interruption case, power cycling
is the injected fault; it is not represented as safe media removal.

## Baseline and normal two-generation transaction

1. At the menu, mount the hash-verified sacrificial copy as device 9.
   Removal safe: **yes**, until an action is entered.
2. Load and run `R0C-MEDIA` from device 9. Choose `I`, then press `Y` at the
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
