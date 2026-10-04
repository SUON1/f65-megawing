---
title: "F65 Flight Physics and Simulation Engineering"
subtitle: "Version 4.0 | 65Aero physics, aircraft data, and verification"
author: "F-65 Megawing"
date: "4 October 2026"
lang: en-US
---

# 0. Document control and engineering intent

**Document ID:** `F65-PHYSICS-4.0`\
**Revision:** 4.0, incorporating R1 corrections; adopted 4 October 2026.\
**Revision provenance:** Corrects the 1 October draft, SHA-256 `9efcdc94d54298c7d6036fd5fee98682c77172ea1033bd03becab827787cb644`. Founder directed coordinated adoption after the R1 correction pass; the adopted identity is recorded in the corpus manifest.\
**Status:** **APPROVED ENGINEERING BASELINE. IMPLEMENTATION VALUES REMAIN GATED.**\
**Role:** Detailed subsystem engineering specification and aircraft-data authoring reference for 65Aero.\
**Predecessor:** Flight Simulation Physics Engineering White Paper v3.3, 23 August 2026.\
**Target:** MEGA65; LLVM-MOS C with selectively admitted 45GS02 assembly.\
**Current parents:** Main Concept v1.7, Gameplay v1.1, and Runtime v1.1 approved candidate amendment. Original review inputs and historical source identities remain recorded in Appendices D and F.

**Adoption authority:** [Founder-directed adoption, 4 October 2026](../../docs/decisions/PHYSICS_V4_ADOPTION_2026-10-04.md). This approves the engineering design, not aircraft data, implementation, measured limits or phase entry.

## 0.1 What this revision accomplishes

The flight model and its aircraft data are one engineering product. A correct rigid-body solver supplied with inconsistent geometry, guessed inertias, poorly defined coefficients, or incompatible control conventions will not produce a credible aircraft. Conversely, a sophisticated aerodynamic database does not rescue an incorrect frame transformation or an unstable fixed-point integrator.

Version 4 therefore specifies both:

1. **The physical computation:** environment, air-relative flow, aerodynamic forces and moments, propulsion, control surfaces, mass properties, six-degree-of-freedom motion, and contact.
2. **The data path:** aircraft definition, source provenance, coefficient generation, normalization, validation, table reduction, deterministic compilation, mission-load admission, and repeatable handling tests.

The intended aircraft is a responsive, consequential fighter, not a prescribed trajectory or an attitude directly attached to a joystick. Turns consume energy; engine asymmetry produces moments; wing sweep changes aerodynamics and mass properties; control surfaces have finite authority and response. Augmentation improves the pilot's command interface without supplying impossible lift, thrust, or instantaneous attitude changes. These objectives carry forward the approved parents and v3.3. [P1, §§7, 19; P2, §§7–8; P4, §§3–15]

## 0.2 Relationship to the core three

The core documents remain the build authorities. This paper supplies the subsystem depth that they deliberately reference rather than duplicate. It does not become a fourth master specification.

| Document | Responsibility retained |
|---|---|
| Main Concept v1.7 | Product scope, architecture, clocks, ownership, capacities, memory boundaries, and phase gates. |
| Gameplay v1.1 | What the pilot commands and experiences, aircraft operation, failures, recovery, and player-facing acceptance. |
| 65Aero Runtime v1.1 candidate amendment | Integration, generated public records, ABI, lifecycle, scheduling, memory accounting, and evidence infrastructure. |
| Physics v4.0 | Detailed physical model, aircraft-data contract, numerical strategy, and physics/data validation. |

Runtime v1 explicitly separates its integration ownership from the physics paper's equations, aerodynamic data, mass/inertia schedules, control models, and oracle acceptance. The new paper preserves that boundary. Runtime v1 is **approved as a candidate design, not FINAL**; the adopted Runtime v1.1 amendment retains candidate status. [P3, front matter, §§0, 5, 11, 23]

Physics v4.0 is the current detailed physics baseline under the coordinated parent revisions. Physics v3.3 is retained provenance. Historical evidence continues to cite the authority under which it was produced; adoption does not retroactively validate it against v4.

## 0.3 Requirement language and change provenance

**MUST** identifies a required behavior of the adopted v4 design. Inherited requirements and newly explicit engineering contracts apply within the controlling parents. Candidate numerical methods and open values still require their named implementation/data evidence gates. **TARGET** is a quality or product goal. **MEASURED** marks a choice requiring admitted target evidence. **TBD** marks an intentionally unresolved value with an owner and closure gate.

Appendix C distinguishes inherited requirements, explicit clarifications, and newly adopted v4 design decisions. The most material additions are the aircraft-data package, its release gates, the low-cost aerodynamic decomposition, the explicit numerical conventions, and the causal scheduling details. None silently authorizes a new hardware allocation, public binary layout, production coefficient set, or change to the 100 Hz contract.

## 0.4 Scope and non-goals

The principal subject is fixed-wing aircraft dynamics, especially the F-65A. A short shared 3DOF section defines physically meaningful point-mass motion for the existing weapon architecture. It does not define new seekers, weapon performance, targeting, fuzes, or damage models.

This revision does not add computational fluid dynamics on the target, aeroelastic structural modes, unrestricted rotary-wing dynamics, weather-cell simulation, icing, cloud-induced forces, wave-driven carrier motion, an aircraft editor, external tanks, or an in-sortie physics-quality switch. It does not require an offline aerodynamic tool to be embedded in the game.

Current program progress belongs in repository status records. Only Appendix D contains a dated R0 evidence snapshot. A technical dependency is not a claim that its acceptance gate has passed.

## 0.5 Reading path

Aircraft authors should start with §§3–7, §13, and Appendix A. FlightDynamics implementers should read §§1–2 and §§4–12. Verification work starts with §14 and Appendix B. Core integration and configuration-control work uses §§1, 12, 15 and Appendices C–F. The Markdown is the editable source; the PDF is a generated reading copy of this revision.

# 1. Placement inside 65Aero

## 1.1 Owners, not a second monolithic physics engine

The term *physics engine* in this paper describes cooperating 65Aero owners, not a new subsystem allowed to bypass them. [P1, §3; P3, §§3, 10–13]

| Owner | Owns and changes | Receives or publishes |
|---|---|---|
| `EnvironmentEngine` | Shared atmosphere, wind, gravity, world queries, and the approved carrier-motion boundary. | Bounded environment samples and canonical terrain/deck references. |
| `ControlAndSystemsEngine` | Engine operating state, fuel/supply state, FCS capability, controller memory, trim, transfer bias, mixer, and actual actuator/sweep state. | Commands in; read-only systems/surface/mass-configuration views out. |
| `FlightDynamicsEngine` | Aircraft motion, approved aerodynamic lag states, derived flight quantities, and the aircraft mass-property result/cache. | Systems/configuration/environment inputs; physical state and derived views. |
| `ContactEngine` | Stage-10 terrain, runway, wheel/deck, catapult, hook, and arrestment resolution. | Contact corrections through the declared aircraft boundary, never arbitrary private-state writes. |
| `WeaponAndDamageEngine` | Weapon motion and guidance state, release/expenditure, damage events, and weapon lifecycle. | Shared environment and approved physical primitives; configuration/damage changes through owned interfaces. |
| `CoreRuntime` / platform | Tick, dispatch, entity lifecycle, buffers, memory access, DMA, checksums, and protected hardware. | Generated interfaces and bounded platform services. |

The exact storage representation remains generated Runtime work. Names such as `AircraftDefinition` and `MassPropertiesView` below specify logical responsibilities, not permission to hand-write a competing public ABI.

**PHY-OWN-01:** Every persistent variable has one owner. Fuel quantity is not independently decremented by the engine model and the mass model. A store is not simultaneously counted in the aircraft and an already detached weapon. Presentation and AI never integrate aircraft state themselves.

## 1.2 Authoritative stage placement

The Main Concept's 21-stage order is unchanged. The following excerpt records the physics-relevant boundary, not a replacement dispatcher. [P1, §4.2; P3, §4]

| Stage | Relevant work and causal boundary |
|---|---|
| 2–3 | Latch pilot commands and legally eligible prior-tick directives. |
| 4 | Advance shared environment/carrier state. |
| 5 | Advance electrical, fuel, engine, and hydraulic supplies. |
| 6 | Evaluate FCS mode/capability and authorized augmentation. |
| 7 | Apply mixer/gearing, hydraulic authority, actuator rates/stops, and asymmetry. |
| 8 | Sample atmosphere for force evaluation; assemble aircraft forces and moments. |
| 9 | Integrate aircraft motion. |
| 10 | Resolve terrain/runway/deck/catapult/arrestment/contact. |
| 11–14 | Accept releases; integrate existing weapons; detect and apply damage. |
| 15–16 | Sensors then AI/RIO. New decisions cannot affect earlier stages of this tick. |
| 18–21 | Commit lifecycle; extract presentation; checksum; publish complete snapshot. |

**PHY-TICK-01:** All live physical aircraft advance on the same exact 100 Hz timeline. `SIX_DOF` and `KINEMATIC` are mission-load selections, not distance, visibility, difficulty, or CPU-pressure switches. Baseline acceptance is six `SIX_DOF` plus three `KINEMATIC` aircraft; a six-DOF AIC is a separate identified variant. Pool capacity 16 is not proof that 16 full models can coexist within the required workload. [P2, §4; P3, §7]

## 1.3 Sampling and handoff detail

The parents fix stage order but not every internal sample age. The adopted integration contract specifies the following explicit rule to avoid accidental algebraic loops:

- Stage 6 uses the last committed valid aircraft/air-data feedback, tagged with its source tick. It does not read the not-yet-produced stage-8 air data or stage-9 response of the same tick.
- Stage 7 publishes one coherent actual-surface/configuration view for stage 8. Commanded and actual positions remain different fields.
- Stage 5 consumes throttle demand already eligible at that stage. A conventional autothrottle or ADLC throttle correction generated at stage 6 becomes eligible at stage 5 of the next tick. Pilot override arbitration occurs at the next legal consumption boundary, not by rerunning stage 5.
- Fuel mass consumed at stage 5 participates in the stage-8/9 mass-property evaluation. A stage-11 release or stage-14 damage change becomes visible to aircraft force integration on the next tick. It cannot retroactively alter stage 9.
- Spawned entities begin their scheduled physical update after the stage-18 lifecycle commit, as the Runtime contract requires. Release rejection does not consume inventory or mass.

This one-tick controller/plant timing is a **adopted v4 integration contract**, requiring generated-interface and closed-loop validation. It is not a claim that the current R0 fixture implements flight controls. Source-tick fields, stale-input rejection, and queue ownership must be included in the eventual generated contracts. [P3, §§4–5, 7, 11–12]

### 1.3.1 Signal sampling contract

Tick `n` means the current authoritative tick; this table specifies logical semantics, not binary fields. Runtime owns their eventual cross-module contract. No stage is rerun and the 21-stage order is unchanged.

| Signal | Producer and source | Consumer / eligibility | Validity and transition rule |
|---|---|---|---|
| Aircraft pose/rates feedback | FlightDynamics stage 9, corrected through its stage-10 contact handoff; committed result of tick `n-1` | Stage-6 controls at tick `n` | A coherent post-contact aircraft state; never combine pre-contact position with post-contact velocity. Initialization uses an explicitly initialized mission-start sample, not an invented prior tick. |
| Air-data feedback | Declared air-data producer, including physical sample stage and sensor capability; committed before tick `n` | Stage-6 controls at tick `n` | Preserve actual source tick and sampling stage. Committing a frame does not make its air data post-contact or current. No substitution of omniscient healthy truth for failed instrumentation. |
| Engine atmospheric/flight inputs | Environment service and last committed aircraft state available before stage 5 | Stage-5 engine/spool/fuel update | State the environment-query location/time and aircraft sample age. Do not read future stage-8 data. Stage 8 evaluates aerodynamic loading with its own current legal sample. |
| Systems capability | Stage-5 electrical/fuel/hydraulic/engine result | Stage-6 capability/FCS and stage-7 actuation in tick `n` | Current capability is distinct from previous-tick motion feedback. A current failure cannot be hidden by an older healthy feedback record. |
| Throttle demand | Eligible pilot input and prior controller output | Stage 5 of tick `n`; a stage-6 correction is eligible no earlier than stage 5 of `n+1` | At consumption, arbitrate pilot override and current controller eligibility. Disengagement, failure, mode/context changes and reset invalidate any now-ineligible pending correction; it cannot be replayed as a fresh command. |
| Actual surfaces/configuration | Coherent stage-7 result | Stage 8 of the same tick | Actual positions, limits and validity travel together; never substitute demanded positions. |
| Loading/damage | Fuel expenditure at stage 5; accepted release at stage 11; damage at stage 14 | Fuel affects stages 8/9 of `n`; release/damage affect their next eligible aircraft integration, at `n+1` | One effective event identity; no duplicate mass/impulse change. Release rejection changes neither inventory nor mass. Spawn motion begins only after lifecycle commit. |

Each consumer must declare its permitted sample-age bound, initialization behavior and deterministic invalid/stale-input response in the generated contract and validated control design. These bounds and fallback laws remain TBD; this specification does not invent gains or a universal timeout. Holding a previous value never silently restores validity. Storage resume preserves source age on the paused simulation timeline; a reset/reinitialization explicitly invalidates pending commands and reconstructs initial samples. Required tests cover tick boundaries, contact correction, controller override/failure, rejected release, initialization and resume.

## 1.4 Other subsystem boundaries

Physics supplies attitude, velocity, surface/sweep positions, engine state, aerodynamic loading, and contact events through approved views. Graphics uses snapshots and canonical geometry; it cannot adjust physical attitude to smooth a slow world frame. Audio may synthesize buffet or spool sound from actual state but cannot create a stall. Sensor/AI code receives its legal projections, not an unrestricted copy of the world's private truth. Shared environmental data does not authorize omniscient targeting. [P5, §§3–5; P6, §§2, 7; P7, §§1–4; P8, §§5, 7–8]

# 2. Fidelity philosophy and conventions

## 2.1 Credibility on constrained hardware

The objective is a small model with correct causes, not a large model with an impressive feature list. Retain the terms that materially determine handling, energy, stability, and coupling. Bound or omit secondary effects only with a documented applicability region and an error test.

Yaw input can create sideslip, a rolling aerodynamic moment, altered lift/drag, and inertia-coupled motion. It must not be implemented as an arbitrary yaw-to-roll animation. Natural damping must arise from aerodynamic rate terms; it must not disappear when artificial FCS damping is disabled. Stall must result from the aerodynamic model and its state, not from an unrelated speed trigger.

## 2.2 What to take from earlier and later simulators

Main Concept names early flight simulators as feel and presentation influences, not technical authorities. Where original implementation evidence is absent, this paper does not infer an internal integration rate or equation set from how a game looks. [P1, §1.1]

A useful contrast is documented rather than nostalgic. The *Falcon 3.0* manual exposes alternative flight-model fidelity settings and a coprocessor-dependent high-fidelity option. F65 instead fixes the mission's physical class and does not use player difficulty to change physics. JSBSim documents coefficient build-up and table/function aircraft definitions. X-Plane documents a geometry/element-based force approach. Neither desktop runtime is proposed for direct transplantation to the MEGA65. [R1–R3]

**V4 design choice:** use geometry and higher-cost analysis offline where they help produce defensible data; execute compact, bounded force/moment tables and a small coupled rigid-body model in-game. Preserve component identities needed for failures and asymmetry, without calculating flow over a full mesh every tick. This is the adopted synthesis, not a claim about an undocumented historical simulator.

## 2.3 Coordinate and sign contract

| Quantity | Convention |
|---|---|
| World/local navigation frame | North, East, Down (NED), right-handed. Altitude is positive up, so altitude rate is minus Down velocity. |
| Aircraft body frame | +X forward, +Y right, +Z down. |
| Angular rates | $p$, $q$, $r$ about body X, Y, Z. Positive roll lowers the right wing; positive pitch raises the nose; positive yaw turns the nose right. |
| Attitude | Hamilton quaternion $\boldsymbol\eta=(\eta_0,\eta_1,\eta_2,\eta_3)$, scalar first, rotating body vectors into NED. |
| Aerodynamic angles | $\alpha=\operatorname{atan2}(w_a,u_a)$; $\beta=\operatorname{atan2}(v_a,\sqrt{u_a^2+w_a^2})$. |
| Aerodynamic forces | Positive drag opposes air-relative velocity; positive lift points approximately body-up at small angles. Side-force basis is defined in §6. |
| Moments | $\ell$, $m_y$, $n$ are body roll, pitch, yaw moments. $C_L$ is lift; $C_l$ is rolling moment. They are not interchangeable. |
| Pressure | $\bar q$ is dynamic pressure; $q_c$ is pitot impact pressure; $q$ alone is pitch rate. |

A fixed airframe datum defines authored positions; center of gravity (CG) is computed relative to that datum. An importer must rotate and translate each source convention once, then record the transformation. Do not copy a solver's structural coordinates or product-of-inertia signs by name. JSBSim, for example, documents a structural frame different from its body frame. [P4, §3; R4]

The flight solver uses the project's local NED/world-position service, not a newly introduced rotating-Earth navigation system. A host comparison must use equivalent frame and gravity assumptions. Sector crossing is a coordinate operation, not a force, a discontinuity, or a world boundary that turns the aircraft around. [P2, §6]

## 2.4 Units and physical meaning

The authoring schema permits explicit source units; the import stage converts them to one canonical physical convention. Equations here use feet, seconds, slugs, lbf, radians, and slug-ft². Aviation display values remain knots, feet, pounds, G, and indicated AoA units as specified by Gameplay. The generated numeric registry owns the eventual integer widths, fixed-point scaling, rounding, and bounds. [P1, §§2, 4; P3, §§2, 5]

**PHY-UNIT-01:** A quoted reference weight in lbf becomes mass through $m=W_0/g_0$, using the declared reference gravity. Do not recompute mass from changing local gravity. Current weight is $m g(h)$. A fuel-flow value in lb/hour must identify its mass convention and convert once; do not treat it as slugs/second.

A derivative per degree differs from a derivative per radian. A coefficient derivative with respect to dimensional pitch rate differs from one with respect to $\hat q=q c_{ref}/(2V)$. Record the denominator convention explicitly. An AoA indication of “8 units” is not eight degrees and requires a defined instrument mapping. [P2, §15]

# 3. The aircraft definition: what must be supplied

## 3.1 Separate three kinds of information

**Aircraft definition** is immutable, versioned type data: geometry, coefficient tables, engines, actuators, configurations, source provenance, and valid domains. Multiple instances of the same type share it.

**Aircraft state** changes during the sortie: position, velocity, attitude, rates, remaining fuel/stores, engine spool, actual surfaces/sweep, damage, trim, controller memory, and aerodynamic lag state. Each value has one owner.

**Derived evaluation data** includes CG/inertia, interpolated coefficients, table-cell indices, air data, and force/moment totals. A cache may reduce cost, but it must be invalidated by every relevant state or model-generation change. It may not become an unaccounted second authority. Whether a derived cache participates in a checksum is a generated Runtime decision; recomputing it must produce the same authoritative result.

**PHY-DATA-01:** Geometry and top-speed targets alone are not a flight model. A type is admitted only with enough data to compute all required forces, moments, control response, and mass changes in its supported operating region. “Unknown” is not zero.

## 3.2 Minimum authoring groups

Appendix A gives the detailed data dictionary. The following is the minimum practical intake checklist.

| Group | Required content | Why it matters |
|---|---|---|
| Identity and evidence | Stable model ID/revision, schema version, source catalog, licenses, method versions, approval state, valid domains. | Reproduces a particular aircraft instead of an unidentified collection of numbers. |
| Reference geometry | Datum/frame, fixed coefficient reference area/span/chord, aerodynamic reference point, wing/tail/body geometry identity. | Gives coefficients physical scale and consistent moment arms. |
| Mass and loading | Defined operating-empty contents, empty CG/inertia, fuel tanks, payload stations, ammunition, permitted loads and CG limits. | Determines acceleration, trim, inertia, and release/fuel effects. |
| Aerodynamics | Six force/moment channels; static, dynamic, control, configuration, sweep, and approved asymmetry/stall effects. | Produces consequential coupled motion. |
| Propulsion | Installed engine positions/directions, net thrust, spool response, fuel flow, AB and failure/relight behavior. | Distinguishes thrust from throttle and makes engine-out physical. |
| Surfaces and hydraulics | Individual surface IDs, positive deflections, limits, rates, supply dependencies, jam/loss behavior. | Prevents a requested control from being mistaken for actual authority. |
| Controls and instruments | FCS schedules, trim, anti-windup, transfer behavior, capability mapping, ADLC/autothrottle, air-data validity. | Makes the same airframe fly credibly in both control modes. |
| Ground/deck configuration | Wheels, hook, launch attachment, contact dimensions, friction/response data and legal configuration. | Enables physical takeoff, landing, launch, and recovery. |
| Acceptance | Trim cases, response/energy targets, uncertainty, envelope classes, compiler constraints, validation evidence. | Specifies what “works” means before tuning hides defects. |

## 3.3 What geometry is needed, and what is not

The **offline geometry description** should include wing planform sections, root/tip chords, span, incidence, twist, dihedral, airfoil identity or thickness/camber descriptors, sweep pivot and limits, tail geometry and offsets, fuselage dimensions, and control-surface extents/hinges. Include engine and fuel/payload locations relative to the same datum. Record which details are represented by the selected analysis method and which are approximated.

The **target package** needs only geometry used at runtime: reference scales, moment arms or approved schedules, actual-sweep transformation data, contact landmarks, and the compact tables derived from the analysis. It does not need the high-resolution aerodynamic mesh, CAD history, or every offline panel coordinate.

A visual model is not a mass model or an aerodynamic model. All three should agree on major dimensions, sweep geometry, gear/hook/launch locations, and datum, but a low-poly mesh cannot establish the aircraft's inertia or aerodynamic derivatives. Cosmetic mesh simplification must not silently change the physical definition.

## 3.4 Source quality and uncertainty

Each data item or table family records a `source_kind`: **measured**, **published-derived**, **analytic**, **numerical-analysis**, **estimated**, **tuned**, or **test-only**. These describe provenance, not the project's MUST, TARGET and MEASURED requirement classes.

Record a source citation or file hash, method/tool version, assumptions, units/frame, applicability region, uncertainty or explicit unknown uncertainty, and the reviewer. For blended tables, record the contributing sources and blend rule. Tuning may legitimately shape a fictional aircraft, but a tuned value must not be labeled as measured real-aircraft data.

High-quality data means sufficient coverage and consistency, not merely more decimal places. A coefficient table with undocumented reference area or angle units is inadmissible even when its source is otherwise reputable.

## 3.5 The F-65A's current targets are constraints, not inputs to guess

The approved Gameplay document supplies the following **TARGETS**, which v4 does not promote into measured performance. [P2, §§7.3, 7.7]

| Product target | Recorded value |
|---|---:|
| Operating empty weight | 40,000 lb |
| Internal fuel | 20,000 lb |
| Maximum takeoff weight | 72,000 lb |
| Maximum carrier landing weight | 56,000 lb |
| Top performance / service ceiling | Mach 2.5 / 65,000 ft |
| Structural overspeed boundary | First of 900 KIAS or Mach 3.0 |
| Landing-configuration limit | 300 KIAS |
| Clean augmented command authority | Approximately +9 G / -3 G |
| Maximum commanded roll-rate target | Approximately 180 degrees/second |

The corpus does **not** provide an approved F-65A reference wing area, full geometry, CG envelope, inertia tensor, complete thrust deck, aerodynamic coefficient set, or gain schedule. Those remain authored/validated Phase-2 data. Do not use v3.3's fictitious worked-example geometry as F-65A design data.

These targets do not imply simultaneous achievement at every altitude, sweep, loading, or failure state. The author must build a feasible envelope and identify any target combination that cannot be satisfied without changing an approved product assumption.

# 4. Geometry, mass, CG, and inertia

## 4.1 Fixed reference scales versus changing geometry

**Proposed baseline:** one fixed $S_{ref}$, $b_{ref}$, and $c_{ref}$ per aircraft-model revision for coefficient normalization. Wing sweep changes physical geometry and coefficients, not the meaning of those scales. Actual projected span/area used for ground effect or geometry queries is separately named.

An external solver may normalize each sweep case differently. Normalize dimensional loads into the F65 scales before combining tables. For a force coefficient, $C_{new}=C_{old}S_{old}/S_{new}$. Moment-coefficient conversion also includes the appropriate reference-length ratio and any reference-point shift. This avoids counting a sweep-induced area change twice. [R5]

The wing pivot, zero-angle definition, positive direction, left/right mirroring, and actual angle limits are part of geometry data. A single “sweep percentage” without this mapping is insufficient.

## 4.2 Mass composition

For admitted components $i$, with mass $m_i$ and datum-relative location $\mathbf r_i$:

$$
m=\sum_i m_i,\qquad
\mathbf r_{cg}=\frac{\sum_i m_i\mathbf r_i}{m}. \tag{4.1}
$$

The operating-empty definition must state whether crew, oil, unusable fuel, installed racks, and equipment are included. Add usable fuel, stores, ammunition, and other approved variable components exactly once. Tanks need capacity, position/CG-versus-fill information where material, feed order, and any permitted transfer behavior. A total fuel number alone cannot describe a significant CG shift.

**PHY-MASS-01:** Mass remains positive and inside admitted loading bounds. Fuel cannot become negative. Inventory rejection cannot reduce mass. An approved release has one deterministic effective tick. Record empty, full, landing, asymmetric, and depleted configurations explicitly rather than using an arbitrary “mass bin” label without contents.

## 4.3 Full host tensor and bounded target representation

The authoring/reference model computes each component's inertia about its own center, rotates it into body axes, and applies the parallel-axis theorem:

$$
\mathbf I_{cg}=\sum_i\left[
\mathbf R_i\mathbf I_i\mathbf R_i^{T}
+m_i\big((\mathbf d_i\!\cdot\!\mathbf d_i)\mathbf 1-\mathbf d_i\mathbf d_i^{T}\big)
\right],\quad \mathbf d_i=\mathbf r_i-\mathbf r_{cg}. \tag{4.2}
$$

Source data must distinguish **tensor off-diagonal entries** from **products of inertia**. V3.3 uses negative products in the tensor. Its symmetric-airframe reduction is retained:

$$
\mathbf I=
\begin{bmatrix}
I_{xx}&0&-I_{xz}\\
0&I_{yy}&0\\
-I_{xz}&0&I_{zz}
\end{bmatrix}. \tag{4.3}
$$

Asymmetric fuel/stores or sweep may invalidate the zero $I_{xy}$/$I_{yz}$ assumption. The host reference therefore retains the general tensor. The target may use the reduced tensor **only after** the omitted terms pass the approved trajectory/coupling error test for the admitted loading classes. Otherwise retain the needed terms or restrict the admitted approximation; do not disguise an asymmetric aircraft as symmetric. This extends v3.3's data discipline without mandating a costly general solve in every target tick.

The compiler checks symmetry, positive definiteness, physical inertia consistency, and determinant/conditioning margin **after quantization and interpolation**. For (4.3), require positive diagonal terms and $I_{xx}I_{zz}-I_{xz}^{2}>0$ with a safe numeric margin. Principal moments of a physical mass distribution also obey the triangle inequalities. Near-singular models are rejected, not “fixed” by a large divide clamp. [P4, Appendix A; R4]

## 4.4 Scheduling and changing mass

Precompute or cache mass/inertia results when configuration changes make this beneficial. Every cache key includes the variables that affect it: fuel distribution, store inventory, ammunition, actual left/right sweep, relevant damage, and model revision. Caching cannot discretely jump inertia at an ordinary sweep or fuel-table boundary.

A schedule of inverse inertia is an approximation to the inverse of interpolated inertia, not an algebraic identity. Validate their product and angular response or derive the inverse from the same quantized tensor. Positive interpolation weights preserve positive definiteness before rounding; rounding and compressed representations still require explicit checks.

V3.3 permits quasi-static scheduled inertia on target. Keep that as the initial low-cost candidate. The high-precision reference must evaluate the importance of time-varying inertia, moving-component angular momentum, and mass-flow/release effects. Add a term only when necessary for the approved error envelope, but document its omission. A changing inertia tensor is not permission to inject a fictitious torque or to rescale angular rates merely to hide discontinuity.

For a released store, preserve the kinematics of the retained body and the released component consistently at the event boundary. Translational velocity at a datum offset includes $\boldsymbol\omega\times\mathbf r$. Any modeled separation impulse acts equal-and-opposite through declared event semantics. Ordinary fuel expenditure must not add a second rocket term when net engine thrust already represents momentum transfer.

### 4.4.1 CG state and datum continuity

The integrated position and ground-relative velocity refer to the instantaneous aircraft CG. Authored geometry remains relative to the fixed aircraft datum. Let `r_cg` be the body-frame datum-to-CG vector. At a loading/configuration event, first preserve the retained body's world datum pose and its declared physical velocity field; then express the new CG state from that same datum and attitude. Changing a coordinate origin alone must not move contact points, rotate the aircraft or apply an impulse.

In the rigid instantaneous-event approximation, a CG offset change `delta_r` gives `p_cg_new = p_cg_old + R delta_r` and `v_cg_new = v_cg_old + R (omega cross delta_r)`, before any separately modeled physical impulse. For continuously moving fuel/sweep components, the host reference must include or justify omission of the corresponding relative-motion terms; these event formulas are not a substitute for that moving-mass analysis. Geometry queries reconstruct the datum consistently from the current CG state. Position, velocity, loading revision and geometry view change atomically at the declared effective boundary in §1.3.

Contact resolution and store creation must use the same event convention. A separation impulse, if modeled, is a distinct equal-and-opposite physical event, applied once; coordinate rebasing is not that impulse. Validate stationary-datum rebasing, rotating-body release, changing sweep/fuel distribution and contact continuity. Generated state semantics and any omitted moving-mass approximation remain subject to Runtime review and the approved error envelope.

# 5. Shared atmosphere, wind, and air data

## 5.1 Environment service

One deterministic environment service provides temperature, static pressure, density, speed of sound, gravity, and wind. Aircraft and weapon models consume the same service and unit definitions. Mission weather defines the approved temperature profile and wind layers; clouds remain presentation-only. [P2, §6]

Use the U.S. Standard Atmosphere 1976 as an offline reference atmosphere, with a documented conversion between geometric and geopotential height where required by its equations. Compile a bounded table or equivalent admitted approximation for the target; do not run a scientific atmosphere package in-game. The mission-temperature extension must state how pressure and density remain consistent. For a dry ideal-gas model, $\rho=P/(R_{air}T)$ and $a=\sqrt{\gamma R_{air}T}$; units and absolute temperature are explicit. Do not alter density independently of temperature/pressure without declaring a different model. [R6]

A temperature deviation is not a complete weather model. Wind layers interpolate vector components, not compass angles across the 359-to-0-degree discontinuity. Gusts or turbulence require a separately admitted bounded model, deterministic state/seed, workload, and data; v4 does not add random gusts merely to make the airplane feel “alive.”

## 5.2 Air-relative versus ground-relative velocity

Let $\mathbf R$ rotate body vectors to NED; $\mathbf v_b$ is CG ground-relative velocity expressed in body axes; $\mathbf W_n$ is wind in NED:

$$
\mathbf v_{g,n}=\mathbf R\mathbf v_b,\qquad
\mathbf v_{a,b}=\mathbf v_b-\mathbf R^T\mathbf W_n. \tag{5.1}
$$

$$
V=\|\mathbf v_{a,b}\|,\qquad
M=V/a,\qquad
\bar q=\tfrac12\rho V^2. \tag{5.2}
$$

Aerodynamics uses air-relative velocity. Position integration uses ground-relative velocity. Changing wind changes aerodynamic loading through (5.1); do not directly add the same wind change to ground velocity or introduce an extra wind-acceleration term into the chosen ground-relative equations.

## 5.3 Indicated, calibrated, equivalent, and true airspeed

**PHY-AIRDATA-01:** Keep TAS, EAS, CAS, IAS/KIAS, Mach, dynamic pressure, and impact pressure distinct. They are not interchangeable labels for a single speed.

$$
V_{EAS}=\sqrt{2\bar q/\rho_0}=V\sqrt{\rho/\rho_0}. \tag{5.3}
$$

CAS is the sea-level-standard speed corresponding to a defined pitot impact pressure. IAS is the indicated result including whatever instrument/position-error model has actually been selected. A healthy ideal-instrument approximation may set IAS equal to CAS, but must state that approximation. Failed or unavailable air data cannot silently become healthy merely because physical truth still exists.

For a calorically perfect gas, define a pitot pressure-ratio function $H(M)$. Below Mach 1 it is the isentropic total/static ratio. Above Mach 1 it includes the normal-shock total-pressure loss:

$$
H(M)=\left(1+\frac{\gamma-1}{2}M^2\right)^{\gamma/(\gamma-1)}
\quad (0\le M\le1), \tag{5.4}
$$

$$
\begin{aligned}
\Pi(M)&=\left[\frac{(\gamma+1)M^2}{(\gamma-1)M^2+2}\right]^{\gamma/(\gamma-1)}
\left[\frac{\gamma+1}{2\gamma M^2-(\gamma-1)}\right]^{1/(\gamma-1)},\\
H(M)&=\Pi(M)\left(1+\frac{\gamma-1}{2}M^2\right)^{\gamma/(\gamma-1)}
\quad (M>1).
\end{aligned} \tag{5.5}
$$

Then $q_c=P[H(M)-1]$ and the ideal CAS satisfies
$H(V_{CAS}/a_0)=1+q_c/P_0$. Generate and validate the forward/inverse tables offline over the actual admitted range, including the sonic transition. The inverse must use the appropriate branch; do not extrapolate the subsonic calibration through arbitrary impact pressure. These are ideal aligned-probe relations, not a complete installation-error model. [R7]

The old shorthand “same KIAS means same loading” is only an approximation. Dynamic pressure follows EAS exactly under (5.3); compressibility prevents a blanket KIAS equivalence at high Mach. Controller schedules must consume the physical variable they actually intend.

## 5.4 Low speed and invalidity

At zero airspeed, angle of attack and sideslip are undefined. Mark the aerodynamic-angle validity explicitly. A guarded $V_{safe}$ may be used in normalized-rate denominators, but must not replace physical $V$ in dynamic pressure or invent lift at rest. Forces have a bounded low-speed continuation; thrust, gravity, and ground contact remain active.

The model specifies a smooth treatment near the low-speed transition, including high angular rates. A previous angle may be retained for display continuity only where appropriate, not reused indiscriminately as current physical evidence. Air-data validity, sensor capability, and aerodynamic-table-domain validity are separate flags.

# 6. Aerodynamic model and compact tables

## 6.1 Force and moment channels

Use one unambiguous primary coefficient convention per normalized dataset. The normalized convention defined here is wind-axis $C_D,C_Y,C_L$ and body-axis $C_l,C_m,C_n$. The table descriptor records its convention; source datasets using body-axis forces are converted, not mixed inside one unlabeled array. [R2]

Define orthonormal body-expressed wind basis vectors:

$$
\begin{aligned}
\mathbf e_v&=(\cos\alpha\cos\beta,\ \sin\beta,\ \sin\alpha\cos\beta),\\
\mathbf e_y&=(-\cos\alpha\sin\beta,\ \cos\beta,\ -\sin\alpha\sin\beta),\\
\mathbf e_z&=(-\sin\alpha,\ 0,\ \cos\alpha).
\end{aligned} \tag{6.1}
$$

$$
\mathbf F_{a,b}=\bar q S_{ref}
(-C_D\mathbf e_v+C_Y\mathbf e_y-C_L\mathbf e_z), \tag{6.2}
$$

$$
\mathbf M_{a,ref}=\bar q S_{ref}
\begin{bmatrix}b_{ref}C_l\\c_{ref}C_m\\b_{ref}C_n\end{bmatrix},\qquad
\mathbf M_{a,cg}=\mathbf M_{a,ref}
+(\mathbf r_{ref}-\mathbf r_{cg})\times\mathbf F_{a,b}. \tag{6.3}
$$

The reference-point shift occurs exactly once. A coefficient already referenced to current CG must not receive another CG correction. In ideal still-air force accounting, lift and side force in (6.2) are perpendicular to air-relative velocity; drag removes energy. That useful diagnostic does not imply that the total aircraft always loses ground-frame energy in a moving wind field.

**PHY-CONVENTION-01:** Compiled tables identify a closed, versioned coefficient-convention registry entry supported by the evaluator. The entry fixes force axes/basis and signs, moment axes and reference, fixed reference scales, angular units, rate normalization, surface signs, coefficient ordering, and contribution-inclusion rules. Free-text labels or a name such as `Cm_q` cannot select semantics. An authoring source using another convention must be converted once with provenance and conformance vectors, or rejected. Unknown or incompatible registry versions fail compilation/admission; they cannot fall back to a default. Exact registry encoding remains generated-schema work, not a new public ABI in this paper.

## 6.2 Required physical contributions

The target computes a bounded build-up rather than one enormous all-variable table:

$$
\mathbf C=\mathbf C_{base}(\alpha,M,\Lambda_s)
+\Delta\mathbf C_\beta
+\Delta\mathbf C_{surf}
+\Delta\mathbf C_{rate}
+\Delta\mathbf C_{config}
+\Delta\mathbf C_{asym}
+\Delta\mathbf C_{sep}
+\Delta\mathbf C_{ground}. \tag{6.4}
$$

This is a proposed factorization, not proof that the effects are independent. Here $\Lambda_s$ is an explicitly defined symmetric-sweep coordinate; the actual left/right angles remain available for asymmetry. Cross-effects that materially affect behavior must use an appropriate correction table or richer basis, with byte/cycle cost recorded. Do not multiply independent “bonuses” until an arbitrary response emerges.

| Contribution | Minimum obligation |
|---|---|
| Base/static | Lift, drag, side force and all three moments over the admitted state region; trim and static stability represented. |
| Sideslip | Lateral force, dihedral/roll coupling, directional stability, and material nonlinear sideslip behavior. |
| Actual surfaces | Signed effect of each admitted surface or explicitly validated combined control coordinate. |
| Rates | Natural aerodynamic damping and material cross-axis derivatives, retained in AUG_OFF. |
| Configuration | Flaps, gear, speedbrake, hook/stores and sweep effects where physically material. |
| Asymmetry/damage | Aerodynamic installation effects, differential sweep, asymmetric stores/surface loss and their admitted aerodynamic effects. Propulsive installation moments are excluded from this coefficient contribution. |
| Separation | Bounded nonlinear stall/departure behavior and deterministic hysteresis. |
| Ground effect | Height-dependent lift/induced-drag behavior from the same physical geometry/query frame. |

Propulsive installation moments are computed by (7.1) and added exactly once to the total applied moment. An aerodynamic installation effect may enter (6.4) only when its data definition excludes that propulsive contribution. The compiler/reference build-up records the owner and inclusion policy for each contribution; engine-out cases verify that thrust asymmetry is not counted again in an aerodynamic increment.

V3.3 explicitly requires $C_{m_q}$, $C_{l_p}$, $C_{n_r}$, $C_{l_r}$, and $C_{n_p}$ plus appropriate longitudinal, directional, and lateral static stability. Retain them unless a controlled revision proves an equivalent representation. Additional force-rate or unsteady terms are selected by sensitivity/error evidence, not added automatically. [P4, §7]

## 6.3 Derivative normalization and coupling

$$
\hat p=\frac{p b_{ref}}{2V_{safe}},\qquad
\hat q=\frac{q c_{ref}}{2V_{safe}},\qquad
\hat r=\frac{r b_{ref}}{2V_{safe}}. \tag{6.5}
$$

For example, $\Delta C_m=C_{m_q}\hat q$, while roll and yaw may each depend on both $\hat p$ and $\hat r$. A sideslip derivative is with respect to the explicitly stated angular unit. Labels such as `Cm_q` alone are insufficient metadata.

Near the healthy small-disturbance direct-flight envelope, the expected restoring tendencies include a stabilizing pitch response to increased AoA and a restoring yaw response to sideslip. Signs must be checked in this paper's axes and at the correct CG. Local derivative signs are useful diagnostics, not a complete stability certificate: trim, dynamic modes, nonlinear behavior, actuators and numerical integration must also be tested.

**PHY-AERO-01:** A yaw/roll coupling test must exercise the actual side-force/moment coefficients and inertia terms, not an artificial kinematic bank command. A model with all cross-derivatives defaulted to zero is not automatically a valid simplified fighter.

## 6.4 Drag and energy bookkeeping

Declare whether each supplied baseline drag table already includes induced drag, wave/compressibility drag, and particular configuration effects. A parabolic contribution $k C_L^2$ is permissible only when it represents an identified missing contribution within its validated domain. Do not add it again to total drag from a solver that already includes it.

A constant $k=1/(\pi e AR)$ is at most a justified approximation for an identified region; it is not a universal high-AoA, transonic, sweep-varying drag law. Profile/viscous drag, interference, compressibility and separation often require additional data or calibrated corrections. A subsonic potential-flow result cannot be extrapolated into a whole supersonic fighter envelope merely by adding Mach as a table axis. [R5, R8]

Validate level-flight thrust/drag balance, acceleration, idle descent, sustained turns, climbing turns and configuration changes. When a claimed maximum-G maneuver cannot be sustained, speed must decay according to force and energy, not be held at an advertised target.

## 6.5 Stall, departure, and asymmetry

A memoryless clipped lift slope creates an abrupt, rigid-feeling stall. Retain a bounded separation state or hysteresis representation as required by v3.3. A practical candidate is an attached/separated blend with distinct onset/recovery conditions and a bounded lag. Its coefficients, rates, and mixing are authored data. Include all authoritative lag state in replay/checksum ownership.

The model must distinguish a validated ordinary-flight region, an approved unaugmented region, and a bounded degraded/out-of-domain continuation. Beyond validated data, continue without arithmetic failure or instantaneous recovery, record the validity state, and do not claim quantitatively accurate spin/departure prediction. Backward flight and near-zero speed need deliberate handling rather than array overrun or unbounded extrapolation.

Differential sweep must affect the aircraft. A mean-sweep lookup alone is insufficient. A candidate low-cost representation uses symmetric sweep plus signed differential-sweep corrections; mirroring tests require the appropriate roll/yaw/side-force terms to reverse while symmetric terms retain their parity. Large asymmetry needs its own validity limits and tests.

## 6.6 Interpolation and boundaries

Use deterministic piecewise-linear interpolation as the first candidate. Breakpoints are strictly ordered; a constant dimension is explicitly declared. Store axis order, coefficient order, strides, units, quantization, endpoint inclusion, and out-of-range policy. “CSV file” alone does not define a table.

Cell search has a proven bound. Cache cell indices if useful, but invalidate them on model changes. Interpolation weights are nonnegative in the admitted cell, sum consistently, and use a specified evaluation/rounding order. Avoid an unconstrained spline that overshoots between plausible samples. Adaptive sample placement is an offline operation, not an unbounded runtime solver.

**PHY-TABLE-01:** An out-of-domain policy is per table family: bounded physical continuation, explicit clamp of the *lookup coordinate* where justified, or rejected model/admission. Clamping a lookup is not permission to clamp the aircraft's attitude, speed, or energy to the table boundary. Missing table entries cannot be inferred as zero.

# 7. Propulsion, sweep, and aircraft systems

## 7.1 Installed engines

Each engine has its own operating state, throttle eligibility, spool state, fuel flow, damage, and installed thrust. At minimum the data describe net thrust versus the declared atmospheric/Mach/engine-state variables, dry/afterburning operation, response dynamics, idle/windmilling effects where material, and the supported start/flameout/relight rules. [P2, §8]

A throttle lever is a command, not instantaneous thrust. Use a bounded response model such as separately scheduled spool-up/down lag and rate limits, validated against the intended response envelope. Do not extrapolate thrust below idle or beyond AB limits through an unconstrained polynomial.

For engine $i$ with thrust $T_i$, body direction unit vector $\mathbf d_i$, and location $\mathbf r_i$:

$$
\mathbf F_{eng}=\sum_i T_i\mathbf d_i,\qquad
\mathbf M_{eng}=\sum_i(\mathbf r_i-\mathbf r_{cg})\times T_i\mathbf d_i. \tag{7.1}
$$

An engine failure therefore changes yaw/pitch moments without a scripted “engine-out yaw” term. Net installed thrust data must state whether intake losses and ram drag are already included; fuel-consumption and thrust calculations cannot double-count momentum effects.

## 7.2 Supplies and actual surfaces

The systems owner maps electrical/hydraulic/engine capability into actuator availability. Each control surface has a position, physical stops, rate/lag behavior, positive-deflection definition, and failure disposition. A jam retains a position; loss of authority is not necessarily the same failure. Declared supply interactions and degraded rates apply before forces are evaluated.

Wing sweep uses actual left/right positions, independent rate-limited hydraulic motion and approved auto/manual commands. Automatic sweep does not teleport geometry. Aerodynamic and mass schedules reference the same actual sweep state and source model. Manual return to Auto must not discontinuously change the aircraft merely by changing a selector.

## 7.3 Configuration and damage

Flap Up/Half/Full, protective retraction with hysteresis when available, gear overspeed damage rather than magical retraction, speedbrake, hook, startup prerequisites and failure causes remain Gameplay-owned behavior. [P2, §8]

Damage changes a declared physical or capability property. It must not add an arbitrary force merely because a health percentage decreased. Supported approximations may include lost surface authority, altered area/drag, engine degradation or asymmetric sweep, but each has data, a valid range, deterministic application, and a verification case. This paper does not add random reliability failures.

# 8. Flight-control system and handling

## 8.1 Preserve the separated state model

| Logical state | Meaning retained |
|---|---|
| `ControlContext` | Deck/TFL/normal-flight/combat input and presentation semantics; not a physical law. |
| `FCSMode` | Pilot-selected `AUGMENTED` or `AUG_OFF`. |
| `FCSStatus` | Delivered capability `NORMAL`, `DEGRADED`, or `DIRECT_ONLY`. |
| `ADLCState` | `OFF`, `CAPTURE`, `TRACK`, `DEGRADED`; failure is represented by an explicit limiting/failure reason in the Runtime mapping. |
| Autothrottle | Independent capture/override/disengagement state. |
| Pilot trim | Persistent pilot intent, separate from automatic-control memory and transfer bias. |

A commanded AUGMENTED switch can coexist with DIRECT_ONLY capability. A failure does not secretly rewrite the switch. The Runtime's ADLC failure-reason mapping avoids inventing a competing top-level FAILED enum. [P1, §7; P2, §7; P3, §11]

## 8.2 Augmented command path

Longitudinal input requests scheduled normal acceleration; lateral input requests scheduled roll rate. Available yaw coordination/damping, automatic trim and G/AoA protection operate through the same mixer, hydraulics, and actual actuators as every other command. The controller cannot write attitude, velocity, aerodynamic force, or a higher control limit directly.

Schedules must state their independent variables and units. Gains, command ramps, feedback filters, saturation, anti-windup, trim limits and capability fallbacks are data. Tune and verify them with the exact sample age specified in §1.3, not a zero-delay desktop controller that behaves differently on target.

**PHY-FCS-01:** Neutral longitudinal input requests the scheduled trim/approximately 1-G demand where appropriate, not an altitude, attitude or flight-path hold. Protection limits demands rather than clipping measured motion after integration. An impossible G command saturates available authority and incurs the actual resulting energy/trajectory consequence. Digital-input shaping belongs to the approved input/control boundary; it cannot secretly differ by render frame rate.

## 8.3 Direct flight

AUG_OFF removes closed-loop G/rate command, artificial FCS damping and G/AoA protection. It retains non-augmenting mixer/gearing, pilot trim, supplies, actual actuators, limits, damage and natural aerodynamic stability. A fixed or flight-condition-scheduled control gearing is not automatically augmentation; feedback from achieved rates/G used to stabilize the aircraft is. [P4, §8]

The healthy airframe must be controllable within `F65_UNAUGMENTED_FLIGHT_ENVELOPE`. That envelope is a multidimensional data product, not a single minimum/maximum speed. It includes permitted loading/CG, configuration, sweep, altitude/Mach or dynamic pressure, AoA/sideslip and capability assumptions. It does not promise carefree direct handling everywhere the augmented aircraft can survive.

## 8.4 Degradation mapping

The model package includes a capability-to-effective-control table. For each supported sensor, axis, supply, and actuator failure combination, identify legal feedback, disabled protections, direct fallback, trim availability, ADLC disposition and annunciation reason. Undefined combinations fail conservatively and visibly under an approved rule; they do not revert to a hidden healthy law.

This closes a mapping obligation identified by the AI paper without giving AI different physics. AI guidance is translated into legal control intent and is limited by the same available aircraft response. [P8, §§7–8, 27.2]

## 8.5 Bumpless transfer

At AUGMENTED-to-AUG_OFF transfer, preserve actual surfaces and initialize a bounded transfer bias from the outgoing command minus the incoming direct stick-plus-trim command. Keep this bias separate from `PilotTrimState`; decay it deterministically to zero while pilot trim remains unchanged. Freeze/reset outgoing integrators appropriately. On re-entry, initialize controller memory from current state rather than requesting an instant recovery.

“No snap” constrains command-transfer artifacts, not the physical consequences of a real jam, lost surface, collision or engine failure. Such events can legitimately change force or acceleration. Validation isolates a pure mode change from a concurrent physical fault.

## 8.6 ADLC and autothrottle

ADLC remains an approach overlay. AUG_OFF selection disengages it before direct authority becomes effective. Loss of required capability degrades/disengages it with a reason, not an invisible fallback controller. Its AoA/flight-path/throttle interaction must remain within real surface and thrust authority. [P1, §7.8; P2, §15; P3, §11.5]

Conventional autothrottle captures KIAS using the defined air-data model and modulates through military power. Pilot afterburner override and recapture follow Gameplay. Independent state does not mean uncontrolled competition: the arbitration between pilot throttle, conventional autothrottle and ADLC has exactly one eligible demand at stage 5.

## 8.7 Load factor and feel

For the proposed CG-based normal-load signal during free flight:

$$
n_z=-\frac{F_{non\text{-}gravity,z}}{m g_0}. \tag{8.1}
$$

This is not simply $-\dot w/g_0$: the body acceleration equation also contains gravity and rotating-frame terms. Contact impulses contribute through the declared contact/load reporting boundary. A pilot-location accelerometer correction, if needed, has an explicit offset and angular-acceleration model rather than an unexplained camera effect.

Test smooth command onset, believable lag, sustained-turn energy loss, roll damping, recovery from disturbance, trim workload, sweep transitions, engine-out and approach corrections. Add neither excessive input smoothing that makes the aircraft rigid nor random disturbance that disguises a bad model. Audio and visual cues should report these physical effects, not substitute for them.

# 9. Six-degree-of-freedom dynamics and integration

## 9.1 Continuous reference equations

Let $\mathbf F$ be the sum of non-gravitational forces about the CG, $\mathbf M$ the total moment about CG, $\boldsymbol\omega=(p,q,r)$, and $\mathbf g_n=(0,0,g(h))$. For the declared local non-rotating NED approximation:

$$
\dot{\mathbf v}_b=\frac{\mathbf F_b}{m}+\mathbf R^T\mathbf g_n
-\boldsymbol\omega\times\mathbf v_b. \tag{9.1}
$$

$$
\mathbf I\dot{\boldsymbol\omega}
=\mathbf M_b-\boldsymbol\omega\times(\mathbf I\boldsymbol\omega)
\quad\text{for quasi-static inertia}. \tag{9.2}
$$

Gravity is added exactly once. If a helper produces “total body force” including gravity, its interface must say so and (9.1) must not add gravity again. The canonical v4 force accumulator excludes gravity.

For the reduced tensor (4.3), define $\mathbf b=\mathbf M-\boldsymbol\omega\times(\mathbf I\boldsymbol\omega)$ and $D=I_{xx}I_{zz}-I_{xz}^2$. Then

$$
\dot p=\frac{I_{zz}b_x+I_{xz}b_z}{D},\qquad
\dot q=\frac{b_y}{I_{yy}},\qquad
\dot r=\frac{I_{xz}b_x+I_{xx}b_z}{D}. \tag{9.3}
$$

This explicitly preserves inertia coupling without a general matrix inversion each tick. A full-tensor model uses a bounded admitted solve or validated inverse representation. Time-varying mass/inertia corrections follow §4.4; (9.2) does not claim to include them.

## 9.2 Attitude and position

For the Hamilton, scalar-first body-to-NED quaternion:

$$
\dot{\boldsymbol\eta}=\tfrac12\boldsymbol\eta\otimes(0,p,q,r). \tag{9.4}
$$

$$
\mathbf R=
\begin{bmatrix}
1-2(\eta_2^2+\eta_3^2)&2(\eta_1\eta_2-\eta_0\eta_3)&2(\eta_1\eta_3+\eta_0\eta_2)\\
2(\eta_1\eta_2+\eta_0\eta_3)&1-2(\eta_1^2+\eta_3^2)&2(\eta_2\eta_3-\eta_0\eta_1)\\
2(\eta_1\eta_3-\eta_0\eta_2)&2(\eta_2\eta_3+\eta_0\eta_1)&1-2(\eta_1^2+\eta_2^2)
\end{bmatrix}. \tag{9.5}
$$

$$
\dot{\mathbf x}_n=\mathbf R\mathbf v_b,\qquad \dot h=-\dot x_D. \tag{9.6}
$$

The matrix assumes a normalized quaternion. Deterministic normalization, norm-error limits, sign continuity and zero-norm fault behavior are specified by the numeric contract. Equivalent quaternions $\boldsymbol\eta$ and $-\boldsymbol\eta$ represent the same attitude, but a checksum/serialization policy must choose reproducible handling. Euler angles are derived presentation/diagnostic values, not the singular authoritative integrator.

## 9.3 Discrete candidate and selection gate

The published step is always $\Delta t=1/100$ second. V3.3 proposed semi-implicit Euler with an RK2 comparison; no accepted production integrator or tolerance is present in the inspected corpus. [P4, §11]

**Proposed v4 baseline for evaluation:** retain body velocity as the declared state but perform the translational kick in NED, then transform back using the updated attitude. This is an equivalent rotating-frame formulation that avoids a needless free-flight velocity error from separately approximating the $-\boldsymbol\omega\times\mathbf v_b$ term:

$$
\begin{aligned}
\boldsymbol\omega'&=\boldsymbol\omega+\Delta t\,\dot{\boldsymbol\omega},\\
\boldsymbol\eta'&=\operatorname{normalize}
\left(\boldsymbol\eta+\tfrac12\Delta t\,
\boldsymbol\eta\otimes(0,\boldsymbol\omega')\right),\\
\mathbf v'_n&=\mathbf R\mathbf v_b+\Delta t(\mathbf R\mathbf F_b/m+\mathbf g_n),\\
\mathbf x'_n&=\mathbf x_n+\Delta t\,\mathbf v'_n,\\
\mathbf v'_b&=\mathbf R'^{T}\mathbf v'_n.
\end{aligned} \tag{9.7}
$$

Forces/moments in this candidate come from stage 8 at the declared sample. Equation (9.7) is a first-order candidate, not a claim of symplectic conservation for arbitrary rotational dynamics. The extra transformations have a measurable cost. Compare it with the retained v3.3-style body-axis candidate and a fixed-step midpoint/RK2 reference candidate on the same hard cases. Choose the least expensive implementation that meets approved numerical and handling tolerances.

A higher-order candidate must define which continuous forces it reevaluates and must not rerun discrete input, fuel expenditure, weapon events or lifecycle commits during its internal evaluations. No adaptive, load-driven time step is admitted. Fixed internal substeps would require an explicit bounded design and measured acceptance while retaining the single external 100 Hz timeline; they are not assumed here.

## 9.4 Acceptance hazards

The acceptance set includes ballistic motion, torque-free rotation, sustained high-rate rotation, long trimmed flight, high-AoA recovery, rapid sweep, asymmetric loading, maximum-rate surfaces, engine transients, and hard contact. Check quaternion norm, frame orthogonality, energy/work consistency, divergence under step refinement, and fixed-point drift.

A clamp is an overflow/invalid-state guard or a real physical stop. It is not an artificial speed, attitude, G, or energy correction used to make an unstable solver appear stable. A fault retains diagnostic context and follows the Runtime's controlled behavior; do not silently reset the aircraft to wings level.

# 10. Contact, ground effect, and carrier operation

## 10.1 Registered geometry

Terrain queries, contact geometry and displayed landmarks use the same canonical world/carrier transforms. The graphics mesh need not match collision geometry polygon for polygon, but runway/deck edges, landing area, gear/hook points and catapult references must register within approved tolerances. [P1, §§3, 10; P3, §10; P5]

At a body-fixed contact point $\mathbf r_c$ relative to CG, aircraft point velocity is

$$
\mathbf v_{point,n}=\mathbf v_{cg,n}+\mathbf R(\boldsymbol\omega\times\mathbf r_c).
\tag{10.1}
$$

Subtract the supporting surface's velocity at the same location, including its admitted rigid rotation when present. Do not treat a moving deck as stationary Earth or subtract wind from tire-relative velocity. Secured deck aircraft inherit carrier motion through the contact/attachment contract, not through a second integrator.

## 10.2 Stage-10 response

The free-flight update occurs at stage 9 and contact resolves at stage 10. Contact cannot inject an unexplained stage-8 force based on future state. An admitted contact method returns bounded corrections/impulses through the generated boundary; FlightDynamics remains the owner of aircraft motion.

A practical candidate uses wheel/contact points and bounded normal/friction response, without a general-purpose rigid-body stack solver. For an impulse $\mathbf J_n$ at a point, the corresponding velocity and angular-momentum changes obey
$\Delta\mathbf v_n=\mathbf J_n/m$ and
$\Delta\mathbf H_b=\mathbf r_c\times\mathbf R^T\mathbf J_n$.
Its contact iteration count, restitution, penetration correction and force/impulse reporting are explicit. Verify that friction/restitution do not add uncommanded energy; account separately for legitimate work by a moving deck or catapult.

Contact stiffness, damping and friction values cannot be selected independently of the 10 ms step and expected closure speeds. Test stable rest, taxi, braking, touchdown, bounce, edge departure, crosswind rollout and damaged gear. Ground contact is not a script that forces the aircraft onto a predefined approach path.

## 10.3 Ground effect

Retain the v3.3 ground-effect obligation, using height relative to the actual supporting surface and a declared span/height normalization. Ground effect may modify induced drag and, where supported, lift/moment. Identify whether the baseline data already includes it. A carrier below the aircraft and sea outside the deck must not be conflated by a single infinite ground plane.

Exact corrections remain data. They must blend continuously and cannot create lift at zero dynamic pressure or make an aircraft hover near the deck.

## 10.4 Catapult and arrestment

Catapult and arresting forces/impulses are external contact effects with real application geometry, finite work and finite duration. Hook deployment, wire intersection, legal capture, bolter and failure follow Gameplay. A failed capture leaves a flying aircraft, not a teleported landing. Arrestment loads and stopping distance must agree with mass, speed and the admitted response model.

Wave-driven carrier heave/pitch/roll remains out of scope. This paper does not add it because a deck-velocity equation can represent it. [P2, §§6, 15]

# 11. Lower-cost physical classes and shared 3DOF motion

## 11.1 KINEMATIC aircraft

KINEMATIC means a bounded lower-cost physical approximation selected at mission load, not a decorative object. The aircraft remains on the 100 Hz timeline, has physical position/velocity, participates in sensors/contact/lifecycle, and remains owned by FlightDynamics. The rescue/civilian/AIC baseline does not authorize a full helicopter rotor model. [P2, §4; P3, §§7, 11.6]

Its model declares rate/acceleration/climb/turn limits and how guidance requests become achievable motion. It must not teleport between waypoints or use render interpolation as truth. Exact approximation/tuning remains a separate admitted data/model choice. Do not switch a combat aircraft to KINEMATIC because it is distant or expensive.

## 11.2 Point-mass physical primitive

WeaponAndDamage owns authoritative weapon state and guidance. A reusable stateless math routine may evaluate point-mass physics, but calling it does not transfer ownership to FlightDynamics. Sensor assessments retain the one-tick handoff required by the Runtime; physical truth is not substituted for missing legal guidance information. [P1, §9; P3, §12; P7, §§1–4]

A generic translational body has position, ground-relative velocity, mass, propulsion phase, and bounded lateral-force response state as required. With air-relative direction $\mathbf e_v$:

$$
\dot{\mathbf v}_{g,n}=\mathbf g_n+
\frac{T\mathbf e_T-D\mathbf e_v+\mathbf F_\perp}{m},
\qquad \mathbf F_\perp\cdot\mathbf e_v=0. \tag{11.1}
$$

For the baseline reduced model, thrust follows a declared flight-axis approximation; the absence of attitude state does not authorize instantaneous independent thrust vectoring. The normal-force demand is projected into the air-velocity-normal plane and limited by available aerodynamic authority, dynamic pressure, response lag, and the admitted structural/model envelope. A demanded turn is not an instantaneous rotation of the velocity vector. At low dynamic pressure, aerodynamic turning authority must diminish unless an explicitly modeled non-aerodynamic mechanism exists; none is added here.

## 11.3 Maneuver energy is required

A bounded drag model may use a declared normal-force coefficient and a validated induced-drag contribution:

$$
C_N=\frac{\|\mathbf F_\perp\|}{\bar q S_{ref}},\qquad
D=\bar q S_{ref}\,[C_{D0}+k_N C_N^2], \tag{11.2}
$$

only inside its applicability region and only when induced drag is not already included. Handle $\bar q\rightarrow0$ without division failure. More appropriate admitted tables may replace this simple polar. Propulsion phase, mass depletion and coast drag change energy continuously; no constant-speed correction restores energy after a maneuver.

The 3DOF model omits attitude/rate dynamics; its lateral-response approximation therefore needs its own validation. It is not a full 6DOF model with three arrays removed. Guidance, loft policy, seeker/target behavior, fuze, damage and real-weapon performance remain outside this paper. No new weapon requirement or invented missile dataset is introduced.

# 12. Fixed-point execution and hardware fit

## 12.1 Numeric registry contract

Do not choose one fixed-point format for everything. Position, velocity, quaternion components, rates, coefficients, mass/inertia and force accumulators have different range and resolution needs. For each generated numeric quantity specify physical unit, signedness, scale, valid range, intermediate width, rounding, narrowing, saturation/fault behavior and conversion ownership. [P1, §4; P3, §§2, 5–6]

Authoritative code cannot depend on C signed overflow, implementation-defined right shifts of negative values, unspecified evaluation order, host floating-point rounding mode, or native structure packing. Widen before multiplication and verify intermediate bounds. Table interpolation, trigonometric approximations, normalization, reciprocals and division require bit-exact vectors including endpoints and negative operands.

Target code is readable C first. Use named quantities and units, small owner-specific routines, explicit mutation and the repository's C style. An assembly kernel must preserve the same numeric contract and demonstrate a necessary platform/cost benefit. A hardware multiply/divide facility is used through an admitted wrapper; its presence does not prove a whole flight model meets deadline.

## 12.2 What must be resident

Mutable authoritative aircraft state remains in the approved fast-memory owner layout. The total active-simulation region is shared with entities, systems, SensorTrack, handoffs, AI and other owners; it is not 32 KiB exclusively for flight dynamics. Attic is cold resource storage, not a substitute authoritative-state heap. The 32 KiB measured-limits reserve is not spare aircraft-table capacity. [P1, §5; P3, §6]

Mission-load admission resolves the live type set and required hot data before it can be used. Share immutable tables by model revision, not by copying them into every aircraft instance. All mandatory evaluation data must meet its declared residency/access contract before the sortie or before the type becomes live. No unbounded disk or Attic fetch may block an ordinary force evaluation.

Read-only coefficients, scratch, compiler support, lookup indices, controller memory, surfaces, lag states, and generated headers all have a byte owner. Include alignment, metadata and build-profile overhead in the ledger. Do not account only for raw coefficient cells.

## 12.3 Why table factorization is not optional bookkeeping

The following are **storage illustrations, not selected grids or approved budgets**:

- A dense grid with 17 AoA nodes, 9 sideslip nodes, 8 Mach nodes, 7 sweep nodes, 3 configurations, 6 coefficients and 2 bytes/value contains **308,448 bytes** before metadata or control/rate terms.
- A factored base with 17 AoA nodes, 8 Mach nodes, 7 sweep nodes, 6 coefficients and 2 bytes/value contains **11,424 bytes**. Five rate derivatives over 8 Mach by 7 sweep nodes add **560 bytes** before metadata.

The second example is not a complete aircraft database. Sideslip, surfaces, configuration interactions, separation, asymmetry and validation may require more. It demonstrates why offline error-guided decomposition matters. Fitting a base table does not prove the required set of live aircraft types fits the platform.

## 12.4 CPU and deadline evidence

Measure force evaluation, air-data lookup, mass-property updates, FCS/actuators, integration, contact and worst legal invalid-data paths. Record per-call maxima and combined legal workloads, not only averages or an isolated aircraft benchmark.

Acceptance includes the parent's combined profile: nine aircraft, sixteen guided missiles, twenty-four gun groups, forty-eight decoys, required sensor/AI work and protected presentation. Production budgets are set by the measured-limits process. R0 synthetic workload or remaining bytes in a proof executable are not permission to spend those resources in the production engine. [P3, §§7–8; Appendix D]

If the model does not fit, first inspect table factoring, shared computations, state layout, lookup strategy and measured C offenders. Any reduction must retain approved physical behavior within a stated error envelope. Do not reduce the physical clock, change class at runtime, borrow reserve silently, or replace the aircraft with a scripted response.

# 13. Aircraft-data authoring, compilation, and admission

## 13.1 A repository-based workflow

Keep the editable definition in ordinary text files inside the repository. No bespoke GUI or new database service is required. The following is a **proposed layout**, to be adapted to existing repository ownership during implementation:

```text
assets/physics/aircraft/<model_id>/
    aircraft.json            identity, geometry, mass, systems, table catalog
    tables/*.csv             explicit axes/columns; normalized authoring data
    sources.json             provenance, transforms, licenses, uncertainty
    validation/*.json        load cases, trim/response targets, envelope cases

build/physics/<model_id>/
    compiled package         generated target representation
    admission report         validation results and resource accounting
    generated vectors        high-precision and bit-exact test inputs/results
```

Logical schema and numeric-registry sources belong with the existing generated-contract tooling, not in a second handwritten header tree. Exact filenames/encodings are an implementation decision. Generated packages do not replace human-reviewable inputs.

## 13.2 Nine-step data pipeline

**1. Define the aircraft and intended envelope.** Resolve geometry identity, empty-weight contents, loading stations, systems/configuration vocabulary, intended operating region, and source availability. Keep the product's target performance separate from computed performance.

**2. Collect and classify sources.** Retain source files or reproducible retrieval identities and licenses. Record assumptions and applicability for each input. Do not import unrelated-aircraft coefficients as F-65A truth without explicitly labeling the approximation.

**3. Normalize.** Convert units, axes, control signs, reference scales, moment origin, angle conventions, derivative normalization and operating-condition definitions. Preserve raw source values separately; normalized tables are derived artifacts with traceable transformations.

**4. Build a high-precision reference model.** Use analytic, semi-empirical, numerical-analysis and deliberately tuned inputs where appropriate. Trim and exercise the full model. The reference does not acquire credibility merely by using double precision; it must also have independent physical checks and defensible data.

**5. Resolve missing physics.** Identify missing drag, dynamic derivatives, control effectiveness, high-AoA continuation, asymmetric loading and engine-response data. Perform targeted analysis or author bounded approximations. Never fill missing fields with zeros simply to complete a CSV.

**6. Reduce to target tables.** Choose factorization, breakpoints and compact state to meet an explicit error budget over an independent validation set. Preserve derivatives and continuity around trim, stalls, sweep transitions and control limits, not only average coefficient error.

**7. Quantize and compile deterministically.** Generate target data and bindings from normalized inputs and the approved numeric registry. Fix ordering, rounding and endpoint rules. Two builds from identical inputs/tool identities must have identical payload bytes.

**8. Cross-validate and measure.** Compare high-precision physics, bit-exact host reference and target C. Then run the admitted target/emulator/hardware tests and full resource overlap. A compiler success is neither aircraft validation nor hardware admission.

**9. Review and release a model revision.** Approve the data, envelope, errors, resource fit and handling evidence together. Pin the source bundle, generator, numeric contract and compiled package identities. Mission compilation selects that exact revision.

This pipeline extends the parent's high-precision reference -> bit-exact host -> C -> measured assembly method to aircraft data. It does not require target code to parse CSV, JSON, XML or an external solver's expression language. [P1, §2.3; P3, §§2, 5, 17]

## 13.3 Offline tools: useful evidence, limited authority

Digital DATCOM provides a historical semi-empirical route to static/dynamic and control characteristics subject to method and configuration limits. OpenVSP/VSPAERO provides geometry-based potential-flow analysis, with explicit reference scales and solver-version dependencies. Use these as candidate data sources in the regions they support, not as an automatic F-65A generator. [R5, R8]

A useful workflow may combine geometry analysis, empirical drag/correction data, analytical mass properties, and bounded authored nonlinear behavior. It must state what has **not** been resolved, especially transonic drag/moment changes, separated flow, complex twin-tail/sweep interactions, propulsion installation and dynamic derivatives. Low-Reynolds-number airfoil analyses are not a whole-envelope basis for this supersonic fighter; no such tool is mandatory here.

Selection of the actual offline tool/version is a later reproducibility decision. Reference-model independence matters: running the same erroneous generated equations in two languages is not independent aerodynamic validation.

## 13.4 Table and package validation

The authoring/compiler path must reject at least:

- unknown required units, axis conventions, moment origins or reference scales;
- missing required fields, placeholder/null shipping values, non-finite numbers, malformed shape/stride, duplicate or unsorted breakpoints;
- unsupported coefficient/derivative conventions or missing control-sign mappings;
- invalid mass, impossible tank/station loads, invalid CG region or nonphysical/ill-conditioned inertia;
- incomplete valid-domain coverage, undeclared extrapolation, contradictory configuration/capability combinations;
- coefficient double counting, a missing mandatory stability term without approved equivalence, and unreviewed test-only data in a release package;
- fixed-point overflow risk, unacceptable interpolation/quantization error, stale generated bindings or incompatible model/schema/numeric versions;
- mission-hot data, state, scratch, code or cycle costs exceeding admitted owner budgets.

Not every physical concern can be proved by a generic validator. The report distinguishes automatic structural checks, analytic checks, trajectory tests and human-reviewed judgments. Monotonicity checks apply only where the physics requires them; lift is not globally monotonic through stall.

## 13.5 Release and mission-load contract

The model package records a model ID/revision, schema/numeric-contract versions, source/generator identities, table directory and lengths, supported configurations, validity/envelope IDs, integrity checks and resource witness. Exact byte offsets and widths are generated; do not freeze them in this prose.

Load-time validation checks package integrity, compatibility, required tables, model class, requested loadout/CG/configuration, resident data availability and combined mission capacity. It fails before the active clock for inadmissible mandatory content. A rejected model is not silently replaced by a default fighter.

Hot reload during a sortie is not admitted. Model revision changes produce a new deterministic run. Authoritative checksum/replay identity must include the effective physical model/data revision, so a replay cannot quietly run against changed coefficients.

## 13.6 Practical tuning order

Tune in a sequence that exposes causes: mass/geometry and units; steady lift/drag/trim; static and dynamic response with augmentation off; propulsion and energy performance; actual actuator behavior; augmented gains and limits; configuration/sweep; asymmetry/damage; approach/contact; then integrated presentation feel.

Do not start by fitting a G-command controller to conceal an untrimmed or unstable physical airframe. Do not tune separate AI coefficients to make combat opponents easier. Shared model/data produce shared physical capability; behavior/difficulty remains an AI decision matter. [P2, §3.2]

# 14. Verification, validation, and pilot acceptance

## 14.1 Four questions, four kinds of evidence

**Mathematical verification:** Do frames, equations, units and numerical operations implement the specified model?

**Data validation:** Are geometry, mass, coefficients and schedules internally consistent and sufficiently supported over the admitted domain?

**Target verification:** Does compiled target code reproduce the approved bit-exact model while meeting hardware memory/timing/lifecycle obligations?

**Product validation:** Does the resulting aircraft meet the intended operating/handling targets without cheating the physical model?

Passing one does not answer the other three. The independent high-precision and bit-exact host references remain necessary where the parent requires them. NASA's 6DOF check-case work provides a useful independent benchmark pattern, with explicit vehicle, frame, environment, initial-condition and trajectory definitions. Any comparison must match those assumptions and record adaptations; this document does not claim a NASA check-case pass. [R9]

## 14.2 Minimum acceptance catalog

| Family | Required cases and failure signals |
|---|---|
| Frames and units | Axis-basis rotations, quaternion/DCM round-trip, positive control signs, wind transforms, derivative unit conversions, reference-point moment shift. |
| Mass/loading | Empty/full/landing cases, fuel-feed CG travel, mirrored asymmetry, expenditure/rejection, sweep schedules, tensor positivity after quantization. |
| Environment/air data | Reference atmosphere nodes, temperature variation, layer boundaries, still/steady/shear wind, sonic pitot transition, low-speed invalidity, IAS failure behavior. |
| Aerodynamics | Trim curves, six channels, control increments, mandatory rate derivatives, parity, stall onset/recovery, transonic continuity, ground effect, out-of-domain continuation. |
| Integrator | Ballistic/free motion, torque-free and forced rotation, step refinement, long-duration drift, zero-force frame invariance, quaternion norm and signed overflow traps. |
| FCS | Commanded mode versus capability, direct flyability, sensor/axis failure combinations, saturation/anti-windup, transfer-bias decay without trim mutation, ADLC/AB arbitration. |
| Energy and propulsion | Trimmed level flight, idle descent, accelerations, sustained/high-G turns, thrust/fuel/AB transitions, engine-out sign, no artificial speed restoration. |
| Contact/carrier | Rest/taxi/braking, runway and deck touchdown, moving deck, hook capture/bolter, catapult work, gear damage, penetration/energy bounds. |
| 3DOF/KINEMATIC | Shared wind/gravity, finite turn response, coast/depletion, maneuver drag, no teleportation, correct mission-class and lifecycle behavior. |
| Determinism and resources | Repeat runs, pause/resume, render-load changes, PAL/NTSC, model revision mismatch, stale caches, maximum legal overlap and fault paths. |

A golden vector includes full input state, model/data version, eligible command ticks, exact numeric contract, expected outputs and tolerance class. A screenshot or “felt good” is not a substitute for its numerical record.

## 14.3 Error budget

Approve errors by observable quantity and operating region, not one universal percentage. At minimum distinguish coefficient approximation, interpolation, fixed-point quantization, integrator truncation, omitted physical terms, controller sample delay and contact discretization.

Use absolute errors near zero and relative errors only away from zero. Include steady trim residual, rate/attitude response, position/velocity divergence over named durations, energy/work residual, quaternion norm and FCS transfer continuity. A small mean coefficient error may still produce an unacceptable pitch-trim or departure error.

All production tolerances remain **TBD** until the owner approves an error budget and test catalog. The authoring process must define that budget before optimizing the final table set. Appendix B's arithmetic fixtures verify their stated calculations; their tolerances are not aircraft-fidelity limits.

## 14.4 Data completeness gates

**Definition-ready:** geometry, units/frame, mass inventory, supported systems and intended envelope are explicit. Missing values are visible.

**Reference-ready:** the high-precision model can trim and run the required envelope tests, with provenance and limitations recorded.

**Target-ready:** normalized data, compact representation and fixed-point reference agree within approved tolerances; generated formats and resource witnesses are complete.

**Aircraft-admitted:** target and required hardware evidence pass, handling is accepted, and the exact model revision is approved for named missions/envelopes.

These are model-data checkpoints, not renamed R0 program gates. A reference-ready model can support offline research without being admitted to production.

## 14.5 Qualified-pilot and founder handling review

Gameplay §21.4's qualified-pilot acceptance requirement remains mandatory, including the healthy AUG_OFF envelope. Founder/product review is complementary and does not substitute for that requirement. Record the qualified-pilot assessment and founder disposition separately against the same model identity and repeatable cases.

Use repeatable scenarios and record starting mass, CG, sweep, configuration, altitude, airspeed, weather, control mode, device mapping and model revision. Review normal maneuvering, direct trim, pitch/roll/yaw disturbances, sustained turns, rapid configuration changes, engine-out, near-stall recovery, approach corrections, flare/touchdown, catapult and bolter.

Separate objections into physical-model behavior, controller behavior, input shaping, and presentation/latency. A slow display can feel like bad physics; a bad controller can feel like an unresponsive airframe. Instrument those boundaries before changing coefficients. Preserve accepted regressions when tuning a new case.

The acceptance goal is neither “easy” nor “difficult.” It is understandable aircraft response: the pilot can perceive energy, inertia and authority, predict the consequence of commands, and recognize why an aircraft departs or cannot sustain a demand.

# 15. Implementation and controlled adoption

## 15.1 Build in bounded slices

First implement the authoring schema, unit/frame conversion and small mathematical fixtures. Then build the high-precision trim/flight reference and the bit-exact numeric primitives. Introduce target table evaluation and a minimal force/integration path; add actual systems/FCS/contact through the owning stages. Admit realistic F-65A data only after those boundaries are testable.

Production phases remain those in the core three. Phase-1 harness work consumes shapes, ownership, failure and residency contracts through bounded fixtures. Phase-2 work supplies the actual flight/systems data and validated aircraft model. Shared 3DOF primitives do not authorize early production weapons or additional combat scope. [P1, §§18–20]

No repository-wide C restyle, new general engine framework, new scheduling clock, or redesign of proven R0 platform code is required to implement this paper.

## 15.2 Current authority and historical provenance

The canonical Markdown and generated reading PDF are recorded separately in `spec/manifests/spec-corpus.json`. Main v1.7, Gameplay v1.1, Runtime v1.1 candidate amendment and AI v1.1 amendment carry the coordinated current references. CURRENT_STATE, README and the current-authority table in F65_OFFICIAL_RECORD identify this baseline.

Physics v3.3 remains unchanged provenance. Historical R0 evidence, source-input appendices and frozen checkpoint copies keep their original references and hashes. No old run is relabeled as v4 evidence. The manifest retains both identities; a future revision requires deliberate approval and identity updates.

Runtime owns adopted sampling/handoff and package-admission integration. This specification owns physical detail. Numeric candidates, generated representations and measured allocations still require the stated evidence and approval gates; document adoption is not implementation acceptance.

## 15.3 Document versus implementation completion

This delivery is a **adopted engineering document**, not a completed flight engine or populated aircraft database. No source code, ABI, memory ledger, R0 evidence or GitHub branch is changed by publishing these reading artifacts. The referenced target/hardware results predate this document and prove only their named scope.

# Appendix A. Logical aircraft-data dictionary and examples

## A.1 Identity and conventions

| Field group | Minimum logical content |
|---|---|
| Identity | `model_id`, model revision, schema version, applicable physics/Runtime contract IDs, author/reviewer and approval state. |
| Source catalog | Per-source identifier, content hash or durable citation, license, date/version, method settings, `source_kind`, uncertainty and valid region. |
| Conventions | Body/datum axes, handedness, units, angular units, control signs, coefficient force axes, moment reference, inertia/product convention. |
| Validity | Ordinary, unaugmented and bounded-fallback envelope IDs; supported configurations and loading classes; known exclusions. |
| Reproducibility | Source bundle, generator, numerical registry, tool identities, compiled-package hash and acceptance evidence IDs. |

No source-confidence label implies human approval. No filename containing “final” substitutes for a recorded approved identity.

## A.2 Geometry and loading

| Field group | Minimum logical content |
|---|---|
| Coefficient scales | Fixed `reference_area_ft2`, `reference_span_ft`, `reference_chord_ft`; reference point XYZ in feet. |
| Offline wing/body/tails | Geometry source, section coordinates, planform/chords, incidence/twist/dihedral, airfoil or section descriptors, tail areas/arms and analysis exclusions. |
| Sweep geometry | Pivot/axis and left/right transforms; physical zero/sign, permitted limits, actual geometry functions and symmetry convention. |
| Empty aircraft | Explicit included-items definition; mass or reference weight plus gravity convention; datum-relative CG; tensor about stated center. |
| Fuel | Tank IDs/capacities, locations or fill schedules, intrinsic inertia where material, feed/transfer order and unusable-fuel treatment. |
| Stores/ammunition | Station IDs, installed/expended contents, component mass/CG/inertia, aerodynamic configuration effects, event ownership. |
| Loading acceptance | Maximum/minimum supported mass, CG region, allowed combinations, carrier/airfield constraints and asymmetric classes. |

Do not convert a three-view drawing directly into a precise inertia tensor. The mass-distribution model must be stated, even when it is an intentionally simple estimate.

## A.3 Coefficients and table descriptors

Every table family has a descriptor that defines its meaning without relying on its filename:

| Descriptor | Required meaning |
|---|---|
| `table_id` / `revision` | Stable identity inside one model revision. |
| `outputs` | Ordered coefficient/derivative names, physical conventions and units. |
| `axes` | Ordered independent variables, breakpoint values/units and constant-dimension treatment. |
| `reference` | Area/span/chord and force/moment reference frame/point. |
| `composition_role` | Base, increment, derivative, correction or absolute result; included/excluded physical effects. |
| `interpolation` | Cell search, interpolation order, rounding and endpoints. |
| `domain_policy` | Supported region and behavior outside it; no implicit extrapolation. |
| `provenance` | Source IDs, normalization/blending rule, uncertainty and validation set. |
| `numeric_contract` | Generated scale/range/intermediate requirements, not guessed ABI widths. |
| `resource_cost` | Compiled bytes, metadata/scratch requirements and measured evaluation cost. |

Minimum aerodynamic content includes all six channels, static and dynamic stability, actual control effectiveness, sweep/configuration effects and supported asymmetry/separation. Derivative omission requires an explicit rationale and validation, not an absent CSV column.

## A.4 Propulsion, surfaces, FCS and contact

| Group | Required logical values |
|---|---|
| Engines | Independent IDs, installed locations and unit directions, thrust data basis, spool dynamics, fuel flow, AB/idle/failure/relight states and capability outputs. |
| Surfaces | Physical IDs and hinges, positive sign, neutral/stops, rate/lag data, hydraulic dependency, failure dispositions and aero mapping. |
| Mixer | Command-to-surface allocation/gearing, scheduling variables, permitted cross-couplings and no-feedback direct path. |
| FCS | Command schedules/gains/filters, saturation/anti-windup, sensor validity/age, degraded mapping, trim and transfer memory, ADLC/autothrottle arbitration. |
| Contact | Wheel/hook/launch coordinates, radii/clearances, normal/friction response, attachment and capture rules, bounded solver parameters. |
| Presentation outputs | Approved derived air data, G/load, buffet, engine and configuration views; no presentation-owned physical corrections. |

## A.5 Authoring skeleton: intentionally not an admissible aircraft

The following is valid illustrative JSON showing relationships. It is **not** a finalized schema, compiled package, approved F-65A dataset, or a release-ready file. The nulls are deliberate missing inputs. An aircraft-admission validator must reject it until the values, sources and tests exist.

```json
{
  "schema_id": "PROPOSED-F65-AIRCRAFT-AUTHORING-1",
  "model_id": "F65A",
  "model_revision": "UNAPPROVED",
  "approval_state": "AUTHORING_ONLY",
  "physics_class": "SIX_DOF",
  "conventions": {
    "body_axes": "X_FORWARD_Y_RIGHT_Z_DOWN",
    "attitude": "HAMILTON_SCALAR_FIRST_BODY_TO_NED",
    "position_unit": "ft",
    "mass_unit": "slug",
    "angle_unit": "rad",
    "force_coefficients": "WIND_DRAG_SIDE_LIFT",
    "moment_coefficients": "BODY_ROLL_PITCH_YAW"
  },
  "geometry": {
    "source_id": null,
    "reference_area_ft2": null,
    "reference_span_ft": null,
    "reference_chord_ft": null,
    "aero_reference_point_ft": null,
    "sweep_geometry_id": null
  },
  "mass_model": {
    "empty_contents_definition": null,
    "empty_mass_slug": null,
    "empty_cg_ft": null,
    "empty_inertia_tensor_slug_ft2": null,
    "fuel_tanks": [],
    "payload_stations": [],
    "loading_envelope_id": null
  },
  "aerodynamics": {
    "table_catalog": [],
    "separation_model_id": null,
    "asymmetry_model_id": null,
    "ordinary_envelope_id": null,
    "unaugmented_envelope_id": null,
    "out_of_domain_policy_id": null
  },
  "engines": [],
  "surfaces": [],
  "mixer_id": null,
  "fcs_profile_id": null,
  "contact_profile_id": null,
  "source_catalog": "sources.json",
  "acceptance_catalog": null
}
```

The empty lists are not an assertion that the F-65 has no engines or control surfaces. They expose missing authored data rather than inventing it. The real schema constrains required counts and cross-references according to the selected model.

## A.6 Synthetic table example and normalization

A small *test-only* coefficient table can validate the importer without pretending to represent the F-65A:

```csv
alpha_deg,cl_test,cd_test,cm_test
-4,-0.40,0.040,0.040
0,0.00,0.020,0.000
4,0.40,0.040,-0.040
```

A descriptor must explicitly say these columns mean $C_L,C_D,C_m$, angles are degrees, the values are synthetic, the lookup is linear, and release admission is forbidden. At 2 degrees, ordinary linear interpolation gives $C_L=0.20$, $C_D=0.030$, $C_m=-0.020$. The local lift slope is $0.1$ per degree, or approximately $5.729578$ per radian. Neither that slope nor the table's drag/trim behavior is F-65A data.

The table checks text parsing, axis order, unit conversion and interpolation. It does not test high-AoA physics, sweep, dynamics, full fixed-point arithmetic or a production aircraft.

# Appendix B. Mathematical checks and worked fixtures

## B.1 Weight, mass and inertia fixture

Use an explicitly synthetic body: two point masses of 1 slug at datum positions $(0,+1,0)$ ft and $(0,-1,0)$ ft, plus a 2-slug central component with inertia $\operatorname{diag}(1,1,1)$ slug-ft². Equation (4.1) gives mass 4 slugs and CG zero. Equation (4.2) gives inertia $\operatorname{diag}(3,1,3)$ slug-ft².

Move one outer point from Y=+1 to Y=+2. Total mass stays 4 slugs and CG becomes $(0,0.25,0)$ ft. The new inertia is $\operatorname{diag}(5.75,1,5.75)$ slug-ft². This fixture catches using the old CG in the parallel-axis calculation. It is not an aircraft geometry estimate.

A separate scalar example with reference weight 32.1740485564 lbf and declared $g_0=32.1740485564$ ft/s² gives exactly 1 slug by definition of the fixture. Local gravity variation changes weight, not that mass.

## B.2 Frame and force checks

At zero AoA/sideslip, (6.1) is the body basis. With $D=10$, side force zero and lift 100 lbf, (6.2) yields $(-10,0,-100)$ lbf. Across arbitrary valid angles, the basis remains orthonormal and drag contributes $-DV$ to air-relative power while ideal lift/side force contribute zero.

A +90-degree yaw quaternion maps body-forward into East. A +90-degree pitch quaternion maps body-forward into negative Down. These tests detect transposed matrices, reversed rotation direction and scalar-last/scalar-first confusion.

With a right-mounted engine at $(0,3,0)$ ft relative to CG and forward thrust $(100,0,0)$ lbf, the installation moment is $(0,0,-300)$ lbf-ft. The left-mounted counterpart reverses yaw sign. No artificial engine-out yaw term is needed.

## B.3 Inertia-coupling check

For a synthetic reduced tensor with $I_{xx}=4$, $I_{yy}=5$, $I_{zz}=6$, $I_{xz}=1$ in consistent units, rates $(0.2,-0.3,0.4)$ rad/s and applied moments $(1,2,3)$, (9.2–9.3) gives approximately

$$
\dot{\boldsymbol\omega}=(0.4147826087,\ 0.456,\ 0.5991304348)\ \mathrm{rad/s^2}.
$$

Verify both the compact solve and a general matrix solve of the same tensor. They must agree within the floating-point fixture's numerical tolerance. This test validates signs/coupling in the equations, not an aircraft's inertia values.

## B.4 Sonic air-data check

For ideal air with $\gamma=1.4$, equations (5.4–5.5) meet continuously at Mach 1, where $H(1)=1.2^{3.5}\approx1.892929$. At Mach 2, the normal-shock total-pressure ratio is approximately 0.720874 and $H(2)\approx5.640441$.

These are perfect-gas analytical checks. They do not establish installation errors, sensor failures, temperature-profile correctness or a real aircraft's indicated speed. Use them to reject a discontinuity or a swapped static/total pressure convention.

## B.5 Table and bit-exact checks

Test exact nodes, interior interpolation, each endpoint, one-point constant dimensions, invalid axis ordering, missing values, negative operands, and every out-of-domain policy. Generate separate expected results for high-precision interpolation and the eventual selected fixed-point format; do not demand byte equality between a floating reference and a quantized result.

The documentation build's arithmetic checks cover the synthetic calculations in this appendix, wind-basis orthogonality, quaternion mapping, tensor-solve agreement and table-size arithmetic. They do **not** execute the production C flight model, LLVM-MOS, Xemu or physical MEGA65 tests. Those remain implementation/acceptance work.

# Appendix C. V3.3 migration and adopted design decisions

## C.1 Preserved versus changed

| Subject | V4 disposition |
|---|---|
| 100 Hz, fixed-point, C-first, bounded state | Preserved from the core parents and v3.3. |
| Table-driven six-DOF and natural direct flyability | Preserved, with explicit coefficient/data and validation contracts. |
| FCS mode/status, mixer, trim and transfer bias | Preserved; Runtime's ADLC failure-reason mapping incorporated. |
| Environment, two installed engines, sweep, ground effect | Preserved and clarified; no new weather or carrier-wave feature. |
| 3DOF weapons | Physical primitive retained; weapon ownership and guidance remain outside aircraft dynamics. |
| Parent references and phase terminology | Current Main v1.7 / Gameplay v1.1 / Runtime v1.1 candidate; original review inputs retained in Appendix F. |
| Aircraft input data | Expanded into an explicit authoring, normalization, compilation and admission pipeline. |
| Inertia approximation | V3.3 reduced tensor retained where justified; full host mass accounting and asymmetry-error check added. |
| Quaternion, force frames, airspeed distinctions | Fully specified to replace ambiguous/broken notation. |
| Integrator | Concrete candidate and comparisons defined, not declared target-approved. |
| Old worked examples | Replaced by clearly synthetic, checked fixtures; not promoted to aircraft coefficients. |
| R0 status | Removed from normative model prose; dated evidence snapshot only. |

## C.2 Adopted design decisions and remaining selection gates

The aircraft-package separation and source classifications; fixed coefficient reference scales; table factorization and domain policies; the sampled-feedback/autothrottle timing in §1.3; full-host versus reduced-target inertia admission; the numerical candidate in (9.7); and the dataset release gates are **adopted v4 engineering direction; the integrator remains a candidate pending the stated comparisons**.

They fit the existing owner/clock model as designed here, but their exact machine representation and implementation require the named review, generated contracts and measurement. A parent conflict must be resolved through a controlled change, not by asserting that this paper's newer date wins.

## C.3 R1 correction and adoption record

R1 resolves the review findings in §§1.3.1, 4.4.1, 6.1, 6.2, 14.5 and 15.2. The founder subsequently directed that Physics v4 become current and all coordinated authority references be updated. Main v1.7, Gameplay v1.1, Runtime v1.1 candidate amendment and AI v1.1 amendment implement that adoption. The original review package remains retained provenance.

Adoption approves the engineering method and integration direction; it does not select a numerical format, aircraft coefficient, memory allocation, ABI, final integrator, phase transition or measured limit. Appendix D preserves the original draft snapshot. The revision/adoption work starts from `c6ff0cd429bdd233b182e416d1e8a75f91c2ae49`; newer bounded P09/Group-2 evidence is not a production physics allocation.

# Appendix D. Dated source and R0 evidence snapshot

## D.1 Repository baseline inspected for this draft

The live GitHub `main` resolved to:

`ae2b397698cc7197d03349e57cd058b4fb9f3987`

This is the 21 September 2026 merge of pull request #9, preserving the T04 successor exact-carrier evidence history. The corpus manifest at that revision contains the current Main/Gameplay files, Runtime v1 candidate, all five subsystem papers and Product Story; the old statement that GitHub lacks these documents is no longer current. [G1–G2]

## D.2 What the newer successor evidence establishes

The T04 handoff reports direct NTSC/PAL execution and two fresh exact-carrier runs in each mode for the integrated successor. Its same-run lineage proceeds from tick 33 to tick 66 with validated ROM/storage restoration, retained state, resumed services and independently checked SAVE data. Fault cases fail closed. This is newer than the earlier separate CF001/RH001 gap described in some status prose. [G3]

Canonical carrier: `R0FSUCC10.D81`, 819,200 bytes.\
SHA-256: `3721dff9b84cfb7842cc154f6885861e0c7cbd3c3408c8ecec190bf6b405d461`.\
Source-freeze commit: `20b2aab382d0590037443b6a352fbc77fda7aa42`.

The corrected target reports 23,657 resident bytes against its private 40,959-byte bound and zero reserve use. These numbers are proof-fixture accounting, not a production flight-model allocation. They do not establish an aerodynamic coefficient budget, full-aircraft cost, final physics ABI or calibrated handling model.

**Boundary:** T04 establishes `XEMU_BOOT_VERIFIED`, not SD transfer, physical chooser/runtime proof for this successor, measured-limit freeze or full R0-F acceptance. The inspected handoff leaves the physical exact-carrier task separate. Existing older CF001 physical results cannot be transferred to a different successor identity. No newer physical completion is asserted by this document. [G3]

`CURRENT_STATE.md` and `WORK_IN_PROGRESS.md` still contain some historical/task wording at this snapshot. This paper records the specific evidence and merge identity rather than silently treating every summary line as the latest engineering result. It does not edit those files or promote their gate status. [G1, G3–G5]

## D.3 Source byte identities

The attached file named with `(3)` is byte-identical to the repository's recorded Physics v3.3 artifact. The following input SHA-256 values were checked for this rewrite:

```text
Main Concept v1.6 Markdown
  e7d8ed40ce630d82e707e2a9c7f29995fac6f4281849c2c7ef5261d420c2c425
Gameplay v1 Markdown
  b675daa213c02e4b642fd8f8dd439c74f72808488c548a6af14fc8400487645a
Runtime v1 candidate PDF
  bcb50a96ca6aadfd45637c48c4a80a10d8ce61b1e2461ba03448b4f06497d260
Physics v3.3 PDF (including supplied (3) copy)
  2da11ee4f6d0a2c8b5e45ddde896161b94b68ed1e5e8d19bad2c37a0d4bdb9b5
Graphics v2.1 PDF
  b94b3db857b0b7536aad23dcdc4918625fc7da27584df6886da58391b75fdb51
Audio v1.0 PDF
  2ae025b36bdbd92b5a0ac51bcead40baeec96d23765e1519fa5d672915be35ff
SensorAndTrack v1.0 PDF
  cd9369116018b81d622360d7868e534c6e31afc98fc6378e0ed8d7450d617b25
AI Behavior v1.0 PDF
  d11877582c44aed5088354e871bc7825d4dd46fb406e55dbecf84d7a01a85d20
```

# Appendix E. Open values and closure ownership

These are real implementation/data decisions, not missing prose to be filled with arbitrary numbers.

| ID | Decision or data still required | Owner and closure evidence |
|---|---|---|
| PHY-OPEN-01 | F-65A geometry, coefficient scales, mass breakdown, CG and loading inventory. | Aircraft-data owner; definition review and mass/geometry checks. |
| PHY-OPEN-02 | Aerodynamic sources, validity regions, dynamic derivatives, transonic/high-AoA and asymmetry treatment. | Simulation/data owner; source review, independent checks and trajectory validation. |
| PHY-OPEN-03 | Installed thrust/fuel/spool data and actual supply/actuator/sweep parameters. | Aircraft-systems owner; operating-state and energy/response tests. |
| PHY-OPEN-04 | FCS gains, direct gearing, degradation table, trim/transfer/ADLC/autothrottle details. | Controls owner; exact sample-delay, failure and handling acceptance. |
| PHY-OPEN-05 | Ordinary/direct/fallback envelopes and production error tolerances. | Simulation and product owners; approved case catalog and pilot review. |
| PHY-OPEN-06 | Fixed-point formats, bounded math, table compression and integrator selection. | Numeric/platform owners; bit-exact tests and measured target fit. |
| PHY-OPEN-07 | Contact response, hook/catapult geometry and solver stability limits. | Contact/systems owners; ground/deck work and energy tests. |
| PHY-OPEN-08 | Exact public schemas, owner bytes, cache/replay semantics and load-time rejection. | Runtime/schema owners; generated freeze package and resource witness. |
| PHY-OPEN-09 | Final table/state/code/cycle budgets within full combined load. | Platform/test owners; applicable measured-limit and integrated evidence. |
| PHY-OPEN-10 | CLOSED for local design adoption on 4 October 2026; Git publication remains separate. | Founder instruction, adoption record and corpus identities; no implementation acceptance. |

No table count, gain, aerodynamic value or error tolerance is accepted merely because it appears in a synthetic example. The engineering baseline is adopted; it is not a shipping aircraft-data admission.

# Appendix F. References and source roles

Project references below are the inspected corpus at the GitHub snapshot in Appendix D. Bracketed reference IDs in the text point here. External sources inform engineering choices; they do not override F65 requirements. All external material was consulted for this 1 October 2026 review draft. No claim is made that the proposed F65 implementation has passed their verification suites.

## F.1 Project design sources

**[P1] F65 Main Concept v1.6, FINAL / HUMAN-REVIEWED.** Product, architecture, ownership, physical timeline, memory, capacity and phase boundaries. Repository path: `spec/core/F65_Main_Concept_v1.6_FINAL_HUMAN_REVIEWED.md`.

**[P2] F65 Gameplay and Simulation Supplement v1, FINAL / HUMAN-REVIEWED.** Aircraft operation, fidelity/energy, physical classes, FCS, systems, carrier behavior and targets. Repository path: `spec/core/F65_Gameplay_and_Simulation_Supplement_v1_FINAL_HUMAN_REVIEWED.md`.

**[P3] F65 65Aero Engine Runtime and Technical Supplement v1, APPROVED CANDIDATE DESIGN / NOT FINAL.** Especially §§0–8, 10–13, 17, 19–23. Repository path: `spec/core/F65_65Aero_Engine_Runtime_and_Technical_Supplement_v1_HUMAN_APPROVED_CANDIDATE_DESIGN.pdf`.

**[P4] MEGA65 / F65 Flight Simulation Physics Engineering White Paper v3.3, 23 August 2026.** Predecessor physics/FCS model and closed kinematic loop. Repository path: `spec/subsystems/MEGA65_Flight_Simulation_Physics_6DOF_Atmosphere_White_Paper.pdf`. Supplied `(3)` copy has identical bytes.

**[P5] F-65 Megawing Graphics White Paper v2.1.** Presentation-only physics boundary, terrain/deck registration and snapshot coherence. Repository path: `spec/subsystems/F-65_Megawing_Graphics_White_Paper_v2.1.pdf`.

**[P6] F-65 Megawing Audio, Sound Effects and Music Engineering White Paper v1.0.** Actual-state audio parameters and non-authoritative presentation. Repository path: `spec/subsystems/F-65_Megawing_Audio_Sound_Effects_and_Music_Engineering_White_Paper_v1.0_FINAL.pdf`.

**[P7] F-65 Megawing SensorAndTrackEngine Engineering Model, Phase-3 v1.0.** Observation versus physical weapon authority and next-tick handoff. Repository path: `spec/subsystems/F-65_Megawing_SensorAndTrackEngine_Engineering_Model_Phase-3_v1.0.pdf`.

**[P8] F-65 Megawing AI Behavior and Decision Architecture White Paper v1.0.** Legal perception, held guidance, physical limits, degraded FCS and bounded KINEMATIC path. Repository path: `spec/subsystems/F-65_Megawing_AI_Behavior_and_Decision_Architecture_White_Paper_v1.0.pdf`.

The repository C readability standard and development workflow remain applicable to implementation. The root D81 gate remains mandatory for any later task that creates, modifies or tests a carrier; this document creates no D81.

## F.2 GitHub evidence sources

**[G1] Integrated main identity.** [Commit ae2b397](https://github.com/SUON1/f65-megawing/commit/ae2b397698cc7197d03349e57cd058b4fb9f3987), merge of T04 pull request #9.

**[G2] Specification corpus manifest.** [Pinned manifest](https://github.com/SUON1/f65-megawing/blob/ae2b397698cc7197d03349e57cd058b4fb9f3987/spec/manifests/spec-corpus.json), schema 3.

**[G3] R0-F T04 successor emulator and exact-carrier handoff, 21 September 2026.** [Pinned handoff](https://github.com/SUON1/f65-megawing/blob/ae2b397698cc7197d03349e57cd058b4fb9f3987/docs/reports/R0-F_SUCCESSOR_EMULATOR_EXACT_CARRIER_HANDOFF.md).

**[G4] Current Project State.** [Pinned navigation record](https://github.com/SUON1/f65-megawing/blob/ae2b397698cc7197d03349e57cd058b4fb9f3987/CURRENT_STATE.md). Not a design authority or substitute for the later detailed evidence.

**[G5] Work in Progress.** [Pinned task snapshot](https://github.com/SUON1/f65-megawing/blob/ae2b397698cc7197d03349e57cd058b4fb9f3987/WORK_IN_PROGRESS.md). Its review wording is retained as a snapshot, not used to deny the subsequent recorded merge.

## F.3 External engineering references

**[R1] Spectrum HoloByte, Falcon 3.0 manual.** Flight-model option discussion in the Configuration material, including the high-fidelity coprocessor option. [Preserved manual text](https://device.report/m/56b54ea10e2e1acfbbbdaf6f56f401f63f3035bfd3ea0587a2d72f69d216156b). Used only for the documented historical product trade, not inferred internal algorithms.

**[R2] JSBSim reference manual, “Forces and Moments” and “Math.”** [Coefficient build-up](https://jsbsim-team.github.io/jsbsim-reference-manual/user/concepts/forces-and-moments/); [table representation](https://jsbsim-team.github.io/jsbsim-reference-manual/user/concepts/math/). Used for data-driven modeling concepts; no JSBSim aircraft coefficients are imported as F-65A data.

**[R3] Laminar Research, “How X-Plane Works.”** [Developer explanation](https://www.x-plane.com/desktop/how-x-plane-works/). Used as a contrasting geometry/element-force architecture, not a target-runtime prescription.

**[R4] JSBSim, FGMassBalance class documentation.** [Mass, CG, inertia and structural-frame conventions](https://jsbsim-team.github.io/jsbsim/classJSBSim_1_1FGMassBalance.html). F65's normalization must explicitly account for different frame and product conventions.

**[R5] NASA OpenVSP Ground School, “VSPAERO Basics.”** [Reference values, geometry analysis and version caveats](https://www.nasa.gov/reference/openvsp-vspaero-basics/). Used for disciplined offline analysis and coefficient normalization, not blanket validation of a fighter's full envelope.

**[R6] NOAA / NASA / USAF, U.S. Standard Atmosphere, 1976.** NASA-TM-X-74335. [NTRS document 19770009539](https://ntrs.nasa.gov/citations/19770009539). Reference atmosphere source; mission weather and target approximation still require their own validation.

**[R7] NASA Glenn, “Normal Shock Wave Equations” and “Pitot-Static Tube.”** [Compressible shock relations](https://www.grc.nasa.gov/WWW/k-12/airplane/normal.html); [probe limitations](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/pitot-static-tube-speedometer/). Equations (5.4–5.5) combine ideal isentropic and normal-shock relations; no instrument installation is validated by that combination alone.

**[R8] USAF Stability and Control Digital DATCOM, documentation preserved by Public Domain Aeronautical Software.** [Software/documentation overview](https://www.pdas.com/datcom.html); [capabilities and method limitations](https://www.pdas.com/datcomDescription.html). Used as a semi-empirical candidate data-generation method, not a mandatory or universally applicable solver.

**[R9] NASA Engineering and Safety Center, Check-Cases for Verification of 6-Degree-of-Freedom Flight Vehicle Simulations.** NASA/TM-2015-218675 and the maintained [2015 check-case collection](https://nescacademy.nasa.gov/flightsim/2015). Use corrected case definitions and matching frame/environment assumptions; no certification or completed F65 comparison is implied.

---

**End of Physics v4.0 engineering baseline.** The model/data architecture is adopted. Aircraft coefficients, selected numeric layouts, performance budgets and implementation acceptance remain explicitly gated.
