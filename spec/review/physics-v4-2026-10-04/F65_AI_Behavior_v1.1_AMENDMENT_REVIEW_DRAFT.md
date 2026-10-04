# AI Behavior v1.1 - controlled amendment review draft

Status: REVIEW DRAFT. NOT APPROVED OR ACTIVE. Date: 4 October 2026.

This proposed successor consists of the unchanged [AI v1.0 PDF](../../subsystems/F-65_Megawing_AI_Behavior_and_Decision_Architecture_White_Paper_v1.0.pdf), SHA-256 `d11877582c44aed5088354e871bc7825d4dd46fb406e55dbecf84d7a01a85d20`, plus the following exact amendment. No full-document transcription is asserted.

## Replace §27.2 and its contents entry

### 27.2 Degraded-FCS mapping under the adopted Physics/Runtime contracts

Physics / FCS integration must provide the deterministic mapping from AI guidance modes to legal degraded control behavior under FCSStatus = NORMAL, DEGRADED and DIRECT_ONLY. The mapping is compiled/validated against the adopted Physics v4.0 and Runtime integration identities, not inferred from a document filename.

AI may request only behavior the remaining control capability can honor. Requests use the approved command path and eligible tick; AI never bypasses FCS, hydraulics, mixer/gearing, actuator limits or the aircraft's physical force/integration path. Capability and feedback source age/validity are consumed through generated views, not access to another owner's private state. Values, schedules and generated layouts remain later controlled work.

## Parent table treatment

Retain the existing parent/input table in the v1.0 PDF as provenance. In this successor add a distinct current-contract note: proposed controlling parents are Main v1.7, Gameplay v1.1 and Runtime v1.1 amendment, with Physics v4.0 R1 as detailed physics. All are review drafts in this package; the admitted corpus remains unchanged until coordinated approval.

## Unchanged scope

§27.3's mission-selected, bounded, deterministic, 100 Hz KINEMATIC path remains unchanged. No AI doctrine, difficulty rule, targeting knowledge, capacity, guidance gain, command privilege or physical-class switching is introduced. All other v1.0 clauses remain unchanged.
