# Platform clock correction — draft publication

**READY FOR REVIEW — NOT FOR MERGE.** The founder approved the Platform clock
correction and normalization-bound fix for commit, push, draft publication and
static CI verification. This checkpoint grants no target execution or admission.

The incremental parent is `5c78bf7d00aadda0e63ce800e27fe3e142c651c0` on
`codex/65aero-m2-platform-clock`. Fetched main remains
`9570f0ab427121a4e8f042041a14c89aaaeff9e2`. The branch retains ten prior
experimental commits and 544 cumulative changed paths before this increment;
the draft against main therefore includes unadmitted ancestry. Prior branches
and draft PRs are preserved. This is not a mergeable clock-only integration.

## Approved scope and evidence

The [clock handoff](M2_PLATFORM_CLOCK_CONTINUITY.md) documents the private
Platform converter, calibration/read consistency and sticky fault handling.
The [P2 handoff](M2_PLATFORM_CLOCK_GAP_P2.md) documents the corrected cap of 12,
divisor/product coverage and fail-closed verifier regressions. Their source,
tests, intent, reports and evidence remain byte-identical to founder review.

- Original packet: 13 members plus seal; seal SHA-256
  `0b0abb69eebb774bbba81203cb9f7b8a990b634c8b1e2968e28af091cc89e593`.
- P2 packet: 16 members plus seal; seal SHA-256
  `59c17610191f1079b7ac076978d70e06b2f70ace1d745eb4ad4f1eeb9742bb3e`.
- Preserved evidence: 11 C host/sanitizer checks, eight P2 Python regressions,
  4,128,705 sampler cases, and the corrected old-image static replay. These
  accepted engineering checks are not rerun for publication.
- Conservative normalization/divide bounds remain 14,191/63,084 cycles; the
  old-image gap remains 728,824,896 native counts. No changed-image timing is
  implied.

The [publication packet](../evidence/flight-demo/2026-11-11-m2-platform-clock-publication/)
preserves the reviewed WIP, all 41 approved file identities and the successful
prepublication preservation result: 16,628 pre-existing identities, six related
checkouts and 480 unrelated paths. WIP alone advances to record publication
authority. Historical checkers retain their original prepublication assumptions;
their sealed inputs and results must not be rewritten for the later Git state.

Publication checks cover exact scope, hashes, syntax, whitespace, artifact
exclusions and Git ancestry. All 16 CI fail-closed fixtures pass. Hosted static
CI must be checked on the pushed draft's exact head; its result is recorded by
GitHub, separately from the retained host/target evidence.

## Unchanged limits and stop

Public ABI, precision, physical ownership, reserve, MAP/B, register/clobber,
DMA, IRQ/NMI and 100 Hz/21-stage contracts are unchanged by publication.
No generated contract changes or new architecture exception are introduced.
The historical 755-byte resident deficit and independent 298,776-cycle cold-frame
deficit remain failures. Changed-image fit, scratch, stack and timing remain
unmeasured. Two unavailable historical checkouts remain **NOT VERIFIED at the
Git-worktree tier**.

Stop at READY FOR REVIEW with the draft NOT FOR MERGE and the exact CI result.
No target relink, runtime/Xemu, D81, SD or physical testing, further engineering
or merge is included.
