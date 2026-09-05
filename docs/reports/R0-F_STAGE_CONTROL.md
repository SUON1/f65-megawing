# R0-F Stage Control

## Current stage

`BOUNDED FUNCTIONAL/RASTER SLICE: HOST_CONTENT_VERIFIED; XEMU BLOCKED`

R0-F development is authorized by AD-001, but R0-F acceptance is not. On
2026-09-05 the owner-directed first test slice compiled, passed native functional
and timeout tests, and produced host-verified F65R0F1.D81. Xemu preflight reports
the pinned emulator and owner ROM missing. No SD, chooser, physical-runtime,
DMA, IRQ, latency or platform-identity result is complete. The full F1
measurement contract (real scheduling, calibration, latency and high-water)
remains incomplete; this narrower proxy does not pass that stage wholesale.

## Stage transitions

| Transition | Required condition | Authority |
|---|---|---|
| F0 → F1 | R0-F control records reviewed; exact R0-E configuration and non-claims retained | Repository task owner |
| F1 → F2 | Measurement contract has units, calibration, wrap handling, sample/phase/window rules, result encoding, and failure behavior | Architecture/platform review for any wrapper |
| F2 → F3 | Every target impact and validator is explicit; no public ABI/memory/reserve violation | Build/static validation |
| F3 → F4 | Host proof passes; fresh D81 identity/payload manifest is assigned | D81 loadability gate |
| F4 → F5 | Exact candidate is host structural/content verified | D81 loadability gate |
| F5 → F6 | Two clean Xemu boots of the exact filename/hash pass | Pinned Xemu/ROM evidence |
| F6 → F7 | Exact SD hash, one extent before/after in-place fill, identical allocation, and safe eject pass | Owner/admin/card action |
| F7 → F8 | Physical chooser, runtime capture, and complete attributed measurement matrix are retained | Owner physical capture |
| F8 → closed | Owner explicitly reviews and accepts complete R0-F evidence | Owner only |

## Stop conditions

Stop at `NOT VERIFIED` for missing tools, owner ROM, Xemu configuration, admin
authentication, SD-card movement, MEGA65 operation, platform identity, or
physical capture. A chooser `ERROR CODE FF` retires the tested identity and
requires diagnosis of construction, copied bytes, FAT32 allocation, safe eject,
and platform identity before any replacement. No stage permits measured-limit
selection, Phase 1, or gameplay implementation.
