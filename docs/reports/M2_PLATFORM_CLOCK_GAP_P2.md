# Platform clock gap verifier — P2 correction

**READY FOR REVIEW.** The approved normalization-bound correction is complete
under analysis identity `65AERO-M2-PLATFORM-CLOCK-GAP-2`. Eight Python regressions
and the static replay passed. No C source, target executable, memory allocation
or runtime grant changed.

The branch remains `codex/65aero-m2-platform-clock`, HEAD
`5c78bf7d00aadda0e63ce800e27fe3e142c651c0`. Main remains
`9570f0ab427121a4e8f042041a14c89aaaeff9e2`. This is the founder-approved P2
addition to [PC-D1–PC-D6](../plans/65AERO_M2_PLATFORM_CLOCK_CONTINUITY_INTENT.md),
not publication or executable admission.

## Corrected bound

The [new verifier](../../tools/flight_demo/m2_rebuild/clock_gap_v2.py) is a
versioned successor to the sealed `inspect_gap.py`. The original 13-member
packet, seal and [original report](M2_PLATFORM_CLOCK_CONTINUITY.md) are unchanged.
The original normalization bound is superseded by this correction, rather than
rewritten in historical evidence.

The divisor call at `$298F` uses widths 1–6, requiring 0–5 body iterations.
The product call at `$29B3` passes 13 (`LDA #$0D` at `$29AB`), requiring 12 body
iterations and 13 condition visits. A global cap of 12 conservatively covers
both callers. The previous cap of six charged only seven cyclic visits.

The new constructor rejects an insufficient/missing cap, changed callsite set,
changed product count or changed countdown control flow before cost analysis.
The raw target, disassembly and symbols now come from the same verified baseline
directory. The SCC algorithm, all other loop caps, sampler model and observation
gap policy are unchanged.

| Conservative static quantity | Original packet | Corrected replay |
| --- | ---: | ---: |
| Normalization CPU-cycle bound | 10,459 | 14,191 |
| Divide-setup CPU-cycle bound | 55,620 | 63,084 |
| Continuation CPU-cycle bound | 406,245 | 406,245 |
| Largest caller interval, CPU cycles | 26,920,964,465 | 26,920,964,465 |
| Native-count observation-gap bound | 728,824,896 | 728,824,896 |
| Margin below strict 2,147,483,648 limit | 1,418,658,752 | 1,418,658,752 |

These are analyzer bounds, not measured execution times. Normalization charges
six additional cyclic visits of 622 conservative cycles each. Both calls gain
that allowance, increasing divide setup by 7,464 cycles. Another path still
dominates the continuation envelope, so the overall gap is unchanged. The old
cap is nevertheless rejected; spare aggregate margin does not excuse it.

## Validation and independence

- `python3 -B tests/flight_demo/m2_rebuild/test_clock_gap_v2.py`: exit 0,
  **8/8 PASS**. Independent reverse-byte index sequences cover widths 1–6 and
  13. An independent linear sum of the actual linked loop verifies the extra
  cost without using the verifier's SCC partition or visit multiplier.
- Negative fixtures reject cap six, cap eleven, a missing cap, changed product
  width, changed count initialization/decrement/test/backedge, missing/additional
  callers and a shifted entry. Fixtures alter analysis objects only; the sealed
  input files and clock source are hash-checked before and after both outcomes.
- `python3 -B tools/flight_demo/m2_rebuild/clock_gap_v2.py --baseline
  /private/tmp/f65-m2-fixed-kernel-cost-correction`: exit 0, **static preflight
  PASS for its old-image/host-only scope**. All 81 pinned target inputs, the
  sealed target and eight emulator reference files were verified. The retained
  4,128,705 sampler cases still pass within that same bounded model.
- The original 11 C host/sanitizer tests were **not rerun**. Their source,
  evidence and acceptance scope remain unchanged.

Fresh [evidence](../evidence/flight-demo/2026-11-11-m2-platform-clock-p2/) retains
exact commands, exit codes, stdout/stderr, Python identity, source identities
and source archive. Outputs were captured in a fresh temporary directory before
being copied into this new packet. The original packet seal remains
`0b0abb69eebb774bbba81203cb9f7b8a990b634c8b1e2968e28af091cc89e593`.
The analyzed PRG remains
`7fdcea61387c0e6b7ae92310725966ac6c0e29e82e8ba1c9a6be77335af76aad`.

## Preservation and remaining limits

Scope, syntax, JSON, local-link, whitespace and preservation checks verify the
16,628 pre-existing file identities outside WIP, the full original packet,
original report, all clock C/test source, six related checkouts and 480 unrelated
paths. Prior WIP is retained in the new packet. Two unavailable historical
checkouts remain **NOT VERIFIED at the Git-worktree tier**; nothing was rebuilt
or reconstructed.

The first preservation-harness attempt incorrectly resolved the archived WIP's
relative links from its new packet directory. Its source and failed output are
retained. The successor checks those links from the original repository root;
this tooling correction changes no archived document or admission result.

Only the new verifier, Python tests, correction report/evidence and WIP change.
Generated contracts, public ABI, precision and memory owners are unchanged.
Register/clobber, CPU/physical memory, MAP/B, DMA, IRQ/NMI and runtime deadline
effects are not applicable to this host-only correction. No code-size or service
optimization was performed.

Changed-image code size, state padding, compiler scratch, stacks and timing remain
unmeasured. The historical **755-byte resident deficit** and independent
**298,776-cycle cold-frame deficit** remain failures. The corrected old-caller
gap is not a new executable grant or complete-frame scheduling proof.

Next: founder review of this focused P2 correction. No compiler, target relink,
runtime/Xemu, D81, SD, physical testing, commit, push, PR or merge was performed.
