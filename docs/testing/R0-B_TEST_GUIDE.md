# R0-B Owner Test Guide — Current Partial Harness

Status: targeted register/input-fixture/SID-configuration check. This is not
the eventual R0-B full graphics, swap, cockpit, input-latency, or audio
acceptance run.

## Exact artifact identity

- Target-source commit: `b76eccd68ec2dcdb9debae25c2aec2c84b55a48e`.
- D81: `build/r0b/artifacts/F65-R0B-PROOF.d81`.
- D81 SHA-256: `5cd3c43e8c6c5618416871984c88540294c931aca84178c8136e97979d4a49d9`.
- PRG SHA-256: `170c21627d055f625c25ac5191129c501e80045f0c7b6d5a3a450551f4628c81`.
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

All of the following must be visible and marked `PASS`:

- `R0B-FCM-REG-001 PASS`
- `R0B-IN-001 FIXTURE PASS`
- `R0B-AUD-003 MODEL PASS`
- `R0-B TEST RUN COMPLETE`
- `R0B-BLD-001 PASS`

The screen must also state `FCM FRAME: DEFERRED`,
`REASON: DMA/POINTER PROBE`, and `HARDWARE: NOT RUN`. Those lines are expected
because this iteration does not claim a visible FCM frame, DMA, raster swap,
hardware input path, or audio timing result.

## Evidence to return

- A photo or video showing the complete result screen.
- MEGA65 model/revision, core version, ROM/system-file identity where available,
  PAL/NTSC mode, display connection, and whether the SID proxy was audible.
- The SHA-256 of the D81 actually tested.
- Any observed failure text, reset, graphics corruption, or unexpected sound.

## Failure interpretation

- `R0B-FCM-REG-001 FAIL`: VIC-IV unlock/latch/restore probe failed; do not infer
  FCM support or alter display configuration.
- `R0B-IN-001 FIXTURE FAIL`: target deterministic accumulator disagreed with its
  generated host expectation; this is not a keyboard/joystick test.
- `R0B-AUD-003 MODEL FAIL`: target priority model failed; it does not diagnose
  audio hardware timing.
- `R0B-BLD-001 FAIL`: a prerequisite proof failed; retain the screen and stop.

No result in this guide can be recorded as `R0-B EVIDENCE PASSED`. Physical
evidence from this build is targeted hardware evidence only and will be
compared with the retained Xemu result block and reports.
