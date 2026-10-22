# M2 PR2 interpolation experiment — resumed single relink

**READY FOR REVIEW — bounded size PASS; full resident fit FAIL.**

The single composed candidate relink saves **385 resident bytes**, reducing the
exact 34,149-byte reference to **33,764 bytes**. It still exceeds the unchanged
`$8000` resident ceiling by **9,189 bytes**, ending at `$A3E5` exclusive. No
second candidate, further optimization or target execution followed.

The current task prompt authorizes resuming the remaining static checks and
unused relink under the [approved I1–I6 intent](../plans/65AERO_M2_PR2_INTERPOLATION_BUILD_INTENT.md).
The founder separately approved the [bounded BIT/CLV verifier correction](M2_BIT_CLV_VERIFIER_FIX.md).
This continues on `codex/65aero-m2-interpolation-experiment`, HEAD
`c6a41e0988a3e329f1b30f7d48c87d92e00b523b`, in
`/private/tmp/f65-m2-interpolation-experiment`. No branch/source reconstruction,
new reference build or production edit was repeated during this resume.

## Gate completion and preserved prerequisite evidence

The [original interpolation packet](../evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk/README.md)
retains the exact fresh reference, fixed corpus, original failed standalone
checker gate, passed host/oracle tests and five byte-identical renderer images.
Its [failed-gate report](M2_PR2_INTERPOLATION_BITWALK_EXPERIMENT.md) remains unchanged.
The verifier correction's original/accepted checker identities and replay
results remain in their separate packet. No historical failure was relabeled.

Before the candidate relink, the new preflight:

- revalidated all **79 candidate source/input hashes**, frozen direct-helper
  and projection test sources, Q46 source, approved checker/tests and locked
  compiler/objdump/nm/host-Clang hashes;
- completed every remaining standalone assertion after the original builder's
  failed stack-check line against its **exact pinned binary/disassembly/map**:
  stack bound, forbidden ROM/platform call exclusions, resident section ranges,
  software-stack symbol, compiler scratch and retained raster/record owners;
- verified the passed host inputs, three original host commands and all five
  image hashes, then copied that evidence into a fresh output directory;
- verified all **57 previous raw artifacts** and all 17 prior flight-evidence
  inventories before proceeding.

The standalone static result is **PASS**: 20 hardware-stack bytes including
entry return, zero dynamic software bytes and **487 resident scratch bytes**.
No standalone compile/link or numerical test was repeated. The original
builder's exit-1 record and missing success report remain intact; the new
[static result](../evidence/flight-demo/2026-10-22-m2-interpolation-relink/standalone-static.json)
records the later gate completion separately.

Previously passed numerical/host evidence is reused with exact source/corpus
identities: 457,334 direct old/new/independent-integer helper cases, 29,269,376
intermediate bit-state steps, 799,886 frozen projection cases +34 contract
checks, 3,857 independent Decimal cases, 841 near/far/reversed regressions with
sanitizer replay, and renderer generation/cache/cancellation/failure checks.
No oracle, tolerance, case set or source changed during the resume.

## Actual resident accounting

Allocated ELF32 sections were parsed independently and reconciled with the map,
including BASIC, zero-sized base-page sections, BSS, scratch and alignment gaps.

| Item | Fresh reference bytes | Candidate bytes | Delta |
|---|---:|---:|---:|
| BASIC header | 22 | 22 | 0 |
| Text | 30,747 | 30,368 | −379 |
| Read-only data | 1,561 | 1,560 | −1 |
| Initialized data | 2 | 2 | 0 |
| BSS | 1,611 | 1,611 | 0 |
| Compiler scratch `.noinit` | 200 | 200 | 0 |
| Alignment gaps | 6 | 1 | −5 |
| **Total resident span** | **34,149** | **33,764** | **−385** |
| End exclusive | `$A566` | `$A3E5` | −385 |
| Deficit against 24,575 allowed bytes | 9,574 | **9,189** | −385 |

Both `.zp.data` and `.zp.bss` remain zero bytes at logical `$22`.
Compiler scratch is charged once in the resident span, separately from dynamic
stacks. There is no reserve allocation, bank relocation or limit increase.
Above-ceiling placement is failed-fit diagnostic evidence, not admitted memory.

The complete symbol comparison finds exactly these size/kind/removal effects:

| Symbol/object | Reference | Candidate | Explanation |
|---|---:|---:|---|
| `interpolate_delta` own text | 1,605 | 1,257 | −348 bytes |
| `__ashldi3` own text | 31 | Absent | −31 bytes; no remaining symbol/call |
| SDK `__set_v` read-only constant | 1 | Absent | Map confirms removal of the one-byte `const.S.obj` contribution |
| Other symbol sizes/kinds | Exact | Exact | Address movement only |
| Alignment | 6 | 1 | Smaller text changes the next 8-byte-aligned rodata placement |

The unchanged transform descriptor table is 56 bytes; Q46 is 1,054 text bytes,
transform 985 and prepared projection 1,900. No added helper, table, persistent
state or secondary function-size regression appeared.

All named linked owner objects retain their sizes and symbol kinds. Addresses
below are CPU-visible diagnostic link addresses, not new physical allocations:

| Owner symbol | Bytes, both | Reference → candidate address |
|---|---:|---|
| `core` | 64 | `$A0C9` → `$9F48` |
| `glyphs` | 472 | `$9C2B` → `$9AAA` |
| `input.0` | 1 | `$A46D` → `$A2EC` |
| `m2_fit_activate_ok` | 1 | `$9E52` → `$9CD1` |
| `m2_fit_camera_down` | 2 | `$9E53` → `$9CD2` |
| `m2_fit_copy_ok` | 1 | `$9E51` → `$9CD0` |
| `m2_fit_return_ticks` | 4 | `$9E9C` → `$9D1B` |
| `m2_fit_service_ticks` | 4 | `$9E98` → `$9D17` |
| `m2_fit_staging` | 64 | `$9E58` → `$9CD7` |
| `m2_fit_store` | 1 | `$9E55` → `$9CD4` |
| `m2_fit_tile` | 2 | `$9E56` → `$9CD5` |
| `previous_camera_keys` | 2 | `$A49C` → `$A31B` |
| `renderer` | 846 | `$A11F` → `$9F9E` |
| `requested` | 22 | `$A109` → `$9F88` |
| `snapshots` | 46 | `$A46E` → `$A2ED` |

## Stack, compiler and conservative work bounds

The approved BIT/CLV checker was applied identically to the emitted reference
and candidate projection closures, including direct calls, tail jumps and
conditional transfers. Only the root label is renamed to `main` for the
existing checker; instruction bytes/addresses are unchanged.

| Static projection-closure result | Reference | Candidate |
|---|---:|---:|
| Hardware bytes including root entry return | 24 | 24 |
| Dynamic software bytes | 8 | 8 |
| Constant software-pointer adjustments | 2 | 2 |
| Checked call entries | 13 | 12 |
| Result | PASS | PASS |
| Shared resident compiler scratch | 200 | 200 |

Both roots syntactically allocate/free the same eight-byte software frame;
there are four software-pointer writes in each closure and no new write form.
The smaller helper preserves public/generated ABI and introduces no new caller
contract. These are **projection-closure** bounds, excluding renderer callers,
platform/IRQ/NMI frames and executed high-water. The complete composed probe
remains **UNPROVEN** with the unchanged checker: both artifacts stop at
`unrecognized instruction: cld`. No further allowlist change was made.

Conservative instruction-visit accounting uses the frozen loop bounds and
actual instruction inventories, not measured cycles:

| Bound | Reference | Candidate |
|---|---:|---:|
| Interpolation own instruction inventory | 748 | 596 |
| One interpolation including helper work | 216,580 | 116,220 |
| One `m2_project_prepared` closure | 4,437,026 | 2,630,546 |

Interpolation uniformly overcounts local instruction visits by `65 × 3`,
covering 64 bit steps, two subtraction tests per step and guards. The reference
also charges 64 calls to the 17-instruction variable-shift helper with 65 visits
per instruction. That emitted helper is absent in the candidate, whose 64
unsigned magnitude advances are included locally. At source level all 64
quotient/remainder steps, tie rounding, signed narrowing and sign restoration
remain identical to the already proved candidate.

Both sides already contain the accepted compact projection, so both bounds
charge three bounded copies, not the older nineteen-copy implementation.
They retain two endpoint transforms, 18 Q46 products / 162 limb products,
12 plane distances, 18 coordinate interpolations and four wide divisions.
No CPU-cycle WCET, speedup, wait-state cost, 100 Hz margin or dispatch service
budget is inferred. Unknown budgets remain zero and guards fail closed.

## Commands, identities and stop boundary

Commands run in this resume:

1. `python3 -B docs/evidence/flight-demo/2026-10-22-m2-interpolation-relink/preflight.py`
   — exit 0, remaining standalone static checks and all frozen identities PASS.
2. `python3 -B docs/evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk/run_recipe.py link --output /private/tmp/f65-m2-interpolation-experiment/build/flight-demo/m2-interpolation-resumed-1792701029486920000`
   — **one candidate relink**; backend compile, target compile/link, objdump and
   nm all exit 0. Recipe wrapper exits 1 for the measured full-fit FAIL. The
   outer capture wrapper exits 0 after preserving that exact result. Immediate
   size/deficit/scratch results were reported, then implementation stopped.
3. `python3 -B docs/evidence/flight-demo/2026-10-22-m2-interpolation-relink/account.py`
   — exit 0; read-only ELF/map/symbol/owner, stack and instruction accounting.
4. `python3 -B docs/evidence/flight-demo/2026-10-22-m2-interpolation-relink/verify.py`
   — preservation, scope, generated-file, exact command-recipe, link, JSON,
   whitespace and packet-inventory checks; no build or execution.

The original three host commands remain recorded with their original paths.
The fresh `build.json` explicitly labels their evidence reuse; those host
commands were not rerun in the fresh output. The old host `build.json`, its
binary/images/logs and every previous raw file remain unchanged.

The full target flags remain `-mcpu=mos45gs02 -mlto-zp=0
-DM2_TARGET_LAYOUT_CHECK=1 -Oz -fno-inline-functions -fno-jump-tables -Wall
-Wextra -Wconversion -Werror`; the opaque backend retains its separate
`-fno-lto -c` compile and omits `-mlto-zp=0`, exactly as in the reference.
Compiler SHA-256 remains
`cc557ae99a68ed36e098062b0f5376a878e94ac187b87446c8e603e4fb45a906`.
The [packet](../evidence/flight-demo/2026-10-22-m2-interpolation-relink/README.md)
retains exact argv, all tool hashes, 79 source hashes and raw artifact identities.

| Identity | SHA-256 |
|---|---|
| Reference PRG | `72fd75a63771794a0f1936f92289cac612db149317781ab5646756a8045aa94d` |
| Reference ELF | `81fbae03f52e8548e8b3a9c304807c969f96097611dc1d6888993c344609c5d2` |
| Candidate PRG, 31,955 bytes | `5ba1a5a8cc60a896e3f9e9332157d6ddef08a61b313d68663c9c8e6791f62bd3` |
| Candidate ELF, 41,328 bytes | `5657e8abb806af78d2b0ebb34da7c77f410297e574161cbb3375efff1870c941` |

## Impact, preservation and handoff

Graphics still owns the private arithmetic. All renderer/cache generations,
cancellation/invalidation, workspace lifetimes, labels/anchors, precision and
memory/stack ceilings remain frozen. No ABI/layout, physical allocation,
MAP/base-page, DMA, IRQ/NMI or platform source change. The compiler's actual
emitted code, call removal, data alignment and closure stacks are accounted
above; no runtime hardware effect was exercised. No architecture deviation or
new acceptance of the retained composition scaffold is implied.

All 17 earlier flight-evidence inventories, four original checkout path sets,
57 old raw artifacts, 20 unrelated entries and all 43 generated/interface/memory
files are preserved. In this experiment, only WIP and the new result/evidence
paths changed during the resume; every pre-existing source/report/packet remains
exact. The approved verifier source and regressions are unchanged.

Recommended next action: review the bounded interpolation result and its
accounting. **9,189 resident bytes**, whole-program stack/ABI, cycle/service
proof and runtime/display admission remain unresolved. No further optimization,
new relink, publication or target test follows automatically. No Xemu, D81, SD
or physical testing occurred. Stop READY FOR REVIEW.
