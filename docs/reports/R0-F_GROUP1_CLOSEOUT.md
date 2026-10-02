# R0-F Group 1 campaign closeout — 2026-10-01

## Disposition

The owner requested analysis and closeout of this long-running work unit before
publication/review and a fresh chat for the remaining R0-F work. Close the
development campaign as a **preserved checkpoint with a physical blocker**,
not as a successful Group 1 hardware result or full R0-F acceptance.

Local fit, host and exact-carrier Xemu evidence pass. P05 SD delivery and
physical entry pass. The one physical run fails at post-storage display resume
after tick 1600. Actual returned-card SAVE is independently verified; no
physical trace was exported. No correction or further test is part of closeout.

| Evidence tier | Outcome |
| --- | --- |
| Resident fit and prior native host checks | PASS; `$BFFD`, 3 bytes free |
| Four exact-name P05 Xemu boots | PASS; 3200 records and 20 chunks per run |
| SD hash / allocation / safe eject | PASS; one 819200-byte extent |
| Physical chooser and entry | PASS; owner confirms P05, photo shows execution |
| Physical returning SAVE | PASS; actual 34-byte `RSSTATE`, tick-1600 golden |
| Physical resumed workload | FAIL; `$5D`, state `$0A`, tick `$0640` |
| Physical trace / timing reduction | UNAVAILABLE; no `G1Txx` files |
| Group 1 acceptance / full R0-F acceptance | NOT GRANTED |

This is administrative closure of the present campaign, not a waiver of the
failed resumed-workload requirement. Its correction and physical proof are
explicit carry-forward work. Measured-limit approval and Phase 1 remain separate.

## Authority and changes

Inspected AGENTS.md, CURRENT_STATE.md, the complete pre-closeout WIP,
[development workflow](../DEVELOPMENT_WORKFLOW.md),
[Group 1 Build Intent](../plans/R0-F_GROUP1_BUILD_INTENT.md),
[measurement matrix](../plans/R0-F_GROUP1_MEASUREMENT_MATRIX.md),
[export amendment](../plans/R0-F_GROUP1_EXPORT_AMENDMENT.md), original generated
successor lifecycle, frozen version-7 implementation and validation tooling,
root D81 gate and D81 workflow. The latest owner request authorizes analysis,
local evidence preservation and a compact closeout/handoff. Commit, push, PR
and merge are the subsequent review/publication step, not performed here.

Changed scope: this report, the physical evidence packet, current WIP and
explicit do-not-repeat disposition links in the local P04/P05 handoff reports.
The 994-line WIP is preserved byte-for-byte as `WIP-before-closeout.md`; routine
WIP now contains only the current review task. Historical reports and twelve
prior freezes are not rewritten. CURRENT_STATE.md is unchanged because this
checkpoint has not merged and does not establish a new integrated acceptance.

Target source, generated interfaces, public ABI and capacities are unchanged.
Registers/clobbers, CPU-visible/physical allocations, MAP/base-page, DMA,
timing/deadline and IRQ/NMI effects of closeout are **non-applicable**. Only
off-card evidence and an ignored local P05 retirement guard are added. No SD
write, unmount/eject, target rebuild, Xemu launch or new hardware run occurred.

## Exact identities

- Branch: `codex/r0f-successor-physical-exact-carrier`.
- Published preservation checkpoint: `2d9a42e110cdd9066031e28e83662ce4fdec6219`.
- Qualified version-7 PRG: 37517 bytes, SHA-256
  `c068cc532dc820845d8c0649b1c2ea7dfc0bda394b32f7c186088a04d0dc048b`.
- P05 canonical/pre-run SD D81: 819200 bytes, SHA-256
  `046198fc400988abd7e92d384db9efbb13d0ef0f0c77ede346d6942cf75ee4ff`.
- Actual returned P05 D81: SHA-256
  `9816043f16eccad79c833419f19655ea0234d61be48854bae1d82a90fcf4197d`.
- Actual `RSSTATE`: 34 bytes, SHA-256
  `7d2f63b8e8e970bb35c351174fae1ca365245f14acf35db0d3cf9016ba8ba5bd`.
- Original `ec259fc7...` baseline and all passing/failed predecessors remain
  unchanged. P04 remains retired for its ten-extent allocation failure.

The latest target source is the published isolated snapshot at
`docs/evidence/r0f/group1/2026-10-01-capacity-summary/experiment/runtime-01/source-checkpoint/`.
Root working source is an earlier passing variant, not this target; do not
rebuild it and assume it reproduces P05. The live isolated build remains at
`build/r0f/group1/capacity-summary/integrated-02/source-inputs/`.

## Physical data analysis

Owner installer output reports clean read-only pre/post filesystem-check
completion, mounted verification and safe eject. File count increases 147 to
148 and free space falls by 800 KiB / 200 4-KiB clusters, consistent with one
new 819200-byte image. That arithmetic is corroboration, not contiguity proof:
the retained raw staged/final records independently show one extent at device
offset 62275584 and the exact canonical hash.

The owner confirms the photo is the file created, `R0FG1P05.D81`. It reads
`FAULT 5D / STATE 0A / TICK 0640 / MASK 00 / NMI 00`. Running banner plus
explicit filename confirmation establish physical entry, not runtime success.
Current run video mode and fresh core/ROM/HYPPO/Freezer identities are not
recorded; do not infer them from the emulator or older hardware records.

The returned removable FAT32 volume matches UUID
`83FFC12E-67E1-307F-91AD-E584C2E01E87`, currently `disk4s1`. A host-only snapshot
was copied without modifying the mounted file and then compared again.
Independent chain/BAM parsing and pinned `c1541` extraction agree. Exactly
four closed entries exist: `AUTOBOOT.C65`, `R0FSUCC`, `TOKEN`, `RSSTATE`.
All three original payload hashes match canonical. No trace chunks exist.

`RSSTATE` loads at `$3063`; its 32 payload bytes exactly match the independent
host model at tick 1600, checksum `6B765FDB`, and the declared checksum/index
encoding. It also equals the returning SAVE in every retained P05 Xemu run;
the physical bytes were read from the card, never substituted from Xemu.
The changed post-run D81 hash reflects the added SAVE, not candidate drift.
There is no actual physical 512-byte terminal result or complete timing trace
to validate, and no Java full-result oracle PASS is claimed.

## Exact failure boundary and remaining uncertainty

In the frozen `src/diagnostics/r0f/successor_integration.c`, lines 1101-1103
call `lockout(93u)` when `display_resume()` rejects: decimal 93 is `$5D`.
The IRQ override codes are 105/106, not 93. Reaching this branch follows the
storage return/status and readback/TOKEN checks, context/DOS/low-memory restore,
CRC/model/base-page/CPU-port checks, context invalidation and ROM reclaim.
The photograph therefore identifies a **program resume failure**, not chooser
`FF`, fragmentation, pre-acquisition stall or terminal SAVE collision.

`display_resume()` has three rejecting paths: suspended/outstanding-DMA state,
staging seeding, and the buffer-clear DMA loop. Its generic `$5D` overwrites
the lower-level fault, so the exact rejecting path is not recoverable from
this photo or disk. No instruction-level physical stall is claimed.

The specific leading hypothesis is clock/restart ordering: display clear uses
`cfdma()`, which calls `cfnow()` on CIA1 `$DC04-$DC07`, before `cfclock_begin()`
at line 1106 reinitializes the application clock after KERNAL. Its bounded
reader can fail with code 3, which this handler masks. This is a demonstrated
ordering hazard, **not a physically confirmed inner fault**. Existing audio
ordering correction does not protect these earlier display DMA timestamps.
Also, `cfclock_begin()` starts IRQs: moving it earlier without reviewing the
resume/IRQ contract is not an automatically safe correction.

Clock restart, audio restart and resumed tick 1601 are not reached on this
branch. The zero resumed-service mask is consistent with this boundary;
it is not proof that all services individually failed. Fault suppresses
terminal trace export, explaining the absent `G1Txx` files.

## Fresh closeout checks and preserved observations

- Actual card snapshot/extraction, original payload comparisons and independent
  tick-1600 SAVE oracle: PASS; see the evidence packet's returned verification.
- Unchanged release identity/current allocator qualification and staged/final
  SD hash/one-extent/safe-eject records: PASS. No new raw-card extent audit or
  filesystem check was performed; their pre-run records remain the authority.
- Twelve prior freezes: all 7511 entries match. Passing root/P02/P03 input
  sets (93/95/133), all 134 P05 inputs and four original PRGs match.
- All four retained P05 traces re-reduce with their frozen **version-7**
  decoder: PASS, 3200 records, 955 NTSC / 807 PAL world pairs, nominal timing
  `WITHIN_OBSERVED_BOUNDS`. The first audit accidentally used the older root
  version-5 decoder and correctly rejected the length; selecting the matching
  frozen decoder resolved the tooling mismatch without changing a trace.
- `python3 -B -m unittest discover -s tools/diagnostics -p 'test_r0f_group1_*.py' -v`:
  47 tests PASS. This is fresh host evidence, not a new emulator/hardware run.
- `python3 -B tools/diagnostics/test_d81_delivery.py`: 18 host tests PASS;
  disposable fixtures only, no card access.
- JSON, paths/links, frozen manifest, retirement rejection and
  `git diff --check`: recorded in the evidence packet's closeout validation.

The prior fit/native-sanitizer and four boot observations remain historical
evidence. They do not replace the failed physical run or establish SI accuracy,
whole-ISR/entry latency, external input/audio latency, universal phase coverage,
production renderer behavior or universal worst-case pool pressure. These are
existing stated boundaries, not newly added Group 1 feature requirements.

## Publication and next-chat handoff

Review and publish this closeout as **development checkpoint; physical resume
blocked**, never "Group 1 hardware PASS". Preserve evidence-bearing commit
history. Include this packet and WIP plus the P04/P05 handoff reports; do not
stage unrelated SD backup/mirror tools, reports or older physical directories.
Commit/push/PR/merge require their intended next-step authority and fresh
branch/remote/CI review. This closeout neither performs nor certifies them.

The next chat needs only AGENTS.md, CURRENT_STATE.md, compact WIP, this report,
the original Build Intent and the relevant named contracts before task work.
Do not reconstruct the campaign from the archived WIP or replay passing tests.

1. First carry-forward task: isolate the physical `$5D` subfault and correct
   the post-storage restart path in a **new copied-source experiment**. Use
   a bounded narrow diagnostic; the earlier 30-minute/two-experiment discipline
   is the recommended initial cap. Preserve first-fault identity and review
   CIA/IRQ ordering. No extra feature, capacity or acceptance-threshold change.
2. Require fit/host checks before focused changed-build NTSC, then PAL and
   exact-carrier gates. Three free resident bytes are not expansion headroom.
   Any later physical retest needs a fresh identity and separately approved
   SD/hardware delivery; P05 is retained **INVALID — DO NOT USE**.
3. After that blocker and actual resumed-workload evidence are resolved,
   continue only the originally approved remaining R0-F campaign/Groups 2-3
   and reconcile existing admission/matrix boundaries. Do not invent a new
   production feature checklist. Owner acceptance and measured-limit approval
   remain named decisions, not implications of a Git merge.

Evidence: [physical closeout packet](../evidence/r0f/group1/2026-10-01-physical-closeout/README.md).
