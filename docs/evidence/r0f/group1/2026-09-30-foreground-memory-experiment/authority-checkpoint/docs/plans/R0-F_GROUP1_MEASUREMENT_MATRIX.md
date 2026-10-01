# Group 1 workload and timing integration

This is the local integration protocol under the already approved Group 1 Build
Intent. Main Concept v1.6 §§4, 6 and 17, Gameplay v1 §21, candidate Runtime v1
§§8 and 19, successor admission and the generated private contracts govern.
It neither changes product thresholds nor closes the whole campaign.

## Acquisition protocol

- One deterministic model advances from tick 1 through 3200. Returning storage
  occurs after tick 1600; tick 1601 is the first measured resumed tick. Model,
  snapshots, held intentions and trace state survive the transition.
- Each side of storage contains sixteen independently released 100-tick
  cohorts. Initial releases sample sixteen offsets of the observed display
  frame. Within a cohort, Q16 releases follow an independent nominal 10 ms
  clock, preserving fractional counts; no tick is skipped, merged or stretched.
- Cohort boundaries deliberately pause acquisition to select another phase.
  They are not represented as continuous ACTIVE_SORTIE execution. Storage
  pauses acquisition and restarts the CIA epoch. No rolling window or SI age
  crosses that discontinuity. The first resumed cohort uses the returning
  path's restart release, without an intervening recalibration or warmup.
- Retain all 3200 fixed-size tick records, every completed-world swap event,
  pre/post 16-frame calibration samples, read/capture costs, final high-water
  and the actual successor result. A separate append-only world log prevents
  two swaps between tick records from losing an age observation.
- Format version 5 retains bounded per-epoch IRQ body-read summaries and
  six-order service-phase masks, and adds bound presentation evidence. Tick
  records are 92 bytes; 16-byte complete-pair events retain the swap timestamp
  without duplicating it in tick records. A maximum of 2000 world events yields
  327172 total bytes inside the admitted 327680-byte allocation. Capacity or
  duration overflow rejects acquisition; no saturation or dropped raw records.
- Instrumentation cost remains included. END precedes CRC/write; the measured
  cost of that capture is retained by the next record (the last cost is in the
  header), and the host adds it to the tick completion. Observed read overhead
  bounds the nominal boundary classification. It is not an independently
  proven physical uncertainty ceiling or traceable SI calibration.

## Requirement/case mapping

| Requirement | Implemented observation / case | Boundary still retained |
| --- | --- | --- |
| Exact stage order and input latch | Guarded stages 1–20 plus actual stage-21 publication; 3200 native stage-order cases; stage-2 input consume | Bounded instruction fixture, not production simulation |
| Combined live workload | Retained nine-aircraft/16-missile/24-projectile/48-decoy, mission/objective, 64-effect and event-queue fixture; additional six full-shape and three reduced-shape aircraft work, two separate 24-track domains | Arithmetic is synthetic; no flight coefficients, radar tables or AI doctrine are invented |
| AI held intentions | Three diagnostic due patterns, output eligible on the following tick, independent final lineage and service counts | Cadences are fixture parameters, not frozen production AI scheduling; complete legal-knowledge/queue-pressure corpus remains separate |
| Tick, stage, publication and service cost | All 21 stage durations, release/start/publication/end timestamps, input/audio/display invocation time; p95/max and overlapping 33-tick elapsed/execution windows | No equal stage slices or new service budgets; invocation time is distinct from external input/audio latency |
| IRQ/DMA contention | Coherent IRQ counts, per-epoch handler-body read intervals and per-record synchronous DMA jobs/max duration during both epochs | CIA read intervals exclude entry/exit tails and entry latency. Pinned Xemu batches CIA updates by scanline: all-zero intervals are unresolved, never a zero-cost claim. Exhaustive relative service phases remain open |
| Clock calibration | 32 read pairs; raw pre/post frame samples, nominal counter ratio, fractional release checks and capture cost | Physical SI reference/uncertainty remains unresolved; emulator timing is not hardware acceptance |
| Phase coverage | Sixteen declared initial offsets in both epochs; every overlapping 33-tick window within each cohort | Sampled phase sweep, not proof of every legal combination of independent service phases |
| Snapshot/world coherence | Immutable held snapshot; incremental clear/scene/copy/completion; complete matching registration/view/buffer pair; superseded-view cancellation, priority anchor eviction, ridge clipping, size-LOD hysteresis and independent per-pair scene CRC | Bounded diagnostic byte pattern, not complete production renderer, physical scanout/pixel readback, directional angle hysteresis or projected terrain/carrier registration |
| World cadence/age | Count complete events inside each measured cohort; nominal cadence, source-publication-to-swap and displayed age distributions | 20 Hz remains the floor; 25/30 Hz remain targets. No maximum age is approved. Cross-storage clock age is explicitly unavailable |
| High-water and reserves | Exercised hardware/software stack canaries, snapshot/event occupancy, actual four-entry anchor/column high-water and drop counts, fixed domain/class occupancy, linker envelope and original reserve CRCs | Exercised fixture high-water is not universal worst-case; remaining geometry/audio/sensor pool instrumentation is not fabricated |
| Storage continuation | One original T02 returning transition; original snapshot invalidation; resumed IRQ/DMA/input/audio/display and independent tick/model/SAVE lineage | Original CAP14 physical evidence is retained; this changed program requires new carrier and hardware gates |

The current thirty corruption cases reject reordered ticks, epoch/phase changes,
release drift, impossible stage totals, snapshot overflow, future world
sources, forged capture cost, broken AI lineage, damaged world events,
registration/view/LOD/anchor changes and CRC/length errors. They
repair the outer CRC where appropriate so a checksum alone cannot earn PASS.
IRQ cases additionally reject a failed reader, missing observations and impossible
aggregates. Integrated capsule, sticky-NMI and reader-error lockout are tracked
in the subsequent IRQ/space checkpoint; a simulated sticky flag is not an
electrical NMI or a proof of arbitrary NMI arrival timing.

## Evaluation policy

The reducer reports acquisition validity separately from nominal timing.
Any observed nominal deadline miss or cohort below the existing 20 Hz floor
produces a timing FAIL. A boundary within the observed read-cost band is
INCONCLUSIVE, not PASS. The cadence interval begins at the first release and
ends at the last completion including capture; count only world events inside
that interval. Report every cohort, not just averages. No 530000-clock tick
allowance, per-service limit, world-age limit or SI accuracy claim is introduced.

## Platform impact

The existing bounded CIA1 coherent reader observes `$DC04-$DC07`; ownership
and restart use the existing `$DC0E/$DC0F` path. The Group 1-only IRQ probes
surround the shared PF handler body after A/X/Y/Z/B preservation and before
restoration. The private bounded assembly reader uses `$DC04-$DC07`, no C
calls, direct page, MAP, DMA or CIA writes. RTI restores interrupted P,
including decimal mode. Ordinary successor/PF builds omit the probes.
C ABI clobbers remain compiler-managed; B=2 and the
admitted PF flat-copy adapter are retained. Existing synchronous DMA and
display/audio/input owners call measurement hooks. No handler calls C. Private
IRQ state is resident and sampled for export only after interrupts stop.

New resident recorder/workload state and a 1024-byte generated CRC table are
charged by the target map. Trace/event data stays within the already approved
Attic range. No reserve borrowing or new physical allocation occurs. Terminal
export retains the approved no-return capsule/staging contract. It runs after
measurement and is excluded from workload deadlines. After restoring entry-time
DOS context, terminal export issues the public device-8 initialize command to
refresh the stale allocation cache before any trace SAVE. It preserves the
one-use original context and immutable separate export capsule; no private DOS
field is patched. Failed refresh stops before export; independent on-disk
chain/BAM/content checks remain mandatory even if KERNAL reports success.

## Closure boundary

The [presentation integration checkpoint](../reports/R0-F_GROUP1_PRESENTATION_INTEGRATION.md)
links the previously isolated kernel into the actual 3200-tick display path.
Its generated capacities, thresholds and scene encoding remain private fixture
parameters, not production limits. Target fit and fresh timing/carrier evidence
are recorded there, including failures and the terminal DOS-cache correction.
The preceding `c249f4e4...` evidence remains immutable. Production projection,
physical scanout, directional angle hysteresis, terrain/carrier registration
and remaining geometry/audio/sensor pools are not established by this slice.

The subsequent [isolated pool-observation core](../reports/R0-F_GROUP1_POOL_OBSERVATION_CORE.md)
qualifies owner-fed counters, synthetic empty/full pressure and isolation on
the host, plus target-object/native-size evidence. It does not close actual
runtime pool observations. Eight observer states need 64 bytes; the cold
retained-code/state fit ends at $C272, 626 bytes over before hooks/transport.
Recover resident space without reserve borrowing before integration and
fresh changed-build timing. The passing presentation PRG/carrier remain intact.

Successful local integration is useful evidence, not full Group 1 or R0-F
acceptance. Before a hardware-ready Group 1 carrier, complete the unestablished
Group 1 rows above, integrated near-capacity trace coverage, a compact success
summary and the exact-name carrier boot gates. Integrated capsule-guard,
simulated sticky-NMI and IRQ-reader-error rejection already passed; they do
not establish electrical NMI timing. Groups 2 and 3, physical measurements
and owner acceptance retain their separate scopes.

The [development transport capacity checkpoint](../reports/R0-F_GROUP1_EXPORT_CAPACITY.md)
passed the 327,680-byte export, final-name collision and one-byte-over
rejection. Those direct-PRG cases qualify the transport boundary; they do not
exercise an integrated 3200-tick trace at the allocation limit or close the
remaining Group 1 rows.
