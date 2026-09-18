# F5 physical photo intake

Owner-supplied batch `1C31151B-15DD-4DAD-846F-1273113B67EF`, reviewed
2026-09-17. All 23 original JPEGs are retained unchanged in `photos/`;
`SHA256SUMS.txt` identifies the originals and retained SD pre/post records.
The subsequent reconstruction and independent raw reduction now PASS, as
recorded below. This is not calibrated timing or R0-F acceptance.

## Observed evidence

Photo 1 is the F65R0F5 summary. Photos 2–23 cover the 22 displayed pages,
`0001`–`0016` inclusive, with offsets `0000`–`2A00`. Page labels are one-based
hexadecimal. Earlier conversational instructions saying `0000`–`0015` were
incorrect; the owner supplied the complete displayed sequence.

The summary visibly reports acquisition complete and inherited functional
fixture PASS. The following visual transcription has now been confirmed by
independent reduction of the reconstructed bytes. All values are hexadecimal
raw CIA counts:

| Case | P50 | P95 | Max | Late | Miss | Mask | Span33 |
|---|---|---|---|---|---|---|---|
| NORMAL | 0034 | 0034 | 0035 | 0000 | 0000 | FFFF | 0004E23F |
| LAG | 003A | 003E | 003F | 0000 | 0000 | FFFF | 0004E247 |
| SHED | 0039 | 0045 | 0048 | 0000 | 0000 | FFFF | 0004E253 |
| FAULT | 0034 | 0035 | 0035 | 0000 | 0000 | FFFF | 0004E240 |
| PRESS | 0034 | 0034 | 0037 | 0000 | 0000 | FFFF | 0004E23F |

Displayed frame counts before/after: `00040B8F` / `00040B89`.
Fault / ready high-water / video / speed: `00 03 87 60`.
Raw address/length: `5162 2A80`; exported total including result: `2B80`.
Displayed stream CRC: `8D78FBC0`, now independently matched from the
reconstructed physical byte stream. The summary and page sequence support observed
summary/capture viewing and forward navigation; previous-page navigation
and boundary behavior are not independently established by these stills.

## Initial general-OCR attempt: NOT VERIFIED (superseded below)

Local macOS Vision OCR was attempted on all original photos with language
correction disabled. Its exact output is `ocr-unvalidated.jsonl`; strict
row/header assessment is `ocr-assessment.json`. Neither is accepted evidence
of the raw byte values. OCR split some headers/rows, inserted spaces and
misrecognized digits. No page yielded all 16 exact, ordered data rows through
this strict extraction path, so page/whole-stream CRC validation and the
independent Java timing reduction have **not** passed for this physical run.
The summary photo's absence of a page header is expected, not an error.

At that initial intake, no physical capture or successful Java reduction was
issued. It was a transcription limitation, not a target-test failure. The
original failed OCR output is retained, not silently replaced.

## Reviewed reconstruction: PASS

All 22 page CRCs pass, as does whole-stream CRC `8D78FBC0`. The unchanged
strict Java importer accepts the 25-line page transcripts, checks ordering,
offsets, lengths, padding, page and stream CRCs, then invokes the independent
timing validator. Its physical-capture result and separate corruption tests
pass: 2640 samples, 80 cohort spans, 35 corrupted summaries and 163 corrupted
fixed fields rejected. The five summary rows above are independently confirmed.

- Capture: `physical-capture.bin`, 11136 bytes.
- SHA-256: `042b8155e16591864c6de5b5855fc28427b789b40b90b0c23623d2540815d700`.
- Machine-readable result: `physical-validation.json` (numeric values decimal).
- Java output: `physical-capture.java.txt` and `physical-timing.java.txt`.
- Final transcripts: `transcription/page-0001.txt` through `page-0016.txt`.
- Per-page identity and address-label corrections:
  `transcription/transcription-manifest.json`.

Method: segment photographed rows and glyphs using image intensity and local
or fitted line boundaries; recognize hexadecimal glyphs against photographed
address-label examples, excluding poorly classified training examples by
cross-photo address-label checks. This classifier never reads a CRC or an
expected measurement value. Two image-processing variants are retained as
`automatic-local/` and `automatic-fitted/`; photos 5 and 20 use the fitted
candidate, others the local candidate. Every selected whole-page candidate
must pass its independently read displayed checksum.

Four single-digit visual corrections and one complete row transcription are
explicitly recorded in `transcription/analysis/r0f-manual-corrections.json`,
with enlarged-original review images retained alongside it. Printed address
labels and fixed presentation text are separately restored to the observed
screen layout; they are not substituted measurement bytes. The manifest
retains all 14 address-label corrections. Three initially misread page-CRC
headers were also corrected by direct inspection of enlarged original pixels;
`r0f-headers.png` retains that review. Checksums were used only to accept/reject
transcriptions, never to solve missing bytes or select guessed character values.
No emulator captures or expected fixture values supplied physical payload bytes.

The one-off analysis scripts are retained under `transcription/analysis/`;
they depend on Python 3.12, NumPy 2.3.5 and Pillow 12.3.0 and retain the local
workspace/temporary paths used. They are evidence-processing scripts, not a
production OCR tool, target change, or a replacement for the Java validator.
Original JPEG hashes remain unchanged. No repeat hardware run was needed.

### Independent validation commands

Run from repository root, with the JDK recorded in `../java-identity.json`:

```sh
mkdir -p /tmp/r0f-physical-java
R0F_JDK='/Users/slice/Documents/Codex/f65-megawing/toolchain/runtime/jdk-full/jdk-21.0.12+8/Contents/Home'
"$R0F_JDK/bin/javac" -d /tmp/r0f-physical-java tools/generators/src/main/java/f65/tools/R0FTimingOracle.java tools/generators/src/main/java/f65/tools/R0FCapturePages.java
r0f_verify_dir=$(mktemp -d /tmp/r0f-java-verify.XXXXXX)
"$R0F_JDK/bin/java" -cp /tmp/r0f-physical-java f65.tools.R0FCapturePages --decode "$r0f_verify_dir/physical-capture.bin" docs/evidence/r0f/capture/physical/transcription/page-*.txt
cmp "$r0f_verify_dir/physical-capture.bin" docs/evidence/r0f/capture/physical/physical-capture.bin
"$R0F_JDK/bin/java" -cp /tmp/r0f-physical-java f65.tools.R0FTimingOracle docs/evidence/r0f/capture/physical/physical-capture.bin
git diff --check
```

All commands passed. Validator source hashes are in `physical-validation.json`;
neither validator was modified to accept this physical capture.

## SD delivery evidence

Saved helper records were found locally and retained:

- Blank SHA-256: `ab8cee8b00313d7e1a0a5b731733eec2fc5135ad931960ea7d927224d084463e`.
- Filled SHA-256: `67183150719f1bbba01b862532c5996953e1d6c10cc38e1f9352b281895cc627`,
  matching the Xemu-verified F65R0F5.D81 release identity.
- Path `/Volumes/MEGA65FDISK/F65R0F5.D81`, FAT32 removable `disk4s1`.
- Both audits show one 819200-byte extent at device offset 113143808,
  logical offset zero. Allocation remained unchanged.
- Safe eject: **PASS, owner-supplied Terminal evidence**. The subsequent
  `TRANSFER-TERMINAL.txt` records `Disk /Volumes/MEGA65FDISK ejected`,
  `D81 MEGA65 SLOT FILL PASS` and `safe_eject=PASS`. Its pre/post fields match
  the retained audit records. This closes the previously missing eject
  evidence for F5 only; it does not revise the earlier F2 eject incident.
- Physical F5 runtime is observed. The stills do not separately document the
  chooser filename/directory or every delivery gate. The release manifest
  is not retroactively promoted to TEST_ELIGIBLE.

No further SD transfer or repeated hardware run is requested for this evidence
update. Delivery and photographic raw reduction are separate verified results;
neither supplies calibrated units or full combined-workload acceptance.

## Scope and next work

Keep calibration, full combined-service proof, platform/evidence provenance,
and R0-F acceptance open. IRQ was masked, DMA was not run, and the display
expressly disclaims calibrated time/latency. No new target code, D81 build,
SD write, register/memory/ABI/timing contract change, commit or push occurred
in this review. Applicable checks: original-photo copy identity, retained
record hashes, JSON syntax, strict OCR assessment, and `git diff --check`.
