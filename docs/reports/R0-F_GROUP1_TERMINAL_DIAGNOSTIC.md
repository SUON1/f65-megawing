# Group 1 terminal-preparation diagnostic — 2026-10-02

**BLOCKED by resident fit. Neither diagnostic is executable or deliverable.**
The owner authorized continuation after P06 reached tick 3200 with mask 1F,
then failed terminal preparation with 6B. Actual returned SAVE passes;
no G1Txx export exists. See the [physical record](../evidence/r0f/group1/2026-10-02-p06-physical/returned/README.md).

## Build Intent and inspected authority

Continue on `codex/r0f-group1-resume-clock`, remote main freshly verified at
`c27d89787d1d5c4472e24262e0181c47943d46be`. The existing dirty work and P06
remain preserved. Inspect current state/WIP, development workflow,
programming/C standards, original Group 1 Build Intent and export amendment,
private capture/transport interfaces, generated export/trace bounds, qualified
P06 implementation and host/build controllers. Use a fresh copy of P06 to
separate terminal rejection paths without weakening any guard. Initial bound:
30 minutes/two target variants, started about 20:42 PDT; both variants and
host analysis completed by 20:47 PDT. No third target variant was attempted.

Completion condition is a fitting, host-qualified local diagnostic or a
preserved bounded fit blocker. Fit must pass before focused NTSC, then PAL
and exact-carrier gates. No new SD write, physical run, publication, acceptance
or Group 2 implementation is authorized by this diagnostic step.

## Attempted change

Private terminal capture and transport preparation return zero on success
and a nonzero diagnostic code on rejection, replacing their former boolean
return convention. Names and private header comments explicitly reflect this
convention. Main propagates the result through lockout; DOS-copy rejection
retains 6B. The capture host mock and extractor follow the private convention.
Original storage/resume logic, public/generated ABI and all integrity checks
remain unchanged. The transport policy implementation is unchanged.

The attempted codes distinguish:

| Code | Rejection |
| --- | --- |
| 6B | Terminal DOS-context copy |
| 70 | Capture record/fault/IRQ status precondition |
| 71 / 72 | Header / result write |
| 73 | Trace-region read |
| 75 / 77 / 78 | Record / pool / world acquired-versus-readback CRC |
| 79 / 7A | Capacity-tail copy / pattern comparison |
| 7B | Final CRC write |
| 80 | Transport fault/result-stage/ROM-restoration precondition |
| 81 | Transport read or append |
| 82 | Whole-trace CRC or freeze |
| 83 | Export readiness rejection |

Some codes still cover multiple checks; this is diagnostic narrowing, not a
promise to distinguish every readiness field. **No code in this table was
observed on physical hardware.** P06 still has only the generic 6B boundary.

## Exact build results

| Variant | Change | End exclusive | Free bytes | Result |
| --- | --- | --- | --- | --- |
| P06 preserved | Qualified predecessor | BFF1 | 15 | Historical fit PASS |
| diagnostic-01 | Distinct private failure returns | C02A | -42 | FAIL; not executed |
| diagnostic-02 | Same, finalization marked noinline | C0EE | -238 | FAIL; not executed |

Variant 1 PRG: 37562 bytes, SHA-256
`41d2e28f48e317a6ff3d010889b04d93295ce1ce4302c6af15ce1126268ed723`.
Variant 2 PRG: 37758 bytes, SHA-256
`4181b39554104f408a60bb68174dbd5868fc29fba6cbc4b25a444e5a3ff6e935`.

Both link and pass the existing protected IRQ/terminal static checks, but fail
the resident end bound. Variant 1 adds 57 bytes relative to P06; its `main`
symbol grows by 57 bytes. Outlining finalization in variant 2 makes total
growth 253 bytes rather than saving space. No reserve or capacity changed.
Do not use either PRG. There is no P07 or other new carrier.

## Hardware and contract impact

The attempted changes affect ordinary resident terminal C code and its private
return values. C ABI clobbers remain compiler-managed. Existing CPU-visible
and physical ranges are reused; the failed builds exceed the resident bound
and therefore cannot be admitted. No MAP/base-page, DMA submission or register
access changes were introduced. Terminal work remains outside acquisition;
IRQ/NMI ownership and readiness predicates remain intact. Variant 2 introduces
a terminal-only call frame; its target stack/runtime behavior is unqualified.
Generated artifacts are unchanged. Root target source and P06 are untouched.

## Validation actually performed

Both build commands reuse `r0f_group1_owner_integration.build`, with explicit
isolated source/output paths, the P06 predecessor build record, and the frozen
capacity controller's terminal validator. Exact compiler commands, source input
hashes, section bounds and PRG identities are retained in each `build.json`.
No emulator or hardware execution is permitted after either fit failure.

The second variant's host analysis was run independently of target admission:

```sh
cd build/r0f/group1/terminal-recovery/diagnostic-02/source-inputs
python3 -B tools/diagnostics/r0f_group1_owners_validate.py \
  /Users/slice/Developer/f65-megawing/build/r0f/group1/terminal-recovery/diagnostic-02/host-analysis \
  --reference-pool /Users/slice/Developer/f65-megawing/build/r0f/group1/pool-integration/owner-01/source-inputs/src/diagnostics/r0f/group1_pool.c
```

PASS: native ASan/UBSan owner, scene, workload, audio, display, pool and CRC
checks; 83 codec rejects; extracted capture finalization retains zero/partial/
full world cases, region CRC/read failures, capacity-tail corruption and copy
failures, result/header/final-CRC write rejection, immutable checkpoints and
repeated finalization. This validates success/rejection behavior with mocked
transport. It does not establish every new numeric code or actual transport
readiness on hardware. The first variant's copied host extractor still used
the old function name and was not run; the second updates that extractor.

All 522 files of the prior resume packet, nine original physical-observation
files and twelve returned-card files still match their manifests. Source
patch replay and changed-file/generated-output scope are checked in the new
[evidence packet](../evidence/r0f/group1/2026-10-02-terminal-diagnostic/README.md).
No original freeze is rewritten. CURRENT_STATE remains unchanged.

## Disposition and next action

The broad return-code diagnostic does not fit and is not a candidate correction.
The physical inner cause is still unknown. Preserve both failures and the
passing P06 source; do not bypass CRC/readback, capsule, stop-state or reserve
checks to obtain an export.

The next narrow approach should preserve the current boolean interfaces and
expose a terminal-only first-failure breadcrumb in an already-admitted private
status byte, rather than propagating many return values through inlined main.
First measure its full resident fit; no savings are assumed. Do not conflate
this proposed implementation with a confirmed hardware cause or a qualified
build. A fresh bounded continuation is required before another target variant.
