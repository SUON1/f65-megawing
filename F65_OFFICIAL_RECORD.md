# F-65 Megawing Official Project Record

This file is the primary status and configuration index for the project. It does not replace the preserved specifications or approve draft material.

## 1. Project identity

| Field | Current value |
|---|---|
| Project | F-65 Megawing |
| Target platform | MEGA65 |
| Production target language | LLVM-MOS C primary; selective 45GS02 for admitted platform-critical or measured work |
| Host tooling and reference models | Java |
| Repository | `f65-megawing` |
| Branch | `main` |
| GitHub remote | `https://github.com/SUON1/f65-megawing.git` (private) |

## 2. Specification authority

The exact machine-readable record is [`spec/manifests/spec-corpus.json`](spec/manifests/spec-corpus.json).

| Exact filename | Version | Declared status | SHA-256 | Authority and current state | Repository location |
|---|---|---|---|---|---|
| `F-65_Technical_Alignment_and_Read_First_Supplement_v1.0.md` | 1.0 | APPROVED — FIRST-READ AUTHORITY | `f957b97e146fc4d35d094072eee52d2cc91185f76c7cef232efe898ce7628cc7` | Approved orientation and configuration control; does not approve parent candidates | `spec/alignment/F-65_Technical_Alignment_and_Read_First_Supplement_v1.0.md` |
| `F-65_Architecture_Decision_AD-001_R0_Program_Development_Authorization.md` | 1.0 | APPROVED — R0-A–F DEVELOPMENT AUTHORITY | `ce3cb019082081bb7908146de0cc689a74abca517bf32520f5bd9fdf30e375dd` | Development authorization only; it does not pass any R0 gate | `docs/decisions/F-65_Architecture_Decision_AD-001_R0_Program_Development_Authorization.md` |
| `F-65_Specification_Approval_Record_2026-08-20_R0_Development.md` | 1.0 | APPROVED — ACTIVE | `9fc23bb8555bbd2b84c8f925e909bc5245448ee87db9fb1fb596e8e67c288d8e` | Records the human approval scope and exclusions for Read-First v1.0 and AD-001 | `docs/approvals/F-65_Specification_Approval_Record_2026-08-20_R0_Development.md` |
| `F-65 Megawing Revision 1.5.1 — Architecture Invariants.md` | 1.5.1 | Architecture-freeze candidate | `46ba078cb397d257de6aeee66cff510c5e3243bca97767db1738d86d9ebd1fec` | Highest current architecture candidate; Revision 1.4.1 remains the last frozen baseline | `spec/architecture/F-65 Megawing Revision 1.5.1 — Architecture Invariants.md` |
| `F-65 Megawing Revision 1.4.1.md` | 1.4.1 | Frozen architecture baseline | `c54f77c817b8263f8d03de3ed442c115ff06b0b622c1f14be122df8963079922` | Last frozen architecture baseline retained for context and preserved contracts | `spec/architecture/F-65 Megawing Revision 1.4.1.md` |
| `F65_Gameplay_and_Simulation_Requirements_Supplement_Draft_0.2.md` | Draft 0.2 | Freeze candidate | `5db0344f8e7fd66143874310c3794a64391d4767229a90f5caee5e5e287d84e4` | Candidate player-facing requirements; not an approved production baseline | `spec/gameplay/F65_Gameplay_and_Simulation_Requirements_Supplement_Draft_0.2.md` |
| `F-65 Engine Runtime and Toolchain Design Supplement Draft 0.2.md` | Draft 0.2 | Architecture-review candidate | `dfd4bf0b557b4dae6382de502db42e4b2d269ceaf44bd67440bb6d047341454a` | Candidate implementation contract subordinate to Architecture and Gameplay; not approved | `spec/engine/F-65 Engine Runtime and Toolchain Design Supplement Draft 0.2.md` |
| `F65_Engine_Runtime_and_Toolchain_Design_Supplement_Draft_0.1.md` | Draft 0.1 | Historical architecture-review candidate | `63f0d2e136507485296bd3424e83e9db796b2bf612d81f3fe5ac2744297d27aa` | Preserved historical provenance; superseded as the current candidate by Engine 0.2 | `spec/engine/F65_Engine_Runtime_and_Toolchain_Design_Supplement_Draft_0.1.md` |
| `F-65_Technical_Alignment_and_Corrections_Supplement_v0.2.md` | 0.2 | Historical/superseded draft | `fd8188f3787d902466a3d07b13c46e88f9afe32d7d5839945c4bc33143e0249b` | Preserved historical orientation/audit; Read-First v1.0 is the current approved operating alignment | `spec/alignment/F-65_Technical_Alignment_and_Corrections_Supplement_v0.2.md` |

Current precedence is:

1. Approved Read-First v1.0 governs orientation and configuration control.
2. Approved AD-001 governs whether bounded R0 proof work may be developed now.
3. Architecture 1.5.1 remains the highest architecture candidate; Revision 1.4.1 remains the last frozen baseline.
4. Gameplay 0.2 remains a freeze candidate and Engine 0.2 remains an architecture-review candidate; neither is silently approved.
5. Engine 0.1 and Alignment 0.2 remain preserved historical provenance.

Revision 1.4 is referenced as superseded and retained by Revision 1.4.1 but was not supplied. Its filename, contents, and hash are unknown. Nothing in this repository resolves or reconstructs it.

## 3. Current engineering state

R0-F platform development (2026-09-17): the owner approved the additive
proof-platform work and required Xemu before native-blank SD delivery.
PF-001 now implements reset-only canonical entry, a resident raster IRQ with
register canaries, bounded real DMA copy and actual PCM playhead/stop probes.
Host/target checks pass; normal-speed Xemu observed those primitives passing.
Current exact evidence and limitations: `docs/reports/R0-F_PLATFORM_HANDOFF.md`.
**The full combined calibration/workload carrier is not built or delivered.**
The reversible ROM-reclaim contract, calibrated workload, complete service
integration and full measurement matrix remain open. No SD write/eject, D81
packaging, physical run, gate acceptance, commit or push in this increment.
F65BLK01 was read-only observed at 688128 bytes (ineligible); F65BLK02 at
819200 bytes (size only, not yet content/extent verified). Both are untouched.

R0-F combined-build request (2026-09-17): host clock-source preflight code is
built and tested; **the combined target is not built**. The pinned source-model
comparison of F5 raw data does not supply independent calibration or SI units.
Existing admission prohibits public-ABI changes, while combined IRQ/DMA/PCM
and canonical startup contracts are missing or explicitly unverified/deferred.
`docs/reports/R0-F_COMBINED_PLATFORM_ADMISSION.md` records the bounded
cross-interface review required before target integration. No target, D81,
SD, or existing evidence bytes changed in this increment. No new Xemu or
physical run; the full-closure direction and all unpassed gates are unchanged.

R0-F5 physical intake (2026-09-17): owner supplied the summary and all 22
one-based capture pages. Originals, visual summary and matching pre/post SD
hash/one-extent records are retained in
`docs/evidence/r0f/capture/physical/REVIEW.md`. Acquisition-complete and
inherited functional PASS are observed. Subsequent image-only transcription
with recorded visual corrections passed all 22 page CRCs, full CRC 8D78FBC0,
and the unchanged Java validators (2640 samples, 80 spans, 198 corruptions
rejected). The physical raw-count capture is validated, not calibrated time.
Subsequent owner Terminal output confirms matching SD bytes, one unchanged
extent and successful safe eject for F5. No R0-F acceptance or release-state
promotion.

R0-F capture implementation (2026-09-17): RC-1 screen transport is built as
F65R0F5.D81. Host/static and independent Java capture checks passed; the fresh
carrier passed structural/content gates and two clean exact-image Xemu boots
with inspected screenshots. Handoff: `docs/reports/R0-F_CAPTURE_HANDOFF.md`.
This adds a post-acquisition read-only viewer/importer, not calibrated timing
or the full combined workload. No SD/hardware test is requested yet. F4/F2
remain unchanged. Full R0-F and measured limits remain open.

R0 full-closure direction (2026-09-17): the owner selected option 1, completing
the full R0 proof program on the current design. The archive option was not
selected. `docs/plans/R0_FULL_CLOSURE_WORK_PLAN.md` tracks clock/capture,
protected-workload and combined-harness reconciliation, implementation, Xemu,
and corresponding hardware acceptance. This resolves the direction question
below, not a gate or a hardware-wrapper contract. The displayed core prefix
has been resolved to an official source commit; installed binary provenance
and calibration remain open. No new target/carrier build in this kickoff.

R0-F evidence review (2026-09-17): owner photographs now show F65R0F4
acquisition complete, inherited functional PASS, all requested phase masks,
and platform display identities (R6, ARTIX B5C770C6, ROM V920413, NTSC).
Original photos and raw-count transcription are retained under
`docs/evidence/r0f/cia-timing/physical/`. Physical raw-data reduction, exact F4
SD delivery chain and calibrated timing remain unverified. The host release
manifest remains XEMU_BOOT_VERIFIED; it is not retroactively promoted.
`docs/reports/R0-F_CLOSEOUT_REVIEW.md` identifies a scope gap: the accepted
R0-E bounded proxy and its F4 timing do not satisfy the full combined-service
R0-E/F requirements under AD-001. Owner direction is needed on continuing that
full proof program versus archiving this bounded experiment with gates open.
No scope waiver, gate acceptance, new build, SD operation, commit or push was
performed by this documentary review. Historical updates below describe the
evidence available at their respective handoff times.

R0-F CIA-count measurement build (2026-09-17): the new reset-only diagnostic
times 2,640 inherited fixture ticks in 80 phase-started cohorts, retains raw
durations/lateness and frame cross-checks, and has independent Java validation.
Fresh F65R0F4.D81 passed host structural/content checks and two clean Xemu boots,
with Java-validated raw captures and visually inspected screenshots. Current emulator and
release results are in `docs/reports/R0-F_CIA_TIMING_HANDOFF.md`. Units remain
raw CIA counts, not calibrated time; physical evidence and full R0-F acceptance
remain open. Private wrapper/state decision: `R0-F_CIA_TIMING_CONTRACT.md`.
No production ABI, memory ownership, reserve, DMA or interrupt-service change.

R0-F startup correction (2026-09-17): the proof-specific link now excludes the
unused SDK character-set initializer that caused `R0F-STATIC-STARTUP-001`.
F65R0F2.D81 passed bounded host/static, D81 structural/content checks, and two
fresh pinned Xemu boots. Both screenshots and result blocks were verified.
The owner subsequently supplied matching SD hash/extent records and a physical
photo showing F65R0F2 startup-fix identity, functional PASS and 80 valid samples.
The owner reported Finder crashed during eject; safe eject is NOT VERIFIED,
not PASS. Full R0-F
measurements and acceptance remain open. See `docs/reports/R0-F_STARTUP_FIX_HANDOFF.md`.

R0-F Step 3 audit (2026-09-16): native host validation and compile/link pass;
static acceptance is BLOCKED by `R0F-STATIC-STARTUP-001`. Linked startup calls
KERNAL $FFD2 after setting B=$02 without the separately required thunk. The
private ledger now accounts for 107 bytes of existing compiler static-stack
storage. The target PRG is unchanged. Prior Step 2 completion wording was
corrected: the bounded proxy contract does not complete the calibrated R0-F
measurement contract. See `docs/reports/R0-F_STEP3_AUDIT.md`.

R0-F update (2026-09-05): the owner-directed first bounded functional/raster
test slice is implemented and compiled with pinned LLVM-MOS. Native C tests
and fresh F65R0F1.D81 host structural/content gates passed. Two clean Xemu boots
of the exact carrier passed after locating the pinned runtime in the owner's other
checkout; SD-native transfer hash/extent/safe-eject passed and owner-reported
hardware chooser/runtime was observed on MEGA65.
See `docs/reports/R0-F_BUILD_HANDOFF.md`. This does not complete the full
R0-F measurement contract or change any approved limits or production authority.

R0-A and R0-B are closed bounded proof milestones and R0-D is closed for its
accepted calibration-proof scope; their accepted evidence is retained in their
handoffs and evidence maps. R0-C remains a bounded proof candidate completed
under its recorded owner waiver, not a formal R0-C gate pass. R0-E is closed
for its owner-accepted bounded combined-load functional-proxy and read-only
raster-observation scope: `F65R0EG.D81` was delivered through a verified
one-extent MEGA65-native slot, mounted, and loaded its physical Rev3 result
screen. Its DMA hardware probe remains `DMA_HARDWARE_PROBE_NOT_EXECUTED`; its
raster values are raw modulo-256 line deltas, not CPU-cycle, latency, or
physical-limit measurements. R0-F timing/DMA/IRQ measurement and platform
identity remain pending. None of these facts passes R0-F, a measured-limits
gate, or any candidate specification. Autonomous full-game production remains
unauthorized. The repository does not authorize production flight, radar,
weapons, tactical AI, campaign, audio, gameplay, or production-renderer code.

Draft, proposed, `TBD`, `TARGET`, and `R0-GATED` material remains exactly that until the named human or measurement gate changes its status.

## 4. Current authorized milestone: R0-F physical measurement evidence

The owner selected full closure on the current design. Reconcile the current
bounded admission with the full combined-harness requirements under AD-001;
track execution in `docs/plans/R0_FULL_CLOSURE_WORK_PLAN.md`. Existing bounded
evidence remains valid only for its stated scope. No gate is passed by the
choice to finish the program.

R0-F is limited to separately admitted physical-MEGA65 timing, DMA, IRQ, and
platform-identity evidence corresponding to the closed bounded R0-E
configuration. The R0-E carrier-delivery issue is resolved: future D81 images
must use a fresh MEGA65-created `NEW D81 DD IMAGE` root slot and the guarded
in-place-fill procedure recorded in
`docs/reports/D81_MEGA65_NATIVE_SLOT_DELIVERY_2026-09-03.md`. R0-F does not
select a renderer, display mode, queue capacity, DMA duration, cadence, memory
layout, or measured limit.

## 5. Hard gates

- R0 hardware measurement is mandatory; Xemu supports regression but cannot close hardware-sensitive behavior.
- A D81 is not eligible for functional hardware testing until the exact
  Xemu-verified bytes have an exact SD-copy hash and pass the physical chooser
  gate without an error; a chooser `ERROR CODE FF` permanently invalidates that
  carrier identity.
- A measured-limits revision must freeze the hardware-dependent display, timing, memory, DMA, input, and audio values used downstream.
- The Phase 1 integrated-engine harness is a hard gate: all core engines must run concurrently within the accepted limits with deterministic evidence.
- Gameplay implementation may not merge before the applicable R0-F/measured-limits and Phase 1 gates specified by the governing documents.

## 6. Human-owned decisions

Codex and other implementation agents may not autonomously decide architecture changes, public/core contract changes, player-visible gameplay changes, flight or control feel, still-gated defaults, difficulty, mission/campaign creative content, production coefficients, `R0-GATED` values, reserve/resource changes, product scope, or acceptance waivers.

## 7. Open high-priority issues

- Revision 1.4 is missing; a human must supply and hash it or explicitly approve a consolidated-corpus disposition.
- Gameplay 0.2 and Engine 0.1 remain candidates, not approved production baselines.
- Every correction in Alignment 0.2 remains proposed unless separately approved and recorded.
- The supported MEGA65 hardware/core/ROM/video/storage/input matrix requires explicit closure and evidence identity.
- Snapshot lifetime/storage, independent display-versus-simulation timing, storage transactions, canonical interfaces/numerics, and other later contracts remain open at their named gates.
- Alignment 0.2 identifies some items as blockers for formal milestone acceptance; because that document is itself draft, those classifications are retained as review findings rather than silently promoted here.
- `DEC-002` (candidate specification approval state) and `DEC-003` (supported platform/evidence matrix) remain open; their absence does not block bounded R0-A construction but does block the relevant formal acceptance.

These later-phase gaps do not prohibit independent, bounded R0-A work unless an authoritative source or explicit human decision says they do.

## 8. Repository conventions

- Preserved files under `spec/` are source records and are not casually edited.
- Generated artifacts must identify their source and generator and remain distinguishable from authority documents.
- Generated files are regenerated, not hand-edited.
- Substantive work uses task-specific branches and focused commits after the bootstrap of `main`.
- Tests, logs, measurements, and retained evidence accompany implementation at the required evidence tier.
- Contradictions are recorded and escalated; they are never silently reconciled.
- Shared memory, ABI, timing, and ownership changes require matching memory-map or decision-log updates.

## 9. Append-only change log

| Date | Bootstrap/project version | Major action | Commit | Human approval status |
|---|---|---|---|---|
| 2026-08-17 | Repository bootstrap 0.1 | Created the local project home, preserved the four supplied documents, recorded hashes/status, and established empty ownership structure | Initial bootstrap commit containing this record; resolve with Git history after commit creation | User authorized repository bootstrap only; no draft, correction, TBD, or architecture decision was approved by this action |
| 2026-08-17 | Repository bootstrap 0.1 | Configured the private GitHub remote and published `main` | Initial bootstrap commit `7c9beb26a33e7a47c75893b595bc2e56c131aa8f`; this append-only publication entry is in the following project-control commit | User created the private repository and authorized publication; specification approval state is unchanged |
| 2026-08-20 | R0 configuration synchronization | Added exact approved Read-First/AD-001/approval-record copies and candidate Architecture 1.5.1/Engine 0.2; updated control index without promoting candidate parents or passing R0 | Pending configuration-control commit | AD-001 authorizes development only; `DEC-002`, `DEC-003`, physical evidence, and human acceptance remain open |
| 2026-08-20 | R0-A handoff / R0-B admission | R0-A focused physical base-page and pointer proof was owner-recorded as passed at `1ab5b62`; created bounded R0-B graphics/display/cockpit/palette/input/representative-audio proof admission on `codex/r0-b-development` | R0-B admission commit | R0-B development is authorized by AD-001; parent candidates remain unapproved; no R0-B physical evidence or production selection is implied |
| 2026-08-21 | R0-B closure / R0-C admission | Recorded accepted R0-B physical composite evidence at `18cac27f1d0de9b50123ccfd4148ad40a3ecec4c` and opened bounded R0-C proof implementation on `codex/r0-c-development` | R0-C reconciliation commit | R0-B is closed PASS only for its admitted proof scope. R0-C remains development work; `DEC-012`, physical storage/media evidence, and human acceptance remain open. |
| 2026-08-21 | R0-C DEC-012 fixture authorization | Owner approved a separate sacrificial writable D81 solely for the R0-C media-fault fixture and two-generation recovery evidence | Pending focused R0-C contract-planning commit | This does not select a production save medium, disk split, or player-facing recovery UX. Target adapter, physical fault evidence, and human R0-C acceptance remain open. |
| 2026-08-21 | R0-C Attic platform-contract admission | Owner admitted `R0C-PLAT-ATTIC-001` for bounded proof-only real Attic-to-chip CPU-copy staging; registered the private proof ABI and `$050000-$052FFF` destination ownership | Pending focused R0-C contract-admission commit | This does not admit DMA, production ResourceManager behavior, production staging cadence, tile policy, or renderer behavior. `R0C-PLAT-ROM-001` remains deferred; no ROM wrapper is authorized. |
| 2026-08-29 | R0-C candidate completion by owner waiver | Corrected D81 carrier loads without chooser `ERROR CODE FF`; owner waived remaining physical media-fault execution and requested R0-C candidate completion | Local commits `1ef7369`, `cde5555`, `2ce0e35` | R0-C implementation is complete for the bounded proof candidate. This is not formal `R0-C GATE PASSED`; `R0C-ROM-001` remains deferred and unexecuted media faults are recorded as WAIVED. |
| 2026-09-01 | R0-E functional-proxy evidence and R0-F handoff | Reworked the R0-E target proof so its result block reflects executed bounded cases, then passed two clean Xemu boots of the exact host-gated carrier and published the retained evidence | Source `ae2b0ae`; evidence record `e2e2b46` on `codex/r0-e-development` | The carrier is `XEMU_BOOT_VERIFIED` only. Timing is `NOT_MEASURED`; DMA hardware probe is not executed; physical chooser, SD-copy hash, physical measurements, human acceptance, and all measured-limit decisions remain open. |
| 2026-09-01 | R0-E physical carrier verification | Exact SD-copy hash matched; MEGA65 chooser showed the readable `F65R0E.D81` directory and loaded its physical functional-proxy banner | Physical evidence record pending publication | The D81 is `TEST_ELIGIBLE` only for the bounded functional-proxy scope. Timing, DMA, IRQ, phase-sweep, platform-identity, R0-E/R0-F closure, and measured-limit decisions remain open. |
| 2026-09-04 | R0-E bounded proof closure and D81 delivery correction | `F65R0EG.D81` passed pre/post raw FAT32 one-extent audits, safe eject, physical chooser, and Rev3 runtime capture; recorded the MEGA65-native slot procedure for later carriers | `702700f`, `2559e18`, and the R0-E closure reconciliation commit on `codex/r0-e-development` | Owner accepted closure of the bounded R0-E functional-proxy/raster-observation scope only. R0-F measurement/platform work, measured limits, and production authorization remain open. |
| 2026-09-12 | R0-F physical/SD evidence lock-in | Working-tree report-only updates; no commit yet | SD copy was hash-verified and contiguous with a single extent/safe eject; owner-reported physical runtime banner evidence captured in `docs/evidence/r0f/physical/R0F-PHYSICAL-RUNTIME-2026-09-12.md`. R0-F measured-limits items remain open. |
| 2026-09-16 | R0-F Step 3 static/host audit | Strengthened result validation, accounted for 107-byte compiler static stack, corrected proxy-contract claims, and recorded startup B/KERNAL conflict | Working tree on `744920d`; no commit or push | Owner requested Step 3 execution. Host/build PASS does not pass the blocked static gate, approve a new platform wrapper, close R0-F, or freeze limits. |
| 2026-09-17 | R0-F bounded startup fix | Excluded unused SDK ROM initializer, added static rejection checks/build banner, fresh-built F65R0F2.D81, passed host gates and two clean Xemu boots | Working tree on `744920d`; exact hashes retained; no commit or push | Owner requested continuation. SD/physical retest, full measurements, owner acceptance and measured-limits approval remain pending. |
| 2026-09-17 | R0-F2 physical runtime evidence | Retained hashed owner photo and pre/post SD extent records; new build banner, functional PASS and all 80 samples valid observed | Working tree; no commit or push | Observation only. Safe-eject confirmation, full measurement obligations, owner gate acceptance and measured limits remain open. |
| 2026-09-17 | R0-F private CIA-count diagnostic | Added reset-only CIA1 timer ownership, generated REV2 encoding, retained raw phase-started tick/cohort measurements and independent Java reduction; F3 withheld after serial-mode guard review, fresh F4 built | Working tree on `744920d`; source hashes in build accounting; no commit or push | Owner requested build under AD-001. No SI calibration, physical result, public ABI change, measured-limit selection, or R0-F acceptance implied. |
| 2026-09-17 | R0-F4 physical evidence and closeout review | Retained four original hashed photos, transcribed physical raw-count summaries and displayed platform identities; documented full-scope versus bounded-proxy evidence gap | Working tree; documentation/evidence only; no commit or push | User requested continuation of evidence review. Physical observation does not establish exact SD bytes, calibration, complete combined load, a waiver, or full R0-F acceptance. Owner scope direction remains open. |
| 2026-09-17 | Full R0 closure direction selected | Owner replied `1` to select full proof-program completion on the current design; added dependency-ordered work plan and initial source audit | Working tree; documentation only; no commit or push | Direction question resolved. No gate pass, parent approval, measured-limit selection, unspecified wrapper admission, Phase 1 or gameplay authorization. |
| 2026-09-17 | RC-1 raw-capture viewer implementation | Built F5 post-acquisition screen transport and Java importer; host/static, fresh D81 and two exact-image Xemu boots passed; source-traced video-derived CIA clock enable | Working tree; exact inputs in F5 accounting; no commit or push | Owner requested Build it. Capture slice only: no calibrated units, full combined workload, SD/physical proof or gate acceptance. |
| 2026-09-17 | R0-F proof-platform approval and qualification | Owner approved additive platform-contract development; PF-001 adds canonical-entry/IRQ/DMA/PCM development PRG and fail-closed host/Java/Xemu tests | Working tree on `744920d`; exact inputs in PF-001 accounting; no commit or push | Approval is recorded in task admission. Primitive qualification does not pass the full combined harness, admit deferred reversible ROM reclaim, calibrate SI/cycles, or authorize physical delivery without the exact-D81 gates. |
| 2026-09-18 | R0-F CF001 combined experiment | Implemented reset-only ROM backup/reclaim/byte-verified recovery, nominal clock/work calibration, populated synthetic workload, snapshots, renderer, matrix input, SID/PCM, DMA and IRQ; host/Java checks and two NTSC plus two PAL boots of exact F65BLK02 candidate pass | Working tree on `744920d`; D81 SHA-256 `b13853a7ddaf3bf26dfcaceb7e4466ab2d58702b96bfcbe9ae62c7db56ed3d82`; retained CF001 evidence; no commit or push | Owner requested ROM/calibration/integration/Xemu and F65BLK02 preparation. SD remains untouched pending owner sudo command and raw FAT32/eject gates. Reset-only recovery does not admit production ROM/storage return; physical calibration, full parent workload/latency/window requirements, measured limits and R0-F acceptance remain open. |
