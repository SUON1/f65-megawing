# R0-F T08 post-storage clock ordering — 2026-09-25

## Build Intent and boundary

After the owner-confirmed exact `R0FDBG07.D81` physically loaded but locked
out at `FAULT 03`, the owner said "Continue" to the next narrow checkpoint.
This change addresses only the first post-storage clock fault hypothesis. It
does not authorize a replacement physical D81, SD operation, hardware run,
full R0-F acceptance, or a measured-limit decision. The tested `R0FDBG07.D81`
and all earlier carriers remain unchanged.

## Evidence-backed hypothesis and change

`cfnow()` sets fault `03` after 32 unsuccessful attempts to read a coherent
CIA Timer A/B snapshot. On the post-storage path, the KERNAL storage wrapper
performs initialization and file I/O, then returns to the application.
`storage_transition()` previously called `cfaudio_begin()` before
`cfclock_begin()`, while `cfaudio_begin()` calls `cfnow()` to set its service
timestamp. The initial pre-storage path starts the clock before audio.

T08 moves only the post-storage `cfclock_begin()` call before
`cfaudio_begin()`, matching the initial order. The builder's source-order gate
now requires `display_resume()` -> `cfclock_begin()` -> `cfaudio_begin()` ->
`next_deadline = cfnow()`. This prevents that known early audio timestamp read
before the application clock restart. It does **not** prove that this was the
physical `FAULT 03` site; later clock reads can still fail. The first-fault
diagnostic remains intact and a future physical retest is required.

## Contract and hardware impact

- Registers/clobbers: no new register or clobber. Existing CIA Timer A/B
  setup (`$DC04-$DC07`, `$DC0E-$DC0F`) and raster IRQ restart now precede
  existing SID/PCM setup on the post-storage path. Initial startup already
  used this order. The IRQ handler does not call C, DMA or audio services.
- CPU-visible/physical memory: no range, ownership or allocation change.
  Generated successor and memory ledgers remain unchanged. Linked resident
  use remains 24,098/40,959 bytes; protected end `0x2B07`; measured-reserve
  consumption zero.
- MAP/base-page and KERNAL return: unchanged; `r0f_pf_enter()` still restores
  canonical platform state before display/clock/audio resume.
- DMA: no new submission or ownership change; the existing synchronous audio
  sample copy occurs after IRQ restart, as on initial startup.
- Timing/deadline: the calibrated period, 100 Hz release, 21-stage order and
  33/33 storage boundary are unchanged. The next deadline is still established
  after both clock and audio initialization.
- IRQ/NMI: existing raster IRQ begins earlier relative to audio setup after
  storage; sticky NMI observation and lockout rules are unchanged.
- Public ABI/private result layout: unchanged. No generated file was edited.

## Validation and evidence identity

- `python3 -B tools/diagnostics/r0f_successor_integration.py build`: PASS.
  1,527,538 successor lifecycle/continuation/fault checks, CF001 and RH001
  regressions, target compile/link and static accounting passed, including the
  new source-order gate.
- Target PRG: 21,922 bytes, SHA-256
  `fd8b61263ba5f33ba3a4084ff33051e6dadf29cbc8dda51d0c97a58fa1f4089a`.
  The accounting identifies HEAD `69e4e161c86d8c3eed93e1a976c6b5072945f896`
  plus dirty-tree input hashes; this is **not** a pushed source freeze.
- First disposable direct-PRG Xemu attempt: **NO RUNTIME RESULT**. macOS
  denied Xemu's config-template write; log retained under
  `../evidence/r0f/successor/2026-09-25-t08-clock-order-development/failed-environment/`.
- Fresh second direct-PRG Xemu attempt: NTSC and PAL **PASS** with independent
  result reduction and Java oracle. Each showed `FAULT 00`, `STATE 09`,
  `TICK 0042`, `MASK 1F`, `NMI 00`, and matching reserve CRCs. The NTSC
  screenshot was visually inspected. Summary SHA-256:
  `955753d6f86ff367e507b86ef269aa9430300501eb3c8ff13c0bfe397f93dc08`.
  Retained [development evidence](../evidence/r0f/successor/2026-09-25-t08-clock-order-development/summary.json)
  includes per-mode result bytes, screenshots, oracle output and logs. Its
  token-only D81s were disposable emulator fixtures, **not** successor
  carriers or SD candidates.
- New exact-name full-payload D81, SD copy/extent/eject, physical MEGA65 and
  full R0-F acceptance: **NOT RUN**.

## Next decision

Review this narrow source diff and its dirty-tree provenance. If accepted,
freeze the source separately before a new exact-name D81 build and full host/
Xemu gates. Obtain a separate delivery decision, raw SD hash/one-extent audit
and safe eject before physical testing. The next hardware observation must
determine whether `FAULT 03` is actually resolved; no current result claims
that it is. Broader R0-F testing remains stopped.
