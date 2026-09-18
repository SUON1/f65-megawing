# Full R0 closure work plan — 2026-09-17

Status: **OWNER SELECTED FULL CLOSURE ON THE CURRENT DESIGN; WORK IN PROGRESS.**

Implementation update: F65R0F5 supplies a post-acquisition raw screen transport
and independent Java importer, with host/static and two exact-D81 Xemu boots
passing. See `docs/reports/R0-F_CAPTURE_HANDOFF.md`. RC-1 calibration is still
open. The owner subsequently supplied the F5 summary and all 22 pages; the
physical byte stream now passes all CRCs and independent Java raw-count
reduction. SD hash/extent/eject also pass; see
`docs/evidence/r0f/capture/physical/REVIEW.md`. No repeat run is requested.
Clock wiring was traced through iomapper, machine and pixel_driver. The
frame-generator PHI producer is now modeled by the host-only
`R0FClockPreflight`; 32 modeled NTSC frames and negative-input checks pass.
Board-clock provenance, independent calibration, uncertainty, complete CIA/bus
semantics and instrumentation overhead remain pending. See
`docs/reports/R0-F_COMBINED_PLATFORM_ADMISSION.md`: the owner subsequently
approved additive proof-platform development. PF-001 now supplies a precise
reset-only qualification contract and C/assembly IRQ/DMA/PCM test implementation;
normal-speed direct-PRG Xemu observations pass. See
`docs/reports/R0-F_PLATFORM_HANDOFF.md`.
CF001 now implements a combined experiment (not a primitive-only replacement):
reset-only verified ROM reclaim/restore, nominal clock-ratio/calibrated C work,
synthetic populated SoA workload, snapshots, complete-buffer display, matrix
edges, SID/PCM and DMA/raster IRQ. See `R0-F_COMBINED_HANDOFF.md` for current
gates and exact identity. The full program remains open: production ROM/storage
return, traceable physical uncertainty, complete parent renderer/input corpus,
per-module/IRQ/rolling-window limits and owner acceptance are not established
by CF001 acquisition. No historical R0-C deferral is silently promoted.

The owner replied `1` to the closeout review's two options, selecting “Finish
the full R0 proof program on the current design.” This resolves the program
direction question. It does not pass a gate, approve candidate parent documents,
freeze measured limits, authorize Phase 1/gameplay, or admit an unspecified
hardware wrapper. Do not ask the owner to choose this direction again.

## Dependency-ordered execution

| Work package | Concrete deliverable and exit evidence | Current state |
|---|---|---|
| RC-1: identity, clock and capture | Resolve displayed core to official source; trace clock generation and timer/cascade/read semantics; specify calibration reference, uncertainty and instrumentation overhead; define reproducible physical raw capture and independent reduction. Reject stopped clocks, wrap/coherence faults, incomplete and corrupted captures. | F5 bounded capture contract, physical export, CRCs and independent raw reduction PASS. Source commit resolved; timer block inspected. Clock-generation chain, calibration/uncertainty, overhead and full wrapper audit remain open. |
| RC-2: protected workload and combined fixture admission | Reconcile R0-B/C/D/E proof identities, owners, memory/stack/cycle budgets and missing contracts against the full parents. Define exact combined fixture, real services, synthetic assets, fault cases and provisional assumptions. Calibrate protected work rather than relabel loop iterations as cycles. | CF001 private contract and reset-only ROM recovery implemented; measured nominal comparison calibration exists. Production storage return, physical uncertainty and full parent fixture remain open. |
| RC-3: implementation and independent host proof | Implement admitted C proof services and measured platform wrappers; generated records/ledgers; Java reference reduction; normal, boundary, overflow, wrap, starvation, shedding and fault tests. Preserve public ABI, owners and reserves. | CF001 integrates populated synthetic workload, snapshots, renderer, IRQ/DMA/PCM/matrix services; native sanitizers and independent Java checks pass. Full parent renderer/input/latency coverage remains open. |
| RC-4: corresponding combined Xemu evidence | Target compile/link, maps/symbols/disassembly, static ownership/ABI checks, host oracles and exact fresh D81 gates; two clean Xemu boots plus required combined phase/window/fault coverage and machine-readable captures. | CF001 compile/link/accounting, host D81 gates, two exact-D81 NTSC and two PAL boots, 2640-sample checks and original-PNG review PASS. This is combined experimental evidence, not all parent phase/window/limit requirements. |
| RC-5: physical matrix and acceptance | Verified SD delivery, chooser/runtime identity, calibrated phase/window captures and raw reduction for the corresponding configuration; input/audio/DMA/IRQ, snapshot/memory/high-water, storage and reserve evidence; owner review of all requirements. | CF001 F65BLK02 candidate and hardware checklist prepared. Exact native blank inspected; SD not written, raw-device sudo password required. Physical chooser/run/raw reduction and acceptance remain pending. |

Measured-limits approval follows accepted R0 evidence as a separate action.
No completion date or number of hardware runs is promised before the fixture
and evidence protocol are defined.

## Initial source audit

### Core identity and timebase

The owner's MEGAINFO photo displays ARTIX `B5C770C6`, dated `2025-09-14`.
On 2026-09-17 the official GitHub commit endpoint resolved that prefix to
[`b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f`](https://github.com/MEGA65/mega65-core/commit/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f),
with matching author date. This is a **candidate source attribution**, not
verification of the installed bitstream bytes or build provenance.

The [CIA source at that commit](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/vhdl/cia6526.vhdl)
exposes `cpuclock` and `phi0_1mhz` separately; Timer A's selected PHI path
decrements when the latter is asserted, and Timer B source `10` consumes
Timer A underflows. Both timer-running blocks are gated by hypervisor mode.
The signal name is not evidence of an exact 1 MHz frequency. Trace its producer,
clock domain and pulse width before deriving time units. Explicitly examine
the delay from A wrapping through its underflow signal to B decrementing when
checking coherent cascade reads. No wrapper defect or correctness conclusion
is established by this initial inspection.

The F4 contract references a different source commit (`e9677ac...`); leave its
build-time record unchanged. A successor needs an explicit comparison against
the source attributed to the tested hardware, not a silent reference swap.
No calibration conversion has been applied to the owner's F4 counts.

### Existing proof components

| Component inspected | Reusable evidence / implementation | Not established |
|---|---|---|
| `src/input/r0b/input_ascii_event.c` | Real `$D610` read/acknowledge probe | End-to-end input latency or loss-free combined edge service |
| `src/audio/r0b/audio_fixture.c`, `src/diagnostics/r0b/final_composite.c` | SID tone setup and repeated service; bounded priority model; R0-B owner heard a tone | Concurrent real audio latency; admitted PCM/DMA start/stop wrapper (R0-B explicitly deferred it) |
| `src/platform/r0b/timing.c` | Read-only modulo-256 raster delta | CPU cycles, calibrated time or wrap-resolved latency |
| `src/diagnostics/r0d/composite.c` | Reproducible 21-stage comparison-work loop | Measured 530000 CPU cycles: the returned value sums declared loop work and the source explicitly disclaims a CPU-cycle budget |
| `src/diagnostics/r0e/composite.c` and F4 timing contract | Deterministic functional proxy and raw-count measurement infrastructure | A full real-service combined workload |

R0-B/D's historical bounded owner acceptances are retained. They are not
revoked, but their labels cannot supply missing measurements to the new proof.
R0-D's source finding makes workload calibration an explicit RC-2 obligation.
This inventory is not permission to copy R0-B routines into a different
MAP/base-page/IRQ/memory context without contract and state review.

## Immediate implementation-readiness checklist

Before the next code/contract edit, complete the repository-required full
architecture reading, current memory/interface/calling-convention review and
relevant subsystem specifications. Then record:

- Exact supported candidate configuration, reference-clock chain and
  calibration/capture method; do not assume Freezer 40 MHz is the CIA rate.
- Proof-only generated records, sample ordering, bounds, overflow/fault rules,
  phase and rolling-window definitions, and independent oracle inputs.
- Each wrapper's registers/clobbers, CPU and physical ranges, mapping/base page,
  IRQ/NMI interactions, DMA ownership, deadline cost and save/restore or reset
  obligations. An F4 reset-only SEI loop is not the combined IRQ design.
- Exact source/toolchain identities, linked budgets and validation commands;
  dynamic measurements must not be replaced with literal zero counters.
- A physical raw-capture path compatible with the existing development →
  Xemu → SD → owner hardware workflow. No network cable, expansion hardware,
  new test equipment or tactical SD access is assumed or required by this plan.

Missing combined clock/capture and PCM/DMA/IRQ contracts remain missing; this
plan does not invent them. DEC-002/DEC-003 and human-owned limits remain formal
acceptance dependencies, not blanket blockers on independent proof work.

## Work split and current handoff

Codex owns source/contract reconciliation, implementation, host/oracle checks,
target accounting and Xemu evidence before issuing a hardware checklist.
The owner supplies hardware actions and human-owned decisions when a specific
ready test or decision is presented. **No SD or MEGA65 action is requested now.**

This kickoff changed documentation only. Registers/clobbers, CPU/physical
memory, MAP/base-page, ABI, IRQ/NMI, DMA, timing/deadline behavior and generated
artifacts: no changes. Existing dirty implementation files were preserved.
Validation: official commit lookup succeeded; source audit is partial and
explicitly not hardware verification; `git diff --check` passed. No target
build, host functional run, Xemu run, D81/SD operation, commit or push in this
kickoff. Next work is RC-1 clock-chain/capture specification and RC-2 admission
reconciliation, not another scope-choice request.
