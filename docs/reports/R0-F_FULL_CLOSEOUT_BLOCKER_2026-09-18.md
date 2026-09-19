# Full closeout implementation review — 2026-09-18

Status of this earlier review: **NOT IMPLEMENTED / NOT READY FOR ANOTHER HARDWARE RUN**.

Subsequent owner disposition (2026-09-18): **resume without restarting or
reloading**. Development has resumed as RH001 using documented public KERNAL
initialization and file-I/O routines, not a reset primitive or guessed private
KERNAL fields. See `../decisions/R0-F-RH001-NO-RESTART-HANDOFF.md` for the
bounded experiment and `R0-F_RESUME_HANDOFF.md` for its actual test status.
The remainder of this document preserves the earlier review, not a new
request for the already-granted development authorization.

The owner requested the full closeout harness, Xemu verification, and the
corresponding physical test. This review does not satisfy that request. No new
target, D81, Xemu execution, SD operation, or physical execution was performed.
The verified CF001 physical retest remains valid within its recorded scope.

## Required platform boundary

Frozen Architecture 1.4.1 §2 permits ROM calls after display-store reclaim only
when the platform explicitly restores the ROM's required environment. The
current `interfaces/f65_platform_abi.json5` still marks R0C-PLAT-ROM-001 deferred.
Its CF001 entry authorizes a separate **reset-only** experiment, not a usable
ROM/storage return.

`src/diagnostics/r0f/combined_platform.c` verifies restoration of the 128 KiB ROM
contents and write protection. `combined.c` then remains in its capture viewer;
it never restores the pre-launch BASIC/KERNAL working state, vectors, timers,
stack or storage environment. The full closure plan explicitly retains the
post-reclaim storage transition as unfinished. Byte equality alone cannot close
that requirement.

The repository requires stopping at an undocumented hardware dependency rather
than inventing its behavior. No private KERNAL-memory reconstruction or guessed
return sequence is admitted by this review.

## Restart alternative checked, not selected

The retained official source attributed to core
`b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f` supplies a restart operation:

- [dos.asm](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/hyppo/dos.asm):
  trap `$00:$7E` dispatches to `reset_entry`.
- [main.asm](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/hyppo/main.asm):
  `reset_entry` resets mapping, stack and machine state; `go64` establishes
  reset-vector entry and erases `$0800-$08FF`.

This is a restart, not evidence of a returning storage call preserving the
running diagnostic/application context. The proposed successor's capture and
state-retention contract would have to account for that distinction explicitly.
No restart experiment was executed or claimed successful.

The official [ROM changelog](https://github.com/MEGA65/mega65-rom-public/blob/main/CHANGELOG.md)
documents a warm-boot/second-program-launch KERNAL API added in ROM **920416**.
The photographed hardware uses **920413**. This finding does not establish
that an upgrade is necessary or sufficient, nor authorize installing one. The
same changelog warns that private KERNAL-memory access is unsupported.

## What needs resolution

Before implementing the post-reclaim storage portion, establish a documented
and reviewed transition for the existing platform, or obtain explicit owner
approval for a changed platform/lifecycle strategy. Any proposed replacement
must specify retained state, storage API, clobbers, canonical public exits,
failure lockout, capture survival and Xemu/physical tests. It must not promote
reset-and-reboot evidence into a returning-call claim.

This is not another request to authorize the already-approved full proof
program. It identifies an unresolved platform contract inside that program.
No architecture revision, ROM upgrade, acceptance waiver or production behavior
is selected here. Renderer, input, phase/window and timing work also remain
unfinished; resolving this dependency alone will not finish the harness.

## Inspected scope and impact

Read the official record first; complete frozen Architecture 1.4.1; approved
Read-First and current approval/AD-001; candidate Architecture 1.5.1, Engine 0.2
and Gameplay 0.2; all current memory ledgers, public/interface registries and
R0-B–F contracts; the B-register calling-convention decision; CF001 generated
headers, C/model/platform sources, IRQ/trap assembly, linker and build runner;
R0-F closeout/combined/admission/stage records and full closure plan; R0-C ROM
research; and the root D81 loadability gate.

Changed paths: this report and the full closure work-plan pointer only.
Register/clobber, CPU/physical memory, MAP/base page, DMA, IRQ/NMI, stack,
timing/deadline and generated-target impact: **none**. Existing dirty evidence
and documentation were preserved. No new module, layout, reserve allocation,
hardware API, target result, or gate pass is introduced.

Validation: source/contract comparison and `git diff --check`; target build,
new host functional tests, Xemu, SD and physical tiers **NOT RUN** in this review.
No commit or push.
