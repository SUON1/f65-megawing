# R0-F platform qualification — decision PF-001

2026-09-17. Owner approved the proof-only platform development described in
`R0-F_COMBINED_PLATFORM_ADMISSION.md`, with Xemu before filling a native blank
SD slot. This additive decision does not approve candidate parents or R0 gates.

## Implementation sequence and boundary

Qualify canonical entry, asynchronous IRQ preservation, bounded DMA, actual PCM
progress/stop, and clock observations **before** integrating the full workload.
The qualification PRG is a development test, not the requested completed combined
carrier. Do not package/deliver it as that carrier. No production core, earlier
proof, preserved spec, physical ownership or reserve changes are authorized.
The R0-C reversible ROM-reclaim contract remains deferred: this qualification
neither overwrites `$020000–$03FFFF` nor calls a hypervisor trap. A full renderer
still needs its documented handoff/recovery contract.

## Inspected inputs and validation

Official record; root AGENTS and D81 gate; frozen Architecture 1.4.1 (complete,
including §§2–3); Read-First, AD-001 and approval record; current `memory/` and
`interfaces/` contracts; B-register integration decision; candidate Architecture
1.5.1 memory/timing/snapshot requirements and Engine 0.2 §§2.5, 3–5, 8, 11–12,
14–17 and 19; R0-F timing/capture/admission/ownership/full-closure records;
existing R0-A/R0-B/R0-C platform wrappers, F5 clock and build tooling.

Pinned official core source: `b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f`:
`iomap.txt`, `src/vhdl/{gs4510,cia6526,clocking,mega65r6,pixel_driver,frame_generator}.vhdl`
and `src/hyppo/mem.asm`. URLs are relative to
<https://github.com/MEGA65/mega65-core/tree/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f>.
Retained downloads and hashes belong in `build/r0f/combined/references/`.
Source attribution is not installed-bitstream verification.

Commands: `python3 tools/diagnostics/r0f_platform_build.py build` (native
ASan/UBSan validation, LLVM-MOS compile/link, map/symbol/disassembly and static
checks); `python3 tools/diagnostics/r0f_platform_build.py xemu` (two disposable
SD-image PRG boots and independently checked result bytes); `git diff --check`.
Physical tier is unavailable until an exact combined D81 passes its gates.

## R0F-PLAT-PF001 private ABI

All C uses pinned LLVM-MOS, `-mlto-zp=0`, B=`$02`, compiler logical rc0–31 at
`$02–$21`. C clobbers follow that compiler ABI (A/X/Y/Z/P and compiler scratch).
Zero-argument assembly helpers use an absolute mailbox, never guessed C argument
registers. Pointer-copy helper preserves X/Y/Z/B/P/SP, returns in A, so it **does
not claim Q preservation independently of A** (Q comprises A/X/Y/Z).
Scratch `$0222–$0229` is exclusive to the non-reentrant flat-copy helper; IRQ
does not touch it or compiler temporaries. Helper count is 1–255 only.

Canonical entry executes under SEI: MEGA65 I/O key `$47,$53`; D030 ROM overlay
bits and CRAM2K cleared; temporarily B=0 for real CPU port `$01=$35`; zero MAP offsets and
megabyte selectors followed by EOM; B=`$02`; local IRQ/NMI vectors at FFFA/B
and FFFE/F. No MAP windows, no ROM calls, no public restoration to BASIC.
No cartridge override is invented: supported proof configuration has no active
cartridge mapping. CPU stack remains the inherited page-1 stack; entry checks
its high byte. IRQ uses fixed resident code below `$8000`, eight stack bytes
including hardware PC/P and saved A/X/Y/Z/B. IRQ does not call C or change MAP.
RTI restores flags and PC; matched pushes/pops preserve SP and A/X/Y/Z/Q/B.
Non-nesting raster IRQ at line 0 is acknowledged with D019 bit 0; CIA IRQ masks
are disabled, including CIA2 NMI sources, and pending ICRs read. Audio IRQs are
disabled. NMI sets a sticky interference flag; any observed NMI invalidates
the test. RESTORE/hypervisor intervention remains forbidden during acquisition.

The LLVM-MOS linker can relax even `mos16($0001)` to a direct-page operand;
therefore B=0 is explicit during the port access and B=2 is re-established
before returning to C. The first PRG experiment exposed this in Xemu before
any carrier was packaged. CPU-port observations come from that assembly access,
not a C constant-address read which can have the same relaxation.

Entry clobbers A/X/Y/Z/P while establishing B; IRQ start/stop clobber A/P
and intentionally change I. The register-probe helper saves/restores A/X/Y/Z/P;
B is unchanged. Flat-copy return loads its A status **before** PLP so that the
documented P preservation includes N/Z. NMI saves A and uses four stack bytes
including hardware PC/P; its flag cannot wrap back to zero.

IRQ mailbox increments use a seqlock for C-side atomic reads; bounded 32 retry
limit. Before IRQ enable, hardware-stack scratch is not filled or overwritten.
No stack-high-water or bounded IRQ-latency acceptance is claimed by event counts.

## Memory and DMA

CPU/physical low-memory screen `$0800–$0FCF`, result `$1900–$19FF`, code/data
linked `$2001–$7FFF` only; software stack top `$D000`, with linked storage below
`$8000` and stack headroom reported, not a measured high-water pass. Resident
vectors FFFA/B and FFFE/F; base page/stack as above. These are standalone proof
allocations, not co-resident production allocations.

Core-owned proof DMAService alone submits one synchronous Enhanced F018A copy
at a time. Input length 1–255; normalized source/destination must be wholly in
resource staging `$050000–$052FFF` and non-overlapping. No chained jobs, IO,
hypervisor, Attic or zero-length (=64K hardware) requests. List is encoded into
`$056000–$056010`, immutable until the trigger store completes and CPU execution
resumes. Options explicitly select F018A, source/destination MB zero, then end;
command COPY, count, source and destination, zero modulo. CPU is blocked by
hardware until completion; software cannot enforce a timeout while halted.
Caller must measure the blocking interval and verify copied bytes. A hung job
requires physical reset. No latency bound is presumed. Interrupts remain enabled
outside initialization; IRQ has no DMA or list access.

Flat-copy helper may move bytes between its linked bank-0 buffer and only
`$050000–$0501FF`, `$053000–$0530FF`, or `$056000–$056010`. Destination allowlist
is checked by C before helper calls. No writes to `$057000–$05FFFF`, ROM stores,
other modules' allocations, SD or filesystem. Physical reserve verification is
not inferred merely from these whitelists.

## PCM, SID, input and clock qualification

PCM channel 0 only; unsigned 8-bit synthetic sample pre-staged at `$053000`.
Disable channels first. D711=`$80` enables normal mixer path (not bypass);
channel base/current `$053000`, top low16 `$30FF`, volume low, explicit
24-bit phase increment; looping enabled with E2, stop with 00. Poll current
address for actual progress and stop stability, with bounded clock/iteration
guards. Readback alone is not audible-output or start/stop latency evidence.
No production format/rate/cache split selected. SID voice 1 can be exercised
separately at low master volume, then gate/master volume cleared. No audible
PASS without owner evidence. Input D610 event read/ack is not physical edge
latency; raw keyboard press/release integration remains a full-workload obligation.

CIA1 A/B run the existing free-running cascade, with added near-A-reload
rejection to avoid accepting delayed B underflow. Reads have bounded retries;
all timestamps are raw CIA counts. Record read overhead and per-frame samples
before/after workload; reject non-monotonic/stopped/interfered observations.
Clocking.vhdl supplies nominal R6 CPU 40.5MHz/pixel 81MHz from a nominal 100MHz
input, but oscillator tolerance and installed provenance remain unverified.
No exact 1MHz assumption, SI conversion, calibrated 100Hz claim, or protected
530000-cycle claim. Actual combined timing is not qualified by this PRG.

## Failure and release

Every stage records observed values and a nonzero fault code on failure. Stop
DMA/audio submissions and disable IRQ/timers on exit; retain readable results
and require reset. No path returns to ROM. Missing emulator functionality is
NOT VERIFIED and blocks promotion; never treat a readback-only test as progress.
Only the full combined carrier may proceed to the requested hardware delivery.
Proposed matching filename `F65BLK02.D81` is unassigned until packaging; BLK01
was observed at 688128 bytes and is not eligible. No slot is renamed.
