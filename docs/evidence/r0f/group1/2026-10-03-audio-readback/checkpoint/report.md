# Group 1 terminal audio readback correction — 2026-10-03

## Intent and authority

Owner's “Continue” authorizes a narrow copied-source correction of P08's
terminal audio readiness failure. The Group 1 Build Intent, export amendment,
generated export contract, memory ledger, programming principles/C standard,
development workflow and D81 gate/workflow were inspected. Remote main remains
`c27d89787d1d5c4472e24262e0181c47943d46be`; the existing focused branch is
`codex/r0f-group1-resume-clock`. Local qualification is separate from SD delivery,
physical execution, publication and Group 1/full R0-F acceptance.

## Problem and correction

P08 physically reaches tick 3200 with resumed-service mask 1F, then rejects
terminal export with fault 75: the audio-stopped predicate. Actual returned
program/original payloads and tick-1600 SAVE pass; no physical trace exists.
No raw channel values or fresh installed core identity were captured.

The old predicate requires the entire byte at each channel control register
($D720/$D730/$D740/$D750) to be zero. Official core source at commit
[bc7a3ece8aaee3d4d9f5df09cd71c70b1225a827](https://github.com/MEGA65/mega65-core/blob/bc7a3ece8aaee3d4d9f5df09cd71c70b1225a827/src/vhdl/gs4510.vhdl#L2643)
returns sample-valid in bit 2 and stopped in bit 3. Control writes do not assign
sample-valid (lines 3492-3497); hardware can assert stopped when current and top
addresses match (4681-4689). These status bits do not establish enabled playback.
This confirms a source-level readback mismatch; it does not identify P08's
actual rejected bits or certify the installed core version.

The fresh source copies P08 exactly and changes only `group1_transport.c`.
It ORs all four channel readbacks and requires mask F3 to equal zero. This
excludes status bits 2/3 while retaining rejection for every enable, loop,
sign, sine and sample-width bit. This is stricter than checking enable alone.
All shutdown writes and every other readiness/integrity check are unchanged.

## Hardware and contract effects

The same four volatile registers are read; the revised expression evaluates
all four rather than short-circuiting. Reads have no acknowledged/cleared
status side effect in the inspected implementation. Ordinary C ABI clobbers
apply. No new CPU-visible or physical allocation, MAP/base-page, DMA, IRQ/NMI
policy or public/generated interface changes occur. Timing cost changes only
in terminal admission after acquisition stops; no workload/deadline threshold
changes. Original context invalidation and the separate terminal capsule remain
unchanged. Audio global-disable/SID shutdown writes remain in `cfaudio_stop()`;
no new global-register predicate or audio feature is introduced.

## Local identity and validation

Experiment: `build/r0f/group1/terminal-recovery/audio-readback-01/`.
Qualified source: its `source-inputs/`; root working target remains unchanged.

- First fit attempt PASS: exclusive resident end $BFF5, 11 bytes free;
  seven bytes smaller than P08, no protected-region growth.
- PRG 37509 bytes, SHA-256
  `acc735f280f9d4e86b3b2040e5b2bed987908331f7899a87f5382c6cd23cd4d8`.
- Native owner/workload/scene/audio/display/pool/CRC and resume checks PASS,
  including 83 codec rejects, under the existing sanitizer harness.
- Actual extracted transport and unchanged export policy pass ASan/UBSan:
  18 prior integrity cases plus 1,280 audio readback cases. Every possible byte
  on each channel is tested, accepting only 00/04/08/0C; all 256 simultaneous
  status combinations pass. Enabled channels still reject, with or without
  status bits. 2,624,256 prior policy comparisons pass.
- All 47 Group 1 Python tests PASS.
- Exact source/checkpoint and generated/ledger identity checks PASS; all 9,726
  prior frozen entries match. Only the named target predicate changed.
- Focused NTSC and PAL PASS: actual 327680-byte, 3200-record trace and SAVE, 20 chunks;
  nominal timing WITHIN_OBSERVED_BOUNDS, zero misses/low-cadence cohorts.
- Collision preservation PASS: exact unchanged PRG refuses existing G1T00,
  preserves prior bytes and actual returning SAVE, reports S5/E03/F00.
- Fresh P09 structure/content and four exact-name boots PASS (two NTSC,
  two PAL), each with 3200 records, 20 chunks, actual SAVE, corruption checks,
  capacity and operator summary checks. Canonical remains unchanged.
  P09 is XEMU_BOOT_VERIFIED only.
  Canonical SHA-256:
  `bd1b645630c93d0ef764f3b6167924c0962ad67ed528d4ac8172ff2d4f9c5959`.

Commands (run from repository root):

```sh
python3 -B tools/diagnostics/r0f_group1_audio_readback_validate.py build/r0f/group1/terminal-recovery/audio-readback-01
python3 -B tools/diagnostics/r0f_group1_resume_recovery.py host --experiment build/r0f/group1/terminal-recovery/audio-readback-01
python3 -B tools/diagnostics/r0f_group1_resume_recovery.py qualify --experiment build/r0f/group1/terminal-recovery/audio-readback-01
python3 -B -m unittest discover -s tools/diagnostics -p 'test_r0f_group1_*.py' -v
python3 -B tools/diagnostics/r0f_group1_audio_readback.py ntsc
python3 -B tools/diagnostics/r0f_group1_audio_readback.py pal
python3 -B tools/diagnostics/r0f_group1_audio_readback.py negative-export
python3 -B tools/diagnostics/r0f_group1_audio_readback.py carrier-build --name R0FG1P09.D81
python3 -B tools/diagnostics/r0f_group1_audio_readback.py carrier-boot --name R0FG1P09.D81 --mode 1 --number 1
python3 -B tools/diagnostics/r0f_group1_audio_readback.py carrier-boot --name R0FG1P09.D81 --mode 1 --number 2
python3 -B tools/diagnostics/r0f_group1_audio_readback.py carrier-boot --name R0FG1P09.D81 --mode 0 --number 1
python3 -B tools/diagnostics/r0f_group1_audio_readback.py carrier-boot --name R0FG1P09.D81 --mode 0 --number 2
python3 -B tools/diagnostics/r0f_group1_audio_readback.py carrier-finish --name R0FG1P09.D81
```

The exact pinned target build command and input hashes are in `runtime-01/build.json`;
preparation and `audio-readback.patch` bind the sole target change to P08.
The zero-context review patch independently replays to the exact target;
original contextual patch remains retained locally and hash-indexed.
Tooling adds a thin adapter to the existing qualification/carrier pipeline and
reuses the prior full transport/policy tests. No historical tooling is rewritten.

## Boundaries and next action

SD delivery and physical execution are NOT RUN for this revision. Eleven free
bytes are not feature expansion headroom. Physical cause, installed core,
physical trace/timing, Group 1/full R0-F acceptance and Group 2 remain pending.
Preserve P08/P07/P06/P05 and all older tested identities; do not overwrite,
repair, rename or rerun them. No card operation or publication is included.

The [frozen packet](../evidence/r0f/group1/2026-10-03-audio-readback/README.md)
preserves source, PRG, tests, hardware-reference excerpts and actual emulator
exports. Complete canonical image:
`build/r0f/group1/carriers/R0FG1P09/canonical/R0FG1P09.D81`.
Next action is owner-run pinned allocator delivery, live hash/extent/eject
gates and exact P09 physical chooser/entry/runtime observation. The desired
terminal summary is S4/E00/F14, followed by return of the card for independent
actual-trace reduction. A photo or emulator pass alone cannot close physical
proof. Record actual video mode and core/ROM identities when available.
