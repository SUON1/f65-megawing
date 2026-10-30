# M2 unbanked exact renderer

Identity: `65AERO-M2-UNBANKED-1`. Founder Build Intent: attached
“M2 Renderer Architecture and Emulator Execution”, 30 October 2026.
Base: freshly fetched and remote-verified `9570f0ab427121a4e8f042041a14c89aaaeff9e2`.
PR #30 remains a separate failed experiment, unchanged and not for merge.

## Engineering selection

Use one shared exact byte-limb arithmetic kernel, resumable transform/clip/project
control, cached projected segments, and exact scanline horizon boundaries.
Keep public Q12/Q24/Q46/Q16 and every generated public record unchanged.
No reduced-precision authority, bank, memory exception, DMA or reserve use.

Exact baseline: 32,839 / 24,575 resident bytes, deficit 8,264, scratch 190.
Source-pinned PRG SHA-256:
`1873c76d7b13f438244d5c3f99d8c80bc951af47cda9fc5ba9a6fadbeb4eda51`.
Linked cost ranking from its symbols: wide geometry 8,467; Graphics composition/
validation 4,193; CF safety seams 3,141; compiler arithmetic 2,301; M2 Platform
2,118; Core/snapshot/input 1,785; font/text 1,743; camera controls 1,730; raster
1,205; fixture 838; M1 adapter 670; root 601; guard 204; other/padding 715.
Text total 29,711. Other allocation: rodata 1,439, BSS 1,475, scratch 190,
prefix 22 and alignment 2.

The integrated replacement envelope is 6,376 bytes: the 14,640-byte math,
exclusive64-helper, camera/registration/coherence, raster and text closure leaves
18,199 bytes of the baseline resident allocation. Additional continuation/cache,
constants, scratch and alignment must also fit that envelope. This is a
selection rationale, not measured savings. Geometry alone leaves only 1,354
replacement bytes and is rejected. Horizon-only/formatter-only work cannot
close the deficit; reduced public precision and rejected banking are excluded.

## Numeric and owner contracts

Let S=2^46 and T=2^24. Coefficient magnitude <=S+8. For all valid public points
and cameras, each transformed Q24 component <=217608*T+3=3650856419331 (<2^42).
Rounded convex clipping preserves endpoint extrema. Vertical distances <=7P
(<2^45); crossing denominators <=14P (<2^46); interpolation products <2^88;
Q46 products <2^94. Full96 products retain every intermediate bit. Projection
numerators remain below signed64 (including the rounding bias). Horizon
magnitude <=766*(S+8) <2^56: its accumulator and steps retain64 bits.
Rounding remains nearest/ties away, with checked narrowing and overflow failure.

Graphics owns private arithmetic/cached geometry, horizon and registration.
Environment retains canonical17 segments; selection remains nine. Core/Input/
Presentation preserve100Hz,21stages and immutable snapshot ownership.
Physical stores and all protected Platform/ROM/clock/copy/fault seams remain.
Registers/clobbers, MAP/B, CPU-port, DMA, IRQ/NMI and physical allocations are
unchanged by the pure Graphics replacement. Software/hardware stack and service
cost require exact linked admission; no launch or positive target grants yet.

The horizon transition is monotone in x. For legal pitch/roll, m[8]>0, so its
boundary moves monotonically between scanlines. Cache128 exact integer edges;
tile painting performs narrow comparisons. D=0 remains sky. No repeated
projection per tile and no screen-fixed runway.

## Future engine capacity

M2 success would establish this development executable only. M3 host datasets/
references do not prove target code space. Active simulation state has its own
physical010000–017FFF owner; Graphics workspace048000–04FFFF is separate.
M4 Flight/Systems and M5 Contact need actual code/state/service budgets in their
21stage owners. No remaining M2 margin is promised to future physics. If those
cannot fit existing ownership, a separate architecture decision is required;
Attic resources and protected reserve are not mutable simulation donors.

## Evidence and admission

**READY FOR REVIEW — FAILED FIT, NOT FOR MERGE.** One complete candidate link
was performed. Stop at this first unresolved mandatory gate; no second link,
further optimization, target execution or media/hardware activity.

Implementation adds `m2_limb`, `m2_compact` and public batch compatibility
adapters. The active renderer uses only resumable services. The original
`m2_geometry.c` is unchanged and is compiled separately as the native reference.
Camera edge handling uses paired semantic bits with unchanged clamps/reset/
revision behavior. Text uses private offset descriptors; altitude remains left,
airspeed right, both NOT IMPLEMENTED, with NON-FLIGHT DIAGNOSTIC prominent.
Graphics comparisons use scalar arrays, avoiding public-structure padding.
Public contracts, generated files, Platform/startup, input, Core and immutable
snapshot implementation remain unchanged.

Exact measured allocation:

| Allocation | Main baseline | Candidate | Delta |
| --- | ---: | ---: | ---: |
| Text | 29,711 | 24,363 | -5,348 |
| Constants | 1,439 | 1,643 | +204 |
| BSS | 1,475 | 1,962 | +487 |
| Compiler scratch | 190 | 53 | -137 |
| Prefix | 22 | 22 | 0 |
| Alignment | 2 | 6 | +4 |
| **Resident** | **32,839** | **28,049** | **-4,790** |
| Ceiling | 24,575 | 24,575 | 0 |
| **Deficit** | **8,264** | **3,474** | **-4,790** |

Resident interval is `$2001–$8D91` inclusive, end-exclusive `$8D92`.
The entire allocation exceeds its permitted owner range; no fit or execution
admission follows from the absence of a software-stack collision.
Compiler scratch is `$8D5D–$8D91`. Renderer object is 1,163 target bytes
(676 baseline): geometry continuation 200, horizon/cache 285, two flags.
Host renderer size is 1,200, not a target ABI/stack measurement.
Hardware/software stack envelopes remain 256 / 4,096 bytes; actual whole-program
maximum use is UNPROVEN. No reserve consumption or other-owner allocation.

Measured text changes by subsystem:

| Subsystem | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Geometry/arithmetic, including prepare adapter | 8,470 | 5,730 | -2,740 |
| Compiler/library helpers | 2,301 | 1,239 | -1,062 |
| Telemetry/font | 1,743 | 946 | -797 |
| Graphics composition/validation | 4,193 | 3,764 | -429 |
| Diagnostic camera | 1,730 | 1,393 | -337 |
| Raster | 1,205 | 1,222 | +17 |

Protected CF 3,141, M2 Platform 2,118, M1 adapter 670, Core/Input/Presentation
1,785, fixture 838 and root/guard 834 text bytes remain unchanged.
The actual limb kernel is 1,694 bytes, continuation/control 4,036: projection
1,913, horizon 739, transform service 586, plane distance 457, sine 190 and
begin adapters 151. This control cost defeats the selection estimate. No native
64-bit multiply/divide helpers or monolithic geometry/batch adapters remain
in the target; required resumable behavior is reachable from main.

PRG: 26,036 bytes; SHA-256
`5cbe53fce1440ea429c5bd4e1308e1460f6bb344fe459a403b975a50ca448758`.
Exact target packet:
[`target-1793345752710330000`](../evidence/flight-demo/2026-10-30-m2-unbanked-renderer/target-1793345752710330000/result.json).
Its seal SHA-256 is
`a77aab97c28e189f2027d6ff7fe648cf5343a81844d5966f1440d776d2a28ae4`.
Compiler and objdump match the pinned LLVM-MOS lock; flags unchanged. Full SDK
identity is unchanged before/after: 1,139 entries, digest
`4166ea6e185bc8471593336e0ac691b784fb5c0a51f861a1c26463c1609bbfd4`.
The shared builder's `base=b044440` is its historical ancestry check, not this
implementation's start. `head=9570f0a` plus exact source hashes identify the
tested uncommitted tree, subsequently preserved in Git and the source archive.

## Gate disposition and exact operation scope

| Gate | Result |
| --- | --- |
| Public/generated contracts and precision | PASS for host/static scope |
| Immutable capture, cancellation, complete-pair and fault behavior | PASS host |
| Actual complete resident fit | **FAIL by 3,474** |
| Startup | **UNPROVEN overall**; linked prefix/raw closed sink PASS only |
| Whole-program hardware/software stack | **UNPROVEN** |
| Renderer service and sustained 20Hz world capacity | **UNPROVEN** |
| Fixed physical owners/reserve | Unchanged/zero; resident boundary fails |
| Xemu PAL/NTSC | **NOT RUN** |
| Emulator visual behavior/cadence/latency | **NOT OBSERVED** |

Launch, eight service grants and guard grant stay zero. The existing stack
probe reports software-SP writes needing fresh accounting; it is not a
whole-program admission tool. Startup's static scope excludes inherited-entry,
asynchronous NMI and ROM-trap execution proof. Platform comments about masked
IRQ do not establish that state: clock initialization enables raster IRQ;
any future bound must include IRQ and NMI-over-IRQ paths.

The sealed target result inherits the common builder's old
`service.quantum_cardinality` strings. **Those strings are stale metadata, not
descriptions of this implementation or timing evidence.** They are superseded
here without modifying the sealed packet:

| Slot | Actual candidate operation |
| --- | --- |
| BEGIN | Validate, acquire/copy/release one snapshot, initialize continuation |
| PREPARE | One transform/horizon state transition; final completion also builds registration |
| PROJECT | One segment begin or transform/clip/project state transition |
| BACKGROUND | Eight narrow cached-boundary comparisons and staging writes |
| COPY | One checked 64-byte physical copy and index/phase update |
| LINE | Visibility/segment transition, cursor begin, or one pixel/one-byte copy |
| TEXT | At most one 40-character format plus one 64-byte glyph |
| COMMIT | Complete-bundle validation, checked border selector and coherent latch |

Arithmetic wait transitions process one six-cell multiply row or restoring-
division bit. Their setup/finalization, result copying, rounding and following
bookkeeping belong to the same eventual bound. Some transitions also perform
12 byte-loop doublings or two plane distances. No cycle, interrupt overhead,
guard/return cost, frame-rate or latency bound has been invented. Cardinality
does not establish admission; fit failed before that engineering stage.

## Host and independent evidence

Actual commands, exits, inputs and logs are under
[`2026-10-30-m2-unbanked-renderer`](../evidence/flight-demo/2026-10-30-m2-unbanked-renderer/accounting.json).
Reproduction entry: `python3 -B tools/flight_demo/m2_rebuild/compact_validate.py
--tier host`. This is the candidate's canonical build composition; the shared
baseline builder alone retains its baseline source list. The target entry
adds `--tier target --sdk <absolute pinned SDK>` and is create-once guarded.
No repeat target link is authorized here.

- ASan/UBSan complete frame, mutable camera, held snapshots, cancellation,
  registration corruption, transfer/commit faults, exhaustion and replay PASS;
  identical 600-tick checksum `DE675132` across rendering schedules.
- 16,588,800 exact horizon pixels, including +/-60-degree extrema, +/-45-degree
  zero ties, zero slopes and yaw variations; maximum 469 preparation services,
  not a cycle or throughput claim.
- Cancellation at 5,487 actual numeric continuation cutpoints PASS.
- Independent bigint: 3,252 complete products/Q46/divisions, 117,072 actual
  multiplication cells, every row carry and every division-bit remainder and
  quotient, ties/signs/overflow/invalid paths PASS.
- Independent native-reference comparison: 1,360 bit-exact transforms and
  4,080 bit-exact clipped/projection results, including unchanged empty outputs.
- Frozen independent Decimal oracle: 3,857 cases PASS; maximum projection error
  0.0000212243 pixel. Near/far regressions: 841 PASS; maximum 0.035136325 pixel.
- All 32,768 camera edge-mask/pose cases match the preserved main implementation.
- 2,048 independent telemetry rows PASS under sanitizers, including all labels,
  counters, signs and placement. Required glyph definitions remain unchanged.
- Original 31 contract/startup/SDK regressions plus four closure checks PASS;
  later six focused closure/specialization checks also PASS. Missing/dead code,
  native-wide retention and changed generated precision fail closed.

The first host packet is a retained test-fixture failure: the new cancellation
test reused the original snapshot pool after its capture had been released.
The correction clones the pool and publishes a fresh snapshot before restart;
it does not weaken rendering assertions. A later focused host test compile
failure from a host `long` conversion is also retained, followed by its passing
strict-compile/sanitizer result. Earlier syntax-check diagnostics remain in the
task transcript; only the sealed packets above support the final claims.

The [host preview](../evidence/flight-demo/2026-10-30-m2-unbanked-renderer/host-1793345435740522000/host-frame.png)
shows the actual host-composed sky, ground, runway and telemetry. It is **not an
Xemu screenshot**, frame cadence measurement or target behavior evidence.

## Stop and next action

Complete resident fit is the single next engineering blocker. Text plus prefix/
alignment leaves 184 bytes for 3,658 bytes of constants, BSS and scratch.
Moving only the 487-byte new state—or even all 1,163 renderer bytes to legal
Graphics workspace—cannot solve it before access overhead. That workspace is
not executable resident capacity. No such move is implemented or authorized.

There is no credible isolated small fix: control-only replacement would have
to shrink 4,036 to 562 bytes. The smallest meaningful follow-up review target
is the combined 7,800-byte numeric-control plus composition closure, requiring
at most 4,326 replacement bytes before any new overhead. A shared bounded
render-command interpreter is a concrete strategy to evaluate against this
threshold, not a proven saving or permission to implement another experiment.
Founder review owns the next implementation direction. This task preserves
the failed candidate; it does not start that follow-up, banking or a new limit.

Physical follow-on is deferred. There is no admitted executable to package.
After a later fit/safety-qualified PAL/NTSC emulator result, a separate handoff
must pin that executable and cover media verification, ROM/startup differences,
input/video differences, memory/timing measurements and abort conditions.
