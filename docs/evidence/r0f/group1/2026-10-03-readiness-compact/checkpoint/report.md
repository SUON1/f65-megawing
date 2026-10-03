# Group 1 compact readiness reporting — 2026-10-03

The owner authorized a size-focused revision after the first readiness
candidate exceeded resident memory by 18 bytes. A fresh copy now fits with
**4 bytes free**. Only two failure-screen strings changed from that candidate;
22 bytes of read-only text were removed. This enables a specific first-failed
readiness code while preserving all integrity checks. The physical cause of
P07's terminal-readiness failure remains unknown.

## Authority and implementation

Inspected current state/WIP, repository workflow and programming/C standards,
original Group 1 Build Intent, approved terminal-export amendment, qualified
P07 source, prior named-predicate diagnostic, generated interfaces and memory
bounds, linker/disassembly and existing host/carrier tools. Remote main is
`c27d89787d1d5c4472e24262e0181c47943d46be`; branch remains
`codex/r0f-group1-resume-clock`. The new request authorizes this local revision
and its existing validation gates. No SD write, physical run or publication
is included.

The source is
`build/r0f/group1/terminal-recovery/readiness-compact-01/source-inputs/`.
It derives from preserved readiness-01; only these two literals change:

- `GROUP 1 LOCKOUT - NO ACCEPTANCE` becomes `G1 FAIL - NO ACCEPTANCE`.
- `RESET TO EXIT - RETAIN FAILURE` becomes `PHOTO THEN RESET`.

Fault, state, tick, mask and NMI fields retain their positions and widths.
The existing development/non-acceptance banner remains. The linker reports
unchanged executable and protected-section sizes versus readiness-01; only
`.rodata` shrinks 22 bytes, shifting following sections. No second new target
variant was required. Earlier failed builds remain preserved.

Qualified PRG: 37516 bytes, SHA-256
`1c842e345a3d5ec15b3eb167535a776da5e78eaf26a0d0d6239f7073f5a3b468`.
Resident exclusive end: **$BFFC**. Four free bytes are not expansion headroom.
Root target source is unchanged and does not reproduce this candidate.

The existing protected status byte at $2F98 reports the terminal rejection.
The pure diagnostic policy introduced in readiness-01 returns zero on success;
the existing boolean interface wraps it and preserves state transitions.
All acquisition, DMA, display, audio, IRQ, ROM, capsule, NMI and byte-bound
predicates remain. Capture and transport executable-token comparisons pass
when only the diagnostic reporting adapter is removed.

| Fault at terminal boundary | Rejection |
| --- | --- |
| 6B | Preparation before detailed readiness reporting |
| 70 | Invalid export policy state or null export |
| 71 | Null readiness object |
| 72 / 73 | Acquisition not stopped / DMA not empty |
| 74 / 75 | Display / audio not stopped |
| 76 | IRQs not masked |
| 77 | ROM restoration status |
| 78 | Export capsule guard, copy or CRC verification |
| 79 | NMI seen |
| 7A / 7B | Empty export / capacity exceeded |

Interpret these only for this new exact PRG and terminal context. Earlier
fault codes retain their prior meanings. No new physical code has been seen.
Capsule code 78 still groups its guard/copy/CRC checks.

Hardware impact: ordinary C compiler clobbers and the existing status byte.
No additional register access, physical allocation, MAP/base-page, DMA,
clock, deadline or IRQ/NMI policy changes. Reporting occurs after acquisition.
Public/generated ABI, capacity, reserves and ownership contracts are unchanged.

## Validation

Pinned compile/link and protected IRQ/terminal static checks pass. Exact
patch replay, full input identities and generated/memory contract identities
pass. Native ASan/UBSan owner/scene/workload/audio/display/pool/CRC and resume
checks pass, including 83 codec rejects. The dedicated readiness validator
passes 18 actual extracted transport cases (mocked physical edges), plus
2,624,256 differential policy comparisons against the original P07 implementation.
The readable host-test revision was rerun in a fresh host output directory;
no target bytes changed. All 47 Group 1 Python regressions pass.

Focused NTSC and PAL pass complete 3200-record, 327680-byte exports in 20
chunks, actual returning SAVE, version-7 independent reduction, corruption
and capacity rejection checks. Nominal timing is WITHIN_OBSERVED_BOUNDS with
zero recorded misses and low-cadence cohorts. Screens show S:4 E:00 F:14.
These remain emulator observations, not physical timing or acceptance.

The unchanged-PRG export collision case passes: existing bytes are preserved,
no retry occurs, and S:5 E:03 F:00 is shown. Fresh R0FG1P08.D81 construction and
independent extraction/structure checks pass. All four clean exact-name boots
(two NTSC, two PAL) pass complete exports, actual SAVE, independent version-7
reduction, corruption and capacity checks. Each carrier screenshot is byte-
identical to its inspected focused-mode success screenshot.

P08 canonical: 819200 bytes, SHA-256
`9e2030ef8f45077aa29890e60b4d904e37b14b15115e9a6b1611eb0b44849abe`.
Path: `build/r0f/group1/carriers/R0FG1P08/canonical/R0FG1P08.D81`.
State: **XEMU_BOOT_VERIFIED only**. Canonical bytes remain unchanged and were
never mounted writable. No SD installation or physical run occurred.

The retained commands use `r0f_group1_resume_recovery.py host/qualify
--experiment build/r0f/group1/terminal-recovery/readiness-compact-01`, then
`r0f_group1_readiness_validate.py` with that experiment and
`r0f_group1_readiness.py verify/ntsc/pal/negative-export/carrier-build/
carrier-boot/carrier-finish`. Exact invocations and artifacts are frozen in
[the evidence packet](../evidence/r0f/group1/2026-10-03-readiness-compact/README.md).
They are provenance; do not rerun into existing evidence directories.

## Handoff

P07's actual returned SAVE and original payloads pass, but physical trace
export failed at 6F. It remains retired, as do P06/P05 and earlier tested
identities. This candidate diagnoses the first readiness rejection; it does
not claim to correct that physical condition. SD allocation, exact-copy hash,
safe eject and physical chooser/entry remain separate gates for any later
owner-approved delivery. Group 1 and full R0-F acceptance remain ungranted;
Group 2 has not started. CURRENT_STATE and prior freezes remain unchanged.
