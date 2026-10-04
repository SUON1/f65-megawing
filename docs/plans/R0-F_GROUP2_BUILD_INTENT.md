# R0-F Group 2 — Build Intent

**GROUP 2 WORK PACKAGE CLOSED — owner-approved bounded closeout, 2026-10-04.
Missing broader-suite proof is carried forward, not marked PASS.**
The first event-owner host slice is PASS and ready for review.
Prepared 2026-10-03 on `codex/r0f-group2-preparation`, from freshly fetched
`origin/main` = `abd3a0803b96090654db5dbdda43ad42d7b29a5a` (PR #13).
The preparation and follow-up revision requests authorize documentation only.
Owner response “Approved” on 2026-10-03 approves the revised actual event-owner
host-test first slice below. It supersedes the manifest-only increment. The
subsequent owner “Built it” authorized the host implementation; no target or
physical action was authorized by that host-only instruction. The later owner
selection “broader proposed fault/pressure suite” now approves the grouping
prospectively for hardware preparation. It does not recover historical approval.

## Scope provenance and missing decision

The [Group 1 intent](R0-F_GROUP1_BUILD_INTENT.md) records approval of a
three-group campaign on 2026-09-29, defines Group 1 normal combined-workload,
timing and returning-storage coverage, and keeps Groups 2 and 3 separate.
The [contemporaneous WIP excerpt](../evidence/r0f/group1/2026-09-30-presentation-integration/authority-checkpoint/WORK_IN_PROGRESS.md)
at lines 187–198 confirms that approval but supplies no Group 2 definition.
Targeted searches of current plans/reports, retained grouping references and
Git history (including the first integrated Group 1 checkpoint `2d9a42e`)
did not recover an exact Group 2 case allocation. The
[successor admission matrix](../reports/R0-F_SUCCESSOR_ADMISSION_RECONCILIATION.md)
defines remaining obligations, not their assignment to campaign groups.

**Scope decision resolved prospectively:** owner selected the broader proposed
fault/pressure suite after requesting hardware testing before publication. The
four families below now define this task. Historical allocation remains
unrecovered; this is a new explicit approval, not a historical reconstruction.
Neither the handoff nor unresolved Group 1 limitations adds other obligations.
Group 3 is not defined or reassigned here.

## Objective, authority and exact proposed scope

Answer this engineering decision: does the admitted private combined fixture
handle selected resource pressure and failures deterministically, preserve
protected state/services, and refuse invalid storage/resume/export success?
P09 has resolved the bounded physical resume/export blocker, making review of
the next campaign slice useful without replaying its passing acquisition.

Authority: [Main Concept v1.6](../../spec/core/F65_Main_Concept_v1.6_FINAL_HUMAN_REVIEWED.md)
§§4.6, 5, 15.2–15.3 and 17.6–17.8; the admission matrix's “Deterministic
overflow, fault, starvation and shedding” row and its referenced Gameplay,
candidate Runtime and subsystem requirements; the
[Group 1 matrix](R0-F_GROUP1_MEASUREMENT_MATRIX.md); and the
[development workflow](../DEVELOPMENT_WORKFLOW.md). Runtime remains candidate,
not FINAL. Subsystem policy must be read at the named authority before any
case implementation; missing policy is a decision dependency, not permission
to invent it.

Approved Group 2 scope is limited to these private-fixture case families:

| Family | Required observation / owner |
| --- | --- |
| Capacity and queue/pool pressure | Owning allocator/queue's existing full and one-over disposition; no silent growth, foreign-owner mutation or lost fault. Observer overflow is invalid evidence, not proof of allocator shedding. |
| Snapshot starvation / presentation shedding | Existing snapshot and presentation owners retain immutable complete publications and their specified drop/supersession behavior under bounded pressure. |
| Optional resource absence | Existing resource/audio owner follows an explicitly sourced fallback or failure policy while retaining protected-service obligations. |
| Storage and terminal failure lockout | Proof-platform/storage/export owners reject invalid context, guards/CRC, DMA/IRQ admission, sticky NMI, storage error or export collision; no false resumed/exported success, forbidden retry or overwrite. |

Before a case is admitted, record its requirement, exact owner API, stimulus,
expected disposition, protected-state comparison and evidence tier. Reuse
already satisfied cases. Missing behavior or policy stays unresolved; this
proposal does not authorize new production behavior to fill a test list.

Excluded: production renderer/model/audio/input features; public StorageService;
new capacities, reserves, ABI layouts, budgets or acceptance thresholds; general
optimization/style work; universal phase/high-water claims; SI calibration,
external input/audio latency, whole-ISR cost and electrical NMI timing. These
remain existing campaign boundaries, not automatically Group 3 assignments.
Full Group 1/R0-F acceptance, measured limits and Phase 1 are separate decisions.

## Reuse and preservation

- Reuse [actual P09 physical proof](../evidence/r0f/group1/2026-10-03-p09-physical/README.md):
  3200 records, twenty chunks, correct SAVE, 955 world pairs, five resumed
  services and integrity checks; zero nominal deadline misses, below-20-Hz
  cohorts or uncertain boundaries. This is bounded nominal evidence only.
- The [audio-readback report](../reports/R0-F_GROUP1_AUDIO_READBACK.md) and
  [frozen packet](../evidence/r0f/group1/2026-10-03-audio-readback/README.md)
  retain fit, sanitizer/policy/readback negatives, PAL/NTSC and collision proof.
  Reuse their recorded results without execution. Source authority is frozen
  copied input `build/r0f/group1/terminal-recovery/audio-readback-01/source-inputs/`
  and the packet's source/checkpoint identities, **not root working target code**.
- P09 PRG SHA-256 is
  `acc735f280f9d4e86b3b2040e5b2bed987908331f7899a87f5382c6cd23cd4d8`;
  resident end `$BFF5`, 11 bytes free: no expansion headroom. Canonical D81 SHA
  `bd1b645630c93d0ef764f3b6167924c0962ad67ed528d4ac8172ff2d4f9c5959`.
- Retain predecessor evidence under admission's stated boundaries. Prior
  negative cases establish only their recorded software/configuration tier.
  Never rerun, overwrite, rename or repair P09 or any earlier tested carrier.
  Preserve unrelated local SD backup/mirror work and physical evidence.

## Required changes and contract effects

Initial preparation changed this intent and compact WIP; this revision changes
only this intent. All hardware effects and
generated-artifact changes are **non-applicable**; no evidence is relabeled.
Proposed implementation ownership starts with host diagnostic tooling. Later
target work, if admitted, belongs to the existing subsystem/platform owners.

| Area | First host-only increment / later target admission requirement |
| --- | --- |
| Registers/clobbers | Non-applicable initially. Before target edits, enumerate actual touched registers and C/assembly clobbers against the frozen owner wrappers. No new register owner is selected here. |
| CPU-visible / physical memory | No target allocation initially. Preserve `$2001–$BFFF` resident, `$C000–$CFFF` software stack and generated lifecycle overlaps; `$058000–$05FFFF` remains read-only reserve. Stop target integration until a fresh fit proves room without reducing checks/capacities. |
| MAP/base-page | Non-applicable initially; preserve canonical B=2, port `$35`, protected MAP accessibility and restoration contracts. |
| DMA | Non-applicable initially; preserve drain/empty admission and exclusive storage ownership. Inject software conditions only through an admitted fixture, not unsafe live DMA. |
| Timing/deadline | Non-applicable initially; target instrumentation requires measured overhead and fresh changed-build evidence. Keep 100 Hz, 21-stage order, 20 Hz floor and existing failure/inconclusive rules. No invented service budget. |
| IRQ/NMI | Non-applicable initially; retain masking/restoration and sticky-NMI lockout. Simulated flags never establish electrical arrival behavior. |
| Interfaces / serialization | No change initially. Use generated successor, integration, export, trace, pool and presentation contracts; never hand-copy layouts. Any later private evidence extension needs its generator, decoder and ledger reviewed together. |

Inspected contracts include [successor](../../interfaces/r0f_successor_contract.json),
[export](../../interfaces/r0f_group1_export_contract.json) and
[pool observation](../../interfaces/r0f_group1_pool_contract.json), plus
[successor ledger](../../memory/r0f-successor-memory-ledger.json) and
[export ledger](../../memory/r0f-group1-export-memory-ledger.json).
Original context invalidation before resume and the separate no-return export
capsule remain mandatory. No integrity comparison may be removed to gain space.

## Validation gates and completion

1. **Preparation:** local link/path checks, `git diff --check`, focused diff
   review and baseline comparison. No passing campaign tests are replayed.
2. **First increment, after scope approval:** the focused actual event-owner
   host test specified below, with ASan/UBSan, exact frozen input hashes and
   explicit rejection/state-preservation assertions. A case manifest is navigation,
   not behavior proof. No target compile, fit experiment, emulator or carrier
   is needed for this step.
3. **Any later target increment:** fresh copied-source experiment with retained
   hashes; programming principles/C standard; fit/map/symbol/disassembly,
   generated consistency, memory lifetimes and stack checks before execution.
   Native sanitizers and independent normal/boundary/failure oracles must pass.
   Fit failure stops integration; propose a separately reviewed bounded remedy.
4. **Emulator:** once separately authorized for the admitted changed target,
   focused PAL/NTSC cases and independent actual result/trace/SAVE reduction;
   test failure lockout without destructive media behavior. Do not run P09.
5. **Carrier:** if a target carrier is later authorized, obey the
   [D81 gate](../../00_D81_LOADABILITY_GATE.md) and [workflow](../D81_WORKFLOW.md):
   fresh uppercase FAT 8.3 identity, one-session construction, independent
   structure/extraction checks, immutable canonical, fresh exact-name copies,
   two clean boots in each mode. No carrier name is allocated in preparation.
6. **SD / physical:** separate owner authorization, exact bytes, positively
   identified partition, independent one-extent and safe-eject proof, then exact
   chooser/entry gate before runtime tests. Record actual platform/video identity
   and independently reduce returned data. A physical case needs its own safe
   stimulus/capture protocol; no electrical NMI or destructive storage injection
   is implied. Host and Xemu results never substitute for physical evidence.

Preparation completes when this proposal and WIP are reviewable, preserving
all tested identities. Proposed Group 2 completes only when the owner-approved
case allocation has an auditable disposition for every case, all required
tiers and changed-configuration gates pass, and owner review resolves remaining
dependencies. Deferred/blocked cases cannot silently become PASS. Group 2
completion alone is not full R0-F acceptance.

Owner holds the original grouping decision, policy gaps, any target fit remedy,
SD/hardware authorization, publication, waivers, measured-limit approval and
acceptance. P09's successful nominal proof supplies none of these implicitly.

## Concrete case and evidence map — revision 2026-10-03

Paths below use **P** =
[the retained P09 source/evidence packet](../evidence/r0f/group1/2026-10-03-audio-readback/).
`P/source/` is the frozen copied-source tree; `P/host/` contains retained commands
and outputs, not newly executed results. Test filenames below are relative to
`P/source/tools/diagnostics/` unless a different prefix is given.

| Concrete case / requirement | Actual owner and existing test | Located proof and remaining gap |
| --- | --- | --- |
| Event queue full + one over; Main §15.2, admission deterministic overflow row | `P/source/src/diagnostics/r0f/combined_model.c:r0fc_event`; `r0f_combined_host_test.c` fills 64, rejects one more and checks count | [Foreground memory report](../reports/R0-F_GROUP1_FOREGROUND_MEMORY_EXPERIMENT.md) retains combined-corpus host PASS for its historical copied source. The test is also present in P, but P's `host/host-01/validation.json` does not record running that combined test. Its existing assertions do not establish rejection-flag plus complete queue/model preservation. **New proof: selected below.** |
| Snapshot exhaustion / held reader; admission snapshot ownership row | Same model's `r0fc_publish/acquire/release`; same combined test holds slot 0, fills 1/2, rejects another publication, checks held bytes and newest acquisition | Same historical host report; retained test located. No claim of fresh P09 exhaustion execution or universal starvation proof. Locating exact historical invocation/hash is evidence bookkeeping, not grounds to rerun the corpus. |
| Owner observation one-over, sticky first fault and counter overflow; Main §15.2 and high-water row | `group1_pool_owners.c:r0fg1_owner_sample`; `r0f_group1_owners_host_test.c` checks invalid owner, FACES capacity+1 and sample overflow without peer mutation | `P/host/host-01/owners-output.txt` and `validation.json` retain PASS. **Located/reuse**, but this proves observer rejection, not a geometry allocator's shedding policy. |
| Display DMA/copy failure, snapshot CRC fault, obsolete-view cancellation; admission complete-buffer/registration row | `successor_integration.c` display owner, extracted in `P/host/host-01/display_owner_under_test.inc`; `r0f_group1_display_owner_host_test.c` | `P/host/host-01/display-output.txt` and `validation.json`: PASS for DMA/copy retry, CRC fault 70, 26 cancellation boundaries and no obsolete swap. **Located/reuse**; mocked physical edges, not scanout proof. |
| Failed audio cache copy; admission optional resource/fault and protected audio rows | `combined_platform.c:cfaudio_begin/stop/service`; `r0f_group1_audio_owner_host_test.c` sets `copy_ok=0` and checks invalid cache/PCM off | `P/host/host-01/audio-output.txt` and `validation.json`: **located/reuse** for failed-begin observation. No subsequent service is called after failure. **Missing continuation proof**, distinct from choosing a production optional-resource fallback. |
| Resume clock/copy/DMA/restoration/NMI/IRQ failure; admission storage/resumed-service rows | Extracted actual resume/display/clock/DMA functions; root `tools/diagnostics/r0f_group1_resume_host_test.c` identified by retained command | `P/host/resume-host-02/validation.json`, `candidate/resume_under_test.inc` and `candidate/run.txt`: **located/reuse**, mocked edges. Not electrical NMI, arbitrary storage-device failure or every lifecycle case. |
| Terminal readiness rejection and first-fault policy; export contract admission | `group1_transport.c` extracted actual predicates + `group1_export.c`; `P/checkpoint/tools/r0f_group1_audio_readback_host_test.c`, readiness host/policy tests | `P/host/readiness-host-02/validation.json`, `transport-run.txt`, `policy-run.txt`: **located/reuse**, 18 integrity + 1280 audio-readback cases and 2624256 policy comparisons. Readiness is not a hardware fault-injection campaign. |
| Existing G1T00 collision preserves bytes, fails before trace export; export no-overwrite rule | Actual unchanged P09 program / terminal exporter, driven by `tools/diagnostics/r0f_group1_audio_readback.py negative-export` (historical command only) | `P/focused/export-failure-01/` actual files, operator summary and build identity; audio-readback report records S5/E03/F00 and SAVE preservation. **Located/reuse**, Xemu only; no new run. |

Actual returned P09 normal acquisition and integrity evidence remains in the
[physical packet](../evidence/r0f/group1/2026-10-03-p09-physical/README.md).
It does not turn any of the above synthetic failure cases into physical proof.

Three dispositions must stay distinct:

1. **Evidence location:** the concrete retained records above resolve several
   initially unspecified gaps. The historical combined-corpus exact command/hash
   still needs locating if that older run is cited as configuration-equivalent
   evidence; test source presence alone is not a PASS record.
2. **New test:** event rejection's observable flag and state-preservation
   properties are not asserted by the inspected queue test. Audio failed-copy
   continuation is another untested sequence in the inspected audio corpus.
   These are bounded findings, not a claim that all historical tests were searched.
3. **Owner decision:** Group 2 allocation remains proposed. Inclusion of a case,
   broader optional-resource fallback policy and any target fix require their
   own authority. Nothing here assigns Group 3 or promotes a diagnostic limit.

Static audio finding: the retained `cfaudio_service()` non-warning branch can
write `$D720=$E2` when `pcm_on=0`, without testing `audio_cache_valid`. The retained
failed-copy stub returns false without setting `cffault`, whereas real `cfcopy()`
sets fault 21/22. A future continuation test must reproduce the real failure
side effects and inspect caller lockout/reachability before alleging an integrated
failure or prescribing a fix. No such test was run here; no audio change is
included in the first increment.

## Smallest first implementation increment — actual event-owner proof

**Proposed test:** `tools/diagnostics/r0f_group2_event_owner_host_test.c`, with a
small isolated host runner. This is a new path to create only after scope approval
and a subsequent implementation instruction. Its requirement is Main §15.2's
observable deterministic overflow without silent allocation or foreign mutation;
the existing private API returns 0 and latches `model.rejected=1` on rejection.
No new policy is needed to check that implementation contract.

Compile/link the actual frozen `P/source/src/diagnostics/r0f/combined_model.c`
with its frozen `combined_model.h` and generated `r0f_combined.h`, using a host
compiler, strict warnings and ASan/UBSan. Compile without `R0FG1_INTEGRATION`
for this isolated model API; `r0fc_event` itself has no conditional branch for
that macro. Do not substitute a rewritten queue model or test an observer.
Record input hashes, exact command, sanitizer output and assertion results in
new host-only output. Keep all frozen inputs read-only.

The focused sequence is:

1. Initialize the complete model object (including padding before reset) and
   a separate peer model deterministically. Fill through generated
   `R0FC_QUEUE_CAPACITY-1`, then accept the final legal event. Check order,
   count and high-water against independently constructed expected values.
2. At capacity, submit one additional **valid** entity ID. Require return 0,
   count and high-water unchanged, all queued bytes unchanged, `rejected=1`,
   and every other model byte unchanged. Compare to a saved model copy with
   only the expected rejection field set; verify the peer model is unchanged.
3. Repeat rejected submissions with valid IDs to verify sticky observable
   rejection and no cumulative mutation. Separately submit invalid IDs 9 and
   255 to a non-full initialized queue so range rejection cannot be masked by
   fullness. Require the same no-mutation-except-rejection disposition.
4. Check reset clears the rejection state and permits a legal enqueue again.
   Do not grow capacity, alter production state/layout or invoke target ticks
   to manufacture a different pressure policy.

The old full/count assertion is partial reusable coverage. The new test earns
only the additional actual-owner flag, queue and peer/model preservation proof;
it does not establish integrated timing, storage continuation, allocator shedding
or physical behavior. A manifest validator cannot supply those assertions.

**Completion of this increment:** assertions and sanitizers pass against the
identified frozen owner, or a precise failing assertion and inputs are retained
for review. A failure completes diagnosis only, not behavior proof, and does not
implicitly authorize modifying the owner. No target fit recovery, target build,
Xemu, SD/carrier or hardware action is part of this increment. P09's 11 resident
bytes remain unavailable as expansion headroom. The owner approved this first
host-test slice on 2026-10-03; the historical allocation remains unrecovered.
Implementation and the focused sanitizer run are complete. See the
[event-owner host proof](../evidence/r0f/group2/2026-10-03-event-owner-host/README.md)
for 71 accepted / 17 rejected calls, unchanged frozen inputs and exact commands.
Only this first slice has completed proof; broader scope is now approved but
not implemented or validated.

## Owner sequencing — hardware before publication

Owner requested hardware testing next and no commit/push until Group 2 is
finished. This supersedes publication as a possible immediate next action;
completion still does not by itself authorize publication. The host slice is
complete, but it supplies no target program or carrier.

Owner selected **the broader proposed fault/pressure suite**. This resolves the
scope choice prospectively. A dedicated event-owner target alone is insufficient.
Group 2 completion requires dispositions for all four approved families and their
required host, changed-target, emulator and physical evidence. Group 3 is not
inferred. No existing carrier is to be replayed.

## Hardware preparation: concrete cases and admission gates

| Case | Actual owner / stimulus | Required outcome and boundary |
| --- | --- | --- |
| G2-Q: event queue pressure | Frozen `r0fc_event`; capacity, one-over, invalid owner and repeated rejection | Existing rejection flag/return; queued data, count, model and peer preserved. Reuse completed host proof; add corresponding target evidence. |
| G2-S: snapshot starvation | `r0fc_publish/acquire/release`; hold reader, fill other slots, attempt another publication, then release | No held-data overwrite; skipped publication observable; no partial publication; newest complete acquisition. Bounded case, not counter-wrap or universal starvation claim. |
| G2-P: presentation pressure | `r0fg1_anchor_add`; four retained anchors plus worse/better ranked candidates, then superseded view and incomplete generation | Existing priority/handle order and counted shedding; complete matching buffer/registration only. Observer full samples do not substitute for this owner behavior. Reuse existing presentation tests where exact identity applies. |
| G2-D: failed display work | Actual display owner; failed DMA/copy and damaged held snapshot through isolated injection seam | No partial/obsolete swap; existing bounded retry or CRC fault disposition; displayed generation protected. Never submit intentionally unsafe DMA to hardware. |
| G2-A: unavailable audio resource | Actual `cfaudio_begin/service` plus caller fault handling; failed sample copy with real fault 21/22 side effects | Establish actual lockout/reachability before judging later service calls. Preserve invalid-cache state and protected-service obligations. An invented fallback or production audio policy is excluded; a conflict requires owner disposition. |
| G2-L: lifecycle/export failure | Actual admission and orchestration; guard/CRC or admission rejection, controlled storage error, export collision | No false resume/export success, retry or overwrite; original-context invalidation and separate terminal capsule unchanged. Never corrupt the card or physically induce unsafe DMA/NMI. Each fail-stop case needs its own capture path. |

These are bounded cases within the approved families, not a new production
checklist. Preserve the existing retained-evidence map above. Locate and reuse
passing cases before adding tests; close only genuinely missing properties.

**First local increment: target admission, before a carrier.** From a fresh
copy of the qualified P09 source, identify injection seams and case-result
ownership. Account for actual resident code/data, stacks, trace capacity and
lifetime overlays. Select only an arrangement that retains the complete required
combined workload, every integrity check, generated capacity and timing gate.
P09 ends at `$BFF5`; no new code is admitted merely because 11 bytes remain.
If the suite cannot fit, retain the failed admission and present a concrete
bounded space remedy for review. Do not silently substitute standalone tests
for combined-load proof or create new MAP/overlay semantics to make it fit.

Before target edits, record exact register/clobber and memory effects for the
selected seams. The owner APIs are foreground C; their eventual wrappers may
touch audio/display, DMA, clock or lifecycle state. No new register, MAP/base-page,
IRQ/NMI or physical-memory ownership is approved by this case list. Preserve
canonical restoration, exclusive storage/DMA ownership, reserve integrity and
existing timing thresholds. Current documentation changes have none of these
hardware effects and change no generated artifact.

**Capture admission:** versioned private case IDs, expected/observed disposition,
protected-state checks, build identity and complete-case accounting must survive
each test. Expected injected faults must be distinguishable from harness faults.
Fail-stop cases must not require violating lockout to export their result; define
a bounded independently checkable screen/result capture before implementing
those cases. Never call a successful summary alone full-suite acceptance.

After admitted fit and focused actual-owner host checks, qualify changed-target
behavior in PAL/NTSC, then construct a fresh uniquely named carrier using the
existing D81 gates. No carrier name or SD write is selected in this preparation.
Hardware runs follow exact SD hash/one-extent/eject and chooser/entry gates, with
actual configuration and captured results independently reduced. Hardware test
intent does not select a raw-card write method; the owner retains delivery choice.

**Completion:** every listed case has traceable actual-owner evidence at the
required tier, every retained result keeps its original limits, unresolved policy
or fit issues have explicit disposition, and the owner reviews the full suite.
A host-only, standalone-only or partially captured suite is not Group 2 finished.
No commit/push until Group 2 is finished, and no automatic measured-limit or
full R0-F acceptance follows.

## Target admission result — 2026-10-03

Owner “Build it” authorized the target-admission increment. The minimal queue
probe passed its focused host test, but the complete copied P09 image plus
probe ends at `$C16F` (378 bytes growth, 367 bytes over the resident ceiling).
See [retained admission and proposed bounded remedy](../evidence/r0f/group2/2026-10-03-target-admission/README.md).
No target execution, carrier, SD/hardware or publication occurred. Proceed only
after review of the named outlining remedy; this is not complete-suite fit.

## Approved outlining trials — 2026-10-03

Owner “Build it” approved the two proposed compile-only outlining experiments.
[Both failed to recover space](../evidence/r0f/group2/2026-10-03-outline-trials/README.md):
`cfframe_wait` saves zero; separate `cfratio` adds 503 bytes, including three
compiler static-stack bytes. Neither advances to execution. Group 2 remains
blocked pending a newly reviewed bounded space remedy; no additional compiler
trial, reserve borrowing, workload reduction or publication is implied.

## Concrete redesign for review — 2026-10-03

The [size and capture redesign](R0-F_GROUP2_SIZE_CAPTURE_REDESIGN.md) proposes
private scratch sharing, common PF request encoding, per-subcase full-workload
builds and a 352-byte generated evidence block. The first implementation is
bounded to scratch ownership/lifetime proof and measured fit. Gross savings
and capture arithmetic are not target qualification; no implementation was
performed under the redesign request. Review the explicit private ownership
and schema amendments before applying them.

## R1 scratch sharing implemented — 2026-10-03

Owner “Build it” authorized the first bounded redesign increment. The
[retained R1 evidence](../evidence/r0f/group2/2026-10-03-scratch-sharing/README.md)
records actual-owner host PASS (1484 poisoned handoffs, ASan/UBSan) and one
compile-only fit PASS at $BF62 / 158 bytes remaining. BSS shrinks exactly 510
bytes; LTO main shrinks another 15. Protected and static-stack sizes are
unchanged. This is a fresh copied-source minimal-probe experiment. Full-suite
fit and target execution remain unproven; no carrier or publication occurred.
Next bounded implementation is R2 factoring, then capture-skeleton admission.

## Continued hardware preparation — 2026-10-03

Owner approved proceeding toward hardware without routine per-increment
approval pauses. R2 host/fit passes; the first empty capture skeleton fails fit
by 397 bytes. [Evidence and next concrete remedy](../evidence/r0f/group2/2026-10-03-encoder-capture/README.md).
No target/carrier admission follows a failed fit. Continued bounded capture
implementation is authorized; public ABI, capacities, reserves, policy choices,
raw SD delivery and publication boundaries remain as stated above.

## First bounded hardware case — 2026-10-03

The owner's continued approval authorizes local qualification and a first useful
physical subcase without serial routine approval pauses. It does not change the
broader suite's completion condition. Integrated empty capture fits (119 bytes
free; 403 host boundary/error cases), but the best live queue/case capture still
fails by 511 bytes. See [retained capture budget](../evidence/r0f/group2/2026-10-03-capture-budget/README.md).
Neither draft executes or becomes an admitted version-8 trace.

**Selected case: G2-L-EXPORT-COLLISION.** The existing terminal export owner must
reject an already present `G1T00`, preserve every pre-existing payload, write no
trace chunks, and halt with `S:5 E:03 F:00`. A fresh disk's pre-existing `G1T00`
contains the bounded TOKEN fixture; it is not a damaged trace or SD error. The
real SAVE error path is exercised after the full combined workload, with no
target injector, fault clearing, storage retry or return from terminal ownership.

The new R1/R2 control removes the startup-only queue probe. Resident end is
$BD16, 746 bytes free; protected bytes and static-stack allocation are unchanged.
Exact tested R2 owner bodies reuse 1484 sanitizer handoffs and 256 encoder cases.
New NTSC/PAL control acquisitions independently validate all 3200 records,
twenty chunks, SAVE, capacities and nominal timing. Queue proof is not inherited
from this control. Source is a new frozen copy derived from P09, never the root
working target or a replay of P09.

The case adds no target code, resident data, register/clobber, MAP/base-page,
physical-memory, DMA, timing or IRQ/NMI effects beyond the qualified R1/R2 control.
Existing terminal KERNAL clobbers, capsule lifetime and no-return ownership remain
the governing contracts. The private scratch header is generated from its contract
in the copied source; no public layout/capacity/reserve changes. Trace remains v7.

**Hardware gates:** fresh `R0FG2L2.D81`, independent host structure/extraction,
two clean NTSC and two PAL disk boots with no PRG injection, expected actual
collision/status/SAVE and readable screenshot; then exact SD bytes, one FAT32
extent, safe eject and physical chooser/entry. The program's identity banner
is `R0FG2C1` (the normal control); the disk fixture identity is `R0FG2L2`.
Retain the mistaken L1 visual stop and its correction; do not retest L1.

**Bounded physical completion:** identified chooser/entry and terminal photo,
`S:5 E:03 F:00`, and independently checked returned-card structure, unchanged
four inputs plus the correct 34-byte `RSSTATE`, with no extra trace files.
The SAVE is only the pre-storage checksum fixture. It cannot establish the
512-byte lifecycle result, full resumed-service state or physical timing.
Use the [case handoff](../evidence/r0f/group2/2026-10-03-export-collision/README.md)
and read-only returned-file checker; never promote its file checks alone to
physical runtime proof. Other G2-L failures and G2-Q/S/P/D/A remain open.

**Next implementation:** resolve the live case/capture fit and admit its complete
generated schema plus independent reducer before execution; then qualify the
smallest missing owner case under the combined workload. Do not change capacities,
borrow reserves or invent a fallback. Policy conflicts still require the owner;
delivery choice, suite acceptance, measured limits and publication stay separate.
No commit or push until Group 2 is finished.

## SD delivery handoff — 2026-10-03

The owner-run raw audit of the Finder copy `R0FG2L2.D81` passes exact bytes,
hash and uppercase short name but reports **39 FAT32 extents**. The SD copy is
`INVALID — DO NOT USE`; no physical chooser/runtime test is authorized for it.
Retain it unchanged alongside the original valid host/Xemu release and failed
audit attempts. See the [allocation failure](../evidence/r0f/group2/2026-10-03-export-collision/sd-finder-01/allocation-failure.json).

The concrete proposed delivery recovery is `R0FG2L3.D81`, identical four disk
payloads and PRG, fresh construction and repeated host/exact-name Xemu gates,
then the owner-executed pinned contiguous allocator. Current eight input hashes
match the retained CAP14 qualification; reuse it. The replacement identity and
raw delivery method still require explicit owner authorization under the D81
gate/workflow. No replacement, target change or SD write is made here. Evidence
and WIP edits have non-applicable register/clobber, CPU-visible/physical memory,
MAP/base-page, DMA, timing/deadline and IRQ/NMI effects. Publication remains held.

## Physical procedure refinement — 2026-10-04

The [bounded hardware test](R0-F_GROUP2_HARDWARE_TEST.md) specifies one owner
run, exact chooser/entry evidence, readable S5/E03/F00 photo and actual
returned-card payload/SAVE checks after a qualified delivery. It introduces
no target code, observation timeout threshold or replacement carrier.
Read-only inspection of all four retained L2 memory dumps locates existing
first SAVE failure proof at Xemu tier. Physical photos/SAVE alone cannot
distinguish the shared initialization/SAVE error handler or count attempts.
Observable terminal rejection and preservation remain the bounded physical
objective; strict physical call-stage provenance requires a separately qualified
observation if needed for broader closure. Delivery authorization is unresolved.

## L3 construction authorization — 2026-10-04

Owner instruction: "Build the working R0FG2L3.D81". This authorizes the fresh
replacement identity, single-session construction and required independent
host/four exact-name Xemu gates using the unchanged qualified program and four
collision payloads. Retain L2's allocation failure and all prior tested images.
This isolates identity while addressing the proven allocation layer separately;
it is not a program/content fix. No new compile is needed for identical PRG bytes.
Host controller v5 selects L3 and is separately frozen/pinned; earlier controller
and evidence records remain unchanged. No target register/clobber, memory,
MAP/base-page, DMA, timing/deadline, IRQ/NMI or generated-contract change.
Raw delivery choice/write, physical run and publication remain separate.

## L3 local qualification result — 2026-10-04

[L3 qualification](../evidence/r0f/group2/2026-10-04-l3-carrier/README.md)
passes fresh construction, independent structure/extraction, exact four-payload
comparison and two clean NTSC/two PAL ordinary disk boots. Canonical is 819200
bytes, SHA-256 c3df1ceda3979cf6e49e7885b563555379c7d64557360bed0d288144085092e5,
state XEMU_BOOT_VERIFIED. Every run supplies readable S5/E03/F00, unchanged
inputs, correct SAVE and full lifecycle checks at Xemu tier. Protected state
locates first SAVE failure; the physical call-stage limit remains unchanged.
The existing read-only checker passes L3's actual new PAL post-run image.

The original combined PRG/freeze/host acquisitions are reused without recompile
or replay. Bootstrap regeneration is byte-identical. New image bytes differ
from L2 only in its disk-label identity; this is not an allocation/content fix.
Failed L2 and prior evidence remain untouched. The concrete owner CLI proposal
is prepared from the verified release and matching retained allocator
qualification. SD write/method and actual physical gates are still owner-held;
Group 2 remains incomplete and publication remains held.

## L3 physical acquisition — 2026-10-04

The [physical packet](../evidence/r0f/group2/2026-10-04-l3-physical/README.md)
retains owner-confirmed L3 selection/ordinary entry, expected red S5/E03/F00
photo and a fresh actual returned-card snapshot bound to the live removable
FAT32 UUID. The existing read-only checker passes structure, all four unchanged
inputs, correct 34-byte RSSTATE and no extra chunks. No target build/execute,
SD write or prior proof replay occurred during acquisition/checking.

Observable rejection/preservation results pass; formal bounded-case closure
and complete release chain remain pending operator record. Safe ejection and
one-run/no-restart are unconfirmed, chooser photo absent, actual configuration
UNKNOWN. Do not rerun to fill these gaps. Physical call-stage/attempt count,
full lifecycle and timing remain unproven. Broader cases, live capture fit,
schema/reducer and owner decisions remain open; publication remains held.
Evidence-only register/clobber, memory, MAP/base-page, DMA, timing/deadline
and IRQ/NMI effects are non-applicable; generated contracts are unchanged.

## Owner-requested wrap-up review — 2026-10-04

Owner requested wrapping Group 2 ahead of a new flight simulation supplement
and another development-plan review. The [closeout proposal](../reports/R0-F_GROUP2_CLOSEOUT_REVIEW.md)
reconciles existing case evidence, locates historical snapshot owner proof and
lists the exact missing host/combined-target/emulator/physical obligations.
No passing proof is rerun. Recommended bounded work-package closure carries
those obligations explicitly into that review, without promoting them to PASS.
It requires owner approval because it changes the broader completion condition
above; approval is not inferred from the wrap-up request. Full R0-F acceptance,
measured limits, Phase 0 exit/Phase 1 entry and publication remain separate.
The new supplement is not yet supplied/ingested. No target/code, generated
contract or hardware effect changes are made by this review.

## Approved bounded closeout — 2026-10-04

Owner: “approved: bounded closeout and carrying the listed gaps into that review.”
This explicitly approves the [closeout disposition](../reports/R0-F_GROUP2_CLOSEOUT_REVIEW.md)
and supersedes this work package's earlier full-suite completion condition.
Group 2's current package is closed as bounded Phase 0 evidence. All six rows'
listed missing proof, audio continuation, live capture fit/schema/reducer and
L3 operator/configuration gaps remain explicit carry-forward items for the
new flight-supplement/development-plan review. Results are not relabeled PASS;
the successor overflow/fault/starvation/shedding admission row remains OPEN.

The [separate owner decision](../evidence/r0f/group2/2026-10-04-closeout-review/owner-disposition-01/decision.json)
preserves approval without rewriting the earlier review or physical evidence.
Historical Group 2 allocation remains unrecovered; Group 3 is unassigned.
Full R0-F acceptance, measured limits, Phase 0 exit/Phase 1 entry and publication
are not granted. No new instrumentation campaign is part of this closed package.
The supplement is not supplied/ingested. No code/generated or hardware effects;
register/clobber, memory, MAP/base-page, DMA, timing and IRQ/NMI are non-applicable.
