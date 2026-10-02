# R0-F Group 1 P05 delivery preparation — 2026-10-01

## Later disposition — do not repeat the installer or hardware run

Owner-run installation passed exact hash, one extent and safe eject. The owner
confirms selecting P05; its photographed physical runtime fails
`5D/0A/0640/00/00` at post-storage display resume. Actual returned-card
`RSSTATE` is independently verified, original payloads are unchanged and no
trace chunks exist. P05 is retired **INVALID — DO NOT USE**; preserve the
tested SD copy. See [campaign closeout](R0-F_GROUP1_CLOSEOUT.md).
All preparation states and the command below are historical, not instructions
to retry, repair, overwrite or retest P05.

## Outcome and authority

Fresh `R0FG1P05.D81` is **XEMU_BOOT_VERIFIED only**. Host structure/content and
four clean exact-name boots pass. All three contained payloads are byte-identical
to P04, including the qualified version-7 PRG. This corrects delivery identity
after P04's ten-extent Finder allocation failure; it is not a program correction.
The fresh images differ only at offset 399371, the label's final `4` -> `5`.
P05 was freshly formatted and populated once, not patched or renamed from P04.

Owner replied "Begin" to approval of this new identity and an owner-run pinned
allocator transfer. The agent has made no SD write, unmount or eject. Preserve
failed P04 and all passing/failed predecessors; no card repair, reformat,
overwrite, native blank, automatic transfer, commit/push or merge is included.
The approved bounded physical Group 1 test remains separate and may proceed
only after SD gates, safe eject and physical chooser/entry verification pass.

Inspected authority: AGENTS.md, CURRENT_STATE.md, WORK_IN_PROGRESS.md,
development workflow, Group 1 Build Intent and generated export/trace contracts,
root D81 loadability gate, D81 workflow, carrier admission/controllers and the
pinned allocator lock/wrapper/qualification. No target source or generated
artifact changes. Registers/clobbers, CPU-visible/physical memory, MAP/base-page,
DMA, timing/deadlines and IRQ/NMI remain unchanged. Only the later owner-run
installation may add the new carrier and its required FAT/FSInfo metadata.

## Exact identity and retained records

- Canonical:
  `build/r0f/group1/carriers/R0FG1P05/canonical/R0FG1P05.D81`, read-only,
  819200 bytes; label `R0FG1P05`, ID `65`.
- D81 SHA-256:
  `046198fc400988abd7e92d384db9efbb13d0ef0f0c77ede346d6942cf75ee4ff`.
- PRG SHA-256:
  `c068cc532dc820845d8c0649b1c2ea7dfc0bda394b32f7c186088a04d0dc048b`.
  37517 bytes, resident end exclusive `$BFFD`, 3 free bytes; unchanged fit.
- Entry: `AUTOBOOT.C65` loads `R0FSUCC` on device 8, entry `$31A6`.
- Branch `codex/r0f-successor-physical-exact-carrier`; source checkpoint
  `2d9a42e110cdd9066031e28e83662ce4fdec6219`. The qualified isolated source
  and its prior freeze remain the source authority; root code is not replaced.
- Host gate, capacity admission, release manifest, screens, actual SAVE/trace,
  reductions and negative cases:
  `build/r0f/group1/carriers/R0FG1P05/`.
- `release.json` is derived from those actual records, not synthesized target
  results. Its allocator-compatible `ntsc-1`/`ntsc-2`/`pal-1`/`pal-2` labels
  retain the corresponding `group1Run` names and evidence directories.
- Retained current-pin allocator qualification:
  `build/r0f/cap14-allocator-qualification-1.json` (16 fixture tests).
- Failed P04 audit:
  `build/r0f/group1/physical/R0FG1P04/sd-copy-01.json` — exact hash, ten extents.
  P04 is retired; neither it nor its audit may be overwritten or retried.
- Original passing `ec259fc7...` PRG and P04 canonical hashes were rechecked
  unchanged. Every older source/PRG/carrier remains preserved.

## Validation commands and results

From the repository root:

```sh
python3 -B tools/diagnostics/r0f_group1_capacity_carrier.py build --name R0FG1P05.D81
python3 -B tools/diagnostics/r0f_group1_capacity_carrier.py boot --name R0FG1P05.D81 --mode 1 --number 1
python3 -B tools/diagnostics/r0f_group1_capacity_carrier.py boot --name R0FG1P05.D81 --mode 1 --number 2
python3 -B tools/diagnostics/r0f_group1_capacity_carrier.py boot --name R0FG1P05.D81 --mode 0 --number 1
python3 -B tools/diagnostics/r0f_group1_capacity_carrier.py boot --name R0FG1P05.D81 --mode 0 --number 2
python3 -B tools/diagnostics/r0f_group1_capacity_carrier.py finish --name R0FG1P05.D81
python3 -B tools/diagnostics/test_r0f_group1_capacity_carrier.py
python3 -B tools/diagnostics/test_d81_delivery.py
git diff --check
```

All PASS. Targeted tests: 2 capacity-carrier admission and 18 delivery tests.
Each boot uses a fresh exact-name copy and disposable local SD fixture, no
direct PRG injection and a 120-second capture allowance. Canonical never runs
writable. Each actual exported stream is 327680 bytes / twenty closed files,
3200 ticks, complete capacity checks and 114 corruption rejects (30 existing,
72 pool, 12 capacity). NTSC retains 955 actual world pairs; PAL retains 807.
All report `WITHIN_OBSERVED_BOUNDS`, zero nominal deadline misses, uncertain
boundaries and below-floor cohorts. All four actual screenshots were inspected:
readable `S:4 E:00 F:14`, status legend, reduce/not-acceptance/reset and green.
The terminal export summary is not a physical timing PASS or acceptance.

The unchanged `d81_direct_delivery.verify_release` admits the actual canonical
and release record; `require_qualification` matches all current tool inputs.
No new target build or 180/360-second run was needed. These results do not prove
current physical-card filesystem health, allocation or hardware behavior.

## Explicit owner-run installation

Current read-only identity is removable Secure Digital MS-DOS FAT32 at
`/Volumes/MEGA65FDISK`, UUID `83FFC12E-67E1-307F-91AD-E584C2E01E87`.
P05 `.D81` and `.TMP` names were absent during preparation. The installer must
resolve the device again, refuse any name/alias collision and recheck UUID.
Current live filesystem health/free-run/allocation remain **NOT VERIFIED**.

This command writes to the identified card after its safety gates pass.
Run it **once**, with no concurrent card operations, leaving the card connected
and the Mac powered. Enter the administrator password only in local Terminal.
Do not copy P05 in Finder or create another blank.

```sh
cd /Users/slice/Developer/f65-megawing &&
sudo /usr/bin/python3 -B tools/diagnostics/d81_direct_delivery.py install-sd \
  build/r0f/group1/carriers/R0FG1P05/canonical/R0FG1P05.D81 \
  --manifest build/r0f/group1/carriers/R0FG1P05/release.json \
  --mount /Volumes/MEGA65FDISK \
  --volume-uuid 83FFC12E-67E1-307F-91AD-E584C2E01E87 \
  --qualification build/r0f/cap14-allocator-qualification-1.json \
  --report build/r0f/group1/carriers/R0FG1P05/sd-install-01 \
  --confirm-raw-write
```

The helper checks identical FATs, qualified layout, no existing final/staging
name/alias, spare directory slots, a sufficient actual contiguous free run,
non-forced unmount and clean read-only filesystem check. It preserves original
metadata off-card before allocation. It then stages `.TMP`, verifies exact raw
hash/predicted one extent and unchanged unrelated metadata, renames without
rewriting, checks again, repeats read-only filesystem validation, remounts and
independently reads back before safe eject. It is not power-loss transactional.

Success ends with:
`SD copy, one extent, mounted hash and safe eject PASS; physical chooser pending`.
Report back the output; the agent must review actual
`sd-install-01/sd-release.json` before issuing the physical handoff.
Any error or stall stops: do not retry, repair, overwrite, reconnect during
writing or select another filename. If failure leaves the card unmounted,
leave it that way and report the exact phase. No automatic fallback.

SD installation, one-extent proof, safe eject, physical chooser/entry, the
bounded hardware run and actual returned-byte reduction remain **NOT RUN**.
Full Group 1/R0-F acceptance remains separate; Groups 2/3 are not added here.
