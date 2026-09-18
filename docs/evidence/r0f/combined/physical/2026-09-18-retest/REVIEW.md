# CF001 physical retest — 2026-09-18

Status: physical summary/input exercise observed; all fourteen capture pages
received; byte reconstruction and independent reduction NOT VERIFIED.
This is not R0-F acceptance.

Owner statement: "I pressed A during the video / audio test during this retest."
This describes a new run, not a correction to the first run's zero-edge result.
The prior run remains separately retained under `../2026-09-18/`.

## Provenance and coverage

All 17 explicitly supplied HEIC originals are copied unchanged under
`originals/`. `originals.json` maps supplied order, exact original path,
retained filename, and SHA-256. The Apple Photos library was not modified.
Lossless decoded PNG previews were used for inspection in temporary storage;
these are derivatives, not substitutes for the originals.

Photo 1 shows the ROM-backup verification stage. Photo 3 is the completed
summary. Photos 4–17 contain raw pages 01–0E in order, offsets 0000–1A00.
The first thirteen headers specify 0200 bytes; the last specifies 01A0 bytes.
Every header displays result CRC `32B8A599` and duration CRC `105995A3`.
`analysis/headers.png` retains the separate header-review montage.
The CF001 transport has two whole-block CRCs, not individual page CRCs.

## Visually confirmed summary

| Field | Displayed hexadecimal | Interpretation |
|---|---|---|
| Fault | 00 | No target-reported acquisition fault |
| Reference | 02 | Nominal hardware counter ratio |
| ROM restored | 02 | Target reports restored ROM |
| Ticks | 00000A50 | 2640 ticks |
| Result CRC32 | 32B8A599 | Displayed, not independently verified |
| Kernel clock estimate | 0008013C | 524604 nominal CPU clocks |
| Calibration error | 00001514 | 5396 nominal CPU clocks |
| Clock frame | 000A5461 | 676961 |
| DMA jobs | 2759 | 10073 |
| PCM moves | 00000616 | 1558 |
| Real key edges | 00000004 | 4 observed edges reported by the target |
| World swaps | 00000250 | 592 |

The nonzero edge counter plus the owner's A-press report resolves the prior
question of whether real keyboard input was exercised in this retest. The
aggregate counter does not identify the key or prove semantic command behavior,
all presses consumed once, or external latency. Do not infer a count of A
presses from this aggregate alone. Audible sound was reported for the earlier
run; the current statement confirms A exercise during this video/audio retest,
not a separate acoustic timing or warning-preemption measurement.

## Transcription checks — not a hardware failure

Unmodified macOS Vision OCR output is retained as `ocr-01.json` through
`ocr-17.json`. Language correction was disabled. Dense rows are split or
misrecognized. Experimental image-only glyph segmentation/classification also
misread characters; its candidate bytes failed the two displayed CRCs.
Unvalidated rows, analysis scripts and strict Java rejection are retained in
`analysis/`. No guessed values were adjusted to force a checksum match, and
no emulator/reference-model bytes were substituted for photographed bytes.

The visual header coverage check passes, but the raw-byte reconstruction does
not. Therefore the independent physical oracle, cohort percentiles, real-edge
consumption, restored-ROM CRC agreement and performance reductions remain
unverified for this run. A rejection of OCR-derived bytes is not a target fault.
The next work is improved/reviewed transcription of these retained originals;
another hardware rerun is not requested merely because automated reading failed.

## Scope and validation

Inspected: official project record, repository instructions, existing CF001
handoff/evidence record, `interfaces/r0f_combined_contract.json`, CF001 summary
and page-export code, unchanged `R0FCombinedOracle.java`, and prior photo-analysis
tools. Changed paths are this evidence directory plus status links in the
official record, evidence map and combined handoff. No target source, ABI,
ownership, memory map, register/clobber, MAP/base-page, IRQ/NMI, DMA or timing
contract change. No D81/SD operation, rebuild, Xemu run, commit or push.

Original byte/hash comparisons and retained-file hash checks pass. All JSON
records parse. `git diff --check` passes. The unchanged Java `--pages` invocation
rejects the unvalidated reconstruction, as recorded in `analysis/oracle.txt`.
No physical raw-validation pass or release-state promotion is claimed.
