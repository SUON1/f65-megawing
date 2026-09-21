# R0-F T04 successor emulator and exact-carrier handoff

Date: 2026-09-21

Status: **READY FOR REVIEW - XEMU BOOT VERIFIED ONLY**

## Outcome

T04 established the first direct and exact-carrier Xemu runtime evidence for
the frozen successor architecture. The reviewed T03 input was reproduced
before any runtime correction. Direct execution then exposed two entry
assumptions; bounded corrections were made, the target and all carriers were
invalidated and rebuilt, and the complete T03 host/static regression remained
green.

The final immutable local canonical is:

- path: `build/r0f/successor-t04/canonical-10/R0FSUCC10.D81`;
- bytes: 819,200;
- SHA-256:
  `3721dff9b84cfb7842cc154f6885861e0c7cbd3c3408c8ecec190bf6b405d461`;
- state: `XEMU_BOOT_VERIFIED`;
- label/id: `R0F SUCC T04` / `65`.

It is an ignored local build artifact, not tracked evidence. The corrected
non-D81 evidence is under `docs/evidence/r0f/successor/2026-09-21/`. The prior
`2026-09-20/` set is retained explicitly as historical diagnostic evidence and
is not final Gate-3 evidence.

All corrected evidence was rebuilt from clean source-freeze commit
`20b2aab382d0590037443b6a352fbc77fda7aa42` on branch
`codex/r0f-successor-emulator-exact-carrier`. The source-freeze commit was
pushed before the runtime rerun. Every corrected manifest records that exact
source commit.

## Baseline and corrected target identity

Local `main`, `origin/main`, and live GitHub `main` were refreshed and verified
at `e3cf022c73e76679d85532795d9f79095fa8ead5` before branch creation. A fresh
T03 build reproduced the reviewed image exactly:

- 21,489 bytes;
- SHA-256
  `43074a4322b9a2ec35428e966d9f64ab30655c8f0f27516317e7e3f9e417264a`;
- resident 23,665 / 40,959, margin 17,294;
- high-water exclusive `$7C72`, protected end exclusive `$2B0F`;
- Attic transition 5,664 bytes, new physical allocations 0, reserve 0.

The reproduced image's first direct run correctly failed closed rather than
being treated as evidence. Diagnosis established that it consumed linked
high-BSS state before canonical entry and touched direct-page/I/O state before
clearing the inherited MAP. T04 therefore:

1. calls `cfentry()` before lifecycle initialization or `cfscreen()`; and
2. performs the official one-operation all-zero MAP clear before selecting
   B=0, setting CPU port `$35`, and normalizing I/O.

The corrected target is:

- 21,481 bytes;
- SHA-256
  `d0979c56c373f8885e4741670141ebf22c0a2e9ef8a84f6a931eaef05592d9df`;
- resident 23,657 / 40,959, margin 17,302;
- high-water exclusive `$7C6A`, protected end exclusive `$2B07`;
- Attic transition 5,664 bytes, new physical allocations 0, reserve 0.

No public ABI, generated contract, memory ownership, stage order, 100 Hz tick
model, production storage ABI or measured limit changed.

## Authority, contracts and hardware effects

The governing inputs were the current specification-corpus authority order,
T01 reconciliation, frozen T02 contract and ledgers, reviewed T03 source,
private integration contract/ledger and handoff, development workflow, C style
standard, and the root D81 loadability gate. The gate's mandatory block is
retained verbatim in both the execution plan and runner.

- Registers/clobbers: the one-way platform entry owns A/X/Y/Z, B, status, MAP,
  CPU port and I/O normalization as before. The correction changes order, not
  the final state.
- CPU-visible/physical memory: target ownership is unchanged. The carrier-only
  bootstrap transiently uses bank-0 `$1000-$106A` and failure capture
  `$0FF0-$0FF3` before target entry; the exact target is then loaded at its PRG
  address. `$058000-$05FFFF` remains untouched.
- MAP/base page: one all-zero MAP operation establishes canonical physical
  visibility before `$01`; B is then restored to 2 before C code.
- DMA: no ownership change; application DMA remains synchronous and empty at
  the KERNAL boundary.
- Timing/deadline: the authoritative 100 Hz schedule and 21 stages are
  unchanged; lineage remains tick 33 `D9EEAB81` to tick 66 `307A70D6`.
- IRQ/NMI: quiesce/restoration and sticky-NMI fail-closed behavior are
  unchanged.

## Canonical D81 admission

The final image was fresh-formatted and populated once in one pinned `c1541`
construction session. It contains only:

| Entry | Bytes | Extracted SHA-256 |
|---|---:|---|
| `AUTOBOOT.C65` | 464 | `9bdf352c44c411965229f68b2d92c358f08f0e6ef6486142115b53c9da246cc7` |
| `R0FSUCC` | 21,481 | `d0979c56c373f8885e4741670141ebf22c0a2e9ef8a84f6a931eaef05592d9df` |
| `TOKEN` | 34 | `0e8d0ac2ce727ba51285be0173ea784b52b56fdc4729a1f7c0d2d7271005b572` |

The boot entry embeds a compiled 107-byte bootstrap with SHA-256
`84f6e574fe042001fcbed64e0ca7c274d4c847835deea8a64c7f39f1cdbb6bba`.
It is placed at `$1000`, selects KERNAL bank 0 through `$FF6B`, loads the exact
on-disk `R0FSUCC` PRG using its embedded address, and jumps to linked `_start`.

Independent inspection verified the D81 header, label/id, both BAM sectors,
directory chain, every file chain, allocated-sector uniqueness, extracted
payload equality and free-block accounting. The BAM has 92 allocated and
3,108 free sectors; `c1541` reports 3,072 user blocks free, with the 36-sector
difference being the free directory-track sectors excluded from its display.
The canonical was made read-only and was never mounted in Xemu. Its hash was
rechecked after all runs and remained unchanged.

## Clean runtime evidence

Direct diagnostic runs passed independently before final carrier admission:

| Run | Result SHA-256 | Result CRC32 | SAVE SHA-256 |
|---|---|---|---|
| NTSC | `bd42a640d4f85c9fc8ccd79d92a48c5bfcee8b718ecf9eb6d6db383a61671b5c` | `0B7BB5BF` | `86bef4e96b96b157857587afe9bc5d9d5f69e4849320affe5b867a19e6627784` |
| PAL | `9d2bbb223afa30f8f53da10069c4b479ec12ea3e5cddfbbf1f0f737b2addb1a9` | `C3906812` | `86bef4e96b96b157857587afe9bc5d9d5f69e4849320affe5b867a19e6627784` |

Each exact-carrier run started with a new writable copy whose SHA-256 matched
the canonical and whose mounted basename was exactly `R0FSUCC10.D81`. All four
copies passed target validation, Python reduction, the independent Java
oracle, post-run filesystem validation and extracted SAVE comparison:

| Run | Result SHA-256 | Result CRC32 | Post-run D81 SHA-256 |
|---|---|---|---|
| NTSC 1 | `b0a00c09c9e260466e36a6d054954c3d000061fd3a72c1f4ce3720a5661bf796` | `9B3415E1` | `2ad1c08b75efcae9e35438bf82da3ba23e59666ef8c2a7296c939aa56d55134d` |
| NTSC 2 | `aa792655fb0f210820fa6e5f7e61eee28154150e3a20b095bb0e2aeb663d5209` | `67698C03` | `2ad1c08b75efcae9e35438bf82da3ba23e59666ef8c2a7296c939aa56d55134d` |
| PAL 1 | `be60689f0adc7e2bb28c6f5cde73392878d4ba56e813a5f55f0fa73c782b1bad` | `18B7D55B` | `2ad1c08b75efcae9e35438bf82da3ba23e59666ef8c2a7296c939aa56d55134d` |
| PAL 2 | `54bba56f94e156b923b23db0f294b56a7fed3ca8a62e52bd893d9473376a6ceb` | `74CDED2E` | `2ad1c08b75efcae9e35438bf82da3ba23e59666ef8c2a7296c939aa56d55134d` |

Every clean run recorded identity `RSI1`, fault 0, lifecycle 9, completion
stage `$7F`, ticks 33 to 66, lineage `D9EEAB81` to `307A70D6`, valid context
invalidation, identical pre/post ROM, low-memory, DOS and reserve CRCs, sticky
NMI 0, resumed service mask `$1F`, storage phase 5, storage error 0, returned
1 and denied 0. Every extracted SAVE has SHA-256
`86bef4e96b96b157857587afe9bc5d9d5f69e4849320affe5b867a19e6627784`.

## Fault and fail-closed evidence

- Missing `TOKEN` produced the contracted fault 77 (`$4D`), lifecycle 10,
  stage 3 and no false resumed service/PASS.
- Invalid `TOKEN` produced the contracted fault 78 (`$4E`), lifecycle 10,
  stage 3 and no false resumed service/PASS.
- The Java oracle rejected a corrupted completion record and a corrupted SAVE
  payload.
- The Python reducer rejected the corrupted completion/CRC record.
- No destructive-media case was invented, and the canonical was not modified.

All failed diagnostic and carrier identities were retired in place and never
repaired, appended to or used as a starting image for a claimed run. Only
`R0FSUCC10.D81` is the successful canonical identity.

## Validation and evidence boundary

Passed checks include full T03 host/static regression (1,516,258 lifecycle
checks), fresh CF001/RH001 regressions, LLVM-MOS compile/link, map/symbol/
disassembly and protected-access checks, generated bindings, JSON, Python and
shell syntax, D81 structural/content validation, exact extraction comparison,
direct NTSC/PAL Xemu, two NTSC and two PAL exact-carrier boots, independent
result/SAVE oracles, mutation extraction, fault lockouts, artifact hygiene and
`git diff --check`.

The retained evidence intentionally excludes every D81. Repository static CI
allows only the existing `docs/evidence/r0f/combined/F65BLK02.D81` exception;
it does not establish emulator, SD, physical or R0-F acceptance evidence.

## Non-claims and next task

T04 does not establish `SD_COPY_VERIFIED`, `SD_CONTIGUITY_VERIFIED`,
`PHYSICAL_CHOOSER_VERIFIED`, `TEST_ELIGIBLE`, physical MEGA65 behavior,
measured-limit freeze, founder acceptance or full R0-F acceptance.

After founder approval, the next bounded task is physical exact-carrier
confirmation of this exact canonical identity. It must separately authorize
copying the exact bytes to SD, verify the copied hash, prove exactly one FAT32
extent, safely eject, verify physical chooser attachment, run the physical
target and retain physical evidence. Measured-limit closure remains later.

The corrected evidence commit is the commit containing this handoff and the
two dated evidence directories. Stop here after pushing it to the existing
branch. Do not open or merge a PR, touch SD, perform physical work or start the
next task without separate authorization.
