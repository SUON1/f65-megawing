# F65R0F4 physical observation — recorded 2026-09-17

Status: **OWNER-SUPPLIED PHYSICAL SCREEN OBSERVATION; NOT R0-F ACCEPTANCE.**
Record date is not an independently verified acquisition timestamp.

## Provenance

Original, unmodified owner photographs retained here:

| File | Original attachment directory / file | SHA-256 |
|---|---|---|
| `sweep-running.jpg` | `D4ADC7C3-A19F-4CE2-97E7-2C6B7115DABD/1-Photo-1.jpg` | `4fdf3aa36be51bc0db3674409c3608035ea79496ba8090a877e697a28d413aa5` |
| `sweep-complete.jpg` | `D4ADC7C3-A19F-4CE2-97E7-2C6B7115DABD/2-Photo-2.jpg` | `eb81ac9f58d0d795ab9c0feaa54609ed973b7ea679a8213ffe0f4f7230d2a7b5` |
| `megainfo.jpg` | `AC698FF5-93E1-4990-B01F-14D1B341CDC3/1-Photo-1.jpg` | `40ad43a378c159b3c3cb803f65fac8d9d7201ec43471c6cc47371998c5c0093a` |
| `freezer.jpg` | `AC698FF5-93E1-4990-B01F-14D1B341CDC3/2-Photo-2.jpg` | `7b97ae86cec8cdb74fe18499f93a751a8ba508658df5acb29d3e0bf895235262` |

Attachment root:
`/tmp/codex-remote-attachments/01a06d60-837c-7c02-a078-2c80f635ef39/`.
Values below are manual visual transcriptions, not a physical memory dump or
independent Java reduction of physical samples.

## Runtime screen

The intermediate image includes the inherited F2 startup-fix banner and
`CIA TIMING SWEEP RUNNING - DO NOT PRESS RESTORE`. The final image identifies
`R0-F CIA COUNT SWEEP - F65R0F4`, inherited functional fixture `PASS`, and
`ACQUISITION: COMPLETE - NOT R0-F ACCEPTANCE`.

All table values are hexadecimal **raw CIA counts**, except the phase mask:

| Case | P50 | P95 | Max | Late | Miss | Mask | Span33 |
|---|---|---|---|---|---|---|---|
| NORMAL | 0035 | 0036 | 0038 | 0000 | 0000 | FFFF | 0004E240 |
| LAG | 003C | 003F | 0040 | 0000 | 0000 | FFFF | 0004E249 |
| SHED | 003A | 0047 | 0049 | 0000 | 0000 | FFFF | 0004E255 |
| FAULT | 0035 | 0036 | 0038 | 0000 | 0000 | FFFF | 0004E241 |
| PRESS | 0035 | 0036 | 0036 | 0000 | 0000 | FFFF | 0004E240 |

- 16-frame counts before/after: `00040B8F`, `00040B8B`.
- Displayed period: **10000 counts**; 16 phases × 33 ticks × 5 cases.
- Fault / READY high-water / video / speed bytes: `00 03 87 60`.
- Raw capture address/length: `$4941`, `$2A80` (10880 bytes).
- Screen explicitly disclaims calibrated Hz/µs, CPU cycles, input/audio latency;
  IRQ is masked, DMA not run, reset required after test.

The complete banner and masks report completion of the requested 80 cohorts
(2640 ticks). No physical raw sample bytes or result-block checksum were
collected here; completion is observed on screen, not independently reconstructed.
Zero displayed late/miss values concern the nominal count schedule only.
`FFFF` is not exhaustive coverage of every legal display/audio/DMA alignment.

## Platform screens

MEGAINFO displays MEGA65 R6, ARTIX `B5C770C6` dated `2025-09-14`, ROM
`M65 V920413`, HYPPO/HDOS `1.2 / 1.3`, screen mode `NTSC`, HYPPO status
`NORMAL`. FREEZER.M65 and MEGAINFO.M65 display
`250422.09-R0.4.0-6725505`.

Freezer displays version `V0.4.0`, CPU mode `4502`, frequency `40MHZ`, video
`NTSC60`, CRT emulation `ON`, cartridge enable `YES`, joystick swap `NO`.
Internal unit 8 displays `MEGA65.D81`; external unit 9 displays no disk.

These later identity screens are useful platform observations, not full binary
hashes, an exact core-source pin, a measurement of the timer frequency, proof
of the effective clock during the sweep, or identification of the F4 carrier.
Keyboard version `FFFFFFFF` / date `2064-10-05` and RTC `INTERNAL CHECKING`
are retained literally in the photograph; no fault diagnosis is inferred.

## Artifact attribution and missing delivery evidence

The intended host/Xemu artifact is `build/r0f/cia-timing-safe/F65R0F4.D81`,
819200 bytes, SHA-256
`a30880f83be9c9ff414065d9331d5bba737e393e1a6441f07741e87f000ff39d`.
Its F4 banner matches the final screen. The supplied photographs do not prove
byte identity with that artifact. No F4 SD-transfer hash/extent/eject report
was supplied or found under `build/d81-sd-transfer/` during this review.
Chooser-stage evidence is likewise not supplied for F4.

Do not inherit F1/F2 delivery results, infer failure from missing records, or
retroactively promote the F4 release manifest beyond `XEMU_BOOT_VERIFIED`.
F2's reported Finder/eject incident is separate; it does not prove an F4 failure.
No new transfer or hardware rerun is requested by this record.

## Disposition

This is successful physical execution evidence for the displayed bounded
functional/CIA-count diagnostic, with the attribution limitations above.
Full R0-F, physical raw-data validation, calibrated time, combined-service
measurements, supported-platform coverage, and measured-limit acceptance remain
open. See `docs/reports/R0-F_CLOSEOUT_REVIEW.md` for the scope decision.
