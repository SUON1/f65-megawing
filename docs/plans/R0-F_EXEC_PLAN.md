# R0-F Execution Plan

Status: **First bounded functional/raster slice implemented; F65R0F1.D81 is
HOST_CONTENT_VERIFIED. Xemu blocked; R0-F is not passed.**

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
| F1 | R0-F measurement contract and host oracle | Private proxy encoding implemented. Full measurement contract and Java oracle pending. |
| F2 | Target diagnostics and any separately admitted platform wrapper | Functional proxy and read-only raster helper implemented; no DMA/IRQ wrapper. |
| F3 | R0-F ledger/interface impact and static/host validation | Native tests, compile/link and accounting pass; dynamic high-water unmeasured. |
| F4 | Fresh R0-F D81 construction and host gates | F65R0F1.D81 host structural/content PASS; exact identity in handoff. |
| F5 | Exact-artifact Xemu gate | Pending. Two clean boots with pinned Xemu/ROM identity, captured screen/result block/hashes. Stop at `NOT VERIFIED` if unavailable. |
| F6 | SD byte and contiguity gates | Pending owner/admin/card action. On a fresh MEGA65 `NEW D81 DD IMAGE` root slot, use only `d81_sd_fill_mega65_slot.sh`; prove exact hash, one extent before/after at the same device offset/length, and safe eject. |
| F7 | Physical chooser, platform identity, and measurement sweep | Pending MEGA65 operation/capture. Record platform identity before interpreting results; chooser pass precedes runtime testing. |
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
sh tools/build/r0f.sh package
python3 tools/diagnostics/r0f_d81_loadability_gate.py . build/r0f/F65R0F1.D81
sh tools/build/r0f.sh xemu
sudo tools/diagnostics/d81_sd_fill_mega65_slot.sh SOURCE.D81 /Volumes/MEGA65FDISK EXPECTED_SHA256
```

`package` refuses an existing carrier filename. Never delete or rename it to
bypass that guard. The final
physical command requires administrator authentication, an owner-created slot,
and physical SD-card movement; it is intentionally not run autonomously.
