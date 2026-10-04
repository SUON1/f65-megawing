# R2 passes; capture skeleton fails resident fit

2026-10-03. Owner approved continuing toward hardware without serial approval
for routine increments. Existing capacities, reserves, acceptance and carrier
gates still apply. No target executed; no D81 or SD operation occurred.

## R2 retained result

Command: `python3 -B tools/diagnostics/r0f_group2_copy_encoder.py`.
Fresh source: `build/r0f/group2/copy-encoder/r2-b4wd7lrc/source-inputs`.
Source is derived from the exact R1 copy; no frozen source is edited.

PASS: 1484 actual-owner poisoned scratch handoffs under ASan/UBSan, plus 256
independent nine-byte request checks for 32-bit address/carry boundaries,
lengths 1/255 and success/failure propagation. Exact commands/logs are under
`r2/`; the supplemental encoder harness is under `r2/encoder-host/`.

The shared foreground encoder is explicitly not inlined so the three owners
share one packing body. Their original admission checks and fault assignments
remain at the callers. No public arbitrary-pointer interface, new physical
range, MAP/base-page, DMA or IRQ/NMI change. C call costs change; runtime timing
and hardware stack high-water are not qualified by this compile-only result.

R2 recovers 214 text bytes: resident end **$BE8C**, **372 bytes free**. BSS,
rodata/data, compiler static stack and protected section are unchanged from R1.
`r2/result.json` identifies the PRG, complete inputs and exact commands.

## Capture admission failure

Command: `python3 -B tools/diagnostics/r0f_group2_capture_fit.py`.
Fresh source: `build/r0f/group2/capture-fit/empty-11s9hxxh/source-inputs`.

This first empty-block encoder uses the existing 92-byte record workspace,
retains every acquisition region comparison, writes and independently reads
back the 352-byte extension, updates the outer CRC, and retains remaining tail
checks. It has zero used case slots and adds no live state. It is a compile-only
skeleton, not an admitted version-8 format or a fault observation. The existing
trace-version contract is deliberately not promoted; this output must never run.
A complete versioned generator/reducer and host negative corpus would be needed
before any execution, even if fit passed.

**FIT FAIL:** +741 text and +28 rodata = **769 resident bytes added**.
Resident end **$C18D**, **397 bytes beyond $C000**. BSS, data, static stack and
protected bytes remain unchanged. Additional live records and injectors are
not included, so this is not a near-complete suite failing by only 397 bytes.
The failed source/map/commands are retained under `capture/`; no retry or
repair of this identity occurred. No host behavioral PASS is claimed for the
capture skeleton; the compile/fit gate rejected it before runtime admission.

## Concrete consequence

R1 and R2 remain useful bounded improvements, but neither image is a hardware
fault-suite candidate. Do not construct a carrier from a startup-only probe or
an over-limit capture image to obtain a superficial hardware run.

The next engineering task is to integrate extension encoding with the existing
tail write/readback loop, eliminating the skeleton's separate chunk traversal
and per-byte CRC calls while preserving extension CRC, independent readback,
outer CRC and every existing acquisition comparison. This is within the approved
capture redesign; it does not need a new scope approval. Measure it before any
further case implementation. If that cannot fit the capture plus real cases,
a different resident-layout/capture architecture requires an explicit owner
choice; capacities/reserves may not be silently borrowed.

Frozen P09, R1 and R2 input inventories remain unchanged. Group 2 is incomplete.
Hardware-first and no-commit/no-push instructions remain in force.
