# R0-D Handoff

Status: **R0-D CLOSED — OWNER ACCEPTED 2026-08-31.**

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

The former D81 construction tool emitted an OpenCBM error despite exit status
zero. That violates the fail-closed D81 gate, so all old host results are
diagnostic only. The corrected builder disables VICE real-device/OpenCBM
support and rejects any stderr or warning/error/failure diagnostic in
construction, listing, or extraction.

Observed target artifact: `build/r0d/artifacts/F65-R0D-CALIBRATION.prg`,
SHA-256 `ad4827da70d6f4a571817df2268bb3ca4e88d11a0f8aacfc11441abca2fd1677`.
The linked map reports 696 code bytes, 618 rodata bytes, zero data bytes, one
BSS byte, stack symbol `$D000`, and zero reserve bytes. These are evidence
observations, not measured-limit selections.

The corrected carrier is `F65R0D3.D81`, SHA-256
`107c6a356b932e9ade875c24539d75b1b0a0078122a6a3910f524570aafec5ef`, 819,200
bytes, disk `F65 R0-D3`/ID `65`. It is a fresh format with both payloads written
in one session and has passed host structural plus content extraction/hash
validation. Its complete release state is recorded in
`docs/evidence/r0d/R0D-D81-D3-PHYSICAL-RELEASE.md`.

After publication at `48b3647`, D3 completed two independent clean Xemu drive-8
AUTOBOOT runs. Both mounted the unchanged D81, reached the stable calibration
identity, and produced the same screen SHA-256
`cd424a2b51109d891a3c3388f0da114042462ddab43f543d912bcdff41e8bcf2` plus
result-block SHA-256 `24f8e8dac28e79d9615bbae9fb58b716e92cf55b515e66483769721cf14587f7`.
The post-Xemu host D81 gate passed again. The exact Xemu evidence remains in
`docs/evidence/r0d/R0D-D81-D3-XEMU-RELEASE.md`.

The owner supplied physical MEGA65 photos showing the `F65 R0-D3` directory
with `AUTOBOOT.C65` and `R0D-CALIB`, followed by the calibration result screen.
The returned SD-copy SHA-256 exactly matches D3. The artifact is therefore
`TEST_ELIGIBLE`, and the owner accepted the admitted R0-D proof. This does not
close a later R0-E/R0-F or measured-limits gate.

`F65R0D.D81` (SHA-256
`a1d11bfb2b18a92618d55b5f3051a44d019adbdf2ba70b7c6715049567638d48`) and
`F65R0D2.D81` (SHA-256
`51dd4ad5a0fe402eccbac81b1ec0e44d12f5ab2294a9f01b1e7452711fa52643`) are
**INVALID — DO NOT USE** after physical chooser `ERROR CODE FF`. D2's SD-card
copy was independently re-hashed and matched exactly, so the transfer did not
cause its failure. No physical R0-D program execution is claimed for either
failed carrier.

Historical direct-PRG Xemu result: PASS from two clean boots using the pinned Xemu build and ROM
SHA-256 `af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0`.
Both boots produced result-block SHA-256
`24f8e8dac28e79d9615bbae9fb58b716e92cf55b515e66483769721cf14587f7` and the
same display identity. The first D81 then passed two clean boots at the
published `d5acdce` branch head: it mounted at drive 8, auto-booted, showed the
stable R0-D identity, and reproduced screen SHA-256
`cd424a2b51109d891a3c3388f0da114042462ddab43f543d912bcdff41e8bcf2` and
result-block SHA-256
`24f8e8dac28e79d9615bbae9fb58b716e92cf55b515e66483769721cf14587f7`.
That Xemu evidence is preserved but superseded for carrier eligibility by the
two physical chooser failures. Physical timing and all physical R0-D program
behavior remain unverified.
