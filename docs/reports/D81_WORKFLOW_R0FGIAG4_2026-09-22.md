# D81 workflow recovery — R0FGIAG4

**Subsequent physical result: FAIL — INVALID, DO NOT USE.** The owner supplied
a chooser-FF photo after copying GIAG4. The host/emulator results below remain
historical; they did not establish successful delivery. See
`D81_GIAG4_ALPHA_COMPARISON_2026-09-22.md`. Do not follow the earlier handoff
to copy or retest this identity.

## Build intent and authority

Owner request: reconstruct a repeatable D81 workflow, document mandatory
engineering requirements in AGENTS.md and appropriate engineering documents,
and build exact `R0FGIAG4.D81` before further R0-F physical tests.

Inspected authority: AGENTS.md, CURRENT_STATE.md, WORK_IN_PROGRESS.md,
DEVELOPMENT_WORKFLOW.md, root D81 loadability gate, private successor
diagnostic build/contracts, existing builders/auditors, retained physical and
emulator evidence, and the supplied raw FAT audit. The owner explicitly
authorized the workflow/gate documentation amendments.

This task changes host construction/delivery tooling and engineering rules.
No additional target C or private/public ABI change was made for GIAG4.
Registers/clobbers, CPU-visible and physical memory, MAP/base-page, DMA,
timing/deadlines, IRQ/NMI: unchanged from the existing T06 diagnostic. The
earlier uncommitted T06 code remains intact and is not attributed to this
workflow-only change. No publication, merge, full R0-F acceptance or wider
architecture work is authorized.

## Root cause established at the delivery layer

The exact failed Finder copy passes internal structure and has the expected
hash, but occupies 13 FAT extents. Native `R0FDIAG3.D81` and the previously
hardware-mounted host carrier each occupy one. Apple FSKit source ignores
the contiguous allocation flag. The old workflow's assumption that a
successful preallocation request guaranteed contiguity was wrong. This is
not a finding that the SD card is defective, nor a claim that FF alone
identifies fragmentation.

See `D81_NATIVE_COMPARISON_2026-09-22.md` and its retained raw audit.
The replacement uses a genuinely contiguous free-run allocator from official
MEGA65 tools, pinned by source and executable hash; it does not depend on the
owner manually creating another native blank.

## Changed responsibilities

- `AGENTS.md`, `00_D81_LOADABILITY_GATE.md`, `docs/DEVELOPMENT_WORKFLOW.md`:
  mandatory repeatable construction/allocation/verification requirements.
- `docs/D81_WORKFLOW.md`: operational build, qualification, permission,
  transfer and physical-test procedures and explicit limitations.
- `r0f_successor_physical_diagnostic.py`: explicit validated `--name`, fresh
  per-identity output/evidence, no overwrites, deterministic label and same
  T06 payload. Canonical made read-only; writable emulator copies separated.
- `d81_direct_delivery.py`: pinned official allocator wrapper; bounded
  preflight, metadata retention, staging/rename, independent raw audits,
  FSInfo accounting, optional explicitly authorized unmounted-card route.
- `d81_fat32_audit.py`: optional directory enumeration for collision checks;
  existing default diagnostic behavior unchanged.
- `test_d81_direct_delivery.py`: real-executable fragmented-volume fixtures,
  whole-partition preservation checks, independent read-only filesystem check
  and fail-closed cases. No SD device access.
- `toolchain/d81_delivery.lock.json`: official allocator identity and hashes.
- WIP and retained evidence: truthful status and next gate.

## Artifact identity

```text
D81_FILENAME: R0FGIAG4.D81
D81_BYTES: 819200
D81_SHA256: 90a819f49c5b6cb3bf66f71317c1f40e3cae3f4059fb422b46b05589e86915fa
D81_STATE: XEMU_BOOT_VERIFIED
DISK_LABEL: R0FGIAG4
DISK_ID: 65
ENTRY_FILENAME: AUTOBOOT.C65 -> R0FSUCC
TARGET_PRG_BYTES: 21921
TARGET_PRG_SHA256: 3ce9aeb1029676465d47755145ec31d6b30ab2ca0c8ae95dc88e9703dd99446b
SOURCE_BRANCH: codex/r0f-successor-physical-exact-carrier
SOURCE_COMMIT: ae2b397698cc7197d03349e57cd058b4fb9f3987
SOURCE_STATE: working tree; exact accounting input hashes retained
HOST_STRUCTURAL_RESULT: PASS
HOST_CONTENT_RESULT: PASS
XEMU_RESULT: PASS
SD_COPY_SHA256: NOT RUN
SD_CONTIGUITY_RESULT: NOT RUN
SD_EXTENT_COUNT: NOT RUN
SD_EXTENT_EVIDENCE: NOT RUN
SD_SAFE_EJECT_RESULT: NOT RUN
PHYSICAL_CHOOSER_RESULT: NOT RUN
PHYSICAL_RUNTIME_RESULT: NOT RUN
```

Canonical: `build/r0f/d81-workflow/R0FGIAG4/canonical/R0FGIAG4.D81`.
Retained release/accounting/screens/result/SAVE evidence:
`docs/evidence/r0f/successor/2026-09-22-workflow/R0FGIAG4/`.
The source is not claimed as a newly committed/published freeze.

## Validation performed

1. `python3 -B tools/diagnostics/r0f_successor_physical_diagnostic.py all --name R0FGIAG4.D81`
   — PASS. Rebuilt target, 1,527,534 lifecycle checks and 16,842,752 RH001 states;
   fresh one-session D81; structural and all-payload extraction/hash checks;
   two NTSC plus two PAL exact-name/pre-run-hash Xemu boots with result/SAVE
   verification. NTSC/PAL final screenshots visually inspected.
2. `python3 -B tools/diagnostics/test_d81_direct_delivery.py --qualification build/r0f/d81-workflow/R0FGIAG4/allocator-qualification-2.json`
   — 11 tests PASS. Three successive real-tool contiguous allocations in a
   deliberately fragmented local partition; exact content and no unrelated
   byte changes; `fsck_msdos -n` PASS. Includes source drift and upstream
   zero-exit/error-output rejection. Qualification report retained in evidence.
   The unsuffixed report predates final dependency pinning/release-record
   completion and is retained as superseded, not the current qualification.
3. `python3 -B tools/diagnostics/test_d81_delivery.py` — 18 tests PASS.
4. `python3 -B tools/diagnostics/r0a_validate.py .` — PASS. An initial invocation
   without the required repository argument failed at argument access, then
   was corrected; it made no changes.
5. `git diff --check` — PASS.

All Xemu screens show fault `00`, state `09`, tick `0042`, service mask `1F`,
NMI `00`, and equal reserve CRCs `3C7D60D8`. Result CRC varies by run. These
are emulator observations, not physical runtime results.

## Unresolved boundary and handoff

No SD file was written, renamed, removed or filled in this task. The owner
prohibited automatic CLI transfers; that remains respected. The direct
allocator's real-card unmount/write/remount path has not been exercised on
this card. Fixture success is not hardware qualification. Supported geometry
is deliberately narrow: mirrored FAT32, 512-byte sectors, 4KiB clusters,
root cluster 2. Missing contiguous space or pre-existing filesystem errors
stop the method without authorizing card repair. Raw writes are not atomic
against power loss; metadata snapshots are not a full-card backup.

The canonical path is ready for owner-controlled copying, but that copy is
not yet a gate-passed physical test image. After a copy, obtain a read-only
raw hash/extent audit and safe eject; or separately authorize the documented
direct allocator. Then verify physical chooser and entry load and retain a
photo of the diagnostic values. Do not advance wider R0-F testing or claim
that physical loadability is solved until that gate passes.
