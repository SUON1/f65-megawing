# M2 PR2 bounded transform-sequence experiment

**READY FOR REVIEW — bounded experiment complete; full resident fit FAIL.**
Verified main baseline `b3406ed8b9e141b50ca7ea7d3b5edd169c1ae310`;
branch `codex/65aero-m2-transform-experiment`.
The founder approved S1–S6 in the
[Build Intent](../plans/65AERO_M2_PR2_DEFICIT_BUILD_INTENT.md): reconstruct the
pinned reference, implement one compact transform candidate, run the specified
checks and stop after its relink. No publication or execution is authorized.
[Fresh evidence](../evidence/flight-demo/2026-10-21-m2-transform-sequence/README.md).

## Immediate relink result

| Metric | Reconstructed reference | Candidate | Change |
|---|---:|---:|---:|
| `m2_transform` code | 3,112 | 985 | 2,127 fewer |
| Private descriptor table | 0 | 56 | 56 more |
| Entire text | 32,933 | 30,806 | 2,127 fewer |
| Read-only data | 1,505 | 1,561 | 56 more |
| Initialized data / BSS | 2 / 1,611 | 2 / 1,611 | unchanged |
| Compiler resident scratch | 216 | 216 | unchanged |
| BASIC header / alignment gaps | 22 / 4 | 22 / 3 | one fewer gap byte |
| Total resident span | 36,293 | **34,221** | **2,072 fewer** |
| Resident end exclusive | `$ADC6` | **`$A5AE`** | 2,072 lower |
| Deficit above unchanged `$8000` ceiling | 11,718 | **9,646** | 2,072 lower |
| Transform-call-closure hardware stack | 15 | 15 | unchanged |
| Transform-call-closure dynamic software adjustment | 0 | 0 | unchanged |
| Conservative transform instruction-work bound | 248,945 | 256,796 | loose bound rises 7,851 |

The resident saving is `2,127 code - 56 table + 1 alignment = 2,072 bytes`.
No shared runtime code is omitted from the bill. Compiler scratch is charged
once as resident `.noinit`; it is not added again as dynamic software stack.
The admitted resident span remains 24,575 bytes (`$2001–$7FFF`), with no reserve
or memory-limit increase. Above-ceiling addresses describe failed diagnostic
placement; this target must not execute.

Implementation stopped at this candidate relink and the result was reported
immediately. Subsequent activity was read-only accounting and evidence/handoff
retention. No second candidate or additional build followed.

## Reference integrity and scoped change

The original development checkout was not used as a source overlay. A fresh
worktree from verified main restored only the 16 hash-pinned paths in the
[reconstruction manifest](../plans/65AERO_M2_PR2_DEFICIT_RECONSTRUCTION.json).
All 79 recorded input hashes, tool hashes, owner symbols and sections match the
retained Q46 composition. The reconstructed PRG is byte-identical to that
artifact; the known 11,718-byte reference fit failure was preserved as required.
Restoration supplies experiment scaffolding, not acceptance of renderer/cache
runtime code into main.

Relative to that reconstructed reference, the only production change is the
body of `m2_transform` in `src/graphics/m2_geometry.c`. The other 78 recorded
inputs are unchanged. This includes the accepted Q46 helper, clipping and
projection routines, renderer/cache/dispatch, platform source, generated records
and memory ledgers. The original full reference function and exact candidate
source are both retained in the new evidence packet.

The candidate uses six bounded sine evaluations and a fixed fourteen-entry
private operation table. The first two products retain the separately rounded
roll/pitch intermediates; the remaining twelve retain every original product
and signed addition/subtraction. All nine coefficients are assigned before the
final result copy. No rounding stages are fused or reordered algebraically.
The table occupies 56 actual linked read-only bytes, private to Graphics.

Table operands are read only after definition: slots 0–5 hold sine/cosine inputs,
slots 6–7 are assigned by the first two operations, and subsequent operations
read only those eight slots. Coefficient 2 is assigned directly; every other
coefficient receives a SET before any ADD/SUB. Source and destination indices
remain within the declared private arrays. Each rounded product has magnitude
at most `2^46`; each two-term sum/difference fits signed int64. Exhaustive
comparison also confirms every final coefficient remains within `±2^46`.

## Numerical and host checks before candidate relink

- **5,270,760 angle triples**: ASan/UBSan exact comparison to the archived
  expression function across yaw 0–359 and pitch/roll -60–60. This reference
  shares only unchanged validation/sine/Q46 primitives, which have independent
  coverage. It does not interpret the candidate table.
- **33 boundary cases**: null/invalid camera, revision, angle and position
  extrema with unchanged failure outputs; additional null-output and same-object
  prepare/registration alias checks pass. Camera fields are compared without
  depending on native padding bytes.
- **63,560 independent unbounded-integer matrix cases**: canonical generated
  sine inputs with independently written staged equations; 42,619 half ties,
  387,684 negative products, 838,025 products above 64 bits, 110,092 opposite-sign
  term cancellations and 453 coefficient extrema. No nonzero-term exact-zero
  cancellation occurred in this corpus; this count is not claimed otherwise.
- **217,091 frozen Q46 equivalence comparisons**, **102,213 independent integer
  product cases** and **919,917 carry-state checks** pass unchanged.
- `python3 -B tools/flight_demo/m2/build.py`: host/sanitizer, all **3,857 Decimal
  oracle** and **841 near/far** cases, and standalone target compile/link/static
  checks pass. This separate probe reports hardware stack 21, dynamic software
  adjustment 0 and compiler scratch 512 bytes. These are probe-specific figures,
  not the composed artifact's 216-byte scratch charge or runtime admission.
- The exact retained renderer recipe's host/contracts phases pass. All five
  host PPM images are byte-identical to the reconstructed reference, including
  the cache/cancellation/failure behavior covered by the unchanged host suite.

Exact commands/logs are retained in `01-transform-proof/`, `02-q46-proof/`,
`03-standalone/` and `04-candidate/`. Host results establish their own tier.
No target binary was executed.

## Compiler, ABI, stack and work cost

The composed recipe is byte-identical after fresh output-directory substitution.
The same opaque non-LTO backend, source list, `-mcpu=mos45gs02`, `-mlto-zp=0`,
`-Oz`, `-fno-inline-functions`, `-fno-jump-tables` and warning flags are retained.
Compiler SHA-256 remains
`cc557ae99a68ed36e098062b0f5376a878e94ac187b87446c8e603e4fb45a906`.
Objdump, nm and host compiler hashes also match the reference.

The public function signature/layouts are unchanged. New emitted code uses a
single repeated product call-site and one 72-byte `memcpy` for result publication;
the original result stores were emitted inline. `memcpy` was already linked by
other users, so the entire text reduction equals the transform reduction.
The compiler preserves the callee-saved pseudo-registers it uses; no handwritten
register/clobber contract is introduced. Static compiler-frame reuse retains
the existing exclusive, non-reentrant Graphics calling context.

The existing fail-closed stack checker covers the entire transform closure,
including tail jumps, sine remainder helpers, Q46/multiplication/zero-fill and
the candidate's copy routine. Both closures require **15 hardware bytes including
the transform entry return**, with zero dynamic software adjustment. This excludes
callers, IRQ/NMI, target high-water and complete renderer/platform ABI admission.

The retained conservative instruction-work formulas include full bounded callee
work. The reference's own 1,345 instruction locations are acyclic. The candidate
has 506 locations with six sine and fourteen product iterations (at most fifteen
guard visits), plus the separately bounded 72-byte copy. Both execute fourteen
Q46 operations and six sine evaluations. The 16-bit remainder uses at most
sixteen alignment and sixteen restoring shifts; every helper is charged.

These deliberately loose bounds rise from 248,945 to 256,796. Different path
overcounts mean this establishes neither an actual speed regression nor an
improvement. CPU-cycle WCET, wait states, interrupt overhead and dispatcher
return margins remain unproven. No service budget is admitted or increased;
unknown/zero bounds continue granting no renderer work.
Reproduce read-only accounting with
`python3 -B docs/evidence/flight-demo/2026-10-21-m2-transform-sequence/analyze.py`.

## Artifact identities and preservation

Reference PRG SHA-256:
`1d4605236b408b1273fee14c915ae85e1779c6b9bc752dbbb1b9f0a0f15940a9`.
Candidate PRG SHA-256:
`98822933724ec7b373622445723fb18be2ebac7ca74947e9a046f8b41acb9c51`.
Raw PRG/ELF files remain in the fresh build directories recorded in the packet;
maps, symbols, disassembly, logs, source and comparison identities are retained.

All 15,731 original-checkout files and the 20 unrelated untracked entries remain
unchanged. Every existing flight-demo packet inventory passes. No historical
source, report, carrier or generated contract was rewritten. The restored font's
original whitespace is preserved as part of the exact reference, not restyled.
New proof/tooling sources and this report are the only additional experiment
material beyond the explicitly authorized reconstruction and transform change.

No new hardware accesses, MAP/base-page or DMA changes, IRQ/NMI handlers,
persistent-state changes, precision reductions, memory expansion or reserve use.
The 289-byte cache/320-byte workspace lifetimes, generation cancellation and
deadline guards remain unchanged. Display mapping/admission is not reached.

Stop at this failed full-fit gate. Review the exact 2,072-byte saving and
remaining 9,646-byte deficit before deciding any next work. No further
optimization, Xemu, D81, SD, physical testing, commit/push/PR/merge or milestone
progression occurred.
