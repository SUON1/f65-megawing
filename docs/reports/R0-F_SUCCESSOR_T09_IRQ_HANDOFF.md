# R0-F T09: post-storage IRQ handoff

## Subsequent physical result — failed, do not repeat delivery

The owner filled IRQ10 successfully (retained post-fill audit in
`build/d81-sd-transfer/R0FIRQ10.D81.slot-post.json`) and tested it. The new
photo reports `65/0A/0042/17/00`, reserve `3C7D60D8` unchanged, CRC
`E96A691D`, IRQ `0000 -> 0000`, IEC `00/00`, features `2B`.
Thus carrier entry passed but runtime did not; the IEC change did not fix
Fault 65. The feature byte does not support persistent IRQ deferral at the
sampled reclaim. Preserve IRQ10; the historical helper command below must
not be run again. Continue with the [T10 investigation](R0-F_SUCCESSOR_T10_RASTER_IRQ.md).

## Approved Build Intent and boundary

Owner request, 2026-09-26: "Please correct Fault 65, we need to finish R0F
phase." Continue the existing successor branch; preserve the tested CLK09
carrier and all prior evidence. Correct the narrow IRQ handoff, add regression
coverage and actionable diagnostics, and build the fresh exact-name
`R0FIRQ10.D81` for the owner's MEGA65-native blank. No commit, push, merge,
filesystem repair, public ABI change or R0-F acceptance is implied.

Inspected authority: Main Concept v1.6 and current specification precedence;
PF001 qualification and CF001 combined contracts; T02 successor admission
contract/ledger; T03 integration contract/ledger and handoff; T08 clock-order
report; C readability standard; D81 loadability gate and workflow.

## Physical observation and diagnosis

Owner's CLK09 photo reports `FAULT 65`, `STATE 0A`, `TICK 0042`, `MASK 17`,
`NMI 00`, equal reserve CRCs `3C7D60D8`, result CRC `42FBFDA2`. Hex `65` is
decimal 101, `FINAL_IRQ`. Display/audio/input/DMA activity passed their
individual final checks; IRQ advancement did not. The carrier loaded and
this run completed 66 ticks without the previous clock-read fault `03`.
This is a runtime failure, not a D81 chooser failure or full R0-F pass.

The retained official MEGA65 core at
`b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f` exposes an asymmetric register:

- `gs4510.vhdl`: reading `$D67D` bit 6 returns `iec_bus_active`; writing bit 6
  sets `irq_defer_request`. An asserted request continually reloads the
  deferral counter and suppresses IRQ/NMI service.
- `hyppo-dos.asm`, `trap_task_toggle_rom_writeprotect`: reads `$D67D`, XORs
  bit 2, and writes the whole byte back. Thus a busy IEC bus can accidentally
  request persistent interrupt deferral during an otherwise valid ROM toggle.
- `iomapper.vhdl`: CIA2 port-A bits 3/4/5 drive ATN/CLK/DATA; CIA1 serial
  output can drive SRQ. The R6 board derives bus-active from CLK/DATA/SRQ
  drive enables. `$D7F1` bit 0 exposes bus-active without entering HYPPO.
- The pinned Xemu `io_mapper.c` handles `$D67D` writes for enhanced-opcode
  and ROM-protection bits but does not model the IRQ-defer bit.

Primary pinned sources:
[CPU](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/vhdl/gs4510.vhdl),
[ROM toggle](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/hyppo/dos.asm),
[CIA wiring](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/vhdl/iomapper.vhdl),
[R6 bus-active wiring](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/vhdl/mega65r6.vhdl).

This is a source-supported cause consistent with the observed hardware-only
failure, **not yet a captured register-level proof on the installed core**.
The next physical run must test it. An emulator pass alone cannot do so.

## Implementation and hardware effects

The successor-only guard runs before initial ROM reclamation, before each
ROM restoration, and before post-storage reclamation. It clears only CIA2
port-A bits 3/4/5 while storage is idle and IRQs are stopped. It preserves the
VIC bank bits, all other port bits, all DDRs, and all CIA1 timer/serial state.
It refuses CIA1 serial-output ownership before calling the trap, with `69`
hex (105). It never resets the hardware IEC controller or writes `$D67D`
directly. If another hardware owner still suppresses interrupts, the existing
IRQ advancement criterion still locks out with `65`. The returned feature
byte is retained for physical diagnosis, not treated as portable status:
the pinned Xemu does not implement the hardware IEC/defer semantics.
The IEC outputs stay released;
reasserting them after the trap would recreate the hazard at the next toggle.

IRQ counts now use PF001's existing odd/even sequence byte, with 32 bounded
read attempts and fault `6A` hex (106) on exhaustion. The before snapshot is
after storage returns; only advancement during the resumed 33-tick interval
earns the IRQ service bit. Modular subtraction handles counter rollover.
Zero advancement still yields `65`; no acceptance predicate is weakened.

Registers/clobbers: ordinary LLVM-MOS C ABI; reads `$DC0E`, `$DD00`, IRQ
sequence/counter; writes only the stated `$DD00` bits. Existing ROM-trap and
IRQ wrappers retain their register contracts. No new assembly, MAP/base-page
change, physical allocation, DMA submission, reserve write, or NMI handling
change. Guards run outside timed workload phases; the 100 Hz release period,
21-stage order and tick-33 storage boundary remain unchanged. IRQ handler
and its preservation sequence are unchanged.

Private result bytes 97–99, generated from the integration contract, retain
post-storage IEC port-output bits before release, the commanded released
bits, and the returned reclaim-feature byte; `FF`
means that observation was not reached. Existing offsets and 512-byte result
size are unchanged. The final screen also displays coherent IRQ counts.

## Validation and delivery

Host tests exercise the actual guard with injected I/O, including
all port/DDR combinations, foreign serial ownership, a remaining hardware
owner, seqlock tearing and rollover. This hardware
model is not a substitute for physical observation. Full target, predecessor,
exact-name Xemu and D81 structure/content gates remain required before fill.
Raw SD allocation/hash checks and safe eject remain required before the
owner selects the new disk. Do not overwrite or retest CLK09.

Completed on 2026-09-26:

- `python3 -B tools/diagnostics/r0f_successor_integration.py build`: PASS;
  524,307 new ASan/UBSan IRQ-handoff checks, 1,527,538 integration checks,
  CF001 regression and 16,842,752 RH001 admission checks. Target compile/link,
  IRQ-preservation, canonical mapping, memory bounds and ordering checks PASS.
- Direct-PRG NTSC/PAL probe, output
  `build/r0f/successor-irq-handoff-probe-3`: PASS, `00/09/0042/1F/00`.
- `python3 -B tools/diagnostics/r0f_successor_irq_negative.py --good-run
  build/r0f/successor-irq-handoff-probe-3/ntsc --out
  build/r0f/successor-irq-negative-1`: PASS. A disposable PRG derivative
  changed only the IRQ restart's CLI to SEI. It completed 66 ticks with
  `65/0A/0042/17/00`, zero IRQ count advancement and a valid result CRC.
  Independent Python/Java reducers rejected a forged all-services-pass record
  with equal IRQ counts even after its CRC was recomputed. Rollover passed.
- `python3 -B tools/diagnostics/r0f_successor_physical_diagnostic.py all
  --name R0FIRQ10.D81`: PASS, independent structure/extraction/content checks
  and four fresh exact-name boots (two NTSC, two PAL), all
  `00/09/0042/1F/00`. Independent result/SAVE oracles PASS. The canonical
  image remained unchanged and was never mounted writable.
- `python3 -B tools/diagnostics/test_d81_delivery.py`: 18 tests PASS.
- Repository JSON/Python syntax, generated integration contract consistency,
  retained target input hashes, shell syntax and `git diff --check`: PASS.

Target PRG: 22,566 bytes, SHA-256
`517bda104fb0875f67940533a4ac06396c6486118738e06ec1f096a2f7f52a49`.
Resident usage 24,745 bytes; margin 16,214 bytes; high-water exclusive
`$80AA`; protected resident end `$2B07`. No new physical allocation or reserve
consumption. Generated header matches its JSON authority. This is an
uncommitted working-tree correction on base commit `9e2ffdb`; the retained
per-input hashes identify the tested source, not a new published source freeze.

Canonical candidate:
`build/r0f/d81-workflow/R0FIRQ10/canonical/R0FIRQ10.D81`, 819,200 bytes,
SHA-256 `ae0b45d8cfa3324ddb829fd9127d2a9cbfb887a4486c96490238158fdb080355`.
State: **XEMU_BOOT_VERIFIED only**. Full exact-name records are under
`docs/evidence/r0f/successor/2026-09-22-workflow/R0FIRQ10/`.

The owner's root-level native blank was independently parsed as valid and
empty, 819,200 bytes, label `R0FIRQ10`, SHA-256
`dd7fbc7f319c0faa8504d75c405ed2f4c3c438d8a7bdfedd334c552840d0feb1`.
No SD data write, raw one-extent verification, safe eject or physical IRQ10
test occurred during this build. The owner must run the privileged helper
below; it refuses a changed blank or failed raw allocation check before
writing, retains a backup, fills only this blank, checks unchanged allocation
and exact final hash, and safely ejects. No Finder replacement is needed.

```sh
cd /Users/slice/Developer/f65-megawing
sudo tools/diagnostics/d81_sd_fill_mega65_slot.sh \
  build/r0f/d81-workflow/R0FIRQ10/canonical/R0FIRQ10.D81 \
  /Volumes/MEGA65FDISK \
  ae0b45d8cfa3324ddb829fd9127d2a9cbfb887a4486c96490238158fdb080355 \
  dd7fbc7f319c0faa8504d75c405ed2f4c3c438d8a7bdfedd334c552840d0feb1
```

After `D81 MEGA65 SLOT FILL PASS` and `safe_eject=PASS`, select
`R0FIRQ10.D81`, run the normal `AUTOBOOT.C65` entry, and photograph the
whole stable screen including the new bottom row. Expected success values:
`FAULT 00`, `STATE 09`, `TICK 0042`, `MASK 1F`, `NMI 00`, equal reserve
CRCs, and advancing IRQ counts. CRC and counts vary per run. If any fault
appears, preserve that image and photograph rather than retesting it.
Physical resolution of fault `65` and full R0-F acceptance remain pending.

The first development-only Xemu probe retained a `69` lockout at tick zero:
`build/r0f/successor-irq-handoff-probe-1/ntsc/`. That draft polled `$D7F1`,
which the pinned emulator does not implement as IEC status (its read stayed
odd). A second draft checked returned feature bit 6 and also stopped at tick
zero: the emulator returns `6B`/`6F` despite normal IRQ operation, because
that bit is stored data rather than a hardware IEC status signal. Evidence
is retained under `successor-irq-handoff-probe-2/ntsc/`.

Neither draft produced a release carrier or SD write. The final correction
releases the CIA outputs and uses the actual coherent IRQ count as the
portable pass criterion. It does not alter Xemu, special-case its identity,
or waive the requirement for real IRQ service. Hardware feature-byte
interpretation remains a diagnostic distinction in the physical follow-up.
