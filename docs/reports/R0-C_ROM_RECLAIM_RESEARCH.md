# R0-C ROM-Reclaim / Storage-Handoff Research

Status: **DEFERRED — NO RECLAIM OR RESTORATION WRAPPER AUTHORIZED**

Date: 2026-08-21  
Contract: `R0C-PLAT-ROM-001`  
Scope: research record only; it makes no executable platform claim.

## Pinned finding

The current official [MEGA65 Chipset Reference](https://files.mega65.org/files/m/mega65-chipset-reference_4hh2eE.pdf)
documents the 28-bit memory map, including the Attic range, and documents
Hypervisor Trap 00 subfunction `$70` at `$D640` with a required `NOP` as a
**toggle of ROM write protection** for `$020000-$03FFFF` while MEGA65 I/O is
visible. It does not describe a complete, reversible transaction that hands
that range to display ownership, restores it, and then proves an approved
storage environment can legally be called again.

The official [MEGA65 User Guide](https://files.mega65.org/files/m/mega65-userguide_Q5jaf7.pdf)
documents file loading and 28-bit load destinations, including Attic loading.
It does not supply the missing runtime reclaim/inverse-reclaim/storage-service
contract. The reviewed material therefore supports neither a KERNAL/ROM call
after reclaim nor a speculative Hyppo recovery sequence.

## What is documented enough to retain

- `$020000-$03FFFF` is the architecture's candidate pair of complete display
  stores after a documented ROM-emulation reclaim path.
- Trap `$00`, subfunction `$70`, `$D640`, and the mandatory `NOP` are a
  documented write-protect control operation only.
- MAP work, base-page state, `$01`, IRQ/vector state, and C/assembly clobbers
  require an admitted platform boundary; none may be inferred from the toggle.

## Facts still missing for admission

1. A documented primitive to transfer `$020000-$03FFFF` from ROM-emulation to
   display-store ownership, and the documented inverse.
2. A supported core / ROM / system-files / storage-device matrix that proves a
   usable storage service after the inverse transition.
3. Exact entry state, return values, register/flag clobbers, IRQ treatment,
   timeout behavior, and recovery behavior for both halves of the transaction.
4. A recovery-lockout route that never invokes ROM, KERNAL, Hyppo, disk, save,
   or callback code after a failed restoration.
5. A physical proof procedure using exact core/ROM/system-file/media identity.

## Required future evidence

Only pinned official documentation or a platform-owned, documented service may
close the gap. A future admission packet must link the source pages/version,
state the supported matrix, provide the bounded wrapper contract, and define
normal and failure tests. Until then, `ROC-ROM-001` remains deferred; the
R0-C target must keep storage out of the reclaimed state and must not claim a
post-reclaim save/media test.

## Non-decisions

This research does not select a production ROM strategy, storage medium,
display-store implementation, DMA policy, or recovery UX. DEC-012 remains the
narrow approval of a sacrificial writable D81 only for future R0-C media-fault
evidence.

## Owner closure disposition (2026-08-29)

The owner waived further R0-C physical media testing and requested candidate
completion. This does not resolve or pass `R0C-ROM-001`; post-ROM-reclaim
storage handoff remains deferred for a later authorized gate.
