# R0-F closeout review — 2026-09-17

**The F4 bounded diagnostic ran on hardware. Full R0-F is not complete.**
This review records evidence, not a new acceptance contract or waiver.

Subsequent owner decision: **option 1 selected** by reply `1` — finish the full
R0 proof program on the current design. Program direction is resolved.
Execution tracking: `docs/plans/R0_FULL_CLOSURE_WORK_PLAN.md`. Historical
options below explain the decision; no archive disposition or waiver was chosen.

## Why this is more than one remaining test

AD-001's authorized-scope table defines R0-E as an independent-clock combined
snapshot/memory/renderer/input/audio/DMA/IRQ/storage/reserve/fault harness in
Xemu, and R0-F as corresponding physical evidence satisfying the parent
acceptance requirements. Its dependency rules prohibit gate closure without
complete evidence and owner review. Candidate-parent approval remains separate.

The accepted R0-E record instead explicitly closes a **bounded functional
proxy plus read-only raster observation**, not the full combined measurement
gate. That bounded acceptance remains valid and is not revoked here. F4 times
the inherited proxy; adding a timer does not supply the missing real services.
Earlier near-closeout wording understated this gap. Neither another photo nor
a clock conversion alone would close it.

## Evidence and requirement matrix

| Obligation / source | Established evidence | Remaining work / disposition |
|---|---|---|
| Exact build and Xemu regression; Architecture 1.5.1 §12.6 | F4 host gates, two clean exact-carrier Xemu boots, raw captures independently reduced by Java; see CIA timing handoff | Retain these results; they are not physical timing evidence. |
| Physical execution; AD-001 R0-F | Owner screen shows F4 acquisition complete, inherited functional PASS, all requested masks FFFF, fault 00, zero nominal-count misses | Retained photos and transcription; no new hardware action now. |
| Evidence identity; Architecture §12.6, DEC-003 | R6, displayed core/ROM/HYPPO/Freezer and NTSC identity | Exact core/binary provenance, runtime clock relation, supported-mode matrix, storage/input/capture identity remain incomplete. Later Freezer settings do not prove sweep configuration. |
| D81 delivery gate | F4 banner observed; host/Xemu artifact identity retained | F4 SD byte hash, independent extent record, safe-eject and chooser chain not supplied. Preserve unknown status; do not infer a carrier failure or borrow F2 evidence. |
| Calibrated 100 Hz and phase/window evidence; Architecture §§6.2–6.3, §16 | 10000-count release period, 16 requested phases/case, 33-tick cohorts, frame-count cross-checks | Establish timer frequency/reference, overhead and effective clock; full legal phase and rolling-window coverage. Frame-count agreement is not SI calibration. |
| Physical raw measurement integrity; Architecture §12.6 | Displayed aggregate hex values transcribed | Physical result block and 10880-byte raw sample capture not obtained; physical Java reduction not performed. |
| Combined workload; AD-001 R0-E/F, Engine 0.2 §17.2 | Functional proxy exercises normal/lag/shed/fault/pressure cases | Identify and integrate admitted proof renderer, input, audio and protected non-render workload; establish corresponding Xemu configuration before physical acceptance. No production gameplay required or authorized. |
| Input/audio service latency; Architecture §16, Engine §17.2 | Proxy flags only | Real service/edge/deadline measurements under combined load, with accepted measurement definitions. No production input bindings or gameplay tuning selected. |
| DMA/IRQ contention; AD-001, Architecture §16 | F4 explicitly has IRQ masked and no DMA execution | Separately admitted wrappers, blocking/masking/service-duration and alignment evidence; cannot be inferred from F4. |
| Snapshot/memory/stack/reserve/storage; Architecture §§6, 12.6, Engine §§17.2, 18 | Linked ledger, synthetic snapshot READY high-water 3 and functional fault/shedding results | Required combined ownership/age/drop and dynamic high-water/fit evidence, storage behavior and reserve isolation; static accounting is not dynamic proof. No reserve consumption authorized. |
| Formal acceptance; AD-001 dependency rules, approval record | Development authorized; bounded predecessor acceptances retained | Full evidence review, dependency reconciliation and named human acceptance; candidate-parent/DEC-003 issues remain explicit. Measured limits and Phase 1 remain separate gates. |

## Decision needed before changing scope

The current admission is bounded physical measurement corresponding to the
accepted R0-E proxy. Completing the full parent-scope program requires a
reconciled combined-harness admission, rather than silently expanding F4.
The owner has also signaled substantial coming development changes.

The two dispositions presented were (option 1 subsequently selected):

1. **Continue toward full R0 closure on the present design.** Reconcile the
   bounded R0-E acceptance with the missing combined-harness evidence, then
   admit and implement that proof program. Full acceptance requires the
   evidence above; it is not one more SD test.
2. **Archive the bounded F4 experiment before the redesign.** Preserve its
   successful observations and explicitly leave full R0-E/F acceptance and
   measured limits open. This ends this experiment, not the R0 gate, and does
   not authorize Phase 1 or production development.

No waiver, architecture change, or scope selection is inferred from “Continue.”

## Work split if full closure is selected

Codex first prepares the reconciled admission and exact evidence checklist;
audits the installed core's CIA behavior and usable frequency reference;
specifies raw physical capture and validation without assuming a new hardware
connection; and implements the admitted combined fixture and measurement
wrappers. Each target change gets host/static and fresh exact-D81 Xemu gates
before a hardware request. Do not assume an oscilloscope or any other new
equipment is needed until the reference/capture design is resolved.

The owner reviews scope/platform decisions, then performs only the specified
SD transfer and physical test steps after a verified build and explicit
checklist are ready. Existing transfer logs can be supplied if available;
their absence is not a reason to repeat a hardware run now. No SD/configuration
change is requested at this review stage.

## Reviewed authority and evidence

- `F65_OFFICIAL_RECORD.md`, Read-First v1.0 relevant precedence/gate sections,
  AD-001 and the 2026-08-20 approval record.
- Candidate Architecture 1.5.1 §§6.2–6.3, 12.6, 14, 16 and Engine 0.2
  §§17.2, 18; exact identities remain in the official record. Review does not
  promote them to approved production sources.
- `docs/evidence/r0e/R0E5-D81-PHYSICAL-RUNTIME-2026-09-04.md`.
- `R0-F_CIA_TIMING_CONTRACT.md`, `R0-F_CIA_TIMING_HANDOFF.md`, current
  admission, execution plan, stage control, and R0-F evidence map.
- `docs/evidence/r0f/cia-timing/physical/R0F4-PHYSICAL-OBSERVATION.md`
  and its four hashed original photographs.

## Review impact and verification

Changes are evidence/control documentation and retained photographs only.
Register/clobber, CPU/physical memory, MAP/base-page, public/private ABI,
DMA, IRQ/NMI, timing/deadline and generated-artifact impact: **none**.
No target source, contract, build manifest, D81, or SD content is changed by
this review. Existing working-tree implementation changes are preserved.
No compile, host functional, Xemu, or physical test was rerun for this
documentary change; earlier test results remain attributed to their handoff.

Validation: compare each retained photograph byte-for-byte with its attachment;
verify SHA-256 values; visually check the manual table and identity fields;
run `git diff --check`. No commit or push performed. The scope decision was the
review handoff blocker and has since been resolved by the owner's option 1.
