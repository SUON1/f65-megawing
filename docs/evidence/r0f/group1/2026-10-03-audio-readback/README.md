# Group 1 audio readback correction — 2026-10-03

The fresh copied-source revision changes only terminal audio verification:
status bits 2/3 do not count as enabled/configured channels; every other
control and integrity check remains. See the
[report](../../../../reports/R0-F_GROUP1_AUDIO_READBACK.md).

Local fit/static, native and dedicated host, focused NTSC/PAL, filename
collision protection and four exact-name P09 boots pass. P09 is
XEMU_BOOT_VERIFIED only. No new SD write or physical execution occurred;
Group 1/full R0-F acceptance and Group 2 remain pending. Actual P08 failing
register bits and installed core identity remain unrecorded.

The packet preserves copied source, PRG/build identities, hardware reference,
host checks, actual exported traces/SAVEs, screens, carrier records and tool
checkpoints. Large disposable images and whitespace-bearing originals remain
unchanged at paths/hashes in local-artifacts.json. Never reuse retired P08 or
earlier tested carriers. The complete source remains in the named isolated
experiment, never the older root working target.
