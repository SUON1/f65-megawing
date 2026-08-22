# R0-C Authority Blockers

Status: **OPEN — affected target paths are not implemented.**

This is a focused escalation record, not a waiver request and not a gate-closure
record. The candidate host/Xemu evidence is retained separately.

## R0C-STG-001 — physical Attic residency and staging

The current target diagnostic proves a bounded CPU copy from an explicitly
labelled Attic-model array into an owned proof buffer. It does **not** address
physical Attic RAM. The architecture prohibits arbitrary physical C pointers
and requires `MemoryAccessABI` to own MAP/base-page changes. No approved
target-side `MemoryAccessABI` or resource storage service is presently in the
R0-C admitted source surface.

Required resolution: admit or identify the authoritative existing wrapper for
physical Attic mapping/copy, including its MAP, `$01`, base-page, IRQ, callback,
and error-restoration contract. R0-C can then stage a package resource into the
declared `$050000-$052FFF` candidate range and measure it without touching
`$058000-$05FFFF`.

## R0C-ROM-001 — reclaim/storage handoff and restoration

No official, pinned mechanism has been supplied that proves how the target can
make the last storage call, enter reclaimed display-store ownership at
`$020000-$03FFFF`, guard unavailable ROM/storage calls, then restore an
approved storage environment on normal and failure exits. Guessing a ROM,
KERNAL, hypervisor, MAP, or vector restoration sequence is forbidden by the
current R0-C admission contract.

Required resolution: provide official-platform evidence plus an admitted,
reviewed wrapper/contract for the supported transition and restoration path, or
formally record that no supported path exists. The latter would leave
R0C-ROM-001 deferred rather than passed.

## R0C-SAVE-001 / R0C-MEDIA-001 — acceptance medium

`DEC-012` remains open. The candidate decision packet recommends a **separate
sacrificial writable D81/image** for R0-C acceptance, but it makes no
production selection. Without owner approval of the medium and recovery policy,
the target may not claim write-protect, removal, full-media, changed-media, or
interrupted-write proof.

Required resolution: owner approval or rejection of the documented candidate
in `docs/reports/R0-C_DEC-012_DECISION_PACKET.md`. R0-C will then bind the
selected adapter, use only sacrificial/recoverable media, and run the required
two-generation fault matrix.

## Consequence

These three items prevent both `R0-C IMPLEMENTATION COMPLETE` and `R0-C GATE
PASSED`. They do **not** invalidate the completed host and Xemu candidate
evidence listed below.

| Candidate evidence | Result | Identity |
|---|---|---|
| Host package/capacity/resource/staging/save-model test | PASS | `r0c-0.1.0-proof` |
| Xemu diagnostic candidate | XEMU PASS | result block SHA-256 `dc324cdd4f14501ad1551aad31b159ede272698e63b6e036d47577566fb7a378` |
| Package | PASS | SHA-256 `9b535b022c97a7b9eb52552ac07f7776c677f23a3c604b75f9541d43c114f19f` |
| D81 | PASS (package image build only) | SHA-256 `cd8a653eee2ba8d0233d500f50856ccaf46fc8efcf3555cfe7f73e5f3f2b0f56` |

