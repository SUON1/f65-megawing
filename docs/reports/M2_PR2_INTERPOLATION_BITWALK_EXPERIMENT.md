# M2 PR2 interpolation bit walk — failed prerequisite gate

**FAILED GATE — stopped for review; no candidate composed relink.**

I1–I6 were approved in the task prompt on 22 October 2026. The one permitted
source candidate and its numerical checks are complete. The required standalone
builder compiled and linked, then exited 1 because its unchanged stack checker
rejects emitted `BIT`. I5 requires stopping on an unexpected prerequisite failure.
No checker change, retry, second candidate or composed candidate relink followed.
This is a verifier coverage failure, not an observed arithmetic mismatch or a
proved stack overflow. The candidate is not approved for integration.

Branch: `codex/65aero-m2-interpolation-experiment` in
`/private/tmp/f65-m2-interpolation-experiment`. Main, fetched origin/main and
GitHub main were freshly verified at
`c6a41e0988a3e329f1b30f7d48c87d92e00b523b`;
[exact-main CI passed](https://github.com/SUON1/f65-megawing/actions/runs/39724644712).
The [approved intent](../plans/65AERO_M2_PR2_INTERPOLATION_BUILD_INTENT.md) retains
its historical planning status; the current task prompt supplies authority.

## Change and authority

The only candidate production difference from the reconstructed reference is
inside private `interpolate_delta` in `src/graphics/m2_geometry.c`: select the
unsigned magnitude's high bit, then advance it left by one unsigned bit after
the existing two subtraction tests. The loop still consumes all 64 positions.
Quotient/remainder arithmetic, rounding threshold, narrowing, sign restoration
and return remain byte-for-byte unchanged. See the exact
[candidate patch](../evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk/candidate.patch)
and [bit/state proof](../evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk/bit-state-proof.md).

Before editing, the governing numeric/public schemas, memory ledger, design
hierarchy, development workflow, programming principles, C style and I1–I6
contracts were inspected. Graphics retains private temporary arithmetic
ownership. Public/generated ABI, Q46/Q24/Q16 precision, world bounds, resident
ceiling `$8000`, 4 KiB software-stack envelope and zero reserve remain fixed.
Compiler register/flag clobbers, emitted code and scratch can change; no new
public calling convention is introduced. Dynamic stack safety is unproved at
the failed checker gate. Hardware register access, physical allocations,
MAP/base-page setup, DMA and IRQ/NMI behavior have no source changes and were
not exercised. No runtime deadline or service budget was admitted.

The 16 exact restorations are authorized reconstruction scaffolding, identified
separately in the [manifest](../plans/65AERO_M2_PR2_INTERPOLATION_RECONSTRUCTION.json).
They restore the previously retained full composition from main; they are not
new feature changes or acceptance of that composition. All other 78 reference
inputs remain exact, including renderer continuations, 17 cached segments,
four anchors, workspace lifetimes, cancellation/invalidation and deadline guards.
The accepted Q46, transform and local-forward projection correction remain exact.
Generated interfaces and memory ledgers are unchanged from main.

## Completed checks and first failure

| Check | Actual result |
|---|---|
| One fresh reference reconstruction/build | Exact 79 inputs, tools, recipe, PRG/ELF, sections and owner identities; known full-fit FAIL reproduced |
| Direct old/new/unbounded-integer helper comparison | PASS 457,334 cases, 228,430 negative; 12,012 ties in the frozen corpus; ASan/UBSan clean |
| Intermediate bit-state comparison | PASS 29,269,376 steps; inductive proof retained |
| Frozen projection suite | PASS 799,886 exact cases +34 contract checks; 18 same-pointer cases; ASan/UBSan clean |
| Standalone contract and host | PASS 5 contracts and 600 per-tick replay comparisons |
| Independent 60-digit Decimal oracle | PASS 3,857 cases; maximum projection error 0.000021225 pixels, below unchanged 0.5 limit |
| Independent near/far/reversed regressions | PASS 841 cases; maximum error 0.035137 pixels; sanitizer replay PASS |
| Standalone LLVM-MOS compile/link, objdump, nm | All completed, exit 0; target never executed |
| Required standalone stack gate | **FAIL** `ValueError: unrecognized instruction: bit`; builder exit 1 |
| Renderer host/contracts/images, run concurrently with standalone | PASS 3 contracts, generation/cache/workspace/dispatch/cancellation/failure checks, 600-tick replay and five byte-identical images |
| Composed candidate compile/link | **NOT RUN**, stopped at the first failed admission gate |

The new direct corpus uses the exact approved structured sets and
`Random(650018)` draw order, with 357,334 structured and 100,000 seeded cases.
The original helper was frozen before editing; expected results use independent
unbounded integer multiplication/division, not the C recurrence. Frozen corpus
SHA-256:
`d86ade1681153dca3ea00d72de2272b64c09bda5c5c16ce489194aa566132b37`.
Projection corpus identity remains
`92c334a7812dabafe70ccef7ab8703db424c15ef1f312c56fd314bf36f90a8d5`.
These valid-domain checks do not expand invalid-input or world admission.

In the standalone disassembly the rejected instruction is
`$463c: bit $5ab0 <__set_v>` in `main`, following a carry/shift sequence.
The checker at `tools/flight_demo/m2/stack_check.py:82` excludes `bit` from its
recognized instructions. Its source/hash is unchanged:
`4d344f815d246859b621caac01f2c9e27f1501ecec32c7f9491d7f2e427522ef`.
The failed builder never writes its success `build.json`; this absence is retained.
Later builder assertions were not reached. A separately labeled
[recovered command record](../evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk/03-standalone/recovered-command-record.json)
documents the unchanged recipe and existing logs without fabricating success.

## Exact accounting and its limits

The independently parsed fresh reference ELF reproduces the accepted composed
reference. There is **no after composed ELF**, so no composed helper size,
scratch, owner movement, savings or remaining candidate deficit can be reported.

| Composed resident item | Fresh reference | Candidate |
|---|---:|---|
| BASIC header | 22 | Not linked |
| Text | 30,747 | Not linked |
| Read-only data | 1,561 | Not linked |
| Initialized data / BSS | 2 / 1,611 | Not linked |
| Compiler scratch `.noinit` | 200 | Not linked |
| Alignment gaps | 6 | Not linked |
| Total span | **34,149** | **Unmeasured** |
| End exclusive | `$A566` | Unmeasured |
| Allowed span `$2001–$7FFF` | 24,575 | Unchanged |
| Last verified deficit | **9,574** | Unmeasured |
| `interpolate_delta` own code | 1,605 | Unmeasured |
| `__ashldi3` own code | 31 | Reachability unmeasured |

Reference PRG SHA-256:
`72fd75a63771794a0f1936f92289cac612db149317781ab5646756a8045aa94d`;
ELF SHA-256:
`81fbae03f52e8548e8b3a9c304807c969f96097611dc1d6888993c344609c5d2`.
Above-ceiling reference placement is failed-fit diagnostic evidence only.

The completed standalone link is a **different probe and compiler recipe**
(`-Os`, inlining allowed), not the full renderer's `-Oz`/no-inline composition.
Compared with the retained corrected-projection standalone artifact:

| Standalone resident item | Retained before | New candidate | Delta |
|---|---:|---:|---:|
| BASIC header | 22 | 22 | 0 |
| Text | 14,360 | 14,270 | −90 |
| Read-only data | 793 | 794 | +1 |
| Initialized data | 22 | 22 | 0 |
| BSS | 1,456 | 1,456 | 0 |
| Compiler scratch `.noinit` | 497 | 487 | −10 |
| Alignment gaps | 1 | 3 | +2 |
| Total resident span | **17,151** | **17,054** | **−97** |
| End exclusive | `$6300` | `$629F` | −97 |

All nonempty allocated standalone sections fit below `$8000`; zero-sized
`.zp.data`/`.zp.bss` remain at `$22`. Compiler scratch is charged once in the
resident span and is not a dynamic stack measurement. Interpolation is inlined
into `main`, so there is no independently sized standalone helper.
`__ashldi3` is absent from this probe's symbols. These observations do not
predict composed helper elimination or subtract 97 from the 9,574-byte deficit.
Standalone candidate PRG SHA-256 (15,113 bytes):
`622ff2318cdf7cee9cd3be721fabb118a56cf0929eb0fb58debcad6cd53fb88d`;
ELF SHA-256 (20,840 bytes):
`e23b9cf0ef77120d405a156835b99ab4c152cb5bc624035d0c44189c970c5f5b`.

The retained standalone checker proved 20 hardware bytes including entry return,
zero dynamic software bytes and 497 resident scratch bytes for its old probe.
Those dynamic bounds do **not** transfer to the new candidate: its required
checker failed, so hardware/software dynamic stack bounds are **UNPROVEN**.
The composed reference's prior stack proof was also unproved, separate from
this new standalone failure. No checker allowlist was relaxed to produce a pass.

At source level the candidate executes 64 one-bit magnitude advances per helper
call, replacing 64 variable bit selections; all 64 recurrence steps and 128
subtraction tests remain. The reference's emitted variable-shift helper performs
2,016 one-bit shift-body iterations per call. No composed candidate emitted
work bound, cycle WCET, platform/IRQ/NMI overhead or 100 Hz margin exists yet.
Unknown service budgets remain zero and deadline guards fail closed.

## Reproduction and evidence

Commands actually run, in gate order (the three prerequisite groups were run
concurrently; none was repeated):

1. `python3 -B tools/flight_demo/m2_full/renderer_build.py` — one fresh reference;
   wrapper exit 1 is the known full-fit failure; all underlying commands exit 0.
2. `python3 -B tests/flight_demo/m2_full/interpolation_corpus.py build/flight-demo/interpolation-comparison/corpus.bin`
   — frozen before the production edit, exit 0. Direct comparator Clang compile
   and run exit 0; exact argv in packet `01-direct/commands.json`.
3. Frozen projection Clang compile and run — exit 0; exact argv and read-only
   original corpus path in packet `02-projection/commands.json`.
4. `python3 -B tools/flight_demo/m2/build.py` — wrapper exit 1 at stack gate;
   all 12 prior subprocesses complete, logs retained.
5. `python3 -B docs/evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk/run_recipe.py host`
   — exit 0; exactly three host commands, no candidate target commands.
6. `python3 -B docs/evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk/collect.py`
   — read-only inspection of artifacts and preservation into this new packet;
   no build or target execution.
7. `python3 -B docs/evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk/verify.py`
   — PASS preservation of four checkouts, 20 unrelated entries, 15 historical
   flight inventories and 43 generated/memory files; scope, local links, JSON,
   whitespace and new packet identities checked. Repeated only to seal final
   report edits; no numerical checks or builds repeated.

The locked LLVM-MOS compiler and all flags remain unchanged. Compiler SHA-256
`cc557ae99a68ed36e098062b0f5376a878e94ac187b87446c8e603e4fb45a906`;
objdump `5327f031a741bfcd4104317fbad3d1e45275d70b49821f0da52391120848a8e9`;
nm `3db2d4f247dc2ae7fefbc5c7f8fde21ecc7925e353650b6103d6d6e64a88bed7`.
The [packet README](../evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk/README.md),
comparison, source freeze and artifact identities retain exact raw paths, bytes,
hashes, commands and successful/failed logs. Large corpora, PRG/ELF and host
executables remain in fresh ignored build directories; identities are archived.
No earlier packet was rewritten.

## Handoff

The candidate is stopped at the first failed prerequisite gate. Recommended next
action is a separate review of narrowly supporting the emitted `BIT` instruction
in the standalone stack verifier, with appropriate flag/control-flow and stack
regressions, before authorizing any resumed checks or the unused composed relink.
That review/fix is not implemented or authorized by this result. No further size
optimization, anchor/cache refactoring or automatic next experiment follows.

All four original checkout path sets/content and the 20 unrelated entries are
preserved; all 15 historical flight-evidence inventories remain exact. The
preservation record and packet inventory pin the checks. New changes consist of
the approved reconstructions, sole interpolation candidate, private test corpus/
comparator, new intent/evidence/report and this experiment's WIP. No generated
layout, memory ledger or public ABI changes. No Xemu, D81, SD, physical testing,
runtime/display admission, commit, push, PR or merge occurred.
