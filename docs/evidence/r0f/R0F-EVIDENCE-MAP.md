# R0-F Evidence Map

Current development: **CF001 combined experiment**. Contract and current
artifact/test/delivery state: `docs/reports/R0-F_COMBINED_HANDOFF.md` and
`build/r0f/combined/`. This combines actual ROM reclaim/recovery, clock-ratio
measurements, populated synthetic workload and real IRQ/DMA/PCM/matrix services.
Reference classes distinguish Xemu from nominal physical CPU-counter ratios.
Neither class establishes traceable SI time, full production ROM/storage return
or full R0-F acceptance. Previous records below retain their original scope.

Previous development increment: **PF001 platform qualification PRG, not a D81**.
Native sanitized range/CRC tests, target compile/link/static checks and two
normal-speed direct-PRG Xemu boots PASS. The independent Java oracle rejects
316 corrupted/invalid result cases. These observations cover canonical entry,
register preservation under raster IRQ, one real DMA copy and PCM playhead
progress/stop only. Evidence: `platform-qualification/`; handoff:
`docs/reports/R0-F_PLATFORM_HANDOFF.md`. No full combined workload, calibration,
exact-D81 Xemu, SD delivery, physical validation or gate acceptance is claimed.
The earlier table below remains the historical F1 evidence map, not PF001 status.

Current successor: **F65R0F5.D81 — RC-1 raw-capture screen transport**.
Host/static/Java, fresh D81 structure/content, and two clean exact-image Xemu
boots PASS. Evidence: `capture/`; handoff: `docs/reports/R0-F_CAPTURE_HANDOFF.md`.
F5 SD hash/unchanged single extent/safe eject PASS. Owner photos cover the
summary and all 22 pages; all page/full CRCs and independent Java physical
raw-count reduction PASS. See `capture/physical/REVIEW.md`. No calibrated time
or full R0-F acceptance. The prior F4 evidence below remains bounded and is
not inherited as F5 hardware proof.

Current measurement successor: **F65R0F4.D81**, private CIA-count diagnostic.
See `docs/reports/R0-F_CIA_TIMING_HANDOFF.md` and `cia-timing/` for source,
host/Java, exact-image Xemu, and release identities. Physical F4 completion and
displayed platform identities are now observed in four owner photos; see
`cia-timing/physical/R0F4-PHYSICAL-OBSERVATION.md`. F4 SD hash/extent/eject/chooser
chain and physical raw-data validation remain NOT VERIFIED. The release
manifest remains XEMU_BOOT_VERIFIED. Full scope review and remaining obligations:
`docs/reports/R0-F_CLOSEOUT_REVIEW.md`.
F3 was withheld for a source-level serial-mode guard improvement; no F3 carrier
failure or hardware run. F2 safe eject is NOT VERIFIED: owner reported Finder
crashed. Historical entries below do not establish F4 results or R0-F closure.

Previous successor, 2026-09-17: **F65R0F2 startup fix — bounded STATIC/HOST PASS;
two fresh Xemu boots PASS; matching SD hash/extent PASS; physical runtime photo
observed; safe-eject confirmation outstanding.** Evidence and source
identities: `startup-fix/`; handoff: `docs/reports/R0-F_STARTUP_FIX_HANDOFF.md`.
Physical record: `startup-fix/physical/R0F2-PHYSICAL-RUNTIME-2026-09-17.md`.
`R0F-STATIC-STARTUP-001` is corrected for this successor. The table below retains
the F65R0F1 findings and delivery history; none of its physical evidence is
inherited by F65R0F2. Full measurement and owner-acceptance rows remain open.

Historical F1 status: **BOUNDED PROXY HOST, TWO-CLEAN-BOOT XEMU, SD TRANSFER, AND OWNER-REPORTED HARDWARE LOAD PASS; MEASURED-LIMITS ITEMS STILL PENDING.**

2026-09-16 Step 3: current native/compile checks PASS, but static gate BLOCKED
by `R0F-STATIC-STARTUP-001` (KERNAL call after B=$02 without the required thunk).
See `docs/reports/R0-F_STEP3_AUDIT.md` and `step3/2026-09-16/` for retained
results and hashes. Prior boot/load observations do not establish ABI compliance.

2026-09-05: first source rebuild, native sanitizer tests and phase-timeout
injection passed. Result `R0F1 REV1`; no real 100Hz or elapsed-time claim.
Retained host reports are under `docs/evidence/r0f/host/`; handoff is
`docs/reports/R0-F_BUILD_HANDOFF.md`.

| Evidence ID | Required evidence | Current state | Non-claim / blocker |
|---|---|---|---|
| R0F-STATIC-STARTUP-001 | Linked startup conforms to B-register/KERNAL contract | `BLOCKED` | $2035 calls $FFD2 after B=$02; platform resolution and renewed target evidence required. |
| R0F-STATIC-LEDGER-001 | Linked storage and private ledger reconcile | `PASS_BOUNDED_STATIC_ONLY` | Includes 107-byte compiler static stack; dynamic stack high-water and production fit remain unproved. |
| R0F-IDENTITY-001 | Complete pinned MEGA65/core/ROM/HYPPO/Freezer/video/clock/storage/input/capture identity | `AWAITING_PHYSICAL_CAPTURE` | No platform identity may be inferred from R0-E. |
| R0F-CONFIG-001 | Exact R0-E source/configuration reconstruction identity | `PLANNED` | R0-E source `2559e18`; Rev3 carrier is evidence only, never a template. |
| R0F-D81-STRUCT-001 | Fresh one-session R0-F D81 structural validation | `PASS` | F65R0F1.D81; host gate only. |
| R0F-D81-CONTENT-001 | Source/extracted payload hashes | `PASS` | AUTOBOOT.C65, R0F-PROOF, R0F-EVID; exact hashes in host release record. |
| R0F-XEMU-001 | Two clean boots of exact R0-F filename/hash with pinned Xemu/ROM | `PASS` | Fresh R0-F evidence in xemu/evidence.json; no inherited R0-E gate. |
| R0F-SD-001 | Exact SD-copy hash and safe eject | `PASS` | Source pre/post hashes and command output retained in `build/d81-sd-transfer/F65R0F1.D81.slot-pre.json` and `.slot-post.json`. |
| R0F-SD-CONTIG-001 | One raw FAT32 extent before/after slot fill, same offset/length | `PASS` | Pre/post extent `104755200, bytes=819200, count=1` from slot audit JSONs. |
| R0F-CHOOSER-001 | Physical chooser directory and stable identity banner | `PASS` | Owner-reported MEGA65 native load/reported screen includes `R0-F COMBINED-LOAD FUNCTIONAL PROXY` banner and `100HZ / 21-STAGE MODEL: FUNCTIONAL PASS`. |
| R0F-PHASE-001 | Independent 100 Hz simulation/display phase sweep and rolling-window/deadline evidence | `NOT IMPLEMENTED` | No elapsed-time or limit claim. |
| R0F-INPUT-001 | Physical input-latency evidence | `NOT IMPLEMENTED` | R0-E proxy result is not latency evidence. |
| R0F-AUDIO-001 | Physical audio-latency/service evidence | `NOT IMPLEMENTED` | R0-E proxy result is not latency evidence. |
| R0F-SNAPSHOT-001 | Snapshot ownership, age, drops, and high-water evidence | `NOT IMPLEMENTED` | No production snapshot sizing is selected. |
| R0F-FAULT-001 | Deterministic faults, shedding, and reserve proof | `NOT IMPLEMENTED` | No reserve use is authorized. |
| R0F-STORAGE-001 | Storage inactivity/behavior evidence | `NOT IMPLEMENTED` | No production storage decision is selected. |
| R0F-DMA-001 | Separately admitted DMA wrapper and hardware observation | `DMA_HARDWARE_PROBE_NOT_EXECUTED` | No DMA behavior is inferred. |
| R0F-IRQ-001 | Separately admitted IRQ wrapper and hardware observation | `IRQ_MEASUREMENT_NOT_EXECUTED` | No IRQ behavior is inferred. |
| R0F-OWNER-001 | Owner review and explicit R0-F acceptance | `AWAITING HUMAN` | R0-F cannot be passed without it. |

All threshold-free evidence is observation-only for a later measured-limits
revision. This map does not freeze a value or open Phase 1.
