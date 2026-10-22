# M2 PR2 prepared-projection compaction experiment

**READY FOR REVIEW — bounded size gate FAILED.** The one approved candidate
increases resident usage by **312 bytes**, leaving **9,958 bytes over** the
unchanged `$8000` ceiling. Implementation stopped immediately after its composed
relink. Do not adopt this candidate as a size improvement. A further proposal
requires separate review; no second candidate or helper rewrite was attempted.

## Authority and exact scope

The founder approved P1–P6 in the
[projection Build Intent](../plans/65AERO_M2_PR2_PROJECTION_BUILD_INTENT.md).
The retained planning file's pending status is provenance; the current prompt
supplies implementation authority. Fresh fetch, GitHub main and exact-main CI
verified `9dae245314ddd41cceaa7c6c3e7fce90c564138e` before creating
`codex/65aero-m2-projection-experiment` in
`/private/tmp/f65-m2-projection-experiment`.
[Exact-main CI](https://github.com/SUON1/f65-megawing/actions/runs/39715650122)
passed. No commit, push, PR or merge was authorized or performed.

The workflow, programming principles and C standard were inspected, along with
the controlling corpus and approved predecessor authority carried by the intent,
`interfaces/m2_pr1.json`, `interfaces/m2_full.json`,
`memory/m2-full-ledger.json`, generated headers, geometry, fixture, renderer,
private prepared context, camera and validation tooling.

The [reconstruction manifest](../plans/65AERO_M2_PR2_PROJECTION_RECONSTRUCTION.json)
restores 16 pinned paths from retained snapshots. All 79 reference inputs match.
This scaffolding includes unmerged renderer/cache/dispatch code and its private
owner comparison; it is not accepted runtime/display implementation. Against
that exact reconstructed reference, the **only production change is the body
of `m2_project_prepared`**. Fifteen other restored paths remain exact, and 78/79
composed build inputs are unchanged. Helpers, accepted transform/Q46, raster
cursor, cache, continuations, generation cancellation and deadline guards are
byte-identical. No public/generated declaration, interface version or ledger
changed. `CURRENT_STATE.md` remains unchanged.

## Implementation and arithmetic

Two indexed private `ClipPoint` records retain endpoint order. Bounded endpoint
loops share transformation and distance setup; the final loop still projects
`x[0], y[0], x[1], y[1]` in that order into a local result. It does not flatten
public fields. Both transformations finish before any caller output is written.

For each plane, both distances are calculated before mutation. Both-outside and
sign-crossing tests are unchanged. When signs cross, `outside` is 0 or 1 and
`inside = outside ^ 1`; numerator is the nonnegative inside distance and
denominator is inside minus outside distance. These are the exact previous
values. They stay fixed through the three coordinate updates. The inside point
is immutable; each updated outside coordinate reads its own prior value, so no
update changes a later axis's delta. The formula, Q24 interpolation, Q46
transformation, six-plane order, near/far handling, positive-forward guard,
Q16 output/clamping and failure publication behavior are unchanged.

Endpoint validity and guard ordering remain exact. Successful output assignment
occurs after all input reads, preserving the tested input/output overlaps.
Same-pointer endpoints remain legal. The tests avoid fabricated matrices or
private-context states outside the successful-prepare contract.

## Actual composed accounting

The fresh reference exactly reproduces retained PRG
`98822933724ec7b373622445723fb18be2ebac7ca74947e9a046f8b41acb9c51`,
including all sections, owner sizes/addresses and physical tool hashes.
Recipe normalization covers only fresh checkout tool paths and output paths.
Its wrapper exits 1 for the already-known fit failure; every underlying
compile/link/host command exits 0.

| Allocation or result | Reference | Candidate | Change |
|---|---:|---:|---:|
| `m2_project_prepared` own code | 1,959 | 1,863 | -96 |
| `.text` | 30,806 | 31,134 | +328 |
| `.rodata` | 1,561 | 1,561 | 0 |
| `.data` | 2 | 2 | 0 |
| `.bss` | 1,611 | 1,611 | 0 |
| `.noinit` compiler scratch | 216 | 200 | -16 |
| BASIC header | 22 | 22 | 0 |
| Alignment gaps | 3 | 3 | 0 |
| **Total resident span** | **34,221** | **34,533** | **+312** |
| Allowed span `$2001–$7FFF` | 24,575 | 24,575 | 0 |
| End exclusive | `$A5AE` | `$A6E6` | +312 |
| **Remaining resident deficit** | **9,646** | **9,958** | **+312** |
| Reserve allocation | 0 | 0 | 0 |

The [comparison](../evidence/flight-demo/2026-10-21-m2-projection-sequence/comparison.json)
independently parses every ELF SHF_ALLOC section, including zero-sized
`.zp.data`/`.zp.bss`, BASIC and scratch; summing them plus gaps reproduces the
span. All owner object sizes are unchanged, including renderer 846 bytes,
requested camera 22, core 64 and snapshots 46. Their addresses relocate with
text. The existing 289-byte cache and 320-byte HUD lifetime arrangement is
unchanged. Scratch is charged once as resident allocation, separately from
dynamic software and hardware stacks. Above-ceiling addresses are failed-link
diagnostic placement, not approved allocations or reserve use.

Only three text-symbol sizes change:

| Symbol | Before | After | Delta |
|---|---:|---:|---:|
| Projection body | 1,959 | 1,863 | -96 |
| `rounded_ratio` | 255 | 336 | +81 |
| New `__divdi3` compiler helper | 0 | 343 | +343 |
| **Text total** | | | **+328** |

The `rounded_ratio` C source is frozen. Its reference machine code uses
`__udivdi3`; the candidate machine code uses the signed `__divdi3` wrapper, which
calls the existing unsigned division routine. The changed context loses the
reference's emitted unsigned-only form. This observable compiler effect accounts
for all added text; no claim is made about a uniquely identified optimizer pass.
Every other text-symbol size is unchanged. The accepted 985-byte transform,
56-byte descriptor table and 1,054-byte Q46 helper are unchanged in size.

The composed target uses the unchanged LLVM-MOS compiler and flags:
`-mcpu=mos45gs02 -mlto-zp=0 -DM2_TARGET_LAYOUT_CHECK=1 -Oz
-fno-inline-functions -fno-jump-tables -Wall -Wextra -Wconversion -Werror`.
The opaque backend retains `-fno-lto` and omission of its inapplicable LTO option.
Compiler SHA-256 is
`cc557ae99a68ed36e098062b0f5376a878e94ac187b87446c8e603e4fb45a906`.
All compiler, objdump, nm, host compiler, source and recipe identities are in
the evidence. No compiler/ABI configuration changed; the extra signed-division
callee and changed scratch are charged as emitted effects.

Candidate PRG SHA-256:
`5001b3ee71e0843b191f5fa818fe5305d34340f42a3d2e93aa6a531641e3be7a`.
Candidate ELF SHA-256:
`82c1ced0dfabb92f503e944d3a7fa8b066bbfa3568cfae5ae7d3e7ea198703b8`.
Raw paths, byte sizes, reference ELF identity and backend identities are in
`comparison.json`; separate fresh build directories retain the binaries.

## Validation and work/stack limits

[Exact command ledger](../evidence/flight-demo/2026-10-21-m2-projection-sequence/commands.json)
and archived build records retain the commands and exits:

| Check | Result |
|---|---|
| Exact reconstructed reference | PASS identity; expected resident fit FAIL |
| New old/new comparison, `-O2`, ASan/UBSan, warnings as errors | PASS 799,886 cases |
| Canonical fixture / seeded / analytic counts | 599,760 / 200,000 / 126 |
| Visible / clipped outputs, every field and return status | 100,058 / 699,828 exact |
| Same-pointer degenerate cases | 18 exact |
| Additional null/readiness/bounds/output/alias checks | 34 PASS |
| Standalone `python3 -B tools/flight_demo/m2/build.py` | PASS host/oracle/target compile-link-static |
| Independent Decimal quaternion/parametric oracle | 3,857 PASS; maximum error 0.000021225 pixel |
| Near/far regressions and sanitized clipping replay | 841 PASS; maximum error 0.035137 pixel |
| Renderer host contract and generation/cache/dispatch checks | PASS, including cancellation/faults, label permutations and 600-tick replay |
| Five completed renderer images | Byte-identical to fresh reference |
| Single candidate composed target relink | Compile/link PASS; bounded size gate FAIL |

The corpus generator, Python 3.9.6 identity, seed 650017, exact draw order and
reference function were frozen before the production edit. The corpus contains
44,793,616 bytes, SHA-256
`92c334a7812dabafe70ccef7ab8703db424c15ef1f312c56fd314bf36f90a8d5`.
It covers public integer-Q12 bounds without filtering/retries. C checks every
canonical segment against Environment's actual fixture function. Every
unsuccessful comparison preserves sentinel output. Accepted arithmetic/carry
and exhaustive transform proofs were hash-verified with historical inventories;
their implementations are unchanged, so those large suites were not rerun.

The standalone probe passes the unchanged fail-closed stack checker: hardware
20 bytes including entry return, dynamic software 0, resident compiler scratch
497 bytes. Its resident end is `$6488`. The retained pre-candidate transform
probe had 21/0/512 bytes respectively; this historical probe comparison is
separate from the fresh composed reference/candidate accounting.

For **both composed projection closures**, the unchanged checker reports
`UNPROVEN: unrecognized instruction: bit` in frozen `interpolate_delta`.
The complete read-only closure includes direct calls, tail jumps and cross-routine
branches, including the candidate's signed wrapper. It is preserved in
[static analysis](../evidence/flight-demo/2026-10-21-m2-projection-sequence/static-analysis.json).
No checker relaxation or replacement proof was used. Both emitted roots have
the same syntactic 8-byte software-frame allocation/deallocation; no other
software-SP writes occur in the reachable closure. This observation does not
turn the rejected integrated stack proof into PASS. Composed hardware-stack
and full renderer/caller/IRQ/NMI bounds remain unproven. The previous transform
closure's 15-byte result is not a projection or whole-renderer bound.

Conservative source-operation maxima per projection are unchanged: 2 endpoint
transforms, 18 Q46 products (162 limb products), 12 plane distances, 18 coordinate
interpolations, 1,152 interpolation bit steps, 2,304 subtraction tests and four
projected coordinates/divisions. Read-only emitted instruction inventories with
uniform loop overbounds give **4,446,090 reference** and **4,437,462 candidate**
instructions per call. These deliberately loose structural bounds include all
helper/tail-call work, shifts, division and copies; mutually exclusive paths are
overcounted. They are not measured speed, cycle WCET, wait-state, interrupt or
100 Hz service proof. Unknown service budgets remain zero; no expensive work is
newly admitted. Full fit, runtime/display mapping and timing gates are not reached.

## Preservation, effects and handoff

[Preservation](../evidence/flight-demo/2026-10-21-m2-projection-sequence/preservation.json)
verifies all 15,731 recorded paths in the original checkout and 15,536 in the
prior transform checkout, with identical path sets and contents. The 20
unrelated entries are unchanged. All 12 historical flight-evidence inventories
pass, and generated files and memory ledgers are identical to main. All failed
and successful historical artifacts remain untouched. New evidence records the
reference-verification schema/path normalizations and preliminary read-only
analysis assertions corrected from actual emitted frame instructions.

Changed task paths comprise this report, WIP, the retained approved planning
documents, focused comparison generator/test, new evidence packet, and the 16
exact reconstruction paths (geometry then receives the single candidate body).
The restoration manifest distinguishes scaffolding from the candidate delta.
The source snapshots and pre-edit freeze make that distinction independently
reviewable. No original working path was modified.

Graphics owns all temporary clipping state. No persistent state or workspace
reuse changed. Compiler register saves, ABI helper calls, resident scratch and
instruction effects are recorded above; public ABI and precision are fixed.
Registers/hardware access, physical allocations, MAP/base-page setup, DMA,
IRQ/NMI and platform contracts are unchanged and not applicable to this pure-C
edit. CPU-visible failed resident placement is reported explicitly. No new
handlers, assembly or reserve use occurred.

**Recommended review disposition:** retain the experiment as a failed bounded
result and keep the accepted reference as the engineering baseline. Review the
emitted compiler effect before authorizing any next proposal. No anchor/cache
refactoring, helper rewrite, further optimization, target execution, Xemu, D81,
SD or physical test, publication or later milestone follows this result.
