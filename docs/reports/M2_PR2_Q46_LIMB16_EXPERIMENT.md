# M2 PR2 bounded Q46 limb experiment

**READY FOR REVIEW — experiment complete; full renderer still fails resident fit.**
Baseline `8ee5214ea9c63b86e92ca9bc4fa0779115dbd57f`;
branch `codex/65aero-m2-pr2-renderer-fit`.
Founder authorized one private-helper experiment with exact equivalence,
unchanged compiler/flags/limits, before/after accounting and a stop after relink.
[Evidence](../evidence/flight-demo/2026-10-21-m2-q46-limb16/README.md).
The [prior generation-cache failure](M2_PR2_GENERATION_CACHE_GATE.md) and all
previous artifacts remain unchanged.

## Measured result

| Metric | Before | After | Change |
|---|---:|---:|---:|
| Private Q46 function | 1,157 bytes | 1,054 bytes | **103 fewer** |
| Entire text section | 33,036 | 32,933 | 103 fewer |
| Total resident span, including header/gaps/scratch | 36,394 | 36,293 | **101 fewer** |
| Resident end exclusive | `$AE2B` | `$ADC6` | 101 lower |
| Compiler resident scratch | 213 | 216 | 3 more |
| Alignment gap | 5 | 4 | 1 fewer |
| Read-only data / initialized data / BSS | 1,505 / 2 / 1,611 | 1,505 / 2 / 1,611 | unchanged |
| Remaining deficit below `$8000` | 11,819 | **11,718** | 101 fewer |
| Helper direct-call hardware stack, including entry return | 13 | 9 | 4 fewer |
| Helper dynamic software stack | 0 | 0 | unchanged |
| Conservative helper instruction upper bound | 15,562 | 16,299 | bound increases 737 |

The resident saving is `103 code + 1 alignment - 3 scratch = 101 bytes`.
The compiler, all flags, source list and link recipe are identical after
normalizing fresh output paths. Compiler SHA-256:
`cc557ae99a68ed36e098062b0f5376a878e94ac187b87446c8e603e4fb45a906`.
No helper is removed from the accounting merely because shared runtime code
remains linked elsewhere. There is no full-fit PASS or performance-improvement claim.

## Scoped implementation and arithmetic proof

Only production change: `src/graphics/m2_q46_private.h`.
Three test files provide retained-implementation comparison, the independent
integer oracle and test-only observations of actual intermediate cells/carries.
The observer is absent from the target compilation. No public ABI, signatures,
generated layouts, numeric scales, envelopes or memory ownership change.

Magnitudes remain bounded by `2^46`, as in the prior private contract. Each is
split into three 16-bit words. A fixed three-by-three schoolbook loop retains
the entire product in six 16-bit words; no intermediate product bit is discarded.
For every multiplication cell:

`65535*65535 + 65535 existing-word + 65535 carry = 4294967295`.

Thus each cell fits uint32, its stored low word fits uint16 and the next carry
is at most 65535. Induction over each row establishes the full unbounded product.
The final carry slot was untouched by earlier rows. All indices are within the
three input/six result words. Full product storage also handles valid products
above 64 bits, including `2^46 * 2^46`.

The exact quotient after shifting by 46 is assembled from product words 2–5.
Bit 45 determines whether the remainder is at least one half, including exact
ties; adding that bit then restoring sign gives nearest/ties-away rounding.
The rounded magnitude is at most `2^46`, so signed narrowing/negation are safe.
Negative extrema here mean `-2^46`, the contract minimum. Out-of-contract int64
extrema are not newly admitted, saturated or silently assigned semantics.

Before target relink:

- **217,091 ASan/UBSan cases** agree with both the archived original ratio C
  implementation and the retained 23-bit-limb Q46 implementation.
- **102,213 independent unbounded-integer cases** pass: signed domain extremes,
  split boundaries, rounding ties and neighboring values, seeded cases, long
  carry chains and products beyond 64 bits.
- **919,917 actual intermediate carry states** match independently calculated
  full-integer partial products. 903,210 carry states are nonzero; largest observed
  cell is 4,294,967,294, within the universal bound above. No unsigned wrap is
  needed to obtain the correct result.

## Compiler, stack and conservative cost

The emitted Q46 helper has 526 instruction locations versus 562 before.
It calls the 32-bit multiplication routine nine times and zero-fills 12 result
bytes once. The prior helper has four source products and four corresponding
64-bit runtime multiplication calls. The shared arithmetic
runtime remains reachable from other geometry operations and is still charged.

The existing fail-closed stack checker was applied to each helper's complete
direct-call closure (including multiplication/zero-fill callees), producing the
13-to-9 hardware-stack comparison above. It includes the helper entry return
address, but excludes its callers, IRQ/NMI and exercised high-water. Dynamic
software adjustments are zero in both closures. The composed artifact's compiler
scratch is counted separately once in resident `.noinit`, not added again as
software stack. Complete renderer stack/ABI admission remains unresolved.

A separate conservative instruction-work bound counts every instruction in each
routine at a safe maximum visit multiplicity, plus all bounded callee work:

- Before: `562 + 4*150*25 = 15,562`. The helper is acyclic; each runtime multiplier
  has at most 24 significant operand bits (23-bit limbs/high limb at most 2^23).
- After: `526*12 + 9*64*17 + 15*13 = 16,299`. The busiest inner-loop guard has at
  most 12 visits; nine multipliers receive uint16 operands (at most 16 shift
  iterations); the zero-fill writes 12 bytes.

These are deliberately loose structural upper bounds with full callee
instruction work included. Different overcounts mean the larger new bound
establishes neither an actual speed regression nor an improvement. They are
**not CPU-cycle WCET**: cycle timing, wait states, clock/interrupt overhead and
full dispatcher return margins remain unproven. No target service budget is
admitted or increased; the unchanged guard still denies unknown/zero budgets.
Reproduce this read-only analysis with:
`python3 -B docs/evidence/flight-demo/2026-10-21-m2-q46-limb16/analyze.py`.

## Checks and exact identities

- Proof output: `build/flight-demo/m2-limb16-proof-1792626239681145000/`.
  Exact compiler/runner commands, old helper bytes and inputs are retained.
- `python3 -B tools/flight_demo/m2_full/renderer_build.py`:
  `build/flight-demo/m2-renderer-1792626267808959000/`.
  Three generated-contract tests and renderer host ASan/UBSan PASS;
  compile/link and cache layout assertions PASS; resident fit FAIL.
  All five completed host images are byte-identical to the previous artifact.
- `python3 -B tools/flight_demo/m2/build.py`:
  `build/flight-demo/m2-pr1-1792626267805790000/`.
  Five contract tests, host/sanitizer/replay, 3,857 independent Decimal oracle
  and 841 near/far cases PASS. Error bounds are unchanged. Standalone target
  compile/link/static checks PASS; this probe's hardware stack is 24 (before 28),
  dynamic software 0 (before 0), compiler scratch 472 (before 468). These are
  standalone-probe figures, not renderer stack admission.
- Corpus/ledger/scope, whitespace, exact input identities, preservation and
  evidence inventories PASS. The older standalone input inventory is supplemented
  with the new private header's exact hash without rewriting its report.

Before target SHA-256:
`87d2a64bc3d536daecbaaac977eb543e92be23093ec80c17ae343487570af583`.
After target SHA-256:
`1d4605236b408b1273fee14c915ae85e1779c6b9bc752dbbb1b9f0a0f15940a9`.
Raw PRG/ELF identities remain in their original fresh output directories; maps,
symbols, disassembly, logs, source snapshots and comparisons are retained in the
new packet. The oversized artifact is not admitted for execution.

## Preservation and stop

Renderer continuations, the 289-in-320 cache and its lifetime, generation
cancellation/invalidation, deadline guards, platform seams and all unrelated
repository paths remain byte-identical. No registers/clobber convention,
CPU/physical owner ranges, MAP/base-page, DMA, timing budget or IRQ/NMI change.
No reserve use or memory-limit increase.

Implementation stopped after the target relink and immediate measured report.
Only read-only accounting, evidence retention and this handoff followed.
No anchor/cache refactoring, further arithmetic experiments, speculative
optimization, publication or target execution. No Xemu, D81, SD or physical
hardware testing. Review this exact 101-byte saving; the 11,718-byte resident
deficit and all runtime/display admission obligations remain open.
