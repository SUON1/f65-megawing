# R0-F Execution Plan

2026-09-18 current increment: CF001 combined experiment implemented. See
`docs/reports/R0-F_COMBINED_HANDOFF.md` for actual build/Xemu/delivery state and
remaining full-program requirements. Historical successor descriptions below
are not the current candidate identity. Full R0-F remains open.

RC-1 update: F65R0F5 read-only raw-capture viewer/importer built and host/Xemu
tested; see `docs/reports/R0-F_CAPTURE_HANDOFF.md`. RC-1 calibration and RC-2
combined admission remain open. No physical card action requested now.

Owner selected full closure on the current design by reply `1` on 2026-09-17.
Direction is resolved; current work packages and initial source audit:
`docs/plans/R0_FULL_CLOSURE_WORK_PLAN.md`. The original bounded admission and
historical stages below remain evidence of prior scope, not full acceptance.

Status: **F65R0F4 physical completion observed; full R0-F is not passed.**
Current closeout review: `docs/reports/R0-F_CLOSEOUT_REVIEW.md`. Four original
owner photos and transcribed results are retained under
`docs/evidence/r0f/cia-timing/physical/`. Displayed platform identity is now
partially known; full pinning, calibrated timing, physical raw validation and
the F4 SD delivery chain remain open. Owner direction is now selected; the
combined-harness contracts must be reconciled before target implementation.

Current handoff: `docs/reports/R0-F_CIA_TIMING_HANDOFF.md`. It adds 2,640 raw
timed fixture records, nominal-count release deadlines, 80 phase-started cohorts,
frame-count cross-checks, and independent Java checks. SI calibration, full
sliding-window/phase coverage, actual input/audio/IRQ/DMA and complete physical identity
remain open. The F1/F2 tables below are historical, not the new release record.

2026-09-17 previous handoff: `docs/reports/R0-F_STARTUP_FIX_HANDOFF.md`.
The table below retains the original F65R0F1 stage history; its startup blocker
is corrected in F65R0F2. F65R0F1's hardware observation does not transfer to F65R0F2.

The owner-directed first test build passed native C sanitizer tests and LLVM-MOS
compilation on 2026-09-05. The full measurement obligations below remain pending.
This proxy is not real scheduling, latency, calibration or high-water evidence.

## Scope and invariant inputs

R0-F confirms the bounded, owner-accepted R0-E configuration recorded at source
commit `2559e18`, reconciled on this branch from commit
`97ead74605217df365e17eeb8d38a1d391372688`. Its accepted physical carrier was
`F65R0EG.D81` (`ca85f73ffba93ea290078a60b372406dc6ab58eddacdf0765f7589cea039c40f`),
with `R0E1 REV3` at `$1900-$19FF`. That carrier and every retired R0-E carrier
are read-only evidence, never an R0-F template or payload source.

The R0-E physical result established only the bounded functional proxy and a
read-only raster-low-byte observation. It did not establish CPU cycles,
input/audio latency, elapsed-time percentile/worst values, physical limits,
DMA or IRQ measurements, or platform identity. The Rev3 carrier did not have a
fresh Xemu run; R0-F cannot inherit that missing gate.

## Staged execution

| Step | Deliverable | Status / exit condition |
|---|---|---|
| F0 | Admission, ownership, stage control, test guide, evidence map, interface/ledger impact | Updated for the owner-directed bounded test-code build. |
| F1 | R0-F measurement contract and host oracle | Bounded proxy encoding documented; full calibrated measurement contract and Java oracle incomplete. Prior Step 2 completion wording corrected. |
| F2 | Target diagnostics and any separately admitted platform wrapper | Functional proxy and read-only raster helper implemented; startup ROM call needs platform resolution (`R0F-STATIC-STARTUP-001`); no DMA/IRQ wrapper admitted. |
| F3 | R0-F ledger/interface impact and static/host validation | Executed 2026-09-16: native tests and compile/link PASS; 107-byte compiler static stack now accounted. Audit BLOCKED by startup ABI conflict. See `docs/reports/R0-F_STEP3_AUDIT.md`. |
| F4 | Fresh R0-F D81 construction and host gates | F65R0F1.D81 host structural/content PASS; exact identity in handoff. |
| F5 | Exact-artifact Xemu gate | PASS: two clean boots; pinned identities, matching result blocks and inspected screenshots retained under docs/evidence/r0f/xemu/. |
| F6 | SD byte and contiguity gates | Prior F65R0F1 transfer PASS: exact hash, one pre/post extent at offset 104755200, length 819200, safe eject. No new transfer in Step 3. |
| F7 | Physical chooser, platform identity, and measurement sweep | Owner-reported F65R0F1 load/runtime observed. Full platform identity and measurement sweep remain pending. |
| F8 | Evidence review and owner acceptance | Pending. Report observations without freezing limits; only explicit owner acceptance may close R0-F. |

## Measurement obligations

The R0-F record must identify the MEGA65 revision/model/serial or board identity
when available; core, ROM, HYPPO, Freezer/SD Essentials, video, clock, storage,
input, and capture identities. It must execute an independent 100 Hz
simulation/display phase sweep and retain rolling-window/deadline evidence.
It must include input/audio latency, snapshot ownership/high-water, deterministic
fault/shedding, reserve, and storage inactivity/behavior evidence required by
the admitted fixture.

DMA or IRQ data is not permitted by implication. Until a separately justified
and executed wrapper exists, the exact non-claims are
`DMA_HARDWARE_PROBE_NOT_EXECUTED` and `IRQ_MEASUREMENT_NOT_EXECUTED`.

## Current technical impact

See `docs/reports/R0-F_INTERFACE_LEDGER_IMPACT.md`,
`memory/r0f-memory-ledger.json`, and `interfaces/r0f_proof_contract.json`.
No production ABI, pool or reserve change.

## Required validation commands

Implemented commands (physical command remains gated and was not run):

```sh
git diff --check
sh tools/build/r0f.sh host-test
sh tools/build/r0f.sh build
sh tools/build/r0f.sh audit
sh tools/build/r0f.sh package
python3 tools/diagnostics/r0f_d81_loadability_gate.py . build/r0f/F65R0F1.D81
sh tools/build/r0f.sh xemu
sudo tools/diagnostics/d81_sd_fill_mega65_slot.sh SOURCE.D81 /Volumes/MEGA65FDISK EXPECTED_SHA256
```

`package` refuses an existing carrier filename. Never delete or rename it to
bypass that guard. The final
physical command requires administrator authentication, an owner-created slot,
and physical SD-card movement; it is intentionally not run autonomously.

`audit` rebuilds the target, reconciles the private ledger, checks linked startup,
and revalidates retained Xemu result bytes without operating on a D81. It now
passes for the bounded startup fix. Current outputs are in
`build/r0f/startup-fix/`; `package` assigns only F65R0F2.D81 and refuses to
overwrite it. Full measurement-contract gates remain open; this follow-up is
the owner-directed correction/retest of the bounded proxy only.
