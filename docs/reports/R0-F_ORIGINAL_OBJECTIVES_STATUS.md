# R0-F original-objective status — 2026-09-18

## Scope of this status record

This record consolidates the original bounded R0-F proof objectives. It does
not alter the immutable CF001 D81 release manifest or relabel the later RH001
no-restart development proof as a physical combined result.

The exact CF001 carrier is `F65BLK02.D81`, SHA-256
`b13853a7ddaf3bf26dfcaceb7e4466ab2d58702b96bfcbe9ae62c7db56ed3d82`.
Its SD fill, one-extent audit and safe eject are retained in
`docs/evidence/r0f/combined/physical/2026-09-18/`. The original manifest
remains an immutable pre-physical record; its historical
`AWAITING_HUMAN` fields are not a statement that the later retained physical
evidence does not exist.

## Original objectives

| Objective | Evidence status | Boundary retained |
|---|---|---|
| Compiled-C 45GS02 workload under the R0-F platform conventions | PASS | Private diagnostic fixture, not production CoreRuntime/ABI admission. |
| Safe 128 KiB ROM backup, reclaimed-store workload, byte-verified restore and reprotection | PASS in CF001 Xemu and reported/photographically captured CF001 hardware run | Physical evidence is target-generated result/capture evidence, not an independent physical ROM dump. |
| CIA/raster capture and calibrated synthetic workload | PASS for the bounded CF001 fixture | Hardware values are raw CIA counts and nominal counter-ratio calibration, not traceable SI time or accepted limits. |
| Combined IRQ/DMA/display/PCM-SID/input/snapshot/render/lag/fault/recovery activity | PASS in CF001; complete physical capture reduction also retains corresponding counters | The fixture is synthetic; it is not the complete production renderer, semantic-input, latency, or rolling-window matrix. |
| Machine-readable results, raw pages, host checks, PAL/NTSC Xemu and loadable D81 path | PASS | The exact candidate's original release-state document is retained unchanged; later evidence is linked above. |
| Physical MEGA65 observations and SD integrity/contiguity | PASS for the bounded CF001 evidence: runtime, raw pages, four detected/consumed real edges in the retest, owner-reported sound, matching hash, one extent and safe eject | Audible output and input counts do not establish external latency, every command path, or a complete supported-configuration matrix. |

## Later no-restart objective

The owner later required continuation without restarting or reloading the
application. RH001 proves that returning KERNAL/storage lifecycle separately:
its retained C model advances from tick 33 to 34 after ROM restoration and
verified LOAD/SAVE/reload in NTSC and PAL Xemu. See
`R0-F_RESUME_HANDOFF.md` and
`../decisions/R0-F-RH001-NO-RESTART-HANDOFF.md`.

That proof is **not co-resident with CF001**, is not a physical carrier, and
does not close full R0-F. Folding it into the full combined fixture currently
exceeds the frozen resident-memory range because the pre-C KERNAL snapshot
needs 5,632 bytes while CF001 has only 143 bytes before `$8000`. See
`R0-F_FULL_CLOSEOUT_BLOCKER_2026-09-18.md`.

## Disposition

The original bounded functional-proxy objectives are complete as development
evidence. Full R0-F acceptance is still open: it requires a documented
MemoryAccessABI-compatible solution for the integrated no-restart handoff,
the corresponding exact-carrier Xemu and physical evidence, remaining parent
coverage, and explicit owner acceptance. No measured limit, production ABI,
or parent-spec approval is implied by this status record.
