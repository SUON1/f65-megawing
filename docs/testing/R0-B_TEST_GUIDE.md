# R0-B Owner Test Guide — Current Partial Harness

Status: targeted input-fixture/SID-configuration baseline check. This is not
the eventual R0-B full graphics, swap, cockpit, input-latency, or audio
acceptance run.

## Exact artifact identity

- Target-source commit: `73c2dbee55afe2b754358021505c6520737e2105`.
- D81: `build/r0b/artifacts/F65-R0B-PROOF.d81`.
- D81 SHA-256: `e902fad80eb6e34945a799dda2444e8a3a7cab3984bb372d8fef22e1de60323b`.
- PRG SHA-256: `31ee32fe7f5c03e1372ce8535cdb3590e4ac7d466b969f83a57b89ab5a8761d7`.
- Evidence ID: `F65-R0B-EVIDENCE-SET` (partial fixture iteration).

The disk uses PETSCII-compatible directory names: `AUTOBOOT.C65` and
`F65-R0B-PROOF`. Do not rename the files through a host filesystem after the
D81 is built.

## Setup and boot

1. Copy the exact D81 to the MEGA65 SD card without unpacking it.
2. On the MEGA65, mount the D81 as drive 8 and type `BOOT` at the BASIC prompt.
3. Wait for the static R0-B result screen. The SID proxy may be audible; volume
or speakers should be connected if you choose to record that observation.
4. Photograph the complete result screen and retain the D81 used.

## Expected result screen

All of the following must be visible:

- `R0B-FCM-REG-001 DEFERRED`
- `R0B-IN-001 FIXTURE PASS`
- `R0B-AUD-003 MODEL PASS`
- `R0-B TEST RUN COMPLETE`
- `R0B-BLD-001 PASS`

The screen must also state `FCM FRAME: DEFERRED`,
`REASON: D054 PROBE NOT SAFE`, and `HARDWARE: BASELINE ONLY`. Those lines are
expected because this iteration does not access `$D054` and does not claim a
visible FCM frame, DMA, raster swap, hardware input path, or audio timing
result.

## Evidence to return

- A photo or video showing the complete result screen.
- MEGA65 model/revision, core version, ROM/system-file identity where available,
  PAL/NTSC mode, display connection, and whether the SID proxy was audible.
- The SHA-256 of the D81 actually tested.
- Any observed failure text, reset, graphics corruption, or unexpected sound.

## Failure interpretation

- `R0B-FCM-REG-001 DEFERRED`: expected. The original `$D054` probe caused an
  unreadable physical text display and is excluded pending an isolated restore
  proof; do not infer FCM support.
- `R0B-IN-001 FIXTURE FAIL`: target deterministic accumulator disagreed with its
  generated host expectation; this is not a keyboard/joystick test.
- `R0B-AUD-003 MODEL FAIL`: target priority model failed; it does not diagnose
  audio hardware timing.
- `R0B-BLD-001 FAIL`: a prerequisite proof failed; retain the screen and stop.

No result in this guide can be recorded as `R0-B EVIDENCE PASSED`. Physical
evidence from this build is targeted hardware evidence only and will be
compared with the retained Xemu result block and reports.
