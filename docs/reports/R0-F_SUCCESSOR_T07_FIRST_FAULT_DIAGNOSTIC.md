# R0-F T07 first-fault diagnostic — 2026-09-23

## Trigger and scope

The physically loadable `R0FDIAG3.D81` reached the successor diagnostic on
the MEGA65 but locked out with screen fault `0x57`, state `0x0A`, tick `0x0021`,
service mask `0x00`, NMI sticky `0x00`, and equal reserve CRCs. The owner
confirmed the exact selected filename. See
`D81_R0FDIAG3_NATIVE_SLOT_2026-09-23.md` and its retained photo.

The old post-storage caller unconditionally called `lockout(87u)` whenever
`run_ticks(33)` returned false. `run_authoritative_tick()` can first set a
more specific fault, which the caller then erased. This prevented the screen
from distinguishing the underlying failure. `0x57` established only that no
post-storage authoritative tick completed; it did not identify the cause.

## Narrow change

`r0fs_post_storage_tick_fault()` now selects an already-recorded nonzero
fault; it returns `0x57` only when none exists. The post-storage failure
branch still enters lockout and still stops audio and IRQ through the existing
`lockout()` path. The private diagnostic contract names the fallback code.
No success predicate, storage operation, simulation tick, display service,
DMA path, or physical memory ownership changed.

This change is diagnostic only. It does not fix or claim to explain the
physical failure. The original `R0FDIAG3.D81` host image and tested SD copy
remain unchanged and must not be retested or overwritten.

## Validation and evidence tiers

- `python3 -B tools/diagnostics/r0f_successor_integration.py build`: PASS,
  including 1,527,538 host lifecycle/continuation/fault checks, CF001 and
  RH001 regressions, target compile/link and static accounting.
- Target PRG: 21,922 bytes, SHA-256
  `5600782308a16976d0d20303e0c8d215b9db0f1dab1680f17e9a07ccfea47d7c`.
- Resident use/capacity: 24,098 / 40,959 bytes; high-water exclusive `0x7E23`.
  Protected transition end remains `0x2B07`; new physical allocations and
  resource/measured-reserve consumption remain zero.
- `python3 -B tools/diagnostics/r0f_successor_post_storage_probe.py`: PASS,
  one NTSC and one PAL direct-PRG Xemu development run. Each used a fresh
  token-only disposable D81 fixture, reached `FAULT 00`, passed independent
  result reduction and the Java oracle. Summary:
  `build/r0f/successor-post-storage-first-fault-probe/summary.json`.
- `python3 -B tools/diagnostics/r0f_successor_physical_diagnostic.py all
  --name R0FDBG07.D81`: PASS. The fresh one-session canonical image is
  `build/r0f/d81-workflow/R0FDBG07/canonical/R0FDBG07.D81`, 819,200 bytes,
  SHA-256 `c780d79a0e24ff00f10fbb7f3829ec943783c8b2d4413417ba389d900edcc775`.
  Independent host structure/content checks and four fresh exact-name carrier
  boots (two NTSC, two PAL) passed with screen fault `00`. Retained release
  and run evidence:
  `docs/evidence/r0f/successor/2026-09-22-workflow/R0FDBG07/`.
  The first NTSC and final PAL screenshots were visually inspected: the
  complete fault/state/tick/mask/NMI and reserve/result rows are legible.
- SD copy, FAT allocation, safe eject, physical chooser and physical runtime
  for T07: NOT RUN.

At this initial build, the source was an uncommitted working tree on
`codex/r0f-successor-physical-exact-carrier` at HEAD
`ae2b397698cc7197d03349e57cd058b4fb9f3987`; the PRG hash pins the built
target but that initial run was not a pushed source freeze or final release
identity. See the source-freeze follow-up below.

## Hardware and contract impact

- Registers/clobbers: no change to VIC-IV, CIA, SID/PCM, DMA, keyboard or
  storage wrapper register interactions. On post-tick failure, the existing
  lockout still stops audio and IRQ.
- CPU-visible/physical memory: no new allocation or range; only one byte of
  additional resident linked code under the existing envelope.
- MAP/base-page and KERNAL return: unchanged.
- DMA: unchanged; no new submission or ownership change.
- Timing/deadline: 100 Hz release, 21-stage order and the 33/33 tick boundary
  unchanged; the selection runs only after a failed post-storage tick.
- IRQ/NMI: existing stop/restore paths and sticky NMI behavior unchanged;
  original inner NMI fault can now remain visible rather than be replaced.
- Private result layout and public ABI: unchanged. The private diagnostic
  fault enumeration adds a name for the existing fallback value `87`.

## Next boundary

The fresh exact-name carrier has passed host and Xemu gates and is retained
locally. It is **not SD- or physically verified**. A physical retest needs a
separate safe SD delivery decision and exact one-extent/hash/safe-eject proof;
neither a plain copy nor reuse of the failed physical carrier is allowed.
The owner's Finder-copy preference remains respected, but a Finder copy alone
is not an SD allocation gate. The existing card's unrelated FAT errors block
the direct allocator's clean-filesystem gate; no card repair is authorized.
Do not run broader R0-F acceptance while the post-storage runtime failure
remains open.

## Source-freeze follow-up — 2026-09-24

Source, private contract, generated header, delivery tooling and tests were
committed as `e8caf09002b7793be2effd9f5badd825aeedf301` and pushed to
`origin/codex/r0f-successor-physical-exact-carrier`. The post-commit host/target
build again passed 1,527,538 successor checks, CF001 and RH001 regressions,
target compile/link and static accounting. Its 21,922-byte PRG still hashes to
`5600782308a16976d0d20303e0c8d215b9db0f1dab1680f17e9a07ccfea47d7c`.
The existing canonical `R0FDBG07.D81` still hashes to
`c780d79a0e24ff00f10fbb7f3829ec943783c8b2d4413417ba389d900edcc775`;
it was not rebuilt or mounted writable. Its original construction record
truthfully retains the pre-freeze working-tree identity.

After the source push, four new disposable exact-name carrier copies passed
Xemu (two NTSC, two PAL), independent result reduction and the Java oracle.
Each displayed fault `00`, state `09`, tick `0042`, service mask `1F`, NMI `00`
and equal reserve CRCs. The first NTSC and final PAL screenshots were visually
checked. The new run evidence and release snapshot are retained under
`docs/evidence/r0f/successor/2026-09-22-workflow/R0FDBG07/post-source-freeze-e8caf09/`;
the run records name source commit `e8caf09002b7793be2effd9f5badd825aeedf301`.
The release snapshot's top-level `SOURCE_COMMIT` still identifies the original
pre-freeze construction; its `XEMU_EVIDENCE` entries identify the post-freeze
runs. A first post-freeze attempt produced no runtime result because sandboxed
Xemu could not save its configuration template; that log is retained in the
same evidence directory under `failed-environment/`. A fresh retry with app
configuration access produced the four passes.

These checks establish source-frozen exact-carrier Xemu evidence, not SD
allocation, safe eject, physical chooser, physical runtime, or R0-F acceptance.
No card write or filesystem repair occurred in this follow-up.
