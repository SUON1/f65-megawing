# F65 Main Concept v1.6

## Product, Architecture, Integration, and Development Master

**Document ID:** `F65-MAIN-1.6`  
**Version:** 1.6  
**Status:** FINAL - HUMAN-REVIEWED  
**Authority:** Active master baseline  
**Human review completed:** 27 August 2026  
**Date:** 27 August 2026  
**Platform:** MEGA65 - 45GS02 + VIC-IV  
**Engine name:** **65Aero**  
**Primary purpose:** Master product concept, architecture, high-level subsystem integration, and development plan  
**Supersedes:** `F-65 Megawing Revision 1.5.1 - Architecture Invariants and Gameplay Alignment`  
**Retires:** `F-65 Technical Alignment and Read-First Supplement` as an active design authority; `F65-GAD-001` as a separate active architecture memo because its durable graphics decisions are absorbed here  

> **Revision 1.6 consolidates the durable architecture of F-65 Megawing into the master document.** This final human-reviewed revision incorporates the accepted engineering direction from the current Flight Physics, Graphics, Audio, Radar/Sensor, and AI Behavior/Decision white papers; preserves the proven MEGA65 platform, memory, timing, deterministic-runtime, and C/45GS02 contracts; incorporates the reviewed Product Story framing; and retains the development baseline with R0-A, R0-B, and R0-C complete and R0-D current. Human review is complete. Revision 1.6 is the active Main Concept baseline for the Gameplay v1 and 65Aero Runtime v1 rewrites and for continued R0-D/E/F production work.

---

## 0. Purpose, authority, and document family

### 0.1 Purpose

F65 Main Concept v1.6 is the highest-level active design document for F-65 Megawing. It defines:

- what the product is;
- the immutable or architecture-level properties of the simulation;
- the division of responsibility among the major 65Aero subsystems;
- the high-level physics, graphics, sensor, weapon, audio, input, AI, mission, storage, and toolchain models;
- the fixed development order and acceptance gates;
- the relationship between the master architecture, player-facing gameplay requirements, low-level runtime engineering, and subsystem white papers.

This document intentionally does **not** reproduce every coefficient table, radar schedule, render-pool count, sound envelope, or implementation structure. Those belong in the appropriate subordinate document or generated registry.

### 0.2 Active design-document hierarchy

The controlled F-65 design hierarchy consists of **eight** documents:

1. **F65 Main Concept v1.6** - master product and architecture authority.
2. **F65 Gameplay and Simulation Supplement v1** - player-facing behavior, aircraft operation, missions, campaign, controls, presentation, and gameplay acceptance.
3. **F65 65Aero Engine Runtime and Technical Supplement v1** - low-level implementation umbrella for the complete backend/game engine.
4. **F65 Flight Physics and Simulation Engineering White Paper v3.3** - detailed 6DOF, atmosphere, engine, FCS, actuator, mass-property, and validation model.
5. **F65 Graphics Engineering White Paper v2.1** - detailed hybrid world renderer, presentation, LOD, occlusion, world-registration, and VIC-IV integration model.
6. **F65 Audio, Sound Effects and Music Engineering White Paper v1.0** - detailed SID/PCM, warning, music, speech, priority, and audio integration model.
7. **F65 Radar, Sensors and Track Engineering White Paper v1.0** - publication name for the human-reviewed SensorAndTrackEngine Phase-3 v1.0 baseline; detailed radar, track, tactical-link, seeker-assessment, RWR, IR-signature, and countermeasure model.
8. **F65 AI Behavior and Decision Architecture White Paper v1.0** - detailed deterministic hierarchical AI, bounded knowledge, mobility/procedural, doctrine, tactical decision, and AI-to-engine intent model.

The first three documents are the core specification set. The **five** white papers provide subsystem engineering depth. White papers do not independently override the core three; durable subsystem changes are propagated upward through controlled revisions.

### 0.3 Authority and precedence

When two active documents touch the same subject, precedence is:

1. **F65 Main Concept v1.6** controls product scope, architecture, ownership, timing, determinism, memory boundaries, high-level subsystem contracts, and development gates.
2. **F65 Gameplay and Simulation Supplement v1** controls observable player behavior inside the Main Concept invariants.
3. **F65 65Aero Engine Runtime and Technical Supplement v1** controls implementation architecture and integration inside the Main Concept and Gameplay contracts.
4. The **five subsystem white papers** control detailed subsystem engineering only where they do not conflict with the core three.
5. Generated schemas, registries, ledgers, test catalogs, build locks, and evidence records implement and prove the design; they are not independent design authorities.

A human-reviewed white paper may intentionally identify an older parent concept that must be corrected. Revision 1.6 is the controlled propagation point for the accepted high-level concepts from the current Physics, Graphics, Audio, Radar/Sensors, and AI white papers. Detailed algorithms, tables, record layouts, tuning data, equations, and implementation mechanics remain in the relevant white paper and 65Aero Runtime document.

Future revisions should preserve this flow: decide or revise detailed subsystem engineering, propagate any durable architectural consequence into Main Concept, then reconcile Gameplay and 65Aero Runtime. Do not accumulate new overlay authority documents.

### 0.4 Retired alignment layer

The Read-First / Technical Alignment document family is retired from the active design hierarchy by Revision 1.6. It remains archived for provenance only.

Revision 1.6 does **not** recreate a separate first-read, overlay, or correction authority inside the Main Concept. Current product and architecture requirements must live in the Main Concept, Gameplay v1, 65Aero Runtime v1, the five subordinate white papers, or their generated implementation/evidence artifacts according to the hierarchy in §0.2-0.3.

### 0.5 Requirement classes

This document uses four requirement classes:

- **MUST** - durable product or architecture contract.
- **TARGET** - intended engineering or product target that may move through recorded evidence or human review.
- **R0-GATED / MEASURED** - hardware-dependent value that freezes only through the R0 evidence and measured-limits process.
- **TBD** - required value, table, content, or threshold whose selection belongs to a named later phase or human decision.

Implementation may not convert TARGET, R0-GATED, or TBD material into a shipping constant merely because a convenient value is needed for a prototype.

---

## 1. Product concept

### 1.1 F-65 Megawing

F-65 Megawing is a single-player, cockpit-primary, retro-synthwave fleet-interceptor combat-flight simulator built specifically for the MEGA65.

The game combines:

- consequential flight physics;
- meaningful aircraft systems and failures;
- long-range interception and beyond-visual-range combat;
- carrier and airfield operations;
- an AI Radar Intercept Officer (RIO);
- wingman, AIC, enemy AI, and tactical-link support;
- radar, RWR, jammer, countermeasures, active-radar and passive-IR missile combat;
- a deliberately early-1990s visual and interaction character;
- SID-led procedural audio and synthwave music with PCM used selectively for speech and high-information transients.

The intended feel draws from the early flight-simulator lineage, Chuck Yeager's Advanced Flight Trainer, early subLOGIC/Microsoft Flight Simulator, A-10 Cuba!, F/A-18 Korea, and Falcon 3.0. These are feel and presentation references, not feature checklists or technical authorities.

### 1.2 Player aircraft

The player aircraft is the fictional **F-65A**, a large two-seat, twin-engine, variable-geometry fleet interceptor.

At the master level the F-65A includes:

- two independently modeled engines;
- variable left/right wing sweep;
- retractable landing gear, flaps, speedbrake and arresting hook as required by the detailed gameplay model;
- electrical, hydraulic, fuel, flight-control, radar, jammer, RWR, countermeasure, weapon, and damage systems;
- AI RIO support;
- a standard combat load of six long-range radar missiles, two medium-range radar missiles, two heaters, and 675 cannon rounds;
- carrier catapult launch and arrested recovery;
- airfield takeoff and landing;
- cockpit-primary operation with a low-cost chase view.

The final Gameplay Supplement defines the player's exact cockpit interactions, control bindings, procedures, failure handling, loadout rules, and mission behavior.

### 1.3 Presentation identity

The core presentation identity is:

- bubble-canopy cockpit-primary view;
- green monochrome HUD as the primary flight-data display;
- right-side RIO-operated fused radar/navigation presentation;
- left-side grayscale aircraft-status presentation;
- aviation-facing units including nmi, knots, feet, lb, lbf, lb/hour, psi, and G;
- positive-G desaturation beginning near +6 G and reaching grayscale near +7 G;
- early-1990s low-poly/impostor combat-flight-sim visual language rather than photorealism;
- retro-synthwave music and limited-polyphony audio designed as part of the cockpit information system, not merely background decoration.

### 1.4 Control contexts

The four semantic control contexts remain:

- **Deck**
- **TFL** - Takeoff and Landing
- **Normal Flight**
- **Combat**

Control context changes input semantics and presentation. It does **not** itself select the physical flight-control law.

### 1.5 World, origin, and campaign premise

The attached Product Story supplies a deliberately light, slightly tongue-in-cheek origin frame while the flying, systems, and combat remain serious.

For this **human-reviewed v1.6 baseline**, the world framing is:

- the **Coalition of American States (CAS)** projects power through carrier groups and long-range fleet interception;
- the **Pacific Directorate** is expanding a chain of reef outposts and runways around the independent island city-state of **Aurelia**;
- the CAS sends carrier forces into the approaches, and the player is an F-65A pilot flying cover for that deployment;
- **Aero Dynamics West** developed the F-65A after President **Richard Rump**, portrayed in the Product Story as openly nostalgic for large carriers and swing-wing fleet interceptors, pushed for a modern 4.5-generation two-seat, twin-engine, variable-geometry interceptor with strong 1980s design DNA;
- the F-65A is therefore both a serious contemporary combat aircraft inside the fiction and a knowingly nostalgic product statement.

The Product Story's visual framing also reinforces variable-sweep geometry as the defining aircraft silhouette, a dusk carrier-catapult launch as a principal visual identity, and the pilot-forward/RIO-aft cockpit with green HUD and dual displays.

**Configuration-control disposition:** older architecture material used **Meridian Maritime Compact** versus **Boreal Directorate**. The supplied Product Story instead uses CAS, Pacific Directorate, and Aurelia and explicitly identifies itself as origin framing for Main Concept v1.6. Human review of Revision 1.6 adopts the Product Story naming as the active master framing. The older faction labels remain archived provenance rather than silently erased history.

The campaign/product scope remains:

- a non-narrative **Technical Combat Slice** used to prove integrated combat systems;
- the separately authored **Midnight Spear** mission after its own manifest is approved;
- a ten-operation campaign;
- two endings;
- one independently bootable MVP D81;
- multi-D81 campaign packaging where required and supported.

Operations, dialogue, detailed mission geometry, ending predicates, and authored campaign content not already fixed elsewhere remain Gameplay/content work. This Main Concept does not invent additional wars, governments, dates, character biographies, political ideology, or campaign events beyond the supplied Product Story.

---

## 2. MEGA65 platform and implementation model

### 2.1 Target platform

F-65 is designed for the MEGA65 and its 45GS02 CPU, VIC-IV video subsystem, DMA engine, SID audio resources, PCM/audio-DMA channels, chip RAM, and Attic RAM.

The design assumes the verified platform baseline established through R0 rather than generic 6502 behavior.

### 2.2 Production language policy

**MUST:** Primary production target code is C compiled with LLVM-MOS for the verified MEGA65/45GS02 target.

Handwritten 45GS02 assembly remains a first-class production tool for:

- platform wrappers;
- interrupt and vector handling;
- MAP/base-page operations;
- DMA control;
- Q/extended-register and hardware-math use;
- VIC-IV or audio-register primitives;
- cycle-bounded hot kernels;
- renderer inner loops;
- fixed-point kernels;
- measured compiler offenders that fail approved timing or memory budgets.

There is no required C/assembly percentage. C is not a throwaway prototype language, and assembly is not the default merely because the platform is an 8-bit lineage machine.

### 2.3 Host engineering language and independent verification

**Java is host-development tooling only. It does not run on the MEGA65.**

Java executes on the developer Mac/PC and is not shipped as part of the MEGA65 runtime, is not required by the player, and has no role in the live 45GS02 execution environment.

Host Java is used where appropriate for:

- independent high-precision physics or subsystem oracles;
- bit-exact fixed-point reference models;
- generated schemas and interface bindings;
- asset conversion;
- mission compilation;
- capacity validation;
- table generation;
- golden-vector generation;
- build and evidence validation; and
- offline engineering analysis.

The actual MEGA65 target executes only the admitted target artifacts: LLVM-MOS-generated C, selected handwritten 45GS02 assembly, and generated data/resources.

The purpose of the independent host implementation is verification, not runtime dependency. Where a subsystem requires both reference layers, the conceptual chain is:

```text
high-precision host model
    ->
bit-exact fixed-point host reference
    ->
production MEGA65 C
    ->
measured handwritten ASM replacement only where justified
```

The high-precision model establishes the intended physical/engineering result within tolerance. The bit-exact host reference establishes the exact integer/fixed-point behavior expected from the target implementation. Production C is then tested against those references. Assembly is admitted only for measured or platform-critical reasons and must preserve the same public behavior unless an approved contract says otherwise.

Not every subsystem is required to contain two complete Java implementations. The relevant white paper and 65Aero Runtime specification define which host oracle/reference artifacts are required for that subsystem. The architectural requirement is independent, testable host reference behavior where such a reference is necessary to prove the target implementation.

### 2.4 Deterministic target-C restrictions

Authoritative runtime code follows a restricted deterministic C profile:

- no general-purpose deterministic-runtime heap;
- no uncontrolled recursion;
- no unbounded automatic allocations;
- no target floating point in authoritative simulation;
- fixed-width integer types for public, deterministic, serialized, hardware-facing, and fixed-point state;
- bounded and instrumented stack use;
- no public reliance on compiler-specific structure packing, bit-field layout, enum size, or pointer size;
- no arbitrary MEGA65 physical address represented by an ordinary C pointer;
- hardware ownership remains behind PlatformABI / CoreRuntime services.

### 2.5 Platform ABI

C and handwritten assembly cross one narrow, generated, version-pinned ABI boundary. Public entry points define and test:

- symbol/linkage rules;
- argument and return conventions;
- A/X/Y/Z/Q and status preservation/clobber rules;
- compiler scratch/base-page rules;
- hardware/software stack assumptions;
- IRQ/NMI assumptions;
- canonical MAP state;
- base page restored to `$0200`;
- `$01 = $35` and required I/O personality;
- no hidden mapping state across public calls.

---

## 3. 65Aero - the F-65 simulation and game engine

### 3.1 Engine identity

The complete F-65 backend/game-engine architecture is named **65Aero**.

65Aero is not only the flight model. It is the integrated deterministic runtime that owns or coordinates:

- platform services;
- memory and DMA;
- scheduler and tick semantics;
- entity pools;
- environment/world queries;
- controls and aircraft systems;
- flight dynamics;
- contact and carrier mechanics;
- weapons and damage;
- sensors, tracks, tactical links, seekers, RWR and threat state;
- AI, RIO, wingman and AIC behavior;
- missions and scoring;
- presentation extraction;
- graphics;
- audio;
- resources and storage;
- replay, checksum, diagnostics, fault injection, and evidence.

### 3.2 Core module graph

At the architecture level 65Aero is organized as:

```text
CoreRuntime
|-- PlatformABI
|-- InputEngine
|-- EnvironmentEngine
|-- ControlAndSystemsEngine
|-- FlightDynamicsEngine
|-- ContactEngine
|-- WeaponAndDamageEngine
|-- SensorAndTrackEngine
|-- AIEngine
|-- MissionEngine
|-- PresentationExtractor
|-- GraphicsEngine
|-- AudioEngine
|-- ResourceManager
|-- StorageService
`-- Diagnostics
```

`AIEngine` is no longer a thin generic "utility AI" placeholder. At the master level it owns bounded deterministic decision state, hierarchical doctrine evaluation, legal knowledge consumption, held intent state, formation/team coordination state, mobility/procedural state, and the stage-16 production of `AIIntentFrame` outputs. It does **not** own sensors, flight physics, aircraft systems, weapons, damage, or mission truth.

The key authority path is:

```text
SensorAndTrackEngine
    -> legal side/domain-specific knowledge and declared views
AIEngine
    -> deterministic AIIntentFrame / bounded next-tick intent
CoreRuntime command/intent application
    ->
ControlAndSystemsEngine / WeaponAndDamageEngine / SensorAndTrackEngine
    ->
physical and system consequences through the owning modules
```

`MissionEngine` supplies authored objectives, ROE, route/task references, mission posture, and other allowed mission state. It does not give AI unrestricted access to global truth.

The v1 65Aero Engine Runtime and Technical Supplement will define the exact public records, APIs, generated interfaces, ownership ledgers, build layout, AI state/cycle budgets, and evidence requirements.

### 3.3 Sacred CoreRuntime boundary

CoreRuntime exclusively owns:

- the 100 Hz authoritative clock and tick dispatcher;
- canonical mapping/base page/stack/vector state;
- entity allocation and lifecycle commit;
- deterministic command and event ordering;
- DMA arbitration and submission ownership;
- RNG stream initialization and checksum orchestration;
- presentation extraction coordination and snapshot publication;
- deadline debt and protected-service arbitration.

No gameplay or subsystem module may independently change the simulation clock, execute MAP, start DMA hardware, publish a presentation snapshot, or allocate outside its fixed pool.

### 3.4 Cross-module isolation

Modules communicate only through approved:

- read-only views;
- command frames and intent frames;
- deterministic events;
- core-owned bounded queues;
- resource handles;
- fixed cross-tick handoff state;
- immutable `PresentationSnapshot` fields.

A module does not reach into another module's private arrays simply because both happen to occupy the same physical RAM region.

For AI specifically:

- `SensorAndTrackEngine` exposes only legal side/domain knowledge and declared projections such as tactical tracks, RWR/threat state, visual-contact data, and other approved views;
- `WeaponAndDamageEngine` exposes bounded own-weapon status/employment projections rather than private missile truth;
- `MissionEngine` exposes objectives, ROE, authored routes/goals, facility/task information, and mission posture as allowed;
- `AIEngine` produces bounded intents and never directly edits position, velocity, G, control surfaces, sensor detection, missile state, damage state, or mission state.

Any authoritative AI state that can affect future simulation behavior participates in the canonical deterministic state/replay/checksum model. Read-only debug traces do not become authority.

---

## 4. Deterministic simulation architecture

### 4.1 Single authoritative clock

**MUST:** `ACTIVE_SORTIE` simulation runs at exactly **100 Hz**.

The complete authoritative simulation tick is therefore **10 ms**. Every live physical aircraft, missile, countermeasure, projectile group, ship/surface entity, and other authoritative physical entity advances on this same 100 Hz timeline according to its declared physical model.

There is no secondary physical-integration clock for distant, invisible, AI-controlled, or simplified entities. An approved `KINEMATIC` aircraft class may use a cheaper physical model, but it still advances on the same 100 Hz authoritative timeline and remains subordinate to `FlightDynamicsEngine`.

Lower-rate work is permitted only where the architecture explicitly schedules decision production or presentation/audio services without changing the physical timeline. In particular, AI deliberation may run at deterministic lower logical cadences inside stage 16 while the AI-controlled aircraft itself continues to integrate physically every 10 ms.

### 4.2 Exact 21-stage tick order

**100 Hz is the frequency of the complete authoritative tick. The 21 stages are ordered operations inside that one tick.** They are not 21 different simulation rates, are not 21 separate ticks, and are not equal CPU-time slices. A stage may perform substantial work on one tick and almost nothing on another. No architecture rule expects each stage to consume one twenty-first of 10 ms.

Conceptually:

```text
Tick N (10 ms authoritative step)
    Stage 1
    Stage 2
    ...
    Stage 21

Tick N+1 (next 10 ms authoritative step)
    Stage 1
    Stage 2
    ...
    Stage 21
```

The authoritative order is:

1. Increment `SimulationTick`.
2. Latch `InputCommandFrame`.
3. Apply queued commands and prior-tick directives.
4. Update environment and carrier motion.
5. Resolve electrical, fuel, engine, and hydraulic supply.
6. Run flight-control laws and stability augmentation.
7. Apply actuator authority, rates, damage, asymmetry, and control mixing.
8. Sample atmosphere and calculate forces.
9. Integrate aircraft motion.
10. Resolve terrain, runway, deck, arrestment, and contact.
11. Accept weapon requests and create pending spawns.
12. Integrate existing weapons and countermeasures; consume eligible prior-tick sensor/support handoffs.
13. Detect collision, fuze, and damage events.
14. Accumulate and apply damage deterministically.
15. Run `SensorAndTrackEngine`: observations, organic radar, tactical-link ingest/fusion, semantic tracks, seeker assessment, weapon-support updates, RWR, and threat state.
16. Run the deterministic AI/RIO scheduler and due decision services; any newly produced `AIIntentFrame`/commands become eligible **no earlier than the following tick**.
17. Update mission objectives and scoring.
18. Commit despawns and spawns.
19. Extract bounded cockpit, warning, audio, and presentation state.
20. Calculate the canonical authoritative checksum.
21. Atomically publish a complete `PresentationSnapshot`.

The stage-15 internal order is further defined by the Radar, Sensors and Track White Paper and the 65Aero Runtime Supplement.

#### 4.2.1 Stage-15 / stage-16 AI causality

AI-controlled physical entities still move at 100 Hz. AI decision logic does not need to recompute every tactical or navigational decision at 100 Hz.

The durable relationship is:

```text
100 Hz physical simulation
    ->
stage 15 completes legal sensor/track state
    ->
stage 16 AI/RIO scheduler
    - reflex/safety evaluation when due
    - doctrine/tactical evaluation when due
    - navigation/operational evaluation when due
    - slower reassessment when due
    ->
bounded AIIntentFrame / command output
    ->
eligible no earlier than the following simulation tick
```

Exact AI service cadences remain later-gated unless explicitly frozen by the AI white paper or a subsequent approved specification. If a service is not due, the applicable previously approved held intent remains active and the owning high-rate controller continues closing against it on every 100 Hz physical tick.

No stage-16 result may create same-tick feedback into flight physics, weapons, sensors, damage, or mission state.

### 4.3 Simultaneous-event rules

- deterministic events sort by event class, source handle, target handle, then producer sequence;
- commands valid at tick start execute before damage produced later in the same tick;
- mutual kills are legal;
- component damage accumulates before capability recalculation;
- freed pool slots are not reused before stage 18 lifecycle commit;
- new entities begin updates on the next tick;
- presentation order never changes simulation order.

### 4.4 Deterministic arithmetic and RNG

Authoritative arithmetic uses generated fixed-point/integer contracts with explicit range, rounding, saturation, and fault behavior. RNG streams are owned and seeded by declared systems so changes in presentation, frame rate, or unrelated subsystems cannot perturb combat or simulation results.

### 4.5 Pause

Full pause freezes authoritative simulation advancement. Presentation/UI work may continue under the Gameplay and 65Aero Runtime rules, but it may not invent new physical, sensor, weapon, damage, or mission events while simulation time is frozen.

### 4.6 Product performance bar

The product performance goal is **responsive simulation with protected cockpit information and a consistently complete outside-world picture**, not display-rate world rendering at any cost.

- **MUST:** `ACTIVE_SORTIE` remains exactly 100 Hz. A late world frame is never permission to slip, merge, stretch, or reorder an authoritative simulation tick.
- **MUST:** HUD/cockpit composition, critical warnings, input service, protected audio, and other protected services retain their approved deadlines independently of world-frame construction.
- **MUST:** World construction uses remaining time, may yield and resume, and publishes complete buffers only. Sustained completed-world cadence below **20 Hz** is a failure condition, not permission to reduce simulation fidelity or create another physical clock.
- **TARGET:** Completed-world presentation should reach approximately **30 Hz in ordinary cruise** and **25 Hz under the approved combined-combat load**, subject to R0-D/E measurement and R0-F physical-hardware confirmation.
- **R0-GATED / MEASURED:** Maximum permitted displayed-world age remains a measured value. It is instrumented in R0-D/E, confirmed on physical hardware in R0-F, and frozen only through measured-limits closure.
- **MUST:** If presentation falls behind, the engine sheds optional presentation cost and world detail according to the approved degradation policy before compromising protected services. Presentation cadence or LOD never changes the physical aircraft clock, sensor causality, weapon causality, AI knowledge, or authoritative checksum.

Detailed per-stage CPU ceilings, exact warning/input latency budgets, and final world-age limits belong to R0-D/E/F evidence and the 65Aero Runtime technical ledgers rather than this master document.

---

## 5. Memory, mapping, DMA, and resource architecture

### 5.1 Complete MEGA65 memory picture

Revision 1.6 distinguishes three materially different memory resources. They are not interchangeable pools.

#### A. General fast chip RAM - 384 KB

Physical `$000000-$05FFFF` is the primary fast RAM used for executable code, authoritative runtime state, display stores, workspaces, staging, and reserve. The high-level ownership map remains:

| Physical range | Size | Primary ownership |
|---|---:|---|
| `$000000-$00FFFF` | 64 KB | Resident executable, base page, stack, vectors, scheduler, hot state |
| `$010000-$017FFF` | 32 KB | Active simulation, entities, aircraft systems, sensor/track, AI and tactical state |
| `$018000-$01BFFF` | 16 KB | Audio state, mission-hot data, bounded queues and cross-tick handoff state |
| `$01C000-$01CFFF` | 4 KB | Display pointer tables and display-control records |
| `$01D000-$01FFFF` | 12 KB | Shared scratch and transient CPU workspace |
| `$020000-$02FFFF` | 64 KB | Display store A |
| `$030000-$03FFFF` | 64 KB | Display store B |
| `$040000-$047FFF` | 32 KB | Cockpit, HUD, MFD, sprite and palette assets |
| `$048000-$04FFFF` | 32 KB | Renderer clipping, bucket, occlusion and span workspace |
| `$050000-$057FFF` | 32 KB | Resource staging and DMA lists |
| `$058000-$05FFFF` | 32 KB | Measured-limits reserve |

The `$010000-$017FFF` region's internal SensorTrack/AI subledger is **not** frozen by this high-level table. Revision 1.6 adopts two 24-track tactical knowledge domains plus persistent `SensorHandoffState` and the new bounded AI owner. The 65Aero Runtime ledgers and generated schemas must regenerate the exact internal allocation without silently borrowing from another owner or consuming the measured-limits reserve.

**Phase-1 closure rule:** the generated ledger must prove that the complete `$010000-$017FFF` active-simulation region fits using the actual generated sizes for entity/system state, both SensorTrack knowledge domains, `SensorHandoffState`, command/intent state, and bounded AI persistent state **before any Phase-2, Phase-3, or Phase-4 resident state is admitted as production-ready**. The 32 KB reserve at `$058000-$05FFFF` is not a donor for baseline overflow. If the active-simulation ledger does not close, the owning records/suballocations must be corrected through the normal architecture and measured-limits process rather than borrowing reserve or display memory.

#### B. VIC-IV Color RAM - 32 KB

Physical `$FF80000-$FF87FFF` is **32 KB of VIC-IV Color RAM**. It is a separate presentation/video hardware resource owned through the protected graphics/platform path.

It is not additional general simulation RAM and is not available as an undocumented extension of the authoritative entity/system heap. Its exact packing, allocation, palette/attribute usage, and display-mode relationship are controlled by Graphics and 65Aero Runtime under the measured configuration.

#### C. Attic RAM - normally 8 MB

Physical `$8000000-$87FFFFF` is normally **8 MB of Attic RAM** used primarily for cold/large resources, mission packages, generated tables/assets, and controlled staging sources.

Attic RAM is not a second general mutable authoritative-simulation heap. Consumers that cannot directly use Attic data receive it through bounded `ResourceManager`/DMA staging and approved residency rules. A tactical update or required presentation service may not stall indefinitely waiting for optional Attic content.

### 5.2 Canonical CPU-visible state

Public 65Aero routines assume the canonical CPU-visible map established by R0, including:

- hardware stack at `$0100-$01FF`;
- relocated game base page at `$0200-$02FF`;
- temporary MAP windows only in `$8000-$BFFF`;
- MEGA65 I/O personality in the appropriate range;
- critical resident code/vectors never covered by temporary mapping;
- canonical mapping restored before return or yield.

### 5.3 MemoryAccessABI

Only the protected memory/platform layer may manipulate MAP or arbitrary physical memory windows. Public physical-memory semantics use `FarPtr32`, `ResourceHandle16`, generated address classes, and approved platform wrappers.

### 5.4 DMA

Only the CoreRuntime/Platform DMA service starts DMA jobs.

Every DMA request declares and validates:

- normalized physical source/destination;
- address classes;
- length and overlap legality;
- list storage lifetime;
- deadline class;
- completion behavior;
- interaction with protected audio/display service.

World-render DMA is subordinate to protected presentation/audio latency contracts and is split into bounded jobs where required. No blocking job is described as preemptible merely because its submission API is asynchronous.

### 5.5 Attic RAM and residency

Attic RAM is the cold/large-resource tier described in §5.1, not a second mutable authoritative simulation heap.

Mission resources are loaded and staged through `ResourceManager`. A valid tactical frame or simulation update cannot depend on an unbounded disk or Attic fetch completing at an arbitrary time.

Graphics and audio therefore define resident fallback behavior. Missing optional high-detail graphics fall to a cheaper resident LOD; unavailable optional PCM falls to SID/text/visual fallback according to priority. AI route/doctrine resources required for a live entity must likewise follow deterministic mission-load/hot-residency rules rather than ad hoc runtime allocation or path search.

### 5.6 Storage and tactical I/O

Tactical packages are preloaded. Ordinary disk access is inactive during authoritative combat simulation except for a separately approved bounded diagnostic/fault path.

R0-C is considered complete for the Revision 1.6 program baseline. The previously unresolved reversible post-ROM-reclaim storage-service mechanism is reclassified as a later `StorageService` implementation/acceptance concern. It does not reopen R0-C. It must still be resolved before any Phase-1/production feature depends on such restoration.

---

## 6. Entity identity, capacity, and lifecycle

### 6.1 EntityHandle

The canonical `EntityHandle` remains four bytes:

- entity type;
- pool index;
- 16-bit generation.

Zero and generation-zero forms remain invalid/reserved. Stale generations fail validation.

### 6.2 Capacity envelope versus required live load

A **pool capacity** is the hard maximum number of records the runtime can own for that class. A **required live peak** is a specific acceptance/stress scenario the product must support. Mission authoring may use any legal load up to the hard capacities, but the mission compiler must prove that required non-droppable peaks cannot exceed them. Unused capacity is headroom, not an invitation for an AI or mission author to assume every pool can be saturated simultaneously.

| Pool / state | Hard capacity | Required current live peak / interpretation | Headroom / note |
|---|---:|---:|---|
| Aircraft | **16** | **9 simultaneously live aircraft**; baseline acceptance harness = **6 `SIX_DOF` + 3 `KINEMATIC`**, with a `KINEMATIC` AIC. A `SIX_DOF` AIC is a separately identified/compiler-proved harness variant; mission behavior remains governed by §6.4 | **7 aircraft slots** |
| Ships and carriers | 8 | 1 in the baseline air-combat overlap | 7 in that overlap |
| Surface radar/SAM entities | 16 | scenario-dependent; surface profile validated separately | capacity remains 16 |
| Guided missiles | 32 | 16 simultaneously live | 16 |
| Gun projectile groups | 32 | 24 simultaneously live | 8 |
| Chaff/flare entities | 64 | 48 simultaneously live | 16 |
| Dynamic mission entities | 32 | 8 in the baseline overlap | 24 |
| Simulation-relevant effects | 32 | currently no required persistent physical-effect peak | capacity remains 32 |
| Presentation effects | 64 | 64 optional presentation effects may be stressed | 0 in that test; droppable by policy |
| Radar truth contacts | 32 shared physical candidates | scenario-dependent | shared candidate set |
| Semantic tactical tracks | **24 per tactical-link knowledge domain** | two current domains: MEGA/BLUE and RED | **maximum 48 physical semantic-track records** |
| RIO priority tracks | 4 | subset of MEGA-domain tracks only | not a third/global track pool |
| Active objectives | 16 | 8 in baseline opening-operation stress | 8 |

For semantic tactical tracks, exact record size and final SensorTrack byte allocation remain generated/measured. The old 1,920-byte single-24-track interpretation is not the final architecture. `SensorHandoffState` is also persistent owned memory and its missile mailboxes/link queue are charged to `SensorAndTrackEngine`.

### 6.3 Lifecycle

- lowest free pool index is used for allocation;
- despawns commit deterministically before allocations;
- spawn requests sort by class priority, requester, and sequence;
- slots become reusable only at lifecycle commit;
- new entities begin updating on the next tick;
- pools never grow dynamically;
- required-entity exhaustion is a mission/tool validation failure, not a reason to silently replace a live entity.

### 6.4 Required combined-load acceptance profile

The current baseline combined-load stress case requires **nine simultaneously live aircraft out of the hard 16-aircraft pool**:

1. one human-player F-65A;
2. one AI wingman;
3. four hostile combat aircraft;
4. one rescue helicopter;
5. one civilian aircraft; and
6. one physical AIC aircraft.

There is **one human player**. The other eight aircraft are physical entities controlled by AI and/or mission systems according to their authored roles and approved physical class.

The baseline physics-class rule is:

- the player F-65A, wingman, and four hostile combat aircraft are `SIX_DOF`;
- the rescue helicopter and civilian aircraft are `KINEMATIC`;
- the physical AIC aircraft uses the **mission-authored immutable physics class required by its approved role**: a route-bound/protected AIC may be `KINEMATIC`, while an AIC required to maneuver defensively or participate as a combat actor is `SIX_DOF`.

**Baseline harness default:** For the required baseline combined-load acceptance harness, the physical AIC uses `KINEMATIC`, producing **six `SIX_DOF` and three `KINEMATIC` aircraft**. A `SIX_DOF` AIC is exercised only in a separately identified `SIX_DOF-AIC` harness variant whose higher-cost overlap is compiler-proved and admitted through the applicable performance gate.

Both `SIX_DOF` and `KINEMATIC` aircraft remain in the same aircraft pool, advance on the same **100 Hz authoritative timeline**, and remain subordinate to `FlightDynamicsEngine`. Physics class is selected at mission load and does not change because of distance, visibility, camera state, combat load, or renderer pressure. A mission that requires a `SIX_DOF` AIC must prove that more expensive overlap through the mission compiler and the applicable integrated harness; it may not assume the cheaper AIC class merely to make timing fit.

Therefore the aircraft stress case uses **9 of 16 slots**, leaving **7 slots of pool-capacity headroom**. This does not mean every mission should fill all 16 slots, and it does not change the mission compiler's responsibility to prove each authored overlap.

The integrated acceptance profile also exercises, concurrently where legal:

- sixteen guided missiles;
- twenty-four gun projectile groups;
- forty-eight live decoys;
- eight dynamic mission entities;
- eight active objectives;
- sixty-four presentation effects;
- required MEGA and RED sensor/track load;
- representative AI reflex/doctrine/mobility scheduling and held-intent state;
- damage, audio, HUD, renderer, input, DMA, resource and diagnostics work.

This profile is a required overlap case, not a claim that every hard pool maximum must coexist simultaneously.

---

## 7. Flight physics, FCS, aircraft systems, and carrier flight

### 7.1 Governing model

The Flight Physics and Simulation White Paper v3.3 is the detailed governing Phase-2 engineering model. Revision 1.6 adopts its durable architecture-level decisions.

### 7.2 Consequential 6DOF airframe

The F-65A uses a table-driven, deterministic six-degree-of-freedom rigid-body model at 100 Hz with:

- NED world coordinates and body-axis dynamics;
- shared deterministic atmosphere, gravity and wind;
- actual air-relative velocity, TAS, Mach, dynamic pressure, EAS and KIAS/CAS definitions;
- table-driven aerodynamic force/moment coefficients;
- static and dynamic stability derivatives;
- stall/separation state and deterministic hysteresis;
- two independently modeled engines with installation moments;
- sweep-dependent mass/inertia scheduling;
- actual left/right wing-sweep state;
- individual control surfaces, hydraulic authority and actuator rates;
- deterministic ground effect;
- terrain/runway/deck/contact interaction.

The airframe must remain physically flyable with control augmentation off inside the approved unaugmented envelope.

### 7.3 Flight-control state model

Revision 1.6 replaces the older paired control-law terminology with the following separated concepts:

```text
ControlContext = DECK / TFL / NORMAL_FLIGHT / COMBAT
FCSMode        = AUGMENTED / AUG_OFF
FCSStatus      = NORMAL / DEGRADED / DIRECT_ONLY
ADLCState      = OFF / CAPTURE / TRACK / DEGRADED
Autothrottle   = independent state
```

`FCSMode` records the commanded/pilot-selected mode. `FCSStatus` records what augmentation capability the aircraft can actually deliver. `DIRECT_ONLY` forces direct behavior without rewriting the pilot's switch state.

### 7.4 Command hierarchy

The high-level path is:

```text
InputCommandFrame
 -> ControlContext
 -> FCS mode + capability manager
 -> optional ADLC longitudinal/throttle overlay
 -> command generation
 -> non-augmenting Control Mixer / approved gearing
 -> hydraulic authority
 -> actuator dynamics
 -> actual ControlSurfaceState
 -> 6DOF aerodynamics
```

No control law bypasses physical control-surface authority, hydraulic state, actuator rate, damage, aerodynamic loading, or available energy.

### 7.5 AUGMENTED mode

AUGMENTED is the normal/default F-65 mode and has the character of a modern F/A-18-like augmented fighter without attempting to copy specific real-world control-law software.

At the concept level:

- longitudinal input commands scheduled normal acceleration with pitch-rate/AoA feedback where appropriate;
- lateral input commands scheduled roll rate;
- yaw damping and coordination operate when capability is available;
- automatic trim and approved G/AoA protection operate through the physical surface path;
- scheduling may depend on configuration, sweep, dynamic pressure, Mach, hydraulics and damage;
- there is no hidden altitude hold and no artificial creation of lift or energy.

### 7.6 AUG_OFF / direct mode

AUG_OFF is a real manual/direct flying mode, not a second rate-command law.

It retains:

- pilot trim;
- non-augmenting control mixing/gearing;
- hydraulics;
- actuator rates and stops;
- damage and asymmetry;
- natural aerodynamic static and dynamic stability.

It removes closed-loop G-command, roll-rate-command, AoA/G limiting and artificial FCS stability damping.

### 7.7 Bumpless transfer

Mode/capability changes may not create a discontinuous aircraft response solely because a switch or failure state changed. AUGMENTED to AUG_OFF uses a bounded temporary transfer bias separate from `PilotTrimState`; the bias decays to zero and never silently becomes pilot trim.

### 7.8 ADLC and autothrottle

ADLC is an approach-control overlay, not a peer fundamental flight law. Selecting AUG_OFF while ADLC is engaged disengages ADLC before direct authority becomes active. Loss of required augmentation capability causes ADLC to degrade or disengage according to the approved contract.

Autothrottle is a separate state machine.

### 7.9 Aircraft systems

The player-facing systems model includes at minimum:

- independent engine state;
- electrical generation/distribution;
- fuel quantity/flow and Joker/Bingo logic;
- hydraulic supply and control authority;
- landing gear, flaps, hook and related configuration;
- avionics/sensor capability states;
- damage-driven subsystem degradation;
- cold-start and operating procedures as defined by Gameplay v1.

Detailed subsystem dependencies and failure propagation belong in Gameplay v1 and the 65Aero Runtime v1.

---

## 8. Radar, sensors, tracks, tactical links, seekers, RWR, and countermeasures

### 8.1 Governing model

The human-reviewed SensorAndTrackEngine Phase-3 v1.0 engineering model is adopted for rewrite purposes and will be published in the active corpus as **F65 Radar, Sensors and Track Engineering White Paper v1.0**.

### 8.2 Ownership boundary

`SensorAndTrackEngine` owns observation and assessment. `WeaponAndDamageEngine` owns authoritative missile state and physical weapon evolution.

SensorAndTrackEngine owns:

- radar/IR observables;
- organic radar observations;
- semantic tactical-track processing;
- MEGA LINK / RED LINK fusion;
- RWR-emission assessment and threat-state inputs;
- chaff/flare competition against sensors and seekers;
- `SeekerAssessment` generation;
- `WeaponSupportUpdate` generation from valid local fire-control state.

WeaponAndDamageEngine owns:

- authoritative `WeaponGuidanceState`;
- missile target/lock/countermeasure state;
- support/autonomy transitions;
- missile 3DOF motion and propulsion;
- guidance integration;
- fuzes, detonation, damage, and weapon lifecycle.

SensorAndTrack may assess what a seeker can see; it does not mutate missile guidance state directly.

### 8.3 One-tick sensor/weapon causality

SensorAndTrack executes at stage 15. A `SeekerAssessment` or `WeaponSupportUpdate` generated on tick N may be consumed by WeaponAndDamage no earlier than stage 12 of tick N+1.

No same-tick sensor-to-guidance feedback is permitted.

### 8.4 SensorHandoffState

Cross-tick sensor/weapon/link records use fixed persistent `SensorHandoffState`, owned and byte-accounted by SensorAndTrackEngine. It contains at least:

- one pending `SeekerAssessment` mailbox per guided-missile slot (32);
- one pending `WeaponSupportUpdate` mailbox per guided-missile slot (32);
- a bounded tactical-link pending queue.

Exact widths, alignment, queue capacity and total bytes are generated/measured data, not free memory.

### 8.5 Tactical knowledge domains

The current product has exactly two capacity-isolated tactical-link knowledge domains:

- **MEGA / BLUE**
- **RED**

Each domain has up to 24 semantic tactical tracks. Neutral/friendly/hostile are identification states inside a domain, not additional track domains.

Association, fusion, track aging, capacity pressure and eviction are strictly intra-domain. The same physical truth contact may have one semantic representation in each opposing domain because those records represent different knowledge.

RIO priority tracks are a four-track subset of the MEGA/player domain only. RED transmit priority is a separate concept.

### 8.6 MEGA LINK and RED LINK

Tactical links carry bounded offboard tactical reports between eligible participants. They do not create perfect shared truth.

Key architecture rules:

- link reports obey at least one-tick causality;
- organic and offboard evidence can fuse into one semantic track within a domain;
- offboard-only information may cue/fuse but cannot create ownship weapon-quality state or valid local weapon support by itself;
- tactical link is not a substitute for Weapon Support Datalink;
- the ownship defensive jammer denies organic radar operation and MEGA LINK transmit/receive while active according to the accepted gameplay rewrite;
- denied in-flight reports are lost, not replayed as a backlog when the jammer is turned off.

### 8.7 Radar and RWR character

Radar behavior is deterministic and geometry/physics driven. Detailed Phase-3 data will define detection ranges, scan schedules, beamwidths, clutter/notch thresholds, association gates and track quality.

The architecture requires:

- radar truth/observations/tracks to remain distinct;
- terrain/clutter and Doppler/notch behavior to use authoritative geometry;
- beaming/weaving/chaff/jamming to work through actual geometry and susceptibility rather than magic bonuses;
- active radar seekers to be valid radar emitters that may produce an RWR indication when receiver geometry/sensitivity permits;
- passive IR seekers to remain electromagnetically silent.

### 8.8 IR model

The detailed sensor paper defines a simplified deterministic IR-signature model based on aggregate engine state and target aspect, including LOW/MIL/MAX behavior and a frontal weak/blind sector. Exact tables remain Phase-3 data.

There is **no dedicated IR missile-approach-warning system** in the current product. The own-heater seeker tone represents the player's own IR seeker only.

### 8.9 Countermeasure maneuver qualification

Chaff and flare may be released at any legal time, but effectiveness is qualified by the approved maneuver rule: the aircraft must achieve at least **+3 G positive normal load** within the defined qualification window. Negative G does not satisfy the requirement.

Exact windows, signatures, decay and scoring remain Phase-3 data.

### 8.10 Current radar-missile concept

Current radar missiles use supported midcourse guidance followed by autonomous active-seeker operation. They are not modeled as semi-active-homing weapons.

Weapon Support Datalink is a dedicated shooter-to-missile support path. MEGA LINK / RED LINK may improve tactical knowledge but cannot replace missile support.

---

## 9. Weapons, collision, and damage

### 9.1 Weapon authority

Weapon requests are accepted at stage 11 using legal prior/current state as defined by 65Aero. Existing weapons and countermeasures integrate at stage 12. Collision/fuze events resolve at stage 13 and damage is accumulated/applied at stage 14.

### 9.2 Missiles

Guided missiles use deterministic 3DOF physical motion and generated weapon data. The sensor engine evaluates seeker observability; the weapon engine owns guidance state and missile physics.

Current weapon families include:

- long-range radar missiles;
- medium-range radar missiles;
- passive-IR heaters;
- cannon.

Exact energy, seeker, loft, guidance, fuze and damage tables remain phase-authored data.

### 9.3 Cannon

Gunfire uses bounded projectile-group entities rather than one entity per round. Pool exhaustion rejects a shot without consuming ammunition.

### 9.4 Damage

Damage is deterministic, component/system aware, and may degrade engines, hydraulics, FCS capability, sensors, weapons and other aircraft systems. Presentation effects such as smoke, sparks and explosion flashes do not themselves become authoritative damage unless a future numbered design explicitly creates a physical effect volume.

---

## 10. Graphics and presentation architecture

### 10.1 Governing model

Revision 1.6 absorbs the durable architecture decision previously carried by F65-GAD-001 and adopts Graphics White Paper v2.1 as the detailed graphics engineering baseline.

The world renderer is **hybrid**, not a Mode-7-only world model and not a general dense 3D engine.

### 10.2 Layered world model

The intended layer ownership is:

| Layer | Primary presentation technique |
|---|---|
| Sky / atmosphere | Analytic fill, gradients, haze |
| Distant terrain / horizon | Ridge/silhouette strips, very-low-detail impostors/parallax |
| Ocean / broad flat terrain | Affine or scanline surface, DMA accelerated where useful |
| Gentle relief | Bounded height modulation or selective silhouette features |
| Carrier deck/island | Sparse projected geometry |
| Airfield | Affine/scanline base where suitable plus registered overlays/sparse structures |
| Ships / close structures | Sparse projected geometry |
| Aircraft | Point/glint -> billboard -> directional impostor -> low-poly geometry |
| Missiles/effects | Point, sprite, streak, billboard or sparse geometry as appropriate |
| Cockpit/HUD | Protected VIC-IV composition; exact RRB/other method remains measured |

Affine rendering is a useful primitive, not the world model.

### 10.3 Sparse polygon pipeline

The sparse path is bounded and deterministic:

```text
PresentationSnapshot
 -> camera-relative transform
 -> visibility/bounds
 -> LOD selection
 -> vertex transform
 -> near-plane clipping
 -> backface rejection
 -> projection
 -> screen clipping
 -> terrain-occlusion reject/clip where applicable
 -> deterministic depth bucket
 -> painter ordering
 -> bounded span generation
 -> CPU fill / DMA submission
 -> complete-buffer publication
```

There is no production requirement for a Z-buffer or arbitrary perspective-correct mesh texturing.

### 10.4 Incremental world construction

A world-frame construction job may span multiple display services. It uses remaining time only and yields at bounded work/DMA boundaries.

Only a completed world buffer may become visible. If a new frame is late, the last completed frame remains displayed while simulation, input, protected audio, HUD, warnings and other protected services continue.

World rendering may reduce cadence; it may not slow or reorder the 100 Hz simulation. Under the master performance bar in §4.6, ordinary cruise world presentation carries a **30 Hz TARGET**, approved combined-combat load carries a **25 Hz TARGET**, and sustained completed-world cadence below **20 Hz** is a failure condition. Maximum displayed-world age remains **R0-GATED / MEASURED**, not a fixed value in this document.

### 10.5 PresentationSnapshot ownership

The renderer never integrates its own aircraft dynamics. It consumes complete immutable `PresentationSnapshot` data.

Each world-buffer attempt binds one source snapshot, one view, one tier, one destination store and one resumable work cursor.

### 10.6 World-registration coherence

A completed world buffer is paired atomically with a bounded `WorldRegistrationRecord` derived from the same snapshot. The record carries the camera/projection/horizon state and bounded spatial anchors required to keep world-registered HUD cues aligned while that world buffer remains on screen.

World-registered cues include, as applicable:

- pitch ladder/attitude references;
- flight-path marker;
- target designators;
- steering/weapon cues.

Non-spatial status such as fuel, warnings, counts and mode text may use the newest permitted snapshot.

Atomic view changes keep world buffer, registration record, view identity and composition profile coherent.

### 10.7 Terrain occlusion and registration

Graphics may use a bounded presentation-only `TerrainOcclusionEnvelope` or equivalent approved mechanism so aircraft/missiles/objects do not visibly draw through foreground ridges without requiring a Z-buffer.

Authoritative terrain collision, height, LOS and sensor queries never derive from the visual LOD. Presentation terrain and authoritative terrain-query data share canonical transforms and authored registration references.

Carrier visual geometry and carrier contact geometry similarly share canonical deck transforms and key landmarks.

### 10.8 Residency and LOD fallback

Every streamable optional visual asset class has a resident fallback. A valid frame never blocks waiting for optional high-detail Attic content.

Examples:

- detailed terrain -> coarse terrain;
- low-poly aircraft -> directional impostor -> billboard -> point/glint;
- detailed structure -> coarse hull/silhouette.

LOD transitions use deterministic hysteresis to avoid flicker.

### 10.9 Protected presentation

Protected every display service:

- HUD compositor;
- cockpit compositor;
- critical warnings;
- display publication/housekeeping.

Radar symbology, systems pages and lower-priority instruments may refresh on approved lower cadences while remaining visually present.

Exact VIC-IV composition mode, RRB use, display resolution, LOD distances, span/polygon ceilings, world-age limit and shedding tiers remain measured values to close through R0-D/E/F and the measured-limits process.

---

## 11. Audio, sound effects, warnings, speech, and music

### 11.1 Audio is protected presentation

Audio never changes authoritative simulation state. It consumes semantic events and bounded continuous parameters extracted from approved state.

Missing samples, voice stealing, preemption, music state, panning or dropped effects cannot affect flight, sensors, weapons, AI, mission state, RNG or checksums.

### 11.2 MEGA65 audio resource model

The audio baseline uses:

- **four SID synthesizers / twelve SID oscillator voices**;
- **four pooled hardware PCM/audio-DMA channels**.

SID is preferred for continuous, procedural, repeating, parameter-driven, warning and musical synthesis. PCM is a scarce enhancement resource for speech and characteristic transients whose spectral content is inefficient to synthesize.

### 11.3 Preferred SID allocation

Normal logical allocation:

- SID 1 - music left / primary musical synthesis;
- SID 2 - music right / complementary music;
- SID 3 - continuous aircraft/environment;
- SID 4 - warnings, RWR, procedural cockpit and transient effects.

This is a logical preference, not an unbreakable hardware partition. Priority arbitration may borrow or silence lower-priority voices.

### 11.4 Procedural aircraft audio

Continuous aircraft sound responds to actual aircraft state, including:

- individual engine RPM/N1 or equivalent operating state;
- military/afterburner state;
- engine failure/flameout and twin-engine asymmetry;
- airspeed;
- AoA/buffet where available;
- cockpit/external view mix.

Throttle position alone is not the engine-audio state.

### 11.5 PCM scheduler

The four PCM channels form one pooled scheduler. Most assets are mono unless a stereo event justifies consuming two channels.

PCM is preferred for selected:

- catapult/arrestment/touchdown transients;
- gear/hook mechanisms;
- weapon-release and cannon layers;
- impacts/crashes;
- short RIO/AIC/ATC phrases.

Every gameplay-essential audio event has an approved SID, text or protected visual fallback.

### 11.6 Audio priority classes

The protected priority hierarchy is:

- **P0** - missile warning, fire, critical engine/FCS state, stall/ground-impact warning;
- **P1** - other immediate aircraft-safety cautions;
- **P2** - critical RIO defensive, Bingo/fuel and recovery callouts;
- **P3** - ordinary RIO, ATC, AIC and mission speech;
- **P4** - ordinary weapon transients, impacts, ambience and decorative effects.

P0 may steal SID voices, stop/duck music, terminate lower-priority PCM and interrupt speech. Warning latency is not sacrificed to preserve music or ambience.

### 11.7 Music

Music is part of the product identity. The preferred six-voice music allocation degrades toward a protected three-part core:

1. percussion;
2. bass/rhythm;
3. lead.

Optional harmony/doubling/pad/echo voices may be stolen under load. Music recovery occurs at musically valid boundaries without stuck notes or corrupt synth state.

### 11.8 Sensor and seeker audio

RWR audio must distinguish at minimum search/surveillance, track/fire-control attention, launch/support warning, and valid active-seeker warning.

The heater seeker tone is the player's own passive IR seeker cue. It is not an incoming IR missile warning, and the current aircraft has no IR MAWS.

### 11.9 Audio degradation

Stable degradation removes presentation value before safety information:

1. decorative ambience;
2. ordinary weapon/impact PCM;
3. optional music voices;
4. queued/abbreviated ordinary speech;
5. PCM replaced by SID/text fallback;
6. music duck/suspend if required;
7. preserve P1;
8. preserve P0.

Audio hardware register/DMA access remains behind the protected platform/audio layer.

---

## 12. Input and player-control architecture

### 12.1 Semantic input

Raw hardware never writes aircraft state directly. Devices feed `InputEngine`, which creates semantic, tick-tagged `InputCommandFrame` actions.

This permits joystick, keyboard and future supported layouts to share the same simulation semantics.

### 12.2 Context versus FCS

Deck/TFL/Normal Flight/Combat contexts define bindings, HOTAS behavior and presentation priorities. They are independent from `FCSMode` and `FCSStatus`.

### 12.3 Accessibility

The game supports a complete keyboard-only flight layout when no joystick is present, while joystick plus keyboard remains the intended primary experience.

Automation such as the AI RIO, AUGMENTED FCS, autothrottle and ADLC reduces workload without making the simulation consequence-free or bypassing actual physical limits.

---

## 13. AI behavior, RIO, wingman, AIC, and tactical decision architecture

### 13.1 Governing model and scope

The **F65 AI Behavior and Decision Architecture White Paper v1.0** is the fifth detailed subsystem engineering white paper and the human-reviewed baseline for AI architecture.

The player aircraft remains under direct human flight control. The AI RIO is a workload-management and tactical-assistance system, not a hidden player autopilot. It may request sensor, weapon, defensive, navigation-information, and approved system actions where Gameplay authorizes them, but it does not silently fly the player's aircraft through AI `GuidanceIntent`.

All other aircraft, ships, SAM sites, applicable ground vehicles, and surface combatants use AI decision logic according to their authored role. Guided missiles after launch are not tactical AI entities; their lifecycle remains owned by `WeaponAndDamageEngine`.

### 13.2 Bounded legal knowledge - no global truth

AI never reads global truth merely because the engine contains it.

An AI entity may consume only declared information legally available to its side/knowledge domain and its own physical/system state, including as appropriate:

- semantic tactical tracks from its legal MEGA/BLUE or RED domain;
- track quality and legally available local fire-control/support state;
- limited MEGA LINK / RED LINK reports;
- RWR and `MissileThreatState`;
- legitimate `VisualContactView` information;
- bounded own-weapon status and weapon-employment projections;
- mission-authored route/goal/ROE information;
- facility/recovery/formation coordination state; and
- its own aircraft/vehicle/system state.

AI cannot infer visual contact from entity existence, cannot inspect hidden hostile fuel/configuration/inventory, and cannot defend against an IR missile using secret missile truth. This applies symmetrically to Blue and Red AI. Team coordination does not become a hidden sensor network.

### 13.3 Hierarchical doctrinal controller

F-65 AI is a bounded hierarchical doctrinal controller, not a generic unrestricted utility AI. Local utility scoring is permitted only among doctrinally legal choices.

The durable hierarchy is:

```text
HARD SAFETY / REFLEX
    ->
MISSION
    ->
FORMATION / TEAM
    ->
OPERATIONAL / MOBILITY
    ->
TACTICAL PHASE, when applicable
    ->
MANEUVER / GUIDANCE
    ->
CONTROL / INTENT OUTPUT
```

Aviate-first or drive-first is absolute. Tactical defense may preempt mission, formation, operational, tactical, and maneuver behavior, but it may not preempt a HARD SAFETY recovery required to avoid immediate loss of control/collision.

Mission supplies the authored objective, ROE, route, station, recovery destination, and abort criteria. AI does not invent strategic objectives.

### 13.4 Deterministic interrupt precedence

Consequence-based interrupts are ordered broadly as:

1. **FLIGHT / SURFACE SAFETY** - terrain/collision, departure/loss of control, or other immediate physical safety hazard;
2. **TERMINAL SURVIVAL** - a credible legally cued missile threat requiring immediate defense;
3. **TACTICAL** - fire-control attention, deteriorating combat geometry, wingman emergency, or other significant tactical event;
4. **MISSION LIMIT** - Bingo/fuel, survivable damage, mission abort, recovery requirement.

A condition may move upward when its consequence changes; for example survivable damage becomes Level 1 when it causes imminent loss of aircraft control.

### 13.5 Stage-16 reflex and doctrine passes

All AI decision production remains inside stage 16 or at a slower deterministic schedule driven from stage 16. There is no second authoritative AI clock.

- **Reflex evaluation** handles immediate safety, collision avoidance, departure recovery, legally cued missile threats, immediate defensive transitions, and local surface avoidance.
- **Doctrine evaluation** may run at a lower scheduled cadence for target selection, sorting, commit/recommit, formation, BVR reasoning, IADS planning, route sequencing, operational-state changes, and recovery planning.

Exact per-service cadences remain Phase-4/65Aero tuning unless already frozen elsewhere. A non-due service retains its approved state/held intent; the physical entity continues to integrate at 100 Hz.

### 13.6 AIIntentFrame and held-intent boundary

`AIEngine` produces a bounded stage-16 `AIIntentFrame` for effects no earlier than the following tick. Conceptually it separates intent classes such as:

```text
AIIntentFrame
    GuidanceIntent
    SystemIntent
    WeaponIntent
    SensorIntent
    coordination / mission intent as approved
```

- `GuidanceIntent` expresses desired movement/navigation/formation/recovery behavior and is consumed by the appropriate physical/control owner.
- `SystemIntent` requests systems actions such as engine start, gear, flaps, hook, brakes, ADLC or other approved configuration through the owning systems module.
- `WeaponIntent` requests tactical selection/release/support behavior through the weapon interface; `WeaponAndDamageEngine` retains launch legality, guidance state and physical lifecycle.
- `SensorIntent` requests declared sensor modes/emission/scan behavior through SensorAndTrack/system interfaces; AI never manipulates sensor internals.

Guidance is a **held intent**. The owning high-rate controller continues closing against the latest legal intent on subsequent 100 Hz ticks until completion, replacement, cancellation, invalidation, mode transition, or HARD SAFETY override. Exact layout, masks, lifetime and replacement rules belong in 65Aero Runtime/generated schemas.

For SIX_DOF aircraft, AI guidance flows through the normal control/system path:

```text
GuidanceIntent
    -> ControlAndSystemsEngine / FCS
    -> control mixer
    -> hydraulics / actuators
    -> actual surfaces
    -> FlightDynamicsEngine
```

An approved KINEMATIC aircraft remains bounded and subordinate to `FlightDynamicsEngine`; it is not a second uncontrolled motion authority. Ships and ground vehicles use their own bounded surface-motion controllers rather than an aircraft FCS.

### 13.7 Doctrine composition, skill, and faction behavior

Effective doctrine is composed from bounded authored data rather than a combinatorial runtime planner:

```text
unit base
+ faction modifiers
+ proficiency modifiers
+ mission posture overrides
+ optional novice-hostile modifiers
```

Faction may alter aggression, emission-control preference, support obligations, conservatism, and coordination doctrine. Proficiency may alter reaction latency, timing, precision, scan discipline, prediction tolerance, shot discipline, support patience, abort willingness, and formation coordination.

Skill never changes physics, weapon kinematics, seeker/radar performance, damage, or hidden-information access. Authorized behavioral variability uses only the entity-local AI RNG stream.

### 13.8 Realistic and Novice AI modes

Revision 1.6 adopts the AI white paper's two-mode player-facing difficulty concept:

- **Realistic** - baseline doctrine thresholds, employment timing, defensive response, aggression, support discipline, and maneuver logic. **Realistic is the default architecture baseline.**
- **Novice** - the same controller, state graphs, and maneuver primitives, but a more forgiving hostile tactical doctrine: later hostile employment, later defensive reaction, reduced commitment, and earlier skate/abort preference.

Novice modifiers apply to **hostile tactical AI only** unless Gameplay v1 deliberately expands the scope. Friendly AI, including the player wingman, AIC, and other Blue forces, remains on normal doctrine by default.

Gameplay v1 owns the final settings/menu wording, persistence UX, and any additional player-facing explanation. The underlying controller architecture is shared between modes.

### 13.9 Mobility and procedural behavior

AI navigation is authored/precompiled and bounded. No general-purpose runtime pathfinding, A*, recursive planning, unrestricted behavior-tree growth, neural model, GOAP, or continuous trajectory optimization is part of the authoritative target AI.

At the master level:

- aircraft use authored `RoutePlan` concepts, precompiled taxi/deck routes, bounded parking-to-parking procedural states, physical takeoff/landing/carrier launch/recovery, and deterministic route interruption/resumption;
- ships use authored sea routes/patterns with bounded tactical deviations and return-to-route behavior;
- ground vehicles/mobile SAMs use precompiled routes/relocation options rather than runtime graph search;
- shared runways/catapults/recovery slots use bounded deterministic facility-clearance state;
- tactical deviations never authorize arbitrary route recomputation.

Physical consequences remain owned by the applicable physics/contact/system model.

### 13.10 Tactical behavior scope

The detailed AI white paper governs BVR timeline reasoning, defensive behavior, relational BFM, IADS, ship doctrine, formation/team behavior, and authored tactical state graphs.

At the Main Concept level:

- BVR AI reasons about legal track geometry, estimated weapon effectiveness, support timelines, fuel/team state, crank/press/drag, abort and recommit without integrating missile physics itself;
- defensive AI uses real threat/sensor geometry and actual countermeasure/jammer trade-offs rather than magical success bonuses;
- WVR/BFM uses relational geometry, bounded maneuver primitives, energy/performance-class estimates, and legal visual knowledge;
- IADS uses role-based emission control, legal shared knowledge, ambush/support behavior and precompiled mobile-SAM routes;
- surface combatants allocate sensors/weapons under authored doctrine rather than firing every compatible weapon at the first track.

Detailed state tables, scoring weights, proficiency thresholds, doctrine constants, maneuver primitives, route records, and Phase-4 tuning remain in the AI white paper, Gameplay v1, 65Aero Runtime v1, and generated data as appropriate.

### 13.11 RIO, wingman, and AIC

The AI RIO manages or assists with radar/tactical-picture interpretation, priority handling, weapon recommendation/support awareness, countermeasures/jammer use where Gameplay authorizes, fuel/navigation/recovery information, startup/procedural guidance, and defensive coaching. It reduces workload but does not secretly fly the player aircraft.

RIO priority tracks remain limited to four MEGA-domain tracks. They are not the same as RED doctrine/link transmit priority.

Wingman behavior uses authored formation/team doctrine and explicit player intent such as Engage, Cover, Rejoin, and Return while independently selecting legal path, target, weapon, and defensive action.

AIC is a physical aircraft when instantiated, consumes an aircraft-pool slot, and operates from its own legal sensor/fused-track picture rather than global truth.

### 13.12 AI memory, queues, and deterministic state

AI introduces no dynamic queues, heap-backed planning graphs, unbounded candidate lists, hidden second simulation clock, or presentation-dependent decisions.

Persistent AI state may include bounded hierarchy/operational/tactical/interrupt state, route cursors, held intents, target references, team roles, own-weapon summaries, facility coordination, and limited candidate sets. The exact records and capacities are generated/65Aero Runtime work.

`AIIntentFrame` and any AI command/event handoff use fixed-capacity, tick-tagged, deterministic storage owned through the existing CoreRuntime command/intent architecture. Authoritative AI state that affects future decisions is included in replay/checksum serialization according to the generated schema.

AI diagnostics are read-only and should expose enough state to explain why an entity acted without changing the simulation.

---

## 14. Missions, campaign, saves, and authoring

### 14.1 Declarative mission model

Missions are authored as data and compiled into bounded runtime packages. The target does not parse an unrestricted general scripting language during a sortie.

The mission compiler proves pool/concurrency bounds and rejects authored missions whose legal execution can exceed required non-droppable capacities.

Mission data also provides the outer envelope for AI behavior: objectives, ROE, mission posture, authored routes, recovery/facility references, formation/team assignments, doctrine/profile handles, and legal relocation/continuation options. This mission authority does not expose unrestricted global truth to AI and does not permit runtime general-purpose path planning.

### 14.2 Product flow

The product flow includes:

- Continue;
- Campaign;
- Free Flight;
- Settings;
- three user-managed campaign save slots;
- no normal mid-sortie save/restore;
- validated Free Flight presets rather than a general-purpose player mission editor.

### 14.3 Technical Combat Slice

The Technical Combat Slice is a non-narrative integrated combat proof, not the same artifact as Midnight Spear and not automatically the release MVP.

### 14.4 Midnight Spear and campaign

Midnight Spear begins only from an approved mission manifest. Campaign content after currently authored operations remains a human-authored product requirement, not an AI completion task.

### 14.5 Save integrity

Campaign saves occur outside live sortie simulation. Save transactions use a bounded, recoverable scheme defined by Gameplay v1 and 65Aero Runtime v1. Storage/media mechanics that require platform-specific restoration are closed as implementation work at the gate where they are actually consumed, not by reopening historical R0-C.

---

## 15. Replay, diagnostics, fault handling, and observability

### 15.1 Canonical replay/checksum

Authoritative replay and checksums cover deterministic simulation state and intentionally exclude presentation-only differences such as world-render cadence, dropped particles, SID voice choice, music voice stealing or PCM channel selection.

### 15.2 Fault contract

Faults and overflows are deterministic and observable. A subsystem cannot hide a failure by silently allocating more memory, skipping required work, mutating another owner, or changing tick order.

### 15.3 Evidence

Every major gate records exact build identity, source commit, toolchain identity, configuration, maps/symbols/listings where applicable, memory/code/stack/cycle/DMA measurements, tests, Xemu results, physical-hardware results where required, and human acceptance.

### 15.4 Repository relationship

The active design corpus is deliberately small, but Git/GitHub contains many legitimate implementation/evidence artifacts: AGENTS rules, plans, generated interfaces, memory ledgers, R0 handoffs, test guides, evidence maps, build locks and source. Those remain part of engineering configuration control but are not extra design documents.

---

## 16. AI-assisted development policy

### 16.1 Repository-driven engineering

AI coding agents work from the checked-in specification identity, module scope, generated interfaces, task admission, tests and evidence requirements.

### 16.2 Allowed autonomous work

Within an approved task and interface, an agent may perform:

- local C implementation;
- approved platform/assembly wrappers;
- generators and schemas;
- host reference models and golden vectors;
- validators and deterministic fixtures;
- instrumentation and evidence capture;
- build/toolchain work;
- behavior-preserving refactoring;
- measurement-driven optimization;
- documentation updates required by the same change.

### 16.3 Stop/escalate conditions

An agent must stop the affected work rather than invent semantics when a task requires:

- a change to this master architecture;
- new player-visible gameplay;
- a public ABI or state-ownership change not already approved;
- a memory-map, pool or tick-order change;
- choosing a TBD/TARGET/R0-GATED production value without the required evidence/owner;
- relying on undocumented MEGA65 behavior;
- bypassing MemoryAccessABI or protected platform ownership;
- inventing campaign/missions, control feel, art/audio content, or acceptance waivers.

Independent reversible work may continue.

### 16.4 Evidence principle

Code is implementation evidence, not specification authority. A passing compiler build does not prove hardware behavior. Xemu does not replace physical MEGA65 evidence where the named gate requires hardware confirmation.

---

## 17. Phase 0 / R0 status and current development baseline

### 17.1 R0 purpose

R0 exists to prove the platform, toolchain, memory, display, input, audio, storage, resource, timing and combined-load assumptions that the production 65Aero engine depends on.

### 17.2 R0-A - COMPLETE

R0-A established the compiler/toolchain and MemoryAccessABI platform identity, minimal compiled-C/assembly boundary, mapping/base-page discipline, boot/link path, symbols/maps/profiling and required platform proof infrastructure.

Revision 1.6 does not reopen R0-A.

### 17.3 R0-B - COMPLETE

R0-B established the bounded graphics/display/cockpit/palette/swap/input-latency and representative audio measurement evidence for the scope tested at that milestone.

Later Graphics v2.1 or Audio v1.0 additions do not retroactively rewrite the R0-B acceptance scope.

### 17.4 R0-C - COMPLETE

For the Revision 1.6 development baseline, R0-C is closed as the production-shaped package/resource/residency/D81/storage-save proof milestone.

Revision 1.6 therefore begins downstream work at R0-D. Outstanding storage-service details that were not required by the final R0-C proof configuration are carried forward to 65Aero `StorageService` implementation/acceptance and do not reopen Charlie.

### 17.5 R0-D - CURRENT

R0-D is the protected-workload/calibration milestone built around the historical **530,000-clock protected non-render workload** and current instrumentation.

R0-D adds or completes measurement hooks needed by the accepted subsystem white papers without turning Delta into a second renderer, audio engine, flight model, or sensor implementation phase.

Representative additions include:

- world-generation/source-snapshot/world-age counters;
- renderer pool, occlusion, registration-anchor and LOD-transition high-water counters;
- protected compositor and graphics DMA accounting;
- audio service, voice/channel, preemption, staging and P0/P1 latency counters;
- snapshot/memory/DMA/input/storage timing needed by Echo;
- AI owner measurement hooks for resident code, runtime state, held-intent storage, route/doctrine hot data, and worst-case reflex/doctrine/mobility execution;
- bounded stage-16 scheduler/AIIntentFrame fixtures needed to prove next-tick causality without implementing Phase-4 production doctrine;
- reserve and protected-service accounting.

Actual Phase-2 flight coefficient implementation and Phase-3 radar tables do not move backward into R0-D.

### 17.6 R0-E - combined Xemu integration

R0-E is the primary combined Xemu integration gate for the final pre-Phase-1 proof configuration.

It combines, concurrently:

- independent simulation/display/audio/input clocks;
- snapshot publication/consumption;
- memory/resource staging;
- renderer and cockpit/HUD presentation;
- Graphics v2.1 additions such as occlusion, world registration, LOD hysteresis, atomic view/generation coherence and G-desaturation presentation;
- Audio v1.0 scheduler contention, warning priority, music/SFX/speech behavior and resource staging;
- input edges;
- DMA/IRQ contention;
- storage/resource behavior;
- deterministic faults and shedding;
- bounded AI interface/scheduler fixtures, held-intent persistence, legal-knowledge isolation and worst-case scheduled AI-owner measurement without promoting Phase-4 tuning;
- the required combined entity/presentation load.

R0-E still uses bounded proxies/fixtures for later production physics, sensor, weapon and tactical content where those phases have not begun.

### 17.7 R0-F - physical MEGA65 confirmation

R0-F confirms the identified R0-E configuration on physical MEGA65 hardware and performs the required phase/timing sweeps.

A materially changed configuration after hardware failure returns to the appropriate upstream validation and produces a new identified E->F evidence chain.

### 17.8 Measured-limits closure

After R0-F, the measured-limits process freezes only the values actually supported by accepted evidence, including as applicable:

- protected-service ceilings;
- renderer/display tier and world-age limits;
- DMA latency/batch limits;
- RRB/VIC-IV composition selection;
- audio service/channel/latency ceilings;
- code/data/stack/reserve limits;
- resource/scene/presentation pool limits where still measured.

The measured limits are repository configuration/evidence artifacts and generated registries, not a new competing design-document layer.

---

## 18. Phase 1 - 65Aero integrated engine harness

### 18.1 Purpose

Phase 1 constructs and proves the production-shaped 65Aero backend architecture before the detailed flight, radar/weapon and tactical models are filled in.

Phase 1 is the bridge between the completed platform proof program and production simulation systems.

### 18.2 Phase-1 engine scope

Phase 1 builds the integrated production infrastructure for:

- CoreRuntime scheduler/determinism;
- PlatformABI and MemoryAccessABI;
- fixed entity pools/lifecycle;
- commands and deterministic events;
- memory/resource ledgers and ResourceManager;
- StorageService/package loader;
- InputEngine and input edge bridge;
- PresentationExtractor and immutable snapshot handoff;
- GraphicsEngine, cockpit, HUD, MFD composition and world-generation pipeline using R0-selected/measured limits;
- AudioEngine using the v1.0 audio architecture and R0-selected limits;
- world-query/environment substrate;
- mission-record loader and capacity metadata;
- AI scheduler hooks, bounded AI state ownership, legal-knowledge/view interfaces and `AIIntentFrame`/held-intent infrastructure sufficient for later Phase-4 implementation;
- fault catalog;
- replay/checksum;
- generated interface/numeric registries;
- diagnostics and synthetic integrated harness.

### 18.3 Phase-1 proxy interfaces for later systems

Phase 1 also freezes production-compatible interface shapes and bounded proxy/fixture behavior for later phases so those systems plug into 65Aero without redesign.

From Flight Physics v3.3 this includes:

- FCSMode/FCSStatus;
- control-surface and actuator pipeline records;
- environment/atmosphere interfaces;
- table-residency contracts;
- physics oracle/golden-vector interfaces;
- appropriate aircraft/system state ownership.

From Radar/Sensors v1.0 this includes, at minimum where needed for generated public schema readiness:

- two-domain track ownership semantics;
- `SensorHandoffState` ownership;
- read-only seeker/countermeasure views;
- stage-15 handoff contracts;
- generated record identities required before Phase 3.

From AI Behavior/Decision v1.0 this includes, at minimum:

- bounded `AIIntentFrame` ownership and next-tick application semantics;
- conceptual `GuidanceIntent`, `SystemIntent`, `WeaponIntent`, and `SensorIntent` separation;
- held-intent lifetime/cancel/replace/invalidate hooks;
- bounded authoritative AI state ownership and checksum/replay participation;
- doctrine/profile/task/state identifiers and mission-handle references;
- legal knowledge/view boundaries between SensorAndTrack, WeaponAndDamage, MissionEngine, and AIEngine;
- stage-16 scheduler hooks for reflex and lower-cadence doctrine services;
- route/facility/recovery interface shapes needed so Phase 4 can plug in without redesign;
- measurement hooks for resident code/state/hot data and legal worst-case AI cycles.

Phase 1 does **not** author production aerodynamic coefficient tables, radar detection schedules, seeker thresholds, final AI doctrine weights/cadences, campaign narrative, or Phase-4 tactical tuning.

### 18.4 Phase-1 pass criteria

A partial pass is failure. The concurrent harness must prove:

- canonical mapping and ABI restoration;
- deterministic checksum/replay behavior;
- entity lifecycle correctness;
- generated interface consistency;
- memory/code/stack ceilings and required reserve;
- combined p95/worst timing inside accepted limits;
- snapshot correctness and presentation isolation;
- graphics/audio/input latency and shedding behavior;
- resource/storage correctness;
- PAL/NTSC equivalence for authoritative results;
- no subsystem dependence on presentation cadence or visual LOD.

Phase 2 does not begin until the integrated harness passes.

---

## 19. Phase 2 - flight, controls, carrier mechanics, and aircraft systems

Phase 2 implements the actual F-65 aircraft model using the Flight Physics v3.3 white paper as the governing detailed engineering source.

Phase 2 includes:

- atmosphere/wind/gravity tables;
- F-65 6DOF aerodynamics;
- static/dynamic stability derivatives;
- FCS AUGMENTED/AUG_OFF behavior;
- FCS capability degradation;
- control mixer/gearing;
- hydraulic/actuator behavior;
- engine thrust/fuel/spool/install moments;
- variable wing sweep and mass/inertia schedules;
- stalls/departure and ground effect;
- aircraft electrical/fuel/hydraulic/system dependency behavior;
- landing gear/flaps/hook;
- ground/runway/deck/arrestment/carrier flight mechanics;
- ADLC and autothrottle;
- host high-precision oracle, bit-exact reference, golden vectors and qualified handling acceptance.

The approved `F65_UNAUGMENTED_FLIGHT_ENVELOPE` must demonstrate that a healthy aircraft remains conventionally flyable with augmentation off.

---

## 20. Phase 3 - radar, weapons, countermeasures, and damage

Phase 3 implements the detailed combat-sensor and weapon model on the already-proven 65Aero architecture.

It includes:

- organic radar and emitter instances;
- radar truth/observations;
- two isolated semantic track domains;
- MEGA LINK / RED LINK;
- IFF/identification evidence;
- RWR and MissileThreatState;
- deterministic IR signature;
- passive IR seeker assessment;
- active radar seeker assessment;
- Weapon Support Datalink;
- chaff/flare competition and +3 G qualification;
- radar notch/clutter/terrain/jamming behavior;
- missile/gun physical models;
- collision/fuze/damage integration;
- generated SensorHandoffState and Phase-3 schemas;
- Phase-3 numeric tables, schedules, thresholds and acceptance vectors.

The SensorAndTrack white paper's ownership/causality model is authoritative at subsystem detail; WeaponAndDamage remains authoritative for missile physical/guidance state.

---

## 21. Phase 4 - AI/tactical layer, Technical Combat Slice, and Midnight Spear

Phase 4 implements and tunes the production tactical layer using the AI Behavior and Decision Architecture White Paper v1.0 on top of accepted Phase-2/3 aircraft, sensor, weapon, countermeasure, and damage systems.

Phase 4 includes:

- full hierarchical doctrinal controller implementation;
- deterministic HARD SAFETY/reflex and doctrine scheduling;
- airborne AI operational/tactical/BVR/WVR/defensive behavior;
- wingman formations, team roles and player intent handling;
- RIO tactical/workload behavior within the player-control boundary;
- physical AIC behavior where authored;
- IADS, SAM/mobile-SAM and surface-combatant doctrine;
- authored route/procedural aircraft, ship and ground-vehicle behavior;
- Realistic/Novice hostile-AI doctrine modifiers using the same controller architecture;
- proficiency/faction/mission-posture doctrine tables without cheating;
- generated Phase-4 AI schemas, route/doctrine data and diagnostics;
- mission graph/objectives/tutorial mechanics;
- debrief/scoring behavior;
- the non-narrative **Technical Combat Slice**;
- **Midnight Spear** only after its separately approved manifest.

Phase 4 tunes exact AI service cadences, scoring weights, thresholds, state tables, tactical alternatives and doctrine data. These values are not back-authored into Phase 1 merely because Phase 1 exposes their interfaces.

The Technical Combat Slice is the first integrated combat proof, not a substitute for the full campaign or an excuse to invent missing mission content.

---

## 22. Phase 5 - campaign, compatibility, optimization, and release

Phase 5 completes:

- operations 3-10 and all remaining authored campaign content;
- ending predicates and campaign-state transitions;
- final mission packaging and multi-D81 flow;
- save/compatibility behavior;
- final art/audio/content integration;
- hardware compatibility matrix closure;
- measured optimization;
- accessibility and usability closure;
- final release packaging and acceptance.

Optimization remains evidence-driven and may not cross architecture boundaries, remove deterministic safeguards, consume protected reserve, or alter gameplay merely to improve a benchmark.

---

## 23. Acceptance philosophy

### 23.1 Technical and human acceptance are both required

F-65 is both a deterministic software system and a flight/combat game. Technical proof alone cannot establish flight feel, visual readability, audio quality, warning recognition or mission quality.

Subsystem acceptance therefore combines:

- deterministic host tests;
- bit-exact target/reference tests where applicable;
- Xemu integration;
- physical MEGA65 evidence where required;
- qualified human review for handling, presentation, audio and gameplay.

### 23.2 Subsystem-specific human review

At minimum:

- flight review evaluates AUGMENTED handling, AUG_OFF flyability, carrier approach/recovery, stall/departure and damage behavior;
- graphics review evaluates horizon stability, cockpit readability, combat aspect cues, occlusion, LOD behavior and world/HUD registration;
- audio review evaluates engine/speed cues, warning recognition, RWR differentiation, speech intelligibility, music identity and fatigue;
- radar/combat review evaluates tactical readability, track behavior, countermeasure logic, RWR cues and missile-support behavior;
- AI/tactical review evaluates safety precedence, legal-knowledge behavior, formation/team coordination, BVR/WVR/defensive decisions, surface/IADS doctrine, procedural mobility, Realistic/Novice differentiation and absence of cheating;
- gameplay review evaluates controls, workload, mission pacing, accessibility and campaign quality.

---

## 24. Explicit current non-goals and future expansion

The following are not silently added to the current production scope:

- general-purpose dynamic simulation heap;
- secondary visibility-dependent physical integration clocks;
- any second physical integrator for off-screen, distant, traffic, or AI-controlled aircraft; `KINEMATIC` is a cheaper model on the same 100 Hz authoritative clock, not another timeline;
- a requirement that the outside world render at display/raster refresh rate or at 50/60 Hz; world presentation is independently scheduled under the §4.6 cadence floor/targets;
- dense general-purpose 3D terrain/scene rendering;
- Z-buffered arbitrary-mesh renderer;
- destructible static scenery as a blanket capability;
- general in-sortie code overlays;
- neural/GOAP/unbounded planner architectures or general runtime pathfinding for authoritative AI;
- continuous tactical disk streaming as a requirement;
- player-facing mission editor;
- IR missile-approach-warning system;
- automatic conversion of every white-paper idea into a production feature;
- native high-resolution graphics outside a separately approved future expansion;
- any new aircraft, weapon family, campaign branch or mission not added by an approved product revision.

Future expansion requires a numbered Main Concept revision when it changes product or architecture.

---

## 25. Revision 1.6 configuration-control disposition

### 25.1 Changes intentionally incorporated from the Flight Physics white paper

Revision 1.6 adopts:

- actual 100 Hz table-driven 6DOF/atmosphere engineering model;
- independent engine force/moment model;
- natural static/dynamic stability;
- separate FCSMode/FCSStatus;
- AUGMENTED/AUG_OFF as the controlling flight-control mode terminology;
- non-augmenting control mixer retained in AUG_OFF;
- ADLC as an overlay;
- bumpless transfer with temporary transfer bias separate from pilot trim;
- variable-sweep/mass/inertia scheduling;
- ground effect and Phase-2 oracle/validation model.

### 25.2 Changes intentionally incorporated from the Graphics white paper and GAD-001

Revision 1.6 adopts:

- hybrid affine/scanline + sparse-polygon + impostor architecture;
- affine as a primitive, not the world model;
- complete-buffer-only publication;
- incremental/resumable world construction;
- protected presentation deadlines;
- TerrainOcclusionEnvelope concept;
- atomic WorldRegistrationRecord/display generation;
- terrain/carrier visual/query registration;
- deterministic LOD hysteresis and resident fallback;
- R0-D/E/F downstream integration of the v2.1 additions.

`F65-GAD-001` is historical provenance under Revision 1.6 because its durable decisions are now in the master architecture.

### 25.3 Changes intentionally incorporated from the Audio white paper

Revision 1.6 adopts:

- four SID / twelve-voice procedural/music foundation;
- pooled four-channel PCM scheduler;
- SID-first/PCM-selective resource strategy;
- protected P0/P1 warning priority;
- music degradation to a three-part core;
- speech interruption/fallback rules;
- own-heater tone versus no IR MAWS distinction;
- C-primary AudioEngine plus protected low-level hardware wrappers;
- Delta/Echo/Foxtrot integration and acceptance model.

### 25.4 Changes intentionally incorporated from the Radar/Sensor white paper

Revision 1.6 adopts:

- two isolated 24-track MEGA/BLUE and RED tactical knowledge domains;
- fixed SensorHandoffState and next-tick seeker/support causality;
- independent tactical-link and weapon-support semantics;
- ownship jammer MEGA LINK denial behavior;
- simplified deterministic IR signature architecture;
- +3 G countermeasure qualification;
- active-radar versus passive-IR seeker/RWR distinctions;
- SensorAndTrack observation/assessment ownership and WeaponAndDamage missile/guidance ownership.

### 25.5 Changes intentionally incorporated from the AI Behavior/Decision white paper

Revision 1.6 adopts:

- AI as the fifth detailed subsystem white-paper domain;
- player aircraft under human flight control with RIO assistance, not hidden AI autopilot;
- all other applicable aircraft/surface entities driven by deterministic authored-role AI;
- strict legal-knowledge boundaries with no global truth, sensor telepathy, hidden inventory, or IR-missile omniscience;
- the hierarchical doctrinal controller from HARD SAFETY through CONTROL / INTENT OUTPUT;
- deterministic consequence-based interrupt precedence;
- separated reflex and lower-cadence doctrine evaluation inside stage 16;
- bounded `AIIntentFrame` with guidance/system/weapon/sensor intent separation;
- next-tick-only consumption and held-intent semantics while high-rate controllers continue at 100 Hz;
- authored/precompiled route mobility and no general runtime pathfinding;
- doctrine composition from unit/faction/proficiency/mission posture and optional Novice-hostile modifiers;
- Realistic baseline plus Novice hostile-only tactical difficulty architecture;
- Phase-1 interface/measurement hooks with production AI implementation and tuning remaining Phase 4.

### 25.6 Product Story framing incorporated by human review

Revision 1.6 selectively incorporates the supplied Product Story's CAS / Pacific Directorate / Aurelia strategic premise, Aero Dynamics West aircraft origin, President Richard Rump nostalgia framing, and carrier/swing-wing/cockpit visual identity. It intentionally does not expand that short framing into additional campaign narrative.

Because older architecture used Meridian Maritime Compact / Boreal Directorate names, the lore/faction naming change is explicitly recorded here. Human review of Revision 1.6 adopts the CAS / Pacific Directorate / Aurelia framing while preserving the older names as provenance.

### 25.7 Historical and transitional documents under Revision 1.6

Revision 1.6 now supersedes the prior master architecture and retires the alignment overlay. Gameplay 0.2 and Engine Runtime 0.2 remain transitional provenance/input until their v1 successors are human-reviewed; where either conflicts with Revision 1.6, this Main Concept controls. The disposition is:

- Architecture Revision 1.5.1 and earlier - **superseded by Revision 1.6**;
- Gameplay 0.2 and earlier - **transitional source until Gameplay v1 is human-reviewed**, then historical;
- Engine Runtime 0.2 and earlier - **transitional source until 65Aero Runtime v1 is human-reviewed**, then historical;
- Read-First / Technical Alignment documents - **retired from active authority**;
- F65-GAD-001 - **historical provenance; durable graphics decisions are absorbed into Revision 1.6**;
- older physics/graphics research revisions - historical/supporting only unless explicitly identified by an active white paper.

Engineering evidence, Git history, generated schemas, test reports and acceptance records remain retained.

---

## Appendix A - source corpus used for the corrected 1.6 rewrite

The following exact files were reviewed for this controlled correction. SHA-256 is included for provenance; it does not make a subordinate source equal in authority to the resulting Main Concept.

- **Superseded Main Concept working draft reviewed/corrected:** `F65_Main_Concept_v1.6.md`  
  SHA-256: `bba212a95232cce851025f79c41578e7878704f4e5211635b853272224766398`
- **Architecture provenance/source:** `F-65 Megawing Revision 1.5.1 - Architecture Invariants.md`  
  SHA-256: `46ba078cb397d257de6aeee66cff510c5e3243bca97767db1738d86d9ebd1fec`
- **Gameplay provenance/source:** `F-65 Megawing Gameplay and Simulation Requirements Supplement.md`  
  SHA-256: `5db0344f8e7fd66143874310c3794a64391d4767229a90f5caee5e5e287d84e4`
- **Runtime provenance/source:** `F-65 Engine Runtime and Toolchain Design Supplement Draft 0.2.md`  
  SHA-256: `dfd4bf0b557b4dae6382de502db42e4b2d269ceaf44bd67440bb6d047341454a`
- **Flight Physics / Simulation:** `MEGA65_Flight_Simulation_Physics_6DOF_Atmosphere_White_Paper.pdf`  
  SHA-256: `2da11ee4f6d0a2c8b5e45ddde896161b94b68ed1e5e8d19bad2c37a0d4bdb9b5`
- **Graphics:** `F-65_Megawing_Graphics_White_Paper_v2.1.pdf`  
  SHA-256: `b94b3db857b0b7536aad23dcdc4918625fc7da27584df6886da58391b75fdb51`
- **Audio:** `F-65_Megawing_Audio_Sound_Effects_and_Music_Engineering_White_Paper_v1.0_FINAL(1).pdf`  
  SHA-256: `2ae025b36bdbd92b5a0ac51bcead40baeec96d23765e1519fa5d672915be35ff`
- **Radar / Sensors / Tracks:** `F-65_Megawing_SensorAndTrackEngine_Engineering_Model_Phase-3_v1.0(1).pdf`  
  SHA-256: `cd9369116018b81d622360d7868e534c6e31afc98fc6378e0ed8d7450d617b25`
- **AI Behavior / Decision Architecture:** `F-65_Megawing_AI_Behavior_and_Decision_Architecture_White_Paper_v1.0(1).pdf`  
  SHA-256: `d11877582c44aed5088354e871bc7825d4dd46fb406e55dbecf84d7a01a85d20`
- **Product Story / lore add-on:** `F65_Megawing_Product_Story_Paper.docx`  
  SHA-256: `e15aa27f2e77e2a6c21eec450c10fff570174510bbfe1777f6d1b75a62ca9511`
- **Graphics decision provenance:** `F-65_Graphics_Architecture_Decision_Memo_Hybrid_Affine_Sparse-Polygon_World_Renderer_v0.1.md`  
  SHA-256: `f4610bf55a63030cf7aee5a6a8b20f98a59a3b3dba79af12eb45bb868fcbf591`
- **Historical alignment provenance only:** `F-65_Technical_Alignment_and_Read_First_Supplement_v1.0.md`  
  SHA-256: `f957b97e146fc4d35d094072eee52d2cc91185f76c7cef232efe898ce7628cc7`

The Read-First/Technical Alignment family is not carried forward as an active authority layer in v1.6.

---

## Appendix B - current program gate summary

| Gate | Revision 1.6 status | Purpose |
|---|---|---|
| R0-A | **COMPLETE** | Toolchain, MemoryAccessABI, C/45GS02/platform identity |
| R0-B | **COMPLETE** | Display/cockpit/input/audio measurement baseline |
| R0-C | **COMPLETE** | Package, D81, resource/residency, storage/save proof baseline |
| R0-D | **CURRENT** | Protected-load calibration and instrumentation |
| R0-E | Planned | Combined Xemu integration and white-paper downstream adoption |
| R0-F | Planned | Exact physical-MEGA65 confirmation |
| Measured limits | Planned after R0-F | Freeze demonstrated hardware-dependent limits |
| Phase 1 | Next major production gate | Build and prove integrated 65Aero engine harness |
| Phase 2 | After Phase-1 PASS | F-65 flight/aircraft systems |
| Phase 3 | After Phase-2 acceptance | Radar, weapons, countermeasures, damage |
| Phase 4 | After Phase-3 acceptance | Tactical layer, Technical Combat Slice, Midnight Spear |
| Phase 5 | Final | Campaign, compatibility, optimization, release |

---

## Appendix C - rewrite instructions for the two core subordinate documents

### C.1 Gameplay and Simulation Supplement v1

The next Gameplay rewrite shall describe **how F-65 works and plays from the player's perspective**. It shall carry forward the product scope while reconciling:

- AUGMENTED/AUG_OFF and FCS capability/degradation;
- ADLC/autothrottle behavior;
- player aircraft systems and procedures;
- MEGA LINK / RED LINK behavior;
- offboard-versus-ownship fire-control limits;
- jammer behavior;
- +3 G chaff/flare qualification;
- radar/RWR/IR/seeker presentation;
- no IR MAWS;
- graphics/presentation contracts visible to the player;
- audio/warning/music/speech behavior visible to the player;
- Realistic/Novice AI difficulty behavior, with Novice hostile-only unless deliberately expanded;
- player/RIO boundary, wingman/AIC behavior, AI procedural operation and tactical behavior visible to the player;
- adopted CAS/Pacific Directorate/Aurelia product framing and any approved campaign-facing lore details;
- mission/campaign progression, controls, accessibility and acceptance;
- the §4.6 player-facing performance bar where observable, without promoting R0-gated engineering values into gameplay constants;
- mandatory retirement of stale `Assisted`/`Manual` flight-law terminology and stale `SimulationSnapshot` presentation wording in favor of `AUGMENTED`/`AUG_OFF` + `FCSStatus` and `PresentationSnapshot`;
- named acceptance scenarios for at least ordinary cruise, the combined fleet fight, carrier Case I/recovery registration, warning/audio contention, AUG_OFF handling, and PAL/NTSC authoritative equivalence, with exact measured pass bars supplied by the 65Aero Runtime/evidence set.

Gameplay v1 shall not become the low-level implementation manual. It must describe what the player sees, commands, hears, and experiences while referring implementation timing, memory, generated record layouts, and hardware-measurement detail to 65Aero Runtime v1.

### C.2 65Aero Engine Runtime and Technical Supplement v1

The next 65Aero Runtime rewrite shall be the **complete low-level backend engineering umbrella**. It shall define how all major technology works together on the MEGA65, including:

- CoreRuntime and module ownership;
- compiler/toolchain and C/assembly ABI;
- memory/map/DMA/IRQ/platform services;
- fixed pools, commands/events and tick dispatch;
- generated interfaces/numeric registries;
- resource/storage/package systems;
- renderer, world-registration, occlusion and protected presentation;
- audio scheduler, SID/PCM wrappers and latency;
- physics/controls/system interfaces and Phase-2 implementation path;
- sensor/track handoff, two knowledge domains and Phase-3 schemas;
- weapons/damage ownership;
- AIEngine ownership, bounded legal-knowledge views, stage-16 scheduler, AIIntentFrame/held-intent semantics, route/facility/procedural records, doctrine/profile data, AI memory/cycle ledgers and Phase-4 plug-in boundary;
- AI/mission/toolchain integration;
- replay/checksum/fault/diagnostic/evidence systems;
- `AircraftPhysicsClass` records, mission-load selection rules, and integrated timing evidence for the required nine-aircraft overlap, including the conditional AIC class;
- per-tick and per-stage CPU/latency ledgers measured in R0-D/E/F rather than guessed in the Main Concept;
- world-cadence and displayed-world-age instrumentation/counters, including validation of the 30 Hz cruise TARGET, 25 Hz combined-combat TARGET, 20 Hz failure floor, and the later-selected maximum world-age limit;
- hard closure of the `$010000-$017FFF` active-simulation subledger with generated SensorTrack, `SensorHandoffState`, systems, command/intent, and AI record sizes before downstream resident-state admission;
- R0-D/E/F closure and Phase-1 acceptance.

65Aero Runtime v1 owns the detailed performance constitution: actual clock budgets, p95/worst measurements, warning/input latency ceilings, DMA contribution, high-water counters, and evidence identities. Those values are deliberately not frozen as master-document constants before measurement.

It shall preserve the detailed white papers as subsystem depth, not duplicate every equation or tuning table.

---

**End of F65 Main Concept v1.6 - FINAL - HUMAN-REVIEWED**
