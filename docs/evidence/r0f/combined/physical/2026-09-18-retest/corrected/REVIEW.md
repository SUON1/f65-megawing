# CF001 retest — corrected capture and phase-3 verification

2026-09-18. **Physical transcription and independent CF001 acquisition checks
PASS. Full R0-F acceptance remains OPEN.**

This supersedes only the unverified-transcription status in `../REVIEW.md`.
That intake, its failed OCR candidates, originals and original SHA256SUMS remain
unchanged. The first hardware run (`../../2026-09-18/`, zero real edges) is a
different acquisition and is not merged with this retest.

## 1. Transcription and both checksums

All fourteen photographed pages 01–0E are present, ordered by their displayed
offsets. Each has sixteen 32-byte rows; the final page has 416 valid bytes and
96 zero padding bytes. The reconstructed stream is exactly 7072 bytes:
1792 result bytes followed by 5280 duration bytes.

| Check | Photographed/stored value | Independently computed | Result |
|---|---|---|---|
| Result CRC32, first 1788 bytes | `32B8A599` | `32B8A599` | PASS |
| Duration CRC32, 5280 bytes | `105995A3` | `105995A3` | PASS |

Capture SHA-256:
`85929a342620677dbf7b98cdf46eeb670be9ddf0797cfff7ce5e463f6821d982`.
Block hashes and unchanged Java-source hash are in `verification.json`.
These are two whole-block checksums, not per-page CRCs.

The correction used original image pixels, not expected target/model bytes.
Connected glyph components replaced the earlier grid that cut through letters.
Two manually read photographic rows trained the image-only classifier. Final
manual corrections are recorded in `corrections.json`: photo 12 row 4,
photo 15 row 15, and clipped leftmost F glyphs in photo 13 row 0 and photo 15
row 2 (row/column indexes are zero-based). The review crops and uncorrected
classifier rows are retained. No CRC inversion/search or substitution from
Xemu was used. CRCs were checked only after image-based reconstruction.

`verify_capture.py` reproduces the final stream from the retained classifier
rows and explicit corrections, compares every exported page/binary, checks
padding, recomputes both CRCs, and checks real input counts. The original
analysis scripts retain their historical temporary-directory paths; the
read-only reproduction script uses paths relative to itself.

## 2. Independent physical reduction

The unchanged Java oracle was freshly compiled with pinned JDK 21, all warnings
treated as errors. Both `--pages` and binary-block inputs PASS:

- 2640 nonzero measurements, 80 independently reduced 33-tick windows;
  all cohort medians, p95, maxima, sums and span relationships agree.
- Independent workload golden checksum `D9EEAB81` agrees; 30 resealed semantic
  corruptions are rejected. Eight additional transport negatives are rejected.
- Acquisition stage 7F, fault 00, nominal hardware reference 02, ROM state 02,
  base page 02, CPU port 35, no recorded NMI; 187 active synthetic slots.
- Complete 131072-byte ROM comparison count and before/after ROM CRCs agree;
  reserve before/after CRCs agree. These are target-generated observations
  independently checked for consistency, not a separate physical memory dump.
- Real edges **4 detected / 4 consumed**; scripted edges **32 / 32**.
  This supports the owner's A-key exercise. Aggregate counts do not identify
  each key, establish four A presses, prove every semantic command, or measure
  external key-to-display latency.
- IRQ count 1648; DMA jobs 10073; input samples 1618; audio services 1647;
  PCM progress 1558; preemptions 16; complete-buffer swaps 592.
- Hardware/software stack observations 58/73 bytes; snapshot high-water 3,
  queue high-water 64, controlled faults 16, storage rejection count 1.

| Case | Swaps | Nominal aggregate Hz | Max tick, CIA counts | Max late, CIA counts |
|---|---:|---:|---:|---:|
| Normal | 144 | 27.334 | 4601 | 2108 |
| Deliberate renderer lag | 16 | 3.031 | 4592 | 838 |
| Tiers | 144 | 27.335 | 4591 | 2112 |
| Fault | 144 | 27.333 | 4708 | 2112 |
| Pressure | 144 | 27.333 | 4592 | 2105 |

Comparison calibration is 524604 nominal CPU clocks versus 530000, absolute
residual 5396 (about 1.018%). Timestamp overhead is 5 CIA counts; DMA maximum
221; maximum observed audio-service gap 20605. Before/after mean CIA frame
counts are both 16569; recorded spread is 4. Neither zero mean drift nor the
small calibration residual establishes traceable physical-clock accuracy.
Aggregate cadence is not a minimum-frame-rate or accepted scene-budget proof.
The lag case deliberately suppresses rendering; no production 3 Hz tier is
approved. No new timing/latency acceptance threshold has been invented.

## 3. Full verification of the existing CF001 candidate

Executed without modifying the delivered PRG or D81:

- Fresh ASan/UBSan host compilation and execution PASS: model, snapshots,
  queue/range/DMA boundaries, 6092 exact-ratio vectors and 10000 edge pairs
  plus simultaneous-bit latching.
- Fresh pinned LLVM-MOS compile/link reproduces the candidate PRG byte for
  byte. The existing build's static map/ABI/IRQ/trap checks were rerun on
  the new ELF/disassembly. Generated contract header matches its JSON exactly.
- All 20 recorded source inputs match the build accounting. The immutable
  pre-SD evidence manifest and prior retest-intake manifest pass SHA-256
  verification; all 17 retained originals match their supplied source files.
- All nine archived Xemu captures pass the freshly compiled Java reducer.
- The unchanged D81 validator's complete structural/content/extraction checks
  PASS. Its final release-record-writing section was deliberately not executed,
  preserving the delivered candidate's existing release state. Executed source
  and prefix hashes are in `host-d81-gate.json`.
- Fresh exact-D81 NTSC and PAL Xemu runs both PASS, each with zero faults,
  2640 samples, independent Java PASS and complete restored-ROM SHA-256
  agreement. Both original screenshots were visually inspected: readable
  CF001/F65BLK02 completion banners and results. See `fresh-xemu.json` and
  retained boot directories. The earlier two-per-mode boot evidence remains
  intact; these are two additional clean starts, not replacements.

An initial sandboxed Xemu launch failed before producing a memory capture;
`xemu-sandbox-failed.log` records the denied configuration/OS-service access.
It is not a target failure or a passing test. The subsequent launches use
the required macOS access and disposable emulator SD images, not the physical
SD card. The release manifest is not downgraded or promoted.

Exact unchanged candidate: `F65BLK02.D81`, 819200 bytes, SHA-256
`b13853a7ddaf3bf26dfcaceb7e4466ab2d58702b96bfcbe9ae62c7db56ed3d82`.
PRG SHA-256:
`163579294c45994c647a02efc190c94e53d4df7149ae234d44357ec97ac08530`.
Source HEAD is `82df3dbffdfc562c496a8fffe768434d169d7698`; the candidate's
original build accounting retains its historical dirty-tree baseline and
authoritative per-input hashes. No new carrier or SD transfer was performed.

## 4. Full R0-F coverage disposition

The requested phase-3 review verifies the current experiment; it is not a new
contract that redefines full R0-F as this experiment alone.

| Obligation | Current evidence | Still needed for full closure |
|---|---|---|
| Physical capture integrity | Both CRCs, complete pages, independent reductions PASS | Closed for this acquisition; no recapture requested |
| ROM handoff | Reset-only reclaim, restoration/protection and CRC checks | Usable production ROM/filesystem return; current test requires reset |
| Clock/calibration | Hardware counter ratio, overhead, spread, nominal calibration | Independently quantified uncertainty and installed-binary provenance |
| Combined workload | Synthetic 21-stage/187-slot scene with concurrent services | Complete production-shaped mesh/terrain/rendering and semantic input/context/joystick corpus |
| Timing and contention | Cohort tick/late/DMA/service-gap measurements | Required relative/rolling-window matrix, per-module ceilings and IRQ response/masking evidence |
| Physical configuration | NTSC R6 capture, model 6, core ID B5C770C6; earlier SD hash/extent/eject | Complete attributed supported configuration matrix and formal chooser/release-state review |
| Acceptance | Development authorization and bounded evidence | Full dependency/DEC-002/DEC-003 review, named owner acceptance, then separate measured-limits approval |

The next engineering work is the missing proof coverage/contract work above,
not another attempt to photograph this same capture. No scope waiver, accepted
limit, candidate-parent approval, Phase 1 or gameplay authorization is inferred.
Audible sound was reported for the earlier run; this retest's owner statement
confirms A exercise, not separate acoustic latency or warning-tone acceptance.

## Reproduction, inspected scope and impact

Exact argument arrays and exit codes: `commands.json`, `target-reproduction.json`,
`static-checks.json`, `transport-negative.json`, `retained-xemu-reduction.json`
and `fresh-xemu.json`. Standard read-only entry point:

```sh
python3 docs/evidence/r0f/combined/physical/2026-09-18-retest/corrected/verify_capture.py
```

Fresh Java: `javac -Xlint:all -Werror -d CLASSES
tools/generators/src/main/java/f65/tools/R0FCombinedOracle.java`, followed by
`java -cp CLASSES f65.tools.R0FCombinedOracle --pages` and all fourteen
`transcripts/page-*.txt` paths in order; alternatively pass `result.bin durations.bin`.
For evidence integrity, run `shasum -a 256 -c SHA256SUMS` inside this directory.

Inspected: official record, repository instructions and D81 gate; CF001
contract/schema, Java oracle, builder/static checks and host tests; handoff,
stage control, closeout review, full-closure plan and retained photographs,
OCR, manifests and SD reports. No target or public contract was edited.
Changed paths are evidence artifacts and current status links, including the
full-closure plan's stale physical-status row. Preserved specifications,
original records, target sources, generated interface and existing carriers
remain unchanged. Registers/clobbers, CPU/physical memory ownership,
MAP/base-page, IRQ/NMI, DMA and timing/deadline contracts: **no changes**.
Generated map/symbol/disassembly verification copies are retained here; no
new target is delivered. No commit or push performed in this increment.

Final checks: corrected evidence SHA-256 manifest, all retained JSON syntax,
read-only capture reproduction and `git diff --check` PASS. Phase-3 review
of this CF001 acquisition is complete; full R0-F still requires the explicit
coverage and acceptance items above.
