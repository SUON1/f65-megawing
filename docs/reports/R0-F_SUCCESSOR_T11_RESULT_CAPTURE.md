# R0-F T11: complete physical result capture

## Latest physical checkpoint — 2026-09-28

CAP14's direct-allocator delivery and physical entry succeeded. The three
owner photographs supplied all 512 result bytes; transcription, CRC32
49C0FF3E and existing semantic validation PASS. Fault 00, state 09, tick 0042,
mask 1F, NMI 00, advancing IRQ and matching preserved-memory CRCs are recorded.
See [physical evidence](../evidence/r0f/successor/2026-09-28-cap14-physical/README.md).
The card has returned: actual RSSTATE SAVE extraction, unchanged original
payload checks, post-run D81 structure/content checks and independent Java
result/SAVE reduction all PASS. See the physical evidence's `returned/`
reports. T11's bounded capture/storage validation is complete for review.
No new blank or hardware rerun needed; no SD changes were made.
This supersedes earlier pending CAP14 statements below, not the broader R0-F
closure requirements. No full R0-F acceptance is claimed.

## Build Intent and boundary

Owner approved building the next focused test after IRQ11's photographed
physical success. Build R0FCAP12.D81 locally: expose the existing 512-byte
successor record as two stable hexadecimal pages after acquisition/cleanup.
CAP12 was retained as a development-only discarded candidate after visual
QA found inherited banner text trailing its shorter CRC heading. Its host and
viewer checks passed, but its full carrier sequence was stopped. Never deliver
CAP12. The corrected, separately fresh-built identity is **R0FCAP13.D81**.
Keep workload, lifecycle, generated layouts, fault predicates and raster
correction unchanged. No SD transfer, commit/push, production ABI, measured
limit or full R0-F acceptance is authorized by this local build.

Authorities: repository development/C standards, D81 gate/workflow, successor
admission reconciliation, T02/T03 generated contracts and memory ledgers,
T10 IRQ correction. Fresh origin/main is ae2b397, an ancestor of this branch;
preserve the existing uncommitted T09/T10 source and evidence.

## Hardware impact

Result bytes remain at CPU $1900-$1AFF, read-only during viewing. Screen writes
use inherited cffinal_screen/cfscreen/cfline/cfhex helpers and the existing
final display buffer. Poll/acknowledge $D610 only after cleanup, as in CF001.
No extra storage call, DMA, physical allocation, MAP/base-page change,
IRQ/NMI handler change, workload timing or deadline change. Application-text
and small local stack growth must pass target accounting. No reserve use.
The recorded result describes acquisition, not later user key activity.

## Predecessor observation (not full record validation)

Owner photo identifies R0FIRQ11: fault 00, state 09, tick 0042, mask 1F,
NMI 00; reserve 3C7D60D8 before/after; result CRC F9A5C840;
IRQ 0015 -> 0029; IEC 00/00; features 2B;
CPU/VIC/EN/VIDEO/CMP/MODE = 31/60/E1/87/80/88, vector 28BE.
The exact pre-run SD hash was
e7889a59f95a68d3b167880398881f4d17b628b0cd2c1b269f8e4b701797e5fa,
819200 bytes in one extent at 59404288; safe eject succeeded.
This supports entry/runtime-summary success and resumed IRQ advancement in
that run. It does not independently validate the unseen 512 result bytes,
saved file or full parent requirements. Preserve IRQ11 unchanged.

## Planned evidence

Native tests execute the actual page renderer with mocked screen callbacks,
checking all 512 bytes, offsets, page bounds and immutable source data.
Importer rejects missing/duplicate/out-of-order rows and CRC mismatches,
then uses the existing successor semantic validator. Independent Java result
and actual SAVE validation remain separate and must not synthesize a SAVE
file as physical evidence. Exact-name NTSC/PAL carrier regressions and target
memory/ROM bridge checks are required before any delivery handoff.

Physical checklist, only after SD hash/extent/eject gates: photograph summary,
press N and photograph page 01, press N and photograph page 02. S returns to
summary. No typing of hexadecimal data is required of the owner. No new blank
is requested. This capture fixture does not add missing latency/phase/load
measurements; those remain separate subsequent work.

## Closure coverage after the IRQ11 observation

| Area | Supported now | Still required |
| --- | --- | --- |
| Exact carrier and resumed IRQ | IRQ11 SD hash/extent/eject plus physical entry and advancing IRQ summary | CAP13 is a different candidate and needs its own delivery/physical evidence |
| Same-run storage/context/services | IRQ11 summary indicates completion; predecessor host/Xemu full records | Capture full physical result; independently reduce it and actual saved bytes without inventing missing data |
| Phase/deadline/calibration | Retained bounded nominal observations | Current-parent phase/window coverage, overhead and physical uncertainty |
| Input/audio/display | Existing bounded model/service evidence | Required semantic edge/load corpus, latency, complete-world age/cadence and protected-service contention |
| Memory and faults | Static fit, bounded reserve/negative tests | Worst exercised dynamic high-water and remaining deterministic pressure/fault corpus |
| Acceptance | Development authorization and one bounded runtime observation | Evidence review and explicit owner R0-F acceptance; measured-limit approval stays separate |

CAP13 addresses only the second row's result transport. A result-page PASS
cannot close the other rows. No new measurement equipment or repeated native
blank creation is assumed by this task.

## Local validation and identity

Canonical CAP13: `build/r0f/d81-workflow/R0FCAP13/canonical/R0FCAP13.D81`,
819200 bytes, SHA-256
`86377dd0d677b91a8a21c87ed243a1ed22f78d8cbbace8f048aa75cbd6a157c0`.
PRG: 23792 bytes, SHA-256
`cf605bd377ddcee2c72cdc4abfd20c3ae9eee350b7b78b36cbde8ff1adf8fc23`.
Resident use 25971 bytes; margin 14988; high-water exclusive $8574;
protected end remains $2B07; zero reserve bytes. Exact dirty-tree input hashes
are retained; no new source commit, push or generated-contract layout change.

Commands/results:

- `python3 -B tools/diagnostics/r0f_successor_physical_diagnostic.py all --name R0FCAP13.D81`:
  host/target PASS (1527538 integration checks, 525587 IRQ checks, CF001
  regressions and 16842752 RH001 cases), memory/layout/ROM-bridge gates PASS;
  exact-carrier run status is recorded separately in the release manifest.
- `python3 -B tools/diagnostics/test_r0f_successor_capture.py`: seven tests PASS.
  ASan/UBSan actual-C renderer test is also run by the builder: all 512 bytes,
  two pages, 254 rejected page numbers and immutable input PASS.
- `python3 -B tools/diagnostics/r0f_successor_capture_probe.py --out build/r0f/cap13-viewer-1`:
  exact-copy NTSC viewer PASS. N/S/wrap/reset navigation, every displayed byte,
  CRC/semantic import and immutable record PASS. Page-1 PNG visually inspected;
  page 2 shares the checked layout and all 256 displayed bytes were decoded.
- `python3 -B tools/diagnostics/r0f_successor_capture.py build/r0f/cap13-viewer-1/transcript.txt --out build/r0f/cap13-viewer-1/imported`:
  PASS; imported bytes equal actual emulator record. Not physical evidence.
- `python3 -B tools/diagnostics/r0f_successor_irq_negative.py --good-run build/r0f/d81-workflow/R0FCAP13/carrier-source-freeze/ntsc-1 --out build/r0f/cap13-negative-1`:
  PASS: disabled IRQ yields 65, forged pass rejected by Python and Java,
  valid modular rollover accepted. Disposable development fixture only.
- `python3 -B tools/diagnostics/test_d81_delivery.py`: 18 tests PASS.
- `python3 -B tools/diagnostics/r0a_validate.py .`, Python AST parsing and
  `git diff --check`: PASS.

CAP12's first sandboxed Xemu launch failed before runtime because config
template access was denied. The permitted retry and separate viewer run
executed, but visual QA retired CAP12 before delivery. Its evidence remains;
it is not a released artifact. CAP13 was constructed fresh, never patched
into the earlier image. Source files and canonical hashes were rechecked.

Final exact-carrier result: two NTSC and two PAL clean boots PASS, with
independent Python and Java result/SAVE checks for all four runs. Canonical
state is **XEMU_BOOT_VERIFIED**, not physical acceptance. Release/accounting
and full per-run evidence are retained under
`docs/evidence/r0f/successor/2026-09-22-workflow/R0FCAP13/`.
Additional viewer and negative summary evidence:
`docs/evidence/r0f/successor/2026-09-28-cap13-viewer/`.

At local build completion no CAP13 SD delivery or physical run had occurred.
The owner's subsequent Finder copy matched bytes/hash but failed allocation
with 13 extents; do not physically test, overwrite or retry it. The separately
approved CAP14 delivery preparation preserves the program unchanged and repeats
all exact-name host/emulator gates. See
[CAP14 preparation](R0-F_CAP14_DELIVERY_PREPARATION.md); its actual card write
and physical confirmation remain pending.
The local viewer requires only two result photographs plus the summary,
after separately approved delivery passes its gates. Retain actual post-run
SAVE bytes when the card returns; do not replace them with expected bytes.
