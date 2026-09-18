# R0-F combined experiment CF-001

2026-09-17, updated 2026-09-18. Owner-authorized proof development, **not gate acceptance**.
Implements the owner's ROM handoff, calibration, workload integration and Xemu
request. F65BLK02 is the intended native destination only after exact-image
gates; neither PF-001 nor an incomplete CF-001 may be delivered instead.

## Authority, inspected contracts and scope

Read before editing: F65_OFFICIAL_RECORD.md; AGENTS.md; 00_D81_LOADABILITY_GATE.md;
complete frozen Architecture 1.4.1, including memory/MemoryAccessABI; approved
Read-First 1.0, AD-001 and approval record; all current memory and interface
registries; Architecture candidate 1.5.1 memory, execution and timing sections;
Engine candidate 0.2 platform, memory, scheduler, renderer, input, audio, storage,
tooling/admission and R0 acceptance sections; R0-F admission, ownership, execution,
full-closure, timing/capture and PF-001 records and implementation. Requirements:
MEM-001/002/004/005, ENGINE-001/002/004/006, PERF-001/002/003, RENDER-001/002,
INPUT-002, AUDIO-001/002/003, TOOL-003/004 and TEST-001/003/005.

No production CoreRuntime, public ABI, preserved specification, capacity or
reserve is changed. All new services are private R0-F stand-alone candidates.
No gameplay/flight/weapon/AI behavior or production coefficients are selected.
Campaign and shipping-content fields: NOT_APPLICABLE_UNTIL_GATE Phase 4/5.
The historical R0-C ROM wrapper remains deferred; this is an independently
versioned recovery experiment, not retroactive qualification of that wrapper.

## ROM/display handoff and recovery lockout

Pinned core: b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f. Sources:
[HYPPO memory](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/hyppo/mem.asm),
[DOS trap](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/hyppo/dos.asm),
[return](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/hyppo/main.asm).
A=$70 / STA $D640 / NOP toggles feature bit 2 and returns the feature byte in A;
success is carry SET (the source's contrary comment is not its implementation).
The operation changes protection, **not ROM contents or a storage context**.

Supported entry is ROM protected. Before toggling, copy all 128 KiB at
$020000-$03FFFF to immutable Attic resource $08000000-$0801FFFF in bounded
255-byte CPU transfers; independently compare every byte before permitting
any ROM-store write. The first toggle must report protection cleared and
success. Unexpected state is toggled back immediately, with no display writes.
No ROM/KERNAL/hypervisor/storage calls are permitted during ownership of the
display stores, except this same protection control at recovery. The binary
has no filesystem implementation. A storage-admission request during the
reclaimed state is rejected without I/O; a counter records rejection.

Recovery: stop submissions and PCM/IRQ, disable display fetch, copy the immutable
backup back to both ROM banks and compare every byte, then toggle protection
back and verify the complete feature byte. Verify the backup hash did not
change. On any failed restore, remain reset-only and never issue storage/ROM
calls. Normal completion is also reset-only: this experiment restores ROM
contents/protection, **not the pre-launch BASIC stack or filesystem state**.
The missing production transition to a usable ROM-hosted storage environment
is not declared solved by this reset-only experiment.

The trap wrapper saves P/X/Y/Z/B; A is the returned feature byte (therefore Q
is not preserve-all). It masks IRQ around the trap, records carry and observed
B, restores saved B/P, and never exposes a mapped window. Hypervisor hang is
not software-timeout recoverable. RESTORE/NMI invalidates acquisition.

## Time reference and uncertainty

CIA1 A/B free-running cascade is the timestamp. Stable high/low/high reads
reject the first 16 A counts after reload to avoid delayed B underflow. Read
overhead and before/after frame samples are retained. No exact 1 MHz assumption.

On hardware, VFAST and the source-attributed R6 video configuration are checked;
$D7F2-$D7F5 at full speed count CPU clock cycles per frame (gs4510.vhdl, not the
misleading PHI register name alone). Read only across a stable $D7FA frame.
Measure CIA counts per frame and derive a rational CIA/CPU-clock conversion.
40.5 MHz is the **nominal source clock**, not traceable SI calibration; oscillator
tolerance and installed binary provenance remain external evidence obligations.
Clock/profile changes invalidate the run. PAL/NTSC are separate executions;
no exact frame/tick superperiod is assumed.

Pinned Xemu 40dfef0d1d5f56be2469492715c12bdb32c75b67 does not implement D7F2-5.
D60F bit 5 distinguishes its declared emulator profile. Xemu runs explicitly
at fastclock=40.5. `vic4.h` defines 31468.5/31250 line Hz and 526/624 physical
rasters; integer CPU clocks per line are 1287/1296, giving 676962/808704 per
frame. `mega65.c` advances CIA by a fixed 32 per line (16832/19968 per frame).
Its known scanline CPU/CIA model is an **emulator reference**,
never hardware-counter evidence. Target profile and reference class are encoded
in results. Host validation refuses to promote emulator results to physical
clock calibration. Source-model conversion and observed timestamp intervals
retain rounding, instrument overhead and spread rather than fake exact cycles.

The synthetic protected kernel uses finite SoA loads/stores, table/arithmetic,
branches and event fan-out, with all requested pool members executed. Work is
calibrated by measured batches and a recorded iteration count, not relabelled
loop counts. 530000 clocks is the historical comparison fixture over a nominal
two-NTSC-frame interval, not an approved shipping budget or exact CPU guarantee.
Calibration error and each observed execution are reported. Scheduler ticks
remain independently deadline-driven; presentation/extra comparison work is
yieldable. No skipped or merged tick is permitted.

## Workload and ownership

Generated private CF-001 schema fixes the experiment, not production limits.
Core fixture executes the 21 architectural stage positions; stage-16 directives
apply on the following tick. Synthetic slots cover 9 aircraft, 16 missiles,
24 gun groups, 48 decoys, 8 mission objects, 8 objectives, 64 effects and 10
tracks. These are exercised arrays, not just labels. Three immutable extracted
snapshots have FREE/PUBLISHING/READY/READING transitions; lag holds READING,
exhaustion skips publication but not ticks; presentation discards obsolete READY.
All cases must produce identical authoritative hashes for identical tick inputs.

Display candidate is bounded FCM indexed-color, double complete buffers in the
canonical display stores. Resumable synthetic geometry is rendered with bounded
projection, viewport rejection, depth-sorted painter order and eight generated
spans per 8x8 triangle card. Filled, reduced-filled, wireframe and 4x4 impostor
patterns are distinct. This is a small synthetic stress scene, **not** the full
terrain/mesh/backface/near-plane pipeline or production scene-limit proof.
Tier selection changes only presentation. Input samples the real keyboard matrix
once per display frame, OR-latches press/release bits and consumes them once per
tick. Scripted edge
injection is separately identified and cannot be passed off as human latency.
SID/PCM use synthetic data, protected services, priority preemption and text
fallback. Software service latency is not external key-to-photon/acoustic latency.
Core DMAService owns immutable, range-validated, unchained copy jobs. Interrupt
handlers remain resident leaf routines and never access C compiler temporaries,
mutable DMA lists or mapped memory.

The native edge test runs 10000 short/held/repeated press-release pairs and a
simultaneous-bit test through the same latch; it does not claim the complete
semantic-command/context/approved-joystick corpus. During the pressure case the
target measures 32 script transitions and 32 consumptions using that latch,
not literal pass counters. Real keyboard transitions/consumptions are separate.
PCM service runs each display frame plus immediate warning state changes.
Phase swap counts are retained (80 bytes) and reduced to per-case nominal
cadence by the independent checker. Lag intentionally suppresses rendering.
An acquisition pass is not a 20Hz-floor or measured-limits acceptance.

## Memory, clobbers and validation

CF-001 is not co-resident with PF-001/F5. CPU B=$02, $01=$35, MAP offsets and
megabyte selectors zero/EOM, resident IRQ/NMI vectors. Compiler rc0..31 use
$0202-$0221; flat wrapper scratch $0222-$0229. Page-1 hardware stack and linker
software stack (top $D000) have separately measured canary bounds. C follows
pinned LLVM-MOS A/X/Y/Z/P/scratch clobbers. PF-001 IRQ preserves A/X/Y/Z/B/P/SP
and thus Q; no C calls. NMI sticky flag causes failure. Timers/IRQ are stopped
at completion, no normal return to BASIC. Assembly is platform-boundary code
only; workload, rendering and scheduler are C.

Transient raw capture uses canonical hot-state RAM $0300-$179F (5280 bytes).
The startup screen $0800-$0FCF aliases it only before acquisition. Final text
uses the already-owned cockpit/HUD slice $040000-$0407CF, through the physical
copy wrapper and display pointer, preserving all samples. No MAP window or
reserve is borrowed. Color attributes use physical $FF80000-$FF807CF, not the
CPU CIA aliases. CF001 uses -Oz -fno-inline-functions; initial -Os inlining
failed the resident-size check and was never run or packaged.
Low-memory result $1900-$1FFF; linked code/data must fit
$2001-$7FFF, with maps/symbols/disassembly and every C/runtime/static-stack byte
charged. The 977-byte synthetic model is linked C BSS, not a serialization or
full production pool-layout proof. Three snapshot records and work/matrix scratch
use $17A0-$18FA (347 bytes, NOLOAD, explicitly initialized); only the 192-byte
snapshot mirror uses active-simulation $017000-$0170BF. No unused $010000 state
allocation is claimed or whitelisted. Display metadata $01C000-$01CF9F;
A/B display $020000/$030000; staging $050000-$051FFF;
audio $053000-$055FFF; DMA lists $056000-$056FFF. Exact slices are generated in
the machine-readable contract. All other owner/reserve areas are write-forbidden.
Reserve evidence is read-before/read-after comparison, never destructive fill.
Attic backup is immutable cold recovery data, not authoritative runtime state.

Tests: native ASan/UBSan boundary, wrap, snapshots, edge/fault and checksum tests;
independent Java deterministic model/result reduction and corruption rejection;
pinned LLVM-MOS compile/link/static ownership checks; Xemu PAL/NTSC development
regressions, then two clean boots of the exact freshly constructed F65BLK02.D81.
Generated output and references are hashed. Hardware obligations: same D81,
verified native-slot delivery, chooser/run/summary capture, actual input and
audible-output observations, source/core attribution and physical clock data.
Unmet requirements remain explicit; partial results are never full R0-F PASS.

## Raw transport and measurement interpretation

After acquisition, `N`/space and `P` select 14 pages; `S` returns to summary.
Virtual stream is 1792 result bytes then 5280 duration bytes. Each page shows
512 bytes; last page contains 416 valid bytes, followed by zero display padding.
Header fields are page, byte offset, valid length, result CRC32 and duration
CRC32; all hex. The Java checker refuses incomplete/corrupt streams. Xemu pager
tests operate the virtual keyboard only after acquisition and compare every
screen-transport byte against independently read result/capture RAM.

Comparison calibration measures the model's 33-tick average scaled by 10/3,
then adds measured C filler only for the remaining part of 530000 nominal
clocks. Input/audio/HUD/snapshot overhead is measured in actual tick durations
but is **additional** to that comparison calibration. Quantization, read cost,
before/after frame spread and residual are retained; no exact all-protected-work
530000-clock or 100Hz physical accuracy claim follows. No oscillator tolerance
or new acceptance threshold is invented. CPU periods are independent of raster.

Pinned compiler initially exhausted registers in a combined byte-latch update;
separating volatile byte accesses in C fixed it, with the same native vectors.
No handwritten workload assembly or additional base-page allocation was added.
