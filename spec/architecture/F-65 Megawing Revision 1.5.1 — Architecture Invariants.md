
# F-65 Megawing  
## Revision 1.5.1 — Architecture Invariants and Gameplay Alignment

**Status:** Architecture-freeze candidate  
**Supersedes:** Revision 1.5 upon human approval  
**Preservation rule:** Preserves Revision 1.5 except where explicitly modified by Revision 1.5.1  
**Primary update:** Aligns the architecture with the hash-pinned Gameplay and Simulation Requirements Supplement and incorporates applicable Technical Alignment corrections under the C-primary production model  
**Approval effect:** Until Revision 1.5.1 is approved, Revision 1.5 retains its existing candidate status and Revision 1.4.1 remains the last frozen architecture baseline.

---

## 1. Preserved product baseline

Revision 1.5.1 preserves Revision 1.5's product and C-primary architecture, aligns it with the Gameplay Supplement identified in §1.2, and applies the non-assembly-specific corrections identified in §19:

- Retro-synthwave heavy fleet-interceptor game for the MEGA65.
- Primary production game code written in C using LLVM-MOS for the MEGA65/45GS02 target, with handwritten 45GS02 assembly retained as a first-class production language for measured or platform-critical work.
- Cockpit-primary presentation with a low-cost chase view.
- Bubble canopy, green monochrome HUD, automatic RIO-operated fused radar/navigation repeater, and grayscale aircraft-status display.
- Aviation-facing units: nmi, knots, feet, lb, lbf, lb/hour, psi, and G.
- Positive-G desaturation beginning near +6 G and reaching grayscale near +7 G.
- F-65A with two engines, the standard six-long-range/two-medium-range/two-heater missile load, 675 cannon rounds, fuel, electrical, hydraulic, radar, jammer, RWR, countermeasures, and damage simulation.
- One-button Deck, TFL, Normal Flight, and Combat contexts.
- Meridian Maritime Compact versus Boreal Directorate.
- A non-narrative Technical Combat Slice for integration proof, followed by the separately approved Midnight Spear mission, ten-operation campaign, and two endings.
- One independently bootable MVP D81; multi-D81 campaign permitted.
- Absolute R0 hardware-measurement gate.
- Hard Phase 1 integrated-engine-harness gate.
- Engine-first Phase 0–5 development order.

Revision 1.5.1 introduces no mission, weapon, aircraft, mechanic, or campaign content beyond the hash-pinned Gameplay Supplement. It does not invent the still-unwritten Midnight Spear manifest, operations 3–10, ending predicates, or any `TARGET`, `TBD`, or `R0-GATED` value.

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

### 1.2 Controlled specification corpus and precedence

The Revision 1.5.1 candidate corpus is:

| Role | Exact input | SHA-256 | Status in this revision |
|---|---|---|---|
| Architecture parent | `F-65 Megawing Revision 1.5 — Architecture Invariants.md` | `f68cd491adc1fdabf252f6460e305486a6aed47245d848b2caf7a3290ea75d8f` | Preserved except for explicit 1.5.1 edits |
| Gameplay companion | `F-65 Megawing Gameplay and Simulation Requirements Supplement.md` | `5db0344f8e7fd66143874310c3794a64391d4767229a90f5caee5e5e287d84e4` | Its `MUST` gameplay contracts are adopted upon approval of 1.5.1 |
| Correction input | `F-65_Technical_Alignment_and_Corrections_Supplement_v0.2.md` | `fd8188f3787d902466a3d07b13c46e88f9afe32d7d5839945c4bc33143e0249b` | Only the dispositions expressly listed in §19 are incorporated |

The architecture document controls architecture, ownership, memory, timing, determinism, platform gates, and implementation admission. The Gameplay Supplement controls player-visible behavior and simulation requirements within those invariants. `TARGET`, `TBD`, and `R0-GATED` retain their Gameplay Supplement meanings and cannot override an architecture `MUST` or be silently promoted by implementation.

References in the Gameplay Supplement to Revision 1.4.1 are interpreted as references to the corresponding preserved invariant in Revision 1.5.1. If wording still conflicts, Revision 1.5.1 controls architecture and the conflict must be recorded; implementers may not choose a local interpretation.

Revision 1.5.1 is self-contained for architecture invariants but does not duplicate the full gameplay companion. A release or conforming gameplay build must identify the exact approved architecture and gameplay hashes in its specification-set manifest.

### 1.3 Gameplay alignment rules

The following points resolve architecture-facing gameplay interpretation without changing Gameplay Supplement tuning status:

- The simulation remains a consequential table-driven six-degree-of-freedom model for player and combat aircraft, with physical energy loss, stalls/departure, fuel burn, mass change, atmosphere, and damage.
- Assisted and Manual laws share the actuator/hydraulic/aerodynamic pipeline; Manual removes envelope protection but never bypasses physical authority or damage.
- The four control contexts are Deck, Takeoff-and-Landing, Normal Flight, and Combat. Device bindings remain behind semantic `InputCommandFrame` actions and their stated hardware gates.
- Autothrottle, ADLC, cold start, independent engines/generators/hydraulics, system capability, carrier/airfield operation, and dynamic Joker/Bingo are current-scope gameplay contracts.
- The right cockpit display is the RIO-operated fused radar/navigation picture; the left display is the integrated aircraft-status picture; the HUD remains the primary flight-data source.
- Sensor truth, observations, semantic tracks, fire-control state, and display presentation are distinct. Display cadence cannot alter detection, guidance, AI knowledge, or replay.
- The standard load is six long-range radar missiles, two medium-range radar missiles, two heaters, and 675 cannon rounds. No tactical launch inhibit converts a poor or unauthorized shot into a non-event; physical release, lifecycle, and ROE rules apply.
- Radar/missile/notch/countermeasure behavior remains deterministic and geometry/energy driven, using the Gameplay Supplement's `MUST` contracts and later table gates.
- Static scenery remains non-destructible. Only valid live entities from frozen pools may receive current-scope damage.
- The combined-load profile in Gameplay §3.1 is an acceptance case inside the larger frozen pools, not a reduction of any pool capacity.
- Operations 1 and 2 follow the Gameplay Supplement. Operations 3–10, the two ending predicates, detailed doctrine, and final Midnight Spear content remain authored-data gates rather than implementation discretion.

### 1.4 Production-language architecture

The primary production implementation language is C compiled for the MEGA65 and 45GS02 architecture.

The initial required compiler/toolchain baseline is:

- LLVM-MOS.
- The LLVM-MOS MEGA65 target.
- The 45GS02 CPU target where supported by the selected LLVM-MOS release.

The exact compiler version and hashes, SDK and runtime-library versions and hashes, target options, linker configuration, optimization flags, assembler/linker versions, reproducible host configuration, and generated-output identity belong in the checked-in toolchain lock and implementation documentation. They are not casually hard-coded here. A selected LLVM-MOS release may not be represented as providing 45GS02 support that it does not actually provide; unsupported low-level operations remain behind approved platform or assembly wrappers until the toolchain evidence says otherwise.

Handwritten 45GS02 assembly remains a first-class production language and is expected when justified by one or more of:

- Measured performance requirements.
- Deterministic cycle-bound requirements.
- Interrupt handling.
- MAP or memory-window operations.
- DMA control.
- Q-register or extended-register operations.
- Hardware math access.
- VIC-IV or platform-specific low-level control.
- Renderer inner loops.
- Fixed-point kernels.
- Routines for which compiler-generated code cannot meet an approved memory or timing budget.
- Other explicitly approved platform-critical functions.

No fixed percentage of C versus assembly is an architecture requirement. The implementation split is determined by contracts, measurement, hardware behavior, and retained evidence.

Production optimization follows this sequence:

1. Define the behavioral contract.
2. Establish the applicable Java oracle and golden-vector tests.
3. Implement the production routine in C unless architecture or hardware requirements justify assembly immediately.
4. Measure target-code size, cycle cost, memory impact, and hardware behavior in the required environments.
5. Retain the C implementation when it satisfies the approved budget and behavior.
6. Replace or supplement only measured offenders with handwritten 45GS02 assembly.
7. Require the assembly replacement to satisfy the same public contract and validation suite unless an approved requirement explicitly defines different behavior.

Assembly optimization is evidence-driven, not presumed merely because assembly is available.

### 1.5 Deterministic C-runtime restrictions

Production C must remain compatible with the fixed-capacity, deterministic architecture in this document.

- No general-purpose dynamic heap allocation occurs during deterministic runtime.
- `malloc`, `calloc`, `realloc`, and equivalent runtime allocation are forbidden unless a future explicitly approved architecture revision permits a tightly bounded use.
- Authoritative deterministic simulation uses no floating-point arithmetic.
- Serialized, ABI-visible, deterministic, hardware-facing, and numerically bounded state uses explicitly sized integer types and generated numeric contracts.
- Stacks are bounded and instrumented.
- Uncontrolled recursion is forbidden.
- Large or unbounded automatic allocations are forbidden.
- Persistent, public, hardware-facing, replay, checksum, package, and serialized data never depends on implementation-defined C structure packing, padding, bit-field layout, enum width, or pointer size.
- Ordinary C pointers do not represent arbitrary MEGA65 physical or far memory.
- Physical and far memory continue to use the approved `MemoryAccessABI`, `FarPtr32`, resource handles, and platform wrappers.
- Direct DMA, MAP, IRQ, hardware-math, and protected platform ownership remains confined to the owning services.
- Standard-library functionality with unacceptable, unbounded, or unknown timing, stack, allocation, memory, or platform behavior is forbidden in deterministic runtime paths.

Ordinary C naming, formatting, and local coding style are implementation concerns rather than architecture invariants.

### 1.6 C/platform ABI boundary

Generated C and any handwritten low-level target routine cross one documented, generated, and testable target ABI boundary.

- The calling convention is documented and pinned to the selected compiler/toolchain identity.
- Argument, return-value, preservation, and clobber rules are explicit.
- Compiler-required processor state is restored before returning to generated C.
- Hardware-stack, software-stack, base-page scratch, reentrancy, and maximum-stack assumptions are documented.
- A, X, Y, Z, Q, processor flags, and any compiler-reserved register or memory state have explicit ownership and preservation rules.
- MAP and base-page state are restored to the canonical platform ABI before every public return.
- Interrupt-mask, IRQ-safety, NMI assumptions, and allowed interrupt windows are documented.
- Public entry and exit invariants are exercised by target tests.
- Handwritten assembly is exposed through narrow wrappers rather than scattered, uncontrolled inline assembly.

Exact LLVM-MOS ABI mechanics, wrapper spellings, generated annotations, and compiler-version details belong in the Engine/Toolchain supplement and generated Platform ABI registry. This architecture freezes the boundary invariant, not those implementation details.

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

C addressability rules:

- An ordinary C pointer may address only memory that the selected compiler ABI and current canonical CPU map make valid for that pointer type.
- An ordinary C pointer is never a substitute for `FarPtr32`, `ResourceHandle16`, or a normalized DMA physical address.
- No higher-level module constructs, truncates, aliases, or dereferences an arbitrary MEGA65 physical address through a generalized C pointer.
- Compiler-specific near/far pointer bridges, address-space qualifiers, or calling shims remain beneath `MemoryAccessABI` or another explicitly approved platform wrapper.
- Public physical-memory semantics remain identical for C and assembly callers.

### 2.5 DMA rules

- DMA uses normalized physical addresses, never CPU-window addresses.
- MAP state does not alter DMA addresses.
- Every range is validated before submission.
- I/O, hypervisor, reserved, and color-RAM access requires an explicit whitelist.
- Attic/chip transfers are owned by the resource manager.
- DMA lists remain resident and immutable until completion.
- `DMAService` is owned by `CoreRuntime`; other modules submit validated requests and never start hardware jobs directly.
- Each job declares source, destination, length, address classes, overlap legality, list storage, deadline class, completion method, and audio-arbitration requirement.
- Ordinary DMA is budgeted as CPU-unavailable time wherever the pinned core blocks the CPU.
- The measured-limits revision freezes maximum uninterruptible job duration by address class and competing audio state.
- All jobs obey measured timer, audio, input, and critical-warning latency bounds.
- No software organization may describe a blocking DMA job as preemptible merely because submission is asynchronous.

### 2.6 R0-A deliverable

`MemoryAccessABI` must provide:

- Canonical-map setup and assertions.
- Scoped MAP-window proof.
- Base-page restoration tests.
- Far-pointer tests.
- Resource-directory validation.
- Physical DMA copy/fill tests.
- IRQ-latency measurement.
- Minimal compiler-generated C access through the public abstraction.
- C-to-assembly and assembly-to-C wrapper tests for canonical map, base page, stack, register/Q state, and interrupt state.
- Verified platform-wrapper vectors for extended addressing, Q operations, and any selected hardware-math backend, including invalid input and divide-by-zero behavior.
- Xemu and hardware verification.

---

## 3. Deterministic execution semantics

### 3.1 Simulation clock

- Simulation runs at exactly 100 Hz while the sortie is in `ACTIVE_SORTIE`.
- `SimulationTick` is unsigned 32-bit and monotonically increasing.
- Every command and event contains its originating tick.
- Tick wrap is a fatal invariant violation.
- PAL/NTSC timing and presentation cadence cannot change results for identical tick-tagged inputs.
- Display/raster service and the 10,000-microsecond simulation period are independent clocks; no integer frame/tick superperiod is assumed.

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
19. Extract bounded cockpit, warning, audio, and presentation state.
20. Calculate the canonical authoritative checksum.
21. Atomically publish a complete `PresentationSnapshot`.

Presentation sees only a complete published `PresentationSnapshot`; authoritative simulation state is never exposed directly.

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

The approved fault catalog defines the exact development stop and release abort/recovery transition. A timing fault never normalizes a corrupted sortie into a normal save.

### 3.7 Implementation-language independence

Changing the target implementation language does not weaken deterministic execution.

- The 100 Hz clock, 21-step tick order, state ownership, event ordering, lifecycle, RNG ownership, arithmetic rules, replay/checksum behavior, fault behavior, and presentation boundary apply identically to C and assembly routines.
- Compiler evaluation order, integer promotion, implementation-defined behavior, undefined behavior, structure layout, library behavior, or optimization choice cannot become implicit authority over game semantics.
- Every authoritative operation has contract-defined widths, signedness, rounding, saturation, ordering, and fault behavior where those properties can affect results.
- A C implementation and any assembly replacement consume the same logical inputs and produce the same contract-defined outputs within the approved tolerance.
- Toolchain or optimization-flag changes that can affect deterministic target behavior require the applicable golden-vector, replay, checksum, size, cycle, and hardware suites to pass again.

### 3.8 Full-pause semantics

- Entry to `FULL_PAUSE` occurs only at a completed active-tick boundary.
- While paused, no simulation tick, simulation RNG, mission time, authoritative event, or tick debt advances.
- Presentation, pause-menu input, and permitted non-authoritative audio may continue on wall/raster time.
- Gameplay input edges are cleared at pause entry and re-armed only after controls return to their release or neutral state.
- Resume establishes a new wall-time deadline origin; the next active tick is exactly the prior `SimulationTick + 1`.
- Replay represents pause/resume as out-of-band control events and reproduces the same active-tick checksum stream regardless of paused wall duration.

### 3.9 Presentation-snapshot handoff

`PresentationSnapshot` is a generated, bounded, versioned extraction containing only values needed by graphics, HUD, cockpit, map/radar presentation, audio presentation, and UI consumers.

- The measured-limits revision freezes its maximum bytes and buffer count; all storage is charged to the memory ledger.
- Buffer states are `FREE`, `PUBLISHING`, `READY`, and `READING`.
- Simulation alone performs `FREE → PUBLISHING → READY`; presentation alone performs `READY → READING → FREE`.
- Publication is an atomic index/state transition after extraction and checksum completion.
- Simulation never mutates `READY` or `READING` storage.
- If no `FREE` buffer exists, simulation continues, skips that presentation publication, and increments a diagnostic counter.
- Presentation may retain its current complete record, acquire the newest complete `READY` record, and discard older unread presentation records.
- Dropping or coalescing presentation records cannot change simulation, replay, sensors, AI, weapons, objectives, or scoring.

An extracted three-buffer arrangement is the initial benchmark candidate, not a frozen buffer count.

### 3.10 Deterministic fault contract

Every bounded resource and external operation has a named fault code, detection point, authoritative or presentation-only classification, diagnostic fields, and development/release response.

- An authoritative overflow or invariant breach cannot wrap, corrupt adjacent memory, depend on presentation order, or silently change simulation.
- Development handling stops at a deterministic tick boundary and writes a fixed-size fault record.
- Release handling enters the approved controlled-performance pause or abort-to-debrief path and does not write a normal save from the faulted sortie.
- Presentation-only overflow uses its documented stable priority/drop rule and increments a counter.
- Corrupt resources and packages are rejected before activation.
- Save failure preserves the last verified generation.
- Unknown hardware identity may enter labeled diagnostic mode but cannot close measured or release evidence.

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

### 4.5 Numeric registry

Every authoritative scalar and vector field declares its physical meaning, reference frame, unit, signedness, storage width, integer/fraction bits, valid and representable ranges, invalid encoding, rounding mode, overflow/saturation rule, normalization rule, and host conversion.

The generated numeric registry covers at minimum attitude, angular rate, linear velocity, acceleration, force, moment, mass, pressure, temperature, density, range, bearing/elevation, time, fuel flow, probability/RNG comparison, and all aviation-display conversions.

- All frame transforms state handedness, axis order, and source/destination frames.
- Out-of-domain tables, invalid normalization, divide-by-zero, and sector-boundary overflow follow the deterministic fault contract.
- Authoritative target state never uses floating point.
- Java high-precision and bit-exact models, C target code, serializers, and optional low-level replacements consume the same generated definitions.

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

### 5.4 Generated memory and concurrency admission

All resident arrays, pools, queues, snapshots, fault records, compiler/runtime support, stacks, and active resources are generated or measured against one owner ledger.

- Each pool proof states record size, explicit alignment, debug-guard policy, capacity, maximum simultaneous live count, and spawn/free ordering.
- Queue proofs enumerate every legal producer and maximum per-tick fan-out.
- The linker/build report emits per-owner actual, limit, reserve, and overlap results; any excess fails the build.
- The 32 KB measured-limits reserve is not consumed by baseline features without a numbered architecture decision.
- A record-size estimate is not a frozen capacity proof until every required field maps to its generated layout.

The required combined-load acceptance profile is nine aircraft, sixteen guided missiles, twenty-four gun projectile groups, forty-eight live decoys, eight dynamic mission entities, eight active objectives, sixty-four presentation effects, the required radar/track load, damage, audio, HUD, and renderer work concurrently. This profile does not reduce the larger individual pool capacities in §5.2 and does not claim that every pool maximum is legal simultaneously.

---

## 6. CPU and timing ledger

### 6.1 World rendering

World rendering is incremental and resumable.

- Work yields at object, face, span-batch, or DMA-batch boundaries.
- Only complete buffers are displayed.
- The previous complete buffer remains visible if a new world frame is unfinished.
- HUD, cockpit, input, audio, warnings, and simulation have independent deadlines.

### 6.2 Synthetic-load definition

The R0-D fixture retains the 530,000-clock protected non-render workload over its nominal two-display-frame measurement interval so historical R0 comparisons remain reproducible.

This is a planning fixture, not a production per-tick budget and not proof of a safe deadline. R0 additionally reports protected work per simulation tick, per display service, and across every relative tick/raster/DMA/audio phase in a measured rolling window. The synthetic kernels must match intended structure-of-arrays access, branching, table use, arithmetic, event pressure, and audio service as closely as possible.

### 6.3 Independent-clock planning ledger

The legacy two-frame NTSC envelope remains useful only as a comparison target:

| Class | Planning allocation |
|---|---:|
| Protected non-render workload | 530,000 clocks |
| Protected HUD/cockpit/display service | 100,000 clocks |
| Incremental world rendering | 585,000 clocks |
| Mandatory reserve | 135,000 clocks |
| **Total** | **1,350,000 clocks** |

At the nominal 40.5 MHz CPU rate, one 10-ms simulation interval supplies 405,000 clocks before stalls and interrupt overhead. Actual raster periods, CPU availability during DMA, and legal overlap are measured on the pinned hardware/core. The table above cannot approve a module merely because its average fits.

The measured-limits revision replaces these planning allocations with:

- Per-simulation-tick ceilings.
- Per-display-service ceilings.
- Per-module and per-work-unit ceilings.
- Maximum uninterruptible DMA duration.
- Maximum masked-interrupt duration and response latency.
- Snapshot extraction/publish bytes and cycles.
- Event count, bytes, sort/apply cycles, and fault bounds.
- Audio aggregate rate, cache, latency, and contention limits.
- Worst-phase rolling-window ceilings and mandatory reserve.

Every supported PAL/NTSC mode is phase-swept. No document or implementation may assume exactly ten ticks in six NTSC frames.

### 6.4 Deadline protection

- Simulation: fixed 100 Hz.
- Raw input: every display service or approved higher-rate source, edge-preserved into one tick-tagged command frame per active tick.
- Audio: every display frame or required interrupt interval.
- HUD and critical warnings: every display frame.
- Radar and systems displays: scheduled presentation rates; immediate critical presentation never creates a second sensor or track update.
- World rendering: remaining time only.
- DMA: admitted only within measured blocking and latency bounds.
- A 20 Hz world cadence is a failure floor, not permission to alter simulation.

### 6.5 Target-code budget and optimization admission

The existing code-size, memory, cycle, DMA, resident-simulation, and reserve limits apply to all target code regardless of implementation language.

- Compiled C code, compiler runtime support, constant pools, thunks, wrappers, stack use, generated tables, and handwritten assembly are charged to their owning target-code and memory ledgers.
- No budget or reserve is loosened merely because C is introduced.
- Module reports use measured target-code bytes, data bytes, stack high-water, cycle counts, call counts, DMA blocking, and hardware behavior rather than source-language estimates.
- C remains the production implementation when it meets the approved behavioral, size, timing, memory, and hardware limits.
- Measured offenders may be replaced or supplemented by assembly behind the same public contract.
- Assembly optimization does not authorize crossing module ownership, bypassing saturation or assertions, changing ordering, consuming reserve, or altering player-visible behavior.
- Compiler or linker changes require renewed target measurements when they can affect admission to a frozen budget.

---

## 7. Flight-control and actuator layer

Raw keyboard and joystick sampling produces semantic, tick-stamped input; physical key codes and device-specific states never enter flight, systems, weapons, radar, AI, or mission modules.

`InputCommandFrame` covers signed pitch, roll, yaw/taxi-steer demand; absolute or relative throttle command; control context; trim; trigger/release; weapon/target/radar/countermeasure/jammer actions; gear/flap/hook/brake/ADLC and flight-law actions; view/glance; and applicable tick-bound commands. The generated input registry defines numeric ranges, calibration, inversion, dead zones, quantization, levels versus edges, repeat policy, context legality, mutually exclusive actions, and device arbitration.

- If multiple raw samples precede one tick, axes use the latest calibrated sample and non-repeatable edges are OR-latched once.
- Edge latches clear only after the command frame consumes them.
- Menu and full-pause commands are consumed outside active simulation.
- Queue overflow follows the deterministic fault contract; legal input edges cannot disappear silently.
- Exact default bindings, pie timing, dead zones, digital shaping, and device profiles retain their Gameplay `TARGET` or `R0-GATED` status.

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

Java host tools provide:

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

The validation relationship is:

```text
approved behavioral and numeric contract
→ independent Java host oracle and golden vectors
→ production target implementation in C or assembly
→ optional measured handwritten-assembly optimization
```

The production target implementation bit-matches the bit-exact model unless a contract defines an approved LSB tolerance. A handwritten assembly replacement must match the same vectors and contract as the C implementation it replaces unless an approved requirement explicitly defines different behavior. The Java oracle remains independently authoritative for expected behavior; neither C compiler output nor an existing assembly routine defines the golden result by itself.

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
- Compiler/runtime support bytes and ownership.
- C/assembly boundary calls and invariant failures.
- Per-routine target-code size and cycle deltas across toolchain or optimization changes.

### 10.4 Generated target and host interfaces

Where a public record, constant, enum, offset, numeric format, handle, memory range, or ABI fact is generated, one canonical machine-readable description remains the source of truth.

The canonical registries cover public interfaces, numeric formats, platform ABI, memory ownership, faults, replay/checksum fields, missions, assets, acceptance criteria, and evidence. Exact repository paths are fixed by the approved repository layout; only one source exists for each artifact class.

That source may generate:

- C headers, fixed-width types, constants, declarations, and compile-time assertions.
- Low-level target constants, offsets, macros, declarations, and build-time assertions where a handwritten platform routine exists.
- Java host bindings, serializers, and oracle-facing records.
- Human-readable interface and memory reports.

Public record definitions are not independently duplicated across C, low-level target code, and Java. Generated layouts define stable numeric IDs, owner/readers, production/consumption stage, byte order, width, alignment, padding policy, valid ranges, enum/sentinel values, units, numeric format, invalid values, and serialization behavior. Native compiler structure packing or padding is not used as the authority for persistent, replay, checksum, package, hardware-facing, or cross-language records.

### 10.5 Production-routine acceptance

A target routine is accepted by evidence, not by source language.

- The public contract and owning module are identified.
- Java oracle and golden-vector evidence exists where applicable.
- Generated interface and numeric definitions are current.
- C and assembly entry points satisfy the applicable Platform ABI and `MemoryAccessABI` invariants.
- Target-code size, data size, stack high-water, cycle cost, DMA impact, and hardware behavior fit their approved ledgers.
- The implementation assembles/compiles, links, runs in Xemu, and passes physical-hardware evidence where the gate requires it.
- Optional assembly optimization reports the measured offender, before/after evidence, and unchanged contract result.

### 10.6 Canonical replay and checksum

The authoritative checksum is generated from schema-versioned canonical serialization after tick stage 19 and before presentation publication.

- The field set, entity ordering, byte order, padding exclusion, RNG streams, free-list state, mission state, and checksum cadence are explicit and versioned.
- Replays contain specification/build/platform identities, package identities, initial state and seeds, one semantic command frame per active tick, and out-of-band pause/control events.
- Presentation state, wall time, non-authoritative diagnostics, and uninitialized padding are excluded.
- An incompatible schema/build is rejected unless an approved migration exists.
- Host and target comparison reports the first divergent tick and field group.
- Golden output cannot be blessed from current C or low-level target behavior without independent contract/oracle review.

---

## 11. Expanded R0-A identity

R0-A pins:

- MEGA65 model/hardware revision and supported memory configuration.
- FPGA core version and hash.
- ROM version and hash.
- System-files version and hash.
- CPU speed, PAL/NTSC and selected 50/60/63-Hz mode, video output, storage device/media, and input devices.
- Official documentation versions and hashes.
- Java/JDK versions and hashes.
- LLVM-MOS compiler, MEGA65 target support, 45GS02 CPU-target support where available, SDK/runtime-library, linker, flags, and hashes.
- Handwritten-assembly tool versions and hashes.
- Xemu build and configuration.
- Host-tool versions.
- Game source/build hash.
- D81 hash.
- Benchmark-scene hash.

Reports without the complete identity are nonauthoritative.

R0-A cannot pass without `MemoryAccessABI`, mapping assertions, required opcode proof, a minimal compiler-generated target proof, C/assembly boundary proof, reproducible boot, symbols, compiler/linker maps and applicable listings, profiling, and benchmark identity.

The repository toolchain lock records exact compiler, SDK/runtime, linker, any low-level assembler, Java/JDK, host dependencies, Xemu, deterministic locale/time-zone, target flags, and hashes. One documented non-interactive command regenerates interfaces, host data, assets and mission fixtures in scope; builds and links target code; constructs the D81; runs host and target smoke tests where supported; and emits a machine-readable evidence index. Generated files identify generator/source hashes and fail validation when stale.

Two clean supported macOS environments must reproduce deterministic artifacts byte-for-byte except for explicitly cataloged metadata before release labeling. LLVM-MOS success, host tests, or Xemu execution cannot replace physical-hardware evidence.

---

## 12. Early contracts retained for later phases

### 12.1 Resource residency and asset admission

States:

- Unloaded.
- Disk-known.
- Attic-resident.
- Chip-resident/staged.

Only the resource manager changes residency. Consumers retain handles.

Every required visual/audio/data asset has a stable ID, owner, gameplay use, source/provenance, conversion recipe/version, converted-size limit, residency class, preload group, fallback/proxy, and acceptance owner. Meshes declare converted vertex/edge/face and LOD limits; images declare dimensions, encoding, transparency, and palette roles; audio declares encoding, rate, duration, cut/loop points, priority, and channel policy. Converters reject out-of-envelope input rather than silently truncating it.

### 12.2 Packages, D81, and saves

- Versioned field-wise chunks.
- Explicit endianness and widths.
- No raw runtime structures.
- Optional unknown chunks can be skipped.

The build emits a disk manifest with every file's exact and allocated bytes, checksum, schema/package version, residency destination, and load phase. A release gate proves the independently bootable MVP image fits the selected D81 filesystem including allocation overhead and required save/free-space policy.

- Tactical packages are loaded and validated before sortie; no tactical disk read is required.
- Packages contain magic, version, declared length, a non-overlapping bounded section directory, capacity declarations, and integrity data.
- Failed package validation leaves active state unchanged.
- Saves are transactional: write and verify a new generation, then select it while retaining the prior valid generation.
- Absent, changed, write-protected, full, corrupt, removed, and power-interrupted media have explicit results.
- Boot, transition, disk-change, and save behavior are measured on each supported physical storage configuration.

### 12.3 Mission runtime and compiler

Phase 4 defines `MissionRuntime`, fixed `ObjectiveSet`, tick-tagged commands, and deterministic objective evaluation.

Mission graphs are finite and statically bounded. Loops declare maximum iterations and concurrency. The host compiler computes conservative per-resource may-live maxima over all legal branches, spawn/despawn delays, weapon lifetimes, decoy/projectile lifetimes, AI actions, and required effects; it emits a witness path for each peak and rejects an unknown or excessive bound.

The Technical Combat Slice is a non-narrative integration proof and does not define Midnight Spear. Midnight Spear requires a separately approved mission manifest naming start state, packages, entities/loadouts, objective graph, branches, success/failure/abort conditions, duration, controls/views/displays/audio, doctrine, assets, load case, replay seed, and acceptance IDs.

A ten-row campaign manifest is required before full campaign production. Each operation declares prerequisites, carried state, scoring/grade/retry effects, objective branches, ending predicates, assets, concurrency proof, and acceptance playthroughs. Unwritten operations may use labeled non-shipping fixtures but are never invented by implementation agents.

### 12.4 Fire control and sensor cadence

Phase 3 defines `WeaponSolutionFrame` with shooter, target, weapon, range, closure, aspect, launch state, time of flight, loft/direct recommendation, seeker support, and source tick.

Physical truth advances only in the frozen physical stages. Each sensor declares a tick-indexed scan and revisit schedule. Observation, association, track quality/identity/aging/overflow, and fire-control consumption occur only in their named simulation stages. Displays sample semantic tracks at an approved presentation cadence; an urgent cue may request the next presentation service but cannot advance sensor or track state.

Track records define source/fusion state, quality, age, confidence/error surrogate, coast/loss/delete thresholds, capacity ranking, and stable tie breaks. One physical contact cannot become duplicate fused tracks.

### 12.5 Audio and RIO callouts

Hybrid presentation is frozen:

- Short samples when budgets permit.
- Tones and text are authoritative.
- Every sample has text fallback.
- Critical warnings preempt samples.
- Gameplay never depends on sample availability.

The audio registry assigns SID/PCM categories and defines priority, preemption, retrigger, ducking, loop/cut boundaries, maximum service latency, deterministic event mapping, reachable-memory requirements, and fallback. The measured-limits revision freezes sample encoding/rate, cache, channel use, aggregate bandwidth, and DMA contention. Presentation-audio overflow follows stable priority/drop rules and cannot alter simulation or RIO decisions.

### 12.6 Controlled fault and evidence catalogs

The fault catalog maps every queue, pool, resource, storage transaction, DMA request, input bridge, and invariant to its detection point, fault code, diagnostic payload, release response, and recovery rule.

Every acceptance record identifies requirement IDs, build/spec/package hashes, environment, preconditions, inputs/seed, duration/sample count, measured variables and units, threshold/tolerance, oracle, expected/actual result, first divergence/fault, retained artifacts, executor/date, and required human sign-off. Static bounds, Java oracle results, Xemu results, physical-hardware evidence, and human playtest each prove only their stated evidence tier.

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

1. R0-A: references, benchmark identity, LLVM-MOS/assembly toolchain, `MemoryAccessABI`, required opcode and C/assembly boundary proof, and profiler.
2. R0-B: graphics/display, cockpit, palette, swap, input-latency/edge, and representative audio measurements.
3. R0-C: production-shaped host tools and scene plus package, D81, resource-residency, and storage/save proof.
4. R0-D: 530,000-clock protected workload.
5. R0-E: independent-clock, combined-load, snapshot, memory, renderer, input, audio, and storage Xemu report.
6. R0-F: corresponding physical-hardware report and phase sweep.
7. Measured-limits revision.

R0 proof software may combine minimal C, generated compiler output, and handwritten 45GS02 assembly as appropriate to the behavior under test. R0 still proves actual MEGA65 behavior. Successful compilation, host-only testing, or Xemu execution cannot substitute for physical-hardware evidence where the gate requires hardware measurement. R0-A remains a platform and `MemoryAccessABI` proof and does not become gameplay implementation merely because C is available.

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
- Presentation extraction and bounded snapshot handoff.
- Input edge bridge, fault catalog, replay/checksum, and generated interface/numeric registries.
- Synthetic integrated harness.

Phase 2 cannot begin until the concurrent harness proves canonical mapping, deterministic checksums, lifecycle correctness, combined p95 timing, memory compliance, reserve, audio stability, correct input, and PAL/NTSC equivalence.

Phase 1 target modules may be implemented in C, handwritten assembly, or a measured combination, but every module remains subject to the same ownership, generated-interface, target-code, timing, memory, deterministic, and hardware-evidence gates.

A partial pass is failure.

### Phases 2–5

- Phase 2: flight and aircraft systems.
- Phase 3: radar, weapons, and damage.
- Phase 4: tactical layer and non-narrative Technical Combat Slice, then Midnight Spear only from its approved manifest.
- Phase 5: campaign, compatibility, optimization, and release.

The future expansion goals are not inserted into these phases or their exit criteria.

---

## 15. Architecture-invariant acceptance tests

### Memory

- Public routines preserve canonical mapping regardless of whether the caller or callee is C or assembly.
- IRQ behavior survives temporary MAP scopes.
- Far pointers and DMA resolve identically in Xemu and hardware.
- Resource handles survive relocation.
- Illegal physical ranges are rejected.
- Ordinary C pointers cannot bypass `MemoryAccessABI` or represent arbitrary physical memory.
- Compiler runtime, wrapper, stack, and target-code allocations remain inside their owning ledgers.
- Generated pool, queue, snapshot, fault, stack, compiler-runtime, and asset reports fit their owners with the measured reserve intact.
- The combined gameplay profile and every deliberate one-slot overflow mutation produce the specified admission or fault result.

### Determinism

- PAL and NTSC replays match.
- Presentation ordering cannot affect simulation.
- Simultaneous events follow the frozen order.
- RNG streams remain independent.
- Stale handles fail.
- Render overruns never skip ticks.
- Compiler version, target selection, optimization flags, or C-versus-assembly implementation do not change approved checksum results.
- Full pause of arbitrary wall duration advances no active tick, RNG, mission time, or debt; resume advances exactly one next tick.
- Canonical replay comparison identifies the first divergent tick and field group.

### Coordinates

- All frame transforms match the frozen axes.
- Sector crossings are continuous.
- Deck contact remains within two inches.
- Altitude and operational extent do not overflow.

### Timing

- Protected simulation, protected presentation, world rendering, and reserve are separate.
- Incomplete buffers are never shown.
- HUD, input, audio, warnings, and simulation retain deadlines.
- Compiled C and handwritten assembly are measured against the same target timing and reserve rules.
- PAL and NTSC phase sweeps cover every legal relative tick/raster/DMA/audio alignment and report worst, p50, and p95 costs.
- No legal phase skips or merges a tick, loses an input edge, misses an essential audio/critical-warning deadline, overwrites a snapshot, or breaches reserve.
- DMA blocking and masked-interrupt durations remain within their hardware-measured ceilings.

### Input and presentation handoff

- Ten thousand scripted short, held, repeated, simultaneous, pause/resume, keyboard, and approved-joystick transitions lose or duplicate zero legal semantic edges.
- Delaying presentation beyond two display periods never exposes authoritative state, tears a record, overwrites a held buffer, stalls simulation, or changes checksums.
- Radar/display cadence and quality-tier changes cannot change semantic tracks, fire control, AI decisions, or outcomes.
- Every completed world store identifies one presentation tick; incomplete stores are never displayed.

### State and presentation

- Input cannot bypass actuators.
- Hydraulic failure changes physical control surfaces.
- System colors are derived.
- Palette violations fail the build.
- Grayout preserves essential identity.
- Critical identity is never color-only and remains interpretable in all supported lighting and G-desaturation states.
- Right-display track identity/source/quality and left-display system health/supply/mode/capability derive from authoritative records rather than stored display colors.

### Storage, audio, and missions

- The D81/package manifest proves exact and allocated-byte fit, integrity, residency, and required save/free-space policy.
- Save fault injection across absent, write-protected, full, corrupt, removed, and interrupted media preserves at least one verified generation.
- Essential warning audio starts within the hardware-approved latency under combined load and always has tone/text fallback.
- Mission compilation emits a conservative witness for every pool/concurrency peak and rejects every one-slot overflow fixture.
- Technical Combat Slice and Midnight Spear use distinct manifest identities; no proxy or non-narrative fixture is labeled campaign content.
- Every approved operation/branch/ending must eventually have at least one deterministic acceptance replay before release.

### Host validation

- Production target routines in C or assembly match golden vectors.
- C headers, assembly offsets/macros, and Java bindings agree with the canonical generated interfaces.
- C-runtime restriction checks reject forbidden heap use, floating point in authoritative paths, uncontrolled recursion, unbounded automatic storage, and implicit public/serialized layout dependencies.
- C/assembly wrapper tests verify calling convention, stack, A/X/Y/Z/Q and flag preservation/clobbers, canonical MAP/base-page restoration, and interrupt-state behavior.
- Instrumentation reports required failures and high-water marks.
- Benchmarks include complete identity.
- Every acceptance artifact records requirement IDs, spec/build/package hashes, environment, seed/inputs, duration, measured units, threshold/tolerance, oracle, actual result, first fault/divergence, retained artifacts, and required human sign-off.
- Static bounds, Java oracle, Xemu, physical hardware, and human playtest evidence are not substituted for one another.

The future expansion goals are excluded from these acceptance tests.

---

## 16. Decision log additions

| Decision | Reason |
|---|---|
| LLVM-MOS C is the primary production language | It improves maintainability and development throughput while retaining measured target accountability |
| Handwritten 45GS02 assembly remains first-class and targeted | Platform-critical and measured hot paths still require explicit low-level control |
| No fixed C/assembly percentage exists | The split follows contracts, profiles, budgets, and hardware evidence rather than ideology |
| C is admitted under bounded deterministic-runtime restrictions | The language change cannot introduce heaps, floating-point authority, unbounded stack behavior, implicit layout, or arbitrary physical pointers |
| C/assembly boundaries use a documented generated Platform ABI | Cross-language calls must preserve compiler, stack, register/Q, MAP, base-page, and interrupt invariants |
| Java host oracles remain independent | Target-language migration does not make compiler output or target code the expected-behavior authority |
| C, assembly, wrappers, and runtime support share the existing budgets | The language change does not loosen code, memory, cycle, DMA, or reserve limits |
| A-10 Cuba!, F/A-18 Korea, and Falcon 3.0 are primary feel references | They define the desired systems density, HUD language, and combat-sim character |
| High-resolution rendering is a future measured goal | It must not prejudice R0 mode selection or budgets |
| 720×576-class modes may be benchmarked but are not required | Ambition is preserved without converting hope into architecture |
| Ground objects remain non-destructible | Current capacity, persistence, and rendering rules do not support destruction |
| Destructibility requires analysis and possibly a numbered revision | It affects entities, resources, rendering, missions, and saves |
| R0 and Phase 1 gates remain unchanged | Documentation goals cannot weaken engineering discipline |
| Gameplay Supplement `MUST`s are the player-facing companion baseline | The architecture and gameplay documents now describe one coherent product without promoting tuning classes |
| Simulation and raster clocks are independent | Official timing cannot support an exact six-frame/ten-tick superperiod |
| Presentation uses bounded extracted snapshots | Rendering and audio cannot retain or race authoritative simulation storage |
| One canonical registry generates C, Java, documentation, and any required low-level bindings | Public layouts and numeric semantics cannot drift by implementation language |
| Static/generated bounds precede runtime admission | Pools, queues, snapshots, stacks, assets, packages, and fault records must fit with reserve intact |
| Technical Combat Slice and Midnight Spear are distinct | Engineering proof cannot invent or silently become narrative campaign content |
| Alignment corrections are adopted selectively and C-adapted | Draft assembly-only prescriptions and unrelated benchmark proposals do not override Revision 1.5 |

---

## 17. Smallest authorized next milestone

The smallest authorized milestone remains R0-A:

- Pin authoritative references.
- Pin hardware/model/memory, FPGA core, ROM, system files, video/storage/input configuration, Xemu, LLVM-MOS compiler/MEGA65 target/45GS02 support, SDK/runtime, linker, flags, and any low-level target tools actually used.
- Implement and validate the `MemoryAccessABI` proof.
- Prove required 45GS02 platform behavior, addressing modes, MAP/base-page, DMA, IRQ, and selected hardware-math wrappers on the pinned hardware.
- Compile and link a minimal non-gameplay C target proof.
- Prove narrow C/platform wrappers restore compiler-required stack, register/Q, flags, MAP, base-page, and interrupt state.
- Produce a reproducible D81.
- Generate symbols, compiler/linker maps, target listings where applicable, and the evidence index.
- Establish independent-clock cycle, mapping, DMA, interrupt, stack, and fault instrumentation.

R0-A contains no flight, radar, weapons, H.O.T.S., mission, campaign, high-resolution production renderer, or destructible-world implementation.

The absolute R0 gate and hard Phase 1 integrated-harness gate remain unchanged.

---

## 18. Explicit non-changes in Revision 1.5.1

Revision 1.5.1 aligns Revision 1.5 with the exact Gameplay Supplement and adopts the applicable correction rules listed in §19. It does not redesign the product or authorize implementation.

Revision 1.5.1 does **not** authorize changes beyond those explicit alignments and corrections to:

- Gameplay scope beyond the hash-pinned Gameplay Supplement.
- The ten-operation campaign or two-ending product boundary.
- Unwritten Midnight Spear, operations 3–10, ending predicates, doctrine tables, or narrative content.
- Aircraft, flight, systems, radar, weapons, AI, controls, H.O.T.S., carrier, or presentation behavior beyond adopted Gameplay `MUST`s.
- Any Gameplay `TARGET`, `TBD`, or `R0-GATED` value.
- Memory ranges, capacities, ownership, or reserves.
- The numerical 530,000/100,000/585,000/135,000 planning allocations; Revision 1.5.1 corrects their interpretation and requires measured independent-clock ceilings.
- The 100 Hz simulation tick rate.
- The 21-step tick order.
- Entity identities, pools, capacities, lifecycle, or exhaustion rules.
- RNG algorithms, stream ownership, arithmetic rules, replay, or checksum requirements.
- R0 hardware gates, the 20 Hz world failure floor, or existing R0 acceptance thresholds.
- The measured-limits revision.
- The Phase 1 integrated-engine-harness gate.
- Native high-resolution and destructible-ground-object status as future goals only.

All such requirements remain as stated in this document and retain their existing approval or measurement status.

---

## 19. Technical Alignment correction disposition

Revision 1.5.1 incorporates correction principles from the exact Draft v0.2 input only as listed here. These dispositions take effect only when Revision 1.5.1 receives human approval; the original Draft does not otherwise gain authority.

| Correction | Revision 1.5.1 disposition |
|---|---|
| `CORR-AUTH-001/002` | Adopted as the hash-pinned corpus, approval, and precedence rules in §1.2 |
| `CORR-REF-001` | Adopted through the expanded R0 evidence identity in §11 |
| `CORR-TIME-001` | Adopted; the integer superperiod is removed and replaced by independent-clock worst-phase admission in §§3.1 and 6 |
| `CORR-SNAP-001` | Adopted as bounded extracted `PresentationSnapshot` semantics in §§3.2 and 3.9; byte count and buffer count remain measured |
| `CORR-IFACE-001` | Adopted and C-primary in §10.4; C and Java bindings are required, low-level bindings are generated only where needed |
| `CORR-NUM-001` | Adopted in §4.5 without selecting still-unmeasured fixed-point formats |
| `CORR-INPUT-001` | Adopted at semantic-contract level in §7; bindings and shaping retain their gameplay gates |
| `CORR-PAUSE-001` | Adopted in §3.8 |
| `CORR-FAULT-001` | Adopted in §§3.6, 3.10, and 12.6; player-facing recovery text remains a later product decision |
| `CORR-PLAT-001` | Adopted only as C/platform-service ownership, verified wrapper behavior, DMA/IRQ/MAP/math evidence, and hardware gates; assembly-only production prescriptions are excluded |
| `CORR-MEM-001` | Adopted in §5.4 without changing ranges, capacities, or reserve |
| `CORR-STORE-001` | Adopted in §12.2; exact media UX and package values remain gated |
| `CORR-TOOL-001` | Adopted for LLVM-MOS C in §11; KickAssembler-only and assembly-only build assumptions are excluded |
| `CORR-ASSET-001` | Adopted in §12.1 as bounded manifest/converter requirements |
| `CORR-MISSION-001` | Adopted in §12.3; Technical Combat Slice and Midnight Spear are explicitly distinct |
| `CORR-CAMP-001` | Adopted in §12.3 without inventing campaign content |
| `CORR-RADAR-001` | Adopted in §§1.3, 6.4, and 12.4 |
| `CORR-AUDIO-001` | Adopted in §12.5 with values left to R0 measurement |
| `CORR-REPLAY-001` | Adopted in §10.6 |
| `CORR-TEST-001` | Adopted in §§12.6 and 15 |
| `CORR-BENCH-001` | Not adopted as a product requirement; the F-117A comparison was external to the three product baselines and remains deferred/non-blocking unless separately approved |

Every use of “target code” in these adopted corrections means LLVM-MOS C by default plus only the measured or platform-critical low-level routines permitted by §1.4. Revision 1.5.1 does not restore an assembly-first architecture.
