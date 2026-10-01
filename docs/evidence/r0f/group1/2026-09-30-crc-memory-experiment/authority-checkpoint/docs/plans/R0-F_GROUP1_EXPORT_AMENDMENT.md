# Group 1 terminal trace export: approved private admission amendment

Status: OWNER APPROVED FOR IMPLEMENTATION on 2026-09-29 by "Make the
corrections" following presentation of this amendment. Validation and target
integration remain required. This changes a private proof contract, not
production StorageService. The owner also requires immediate DRY, ETC and
orthogonality; see `docs/PROGRAMMING_PRINCIPLES.md`.

## Problem and controlling rule

The accepted campaign calls for complete raw evidence including the post-storage
interval, exported after acquisition so the owner returns the card rather than
photographing a large trace. The current T02 contract requires the guarded
pre-C KERNAL context at `$08020000-$0802161F` to be invalidated before services
resume. Its forward-only lifecycle cannot re-enter storage. This is enforced
by `r0fs_resume_allowed` and `r0fs_transition`, not just documentation.

Calling the existing wrapper twice, suppressing invalidation, or treating
`SERVICES_RESUMED` as `APPLICATION_SAVED` is not an admissible implementation.

## Approved disposition

Admit an additional **terminal-only export capability** for the Group 1 variant:

1. Preserve the original one-use transition and invalidation semantics.
2. Explicitly admit a separate guarded opaque KERNAL export capsule captured
   before C initialization. It persists through acquisition, is inaccessible
   to simulation, and can only be consumed after acquisition has permanently
   stopped. This is an intentional extension of private context retention,
   not a claim that duplicating the old context avoids its lifetime rule.
3. Admit bounded non-authoritative trace storage in disjoint resource memory.
   Select exact ranges only after the generated ownership/overlap model proves
   them disjoint from every live allocation and both reserves. An unavailable
   range or target-fit failure stops admission; do not borrow reserves.
4. At terminal export, drain application DMA, stop display/audio/IRQs, restore
   and verify ROM, validate the export capsule, preserve the required terminal
   result state, and enter KERNAL exclusively. No measured workload resumes.
5. Write uniquely named diagnostic trace chunks inside the newly built test D81. Never
   replace RSSTATE, an existing trace or a tested carrier. The exact filename,
   byte count, format version, acquisition CRC and export status are recorded.
6. Invalidate the export capsule on consumption. A failed export cannot emit
   an acquisition/export PASS. Do not retry automatically. Where safely
   recoverable, display a compact terminal failure; otherwise fail closed.
7. Independently extract and reduce the actual exported bytes. A screenshot,
   expected bytes or an emulator memory dump cannot stand in for physical
   post-run export evidence.

## Validation required before any delivery

- Generated capture/export memory lifetimes and all overlap/exclusion checks.
- Boundary/corruption/double-use cases; no export while acquisition is active;
  invalid guards/CRC/NMI and failed ROM/storage operations reject.
- Explicit register/stack/base-page/MAP/vector and IRQ/DMA contracts; protected
  code/data remain accessible during KERNAL mapping.
- Source/disassembly and host tests verify original resume still invalidates
  its original context, and terminal export cannot restart the workload.
- Normal and negative Xemu runs; actual extracted trace matches target CRC and
  independent reduction in NTSC and PAL.
- New exact-carrier gates. CAP14 and predecessor artifacts remain unchanged.

## Implementation allocation and effects

`interfaces/r0f_group1_export_contract.json` owns constants and generates C
and assembly bindings. `memory/r0f-group1-export-memory-ledger.json` extends
the T02 ownership model without changing its source ledger or original
context lifetime. The separate capsule occupies `$08022000-$0802361F`;
non-authoritative trace storage occupies `$08030000-$0807FFFF`. Neither reserve
is used. The existing DOS entry backup remains live through terminal export;
it is restored and checked before entry.

After irreversible entry only, `$4000-$7FFF` becomes 16 KiB SAVE staging,
overlaying dead ordinary resident code/data. Link checks keep terminal code
and data below `$4000`. Terminal entry clobbers CPU registers/flags, the stack,
base page and `$0000-$15FF`, restores opaque KERNAL context, consumes the
capsule, and maps ROM for the admitted KERNAL calls. It never returns to C.
Measured work and application DMA have stopped; display/audio/IRQ are stopped
and pre-existing NMI rejects entry. The export interval is outside acquisition
and cannot be counted as a passing workload deadline. Original one-use
storage/resume semantics remain unchanged.

The development probe exports 33,025 deterministic bytes in `G1T00`, `G1T01`
and `G1T02`, including the actual 512-byte successor result. It tests complete
and partial chunks; it is not a delivery disk or a Group 1 timing workload.

## Alternative

Keep T02 unchanged and export the trace through read-only screen pages after
cleanup. This avoids a storage-lifecycle amendment but increases owner capture
work considerably. No screen count is promised before the trace format and
corpus are sized. It does not satisfy the earlier compact-summary/card-return
workflow without an additional verified capture mechanism.

## Approval boundary

Approval of this amendment permits implementing and qualifying the private
terminal capability, its generated memory admission and evidence transport
as part of Group 1. It does not authorize SD writes, physical execution,
production storage APIs, measured limits, publication or full R0-F acceptance.
