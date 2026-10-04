# 65Aero Runtime v1.1 - controlled amendment review draft

Status: REVIEW DRAFT. NOT APPROVED, FINAL OR ACTIVE. Date: 4 October 2026.

This proposed successor is defined as the unchanged Runtime v1 PDF plus the exact amendments below. It is not a lossy transcription of the PDF. Unlisted clauses and Appendix A source provenance are unchanged. Acceptance would retain candidate-design status; it would not satisfy the Runtime FINAL freeze gate.

Base: [Runtime v1](../../core/F65_65Aero_Engine_Runtime_and_Technical_Supplement_v1_HUMAN_APPROVED_CANDIDATE_DESIGN.pdf), SHA-256 `bcb50a96ca6aadfd45637c48c4a80a10d8ce61b1e2461ba03448b4f06497d260`.

Proposed coordinated parents: Main v1.7 and Gameplay v1.1 review drafts. Detailed physics: [Physics v4.0 R1](F65_Flight_Physics_and_Simulation_Engineering_v4.0_R1_REVIEW_DRAFT.md). Current Main v1.6 / Gameplay v1 / Runtime v1 candidate remain active. This amendment has no independent override authority.

## R1 - current-reference substitutions

In §0.2's current hierarchy only, replace Physics v3.3 with Physics v4.0 R1, Main v1.6 with the proposed Main v1.7, and Gameplay v1 with proposed Gameplay v1.1. These are conditional successor references, not statements that those drafts are already approved. Do not alter the historical input list in Appendix A.

In §21.1 replace only the opening sentence with:

> Phase 2 fills the production Physics v4.0 and aircraft-system behavior behind the admitted Phase-1 interfaces, using an approved aircraft-data revision and the adopted detailed physics contract.

Retain its completion list, ownership restriction and existing phase gates.

## R2 - replace §11.1 White-paper relationship

Physics v4.0 owns detailed equations, coefficient definitions and data, mass/inertia schedules, control models and gains, actuator/hydraulic models, unaugmented envelope, atmosphere/engine details, numerical comparisons and physics/data acceptance.

Runtime owns integration, state ownership, stage placement, generated public records, mission-load class and package admission, cycle/memory evidence, and fault/replay integration. The adopted Physics revision and convention-registry identity are explicit package dependencies. The runtime rejects unsupported identities rather than inferring compatibility from filenames or coefficient labels.

Detailed physical mathematics remains in Physics. Cross-module sampling and mutation eligibility follow §11.7 below and the corresponding generated contracts; a Physics revision cannot change them unilaterally.

## R3 - replace §11.5 ADLC and autothrottle

ADLC is an approach-control overlay, not a peer fundamental flight law. Selecting AUG_OFF disengages ADLC control authority through the approved transition before direct authority becomes active. A DEGRADED/failure indication may describe capability but cannot retain hidden ADLC commands in direct flight.

Autothrottle remains independent. FCS mode changes do not rewrite its state unless a specific approved safety/state rule requires that transition. Pending throttle corrections are consumed only when still eligible; pilot override, disengagement, failure and reset cannot leave an obsolete controller command eligible for later replay. Eligibility/arbitration follows §11.7 without rerunning an earlier stage.

## R4 - add §11.7 Sampling and handoff contract

The existing 21-stage, exact 100 Hz timeline remains unchanged. At tick n:

- Stage 5 consumes eligible pilot demand/prior controller output and current legal systems/environment inputs. Its engine model uses explicitly identified already-available aircraft feedback, never future stage-8 data.
- Stage 6 combines current stage-5 capability with committed aircraft feedback from the previous tick. Aircraft pose/rates include the stage-10 contact correction. Air data carries its actual source tick and sampling stage; commit does not make a pre-contact observation post-contact.
- A stage-6 autothrottle/ADLC correction is eligible no earlier than stage 5 of n+1. Consumption rechecks authority and override; invalidated pending corrections are not replayed.
- Stage 7 exposes a coherent actual-surface/configuration view for stage 8. Commands are not actual positions.
- Fuel expenditure at stage 5 affects current stage-8/9 mass properties. Stage-11 accepted release and stage-14 damage affect the next eligible aircraft force integration. Rejected release changes neither inventory nor mass. Spawned entities begin physical service only after stage-18 commit.
- ContactEngine resolves stage-10 contact and submits its correction through FlightDynamicsEngine's sole aircraft-motion mutation boundary. No duplicate force/impulse is applied on the next tick.

The generated contract declares each producer, source tick/stage, consumer, age bound, initialization, invalid/stale fallback and cancellation rule. Mission initialization supplies explicit initial samples. Storage resume preserves age on the paused simulation clock; reset/reinitialization clears pending commands. Numeric age limits and fallback control laws remain TBD pending controls validation. No raw struct layout or enum value is allocated here.

Authoritative lag/hysteresis state belongs to FlightDynamicsEngine. Systems, engine, fuel, FCS and actuator state retain ControlAndSystemsEngine ownership. Derived mass/inertia caches must be reproducible from authoritative loading/configuration and model identity; cache keys/invalidation and replay reconstruction are declared. CG state and datum/contact geometry follow Physics §4.4.1 at one atomic effective boundary.

## R5 - additions to §§5, 7 and 23

Append to §5's generated-interface obligations: generate the logical sampling, validity, command-eligibility, actual-configuration, contact-correction, loading-revision and aircraft-package records required by §11.7. Define widths, packing, ownership, lifetime and checksum/replay participation only through the existing generated-contract process. No production ABI is frozen by this amendment.

Append to §7's mission-load admission obligations: before simulation begins, validate aircraft identity, schema and convention compatibility, exact data integrity, admitted physical class/loading/envelope, capacity and resource witnesses. Resolve immutable table residency deterministically; reject an unsupported or non-fitting package. Share immutable type data where admitted. Do not hot-reload authoritative aircraft data or borrow the measured-limits reserve. All owner state, caches, scratch, tables and code count toward existing ledgers. This creates no new allocation or capacity.

Append to §23's freeze checklist: require versioned aircraft schemas/conventions, reproducible compiler identity, source-to-package provenance, high-precision versus bit-exact comparison, interpolation/overflow/invalid-input cases, source-age and override tests, release/contact continuity, and complete combined-load resource evidence. Aircraft-data readiness gates do not replace R0/phase gates or qualified-pilot acceptance.

## R6 - clarification to §12

WeaponAndDamageEngine retains seeker/guidance, target selection, release, lifecycle, fuze, detonation and damage ownership. A shared 3DOF mathematical primitive may provide bounded physical integration using common environment/numeric conventions; it creates no new motion authority in FlightDynamicsEngine and does not alter stage-12 service eligibility.

## Review boundary

R1 is reference/authority migration; R2-R6 clarify and propose integration detail. No stage order, pool capacity, physical law, fixed-point format, memory map, public binary ABI, weapon doctrine or phase gate changes. Required measured limits and current R0-F carry-forward obligations remain open.
