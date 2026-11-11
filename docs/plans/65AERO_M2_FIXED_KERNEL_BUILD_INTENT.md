# M2 fixed-layout exact renderer — approved conditional Build Intent

Status: **FK-D1–FK-D8 approved by founder; READY FOR REVIEW after failed preflight.**
Implementation and one target link are conditional on the ordered preflight gates.
The original planning checkout is preserved unchanged.
Execution stopped at the complete-cost gate; see the
[preflight handoff](../reports/M2_FIXED_KERNEL_PREFLIGHT.md). No target source,
generated profile, link or runtime execution followed the failure.
Proposed private identity: `65AERO-M2-FIXED-KERNEL-1`, outer composition revision
4 with the existing inner public registration revision unchanged; no generated
profile is adopted by this document. This is one bounded implementation strategy, not an
authorization to resume the failed experiment or run its executable.

## Baseline and authority

Remote references verified for this plan:

- Main: `9570f0ab427121a4e8f042041a14c89aaaeff9e2`.
- Preserved source and CI correction: `0e63edfb7de62ff991c91072a02397f432c12582`.
- [PR #32](https://github.com/SUON1/f65-megawing/pull/32) remains draft,
  **FAILED FIT AND TIMING — NOT FOR MERGE**.
- Sealed target PRG SHA-256:
  `7fdcea61387c0e6b7ae92310725966ac6c0e29e82e8ba1c9a6be77335af76aad`.
  Its source packet and all 12 target seal members were checked without relinking.

The [Phase 1 plan](65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md),
[minimum profile](65AERO_M2_MINIMUM_REBUILD_BUILD_INTENT.md),
[extended resident contract](../../interfaces/m2_extended_resident.json),
[display contract](65AERO_M2_PR2_BUILD_INTENT.md),
[Platform registry](../../interfaces/f65_platform_abi.json5) and current
[specification manifest](../../spec/manifests/spec-corpus.json) govern.
The founder's throughput direction permits a private hidden screen-map and
immutable-tile representation; its implementation never cleared the integrated
estimate gate. This proposal requires explicit renewal of that bounded scope.
It does not adopt RF banking or amend permanent production ownership.

## Recommendation and actual blockers

Replace the generic numerical command interpreter and its pointer-heavy limb
execution with fixed-layout exact continuations; construct the hidden display
through solid/glyph tile references and exclusive mixed tiles. Keep the current
per-generation line cache, exact raster algorithm, telemetry values and public
records. Do not build a second generic interpreter or add another persistent
geometry cache. Prove tick feasibility first, before extensive renderer work.

The two historical failures remain independent:

| Gate | Preserved result | Meaning for the next implementation |
| --- | --- | --- |
| Resident | 29,426 / 28,671 bytes; **755 bytes over** | New code, constants, state, scratch and alignment must all fit below end-exclusive `$9000`. Production remains end-exclusive `$8000`. |
| Cold numerical work | At least 2,323,776 / 2,025,000 cycles; **298,776 over** | This lower bound excludes display, ticks and other work. Recovering only 298,776 cycles cannot establish 20 Hz. |
| Tick service | Prior SERVICE1 conservative envelope 438,269 / 405,000 cycles | This is an unresolved upper-bound proof, not a measured tick overrun and not a bound for a new executable. |
| Worst clipping | 198 divisions; 32,760-cycle existing division bound, before numerator/wrappers | The old conservative division envelope alone is 6,486,480 cycles. Faster default frames or cache hits cannot close this gate. |

Sources: [wide report](../reports/M2_EXACT_WIDE_ARITHMETIC.md),
[throughput report](../reports/M2_THROUGHPUT_ARCHITECTURE_CORRECTION.md),
[sealed throughput estimate](../evidence/flight-demo/2026-11-09-m2-throughput-architecture/throughput-estimate.json).
No new fit or timing success is claimed here.

## Founder decisions

| ID | Exact decision requested | Recommendation |
| --- | --- | --- |
| FK-D1 | Approve one successor implementation from `0e63edf`, under a new private identity, replacing generic numerical execution with fixed-layout bounded continuations? | **Approve**, preserving the failed branch and all original source/evidence. Retain public APIs and exact operation/rounding order. No new general interpreter. |
| FK-D2 | Permit measured, narrowly scoped 45GS02 kernels for exact byte packing, arithmetic, Platform math transactions and bounded display copies? | **Approve conditionally** on explicit compiler ABI, generated private offsets, register/clobber and stack contracts. Graphics owns pure arithmetic; Platform alone owns MMIO. Preserve exclusive acquisition, bounded polling, output-on-success, fault lockout and canonical state. |
| FK-D3 | Renew the private hidden-map/immutable-tile display exception for this successor, retaining the approved image and existing display ranges? | **Approve** the previously examined layout, implemented together with the numeric replacement only after the cost gate. No cross-store references, visible writes, new physical allocations, DMA or reserve use. |
| FK-D4 | Approve a private captured-camera publication rule in place of cancellation on every newer requested pose? | **Approve explicitly as a development-only contract amendment**: capture-to-commit at most 50 ms; accept input on every authoritative tick; finish the coherent capture and take the latest pose at the next begin. A persistent accepted pose must appear in a committed frame within 100 ms, with scanout latency separately qualified. Faults, explicit cancellation and identity invalidation still abort immediately. |
| FK-D5 | Keep precision, nine segments, camera envelope, telemetry, resident ceiling and timing requirements fixed? | **Approve unchanged**: Q12/Q24/Q46/Q16, all nine selected segments, 320×200 image, 100 Hz/21 stages and 20 Hz complete-frame requirement. No cache-hit-only qualification or smaller camera envelope. |
| FK-D6 | Require tick and complete-cost proof before extensive renderer implementation, with a single failure stop? | **Approve**. First tighten the tick proof using executable control-flow invariants. If the proof still cannot establish sufficient slack, stop; do not alter CoreRuntime, the clock or queue contract automatically. |
| FK-D7 | Authorize the bounded implementation, independent host/sanitizer checks and one complete pinned-toolchain target link after preflight succeeds? | **Approve conditionally**. Charge every new byte and full successful/fault service path; target at least 256 resident bytes of headroom. Preserve any failed link and stop rather than start another size campaign. |
| FK-D8 | What publication and execution authority follows that increment? | **Stop at READY FOR REVIEW after static gates or the first unresolved mandatory gate.** No automatic publication, merge or Xemu. Separately authorize exact-image enabling and PAL/NTSC qualification after review. No D81, SD or physical testing. |

## Concrete implementation boundary

### 1. Fixed-layout numerical continuations

Replace `m2_command_service`, `bind`, `operand`, their command tables and the
private limb execution closure. Retain the public geometry adapters and the
independent implementation/oracles as host reference code. The candidate must
link one selected backend, not both. Existing begin/service result semantics
and fault refusal remain checked. Explicit bounded phases are: rotation setup,
endpoint transform, six ordered clipping planes, projection and horizon scan.
Generate private field offsets and enforce static layout checks; do not assume
host struct layout or LLVM-MOS argument registers in hand assembly.

For each endpoint, subtract the captured camera coordinates once per axis,
convert each signed Q12 delta to Q24 by exact sign-extended byte/nibble packing,
and reuse that three-component delta across the three matrix rows. This reduces
the current 162 conversions to 54 without deduplicating fixture endpoints.
Reserve at most one explicit 24-byte delta buffer; no assumed lifetime overlay.
The current repeated 12-step, eight-byte doubling loop is eliminated. This is
the exact scaling operation, not reduced precision. Check extrema and preserve
the existing rounding of each matrix product before summation: do not replace
three rounded products with one differently rounded dot product.

Keep full signed48 magnitudes, complete 96-bit products, exact radix-24
division, bounded estimator correction, ties-away rounding, narrowing and
overflow checks. Replace generic pointer-loop movement and repeated command
decoding with fixed-width kernels. Preserve the current six-plane clip order
and update semantics; no new approximate reciprocal or different clipper.

Platform may expose a private bounded compound transaction to avoid acquiring
and restaging the same fixed-layout operands for every partial product. A
transaction must finish and release ownership before returning to the scheduler;
it cannot leave math registers leased across a yield. Every hardware result
still requires the defined readiness check. Failure cannot expose partial
caller results. Keep the sticky NMI/Platform fault checks before publication,
including faults arriving after the final device check. No blanket IRQ masking.
If a complete transaction cannot fit the admitted atomic budget, split it at
an explicitly proved checkpoint; do not consume the next simulation release.

Do not claim saved cycles from source brevity or from deleting safety checks.
The new engine validates state, indices, generation, buffer identity, product
readiness and continuation transitions directly, rather than relying on an
unchecked instruction stream. Unknown paths remain unproven.

### 2. Hidden-frame tile composition

Use the same two display stores at `$020000` and `$030000`, each with:

| Offset, inclusive | Use |
| --- | --- |
| `$0000–$07CF` | Complete hidden 1,000-entry map; immutable while visible |
| `$07D0–$07FF` | Existing alignment, not scratch |
| `$0800–$A7FF` | 640 cell-exclusive dynamic world tiles |
| `$A800–$B27F` | 42 immutable sky/ground and nonblank glyph tiles |
| `$B280–$F7FF` | Unused existing tile capacity; no new allocation |
| `$F800–$F83F` | Existing immutable black tile for spaces/footer |
| `$F840–$FFFF` | Protected unused display slack |

Generate every tile identifier from its own store. Platform accepts typed local
map/tile operations and checks ranges, map progress, hidden-store ownership and
completion. Graphics never accesses physical RAM or registers directly.
Keep shared Color RAM and palette immutable after initialization.

Build map chunks of at most 32 entries using the existing Platform 64-byte
buffer after initialization has retired; prove synchronous, nonoverlapping use
on success, cancellation and fault. Do not allocate a resident 2,000-byte map.
Use an 80-byte initialized-tile bitmap. Construct a mixed horizon tile once;
when a runway first touches a previously solid cell, materialize its correct
background and change only that hidden cell's reference. Retain exact raster
pixels and then overlay the line. Coalesce physically contiguous same-tile
writes when equivalent; charge remaining single-pixel writes explicitly.
Never rerun projection per tile or redraw all 640 world tiles.

Map telemetry characters to immutable glyphs after computing the same frozen
values. Preserve `NON-FLIGHT DIAGNOSTIC`, both `NOT IMPLEMENTED` labels,
camera fields and source-age provenance. All 1,000 map entries and every dynamic
tile they reference must be complete before the store can become visible.
Cancellation invalidates the partial hidden generation and bitmap; the prior
front remains intact. New begin reconstructs all map entries. Do not reuse
partial data merely because the camera revision matches.

The prior host model reconstructed the default image exactly with 48 dynamic
tiles and 5,168 copied bytes versus 61,536. Its 550-tile geometric union bound
requires rechecking against the implemented raster. Allocation remains safely
bounded by 640 slots even if that tighter performance proof is unresolved.
The previous 40,080-byte worst-demand scenario includes up to 2,880 line writes;
it is not an admitted display timing bound. The old 26-cycle/byte copy body
would already cost 1,042,080 cycles for that scenario, before setup or painting.
Therefore the earlier 925,000-cycle display planning allocation cannot simply
be reused with those independent maxima and the old copy cost. Prove a tighter
joint demand or budget a fixed-count Platform copy kernel (at most 64 bytes,
same PF001 physical-range and interrupt/scratch contract, no historical PF001
source edits) within this same proposal; otherwise stop at the integrated cost gate. No DMA fallback.

### 3. Tick and publication scheduling

Refine proof of the unchanged executable tick path using stage-specific loop
counts, the single producer/next-tick command invariant, queue emptiness after
stage 3, and bounded snapshot/keyboard/clock paths. Independently verify these
invariants; do not suppress unexpected queue states or delete the general
runtime checks. The previously reported 438,269-cycle envelope is not a grant.

Require every authoritative tick to fit its 405,000-cycle interval. For the
frame proof include every tick release intersecting construction/publication,
input, clock retries, guards, IRQ/NMI envelope, dispatch and return costs. Count
phase alignment and top-border/prefetch waiting; a CPU-work total alone does
not guarantee 50 ms completion. Preserve one tick at a time with all 21 stages.
No catch-up debt may be presented as meeting the deadline.

Cold and changed-camera generations must qualify without a geometry-cache hit.
The current `coherent()` cancels on any difference between wanted and captured
camera; [the earlier composition contract](65AERO_M2_PR2_FULL_COMPOSITION_ADMISSION_INTENT.md)
explicitly says a new camera revision invalidates pending work. At continuous
100 Hz changes, work spanning a tick can be repeatedly discarded. Faster
arithmetic by itself is not proof of moving-camera frame cadence.

**FK-D4 requests a narrow, explicit exception**, not a reinterpretation of that
rule: while a generation is active, validate its complete captured identity,
not equality with a newer requested camera. Capture and publish one immutable
camera/snapshot pair within 50 ms, including prefetch-window delay. Continue
accepting every semantic input on each tick; do not stall Diagnostics or mutate
the active capture. At the next begin, capture the latest requested pose.
Intermediate presentation poses may be superseded; authoritative input/ticks
and replay are not dropped. If an accepted pose persists, it must be reflected
in a committed frame within 100 ms (the remaining current frame plus the next).
Device polling and scanout latency require separate accounting; this is not a
claim about observed input-to-photon latency.

Explicit cancellation, fixture/projection/composition invalidation, exhaustion,
fault, corrupt identity, or expiry of the capture deadline still rejects the
candidate and preserves the previous complete frame. Never relabel an older
capture as the latest pose. The registration, telemetry and runway/horizon
must all name the actual captured camera, source tick and generation. Keep
`AGE AT TEXT` provenance unchanged; record capture-to-commit age independently
for qualification. A frame older than the approved bound cannot count as a
normal successful publication.

Encode this exception in the new private profile and validator, preserving the
old rule and tests for older profiles. This requires coordinated Graphics,
Diagnostics and Presentation acceptance, with no public record layout change.
Without FK-D4 approval, retain the old cancellation rule and require proof of
completion within the available between-change window; do not claim this plan
has solved moving-camera throughput. Source changes are conditionally authorized only after preflight passes.

## Replacement budget, not predicted savings

The following values are from the sealed exact-wide linked symbol sizes, not
standalone compilation. They are nonoverlapping selected symbols, not the
entire renderer or a claim that shared helpers will disappear automatically.

| Candidate replacement group | Existing bytes |
| --- | ---: |
| `m2_command_service` 3,090 + `bind` 261 + `operand` 245 | 3,596 |
| Selected private wide/limb helpers listed below | 2,553 |
| `math_transact`, `math_ready`, two math entry wrappers | 334 |
| `m2_commands` + `m2_command_constants` | 452 |
| **Selected replaceable footprint** | **6,935** |

The 2,553-byte group is `m2w_i32`, `m2w_negate`, `m2w_add`, `m2w_double`,
`m2w_compare`, `m2w_positive`, `m2w_narrow`, `magnitude`, `m2l_multiply`,
`m2l_divide`, `m2l_service`, `normalize`, `multiply_part`, `divide_digit`,
`finish`, `subtract_product`. Inspect all linked callers before taking any
retirement credit; replacements serving retained callers count as new costs.
Shared compiler routines, boot code, glyph data, general runtime checks and
stack reservations receive **zero assumed savings**.

If all selected old bytes are replaced, unchanged resident cost is
`29,426 − 6,935 = 22,491`. The maximum net replacement/addition allowance is
`28,671 − 22,491 = 6,180` bytes. A recommended 256-byte margin reduces that
allowance to **5,924 bytes**. Charge the proposed 80-byte bitmap and 24-byte
delta buffer first, leaving **5,820 bytes** for all replacement code/constants,
net tile/Platform changes, descriptors, metadata, added state, scratch and
alignment. Existing BSS is retained in this conservative arithmetic; no
workspace-reuse or old-controller BSS saving is assumed. Any old symbols that
remain linked reduce the allowance byte for byte.

This is a falsifiable implementation budget, **not evidence that the new engine
fits**. Stack safety is an independent gate; using a reserved stack or static
scratch does not make costs disappear. Report actual text, rodata, data, BSS,
compiler scratch, padding, stack maxima and physical owner ranges together.

## Gates and bounded execution order after approval

1. **Tick proof and ownership preflight.** Read the pinned code and control flow;
   establish a defensible per-tick bound and frame slack, exact private ABI,
   math-register exclusion, display-map ownership, workspace and cancellation
   lifetimes, including the explicitly approved FK-D4 amendment. Stop if the unchanged tick or publication contract cannot qualify.
2. **Complete implementation cost gate.** Produce an instruction-level design
   bound for the fixed kernels and all display operations, with byte encoding
   estimates and compiler-wrapper allowances. Retain up to 162 interpolation
   and 36 perspective divisions unless a stronger joint bound is proved.
   Include full transforms, clipping, horizon, raster, text, transfers, guards,
   interrupts, tick interference and commit delay. Unknown cost is not zero.
   Require total resident budget closure and a justified schedule within the
   2,025,000-cycle/50 ms frame interval before the extensive rewrite. Sample
   cameras, operation-count savings and the 6,935-byte footprint alone do not
   satisfy this gate. If credible closure cannot be established, stop.
3. **One coherent implementation.** Implement the fixed-layout backend and tile
   representation as the selected private profile. Preserve portable/reference
   source and evidence. No unrelated cleanup or new engine services.
4. **Independent host correctness.** Bit-exact products/carries, division
   digits/remainders/corrections, signed extrema, ties and overflow; original
   geometry oracle plus near/far and all clip boundaries; camera/horizon,
   pixel reconstruction of maps/tiles, telemetry, cancellation, held snapshots,
   fault/reentry/timeout/exhaustion and replay under ASan/UBSan. The reference
   must not call the replacement arithmetic. For assembly, host C tests alone
   do not prove its machine semantics: require a separate instruction-level
   equivalence argument/checker before target execution.
5. **One complete target link.** Use the pinned LLVM-MOS compiler and flags;
   retain source/tool hashes, commands, output, PRG, ELF, symbols and disassembly.
   Include all real camera/input/runtime/font/platform code. Require resident
   ≤28,671 and zero reserve. Preserve a failure, report its exact deficit and
   stop. A fit with under 256 bytes margin is a review concern, not permission
   to increase the limit or perform another automatic rewrite.
6. **Exact-image static admission.** Verify PRG loading and CPU visibility through
   `$9000`, startup before BSS/scratch, ROM/cartridge policy, MAP/B restoration,
   full reachable hardware/software stacks, IRQ/NMI/fault paths and each service
   bound. Bind proofs to raw linked bytes, then establish the whole-frame
   schedule for cold, unchanged, moving and cancellation cases. Earlier boot-only
   PAL/NTSC traces do not qualify this executable. Unsupported paths stop.
7. **READY FOR REVIEW.** Report both measured fit and proved service results
   independently. Keep enablement and grants zero for this static checkpoint.
   A later founder-approved enabling build must bind its exact bytes, nonzero
   budgets and startup/stack/service proofs before direct-PRG PAL/NTSC execution;
   no post-proof patching of the quarantined PRG. No runtime authorization is
   implied by approval of the strategy alone.

If this coherent replacement cannot close the mandatory gates, recommend a
single explicit founder decision on the development presentation/camera
latency contract. Do not select reduced cadence, precision, pixels, banking,
another memory ceiling or another sequence of micro-optimizations automatically.

## Preservation and current planning handoff

Plan branch: `codex/65aero-m2-fixed-kernel-intent`, separate clone based on
`0e63edf`. Only this document and WIP change. The implementation, generated
contracts, historical seals and PR #32 remain untouched. No target tool,
arithmetic optimization or runtime test was run for this plan.

Future implementation should use a new branch from the explicitly approved
preserved source identity, refreshing main and checking conflicts first. This
is experimental ancestry, not verification or admission on main. A future
integration path requires separate review; do not merge the failed PR.
Two unavailable historical checkouts remain NOT VERIFIED at the Git-worktree
tier. Retained hash evidence is not reconstruction of their Git metadata.

Hardware impact of the **plan itself**: none. Proposed implementation impact is
limited to Platform math status `$D70F`, operands/results `$D768–$D77F`, existing
typed display-copy/register seams and Graphics-private resident state. Every
assembly entry must state A/X/Y/Z/Q/P clobbers, preserve required compiler ABI
state and canonical B/MAP/ports, and charge hardware/software stacks. No new
base-page scratch lease, CPU-port change, IRQ/NMI owner, DMA, banking or
protected-reserve allocation is proposed. Any required exception stops for review.
