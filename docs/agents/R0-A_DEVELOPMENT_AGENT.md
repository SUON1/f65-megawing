# R0-A Development Agent Record

## Role and status

| Field | Value |
|---|---|
| Role | R0-A development agent |
| Milestone | Phase 0 / R0-A — toolchain, platform, memory-access, and C/45GS02 ABI proof |
| Classification | Non-gameplay proof/candidate artifact set |
| Development authority | Approved Read-First v1.0 and `AD-001` |
| Gate status | **NOT PASSED** |
| Hardware status | **AWAITING HUMAN HARDWARE TEST** |
| Starting branch / commit | `main` / `0f650e7fed72933a2ff9d5eaa9a9bd5a70e92975` |
| Working branch | `codex/r0-a-development` |

## Governing identities

| Artifact | Publication SHA-256 | Status |
|---|---|---|
| Read-First v1.0 | `f957b97e146fc4d35d094072eee52d2cc91185f76c7cef232efe898ce7628cc7` | APPROVED — FIRST-READ AUTHORITY |
| AD-001 | `ce3cb019082081bb7908146de0cc689a74abca517bf32520f5bd9fdf30e375dd` | APPROVED — R0-A–F DEVELOPMENT AUTHORITY |
| Approval record | `9fc23bb8555bbd2b84c8f925e909bc5245448ee87db9fb1fb596e8e67c288d8e` | APPROVED — ACTIVE |
| Architecture 1.5.1 | `46ba078cb397d257de6aeee66cff510c5e3243bca97767db1738d86d9ebd1fec` | Architecture-freeze candidate |
| Gameplay 0.2 | `5db0344f8e7fd66143874310c3794a64391d4767229a90f5caee5e5e287d84e4` | Freeze candidate |
| Engine 0.2 | `dfd4bf0b557b4dae6382de502db42e4b2d269ceaf44bd67440bb6d047341454a` | Architecture-review candidate |
| Frozen Architecture 1.4.1 | `c54f77c817b8263f8d03de3ed442c115ff06b0b622c1f14be122df8963079922` | Last frozen baseline |

## Scope and review boundary

The admitted paths, prohibited paths, ownership map, and stable acceptance identifiers are machine-readable in [`../plans/r0-a-task-admission.json`](../plans/r0-a-task-admission.json), [`../plans/r0-a-ownership-map.json`](../plans/r0-a-ownership-map.json), and [`../../tests/fixtures/r0a/acceptance-ids.json`](../../tests/fixtures/r0a/acceptance-ids.json).

The work may create R0-A tooling, schemas, Java oracles, C proof source, narrow target wrappers, a proof D81, and evidence. It must not implement gameplay, a production renderer, a scheduler/tick loop, or any production ABI, pool, memory-map, reserve, or ownership change.

## Build, test, and evidence interface

The root build interface is `make r0a-bootstrap`, `r0a-generate`, `r0a-host-test`, `r0a-build`, `r0a-xemu`, `r0a-evidence`, `r0a-verify`, and `r0a-clean`. Each stage records verified facts in the toolchain lock, generated reports, and evidence index. The task is not complete unless the commands and their retained outputs agree.

## Stop / escalate

Stop the affected implementation and report the exact authority section if a public ABI, ownership, memory range, reserve, unresolved platform behavior, object/link path, or physical-hardware requirement would otherwise be guessed. `DEC-002`, `DEC-003`, human hardware execution, and R0-A acceptance remain human-review boundaries.

## Current state

Configuration control and governance are committed. LLVM-MOS v23.1.0, Temurin 21.0.12+8, KickAssembler 5.25, and the candidate Xemu identity are pinned from inspected artifacts. The compiler's default MEGA65 startup uses `$0002–$008f` for imaginary registers; the required `$0200` base-page setup path is unverified and blocks conforming target/Xemu/hardware proof. See `docs/evidence/r0a/R0A-TOOLCHAIN-BASE-PAGE-FINDING.md`.
