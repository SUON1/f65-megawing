# Group 2 size and capture redesign

**R1 IMPLEMENTED — bounded host/fit proof; R2–R5 remain design.**
Current disposition, 2026-10-04: [Group 2 bounded work-package closure approved](../reports/R0-F_GROUP2_CLOSEOUT_REVIEW.md).
Remaining capture/fit work is carried into the upcoming supplement/plan review;
the proposal and measured history below are preserved, not new execution authority.
2026-10-03. Scope: owner's request for a concrete redesign after the two failed
outlining trials, under the [Group 2 intent](R0-F_GROUP2_BUILD_INTENT.md).
The original design proposed private scratch ownership, source factoring and a
generated trace extension. Owner subsequently authorized the first R1 increment;
see the measured update below. Original estimates remain labeled as proposals.
No commit/push until Group 2 is finished. Group 3 is not assigned.

## Decision and measured starting point

Use per-subcase compiled variants of the complete combined fixture, a single
foreground scratch allocation and one shared PF request encoder. Keep a bounded
case extension inside the existing trace allocation. Do not widen resident
memory, borrow reserves, remove integrity checks or replace combined-load proof
with standalone tests. This is a proposed implementation remedy, not fit proof.

| Retained configuration | Resident end | Margin below $C000 |
| --- | --- | --- |
| Frozen P09 | $BFF5 | 11 bytes |
| Minimal G2-Q admission | $C16F | -367 bytes |
| Frame-wait outlining | $C16F | -367 bytes |
| Ratio outlining | $C366 | -870 bytes |

Sources: [admission](../evidence/r0f/group2/2026-10-03-target-admission/README.md),
[outlining](../evidence/r0f/group2/2026-10-03-outline-trials/README.md), and frozen
P09 `runtime-01-sizes.txt` indexed by the
[P09 packet](../evidence/r0f/group1/2026-10-03-audio-readback/README.md).
The P09 map has 32470 text, 497 rodata, 23 data, 3405 BSS, 36 compiler static-stack
bytes and 4495 protected bytes. Large linked bodies include `main` (9006),
`run_ticks` (4730), `display_quantum` (3774) and `cfcalibrate` (2235). These are
LTO symbol sizes, not independent module costs. Do not estimate recovery by
adding or subtracting them as though inlining were additive.

## R1: eliminate duplicate scratch storage, preserving capacity

Propose one generated private `r0fg2_foreground_scratch[255]` ordinary-resident
allocation for these three existing buffers:

| Existing buffer | Inspected lifetime / access | Sharing rule |
| --- | --- | --- |
| `combined_platform.c:cfworkspace` (`check`) | ROM backup/restore readback, immediately compared to separate `block` | Exclusive until compare completes; no logger/capture call while live. |
| `successor_integration.c:transfer` | DOS CRC/pattern; display staging initialization/resume; terminal color initialization | Exclusive until copy/CRC consumes it; no capture/ROM call while data is live. |
| `group1_transport.c:buffer` | Capsule validation; synchronous trace read/write/CRC | Exclusive until transfer/consumer completes; never borrow from a live source/destination buffer. |

The inspected calls use synchronous PF flat-copy. `cfcopy` and
`fixed_physical_copy` do not use these scratch buffers internally; they pack the
request and perform the copy. The inspected IRQ body does not call these C
owners. Display setup finishes using `transfer` before normal acquisition;
ROM verification, DOS work and terminal capture also occur in sequenced calls.
This supports a sharing hypothesis, not a completed alias/reentrancy proof.

**Gross storage recovery: 3 × 255 − 255 = 510 bytes.** Preserve each user's
255-byte capacity. Add explicit generated private ownership/ledger rules and
compile-time size checks; prefer typed access at the named owner boundary over
unscoped textual aliases. Any ownership guard bytes/code count against savings.
Do not share platform `block[255]` with readback scratch: ROM comparisons require
both live buffers. Do not share capture `record[92]` or `header[256]`: they hold
live acquisition data across transport calls. Do not borrow protected context
buffers, hardware/software stack allocations, display RAM or reserves.

Required proof before target integration: enumerate every caller, failure exit,
IRQ/NMI interaction and nested callback; fail closed if simultaneous liveness is
possible. Host-test actual affected ROM/DOS/display/transport functions with
poisoned scratch handoffs, alias-aware copy mocks, guards and forced copy errors.
Verify that source bytes remain live until copy completes, first faults survive,
all ROM/guard/CRC comparisons remain, and actual hardware wrappers still own PF
request state. No reentrancy may be assumed away by only testing success paths.

## R2: factor duplicate PF request encoding, not validation policy

Three source sites pack the same 9-byte PF request then call
`r0f_pf_flat_copy`: `combined_platform.c:cfcopy`,
`successor_integration.c:fixed_physical_copy`, and
`group1_transport.c:transfer`. Their measured P09 bodies are respectively
739, 239 and 450 bytes; only the packing portion is common.

Introduce one private foreground helper accepting source, destination and byte
length; keep original caller range/lifecycle checks and original failure/first-
fault behavior at their owning sites. Preserve all four address bytes and the
length byte. Do not combine callers' admission policies or convert the helper
into a public arbitrary-physical-pointer API. Keep direct ROM/context assembly
paths unchanged. The helper must remain accessible under every caller's existing
MAP conditions and cannot be used from IRQ/NMI.

Host proof compares all nine request bytes against an independent encoding for
boundary addresses, lengths 1/255, read/write direction and carry boundaries;
actual callers must still reject out-of-range writes and propagate PF failures.
Target proof checks emitted calls, preserved registers and stack cost. Net code
savings are **unmeasured**; this is a concrete duplicated operation, not another
global inlining experiment. Reject the factoring if net fit or timing worsens.

## R3: per-subcase combined builds and explicit budget

One compile-time selected fault subcase per variant, with all ordinary workload,
capacities, phase/order coverage, timing and integrity logic retained. Only
unselected **new Group 2 injectors** may be removed by compilation. Use the same
source revision and generated case registry, and retain each configuration/hash.
No branch may omit audio/display/storage or reduce the entity fixture to fit.
The old pre-workload queue probe is an admission experiment, not the final G2-Q
implementation; final pressure must reach the actual owner at its declared live
boundary. Initial nonfatal cases run before and after storage; fail-stop cases
stop at their declared injection point without manufacturing subsequent ticks.

Proposed engineering budget (not an acceptance threshold or measured limit):

| Quantity | Bytes / condition |
| --- | --- |
| Gross scratch recovery | 510, subject to whole-image measurement |
| Minimal admission overage | 367 |
| Arithmetic remaining if nothing else moves | 143 |
| Proposed additional live case state ceiling | 24 |
| Remainder after that state ceiling | 119, **not sufficient evidence of full fit** |
| Additional capture/injector/helper code | Must be measured per variant; currently unknown |

Do not promise a fitting suite from the 510-byte estimate. Admission requires
`actual resident end <= $C000`, protected content within its existing bound,
unchanged generated capacities/reserves, and independent stack accounting for
each variant. If R1/R2 plus the minimum capture skeleton still fail, stop before
more case implementation and return a measured section/symbol breakdown.

## R4: 352-byte case block inside the existing trace capacity

Frozen trace-v7 contract constants give:

`256 + (2 × 16 × 100 × 92) + 512 + (2 × 64) + (2000 × 16) + 4 = 327300`.

Capacity is 327680: **380 bytes guaranteed free**, not the 17100-byte patterned
tail observed with 955 physical world pairs. Preserve all 3200 tick records,
2000 maximum world events, both pool checkpoints, result and outer CRC.

Propose a new private generated format version and a 352-byte extension after
the actual world events, before the remaining patterned tail and outer CRC:

- Header: 28 bytes — magic 4; version, record size, slot count and used count
  (1 each); build/config digest prefix 16; selected case ID 2; mode and flags
  (1 each). Full SHA-256 identity stays in the host manifest.
- Eight fixed 40-byte slots: sequence 2; family/subcase/epoch/disposition 1 each;
  flags 2; tick 2; payload length 2; expected/observed codes 2 each; payload 24.
  Payload fields are case-specific generated definitions, including observed
  timestamps/check masks and before/after integrity values where applicable.
- Extension CRC32: 4 bytes. Total `28 + 8 × 40 + 4 = 352`.

Worst-case remaining tail is **28 bytes**. Unused slots have a specified checked
pattern, never fabricated observations. Case-record overflow rejects evidence;
never drop a case or shrink the world-event capacity. Extend writer, generator,
ledger and independent reducer together; reject old/new version mismatches,
missing/duplicate/reordered events, wrong build/case/epoch, invalid dispositions,
CRC damage and noncanonical padding. Retain all previous region CRC comparisons,
independent readback checks and outer fixed-residue verification.

Proposed live state maximum: 24 bytes (case ID, phase/status/sequence counters,
expected/observed disposition and bounded before/after check accumulators).
Derive exact generated layout before implementation. Serialize through existing
`record[92]` only after the current tick record is written, with no nested
transport use. Eight events allow up to four per epoch for one subcase; a subcase
needing more requires a separately identified variant, not capacity reduction.
Normal timing still includes the changed instrumentation. Do not suppress misses
or relabel an injected run's timing as an unmodified normal acquisition.

## R5: fail-stop evidence without reopening storage

Fatal G2-D/A/L cases must keep the real nonzero fault and lockout. They cannot
use the success-only terminal exporter. Preserve the existing 512-byte lifecycle
result and its CRC; do not repurpose its undefined bytes without a generated
contract. Add a separate versioned diagnostic screen record using the existing
post-quiescence display path and the no-longer-live 92-byte recorder workspace.

Proposed photographed record is 72 bytes: the same 28-byte identity header, one
40-byte terminal case slot and CRC32. Display all bytes in a fixed 9 × 8-byte
hex grid plus readable case/fault labels. Independently transcribe and reduce
it on the host; validate exact expected state, build identity, check mask, fault
and count. A summary photo alone is not enough. No KERNAL save, retry, resumed
workload or cleared fault is permitted to obtain this record. Expected injected
failure is suite evidence, never a normal-workload PASS.

Screen capture itself must be qualified under each admitted terminal state.
ROM/canonical-state restoration failure may make that path unsafe or unavailable;
record UNOBSERVABLE/NOT PROVEN and stop. Do not claim every corruption can be
reported. Those cases need a reviewed independent capture method before they
can be hardware-complete. Controlled storage errors use synthetic return-path
injection, not destructive media operations; physical electrical NMI is excluded.

## Authority, impact and first implementable change

Main Concept §§4.6, 5, 15.2–15.3 and 17; successor admission; generated PF,
MemoryAccessABI, lifecycle/export and trace contracts; and the approved Group 2
scope govern. R1 requires an explicit private scratch ownership/ledger amendment;
R4/R5 require private evidence schema changes. Public ABI and high-level memory
map are unchanged. No capacity, reserve or existing acceptance threshold changes.

At original design preparation, work was documentation only: registers/clobbers, memory, MAP/base-page,
DMA, timing and IRQ/NMI effects are non-applicable. Proposed implementation keeps
ordinary C ABI clobbers and PF hardware semantics, but changes resident layout,
call/stack costs and instrumentation timing. Prove these rather than inheriting
P09 timing. Fault capture is terminal-only after quiescence; original context
invalidation and export's no-return lifetime remain untouched.

**First bounded implementation:** R1 only, copied from P09 with a private generated
scratch contract and lifetime/alias host tests, then one fit build with the
unchanged minimal queue admission. Preserve source maps and failures. Require
exactly the expected BSS reduction and no protected-region growth; explain any
compiler/static-stack delta. If positive, implement R2 separately and measure it,
then admit the R4/R5 capture skeleton before adding per-subcase target injectors.
No carrier until all applicable fit/host/stack/timing and exact-name Xemu gates
pass. Physical run and delivery still require exact SD/chooser gates and owner
handling. Full Group 2 needs all case/variant results and owner review.

## R1 measured update — 2026-10-03

[Implementation and audit](../evidence/r0f/group2/2026-10-03-scratch-sharing/README.md):
510 BSS bytes recovered exactly, plus 15 text bytes in LTO main; resident end
$BF62, 158 bytes free. Protected, data, rodata and compiler static-stack sizes
unchanged. Actual-owner host tests pass 1484 poisoned handoffs under ASan/UBSan.
The old 143/119 estimates above are superseded for this minimal probe by 158/134
bytes (before/after the proposed 24-byte live state); extra capture code is still
unmeasured. R2–R5 are not implemented. No target execution or carrier.

## R2 and first capture measurement — 2026-10-03

R2 implemented in fresh source: 214 additional text bytes recovered, 372 free.
First empty capture skeleton: +769 bytes, end $C18D, 397 over. No live case
records/injectors yet; no target execution. [Retained breakdown](../evidence/r0f/group2/2026-10-03-encoder-capture/README.md).
The next bounded remedy reuses the existing tail traversal rather than adding
a second chunk encoder; preserve all CRC/readback checks. Owner has authorized
continued work toward hardware without serial approvals for these increments.

## Integrated traversal and first hardware subcase — 2026-10-03

The integrated empty encoder adds 253 bytes rather than 769: end $BF89,
119 bytes free. ASan/UBSan executes the actual tail statements in 403 cases,
including 0/1/955/1999/2000-world boundaries, transfer errors and corrupt readback.
All prior acquisition CRC and tail comparisons remain. It is an empty compile-only
skeleton, not a versioned runtime fault record.

Live queue trials add 1187, 1060 and 883 bytes over R2; all fail fit. The best
ends $C1FF, 511 bytes over, with the full 24-byte live state and dynamic record
framing. None executes. [Maps, source and commands](../evidence/r0f/group2/2026-10-03-capture-budget/README.md)
are retained. The 119-byte empty margin does not prove a fitting live suite.

Removing the startup-only admission probe from the R1/R2 control leaves 746 bytes
at $BD16. Its unchanged owner bodies reuse the host results; new PAL/NTSC normal
acquisitions pass at the existing thresholds. This supports a useful first
physical G2-L export-collision case with the existing independently checkable
terminal screen and returning SAVE. That subcase needs no additional injector or
v8 capture block; it does not close the other cases or resolve their fit/capture.
See the current [Build Intent](R0-F_GROUP2_BUILD_INTENT.md#first-bounded-hardware-case--2026-10-03).
P09 and all prior carriers remain untouched; no publication is authorized.
