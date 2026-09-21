# R0-F successor memory/lifecycle static admission

Date: 2026-09-20

Task: R0 Closeout T02

Status: **STATIC ADMISSION PASS - READY FOR HUMAN REVIEW**

## Decision

The reviewed T01 Attic hypothesis is statically admitted for the private R0
proof platform.

The opaque 5,632-byte pre-C KERNAL context can occupy the guarded private
Attic range `$08020000-$0802161F` across the quiesced same-run storage
transition. The 5,632-byte payload is exactly `$08020010-$0802160F`, with
16-byte `$A5` guards before and after it. This allocation is disjoint from the
existing immutable ROM backup at `$08000000-$0801FFFF`.

The snapshot is restoration-only transition state. It is not authoritative
simulation/gameplay state, no simulation decision may consume it, ordinary C
does not receive an Attic pointer, and the lifecycle invalidates it before
workload service resumes. Protected assembly alone owns the fixed generated
address and bounds.

This admits a legal layout and lifecycle. It does not prove runtime behavior
or implement the full successor workload.

## Authority and generated contract

The admission consumes the current `spec-corpus.json` authority order, Main
Concept v1.6, Gameplay v1, Runtime v1 candidate §§5-6, the T01 successor
reconciliation, the R0 full-closure plan, and the retained private CF001 and
RH001 contracts/evidence for their stated scopes.

The authoritative private T02 source is
`interfaces/r0f_successor_contract.json`. The admission builder generates both
`interfaces/generated/r0f_successor.h` and
`interfaces/generated/r0f_successor.inc`; C and assembly do not duplicate the
numeric layout.

There is no public ABI, production `StorageService`, high-level memory-map,
100 Hz timing, 21-stage order, CoreRuntime ownership, pool-capacity, or
measured-limit change.

## Resident fit

Fresh predecessor builds and T02 target accounting produce:

| Charge | Bytes |
|---|---:|
| CF001 complete resident linked charge | 24,432 |
| RH001 complete resident charge except only the 5,632-byte linked context | 14,898 |
| T02 admission skeleton complete resident charge | 693 |
| Conservative successor charge | 40,023 |
| `$2001-$BFFF` resident capacity | 40,959 |
| Remaining conservative margin | 936 |

This is intentionally conservative: the CF001 and RH001 charges double-count
their shared runtime, model, platform and header content, while the entire T02
skeleton is charged again. No shared-code deduction is required for the PASS.
The small 936-byte result is an admission margin, not a production budget or
measured limit; the implementation task must link the actual combined image
and repeat accounting.

Any code and data/constant state required while a temporary `$8000-$BFFF` MAP
window is active must remain accessible and may not be hidden by that mapping.
The T02 protected output section accepts protected code plus protected
read-only/writable data and is linker-constrained below `$8000`; the current
skeleton has no separate protected data/constant input. Ordinary successor
workload code may still use the admitted parent-owned resident range through
`$BFFF` and is not moved below `$8000` merely because a protected path exists.
The T02 early capture uses 45GS02 flat physical access and opens no MAP window.

## Lifetime and exclusion result

`memory/r0f-successor-memory-ledger.json` accounts for resident code/data/BSS,
hardware and software stacks, opaque KERNAL context, low application memory,
DOS and DOS-overlay preservation, retained capture/results, resource staging,
HUD/display stores, PCM cache, DMA list, ROM backup, both reserves, color
attributes, and every transition reuse.

The only newly admitted physical allocation is the guarded Attic transition
snapshot. Existing chip-RAM ownership is not changed. Transition overlays are
legal only under encoded mutual exclusion:

- The unchanged `$010000-$017FFF` active-simulation envelope is partitioned
  into the application DOS-overlay band `$010000-$011FFF` and the application
  remainder `$012000-$017FFF`. This is ledger detail, not a high-level map or
  production ownership change.
- In `WORKLOAD_ACTIVE`, `QUIESCED`, `ROM_RESTORED`, `APPLICATION_SAVED`,
  `APPLICATION_RESTORED` and `SERVICES_RESUMED`, `$010000-$011FFF` has only
  normal application/active-simulation ownership. The bytes are backed up by
  `APPLICATION_SAVED`.
- KERNAL/DOS exclusively owns `$010000-$011FFF` only in `KERNAL_ACTIVE`,
  `STORAGE_COMPLETE` and `KERNAL_CONTEXT_RESTORED`. Authoritative simulation
  advances in none of those states. Application bytes are restored at
  `APPLICATION_RESTORED` before the next authoritative
  `SERVICES_RESUMED` state.
- `$050000-$051EFF` preserves low application memory, page 1 and page 2 only
  after resource work and application DMA are complete.
- `$01D000-$01EFFF` preserves the application DOS overlay only during the
  exclusive storage transition.
- `$054000-$055FFF` preserves entry-time KERNAL DOS context only while audio is
  stopped; it does not overlap the retained `$053000-$0530FE` PCM bytes.
- KERNAL ROM/display and DOS ownership is exclusive of renderer/application
  ownership while display fetch, IRQ service and application DMA are quiesced.
- `$057000-$057FFF` remains the existing staging reserve and is not consumed.
- `$058000-$05FFFF` remains read-only/untouched measured-limits reserve;
  successor allocation is zero bytes.

No allocation is treated as shareable merely because its conceptual users
differ; each physical overlap must have exactly one machine-readable
parent/subrange or exclusive-lifetime declaration. The validator enumerates
every range pair, rejects undeclared overlaps and rejects concurrent owner
lifetimes even when an overlay declaration exists.

## Startup, restoration and failure structure

The proof-only startup skeleton captures physical `$000000-$0015FF` before
base-page relocation and BSS initialization. It uses private B=`$16` scratch
at `$1622-$162A`, outside the captured source, touches no hardware/software
stack, makes no callback, starts no DMA and changes no MAP state. Static
symbol/disassembly checks enforce capture-before-`f65_basepage_enter`-before-
`__do_zero_bss`, flat-copy opcodes, guard initialization and absence of a ROM
call or MAP operation.

The lifecycle has explicit quiesce, ROM restore, application preservation,
KERNAL entry/storage, KERNAL-context restoration, application restoration,
canonical restoration and service-resume states. Any out-of-order event,
guard/CRC failure, NMI/RESTORE, outstanding application DMA, unmasked IRQ,
failed ROM restoration, storage error or failed canonical restoration enters
permanent lockout for that run.

The target skeleton links a protected canonical-restoration path through the
existing `r0f_pf_enter` implementation. It structurally restores MAP/base-page
and platform state before the resume marker. The next task must replace the
markers with the full admitted storage trampoline and prove the actual exits;
T02 does not claim execution evidence.

## Validation

Command:

```text
python3 tools/diagnostics/r0f_successor_admission.py build
```

Actual result:

- generated C/assembly binding regeneration: PASS;
- ledger range/count, exhaustive physical-overlap, reserve and Attic exclusion
  checks: PASS;
- negative static overlap cases: PASS; undeclared overlap, concurrent
  incompatible lifetime and missing DOS/application exclusion were each
  rejected;
- native ASan/UBSan lifecycle, storage/resume gate, zero/one/maximum/overflow
  copy-bound and guard/CRC corruption tests: PASS, 65,558 checks;
- fresh CF001 native/Java/model/compile/link/accounting checks: PASS;
- fresh RH001 16,842,752-state host test, Java/model, compile/link and static
  checks: PASS;
- T02 LLVM-MOS compile/link: PASS;
- target map, symbols and disassembly checks: PASS;
- generated accounting: `build/r0f/successor-admission/accounting.json`;
- conservative resident fit: 40,023 / 40,959 bytes, PASS;
- measured-reserve consumption: 0 bytes, PASS.

Also run during final review:

```text
python3 -m json.tool interfaces/r0f_successor_contract.json
python3 -m json.tool memory/r0f-successor-memory-ledger.json
python3 -m py_compile tools/diagnostics/r0f_successor_admission.py
git diff --check
```

D81 creation/modification, Xemu, SD-card and physical MEGA65 work were not run
and are not claimed. No evidence artifact was promoted. The PDF authority was
read for Runtime v1 §§5-6; no PDF was edited or re-exported.

## Exact next bounded task

**R0 Closeout T03 - successor combined-workload integration**, proposed branch
`codex/r0f-successor-combined-workload-integration`:

1. consume the generated T02 contract without changing its admitted ranges;
2. combine the actual CF001 workload services with the RH001 no-restart
   storage trampoline in one target image;
3. replace the T02 structural markers with complete quiesce, checked storage,
   restoration, failure-lockout and next-tick continuation paths;
4. prove the actual linked image fits `$2001-$BFFF`; ensure every code and
   data/constant byte required while `$8000-$BFFF` is mapped remains
   accessible; consume zero measured reserve and preserve public ABI/stage
   order;
5. run host, sanitizer, target map/symbol/disassembly and static integration
   validation only.

T03 should stop ready for founder review before any D81, Xemu, SD-card,
physical MEGA65, commit, push or PR action.
