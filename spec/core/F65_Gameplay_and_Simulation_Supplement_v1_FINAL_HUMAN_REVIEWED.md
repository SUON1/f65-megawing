# F65 Gameplay and Simulation Supplement v1

## Player-Facing Behavior, Aircraft Operation, Combat, Missions, Campaign, Presentation, and Acceptance

**Document ID:** `F65-GAMEPLAY-1.0`  
**Version:** 1.0  
**Status:** FINAL - HUMAN-REVIEWED  
**Human review completed:** 27 August 2026  
**Approval effect:** Active player-facing Gameplay baseline subordinate to F65 Main Concept v1.6.  
**Date:** 27 August 2026  
**Platform:** MEGA65 - 45GS02 + VIC-IV  
**Parent authority:** **F65 Main Concept v1.6 - FINAL HUMAN-REVIEWED**  
**Parent identity:** `F65_Main_Concept_v1.6_FINAL_HUMAN_REVIEWED.md`  
**Parent SHA-256:** `e7d8ed40ce630d82e707e2a9c7f29995fac6f4281849c2c7ef5261d420c2c425`  
**Technical companion:** **F65 65Aero Engine Runtime and Technical Supplement v1** - pending coordinated rewrite  
**Detailed subsystem references:** Flight Physics v3.3, Graphics v2.1, Audio v1.0, Radar/Sensors/Tracks v1.0, AI Behavior/Decision v1.0  
**Supersedes:** F-65 Megawing Gameplay and Simulation Requirements Supplement Draft 0.2  
**Nature:** Player-facing gameplay and simulation requirements. This document defines what the player sees, commands, hears, and experiences. It does not define low-level target implementation, generated record layouts, memory packing, per-stage cycle budgets, DMA details, or subsystem algorithms.

> **Version 1 aligns the gameplay specification with F65 Main Concept v1.6.** It replaces the stale flight-control vocabulary of the 0.2 draft, adopts the two-domain MEGA/RED tactical-knowledge model, propagates the human-reviewed Radar/Sensor and AI behavior changes, incorporates the current Graphics and Audio presentation contracts, and preserves the established campaign, aircraft-system, weapon, carrier, training, capacity, and deterministic-simulation intent. Exact engineering structures and measured limits remain owned by 65Aero Runtime v1 and the five subsystem white papers.

---

## 0. Purpose, authority, and scope

### 0.1 Purpose

F65 Gameplay and Simulation Supplement v1 is the player-facing requirements authority subordinate to F65 Main Concept v1.6.

It defines:

- the product flow and player role;
- how the F-65A flies and is operated;
- flight-control, engine, aircraft-system, fuel, damage, carrier, and airfield behavior as experienced by the player;
- cockpit, HUD, map, radar, RWR, tactical-link, weapon, countermeasure, audio, and warning behavior;
- RIO, wingman, AIC, friendly and hostile AI behavior visible to the player;
- Realistic and Novice AI difficulty behavior;
- mission, training, ROE, campaign, save, debrief, and progression rules;
- capacity and authored-mission gameplay limits;
- player-facing acceptance requirements.

This document intentionally does **not** reproduce white-paper algorithms, target record packing, AI doctrine tables, radar coefficient tables, physics equations, renderer internals, audio scheduler internals, or 45GS02/LLVM-MOS implementation details.

### 0.2 Active hierarchy

The active design family is:

1. **F65 Main Concept v1.6** - master product and architecture authority.
2. **F65 Gameplay and Simulation Supplement v1** - this player-facing requirements document.
3. **F65 65Aero Engine Runtime and Technical Supplement v1** - low-level engine and implementation umbrella.
4. **Flight Physics and Simulation Engineering White Paper v3.3**.
5. **Graphics Engineering White Paper v2.1**.
6. **Audio, Sound Effects and Music Engineering White Paper v1.0**.
7. **Radar, Sensors and Track Engineering White Paper v1.0**.
8. **AI Behavior and Decision Architecture White Paper v1.0**.

The five white papers provide detailed subsystem engineering depth. They cannot independently override the Main Concept or this approved Gameplay document. When a human-reviewed white paper identifies a durable behavior that was intentionally propagated into Main Concept v1.6, this document uses the updated concept.

### 0.3 Precedence

- **MUST:** F65 Main Concept v1.6 controls architecture, subsystem ownership, 100 Hz timing, deterministic causality, memory boundaries, fixed capacities, development phases, and non-negotiable platform constraints.
- **MUST:** This document controls player-visible and mission-visible behavior within those invariants.
- **MUST:** 65Aero Runtime v1 controls implementation only after satisfying Main Concept and Gameplay requirements.
- **MUST:** The five subsystem white papers control engineering detail only where they remain consistent with the core specification set.
- **MUST:** The retired Read-First / Technical Alignment documents are provenance only and have no active authority.

### 0.4 Development-state relationship

The current program baseline is:

- R0-A COMPLETE;
- R0-B COMPLETE;
- R0-C COMPLETE;
- R0-D CURRENT;
- R0-E planned;
- R0-F planned;
- measured-limits closure follows R0-F;
- Phase 1 builds the integrated 65Aero engine harness;
- Phase 2 implements flight/aircraft systems;
- Phase 3 implements radar/weapons/countermeasures/damage;
- Phase 4 implements the production tactical AI layer, Technical Combat Slice, and Midnight Spear;
- Phase 5 completes campaign and release.

This Gameplay rewrite does not reopen R0-A/B/C and does not promote unmeasured R0-D/E/F values into fixed gameplay constants.

---

## 1. Requirement classes

Every normative statement uses one of four classes.

| Class | Meaning |
|---|---|
| **MUST** | Durable player-facing or simulation behavior required by the product. |
| **TARGET** | Intended feel, tuning, quality, or product target that may move through recorded evidence and human review. |
| **MEASURED** | Hardware/presentation/input/latency choice that freezes only through the applicable R0-D/E/F and measured-limits evidence. |
| **TBD** | Required table, coefficient, threshold, authored value, or content decision whose closure belongs to a named later phase. |

- **MUST:** TARGET, MEASURED, and TBD material cannot weaken a MUST.
- **MUST:** A convenient prototype value does not become shipping behavior merely because it exists in code.
- **MUST:** Exact byte layouts, memory placement, queue depth, cycle budgets, DMA job sizes, and generated schema fields belong to 65Aero Runtime and generated artifacts, not this document.

---

## 2. Product identity and player experience

### 2.1 Product

F-65 Megawing is a single-player, cockpit-primary, retro-synthwave fleet-interceptor combat-flight simulator for the MEGA65.

The player is an F-65A pilot operating inside a serious flight/combat simulation whose presentation deliberately evokes late-1980s and early-1990s computer flight simulators.

The player experience combines:

- consequential 6DOF flight and energy management;
- modern-feeling augmented fighter controls with a genuinely flyable AUG_OFF mode;
- cold start, aircraft systems, failures, fuel, damage, and recovery management;
- long-range interception, radar combat, RWR, jammer, countermeasures, radar and IR missiles, and cannon;
- carrier and airfield operations;
- an AI RIO that manages workload but does not secretly fly the player aircraft;
- wingman, AIC, hostile aircraft, SAM/IADS, ship, and ground AI;
- MEGA LINK tactical information without omniscient shared truth;
- protected cockpit/HUD/warning/audio presentation even when the outside world renders at a lower cadence.

### 2.2 World framing

The active product framing follows Main Concept v1.6:

- the player serves the **Coalition of American States (CAS)**;
- the **Pacific Directorate** is expanding reef outposts and runways around the independent island city-state of **Aurelia**;
- CAS carrier groups move into the approaches and F-65A aircraft provide fleet cover;
- the F-65A was developed by **Aero Dynamics West** as a modern 4.5-generation two-seat, twin-engine, variable-geometry fleet interceptor with deliberate 1980s design DNA.

- **MUST:** Gameplay may use this framing to explain missions, ROE, briefing context, and campaign stakes.
- **MUST:** This document does not invent additional governments, wars, biographies, named squadrons, carriers, dates, ideologies, or campaign events beyond approved authored content.

### 2.3 Core gameplay loop

The intended sortie loop is:

```text
brief / configure
    -> start state or cold start
    -> taxi / launch / takeoff
    -> navigate / form / intercept / execute mission
    -> manage radar, weapons, threats, fuel, damage, and team
    -> recover to carrier or airfield
    -> debrief / grade / campaign consequence
```

Not every mission must contain every step. Training, Free Flight, Technical Combat Slice, campaign, and special missions may start at different legal points while preserving the same simulation rules.

### 2.4 Simulation philosophy visible to the player

- **MUST:** The authoritative physical simulation remains exactly 100 Hz during an active sortie.
- **MUST:** Every live physical aircraft, missile, countermeasure, projectile group, ship/surface entity, and simulation-relevant physical entity remains on that same authoritative timeline according to its declared physical model.
- **MUST:** KINEMATIC aircraft use cheaper physical modeling on the same 100 Hz clock; they do not use a second physical-simulation clock.
- **MUST:** Sensor information, AI decisions, radar/MFD rebuilding, audio parameter refresh, and world rendering may have their own deterministic service cadences without changing the physical clock.
- **MUST:** AI/RIO decisions based on newly completed sensor state cannot take physical effect in the same tick in which those decisions are produced.
- **MUST:** Presentation never changes whether a detection, hit, warning, objective, collision, or AI decision physically occurred.

---

## 3. Product flow, settings, difficulty, saves, and pause

### 3.1 Title and game modes

- **MUST:** The title screen provides **Continue**, **Campaign**, **Free Flight**, and **Settings**.
- **MUST:** Campaign provides three user-managed save slots.
- **MUST:** Free Flight uses validated presets for location, start state, weather, loadout, and friendly/hostile traffic rather than a general-purpose player mission editor.
- **MUST:** The product provides a complete keyboard-only control path when no joystick is present.
- **MUST:** Joystick plus keyboard remains the intended primary control experience.
- **MUST:** PAL/NTSC selection is automatically detected and may expose a compatibility override without changing authoritative simulation results.

### 3.2 AI difficulty

The player-facing AI difficulty setting is:

- **Realistic** - default. Uses the baseline AI doctrine thresholds, employment timing, defensive response, aggression, support discipline, coordination, and maneuver logic.
- **Novice** - uses the same controller, state graphs, maneuver primitives, physical models, sensors, weapons, and legal-information boundaries, but hostile tactical AI employs later, reacts defensively later, commits less aggressively, and favors earlier skate/abort behavior.

- **MUST:** Realistic is the default setting.
- **MUST:** Novice modifiers apply to hostile tactical AI only unless a later approved Gameplay revision explicitly expands their scope.
- **MUST:** Friendly AI, including the player wingman, AIC, and other Blue forces, uses normal doctrine in both modes.
- **MUST:** Difficulty never changes aircraft physics, weapon kinematics, seeker/radar performance, damage, hidden-information access, or authoritative truth.
- **MUST:** The selected AI mode is latched when a sortie starts so AI doctrine does not change invisibly during an active run.
- **TARGET:** The selected AI mode persists as a user setting across sessions. Exact settings-file/save-slot ownership is defined by 65Aero Runtime v1.

### 3.3 Pause and restart

- **MUST:** Full pause freezes authoritative simulation.
- **MUST:** Pause provides **Resume**, **Controls**, **Restart Sortie**, **Settings**, and **Exit to Title**.
- **MUST:** On full pause, authoritative simulation-driven audio events stop advancing; UI/pause music may continue under presentation rules, and stale physical one-shot sounds are not invented or replayed on resume.
- **MUST:** Time acceleration is not supported.
- **MUST:** Restart Sortie starts a new deterministic run from the mission start state rather than rolling simulation time backward.
- **MUST:** Tutorial segment retry ends the current run and starts a new deterministic run from an authored lesson-start state.

### 3.4 Saves and replay

- **MUST:** Campaign saves occur only outside an active sortie.
- **MUST:** There is no normal mid-sortie save/restore.
- **MUST:** Death, capture, ejection, or aircraft loss does not delete a campaign save.
- **MUST:** Player-facing replay is a debrief/event timeline, not a free-camera simulation replay.
- **MUST:** Save data is versioned product/campaign state, not a raw dump of runtime structures.
- **TBD:** Exact save presentation, compatibility policy, and multi-D81 campaign flow close in Phase 5 and 65Aero Runtime v1.

---

## 4. Capacity, simultaneous load, and mission authoring

### 4.1 Capacity is not the same as required live load

The aircraft pool can hold sixteen aircraft records. The required baseline combined-load air-combat case uses nine simultaneously live aircraft. These are different requirements.

| Class | Hard pool capacity | Required current live peak | Baseline headroom | Gameplay meaning |
|---|---:|---:|---:|---|
| Aircraft | 16 | 9 | 7 | One player F-65A plus AI-controlled aircraft |
| Guided missiles | 32 | 16 | 16 | Friendly and hostile missiles may overlap |
| Gun projectile groups | 32 | 24 | 8 | Six gun-capable combat aircraft at four live groups each |
| Chaff/flare entities | 64 | 48 | 16 | Up to six live decoys for each of eight defensive aircraft |
| Ships/carriers | 8 | 1 in baseline air peak | 7 | Player recovery carrier in the baseline air fight |
| Surface radar/SAM entities | 16 | 0 in baseline air peak | 16 | Validated in surface scenarios |
| Dynamic mission entities | 32 | 8 | 24 | Training/mission-specific dynamic objects |
| Simulation-relevant effects | 32 | 0 currently required | 32 | No current persistent damaging/sensor-affecting volume required |
| Presentation effects | 64 | 64 | 0 | Optional visual/audio spectacle may fill then shed |
| Radar truth contacts | 32 | Baseline air picture fits | Remaining by mission | Shared physical candidate set |
| MEGA/BLUE semantic tracks | 24 | Baseline player-domain picture fits | Mission-dependent | Player/friendly tactical knowledge domain |
| RED semantic tracks | 24 | Adversary-domain picture fits | Mission-dependent | Capacity-isolated hostile knowledge domain |
| RIO priority tracks | 4 | 4 | 0 | Subset of MEGA/BLUE tracks only |
| Active objectives | 16 | 8 | 8 | Opening/training upper-bound target |

### 4.2 Baseline nine-aircraft profile

The baseline acceptance profile contains:

- one player F-65A;
- one wingman;
- four hostile combat aircraft;
- one rescue helicopter;
- one civilian aircraft;
- one physical AIC aircraft.

Total: **9 simultaneously live aircraft**.

For the required baseline combined-load acceptance harness:

- player, wingman, and four hostiles are `SIX_DOF`;
- rescue helicopter and civilian aircraft are `KINEMATIC`;
- the baseline AIC is `KINEMATIC`, producing six `SIX_DOF` plus three `KINEMATIC` aircraft;
- a separately identified `SIX_DOF-AIC` harness variant is required when the AIC must maneuver defensively or participate as a combat actor.

- **MUST:** Physics class is fixed by mission/harness load and does not change because of range, visibility, camera, rendering load, or CPU pressure.
- **MUST:** All nine aircraft remain physical entities, sensor contacts, collision participants, and 100 Hz timeline participants.

### 4.3 Surface-scenario profile

- **TARGET:** A current-scope surface mission uses no more than one carrier plus three designated small vessels and eight surface radar/SAM entities unless a later approved mission manifest proves a different legal overlap.
- **MUST:** Only live entity-based surface targets can receive physical damage.
- **MUST:** Static scenery cannot be promoted into a destructible entity during runtime.
- **MUST:** Mission validation accounts for simultaneous air, missile, countermeasure, gun, contact, objective, and effect load rather than validating surface counts in isolation.

### 4.4 Mission-authoring rule

- **MUST:** Authored missions must fit every non-droppable capacity across every legal overlap of spawns, weapons, decoys, route/procedure state, objectives, AI behavior, and required entities.
- **MUST:** A required objective, defensive action, weapon event, launch/recovery path, or tutorial step cannot depend on runtime pool exhaustion behaving favorably.
- **MUST:** Optional presentation effects may shed; required physical gameplay state may not.
- **MUST:** The mission compiler and runtime high-water evidence are the engineering proof mechanisms. Exact compiler algorithms remain outside this Gameplay document.

---

## 5. Semantic input and control contexts

### 5.1 Control contexts

The four primary semantic contexts are:

- **Deck**;
- **TFL** - Takeoff and Landing;
- **Normal Flight**;
- **Combat**.

- **MUST:** Control context changes input semantics and presentation only. It does not itself select FCSMode.
- **MUST:** Entering Combat changes the primary joystick action to weapon fire.
- **MUST:** Entering Combat requests conventional autothrottle capture at current KIAS when autothrottle is available; autothrottle failure cannot prevent the aircraft from entering Combat or arming weapons.
- **MUST:** While conventional autothrottle is engaged, the contextual speed command changes captured KIAS rather than directly commanding throttle angle.
- **MUST:** A separate Safe action returns the primary action to contextual-menu duty.

### 5.2 Durable player actions

The player must have semantic access to at least:

- arm;
- safe;
- fire;
- weapon cycle;
- autothrottle toggle/capture;
- autothrottle speed adjustment;
- ADLC request;
- `AUGMENTED` / `AUG_OFF` mode toggle;
- manual throttle increment/preset;
- minimum and maximum afterburner;
- gear;
- flaps;
- speedbrake;
- hook;
- brakes;
- ejection;
- map anchor/mode;
- radar scale;
- waypoint advance;
- RIO target/interrogate;
- AIC picture;
- wingman command intent;
- wing-sweep override and return-to-Auto;
- aircraft-system/startup actions required by Section 8.

- **MUST:** Bindings request semantic actions. They never directly set physical aircraft, sensor, weapon, or mission state.
- **MUST:** Weapon selection defaults to the RIO recommendation while still allowing explicit player cycling through long-range radar missile, medium-range radar missile, heater, and gun.
- **MUST:** Countermeasure and defensive-jammer operation defaults to RIO control; a dedicated manual decoy binding is not required for Version 1.
- **MUST:** Version 1 intentionally retains RIO-default countermeasure operation. A later numbered Gameplay revision may add an optional manual countermeasure action without reopening the Main Concept or changing the authoritative defensive-system model.

### 5.3 Preferred control layout

The following remain current preferred targets rather than immutable key assignments:

- `A` for contextual autothrottle/ADLC use;
- `Shift-A` for `AUGMENTED` / `AUG_OFF` toggle;
- `W` for weapon cycle;
- `D` for Safe;
- `F` for flaps;
- `G` for gear;
- `H` for hook;
- `B` for brakes;
- `M` for map anchor;
- `[` / `]` for sweep override;
- held `Shift-E` for ejection.

The preferred Normal Flight radial/pie actions include Arm, Autothrottle, RIO Lock/Interrogate, Wingman Commands, AIC Picture, Next Waypoint, and Radar Scale Down/Up.

The wingman command set exposes:

- Engage;
- Cover;
- Rejoin;
- Return.

- **MEASURED:** Exact keys, joystick dwell, hold-versus-motion arbitration, repeat acceleration, dead zones, ejection confirmation duration, throttle step, and radial-menu geometry are selected from input/hardware evidence.
- **MUST:** Final bindings must preserve every required semantic action without an ambiguous fire-versus-mode gesture.

---

## 6. World and environment

- **MUST:** The world uses aviation-facing units and the authoritative North-East-Down world and carrier-local frame defined by Main Concept/65Aero.
- **MUST:** A mission operates in a finite authored region surrounded by valid sparse world coordinates. There is no invisible wall, forced turn, or boundary-triggered failure merely because the player reaches an edge of a dense visual area.
- **TARGET:** A typical authored operating region is approximately 256 x 256 nmi.
- **MUST:** Atmosphere, gravity, wind, pressure, temperature, density, speed of sound, and airspeed conversions are shared deterministic simulation inputs to aircraft and missiles.
- **MUST:** Mission weather may define surface, middle, and high-altitude wind layers and a deterministic temperature profile.
- **MUST:** Clouds are presentation-only in Version 1 unless a later approved revision grants them physical/sensor effects.
- **MUST:** Missions use authored day, dusk, or night lighting presets rather than continuous astronomical time-of-day simulation.
- **MUST:** Rescue, civilian, AIC, wingman, and hostile aircraft remain real physical/sensor/collision entities according to their mission-load physics class.
- **MUST:** Secured deck aircraft inherit deterministic carrier motion.
- **MUST:** Wave-driven carrier heave, pitch, and roll remain outside current scope.

---

## 7. F-65A flight model, FCS, and handling

### 7.1 Physical flight model

- **MUST:** The player F-65A uses consequential table-driven 6DOF rigid-body dynamics on the 100 Hz authoritative timeline.
- **MUST:** Aerodynamic force and moment depend on physical flight state including Mach, angle of attack, sideslip, configuration, actual control-surface state, wing sweep, damage, atmosphere, current mass, and the detailed white-paper model.
- **MUST:** Energy is physical. Turns, climbs, induced drag, configuration drag, damage drag, maneuvering, and density can reduce speed even when the player demands maximum available power.
- **MUST:** Aircraft mass changes with fuel, missile expenditure, and cannon ammunition.
- **MUST:** The model contains no hidden altitude hold in normal maneuvering.
- **MUST:** The aircraft must remain manually controllable in `AUG_OFF` throughout the approved `F65_UNAUGMENTED_FLIGHT_ENVELOPE` when capability permits.

### 7.2 Separated flight-control concepts

The player-facing concepts are distinct:

```text
ControlContext = DECK / TFL / NORMAL_FLIGHT / COMBAT
FCSMode        = AUGMENTED / AUG_OFF
FCSStatus      = NORMAL / DEGRADED / DIRECT_ONLY
ADLCState      = independent approach overlay
Autothrottle   = independent state
```

- **MUST:** `FCSMode` is the commanded/pilot-selected mode.
- **MUST:** `FCSStatus` is the available augmentation capability.
- **MUST:** `DIRECT_ONLY` forces direct effective behavior even if the cockpit switch remains in AUGMENTED.
- **MUST:** The cockpit/status presentation must make a meaningful commanded-mode versus capability failure distinguishable to the player.

### 7.3 AUGMENTED mode

`AUGMENTED` is the normal/default F-65 flight-control mode.

- **MUST:** Longitudinal stick commands scheduled normal acceleration with pitch-rate/AoA feedback where capability allows.
- **MUST:** Lateral stick commands scheduled roll rate.
- **MUST:** Yaw damping, coordination, automatic trim, and approved G/AoA protection operate when capability allows.
- **MUST:** Commands remain limited by real energy, aerodynamics, configuration, sweep, dynamic pressure, hydraulics, actuator authority, and damage.
- **MUST:** Neutral stick does not command altitude hold.
- **TARGET:** A healthy clean aircraft supports approximately +9 G / -3 G command authority inside the validated envelope.
- **TARGET:** A healthy clean aircraft reaches approximately 180 degrees/second maximum commanded roll rate.
- **TARGET:** Digital/keyboard aft-stick response builds progressively rather than snapping immediately to maximum G.
- **TBD:** Exact control gains, schedules, protection boundaries, command ramps, anti-windup, and configuration effects freeze in Phase 2.

### 7.4 AUG_OFF mode

`AUG_OFF` is true direct/manual flight. It is not another hidden rate-command law.

- **MUST:** Pitch input becomes direct elevator/stabilator demand through the approved non-augmenting mixer/gearing.
- **MUST:** Roll input becomes direct lateral-surface demand through the approved mixer/gearing.
- **MUST:** Yaw input becomes rudder demand.
- **MUST:** Pilot trim remains available.
- **MUST:** Hydraulics, actuator rates/stops, control mixing/gearing, damage, asymmetry, and actual surface response remain active.
- **MUST:** Closed-loop G-command, roll-rate command, G/AoA limiting, and artificial FCS stability damping are removed.
- **MUST:** Natural aerodynamic static/dynamic stability supplies the aircraft's unaugmented behavior.
- **MUST:** Stall, departure, over-G, overspeed, energy loss, and unrecoverable situations remain possible.
- **MUST:** `AUG_OFF` does not imply identical carefree handling across the full augmented operating envelope.

### 7.5 Degraded and DIRECT_ONLY capability

- **MUST:** Damage or system failure may place `FCSStatus` in DEGRADED or DIRECT_ONLY without silently moving the player's cockpit-selected switch.
- **MUST:** DEGRADED behavior uses only remaining legal augmentation/control capability.
- **MUST:** DIRECT_ONLY effective behavior obeys the physical direct-control path and cannot restore failed protection through gameplay convenience.
- **TBD:** Exact degradation mapping by failed sensor/axis/hydraulic/FCS capability closes in Phase 2.

### 7.6 Bumpless transfer

- **MUST:** Changing FCSMode or FCSStatus must not create an artificial jump in control surface, attitude, angular rate, G, speed, or position solely because a state changed.
- **MUST:** AUGMENTED -> AUG_OFF uses the bounded temporary transfer behavior defined by the Physics white paper and does not silently rewrite pilot trim.
- **MUST:** AUG_OFF -> AUGMENTED re-enters augmentation from the current physical aircraft state rather than teleporting the aircraft onto a commanded condition.

### 7.7 Aircraft performance targets

| Requirement | Class | Current target |
|---|---|---:|
| Operating empty weight | TARGET | 40,000 lb |
| Internal fuel | TARGET | 20,000 lb |
| Maximum takeoff weight | TARGET | 72,000 lb |
| Maximum carrier landing weight | TARGET | 56,000 lb |
| Operational top performance | TARGET | Mach 2.5 |
| Service ceiling | TARGET | 65,000 ft |
| Structural overspeed boundary | TARGET | First of 900 KIAS or Mach 3.0 |
| Carrier/landing configuration limit | TARGET | 300 KIAS |

- **MUST:** Primary handling speed and autothrottle capture use KIAS; Mach appears where operationally relevant.
- **MUST:** External fuel tanks remain outside current scope.
- **TBD:** Thrust-to-weight, climb, acceleration, turn, stall, drag, unaugmented envelope, and detailed aircraft-performance values freeze through Phase 2 physics/oracle/human handling review.

---

## 8. Engines, configuration, aircraft systems, and startup

### 8.1 Engines and throttle

- **MUST:** Each engine independently exhibits RPM/spool state, thrust, fuel use, military/afterburner state, damage, flameout, and relight capability.
- **MUST:** Engine-out produces real asymmetric aircraft behavior rather than a scripted yaw effect.
- **MUST:** A viable stopped engine may attempt automatic relight when its physical/system prerequisites are satisfied.
- **MUST:** Afterburner materially affects fuel use, thrust, IR signature class, and audio presentation through actual engine state.
- **TARGET:** Canonical throttle-angle detents remain 90% military, 95% minimum afterburner, and 100% maximum afterburner unless Phase 2 human review adjusts them.

### 8.2 Autothrottle

- **MUST:** Conventional autothrottle captures current KIAS and modulates through maximum military power.
- **MUST:** The player must explicitly select afterburner.
- **MUST:** Afterburner overrides conventional autothrottle until the player recaptures speed.
- **MUST:** Autothrottle remains independent of FCSMode and independent of ADLC except when ADLC uses its own approach-throttle behavior.

### 8.3 Variable wing sweep

- **MUST:** Wing sweep follows an automatic flight-condition schedule with manual override and a return-to-Auto action.
- **MUST:** Actual left/right sweep state changes physically through the approved hydraulic/actuator model.
- **MUST:** Damage may create asymmetric sweep and consequential handling.
- **TBD:** Exact schedule, rate, limits, and failure behavior close in Phase 2.

### 8.4 Gear, flaps, hook, and configuration

- **MUST:** Flaps cycle Up, Half, and Full.
- **MUST:** Half is the normal takeoff setting; Full is the nominal landing setting.
- **MUST:** Flap overspeed produces caution and automatic protective retraction with hysteresis when physically available.
- **MUST:** Gear overspeed produces caution and deterministic damage exposure; gear is not magically auto-retracted.
- **MUST:** Speedbrake has a player semantic control and changes drag through actual aircraft configuration; deployment remains subject to the approved actuator/system/damage path.
- **MUST:** Tailhook has dedicated player control and physical stowed/deployed/damaged/unavailable state.
- **MUST:** Configuration changes affect real drag, lift, control authority, carrier/airfield procedures, and damage exposure.

### 8.5 Cold start and assisted start

- **MUST:** A mission may begin cold and dark on an airfield or carrier deck.
- **MUST:** Where mission design permits, preflight offers **Manual Cold Start** or **RIO-Assisted Start**.
- **MUST:** RIO-Assisted Start traverses the same electrical, engine, generator, hydraulic, avionics, and capability states as manual startup. It does not directly set the airplane to healthy/running.
- **MUST:** Manual startup exposes stateful actions for Battery, Engine 2 Start, Engine 1 Start, Systems On, Takeoff Checks, Request Taxi, and Request Takeoff/Launch as prerequisites become meaningful.
- **MUST:** Either engine may be started first; guided procedure recommends Engine 2 first because Hydraulic System 2 supplies most essential services.
- **MUST:** Takeoff Checks require Half flaps and an approved full flight-control sweep before the RIO declares the aircraft ready.
- **MUST:** Raising gear and flaps after departure transitions the aircraft into Normal Flight control context when no higher-priority condition prevents it.
- **MUST:** Request Taxi and Request Takeoff/Launch represent authorization/progression and do not replace player steering, braking, throttle, rotation, or configuration control.
- **TARGET:** Land takeoff rotation begins near 160 KIAS at normal training weight subject to validated weight/configuration schedules.

### 8.6 Power, hydraulics, avionics, and cautions

- **MUST:** Battery power provides only limited indications/intercom capability before generators and dependent systems become available.
- **MUST:** Full radar/navigation/HUD/tactical symbology appears only as supplying systems become actually capable.
- **MUST:** A **Systems On** action requests dependency-driven initialization of ADC, FCS, ADLC, RADAR, WPS, RWR, ECM, OBOGS, communications, and displays; the action does not bypass power, hydraulic, initialization, damage, or supply prerequisites.
- **MUST:** Engine, generator, hydraulic, ADC, FCS, ADLC, RADAR, WPS, RWR, ECM, OBOGS, COMMS, fuel, fire, gear, and flap state can generate meaningful status/caution information.
- **MUST:** Healthy-but-off or initializing systems use amber status, operating systems green, failed systems red, and unavailable/no-data systems gray, subject to the final accessibility-safe palette implementation.
- **MUST:** Commanded mode, system health, supply availability, and actual capability remain distinct.
- **MUST:** Random reliability failures are excluded. Failures arise from damage, misuse, depletion, or authored mission/training events.
- **TARGET:** Engine generators come online near 50% RPM, both engines stabilize near 61% idle, main electrical indication is approximately 480 V, and a healthy hydraulic system indicates approximately 3,000 psi, subject to Phase 2 validation.
- **TBD:** Startup timing, dependency tables, cautions, hydraulic authority, relight envelope, and system initialization close in Phase 2.

---

## 9. Cockpit, HUD, map, chase view, and presentation performance

### 9.1 Cockpit identity

- **MUST:** Cockpit view is the primary authored presentation.
- **MUST:** The canopy/panel character follows the Main Concept's bubble-canopy, pilot-forward/RIO-aft identity.
- **MUST:** The HUD is green monochrome and remains the primary flight-data source.
- **MUST:** The left cockpit display is an integrated grayscale aircraft-status display rather than a player-managed page set.
- **MUST:** The right display is a fused radar/navigation presentation rather than separate player-managed radar and navigation pages.

### 9.2 Aircraft-status display

The left display presents, as applicable:

- aircraft silhouette/status including major configuration such as gear/flap/hook/speedbrake when operationally relevant;
- fuel weight;
- engine state;
- electrical state;
- hydraulic pressure;
- FCS commanded mode and degradation/capability;
- ADLC state;
- major cautions;
- weapons remaining and cannon ammunition;
- chaff and flare inventory;
- defensive-jammer state;
- explicit organic-radar-blanked indication when caused by ownship jammer operation;
- explicit MEGA LINK TX/RX denied state while ownship jammer operation denies the link;
- damage/failure state.

### 9.3 Fused radar/navigation display

- **MUST:** The right display is heading-up and shows current heading at the top.
- **MUST:** It supports 20, 40, 80, and 160 nmi selected scales unless later human review changes that product requirement.
- **MUST:** Map Anchor toggles between tactical lower-screen ownship placement and centered-ownship overview.
- **MUST:** Map context may include land/water, coastline, major elevation regions, airfields, carrier, waypoints, objective markers, tactical tracks, locks, weapon state, and source/quality cues according to available information.
- **MUST:** Offboard, organic, and fused information remain distinguishable without creating duplicate player tracks for one correlated contact.

### 9.4 HUD modes

- **MUST:** HUD content reprioritizes automatically for takeoff, navigation, combat, defense, and landing/recovery conditions.
- **MUST:** Critical warnings may overlay any HUD mode.
- **MUST:** World-registered HUD cues such as pitch ladder, flight-path reference, target designator, steering cue, and weapon pipper remain visually registered with the displayed outside-world frame.
- **MUST:** Status/non-spatial information may update from newer legal presentation state without causing the spatial cues to slide against the displayed world.

### 9.5 Chase view

- **MUST:** A low-cost external/chase view exists.
- **MUST:** It retains an essential reduced HUD with flight path, speed, altitude, target/threat, selected weapon, fuel caution, and critical warning information.
- **MUST:** Changing view cannot alter simulation, sensors, AI, collision, weapon state, or mission outcomes.

### 9.6 Positive-G presentation

- **MUST:** Positive-G desaturation begins near +6 G and approaches grayscale near +7 G as a presentation effect.
- **MUST:** Critical HUD and warning information remains readable through the effect.
- **MUST:** The effect never changes physical G, control authority, sensing, weapon outcomes, or checksums.

### 9.7 Outside-world performance bar

- **MUST:** The aircraft simulation does not slow, merge, stretch, or split physical clocks to preserve graphics performance.
- **MUST:** Protected HUD/cockpit/critical-warning presentation retains its service deadlines even when outside-world rendering is late.
- **MUST:** Only complete world buffers are shown; the player never sees a half-built world frame.
- **TARGET:** Normal cruise aims for approximately 30 completed outside-world frames per second.
- **TARGET:** Combined combat load aims for approximately 25 completed outside-world frames per second.
- **MUST:** Sustained completed-world cadence below 20 Hz is a product failure condition, not permission to slow simulation.
- **MEASURED:** Maximum acceptable displayed-world age remains R0-D/E/F and measured-limits work. This document does not freeze a millisecond value.
- **MEASURED:** Exact resolution, viewport proportions, symbol rasterization, line style, RRB/composition method, LOD distances, and presentation tier limits remain engineering selections under the Graphics/Runtime evidence chain.

---

## 10. Radar, tracks, identification, MEGA LINK, and RWR

### 10.1 Player tactical knowledge domain

- **MUST:** The player/RIO tactical picture belongs to the **MEGA/BLUE** knowledge domain.
- **MUST:** The hostile tactical picture belongs to the separate **RED** knowledge domain.
- **MUST:** Each domain has up to 24 semantic tactical tracks; the current product therefore supports up to 48 physical semantic-track records across the two isolated domains.
- **MUST:** A Blue/MEGA track cannot be evicted, degraded, or denied allocation because RED has heavy private track load, and vice versa.
- **MUST:** Neutral is an identification state, not a third tactical-link domain.
- **MUST:** RIO priority tracks are a maximum four-track subset of the MEGA/BLUE domain only.

### 10.2 Organic radar and tactical-link information

- **MUST:** Organic radar detection depends on deterministic sensor geometry and authored performance including range, aspect/signature, scan/FOV, look-down/clutter, Doppler/notch, terrain masking, and jamming.
- **MUST:** The current ownship radar field-of-regard requirement remains -85 degrees through +85 degrees unless a later approved Phase-3 revision changes it.
- **MUST:** The RIO manages scan volume, elevation, search, correlation, interrogation, and priority-track workload within the legal sensor contract.
- **MUST:** MEGA LINK is the Blue/player tactical track-sharing network. RED LINK is the adversary counterpart.
- **MUST:** An offboard-only report may cue acquisition and appear on the tactical display before ownship radar detection.
- **MUST:** Offboard-only information cannot independently create ownship weapon-quality authority or valid local missile support.
- **MUST:** Organic correlation is required for ownship weapons-quality fire-control state.
- **MUST:** Tactical link is not Weapon Support Datalink and cannot substitute for shooter-to-missile support.

### 10.3 Track source, quality, coast, and identity

- **MUST:** Player presentation distinguishes organic, offboard, and fused information.
- **MUST:** Correlated organic/offboard evidence produces one semantic track rather than duplicated contacts.
- **MUST:** Tracks may visibly transition through detection, firm/weapon-quality, coast/stale, support-lost, and drop behavior according to the approved radar model.
- **TARGET:** Nonpriority coast duration remains approximately five seconds unless Phase 3 evidence selects another value.
- **MUST:** Priority/weapon-quality state enables a valid fire-control solution and RIO recommendation but is not a launch-permission bit.
- **MUST:** Unknown/unclassified returns use a distinct unknown identity presentation; current preferred geometry remains hollow square for unknown, heading-oriented triangle for classified aircraft, and course-oriented rectangle for classified ships.
- **MUST:** Current identity color roles remain yellow unresolved, red hostile, green friendly, white neutral, with non-color redundancy for accessibility.
- **MUST:** Aircraft tracks show two-digit altitude in thousands of feet when altitude data is valid.
- **MUST:** Hostile identity requires valid IFF/mission/AIC authority or an overt hostile act under mission ROE.
- **MUST:** The RIO automatically interrogates tactically relevant unknowns and accepts an immediate player RIO-interrogate command for the selected/nearest suitable unknown.

### 10.4 Defensive jammer tradeoff

For the initial production behavior, while the F-65 defensive jammer is active:

- **MUST:** organic ownship radar is blanked;
- **MUST:** support relying on that non-autonomous organic radar is hard-invalidated at the next legal support-consumption point;
- **MUST:** MEGA LINK transmit is denied;
- **MUST:** MEGA LINK receive is denied;
- **MUST:** link reports arriving while receive is denied are lost rather than buffered for later replay;
- **MUST:** previously received offboard tracks remain and age/coast normally;
- **MUST:** when the jammer is disabled, radar and MEGA LINK resume through normal deterministic scan/update schedules rather than snapping stale tracks to perfect current state.

External hostile jamming may degrade or deny MEGA/RED link and radar behavior according to Phase 3 tables.

### 10.5 RWR and threat state

- **MUST:** RWR reports only radar emissions that are validly received according to emitter/receiver geometry and capability.
- **MUST:** RWR vocabulary distinguishes search/surveillance, track/fire-control attention, launch/support warning, and valid active radar seeker warning.
- **MUST:** Bearing may begin coarse and refine while valid observation persists.
- **MUST:** RWR silence alone does not prove missile defeat.
- **MUST:** `MissileThreatState` distinguishes at least launch/emitter indication, active seeker, indication lost, still-dangerous state, and confirmed-defeat confidence.
- **MUST:** An active radar missile seeker may produce an RWR active-seeker indication when geometry/sensitivity allows.
- **MUST:** A passive IR seeker remains electromagnetically silent.

### 10.6 Infrared sensing

- **MUST:** The current F-65A has **no dedicated IR missile-approach-warning system**.
- **MUST:** The player's heater seeker tone represents the player's own IR seeker only; it is not an incoming-missile warning.
- **MUST:** IR seeker acquisition depends on legal FOV, range, target aspect, aggregate actual engine-emission state, target IR profile, flare competition, and deterministic retention logic.
- **MUST:** Target IR signature is weakest/blind near the nose and strongest toward the tail according to the Phase 3 tables.
- **MUST:** There is no probability-only flare-success roll.

### 10.7 Radar-detail gates

- **TARGET:** Radar/tactical-display data rebuilding remains approximately 10 Hz where appropriate, while launch/active-seeker/defeat/critical-warning transitions are allowed to publish through the protected presentation path as soon as legally available. Exact display cadence remains measured.
- **TBD:** Detection range/aspect tables, scan schedules including 2/4/8-bar behavior, beamwidths, PRF/clutter/notch thresholds, coast/reacquisition, jamming susceptibility, link range/latency/quantization, association gates, IFF timing, and exact track scoring close in Phase 3.

---

## 11. Fire control and weapons

### 11.1 Standard loadout

The standard F-65A combat load is:

- six long-range active-radar missiles;
- two medium-range active-radar missiles;
- two passive-IR heaters;
- 675 cannon rounds.

### 11.2 Engagement presentation

- **MUST:** The player can see which priority target is being supported by the shooter.
- **MUST:** Fire-control presentation identifies a launch-acceptable region and a predicted autonomous-seeker/activation region when applicable.
- **MUST:** Inside the launch-acceptable region, the current design presents an intercept-effectiveness estimate from `1` through `9` in approximate ten-percent bands.
- **MUST:** This estimate is a deterministic tactical estimate based on legal track/weapon state; it is not the hidden hit-resolution probability or a kill roll.
- **MUST:** The RIO announces selected weapon, launch-zone quality, support state, and recommended release when callout priority permits.
- **MEASURED:** Exact line geometry, threshold marks, label positions, flashing, text density, and symbol treatment close through Graphics/Phase-3 human readability evidence.

### 11.3 Player release authority and ROE

- **MUST:** There is no generic tactical launch inhibit.
- **MUST:** With weapons armed, the player may release a poor, unsupported, unidentified, friendly, neutral, or otherwise unauthorized shot if the physical station/release path permits it.
- **MUST:** Lack of target, lock, support, or acceptable intercept does not by itself prevent a selected missile from leaving the rail.
- **MUST:** An empty station, damaged/unavailable mechanism, invalid lifecycle state, or true capacity/lifecycle failure may physically reject release.
- **MUST:** Unauthorized release resolves physically and then produces the appropriate ROE/mission/campaign consequence.

### 11.4 Radar missiles and support

- **MUST:** Current long- and medium-range radar missiles are active-radar missiles with supported midcourse guidance before autonomous seeker operation. They are not modeled as semi-active-homing weapons.
- **TARGET:** The medium-range radar-missile family transitions to autonomous seeker operation earlier and normally requires a shorter support commitment than the long-range family; exact activation/support schedules remain Phase 3 data.
- **MUST:** Weapon Support Datalink is a dedicated shooter/fire-control-to-missile path and is separate from MEGA LINK / RED LINK.
- **MUST:** Support updates derive from a valid committed local fire-control/support track; offboard-only tactical-link information cannot substitute for support.
- **MUST:** A temporary legal support interruption may enter bounded holdover using the last legitimate estimate.
- **TARGET:** Current support-holdover timeout is approximately two seconds before committed support loss; exact value remains Phase 3 gated.
- **MUST:** Valid support restored before timeout may restore supported midcourse behavior.
- **MUST:** After a radar-missile launch, the RIO maintains required support when possible and may advance weapon/target recommendation toward the next suitable unfired priority track without abandoning the supported missile.
- **MUST:** Defensive-jammer blanking of the supporting organic radar and destruction/unavailability of the support subsystem are hard support invalidations.
- **MUST:** Before autonomous seeker activation, committed support loss irrecoverably defeats the current simplified radar missile.
- **MUST:** After autonomous activation, launching-radar field of regard and Weapon Support Datalink are no longer required.
- **MUST:** An active seeker can search, acquire, lose, and reacquire according to the detailed deterministic seeker model.

### 11.5 Passive-IR heaters

- **MUST:** Heaters are passive and create no radar emitter.
- **MUST:** The HUD provides heater acquisition/target cueing and the Audio system provides the player's own seeker acquisition tone state.
- **MUST:** Heater acquisition/retention is physical/deterministic and may be defeated by legal geometry and flare competition.
- **MUST:** An AI aircraft without a modeled IR-warning source cannot react to a heater merely because the engine knows the missile exists.

### 11.6 Missile motion, fuze, and damage

- **MUST:** Guided missiles use physical deterministic 3DOF motion on the 100 Hz authoritative timeline.
- **MUST:** Missile flight includes mass, thrust/burn, gravity, atmosphere, drag, maneuver-energy loss, guidance demand, and valid seeker/support state.
- **MUST:** Long-range missiles use deterministic energy-seeking loft behavior according to Phase 3 data.
- **MUST:** Launch-aircraft altitude, speed, pitch, and geometry can improve or degrade weapon reach without replacing missile guidance.
- **MUST:** Proximity fuze detonation requires its legal seeker/arming/closure/miss-distance conditions.
- **MUST:** Damage depends on physical miss geometry/warhead/fragment/component interaction rather than generic hit-point subtraction.
- **MUST:** Mutual kill is a valid physical outcome when both weapon chains legally complete.
- **MUST:** Current missile presentation uses yellow for supported/in-flight unresolved state, green for autonomous/active state, and red for irrecoverably defeated or physically unable-to-intercept state, with accessible non-color redundancy where required.
- **MUST:** Missile position markers use actual simulated position or a sensor-valid deterministic estimate rather than decorative constant-speed animation.

### 11.7 Cannon and current-scope surface attack

- **MUST:** Cannon sight computes lead from the applicable physical ownship/target/projectile model.
- **MUST:** Cannon rounds use grouped physical projectile behavior rather than one decorative hit ray.
- **MUST:** A gun-capable aircraft may own at most four live projectile groups; further shot requests follow the fixed pool/lifecycle rejection rule and do not consume ammunition.
- **MUST:** Valid live radar/SAM sites and designated small-vessel entities may be disabled by computed cannon intersection according to Phase 3 rules.
- **MUST:** For the current simplified surface-site model, one valid computed burst intersection is sufficient to disable a current-scope site unless a later approved damage revision replaces that simplification.
- **MUST:** Cannon fire cannot damage static scenery.
- **MUST:** Player impacts on the carrier may produce collision/effect/mission consequence but cannot sink/destroy the carrier in current scope.

- **TBD:** Missile, seeker, support, fuze, warhead, cannon, dispersion, drag, grouped-shot, and surface-hit tables close in Phase 3.

---

## 12. Defensive combat, countermeasures, jamming, and threat response

### 12.1 Defensive geometry

- **MUST:** Beaming and notching work through actual geometry, radial velocity, clutter/Doppler rejection, field of regard, dwell, and sensor characteristics rather than named magic bonuses.
- **MUST:** Weaving changes geometry and track-quality inputs but receives no arbitrary deception modifier.
- **MUST:** Terrain masking uses authoritative world geometry, not whatever simplified terrain LOD happens to be drawn.
- **MUST:** Lower/denser air can increase missile drag while terrain/clutter geometry may also change defense effectiveness; neither guarantees survival.

### 12.2 Chaff and flare maneuver qualification

Chaff and flare can be released whenever the request is otherwise legal, but the approved current effectiveness rule is:

> the aircraft must achieve at least **+3.0 G actual positive normal load** during the approved release qualification window for the decoy to become an effective seeker-seduction candidate.

- **MUST:** Commanded stick/G is not sufficient; actual achieved positive normal load is used.
- **MUST:** Negative 3 G does not qualify.
- **MUST:** A non-qualified release still consumes inventory and creates/presents the decoy entity, but its seeker-seduction contribution is ineffective.
- **MUST:** No aircraft may own more than six live chaff/flare entities at once. A dispense request while already at six live decoys is rejected without consuming inventory, and nominal RIO defensive programs are authored to avoid that rejection.
- **MUST:** Pulling G does not magically reduce the aircraft's base RCS or IR signature. It qualifies decoy separation/effectiveness only.
- **MUST:** Flare competes with the aircraft inside a passive-IR seeker's legal region using deterministic geometry/signature/age/qualification scoring.
- **MUST:** Chaff competes with radar returns using deterministic gate geometry, Doppler compatibility, clutter/notch condition, aircraft signature/aspect, age/decay, and qualification.
- **MUST:** Chaff does not create a persistent fake tactical track in the current scope.
- **TBD:** Qualification window, filtering, decoy signatures, lifetimes, switch margins, retention dwell, and scoring close in Phase 3.

### 12.3 RIO defensive assistance

- **MUST:** The RIO may provide threat direction, defensive heading/notch guidance, descent recommendation, roll-out cue, out/recommit cue, and confidence-qualified threat outcome.
- **MUST:** The RIO says an equivalent of **indication lost** when sensing disappears but physical defeat is uncertain.
- **MUST:** The RIO says an equivalent of **missile defeated** only when the legal threat-state logic supports confirmed defeat.
- **MUST:** The RIO automatically manages chaff, flares, and the defensive jammer according to legal threat knowledge, deterministic doctrine, inventory, and the jammer tradeoff.
- **MUST:** Baseline F-65A inventory is 60 chaff and 30 flares.
- **MUST:** The jammer has no separate heat/charge consumable in the current design; its gameplay cost is the radar/support/MEGA LINK tradeoff plus Phase 3 susceptibility/effectiveness.
- **MUST:** When the RIO activates or deactivates the defensive jammer, the player receives an immediate intelligible RIO/text status cue. Jammer-on messaging must make clear that ownship organic radar is blanked and MEGA LINK transmit/receive is denied; critical information must remain understandable if PCM speech is unavailable or preempted.

---

## 13. Fuel, Joker, Bingo, and recovery advisories

- **MUST:** Fuel burns using authoritative engine state and real simulation time.
- **MUST:** Dynamic return-fuel calculation considers fuel remaining, selected recovery destination, moving-carrier position, wind, altitude, configuration, damage drag, expected cruise profile, and recovery reserve.
- **MUST:** Recovery reserve covers one carrier bolter plus another approach or one airfield go-around.
- **MUST:** Joker is an advisory margin above Bingo marking the end of discretionary tactical time.
- **TARGET:** Joker includes approximately ten minutes of expected tactical fuel above the dynamic Bingo requirement.
- **MUST:** Bingo calls for immediate return and produces recovery heading, target altitude, and target KIAS guidance.
- **MUST:** Bingo may select/advise the recovery waypoint but does not take primary flight control from the player.
- **MUST:** Total fuel remains directly visible; computed Joker/Bingo reserve quantities may remain hidden while the RIO communicates the consequence and recommended action.
- **MUST:** Flight-safety and missile-threat calls preempt Joker/Bingo speech while the advisory remains displayed/repeated through the normal priority system.
- **TBD:** Fuel-flow, cruise profile, damage-drag allowance, bolter reserve, Joker margin, and recommendation quantization close through Phase 2/4 evidence.

---

## 14. RIO, wingman, AIC, friendly AI, hostile AI, and doctrine

### 14.1 Player-control boundary

- **MUST:** The player aircraft remains under direct human control.
- **MUST:** The AI RIO is workload assistance, not a hidden player-aircraft autopilot.
- **MUST:** The RIO may manage radar/sensor workload, target priority, weapon recommendation/support, countermeasures, jammer, fuel advisories, startup guidance, navigation information, and defensive coaching where authorized.
- **MUST:** RIO assistance cannot directly edit player position, velocity, G, control surfaces, damage, sensor truth, weapon outcome, or mission truth.
- **MUST:** ADLC and autothrottle are explicit aircraft systems under the player-facing control contract, not secret RIO flight control.

### 14.2 Legal AI knowledge

- **MUST:** Every AI-controlled entity uses only legal information available to its side, platform, own systems, mission assignment, and modeled sensors/links.
- **MUST:** Blue AI uses its MEGA-domain knowledge; Red AI uses its RED-domain knowledge.
- **MUST:** AI never reads global truth simply because the engine contains it.
- **MUST:** Offboard information may improve tactical awareness but cannot become hidden local fire-control quality.
- **MUST:** Team/formation coordination does not become a hidden sensor network.
- **MUST:** AI does not know unobserved hostile fuel, mass, configuration, weapon state, or exact target truth.
- **MUST:** AI without a modeled IR-warning source cannot defend against a hidden incoming IR missile merely because the weapon exists in engine state.

### 14.3 AI behavioral hierarchy

The visible behavior of non-player AI derives from the approved hierarchical doctrine model:

```text
HARD SAFETY / REFLEX
    -> MISSION
    -> FORMATION / TEAM
    -> OPERATIONAL / MOBILITY
    -> TACTICAL PHASE when applicable
    -> MANEUVER / GUIDANCE
    -> CONTROL / INTENT OUTPUT
```

- **MUST:** Flight/surface safety has highest behavioral precedence.
- **MUST:** Mission and ROE define the outer behavioral envelope; AI does not invent new strategic objectives.
- **MUST:** Formation/team behavior coordinates lead/support/sort/rejoin roles without creating telepathic awareness.
- **MUST:** Tactical defense may preempt mission/formation/tactical maneuver behavior but cannot preempt a higher HARD SAFETY recovery requirement.
- **MUST:** AI commands physical systems through the same owning aircraft/system/weapon/sensor interfaces appropriate to that entity class.

### 14.4 Wingman

- **MUST:** Player wingman commands are intent-level: Engage, Cover, Rejoin, Return.
- **MUST:** The wingman independently chooses legal path, target, weapon, formation action, and defense consistent with mission/ROE/doctrine.
- **MUST:** The wingman remains subject to the same physical aircraft, sensors, weapons, damage, fuel, and legal-information rules as other combat aircraft.
- **MUST:** Friendly wingman behavior does not become easier under hostile-only Novice mode.

### 14.5 AIC

- **MUST:** When instantiated, AIC is a physical aircraft consuming one aircraft-pool slot and operating under its mission-authored physics class.
- **MUST:** AIC sensor/track knowledge comes through legal Blue/MEGA information rather than omniscient truth.
- **MUST:** AIC can provide BRAA/picture calls derived from its legal sensor/fused picture.
- **MUST:** BRAA includes bearing from the player, range in nmi, altitude, aspect/flow, identity when known, and group strength where data supports it.
- **MUST:** Route-bound/protected AIC may be KINEMATIC; an AIC that must maneuver defensively or participate as a combat actor is SIX_DOF and must be authored/proved accordingly.

### 14.6 Hostile airborne AI

- **MUST:** Hostile aircraft use the same physical/sensor/weapon causality rules as friendly aircraft.
- **MUST:** BVR behavior may progress through authored/doctrinal phases such as transit, sanitize, intercept, sort, commit, launch, support, assess, second shot/recommit, skate/abort, merge, BFM, separate, and rejoin.
- **MUST:** Defensive behavior responds only to legal threat cues and may use maneuver, chaff/flare, jammer, abort, drag, notch, terrain, and team support according to doctrine.
- **MUST:** WVR/BFM selection uses bounded relational fight geometry, energy estimates, aircraft performance-class assumptions, and doctrinal alternatives rather than global-truth optimization.
- **MUST:** AI never integrates a secret perfect missile trajectory as tactical omniscience; it uses bounded legal weapon-employment estimates.

### 14.7 Mobility and procedures

- **MUST:** Non-player aircraft can perform authored parking-to-parking procedural behavior including startup-ready states, taxi, takeoff/launch, route following, formation, combat interruption, recovery, landing, rollout, and parking when a mission requires those operations.
- **MUST:** AI navigation uses authored/precompiled route/procedure information and bounded guidance, not general runtime A*, recursive planning, neural inference, GOAP, or unrestricted behavior-tree expansion.
- **MUST:** A tactical interruption may suspend an authored route and later resume/rejoin it deterministically when legal.
- **MUST:** AI does not teleport between procedural states merely because it is off-camera.

### 14.8 Surface and IADS AI

- **MUST:** Fixed/mobile SAMs, ships, and applicable ground vehicles use legal sensors, authored mission goals, ROE, doctrine, and bounded mobility.
- **MUST:** Mobile units use precompiled relocation/route options rather than general runtime pathfinding.
- **MUST:** Surface doctrine may control emission, acquisition, engagement, support, relocation, station keeping, and survival behavior according to legal knowledge.
- **MUST:** Surface AI does not use rendered graphics as truth for LOS or targeting.

### 14.9 AI speech and operational text

- **MUST:** RIO/AIC/ATC/wingman text remains authoritative when speech samples are absent, missing, preempted, or dropped.
- **MUST:** A short rolling message log preserves recent operational text.
- **MUST:** Operational callouts are concise; tutorial calls may be more explanatory.
- **MUST:** RIO/AIC/ATC callout priority is flight safety, missile threat, fire/damage, Bingo, tactical, navigation, then flavor; interrupted essential calls repeat or are reissued when the higher-priority channel clears.
- **MUST:** Version 1 does not require a separate callout-verbosity setting.
- **MUST:** Mission-authored proficiency such as Rookie/Average/Veteran/Ace may alter decision latency, maneuver precision, scan discipline, prediction tolerance, shot discipline, support patience, abort willingness, and coordination, but never physics, sensor truth, weapon performance, or hidden-information access.
- **MUST:** Faction doctrine may alter aggression, emission-control preference, support obligations, tactical conservatism, and coordination behavior; faction is doctrine, not a source of hidden information or personality magic.
- **TBD:** Exact phrase templates, callout delays, repetitions, doctrine weights, skill thresholds, maneuver scoring, and tactical service cadences close in Phase 4.


### 14.10 AI decision cadence and held intent

- **MUST:** AI-controlled aircraft and vehicles continue physical motion every authoritative 100 Hz tick even when tactical decision logic is not due.
- **MUST:** Stage-16 AI/RIO decision services may execute deterministic reflex, doctrine, navigation, or slower reassessment work at lower approved cadences.
- **MUST:** Between decision updates, the owning controller continues following the last legal held intent until it is completed, replaced, cancelled, invalidated, or overridden by HARD SAFETY.
- **MUST:** A new Stage-16 intent cannot take physical effect earlier than the following simulation tick.
- **MUST:** AI decision scheduling does not create a hidden second simulation clock.
- **TBD:** Exact per-service AI cadences and held-intent validity details close in Phase 4 and 65Aero Runtime schemas.

---

## 15. Carrier, deck, launch, recovery, and airfield operations

### 15.1 Carrier deck and launch

- **MUST:** Carrier-deck taxi uses guided lanes/routes while the player retains throttle, steering, and brakes.
- **MUST:** Catapult positioning may assist final alignment but the player performs takeoff checks, sets launch power, and gives launch consent.
- **MUST:** Catapult launch applies physical acceleration and hands the aircraft continuously to its flight model; the airplane is not teleported airborne.
- **MUST:** Tailhook state is physical and may be damaged/unavailable.
- **MEASURED:** Exact deck-lane graphics, director cues, final-alignment assistance, hookup presentation, and control prompts close through Graphics/Input evidence.
- **TBD:** Catapult acceleration profile, weight limits, geometry tolerance, and wind correction close in Phase 2 carrier tests.

### 15.2 Carrier recovery

- **MUST:** Normal carrier recovery uses a simplified Case I pattern with optional training vectors toward final.
- **MUST:** Physical IFLOLS and HUD recovery cues derive from the same authoritative recovery geometry.
- **MUST:** The carrier uses three arresting wires with the two-wire as the ideal target.
- **MUST:** Wire capture depends on actual hook position, hook/wire geometry, touchdown/contact state, deck-relative motion, and legal carrier-local contact.
- **MUST:** Missing every valid wire produces a flyable bolter when aircraft state permits.
- **MUST:** Arrestment applies real deceleration and may damage the aircraft when limits are exceeded.
- **TARGET:** Nominal carrier glideslope is approximately 3.5 degrees.
- **TARGET:** Safe carrier touchdown extends through approximately 14 ft/s sink rate subject to Phase 2 evidence.
- **MUST:** LSO grading reports glideslope, lineup, AoA, sink rate, major corrections, bolter/wire, and overall grade.
- **MUST:** Any survivable valid arrestment may complete the sortie even with a poor grade unless the mission defines an additional requirement.
- **MUST:** World/HUD registration must be good enough that the pitch ladder, flight-path reference, IFLOLS/recovery geometry, and deck presentation do not visibly slide apart on an intentionally stale completed world buffer.

### 15.3 ADLC

- **MUST:** ADLC is an approach-control overlay, not a separate fundamental flight law.
- **MUST:** ADLC may engage when airborne with gear down and its required FCS/system capabilities are available.
- **MUST:** ADLC commands on-speed AoA and its own approach-throttle behavior while allowing player flight-path-angle input; lateral control remains with the underlying FCS mode/status.
- **MUST:** Selecting `AUG_OFF` while ADLC is engaged first disengages ADLC and then transfers to direct control.
- **MUST:** Loss of required augmentation/system capability degrades or disengages ADLC.
- **MUST:** Engagement/disengagement never snaps attitude, speed, AoA, control surface, position, G, or trim to a target.
- **MUST:** ADLC works for carrier and land-airfield approaches when prerequisites are satisfied.
- **TARGET:** Full-flap ADLC captures approximately 8 units AoA and 145-155 KIAS across normal recovery weights.
- **TARGET:** Fore/aft approach input changes commanded flight-path angle in approximately 0.25-degree increments over the validated range.
- **TBD:** ADLC gains, speed schedule, filtering, degraded behavior, capture logic, and exact command increments close in Phase 2.

### 15.4 Airfields

- **MUST:** Airfield landing may use conventional control or ADLC.
- **MUST:** Airfield rollout uses simplified directional/deceleration behavior rather than full tire/anti-skid/brake-temperature/hydroplaning simulation.
- **MUST:** Runway departure, terrain impact, gear collapse, and collision remain possible.
- **TBD:** Runway friction, brake effectiveness, steering gain, excursion bounds, and landing-success thresholds close in Phase 2.

### 15.5 AI launch/recovery coordination

- **MUST:** AI aircraft that are authored to use airfields/carriers follow bounded procedural routes, facility-clearance state, and physical launch/recovery paths.
- **MUST:** Facility coordination prevents AI from treating runways, catapults, or recovery slots as unlimited abstract resources.
- **MUST:** AI may hold, wave off, go around, or resume a route according to safety/mission/doctrine rather than teleporting through occupied facilities.
- **TBD:** Exact facility capacities, clearances, timing, taxi/deck routes, and AI recovery tolerances close through Phase 4/mission authoring and Runtime schemas.

---

## 16. Audio, warnings, speech, and music as gameplay presentation

### 16.1 Audio role

- **MUST:** Audio is a protected presentation/information channel, not decorative background only.
- **MUST:** The player can infer meaningful engine, energy, aerodynamic, system, threat, weapon, carrier, RIO/AIC/ATC, and warning state by ear.
- **MUST:** Audio playback never changes simulation, AI, sensing, weapon, damage, mission, RNG, or checksum state.

### 16.2 Flight and aircraft sound

- **MUST:** Engine sound responds to actual engine operating state rather than raw throttle input, including spool lag, military/afterburner character, engine-out, and asymmetric engine state.
- **MUST:** Wind/aerodynamic sound responds to legal flight state such as airspeed, configuration, AoA/buffet, sideslip, and view mix as defined by the Audio white paper.
- **MUST:** Stall/buffet audio reflects actual model state and does not predict/invent stall independently.

### 16.3 Warning priority

The player-facing priority principle is:

1. P0 critical warning - missile warning, fire, critical engine/FCS, stall/ground-impact;
2. P1 other immediate aircraft-safety caution;
3. P2 critical RIO defensive/Bingo/recovery information;
4. P3 ordinary RIO/ATC/AIC/mission speech;
5. P4 weapon transients, impacts, ambience, spectacle.

- **MUST:** P0/P1 safety information may interrupt speech, effects, and music.
- **MUST:** Music continuity never delays a critical warning.
- **MUST:** Every essential spoken call retains text and/or protected tone/visual fallback.
- **MUST:** The own-heater acquisition tone cannot be confused architecturally with an incoming IR warning because no IR MAWS exists.

### 16.4 Music

- **MUST:** Retro synthwave/SID identity is a core product characteristic.
- **MUST:** Music may change/duck/reduce voices by presentation state and contention without changing gameplay.
- **MUST:** The minimum recognizable music identity remains percussion, bass/rhythm, and lead when resource contention requires reduction.
- **MUST:** The soundtrack baseline includes at least menu/briefing, sortie start/high-energy, cruise/nostalgic, threat/dark tactical, carrier approach/recovery, and victory/debrief roles.
- **TARGET:** Musical transitions occur at musically meaningful boundaries when possible.

### 16.5 Speech

- **MUST:** Speech uses short bounded reusable phrases; unrestricted recorded dialogue is not assumed.
- **MUST:** Speech may be interrupted by critical warnings.
- **MUST:** Corresponding text remains available if a phrase never starts, is missing, is preempted, or is dropped.
- **MEASURED:** Exact PCM vocabulary, cache, sample format, warning latency, and simultaneous voice/effect limits close through R0-D/E/F and Audio human review.

---

## 17. Missions, tutorials, ROE, campaign, and debrief

### 17.1 Mission philosophy

- **MUST:** Missions are authored, bounded scenarios with explicit objectives, ROE, routes, facilities, recovery destinations, AI roles/doctrine handles, and legal content.
- **MUST:** Missions may expose physical consequences that remain possible even when they violate ROE or cause failure.
- **MUST:** AI follows mission goals and ROE rather than inventing strategic objectives.
- **MUST:** The player is not given a general-purpose runtime mission editor.

### 17.2 Operation 1 - fleet-replacement check ride

- **MUST:** The first offered campaign sortie is a skippable land-based fleet-replacement check ride.
- **MUST:** It teaches cold start, taxi, takeoff, navigation, radar/weapon employment, missile defense, return navigation, and airfield landing.
- **MUST:** The attack segment uses a cooperative drone.
- **MUST:** The defense segment uses a telemetry training missile that exercises the real seeker/kinematic/RWR/HUD/RIO logic while a training hit records lesson failure without killing the campaign pilot.
- **MUST:** Instruction remains real-time. The RIO may repeat/rephrase missed actions and objectives may wait where safely possible.
- **MUST:** Major lesson failure may offer a segment restart by ending the current run and starting a deterministic replacement run from the authored lesson state.

### 17.3 Operation 2 - introductory carrier CAP

- **MUST:** The second opening campaign sortie begins cold on the carrier and teaches startup, guided deck taxi, catapult launch, CAP, ROE restraint, simplified Case I recovery, ADLC, and arrestment.
- **MUST:** Hostile contacts may approach/maneuver while remaining outside weapons-release authority and may withdraw without requiring engagement.
- **MUST:** Weapons remain physically usable. Unauthorized fire resolves physically and fails the mission under ROE.

### 17.4 Technical Combat Slice and Midnight Spear

- **MUST:** The **Technical Combat Slice** is a non-narrative integrated combat proof and is not the same artifact as Midnight Spear or the release MVP.
- **MUST:** **Midnight Spear** begins only from a separately approved mission manifest.
- **MUST:** Neither artifact authorizes AI generation of missing campaign narrative or content.

### 17.5 Campaign progression

- **MUST:** The campaign contains ten operations and two endings.
- **MUST:** Operations may define success, partial-success, and failure outcomes that can all advance campaign state according to authored rules.
- **MUST:** Ending outcome depends on strategic objectives and player conduct including ROE, rather than one final menu choice or raw score alone.
- **MUST:** Aircraft damage resets before the next mission through repair/replacement logic while debrief/narrative retain the result of the previous sortie.
- **MUST:** Death, capture, aircraft loss, or ejection does not delete a save; the player may retry or accept an authored failure outcome when permitted.
- **MUST:** Simplified ejection survival depends on altitude, attitude, speed, and location and ends the sortie.
- **TBD:** Operations 3-10, branch variables, ending predicates, scoring bands, dialogue, mission geometry, and remaining campaign narrative are Phase 4-5 authored content.

### 17.6 Debrief

- **MUST:** Debrief reports objective outcome, ROE, weapon employment, survival/ejection, fuel, wingman state, damage, landing grade, and a compact event timeline.
- **MUST:** Debrief uses authoritative mission/simulation state rather than presentation-only effects.
- **TARGET:** Debrief gives enough explanation for the player to understand why a shot, warning, landing, mission, or ROE result occurred without exposing hidden enemy truth.

---

## 18. Presentation integrity, accessibility, and information redundancy

- **MUST:** Critical identity is never color-only. Shape, fill, outline, text, luminance, or tone duplicates essential meaning.
- **MUST:** Day, dusk, and night presets preserve HUD, target, warning, and critical aircraft-status readability.
- **MUST:** Positive-G desaturation preserves essential HUD/warning identity.
- **MUST:** Incoming missiles do not need to be visible as world polygons for their physical state to be valid; legal RWR/HUD/RIO/sensor information remains authoritative.
- **MUST:** Presentation effects, music, speech, chase view, map rotation, LOD, dropped optional effects, and unfinished world construction cannot alter sensing, AI, weapons, collision, damage, objectives, scoring, or checksums.
- **MUST:** Missing optional audio/graphics resources degrade presentation gracefully and do not stall simulation.
- **MUST:** Text remains a complete information channel for essential RIO/AIC/ATC speech.
- **MEASURED:** Final symbol size, font density, palette shades, viewport layout, world LOD, audio voice density, input dead zones, and detailed readability thresholds close through R0-D/E/F and human acceptance.

---

## 19. Logical player-facing state contracts

This section defines logical gameplay meaning only. Exact generated binary layouts, widths, packing, memory placement, update masks, and ownership structures belong to 65Aero Runtime v1 and generated schemas.

### 19.1 Flight/control states

- `ControlContext`: Deck / TFL / Normal Flight / Combat.
- `FCSMode`: AUGMENTED / AUG_OFF.
- `FCSStatus`: NORMAL / DEGRADED / DIRECT_ONLY, plus detailed capability indicators as required.
- `AutothrottleState`: enough state to distinguish off/capture/holding/saturated/overridden/failure behavior.
- `ADLCState`: enough state to distinguish off/capture/track/degraded/failed behavior and the limiting reason presented to the player.

### 19.2 Sensor/track/threat states

- `RadarTrackSource`: organic / offboard / fused.
- `TrackQuality`: player-facing detection/firm/weapon-quality/coast/support-lost/drop meaning mapped from the detailed RadarTrack lifecycle/quality model.
- `IdentificationState`: unknown / friendly / neutral / hostile plus legal authority/evidence.
- `MissileThreatState`: launch/emitter indication / active seeker / indication lost / still dangerous / confirmed defeat confidence.

### 19.3 Weapon and advisory states

- `WeaponGuidanceState`: enough player-facing state to distinguish rail/released/supported/autonomous-active/tracking/coasting-reacquiring/defeated/detonated/expired.
- `FuelAdvisory`: destination, return requirement, Joker/Bingo state, recommended heading/altitude/KIAS, reserve class, and source time as needed for presentation.
- `RIOCalloutPriority`: must preserve the safety/threat/damage/fuel/tactical/navigation/flavor priority behavior.
- `LandingGrade`: approach deviation, touchdown, wire/bolter, damage, and overall grade.
- `TutorialLessonState`: mission-owned lesson/progress state; retry starts a new run.

### 19.4 Presentation contract

- **MUST:** Player-facing presentation consumes complete legal `PresentationSnapshot` data and the corresponding completed-world registration state where spatial coherence requires it.
- **MUST:** This document does not define the binary `PresentationSnapshot`, `WorldRegistrationRecord`, AI intent records, or sensor handoff records.

---

## 20. Measured and TBD decision register

| ID | Class | Subject | Current gameplay boundary | Closure evidence/gate |
|---|---|---|---|---|
| IN-01 | MEASURED | Exact key/joystick/radial behavior | Preserve every semantic action and unambiguous Fire/Safe behavior | R0-D/E/F input evidence + Runtime v1 |
| DS-01 | MEASURED | Exact cockpit/map/HUD layout | Bubble cockpit, green HUD, grayscale status, fused right display, required symbols | Graphics/Runtime measured-limits + human readability |
| DS-02 | MEASURED | Maximum displayed-world age | Must remain bounded; no millisecond value frozen here | R0-D/E/F + measured-limits revision |
| FL-01 | TBD | Aerodynamic coefficient set and envelope | Must reproduce consequential 6DOF and AUG_OFF flyability | Phase 2 physics oracle + human flight review |
| FL-02 | TBD | AUGMENTED/AUG_OFF gains and degraded mapping | Must satisfy Section Section 7.3-7.6 without hidden altitude hold or hidden direct-mode damping | Phase 2 |
| FL-03 | TBD | ADLC controls | Approx. 8 units, 145-155 KIAS, 3.5-degree carrier target | Phase 2 carrier/flight review |
| EN-01 | TBD | Engine/sweep tables | Must support F-65 performance targets and system behavior | Phase 2 |
| FU-01 | TBD | Fuel/Joker/Bingo tables | Physical burn + dynamic return/reserve logic | Phase 2 / Phase 4 mission trials |
| RD-01 | TBD | Radar/link/track tables | Two isolated domains, legal fusion, realistic scan/clutter/jam behavior | Phase 3 |
| WP-01 | TBD | Radar-missile support/seeker/fuze tables | Supported active-radar model with holdover/hard loss/autonomy | Phase 3 |
| IR-01 | TBD | IR/aspect/flare model | Deterministic signature/aspect/acquisition/retention | Phase 3 |
| CM-01 | TBD | Decoy qualification window/signatures | +3 G actual-positive-load rule is fixed; exact timing/scoring is not | Phase 3 |
| GN-01 | TBD | Cannon tables | Physical lead/grouped fire/current surface rules | Phase 3 |
| CV-01 | TBD | Catapult/wire/hook/LSO tables | Three wires, two-wire target, physical contact and grade | Phase 2 / Phase 4 |
| AI-01 | TBD | Doctrine/state/skill/tactical tuning | Legal bounded controller; Realistic/Novice contract fixed | Phase 4 |
| AU-01 | MEASURED/TBD | Audio latency/content/sample scope | P0/P1 protected, text/tone fallback, SID-first identity | R0-D/E/F + Audio review + Phase 4/5 content |
| MS-01 | TBD | Remaining campaign/Midnight Spear content | Ten operations, two endings, separately approved Midnight Spear manifest | Phase 4-5 |

- **MUST:** Closing a TBD or MEASURED item records the selected value/table/content, evidence identity, tolerance where applicable, and approving revision/manifest.

---

## 21. Gameplay and simulation acceptance

Acceptance combines deterministic technical proof and human playability/quality review. The Runtime/evidence set owns exact instrumentation and measured pass bars; this document owns the player-visible behavior that must be demonstrated.

### 21.1 Determinism and presentation independence

- **MUST:** PAL and NTSC runs produce equivalent authoritative simulation/checksum results for the same deterministic input/replay across cold start, flight, radar, missile combat, countermeasures, damage, carrier recovery, lesson restart, and debrief.
- **MUST:** Camera, map anchor, chase view, audio/music state, dropped presentation effects, world LOD, and unfinished world rendering cannot change authoritative outcomes.
- **MUST:** All live physical entities remain on the one 100 Hz timeline; instrumentation must detect any unauthorized second physical clock.

### 21.2 Ordinary cruise scene

The acceptance corpus includes an ordinary cruise scene that proves:

- stable 6DOF flight;
- protected HUD/cockpit service;
- normal procedural engine/wind audio;
- fused map/navigation presentation;
- no world-render effect on aircraft behavior;
- world presentation capable of the 30 Hz cruise TARGET under the corresponding measured configuration.

### 21.3 Combined fleet-fight scene

The baseline combined-load scene includes:

- nine aircraft using the Section 4.2 default six-SIX_DOF/three-KINEMATIC profile;
- sixteen simultaneously live guided missiles;
- twenty-four gun projectile groups;
- forty-eight chaff/flare entities;
- both MEGA/BLUE and RED semantic-track domains;
- required RIO/AI behavior;
- damage/events;
- protected audio/HUD;
- world rendering and deterministic shedding.

- **MUST:** The scene does not slow the simulation below exact 100 Hz.
- **TARGET:** Outside-world presentation reaches approximately 25 completed frames/s in the accepted configuration.
- **MUST:** Sustained outside-world cadence below 20 Hz is a failure.
- **MUST:** Optional presentation sheds before protected simulation/HUD/warning behavior.

### 21.4 AUG_OFF handling scene

- **MUST:** A healthy F-65A inside the approved unaugmented envelope remains manually flyable in AUG_OFF with no hidden G-command, roll-rate-command, AoA/G limiter, altitude hold, or artificial FCS damping.
- **MUST:** AUGMENTED <-> AUG_OFF transfer is bumpless and does not mutate pilot trim.
- **MUST:** Damage/degraded capability produces the approved FCSStatus behavior rather than hidden restoration of normal control law.
- **MUST:** Final flight feel requires explicit qualified-pilot human acceptance in addition to oracle compliance.

### 21.5 Carrier Case I / recovery-registration scene

- **MUST:** Deck/catapult, carrier-local contact, IFLOLS, HUD recovery cues, ADLC, arrestment, bolter, and LSO grading all operate from the same physical recovery geometry.
- **MUST:** A world-registered pitch ladder/flight-path cue does not visibly slide against a still-displayed completed world buffer.
- **MUST:** A valid bolter remains flyable and a valid arrestment applies physical deceleration.

### 21.6 Warning/audio-contention scene

The acceptance corpus includes simultaneous legal contention among:

- missile/RWR warning;
- stall/critical aircraft warning;
- Bingo/fuel advisory;
- RIO speech;
- ordinary speech;
- music;
- weapon/transient audio.

- **MUST:** P0/P1 information wins over music/spectacle.
- **MUST:** Essential text remains available.
- **MUST:** Missing/preempted PCM does not suppress required warning behavior.
- **MUST:** Audio contention cannot change simulation state.

### 21.7 Sensor/weapon/defense scene

- **MUST:** Test cases cover organic/offboard/fused track behavior, both tactical knowledge domains, ownship jammer MEGA LINK/radar blackout, support holdover/hard loss, active seeker, passive IR seeker, no IR MAWS, notch/clutter geometry, chaff/flare +3 G qualification, RWR indication lost versus confirmed defeat, and mutual-kill timing.
- **MUST:** AI and RIO receive no hidden global truth while exercising the same scenario.

### 21.8 Training and first-time playability

- **TARGET:** A first-time player using provided instruction should be able to complete startup, takeoff, navigation, attack, defense, return, and landing within two attempts under the accepted training configuration. This target freezes as an acceptance requirement only after Operations 1-2 exist and receive human gameplay review.
- **TARGET:** After instruction, a novice should be able to achieve at least three safe carrier arrestments in five attempts while receiving meaningfully different LSO grades. This target freezes as an acceptance requirement only after the carrier-training content exists and receives human gameplay review.
- **MUST:** Operation 2 permits unauthorized fire, resolves the shot physically, and applies deterministic ROE failure.

### 21.9 Save/campaign acceptance

- **MUST:** Three campaign slots round-trip correctly without serializing raw runtime structures.
- **MUST:** Success/partial/failure branch outcomes persist correctly.
- **MUST:** Death/aircraft loss does not erase a campaign save.
- **MUST:** Endings are reached only through the approved authored predicates, not hidden implementation shortcuts.

---

## 22. Version 1 disposition versus Gameplay Draft 0.2

Version 1 is a coordinated rewrite, not a marginal patch.

### 22.1 Flight-control correction

The old paired flight-law terminology is retired. Version 1 uses:

- `FCSMode = AUGMENTED / AUG_OFF`;
- `FCSStatus = NORMAL / DEGRADED / DIRECT_ONLY`;
- ADLC as an approach overlay;
- autothrottle as a separate state;
- a physically flyable unaugmented airframe;
- bumpless transfer without pilot-trim mutation.

No old rate-command "manual" behavior remains as the gameplay definition of AUG_OFF.

### 22.2 Presentation-snapshot correction

Player-facing presentation now consistently uses `PresentationSnapshot` and completed-world registration state. The stale `SimulationSnapshot` wording from Draft 0.2 is retired.

### 22.3 Sensor/track correction

Version 1 adopts:

- 24 semantic tracks per knowledge domain;
- two capacity-isolated domains, MEGA/BLUE and RED;
- four RIO priority tracks as a MEGA subset;
- offboard cueing without offboard-only ownship weapon quality;
- separate tactical link and Weapon Support Datalink;
- defensive-jammer denial of own radar plus MEGA LINK TX/RX;
- persistent track coasting instead of perfect snapback after jammer use.

### 22.4 IR/countermeasure correction

Version 1 adopts:

- simplified deterministic target IR signature from actual engine-emission state and target aspect;
- passive heater seeker behavior;
- no dedicated IR MAWS;
- +3 G actual-positive-load chaff/flare qualification;
- deterministic geometry/signature competition rather than probability-only decoy success.

### 22.5 AI correction

Version 1 adopts:

- Realistic default and Novice hostile-only tactical modifiers;
- legal side-specific knowledge with no global truth;
- hierarchical safety/mission/team/mobility/tactical/guidance behavior;
- intent-level player wingman commands;
- physical AIC behavior;
- bounded procedural taxi/launch/navigation/recovery;
- AI physical consequences through normal owning systems rather than direct state edits.

### 22.6 Graphics and audio correction

Version 1 adopts the player-visible consequences of the current Graphics and Audio white papers:

- cockpit/HUD protected from late world construction;
- complete world frames only;
- 30 Hz cruise TARGET / 25 Hz combat TARGET / 20 Hz failure floor;
- world-age remains measured;
- world-registered HUD coherence;
- hybrid low-poly/impostor presentation at the engineering layer;
- positive-G desaturation with protected readability;
- SID-led procedural aircraft/warning/music identity;
- PCM as bounded speech/high-information transient enhancement;
- P0/P1 warning priority and text/tone fallback.

### 22.7 Capacity and development alignment

Version 1 preserves the sixteen-aircraft hard pool while defining the required nine-aircraft baseline profile as six SIX_DOF plus three KINEMATIC, with a separately proved SIX_DOF-AIC variant when needed.

R0-A/B/C remain closed. New Graphics/Audio/AI measurement work is integrated through R0-D/E/F and then consumed by Phase 1 and later implementation phases according to Main Concept v1.6.

---

## 23. Human-review approval disposition

Gameplay v1 is **FINAL - HUMAN-REVIEWED**. Human review approved the document with a limited correction pass only. The final pass:

- pinned the approved Main Concept v1.6 parent identity;
- made defensive-jammer / organic-radar-blanked / MEGA LINK denied state explicit in the player status presentation and RIO/text cue path;
- converted the pre-content first-time-completion and carrier-trap thresholds in §21.8 from premature MUST requirements to TARGETS pending implementation and human review of the applicable training sorties;
- recorded that Version 1 intentionally uses RIO-default countermeasure control while permitting a future numbered Gameplay revision to add an optional manual countermeasure action.

No other Gameplay v1 behavior was reopened by this approval pass. Detailed cycle/latency tables, generated record layouts, AircraftPhysicsClass byte representation, AI doctrine weights, radar tables, and Operations 3-10 remain outside this document as already assigned.

---

## Appendix A - source corpus for this rewrite

The rewrite was aligned against the current project corpus, using superseded documents only for provenance where current human-reviewed material intentionally replaced them.

### Active master and rewrite target

- `F65_Main_Concept_v1.6_FINAL_HUMAN_REVIEWED.md` - controlling Main Concept.
- Parent SHA-256: `e7d8ed40ce630d82e707e2a9c7f29995fac6f4281849c2c7ef5261d420c2c425`.
- `F-65 Megawing Gameplay and Simulation Requirements Supplement.md` - Draft 0.2 source superseded by this final Version 1.

### Detailed subsystem engineering inputs

- `MEGA65_Flight_Simulation_Physics_6DOF_Atmosphere_White_Paper.pdf` - v3.3 frozen flight-physics/FCS model.
- `F-65_Megawing_Graphics_White_Paper_v2.1.pdf` - graphics architecture/detail baseline for current rewrite.
- `F-65_Megawing_Audio_Sound_Effects_and_Music_Engineering_White_Paper_v1.0_FINAL(1).pdf` - final human-reviewed audio baseline.
- `F-65_Megawing_SensorAndTrackEngine_Engineering_Model_Phase-3_v1.0(1).pdf` - human-reviewed radar/sensor/track baseline and rewrite input.
- `F-65_Megawing_AI_Behavior_and_Decision_Architecture_White_Paper_v1.0(1).pdf` - final human-reviewed AI baseline and rewrite input.

### Supporting current/legacy engineering sources

- `F-65 Engine Runtime and Toolchain Design Supplement Draft 0.2.md` - implementation source to be superseded by 65Aero Runtime v1 after Gameplay approval.
- `F-65 Megawing Revision 1.5.1 - Architecture Invariants.md` - historical parent incorporated/superseded by Main Concept v1.6.
- `F-65_Graphics_Architecture_Decision_Memo_Hybrid_Affine_Sparse-Polygon_World_Renderer_v0.1.md` - durable decisions absorbed into Main Concept/Graphics; historical provenance.
- `F-65_Technical_Alignment_and_Read_First_Supplement_v1.0.md` - retired provenance only.
- `F65_Megawing_Product_Story_Paper.docx` - product-origin/lore framing adopted by Main Concept v1.6.

---

## Appendix B - intentionally deferred from Gameplay v1

### B.1 To 65Aero Runtime v1

The Runtime document owns, among other things:

- exact `InputCommandFrame`, `PresentationSnapshot`, world-registration, AI intent, sensor handoff, command/event, resource, and save record layouts;
- memory placement and subledgers;
- exact `AircraftPhysicsClass` representation and mission-load encoding;
- per-tick/per-stage CPU ledgers and measured latency;
- world-age instrumentation;
- renderer work queues, DMA, platform ABI, audio scheduler internals;
- mission compiler algorithms and capacity witness format;
- exact Stage-16 AI scheduling/held-intent semantics;
- replay/checksum/fault implementation;
- build/toolchain/evidence contracts.

### B.2 To the white papers

- Physics owns equations, coefficient tables, FCS gains, unaugmented envelope, mass/inertia, actuator/hydraulic details, and physics oracle acceptance.
- Graphics owns renderer algorithms, occlusion, LOD hysteresis, world-registration implementation, presentation tiers, and measured graphical limits.
- Audio owns SID/PCM scheduling, synthesis parameters, sample policy, priority implementation, and audio measurement.
- Radar/Sensor owns scan/detection/association/track/seeker/link/countermeasure algorithms and Phase 3 tables.
- AI owns state graphs, doctrine composition, utility weights, maneuver primitives, exact decision cadences, route/facility structures, and Phase 4 tuning.

### B.3 To later human-authored content

- operations 3-10;
- detailed Midnight Spear manifest/content;
- campaign dialogue and ending predicates;
- final music tracks and speech vocabulary;
- detailed mission geometry and faction-specific narrative content beyond the approved product framing.

---

**End of F65 Gameplay and Simulation Supplement v1 - FINAL - HUMAN-REVIEWED**
