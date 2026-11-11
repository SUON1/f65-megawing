# FC host-only correction evidence

Analysis identity: `65AERO-M2-FIXED-KERNEL-PREFLIGHT-2`.
Baseline: `6c0caa8d453bb647696ef85b5b31b35ef2310def`.
Authority: founder approval of FC-D1–FC-D5; first-failed-gate stop.

The new companion identifies a reachable native-clock rollover discontinuity
in pinned source. This is host arithmetic evidence, not target or emulator
execution. Complete frame scheduling was not reached. See the
[handoff](../../../reports/M2_FIXED_KERNEL_COST_CORRECTION.md).

- `checkpoint-before.json`: 16,582 baseline file size/hash identities.
- `related-before.json`: original preflight, original planning, FC planning and
  failed-wide checkout HEAD/status/diff and dirty-file identities.
- `reference-identities.json`: eight reference files compared with exact Git
  objects at `40dfef0d1d5f56be2469492715c12bdb32c75b67`.
- `initial-commands.json` and `preservation-attempt-1.*`: retained failed use of
  the old scope checker in the new checkout; it rejects the new packet.
- `preservation-before.*`: successful unchanged scope/preservation check from
  the original clean checkout.
- `run-1/sources.tar.gz`: exact new verifier/test source for the first run.
- `run-1/commands.json`: actual commands, working directory, source hashes,
  Python identity and exit codes.
- `run-1/preflight.*`: exit 2, native-clock prerequisite failure; later frame
  gates NOT REACHED, no residual-cycle allowance asserted.
- `run-1/regressions.*`: exit 0, 21 host-only regressions passed.
- Final static/preservation records and `seal.json`: current packet inventory
  and member hashes. The seal does not include itself.

The original 21-file preflight packet, failed target source/artifacts and
accepted results remain unchanged. Two absent historical checkouts remain
NOT VERIFIED at the Git-worktree tier. No recovery is asserted.

No target relink, target instruction execution, Xemu, D81, SD or physical
testing occurred. No runtime grant, production contract or CI gate changed.
