# Minimum renderer P1/P2 corrections — READY FOR REVIEW

Correction packet: `65AERO-M2-MIN-REBUILD-CORRECTIONS-1`. Private development
profile remains `65AERO-M2-MIN-REBUILD-1`; generated records/ledger and public
M1/M2 interfaces are unchanged. Branch remains
`codex/65aero-m2-minimum-renderer-baseline` from verified main
`b044440fa98c2dfc91ec590668049610afc98a1e`.

Founder authorized exactly the reviewed P1 and both P2 repairs, affected checks
and one target relink. All three corrections are implemented. This is source
review readiness, not runtime or full M2 acceptance.

## Corrected behavior

**P1 — terminal interrupt handler.** The early sink now contains absolute
`JMP m2rb_early_stop` after `SEI`. Raw bytes in the new PRG are `78 4C 7E 22`
at `$227E`, so the jump targets `$227E`. The old image's `78 83 FC FF` is retained
and rejected by the extended checker: its long-relative branch reached `$227D`,
the preceding RTS. The sink remains four resident bytes in both measured images.

The full startup check now requires raw PRG bytes and independently checks the
handler's exact opcode and destination. It refuses missing/truncated bytes,
relative/indirect branches, off-by-one destinations, RTS and fallthrough.
Normal-entry prefix checking remains separately named so historical prefix PASS
does not imply a terminal-handler PASS. The historical replay now explicitly
records the old handler FAIL in a fresh packet; original evidence is unchanged.

MAP/megabyte selectors, EOM, B/base-page, CPU-port, stack, I/O and IRQ/NMI vector
setup are unchanged. No new clobber, physical allocation, DMA, bank window,
restoration exception or interrupt service is introduced. Normal linked-entry
ordering and terminal closure PASS; complete asynchronous startup remains
UNPROVEN. No target execution was performed.

**P2 — source-age provenance.** `AGE AT TEXT` now means authoritative tick minus
this candidate's copied snapshot tick at the first telemetry-construction
quantum. That value is frozen through the remaining telemetry and commit delay.
It is not claimed to measure eventual/current display age. `F` is the adjacent
fault counter; both NOT IMPLEMENTED flight labels remain unchanged.

CoreRuntime supplies an immutable tick value through the private dispatch API;
Graphics computes the age using its own captured snapshot. The previous-front
calculation is removed. No public ABI or record layout changes. The private
field is renamed `source_age_at_text` without changing workspace size.
A tick preceding the candidate's source fails closed before publication.

New host regressions cover source 42 measured at 50 (age 8), a deferred commit,
and source 100 measured at 105 (age 5, instead of previous-front age 63), followed
by an invalid backward measurement that preserves the last completed pair.
Both successful generations use their own source identity. The clock remains
100 Hz; tick order, replay and the 21 stages are unchanged. All service grants
remain zero, including the modified TEXT operation's unproven cost.

**P2 — SDK identities.** A shared read-only helper inventories the entire
installed SDK: **833 regular files, 166 directories and 140 confined symlinks**,
1,139 entries total. This includes all driver configurations, C64/platform
includes, Clang resource headers and compiler runtime libraries. File bytes,
sizes and modes, plus literal/resolved link identities, are recorded.
External, dangling, cyclic and unsupported entries fail closed. Files changing
during capture are rejected. No SDK binaries are copied into the packet.

The pre-link inventory is sealed with the new result and is verified unchanged
immediately after linking and during final checks. Existing compiler and objdump
lock hashes remain enforced. Canonical SDK identity digest:
`4166ea6e185bc8471593336e0ac691b784fb5c0a51f861a1c26463c1609bbfd4`.
The original packet retained only a subset; its prior complete-input wording is
superseded for that historical image. No retroactive full-SDK identity or
repeat-relink proof is claimed for the original image.

## Validation and measured accounting

Evidence: [correction packet](../evidence/flight-demo/2026-10-27-m2-min-rebuild-corrections/).
Actual commands and input identities are in each sealed `result.json`.

| Check | Actual result |
| --- | --- |
| Private contracts, startup mutations and SDK identity regressions | 27 tests PASS |
| ASan/UBSan renderer, camera, cancellation, held snapshots, faults, age and replay | PASS, checkpoint `DE675132` |
| Integrated geometry / prepared-context / raster cursor checks | PASS, including 3,672 prepared segment comparisons |
| Independent Decimal geometry oracle | 3,857 cases PASS; unchanged tolerance |
| Independent near/far regressions | 841 cases PASS; unchanged tolerance |
| CI policy unit tests | 15 PASS; no hosted CI for this uncommitted increment |
| Full target compile/link | PASS, exactly one invocation |
| Raw terminal closure and normal-entry prefix | PASS on the new exact PRG |
| Full SDK pre/post-link identity | PASS, unchanged |
| Whole-program stacks / renderer service | UNPROVEN, no admission grants added |
| Resident fit | FAIL retained; 8,264 bytes over the 24,575-byte ceiling |

The host packet is `host-1793167637309996000`. The single target packet is
`target-1793167696482111000`. The create-once `relink-claim.json` prevents another
link in this authorized packet root. Future separately authorized rebuilds can
use `--evidence-root` with a fresh root; no prior packet need be removed or edited.
The historical replay is `historical-replay-1793167739912661000`, without relinking.

| Allocation | Before | Corrected | Change |
| --- | ---: | ---: | ---: |
| BASIC/entry prefix | 22 | 22 | 0 |
| `.text` | 29,756 | 29,711 | -45 |
| Alignment before `.rodata` | 5 | 2 | -3 |
| `.rodata` | 1,435 | 1,439 | +4 |
| `.data` | 0 | 0 | 0 |
| `.bss` | 1,475 | 1,475 | 0 |
| Compiler `.noinit` scratch | 190 | 190 | 0 |
| **Resident union** | **32,883** | **32,839** | **-44** |
| **Deficit** | **8,308** | **8,264** | **-44** |

Corrected resident range is `$2001–$A047`, end `$A048`. The 24,575-byte acceptance
ceiling is unchanged. Renderer workspace stays 676 target bytes (712 host bytes).
Hardware stack envelope remains 256 bytes, base page 256 bytes and software stack
4,096 bytes. Dynamic/whole-program stack safety remains UNPROVEN: the unchanged
checker refuses unaccounted software-stack-pointer writes. No stack or compiler
scratch saving is claimed from the code-size change.

No optimization experiment was performed. The compiler and target flags remain
unchanged; the 44-byte net difference is the actual composed correction result,
including the private dispatch argument and telemetry changes. No second link
or speculative size work followed the failed fit gate.

PRG: **31,176 file bytes**, SHA-256
`1873c76d7b13f438244d5c3f99d8c80bc951af47cda9fc5ba9a6fadbeb4eda51`.
File size is not resident usage; BSS and scratch are charged above.

Display stores remain 63,552 bytes each, immutable Color RAM 2,000 bytes, existing
ROM backup 131,072 bytes, and protected-reserve consumption **zero**. Inherited
M1 result storage `$1900–$1FFF` and initialization message `$09E0–$0A14` remain
explicit unchanged dependencies in `memory/m1-development-ledger.json`.
No other owner band, reserve, banking or staging allocation is introduced.

## Preservation and handoff

The exact reviewed 29-file source/doc baseline is retained in
`before-source.tar.gz`, SHA-256
`6aece6681643d5dfd49308d74ad008a0a5ee123bf0700c2e63424fda9a1d6ee8`.
`before.json` pins all 61 original packet files. Original failed host attempts,
unsafe/oversized PRG, verifier failures, reports and seals remain unchanged.
Final checks retain byte and member verification results for original/new sealed
packets, the original checkout's 480 modified/untracked path identities, branch
ancestry and focused changed-file scope. The prior aggregate inventory encoding
is not reconstructed; explicit current file identities are compared directly.

Historical recovery remains 22 verified / 15 unresolved members. Eight old
checkouts remain NOT VERIFIED at the Git-worktree tier. No missing file or Git
metadata was reconstructed. Unrelated paths and the approved design checkout
remain preserved.

Runtime launch, all eight operation budgets and the guard budget remain zero.
No banking, Xemu, D81, SD or physical tests, commit, push, PR or merge occurred.
Recommended next action: founder review of these three corrections and retained
fit failure. Any publication or subsequent engineering requires its own scope;
no further optimization or banking work starts automatically.
