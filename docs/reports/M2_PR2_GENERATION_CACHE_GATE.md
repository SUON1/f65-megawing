# M2 PR2 generation cache, exact Q46 and dispatch — failed fit gate

**BLOCKED — first resident admission gate FAIL; implementation stopped.**
Baseline: `8ee5214ea9c63b86e92ca9bc4fa0779115dbd57f`.
Branch: `codex/65aero-m2-pr2-renderer-fit`.
Authority: founder requested generation caching, exact Q46 equivalence before
replacement, proved workspace reuse, deadline-aware dispatch and immediate
compile/link measurement, with Xemu conditional on passing admission gates.
The [earlier failed renderer](M2_PR2_RENDERER_FIT_GATE.md) remains unchanged.
[Fresh evidence](../evidence/flight-demo/2026-10-21-m2-generation-cache/README.md).

## Result

The composed early target compiles/links but ends at **`$AE2B`**, occupying
**36,394 resident bytes** against **24,575 allowed**. Excess is **11,819 bytes**,
2,572 worse than the retained `$A41F` attempt. The functional changes improve
reuse and remove repeated projection, but do not recover code space.
No precision, range, reserve or memory ceiling was relaxed. Oversized addresses
are diagnostic placement only, not admitted allocations.

| Requirement | Actual outcome |
|---|---|
| Prepare 17 segments once per generation | Implemented as 17 continuation actions, with cache generation/revision published only after the last entry; bounded host checks PASS |
| Exact specialized Q46 multiplication | Archived-general and independent-integer comparisons PASS before replacement; algebra/domain bounds and unchanged Decimal oracle PASS |
| 289-byte cache/workspace reuse | Target compile-time size checks and host lifetime/cancellation/failure tests PASS; 320-byte existing workspace reused |
| Deadline-aware dispatch | Fail-closed guard and fractional release progression implemented/tested; actual target service bounds remain UNPROVEN |
| Immediate early composed compile/link | Compiler/linker PASS; resident admission FAIL at `$AE2B` |
| Full target/runtime/display admission | NOT REACHED |
| Conditional Xemu | NOT RUN: prerequisite admission failed |

No implementation changes followed the failed fit. No D81, SD, physical testing,
commit/push/PR/merge or later milestone.

## Changes by subsystem

- **Graphics geometry:** `m2_q46_private.h` adds an exact signed Q46 product;
  `m2_geometry.c` replaces only the rotation multiplication path. General
  fractional clipping interpolation, Q24/Q16 behavior and public validation stay.
  A new private prepared-owner comparison validates every camera/transform and
  identity field without reconstructing the matrix at renderer commit; public
  `m2_pair_eligible` still reconstructs untrusted records as before.
- **Graphics renderer:** capture returns before transformation. Continuations
  prepare the matrix, register the bundle, project one corner at a time, build
  telemetry, copy telemetry/footer, project one canonical segment per cache
  action and then render world tiles using cached lines. Segment projection is
  **17 per captured generation rather than 10,880 per completed frame**; four
  protected corner projections remain separate. Full-cursor replay per tile
  remains and is not claimed throughput-admitted.
- **Private Graphics state:** replaces `text[320]` with a 320-byte union; adds
  generation/revision cache tags and captured start tick (12 bytes). Target
  renderer is 846 bytes, previously 834. No generated public layout changes.
- **Diagnostics dispatch:** pure deadline policy rejects zero/unknown bounds,
  zero return margin, overdue releases, insufficient remaining time and overflow.
  Q16 release fractions carry forward instead of discarding fractional ticks.
  The compile-only root gates capture, construction and commit separately using
  a fresh clock sample. Phase bounds must include callees and return overhead.
- **Test backend:** exposes opaque budget inputs defaulting to zero. These keep
  paths reachable for the compile-only measurement while granting no expensive
  target action by default. They are not target WCET or clock calibration.
- **Tests/tooling:** equivalence/oracle fixtures, cache/lifetime/identity and
  deadline tests; completed-image byte comparison to retained prior images;
  target cache-size assertion; build report handles scalarized `input.0` and
  eliminated stage arrays and records the actual failed gate successfully.

## Exact Q46 proof and numeric validation

For magnitudes `a=a1*B+a0`, `b=b1*B+b0`, `B=2^23`, the exact product is
`a1*b1*B^2 + (a0*b1+a1*b0)*B + a0*b0`.
The implementation divides by `B^2=2^46`, retaining the complete low sum plus
`2^45` rounding bias before shifting, then restores the product sign. This is
nearest/ties-away, identical to the archived general-ratio path. There is no
approximation, precision narrowing or discarded carry.

For admitted input magnitudes at most `2^46`, cross terms are below `2^47` and
the biased low sum below `2^48`; all intermediate arithmetic fits uint64.
Translated point magnitudes are bounded by 1,300,838,219,776, below `2^46`.
Exact integer checks over all 14,641 legal roll/pitch pairs and 360 yaw norms
establish the same bound for generated transform coefficients, using Cauchy
bounds plus the two rounded terms' at-most-one-unit error and exact cardinal
zero-roll cases. See `q46-proof.json` for derivation and domain.

Before modifying the production rotation path:

- ASan/UBSan comparison against the archived original general-ratio C path:
  **216,706 cases PASS** (edges, generated sine products and seeded samples).
- Independent Python unbounded multiplication/rounding oracle:
  **101,729 cases PASS**, including split boundaries, half ties and signs.

After integration, the unchanged 60-digit Decimal geometry oracle passes all
**3,857 cases**, and all **841 near/far regressions** pass. Maximum projection
errors remain 0.000021224219 and 0.035136325 pixel. Raster tolerance is unchanged.
All five completed host PPM images are byte-identical to the earlier renderer's
retained images; these are host images, not target scanout evidence.

## Workspace lifetime and identity proof

| Phase | Active union contents | Consumer and end of lifetime |
|---|---|---|
| Telemetry construction/copy | 320 text bytes | HUD tile construction only; synchronous backend copies each finished tile before return |
| After final HUD/footer copy | Neither member may be consumed | Text lifetime ends before first cache write; no backend retains a pointer |
| Cache preparation | 17 lines (272 bytes) + 17 visibility bytes | One entry assigned per action; cache identity stays zero until all entries complete |
| World/ready | Complete immutable cache | Only matching captured generation/revision can be consumed |
| Cancel/failure | Invalid | Tags and prepared readiness cleared before idle/fatal; displayed complete store/bundle retained |
| Next capture | Invalid until rebuilt | Telemetry overwrites all text, then cache entries are reconstructed; no old cache becomes valid |

The target statically asserts exactly **289 cache bytes** and **320 union bytes**.
Native padding is allowed only within the same 320-byte union; it is not a
serialized layout or additional allocation. This saves a separate 289-byte
allocation; it does not reclaim resident text or hide cache bytes in reserve.

Host checks cover all declared preparation/construction/ready cancellation phases,
restart after cancellation, generation exhaustion, stale identity, copy/activation
failures, corrupted transform and outer composition, and exact cached/legacy
projected lines. Cache identity is cleared by the single fatal helper and cancel
path. A future asynchronous backend must supply completion/lifetime proof before
this reuse is admitted; the present seam is explicitly synchronous.

## Actual memory and compiler effects

| Section | Start | Bytes | Change from prior renderer |
|---|---|---:|---:|
| BASIC header | `$2001` | 22 | 0 |
| text | `$2017` | 33,036 | +2,565 |
| alignment gap | `$A123` | 5 | +3 |
| read-only data | `$A128` | 1,505 | 0 |
| initialized data | `$A709` | 2 | 0 |
| BSS | `$A70B` | 1,611 | +20 |
| static compiler scratch | `$AD56` | 213 | -16 |
| End exclusive | `$AE2B` | 36,394 total span | +2,572 |

Static scratch is counted once; no integrated dynamic-stack bound is inferred.
The new Q46 helper occupies 1,157 text bytes; the private prepared comparison
1,025; explicit anchor/cache/register continuations 439/437/332; deadline checks
and release progression 242/156. These are gross symbol costs, not independent
marginal savings: old functions specialize/disappear and helpers remain shared.
The generic 64-bit interpolation routine remains necessary for actual clipping.
The measured combined result is larger, despite reduced repeated work.

No new handwritten assembly or public calling convention is introduced. The
compiler changes stack/helper use: standalone regression reports hardware bound
28 bytes, dynamic software 0 and resident scratch 468, versus prior 25/16/443.
Those results apply only to its standalone direct-call probe, not this renderer.

Target SHA-256:
`87d2a64bc3d536daecbaaac977eb543e92be23093ec80c17ae343487570af583`.
Raw identity: `build/flight-demo/m2-renderer-1792602204844535000/RENDER.prg`.
It is oversized and not admitted for execution.

## Static service disposition

**No target service bound is admitted.** The actual bound table remains absent;
opaque backend values default to zero and the guard grants no action. Host
synthetic grants test policy only. There is no claim that a complete projection,
clipping operation or matrix preparation now fits a 100 Hz service window.
They remain synchronous within their individual continuation action, and must
be subdivided further if conservative target analysis cannot bound them inside
the available service budget. Expensive work is outside the authoritative tick
path; actual enabled-profile stack, interrupt and return overhead remain unproven.

Known static work caps: one matrix preparation, one registration, one anchor or
one segment projection per corresponding action; at most eight background/raster/
overlay samples, or one 64-byte transfer per other action. These counts are not
cycle bounds. The requested per-generation preparation and fail-closed deadline
policy are implemented, but runtime admission is not complete.

## Reproduction and stop

- Exact proof compiler/runner commands are in `q46-before-replacement/commands.json`;
  raw output `build/flight-demo/m2-q46-proof-1792601961875009000/`.
- `python3 -B tools/flight_demo/m2_full/renderer_build.py`: first attempt
  `m2-renderer-1792602193006199000` stopped on a missing test-only fixture include;
  retained exact source/log. Corrected that include before the admission link.
  Fresh `m2-renderer-1792602204844535000`: three contract tests and host
  ASan/UBSan PASS, target compile/link and cache layout assertions PASS, fit FAIL.
- `python3 -B tools/flight_demo/m2/build.py`: fresh
  `m2-pr1-1792602193451187000`, PASS host/oracle/near-far/standalone target checks.
- Corpus/ledger/scope, whitespace, source hashes, historical inventories and
  preservation checks PASS. Original modified sources are archived, earlier
  evidence is byte-identical, and all 20 unrelated entries remain untouched.

Stop at failed fit; no continued optimization, actual display adapter work,
full-target/stress variants, runtime/display admission or Xemu. Recommend review
of this exact regression in code size before authorizing another bounded change.
The conditional Xemu instruction is retained; no failed or unadmitted artifact
will be executed to bypass the gate. D81, SD and physical testing remain excluded.
