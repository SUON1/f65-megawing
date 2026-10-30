# Option B first composed lean renderer — failed fit gate

29 October2026. Identity65AERO-M2-LEAN-1. Branch
`codex/65aero-m2-option-b-lean-renderer`, verified main
`9570f0ab427121a4e8f042041a14c89aaaeff9e2` after PR29 and main CI40940731306 PASS.
Option A is rejected and RF-EX2 not adopted. This is actual unbanked source work.

**STOP: resident fit FAIL.** The single complete candidate link uses33,395 of
24,575 allowed bytes: deficit8,820, a556-byte regression from32,839.
No second link, further optimization or Xemu follows. This increment is not
recommended as a resident-fit improvement; its source and failure are retained.

## Source behavior and exact comparisons

Graphics prepares one full-precision affine horizon origin per generation,
then advances it by exact Q46 additions across pixels, rows and tiles. The
predicate is the same integer expression as the public ground classifier.
Its legal coefficients are conservatively bounded below2^47 in magnitude;
origin and legal traversal (including final unused increments) stay below2^58,
well inside int64. No division, rounding or narrowing is introduced. Projection
still prepares/caches the nine selected segments once per generation; the
existing raster cursor, complete hidden frame, registration pair, cancellation,
held snapshots and transfer/commit failure policies are unchanged.

Telemetry uses a private bounded row recipe and shared numeric field selection.
Required labels, hexadecimal counters, signed camera values, source age and
5x7 glyphs remain byte-identical. No public or generated interface changes.
New private horizon state is24 target bytes, charged to BSS; all other owners,
reserves, input/replay, 100Hz/21stage authority and hardware seams are unchanged.
Launch and all target grants remain zero. No compiler/flag change or banking.

Whole-program review: current M2 already shares transform/project code, so there
is no measured duplicate-geometry recovery credit. M1 offers row/hidden-store
publication patterns already represented here; its fixed-row background cannot
preserve M2 camera pitch/roll registration. The previous26750-byte running
diagnostic is represented only by its pinned published evidence; its full
implementation source was unavailable in the inspected current source trees.
Its6,089-byte difference from this baseline is not recoverable savings or a
source import authority. No missing historical source was reconstructed.

## Measured target accounting

| Allocation | Baseline | Candidate | Delta |
| --- | ---: | ---: | ---: |
| BASIC prefix |22|22|0|
| Text |29711|30218|+507|
| Text/rodata alignment |2|7|+5|
| Read-only data |1439|1459|+20|
| Initialized data |0|0|0|
| BSS |1475|1499|+24|
| Compiler static scratch |190|190|0|
| Resident union |**32839**|**33395**|**+556**|
| Deficit |8264|8820|+556|

Range[$2001,$A274), including BSS/noinit. Renderer700 target bytes versus676;
host736 versus712. Hardware/software stack envelopes remain256/4096, dynamic
whole-program bounds UNPROVEN. Reserve0; display/Color RAM/ROM-backup allocations
unchanged. PRG31708 bytes, SHA-256
`bb170147072970594c301d279a91e7963071f1fca80f60e4419f74884ac0ba03`.

The exact linked symbol deltas explain the text change:

| Area | Linked code delta |
| --- | ---: |
| Horizon preparation (`prepare`) |+617|
| Tile/row advancement (`copy_tile`) |+586|
| Background sampling |+275|
| Removed target `m2_ground_prepared` |−700|
| Horizon subtotal |**+778**|
| Telemetry formatter |−794|
| Shared field selector |+593|
| Hex / decimal / removed label helpers |+10 / −3 / −77|
| Telemetry subtotal |**−271**|
| Total text change |**+507**|

The remaining20 rodata bytes include16 recipe pointers; horizon state adds24.
Full-width recurrence reduces repeated work but increases this compiler's code
for preparation/advancement. No runtime cycle savings are claimed without
admission evidence. Core/Input/Environment/Platform and exact projection/math
symbol sizes remain unchanged; the wide multiplication helper remains linked.

## Evidence and gate outcomes

[Host packet](../evidence/flight-demo/2026-10-29-m2-option-b/host-1793302504990999000/):
31 contract/startup/SDK host tests PASS; ASan/UBSan frame/camera/cancellation/
held/fault/replay PASS (DE675132). Additional36-camera horizon traversal compares
all1,474,560 samples against the unchanged full-width public predicate.
Frozen independent geometry oracle3,857 and near/far841 cases PASS, plus
existing prepared/cursor checks and16 policy fixtures.
[Text packet](../evidence/flight-demo/2026-10-29-m2-option-b/text-1793302574153355000/):
1,152 exact rows and128 glyphs match the pre-change formatter from verified
main, compiled separately under ASan/UBSan.

[Single target packet](../evidence/flight-demo/2026-10-29-m2-option-b/target-1793302615810967000/):
compile/link PASS; actual resident fit FAIL. The unchanged retention list then
also reports `incomplete target composition` because it still requires the old
`m2_ground_prepared` symbol, intentionally replaced in the linked path by the
host-proved affine traversal. This is a stale structural assertion, retained
as the actual outcome; it was not bypassed, repaired or relinked. All other
listed components remain linked. Current startup/stack/service admission is
not completed or claimed; the failed fit already prevents execution.

The reused validator records its legacy source-origin `base=b044440...`;
its actual `head=9570f0a...` and measured input hashes identify this source.
This experiment's verified branch parent is9570f0a. The origin field is not a
claim that the source was compiled from the older commit. The new identity and
fresh root preserve prior claims/evidence; full SDK inventory is unchanged
after the link. The actual compiler and all flags are the pinned baseline ones.

**First mandatory blocker: resident extent$A274 exceeds$8000 by8,820 bytes.**
The candidate cannot proceed to startup/stack/service or PAL/NTSC Xemu admission.
No D81, SD or physical tests; no banking/memory exception or further code-size
campaign. Stop for founder review of the actual source changes and failed link.
Option B source remains uncommitted; earlier rejection publication is complete.
