# R0-F capture viewer contract — RC-1 slice, 2026-09-17

Private AD-001 proof instrumentation under the owner's full-closure direction
and “Build it” instruction. This is not the full combined harness, a calibrated
clock contract, or R0-F acceptance. No prior physical raw-export contract exists;
this document defines a new bounded post-acquisition screen transport only.

## Inputs and impact

Inspected official record; full frozen Architecture 1.4.1; Read-First authority
and escalation rules, approval/AD-001; candidate Architecture 1.5.1 language,
ABI, memory and evidence requirements; all current memory ledgers and interface
registries; B-register decision; F4 timing contract, build, startup, host/Java
tests, ownership and work plan; root D81 gate. Existing candidate authority and
historical F4 contract remain unchanged.

The viewer starts only after `r0f_timing_run` has stopped CIA timers. It reads
the result at $1900–$19FF and the linked 10880-byte capture, and writes only the
existing $0800–$0FCF text screen plus its own linked scalar state/stack. No raw
capture copy or extra page buffer is allocated on target. Linked storage is
charged separately for this variant within $2001–$CFFF; protected physical
$050000–$05FFFF remains untouched. CPU low-memory context is inherited; no
new physical mapping, MAP/EOM, base-page relocation, ROM call, DMA, vector,
ICR, CIA2, or clock-register access occurs in the viewer.

C ABI clobbers A/X/Y/Z/P and compiler pseudo-registers; B remains $02.
Inherited startup SEI remains in effect. No IRQ service measured. NMI remains
unmasked; no RESTORE/Freezer during acquisition. Nonreturning diagnostic;
reset required. Navigation is post-acquisition and cannot rerun or alter the
measurement. Dynamic stack high-water and production canonical exit are not
proved. CRC/render time is outside measured intervals and is not subtracted.

The private input helper reads $D610; nonzero values are written back to
acknowledge one event. This matches the official
[core register map at the photo-attributed source revision](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/iomap.txt)
and the existing R0-B read/ack probe. It is not a production input service or
latency/edge-loss claim. Unknown keys are acknowledged but do not navigate.

## Wire representation

Stream: exact 256-byte REV2 result followed by 10880 raw bytes, total 11136
($2B80), unchanged from the timing oracle's input. Generated constants define
512 payload bytes/page, 32 bytes/row, 16 rows, and 22 pages. The final page
contains 384 valid bytes; padding is zero and excluded from CRCs.

All displayed numeric fields are hexadecimal. Each 80×25 screen contains:

- Row 0: `R0-F RAW CAPTURE - F65R0F5`.
- Row 1: `PAGE NNNN OF NNNN OFFSET NNNN BYTES NNNN` (1-based page).
- Row 2: `TOTAL NNNN CRC32 NNNNNNNN PAGECRC NNNNNNNN`.
- Row 3: explicit hexadecimal/page-count explanation.
- Rows 4–19: four-digit stream offset, colon, and 64 hex digits (32 bytes).
- Row 20: raw counts/non-calibration notice; row 21 acquisition/fixture status.
- Row 23: navigation instructions; row 24 reset/no-disk notice.

CRC is CRC-32/ISO-HDLC (reflected polynomial EDB88320, initial FFFFFFFF,
final XOR FFFFFFFF). Whole-stream CRC appears on every page; page CRC covers
only valid payload bytes. CRC detects accidental capture/transcription errors,
not authenticity or identity with a D81. Carrier hash/platform provenance
must accompany physical captures separately.

First page appears automatically. N/space advances, P goes back; boundaries
clamp. S shows the timing summary, C returns to the current raw page. These
controls never write measurement data or touch media. A failed acquisition
can still be exported for diagnosis; the timing oracle must reject it as a
successful measurement. No success is inferred from valid CRC alone.

## Validation and handoff

Host C sanitizer tests render every page and exercise controls, bounds and
immutability. Independent Java CRC/decoder checks round-trip bytes, offsets,
lengths, padding, page identity/order/completeness, per-page and stream CRCs,
and then invokes the existing timing reducer. Corruption tests must include
duplicate/missing pages, wrong offsets, lengths, data, padding and CRCs.
Text input is exactly 25 ASCII lines/page, padded on the right to 80 columns;
no OCR repair or silent ambiguous-character substitution. All 22 pages are
needed; photos alone are not yet validated raw evidence.

Build variant `capture` outputs only under `build/r0f/capture/`, with a fresh
F65R0F5.D81 identity if packaging proceeds. F4 remains unchanged. Commands:
`F65_R0F_VARIANT=capture sh tools/build/r0f.sh host-test`, `build`, `audit`,
`package`, `xemu`. Xemu must independently validate the memory capture, compare
the displayed first page against the tested formatter, and retain two clean
boots/screenshots. Physical navigation/photographic transfer remains pending.

This fallback screen transport is deliberately usable with the present
hardware connections, but requires 22 pages per full capture. Do not request
an owner run merely to demonstrate it; complete the next admitted measurement
work first. It does not finish RC-1 calibration or RC-2 combined workload.
