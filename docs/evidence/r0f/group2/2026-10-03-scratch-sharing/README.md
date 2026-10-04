# R1 scratch sharing — bounded host and fit PASS

2026-10-03. Owner “Build it” authorized the first bounded implementation in
[the redesign](../../../../plans/R0-F_GROUP2_SIZE_CAPTURE_REDESIGN.md).
This is not complete Group 2, a runnable carrier, runtime acceptance or a
measured-limit approval. No target execution, Xemu, D81, SD operation, physical
run, commit or push occurred.

## Identity and measured result

Fresh candidate: `build/r0f/group2/scratch/r1-j52fobh4`.
It copies the hash-verified minimal admission at
`build/r0f/group2/target-admission/queue-ceu0y7ys`, itself derived from frozen P09.
PRG SHA-256: `3d27f986f8cf7fe2b9d4b511f783e4ac5eea4b8610252ec5f1666d2deb29d5c5`.
Its source is the copied `source-inputs`, not the older root working target.
The PRG remains a compile-only minimal queue admission, not a suite candidate.

| Quantity | Admission | R1 | Change |
| --- | ---: | ---: | ---: |
| Resident exclusive end | $C16F | $BF62 | -525 bytes |
| Margin below $C000 | -367 | 158 | +525 |
| Text | 32847 | 32832 | -15 |
| BSS | 3406 | 2896 | -510 |
| Protected section | 4495 | 4495 | 0 |
| Compiler static stack (`.noinit`) | 36 | 36 | 0 |
| Read-only data / data | 497 / 23 | 497 / 23 | 0 |

The 15-byte text reduction is in LTO's `main` (9408 to 9393). Other function
sizes are unchanged; the private transport function's linker suffix changed
when the separate `transfer` data symbol disappeared. No new functions, local
arrays or calls were introduced by R1. Static-stack allocation is unchanged;
this is not independent runtime stack-high-water or timing qualification.

`source.patch` contains exactly three owner substitutions and the private
contract, generated header and ownership ledger. Capacities remain 255 for each
borrower. Public interfaces, protected source, hardware wrappers and all other
source inputs match admission. P09 frozen input hashes were checked again and
remain unchanged. Root target source and historical proof were not modified.

## Lifetime audit

| Owner / callers | Live interval and handoff proof |
| --- | --- |
| `cfrom_begin`, `cfrom_restore` | Readback occupies shared scratch only through byte comparison against the separate `block`. Subsequent physical CRC uses `block`. `cfline` occurs before readback and uses separate `block`; PF copies do not call C borrowers. Copy/compare failures return immediately. |
| `dos_crc` | Each chunk is initialized or read before CRC, consumed before the next chunk; returns a scalar checksum. Startup and storage orchestration invoke ROM/display/transport in separate completed calls. |
| `dos_copy` | Four live callers use physical-to-physical modes. Private local modes have no callers and carry no cross-call lifetime in this fixture; both remain tested and unchanged. Failure abandons scratch. |
| `display_seed_staging` | Fills scratch, copies all chunks synchronously, then returns. Both `display_begin` and `display_resume` consume physical staging afterward. Resume DMA reads staging, not scratch. |
| Terminal color block in `main` | After quiescence, fills scratch and copies synchronously; failure breaks the loop before `cfscreen`. Screen output uses separate platform `block`. |
| `validate_capsule` | Guards checked immediately; each context chunk consumed by CRC before next transfer. Returns only scalar status/retained CRC. |
| Trace read/write and prepare | Data callers use independent `record[92]`, `header[256]`, or automatic world `event[16]`; no shared-scratch alias. Writes finish before caller continuation; reads copy out before return. Prepare consumes trace bytes by CRC before reusing scratch for capsule validation. Export policy is pure and does not call another borrower. |
| IRQ/NMI | `qualification_45gs02.s` and `group1_irq_45gs02.s` handlers only use their private/protected state. Timing hooks call their own assembly reader, never C or shared scratch. NMI only records the sticky flag. |

All shared users run in synchronous foreground order. No callback acquires a
second borrower while bytes are live. Failure returns do not expose scratch as
persistent state. Existing fault writes, including their existing overwrite
behavior, are unchanged; R1 does not claim a new universal first-fault policy.
Future callbacks or local DOS modes used across calls require a new lifetime
review. `block`, capture record/header, protected context and all reserves stay
separate. PF request ownership, register ABI, base page 2, MAP, DMA and IRQ/NMI
semantics remain unchanged. Resident addresses and potentially timing change.

## Actual-owner host proof

Command that created the candidate and performed the sole target compile:

```text
python3 -B tools/diagnostics/r0f_group2_scratch.py
```

The initial host-only link failure is retained separately. It linked unrelated
integration tick instrumentation without its callbacks. The correction selects
the integration preprocessor path only in the owner-test translation unit;
actual range/CRC/export implementations link normally. No target compile was
performed for that failure.

Final extended verification, without recompiling or changing target inputs:

```text
python3 -B tools/diagnostics/r0f_group2_scratch.py --verify-host build/r0f/group2/scratch/r1-j52fobh4
```

**PASS: 1484 poisoned handoffs, ASan/UBSan, warnings treated as errors.**
`final-host/validation.json` retains exact compiler/run commands and exits. The host
executes exact extracted owner definitions and the exact terminal-color loop;
`final-host/actual_owners.h` retains what executed. Only physical memory, register
reads, screen text and ROM trap are simulated. PF request packing and owner
range checks execute, with alias-aware pointer resolution and ASan redzones.

Coverage: ROM source/readback separation and restore after unrelated scratch
users; early and middle ROM copy failures and readback corruption; all DOS copy
modes and every chunk failure; independent DOS checksum/pattern expectations;
staging and terminal color copies and every failure; capsule guard/context
corruption and every copy failure; trace lengths 1–255, last valid byte,
one-over/invalid ranges, failed writes and unchanged output on failed reads;
terminal preparation's trace-to-capsule handoff, every copy failure, bad CRC,
and existing-fault rejection without granting export permission.

This is function-level host proof, not emulation of the whole lifecycle or
hardware execution. ROM CRC-tail failure semantics were not redesigned or
exhaustively fault-swept. Existing integrity checks remain in exact copied
bodies; no new stronger claim is inferred from buffer sharing.

## Next gate

R1 recovers fit for the minimal probe only. The proposed 24-byte live capture
state would leave 134 bytes before any extra code, so full capture/suite fit is
still unknown. R2 request-encoding factoring is the next separately measured
increment; afterward admit the capture skeleton before adding case injectors.
All combined-runtime, stack high-water, timing, Xemu, carrier and physical gates
remain open for a complete successor. No P09 or earlier carrier was rerun.

The preceding extended host snapshot remains in `host/`; `final-host/` adds
explicit sequencing of DOS execution before independent expected CRC calculation.
Both pass; no additional target compile occurred.
