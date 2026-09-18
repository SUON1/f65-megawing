# R0-F CIA-count diagnostic handoff — 2026-09-17

**Built and tested: F65R0F4.D81 is XEMU_BOOT_VERIFIED.** Subsequent owner photos
show physical acquisition complete and functional PASS; retained under
`docs/evidence/r0f/cia-timing/physical/`. Complete SD provenance, physical raw
validation, calibrated timing and R0-F acceptance remain open. No SD write,
eject, commit, or push was performed by the agent.

Closeout review: `R0-F_CLOSEOUT_REVIEW.md`. The bounded R0-E proxy and F4
measurement do not supply the full combined-service requirements. The owner
has selected full closure on the current design; execution is tracked in
`docs/plans/R0_FULL_CLOSURE_WORK_PLAN.md`. No further SD/hardware action is
requested now. The
build-time record below remains historical, including its original pending
physical-test instructions.

## Artifact

- Path: `build/r0f/cia-timing-safe/F65R0F4.D81`
- Bytes: 819200
- SHA-256: `a30880f83be9c9ff414065d9331d5bba737e393e1a6441f07741e87f000ff39d`
- Disk: `F65 R0-F4`, ID `65`; `AUTOBOOT.C65 -> R0F-PROOF`
- PRG: 10561 bytes, SHA-256
  `6e52b70b77b259363f8bdb8d0d410526864406eedf999ad9e526b7324a310256`
- Source: working tree on `codex/r0-f-development`, HEAD
  `744920dd76d008fbc0ccce82e006cc0b647f477e`; exact source-input hashes are in
  `build-accounting.json` and the D81's `R0F-EVID` file. This is not a clean-commit
  release. The build-time accounting's `d81/xemu` fields describe its pre-package
  state; the later release manifest and Xemu evidence control those gates.

## What changed

New C files `src/platform/r0f/cia_clock.c` and
`src/diagnostics/r0f/timing_sweep.c` add an exclusive, reset-only CIA1 timer,
bounded coherent reads, frame cross-checks, independent raw-count release
scheduling, and a readable results table. `composite.c` exposes its existing
fixture under a timing-build flag; `main.c` selects the new diagnostic only for
that variant. The F2 startup fix is retained. No gameplay was added.

The private JSON contract generates constants. The ledger charges the new
storage. `r0f_build.py` adds an isolated variant, native timer/overrun/fault tests,
and the pinned full-JDK `R0FTimingOracle.java` independent reduction. Generated
header, PRG/ELF, map, symbols, disassembly, host reports, release record and two
Xemu captures were produced. Current control records point here; historical
F1/F2 evidence remains intact.

Before edits, inspected official record, architecture/MemoryAccessABI,
Read-First/AD-001/approval, current memory/interface contracts, R0-D/E/F fixture
and handoffs, startup/B decision and root D81 gate. Full requirements, primary
source pins, register ownership, save/stop behavior and remaining limitations:
`R0-F_CIA_TIMING_CONTRACT.md`.

Register/memory/timing impact: compiled C ABI clobbers A/X/Y/Z/P and compiler
pseudo-registers; B=$02 retained. CIA1 $DC04–07/$DC0E–0F owned exclusively;
reject hidden CIA or active serial-output mode before writes. No ICR, ports,
CIA2, MAP/EOM, DMA, IRQ vector or NMI-source writes. Stock SEI remains in effect;
no interrupt service is measured. Main never returns; reset required. Result
$1900–$19FF, screen $0800–$0FCF, base page $0200–$02FF and hardware stack
$0100–$01FF retain their existing standalone ownership. No new physical mapping
and no allocation/access in protected $050000–$05FFFF. Production canonical
MemoryAccessABI and dynamic stack high-water are not proved.

Linked accounting: BASIC header 22, text 9345, rodata 1192, data 0, BSS 12152,
compiler static stack 158 bytes; total 22869 bytes. BSS $4940–$78B7; static stack
$78B8–$7955; software-stack top $D000. Raw capture starts $4941, length $2A80
(10880). Original samples are retained unsorted; separate sorting scratch is
1056 bytes. No reserve or DMA allocation.

## Verification performed

All commands ran from the repository root:

```sh
F65_R0F_VARIANT=cia-timing sh tools/build/r0f.sh audit
F65_R0F_VARIANT=cia-timing sh tools/build/r0f.sh package
F65_R0F_VARIANT=cia-timing \
F65_MEGA65_ROM='/Users/slice/Documents/Codex/f65-megawing/MEGA65.ROM' \
F65_MEGA65_SD_IMAGE='/Users/slice/Library/Application Support/xemu-lgb/mega65/mega65.img' \
sh tools/build/r0f.sh xemu
git diff --check
```

- Audit PASS: native ASan/UBSan, legacy 358 rejection checks, timer visibility
  and serial-mode guards, byte/cascade/32-bit wraps, bounded unstable reads,
  stop/idempotence, six fault cases, and injected deadline overruns.
- Host Java PASS: 2640 raw records and 80 cohort spans independently reduced;
  functional checksum/counters verified; 35 checksum-correct summary corruptions
  rejected. Injected overload produced 16 deadline misses per case, not a false
  deadline PASS. Pinned Temurin 21.0.12+8 was located in the other checkout;
  its retained archive hash matches the lock. Runtime/compiler hashes retained.
- Target compile/link/map/symbol/disassembly PASS. Ledger reconciled, startup
  B sequence present, no direct ROM calls/jumps or new MAP/EOM instructions.
- Package PASS: fresh format and all three payload writes in one pinned c1541
  session; structural/BAM/chains/ownership/free-block/content extraction gates
  pass with no construction diagnostics.
- Exact-D81 Xemu PASS: two fresh processes, separate disposable emulator SD
  copies, 40 seconds each, pinned emulator/ROM, no carrier-byte change. Each raw
  capture passed Java reduction. Both final screenshots were visually inspected.
- `git diff --check`: PASS.
- A second invocation of the exact `package` command returned expected exit 2
  before any build/media operation: existing carrier identity refused. The F4
  SHA-256 remained unchanged. This is the overwrite-guard negative test, not a
  carrier failure.

Both Xemu runs observed: acquisition complete, inherited functional fixture
PASS, 16 completed requested phases per case, no fault, zero nominal-count
deadline misses, observed READY-snapshot high-water 3. Pre/post 16-frame totals
were 320005 raw counts. Work p50 32 or 64 counts; p95/max 64 counts; maximum
33-tick cohort span 320069 or 320070 counts. These are **emulator observations**,
not physical timing, calibrated microseconds, or proof of real 100 Hz.

Evidence retained under `docs/evidence/r0f/cia-timing/`; complete memory dumps
remain under `build/r0f/cia-timing-safe/xemu/`. Release manifest records all
physical/SD fields as pending. Source hashes distinguish this from earlier
preliminary direct-PRG testing.

F65R0F3.D81 (`62c2f28de32ce3fe60276986e4394ba39ee573b566740d57b1799a8aeaef0a6a`)
was host-built, then withheld before carrier Xemu/SD testing when review added
the serial-mode guard. It remains unchanged; not a chooser/media failure and
not a replacement template. F65R0F2 remains unchanged at its recorded hash.

## Original physical instructions — superseded by the photo review

Do not repeat these steps merely because the original handoff listed them.
The owner has since supplied the F4 completion and platform photos. See the
closeout review for current status and the unresolved delivery evidence.

First record physical MEGA65/core/ROM/HYPPO/Freezer/video/clock identity and
resolve the reported Finder/eject problem. Then create a fresh root slot named
**F65R0F4.D81** using MEGA65 `NEW D81 DD IMAGE`; do not rename F2, F65BLK01 or
F65BLK02. Fill only with the guarded helper after the matching slot/card is
available; require exact hash, unchanged one-extent allocation and successful
safe eject before chooser testing. No transfer command was executed here.

Run AUTOBOOT, wait for the complete/failed acquisition screen, photograph the
entire table and machine identity, and reset afterward. Do not press RESTORE
or enter Freezer during the sweep. Failure code 1 means timer preconditions
were not met; other faults require diagnosis, not a pass override.

This build advances raw measurement, but does not close R0-F. Remaining:
physical execution and external timebase calibration; supported-mode/clock
matrix; exhaustive legal phase and sliding-window coverage; dynamic stack and
other required high-waters; actual input/audio latency and separately admitted
DMA/IRQ evidence where required; owner review/acceptance. The inherited workload
is still a functional proxy. Measured-limits approval and Phase 1 remain separate.
