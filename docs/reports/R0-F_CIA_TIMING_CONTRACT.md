# R0-F CIA timing diagnostic — implementation contract

2026-09-17. Bounded AD-001 diagnostic development, not production admission,
hardware qualification, or R0-F acceptance. The existing R0-E workload remains
a functional proxy. Timing it does not turn it into production input/audio work.

## Inspected inputs and decision

Official record; both architecture sources including MemoryAccessABI; approved
Read-First, AD-001 and approval record; memory ledgers and interface registries;
R0-D/E handoffs and contracts; R0-F admission, ownership, stage control, source,
startup-fix evidence; B-register decision; root D81 gate. No prior calibrated
timebase contract exists. This is a new private, reset-only diagnostic contract,
not a replacement for the public platform ABI.

Primary implementation references, pinned for this diagnostic:

- [MEGA65 CIA implementation](https://github.com/MEGA65/mega65-core/blob/e9677ac1c6e3b9a41669555b8947163cc9833056/src/vhdl/cia6526.vhdl):
  timer registers, load strobes, Timer B counting Timer A underflows. Extended
  latch/mask readback is hypervisor-only, so exact ROM-state restoration is not
  promised.
- [MEGA65 register map](https://github.com/MEGA65/mega65-core/blob/e9677ac1c6e3b9a41669555b8947163cc9833056/iomap.txt):
  CIA1 $DC04–07/$DC0E–0F; elapsed-frame counter $D7FA.
- [Pinned Xemu CIA model](https://github.com/lgblgblgb/xemu/blob/40dfef0d1d5f56be2469492715c12bdb32c75b67/xemu/cia6526.c):
  cascade is modeled, but underflow reload differs by one count from the
  hardware convention. Its MEGA65 main loop advances CIAs in fixed 32-count
  scanline steps and explicitly leaves clock accuracy unresolved. Xemu can
  validate execution/encoding, not the physical clock frequency.

## Ownership, state and failure contract

Exclusive CIA1 Timer A/B ownership lasts only for this standalone run. With
IRQs already masked by the inspected SDK startup, stop both timers, set both
latches to $FFFF, start B on A underflows ($51), then A on PHI ($11), preserving
CRA bit 7 and CRB bit 7. No CIA ports, ICR, CIA2, vectors, MAP, or DMA access.
The timer wrapper verifies $D030 bit 0 is clear (CIA visible) and CRA bit 6 is
clear (serial-output mode inactive); otherwise it fails without a timer write.
It never enables interrupts. NMI is not masked: do not
use RESTORE/Freezer during measurement; such intervention invalidates the run.

There is deliberately no public return to BASIC. Stop both timers after capture
or failure, retaining the preserved control bits; display results and spin.
Reset/reboot is required. No claim of restoring old latches, pending interrupts,
or production canonical MAP/$01 state. B remains $02. C ABI clobbers A/X/Y/Z/P
and compiler pseudo-registers; no preserve-all/Q wrapper or new assembly.

Coherent reads use high/low/high for each 16-bit timer and B/A/B retry for the
cascade, at most 32 attempts. The returned timestamp is the complement of the
32-bit down-counter. Unsigned subtraction handles a 32-bit wrap. All waits have
iteration bounds and reject backwards/implausibly large clock steps. A stopped
timer, frame timeout, unstable read, overflowing observation or incomplete sweep
sets a fault; completion is never inferred from zero-filled storage.

## Measurement protocol

Units are **raw CIA counts**, not CPU cycles or calibrated microseconds.
Measure counts across 16 observed frame-counter transitions before and after
the sweep; retain both totals. This is an internal cross-check, not calibration
against an external standard. Record $D06F and $D054 observations without writes.
Core/ROM/video/clock identity and an external frequency reference remain needed
before assigning SI units or claiming real 100 Hz.

Five inherited cases, in explicit order; 16 initial phase offsets distributed
across the measured mean frame period. Each offset starts a 33-tick cohort.
Release times advance by 10,000 CIA counts independently of display frames;
there is no assumed PAL/NTSC superperiod. This is a nominal-period diagnostic,
not an approved simulation scheduler. Capture every tick's instrumented work
duration and completion lateness against its next release. No tick is skipped
or merged. Work includes the inherited synchronous snapshot operation. Report
miss counts, nearest-rank p50/p95/max durations, max lateness, and max elapsed
33-tick cohort. Cohorts are not exhaustive sliding-window or full legal-phase
coverage. Instrumentation overhead is included; no subtraction is invented.

Raw samples: five x 528 records, each little-endian u16 duration/u16 lateness;
then five x 16 little-endian u32 cohort spans. A linked exported symbol owns the
10,880-byte capture; its address/length is encoded in the result and map. Sorting
uses a separate 1,056-byte scratch array; original phase/time order is retained.
Any u16 overflow fails acquisition instead of saturating or wrapping silently.

Private result revision 2 at $1900–$19FF: functional bytes 0–143 retain REV1
meaning except revision byte 4=2. Bytes 144–150: CT,1,16,33,5,16; 151=127 only
for complete acquisition. 152–155=pre-calibration counts; 156–157=16 frames;
158=$D06F; 159=$D054. Five 16-byte rows at 160: p50,p95,max,max lateness,
misses,phase mask (six u16), max cohort span u32. 240–243=post calibration;
244–247=10000; 248–249=raw pointer; 250–251=10880; 252=fault;
253=observed ready-snapshot high-water; 254=0; 255=byte-sum checksum.

Memory: standalone result/screen/base page/hardware and software stacks retain
their existing ownership; new linked BSS is within $2001–$CFFF and charged by
the map, never $050000–$05FFFF. Current linked BSS is 12,152 bytes (capture,
sorting, snapshots and all clock/fixture state); compiler static stack is 158
bytes, independently reconciled by the audit. No physical mapping change. Dynamic stack high
water, IRQ latency, DMA, real input/audio latency and full reserve proof remain
unmeasured. No shipping budget or pass threshold is selected. A successful
acquisition may contain deadline misses and must display them as observations.

Validation: `F65_R0F_VARIANT=cia-timing sh tools/build/r0f.sh host-test`, `build`,
`audit`, `package`, `xemu`; pinned Java validator recomputes raw-sample summaries;
native ASan/UBSan tests include timer/frame faults and wrap. Package uses fresh
F65R0F4.D81, never F2 or a blank as a template. The earlier host-only F3 candidate
is withheld, unchanged: review added the serial-mode precondition before release;
its carrier was never Xemu-tested or sent to SD. Its direct PRG tests are only
preliminary evidence. Physical transfer of F4 requires its
own matching fresh slot and all D81 gates. Finder crashed during the owner's
F2 eject attempt; safe eject remains **NOT VERIFIED**, not PASS. No SD operation
is authorized by a host build alone.
