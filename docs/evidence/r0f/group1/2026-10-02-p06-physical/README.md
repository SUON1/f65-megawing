# P06 physical observation — 2026-10-02

Status: physical runtime FAIL; returned-card analysis pending. P06 is retired:
**INVALID — DO NOT USE**. Preserve the card and do not rerun, rename or repair it.
The owner supplied these photos in response to the P06 physical instructions;
explicit filename and video-mode confirmation remain pending.

The unmodified [first photo](photo-1.jpg) shows multicolored patterned output,
without readable diagnostic fields. It does not establish renderer correctness.
The [second photo](photo-2.jpg) reads `FAULT 6B / STATE 0A / TICK 0C80 /
MASK 1F / NMI 00`: tick 3200, all five resumed-service advancement bits set,
and no displayed sticky NMI. This supports progression through the resumed
interval beyond the earlier P05 tick-1600 boundary, not independent timing,
model/checksum, trace-integrity or full workload acceptance.

## Exact-source boundary

Inspected the qualified isolated P06 `successor_integration.c`,
`group1_capture.c` and nonreturning `group1_terminal_export_45gs02.s`, alongside
current state/WIP and the previously inspected Group 1 and D81 contracts.
At tick 3200 the applicable `lockout(107u)` is at line 1407 of the qualified
integration source. The initial capture-init sites precede workload execution.
The terminal path enters only with no prior `cffault`; it requires
`dos_copy(KERNAL_BACKUP_TO_DOS)` and `r0fg1_capture_finish()` before handing
control to the nonreturning exporter. That exporter never returns through
this C lockout. Under the qualified control flow, the photo therefore locates
failure in terminal preparation, not a KERNAL trace-file SAVE error.

Capture finalization has multiple rejecting paths: record/fault/IRQ status,
trace writes/reads, acquired-versus-readback CRC comparisons, capacity-tail
readback, and transport preparation. The generic 107 masks which path failed.
No specific inner failure, physical memory corruption or timing cause is
established by these photos. The graphics photo alone does not diagnose one.

The service mask is computed after the resumed tick loop from advancing
counts for display, audio, input, IRQ and DMA. Reaching the final tick with
that mask provides bounded physical continuation evidence; it does not replace
an actual exported trace and independent model/timing reduction. No trace
absence is asserted until the returned card has been inspected.

## Preservation and next step

Original photos are copied byte-for-byte and hashed. Delivery records confirm
exact P06 bytes, one extent and safe eject before this run. The canonical D81,
qualified target source, prior frozen packet and tested card remain unchanged.
An ignored local retirement guard prevents candidate reuse. This evidence-only
update has no register/clobber, CPU-visible/physical allocation, MAP/base-page,
DMA, timing/deadline or IRQ/NMI changes; generated artifacts remain unchanged.
No new build, emulator launch, SD write or hardware run was performed here.

Return the card for a read-only snapshot, original-payload/BAM/chain checks,
actual SAVE validation and export inventory. Resolve the terminal preparation
subfault before requesting another fresh-carrier physical test. Group 2 has not
started; Group 1 and full R0-F acceptance remain ungranted.
