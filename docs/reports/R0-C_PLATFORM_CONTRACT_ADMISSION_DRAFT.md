# R0-C Platform Contract Admission Draft

Status: **PROPOSED — UNADMITTED — NO WRAPPER IMPLEMENTATION AUTHORIZED**

Date: 2026-08-21
Milestone: Phase 0 / R0-C
Scope: real Attic-to-chip staging and post-ROM-reclaim storage handoff only.

This is a review packet, not an interface-registry change, a production ABI,
or evidence that either operation works on Xemu or physical hardware. It is
intentionally separate from `interfaces/f65_platform_abi.json5`: registering
these operations before approval would falsely make a proposal authoritative.

## Authority and evidence reviewed

- Approved Read-First v1.0; AD-001; 2026-08-20 approval record.
- Architecture 1.5.1 (candidate) and Engine Draft 0.2 (candidate):
  `MemoryAccessABI` alone changes MAP/base page; `ResourceManager` alone
  changes residency; consumers use handles rather than physical pointers;
  failed staging must preserve prior active state.
- Existing platform ABI registry: canonical public state includes MEGA65 I/O,
  `$01=$35`, base page `$0200-$02FF`, logical LLVM-MOS ABI page `$02-$21`
  under `B=$02`, and no active MAP scope.
- [Official MEGA65 Chipset Reference](https://files.mega65.org/files/m/mega65-chipset-reference_4hh2eE.pdf),
  v1.2 pinned for R0-B and current official copy: Attic RAM is not visible to
  VIC/SID consumers; it must be transferred into chip RAM before such use. It
  documents Hypervisor trap `$00`,
  subfunction `$70`, as a **toggle of ROM write protection**, with MEGA65 I/O
  visible and a mandatory `NOP`. It does not define the complete storage
  handoff/restoration transaction required below.

The official source also states that normal DMA is blocking and DMA lists use
the `$D700-$D702` registers. That makes DMA a possible later implementation
candidate, not an admitted R0-C backend or a production timing commitment.

## Shared non-negotiable invariants

- CPU stack `$0100-$01FF`; relocated base page `$0200-$02FF`.
- Only `MemoryAccessABI` may alter MAP or base-page state.
- Mapping scopes affect only `$8000-$BFFF`, do not nest, yield, invoke a
  callback, or wait for DMA.
- `FarPtr32` is 28-bit; ordinary C pointers are not physical addresses.
- `ResourceHandle16=$FFFF` is invalid; handle stability survives relocation.
- `$050000-$052FFF` is the candidate 12-KB R0-C resource/decode staging area.
  `$058000-$05FFFF` and the unallocated resident-code reserve are untouched.
- No direct VIC-IV or audio consumer may read Attic RAM. No tactical disk read
  is permitted.
- Canonical public exit must restore MEGA65 I/O, `$01=$35`, `B=$02`, cleared
  MAP offsets/EOM-complete state, base page `$0200`, resident vectors, and the
  documented IRQ state.

## Proposed contract A — `R0C-PLAT-ATTIC-001`

### Purpose and ownership

Provide one narrow operation requested by the R0-C `ResourceManager` proof:
validate a declared Attic-resident resource and copy it into an owned chip-RAM
staging buffer. `ResourceManager` owns the residency state transition;
`MemoryAccessABI` owns any map/base-page operation; a later admitted Core
platform service owns any hardware DMA start. Consumers receive a validated
handle and chip destination only, never an Attic pointer.

### Candidate interface shape (not a registered ABI)

```text
R0cStageResult r0c_stage_attic_resource(
    ResourceHandle16 handle,
    FarPtr32 attic_source,
    ChipStageRange destination,
    uint16_t encoded_length,
    uint16_t decoded_length,
    uint16_t required_alignment,
    Integrity expected_integrity);
```

The canonical schema, C layout, assembly symbol, calling convention, and
clobber list remain **TBD until admission and a compiler-ABI check**. The
prototype is only a review aid and must not be copied into a public registry.

### Preconditions

1. Target has a supported Attic configuration; a Nexys/non-Attic environment
   must return `ATTIC_UNAVAILABLE`, not emulate a physical pass.
2. `handle != $FFFF`, is inside the fixed 16-byte resource directory, and is
   `ATTIC_RESIDENT` under `ResourceManager` ownership.
3. `attic_source` has only bits 0-27 set and lies entirely in
   `$08000000-$087FFFFF`; size arithmetic is checked before addition.
4. Destination is wholly inside the owned candidate staging range
   `$050000-$052FFF`; it is not `$058000-$05FFFF`, display storage, scratch,
   code, or audio cache.
5. Length is nonzero, bounded by the destination, and satisfies the declared
   alignment; encoded/decoded limits and expected integrity have been checked.
6. There is no active mapping scope, callback, save transaction, storage call,
   or unresolved platform DMA. The caller is outside tactical disk I/O.

### Required behavior

1. Validate all inputs before touching mapping or destination bytes.
2. Enter only an admitted bounded platform access scope.
3. Transfer source bytes to chip staging using the admitted backend. A CPU-copy
   backend and a DMA backend are mutually exclusive candidates; neither is
   selected by this draft.
4. Validate destination integrity before changing the resource's active state.
5. On success, publish only `CHIP_RESIDENT_OR_STAGED` through
   `ResourceManager`, update staging high-water, and retain handle identity.
6. On every failure, restore canonical state and leave the previously active
   resource and its recorded integrity unchanged.

### Result classes

`OK`, `INVALID_HANDLE`, `DIRECTORY_RANGE`, `ATTIC_UNAVAILABLE`,
`SOURCE_RANGE`, `DESTINATION_RANGE`, `ZERO_OR_OVERSIZE_LENGTH`, `ALIGNMENT`,
`INTEGRITY`, `BACKEND_UNSUPPORTED`, `BUSY`, and `RESTORE_FAULT` are proposed
proof result classes. Exact numeric values are not admitted here.

### Measurements and required tests after admission

Record source/destination/length, backend, raster or cycle delta, staging
high-water, platform identity, and canonical-state restoration. Prove
zero/one/max/max-plus-one lengths, `$FFFF`, directory bounds, invalid FarPtr
high bits, Attic and destination edge ranges, alignment, integrity mutation,
repeatability, failed-stage rollback, and untouched reserve. Xemu may report
emulation behavior; physical MEGA65 evidence remains required.

## Proposed contract B — `R0C-PLAT-ROM-001`

### Purpose and boundaries

Define a guarded transition from a storage-capable public environment to
reclaimed display-store ownership, then an explicit, documented restoration
before any ROM/KERNAL/hypervisor-dependent storage call. It is not permission
to infer a restoration sequence from the `$D640/$70` write-protect toggle.

### Candidate proof state machine

```text
STORAGE_READY_CANONICAL
  -> LAST_STORAGE_OPERATION_RECORDED
  -> RECLAIM_REQUESTED
  -> RECLAIMED_NO_ROM
  -> RESTORE_REQUESTED
  -> STORAGE_READY_CANONICAL

Any failure -> RECOVERY_LOCKOUT (no ROM/storage call until canonical restoration
                         is positively verified).
```

`RECLAIMED_NO_ROM` forbids ROM, KERNAL, hypervisor, disk, save, and callbacks
from the diagnostic path. It is not a gameplay state. The only accepted route
out is an admitted restoration primitive followed by canonical-state checks.

### Preconditions

1. The final package/load/storage operation is logged with medium identity and
   a completed result; no save transaction, active mapping scope, or DMA is
   outstanding.
2. The platform is in canonical public state; the diagnostic and recovery code
   are proven not to execute from the storage being reclaimed.
3. Exact MEGA65 core, ROM, system-files, video, and storage identities match a
   supported contract matrix.
4. The reclaim primitive and restore primitive each have an official source,
   exact preconditions, effects, error behavior, and physical validation plan.

### Required behavior

1. Guard all storage/ROM entry points before reclaim and record the last legal
   operation.
2. Invoke only the admitted reclaim primitive. The known `$70` operation may
   be part of a later documented implementation, but its documented effect is
   write protection, not a complete ownership or restoration protocol.
3. In `RECLAIMED_NO_ROM`, reject attempted storage/ROM calls as a controlled
   proof failure; do not attempt an unsafe fallback.
4. Invoke only the admitted restoration primitive. Verify canonical MAP,
   `$01`, base page, B register, IRQ/vector condition, display ownership, and
   availability of the required storage environment before re-enabling calls.
5. On normal and failure paths, produce a result record that says whether
   restoration was verified. If it was not, remain in `RECOVERY_LOCKOUT` and
   require reset/recovery rather than calling ROM speculatively.

### Required research evidence before admission

The currently reviewed official materials do **not** provide all of these:

- The exact documented primitive that transfers `$020000-$03FFFF` from
  ROM-emulation ownership to display-store ownership and its inverse.
- Whether the supported ROM/storage service can be restored after that
  transition on the selected core/ROM/system-files matrix.
- Exact compiler/assembly register and flag clobbers, IRQ treatment, timeout,
  and recovery behavior for both operations.
- A supported-storage proof that can run after restoration without depending
  on undocumented KERNAL/hypervisor behavior.

Until evidence supplies these facts, `R0C-ROM-001` remains **DEFERRED** and no
reclaim/restoration wrapper may be implemented.

## Admission checklist

Admission requires an explicit human/platform review accepting each contract
independently, then a versioned addition to the platform ABI registry and an
owned memory-ledger entry. The review must supply:

1. Official source links/pages/version hashes for all platform primitives.
2. Supported physical core/ROM/system-files/storage matrix and no-Attic
   behavior.
3. Exact canonical entry/exit state and C/assembly clobber contract.
4. Backend choice or an explicit proof-only backend policy; no production DMA
   ceiling, staging cadence, tile size, or renderer choice.
5. Target code and stack accounting plus a failure/recovery plan that does not
   risk owner media or protected memory.
6. Host, Xemu, and physical test matrices with separate evidence classes.

## Non-decisions and current result

`DEC-012` is now approved only for a separate sacrificial writable D81 media
fixture. This draft does not choose a production medium, recovery UX, package
format, disk split, DMA policy, or renderer. `DEC-015` remains open.

**Current result:** research and planning are complete enough for admission
review; neither platform contract is admitted, implemented, or passing.
