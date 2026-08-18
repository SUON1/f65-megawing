# F-65 Megawing — Gameplay and Simulation Requirements Supplement

**Draft:** 0.2  
**Status:** Freeze candidate  
**Parent baseline:** F-65 Megawing Revision 1.4.1  
**Nature of document:** Binding gameplay supplement with measured and modeled tuning gates  
**Architecture effect:** None unless a future numbered architecture revision explicitly says otherwise

---

## 0. Purpose and authority

- **MUST:** Draft 0.2 supersedes Gameplay and Simulation Supplement Draft 0.1; it does not supersede Revision 1.4.1.
- **MUST:** Once approved, this supplement is the binding player-facing requirements baseline for the current F-65 scope.
- **MUST:** The supplement defines observable behavior, deterministic state contracts, mission authoring limits, and acceptance evidence while leaving measured implementation choices to their named gates.
- **MUST:** No gameplay implementation is authorized before the parent baseline's R0-F and measured-limits revision.
- **MUST:** Midnight Spear, the ten-operation campaign, the two endings, the F-65A, its ten missiles, and the parent baseline's content limits remain the current product scope.

---

## 1. Requirement-class legend

Every normative statement in this supplement carries one of four classes.

| Class | Meaning |
|---|---|
| **MUST** | Durable gameplay or simulation contract. Release behavior must satisfy it. |
| **TARGET** | Intended numeric or feel target. It may move inside its stated tuning band when host-oracle, hardware, or qualified playtest evidence requires it. |
| **R0-GATED** | Presentation, binding, layout, cadence, or implementation detail that cannot freeze until the Revision 1.4.1 R0 hardware-measurement gate passes. |
| **TBD** | An unresolved coefficient, table, threshold, or authored-data value with a named validation method and decision gate in §19. |

- **MUST:** Revision 1.4.1 takes precedence if any statement in this supplement is later found to contradict a frozen architecture invariant.
- **MUST:** A contradiction cannot be resolved by implementation discretion; the supplement must be corrected or a numbered architecture revision must authorize the change.
- **MUST:** TARGET, R0-GATED, and TBD material cannot weaken a MUST requirement or any Revision 1.4.1 acceptance gate.

---

## 2. Invariant compliance

### 2.1 Unchanged Revision 1.4.1 contracts

- **MUST:** The simulation clock remains exactly 100 Hz, using the frozen tick order and atomic `SimulationSnapshot` publication.
- **MUST:** All physical aircraft, missiles, countermeasures, projectiles, ships, surface entities, and simulation-relevant effects participate in the single 100 Hz simulation timeline; radar truth and track state update only inside their frozen tick-order phase.
- **MUST:** This supplement introduces no secondary physical-integration clock, variable-duration step, skipped tick, merged tick, or visibility-dependent motion update.
- **MUST:** Scheduled RIO and enemy-AI decisions may execute less frequently only through tick-order step 16; resulting commands apply no earlier than the next tick.
- **MUST:** Any future proposal for multi-rate physical integration requires a numbered architecture revision plus PAL/NTSC checksum, promotion-transition, collision, and replay proofs.
- **MUST:** The Revision 1.4.1 memory map, MAP ownership, base-page rules, DMA rules, far pointers, resource handles, entity handles, pool sizes, lifecycle, arithmetic, RNG streams, coordinate frames, timing ledger, and performance-overrun behavior remain unchanged.
- **MUST:** Static terrain and scenery remain resources, never live gameplay entities.
- **MUST:** Static buildings, trees, bridges, decorative vessels, and other scenery cannot receive damage or be promoted into destructible entities at runtime.
- **MUST:** The palette-role registry remains authoritative. Supported missiles reuse unresolved yellow because their terminal outcome remains unresolved; no new arbitrary palette index is authorized.
- **MUST:** R0 and the Phase 1 integrated-harness gate remain absolute. No requirement in this supplement authorizes gameplay implementation to merge early.

### 2.2 New gameplay concepts contained within existing architecture

- **MUST:** ADLC, autothrottle, Assisted/Manual flight laws, radar-track source, weapon-guidance state, fuel advisories, RIO priorities, landing grades, and tutorial lesson state are logical gameplay contracts implemented inside the existing tick order and snapshot model.
- **MUST:** Tutorial lesson state advances during mission-objective processing at tick-order step 17.
- **MUST:** A tutorial segment retry ends the current run and starts a new deterministic run from an authored lesson-start state. It never rewinds or edits the active simulation clock.
- **MUST:** Physical AIC aircraft consume an aircraft-pool slot only in missions that instantiate them.
- **MUST:** Destructible surface targets must be allocated at mission load from the frozen ship/carrier or surface-radar/SAM pools.

---

## 3. Capacity and concurrency contract

### 3.1 Required combined air-combat load

The required fleet-defense stress case deliberately overlaps missiles, gunfire, and defensive dispensing. Inventory totals are not the same as simultaneously live entities.

| Class | Pool | Frozen capacity | Required live peak | Headroom | Required basis |
|---|---|---:|---:|---:|---|
| MUST | Aircraft | 16 | 9 | 7 | Player, wingman, four hostiles, rescue helicopter, civilian aircraft, physical AIC aircraft |
| MUST | Guided missiles | 32 | 16 | 16 | Eight friendly and eight hostile missiles simultaneously in flight |
| MUST | Ships/carriers | 8 | 1 | 7 | Player recovery carrier in the air-combat peak |
| MUST | Surface radar/SAM | 16 | 0 | 16 | Audited separately for surface scenarios |
| MUST | Gun projectile groups | 32 | 24 | 8 | Up to four live groups for each of six gun-capable combat aircraft |
| MUST | Chaff/flare entities | 64 | 48 | 16 | Up to six live decoy entities for each of eight defensive aircraft; civilian traffic has none |
| MUST | Dynamic mission entities | 32 | 8 | 24 | Authored triggers, training apparatus, or mission-specific dynamic objects |
| MUST | Simulation-relevant effects | 32 | 0 | 32 | No currently required persistent physical-effect entity; see §3.4 |
| MUST | Presentation effects | 64 | 64 | 0 | Optional visual/audio effects may fill the pool and then drop under frozen policy |
| MUST | Radar truth contacts | 32 | 10 | 22 | Nine aircraft plus carrier before surface entities are added |
| MUST | Radar tracks | 24 | 10 | 14 | Required air picture before surface entities are added |
| MUST | RIO priority tracks | 4 | 4 | 0 | Four weapon-priority tracks |
| MUST | Active objectives | 16 | 8 | 8 | Required upper bound for the opening instructional operations |

- **MUST:** The combined-load harness must run nine aircraft, sixteen guided missiles, twenty-four gun groups, forty-eight chaff/flare entities, eight dynamic mission entities, eight active objectives, and sixty-four presentation effects concurrently, not as isolated single-pool tests.
- **MUST:** All aircraft and missile motion in that harness remains on the 100 Hz physical integration path.
- **MUST:** The AIC aircraft accounts for one of the nine aircraft; it is not an uncounted service.
- **MUST:** Chaff and flare inventory may exceed active-entity concurrency. A released cartridge creates at most one live decoy entity, and no aircraft may own more than six live decoy entities at once.
- **MUST:** A dispense request made while an aircraft already owns six live decoy entities is rejected without consuming inventory; required RIO programs must be authored so this rejection is not part of their nominal behavior.
- **MUST:** A gun-capable aircraft may own at most four live projectile groups. Further shot requests follow the frozen gun-pool rejection rule and do not consume ammunition.
- **TARGET:** Countermeasure lifetime and dispense cadence should keep ordinary defensive programs below four live decoy entities per aircraft, preserving the six-entity limit for overlapping emergency programs.

### 3.2 Surface-scenario authoring profile

| Class | Pool | Frozen capacity | Draft 0.2 authoring target | Headroom |
|---|---|---:|---:|---:|
| TARGET | Ships/carriers | 8 | 4 | 4 |
| TARGET | Surface radar/SAM | 16 | 8 | 8 |
| TARGET | Radar truth contacts with the required air picture | 32 | 21 | 11 |
| TARGET | Radar tracks | 24 | 21 | 3 |

- **TARGET:** A current-scope surface scenario should contain no more than one carrier plus three designated small vessels and eight surface radar/SAM entities.
- **MUST:** The frozen pool capacities, rather than the authoring targets, remain the absolute limits.
- **MUST:** A surface entity can be damaged only while it owns a valid live handle from its frozen pool.
- **MUST:** Surface-scenario validation must include all overlapping aircraft, missiles, countermeasures, gun groups, contacts, objectives, and required effects rather than validating the surface pools in isolation.

### 3.3 Mission-compiler proof

- **MUST:** The mission compiler must calculate a conservative maximum-live bound for every frozen pool across every authored phase and every legal overlap of scripted spawns, AI doctrine, player commands, weapon flight time, decoy lifetime, projectile-group lifetime, despawn delay, and required effect lifetime.
- **MUST:** The compiler must hard-reject a mission whose legal execution can exceed any non-droppable frozen pool.
- **MUST:** A mission cannot rely on runtime allocation rejection for a required objective, required defensive action, required weapon event, or tutorial step.
- **MUST:** The compiler must emit a per-pool report containing capacity, predicted peak, peak-producing phase/event, and remaining headroom.
- **MUST:** The compiler must also emit a combined concurrency report identifying which peaks can coexist on the same ticks.
- **MUST:** Runtime high-water instrumentation must verify the compiler bound in Xemu, hardware, replay, and synthetic-load runs.
- **MUST:** A measured runtime peak above the compiler bound is a mission-tool defect and fails validation.

### 3.4 Effect ownership

- **MUST:** A simulation-relevant effect is a live entity only when it persists across ticks and can change physical motion, collision, sensing, damage, mission state, or another deterministic simulation result.
- **MUST:** Current-scope missile blast and fragmentation resolve as same-tick collision/damage events and do not allocate persistent simulation-relevant effects.
- **MUST:** Visible flame, leak spray, smoke trail, explosion flash, sparks, contrail, dust, and water spray are presentation effects unless a later numbered design explicitly grants the rendered effect physical influence. Deterministic component fire or leak progression remains ordinary system/damage state rather than an effect entity.
- **MUST:** Presentation effects cannot affect detection, guidance, damage, AI decisions, scoring, or checksums and follow the frozen drop-and-count overflow rule.
- **MUST:** Any future mission that requires a persistent damaging or sensor-affecting volume must declare its simulation-relevant-effect peak and pass the mission-compiler audit before use.

### 3.5 Radar-track overflow

- **MUST:** RIO priority-track count never exceeds four. Promoting a fifth candidate deterministically demotes the lowest-scoring current priority track before promoting the replacement.
- **MUST:** Score ties resolve by the frozen handle and producer-order rules.
- **MUST:** When the 24-track pool is full, the Revision 1.4.1 rule remains authoritative: evict the lowest-scoring nonpriority coasting track.
- **MUST:** A priority track is never silently evicted by nonpriority track creation.

---

## 4. Product flow, saves, and settings

- **MUST:** The title screen provides Continue, Campaign, Free Flight, and Settings.
- **MUST:** Campaign provides three user-managed save slots.
- **MUST:** Campaign saves occur only outside a live sortie; Draft 0.2 provides no mid-sortie save or restoration.
- **MUST:** Free Flight uses validated presets for location, start state, weather, loadout, and friendly/hostile traffic rather than a general mission editor.
- **MUST:** A complete keyboard-only flight layout exists when no joystick is present.
- **MUST:** A joystick-plus-keyboard layout remains the intended primary experience.
- **MUST:** PAL/NTSC selection is automatically detected and offers a compatibility override without changing simulation results.
- **MUST:** A full pause freezes simulation and offers Resume, Controls, Restart Sortie, Settings, and Exit to Title.
- **MUST:** Time acceleration is not supported.
- **MUST:** Player-facing replay is a debrief timeline, not a free-camera mission replay. Engineering replay records remain unchanged.
- **R0-GATED:** Exact title layout, menu navigation timings, save-slot presentation, and control-reference layout freeze after display/input measurement.

---

## 5. Semantic input and control contexts

### 5.1 Durable actions

- **MUST:** The input layer exposes semantic commands for arm, safe, fire, weapon cycle, autothrottle, autothrottle-speed command, ADLC, flight-law toggle, manual-throttle preset/increment, minimum and maximum afterburner, gear, flaps, hook, brakes, ejection, map mode, radar scale, waypoint advance, RIO target/interrogate, AIC picture, wingman intent, and wing-sweep override/Auto.
- **MUST:** Input bindings generate tick-tagged commands through the existing `InputCommandFrame`; bindings never manipulate simulation state directly.
- **MUST:** Deck, Takeoff-and-Landing, Normal Flight, and Combat remain the four primary one-button contexts.
- **MUST:** Entering Combat changes the joystick action to weapon fire. A separate Safe action returns the button to contextual-menu duty.
- **MUST:** Entering Combat requests autothrottle capture at current KIAS when autothrottle is available; autothrottle failure cannot prevent weapons from arming.
- **MUST:** While autothrottle is engaged, the contextual speed command changes captured KIAS rather than directly commanding throttle angle.
- **MUST:** Weapon selection defaults to the RIO recommendation and supports explicit cycling through long-range radar missile, medium-range radar missile, heater, and gun.
- **MUST:** Countermeasure and defensive-jammer commands default to RIO control; manual decoy binding is not required for Draft 0.2.

### 5.2 Preferred but unfrozen layout

- **TARGET:** Preferred keyboard defaults are `A` for autothrottle/ADLC, `Shift-A` for Assisted/Manual, `W` for weapon cycle, `D` for Safe, `F` for flaps, `G` for gear, `H` for hook, `B` for brakes, `M` for map anchor, `[`/`]` for sweep, and held `Shift-E` for ejection.
- **TARGET:** The preferred normal-flight pie assigns Arm, Autothrottle, RIO Lock/Interrogate, Wingman Commands, AIC Picture, Next Waypoint, and Radar Scale Down/Up to eight directions.
- **TARGET:** The wingman submenu exposes Engage, Cover, Rejoin, and Return intent.
- **R0-GATED:** Exact keys, joystick dwell time, hold-versus-motion arbitration, repeat acceleration, dead zones, ejection confirmation duration, throttle-step size, and pie geometry freeze only after hardware input testing.
- **MUST:** Whatever bindings R0 selects must preserve access to every durable semantic action without an ambiguous fire-versus-mode gesture.

---

## 6. World and environment model

- **MUST:** The world uses the frozen North-East-Down frame, sector representation, aviation units, and carrier-local frame.
- **MUST:** A typical mission uses a finite authored operating region surrounded by valid sparse world coordinates; there is no invisible wall, forced turn, or boundary-triggered failure.
- **TARGET:** The typical authored operating region is 256 × 256 nmi.
- **MUST:** Atmosphere supplies pressure, density, temperature, speed of sound, gravity, and true/indicated-speed conversion to aircraft and missiles through shared deterministic tables.
- **MUST:** Mission weather supplies surface, middle, and high-altitude wind layers with deterministic fixed-point interpolation.
- **MUST:** Mission temperature modifies the reference atmosphere through a deterministic fixed-point profile.
- **MUST:** Clouds are presentation-only in Draft 0.2 and cannot affect sensors, AI, flight, icing, turbulence, or weapons.
- **MUST:** Missions use authored day, dusk, or night lighting presets rather than a continuous sun/time-of-day simulation.
- **MUST:** All live aircraft update physical position and collision state every 100 Hz tick.
- **MUST:** Noncombat aircraft may use a type-specific simplified flight/control model fixed at mission load, but the model cannot change because of distance, visibility, camera, or radar state.
- **MUST:** Rescue, civilian, and AIC aircraft remain real sensor contacts and collision objects.
- **MUST:** Secured deck aircraft inherit the frozen deterministic carrier motion.
- **MUST:** Carrier wave-driven heave, pitch, and roll remain outside scope.

---

## 7. F-65A flight model and handling

### 7.1 Physical model

- **MUST:** The player aircraft and combat aircraft use table-driven six-degree-of-freedom rigid-body dynamics.
- **MUST:** Aerodynamic force and moment depend on Mach, angle of attack, sideslip, configuration, actual control-surface state, wing sweep, damage, atmosphere, and current mass.
- **MUST:** Energy is physical. Turns, climbs, induced drag, configuration drag, damage drag, and low-altitude density can reduce speed even when autothrottle requests maximum permitted power.
- **MUST:** Aircraft mass changes with fuel, missile expenditure, and cannon ammunition.
- **MUST:** The model contains no hidden altitude hold in ordinary Assisted maneuvering.
- **TBD:** Aerodynamic coefficient tables, inertia, reference geometry, stability derivatives, buffet boundaries, departure derivatives, and compressibility corrections freeze through the Phase 2 host-oracle gate.

### 7.2 Assisted flight law

- **MUST:** Assisted longitudinal input commands normal G; Assisted lateral input commands roll rate.
- **MUST:** Neutral longitudinal input returns toward a one-G flight-path attitude without commanding level flight or constant altitude.
- **MUST:** G/AoA protection limits demand according to weight, configuration, damage, hydraulic capability, and aerodynamic authority.
- **MUST:** When energy is insufficient, commanded G becomes unavailable and the aircraft exhibits buffet, controlled mush, sink, and altitude loss rather than receiving artificial thrust or lift.
- **TARGET:** A healthy clean aircraft provides a +9 G / −3 G command envelope.
- **TARGET:** A healthy clean aircraft reaches approximately 180°/second maximum commanded roll rate.
- **TARGET:** Initial aft-stick response adds approximately +0.5 G and progresses smoothly toward the scheduled limit over approximately two seconds.
- **TBD:** Control-law gains, command ramps, rate limits, AoA schedule, anti-windup, and configuration schedules freeze after bit-exact sequences and qualified pilot review.

### 7.3 Manual flight law

- **MUST:** Manual mode commands pitch and roll rates rather than G and roll rate.
- **MUST:** Manual removes G/AoA envelope protection but retains stability damping, hydraulic authority, actuator rates, actual surface state, and damage effects.
- **MUST:** Manual mode permits stalls, wing drop, departure, and structural over-G.
- **MUST:** Over-G and overspeed damage accumulate deterministically from magnitude and exposure time.
- **MUST:** Switching back to Assisted requests best-effort recovery but cannot guarantee recovery without sufficient altitude, energy, hydraulics, control authority, and intact structure.
- **TBD:** Manual-mode rate gains, damping, departure thresholds, structural fatigue curves, and recovery gains freeze in Phase 2.

### 7.4 Performance and weight targets

| Requirement | Class | Target |
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
- **MUST:** True airspeed remains available to the physics model and reference tools.
- **MUST:** External fuel tanks are outside Draft 0.2.
- **TBD:** Exact thrust-to-weight, climb, acceleration, instantaneous/sustained-turn, stall, and drag targets freeze after the coefficient model can be measured as a complete envelope.

### 7.5 Engines, throttle, and wing sweep

- **MUST:** Each engine independently models RPM, spool response, altitude/Mach thrust lapse, fuel feed, military thrust, afterburner thrust, damage, and flameout.
- **MUST:** A viable stopped engine attempts automatic relight when windmill RPM, fuel, electrical state, and damage permit.
- **MUST:** Autothrottle captures current KIAS and modulates only through maximum military power.
- **MUST:** The player must explicitly select minimum or maximum afterburner; an afterburner selection overrides autothrottle until the player recaptures speed.
- **TARGET:** Canonical throttle-angle detents are 90% military, 95% minimum afterburner, and 100% maximum afterburner.
- **MUST:** Wing sweep follows an automatic Mach/flight-condition schedule with manual override and a return-to-Auto action.
- **TBD:** Engine thrust, spool, fuel-flow, relight, and wing-sweep tables freeze through the Phase 2 bit-exact host model.

### 7.6 Gear, flaps, and ADLC

- **MUST:** Flaps cycle Up, Half, and Full. Half is the takeoff setting; Full is the nominal landing setting.
- **MUST:** A flap-overspeed condition produces a caution and commands automatic flap retraction with hysteresis.
- **MUST:** Gear overspeed produces a caution and deterministic damage exposure; it does not automatically retract the gear.
- **MUST:** ADLC may engage whenever the aircraft is airborne with gear down. Missing flap, ADC, FCS, hydraulic, engine, or actuator capability can degrade or defeat capture after engagement.
- **MUST:** ADLC incorporates its own autothrottle law; toggling ADLC off returns to conventional gear-down pitch/throttle control without discontinuously changing aircraft state.
- **MUST:** ADLC commands on-speed AoA and weight/configuration-derived approach speed while allowing the player to command flight-path angle.
- **MUST:** ADLC captures through continuous actuator, aerodynamic, and engine response; engagement never snaps speed, attitude, AoA, or position to a target value.
- **MUST:** ADLC lateral control remains the normal Assisted roll-rate law.
- **MUST:** ADLC works at carrier and land airfields.
- **TARGET:** Full-flap ADLC captures 8 units AoA and approximately 145–155 KIAS across normal recovery weights.
- **TARGET:** Fore/aft commands change flight-path angle in approximately 0.25° increments over approximately +2° through −8°.
- **TARGET:** The nominal carrier glideslope is 3.5°.
- **TBD:** ADLC capture gains, speed schedule, flare/non-flare behavior, command filtering, degraded-state behavior, and increment timing freeze through carrier-approach host sequences and playtest.

---

## 8. Aircraft systems and cold start

- **MUST:** A manual sortie start may begin cold and dark on an airfield or carrier deck.
- **MUST:** A preflight choice offers Manual Cold Start or RIO-Assisted Start when the mission permits either.
- **MUST:** Assisted startup traverses the same electrical, engine, generator, hydraulic, and avionics states as manual startup; it cannot set systems directly to healthy.
- **MUST:** Manual startup exposes stateful semantic actions for Battery, Engine 2 Start, Engine 1 Start, Systems On, Takeoff Checks, Request Taxi, and Request Takeoff/Launch as their prerequisites become meaningful.
- **MUST:** Engine 1 and Engine 2 start commands remain independently selectable even though RIO instruction recommends Engine 2 first.
- **MUST:** Takeoff Checks require Half flaps and a four-quadrant flight-control sweep before the RIO reports the aircraft ready.
- **MUST:** Request Taxi and Request Takeoff/Launch represent authorization and mission progression without replacing player steering, braking, throttle, rotation, or configuration commands.
- **TARGET:** Land takeoff rotation begins near 160 KIAS at normal training weight and varies through the validated weight/configuration schedule.
- **MUST:** Raising gear and flaps after departure transitions the aircraft into Normal Flight control context when no higher-priority condition prevents it.
- **MUST:** Battery power provides limited 24-volt indications and intercom/RIO availability.
- **MUST:** Battery-only presentation keeps the tactical radar unavailable, shows only limited systems/fuel/electrical information, and withholds full HUD flight data until its supplying systems become capable.
- **MUST:** Either engine may start first, but the guided order presents Engine 2 first because Hydraulic System 2 supplies most essential services.
- **MUST:** Engine 1 alone may supply its generator and limited dependent systems but cannot provide Hydraulic 2-dependent capability.
- **TARGET:** An engine generator comes online near 50% RPM, both engines stabilize near 61% idle, the main electrical indication is 480 volts, and a healthy hydraulic system indicates 3,000 psi.
- **MUST:** “Systems On” commands a dependency-driven initialization of ADC, FCS, ADLC, RADAR, WPS, RWR, ECM, OBOGS, communications, and displays.
- **MUST:** Full radar, navigation, HUD, and tactical symbology appears only as the corresponding actual subsystem capabilities become available.
- **MUST:** Healthy-off or initializing systems appear amber, operating systems green, failed systems red, and unavailable/no-data systems gray.
- **MUST:** The compact caution set contains ENG 1/2, GEN 1/2, HYD 1/2, ADC, FCS, ADLC, RADAR, WPS, RWR, ECM, OBOGS, COMMS, fuel, fire, gear, and flaps.
- **MUST:** System health, supply, commanded mode, and actual capability remain distinct. A caution clears only when actual state satisfies its rule.
- **MUST:** Random reliability failures are excluded. Failures arise from damage, misuse, depletion, or authored mission/training events.
- **MUST:** Fuel affects total mass and independent engine feed. Tank-by-tank transfer and center-of-gravity migration are outside Draft 0.2.
- **TBD:** Startup spool duration, initialization duration, caution thresholds, power dependencies, hydraulic authority curves, fuel-flow tables, and automatic-relight envelope freeze through system reference models.

---

## 9. Cockpit displays and HUD

- **MUST:** The left display is one integrated aircraft-status display rather than a player-managed page set.
- **MUST:** It shows aircraft silhouette/status, fuel weight, engine state, electrical state, hydraulic pressure, major cautions, weapons remaining, cannon ammunition, chaff, flares, and damage/failure state.
- **MUST:** The right display is one fused radar/navigation moving map rather than separate radar and navigation pages.
- **MUST:** The fused display is heading-up and shows current heading at the top.
- **MUST:** The fused display supports 20, 40, 80, and 160 nmi selected scales.
- **MUST:** A Map Anchor action toggles between tactical lower-screen ownship placement and centered-ownship overview while preserving terrain, tracks, locks, missile state, waypoints, and weapon information.
- **MUST:** Operational map content includes land/water, coastline, major elevation regions, airfields, carrier, waypoints, and objective markers beneath higher-contrast tactical symbols.
- **MUST:** HUD content changes automatically among takeoff, navigation, combat, defense, and landing priorities.
- **MUST:** Critical warnings can overlay every HUD mode.
- **MUST:** Chase view retains an essential reduced HUD containing flight path, speed, altitude, target/threat, selected weapon, fuel caution, and critical warning information.
- **TARGET:** Tactical tracks refresh visually at approximately 10 Hz; launch, active-seeker, defeat, and critical-warning transitions publish immediately through completed snapshots.
- **R0-GATED:** Exact ownship offset, viewport proportions, moving-map rotation method, symbol size, text density, terrain detail, line style, chase-HUD layout, and display refresh cadence freeze after R0-B.

---

## 10. Radar, identification, and fused tracks

- **MUST:** Organic radar detection depends deterministically on range, target signature/aspect, antenna field, altitude/look-down geometry, land/sea clutter, and jamming.
- **MUST:** Radar field of regard remains the frozen −85° through +85°.
- **MUST:** The RIO owns scan-volume, elevation, search, correlation, interrogation, and priority-track management.
- **MUST:** The RIO maintains no more than four weapon-priority tracks.
- **MUST:** AIC/datalink-only tracks use a different outline treatment from organic tracks; the preferred treatment is dashed offboard versus solid organic.
- **MUST:** Correlated organic/offboard information produces one fused track without hiding its source state.
- **MUST:** Nonpriority tracks enter a bounded coasting state after organic detection loss and visibly indicate stale/extrapolated state before dropping.
- **TARGET:** Nonpriority track-coast duration is approximately five seconds.
- **MUST:** A weapon-support track outside field of regard drops support after a bounded continuous timeout.
- **TARGET:** Weapon-support timeout is approximately two seconds.
- **MUST:** Re-entry before support timeout restores supported tracking according to deterministic track-quality rules.
- **MUST:** Support loss before seeker activation makes the current simplified radar missile irrecoverably defeated; a missile that is already active remains independent of launching-radar field of regard.
- **MUST:** Unknown/unclassified returns use hollow square identity. Classified aircraft use heading-oriented triangles; classified ships use course-oriented rectangles.
- **MUST:** Yellow means unresolved, red positively identified hostile, green friendly, and white neutral.
- **MUST:** Filled contact symbols indicate weapon-quality priority/lock state.
- **MUST:** Aircraft tracks show two-digit altitude in thousands of feet when altitude data is valid.
- **MUST:** A hostile identity requires valid IFF/mission/AIC authority or an overt hostile act defined by mission ROE.
- **MUST:** The RIO automatically interrogates tactically relevant unknowns and accepts an immediate player command to interrogate the selected or nearest suitable unknown.
- **TBD:** Detection-strength tables, RCS/aspect classes, clutter rejection, jamming effects, scan schedule, correlation thresholds, track scoring, coasting uncertainty, and IFF timing freeze through the Phase 3 host oracle.

---

## 11. Fire control and weapons

### 11.1 Engagement presentation

- **MUST:** A line links shooter and weapon-priority target when the shooter supports that target.
- **MUST:** The line shows a launch-acceptable threshold and a predicted seeker-activation threshold.
- **MUST:** Inside the launch-acceptable region, the display presents a `1` through `9` intercept-effectiveness estimate in approximate ten-percent bands.
- **MUST:** The estimate derives from physical launch state, target state, atmosphere, seeker support, target maneuver potential, and countermeasure assumptions; it is not the hit-resolution roll.
- **MUST:** The RIO announces selected weapon, launch-zone quality, support state, and recommended launch when callout priority permits.
- **R0-GATED:** Exact line geometry, threshold marks, numeral placement, flash rate, and target-label layout freeze after display measurement.

### 11.2 Loadout and release

- **MUST:** The standard F-65A load is six long-range active-radar missiles, two medium-range active-radar missiles, two heaters, and 675 cannon rounds.
- **MUST:** Long-range missiles require inertial/datalink support before autonomous seeker activation.
- **MUST:** Medium-range radar missiles require a shorter support interval and activate earlier.
- **MUST:** Heaters use passive seeker acquisition, a HUD acquisition circle, target cue, and authoritative acquisition tone/text state.
- **MUST:** There is no tactical launch inhibit. With weapons armed, the player may release a poor, unsupported, friendly, neutral, or otherwise unauthorized shot.
- **MUST:** An empty station, damaged or unavailable release mechanism, stale handle, or pool exhaustion may reject release under frozen lifecycle rules. Lack of a target, lock, support path, or acceptable intercept does not prevent the selected missile from leaving the rail.
- **MUST:** Unauthorized release resolves physically and produces ROE failure or authored campaign consequence.
- **MUST:** After a radar-missile launch, the RIO retains required support and advances selection to the next suitable unfired priority track.

### 11.3 Missile physics

- **MUST:** Guided missiles integrate at 100 Hz using deterministic 3-DOF point-mass physics.
- **MUST:** Missile motion includes mass, thrust/burn time, gravity, atmosphere, drag, lift/turn demand, guidance demand, and maneuver-energy loss.
- **MUST:** Long-range missiles use deterministic energy-seeking loft guidance based on launch and target state.
- **MUST:** Launch-aircraft altitude, speed, and pitch can improve or degrade the resulting trajectory without replacing missile guidance.
- **MUST:** A proximity fuze detonates only after seeker track, arming time, closure, and miss-distance geometry satisfy its physical rule.
- **MUST:** Missile damage depends on miss distance, aspect, fragment path, warhead effect, and intersected components rather than a generic hit-point subtraction.
- **MUST:** Yellow missile marker means supported/in flight, green autonomous/active, and red irrecoverably defeated or physically unable to intercept.
- **MUST:** Missile markers use actual simulated position or a sensor-valid deterministic estimate, never a decorative constant-speed animation.
- **TBD:** Missile mass, thrust curves, drag tables, maximum lateral acceleration, guidance constants, loft schedule, seeker field, activation schedule, fuze radius, warhead, and signature tables freeze through Phase 3 golden trajectories.

### 11.4 Cannon and surface attack

- **MUST:** The cannon sight computes target lead from ownship/target state, projectile velocity, gravity, and approved short-range drag approximation.
- **MUST:** Cannon rounds use the frozen gun-projectile-group pool and per-shooter concurrency cap in §3.1.
- **MUST:** Entity-based radar/SAM sites and designated small-vessel entities may be disabled by a valid computed cannon burst.
- **MUST:** Draft 0.2 treats one valid burst intersection as sufficient to disable a current-scope surface site; it does not add a detailed ground-component graph.
- **MUST:** Cannon fire cannot damage static scenery.
- **MUST:** Carrier impacts register collision/effect and mission consequence, but player fire cannot destroy or sink the carrier in current scope.
- **TBD:** Cannon rate, dispersion, muzzle velocity, drag approximation, burst grouping, lead filter, and valid-surface-burst volume freeze through Phase 3 host tests.

---

## 12. Defensive combat, RWR, and countermeasures

- **MUST:** The F-65A has no dedicated infrared missile-approach warning system in Draft 0.2.
- **MUST:** RWR detects valid radar search, track, illumination, launch-mode, and active-seeker emissions according to emitter and receiver geometry.
- **MUST:** RWR bearing begins as a coarse sector and refines while observation remains valid.
- **MUST:** RWR silence alone cannot prove missile defeat.
- **MUST:** A notch requires suitable beam geometry, look-down land/sea clutter, Doppler conditions, seeker/radar field of regard, and sufficient dwell.
- **MUST:** Descending into denser air and lower clutter geometry can improve defense while increasing missile drag; neither effect guarantees success.
- **MUST:** The RIO supplies threat direction, notch heading, descent recommendation, roll-out cue, out command, recommit call, and confidence-qualified defeat state.
- **MUST:** The RIO says indication lost when sensing is lost but physical defeat is uncertain; it says missile defeated only after track loss plus adequate dwell or a physically impossible intercept.
- **MUST:** The RIO automatically commands chaff, flares, and defensive jammer according to deterministic doctrine and remaining inventory.
- **MUST:** Baseline F-65A inventory is 60 chaff and 30 flares.
- **MUST:** Countermeasure success uses deterministic seeker-versus-signature scoring from timing, geometry, field of view, and signature competition; no probability-only decoy roll is used.
- **MUST:** Defensive jammer operation blanks organic radar and terminates support for nonautonomous missiles. Offboard/datalink tracks may remain.
- **MUST:** Draft 0.2 adds no jammer heat, charge, or time consumable beyond its radar/support tradeoff.
- **TBD:** RWR sensitivity/bearing refinement, notch windows, clutter scoring, countermeasure signatures/lifetimes, RIO defensive programs, and jammer effectiveness freeze through Phase 3 deterministic scenarios.

---

## 13. Fuel, Joker, and Bingo

- **MUST:** Fuel burns through deterministic fixed-point lb/hour tables using real elapsed simulation time.
- **MUST:** Dynamic return-fuel calculation considers fuel remaining, selected recovery destination, moving-carrier position, wind, altitude, configuration, damage drag, expected cruise profile, and recovery reserve.
- **MUST:** Recovery reserve covers one carrier bolter and another approach or one airfield go-around.
- **MUST:** Joker is an advisory threshold above Bingo that marks the end of discretionary tactical time.
- **TARGET:** Joker includes approximately ten minutes of expected tactical fuel above the dynamic Bingo requirement.
- **MUST:** Bingo requires immediate return and generates recovery heading, target altitude, and target KIAS guidance.
- **MUST:** Bingo selects the recovery waypoint but does not take flight control from the player.
- **MUST:** Total fuel remains visible; computed Joker and Bingo quantities remain hidden and are communicated by the RIO.
- **MUST:** Flight-safety and missile-defense calls preempt Joker/Bingo speech, while the advisory remains displayed and repeats after the higher-priority channel clears.
- **TBD:** Fuel-flow tables, cruise profiles, damage-drag allowance, bolter reserve, Joker margin coefficients, and recommendation quantization freeze through the Phase 2 host oracle and mission-duration playtest.

---

## 14. RIO, wingman, AIC, and enemy AI

- **MUST:** The RIO is a deterministic workload manager for radar, target prioritization, weapon recommendation/support, countermeasures, jammer, fuel advisories, startup guidance, navigation, and defensive coaching.
- **MUST:** RIO and AI decisions use only sensor-valid information available to their side, not hidden player truth.
- **MUST:** Enemy AI uses its radar, RWR, visual detection, datalink, doctrine, and received mission commands without omniscient access.
- **MUST:** Wingman commands express Engage, Cover, Rejoin, and Return intent; the wingman independently chooses path, target, weapon, and defensive action.
- **MUST:** AIC is a physical protected aircraft when instantiated and generates BRAA calls from its sensor/fused track picture.
- **MUST:** BRAA calls include bearing from the player, range in nmi, altitude, aspect/flow, identity when known, and group strength.
- **MUST:** RIO/AIC/ATC text is authoritative when voice samples are absent or preempted.
- **MUST:** A short rolling message log preserves recent operational text.
- **MUST:** Callout priority is flight safety, missile threat, fire/damage, Bingo, tactical, navigation, then flavor. Interrupted essential calls repeat when the channel clears.
- **MUST:** Tutorial callouts are explanatory; operational sorties are concise without a verbosity setting.
- **TBD:** Exact phrase templates, callout delays, repetition cadence, voice-sample set, AI doctrine scores, wingman separation limits, and AIC sensor performance freeze through Phase 4 scenarios.

---

## 15. Carrier and airfield operations

### 15.1 Deck and launch

- **MUST:** Carrier-deck taxi uses guided lanes while the player retains throttle, nosewheel steering, and brakes.
- **MUST:** Catapult positioning may assist final alignment, but the player performs takeoff checks, sets launch power, and gives launch consent.
- **MUST:** Catapult launch produces physical acceleration and hands the aircraft to the flight model without teleporting airborne.
- **MUST:** Tailhook has a dedicated semantic command and simulated deployed, stowed, damaged, and unavailable states.
- **R0-GATED:** Deck-lane graphics, director cues, alignment tolerance, hookup animation, catapult presentation, and exact control prompts freeze after R0 rendering/input measurement.
- **TBD:** Catapult acceleration profile, launch-weight limits, hookup tolerance, and launch wind corrections freeze through carrier host tests.

### 15.2 Recovery

- **MUST:** Normal carrier recovery uses a simplified Case I pattern with optional tutorial vectors to straight-in final.
- **MUST:** A physical IFLOLS and redundant HUD glidepath/lineup cues present the same authoritative recovery errors.
- **MUST:** The carrier uses three arresting wires, with the two-wire as the ideal target.
- **MUST:** Wire capture depends on hook position, hook/wire geometry, touchdown state, deck-relative velocity, and valid carrier-local contact.
- **MUST:** Missing every valid wire produces a flyable bolter when aircraft state permits.
- **MUST:** Arrestment applies physical deceleration and can damage the aircraft when touchdown/arresting limits are exceeded.
- **TARGET:** Nominal glideslope is 3.5° and safe carrier touchdown extends through approximately 14 ft/second sink rate.
- **MUST:** LSO grading reports glideslope, lineup, AoA, sink rate, major corrections, bolter/wire, and overall grade.
- **MUST:** Any survivable valid arrestment may complete the sortie even when the landing grade is poor.
- **R0-GATED:** IFLOLS size, brightness, distance readability, HUD error scale, deck visual detail, and cue update presentation freeze after hardware measurement.
- **TBD:** Wire zones, hook dynamics, capture tolerances, arresting-force curve, structural limits, grade thresholds, and pattern gates freeze through Phase 2 carrier-contact oracles and novice playtest.

### 15.3 Airfields

- **MUST:** Airfield landing may use conventional control or ADLC.
- **MUST:** Airfield rollout uses simplified deceleration and directional guidance rather than individual tire, anti-skid, brake-temperature, or hydroplaning simulation.
- **MUST:** Runway departure, terrain impact, gear collapse, and collision remain possible when position or damage warrants them.
- **TBD:** Runway friction, brake effectiveness, steering gain, excursion bounds, and landing-success thresholds freeze through Phase 2 ground-contact tests.

---

## 16. Opening missions and campaign behavior

### 16.1 Operation 1 — fleet-replacement check ride

- **MUST:** The first offered campaign sortie is a skippable land-based fleet-replacement check ride.
- **MUST:** It teaches cold start, taxi, takeoff, navigation, radar/weapon employment, missile defense, return navigation, and airfield landing.
- **MUST:** The attack segment uses a cooperative drone.
- **MUST:** The defense segment spawns a telemetry training missile using real seeker, kinematic, RWR, HUD, and RIO behavior; a hit records lesson failure without killing the campaign pilot.
- **MUST:** Instruction remains real-time. The RIO repeats or rephrases missed actions and mission objectives wait where safely possible.
- **MUST:** Major lesson failure offers a restart from the current authored segment by ending the run and starting a deterministic replacement run.

### 16.2 Operation 2 — introductory carrier CAP

- **MUST:** The second opening sortie begins cold on the carrier and teaches startup, guided deck taxi, catapult launch, CAP, ROE restraint, simplified Case I recovery, ADLC, and arrestment.
- **MUST:** Hostile contacts may approach and maneuver but remain outside weapons-release authority and withdraw without a required engagement.
- **MUST:** Weapons remain physically usable. Unauthorized fire resolves and fails the mission under ROE.

### 16.3 Progression and debrief

- **MUST:** Campaign operations define authored success, partial-success, and failure outcomes that may all advance the campaign.
- **MUST:** The two endings depend on strategic objectives and player conduct, including ROE, rather than one final choice or raw score alone.
- **MUST:** Aircraft damage resets before the next mission through repair or replacement; debrief and narrative retain the prior sortie result.
- **MUST:** Death, capture, or aircraft loss never deletes a save. The player may retry or accept the operation’s authored failure outcome.
- **MUST:** Simplified ejection survival depends on altitude, attitude, speed, and location and ends the sortie.
- **MUST:** Debrief reports objective outcome, ROE, weapon employment, survival, fuel, wingman, damage, landing grade, and a compact event timeline.
- **TBD:** Remaining operation scripts, campaign branch variables, ending predicates, scoring bands, and narrative text freeze during Phase 4–5 mission authoring.

---

## 17. Presentation and accessibility

- **MUST:** Critical identity is never color-only; shape, fill, outline, text, luminance, or tone duplicates it.
- **MUST:** Positive-G desaturation follows the Revision 1.4.1 baseline and preserves essential HUD, threat, and failure identity through protected palette roles.
- **MUST:** Incoming missiles need not be visible as world polygons; RWR, HUD, RIO, radar/datalink state, and background physics remain authoritative.
- **MUST:** Day, dusk, and night presets preserve HUD and contact readability.
- **MUST:** Voice samples are optional presentation. Text and tones remain complete gameplay channels.
- **MUST:** Presentation RNG, effect allocation, chase view, map rotation, and unfinished world buffers cannot change simulation, AI, sensors, weapons, damage, objectives, or scoring.
- **R0-GATED:** Production resolution, cockpit/world split, polygon limits, palette shades, symbol rasterization, voice budget, effect density, and world cadence freeze only through R0.

---

## 18. Logical public contracts

- **MUST:** `ControlContext` distinguishes Deck, Takeoff-and-Landing, Normal Flight, and Combat semantic inputs.
- **MUST:** `ControlLawMode` distinguishes Assisted and Manual and records source tick and degradation/failure state.
- **MUST:** `AutothrottleState` records disengaged/capture/holding/saturated/overridden state, KIAS command, actual throttle authority, and source tick.
- **MUST:** `ADLCState` records commanded/engaged/capturing/holding/degraded/failed state, commanded flight-path angle, target AoA/speed, limiting reason, and source tick.
- **MUST:** `RadarTrackSource` distinguishes organic, offboard, and fused information without duplicating one physical contact.
- **MUST:** `TrackQuality` represents detection, coasting, priority, weapon-quality, support-lost, and dropped transitions.
- **MUST:** `IdentificationState` distinguishes unknown, friendly, neutral, hostile, and the authority/evidence that produced the classification.
- **MUST:** `WeaponGuidanceState` distinguishes rail, supported, autonomous, tracking, coasting/reacquiring, defeated, detonated, and expired states.
- **MUST:** `MissileThreatState` distinguishes emitter/launch indication, active seeker, indication lost, still dangerous, and defeat-confidence state.
- **MUST:** `FuelAdvisory` records destination, normal-return requirement, Joker/Bingo state, recommended heading/altitude/KIAS, reserve class, and source tick while presentation may hide numeric thresholds.
- **MUST:** `RIOCalloutPriority` implements the frozen callout hierarchy and repeat/preemption behavior.
- **MUST:** `LandingGrade` records approach deviations, touchdown state, wire/bolter, damage, and overall grade.
- **MUST:** `TutorialLessonState` belongs to mission runtime, changes at objective evaluation, and serializes only through versioned field-wise mission/save data.
- **MUST:** Presentation consumes these states only from the last completed `SimulationSnapshot`.
- **TBD:** Binary widths, packing, field order, update frequency, and memory placement for new logical contracts require the applicable Phase 1–4 schema and measured-limits reviews; this supplement does not alter the frozen public memory ABI.

---

## 19. TBD and measured-decision register

| ID | Class | Subject | Current target or boundary | Validation method | Decision gate |
|---|---|---|---|---|---|
| IN-01 | R0-GATED | Exact key layout and pie timing | Preserve every semantic action; preferred defaults in §5.2 | Hardware joystick/keyboard latency and ambiguity trials | R0-B / Phase 1 input gate |
| DS-01 | R0-GATED | Map and HUD layout | Fused heading-up picture; four scales; tactical/center anchors | R0 display benchmarks and readability capture | R0-B measured-limits revision |
| FL-01 | TBD | Aerodynamic coefficient set | Must reproduce §7 handling and energy contracts | High-precision and bit-exact host envelopes | Phase 2 flight gate |
| FL-02 | TBD | Assisted/Manual control gains | +9/−3 G, 180°/s, progressive digital response targets | 1,000+ control sequences and qualified pilot signoff | Phase 2 flight gate |
| FL-03 | TBD | ADLC control tables | 8 units, 145–155 KIAS, 0.25°, 3.5° targets | Approach vectors, hardware playtest, landing statistics | Phase 2 carrier gate |
| EN-01 | TBD | Engine and wing-sweep tables | Mach 2.5 / 65,000 ft aircraft target | Host thrust/fuel/acceleration envelopes | Phase 2 engine gate |
| FU-01 | TBD | Fuel, Joker, and Bingo tables | Real-time burn, one bolter/go-around, ten-minute Joker target | Fixed-point route oracle and campaign-duration trials | Phase 2 / Phase 4 |
| RD-01 | TBD | Radar detection and tracking | Aspect/RCS/range/clutter/jamming contract | Deterministic sensor scenarios and track-transition vectors | Phase 3 radar gate |
| WP-01 | TBD | Missile and fuze tables | Physical loft, energy loss, seeker support, proximity fuze | 1,000+ golden trajectories plus boundary suites | Phase 3 weapon gate |
| GN-01 | TBD | Cannon tables | Lead-computing sight, 675 rounds, grouped shots | Host ballistic oracle and intersection cases | Phase 3 weapon gate |
| DF-01 | TBD | Notch/decoy/RWR tables | Geometry/clutter notch and deterministic decoy scoring | Defensive geometry matrix and replay checks | Phase 3 defense gate |
| CV-01 | TBD | Catapult, wire, hook, and LSO tables | Three wires, target two, 3.5°, 14 ft/s target | Carrier-local contact oracle and novice/expert trials | Phase 2 / Phase 4 |
| AI-01 | TBD | RIO, wingman, enemy, and AIC doctrine | Sensor-limited deterministic decisions | Scenario corpus, trace comparison, callout review | Phase 4 tactical gate |
| MS-01 | TBD | Remaining mission/campaign data | Ten-operation campaign and two endings retained | Mission compiler, replay, branch coverage | Phase 4–5 |

- **MUST:** Closing a TBD requires recording the chosen value/table, evidence identity, accepted tolerance, and architecture/gameplay revision that froze it.
- **MUST:** R0-GATED decisions require the full R0 identity defined by Revision 1.4.1 and are nonauthoritative without it.

---

## 20. Acceptance tests

### 20.1 Architecture and determinism

- **MUST:** PAL and NTSC replays match across cold start, flight, radar, missile combat, countermeasures, damage, carrier recovery, lesson restart, and debrief.
- **MUST:** Camera, map anchor, chase view, presentation effects, unfinished rendering, and display refresh cannot change checksums.
- **MUST:** All physical entities integrate on the 100 Hz timeline; instrumentation detects any unauthorized secondary integration cadence.
- **MUST:** Tutorial retry starts a new deterministic run and never rolls back an active `SimulationTick`.

### 20.2 Capacity and combined load

- **MUST:** The mission compiler accepts and reports the §3.1 combined air-combat peak and rejects each deliberate one-slot overflow mutation.
- **MUST:** The combined harness sustains nine aircraft, sixteen missiles, twenty-four gun groups, forty-eight decoys, eight dynamic mission entities, eight objectives, and sixty-four presentation effects while exercising radar tracks, RIO priorities, damage events, audio, HUD, and rendering load.
- **MUST:** The surface audit validates the current authoring target together with concurrent air, weapon, countermeasure, contact, objective, and effect peaks.
- **MUST:** Compiler predictions equal or exceed measured high-water marks in Xemu and hardware.

### 20.3 Flight and systems

- **MUST:** Golden vectors cover atmosphere, KIAS/TAS/Mach conversion, weight changes, engine spool/thrust/fuel, wing sweep, Assisted G, roll buildup, Manual rates, stall/mush, departure, recovery, over-G, overspeed, hydraulic degradation, actuator asymmetry, engine-out flight, and relight.
- **MUST:** Cold start passes in Engine 2-first and Engine 1-first orders, with correct limited capability, status colors, cautions, and dependency transitions.
- **MUST:** ADLC passes capture, saturation, configuration, degraded-system, airfield, carrier, bolter, and go-around sequences.

### 20.4 Sensors, weapons, and defense

- **MUST:** Radar tests cover field-of-regard boundaries, source correlation, configured coast/support timeout boundaries including the five-/two-second targets, clutter, jamming, IFF authority, track overflow, priority replacement, and all four display scales.
- **MUST:** Missile tests cover launch without solution, unsupported launch, loft, support loss, activation, reacquisition, notch geometry, low-altitude drag, countermeasures, fuze miss distance, mutual kill, and component damage.
- **MUST:** Gun tests cover lead solution, burst grouping, pool concurrency, surface-site disable, friendly/neutral impact, carrier consequence, and static-scenery immunity.
- **MUST:** RIO tests distinguish indication lost from confirmed defeat and preserve callout priority under simultaneous missile, fire, and Bingo events.

### 20.5 Missions and playability

- **MUST:** A first-time player using provided instruction can complete startup, takeoff, navigation, attack, defense, return, and landing within two attempts.
- **MUST:** After instruction, a novice can achieve at least three safe carrier arrestments in five attempts while receiving meaningfully different LSO grades.
- **MUST:** Operation 2 permits unauthorized release, resolves the shot physically, and applies the ROE failure outcome deterministically.
- **MUST:** Campaign saves round-trip through three slots and preserve authored branch outcomes without serializing raw runtime structures.
- **MUST:** Final flight feel requires both host-envelope compliance and explicit qualified-pilot approval.

---

## 21. Draft 0.2 decision log

| Decision | Class | Reason |
|---|---|---|
| No multi-rate physical integration | MUST | Preserves the frozen 100 Hz clock, tick order, collisions, and replay semantics |
| Per-pool and combined concurrency audits | MUST | Separates logical capacity from CPU cost and prevents overlap-driven exhaustion |
| AIC consumes an aircraft slot only when instantiated | MUST | Makes physical support aircraft visible to mission capacity validation |
| Static scenery never becomes destructible | MUST | Preserves Revision 1.4.1 §13.2 and resource/entity separation |
| Requirement classes tag every normative statement | MUST | Prevents tuning and presentation details from masquerading as architecture |
| Semantic controls freeze; bindings do not | MUST / R0-GATED | Preserves gameplay while allowing real hardware measurement |
| Fused map behavior freezes; pixel geometry does not | MUST / R0-GATED | Preserves information design without prejudicing R0 |
| Flight and ADLC numbers are calibration targets | TARGET | Retains intended feel while allowing evidence-driven coefficient tuning |
| Tutorial retry starts a new run | MUST | Preserves monotonic simulation time and snapshot semantics |
| Persistent physical effects are not currently required | MUST | Prevents presentation effects from leaking into deterministic simulation |
