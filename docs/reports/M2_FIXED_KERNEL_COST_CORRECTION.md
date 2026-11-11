# M2 fixed-kernel cost correction — native-clock gate stop

**READY FOR REVIEW — BLOCKED at the first mandatory gate.** Founder approval
of FC-D1–FC-D5 authorized this host-only correction. The new companion verifier
and its 21 regressions are implemented. A reachable native-clock discontinuity
stops the work before publication-window qualification or joint frame scheduling.
No new frame cost, remaining-cycle allowance or runtime admission is claimed.

## Identity and focused changes

- Branch: `codex/65aero-m2-fixed-kernel-cost-correction`, from published
  `6c0caa8d453bb647696ef85b5b31b35ef2310def`.
- Fetched main: `9570f0ab427121a4e8f042041a14c89aaaeff9e2`.
- Analysis identity: `65AERO-M2-FIXED-KERNEL-PREFLIGHT-2`.
- [Approved intent snapshot](../plans/65AERO_M2_FIXED_KERNEL_COST_CORRECTION_INTENT.md)
  is copied byte-for-byte from the planning checkout; its pre-approval wording
  is historical. Founder approval and execution status are recorded here/WIP.
- New [companion](../../tools/flight_demo/m2_rebuild/fixed_schedule_preflight.py)
  verifies the old packet, target inputs and eight pinned reference sources,
  then evaluates the first native-clock prerequisite. It refuses admission
  with exit 2 and leaves subsequent gates NOT REACHED.
- New [regressions](../../tests/flight_demo/m2_rebuild/test_fixed_schedule_preflight.py)
  use independent countdown/update models and temporary fixtures. Original
  verifier, tests, reports, generated contracts and target source are unchanged.
- [New evidence packet](../evidence/flight-demo/2026-11-11-m2-fixed-kernel-cost-correction/README.md)
  retains commands, source snapshots, outputs, identities and preservation.

The preserved executable is still SHA-256
`7fdcea61387c0e6b7ae92310725966ac6c0e29e82e8ba1c9a6be77335af76aad`.
The original preflight seal remains
`77641f1f0aed3d8c993d713e7932350d6d824468ce99e736037bdd4cfb15da72`.
No executable was rebuilt or run.

## First failed gate: native-clock continuity

This is a **source-pinned host arithmetic counterexample**, not an observed
emulator run or a measured missed simulation deadline.

At pinned Xemu revision `40dfef0d1d5f56be2469492715c12bdb32c75b67`:

1. `targets/mega65/mega65.c` supplies 32 ticks to CIA1 at each scanline update
   in both PAL and NTSC.
2. `xemu/cia6526.c`, `cia_tick()`, subtracts those ticks from timer A. At
   `TCA <= 0`, it adds the timer's latch, **65,535**, and decrements linked B.
   At `TCB <= 0`, B also adds its latch, **65,535**. Neither reload adds 65,536.
3. Existing `cfclock_begin()` in
   [combined_platform.c](../../src/diagnostics/r0f/combined_platform.c) force-loads
   both latches to `$FFFF`, starts A and selects linked-underflow mode for B.
4. Existing `cfnow()` accepts coherent register reads and returns the complement
   of the binary `(B << 16) | A` composite. Its extra rejection covers only
   timer-A values `$FFF0–$FFFF`; the witness below is outside that exclusion.

Let `L=65,535` and `x=32n` supplied ticks after `n` CIA updates. The pinned
recurrence gives `A=L-(x mod L)` and `B=L-(floor(x/L) mod L)`. Exact multiples
represent a reloaded value of L, not zero. Since
`L² = 32 × 134,213,632 + 1`, the following states are reachable from reset:

| Quantity | Before update | After one update |
| --- | ---: | ---: |
| CIA update count | 134,213,632 | 134,213,633 |
| Timer A | 1 | 65,504 (`$FFE0`) |
| Timer B | 1 | 65,535 (`$FFFF`) |
| Accepted `cfnow()` | `$FFFEFFFE` | `$0000001F` |

Only **32** CIA ticks elapsed. Unsigned 32-bit timestamp subtraction returns
**65,569**, an excess of **65,537 encoded counts**. Both stable eight-read
sequences pass the actual sampler predicate. This is distinct from ordinary
binary wrap: `$FFFFFFF0 → $00000010` correctly subtracts to 32.

The companion's closed form is checked against two independent host oracles:
literal per-update stepping through the first three A reloads, and an
event-countdown model through 65,535 A expiries around the first B reload.
The latter does not call the closed-form implementation. Normal updates yield
32 encoded counts; a single A reload yields 33; the upper reload causes the
larger discontinuity shown above.

The main loop uses this timestamp for due releases and renderer guard slack.
A normal phase with a future release can consequently be reclassified as
overdue across one scanline update. An unsigned-wrap subtraction alone cannot
prove the unchanged 100 Hz timeline. There is no approved run-duration limit
excluding the reachable upper reload. A short earlier diagnostic is not an
all-phase clock proof. No actual tick loss or execution failure is asserted.

## Gates and deferred scope

| Gate or obligation | Result |
| --- | --- |
| Frozen packet/target/source/reference identities | PASS for inspected inputs |
| First-gate checker and fail-closed regressions | PASS, 21 tests |
| Native-clock continuity across required wrap domain | FAIL in pinned source model |
| Full native-count/CPU uncertainty and release-phase proof | UNPROVEN |
| PAL/NTSC publication-window proof | NOT REACHED |
| Joint tick/wait timeline and residual allowance | NOT REACHED; allowance is null |
| Complete fixed-kernel cost admission | UNPROVEN |
| New resident fit, stack or executable qualification | NOT BUILT / UNPROVEN |
| Target links / runtime executions | 0 / 0 |

FC-D5 stops the task here. Joint tick/wait overlap, window edges/misses,
guard equality, Q16 release phases, consecutive cold/moving generations,
cancellation/publication age and full service-cost regressions were **not
implemented or run**. Their prerequisites did not pass. They are listed as
NOT REACHED in the result, rather than marked covered by the clock tests.

Workload ceilings remain 377 products, 198 divisions and 396 quotient digits.
The 640-tile fallback remains the unconditional allocation demand; 550 tiles
remain conditional on proof. No workload credit or new schedule is inferred.
All missing arithmetic, construction, Platform, scheduler and commit costs
remain explicit unknowns. The original separable 251,912-cycle excess remains
historical accounting, not a newly measured or inevitable frame overrun.

Actual historical resident usage remains **29,426 / 28,671 bytes**, a **755-byte
deficit**, compiler scratch 87 and reserve use zero. The independent historical
cold-frame lower bound remains **2,323,776 / 2,025,000 cycles**, **298,776 over**.
Selected hypothetical retirement 6,935; replacement allowance 6,180; allowance
after 256-byte margin and 104-byte proposed data remains 5,820. No savings or
stack improvements were measured in this task.

## Validation and preservation

Commands run from this worktree, with outputs retained under `run-1/` in the
new packet:

```text
python3 -B tools/flight_demo/m2_rebuild/fixed_schedule_preflight.py --references /private/tmp/f65-m2-service-reference
exit 2: BLOCKED AT FIRST MANDATORY GATE

python3 -B -m unittest discover -s tests/flight_demo/m2_rebuild -p test_fixed_schedule_preflight.py -v
exit 0: 21 tests passed
```

Tests reject changed target bytes, source and each reference, missing/symlinked
references, altered/truncated/extra packet members, unsupported source shapes,
malformed samples and attempts to regrade unknown old costs. Both success and
failure cases compare protected input hashes and use temporary output paths.
Original accepted rendering/oracle and target checks were not rerun.

The initial preservation helper was invoked in the new checkout and correctly
refused the new packet outside its historical allowlist. Its output is retained.
The same unchanged helper then passed in the original clean checkout. No
historical checker or allowlist was modified to accept the new task.

Static syntax, all 22 local documentation links, whitespace and focused scope
checks passed. All 16,582 original published files match; all 16,581 baseline
files outside this new worktree's WIP match. The original packet's 20 sealed
members and six source identities, 16,557 failed-experiment files, four related
checkout identities and all 480 unrelated paths remain preserved. Six available
historical checkouts match their recorded Git status and hashes.

Final static and preservation checks are recorded in the new packet. Two
unavailable historical checkouts remain **NOT VERIFIED at the Git-worktree
tier**; available file hashes are separate preservation evidence. No missing
metadata, historical packet member or old result was reconstructed.

## Handoff

Recommended next task: a separately reviewed, bounded **Platform-owned clock
continuity correction** for the actual chained-timer periods, with independent
tests across both A/B reloads and 32-bit output wrap. Preserve the R0 evidence
implementation; evaluate the correction through the narrow current Platform
clock seam. Then resume native-clock/window qualification before joint frame
accounting. A duration cap would be an explicit alternative contract decision,
not an assumption added to this result. Neither alternative is implemented here.

Inspected authority is the approved FC/FK intent, Phase 1 plan, display commit
contract and extended resident contract/ledger. All new work is host-only:
registers/clobbers, CPU/physical allocations, MAP/B, ports, DMA, IRQ/NMI and
target behavior are unchanged. Precision, public ABI, nine runway segments,
diagnostic camera/telemetry, complete-frame publication, 100 Hz/21 stages,
20 Hz, production `$8000`, development `$9000` and zero reserve remain fixed.
Generated contracts and launch/service grants are unchanged. No commit, push,
PR change, merge, banking, Xemu, D81, SD or physical testing was performed.
