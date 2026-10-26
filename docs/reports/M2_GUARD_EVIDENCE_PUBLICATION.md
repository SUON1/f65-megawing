# Accepted P2 host correction — evidence-only publication

25 October 2026. The founder accepted the guard-test evidence-isolation
correction for its reported host-test scope, then explicitly chose **exact patch
and sealed host evidence only**. This publication records that acceptance.
The active M2 implementation remains in its original development worktree.

The correction makes generated guard source, host executable and logs temporary.
Packet file-set/member/inventory checks cover successful execution, intentional
compilation failure and guard exit 17. All 13 reported host regressions passed.
Those accepted tests were not rerun for publication; their exact source and
results are retained in the [publication packet](../evidence/flight-demo/2026-10-25-m2-guard-evidence-publication/README.md).

The test-only unified diff is stored losslessly as JSON lines. A deterministic
archive retains all ten correction-packet members plus their inventory without
normalizing bytes. A read-only packaging check verifies the archive, decoded
patch, source before/after, unchanged positive C fixture and accepted log.
The original complete diff, including historical WIP context, remains inside
the archive and is not applied to main. There are no CI exception changes.

Publication starts from verified main
`44e4c09050a7d3282ea7c3e577d6cdd9124f2a18`, whose exact push CI
[39863685756](https://github.com/SUON1/f65-megawing/actions/runs/39863685756)
passed. Main has none of the minimum-renderer test/startup/stack/timing
dependencies. No active `src/`, `tests/`, `tools/`, generated-interface or memory
ledger change is included. New packaging verification is evidence tooling only.
Registers/clobbers, CPU-visible and physical memory, MAP/base-page, DMA,
target timing/deadlines and IRQ/NMI effects are not applicable.

Latest **preserved development-candidate evidence**, separate from main:

| Gate | Reported result and boundary |
| --- | --- |
| Startup | PASS: canonical MAP/MB/B/Z/port and hardware/software stacks precede BSS |
| Whole-program stack | PASS: 50/256 hardware including IRQ/NMI, 127/4,096 software; separate trap 3; static resident scratch 77 |
| Renderer service | PASS for pinned normal 40.5 MHz PAL/NTSC Xemu, eight bounded slots and runtime guards; no complete-frame cadence acceptance |
| Resident fit | **FAIL: 26,750 / 24,575 bytes; deficit 2,175; reserve zero** |
| Xemu | PASS direct-PRG NTSC/PAL **diagnostic only**; complete scene and camera response observed; multi-second frames |

These outcomes belong to `2026-10-25-m2-runtime-admission`, inventory SHA-256
`d5fce59c011225643d27d884454c7b7982e7a99dfbd4e1af598a4a4fb200a245`,
in `/private/tmp/f65-m2-minimal-runway-renderer`. PRG SHA-256 is
`10c6b083bd37392b8177d3211035a76c599894aa46bb11ff4a18851e97dab6e1`.
The profile is reset-only, excludes external NMI injection and stops below the
clock half range. It does not establish full M2, Graphics v2.1, physical timing
or resident-memory admission. The original 1,991-byte-deficit failed packet
and all later outcomes remain preserved, without regrading.

The **single next technical blocker is resident fit**. The smallest next task
is a bounded whole-program residency/load-contract admission against this exact
working diagnostic: choose one owner-correct placement/lifetime strategy,
account recovery of at least 2,175 bytes plus every added code/data/alignment/
stack/service cost, and obtain the founder's versioned contract decisions before
implementation. The existing code-bank/protected-MAP/boot-load drafts remain
unadopted. Their nine pure bodies total 4,374 bytes, giving only 2,199 gross
bytes before overhead in this candidate; this arithmetic is not measured fit.
No new optimization experiment or architecture implementation starts here.

Publication validation consists of exact-byte packaging, syntax, links,
preservation, source-scope/static hygiene and exact-head CI. It creates no new
host-oracle, target, runtime or emulator admission. No relink, Xemu, D81,
SD-media or physical test was performed. After review checks and integration,
verify main's exact bytes and CI, report the scoped gates, then stop.
