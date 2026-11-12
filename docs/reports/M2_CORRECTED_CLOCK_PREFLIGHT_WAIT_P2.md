# Corrected-clock preflight: publication-wait P2

**READY FOR REVIEW.** The production wait calculation is now called by the
independent timeline regression. All **21 focused host tests pass**. Negative
in-memory probes detect removal of the first-poll charge from either the helper
or the schedule caller. The preflight still returns **2 / UNPROVEN** and its
complete output is byte-for-byte identical to the original result.

## Scope and authority

Founder authorization: fix the reviewed publication-wait P2, test the production
bound against the independent timeline, run focused checks and preserve sealed
evidence/unrelated paths. Stop at READY FOR REVIEW. No relink or runtime testing.
This is a correction within the approved
[CC-D1–CC-D6 intent](../plans/65AERO_M2_CORRECTED_CLOCK_PREFLIGHT_INTENT.md).

- Branch: `codex/65aero-m2-corrected-clock-preflight`.
- Unchanged HEAD: `fcba7cf4f742a216fba1a6954a4e74b7c9d59ec8`.
- Local main reference remains `9570f0ab427121a4e8f042041a14c89aaaeff9e2`.
- Correction record: `65AERO-M2-PREFLIGHT-WAIT-P2-1`; the preflight analysis
  identity remains `65AERO-M2-FIXED-KERNEL-PREFLIGHT-3`.
- [Original report](M2_CORRECTED_CLOCK_PREFLIGHT.md) and original 34-member
  packet/seal remain unchanged. Their original source snapshots and test result
  are historical evidence; this correction does not regrade them.
- New [P2 packet](../evidence/flight-demo/2026-11-11-m2-corrected-clock-preflight-p2/README.md)
  retains prior active sources, exact final sources, commands, positive/negative
  outcomes and preservation results.

Only the active Python preflight, its focused test file and WIP change among
the prior active paths. This report and the P2 packet are new. The approved
intent, original report, prior checkers and all target sources remain unchanged.

## Correction and regression evidence

The previous test computed its own `H-U+2G+Cpub` bound, so a regression in the
production expression could pass. The unchanged formula is extracted into
`publication_wait_bound()` in the
[preflight](../../tools/flight_demo/m2_rebuild/corrected_clock_preflight.py).
`conditional_schedule()` now calls that helper. Unknown, nonpositive, noninteger
or invalid frame/window/gap inputs fail closed.

The [tests](../../tests/flight_demo/m2_rebuild/test_corrected_clock_preflight.py)
compare the helper's returned bound with a separate event-by-event polling
timeline over all discrete ready/first-poll phases of the two existing small
fixtures. They also compare the actual PAL/NTSC schedule result with that
timeline at window edges, missed first polls and frame wrap. The oracle does
not call the helper or duplicate its bound formula.

The closing-window counterexample is explicit: frame 101, window `[0,23)`,
maximum poll gap 7, ready at 16, first poll at 23. Further polls at seven-cycle
intervals first enter the next window at 107; three publication cycles give
elapsed **94**. The correct helper returns **95**. A one-gap bound of **88** is
insufficient.

Two read-only negative probes demonstrate that the new regressions protect
production code:

| In-memory mutation | Expected regression failures | Result |
| --- | --- | --- |
| Remove the first-poll term inside the production helper | Timeline, explicit counterexample and schedule integration tests | All 3 fail; probe PASS |
| Bypass the correct helper in the caller with a one-gap expression | Schedule integration test | Test fails; probe PASS |

The probes restore the original function after each run, write no source or
evidence files, and expose no execution grant. Their harness exits 0 only when
the exact expected failures occur without test errors. Captured output contains
the exact mutated function and test failures. These are successful negative
host checks, not failed target measurements.

## Validation and preservation

Commands and actual results, retained in `run-1/` of the P2 packet:

```text
python3 -B -m unittest discover -s tests/flight_demo/m2_rebuild -p test_corrected_clock_preflight.py -v
exit 0: 21 tests PASS

python3 -B docs/evidence/flight-demo/2026-11-11-m2-corrected-clock-preflight-p2/mutation_probe.py helper
exit 0: exact three regression failures detected

python3 -B docs/evidence/flight-demo/2026-11-11-m2-corrected-clock-preflight-p2/mutation_probe.py caller
exit 0: exact caller-integration failure detected

python3 -B tools/flight_demo/m2_rebuild/corrected_clock_preflight.py --old-root /private/tmp/f65-m2-fixed-kernel-cost-correction --references /private/tmp/f65-m2-service-reference
exit 2: BLOCKED: mandatory changed-image costs UNPROVEN
```

The preflight's output matches the sealed original `run-2/preflight.stdout`
exactly. No numeric cost allowance, launch budget or service grant is emitted.
Accepted target, rendering/oracle, C/sanitizer and exhaustive raw-sampler
campaigns were not rerun.

The first static check resolved the verbatim archived WIP's relative links
from its archival directory and failed. Its source, inputs, archive, command
and raw output remain under `static-attempt-1*`. The corrected check resolves
that one snapshot's links from the original repository-root context, without
altering its bytes. Host code and accepted host checks are unaffected.

Focused source/scope, Python syntax, JSON/contract identity, documentation-link,
whitespace, ancestry and preservation checks are recorded in the P2 packet.
All 34 original packet members plus seal remain unchanged. Of the 40 prior
active file identities, exactly the authorized tool/test/WIP may change; the
other 37 are preserved. All 16,654 published identities, 16,653 candidate
identities outside WIP, eight related checkouts and 480 unrelated paths are
preserved. The old historical preservation checker runs unchanged in its own
checkout, with output captured only in this new packet.

Two unavailable historical checkouts remain **NOT VERIFIED at the Git-worktree
tier**. Available hashes remain separate evidence; no metadata is reconstructed.

## Impact and stopping boundary

Inspected authority: repository workflow/principles, approved CC intent and
current display/resident contracts and ledger. Register/clobber, CPU-visible
and physical-memory, MAP/B, CPU-port, DMA, IRQ/NMI and target deadline changes
are **not applicable** to this host-only extraction and regression correction.
Generated contracts, target sources, precision, nine segments, camera/telemetry,
complete frames, 100 Hz/21 stages, memory ceilings/owners and zero reserve are
unchanged.

The first unresolved executable gate remains corrected-image clock observation,
calibration/rate and batch bounds. Actual complete-cost, resident and stack
admission remain UNPROVEN. Historical **755-byte** resident and independent
**298,776-cycle** cold-frame deficits are unchanged; conditional replacement
allowance remains `5820-C_clock`, at most **5810** before other clock charges.

Next: founder review of this focused P2. No relink, runtime/Xemu, kernel/tile
integration, optimization, banking, D81, SD, physical testing or Git publication
was performed.
