# Corrected-clock complete-cost preflight successor

**READY FOR REVIEW — actual admission BLOCKED / UNPROVEN.** CC-D1–CC-D6
authorized this host-only successor. It establishes conditional calibration,
publication-window and joint cost constraints. The first unresolved executable
gate is the corrected clock's observation/calibration/rate and instruction-batch
envelope. Its target costs have not been measured. No remaining-cycle allowance,
launch budget or service grant is emitted; the preflight returns **2**.

## Identity and scope

- Analysis identity: `65AERO-M2-FIXED-KERNEL-PREFLIGHT-3`.
- Branch: `codex/65aero-m2-corrected-clock-preflight`, from
  `fcba7cf4f742a216fba1a6954a4e74b7c9d59ec8`.
- Main remains `9570f0ab427121a4e8f042041a14c89aaaeff9e2`.
- [Approved intent snapshot](../plans/65AERO_M2_CORRECTED_CLOCK_PREFLIGHT_INTENT.md)
  is copied unchanged from the planning worktree. Its preapproval wording is
  historical; approval and execution are recorded here and in WIP.
- The new [companion](../../tools/flight_demo/m2_rebuild/corrected_clock_preflight.py)
  and [18 focused Python regressions](../../tests/flight_demo/m2_rebuild/test_corrected_clock_preflight.py)
  are the only engineering additions. Target source, historical verifiers,
  contracts, ledgers, CI policy and all runtime grants are unchanged.
- [Evidence packet](../evidence/flight-demo/2026-11-11-m2-corrected-clock-preflight/README.md)
  retains initial fixture failures, successful checks, exact source snapshots,
  the final preflight output, commands and preservation identities.

The historical image uses its separate source root at `5c78bf7`; all 81 inputs
and 12 sealed target members remain pinned. Its PRG SHA-256 remains
`7fdcea61387c0e6b7ae92310725966ac6c0e29e82e8ba1c9a6be77335af76aad`.
The corrected source has 82 separately pinned inputs from `fcba7cf`, including
the private clock header. The unchanged old verifier is never made to accept
the corrected adapter as a constituent of the old executable.

All eight reference sources remain pinned to Xemu
`40dfef0d1d5f56be2469492715c12bdb32c75b67`. The four FC1/FC2/PC/P2 packets retain
their 20/23/13/16 members plus seals. The corrected P2 cap is **12**, with the
prior 14,191/63,084-cycle normalization/division bounds restricted to their
old image. Accepted PC/P2 C and exhaustive sampler evidence is reused without
rerunning those campaigns.

## Source-model results and conditions

The corrected converter preserves actual countdown continuity, independent
hardware-period and uint32-output wrap, duplicate samples and sticky faults.
Its gap requirement remains strictly below `2^31` supplied native counts.
A missed complete hardware period can alias; a small observed delta does not
establish the caller gap. The new countdown-event regressions independently
check A/B reloads, repeated periods and the separate output wrap.

Seventeen successful frame samples span sixteen frame intervals. Let `R` be
624 PAL or 526 NTSC lines, `L` be 1,296 or 1,287 nominal CPU cycles per line,
and `u_i` the sample offset in CIA updates after its detected frame edge.
Under the explicit requirements that every frame-counter observation gap is
less than one frame and frame-read-through-successful-sample work is less than
one line, a conservative complete enclosure is `0 <= u_i <= R`.
Duplicate adjacent timestamps are allowed by the actual converter.

```text
k = u_16 - u_0, every integer k in [-R,R]
elapsed = 32*(16R+k)
elapsed/16 = 32R+2k                    (exact on this reachable lattice)
P(k) = floor(405000*(32R+2k)*65536/(R*L))
release_n = origin + floor((fraction_0+n*P)/65536), modulo 2^32
```

| Conditional enclosure | PAL | NTSC |
| --- | ---: | ---: |
| Endpoint classes | 1,249 | 1,053 |
| Minimum period Q16 | 614,400,000 | 618,696,503 |
| Maximum period Q16 | 696,320,000 | 701,189,370 |
| Minimum logical due-event separation, CPU cycles | 378,432 | 379,665 |
| Interior sample lines, upper endpoint excluded | 5–96 | 5–48 |
| Minimum interior duration, CPU cycles | 117,936 | 55,341 |

These are interval bounds, **not admitted periods or a new 100 Hz tolerance**.
The deliberately broad calibration enclosure permits approximately ±6.25%
phase bias. Nominal 100 Hz rate qualification remains **UNPROVEN**. The model
retains the bias to protect earliest releases; it does not claim that this
large uncertainty is acceptable. All 65,536 fractional carry classes and all
32-count lattice classes are covered by independent integer interval lemmas
and regressions. Host time, CPU cycles and native counts remain distinct.

In the pinned normal multi-operation emulator mode, each CPU batch consumes
at least a nominal line before the one CIA update/render callback. A bounded
batch excess `E` gives a maximum physical frame interval `H=R*(L+E)` in CPU
cycles. This requires no DMA, early batch stop, tracing, single-step or hypervisor
debugging. Those conditions have not been qualified by running an executable.
The eight pinned sources witness batching; the extra read-only DMA inspection
is explanatory only, not an additional admitted reference input.

The unchanged Platform assembly disables CIA interrupt sources, enables only
raster IRQ, and acknowledges raster status in the handler. Pinned VIC source
checks that raster source at scanline advancement. The model deliberately
charges at most one IRQ per line plus a pending IRQ; complete IRQ cost remains
an explicit variable. An NMI/fault path cannot resume successful publication.

For publication, physical raster registers identify the next line to render.
The first selector-dependent screen fetch is at active line 112 PAL / 64 NTSC;
screen selector writes/readback precede first enable and matching Graphics
record publication without a scheduler yield. The sufficient cost constraint
is **the entire first-raster-high-read through matching record publication,
including IRQ, calls, fault checks and first enable, strictly less than one
line**. A selector-only bound is insufficient. Conservatively allowing a stale
line and phase rounding leaves 14 complete lines at the final accepted line,
above the required two. Actual publication timing is still UNPROVEN.

## Conditional joint cost construction

This is a sufficient interval proof, not an implementation of fixed kernels.
All actual costs are typed unknowns. The CLI has no option to supply guessed
costs; its regression-only API labels every synthetic result as conditional and
keeps execution unauthorized.

Let `T` be the minimum due-event separation, `D` the complete tick/observation
cost, `I` the complete IRQ cost, and `F` the **total** unusable atomic/guard/poll
tail per release interval. `F` must include quantization, observation staleness
and no-grant polling, not just one guard call. `W` is all capture-through-ready
foreground work, excluding separately charged ticks/IRQs/wait:

```text
W = 377*C_product + 198*C_division + W_frame_rest
R_ready >= W + (1+ceil(R_ready/T))*(D+F) + (1+ceil(R_ready/L))*I
```

Each whole division includes normalization, two quotient digits, correction,
sign, rounding, overflow and wrappers. The 396 digits are not charged again.
`W_frame_rest` must cover all remaining geometry, horizon, raster, map/text,
Platform transfers/setup, calls/returns, clocks, guards and composition control.
Demand stays **640 tiles / 45,840 bytes**; there is no 550-tile credit or payload
sketch substitution. Fragmentation is an elapsed loss; no CPU work overlaps.

Use the same response recurrence for complete unsuccessful polling work to
obtain maximum first/subsequent sample gap `G`, charging intervening ticks and
IRQs rather than assuming only one tick. Require `G<T` and `G<U`, where `U`
is the conservative interior duration. Tick work plus observation latency and
interrupts must itself finish strictly before the next minimum due event.
Native-count guards additionally require endpoint conversion and strict
inequality: equality, half-range ambiguity and grants above uint16 are refused.

With `Cpub` the whole publication bound, `B` previous-commit-to-next-capture
latency, and `Jinput` persistent-input-to-authoritative-pose latency:

```text
V_wait <= H-U+2*G+Cpub
A = R_ready+V_wait
A <= 2,025,000                         capture age, 50 ms
B+A <= 2,025,000                       inter-commit cadence, 20 Hz
Jinput+2*A+B <= 4,050,000               persistent pose age, 100 ms
```

The two `G` terms cover an initial poll that misses the closing window and a
later poll in the next window. Ticks/IRQs serviced **inside** `V_wait` are not
added again outside it. The interval proof is phase-independent and applies
inductively to consecutive generations without resetting carry or raster phase.
Captured-camera FK-D4 remains proposed successor behavior, not an implemented
feature of the historical executable. Full changed-renderer camera, cancellation,
exhaustion, replay and frame-coherence tests are **NOT REACHED**; their source
and executable do not exist in this host-only task.

Pre-activation cancellation/invalidation/failure retains the previous complete
frame. Uncertain selector/readback requires terminal failure/reset with displayed
identity UNPROVEN, not a claimed rollback. Neither earns cadence credit.
Cell-exclusive tiles, complete maps, 80-byte bitmap, 24-byte delta and retired
synchronous 64-byte Platform buffer lifetimes remain unchanged obligations.

## Gates and accounting

| Gate | Result |
| --- | --- |
| Frozen inputs / separate image and source roots | PASS |
| Focused independent host regressions | PASS, 18 tests |
| Corrected clock and calibration arithmetic source model | PASS within stated conditions |
| Publication and interval cost formulas | Conditional host proof only |
| Changed-image observation/calibration/rate and batch bounds | **UNPROVEN — first unresolved executable gate** |
| Actual joint schedule / complete fixed-kernel costs | NOT REACHED / UNPROVEN |
| New resident fit / whole-program stack | NOT BUILT / UNPROVEN |
| Target relinks / runtime executions | **0 / 0** |

Historical actual resident remains **29,426 / 28,671 bytes, 755 over**, scratch
87 and reserve zero. Historical cold lower bound remains **2,323,776 /
2,025,000 cycles, 298,776 over**. These remain independent failures of the old
image, not measurements of corrected source.

Historical hypothetical retirement 6,935 and gross allowance 6,180 remain
unchanged. Subtracting 256 margin and 104 proposed data leaves 5,820. The current
conditional expression is **5,820 − C_clock**: the 10 logical state bytes alone
reduce its upper ceiling to **5,810**, before additional clock code, padding,
scratch or alignment. Host size 12 is not target layout. No margin or reserve
is consumed, and no actual fit follows from this arithmetic.

## Validation, preservation and handoff

Final commands, from this worktree:

```text
python3 -B -m unittest discover -s tests/flight_demo/m2_rebuild -p test_corrected_clock_preflight.py -v
exit 0, 18 tests PASS

python3 -B tools/flight_demo/m2_rebuild/corrected_clock_preflight.py --old-root /private/tmp/f65-m2-fixed-kernel-cost-correction --references /private/tmp/f65-m2-service-reference
exit 2, BLOCKED: mandatory changed-image costs UNPROVEN
```

The initial run exposed two test-fixture mistakes: a temporary path traversed
macOS `/var`'s symlink, and an intended successful sample was in the sampler's
existing reload exclusion. The corrected fixtures use their canonical temporary
root and an accepted update. Original logs and exact failed sources remain in
`run-0`; `run-1` and final `run-2` are retained separately. No historical packet
was used for regression outputs. Successful and failing cases compare the
protected inventories and refuse changed, missing, symlinked, wrong-root,
extra inputs, cap-six evidence, unknown/zero costs, wrong units,
truncated/unsupported phase partitions and unproved tile credit.

Static syntax, documentation links, JSON/contract identities, whitespace,
ancestry and focused-scope checks are recorded in the new packet. Preservation
checks cover all 16,654 published files, 16,653 candidate files outside WIP,
eight related checkouts and 480 unrelated paths. The original preservation
checker runs unchanged in its original checkout. Two unavailable historical
checkouts remain **NOT VERIFIED at the Git-worktree tier**; available file
hashes are separate evidence. No metadata was reconstructed.

Inspected authority: repository workflow/principles, approved CC/FK/FC/PC
intents, Main v1.8/Runtime v1.2 candidate, Phase 1 plan, display commit contract
and extended resident contract/ledger. New work is host-only: registers/clobbers,
CPU-visible/physical memory, MAP/B, CPU port, DMA, IRQ/NMI and target deadlines
have no implementation changes. Generated artifacts are unchanged. Precision,
public ABI, nine segments, camera/telemetry/NOT IMPLEMENTED labels, complete
frames, 100 Hz/21 stages, production `$8000`, development `$9000` and zero
protected reserve remain fixed.

The smallest next task is a separately authorized exact-image measurement and
qualification of the corrected clock's costs and calibration observation/rate
envelope. It must resolve that first gate before supplying costs to a candidate
schedule. No fixed-kernel implementation, renderer optimization, relink, runtime,
banking, Xemu, D81, SD, physical testing or publication was started here.
