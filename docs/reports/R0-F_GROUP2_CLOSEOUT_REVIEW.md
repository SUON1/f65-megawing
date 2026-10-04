# R0-F Group 2 closeout review

2026-10-04. **OWNER-APPROVED BOUNDED CLOSEOUT — current Group 2 work package
closed; missing broader-suite proof carried forward, not marked PASS.**

The owner requested wrapping Group 2 and moving toward the forthcoming flight
simulation supplement and development-plan review. This report makes the
bounded closeout decision concrete. The owner subsequently approved:
“approved: bounded closeout and carrying the listed gaps into that review.”
That approval closes this work package under the disposition below. It is not
a full-suite proof PASS, full R0-F acceptance or Phase 1 entry approval. The
[approval record](../evidence/r0f/group2/2026-10-04-closeout-review/owner-disposition-01/decision.json)
preserves the decision separately from the original review/evidence records.

## Engineering result and value

The copied diagnostic establishes useful platform evidence before game work:
P09's bounded physical normal workload resumes all five services after returning
storage, preserves integrity and exports 3200 records. The new L3 physical run
observably refuses an occupied export name, preserves four existing payloads
and saves the correct 34-byte RSSTATE without additional trace chunks. New
actual-owner queue host tests establish deterministic rejection/state preservation.
R1/R2 recover resident space without changing capacities, reserves or integrity
checks. These are bounded foundation results, not gameplay or a finished engine.

The additional six-case combined-load fault campaign remains incomplete. Its
best live queue/capture draft is 511 bytes over the resident ceiling; no failed
draft ran. Completing the original broader intent means admitting a capture
schema/reducer and fitting/qualifying changed-target cases before new hardware
work. This report does not describe that work as already done.

## Case disposition: evidence, missing proof and decision

P below is `docs/evidence/r0f/group1/2026-10-03-audio-readback/`. These paths
identify retained tests/results; no passing suite was replayed for this review.
The [reconciliation packet](../evidence/r0f/group2/2026-10-04-closeout-review/README.md)
pins the records inspected and the newly located snapshot comparison.

| Approved case | Actual result available now | Remaining required proof under the broader intent |
| --- | --- | --- |
| G2-Q queue pressure | [Actual P09 owner host PASS](../evidence/r0f/group2/2026-10-03-event-owner-host/README.md): 71 accepted/17 rejected; flag, full queue/model and peer preservation, invalid IDs and reset. | Live combined-workload case records before/after storage; changed-target/emulator/physical gates. The failed fit is not runtime proof. |
| G2-S snapshot starvation | Historical command/output now located in `2026-09-30-foreground-memory-experiment/experiment/host.json` and `bounds-host-output.txt`: held reader, all three slots, rejected publication, held bytes preserved and newest acquisition. Four snapshot owner functions and model/generated headers are byte-identical to P09. Reuse host assertions only. | Live starvation/publication observations in the admitted combined target and required emulator/physical tiers. Historical body equivalence does not prove those tiers or universal starvation. |
| G2-P presentation pressure | P/host/host-01/validation.json records native scene/owner proof, 3200 scene byte comparisons and 83 codec rejections. Frozen scene test observes four retained anchors and 6400 drops. | Explicit named worse/better ranked candidate and superseded/incomplete-generation case accounting under combined load. Scene totals alone do not claim every nominated pressure case. |
| G2-D display failure | P/host/host-01/validation.json and display-output.txt: actual display owner PASS for DMA/copy retry, snapshot CRC fault and 26 cancellation boundaries; obsolete/partial swap protection. Hardware edges are mocked. | Admitted safe live injection/capture and changed-target/emulator/physical fault proof. Never submit unsafe DMA. |
| G2-A unavailable audio | P/host/host-01/audio-output.txt: actual failed-copy begin leaves cache invalid/PCM off. Nominal P09 audio continuation is separately proven. | Failed-copy continuation with real fault 21/22 side effects and actual caller reachability/lockout; safe observable target case. The raw service path is not proof of caller reachability. No production fallback is selected. |
| G2-L lifecycle/export failure | P/host/readiness-host-02 and P/host/resume-host-02 actual owner tests PASS at host tier for stated guards/policy/restoration/NMI/IRQ conditions. [L3 physical screen/returned-card observables PASS](../evidence/r0f/group2/2026-10-04-l3-physical/README.md). | Other controlled storage/admission failure subcases and their required tiers. Physical SAVE-call stage/attempt count are not captured. L3 operator record still lacks safe-eject/one-run confirmation and chooser photo; configuration is UNKNOWN. |

Existing evidence location is resolved for the historical snapshot command and
its owner identity. Missing tests/tier evidence above remain NOT PROVEN. Missing
work-package closure authority is the owner's explicit approval below. Historical Group 2
allocation remains unrecovered; the broader grouping was approved prospectively.
Nothing assigns Group 3.

## Owner-approved bounded closeout

**Approved:** close the current Group 2 work package as bounded Phase 0
evidence, with explicit carry-forward of the missing obligations in the table.
Do not label the six-case suite PASS. Do not label deferred proof as satisfied.

This changes the earlier task completion scope. The prior
[Build Intent](../plans/R0-F_GROUP2_BUILD_INTENT.md) completion condition said:
“A host-only, standalone-only or partially captured suite is not Group 2 finished.”
The owner's explicit approval supersedes that condition for this bounded work
package. It does not satisfy, waive or close the remaining successor admission
requirements; their disposition belongs to the upcoming review.

The approved disposition is:

1. Retain all obtained host/static/Xemu/physical results and all failure records
   at their exact tiers. Accept the L3 observable result with its recorded
   operator/configuration gaps under the owner's bounded approval. Never rerun
   L3/P09 or earlier tested carriers to fill administrative gaps.
2. Carry forward the six rows' missing proof, including audio continuation and
   live capture fit/schema/reducer, into the upcoming supplement/development
   review. Their owner is the founder/review; they are not silently assigned to
   Group 3 or promised as automatic Phase 1 implementation work.
3. Keep successor admission's deterministic overflow/fault/starvation/shedding
   row OPEN unless the owner separately records evidence-supported closure or
   a named row-specific waiver/reassignment. This Group 2 disposition alone
   gives no full R0-F PASS, measured limits, Phase 0 exit or Phase 1 authorization.
4. End speculative instrumentation work for this package after that disposition.
   Any later test must answer a named remaining requirement and a concrete
   product/engineering decision under the reviewed plan.

The owner selected bounded closeout rather than continuing the original broader
campaign in this package. No additional implementation, emulator qualification
or hardware run is authorized by this closeout. Remaining work must be selected
through the upcoming review; no credit/time estimate is claimed for it here.

## Next review, bounded handoff

The forthcoming **new flight simulation supplement has not been supplied or
ingested in this task**. The existing Gameplay and Simulation Supplement v1
remains current authority; its Draft 0.2 predecessor remains provenance. No
authority is promoted or replaced from the owner's description alone.

After the document is supplied, the separate development-plan review should
decide its authority/contradictions, dispose of the remaining R0-F rows, establish
the actual Phase 0 exit/Phase 1 entry conditions and name the smallest gameplay
increment. Carry this evidence table into that review once; do not reconstruct
the campaign or rerun passing results. Phase 1 has not begun.

## Integrity and publication

Branch `codex/r0f-group2-preparation`; HEAD and freshly fetched origin/main both
`abd3a0803b96090654db5dbdda43ad42d7b29a5a`. P09 remains frozen, end $BFF5/free 11;
these bytes are not expansion room. L3 original qualification and physical
evidence remain unchanged; L2's fragmented SD copy remains INVALID — DO NOT USE.
Unrelated SD backup/mirror work and historical carriers are preserved.

Main v1.6, successor admission, Group 2 intent, generated owner/export contracts,
memory ledgers and D81 workflow govern. This report/evidence-index work has
non-applicable register/clobber, CPU-visible/physical-memory, MAP/base-page, DMA,
timing/deadline and IRQ/NMI effects. No target/generated artifact, capacity,
reserve, integrity check or acceptance threshold changes. Input/packet hash and
link/JSON/whitespace checks are recorded in the review packet; they establish
document/evidence consistency, not new fault behavior.

No new target build, Xemu, SD write, hardware run, commit, push or publication
occurred in this closeout review. Publication remains separately owner-held.

### Subsequent publication authorization

On 2026-10-04 the owner separately requested "Commit and push." The focused
publication includes the Group 2 tools, copied-source experiment and failure
records, retained host/emulator/physical evidence, intent and bounded closeout.
Unrelated SD backup/mirror work and older successor evidence remain local.
Main integration and every acceptance/phase decision above remain separate.

The static evidence guard now admits Group 2 paths only as eligible for exact
SHA-256 pins. The 28 original logs, maps, patches, copied specification and
loader listing that contain retained whitespace are pinned without changing
their bytes. Unlisted whitespace, changed pinned bytes and forbidden artifacts
still fail; focused isolated fixtures cover the Group 2 policy. This publication
check establishes repository consistency, not additional fault-behavior proof.

Publication validation: `python3 -B -m unittest discover -s tools/ci -p
'test_*.py' -v` passed all 14 fixtures. The workflow's tracked-file syntax
checks passed for 2425 JSON, 1194 Python and 11 shell files; 534 entries in
the ten Group 2 `SHA256SUMS` manifests matched. The staged changed-range
whitespace check passed with only the exact manifest pins excluded. The
focused staged set contains no new D81, ROM or emulator-state image. No
passing host/target/emulator/hardware campaign was replayed for publication.
