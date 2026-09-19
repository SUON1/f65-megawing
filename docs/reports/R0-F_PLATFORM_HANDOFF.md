# R0-F PF001 platform development handoff

2026-09-17. **PARTIAL IMPLEMENTATION — FULL COMBINED BUILD NOT READY.**

Owner approval authorized additive proof-platform development and required
Xemu before a native-blank SD delivery. That development has started in actual
C/45GS02 code, not just a plan. The resulting **development PRG** passes the
bounded host/static and Xemu checks below. It is not the combined calibration
and workload carrier the owner requested. No D81 was created or delivered.

## Implemented and observed

PF001 performs a one-way, reset-only canonical entry; installs a resident raster
IRQ; checks A/X/Y/Z/B and carry/decimal canaries across an actual interrupt;
executes and byte-verifies one real 255-byte DMA copy; stages an unsigned PCM
sample in its assigned cache, observes playhead progress, stops it and checks
stability. It collects 16 per-frame raw CIA intervals before and after the
probes and seals a versioned 256-byte result with CRC32.

The independent Java reader validates result structure, CRC, observations and
explicit non-promotion flags. It rejects 316 corrupt/invalid result cases,
including semantic mutations with repaired CRCs. This is not a full workload
oracle or proof of timing, audibility, all IRQ states or physical correctness.

Latest retained Xemu observations, both boots: stage `$7F`, fault `$00`,
B `$02`, stack high `$01`, actual CPU port `$35`, D030 `$44`, 47 raster IRQs,
255 DMA bytes matched, one DMA job, five observed PCM playhead changes and
stopped-state flag 1. IRQ canaries are `A5 5A C3 3C 02 B0 80`.
DMA interval is 64 **raw CIA counts**; frame intervals are 16832/16833 raw
counts. Consecutive-read observation is zero at this timer's resolution, not
zero CPU overhead. No count is converted to seconds or CPU cycles.

## Identity and evidence

- Source baseline: `744920dd76d008fbc0ccce82e006cc0b647f477e`, with existing and
  new uncommitted work. Per-input SHA-256 values in accounting are authoritative.
- PRG: `R0F-PLATFORM.prg`, 4987 bytes,
  SHA-256 `aab353cc713ebe41f242dcec7477aed46619aec79a61929a510aab19dbbe7749`.
- Both result blocks: 256 bytes, CRC32 `CF20D082`,
  SHA-256 `ba8763dbe6635c6acb78403af2dbeafa1dadf6c7110cbe05325a1457ab9d2aa4`.
- Xemu: SHA-256 `dd37baf7846b9696adcb662ffe5da040031b07214c66aef9a7f48cc30040b738`.
- ROM: SHA-256 `af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0`.
- Final boot directories: `xemu-1-1789712149385273000` and
  `xemu-2-1789712184556714000` under `build/r0f/platform-qualification/`.
- Retained artifacts: `docs/evidence/r0f/platform-qualification/`. Includes
  PRG/ELF, map, symbols, disassembly, accounting, native test output, per-boot
  raw results/memory/screens/logs/oracle output, commands and hash inventory.
  The 4GB disposable emulator SD clones remain in `build/`, not the evidence
  package. They are not physical-card images and are not distributable D81s.

Both final screenshots were visually reviewed. They show the development-only
identity and explicit full-workload/calibration/acceptance non-claims.
The exact argument arrays are retained in `xemu.json` and `accounting.json`.

## Inspected requirements and interfaces

Before implementation: official record; root AGENTS and D81 gate; complete
frozen Architecture 1.4.1 including its memory map/MemoryAccessABI; approved
Read-First, AD-001 and approval record; current memory/interface contracts;
B-register integration decision; candidate Architecture 1.5.1 memory/timing/
snapshot requirements; Engine 0.2 §§2.5, 3–5, 8, 11–12, 14–17 and 19; existing
R0-A/B/C platform wrappers; F5 CIA/capture sources; R0-F admission, ownership,
timing, capture and full-closure records. Candidate parents remain candidates.

Exact new private contract and source basis:
`docs/reports/R0-F_PLATFORM_QUALIFICATION_CONTRACT.md` and
`interfaces/r0f_platform_contract.json`. The additive platform registry entry
does not promote old R0-A or R0-C wrappers. Existing ROM-reclaim deferral remains.
No expected combined capture/workload or reversible ROM contract is invented.

The pinned official MEGA65 core source is
[`b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f`](https://github.com/MEGA65/mega65-core/tree/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f).
Inspected CPU, CIA, clocking, video, R6 top-level, I/O map and memory-trap source
hashes are in accounting. This matches the photographed core prefix as source
attribution, not installed-bitstream proof. Xemu audio behavior was checked in
[`audio65.c` at `40dfef0d1d5f56be2469492715c12bdb32c75b67`](https://github.com/lgblgblgb/xemu/blob/40dfef0d1d5f56be2469492715c12bdb32c75b67/targets/mega65/audio65.c).

## Changed paths in this increment

- New implementation: `src/diagnostics/r0f/platform_qualification.c`,
  `platform_model.c`, `src/platform/r0f/qualification_45gs02.s`.
- New generated contract/header: `interfaces/r0f_platform_contract.json`,
  `interfaces/generated/r0f_platform.h`; additive entry in
  `interfaces/f65_platform_abi.json5`.
- New checks/tooling: `tools/diagnostics/r0f_platform_build.py`,
  `r0f_platform_host_test.c`,
  `tools/generators/src/main/java/f65/tools/R0FPlatformOracle.java`.
- Control/accounting: R0-F admission/ownership JSON, private memory ledger,
  official record, stage control, interface/ledger impact, combined admission,
  full-closure plan, test guide, evidence map, PF001 contract and this handoff.
- Generated/retained artifacts under `build/r0f/platform-qualification/` and
  `docs/evidence/r0f/platform-qualification/`.

Earlier dirty C, capture, timing, evidence and tooling changes were preserved;
they are not all products of this increment. No prior proof, preserved source
specification, existing carrier or physical SD file was edited. No commit/push.

## Register, memory, timing and platform impact

| Area | PF001 impact / limitation |
|---|---|
| Registers | C follows pinned LLVM-MOS ABI. Entry clobbers A/X/Y/Z/P and establishes B=02. IRQ saves/restores A/X/Y/Z/Q/B/P/SP. Flat helper returns A, preserving X/Y/Z/B/P/SP; no independent Q preservation claim when A changes. |
| MAP/base page | Zero MAP offsets/megabyte selectors plus EOM; actual port 01=35; temporary B=00 only for port access; B=02 before C. rc0–31 physical 0202–0221; private flat-copy scratch 0222–0229. No temporary MAP windows. |
| Low memory | Screen 0800–0FCF; result 1900–19FF; linked resident 2001–35B2. Hardware stack page 1; software stack top D000. Resident vectors FFFA/B and FFFE/F. |
| Generated ledger | BASIC header 22 bytes, text 4510, rodata 453, data 0, BSS 554, compiler static stack/noinit 15. Dynamic high-water NOT MEASURED. Build enforces linked resident ceiling 8000 and empty ordinary zero-page sections. |
| Physical memory | Source 050000–0500FE, destination 050100–0501FE, PCM 053000–0530FE, immutable list 056000–056010. ROM stores 020000–03FFFF and reserves 057000–05FFFF untouched by the implementation. No physical reserve-sentinel acceptance. |
| DMA | One validated normalized non-overlapping COPY in resource staging. Length 1–255; no zero/64K, chaining, I/O, Attic or hypervisor requests. CPU blocks during hardware DMA, so software cannot time out a hung job; reset required. No admitted latency bound. |
| IRQ/NMI | Real raster IRQ; leaf handler does not call C, access compiler temporaries, MAP or DMA. Eight additional hardware-stack bytes including hardware PC/P. CIA1/2 and audio IRQ sources disabled. NMI has a sticky invalidation flag and four stack bytes; no gameplay NMI. No worst-case response/masking/high-water claim. |
| Timing | CIA cascade raw reads with near-reload rejection; bounded software polling. Per-frame checks are plausibility checks only. No calibrated 100Hz, SI time, CPU-cycle budget, rolling-window or deadline acceptance. |
| Audio/input | PCM register progress/stop observed in Xemu, not physical audibility or latency. SID is silenced on exit; no new SID service proof. Physical input-edge service not implemented. |
| Lifecycle/storage | Reset-only diagnostic; no ROM return, hypervisor trap, gameplay, tactical SD I/O, save or post-reclaim storage. No production ownership, capacities, reserves or tick-order change. |

## Validation commands and results

Run from repository root:

```sh
python3 tools/diagnostics/r0f_platform_build.py build
python3 tools/diagnostics/r0f_platform_build.py xemu
PYTHONPYCACHEPREFIX=build/r0f/platform-qualification/pycache python3 -m py_compile tools/diagnostics/r0f_platform_build.py
python3 -m json.tool interfaces/r0f_platform_contract.json >/dev/null
python3 -m json.tool docs/plans/r0-f-ownership-map.json >/dev/null
python3 -m json.tool docs/plans/r0-f-task-admission.json >/dev/null
python3 -m json.tool memory/r0f-memory-ledger.json >/dev/null
python3 -m json.tool interfaces/f65_platform_abi.json5 >/dev/null
git diff --check
```

All listed commands PASS. Build includes native ASan/UBSan tests for all 255
legal lengths, boundary/overlap/overflow and no-write-on-rejection checks, CRC
golden vector, pinned LLVM-MOS compile/link with warnings as errors, map/symbol/
disassembly checks, and pinned Java compilation with `-Xlint:all -Werror`.
Xemu includes two separate normal-speed launches with disposable SD clones and
316 negative-oracle tests per result. This is **direct PRG regression**, not an
exact-D81 boot or physical test. Build-time accounting's `xemu: NOT RUN` is its
pre-run state; the separate subsequent `xemu.json` supplies run evidence.
The retained artifact inventory also passed
`(cd docs/evidence/r0f/platform-qualification && shasum -a 256 -c SHA256SUMS)`.

Development failures were retained, not promoted: the first run exposed linker
relaxation of a CPU-port access into the wrong base page. Explicit B=00 access
and a linked-disassembly regression check fixed it. A later `-sleepless` run
failed PCM progress because this Xemu services audio through a real-time SDL
callback while emulated video raced ahead. Normal-speed reruns passed. Neither
failure had a D81 identity or physical run. Final review also fixed flag return
ordering in the flat helper and made NMI detection sticky; final evidence uses
those corrected bytes.

## Outstanding dependency and hardware boundary

The full renderer needs `$020000–$03FFFF`. The existing
`R0C-PLAT-ROM-001` contract explicitly remains deferred and requires a documented
reclaim/inverse, supported ROM/system-files/storage matrix and recovery-lockout
behavior. The reviewed memory trap provides write-protect control, not that
complete transaction. See `R0-C_ROM_RECLAIM_RESEARCH.md` and
`R0-C_PLATFORM_CONTRACT_ADMISSION_DRAFT.md`. General proof-development approval
does not supply missing hardware behavior. Do not guess a ROM-restoration path
or replace this dependency with a nominal pass.

Next engineering work is that platform-contract resolution alongside clock
reference/uncertainty and protected-work calibration; then the actual renderer,
input/audio/snapshot/service workload and its full phase/window/fault capture
and independent oracle. PF001 alone does not close RC-1 through RC-5 or R0-F.
Physical ABI, input/audio/DMA/IRQ latency, stack/high-water, storage, reserve and
owner acceptance obligations remain open.

Read-only SD observations: F65BLK01.D81 is 688128 bytes and ineligible;
F65BLK02.D81 is 819200 bytes, with unused/blank contents and FAT32 extent still
unverified. Both are untouched. Eventual local **F65BLK02.D81** must be freshly
formatted/populated in one pinned c1541 session, pass host gates and two clean
exact-image Xemu boots, then fill the same-named verified native destination
in place with hash/extent/eject evidence. Do not duplicate/append the blank as a
construction template, rename an SD slot, or overwrite BLK01. No hardware action
is requested from the owner until the combined carrier is actually ready.
