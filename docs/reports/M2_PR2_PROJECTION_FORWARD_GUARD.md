# M2 PR2 bounded local-forward guard correction

**READY FOR REVIEW — bounded size PASS; full resident fit still FAIL.**
The one authorized composed relink uses **34,149 resident bytes**, saving
**72 bytes against the 34,221-byte reference** and **384 bytes against the
failed projection candidate**. It remains **9,574 bytes over** the unchanged
`$8000` ceiling, ending at **`$A566`**. Implementation and target builds stopped
after this relink. Only read-only accounting and this handoff followed.

## Authority, source and contracts

The founder approved the read-only review's bounded local-forward guard fix,
frozen checks and one relink against the 34,221-byte reference. The
[task authority](../evidence/flight-demo/2026-10-21-m2-projection-forward-guard/authority.md)
records that exact scope. Work continues on
`codex/65aero-m2-projection-experiment`, based on
`9dae245314ddd41cceaa7c6c3e7fce90c564138e`. This is a correction on the current
focused branch, not a new main integration or publication task.

Inspected authority/contracts include CURRENT_STATE, WIP, the development
workflow, programming principles, C style, approved P1–P6 projection intent,
numeric/generated interfaces, full memory ledger, geometry, failed source,
retained build recipe, fixed comparison generator and recorded proof identities.
The inherited Main v1.8, Gameplay v1.2, Runtime v1.2 candidate (NOT FINAL),
Graphics v2.1 and Physics v4.1 authority remains unchanged.

The [source delta](../evidence/flight-demo/2026-10-21-m2-projection-forward-guard/guard-only.diff)
adds `const int64_t forward = points[end].v[0]`, checks `forward <= 0`, and uses
that scalar in the two `project_axis` calls inside the final endpoint loop.
The original two-endpoint positivity check, local `M2Line` and final output
publication remain intact. All bytes outside `m2_project_prepared` match the
reconstructed reference. Relative to the failed candidate, no other production
source changed. The failed source and prior WIP were saved before editing.

The outer check already excludes nonpositive forward coordinates; nothing
mutates either point before these pure by-value calls. The new local check
therefore preserves valid behavior while exposing positivity directly at each
call. Endpoint order, exact `-1/0/1` results, failure-output preservation,
same-pointer cases and supported overlap remain unchanged. All transformation,
clipping, rounding, narrowing and clamping arithmetic is frozen, including
Q46/Q24/Q16 precision. No public layout, signature, interface version, helper,
cache, continuation, generation cancellation, deadline guard or ledger changed.

## Target result and compiler effects

The retained reference was freshly identity-verified before this edit; it was
not rebuilt again. Its PRG remains
`98822933724ec7b373622445723fb18be2ebac7ca74947e9a046f8b41acb9c51`.
All 79 current inputs matched the recorded failed candidate before editing.
The final composed build changes only geometry among those inputs; the other
78, physical tools and command recipe remain exact. Fresh output paths are the
only replay substitutions. The standalone check retains its own standard flags.

| Allocation/result | Reference | Failed projection | Guard candidate |
|---|---:|---:|---:|
| Projection own code | 1,959 | 1,863 | 1,900 |
| `rounded_ratio` own code | 255 | 336 | 255 |
| `__divdi3` own code | 0 | 343 | 0 |
| `.text` | 30,806 | 31,134 | 30,747 |
| `.rodata` | 1,561 | 1,561 | 1,561 |
| `.data` | 2 | 2 | 2 |
| `.bss` | 1,611 | 1,611 | 1,611 |
| `.noinit` compiler scratch | 216 | 200 | 200 |
| BASIC header | 22 | 22 | 22 |
| Alignment gaps | 3 | 3 | 6 |
| **Resident span** | **34,221** | **34,533** | **34,149** |
| End exclusive | `$A5AE` | `$A6E6` | `$A566` |
| **Deficit under existing ceiling** | **9,646** | **9,958** | **9,574** |
| Reserve allocation | 0 | 0 | 0 |

The guard costs 37 own projection bytes against the failed candidate, but
recovers the 81-byte `rounded_ratio` expansion and removes the 343-byte signed
wrapper. Text falls 387 bytes; the extra three alignment bytes make the net
saving 384. Against the original reference, text saves 59 and scratch saves
16, offset by three extra alignment bytes: **72 net**. Every other text-symbol
size matches the reference. In particular, accepted transform 985 bytes, its
56-byte table and Q46 helper 1,054 bytes are unchanged in size.

The emitted `rounded_ratio` again calls `__udivdi3` directly. No `__divdi3`
symbol remains. This confirms that the proposed local data-flow repair removes
the observed signed-division cost; it does not identify a particular optimizer
pass or establish execution-time improvement.

The [comparison record](../evidence/flight-demo/2026-10-21-m2-projection-forward-guard/comparison.json)
independently parses all ELF SHF_ALLOC sections, including zero-sized zero-page
sections, BASIC, gaps and compiler scratch. The root span is `$2001–$A565`;
above-ceiling placement is failed-fit diagnostic output, not an authorized
allocation. All owner sizes remain identical: renderer 846, core 64,
requested camera 22, snapshots 46, glyphs 472, and each opaque backend object.
The 289-byte cache, 320-byte HUD lifetime arrangement, display bands, hardware
stack/base-page bands and 4 KiB software-stack envelope remain fixed.

Compiler/flags are unchanged: LLVM-MOS SHA-256
`cc557ae99a68ed36e098062b0f5376a878e94ac187b87446c8e603e4fb45a906`,
`-mcpu=mos45gs02 -mlto-zp=0 -DM2_TARGET_LAYOUT_CHECK=1 -Oz
-fno-inline-functions -fno-jump-tables -Wall -Wextra -Wconversion -Werror`.
The opaque backend retains `-fno-lto` and its existing omission of `-mlto-zp=0`.
All source, tool, PRG, ELF and backend identities are retained in the packet.

Candidate PRG SHA-256:
`72fd75a63771794a0f1936f92289cac612db149317781ab5646756a8045aa94d`.
Candidate ELF SHA-256:
`81fbae03f52e8548e8b3a9c304807c969f96097611dc1d6888993c344609c5d2`.
The raw artifacts remain in the new ignored build directory recorded in the
comparison; no old output was overwritten.

## Frozen checks and remaining proof limits

| Check | Result |
|---|---|
| Fixed old/new comparison, ASan/UBSan, unchanged `-O2`/warnings | PASS 799,886 cases +34 contract checks |
| Canonical / seeded / analytic cases | 599,760 / 200,000 / 126 |
| Visible / clipped / same-pointer cases | 100,058 / 699,828 / 18 |
| Independent Decimal geometry oracle | PASS 3,857 cases; maximum error 0.000021225 pixel |
| Near/far regressions and sanitized replay | PASS 841 cases; maximum error 0.035137 pixel |
| Renderer contract, cache, generation, cancellation/fault and dispatch checks | PASS, including 600-tick replay |
| Completed host images | Five byte-identical to reference |
| Standard standalone target compile/link/static | PASS |
| Single composed target relink | Compile/link PASS; bounded size PASS; full resident fit FAIL |

The comparison reuses the exact frozen 44,793,616-byte corpus, SHA-256
`92c334a7812dabafe70ccef7ab8703db424c15ef1f312c56fd314bf36f90a8d5`.
The generator, seed 650017, original reference function and focused C test
remain unchanged and were hash-verified before execution. No cohort, oracle,
tolerance, compiler flag or failure expectation changed. Existing accepted
arithmetic/carry and transform proofs remain pinned; those unchanged large
suites were not rerun.

Commands include the recorded frozen host compile and executable invocations,
`python3 -B tools/flight_demo/m2/build.py`, and the exact composed recipe split
into `run_recipe.py host` and one `run_recipe.py link --output ...` invocation.
The [command record](../evidence/flight-demo/2026-10-21-m2-projection-forward-guard/commands.json)
links every argv, log and exit. The composed wrapper exits 1 because full fit
still fails; each actual compiler/linker/tool command exits 0. No second
candidate or composed relink occurred.

The standalone probe has a passing 20-byte hardware stack bound including entry
return, zero dynamic software bytes, 497 resident scratch bytes, and resident
end `$6300`. It is distinct from the composed artifact's 200-byte scratch.

The unchanged stack checker still reports `UNPROVEN: unrecognized instruction:
bit` in frozen `interpolate_delta` for both reference and guard projection
closures. Both roots retain the syntactic 8-byte constant software-frame
allocation/deallocation, with no other closure software-SP writes. No relaxation
of the checker or integrated stack PASS is claimed. Projection/caller/renderer
hardware stack and IRQ/NMI composition remain unresolved.

[Read-only static accounting](../evidence/flight-demo/2026-10-21-m2-projection-forward-guard/static-analysis.json)
includes all direct calls, tail jumps and cross-routine branches. The signed
wrapper is absent. Frozen source-operation maxima remain 18 Q46 products,
12 plane distances, 18 coordinate interpolations, 1,152 interpolation bit steps,
2,304 subtraction tests and four projected coordinates/divisions. Loose emitted
instruction bounds are 4,446,090 reference and 4,437,026 candidate, overcounting
alternative paths. These are not cycles, measured speed, WCET or 100 Hz service
admission. Unknown service budgets stay zero. Runtime/display gates are not
reached while full fit fails.

## Preservation and handoff

[Preservation](../evidence/flight-demo/2026-10-21-m2-projection-forward-guard/preservation.json)
checks all 15,636 pre-task current paths: 15,634 are unchanged, and the only two
authorized changes are geometry and WIP, each backed up before editing. New
paths are this report and this correction's packet. The failed projection
report, source snapshot, evidence and raw artifact identities remain intact.
Original checkout 15,731 paths and prior transform checkout 15,536 paths are
unchanged, including all 20 unrelated entries. All 13 predecessor flight packet
inventories verify. Generated files and memory ledgers remain identical to HEAD.

Graphics retains ownership of temporary state; CPU-visible resident usage and
compiler scratch are charged above. No public ABI, physical allocation, hardware
register access, MAP/base-page setup, DMA, IRQ/NMI, assembly, cache lifetime or
timing/deadline contract changed. Compiler clobbers and work cost can change with
emitted code; the outstanding integrated stack/timing boundaries remain explicit.

Review this correction as a **72-byte partial size improvement**. The 9,574-byte
full-renderer deficit remains unresolved. No further optimization, runtime/display
admission, target execution, Xemu, D81, SD, physical testing, commit, push, PR or
merge was performed or authorized by this task.
