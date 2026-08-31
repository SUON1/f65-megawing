# R0-D Handoff

Status: **CODING — D81 HOST VERIFICATION COMPLETE; READY FOR LOCAL COMMIT.**

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

Stage-1 validation now includes a fresh D81 carrier: `F65R0D.D81`, containing
PETSCII-safe `AUTOBOOT.C65` and `R0D-CALIB`, constructed in one pinned
`c1541` format/write session. It has passed independent raw structural and
extraction/hash host checks, so its state is `HOST_CONTENT_VERIFIED` only.

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

The D81 candidate is `build/r0d/artifacts/F65R0D.D81`, 819,200 bytes, SHA-256
`a1d11bfb2b18a92618d55b5f3051a44d019adbdf2ba70b7c6715049567638d48`; disk
label `F65 R0-D 530K`, ID `D1`, entry `AUTOBOOT.C65 -> R0D-CALIB`. The D0
identity SHA-256 `9bac7a0bc28b14618524be487fcd1aeee55dd6f78cb0312d0879401c20a6457f`
failed a host gate and is invalid — do not use.

Historical direct-PRG Xemu result: PASS from two clean boots using the pinned Xemu build and ROM
SHA-256 `af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0`.
Both boots produced result-block SHA-256
`24f8e8dac28e79d9615bbae9fb58b716e92cf55b515e66483769721cf14587f7` and the
same display identity. That evidence does not verify the new D81. The D81 must
be committed, published via VS Code, and Xemu-booted twice from clean starts
before physical chooser testing. Physical timing remains unverified.
