# P08 physical audio-readiness rejection — 2026-10-03

The owner supplied the photograph and returned the SD card after receiving
the P08 installer. The screen reads **75 / 0A / 0C80 / 1F / 00**: tick 3200,
all five resumed-service activity bits, and an audio-stopped readiness
rejection. Compact failure text matches this candidate. Exact filename
confirmation, PAL/NTSC and fresh platform identities remain unrecorded.
The actual returned R0FG1P08.D81 contains the exact qualified PRG.

## Delivery and returned evidence

Retained installer records pass clean read-only pre/post filesystem checks,
staged/final/mounted canonical hash, one 819200-byte extent at device offset
65564672, and safe eject. File count rises 186 to 187 and free space falls
800 KiB/200 clusters; the raw extent records establish contiguity separately.

Live returned volume identity matches removable FAT32 UUID
83FFC12E-67E1-307F-91AD-E584C2E01E87, currently disk4s1. A host-only snapshot
was compared again with the mounted image after extraction. Independent
chain/BAM parsing and pinned c1541 extraction agree on four closed entries:
AUTOBOOT.C65, R0FSUCC, TOKEN and RSSTATE. All original payloads match canonical.
The actual 34-byte SAVE loads at $3063 and exactly matches the independent
qualified-source tick-1600 golden 6B765FDB and checksum/index encoding.

No G1Txx files exist. No actual terminal result or complete physical timing
trace is available; no full-result oracle PASS is claimed. See
[returned verification](returned/verification.json).

- Canonical D81 SHA-256:
  `9e2030ef8f45077aa29890e60b4d904e37b14b15115e9a6b1611eb0b44849abe`.
- Returned D81 SHA-256:
  `2b2998e344ff5d2639cd65a7b9beb4f5cf52ecb30bce22f9bda196e7a3d7d0a5`.
- Actual PRG SHA-256 (37516 bytes):
  `1c842e345a3d5ec15b3eb167535a776da5e78eaf26a0d0d6239f7073f5a3b468`.
- Actual SAVE SHA-256 (34 bytes):
  `7d2f63b8e8e970bb35c351174fae1ca365245f14acf35db0d3cf9016ba8ba5bd`.

The complete returned image remains at
`build/r0f/group1/carriers/R0FG1P08/returned-01/R0FG1P08.D81`.
The changed image hash reflects the added SAVE; original payloads did not drift.

## Exact failure and remaining uncertainty

In the frozen P08 `group1_export.c`, code 75 is the first rejection when
`readiness->audio_stopped != 1u`. Its producer in `group1_transport.c`
requires all four full bytes at $D720/$D730/$D740/$D750 to equal zero.
`cfaudio_stop()` writes zero to these four registers and $D711 before terminal
preparation. Whole-trace readback/CRC and freeze precede readiness evaluation.
The earlier display predicate passes; later IRQ/ROM/capsule/NMI and length
predicates are not proven by a first-rejection code. No channel byte values
were captured. Which channel/bit rejected and whether playback was still
active remain unknown.

The official [MEGA65 chipset reference](https://files.mega65.org/files/m/mega65-chipset-reference_4hh2eE.pdf),
April 3, 2024 edition, printed pages 82-87, distinguishes channel enable
(bit 7) from the stopped flag (bit 3). It describes disabling a channel by
clearing enable and setting the stopped flag on sample completion. Thus a
whole-byte zero test can reject a non-playing channel. This is a concrete
readback-semantics hypothesis, not a captured physical bit value or a finding
about the owner's unrecorded core version. The exact shutdown/check contract
must be reviewed before changing the predicate; preserve genuine playback-
enabled rejection and all other integrity checks.

## Disposition

P08 is **INVALID — DO NOT USE** and locally retired. Do not repeat its
installer, rerun, rename, repair or overwrite it. Its source and all previous
freezes remain unchanged. The next bounded copied-source task is to resolve
audio-control/status readback semantics and correct or diagnose the audio
readiness predicate, with host tests for stopped status and enabled channels,
fit, focused NTSC/PAL and a fresh exact-carrier gate before any later delivery.
Four free resident bytes remain a hard constraint. Group 1/full R0-F acceptance
and Group 2 progression remain pending.

Authority: current WIP and Group 1 Build Intent/export amendment, repository
workflow and D81 gate/workflow. This turn preserves and analyzes off-card
evidence only. No target correction, rebuild, emulator launch, card write,
filesystem repair/check, raw allocation audit, unmount, eject or publication
occurred. Card remains mounted and unchanged. Target registers/clobbers,
CPU-visible/physical allocations, MAP/base-page, DMA, timing/deadline and IRQ/NMI
changes are non-applicable; generated/public interfaces and CURRENT_STATE
are unchanged.
