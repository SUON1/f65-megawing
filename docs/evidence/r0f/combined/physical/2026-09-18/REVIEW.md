# CF001 physical observation — 2026-09-18

Status: hardware acquisition completion observed; raw capture validation pending.
This is development evidence, not full R0-F acceptance.

Owner supplied three original photos and the statement **"Sound occured"**.
Original attachment group: `1208EE7E-E874-48C8-875F-C0C434C56B2F`.
The unmodified photos and contemporaneous SD-transfer records are retained
beside this report, with identities in `SHA256SUMS`.

## Observations

- Photo 1: colored objects on the light test display with a blue border.
  A still photograph cannot prove motion, frame cadence, or absence of tearing.
- Photo 2: blue text display with repeated E glyphs near the bottom. Duration
  and cause are not established. The following photo shows a readable summary;
  this intermediate image alone does not establish a crash.
- Photo 3: `CF001 / F65BLK02`, acquisition complete, physical review required.
- Audible sound is owner-reported. This does not separately establish SID and
  PCM acoustic output, warning preemption, or external audio latency.

Manual visual transcription of photo 3 (all displayed numbers are hexadecimal):

| Field | Displayed hex | Decimal where useful |
|---|---|---:|
| Fault | 00 | 0 |
| Reference | 02 | Nominal hardware counters |
| ROM restored | 02 | Target reports restored |
| Ticks | 00000A50 | 2640 |
| CRC32 | 76684463 | Not independently verified |
| Kernel clock estimate | 0008013C | 524604 |
| Calibration error | 00001514 | 5396 |
| Clock frame | 000A5461 | 676961 |
| DMA jobs | 2759 | 10073 |
| PCM moves | 00000616 | 1558 |
| Real key edges | 00000000 | 0 |
| World swaps | 00000250 | 592 |

The zero fault and restored-ROM fields are displayed target assertions, not
an independently reduced hardware capture. Nominal estimates are not traceable
SI measurements or accepted performance limits. No physical raw bytes, page
CRCs, or full-capture CRC have yet been checked from this run.

## SD evidence

The retained fill log reports success and safe eject. Pre/post audits identify
the same `disk4s1` FAT32 extent, device offset 108425216, logical offset 0,
length 819200. Post-fill SHA-256 is
`b13853a7ddaf3bf26dfcaceb7e4466ab2d58702b96bfcbe9ae62c7db56ed3d82`,
matching the exact CF001 candidate previously tested in Xemu.
The original native blank hash is
`ba963e2c0e8dd686e03568b41ca9d4c6196762e166a2de8a6fcbb829dd5bd4e8`.
This closes the previously outstanding SD hash/one-extent/eject record gap.
OS eject success does not guarantee absence of reader/Finder problems.

The release snapshot remains `AWAITING_PHYSICAL_CHOOSER_VERIFICATION`.
Runtime identity is visible, but no chooser/directory photo is supplied here;
no formal release-state or acceptance promotion is made. The immutable
pre-SD archive and its original manifest remain unchanged.

## Next evidence needed

Before reset, press N and photograph all 14 raw pages, 01 through 0E. N advances,
P goes back, S returns to summary. Retain the current run even if input was
not exercised. Ask whether A was tapped and released during the colored
display: zero real edges can mean no input was supplied or an input-path issue;
the photos cannot distinguish them. Do not infer a keyboard failure yet.

After capture, reset as instructed by the program. Independent page/full CRC
checks and the existing Java reducer must precede raw-measurement conclusions.
Full parent workload, physical uncertainty, latency/window/limit obligations
and owner acceptance remain open as detailed in the combined handoff.

## Intake scope and checks

Inspected: `F65_OFFICIAL_RECORD.md`, `00_D81_LOADABILITY_GATE.md`, combined
handoff, R0-F evidence map, combined main/display/keyboard source, three photos,
SD pre/post audits, fill log, and release-state fields. No code or contract edits.
Registers/clobbers, CPU/physical memory ownership, MAP/base page, IRQ/NMI,
DMA behavior, deadlines and generated target artifacts: unchanged/not applicable
to this evidence intake. No D81 or SD bytes were modified. No new target or
Xemu run is claimed. The source fill log is retained as evidence, not rerun.

Validation: `shasum -a 256 -c SHA256SUMS` in this directory; JSON parsing and
pre/post extent/hash assertions; byte comparison with supplied originals;
`git diff --check`. Results recorded in the task handoff.
