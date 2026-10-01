# Group 1 integrated capacity trace and operator summary — 2026-10-01

The isolated integrated candidate passes resident fit, native host checks and
fresh focused NTSC/PAL acquisition. It exports the full existing 327,680-byte
trace allocation in twenty closed chunks and displays a compact terminal
summary. The new local carrier passes host structure/content and all four
clean exact-name NTSC/PAL boot gates. No SD write, physical run, commit, push
or acceptance promotion.

## Authority and implementation

The approved [Group 1 Build Intent](../plans/R0-F_GROUP1_BUILD_INTENT.md),
[measurement protocol](../plans/R0-F_GROUP1_MEASUREMENT_MATRIX.md) and
[terminal export amendment](../plans/R0-F_GROUP1_EXPORT_AMENDMENT.md) govern.
Private pool version 2 and presentation version 3 remain unchanged.

The passing `523d0369...` PRG, `R0FG1P03.D81`, root passing `25a18c23...`
inputs/carrier and original `ec259fc7...` baseline remain untouched. Changes
are in `build/r0f/group1/capacity-summary/integrated-02/source-inputs/`, not
an overwrite of their root or frozen proof source.

Trace version 7 retains the exact header, 3,200 real tick records, actual
512-byte successor result, two cumulative owner checkpoints and real world
events. After measured acquisition stops, unused bytes between the actual
world log and the final CRC receive a declared diagnostic pattern:
`(absolute_trace_offset & 255) XOR CAPACITY_PATTERN_XOR`. The independent
decoder checks every tail byte, whole-stream CRC and all prior semantics.
The tail is not a tick, world, pool observation or timing sample. Real-world
capacity stays 2,000; none is manufactured to fill the allocation.

All three acquisition/readback CRC comparisons remain. Each tail write is
read back and compared byte-for-byte before transport freeze; the existing
whole-export CRC residue check remains. No allocation, reserve, workload,
100 Hz/21-stage order, resumed cohort or 20 Hz floor changes.

Space is funded by sharing the existing compact CRC implementation across
duplicate cold integrity paths. Private CRC parameters retain `volatile`:
one ordered byte read per iteration, with no qualifier cast-away or removed
comparison. Untimed tail validation uses its deterministic byte oracle,
avoiding another simultaneously live 32-bit CRC accumulator.

## Fit, contracts and platform impact

Qualified PRG:
`build/r0f/group1/capacity-summary/integrated-02/runtime-01/GROUP1.prg`.
SHA-256 `c068cc532dc820845d8c0649b1c2ea7dfc0bda394b32f7c186088a04d0dc048b`.
37,517 bytes; resident end exclusive **`$BFFD`**, **3 bytes free**.

Protected code/data grow by 245 bytes to `$2017-$31A5` inclusive (4,495
bytes), still below terminal staging `$4000`. Ordinary text falls by 211
bytes to 32,457. Constant data 518, initialized data 23, BSS 3,405, noinit 36
and compiler zero-page allocation 0 bytes remain unchanged. This is a narrow
fit, not useful expansion headroom; any further target edit requires a new
fit/host/timing gate.

Trace bindings are regenerated only in the isolated snapshot from its
version-7 authority. Public layouts and export allocation bindings remain
unchanged. Attic trace remains `$08030000-$0807FFFF`; no new physical or
CPU-visible allocation, MAP/base-page lifetime, DMA ownership or reserve use.
C clobbers remain compiler-managed. Measured IRQ/NMI paths are unchanged.

The summary is deliberately protected 45GS02 assembly: export staging
overwrites dead ordinary resident code, and terminal entry cannot return to C.
After admitted KERNAL entry and final close, it uses public CHROUT `$FFD2`
under the existing mapping macro. A bounded protected helper formats two hex
bytes; code and text stay below `$4000`. Terminal registers/flags/stack are
clobbered, not restored to the workload. Early denied entry does not call the
summary or unadmitted KERNAL. Static checks retain the no-return main and
explicitly allow only the protected helpers and declared ROM calls.

## Compact operator screen

The actual NTSC and PAL screenshots show:

```text
G1 EXPORT S:4 E:00 F:14
4=OK 5=FAIL / E,F HEX
REDUCE FOR TIMING
NOT ACCEPTANCE
RESET
```

`S:4` means complete terminal export; `E:00` is no export error; hexadecimal
`F:14` is twenty files. Green is export completion, not a timing PASS. The
card-return/independent reduction workflow remains necessary for physical
timing evidence.

A fresh NTSC fixture with the unchanged PRG and pre-existing `G1T00` rejects
the first SAVE: red border, `S:5 E:03 F:00`. Existing TOKEN/G1T00 bytes are
unchanged, no trace retry or replacement occurs, the actual returning SAVE
and original successor result validate, and disk structure/content pass.
That expected failure is not relabelled as a successful trace acquisition.

## Validation

Pinned LLVM-MOS builds pass map/symbol/disassembly, IRQ and strengthened
terminal checks. All seven compile checkpoints and their source hashes are
retained. The final identical-source rebuild reproduces the same PRG hash.

The full native suite passes ASan/UBSan owner/workload/scene/audio/display
checks, 65,536 generation comparisons, 248,832 observer-state comparisons,
3,200 independent scene comparisons, CRC vectors/u16 boundaries and 83
synthetic owner-codec rejections. Actual finalizer tests cover 0/1/5/6/100/2,000
real-event counts, full-allocation tail pattern, first/page/last corrupt
write/read and copy failures, prior region CRC failures, header/result/final
CRC write failures and repeated finalization. Zero-world cases are finalizer
boundaries only, not accepted acquisition evidence.

Independent host checks reject twelve repaired-outer-CRC capacity corruptions
and five terminal-static violations. The host version-7 codec fixture is
explicitly synthetic. Each actual positive export independently repeats all
102 existing/pool corruptions plus twelve capacity corruptions. Root Python
suite: **47 tests PASS**, including fail-closed capacity/carrier admission and
success/failure PETSCII summary checks. Whitespace checks pass.

| Focused fresh run | NTSC | PAL |
| --- | ---: | ---: |
| Real ticks / closed trace files | 3,200 / 20 | 3,200 / 20 |
| Export bytes | 327,680 | 327,680 |
| Real world events | 955 | 807 |
| Non-timing tail bytes | 17,100 | 19,468 |
| Minimum complete-cohort nominal cadence | 28.0971 Hz | 23.1109 Hz |
| Execution max / p95, CIA counts | 7,296 / 6,752 | 7,232 / 6,496 |
| Capture maximum, CIA counts | 1,153 | 1,153 |
| Hardware / software stack high-water | 62 / 124 bytes | 62 / 124 bytes |

Both have complete pre/post phase/order masks, zero nominal misses,
uncertain boundaries or below-floor cohorts. Actual SAVE, CRC, lineage,
registration, owner checkpoints and original payload preservation pass.
Fresh timing belongs to this PRG; predecessor timing is not reused.

The first sandboxed NTSC fixture failed at Xemu configuration-template
initialization with no memory/screen capture. It is retained as a host-launch
failure, not a target regression. A fresh exclusive fixture outside that
sandbox used identical qualified source/PRG. Two host-checker issues (missing
generic support import and ASCII encoding of the PETSCII clear prefix) are
retained; fixes affect tooling only. The completed collision fixture was
reduced read-only after the prefix correction, never relaunched or retested.

## Carrier and remaining boundary

Fresh canonical `build/r0f/group1/carriers/R0FG1P04/canonical/R0FG1P04.D81`:
819,200 bytes, read-only, SHA-256
`2519af02741197fb8851dccc26ab1379591d5340f1cae3b68cb243844c3730d4`.
Construction/extraction/structure gates and all four exact-name NTSC/PAL
copies pass. Every copy independently validates actual SAVE, twenty full
chunks, timing, all 114 trace corruptions and visible summary. No direct PRG
injection is used for carrier boots. The canonical image is never mounted
writable. State is **`XEMU_BOOT_VERIFIED` only**, not `TEST_ELIGIBLE`.
The gate pins 124 snapshot inputs plus ten retained root workflow inputs;
an additional admission record pins five capacity/summary controllers/tests.

Immutable evidence is at
`docs/evidence/r0f/group1/2026-10-01-capacity-summary/`. It includes all trial
sources/PRGs, actual exports/SAVEs, D81 copies, memory, screenshots and logs;
only disposable multi-gigabyte SD fixtures and bytecode caches are excluded.
All eleven prior freezes and their 5,726 entries, 93 root inputs, 95 P02 inputs,
133 P03 inputs and four original baseline PRGs are audited unchanged.

## Recorded commands and results

These commands produced retained exclusive outputs. They are not instructions
to overwrite or rerun any tested fixture/carrier.

```sh
python3 -B tools/diagnostics/r0f_group1_capacity_summary.py build --label runtime-01
python3 -B tools/diagnostics/r0f_group1_capacity_summary.py host
python3 -B tools/diagnostics/r0f_group1_capacity_summary.py qualify
python3 -B tools/diagnostics/r0f_group1_capacity_summary.py run --mode ntsc
python3 -B tools/diagnostics/r0f_group1_capacity_summary.py run --mode pal
python3 -B tools/diagnostics/r0f_group1_capacity_summary.py negative-export
python3 -B tools/diagnostics/r0f_group1_capacity_summary.py negative-check
python3 -B -m unittest discover -s tools/diagnostics -p 'test_r0f_group1_*.py' -v
python3 -B tools/diagnostics/r0f_group1_capacity_carrier.py build --name R0FG1P04.D81
python3 -B tools/diagnostics/r0f_group1_capacity_carrier.py boot --name R0FG1P04.D81 --mode 1 --number 1
python3 -B tools/diagnostics/r0f_group1_capacity_carrier.py boot --name R0FG1P04.D81 --mode 1 --number 2
python3 -B tools/diagnostics/r0f_group1_capacity_carrier.py boot --name R0FG1P04.D81 --mode 0 --number 1
python3 -B tools/diagnostics/r0f_group1_capacity_carrier.py boot --name R0FG1P04.D81 --mode 0 --number 2
python3 -B tools/diagnostics/r0f_group1_capacity_closeout.py closeout
git diff --check
```

Results: complete fit/host qualification PASS; focused NTSC/PAL PASS; collision
target execution completes with expected failure, while its first host reduction
hits the documented prefix bug; read-only `negative-check` PASS after correction;
47 root tests PASS; carrier build and four boots PASS; closeout and whitespace
PASS. Fresh Xemu calls use 120-second allowances and the pinned runtime outside
the sandbox; no 180/360-second run or physical device is used.

## Remaining boundary

This closes only the requested integrated capacity/summary slice. Physical SI
uncertainty, physical scanout/input/audio/NMI effects, universal worst-case
high-water, production renderer/model coverage, other unestablished matrix
rows and Groups 2/3 remain separate. No hardware-ready or full Group 1/R0-F
acceptance claim follows from these local results.

Recommended next action: review the bounded
physical-test proposal and remaining matrix boundaries with the owner.
SD delivery route and physical execution require separate explicit authority.
