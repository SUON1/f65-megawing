# 65Aero Phase 1 entry and Developer Flight Demo plan

20 October 2026. **FOUNDER-APPROVED ENTRY DISPOSITION AND A1–A6; local versioned adoption, integration pending.**

The [founder decision](../decisions/PHASE1_ENTRY_ADOPTION_2026-10-20.md)
approves bounded program closeout, every named obligation destination and A1–A6.
Proposal labels below preserve the reviewed packet's wording; the decision
supersedes its earlier approval-pending statements. The successor specifications
in the manifest govern the adopted text. M1 is authorized after integration into
verified main, including direct-PRG PAL/NTSC Xemu; no D81/SD/physical testing.

Build Intent: founder's `F65_Codex_R0_Closeout_Phase1_Entry_Kickoff.md`,
followed by explicit authorization to preserve all pre-existing untracked paths
and complete planning/preflight on the focused branch. This is the one combined
handoff. It does not start M1, close full R0-F, approve limits, finalize Runtime,
or authorize publication.

## 1. Verified baseline and authority

Repository: `https://github.com/SUON1/f65-megawing.git`.
Branch: `codex/r0-phase1-entry-closeout`.
Baseline: `44f6c46bfb76a050f88bc343a354220cbf5782ea`.
On 20 October, `git fetch origin --prune`, `git ls-remote origin
refs/heads/main`, and `git rev-parse main origin/main` established identical
live/fetched/local main. No intervening commits from the kickoff reference.
Tracked tree was clean; 20 pre-existing untracked status entries were disclosed
and explicitly authorized to remain untouched. WIP was NONE.

Authority is the [corpus manifest](../../spec/manifests/spec-corpus.json):

| Reference used below | Authority and inspected clauses |
| --- | --- |
| Main | [Main v1.7](../../spec/core/F65_Main_Concept_v1.7_HUMAN_APPROVED.md), §§3–7, 10, 12, 15, 17–19, 23: architecture, owners, memory, clocks, phases |
| Gameplay | [Gameplay v1.1](../../spec/core/F65_Gameplay_and_Simulation_Supplement_v1.1_HUMAN_APPROVED.md), §§5–9, 21: semantic controls, presentation, acceptance |
| Runtime | [v1.1 amendment](../../spec/core/F65_Runtime_v1.1_APPROVED_CANDIDATE_AMENDMENT.md) plus its unchanged base PDF, especially §§5–8, 10, 14, 17–23: **approved candidate, NOT FINAL** |
| Physics | [Physics v4.0](../../spec/subsystems/F65_Flight_Physics_and_Simulation_Engineering_v4.0.md), §§1–3, 9–10, 12–15: detailed physics/data baseline; numeric/data choices remain gated |
| Graphics | [Graphics v2.1](../../spec/subsystems/F-65_Megawing_Graphics_White_Paper_v2.1.pdf), §§2, 7–8, 12, 14, 16: immutable snapshots, complete generation pairs, registration and measured gates |
| Remaining family | Audio v1.0, SensorAndTrack v1.0 and AI v1.1 as identified in the manifest; subordinate to the core three |
| Engineering control | [Workflow](../DEVELOPMENT_WORKFLOW.md), [Physics adoption](../decisions/PHYSICS_V4_ADOPTION_2026-10-04.md), [current state](../../CURRENT_STATE.md), generated contracts and owner ledgers |

The old Main v1.6/Runtime v1/Physics v3.3 references in historical evidence
identify that evidence's original authority. They do not supersede this family.
Navigation and this plan do not amend specifications. No corpus bytes or
manifest hashes were changed.

**Impact of this task:** documentation only. Registers/clobbers, CPU-visible
and physical memory, MAP/base-page, DMA, 100 Hz timing/deadlines, IRQ/NMI,
generated interfaces and target artifacts in the repository: not applicable /
unchanged. The isolated compile below is structural evidence only.

## 2. Retain accepted evidence; do not reconstruct campaigns

Main §§17.2–17.4 and current state retain R0-A/B and current-program R0-C
dispositions. R0-C's historical waiver is not a retroactive historical PASS.
Current state retains R0-D's bounded calibration-proof closure; Main §17.5's
“CURRENT” label describes broader measurement work and must not be read as a
shipping 530,000-clock budget. R0-E remains bounded functional-proxy/raster
evidence, not full current-parent acceptance.

The [P09 physical packet](../evidence/r0f/group1/2026-10-03-p09-physical/README.md)
establishes same-run returning storage, 3,200 records, 955 world pairs, five
resumed services, integrity and nominal timing WITHIN_OBSERVED_BOUNDS.
Its frozen source is the [audio-readback packet](../evidence/r0f/group1/2026-10-03-audio-readback/README.md).
Retained program identity:
`acc735f280f9d4e86b3b2040e5b2bed987908331f7899a87f5382c6cd23cd4d8`;
trace identity:
`e83b0b526c6fe22bb66285a93a25b8107da7c5c112d06f8ceb77af4cf6cc66dd`.
These are quoted retained identities, not newly acquired or rehashed carriers.
P09's observed stack use, IRQ body intervals, phase samples and synthetic
loads do not establish production maxima, whole-ISR cost or absolute SI accuracy.

The [owner-approved Group 2 closeout](../reports/R0-F_GROUP2_CLOSEOUT_REVIEW.md)
and [reconciliation index](../evidence/r0f/group2/2026-10-04-closeout-review/README.md)
retain queue host proof, located snapshot host proof, bounded scene/display/
audio tests, failed-fit experiments and L3 physical observations. The broader
six-case suite is **not PASS**. P09 nominal audio restart is distinct from
G2-A fault/caller continuation. The failed 511-byte-over resident draft did not
run; its capture design is not an obligation to recreate that diagnostic.

L3's [physical packet](../evidence/r0f/group2/2026-10-04-l3-physical/README.md)
retains occupied-name refusal, four preserved payloads and correct 34-byte
SAVE without extra trace chunks. Safe-eject/one-run confirmation, chooser photo,
configuration, and physical SAVE stage/attempt count remain missing. P09 lacks
fresh named core/ROM/HYPPO/Freezer identities and explicit spoken filename
confirmation. Preserve these limitations. Do not replay either carrier to
fill administrative gaps.

### Outstanding requirement-to-disposition matrix

Only outstanding portions are listed. Every reassignment below is **proposed**;
the founder must approve named rows. Until then the
[successor admission](../reports/R0-F_SUCCESSOR_ADMISSION_RECONCILIATION.md)
requirements remain open. “M1 block?” means whether missing proof must precede
an empty visual foundation **under the proposed entry contract**, not whether
the current contract has already been waived.

Classification key (exact meanings):

- **B:** SATISFIED ONLY FOR BOUNDED CONFIGURATION.
- **N:** REQUIRES A NARROW PRE-ENTRY CHECK.
- **F:** PROPOSED REASSIGNMENT TO PHASE 1 FOUNDATION/DEMO GATE.
- **L:** PROPOSED REASSIGNMENT TO LATER SUBSYSTEM ACCEPTANCE.
- **W:** PROPOSED EXPLICIT OWNER WAIVER / CHANGE OF ENTRY CONTRACT.
- **O:** OPEN — TRUE PRE-ENTRY BLOCKER.
- **U:** UNKNOWN — HUMAN/EXTERNAL EVIDENCE REQUIRED.

Retained accepted rows above are SATISFIED — RETAIN EXISTING EVIDENCE for
their stated scope only. B never closes the outstanding portion in this table.

| ID / requirement and exact authority | Existing evidence and limitation | Class / proposed owner and destination; required behavior and tier | M1 block? / consequence |
| --- | --- | --- | --- |
| Q: G2-Q queue pressure; Main §§3.3, 15.2, 17.6; Runtime §§17.4, 19.2 | Group 2 actual P09 owner host: 71 accepted/17 rejected, invalid/reset and peer preservation; no live combined before/after-storage case | F: CoreRuntime commands/events, M1 host/target rejection and no mutation on full/invalid; M6 combined Xemu + physical pressure. Storage crossing rechecked when StorageService is enabled | No historical replay. New M1 queue must reject deterministically before its use |
| S: G2-S starvation; Main §§4.2, 10.5; Runtime §§14.1, 19.2 | Located held-reader/all-three-slots host assertions and byte-equivalent owner functions; no live starvation proof | F: CoreRuntime publication + PresentationExtractor, M1 held-reader/full-slot host/target tests, M2 Xemu visibility; M6 physical starvation under enabled load. Preserve held bytes, reject publication safely, acquire newest complete legal snapshot | No historical replay; immutable ownership is an M1 acceptance requirement |
| P: G2-P pressure; Main §§4.6, 10.3–10.8; Graphics §§2.3–2.6, 7–8, 14 | P09 host 3,200 scene comparisons, 83 codec rejections, four anchors/6,400 drops; named better/worse and incomplete/superseded cases incomplete | F: GraphicsEngine M2 named ranked candidates and supersession host/target/Xemu; M6 physical enabled-load shedding. Retain required anchors, deterministic ranking, discard incomplete/obsolete generation | No; full object/LOD production pressure remains later Graphics acceptance, not M2 runway complexity |
| D: G2-D display failure; Main §§5.4, 10.4–10.6; Graphics §§2.4, 2.6, 7 | P09 display host retry/CRC/26 cancellation boundaries; hardware mocked | F: Graphics/Platform M1 host no partial/obsolete swap; M2 safe Xemu cancellation/retry; M6 safe physical injection and capture. Validate before DMA; last complete frame stays visible; no unsafe DMA submission | No old diagnostic required; each enabled display path must fail safely |
| A: G2-A unavailable audio; Main §§5.5, 11, 15.2; Gameplay §21.6; Runtime §§15, 19.2 | Failed-copy begin leaves cache invalid/PCM off; real fault 21/22 caller reachability, lockout and continued service unproven | L: AudioEngine/Platform at first audio enablement, before M6 if enabled. Host actual caller/fault path then target/Xemu/physical safe failure; required warnings retain text/visual and approved audio fallback. Never infer this from P09 nominal restart | No for explicitly audio-disabled M1. Demo cannot claim audio acceptance; mandatory warning fallback remains required as warnings become live |
| L: G2-L lifecycle/export failure; Main §§5.6, 14.5, 15.2; Runtime §§16, 19.2–19.3 | Host readiness/resume guards plus bounded L3 physical observables; other failure subcases and configuration/attempt evidence absent | L: StorageService before any new feature relies on returning storage. Host refusal/restoration/lockout, target/Xemu, physical returning-service and safe media failure cases. No false resume success or overwrite; collect actual call/attempt observations | No for boot-only M1 with no runtime storage. Enabling save/reload makes it a feature blocker |
| C: clock calibration/absolute uncertainty; Runtime §§8, 19.1–19.4; full-closure RC-1 | P09 raw nominal ratio/read overhead retained; SI reference and independent uncertainty unclosed | F: Platform/Diagnostics during M1 instrumentation, close before M6 timing acceptance; identified clock/reference chain, resolution/read/capture overhead, independent uncertainty, target + physical evidence and founder limit approval | No for implementation; no absolute timing acceptance until closed. If special equipment/new experiment is essential, propose that bounded test separately |
| I: worst interrupt cost/input latency; Main §§4.6, 12, 17.5–17.7; Runtime §§8, 9, 19 | P09 body maxima 7/8 counts exclude entry/exit and external latency; R0-B bounded evidence | F: Platform/Input M1 semantic edges, host/target boundary checks; M6 physical whole ISR, masking/entry delay, external edge-to-consumption and visible response under enabled load | No universal R0 replay; exposed latency fault and actual measured budgets required before demo acceptance |
| T: phase/rolling windows/100 Hz; Main §§4.1–4.6, 17.6–17.7; Runtime §§19.2–19.3, 20.4 | P09 16 cohorts per epoch and within-cohort 33-tick windows; not exhaustive relative service phases or continuous storage crossing | F: CoreRuntime/Diagnostics M1 exact ordered logical tick and debt tests; M6 target/Xemu/physical legal enabled phase/window matrix, no skipped/merged/stretched ticks; source clock uncertainty closed with C | No before writing scheduler; real deadline violations fail acceptance, never justify clock reduction |
| V: complete-world cadence/age; Main §§4.6, 10.4; Gameplay §9.7; Graphics §2.5 | 955 P09 pairs and bounded nominal 28–30 Hz; no approved maximum age or production projection | F: Graphics/CoreRuntime M1 counters, M2 registration, M6 physical p50/p95/worst source age, construction/view latency and cadence. Existing sustained 20 Hz failure floor retained; 25/30 Hz remain targets | No before implementation. Founder must approve measured world-age and protected-service limits before M6 |
| M: code/state/stack/reserve; Main §5.1; Runtime §§6, 20.3 | P09 frozen end $BFF5/free 11; observed stacks 67/123, proof ledgers only; no production allocation | F: every increment gets actual generated owner ledger/link map/static stack bounds and exercised high-water; M1 cannot borrow reserve. M6 physical enabled-load high-water; full 32 KiB simulation closure remains integrated-harness gate | No historical space-recovery campaign. A new slice that does not fit is blocked immediately |
| R: production renderer/audio/pool/AI combined load; Main §§6.4, 17.6, 18.4; Runtime §§20.3–20.5; Physics §12.4 | P09 synthetic six/full + three/reduced workload; no production physics, sensor or AI costs | L: named production owners, full Phase-1 integrated harness and later enabled subsystem acceptance; host/target/Xemu + physical where inherited evidence invalidated; nine-aircraft profile and required concurrent entities retained | No for empty demo foundation; demo is not full harness or shipping capacity acceptance |
| E: current configuration/PAL/NTSC/exact carrier; Main §§15.3, 17.7; Runtime §§17.5, 22.7 | P09/L3 bounded identities; operator/configuration gaps remain U | U/W: founder accepts retained proof limitations for entry, not missing facts. New M1/M2 Xemu PAL/NTSC checks and M6 fresh physical configuration/carrier chain; additional supported physical modes require their evidence | Founder disposition blocks entry; no demand for historical replay. Fresh exact carrier gates apply only when a new carrier is authorized |
| G: formal R0 disposition, measured limits and phase sequence; Main §§17.8, 18.1–18.4, 19; Runtime §§19.4, 20–21; Physics §15.1 | Bounded Group 2 approval carries gaps to review; no full R0-F/entry acceptance | O/W: founder approves row-specific timing of obligations and coordinated amendments in §5; no blanket “R0 PASS” or final Runtime declaration | **Yes**, current authority still controls |
| H: usable tools/generated seam; Main §§2.3, 18.2; Runtime §§5, 18 | See actual preflight below: compiler/generator available; proof interfaces only, canonical JDK directory missing | N: bounded check completed using existing pinned legacy JDK read-only. M1 explicitly selects that dependency or provisions the pinned JDK locally; production records are M1 work | No unresolved tool availability blocker; legacy dependency must be explicit and preserved |

The old [full closure plan](R0_FULL_CLOSURE_WORK_PLAN.md) and
[Group 1 matrix](R0-F_GROUP1_MEASUREMENT_MATRIX.md) remain historical source
records. Their stale “next successor” and Group 3 language does not assign a new
campaign. This table proposes destinations for remaining obligations; it does
not rewrite those reports or manufacture Group 3.

## 3. Small technical preflight actually performed

All outputs were isolated under `/tmp/f65-entry-preflight-rkj92ws8`; no accepted
proof output, carrier or generated repository binding was overwritten.

| Check / exact command or invocation | Actual result and evidence limit |
| --- | --- |
| `git fetch origin --prune`; `git ls-remote origin refs/heads/main`; `git rev-parse main origin/main` | PASS, baseline above; initial sandbox attempts were denied/network-isolated, authorized elevated calls succeeded |
| `python3 -B tools/diagnostics/r0a_validate.py .` | `R0A-CFG-001 PASS`: present corpus hashes, R0-A reserve/base-page ledger, lock/scope and pinned VICE tools. No VICE execution or image access |
| `toolchain/runtime/llvm-mos/bin/mos-mega65-clang --version` | clang 24.0.0git, llvm-mos `77a0dd93c5e9cec324323ecf1ffe05b47809b1ad`, target mos-mega65 |
| Python `hashlib.sha256(Path(path).read_bytes()).hexdigest()` against `toolchain/f65_toolchain.lock.json` | compiler `cc557ae9…a906` and objdump `5327f031…8e9` match; does not independently pin every linker-library file |
| Existing R0-A C/startup compiled directly with the command below | PASS, 840-byte PRG plus ELF/map/disassembly in temporary directory; compile/link availability, **not runtime execution or new R0-A acceptance** |
| `test`/path inspection of lock's local JDK; `/usr/libexec/java_home -V` | Local locked path absent; no system Java runtime located |
| SHA-256 of legacy JDK `bin/java` and `bin/javac` against existing `r0f_platform_build.py` pins | PASS (`34b9c157…81a0`, `ee7be919…b152`); existing dependency at `/Users/slice/Documents/Codex/f65-megawing/toolchain/runtime/jdk-full/jdk-21.0.12+8/Contents/Home` |
| Pinned legacy `javac -d "$out/classes" tools/generators/src/main/java/f65/tools/R0AHostTools.java`; `java -cp "$out/classes" f65.tools.R0AHostTools generate "$out"` | PASS; copied only input registry into temporary root; all three generated C/assembly/Java bindings byte-equal to repository versions |
| Same `java … f65.tools.R0AHostTools host-test "$out"` | `R0A-PTR-001 PASS`, `R0A-RES-001 PASS`; small boundary/sentinel oracle only, not physics math validation |
| `llvm-objdump -d "$out/entry.prg.elf"` and inspected startup | PASS; B=2 setup before main and B=0 finalization visible. Static structure does not prove runtime MAP/IRQ restoration |

Exact isolated target command (`out=/tmp/f65-entry-preflight-rkj92ws8`):

```sh
toolchain/runtime/llvm-mos/bin/mos-mega65-clang \
  -mcpu=mos45gs02 -mlto-zp=0 -Os -Wall -Wextra -Wconversion -Werror \
  -Iinterfaces/generated src/r0a/main.c src/platform/r0a_platform_45gs02.s \
  -Wl,-Map,"$out/entry.map" -o "$out/entry.prg"
```

The application smoke uses the existing build's compiler flags and sources,
without invoking `tools/build/r0a.sh build` (which would generate a D81).
The map/ELF is a toolchain seam check, not the M1 memory layout. No technical
repair was necessary or performed. Do not remove the legacy toolchain dependency.

### Implementation readiness findings

- Existing source is under `src/r0a`–`src/r0f`, `src/diagnostics`, `src/platform`,
  `src/input` and `src/audio`. There is no implemented production CoreRuntime,
  FlightDynamics or complete GraphicsEngine to “turn on.”
- [Interface registry](../../interfaces/f65_interfaces.json5) explicitly says
  proof-only. [Platform registry](../../interfaces/f65_platform_abi.json5)
  carries historical unverified/deferred wrapper fields; later private proof
  evidence does not silently turn it into a current production ABI.
  [R0-A ledger](../../memory/r0a-memory-ledger.json) and
  [successor ledger](../../memory/r0f-successor-integration-memory-ledger.json)
  are proof layouts, not allocations for the new engine.
- Canonical B=2, hardware stack $0100–$01FF, base-page $0200–$02FF,
  scoped $8000–$BFFF MAP windows, canonical restoration and protected DMA/IRQ
  ownership are declared contracts. M1 must inventory the exact reused wrappers,
  including A/X/Y/Z/Q/B/P/SP clobbers and vector/NMI restoration; it cannot
  reuse a private proof wrapper by name alone.
- Existing `group1_scene.c` encodes a bounded diagnostic scene; it is not a
  production horizon/projector. `group1_presentation.c` supplies inspectable
  generation/cancellation policy evidence. New Graphics work can begin with
  analytic sky/ground fill and protected numeric text, then sparse projected
  runway geometry under Main §10. No full HUD/MFD, terrain LOD or aircraft art
  is necessary for that slice.
- Java/Python host tooling and the verified compiler supply a reproducible
  oracle route. Physics §12.1 defines numeric semantics, but production numeric
  registry, frame primitives and independent high-precision/bit-exact physics
  references still need implementation. Missing future features are not
  proof of a broken host toolchain.
- Existing CI is documentation/static hygiene only. This task does not claim
  hosted CI, a target boot, emulator, physical or human acceptance PASS.

Documentation validation and final scope results are recorded in §9.

## 4. Proposed Phase 0 exit / Phase 1 entry checklist

**Phase 1 entry: APPROVED CONDITIONALLY — adoption must first be integrated
into verified main.** The founder approved the decisions below; they are
retained as the exact review checklist, not requests for repeat approval.

1. Founder explicitly retains bounded A/B/C/D/E/P09/Group 2 dispositions, with
   no full R0-F technical PASS and no fabricated configuration facts.
2. Founder approves rows Q/S/P/D/C/I/T/V/M as foundation/demo obligations,
   A/L/R at first owning-feature/full-harness acceptance, and E's bounded
   provenance limitation. Each enabled feature must meet its own gate.
3. Founder approves the coordinated §5 sequence/entry amendment and separate
   adoption transaction. Until adopted, Main §18.4 still prohibits early flight.
4. Founder admits an M1–M2 **non-flight development profile** and authorizes the
   concrete first Build Intent in §8. Compiler/generator availability is checked;
   M1 records the pinned JDK choice, actual wrapper inventory and generated
   development ledger before target implementation.

Items 1–3 are the true present admission blockers. Item 4 is next-task scope
authorization, not missing platform evidence. Full aircraft geometry, coefficient
sets, FCS gains, combat capacity, AI doctrine and final audio are not empty-M1
entry requirements.

Before M3 begins, a separate founder decision names the development airframe,
limited flight envelope and physical/numeric error criteria. Do not demand this
aircraft design before drawing sky/ground. Before M6 acceptance, close actual
enabled-profile timing/input/world-age/stack/reserve evidence and qualified
handling review; missing values cannot be replaced by invented numeric bars.

Formal closeout wording proposed for approval:

> Close the Phase 0 work program for entry into the explicitly limited
> development profile, retaining bounded technical evidence and the named open
> obligations in this plan. This is an entry-contract change, not a declaration
> that full R0-E/F coverage or measured limits passed. Reassign only the listed
> obligations to their named owner gates. Unlisted MUSTs remain in force.

## 5. Exact reviewed coordinated amendments — A1–A6 APPROVED

The founder authorized the versioned adoption transaction with new corpus
identities. The following approved text is retained verbatim as its comparison
source. Predecessors remain unchanged and Runtime remains NOT FINAL. No
mechanics, ownership, 100 Hz, 21-stage order, pool capacity or protected-reserve
change is authorized.

**A1 — Main §17.8: append; add the following §17.9.**

> For the separately approved development profile in §18.5, implementation may
> begin before full production measured-limits closure. Each increment records
> actual resource use and unresolved limits; no observed R0 synthetic maximum is
> a shipping budget. Approval of this profile does not approve a production limit.
>
> **17.9 Bounded Phase 0 program exit.** Entry into §18.5 requires explicit
> founder disposition of the retained R0 evidence and each outstanding row in
> the approved 65Aero Phase 1 entry plan. An obligation reassigned to a production
> owner remains mandatory at that owner's named gate. Full R0-F technical PASS
> must not be inferred from bounded program closeout. Fresh configuration and
> hardware evidence are required when new implementation invalidates inherited
> proof; historical tested carriers are not replayed to fill administrative gaps.

**A2 — Main §18.1: replace first paragraph; §18.3: append qualifier;
§18.4: replace final sentence; add §18.5.**

> Phase 1 progressively constructs the production-shaped 65Aero architecture.
> It begins with the explicitly limited development profile in §18.5 and retains
> the full integrated-harness closure in §18.4.
>
> The prohibition on production aerodynamic coefficient authoring in this
> section does not prohibit separately approved, versioned test-only aircraft
> data for §18.5. Such data does not admit a production F-65A.
>
> Full Phase-2 production admission does not begin until the integrated harness
> passes. The limited development work in §18.5 is the sole early-flight exception.
>
> **18.5 Developer Flight Demo progression.** Under individually approved Build
> Intents, develop M1 visible foundation, M2 registered runway/camera, M3 test-only
> aircraft data and mathematical references, M4 real limited-envelope airborne
> 6DOF, M5 physical takeoff/circuit/landing, and M6 bounded physical developer-demo
> acceptance. Each milestone preserves existing owners, the exact 100 Hz
> 21-stage timeline, deterministic state, generated interfaces and protected
> reserve. M1/M2 make no flight claim. M3–M6 use an explicitly approved development
> data revision and envelope. M6 requires actual enabled-profile timing, memory,
> input, fault, presentation, replay and qualified-pilot/founder evidence.
> This progression is not the full §18.4 harness PASS, full Phase-2 acceptance,
> combat-capacity admission or release acceptance. Unimplemented owners remain
> explicitly disabled/bounded stubs; later subsystem gates remain mandatory.

**A3 — Main §19: replace opening paragraph only.**

> Phase 2 completes and admits the actual F-65 aircraft model using Physics
> v4.0 as detailed authority. The limited development implementations permitted
> by §18.5 may be reused after their evidence is reconciled with the full
> integrated harness, approved aircraft data and all Phase-2 acceptance
> requirements. Developer-demo completion does not satisfy that admission.

**A4 — Gameplay §0.4: append; §21: insert §21.10.**

> The separately approved Main §18.5 development profile permits a limited
> non-release Developer Flight Demo. It does not waive the product behavior or
> acceptance scenes in this supplement.
>
> **21.10 Developer Flight Demo acceptance.** M1/M2 may show clearly labelled
> non-flight diagnostics with sky/green ground, a registered runway and numeric
> telemetry. Altitude is on the left and airspeed on the right, each with
> reference/units and validity. Absent states are omitted or marked NOT
> IMPLEMENTED. Camera/test-pattern values are never represented as flight.
> M4/M5 controls act through actual actuators, forces/moments and contact.
> M6 demonstrates takeoff, circuit, landing and an observable fail/abort path
> on an identified physical MEGA65 within the approved test-only envelope,
> with replay/render independence and actual enabled-profile resource/fault
> evidence. Qualified-pilot handling assessment and founder disposition are
> separate. Full §§21.1–21.9 product acceptance remains required at its owning
> later gate; developer-demo approval is not production F-65A admission.

**A5 — Runtime v1.1 amendment: add R7, controlling only the following clauses.**

> In base §20.1 replace the first paragraph with: “Phase 1 builds the
> production-shaped runtime progressively, beginning with Main §18.5's limited
> development profile. Full integrated-harness acceptance remains §20.5.”
>
> Append to §§19.4 and 20.4: “Development-profile increments record actual
> code/state/stack/DMA/timing costs and unresolved measured limits. They may
> proceed only under the approved row-specific entry disposition. Production
> budgets and the combined-load acceptance profile are not inferred from a
> single-aircraft demo or R0 synthetic timing.”
>
> Append to §§20.2–20.5: “The scope, full active-simulation ledger and complete
> harness criteria here remain mandatory for full Phase-1 PASS. Main §18.5
> permits smaller development increments and limited flight work before that
> PASS; each has generated owner accounting and its own evidence gate. Missing
> subsystem records cannot be labelled complete or charged to reserve.”
>
> Replace §21.1's opening sentence as amended by R1 with: “Phase 2 completes
> production Physics v4.0 and aircraft-system behavior and admission behind
> the proven interfaces, using approved aircraft data; Main §18.5 separately
> permits earlier test-only development implementations.”
>
> Append to §22.1: “The §18.5 development profile may exercise actual limited
> flight before full Phase-2 admission; its evidence remains explicitly scoped
> and does not pass the ordinary production cruise scene.”
>
> No other base clauses, §23 FINAL freeze requirements or candidate status change.

**A6 — Physics §15.1: replace second paragraph only.**

> Production admission remains governed by the core three. Main §18.5 separately
> permits progressive Phase-1 Developer Flight Demo work using approved,
> versioned test-only data and a limited envelope. The schema, high-precision
> reference, bit-exact numeric, target, resource and handling gates in this
> paper still apply to the behavior claimed at each increment. Full Phase-2
> acceptance still supplies the validated production aircraft model and data.
> Shared 3DOF primitives do not authorize early weapons or combat scope.

The founder's decisions are thus separable: row dispositions/program exit;
A1–A6 adoption; M1–M2 development profile; later M3 envelope/data authorization;
later measured limits and M6 handling/demo acceptance. This review requests
the first three decisions, not advance aircraft-data or hardware acceptance.

## 6. Minimum architecture and executable milestones

Paths below are **proposed new production ownership**, not claims that modules
already exist. Existing proof source remains evidence. Reuse policy/math only
through a narrow reviewed extraction or dependency with regression coverage;
never copy the entire P09 harness into a game.

| Owner / proposed path | Contract for the first relevant slice |
| --- | --- |
| CoreRuntime / `src/core/` | Sole 100 Hz tick and 21-stage dispatch; ordered commands/events, lifecycle, checksums, replay, deadline debt and publication. Disabled stages remain explicit no-op slots with no fabricated state |
| PlatformABI/MemoryAccessABI / `src/platform/` | Startup/ABI, protected MAP/B/stack/vector restoration, timer/IRQ and DMA arbitration; ordinary C cannot change MAP/start hardware DMA or use arbitrary physical pointers |
| InputEngine / `src/input/` | Device edges -> tick-tagged semantic commands; presentation-only diagnostic camera commands separated from authoritative commands; no direct aircraft-state writes |
| EnvironmentEngine / `src/environment/` | One canonical NED datum, terrain/runway query geometry; later shared gravity/wind/atmosphere with declared sampling time |
| ControlAndSystemsEngine / `src/systems/` | Stage 5 supply/engines, stage 6 FCS/trim, stage 7 actual surfaces. Commands, capability, actuator positions and physical result stay distinct |
| FlightDynamicsEngine / `src/flight/` | Stage 8 force/moment evaluation and stage 9 sole aircraft-motion update; lag state and reproducible loading caches; stage-10 contact correction through its declared boundary |
| ContactEngine / `src/contact/` | Stage-10 runway/gear response, contact geometry and bounded impulse/correction, no second motion authority |
| PresentationExtractor / `src/presentation/` | Stage 19 legal state/validity/source ages; CoreRuntime stage 21 atomically publishes immutable complete snapshots after stage-20 checksum |
| GraphicsEngine / `src/graphics/` | Snapshot-bound sky/ground, horizon/runway and numeric overlay; complete world store + registration/view/projection pair, bounded yield/cancel, last complete frame retained |
| Diagnostics / `src/diagnostics/flight_demo/` | Read-only counters and explicit non-flight camera fixture; camera is presentation state excluded from authoritative checksum, latched coherently for each world attempt |

Logical interface sources stay under `interfaces/`, generated bindings under
`interfaces/generated/`, owner accounting under `memory/`, host tools under
`tools/`, vectors under `tests/`. Do not hand-author final public structs or
allocate addresses in this plan. The M1 development schema must identify its
scope and preserve the proof registry; it must not claim Runtime FINAL.

**Shared geometry:** Physics §2.3 body +X forward/+Y right/+Z down, NED world,
Hamilton scalar-first body-to-NED attitude. Declare one versioned fixture datum
and runway centerline/endpoints/elevation/width, shared by rendering and later
contact. Altitude is positive up relative to a named datum; AGL is a separate
terrain-relative quantity. Aviation display uses feet/knots; use TAS explicitly
until a valid calibrated KIAS path exists, never label ground speed KIAS.
Do not freeze runway dimensions or camera field of view as aircraft data.
M2 supplies test-only geometry and tolerances; M5 uses the same geometry revision.

**Presentation:** analytic sky and green ground precede projected runway
rectangle/markings. No incomplete screen is exposed. Numeric altitude left,
airspeed right, with heading/attitude/vertical speed/throttle-engine/gear/flaps/
trim/faults only when implemented and valid. Commanded and actual gear/flaps are
separate. M1 camera altitude and any pattern values read NON-FLIGHT DIAGNOSTIC;
unimplemented flight fields read NOT IMPLEMENTED or are absent. No healthy
default instrumentation is invented.

**Measurement home:** each new build's map/symbol/disassembly, generated owner
ledger, static/dynamic stack, protected-reserve checks, timing/DMA/input and
world-age/cadence reports live under its identified `build/flight-demo/` output;
reviewed records go under `docs/evidence/flight-demo/<identity>/` at the relevant
gate. This names an evidence destination, not a new dashboard or a permission
to write evidence for tests not run.

| Milestone and owners / interfaces | Prerequisites and smallest PR sequence | Evidence and observable pass/fail; scope limits |
| --- | --- | --- |
| **M1 Visible foundation** — core/platform/input/presentation/graphics/diagnostics; development command, snapshot, fault/counter and generation contracts | Founder entry/adoption/profile decision; first PR in §8 builds one sky/ground + numeric executable. Follow with narrowly scoped debt/queue/publication hardening only if not already covered | Host determinism/edge/starvation/fault tests; target compile/link/ledger/startup checks; authorized direct-PRG PAL/NTSC Xemu visible proof. Founder sees complete sky/green ground, live tick/command/generation counters, labelled missing flight values. No physical acceptance, aircraft, runtime storage or audio claim |
| **M2 Registered runway/camera** — graphics/environment/presentation; shared datum/runway fixture, registration/projection/view identity | M1 seam; approve test-geometry identity and registration tolerances. PR1 pure transform/clipping/registration + oracle; PR2 bounded renderer/camera integration | Host axis/horizon/clipping/view-change vectors; target fit; Xemu stable projected rectangle/markings and no partial/obsolete frame. Founder moves labelled non-flight camera and checks registration. Physical visual qualification joins M6, earlier only if a named scanout uncertainty requires it. No contact or flight claim |
| **M3 Data and references** — flight/systems/environment, aircraft authoring/compiler/numeric tooling | Founder selects test-only model/envelope, provenance and error criteria. PR1 schema/units/frame/package rejection; PR2 high-precision trim/dynamics reference; PR3 independent bit-exact primitives and deterministic package compile | Host definition/reference/target-data readiness and independent checks; small target-C primitive agreement/fit where claimed. No aircraft executable/physical run required merely to author data. Founder reviews explicit trim/response cases and missing fields; no production F-65A admission |
| **M4 Real airborne 6DOF** — flight/systems/environment/core; forces, mass, actual surfaces, sample-age/override handoffs | M3 admitted development inputs; numeric integrator choice earned by comparisons, not assumed Eq. 9.7 acceptance. PR1 force/air-data path; PR2 integration/actuators/trim; PR3 demo telemetry/replay | Host high-precision versus bit-exact and target golden vectors; target costs; Xemu airborne climb/turn/descent with energy consequences. No-graphics and varied-render-rate identical commands produce identical authoritative checksums, including model identity. Human observes response; qualified/physical final handling belongs M6. No takeoff/landing or full FCS claim |
| **M5 Takeoff/circuit/landing** — contact/systems/flight/graphics; canonical runway, gear/flaps/brakes, contact correction | M4 and approved contact/configuration data/tolerances. PR1 rest/taxi/brake/contact invariants; PR2 real configuration effects; PR3 repeatable circuit and abort fixture | Host penetration/energy/impulse/sign/continuity tests; target bounds/costs; Xemu taxi, rotate, climb, circuit, approach, touchdown/rollout and a failed/aborted attempt. Gear/flaps affect forces/contact rather than animation. Physical/qualified handling acceptance remains M6; carrier/catapult/arrestment deferred |
| **M6 Developer-demo acceptance** — all enabled owners + Diagnostics | Pinned M5 source/data/profile; close C/I/T/V/M and enabled Q/S/P/D/A/L gates; approve measured bars and repeatable handling scenarios before testing. PR sequence: admission/evidence plan; authorized exact carrier/Xemu; separately authorized physical run; review only after results | Host regressions, target maps/stack/resource witnesses, exact Xemu modes, fresh authorized D81/SD/physical chain and recorded actual configuration. Physical takeoff/circuit/landing + fail/abort, input/fault/world metrics, repeat replay; qualified-pilot and founder decisions recorded separately. Failure retains evidence and blocks acceptance; no retries against tested carrier identity. Demo acceptance covers only named envelope/configuration, never full combat/shipping capacity |

All physical/D81 actions require the existing gates and a separate execution
authorization. Xemu is not physical proof. No automatic progression between
milestones is authorized by this planning task. Full integrated-harness work
and later sensors/weapons/AI/mission/campaign remain required, but are not
preconditions for displaying a runway.

## 7. Aircraft-data dependency checklist

Physics §§3, 13–14 govern. The production F-65A lacks approved geometry/reference
area, mass/CG/inertia, full aerodynamic/thrust data and gains. Targets and v3.3
worked examples do not supply them. No values are designed here.

| Input / reviewer-owner | Minimum explicit test-only airborne M3/M4 data | Additional M5 runway/contact data and gate |
| --- | --- | --- |
| Identity/provenance / aircraft author + founder | Model/revision, schema/numeric/Physics identities, sources/licenses, methods, uncertainty, declared test-only scope | Same pinned identity through contact and M6; no silent substitute fighter |
| Frames/geometry / aircraft + environment | Datum, units, body/NED transforms, reference area/span/chord, moment origin, geometry and engine/surface locations | Wheel/gear points and runway frame/elevation/normal; agreed visual/query registration tolerance |
| Loading/inertia / aircraft + flight | Explicit empty contents, selected loading, positive mass/CG and quantization-safe inertia tensor; fuel policy and any allowed variation | Landing/takeoff loads, gear/contact moment arms and CG/datum continuity; no unexplained impulse |
| Six force/moment channels / aircraft + flight | Valid-domain static, dynamic damping and actual control increments for all six channels; approved interpolation/boundary/invalid rules | Flap/gear/ground-effect effects and supported approach/touchdown region; omitted behavior must restrict envelope explicitly |
| Propulsion / systems | Installed thrust direction/moment arm, thrust versus conditions, spool/response and fuel semantics; throttle is demand | Idle/takeoff/approach and abort capability in supported conditions; no throttle-to-speed shortcut |
| Actuators/control / systems | Actual rates/stops/signs, supplies, trim/mixer and direct mode. Augmentation/gains only if separately authored/validated | Actual gear/flap travel/capability, brakes/steering, commanded/actual indicators; absent modes labelled unavailable |
| Environment/air data / environment | Shared gravity/atmosphere/wind with units, domain, validity and TAS/KIAS distinction | Ground-relative tire velocity, runway surface state; wind is not subtracted from tire velocity |
| Contact / contact owner | Not needed for airborne-only tests; prohibit landing claims | Bounded normal/friction response, stiffness/damping/restitution and penetration/energy error limits compatible with 10 ms; stable rest, taxi, touchdown, bounce/abort |
| Envelope/errors / founder + physics reviewer | Explicit altitude/speed/AoA/beta/load/configuration range and out-of-domain response; tolerances by observable, not arbitrary universal percent | Contact/approach/closure-speed domain, abort rules; qualified-pilot scenarios and acceptance limits |
| Validation/compiler / tools + owner | Independent analytic/frame checks, trim/response/energy vectors, high-precision versus bit-exact comparison, overflow/invalid rejection, deterministic compile twice, code/data/residency witness | Contact continuity and target cost vectors; pinned replay identity and physical/human evidence before aircraft-admitted claim |

Definition-ready, reference-ready, target-ready and aircraft-admitted remain
distinct Physics §14.4 gates. For the initial development profile, propose one
fixed loading/configuration region and a land runway, no stores/combat/carrier
systems; the founder must choose its actual bounds. Unknown required input
fails admission. Restricting a domain is an explicit decision, not permission
to fill absent coefficients with zero. Full F-65A, variable sweep, full failure
envelope, carrier and augmented-system completion remain later work.

## 8. Next fresh-window M1 first-PR Build Intent

The following is **ready to paste only after founder decisions and coordinated
adoption**. Approval of this planning packet alone does not execute it.

> **Build Intent — M1 visible 65Aero foundation**
>
> Verify current main, adopted entry/phase decision identities and clean task
> scope; preserve unrelated local state. Create `codex/65aero-m1-visible-foundation`.
> Read current authority, AGENTS, workflow, programming/C standards and exact
> platform contracts. Stop if the entry amendments or named dispositions are
> not adopted.
>
> Build one development-only executable displaying a complete sky and green
> ground with a protected legible numeric overlay: tick, semantic command
> count, published/displayed generation, source tick/age, fault state; altitude
> left and airspeed right labelled NOT IMPLEMENTED. Label the whole display
> NON-FLIGHT DIAGNOSTIC. No runway projection or physics is required in this PR.
>
> Owners/paths: new `src/core/`, `src/presentation/`, `src/graphics/`,
> `src/diagnostics/flight_demo/`; a narrow production `src/input/` seam;
> `interfaces/` generator sources and generated bindings, `memory/` development
> owner ledger, focused `tools/build/` and host/target validators, `tests/`
> vectors. Inspect exact existing platform code before approving any reuse;
> protected ABI changes and edits to retained R0 proof source are out of scope.
>
> Implement the 100 Hz/21-stage dispatcher with explicitly disabled later
> owners, tick-tagged semantic input, deterministic command order and checksum,
> immutable snapshot publication and complete generation-pair display. Never
> divide 10 ms equally across stages. On backlog/fault, expose debt/fault and
> preserve order; never hide it by merging ticks. Renderer yields/cancels
> incomplete work and keeps the previous complete display. Queue exhaustion
> rejects with observable fault and preserves existing/peer state; a held
> snapshot is never overwritten. Hardware acquisition remains behind Platform;
> no production audio or runtime storage dependency in this profile.
>
> Before target edits, generate a development-scoped layout and owner ledger
> from one source, recording byte owners, code/runtime support, stack bounds,
> DMA lists, allowed ranges and untouched reserves. Declare each used wrapper's
> registers/clobbers, CPU/physical ranges, B/MAP, IRQ/NMI/vector and restoration
> behavior. Do not promote R0 private contracts or allocate new public ABI by
> hand. Use the pinned LLVM-MOS profile and explicitly selected pinned legacy
> JDK or a verified local installation of the same lock identity.
>
> Acceptance: deterministic host replay at every tick; exact 21-stage order;
> input press/hold/release and queue rejection; snapshot held-reader/full-slot
> rejection; obsolete/incomplete frame cancellation; presentation-disabled and
> differently paced rendering preserve identical authoritative checksums.
> Target compile/link/map/disassembly and generated-byte consistency must pass;
> show actual code/data/stack accounting and no reserve allocation.
> With this next intent explicitly approved for direct-PRG Xemu, show the
> complete screen and live counters in both PAL and NTSC, with equivalent
> authoritative replay. This is emulator evidence, not physical timing/boot
> acceptance. A missing safe platform seam is a named blocker, not permission
> to modify ABI or restart an omnibus R0 campaign.
>
> Record source/tool/schema/configuration identity and actual checks in the
> normal evidence output, plus absent tiers/limits. No D81/SD/physical work,
> aircraft coefficients/gains, full cockpit/audio, mission/combat/AI, reserve
> borrowing or full-harness PASS. Update WIP to READY FOR REVIEW and stop;
> commit/push/PR/merge require the normal separate founder authorization.

This first PR's on-screen result is deliberately smaller than M2. If platform
admission forces a materially larger change, stop that portion and present its
precise contract issue rather than silently broadening M1.

## 9. Validation, critical risks and review handoff

Documentation/static checks:

- A Python `re.findall(r'\]\(([^)]+)\)', text)` pass over this plan and WIP,
  resolving each non-URL target relative to its document with `Path.exists()`:
  **22 local links PASS**. No link fragments occur in the changed documents.
- `git diff --check`: PASS for tracked changes.
- `git diff --no-index --check /dev/null
  docs/plans/65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md`: no whitespace
  diagnostics (exit 1 denotes the added file's difference, not a whitespace error).
- Final `git status --short --branch` and diff review: only WIP plus this new
  plan are task changes; all 20 pre-existing untracked status entries remain.
  No historical carrier was opened, hashed, mounted or retested for this audit.
- No JSON/Python/shell source was modified, so their broad syntax suites and
  CI policy fixtures were not rerun. The actual corpus/configuration validator
  and narrow generator/oracle/compile checks are recorded in §3. Hosted CI was
  not triggered.

Final scope review checks each named Group 2 destination/tier, preserves the
fault and provenance limitations, keeps every amendment and reassignment
proposed, and separates M1 visibility, full harness, aircraft admission and
M6 acceptance. No additional general governance artifact or technical repair
was required.

| Critical risk | Owner / closure gate |
| --- | --- |
| Nominal clock evidence, unknown whole IRQ/input/world-age bars and production cost may not meet deadlines | Platform/CoreRuntime/Graphics; instrument M1, approve evidence-supported bars and close physical uncertainty by M6. No synthetic budget promotion |
| Resident/code/stack and hot-table fit may fail well before full combined load | Every owner; generated/link accounting at each PR, exercised stack before acceptance, full simulation ledger at harness gate; reserve never a donor |
| Fixed-point/interpolation/integrator errors can disguise unstable physics | Flight/numeric tooling; independent high-precision/bit-exact/target vectors and approved errors before M4/M6 claims |
| Runway/display/contact frames or CG rebasing can diverge | Environment/Graphics/Contact/Flight; same geometry revision and source generation, M2 registration then M5 energy/contact continuity |
| Missing airframe data or unapproved approximations can produce plausible but false flight | Aircraft author/founder/qualified reviewer; staged Physics §14.4 readiness, explicit test-only envelope, no F-65A truth or handling acceptance inferred |

No target execution, Xemu, D81 operation, SD access, physical MEGA65 run,
new production implementation, aircraft design, commit, push, PR or merge
occurred in this task. Existing proof artifacts and generated bindings remain
unchanged. Recommended next action: founder dispositions and A1–A6 review,
then a separately authorized adoption transaction and the M1 intent above.
