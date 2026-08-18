# F-65 Megawing — Engine, Runtime, and Toolchain Design Supplement

**Draft:** 0.1  
**Status:** Architecture-review candidate  
**Parent architecture:** F-65 Megawing Revision 1.4.1  
**Parent gameplay baseline:** Gameplay and Simulation Requirements Supplement Draft 0.2  
**Nature of document:** Binding implementation contracts, pre-R0 proof candidates, and measured-decision gates  
**Architecture effect:** None unless a future numbered architecture revision explicitly says otherwise

---

## 0. Purpose, hierarchy, and authority

This supplement defines how the frozen architecture and player-facing gameplay contracts are to be implemented. It supplies the missing engine module boundaries, runtime data flow, world representation, physical-model strategy, rendering strategy, AI organization, input/audio services, authoring tools, memory subledgers, and AI-assisted development discipline.

```text
Revision 1.4.1 — Architecture Invariants
└── Gameplay and Simulation Requirements Supplement 0.2
    └── Engine, Runtime, and Toolchain Design Supplement 0.1
```

- **MUST:** Revision 1.4.1 is the absolute architecture authority.
- **MUST:** Gameplay Supplement 0.2 is the player-facing behavior authority.
- **MUST:** This document is subordinate to both parents and cannot relax, reinterpret, or silently replace either one.
- **MUST:** If this document conflicts with a parent, the parent wins and this document must be corrected.
- **MUST:** A proposal for a heap, dynamically growing pool, secondary physical-integration rate, mutable simulation state in Attic RAM, in-sortie code overlay, continuous tactical disk streaming, destructible static scenery, or presentation-dependent simulation requires explicit rejection or a numbered architecture revision.
- **MUST:** No gameplay implementation may merge before Revision 1.4.1 R0-F and the measured-limits revision. Host schemas, compilers, reference models, proof harnesses, and R0 experiments remain authorized in their existing phases.
- **MUST:** All production target code remains 45GS02 assembly. Java is the host-tool and reference-model language.

---

## 1. Requirement-class legend

Every normative statement uses one of four requirement classes.

| Class | Meaning |
|---|---|
| **MUST** | Durable implementation or isolation contract. Target code and tools must satisfy it. |
| **TARGET** | Intended engineering or quality target that may move on recorded evidence. |
| **R0-GATED** | Hardware-dependent choice that freezes only through the complete R0 identity and measured-limits revision. |
| **TBD** | Coefficient, format, threshold, table, or cadence with an explicit validation gate in §18. |

- **MUST:** TARGET, R0-GATED, and TBD material cannot weaken a parent MUST or a MUST in this document.
- **MUST:** Every closed R0-GATED or TBD item records the selected value, evidence identity, tolerance, and approving revision.

---

## 2. Invariant compliance

### 2.1 Unchanged parent contracts

- **MUST:** Simulation remains one deterministic 100 Hz timeline with the exact 21-step order in Revision 1.4.1.
- **MUST:** Every physical entity updates on that timeline. Lower-rate work is limited to scheduled AI/RIO decision production at step 16 and display/audio services outside authoritative physical integration.
- **MUST:** Simulation state, commands, events, pool lifecycles, checksums, and atomic `SimulationSnapshot` publication retain the frozen ordering.
- **MUST:** The canonical physical and CPU-visible maps, MAP ownership, DMA rules, pointer formats, resource handles, entity handles, arithmetic, RNG streams, frames, capacities, and overrun behavior remain unchanged.
- **MUST:** Static terrain and scenery remain resources. Only valid live ship/carrier or surface-radar/SAM entities can receive surface-object damage.
- **MUST:** Presentation consumes only the last completed snapshot and cannot change physical state, sensing, AI, damage, objectives, scoring, or checksums.
- **MUST:** Rendering remains incremental and resumable. Incomplete world buffers never display.

### 2.2 Concepts introduced without changing architecture

- **MUST:** `AircraftPhysicsClass` selects one of two mission-load physical implementations but does not create a new entity pool or clock.
- **MUST:** Host-generated engine tables, terrain-query data, mission graphs, AI doctrine tables, and renderer resources use existing resource handles and residency states.
- **MUST:** The mission compiler's static capacity proof supplements, but never replaces, frozen runtime pool rejection and high-water instrumentation.
- **MUST:** Separate boot/menu/campaign and sortie executables are load states, not in-sortie overlays. The entire sortie executable is resident before the sortie clock starts.

---

## 3. Runtime ownership and module graph

### 3.1 Sacred core

`CoreRuntime` exclusively owns:

- The 100 Hz clock and exact tick dispatcher.
- Canonical mapping, base page, stack, vectors, IRQ entry, and `MemoryAccessABI`.
- Entity allocation, generations, lifecycle commit, and pool diagnostics.
- DMA submission and completion state.
- Command and deterministic-event ordering.
- RNG-stream initialization and checksum orchestration.
- Snapshot assembly and atomic publication.
- Deadline debt and protected-service arbitration.

- **MUST:** No other module writes these states directly.
- **MUST:** No module executes MAP, submits DMA directly, allocates outside a frozen pool, publishes a snapshot, or changes the simulation clock.
- **MUST:** Core changes require explicit human authorization and the complete architecture-invariant test suite. A routine module task does not authorize an AI agent to edit core files.

### 3.2 Engine modules

```text
CoreRuntime
├── InputEngine                 raw devices -> semantic commands
├── EnvironmentEngine           atmosphere, wind, gravity, terrain queries
├── ControlAndSystemsEngine     control laws, actuators, supplies, aircraft systems
├── FlightDynamicsEngine        SIX_DOF and KINEMATIC physical updates
├── ContactEngine               terrain, runway, deck, arrestment, collision candidates
├── WeaponAndDamageEngine       missiles, guns, decoys, fuzes, accumulated damage
├── SensorAndTrackEngine        radar truth, observations, tracks, RWR, warnings
├── AIEngine                    doctrine and utility -> next-tick AIIntentFrame
├── MissionEngine               graph, objectives, tutorial state, scoring, debrief events
├── AudioEngine                 SID voices, DMA samples, priorities, text fallbacks
├── GraphicsEngine              incremental world, cockpit, HUD, radar, systems displays
└── ResourceAndDiagnostics      residency requests, traces, counters, replay records
```

- **MUST:** Each module owns only its declared state and exports documented entry points and records.
- **MUST:** Cross-module communication uses read-only inputs, core-owned queues, command frames, deterministic events, resource handles, or snapshot fields.
- **MUST:** A module never reaches into another module's private arrays, even when both reside in the same physical memory region.
- **MUST:** The core invokes modules in the frozen tick order. A module cannot call forward into a later tick stage or recursively invoke the dispatcher.
- **MUST:** Public entry points assume and restore the canonical mapping, `$01 = $35`, base page at `$0200`, and all other Memory Access ABI requirements.
- **MUST:** Code placed in the `$8000–$BFFF` canonical backing range cannot be executing when `MemoryAccessABI` opens either temporary MAP window. Static call-graph validation must prove this.

### 3.3 Tick data flow

- **MUST:** Input sampling produces tick-tagged semantic commands; it never edits aircraft state.
- **MUST:** Environment queries are pure for a given tick, position, and mission environment state.
- **MUST:** Control laws produce `FlightControlFrame`; actuators produce actual `ControlSurfaceState`; aerodynamics consume only actual state.
- **MUST:** Weapons and collisions produce ordered events; damage capability changes occur only at the frozen accumulation point.
- **MUST:** Sensor observations derive from post-motion/post-damage truth in step 15.
- **MUST:** AI produces `AIIntentFrame` at step 16 for application no earlier than the next tick.
- **MUST:** Mission state advances at step 17, lifecycle changes commit at step 18, presentation/audio events derive at step 19, and no presentation module reads a partially assembled snapshot.

---

## 4. Pre-R0 memory and resident-code ledgers

### 4.1 Ledger authority

- **MUST:** The following ceilings are binding pre-R0 module budgets inside the frozen Revision 1.4.1 ownership ranges.
- **MUST:** Every interface definition generates target sizes, offsets, alignment assertions, and a build-time region report.
- **MUST:** Any region or module-ceiling overflow fails the build. An overflow cannot be cured by borrowing undocumented bytes from another region.
- **MUST:** The measured-limits revision may rebalance suballocations within a frozen physical range, but may not alter the public memory ABI without a numbered architecture revision.
- **MUST:** `$058000–$05FFFF` remains an untouched 32 KB measured-limits reserve before R0. No proof candidate may depend on it to pass.

### 4.2 Resident bank-0 allocation

| CPU range | Bytes | Binding pre-R0 use |
|---|---:|---|
| `$0000–$02FF` | 768 | CPU ports, compatibility bytes, hardware stack, relocated game base page |
| `$0300–$1FFF` | 7,424 | Scheduler, IRQ mailboxes, core hot state, command/event cursors |
| `$2000–$7FFF` | 24,576 | Resident sortie code and hot constant tables |
| `$8000–$BFFF` | 16,384 | Canonical resident code/tables temporarily hidden only inside bounded MAP scopes |
| `$C000–$CFFF` | 4,096 | Platform, MemoryAccessABI, DMA, and interrupt-safe code |
| `$D000–$DFFF` | 4,096 | MEGA65 I/O personality; unavailable to ordinary resident storage |
| `$E000–$FFFF` | 8,192 | Critical code, handlers, mapping-safe services, vectors |
| **Total** | **65,536** | Frozen bank-0 ownership |

Callable sortie code has a maximum address envelope of 53,248 bytes across `$2000–$BFFF`, `$C000–$CFFF`, and `$E000–$FFFF`.

| Sortie code owner | Ceiling |
|---|---:|
| Core, platform, IRQ, MAP, DMA, scheduler | 10 KB |
| Math, coordinates, atmosphere, world queries | 4 KB |
| Flight controls, actuators, 6DOF/kinematic motion, aircraft systems | 8 KB |
| Sensors, tracks, weapons, countermeasures, contact, damage | 7 KB |
| AI, formations, mission runtime, objectives | 5 KB |
| Renderer, cockpit, HUD, radar, systems-display service | 6 KB |
| Input, audio, resource service | 4 KB |
| Diagnostics, checksums, replay | 2 KB |
| Unassigned resident code reserve | 6 KB |
| **Total** | **52 KB** |

- **MUST:** The 6 KB code reserve is real headroom and cannot be preassigned to a module before its measured review.
- **MUST:** Draft 0.1 assigns no owner, entry point, table, or contingency feature to the 6 KB code reserve. The machine-readable ledger marks it `UNALLOCATED_RESERVE` and forbids ordinary borrowing.
- **MUST:** Menu/campaign code does not consume sortie-code ceilings because it is a separate resident load state.

### 4.3 Active simulation allocation — `$010000–$017FFF`

| Owner | Ceiling | Capacity assumption |
|---|---:|---|
| Pool metadata, generations, free maps, typed handles | 1,024 B | All frozen pools |
| Aircraft physical/common state | 5,120 B | 16 × 320 B |
| Guided missiles | 3,072 B | 32 × 96 B |
| Gun projectile groups | 1,536 B | 32 × 48 B |
| Chaff/flare entities | 1,536 B | 64 × 24 B |
| Ships and carriers | 1,024 B | 8 × 128 B |
| Surface radar/SAM entities | 1,280 B | 16 × 80 B |
| Dynamic mission entities | 1,536 B | 32 × 48 B |
| Simulation-relevant effects | 768 B | 32 × 24 B |
| Radar truth contacts | 1,536 B | 32 × 48 B |
| Radar tracks | 1,920 B | 24 × 80 B |
| F-65 detailed systems and dependency measurements | 4,096 B | Player hot systems plus shared tables/indices |
| Commands, AI intents, priority/objective indices | 2,048 B | Frozen queue and objective capacities |
| Lifecycle, collision, fuze, and damage-event buffers | 2,048 B | Worst legal tick event set |
| Checksum and snapshot-assembly state | 1,024 B | Does not include display stores |
| Unassigned active-simulation reserve | 3,200 B | Must remain unowned until schema proof |
| **Total** | **32,768 B** | Frozen region size |

- **MUST:** Kinematic aircraft consume ordinary aircraft slots and their complete common-state allocation. They are not hidden contacts or presentation objects.
- **MUST:** Record ceilings include padding and alignment. A larger generated record fails the ledger even if a particular mission uses fewer live entities.
- **MUST:** Draft 0.1 assigns no record, queue, table, or overflow contingency to the 3,200-byte active-simulation reserve. The machine-readable ledger marks it `UNALLOCATED_RESERVE` and forbids ordinary borrowing.

### 4.3.1 Gameplay 0.2 peak paper audit

The full Gameplay 0.2 air-combat peak uses live records inside arrays that are already provisioned to their complete frozen pool capacities. “Peak live bytes” therefore measures active records; it does not release the bytes belonging to inactive fixed slots for another owner.

| Active-simulation owner | Static allocation | Gameplay 0.2 simultaneous peak | Peak live bytes | Static bytes not live at peak |
|---|---:|---:|---:|---:|
| Aircraft physical/common state | 5,120 B | 9 of 16 | 2,880 B | 2,240 B |
| Guided missiles | 3,072 B | 16 of 32 | 1,536 B | 1,536 B |
| Gun projectile groups | 1,536 B | 24 of 32 | 1,152 B | 384 B |
| Chaff/flare entities | 1,536 B | 48 of 64 | 1,152 B | 384 B |
| Ships and carriers | 1,024 B | 1 of 8 | 128 B | 896 B |
| Surface radar/SAM entities | 1,280 B | 0 of 16 | 0 B | 1,280 B |
| Dynamic mission entities | 1,536 B | 8 of 32 | 384 B | 1,152 B |
| Simulation-relevant effects | 768 B | 0 of 32 | 0 B | 768 B |
| Radar truth contacts | 1,536 B | 10 of 32 | 480 B | 1,056 B |
| Radar tracks | 1,920 B | 10 of 24 | 800 B | 1,120 B |
| **Entity/track arrays** | **19,328 B** | — | **8,512 B** | **10,816 B** |

The non-pool portion remains fully reserved during that peak:

| Fixed owner | Bytes | Paper basis |
|---|---:|---|
| Pool metadata | 1,024 B | All pool generations, free maps, ownership/high-water data |
| F-65 detailed systems | 4,096 B | Full breakdown below; no dependence on unused entity slots |
| Commands, AI intents, priority/objective indices | 2,048 B | Full legal tick queue envelope |
| Lifecycle, collision, fuze, and damage events | 2,048 B | Full legal simultaneous-event envelope |
| Checksum and snapshot assembly | 1,024 B | Full protected publication/checksum state |
| Unallocated simulation reserve | 3,200 B | No owner and no peak dependency |
| **Fixed and reserve total** | **13,440 B** | — |

`19,328 + 13,440 = 32,768` bytes. At the required peak, 8,512 bytes of the fixed entity/track arrays contain live records; unused fixed slots remain reserved to their pools. The peak therefore coexists with the entire detailed F-65 system allocation and the untouched 3,200-byte reserve.

The 4,096-byte detailed-system ceiling is itself closed on paper as follows:

| Detailed F-65 system owner | Ceiling |
|---|---:|
| Thirty-two eight-byte `SystemState` records | 256 B |
| Dependency-graph runtime nodes and arbitration state | 768 B |
| Engine, fuel, electrical, and hydraulic measurements | 768 B |
| Flight-control, autothrottle, ADLC, and actuator state | 768 B |
| Stores, loadout, mass/inertia, and wing-sweep state | 512 B |
| Component damage, fire/leak, and structural-exposure state | 768 B |
| Air-data, caution, status, and derived hot caches | 256 B |
| **Total** | **4,096 B** |

- **MUST:** The paper audit is a ceiling proof, not permission to enlarge a generated record. Generated field layouts must still prove every stated per-record size.
- **MUST:** The Gameplay 0.2 combined runtime harness remains required because live-event and queue concurrency must validate the paper assumptions on target hardware.

### 4.4 Remaining chip-RAM allocation

| Physical range | Size | Binding subledger |
|---|---:|---|
| `$018000–$01BFFF` | 16 KB | Mission graph/tutorial/objectives 4 KB; AI doctrine/blackboards/routes 3 KB; audio state/events/descriptors 2 KB; replay command/checksum buffer 2 KB; dialogue/RIO/mission queues 2 KB; reserve 3 KB |
| `$01C000–$01CFFF` | 4 KB | Snapshot/display descriptors 2 KB; display-control records 1 KB; palette/raster records 512 B; reserve 512 B |
| `$01D000–$01FFFF` | 12 KB | Fixed-math/transform scratch 3 KB; event-sort/collision candidates 2 KB; decode/conversion scratch 2 KB; trace/checksum scratch 1 KB; reserve 4 KB |
| `$020000–$02FFFF` | 64 KB | Complete display store A |
| `$030000–$03FFFF` | 64 KB | Complete display store B |
| `$040000–$047FFF` | 32 KB | Cockpit base 12 KB; HUD/MFD glyphs and symbols 8 KB; hot sprites/impostors 6 KB; palettes/lookups 2 KB; reserve 4 KB |
| `$048000–$04FFFF` | 32 KB | Transformed vertices 8 KB; faces/LOD/depth buckets 6 KB; edges/spans 8 KB; visible tile/object lists 4 KB; renderer DMA staging 2 KB; reserve 4 KB |
| `$050000–$057FFF` | 32 KB | Tile/resource decode staging 12 KB; audio sample cache 12 KB; resident DMA lists/descriptors 4 KB; reserve 4 KB |
| `$058000–$05FFFF` | 32 KB | Untouched measured-limits reserve |

- **R0-GATED:** Exact sharing between cockpit assets, hot impostors, renderer records, tile staging, and audio sample cache freezes after simultaneous display/audio/DMA measurement.
- **MUST:** Any R0 rebalance must continue to report each consumer explicitly; “shared” or “miscellaneous” cannot conceal an unbounded allocation.

### 4.5 Attic RAM policy

- **MUST:** The complete compiled sortie package is loaded before tactical play and may remain as immutable cold data in Attic RAM.
- **MUST:** Attic contents use resource handles and are staged through `ResourceManager` into an owning chip-RAM region before VIC-IV, SID/audio DMA, or another direct consumer uses them.
- **MUST:** Authoritative mutable simulation state never lives only in Attic RAM.
- **MUST:** Tactical play performs no disk reads. Disk faults and media latency therefore cannot alter simulation or protected presentation deadlines.

---

## 5. Performance ownership and deterministic shedding

- **MUST:** The frozen two-display-frame NTSC ledger remains 530,000 clocks protected non-render, 100,000 clocks protected HUD/cockpit/display service, 585,000 clocks incremental world rendering, and 135,000 clocks mandatory reserve.
- **MUST:** Pre-R0 modules report cycles and call counts but do not claim production cycle quotas from unmeasured estimates.
- **R0-GATED:** The measured-limits revision subdivides the protected workload by module over the six-NTSC-frame/ten-tick reporting superperiod and records p50, p95, worst observed, and synthetic maximum.
- **MUST:** Each module has a measured cycle high-water counter. Combined reports, not isolated microbenchmarks, determine acceptance.
- **MUST:** Simulation, input, critical audio, HUD, and warnings retain protected deadlines. AI decisions may use only their scheduled budget and cannot delay a tick.
- **MUST:** The fixed presentation shedding ladder is:
  1. Drop optional presentation effects.
  2. Select cheaper distant-object impostors.
  3. Reduce distant terrain detail.
  4. Remove optional shading and decorative faces.
  5. Fall from filled to validated reduced-filled and then validated wireframe tiers.
  6. Retain the previous completed world buffer and reduce world-frame cadence.
- **MUST:** Shedding changes only presentation work and occurs at render-work boundaries. It never changes sensor visibility, collision geometry, AI perception, missile state, mission state, or checksums.
- **R0-GATED:** Tier thresholds, recovery hysteresis, exact LOD distances, and the richest production tier freeze through the identical-scene R0 benchmark.

---

## 6. World, terrain, and environmental engine

### 6.1 Authoritative world representation

- **MUST:** The world uses the frozen sector/local `WorldPosition` and North-East-Down frames.
- **MUST:** Each theater compiles into independently indexed tiles containing authoritative terrain-height/collision data and presentation geometry/resource handles.
- **MUST:** Coarse heightfield-derived tiles represent ordinary land; authored coastline/feature polygons shape islands and shorelines; detailed local meshes represent runways, airfields, carrier interaction areas, and exceptional terrain features.
- **MUST:** Sensor line of sight, terrain impact, ground clearance, and runway/deck contact use authoritative query data, not the currently rendered LOD.
- **MUST:** Rendered tiles may disappear or simplify under load without changing world queries.
- **MUST:** Tile boundaries are continuous in height and collision queries. Camera and physical motion remain continuous across sector and tile crossings.
- **R0-GATED:** Tile dimensions, height sample spacing, presentation triangle ceilings, coastline simplification tolerance, resident tile count, and staging cadence freeze after R0.

### 6.2 Atmosphere and wind

- **MUST:** One deterministic environment service provides pressure, density, temperature, speed of sound, gravity, KIAS/TAS conversion, and wind to aircraft and missiles.
- **MUST:** Missions author surface, middle, and high-altitude wind layers with deterministic fixed-point interpolation.
- **MUST:** A mission temperature profile modifies the reference atmosphere deterministically.
- **MUST:** Clouds, visibility tint, day/dusk/night light, and decorative sea state are presentation/mission parameters only in current scope.
- **MUST:** Dynamic weather cells, icing, evolving fronts, and stochastic turbulence are excluded.
- **TBD:** Atmosphere table spacing, interpolation formats, wind breakpoints, and temperature correction tables close through the Phase 1–2 host oracle.

### 6.3 Spatial queries and contact

- **MUST:** Typed deterministic query routines cover terrain height/material, segment/terrain line of sight, runway containment, carrier-local deck plane, wire/hook geometry, and bounded entity collision candidates.
- **MUST:** Aircraft and ship broad-phase collision uses typed candidate lists and conservative bounds; missiles and gun groups use swept tests so a 100 Hz step cannot tunnel through a legal target.
- **MUST:** Candidate order cannot determine the result. Events enter the frozen deterministic sort before damage applies.
- **MUST:** Carrier contact retains the parent two-inch accuracy requirement independent of visual polygon detail.

---

## 7. Aircraft and missile physical models

### 7.1 Immutable physical class

`AircraftPhysicsClass` has exactly two current values:

| Value | Use |
|---|---|
| `SIX_DOF` | Player, wingman, combat aircraft, and any required physical AIC aircraft |
| `KINEMATIC` | Civilian traffic, rescue aircraft, and authored background aircraft |

- **MUST:** The mission compiler assigns the class before simulation start. Runtime distance, visibility, radar contact, camera, combat state, and CPU load cannot change it.
- **MUST:** An AIC aircraft required to maneuver, defend, or participate as a combat actor uses `SIX_DOF`; a route-bound protected AIC may use a mission-authored class only if its required behavior passes validation.
- **MUST:** Both classes remain ordinary aircraft entities, physical contacts, radar truth contacts, collision objects, and legal damage recipients.

### 7.2 Table-driven 6DOF model

- **MUST:** The 6DOF engine integrates rigid-body translation, orientation, linear velocity, and angular rates at 100 Hz.
- **MUST:** Whole-aircraft aerodynamic coefficients depend on Mach, angle of attack, sideslip, configuration, actual control-surface state, wing sweep, and damage.
- **MUST:** Reference geometry, dynamic pressure, mass, center of gravity, inertia, stores, fuel, cannon ammunition, gravity, thrust, and wind transform those coefficients into physical forces and moments.
- **MUST:** Engine thrust and fuel flow use deterministic tables over throttle state, Mach, altitude/density, damage, and engine state.
- **MUST:** Damage changes capability through explicit actuator/system state and table multipliers or asymmetric increments; it cannot invoke a second “damaged flight model.”
- **MUST:** The target computes no airfoil flow solution, panel method, blade element model, or computational fluid dynamics.
- **TBD:** Coefficient grids, interpolation order, fixed-point formats, reference geometry, inertia, engine tables, departure extensions, and damage modifiers close through high-precision and bit-exact Phase 2 oracles.

### 7.3 Kinematic aircraft model

- **MUST:** Kinematic aircraft integrate position, heading, pitch/flight-path state, speed, and bounded turn/climb/acceleration commands at 100 Hz.
- **MUST:** Their authored performance envelope prevents instantaneous turns, altitude jumps, speed jumps, or route teleportation.
- **MUST:** Formation and route controllers produce commands; they do not write position directly except during mission-start placement.
- **MUST:** Kinematic collision, damage, despawn, sensing, and mission-state behavior follows the same deterministic lifecycle as 6DOF entities.
- **TBD:** Type-specific acceleration, turn, climb, descent, landing, and fuel-use envelopes close through Phase 2 route and contact vectors.

### 7.4 Missile and gun models

- **MUST:** Guided missiles use a 3DOF point-mass model integrated at 100 Hz.
- **MUST:** Missile state includes position, velocity, mass/thrust phase, drag/energy state, guidance command, seeker field of regard, support/autonomy state, target handle, countermeasure state, fuze state, and RNG state where required.
- **MUST:** Boost/sustain thrust, density-dependent drag, gravity, loft, energy-dependent maneuver authority, guidance, look angle, support loss, seeker acquisition, deterministic decoy scoring, and proximity fuzing affect outcome.
- **MUST:** No RNG can convert a failed physical intercept into a hit.
- **MUST:** Cannon fire uses bounded `GunProjectileGroup` records with swept ballistic envelopes, dispersion parameters, lifetime, and ammunition accounting. Individual rounds are not persistent entities.
- **TBD:** Missile motor, drag, maneuver, seeker, guidance, decoy, fuze, and gun-group tables close through Phase 3 golden trajectories.

---

## 8. Renderer and display engine

### 8.1 Software 3D pipeline

- **MUST:** The renderer consumes only the published snapshot and immutable presentation resources.
- **MUST:** Every world-buffer attempt binds one immutable `source_snapshot_tick`, one view, one presentation tier, one destination store, and one resumable work cursor. A single world buffer cannot mix entity or camera state from different snapshots.
- **MUST:** The renderer may finish a buffer from an older snapshot while newer snapshots publish. It may abandon that incomplete buffer only at a legal work boundary, clears its completion state, and never displays the abandoned contents.
- **MUST:** The primary proof pipeline executes these ordered stages:
  1. Acquire the latest completed snapshot permitted by the world-frame scheduler and bind the destination store.
  2. Clear or compose the authored sky/ocean/background bands required by the selected view and lighting preset.
  3. Rebase authoritative snapshot positions to signed camera-relative coordinates.
  4. Gather potentially visible terrain tiles and object presentation records using compiled conservative bounds.
  5. Select the permitted mesh or impostor LOD from the current fixed shedding tier.
  6. Transform model vertices into camera space with widened, saturating fixed-point intermediates.
  7. Reject objects outside the conservative frustum; backface-cull eligible faces; clip surviving geometry against the near plane and required side/top/bottom planes.
  8. Perspective-project clipped vertices into bounded screen coordinates and record every saturation or clip-capacity rejection.
  9. Convert faces and impostors into bounded render primitives containing palette/material role, depth key, edge/span metadata, and source identity.
  10. Place opaque primitives into coarse far-to-near depth buckets. Apply compiled subobject order or bounded local sort where carrier/runway geometry requires it.
  11. Traverse terrain and opaque-object buckets far to near, generate edges with one frozen inclusion rule, and emit clipped spans or validated DMA batches.
  12. Draw ordered transparent-index impostors and presentation effects without changing the authoritative depth/query model.
  13. Mark the world store complete only after every required CPU span and immutable DMA batch completes successfully.
  14. Offer the complete store for swap at a display boundary; compose the protected cockpit/HUD/MFD layers from their latest permitted snapshot independently of world-buffer age.
- **MUST:** The production proof allocates no per-pixel Z-buffer.
- **MUST:** Intersecting local geometry that cannot tolerate coarse painter ordering—especially runway/carrier presentation—uses authored subobject ordering or bounded local sorting.
- **MUST:** `RenderWorkItem` contains the stage, snapshot tick, view/tier identity, resource handles, object/face/span cursor, destination bounds, pending DMA identity, and diagnostic counters needed to resume without repeating or skipping work.
- **MUST:** Rendering yields only at tile, object, face, span-batch, or DMA-batch boundaries and displays only complete buffers.
- **MUST:** A DMA batch is range-validated, immutable until completion, and submitted only by `DMAManager`; the renderer never blocks protected services while awaiting it.
- **MUST:** Edge generation uses a single top/left-versus-bottom/right inclusion convention so adjacent faces neither double-fill nor open presentation cracks from inconsistent rounding.
- **MUST:** Clip-list, vertex, face, bucket, edge, span, or DMA-list exhaustion aborts the incomplete buffer, increments the owning diagnostic, and steps down the fixed presentation ladder; it cannot overwrite workspace or publish a partial frame.
- **MUST:** Arbitrary perspective-correct texture mapping is outside the production proof. Compiled impostors or measured affine/scaled copy candidates may be used only as R0-validated presentation resources.
- **R0-GATED:** DMAgic line/fill/copy operations are used only where hardware measurement beats CPU work without violating input/audio latency. VIC-IV, DMAgic, and audio behavior are verified against the pinned [MEGA65 Chipset Reference](https://files.mega65.org/files/m/mega65-chipset-reference_4hh2eE.pdf) and the complete R0 identity.

### 8.2 LOD and impostors

- **MUST:** Every renderable aircraft, ship, significant world object, and effect declares its mesh LODs, impostor forms, palette roles, bounds, and switching metadata at compile time.
- **MUST:** Impostors and cheap LODs consume explicit asset bytes, visible-list entries, transform work, DMA work, and draw clocks in the same ledgers as filled geometry.
- **MUST:** No R0 report may call an impostor “free” or exclude its composition cost from the benchmark.
- **MUST:** LOD choice is presentation-only and cannot change contact identity, collision bounds, sensor return, damage, or mission behavior.
- **R0-GATED:** Mesh ceilings, impostor dimensions, angle bins, transition distances, overdraw limits, palette assignments, and maximum visible-object counts freeze from the protected-load scene.

### 8.3 Cockpit and views

- **MUST:** The cockpit, HUD, radar/navigation display, and systems display are independent protected presentation layers over or beside the world buffer as selected by R0.
- **MUST:** Supported views are forward cockpit, fixed left glance, fixed right glance, fixed aft-quarter glances, and the low-cost chase view.
- **MUST:** Glance views use authored camera transforms and cockpit framing. A freely rotating camera is not required.
- **MUST:** View changes cannot alter simulation, AI, radar, or checksums and cannot force an unfinished buffer to display.
- **R0-GATED:** Resolution, viewport geometry, cockpit split, view art, raster method, map pixel geometry, and world cadence freeze through R0.

---

## 9. Sensor and track engine

- **MUST:** Radar uses scheduled geometric scan and track processing rather than per-return ray tracing or a full radar-equation integration.
- **MUST:** Detection considers scan volume, field of regard, range, terrain line of sight, target class/aspect tables, altitude relationship, look-down sea/ground clutter, notch geometry, jamming state, and deterministic sensor uncertainty.
- **MUST:** Terrain line of sight and clutter geometry use authoritative world-query data, never rendered LOD.
- **MUST:** Detection observations are separate from correlated tracks. `RadarTrackState` owns detection, coasting, priority, weapon-quality, support-lost, and dropped transitions.
- **MUST:** Organic, offboard, and fused observations can refer to one physical contact without allocating duplicate truth entities.
- **MUST:** Sensor RNG uses the independent sensor stream and cannot affect physical motion or AI RNG consumption.
- **MUST:** RWR and missile-threat state distinguish emitter/launch indication, active seeker, indication lost, still-dangerous state, and confirmed defeat confidence.
- **TBD:** Scan schedules, range/aspect tables, clutter/notch thresholds, measurement errors, coast timers, correlation gates, jamming effects, and RWR confidence close through Phase 3 sensor vectors.

---

## 10. Deterministic tactical AI

### 10.1 Knowledge boundary

- **MUST:** Combat AI is sensor-limited. It may use own sensors, fused/datalink tracks, RWR, visual detections, doctrine, mission orders, fuel/weapons/damage state, and remembered observations.
- **MUST:** Mission triggers and scoring may inspect world truth at step 17, but unauthorized truth cannot enter an aircraft's tactical blackboard or decision score.
- **MUST:** Trace instrumentation records the observations and score components used for each selected action so sensor cheating is testable.

### 10.2 Doctrine plus utility

- **MUST:** Each tactical actor uses an authored hierarchical doctrine state machine with bounded fixed-point utility scoring among legal transitions/actions.
- **MUST:** Current doctrine states cover deck/ground, takeoff, rendezvous, formation, transit, intercept, commit, support, crank/notch/defend, recommit, disengage, RTB, approach, landing, and emergency behavior as applicable to type.
- **MUST:** Doctrine provides legal actions and priorities; utility selects among them using explicit score components and deterministic tie-breaking.
- **MUST:** AI decisions execute only when scheduled in tick step 16. They emit `AIIntentFrame` for application no earlier than the next tick.
- **MUST:** The control, actuator, physics, weapon-request, and lifecycle paths used by AI are the same public paths used by player commands.
- **MUST:** Entity-local AI RNG remains independent. Presentation state, camera, render tier, and frame cadence cannot affect decisions.
- **TBD:** Decision cadences, doctrine graphs, score weights, perception memory, formation gains, difficulty modifiers, and RIO/wingman callout policy close through Phase 4 scenario traces.

---

## 11. Input engine

- **MUST:** Input flows through three isolated stages: raw keyboard/joystick sample, context/gesture recognition, and tick-tagged semantic command production.
- **MUST:** Raw input is sampled every display frame and queued so no display/simulation phase directly edits control state.
- **MUST:** Semantic actions and contexts are those frozen by Gameplay Supplement 0.2.
- **MUST:** Digital joystick shaping is an input-command concern; Assisted/Manual control laws still receive normalized demands through the public command frame.
- **MUST:** Fire-versus-context arbitration has one unambiguous state result for every sampled sequence.
- **MUST:** Keyboard-only and joystick-plus-keyboard paths produce the same semantic command types.
- **R0-GATED:** Exact bindings, dwell thresholds, repeat rates, digital gain curves, ambiguity windows, and hardware latency freeze after input proof on Xemu and hardware.

---

## 12. Audio engine and latency

### 12.1 Ownership

- **MUST:** SID voices produce continuous engines, wind, RWR/weapon tones, cautions, and procedural effects where practical.
- **MUST:** Prioritized audio-DMA channels produce RIO/ATC speech and selected high-value transient samples.
- **MUST:** DMA sample data is staged into the assigned chip-RAM audio cache before playback; Attic addresses are never submitted directly to audio hardware.
- **MUST:** Every spoken callout has authoritative text fallback. Critical warnings additionally have an authoritative tone or protected visual cue.

### 12.2 Priority and service contract

| Priority | Class | Required behavior |
|---:|---|---|
| 0 | Missile warning, fire, engine/flight-control critical, stall/ground-impact warning | Preempts lower sampled audio; protected SID/alert service |
| 1 | Other immediate aircraft safety cautions | Preempts ordinary speech/effects where configured |
| 2 | Critical RIO defensive, fuel, and recovery callouts | Sample when available; text/tone fallback remains immediate |
| 3 | ATC, AIC, mission, and ordinary RIO speech | May queue, abbreviate, or fall back to text |
| 4 | Weapon transients, impacts, ambience, decorative effects | First to drop |

- **MUST:** A priority-0 tone becomes active at the next audio service opportunity and no later than the next display-frame audio service after its published event.
- **MUST:** World rendering cannot delay the audio service routine or DMA preemption decision.
- **MUST:** Critical RIO text appears through the protected display path even if its sample is preempted, absent, or late.
- **MUST:** Speech may be preempted only at an authored safe cut boundary or by immediate stop when a priority-0 warning requires it; resulting text remains available.
- **R0-GATED:** Exact service-cycle ceiling, DMA buffer/cache split, sample rate, sample format, safe cut granularity, voice duration budget, and measured latency freeze through simultaneous render/input/audio testing.

---

## 13. Mission runtime and authoring toolchain

### 13.1 Declarative JSON5 mission source

- **MUST:** Missions are authored as schema-validated JSON5, not assembly and not a target-side scripting language.
- **MUST:** Source declares metadata, resources, theater/environment, carrier/bases, entities, immutable physics classes, routes, formations, doctrine, triggers, objectives, messages, tutorial segments, state transitions, spawn/despawn rules, inventories, and authored burst limits.
- **MUST:** Every loop, repeating trigger, spawn source, and timed emission has an explicit finite bound, cooldown, lifetime, or total inventory from which a conservative maximum can be proven.
- **MUST:** The target executes bounded compiled records and tables. It contains no JSON parser, expression evaluator, heap, or general mission virtual machine.

### 13.2 Mission compiler as authority

- **MUST:** The mission schema/compiler and capacity analyzer are implemented before gameplay mission assembly code.
- **MUST:** The compiler validates schema, references, coordinate ranges, resource identities, entity types, route continuity, graph reachability, terminal outcomes, finite loops, legal doctrine assignments, palette/LOD/audio metadata, and parent gameplay requirements.
- **MUST:** It calculates conservative per-pool and combined-concurrency maxima over every legal overlap of branches, spawns, inventories, weapon flight times, gun-group lifetimes, decoy programs, despawn delay, objective state, effects, and mission entities.
- **MUST:** Mutually exclusive branches may share capacity only when exclusivity is structurally proven. Otherwise their maxima are combined.
- **MUST:** A false-positive conservative rejection is corrected by clarifying the authored graph or bounds, never by disabling validation.
- **MUST:** The compiler emits capacity, memory, resource-residency, coordinate, and combined-overlap reports and hard-rejects every non-droppable overflow.
- **MUST:** Runtime measured high-water above the compiler prediction is a tool defect and fails the mission.

### 13.3 Compiled package

- **MUST:** Output is a versioned, explicit-endian chunk package using `ResourceHandle16` references and integrity metadata.
- **MUST:** The package includes mission records, terrain-query tiles, presentation resources, routes/formations, doctrine tables, objective graph, dialogue metadata, replay identity, and a host-readable symbol/debug map.
- **MUST:** The D81/package builder produces reproducible hashes and records the complete tool/build identity.

### 13.4 Lightweight map/timeline editor

- **MUST:** The Java previewer displays terrain bounds, bases/carrier, groups, routes, formations, trigger volumes, objectives, state transitions, resource/capacity diagnostics, and a scrubbed authored timeline.
- **MUST:** Its first editing scope is limited to waypoint/route geometry, trigger-region geometry, and explicit event times.
- **MUST:** Source-range edits preserve unrelated JSON5 comments and formatting. The editor refuses a write when it cannot map an edit unambiguously to a source field.
- **MUST:** Doctrine graphs, objectives, dialogue, and arbitrary mission logic remain text-authored in Draft 0.1.
- **MUST:** Preview output is advisory; only compiler acceptance authorizes a package.

---

## 14. Asset and interface generation

### 14.1 Standard source formats

- **MUST:** Blender/glTF 2.0 is the primary source path for aircraft, ships, cockpit geometry, significant features, and authored mesh LODs.
- **MUST:** Heightfield sources use documented lossless image/raw formats; 2D art uses lossless PNG plus palette-role metadata; audio masters use PCM WAV plus event metadata.
- **MUST:** Java compilers quantize coordinates, generate/validate bounds, validate or generate permitted LOD/impostor forms, enforce palette roles, encode target resources, and report decoded/staged sizes.
- **MUST:** Target assembly never parses authoring formats.
- **MUST:** Generated resources include a source hash, compiler version, schema version, target format version, alignment, and integrity value.

### 14.2 Machine-readable interfaces

Each module has four co-located artifact classes:

1. A short English contract defining behavior and invariants.
2. A JSON5 interface definition containing records, field widths, units, ownership, public entry points, clobbers, and allowed queues.
3. Generated assembly include files and Java record bindings.
4. The 45GS02 implementation and its golden vectors/traces.

- **MUST:** Offsets and constants are generated once from the interface definition; Java and assembly do not maintain handwritten duplicate layouts.
- **MUST:** Generated assembly includes compile-time size/offset assertions and memory-region attribution.
- **MUST:** Interface changes require regenerated host/target bindings, a version increment, dependent-module rebuild, and all affected vectors.

### 14.3 Logical public records

This supplement requires logical definitions for:

- `AircraftPhysicsClass`
- `RigidBodyState`
- `KinematicAircraftState`
- `AtmosphereSample` and `WindLayerSet`
- `AeroCoefficientSet` and `EnginePerformanceTable`
- `TerrainQuery` and `ContactEvent`
- `AIIntentFrame`, `FormationCommand`, and sensor-limited `TacticalBlackboard`
- `SensorObservation`, `RadarTrackState`, and `TrackFile`
- `MissileGuidanceState` and `GunProjectileGroup`
- `MissionPackageHeader`, `MissionGraphState`, and `TutorialLessonState`
- `AudioEvent`
- `RenderWorkItem`
- `ReplayHeader`, semantic command record, and periodic checksum record

- **MUST:** Record widths and packing must satisfy §4 before they freeze.
- **TBD:** Exact layouts close at their owning phase gate and do not modify frozen public ABI types without the required revision.

---

## 15. Replay, diagnostics, and observability

- **MUST:** Normal engineering replay stores build and package identity, mission identity, all initial RNG seeds, tick-tagged semantic/player/authorized external commands, and periodic checksums.
- **MUST:** Normal replay reconstructs state from mission start. It contains no routine full-state checkpoints and no video frames.
- **MUST:** A separate development trace mode may emit bounded state and score traces to host capture; it is not a player replay format and cannot be required for release execution.
- **MUST:** PAL/NTSC, presentation tier, camera, effect allocation, and unfinished rendering cannot alter replay checksums.
- **MUST:** Diagnostics include all Revision 1.4.1 counters plus per-module cycles, code/data bytes, queue occupancy, AI observation/score traces, resource stage events, audio preemption/latency, LOD/tier selections, and compiler-bound versus measured high-water.
- **MUST:** Debug builds stop on invariant violation. Release builds remain deterministic, record the fault, and enter only parent-authorized controlled failure behavior.

---

## 16. AI-assisted modular development discipline

### 16.1 Module status board

- **MUST:** The repository maintains a machine-readable status source and generated Markdown board with one row per module.
- **MUST:** Each row records contract status, interface version, host oracle status, vector count/result, assembly bit-match status, code bytes, hot-data bytes, p95/worst cycles, open TBDs, and last accepted evidence identity.
- **MUST:** “Implemented” is not a valid terminal state. A module is accepted only when contract, interface, oracle, target match, integration, and measured budget all pass their applicable gates.

### 16.2 Change isolation

- **MUST:** Each AI-assisted change names its authorized module paths, interface version, expected behavior, prohibited files, and required test suites before editing begins.
- **MUST:** Automated diff-scope validation fails a change that modifies files outside its declared module scope.
- **MUST:** Routine module work cannot modify `CoreRuntime`, memory maps, tick order, pool definitions, public ABI, generator schemas, or another module's private state.
- **MUST:** Any authorized core or cross-interface change requires explicit human review and an invariant-impact note before implementation.
- **MUST:** Every change handoff includes the diff, generated-artifact report, tests run, golden-vector result, size/cycle delta, and invariants reverified.
- **MUST:** AI-generated target routines are reviewed as ordinary source; generated authorship does not relax listing, symbol, cycle, mapping, or hardware evidence requirements.

### 16.3 Host-first rule

- **MUST:** For math, atmosphere, flight, controls, actuators, sensors, tracks, missiles, damage, AI scoring, mission evaluation, serialization, and lifecycle behavior, the owning Java reference/oracle and vectors exist before the corresponding production assembly routine is accepted.
- **MUST:** The host suite provides subsystem oracles and production-shaped combined fixtures, not a second playable desktop game.
- **MUST:** Integration authority remains the target runtime in Xemu and on MEGA65 hardware.

---

## 17. Development order and gates

### 17.1 Pre-R0 documentation and host foundations

1. Freeze module ownership, interfaces required for R0, and the §4 ledgers.
2. Implement the interface generator, region/code-size report, source/build identity, and module status board.
3. Implement mission JSON5 schema, conservative capacity analyzer, compiled package skeleton, and diagnostic reports.
4. Implement asset metadata schemas and production-shaped mesh/terrain/palette/audio converters needed by R0.

### 17.2 R0 proof candidates

1. Prove the frozen Memory Access ABI and resident-call graph.
2. Benchmark display candidates, cockpit composition, HUD/MFD service, double buffering, and palette behavior.
3. Benchmark the bucket/painter filled pipeline, reduced-filled pipeline, wireframe contingency, LODs, and impostors using the same scene.
4. Exercise simultaneous audio DMA/SID, input service, DMA staging, and the exact protected 530,000-clock workload.
5. Select the richest passing presentation tier and publish measured subledgers, code/data headroom, scene ceilings, and shedding thresholds.

### 17.3 Phase 1 — core engines

- Build core scheduler, pools, commands/events, snapshot, replay/checksum, resources, input, audio service, renderer/display, world-query substrate, mission-record loader, and synthetic integrated harness.
- Phase 1 cannot pass until mapping, determinism, lifecycle, combined p95 timing, memory/code ceilings, reserve, audio/input latency, and PAL/NTSC equivalence all pass concurrently.

### 17.4 Phases 2–5

- **Phase 2:** Atmosphere, 6DOF/kinematic aircraft, controls, actuators, aircraft systems, ground/deck/contact, ADLC, and carrier flight mechanics.
- **Phase 3:** Geometric radar, observations/tracks, RWR, missiles, guns, countermeasures, fuzes, collision, and damage.
- **Phase 4:** Doctrine AI, formations, AIC/RIO/wingman behavior, mission graph, tutorials, Midnight Spear, and debrief evaluation.
- **Phase 5:** Campaign loading/state, remaining missions, compatibility, measured optimization, and release packaging.

- **MUST:** Optimization cannot cross a module boundary, remove a saturation/assertion, alter ordering, or consume reserve without recorded evidence and owning-gate review.

---

## 18. TBD and measured-decision register

| ID | Class | Subject | Required evidence | Gate |
|---|---|---|---|---|
| MEM-01 | R0-GATED | Rebalance within §4 subledgers | Generated byte reports plus simultaneous R0 workload; 32 KB measured reserve remains protected | Measured-limits revision |
| CPU-01 | R0-GATED | Module cycle ceilings and shedding hysteresis | Six-NTSC-frame/ten-tick p50/p95/worst reports on Xemu and hardware | R0-D–F |
| REN-01 | R0-GATED | Display mode, filled/reduced/wireframe production tiers | Identical protected-load scene, legibility capture, mandatory reserve | R0-B–F |
| REN-02 | R0-GATED | Tile sizes, LOD/impostor bins, visible ceilings | Full asset/time ledger including cheap-path costs | R0-C–F |
| AUD-01 | R0-GATED | Audio cache, rates, formats, service cycles, cut boundaries | Simultaneous render/input/audio latency and distortion tests | R0-B–F / Phase 1 |
| IN-01 | R0-GATED | Input bindings, gesture timing, gain curves | Hardware ambiguity and latency corpus | R0-B / Phase 1 |
| ENV-01 | TBD | Atmosphere/wind formats and tables | High-precision and bit-exact vectors | Phase 1–2 |
| FLT-01 | TBD | 6DOF coefficients, inertia, interpolation, thrust/fuel | Envelope, sequence, boundary, damage, and pilot-review evidence | Phase 2 |
| KIN-01 | TBD | Kinematic type envelopes | Route, formation, landing, collision, and continuity vectors | Phase 2 |
| CON-01 | TBD | Broad/swept collision bounds and contact constants | High-speed crossing, terrain, runway, deck, wire, and two-inch carrier cases | Phase 2–3 |
| SNS-01 | TBD | Scan, aspect/range, LOS, clutter/notch, jamming, track tables | Sensor geometry and track-transition corpus | Phase 3 |
| WPN-01 | TBD | Missile/gun/decoy/fuze tables | 1,000+ trajectories plus numeric boundaries and mutual-event cases | Phase 3 |
| AI-01 | TBD | Doctrine graphs, schedules, utility weights, perception memory | Sensor-limited trace corpus, tie cases, tactics review | Phase 4 |
| MIS-01 | TBD | Final mission schema fields and package chunk versions | Campaign branch, capacity, save/replay, and corrupt-package tests | Phase 4–5 |

---

## 19. Acceptance tests

### 19.1 Memory, code, and module isolation

- **MUST:** Each deliberate one-byte code/data overflow mutation fails the owning generated assertion and build.
- **MUST:** Generated layouts match Java and assembly offsets for every public record.
- **MUST:** MAP call-graph tests prove no executing/called routine is hidden by `$8000–$BFFF` mapping scopes.
- **MUST:** Attic-resource tests prove direct VIC/audio use is impossible and all use passes through validated staging.
- **MUST:** Diff-scope tests reject an AI/module change outside its declared ownership.

### 19.2 Combined runtime

- **MUST:** The Gameplay 0.2 peak harness runs nine aircraft, sixteen missiles, twenty-four gun groups, forty-eight decoys, eight dynamic mission entities, eight objectives, and sixty-four presentation effects with protected services active.
- **MUST:** Compiler bounds equal or exceed measured high-water for every pool and combined overlap.
- **MUST:** Presentation shedding walks the fixed order under induced load while simulation/replay checksums remain identical.
- **MUST:** PAL and NTSC replays match across flight, combat, damage, carrier recovery, lesson restart, and debrief.

### 19.3 World and physics

- **MUST:** Terrain height, line of sight, collision, and carrier-local queries match host vectors at tile/sector boundaries and every numeric edge.
- **MUST:** 6DOF vectors cover atmosphere, thrust, control changes, sweep/configuration, weight/inertia changes, unusual attitudes, stall/departure, energy bleed, asymmetry, damage, and saturation.
- **MUST:** Kinematic vectors cover bounded turns/climbs, route crossings, formation commands, collision, damage, and immutable class behavior.
- **MUST:** Missile vectors cover loft, climb/descent density changes, motor burnout, hard turns, support loss, seeker limits, notch/decoy interaction, fuze miss, and mutual kill.

### 19.4 Rendering, input, and audio

- **MUST:** The same R0 scene reports filled, reduced, wireframe, LOD, and impostor costs including transforms, asset bytes, composition, DMA, and overdraw.
- **MUST:** Incomplete buffers never display; camera/view/tier changes never alter checksums.
- **MUST:** Input corpus covers all semantic commands, context transitions, fire arbitration, held/repeated keys, keyboard-only, and joystick-plus-keyboard paths.
- **MUST:** Priority-0 warning tone begins within the §12 service contract under maximum validated render/DMA load.
- **MUST:** Speech preemption, text fallback, missing samples, and sample-cache pressure never hide authoritative gameplay information.

### 19.5 Sensors, AI, missions, and tools

- **MUST:** Radar/track cases cover field-of-regard edges, terrain masking, look-down clutter, notch geometry, jamming, observation fusion, coast/drop, priority overflow, and replay parity.
- **MUST:** AI traces prove each decision from authorized observations and deterministic score/tie rules; hidden-contact mutations cannot influence behavior until detected or received by datalink.
- **MUST:** The compiler accepts the required peak mission and rejects one-slot overflow, unbounded loop, illegal scenery target, ambiguous exclusivity, invalid handle/resource, coordinate overflow, and corrupt package mutations.
- **MUST:** Previewer route/time edits preserve unrelated comments/data and must recompile before use.
- **MUST:** Every module gate includes contract, generated interface, host oracle, target bit match, code/data report, cycle report, integration result, and module-status update.

---

## 20. Draft 0.1 decision log

| Decision | Class | Reason |
|---|---|---|
| Separate subordinate engine supplement | MUST | Keeps architecture, gameplay, and implementation authority distinct |
| Sacred core with isolated modules | MUST | Protects determinism and makes AI-assisted changes reviewable |
| Concrete pre-R0 byte and code ceilings | MUST | Prevents 384 KB chip RAM and resident code from becoming late surprises |
| Two immutable aircraft physics classes | MUST | Preserves combat fidelity without model promotion or a second clock |
| Whole-aircraft coefficient 6DOF | MUST | Produces credible flight without unaffordable airfoil/flow simulation |
| Hybrid terrain/query tiles | MUST / R0-GATED | Separates authoritative physics/sensor queries from measured visual LOD |
| Bucket/painter renderer with measured tiers | MUST / R0-GATED | Avoids a Z-buffer and lets R0 select the richest proven presentation |
| Impostors consume explicit ledger cost | MUST | Prevents the cheap path from escaping memory/timing proof |
| Geometric radar and sensor-limited AI | MUST | Preserves tactics at bounded cost and prevents omniscient behavior |
| SID continuous audio plus prioritized DMA speech | MUST / R0-GATED | Protects warnings while containing sample RAM and bandwidth |
| JSON5 declarative missions and authoritative compiler | MUST | Moves complexity to host tools and proves capacity before target execution |
| Java subsystem oracles, not a desktop twin | MUST | Provides bit-exact validation without maintaining a second game |
| Commands plus checksums replay | MUST | Preserves deterministic diagnosis with bounded storage |
| No tactical disk reads or code overlays | MUST | Removes media/mapping latency from protected flight execution |
| AI changes use declared module scope and evidence | MUST | Lets a non-assembly owner iterate without allowing silent invariant damage |

---

## 21. Smallest authorized next milestone

The next work remains inside R0-A and host-foundation preparation:

1. Encode the §4 region and resident-code ceilings in a generated ledger schema.
2. Define the initial machine-readable interfaces for `CoreRuntime`, `InputCommandFrame`, entity common headers, resource handles, and renderer proof records.
3. Implement the module status source/report and diff-scope validator.
4. Implement the JSON5 mission schema skeleton and conservative frozen-pool capacity report using the Gameplay 0.2 peak case as its first fixture.
5. Produce the reproducible Memory Access ABI proof D81 with complete identity, symbols, listings, cycle/mapping/DMA/IRQ instrumentation, and no gameplay code.

- **MUST:** This milestone contains no flight, radar, weapon, tactical AI, campaign, or production renderer implementation.
- **MUST:** Passing it does not waive any R0 or Phase 1 gate.

### 21.1 Published bootstrap artifacts

The first non-gameplay deliverable is published with Draft 0.1:

| Artifact | Authority |
|---|---|
| `engine_tooling/schemas/memory-ledger.schema.json` | Machine-readable structure and validation rules for physical regions, allocations, code budgets, and reserve ownership |
| `engine_tooling/ledgers/memory-ledger.draft-0.1.json` | Draft 0.1 ledger data matching §4, including explicitly unallocated code/simulation reserves |
| `engine_tooling/status/module-status.draft-0.1.tsv` | Machine-readable bootstrap module-status source |
| `engine_tooling/status/MODULE_STATUS.md` | Human-readable status board generated from the TSV source |
| `engine_tooling/src/main/java/f65/tools/StatusBoardGenerator.java` | Dependency-free bootstrap board generator |

- **MUST:** The ledger JSON is the machine-readable mirror of §4, not an independent authority. A mismatch fails review and must be corrected in the document and data together.
- **MUST:** The status Markdown is generated output and is not edited by hand.
