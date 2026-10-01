# Group 1 resident recovery, IRQ observations and failure checks

The approved Group 1 workload/timing continuation now has passing host,
target, NTSC/PAL acquisition and integrated fault-handling checks. **Failure
screen presentation remains unresolved.** This checkpoint is not a delivery
carrier, complete Group 1 coverage or full R0-F acceptance.

## Changes and governing boundaries

Main v1.6, candidate Runtime v1 §8, the approved Group 1 Build Intent and the
successor/export contracts and ledgers govern. No product threshold or physical
allocation changed. No reserve was borrowed.

- Group 1 omits CAP14's photographic page viewer and uses a compact lockout
  screen; successful runs use terminal file export. The ordinary CAP14 program
  retains its viewer and remains byte-identical.
- Private assembly probes surround the PF IRQ body after A/X/Y/Z/B preservation
  and before restoration. The shared handler retains raster acknowledgment,
  counters and register restoration. The ordinary build omits the probes.
  The bounded coherent reader uses `$DC04-$DC07`, private resident scratch,
  no C calls, direct page, MAP, DMA or CIA writes. RTI restores interrupted P.
  Read exhaustion and count/total/duration overflow reject acquisition.
- Generated trace version 3 adds count, total and maximum body-read interval
  per epoch in reserved header space. Trace allocation, record/event geometry
  and capacity are unchanged. Metrics cover declared cohorts before and after
  storage and are copied after IRQ shutdown. Instrumentation remains included
  in workload execution; read boundaries exclude IRQ entry/exit tails.
- An integrated sticky-NMI negative exposed generic pre-storage fault 86
  replacing fault 90. Group 1 now retains the first observed fault. This does
  not change the predecessor's path.
- Terminal failure presentation uses the admitted HUD `$040000`, 2000 white
  color cells at `$0FF80000` and restored-ROM font `$02D000`. It clears HOTREG
  (`$D05D` bit 7, preserving border bits) before explicit screen/font pointers
  and final `$D011` display enable. This prevents a verified legacy pointer
  recalculation. These changes occur after acquisition with no return to work.
  They introduce no MAP/base-page, DMA or IRQ/NMI ownership change.

## Current verified binary and measurements

PRG: **36,473 bytes**, SHA-256
`ec259fc7611d8bb5809d15f6c333f5b224df4c945a8e9ffca5b2402d8444cb30`.
Resident end `$BAAB`: **1365 bytes free**, versus 471 at the preceding workload
checkpoint. Protected terminal code/data remains below `$4000`; allocations
are unchanged. Exercised stack high-water is 76 hardware / 85 software bytes.
Generated C/assembly trace bindings and the CRC table are current.

| Run | Ticks | Nominal misses / cohorts below 20 Hz | World cadence | IRQ samples before / after |
| --- | ---: | --- | --- | --- |
| `irq-ntsc-07` | 3200 | 0 / 0 | 29.05–30.12 Hz | 933 / 928 |
| `irq-pal-06` | 3200 | 0 / 0 | 24.11–25.12 Hz | 782 / 782 |

Actual exported traces and returning SAVE files pass independent reduction.
Both traces reject all 18 corruption cases, including mutations with repaired
outer CRCs. The first resumed tick and all sixteen post-storage cohorts are
retained; the storage clock discontinuity is not represented as continuous SI.

**IRQ interval resolution remains unresolved.** All body-read intervals are
zero. The pinned emulator advances CIA1/2 by 32 counts after a scanline CPU
batch: see [pinned `mega65.c`, lines 728–736](https://github.com/lgblgblgb/xemu/blob/40dfef0d1d5f56be2469492715c12bdb32c75b67/targets/mega65/mega65.c#L728).
The reducer reports `NO_NONZERO_INTERVAL_OBSERVED`, not zero IRQ cost or PASS
for whole-ISR cost, entry latency or physical timing. Probe overhead and the
unmeasured tails remain explicit.

| Integrated negative | Result |
| --- | --- |
| Capsule leading guard corruption (`capsule-negative-06`) | Fault 107, lockout, zero export, unchanged disk |
| Sticky NMI flag (`nmi-negative-06`) | Fault 90 retained, NMI=1, lockout, zero export, unchanged disk |
| IRQ reader error (`irq-read-negative-07`) | Fault 107 at tick 3200, zero export, returning SAVE valid |

These are exact-byte-checked disposable PRG derivatives. Sticky flag injection
is not an electrical NMI or proof of arbitrary NMI arrival timing.

## Open presentation defect and retained diagnosis

The early failure screenshot is complete, but the regular late-failure
screenshot displays numeric fields without labels. A terminal register-snapshot
derivative displays the full late screen. Screen text/font bytes match, and
terminal VIC registers match apart from live raster counters. The HOTREG fix
is retained because the earlier register capture demonstrated actual pointer
replacement when display was enabled.

A subsequent `$D031` attribute-disable experiment did not resolve the issue:
its late screenshot was complete but early screenshots lost labels. Reading
actual color RAM found all 2000 cells equal to 1, so inherited blink attributes
are not established as the cause. That speculative attribute change was removed;
rebuilding reproduced the verified binary above exactly. The experimental
36,481-byte `2ff73192...` binary and its passing acquisition/fault checks remain
retained under the evidence directory's `final/` subdirectory, **superseded
regardless of that historical directory name**.

The first broad register diagnostic reused the live IRQ-reader space and
stopped during initialization; its register data is not terminal-state evidence.
The corrected diagnostic used an isolated stub in free resident space and
replaced only the final display-enable store. A visible-window attempt could
not be inspected through the available app interface and timed out during
shutdown; it provides no visual verification. All attempts are retained.

No operator-presentation completion or hardware readiness is claimed. Resolve
this with a controlled display/readback diagnostic before the operator/carrier
gate; avoid further guessed target changes. The presentation issue does not
invalidate independently extracted trace/SAVE or fault-state evidence.

## Validation commands and evidence

Commands run from the repository root:

- `python3 -B tools/diagnostics/r0f_group1_integration.py` — target link,
  map/protected bounds, terminal and IRQ static checks PASS. After removal of
  the attribute experiment, the exact current PRG was reproduced.
- `python3 -B tools/diagnostics/r0f_group1_host_validate.py` — ASan/UBSan,
  3200 stage/input/AI cases and 1025 streaming CRC lengths PASS.
- `python3 -B -m unittest discover -s tools/diagnostics -p test_r0f_group1_contract.py -v`
  — seven geometry/overlap tests PASS.
- `python3 -B tools/diagnostics/r0f_successor_integration.py build` — predecessor
  host/Java/IRQ/capture/CF001/RH001/target regressions PASS. Ordinary PRG SHA:
  `cf605bd377ddcee2c72cdc4abfd20c3ae9eee350b7b78b36cbde8ff1adf8fc23`.
- `python3 -B tools/diagnostics/r0f_group1_run.py --out build/r0f/group1/integration/irq-ntsc-07 --mode 1`
  and `irq-pal-06 --mode 0` — actual trace/SAVE PASS.
- `python3 -B tools/diagnostics/test_r0f_group1_reduce.py build/r0f/group1/integration/irq-ntsc-07/trace.bin`
  and PAL equivalent — all 18 corruptions rejected per trace.
- `python3 -B tools/diagnostics/r0f_group1_negative.py --case capsule-guard --out build/r0f/group1/integration/capsule-negative-06`
  and `nmi-sticky` / `nmi-negative-06`, `irq-read-error` /
  `irq-read-negative-07` — lockout/zero-export PASS; visual limits above.
- `python3 -B tools/diagnostics/r0a_validate.py .`, current input hashes,
  Group 1 Python syntax and `git diff --check` — PASS.

[Evidence index and manifest](../evidence/r0f/group1/2026-09-29-irq-display/README.md)
retain source/binary identity, current runs, failed experiments and pinned
emulator excerpts. Prior workload/IRQ/font freezes are unchanged, as are all
285 older evidence files in the prebuild dirty-file manifest. Earlier baseline
checks also verified 1521 retained evidence files; no tested disk was changed.

## Remaining approved work

Independent-service phase coverage; declared view/registration/occlusion/LOD
and applicable pool observations; full-capacity transport qualification;
operator presentation; and exact-name carrier gates remain open. Whole-ISR
cost, entry latency and physical SI uncertainty remain unproven. The
[measurement matrix](../plans/R0-F_GROUP1_MEASUREMENT_MATRIX.md) preserves
these boundaries. No SD write, physical run, commit or push occurred.
