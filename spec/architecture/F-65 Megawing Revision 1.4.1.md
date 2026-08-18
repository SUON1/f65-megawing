
# F-65 Megawing  
## Revision 1.4.1 — Architecture Invariants and Documentation Update

**Status:** Frozen architecture baseline  
**Supersedes:** Revision 1.4  
**Nature of update:** Documentation-only additions. No architecture, budget, capacity, milestone, or gameplay requirement has changed.

---

## 1. Preserved product baseline

Revision 1.4.1 retains the complete Revision 1.4 product and architecture:

- Retro-synthwave heavy fleet-interceptor game for the MEGA65.
- All production game code written in 45GS02 assembly.
- Cockpit-primary presentation with a low-cost chase view.
- Bubble canopy, green monochrome HUD, automatic RIO radar repeater, and grayscale aircraft-status display.
- Aviation-facing units: nmi, knots, feet, lb, lbf, lb/hour, psi, and G.
- Positive-G desaturation beginning near +6 G and reaching grayscale near +7 G.
- F-65A with two engines, ten missiles, cannon, fuel, electrical, hydraulic, radar, jammer, RWR, countermeasures, and damage simulation.
- One-button Deck, TFL, Normal Flight, and Combat contexts.
- Meridian Maritime Compact versus Boreal Directorate.
- Midnight Spear vertical slice followed by the ten-operation campaign and two endings.
- One independently bootable MVP D81; multi-D81 campaign permitted.
- Absolute R0 hardware-measurement gate.
- Hard Phase 1 integrated-engine-harness gate.
- Engine-first Phase 0–5 development order.

No new missions, weapons, aircraft, mechanics, or current-scope content are introduced by Revision 1.4.1.

### 1.1 Primary feel and presentation inspirations

The following titles define the intended player-facing character:

- Chuck Yeager’s Advanced Flight Trainer.
- Bruce Artwick’s early flight-simulator lineage.
- Early subLOGIC and Microsoft Flight Simulator.
- **A-10 Cuba!**
- **F/A-18 Korea**
- **Falcon 3.0**

A-10 Cuba!, F/A-18 Korea, and Falcon 3.0 specifically inform:

- Density of simulated aircraft systems.
- HUD language and information hierarchy.
- Radar and systems-display presentation.
- Combat tempo.
- Mission pacing.
- Early-1990s combat-flight-simulator character.
- The balance between accessibility and consequential systems.

These are feel and presentation references. They do not override MEGA65 constraints, create feature requirements, or alter the architecture.

---

## 2. Memory Access ABI

The official MEGA65 map provides 384 KB of fast chip RAM at physical addresses `$0000000–$005FFFF`, 32 KB of color RAM at `$FF80000–$FF87FFF`, and normally 8 MB of Attic RAM at `$8000000–$87FFFFF`. Attic RAM must be staged for consumers that cannot access it directly. These facts and MAP behavior are verified against the pinned [MEGA65 Chipset Reference](https://files.mega65.org/files/m/mega65-chipset-reference_cnFcKB.pdf).

### 2.1 Canonical physical ownership map

| Physical range | Size | Owner |
|---|---:|---|
| `$000000–$00FFFF` | 64 KB | Resident executable, base page, stack, vectors, scheduler, hot state |
| `$010000–$017FFF` | 32 KB | Active simulation, entities, systems, radar, and tactical state |
| `$018000–$01BFFF` | 16 KB | Audio state, mission hot data, queues |
| `$01C000–$01CFFF` | 4 KB | Display pointer tables and display-control records |
| `$01D000–$01FFFF` | 12 KB | Shared scratch and transient CPU workspace |
| `$020000–$02FFFF` | 64 KB | Display pixel/glyph store A |
| `$030000–$03FFFF` | 64 KB | Display pixel/glyph store B |
| `$040000–$047FFF` | 32 KB | Cockpit, HUD, MFD, sprite, and palette assets |
| `$048000–$04FFFF` | 32 KB | Renderer edge, clipping, bucket, and span workspace |
| `$050000–$057FFF` | 32 KB | Resource staging and DMA lists |
| `$058000–$05FFFF` | 32 KB | Measured-limits reserve |

The `$020000–$03FFFF` region is reclaimed from ROM-emulation storage through the documented hypervisor mechanism. After game handoff, ROM routines are not callable unless the platform layer explicitly restores their required environment.

The post-R0 measured-limits revision may reassign ownership inside these ranges. It may not change the public memory ABI without a numbered architecture revision.

### 2.2 Canonical CPU-visible map

| CPU range | Canonical state |
|---|---|
| `$0000–$00FF` | CPU ports and reserved compatibility bytes |
| `$0100–$01FF` | Hardware stack |
| `$0200–$02FF` | Relocated game base page |
| `$0300–$1FFF` | Scheduler, IRQ mailboxes, and hot state |
| `$2000–$7FFF` | Resident code and hot constant tables |
| `$8000–$9FFF` | Temporary MAP window 0, normally restored to bank-0 RAM |
| `$A000–$BFFF` | Temporary MAP window 1, normally restored to bank-0 RAM |
| `$C000–$CFFF` | Resident platform and interrupt code |
| `$D000–$DFFF` | MEGA65 I/O personality |
| `$E000–$FFFF` | Critical code, interrupt handlers, and vectors |

Every public routine assumes and restores:

- MAP offsets cleared.
- MAP/EOM sequence complete.
- `$01 = $35`.
- MEGA65 I/O personality selected.
- Base page at `$0200–$02FF`.
- No cartridge or ROM overlay.
- Interrupt vectors resolving to resident bank-0 code.

### 2.3 MAP ownership

Only `MemoryAccessABI` may execute MAP or relocate base page.

- Temporary MAP operations may alter only `$8000–$BFFF`.
- Mapping may not cover resident code, stack, base page, I/O, or vectors.
- Mapping scopes save processor status, disable IRQs, install the map, complete EOM, perform bounded work, restore the canonical map, complete EOM, and restore status.
- Public calls, callbacks, scheduler yields, and DMA waits are forbidden inside mapping scopes.
- Mapping scopes cannot nest.
- IRQ handlers never change MAP.
- No gameplay NMI source is enabled.
- Public routines restore base page to `$0200`.

### 2.4 Pointer and resource representations

`FarPtr32`:

- Four-byte little-endian physical address.
- Bits 0–27 contain the address.
- Bits 28–31 are zero.
- Zero is null.
- Contains no type, flags, or MAP-window state.

`ResourceHandle16`:

- `$0000–$FFFE`: resource-directory index.
- `$FFFF`: invalid.
- Stable across runtime relocation.

A fixed 16-byte directory entry contains source address, encoded and decoded sizes, resource type, residency, alignment, version, and integrity data.

### 2.5 DMA rules

- DMA uses normalized physical addresses, never CPU-window addresses.
- MAP state does not alter DMA addresses.
- Every range is validated before submission.
- I/O, hypervisor, reserved, and color-RAM access requires an explicit whitelist.
- Attic/chip transfers are owned by the resource manager.
- DMA lists remain resident and immutable until completion.
- Only the DMA manager submits production jobs.
- All jobs obey measured audio/input latency bounds.

### 2.6 R0-A deliverable

`MemoryAccessABI` must provide:

- Canonical-map setup and assertions.
- Scoped MAP-window proof.
- Base-page restoration tests.
- Far-pointer tests.
- Resource-directory validation.
- Physical DMA copy/fill tests.
- IRQ-latency measurement.
- Xemu and hardware verification.

---

## 3. Deterministic execution semantics

### 3.1 Simulation clock

- Simulation runs at exactly 100 Hz.
- `SimulationTick` is unsigned 32-bit and monotonically increasing.
- Every command and event contains its originating tick.
- Tick wrap is a fatal invariant violation.
- PAL/NTSC timing and presentation cadence cannot change results for identical tick-tagged inputs.

### 3.2 Exact tick order

1. Increment `SimulationTick`.
2. Latch `InputCommandFrame`.
3. Apply queued commands and prior-tick directives.
4. Update environment and carrier motion.
5. Resolve electrical, fuel, engine, and hydraulic supply.
6. Run control laws and stability augmentation.
7. Apply actuator authority, rates, damage, and asymmetry.
8. Sample atmosphere and calculate forces.
9. Integrate aircraft motion.
10. Resolve terrain, runway, deck, and arrestment contact.
11. Accept weapon requests and create pending spawns.
12. Integrate existing weapons and countermeasures.
13. Detect collision, fuze, and damage events.
14. Accumulate and apply damage deterministically.
15. Update radar truth, returns, tracks, RWR, and warnings.
16. Run scheduled RIO and enemy AI; new commands apply no earlier than the next tick.
17. Update mission objectives and scoring.
18. Commit despawns and spawns.
19. Derive cockpit, warning, and audio events.
20. Calculate checksums.
21. Atomically publish `SimulationSnapshot`.

Presentation sees only the last completed snapshot.

### 3.3 Simultaneous events

- Sort by event class, source handle, target handle, then producer sequence.
- Commands valid at tick start execute before damage generated in that tick.
- Mutual kills are possible.
- Component damage accumulates before capability recalculation.
- Freed slots cannot be reused before lifecycle commit.
- New entities begin updates on the next tick.
- Presentation order cannot affect simulation order.

### 3.4 RNG

Simulation uses defined 32-bit `xorshift32`:

```text
x ^= x << 13
x ^= x >> 17
x ^= x << 5
```

- Operations wrap as unsigned 32-bit.
- Zero seed becomes `$6D2B79F5`.
- Mission seed is stored in replay and save records.
- Mission, AI, sensor, and valid-hit damage streams are independent.
- Entity AI uses entity-local streams.
- Presentation RNG is separate and cannot affect simulation.
- RNG cannot turn a failed physical intercept into a hit.

### 3.5 Arithmetic

- Angles intentionally wrap at 16 bits.
- RNG intentionally wraps at 32 bits.
- Physical state never silently wraps.
- Intermediates widen before narrowing.
- Out-of-range physical results saturate and increment diagnostics.
- Divide-by-zero saturates and records an invariant fault.
- Debug builds stop on unexpected saturation.
- Release builds remain deterministic and record the fault.
- Rounding is contract-defined.

### 3.6 Overrun behavior

Simulation ticks are never skipped, merged, or assigned variable duration.

If execution falls behind:

1. World rendering yields.
2. Decorative presentation is suppressed.
3. The last completed world buffer remains displayed.
4. Simulation, input, audio, HUD, and critical warnings continue.
5. Tick debt is processed without reordering.
6. Debt exceeding eight ticks triggers a controlled performance pause and timing fault.

---

## 4. Coordinate and reference frames

### 4.1 World frame

Right-handed North-East-Down:

- `+X`: north.
- `+Y`: east.
- `+Z`: down.
- World up: `(0,0,-1)`.
- Heading zero: north.
- Positive heading/yaw: clockwise toward east.
- Positive pitch: nose up.
- Positive roll: right wing down.

### 4.2 Body, radar, missile, and camera frames

Aircraft and missiles:

- `+X`: forward.
- `+Y`: right.
- `+Z`: down.

Radar:

- Boresight: `+X`.
- Positive azimuth: right.
- Positive elevation-down: `+Z`.
- Field of regard: `−85°…+85°`.

Camera:

- `+X`: screen right.
- `+Y`: screen down.
- `+Z`: forward.

### 4.3 Terrain and carrier

Terrain coordinates increase north then east. Elevation is positive upward and converts to negative world Z.

Carrier deck:

- `+X`: bow.
- `+Y`: starboard.
- `+Z`: down.
- Deck plane: local `Z=0`.

The carrier moves deterministically in translation and heading. MVP excludes wave-driven heave, pitch, and roll. Secured aircraft inherit carrier motion.

### 4.4 Position format

`WorldPosition` is 16 bytes:

- Signed 16-bit north sector.
- Signed 16-bit east sector.
- Unsigned 24-bit north local.
- Unsigned 24-bit east local.
- Signed 24-bit altitude.
- Three reserved bytes.

Internal sector size is 65,536 metres; local precision is 1/256 metre.

This provides approximately 0.154-inch resolution, at least 13 units across the two-inch contact tolerance, approximately ±107,500 ft of altitude, and operational extent far beyond campaign requirements.

Camera-relative calculations use signed 32-bit intermediates after sector rebasing. Carrier contact uses signed 24-bit local coordinates at 1/256 metre.

---

## 5. Entity identity and lifecycle

### 5.1 `EntityHandle`

Four bytes:

- Entity type.
- Pool index.
- 16-bit generation.

Zero is invalid. Type and generation zero are reserved. Stale generations fail validation.

### 5.2 Capacity envelope

| Pool | Capacity |
|---|---:|
| Aircraft | 16 |
| Ships and carriers | 8 |
| Surface radar/SAM entities | 16 |
| Guided missiles | 32 |
| Gun projectile groups | 32 |
| Chaff/flare entities | 64 |
| Dynamic mission entities | 32 |
| Simulation-relevant effects | 32 |
| Presentation effects | 64 |
| Radar truth contacts | 32 |
| Radar tracks | 24 |
| RIO priority tracks | 4 |
| Active objectives | 16 |

Static terrain and scenery are resources, not entities.

### 5.3 Lifecycle

- Allocation uses the lowest free index.
- Despawns commit in ascending handle order.
- Spawn requests sort by class priority, requester, and sequence.
- Despawns commit before allocations.
- Slots become reusable only at commit.
- New entities update on the next tick.

Pool exhaustion:

- Required mission-entity exhaustion is a validation failure.
- Missile exhaustion rejects release without consuming the weapon.
- Gun-group exhaustion rejects the shot without consuming ammunition.
- Presentation effects are dropped and counted.
- Track exhaustion evicts the lowest-scoring nonpriority coasting track.
- Pools never grow dynamically.
- Live gameplay entities are never silently replaced.

---

## 6. CPU and timing ledger

### 6.1 World rendering

World rendering is incremental and resumable.

- Work yields at object, face, span-batch, or DMA-batch boundaries.
- Only complete buffers are displayed.
- The previous complete buffer remains visible if a new world frame is unfinished.
- HUD, cockpit, input, audio, warnings, and simulation have independent deadlines.

### 6.2 Synthetic-load definition

The R0-D protected workload is exactly 530,000 clocks per nominal two-display-frame world period.

It represents all protected non-render work. It is not a per-tick or per-display-frame value.

Production reporting also uses a six-NTSC-frame superperiod, containing exactly ten simulation ticks. PAL headroom cannot increase the NTSC-derived scene limits.

### 6.3 Two-frame NTSC ledger

| Class | Ceiling |
|---|---:|
| Protected non-render workload | 530,000 clocks |
| Protected HUD/cockpit/display service | 100,000 clocks |
| Incremental world rendering | 585,000 clocks |
| Mandatory reserve | 135,000 clocks |
| **Total** | **1,350,000 clocks** |

### 6.4 Deadline protection

- Simulation: fixed 100 Hz.
- Input: every display frame, converted to tick-tagged commands.
- Audio: every display frame or required interrupt interval.
- HUD and critical warnings: every display frame.
- Radar and systems displays: scheduled lower rates with immediate critical updates.
- World rendering: remaining time only.
- DMA: measured latency bounds.
- A 20 Hz world cadence is a failure floor, not permission to alter simulation.

---

## 7. Flight-control and actuator layer

Pipeline:

```text
InputCommandFrame
→ pilot-command normalization
→ control law / stability augmentation
→ FlightControlFrame
→ hydraulic authority and actuator limits
→ ControlSurfaceState
→ aerodynamic model
```

### `FlightControlFrame`

Fixed 16-byte record containing normalized pitch, roll, yaw, speed-brake and wing-sweep commands; Assisted/Manual mode; G/AoA limiting flags; control-law flags; and source tick.

### `ControlSurfaceState`

Contains actual pitch, roll, rudder, flap, speed-brake, and wing-sweep positions plus actuator authority/rate flags.

Rules:

- Assisted and Manual modes exist in the control-law layer.
- Manual mode cannot bypass hydraulics.
- G and AoA limiting occur in the control-law layer.
- Hydraulics control authority and rate.
- Damage can create reduced, stuck, floating, or asymmetric surfaces.
- Aerodynamics consume actual surface state, never raw input.

---

## 8. System-state representation

Every major system has an eight-byte `SystemState`:

| Field | Type |
|---|---|
| `health` | `u8` |
| `supplied_power` | `u8` |
| `commanded_mode` | `u8` |
| `actual_capability` | `u8` |
| `fault_reason` | `u16` |
| `flags` | `u8` |
| `reserved` | `u8` |

Subsystem measurements such as voltage, pressure, RPM, and fuel are stored separately.

The dependency graph defines required sources, minimum capability, commanded mode, output capability, fault propagation, and deterministic evaluation order. Feedback paths use explicit arbitration nodes.

Green, yellow, red, and gray are presentation results derived from structured state. They are never primary simulation state.

---

## 9. Palette-role registry

| Range | Role |
|---|---|
| `$00` | Background/transparent zero |
| `$01–$0F` | Neutral grayscale and text |
| `$10–$17` | HUD green |
| `$18–$1F` | Friendly green |
| `$20–$27` | Unresolved yellow |
| `$28–$2F` | Hostile red |
| `$30–$37` | Caution |
| `$38–$3F` | Failure/critical |
| `$40–$7F` | Sky, ocean, and terrain |
| `$80–$9F` | Cockpit |
| `$A0–$BF` | Aircraft and world objects |
| `$C0–$DF` | Effects |
| `$E0–$EF` | Radar and systems neutrals |
| `$F0–$F7` | Essential standby cues |
| `$F8–$FF` | Reserved/debug |

Every role defines normal color, luminance, grayout stages, allowed asset classes, and protection status.

Assets cannot use arbitrary indices. The compiler rejects unauthorized use or missing grayout mappings. Critical identity also uses shape, text, outline, or luminance.

---

## 10. Host references and instrumentation

### 10.1 Reference models

Host tools provide:

- Bit-exact fixed-point target models.
- High-precision accuracy oracles.

They cover mathematics, conversions, atmosphere, transforms, flight controls, actuators, flight components, RIO scoring, missile integration, RNG, lifecycle, and system dependencies.

### 10.2 Golden vectors

Minimum suites:

- 10,000 cases per math primitive.
- 10,000 atmosphere/conversion cases.
- Numeric boundaries for every format.
- 1,000 control/actuator sequences.
- 1,000 flight sequences.
- 1,000 RIO scenarios.
- 1,000 missile trajectories.
- Pool, generation, and stale-handle cases.
- MAP, far-pointer, and DMA boundaries.

Target code bit-matches the bit-exact model unless a contract defines an approved LSB tolerance.

### 10.3 Instrumentation

Track:

- Stack/base-page high-water marks.
- Pool and queue occupancy.
- Drops and exhaustion.
- Invalid handles.
- Arithmetic saturation.
- Transform/clipping overflow.
- MAP duration and misuse.
- DMA stalls.
- Missed render deadlines.
- Simulation debt.
- Radar-track transitions.
- RIO score components.
- Audio preemption and latency.
- Resource transitions.
- Snapshot age.

---

## 11. Expanded R0-A identity

R0-A pins:

- Hardware revision.
- FPGA core version and hash.
- ROM version and hash.
- System-files version and hash.
- Video standard and output configuration.
- Official documentation versions and hashes.
- Java and assembler versions.
- Xemu build and configuration.
- Host-tool versions.
- Game source/build hash.
- D81 hash.
- Benchmark-scene hash.

Reports without the complete identity are nonauthoritative.

R0-A cannot pass without `MemoryAccessABI`, mapping assertions, opcode proof, reproducible boot, symbols, listings, profiling, and benchmark identity.

---

## 12. Early contracts retained for later phases

### Resource residency

States:

- Unloaded.
- Disk-known.
- Attic-resident.
- Chip-resident/staged.

Only the resource manager changes residency. Consumers retain handles.

### Save serialization

- Versioned field-wise chunks.
- Explicit endianness and widths.
- No raw runtime structures.
- Optional unknown chunks can be skipped.

### Mission runtime

Phase 4 defines `MissionRuntime`, fixed `ObjectiveSet`, tick-tagged commands, and deterministic objective evaluation.

### Fire control

Phase 3 defines `WeaponSolutionFrame` with shooter, target, weapon, range, closure, aspect, launch state, time of flight, loft/direct recommendation, seeker support, and source tick.

### RIO callouts

Hybrid presentation is frozen:

- Short samples when budgets permit.
- Tones and text are authoritative.
- Every sample has text fallback.
- Critical warnings preempt samples.
- Gameplay never depends on sample availability.

---

## 13. Future expansion goals

The following are explicitly outside the current architecture and acceptance criteria.

### 13.1 Native high-resolution graphics

The long-term goal is to investigate scaling the production graphics engine to MEGA65 native high-resolution modes, potentially reaching the 720×576 class.

This is not a current resolution requirement.

- R0 hardware measurement exclusively determines the production resolution, layout, polygon ceiling, world cadence, and reserve.
- Higher-resolution candidates may be benchmarked during R0.
- A higher mode is rejected unless filled software 3-D, cockpit composition, HUD/MFD presentation, audio/input deadlines, combat load, and mandatory reserve all pass.
- No current budget assumes high-resolution production rendering.
- Failure to reach this goal does not fail R0, the vertical slice, or the release.

### 13.2 Destructible ground objects

A future expansion may make buildings, trees, bridges, and similar ground structures destructible.

This is not part of:

- The current entity capacity envelope.
- The current damage graph.
- The Midnight Spear vertical slice.
- Phase 0–4 exit criteria.
- Current mission or campaign requirements.

Until explicitly accepted, all ground objects remain non-destructible.

Before adoption, destructible ground objects require:

1. Performance and capacity analysis against measured R0 ceilings.
2. A defined representation: entity, resource-state replacement, or hybrid.
3. Persistence and mission-state rules.
4. Rendering and disk-budget analysis.
5. Deterministic lifecycle and save-format design.
6. A numbered architecture revision if any frozen invariant changes.

---

## 14. Preserved development gates

### Phase 0 — R0

1. R0-A: references, benchmark identity, toolchain, `MemoryAccessABI`, opcode proof, and profiler.
2. R0-B: graphics, FCM, cockpit, palette, and swap measurements.
3. R0-C: production-shaped tools and scene.
4. R0-D: 530,000-clock protected workload.
5. R0-E: Xemu report.
6. R0-F: hardware report.
7. Measured-limits revision.

No gameplay implementation may merge before R0-F and the limits revision.

### Phase 1 — Core engines

- Scheduler and determinism.
- Memory and resources.
- Math, coordinates, atmosphere, and units.
- Renderer, cockpit, HUD, MFDs, and palette.
- Sound.
- Input and H.O.T.S.
- Entity pools.
- System dependency schema.
- Synthetic integrated harness.

Phase 2 cannot begin until the concurrent harness proves canonical mapping, deterministic checksums, lifecycle correctness, combined p95 timing, memory compliance, reserve, audio stability, correct input, and PAL/NTSC equivalence.

A partial pass is failure.

### Phases 2–5

- Phase 2: flight and aircraft systems.
- Phase 3: radar, weapons, and damage.
- Phase 4: tactical layer and Midnight Spear.
- Phase 5: campaign, compatibility, optimization, and release.

The future expansion goals are not inserted into these phases or their exit criteria.

---

## 15. Architecture-invariant acceptance tests

### Memory

- Public routines preserve canonical mapping.
- IRQ behavior survives temporary MAP scopes.
- Far pointers and DMA resolve identically in Xemu and hardware.
- Resource handles survive relocation.
- Illegal physical ranges are rejected.

### Determinism

- PAL and NTSC replays match.
- Presentation ordering cannot affect simulation.
- Simultaneous events follow the frozen order.
- RNG streams remain independent.
- Stale handles fail.
- Render overruns never skip ticks.

### Coordinates

- All frame transforms match the frozen axes.
- Sector crossings are continuous.
- Deck contact remains within two inches.
- Altitude and operational extent do not overflow.

### Timing

- Protected simulation, protected presentation, world rendering, and reserve are separate.
- Incomplete buffers are never shown.
- HUD, input, audio, warnings, and simulation retain deadlines.

### State and presentation

- Input cannot bypass actuators.
- Hydraulic failure changes physical control surfaces.
- System colors are derived.
- Palette violations fail the build.
- Grayout preserves essential identity.

### Host validation

- Target routines match golden vectors.
- Instrumentation reports required failures and high-water marks.
- Benchmarks include complete identity.

The future expansion goals are excluded from these acceptance tests.

---

## 16. Decision log additions

| Decision | Reason |
|---|---|
| A-10 Cuba!, F/A-18 Korea, and Falcon 3.0 are primary feel references | They define the desired systems density, HUD language, and combat-sim character |
| High-resolution rendering is a future measured goal | It must not prejudice R0 mode selection or budgets |
| 720×576-class modes may be benchmarked but are not required | Ambition is preserved without converting hope into architecture |
| Ground objects remain non-destructible | Current capacity, persistence, and rendering rules do not support destruction |
| Destructibility requires analysis and possibly a numbered revision | It affects entities, resources, rendering, missions, and saves |
| R0 and Phase 1 gates remain unchanged | Documentation goals cannot weaken engineering discipline |

---

## 17. Smallest authorized next milestone

The smallest authorized milestone remains R0-A:

- Pin authoritative references.
- Pin hardware revision, FPGA core, ROM, system files, video standard, Xemu, assembler, and build identity.
- Implement and validate the `MemoryAccessABI` proof.
- Prove required 45GS02 instructions and addressing modes.
- Produce a reproducible D81.
- Generate symbols and listings.
- Establish cycle, mapping, DMA, and interrupt instrumentation.

R0-A contains no flight, radar, weapons, H.O.T.S., mission, campaign, high-resolution production renderer, or destructible-world implementation.

The absolute R0 gate and hard Phase 1 integrated-harness gate remain unchanged.

