# R0-D Handoff

Status: **XEMU TESTING COMPLETE — READY FOR HARDWARE AUTHORIZATION.**

R0-D adds a proof-only calibration harness around the historical
530,000-clock protected non-render fixture. The fixture preserves the 100 Hz,
21-stage contract and stage-16 next-tick boundary; it does not implement a
renderer, flight model, sensor/weapon system, production AI, R0-E harness, or
measured-limit selection.

The generated target record is 128 bytes at `$1860-$18DF`. It exposes fixture,
stage, world/snapshot, non-render graphics/audio, IO, AI-owner, and reserve
counters. It does not read/write the protected staging/audio/DMA/reserve
ranges. The build map is parsed into a retained accounting report so code,
rodata, data, BSS, linked stack address, and zero reserve use are evidence,
not guessed constants.

Stage-1 validation is host/static/build only. R0-D produces no D81 in this
stage; therefore no D81, Xemu, or physical pass is claimed.

Observed target artifact: `build/r0d/artifacts/F65-R0D-CALIBRATION.prg`,
SHA-256 `ad4827da70d6f4a571817df2268bb3ca4e88d11a0f8aacfc11441abca2fd1677`.
The linked map reports 696 code bytes, 618 rodata bytes, zero data bytes, one
BSS byte, stack symbol `$D000`, and zero reserve bytes. These are evidence
observations, not measured-limit selections.

Local implementation commit: `2bcb54e046e9cdcd8f03b7daaa12141a474c6af0`.
The required publication action, when separately authorized, is VS Code Source
Control push/sync of `codex/r0-d-development` to `origin`, followed by remote
verification of the final commit. Do not start Xemu after publication without
an explicit Xemu authorization.

Xemu result: PASS from two clean PRG boots using the pinned Xemu build and ROM
SHA-256 `af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0`.
Both boots produced result-block SHA-256
`24f8e8dac28e79d9615bbae9fb58b716e92cf55b515e66483769721cf14587f7` and the
same display identity. No D81 exists for R0-D, so physical chooser verification
is not applicable. Physical timing remains unverified and requires separate
authorization.
