# R0-B Final Composite — Single Physical Test Guide

This is the only remaining hardware run for the R0-B composite candidate.
It does not authorize production engine, gameplay, renderer, input, or audio
work.

## Artifact

Copy this exact disk image to the SD-card workflow used for the MEGA65:

`build/r0b/artifacts/R0BFINAL.D81`

SHA-256:

`43fe855abac93b355b36fa509d83cd302920e87fe0a49e64287285f0a8e980f1`

The D81 contains PETSCII-encoded `AUTOBOOT.C65`, which loads
`F65-R0B-FINAL`. Do not rename files inside the disk image.

Keep the *outer SD-card filename* exactly `R0BFINAL.D81`: it is uppercase 8.3
so it is safe for the MEGA65 virtual-disk loader.

## Run

1. Mount/open the D81 using the same MEGA65 SD-card disk-image workflow used
   for the prior R0-B runs.
2. If it does not autoboot, at the BASIC prompt type:

   ```basic
   LOAD"AUTOBOOT",8,1
   RUN
   ```

3. During the short FCM card display, confirm that a complete patterned card
   appears and that normal text returns.
4. At `PRESS ANY KEY DURING THE INPUT WINDOW`, press one ordinary keyboard
   key once.
5. Leave the resulting status page on screen and take one readable photograph
   that includes the environment line, every PASS/DEFERRED/FAIL line, and the
   `$1800` dump.

## Required pass conditions

- `ENV: PHYSICAL MEGA65 DETECTED`
- FCM safe readback, complete matrix, pointer flip/restore, palette,
  rollback, HUD/MFD, renderer, and SID service each display `PASS`.
- Input displays `INPUT ASCII EDGE+ACK / RASTER DELTA: PASS` after the key.
- In the `$1800` dump:
  - bytes `$1800-$1803` are `52 30 42 32` (`R0B2`);
  - `$1805` is `02` (physical environment);
  - `$1830-$183A` are `01` (the eleven defined status bytes); and
  - the input and audio timing fields are nonzero.

`PCM/DMA: DEFERRED` is expected and does not invalidate this R0-B candidate:
the required representative audio proof is the timed SID service. A DMA/PCM
start/stop wrapper is deliberately not introduced by this bounded proof.

## Stop conditions

Do not call the gate closed and do not apply a waiver if any test line is
`FAIL`, if input remains deferred after a key press, if the environment is not
physical, or if the `$1800` record does not match the stated identity. Return
the photograph and the observed line/dump instead; that evidence determines
the next corrective action.
