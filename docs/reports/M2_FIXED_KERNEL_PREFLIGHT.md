# M2 fixed-kernel preflight — stopped before implementation

**READY FOR REVIEW — BLOCKED at complete-cost preflight.** FK-D1–FK-D8 are
approved. The tick CPU-work prerequisite now closes; the required complete-frame
schedule does not. No renderer source, generated profile or target binary changed.
Target links: **0**. Runtime executions: **0**.

The new branch is `codex/65aero-m2-fixed-kernel` in
`/private/tmp/f65-m2-fixed-kernel-preflight`, from
`0e63edfb7de62ff991c91072a02397f432c12582`. Fetched main remains
`9570f0ab427121a4e8f042041a14c89aaaeff9e2`. This is experimental ancestry,
not an admitted main implementation. PR #32, its checkout and the original
planning checkout were not modified. The [approved conditional intent](../plans/65AERO_M2_FIXED_KERNEL_BUILD_INTENT.md)
governs the first-failed-gate stop.

## Tick proof

The [new host verifier](../../tools/flight_demo/m2_rebuild/fixed_preflight.py)
reads the sealed wide-arithmetic PRG, listing and symbols. It checks all 12
target seal members, all 81 source/generated inputs, raw instruction bytes,
branch targets, timing-table identity and the single producer/call graph.
No target instruction is executed.

The linked main invokes one input sample immediately before one tick. The sole
command producer can enqueue at most one command for that next tick. Stage 1
increments the tick, stage 2 latches that command, and stage 3 drains it. The
queue is empty at stage 20. Initialization establishes this invariant and the
terminal tick check prevents another sample after tick exhaustion. Neither
interrupt handler nor Graphics produces commands. General queue checks remain
in the source; this is a proof for this composition, not a reduced queue ABI.

Every stage body runs once, with 22 dispatcher tests and 21 increments. The
verifier deliberately counts other tick instructions twice, including the
unreachable shift/future-command bodies. It separately bounds three snapshot
slots, 13 keyboard rows, three position/angle axes, exact copy lengths, compiler
multiply/shift loops and all 32 clock attempts. Both sides of branches are
charged; undeclared dependencies or uncovered cycles fail closed. Return and
call instructions are included. Terminal fault paths are charged through the
status write, not described as returning from the permanent terminal loop.

| Tick component | Conservative CPU cycles |
| --- | ---: |
| Clock sample | 5,229 |
| Keyboard matrix | 8,290 |
| Camera edges, including validation and copies | 12,144 |
| Ordered core tick and snapshot publication | 11,298 |
| Remaining input, main bookkeeping and terminal-entry paths | 1,929 |
| Two raster IRQs and one terminal NMI, including entry | 236 |
| **Total** | **39,126** |
| 100 Hz interval | 405,000 |
| CPU slack before renderer dispatch | 365,874 |

This replaces the loose 438,269-cycle planning envelope **for the inspected
old executable's CPU work only**. It does not qualify a new executable, convert
native clock counts, establish a complete-frame deadline or enable a grant.
Interrupt scope remains the pinned reset-only configuration: raster IRQ only,
CIA interrupt masks disabled, sticky terminal NMI, no repeated external NMI
injection or unbounded external master. Whole-program stack/startup admission
for any successor still requires its exact linked image.

## First unresolved mandatory gate

The proposed fixed-layout implementation was examined using an explicit
instruction sketch, before writing target code. It already credits compound
operand reuse (20 input bytes for four partial products rather than 32), fused
product accumulation, the pinned emulator's immediate-ready math status, and
a 15-cycle near-to-physical copy payload instead of the old far-source loop.
An eight-poll timeout is not multiplied into every successful transaction.

The fixed-width normalization sketch relocates whole bytes and then uses at
most seven ASL/ROL passes over the 18-byte dividend and six-byte divisor. Only
the memory-shift payload is charged here. It is an examined design choice,
not a theorem that every exact normalization implementation costs this much.

| Partial design-budget item | Cycles |
| --- | ---: |
| 377 full-product payloads/readiness checks, 592 each | 223,184 |
| 396 quotient-digit payloads/readiness checks, 445 each | 176,220 |
| 198 normalization shift payloads, 1,176 each | 232,848 |
| 40,080 display bytes, 15-cycle payload each | 601,200 |
| Six tick reservations, allowing boundary carry-in | 234,756 |
| One complete PAL-frame publication-wait reservation | 808,704 |
| **Partial separable budget** | **2,276,912** |
| Required 50 ms frame interval | 2,025,000 |
| **Unclosed partial-budget amount** | **251,912** |

The product count is 14 rotation + 3 horizon + 162 endpoint-transform + 198
division numerators. Division demand retains the approved conservative
162 clip interpolations + 36 perspective divisions, with two radix-24 digits
each. Display demand provisionally credits the 550-tile geometric union bound:
2,000 map bytes + 550×64 tile bytes + 2,880 runway writes. That tighter raster
bound still needs proof; the allocation itself safely permits 640 tiles.
PAL reserves 624×1,296 cycles under the pinned reference. Tick work during
the wait may overlap that reservation; no credit for that overlap is taken.

**This sum is not a measured frame, a complete WCET, an unavoidable lower
bound, or proof that an actual camera exceeds 50 ms.** It combines independent
maximum-demand allowances and a phase wait. It demonstrates that this
conservative admission construction has not closed. Counting only five ticks
would still leave this partial budget 212,786 cycles over, before missing work.

Still unbounded are normalization relocation/control, sign and correction
paths, rounding/overflow, exact horizon/plane/control work, tile painting,
raster/text/map construction, Platform checks/restoration, compiler wrappers,
continuation/guard overhead and the native-clock/publication phase schedule.
Those costs are **unknown**, not zero. A tighter joint-demand or phase proof
could change the result; sampled cameras cannot establish it. The required
complete instruction/encoding budget and private ABI/layout implementation
therefore are not claimed complete. The first cost-gate failure prevents the
extensive rewrite, host rendering campaign and single target link.

## Memory, ownership and unchanged failures

The sealed linked symbols confirm the selected 6,935-byte replacement footprint.
It leaves a hypothetical 6,180-byte replacement/addition allowance, or 5,820
after a 256-byte margin and the proposed 80-byte bitmap plus 24-byte delta buffer.
No retirement saving has actually occurred. New encoded code, constants,
wrappers, scratch, stacks and alignment remain unmeasured.

The only actual executable remains 29,426 / 28,671 resident bytes: **755 bytes
over**, 87 compiler-scratch bytes and zero protected-reserve use. Its separate
sealed cold-frame lower-bound failure remains 2,323,776 cycles, **298,776 over**.
The new 251,912 figure is a different, partial design budget and never replaces
either sealed failure. There is no new PRG or measured resident result.

Inspected authority: current specification manifest, Phase 1/minimum profile,
extended resident contract and ledger, public geometry/registration records,
Platform registry, approved FK intent, and existing source/sealed evidence.
CoreRuntime still owns 100 Hz/21 stages; Diagnostics owns requested camera;
Environment keeps all 17 fixture segments and Graphics selects the same nine;
Presentation owns snapshots; Graphics owns immutable captures/cache/composition;
Platform alone owns math/display I/O. FK-D4's approved captured-camera amendment
is recorded in the intent but is not silently applied to the old generated profile.

No public ABI, precision or allocation changed. Production stays below `$8000`,
development below `$9000`, with software stack `$C000–$CFFF`, page-one hardware
stack, base page `$0200`, and zero reserve. The proposed tile map stays inside
the two existing Graphics stores and leaves protected display slack intact.
The proposed Platform buffer reuse must remain synchronous and nonoverlapping
after initialization; it was not implemented or credited as a new saving.
Registers/clobbers, CPU ports, MAP/B, DMA, IRQ/NMI and hardware behavior of this
host-only increment: **no change**. No new private assembly ABI was activated.

## Validation and handoff

Evidence: [preflight packet](../evidence/flight-demo/2026-11-11-m2-fixed-kernel-preflight/README.md).
The final preflight command exits **2**, explicitly refusing admission. Its
11 host-only fail-closed regressions pass. Syntax, JSON, documentation-link,
whitespace, scope and preservation results are recorded in the packet.
Earlier verifier-development failures remain alongside the final result.

All 16,556 original tracked files outside this checkout's WIP remain byte
identical. All 480 unrelated root-checkout paths retain their exact inventory
and hashes. Six available historical checkouts match recorded HEAD/status/diff;
two missing checkouts remain **NOT VERIFIED at the Git-worktree tier**. No
missing metadata or old packet member was reconstructed.

Recommended next review: decide whether to revisit the development-only
presentation/camera-latency contract while preserving the 100 Hz simulation.
This result does not certify a replacement deadline or authorize one. Keeping
50 ms requires a complete, stronger joint cost/schedule proof before any rewrite;
do not begin another automatic optimization series. No publication, relink or
runtime work follows this checkpoint without separate review.
