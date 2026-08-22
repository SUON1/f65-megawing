# F-65 Megawing Official Project Record

This file is the primary status and configuration index for the project. It does not replace the preserved specifications or approve draft material.

## 1. Project identity

| Field | Current value |
|---|---|
| Project | F-65 Megawing |
| Target platform | MEGA65 |
| Production target language | LLVM-MOS C primary; selective 45GS02 for admitted platform-critical or measured work |
| Host tooling and reference models | Java |
| Repository | `f65-megawing` |
| Branch | `main` |
| GitHub remote | `https://github.com/SUON1/f65-megawing.git` (private) |

## 2. Specification authority

The exact machine-readable record is [`spec/manifests/spec-corpus.json`](spec/manifests/spec-corpus.json).

| Exact filename | Version | Declared status | SHA-256 | Authority and current state | Repository location |
|---|---|---|---|---|---|
| `F-65_Technical_Alignment_and_Read_First_Supplement_v1.0.md` | 1.0 | APPROVED — FIRST-READ AUTHORITY | `f957b97e146fc4d35d094072eee52d2cc91185f76c7cef232efe898ce7628cc7` | Approved orientation and configuration control; does not approve parent candidates | `spec/alignment/F-65_Technical_Alignment_and_Read_First_Supplement_v1.0.md` |
| `F-65_Architecture_Decision_AD-001_R0_Program_Development_Authorization.md` | 1.0 | APPROVED — R0-A–F DEVELOPMENT AUTHORITY | `ce3cb019082081bb7908146de0cc689a74abca517bf32520f5bd9fdf30e375dd` | Development authorization only; it does not pass any R0 gate | `docs/decisions/F-65_Architecture_Decision_AD-001_R0_Program_Development_Authorization.md` |
| `F-65_Specification_Approval_Record_2026-08-20_R0_Development.md` | 1.0 | APPROVED — ACTIVE | `9fc23bb8555bbd2b84c8f925e909bc5245448ee87db9fb1fb596e8e67c288d8e` | Records the human approval scope and exclusions for Read-First v1.0 and AD-001 | `docs/approvals/F-65_Specification_Approval_Record_2026-08-20_R0_Development.md` |
| `F-65 Megawing Revision 1.5.1 — Architecture Invariants.md` | 1.5.1 | Architecture-freeze candidate | `46ba078cb397d257de6aeee66cff510c5e3243bca97767db1738d86d9ebd1fec` | Highest current architecture candidate; Revision 1.4.1 remains the last frozen baseline | `spec/architecture/F-65 Megawing Revision 1.5.1 — Architecture Invariants.md` |
| `F-65 Megawing Revision 1.4.1.md` | 1.4.1 | Frozen architecture baseline | `c54f77c817b8263f8d03de3ed442c115ff06b0b622c1f14be122df8963079922` | Last frozen architecture baseline retained for context and preserved contracts | `spec/architecture/F-65 Megawing Revision 1.4.1.md` |
| `F65_Gameplay_and_Simulation_Requirements_Supplement_Draft_0.2.md` | Draft 0.2 | Freeze candidate | `5db0344f8e7fd66143874310c3794a64391d4767229a90f5caee5e5e287d84e4` | Candidate player-facing requirements; not an approved production baseline | `spec/gameplay/F65_Gameplay_and_Simulation_Requirements_Supplement_Draft_0.2.md` |
| `F-65 Engine Runtime and Toolchain Design Supplement Draft 0.2.md` | Draft 0.2 | Architecture-review candidate | `dfd4bf0b557b4dae6382de502db42e4b2d269ceaf44bd67440bb6d047341454a` | Candidate implementation contract subordinate to Architecture and Gameplay; not approved | `spec/engine/F-65 Engine Runtime and Toolchain Design Supplement Draft 0.2.md` |
| `F65_Engine_Runtime_and_Toolchain_Design_Supplement_Draft_0.1.md` | Draft 0.1 | Historical architecture-review candidate | `63f0d2e136507485296bd3424e83e9db796b2bf612d81f3fe5ac2744297d27aa` | Preserved historical provenance; superseded as the current candidate by Engine 0.2 | `spec/engine/F65_Engine_Runtime_and_Toolchain_Design_Supplement_Draft_0.1.md` |
| `F-65_Technical_Alignment_and_Corrections_Supplement_v0.2.md` | 0.2 | Historical/superseded draft | `fd8188f3787d902466a3d07b13c46e88f9afe32d7d5839945c4bc33143e0249b` | Preserved historical orientation/audit; Read-First v1.0 is the current approved operating alignment | `spec/alignment/F-65_Technical_Alignment_and_Corrections_Supplement_v0.2.md` |

Current precedence is:

1. Approved Read-First v1.0 governs orientation and configuration control.
2. Approved AD-001 governs whether bounded R0 proof work may be developed now.
3. Architecture 1.5.1 remains the highest architecture candidate; Revision 1.4.1 remains the last frozen baseline.
4. Gameplay 0.2 remains a freeze candidate and Engine 0.2 remains an architecture-review candidate; neither is silently approved.
5. Engine 0.1 and Alignment 0.2 remain preserved historical provenance.

Revision 1.4 is referenced as superseded and retained by Revision 1.4.1 but was not supplied. Its filename, contents, and hash are unknown. Nothing in this repository resolves or reconstructs it.

## 3. Current engineering state

R0-A and R0-B are closed bounded proof milestones; their accepted evidence is
retained in their handoffs and evidence maps. The project is now performing
bounded R0-C proof implementation under AD-001. This status correction does
not pass R0-C or promote any candidate specification. Autonomous full-game
production remains unauthorized. The repository does not authorize production
flight, radar, weapons, tactical AI, campaign, audio, gameplay, or
production-renderer code.

Draft, proposed, `TBD`, `TARGET`, and `R0-GATED` material remains exactly that until the named human or measurement gate changes its status.

## 4. Current authorized milestone: R0-C

R0-C is the current bounded proof milestone. Its scope is limited to
production-shaped host asset/mission tools; deterministic package and D81
proof; conservative capacity witnesses; non-shipping resource residency and
staging; non-tactical disk dependency proof; save-transaction fault
infrastructure; and explicit ROM-reclaim/storage-handoff investigation.
It contains no gameplay implementation and does not select a production
renderer, resource layout, package version, save medium, or campaign disk
boundary.

## 5. Hard gates

- R0 hardware measurement is mandatory; Xemu supports regression but cannot close hardware-sensitive behavior.
- A measured-limits revision must freeze the hardware-dependent display, timing, memory, DMA, input, and audio values used downstream.
- The Phase 1 integrated-engine harness is a hard gate: all core engines must run concurrently within the accepted limits with deterministic evidence.
- Gameplay implementation may not merge before the applicable R0-F/measured-limits and Phase 1 gates specified by the governing documents.

## 6. Human-owned decisions

Codex and other implementation agents may not autonomously decide architecture changes, public/core contract changes, player-visible gameplay changes, flight or control feel, still-gated defaults, difficulty, mission/campaign creative content, production coefficients, `R0-GATED` values, reserve/resource changes, product scope, or acceptance waivers.

## 7. Open high-priority issues

- Revision 1.4 is missing; a human must supply and hash it or explicitly approve a consolidated-corpus disposition.
- Gameplay 0.2 and Engine 0.1 remain candidates, not approved production baselines.
- Every correction in Alignment 0.2 remains proposed unless separately approved and recorded.
- The supported MEGA65 hardware/core/ROM/video/storage/input matrix requires explicit closure and evidence identity.
- Snapshot lifetime/storage, independent display-versus-simulation timing, storage transactions, canonical interfaces/numerics, and other later contracts remain open at their named gates.
- Alignment 0.2 identifies some items as blockers for formal milestone acceptance; because that document is itself draft, those classifications are retained as review findings rather than silently promoted here.
- `DEC-002` (candidate specification approval state) and `DEC-003` (supported platform/evidence matrix) remain open; their absence does not block bounded R0-A construction but does block the relevant formal acceptance.

These later-phase gaps do not prohibit independent, bounded R0-A work unless an authoritative source or explicit human decision says they do.

## 8. Repository conventions

- Preserved files under `spec/` are source records and are not casually edited.
- Generated artifacts must identify their source and generator and remain distinguishable from authority documents.
- Generated files are regenerated, not hand-edited.
- Substantive work uses task-specific branches and focused commits after the bootstrap of `main`.
- Tests, logs, measurements, and retained evidence accompany implementation at the required evidence tier.
- Contradictions are recorded and escalated; they are never silently reconciled.
- Shared memory, ABI, timing, and ownership changes require matching memory-map or decision-log updates.

## 9. Append-only change log

| Date | Bootstrap/project version | Major action | Commit | Human approval status |
|---|---|---|---|---|
| 2026-08-17 | Repository bootstrap 0.1 | Created the local project home, preserved the four supplied documents, recorded hashes/status, and established empty ownership structure | Initial bootstrap commit containing this record; resolve with Git history after commit creation | User authorized repository bootstrap only; no draft, correction, TBD, or architecture decision was approved by this action |
| 2026-08-17 | Repository bootstrap 0.1 | Configured the private GitHub remote and published `main` | Initial bootstrap commit `7c9beb26a33e7a47c75893b595bc2e56c131aa8f`; this append-only publication entry is in the following project-control commit | User created the private repository and authorized publication; specification approval state is unchanged |
| 2026-08-20 | R0 configuration synchronization | Added exact approved Read-First/AD-001/approval-record copies and candidate Architecture 1.5.1/Engine 0.2; updated control index without promoting candidate parents or passing R0 | Pending configuration-control commit | AD-001 authorizes development only; `DEC-002`, `DEC-003`, physical evidence, and human acceptance remain open |
| 2026-08-20 | R0-A handoff / R0-B admission | R0-A focused physical base-page and pointer proof was owner-recorded as passed at `1ab5b62`; created bounded R0-B graphics/display/cockpit/palette/input/representative-audio proof admission on `codex/r0-b-development` | R0-B admission commit | R0-B development is authorized by AD-001; parent candidates remain unapproved; no R0-B physical evidence or production selection is implied |
| 2026-08-21 | R0-B closure / R0-C admission | Recorded accepted R0-B physical composite evidence at `18cac27f1d0de9b50123ccfd4148ad40a3ecec4c` and opened bounded R0-C proof implementation on `codex/r0-c-development` | R0-C reconciliation commit | R0-B is closed PASS only for its admitted proof scope. R0-C remains development work; `DEC-012`, physical storage/media evidence, and human acceptance remain open. |
