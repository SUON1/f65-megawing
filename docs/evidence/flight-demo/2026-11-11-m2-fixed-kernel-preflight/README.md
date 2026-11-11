# Fixed-kernel preflight evidence

Status: **READY FOR REVIEW; complete-cost admission not established.**
This packet contains host/static analysis only. Target links and runtime
executions are both zero. It does not amend any prior sealed measurement.

Source baseline: `0e63edfb7de62ff991c91072a02397f432c12582`.
Fetched main: `9570f0ab427121a4e8f042041a14c89aaaeff9e2`.
Successor branch: `codex/65aero-m2-fixed-kernel`.

- `preflight-final.json`: final calculation, source/reference identities,
  selected linked-symbol accounting, tick bound and refused complete-cost gate.
  Command exit **2**; empty stderr. No new PRG was generated.
- `regressions-final.txt`: **11 host verifier regressions PASS**, exit 0.
- `checkpoint-before.json`: 16,557 file identities captured before the first edit.
- `preservation.json`: 16,556 unchanged baseline identities outside WIP,
  all 480 unrelated paths, six available historical Git checkouts and the
  preserved failed branch. Two missing checkouts remain NOT VERIFIED at the
  Git-worktree tier.
- `tick-attempt-1.stderr`, `tick-attempt-2.stderr`: retained verifier-development
  errors (incorrect source path, then uncovered stage-2 feedback edge), exits 1.
  Their empty stdout captures were initially named `.json`; before sealing,
  the filenames became `.stdout`, with the zero-byte contents unchanged.
- `tick-attempt-3.json`: first successful tick calculation, exit 0; superseded
  by the stronger source-pin checks in the final result, never overwritten.
- `regressions-1.txt`: earlier nine-regression run, exit 0; retained unchanged.
- `preflight.json`: initial budget calculation, exit 0, with refused admission
  in its result. Final CLI now returns exit 2 so calculation success cannot
  be confused with gate success. This earlier record is retained unchanged.
- `commands.json`, `static-checks.json`, `source-identities.json`, `seal.json`:
  commands/results, final scoped static checks, analyzed verifier/document
  identities, and packet inventory. Seal excludes itself.

Final commands, run from the successor checkout:

```sh
python3 -B tools/flight_demo/m2_rebuild/fixed_preflight.py --references /private/tmp/f65-m2-service-reference
python3 -B -m unittest discover -s tests/flight_demo/m2_rebuild -p 'test_fixed_preflight.py' -v
git diff --check
```

The external reference is read-only Xemu source at
`40dfef0d1d5f56be2469492715c12bdb32c75b67`, not a launched emulator.
Static source hashes and opcode costs are evidence only for that pinned model.
Neither existing host renderer/oracle suites nor target/runtime tests were
rerun: the conditional implementation gate was not reached.

Interpretation: 39,126 cycles bounds the pinned tick's CPU work. The 2,276,912
partial separable design budget is **not** an observed or unavoidable frame
cost. Its 251,912 excess is not a new target timing regression. Unknown work
remains unproven. The actual sealed failed executable retains its independent
755-byte resident deficit and 298,776-cycle cold-frame lower-bound deficit.

See [handoff](../../../reports/M2_FIXED_KERNEL_PREFLIGHT.md) and
[conditional intent](../../../plans/65AERO_M2_FIXED_KERNEL_BUILD_INTENT.md).
