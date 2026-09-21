# R0-F successor combined-workload integration handoff

Date: 2026-09-20

Task: R0 Closeout T03

Status: **HOST/STATIC INTEGRATION PASS - READY FOR HUMAN REVIEW**

## Outcome

T03 builds one actual linked successor image combining the admitted CF001
100 Hz / 21-stage workload, immutable snapshots, complete-buffer display,
semantic input, SID/PCM, IRQ and synchronous application-DMA paths with the
RH001 returning KERNAL/storage transaction.

The image reaches storage only between authoritative ticks, drains the active
renderer quantum, confirms application DMA is empty, disables VIC-IV display
fetch, stops audio and IRQ publication, restores and verifies ROM,
preserves application low memory/DOS overlay/page 1/base page, restores the
opaque pre-C KERNAL context, performs checked LOAD/SAVE/reload, restores the
application and canonical platform state in the admitted order, invalidates the
Attic context, resumes display presentation and continues the same
model/checksum lineage at the next tick. Display, audio, input, IRQ and DMA
service must each advance after return before the result can complete. Sticky
NMI/RESTORE observation at any point, including resumed ticks, prevents PASS.

This is compile/link, host and static evidence only. The image has not executed
in Xemu or on a MEGA65, and no D81 or SD-card artifact exists for T03.

## Governing contracts and unchanged T02 admission

The implementation consumes:

- `interfaces/r0f_successor_contract.json` and its generated C/assembly
  bindings;
- `memory/r0f-successor-memory-ledger.json`;
- `interfaces/r0f_combined_contract.json` and the CF001 model/platform paths;
- `interfaces/r0f_resume_contract.json` and the RH001 checked KERNAL operation
  set; and
- `interfaces/r0f_successor_integration_contract.json` plus
  `memory/r0f-successor-integration-memory-ledger.json` for the private T03
  result and linked-image accounting.

T02 ranges remain unchanged. The guarded Attic allocation is still
`$08020000-$0802161F`, its payload is `$08020010-$0802160F`, the resident
envelope is `$2001-$BFFF`, and the software stack is `$C000-$CFFF`.
`$058000-$05FFFF` is read-only sentinel input and consumes zero bytes. There is
no public ABI, production `StorageService`, high-level memory-map, 100 Hz,
21-stage order or measured-limit change.

## Actual linked accounting

The generated accounting record is
`build/r0f/successor-integration/accounting.json`.

| Item | Actual value |
|---|---:|
| Resident capacity, `$2001-$BFFF` | 40,959 bytes |
| Actual linked resident usage | 23,665 bytes |
| Resident margin | 17,294 bytes |
| Resident high-water, exclusive | `$7C72` |
| Protected transition code/data | 2,808 bytes |
| Protected end, exclusive | `$2B0F` |
| Guarded Attic transition allocation | 5,664 bytes |
| New physical allocations | 0 |
| Resource-reserve consumption | 0 bytes |
| Measured-reserve consumption | 0 bytes |

Target identity from the final T03 build:

- PRG: `build/r0f/successor-integration/R0F-SUCCESSOR-INTEGRATION.prg`
- bytes: 21,489
- SHA-256:
  `43074a4322b9a2ec35428e966d9f64ab30655c8f0f27516317e7e3f9e417264a`

Build-directory products are review evidence and are not promoted as retained
runtime evidence or a carrier.

## Hardware and restoration effects

- **Registers/clobbers:** the combined workload reuses the CF001 VIC-IV,
  CIA, SID/PCM, DMA and keyboard-matrix registers. The storage wrapper preserves
  caller X/Y/Z/P/B and the application stack/SP, while A returns storage
  status. Q is not independently preserved because A is the return value.
- **CPU-visible memory:** application page 1, page 2 and `$0300-$1FFF` are
  preserved. `$010000-$011FFF` remains an exclusive application/KERNAL overlay
  with no authoritative simulation during KERNAL ownership.
- **Physical memory:** only T02-admitted and predecessor allocations are reused.
  Page 1 and page 2 use `$051D00-$051EFF`; low application state uses
  `$050000-$051CFF`; DOS overlays use `$01D000-$01EFFF` and
  `$054000-$055FFF`.
- **MAP/base page:** pre-C capture uses B=`$16` scratch without MAP. The storage
  wrapper uses only the checked RH001 ROM-call allowlist. Canonical MAP,
  B=`2`, port `$35` and resident vectors are restored through `r0f_pf_enter`
  before C resumes.
- **DMA:** application DMA uses the inherited synchronous fixed-list path and
  is explicitly tracked as empty before display suspension and transition.
  KERNAL owns any internal storage DMA exclusively. The application DMA
  counter must advance again after return.
- **Display:** the bounded T03 fixture saves `$D011`, clears its display-enable
  bit only after renderer drain, and gates every ROM restoration on that
  suspended state. Presentation is reconfigured and `$D011` restored only
  after application memory and canonical MAP/base-page/platform restoration.
- **Timing/deadline:** authoritative releases retain the calibrated 100 Hz
  period and `r0fc_tick` retains the 21-stage order. The boundary records tick
  33 and resumes with tick 34; no tick executes during storage.
- **IRQ/NMI:** application IRQ service is stopped and masked before storage.
  Sticky NMI/RESTORE observed before storage, during the transition, after
  restart or during resumed authoritative ticks locks out the run and is
  recorded independently in the private result. Resident vectors and IRQ
  service are restored before the resumed-service requirement can pass.

## Validation

Primary command:

```text
python3 -B tools/diagnostics/r0f_successor_integration.py build
```

Actual results:

- native ASan/UBSan lifecycle, continuation, exact mailbox bounds including
  16-bit wrap rejection, chunked full-payload CRC, guard/CRC, post-resume NMI
  and deterministic fault/lockout checks: PASS, 1,516,258 checks;
- independent Java 21-stage lineage: PASS,
  `D9EEAB81` at tick 33 to `307A70D6` at tick 66;
- fresh CF001 native, Java, LLVM-MOS and accounting regression: PASS;
- fresh RH001 16,842,752-state host, Java, LLVM-MOS and static regression:
  PASS;
- T03 LLVM-MOS compile/link: PASS;
- map, symbols and disassembly: PASS;
- pre-C ordering, fixed Attic bounds and bridge carry rejection, display
  drain/suspend/ROM-restore/application-restore/canonical-restore/resume
  ordering, global sticky-NMI lockout, canonical MAP/base-page/port path,
  page-1/page-2 restoration, ROM-call allowlist, long-branch exclusion, IRQ
  preservation and protected code/data accessibility: PASS;
- actual resident fit and reserve accounting: PASS;
- generated C/assembly binding reproduction: PASS.

Additional review checks:

```text
python3 -m json.tool interfaces/r0f_successor_integration_contract.json
python3 -m json.tool memory/r0f-successor-integration-memory-ledger.json
git diff --check
```

No D81, Xemu, SD, physical MEGA65 or human-acceptance tier was run. These
omissions are required T03 boundaries, not implicit passes.

## Remaining runtime uncertainties

Static evidence cannot establish that the pre-C Attic copy, returning KERNAL
stack transition, ROM mapping, checked storage calls, DMA completion, IRQ
restart, PCM/SID restart, complete-buffer display restart or 100 Hz continuation
behaves correctly in the emulator or on hardware. It also cannot establish the
required carrier contents, PAL/NTSC behavior, storage failure presentation,
runtime stack high-water, external latency, calibrated uncertainty, physical
reserve sentinel, or full R0-F acceptance.

## Exact next bounded task

**R0 Closeout T04 - successor emulator and exact-carrier evidence** should:

1. begin from the reviewed and merged T03 image without changing the frozen
   T02 ranges or T03 workload/lifecycle contract;
2. construct one canonical exact input D81 containing the successor PRG,
   deterministic `TOKEN` input and documented boot entry under the repository
   D81 gate, then retain that canonical image immutably;
3. run host structure/content extraction checks and record the exact carrier,
   PRG, ROM, toolchain and source identities;
4. run clean direct-PRG diagnostic boots followed by at least two clean boots
   of the exact D81 in each admitted NTSC and PAL mode;
5. reduce the 512-byte result independently and exercise deterministic
   non-destructive storage/lockout faults; and
6. stop for founder review before SD transfer, physical chooser use, hardware
   evidence, measured-limit freeze or R0-F acceptance.

T04 must retire any failed carrier identity according to
`00_D81_LOADABILITY_GATE.md`; it must not repair or append to a tested D81.
Every writable Xemu run must begin from a fresh byte-identical disposable copy
whose pre-run hash equals the canonical D81. The mutated post-run image, its
hash and the extracted SAVE payload must be retained as run evidence. A
mutated run image must never be repaired or reused as the input for a later
"exact carrier" boot. Canonical construction, disposable-copy verification,
execution and evidence retention all remain subject to
`00_D81_LOADABILITY_GATE.md`.
