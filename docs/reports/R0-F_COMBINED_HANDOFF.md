# CF001 combined hardware-candidate handoff

2026-09-18. **COMBINED EXPERIMENT BUILT; FULL R0-F NOT COMPLETE.**

Current objective disposition: `R0-F_ORIGINAL_OBJECTIVES_STATUS.md` records
the completed bounded CF001 proof objectives, its immutable candidate identity
and the later no-restart integration gap. The physical evidence folder holds
the post-manifest SD/runtime/capture records; do not rewrite the original
pre-physical release manifest to make its historical state appear current.

Subsequent physical retest verification: corrected photo transcription passes
result CRC32 `32B8A599` and raw CRC32 `105995A3`. The freshly compiled,
unchanged Java oracle validates 2640 samples, 80 windows and 30 resealed
negative cases. Four real key edges were detected and four consumed; the
owner confirms A exercise. ROM/reserve checks pass, with zero acquisition
faults. Current phase-3 verification and remaining parent-scope gaps:
`docs/evidence/r0f/combined/physical/2026-09-18-retest/corrected/REVIEW.md`.
The earlier requests below for missing pages/input exercise are satisfied
by this retest. Do not repeat the SD fill or ask for another transcription run.

Physical update, later on 2026-09-18: SD fill completed with matching candidate
hash, one unchanged extent and successful OS eject. Owner photos show CF001
acquisition complete, fault 00, reference 02, restored ROM 02 and 2640 ticks;
the owner reports audible sound. Real key edges are zero. Raw pages 01–0E
and independent hardware reduction remain pending. Evidence:
`docs/evidence/r0f/combined/physical/2026-09-18/REVIEW.md`.
The pre-SD delivery statements and one-time fill command below are historical:
**do not repeat the fill for this run**. Capture the current raw pages first.

This is actual integrated C/45GS02 code, not the earlier PF001 primitive-only
PRG. It adds reset-only ROM backup/reclaim/recovery, nominal clock-ratio and
measured comparison-work calibration, a populated synthetic 21-stage fixture,
immutable snapshots, incremental complete-buffer display, DMA, raster IRQ,
real keyboard-matrix edge latching and SID/PCM warning preemption.

The bounded acquisition checks do not satisfy every full-parent acceptance
requirement. In particular, production ROM-hosted storage return, independently
quantified physical-clock uncertainty, the complete production-shaped mesh/terrain
scene and semantic-input corpus, all relative/rolling-window phases, IRQ response
and per-module ceilings remain open. The 530000 comparison includes the model
and measured filler; additional input/audio/HUD/extraction costs are measured
in tick records, not silently included in that nominal calibration number.
No scope waiver or gate pass has been inferred from the request to prepare it.

## Exact candidate and delivery state

- Candidate: `build/r0f/combined/F65BLK02.D81`, 819200 bytes.
- SHA-256: `b13853a7ddaf3bf26dfcaceb7e4466ab2d58702b96bfcbe9ae62c7db56ed3d82`.
- PRG SHA-256: `163579294c45994c647a02efc190c94e53d4df7149ae234d44357ec97ac08530`.
- Disk label/ID: `F65 CF001` / `65`; files: `AUTOBOOT.C65`, `R0F-PROOF`, `R0F-EVID`.
- Source baseline: `744920dd76d008fbc0ccce82e006cc0b647f477e`, dirty
  `codex/r0-f-development`; per-input hashes in `accounting.json` are authoritative.
- Host independent BAM/chain/ownership and all extracted payload comparisons: PASS.
- Direct-PRG NTSC/PAL acquisition and independent Java: PASS; 14-page byte-for-byte
  screen export/import: PASS. Exact-D81 repeated boots: **two NTSC plus two PAL
  PASS**, each with 2640 samples, zero acquisition faults, full restored-ROM
  hash agreement and independent Java reduction. All four original screenshots
  have matching intact identification/label rasters. Three additional NTSC
  diagnostic runs also pass; see `VISUAL_REVIEW` in the release manifest.
- Physical SD: **NOT WRITTEN**. F65BLK02 native blank is 819200 bytes, empty,
  consistent BAM/directory, SHA-256
  `ba963e2c0e8dd686e03568b41ca9d4c6196762e166a2de8a6fcbb829dd5bd4e8`.
  Extent and safe eject remain unverified. F65BLK01 is untouched/ineligible at
  688128 bytes. The sudo preflight reports that a user password is required.
- Authoritative release state: `build/r0f/combined/manifests/r0f-d81-release.json`.
  Retained immutable pre-SD evidence: `docs/evidence/r0f/combined/SHA256SUMS`.
  No physical chooser, hardware run or R0-F acceptance is claimed.

## Engineering evidence

Native ASan/UBSan tests pass model/checksum, immutable snapshots, queue overflow,
range guards, all 1..4096-byte DMA encodings, 6092 exact rational vectors, and
10000 short/held/repeated press-release pairs plus simultaneous-bit latching.
These raw edges are not the full semantic-command/joystick/context corpus.
Independent Java validates 2640 samples, 80 cohort reductions, golden checksum
`D9EEAB81`, ROM/reserve agreement, actual service counters, stacks, explicit
clock-reference class and 30 resealed semantic corruptions per run.

Final direct-PRG observations:

| Observation | NTSC | PAL |
|---|---:|---:|
| Acquisition / fault / ROM state | 7F / 00 / 02 | 7F / 00 / 02 |
| Total ticks | 2640 | 2640 |
| Normal cadence, nominal source-model Hz | 27.327 | 24.289 |
| Deliberate renderer-lag cadence, nominal Hz | 3.028 | 3.030 |
| Comparison workload estimate, nominal CPU clocks | 530887 | 525001 |
| Absolute comparison residual | 887 | 4999 |
| Largest measured DMA interval, raw CIA counts | 289 | 288 |
| Largest observed audio service gap, raw CIA counts | 21152 | 23937 |
| Hardware / software stack canary observation, bytes | 58 / 73 | 58 / 73 |

Cadence is aggregate for a small synthetic scene, not a complete minimum-frame
or shipping scene-budget proof. Lag deliberately holds rendering and continues
ticks/services; it is not an accepted production 3Hz tier. Audio gap retains
cohort transitions and tick/quantum blocking; no hardware latency limit is
invented. A zero consecutive-read delta is timer quantization, not zero cost.
Both independent restored-ROM hashes match the complete original 128KiB ROM
SHA-256 `af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0`.

The initial packaging wrapper failed while decoding c1541 PETSCII output as
UTF-8, after the image had been written. No D81 was patched or appended.
Independent structure/content checks passed. A fresh one-session reconstruction
in `construction-replay/` captured raw stdout/stderr, exited 0 without diagnostics,
and reproduced the candidate **byte for byte**. `construction-replay.json` and
`construction.log` close that reporting gap. Do not rerun `package` on this
existing identity; use the retained exact artifact.

An image-preview rendering initially appeared to omit text. Inspection of the
original PNG pixels disproved missing text: ten complete constant-label rows
match byte-for-byte across all four gate boots (with the PAL vertical offset).
Three further runs, including clean UART exits and a non-headless launch,
match those rasters. Three live observations per diagnostic also find all
2000 color bytes equal to 1 and unchanged complete screen RAM. This was a
preview concern, not an observed target display defect; no target/D81 bytes
were changed. Do not infer screenshot failure from a differential preview.

## Inspected authority and implementation impact

Full inspected-file/requirement list, source references and decision:
`docs/reports/R0-F_COMBINED_CONTRACT.md`. Generated schema:
`interfaces/r0f_combined_contract.json` → `interfaces/generated/r0f_combined.h`.
The old `R0C-PLAT-ROM-001` deferral and all production ABI/owners remain unchanged.

- Registers: pinned C ABI; private trap returns A and saves X/Y/Z/B/P; A changes
  Q. Flat-copy wrapper preserves X/Y/Z/B/P/SP with A result. Resident IRQ saves
  A/X/Y/Z/B/P/SP (and therefore Q), never calls C, maps memory or starts DMA.
- MAP/base page: zero offsets/MB selectors plus EOM; CPU port 01=35, B=02;
  temporary B=00 only at startup port write. No temporary MAP windows.
- Linked: BASIC 22, text 21894, rodata 775, data 0, BSS 1701, compiler static
  stack/noinit 40 bytes. End $7F71, 143 bytes remaining below the $8000 ceiling.
  Raw capture $0300-$179F (5280), NOLOAD hot scratch $17A0-$18FA (347), result
  $1900-$1FFF (1792). Model is 977 bytes of linked BSS, not a full pool-layout proof.
- Stacks: hardware page 1; private reset-only C software stack C000-CFFF, top
  D000. Canary observations cover acquisition, not every theoretical call path
  or the post-test pager. Base-page scratch 0202-0221, wrapper 0222-0229.
- Physical: snapshots 017000-0170BF, display tables 01C000-01CF9F, reclaimed
  A/B stores 020000-03FFFF, HUD 040000-0409FF, staging 050000-051FFF, PCM
  053000-0530FE, immutable list 056000-056010, color FF80000-FF807CF, immutable
  ROM backup Attic 08000000-0801FFFF. Final text uses HUD, not raw-capture RAM.
  Reserve 058000-05FFFF is CRC-read before/after, never written. No reserve used.
- DMA: one core-owned synchronous unchained 1..4096-byte normalized COPY;
  no I/O/Attic DMA or overlapping ranges; CPU-hung DMA requires reset.
- Timing/IRQ/NMI: independently accumulated Q16 nominal 100Hz releases;
  measured late/tick/cadence records. IRQ active during acquisition; RESTORE/NMI
  invalidates it. No frozen IRQ-response, masked-time or external latency claim.
- Lifecycle/storage: restore ROM bytes/protection, then reset-only lockout;
  no BASIC/filesystem restoration and no tactical or result-writing disk calls.

Changed implementation: `src/diagnostics/r0f/combined*.c/.h`,
`src/platform/r0f/combined_45gs02.s`, `combined.ld`; private contract/header,
additive platform registry, ledger/control docs; `r0f_combined_*` tools and
`R0FCombinedOracle.java`. Delivery tooling additionally enforces removable FAT32
and exact unchanged pre/post extent/device identity before safe eject, with
rollback on post-write failure. Existing dirty PF001/F5 work was preserved.
Preserved specs, prior carriers, user SD files, commits and remote refs unchanged.

## Reproduction and validation commands

```sh
python3 tools/diagnostics/r0f_combined_build.py build
python3 tools/diagnostics/r0f_combined_build.py xemu-pages
python3 tools/diagnostics/r0f_combined_build.py xemu-pal
# Existing candidate: do not construct it again or append to it.
F65_R0F_VARIANT=combined python3 tools/diagnostics/r0f_d81_loadability_gate.py "$PWD" "$PWD/build/r0f/combined/F65BLK02.D81"
python3 tools/diagnostics/r0f_combined_finalize.py tests
# One-time current-candidate visual review, using bundled Python with Pillow:
/Users/slice/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 tools/diagnostics/r0f_combined_visual_review.py
python3 tools/diagnostics/r0f_combined_sd.py inspect
python3 tools/diagnostics/d81_sd_contiguity.py --self-test
sh -n tools/diagnostics/d81_sd_fill_mega65_slot.sh
git diff --check
```

Compile/link and host/static checks PASS. JSON validation and Python compilation
also pass. Exact argument arrays, compiler/Java/Xemu/ROM hashes, maps, symbols,
disassembly, captures and screenshots are retained in generated accounting and
per-boot directories. Xemu is the pinned 40dfef0 source-model class, not a
hardware clock reference. No `-sleepless` is used: PCM advances in a wall-clock
SDL callback. Physical chooser/functional observations must come from the owner.

## SD action and hardware checklist

The local candidate now meets `XEMU_BOOT_VERIFIED`, including original-PNG
review. The card remains untouched because raw-device privilege requires the
owner's password. Run this single guarded command in your Terminal:

```sh
sudo /usr/bin/python3 "/Users/slice/Documents/ChatGPT/F65 Megawing/tools/diagnostics/r0f_combined_sd.py" fill
```

This rechecks the exact blank and all local gates, obtains raw FAT32 extent
evidence, backs up the native slot, fills it in place without truncation or
renaming, checks matching hash and unchanged single extent, and calls diskutil
safe eject. It leaves F65BLK01 and system files alone. **Do not remove the card
unless the command ends successfully with `safe_eject=PASS`.** That means the
OS reported eject success, not a guarantee against Finder or reader problems.
If it errors or Finder misbehaves, stop and share the output; do not force eject.

After successful delivery:

1. Insert the card in the powered-off MEGA65, boot, and mount **F65BLK02.D81**.
   If the chooser reports FF or another error, stop and photograph it.
2. At BASIC, enter `LOAD "R0F-PROOF",8,1` then `RUN`. Use the normal NTSC/R6
   configuration already photographed. Turn the volume down initially.
3. Do not press RESTORE during the test. Once the colored test display appears,
   tap and release **A three times**, about one second apart. Note whether audio
   is audible and whether the warning tone changes near the end. No network,
   expansion cable or runtime SD writes are required.
4. Photograph the complete **CF001 / F65BLK02** summary. Expected acquisition
   fields are fault `00`, physical reference `02`, ROM restored `02`, ticks
   `00000A50`. Real-key edges should be nonzero; timing/CRC values are measured,
   not prescribed. Any other fault is diagnostic evidence, not a pass.
5. Tap **N** to show page `01`, photograph it, then N through page `0E` (14 total).
   Keep each full screen legible. P goes back; S returns to summary. Send the
   summary, all pages, and the audio/key observations. These export actual bytes
   for independent CRC/reduction; no one must manually judge the timing hex.
6. Reset after capturing. The program intentionally does not return to BASIC.

Physical raw validation and full requirement review follow that run. The photos
do not themselves waive remaining R0 requirements or authorize Phase 1/gameplay.
