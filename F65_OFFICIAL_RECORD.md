# F-65 Megawing Official Project Record

This file is the primary status and configuration index for the project. It does not replace the preserved specifications or approve draft material.

## 1. Project identity

| Field | Current value |
|---|---|
| Project | F-65 Megawing |
| Target platform | MEGA65 |
| Production target language | 45GS02 assembly |
| Host tooling and reference models | Java |
| Repository | `f65-megawing` |
| Branch | `main` |
| GitHub remote | Not configured; GitHub CLI is not currently installed/authenticated on the bootstrap host |

## 2. Specification authority

The exact machine-readable record is [`spec/manifests/spec-corpus.json`](spec/manifests/spec-corpus.json).

| Exact filename | Version | Declared status | SHA-256 | Authority and current state | Repository location |
|---|---|---|---|---|---|
| `F-65 Megawing Revision 1.4.1.md` | 1.4.1 | Frozen architecture baseline | `c54f77c817b8263f8d03de3ed442c115ff06b0b622c1f14be122df8963079922` | Current architecture authority, subject to the unresolved incorporated-Revision-1.4 corpus issue | `spec/architecture/F-65 Megawing Revision 1.4.1.md` |
| `F65_Gameplay_and_Simulation_Requirements_Supplement_Draft_0.2.md` | Draft 0.2 | Freeze candidate | `5db0344f8e7fd66143874310c3794a64391d4767229a90f5caee5e5e287d84e4` | Candidate player-facing requirements; not an approved production baseline | `spec/gameplay/F65_Gameplay_and_Simulation_Requirements_Supplement_Draft_0.2.md` |
| `F65_Engine_Runtime_and_Toolchain_Design_Supplement_Draft_0.1.md` | Draft 0.1 | Architecture-review candidate | `63f0d2e136507485296bd3424e83e9db796b2bf612d81f3fe5ac2744297d27aa` | Candidate implementation contract, subordinate to Architecture and Gameplay; not approved | `spec/engine/F65_Engine_Runtime_and_Toolchain_Design_Supplement_Draft_0.1.md` |
| `F-65_Technical_Alignment_and_Corrections_Supplement_v0.2.md` | 0.2 | DRAFT — REQUIRES HUMAN REVIEW | `fd8188f3787d902466a3d07b13c46e88f9afe32d7d5839945c4bc33143e0249b` | Review/correction and orientation layer only; its proposed corrections are not authoritative | `spec/alignment/F-65_Technical_Alignment_and_Corrections_Supplement_v0.2.md` |

Current precedence is narrow:

1. Revision 1.4.1 is identified by the supplied corpus as the frozen architecture authority.
2. Gameplay 0.2 governs player-facing behavior only after human approval; it is presently a freeze candidate.
3. Engine 0.1 is subordinate to Architecture and Gameplay and is presently an architecture-review candidate.
4. Alignment 0.2 is useful first-read review evidence, but only individually approved corrections could gain scoped precedence.

Revision 1.4 is referenced as superseded and retained by Revision 1.4.1 but was not supplied. Its filename, contents, and hash are unknown. Nothing in this repository resolves or reconstructs it.

## 3. Current engineering state

The project is entering implementation through bounded documentation, host-foundation, and R0-A work. Autonomous full-game production is not authorized. Repository bootstrap does not authorize production flight, radar, weapons, tactical AI, campaign, audio, gameplay, or production-renderer code.

Draft, proposed, `TBD`, `TARGET`, and `R0-GATED` material remains exactly that until the named human or measurement gate changes its status.

## 4. Current authorized milestone: R0-A

R0-A is the smallest authorized engineering milestone. Its scope is limited to:

- pinning authoritative reference, toolchain, hardware, core/bitstream, ROM, system-files, video-standard, and emulator identities;
- reproducible host build and bootable D81 proof;
- MemoryAccessABI and canonical mapping/base-page restoration proof;
- required 45GS02 opcode, extended-addressing, and wrapper proof;
- symbols, listings, and build/evidence identity;
- timing, MAP, DMA, IRQ, and interrupt-safety instrumentation; and
- initial non-shipping schemas, ledgers, generators, diagnostics, and fixtures required to make that proof reproducible.

Proxy data may be used only when clearly non-shipping. R0-A contains no gameplay implementation.

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
