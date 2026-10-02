# Unchanged six-order PRG: complete PAL export and reduction

The fresh PAL run with a 120-second allowance passed complete acquisition,
terminal export and independent reduction on 2026-09-30. All 3200 records,
20 closed trace chunks and the actual SAVE validated. Nominal timing is
`WITHIN_OBSERVED_BOUNDS`: zero deadline misses, zero boundary-uncertain cases
and zero cohorts below the existing 20 Hz floor.

## Exact identity and authority

No rebuild or target-source change occurred. PRG SHA-256 remains
`c249f4e4da972cdc0c5d0958a1a3a148387eb1ad4de602404c6b79fb7c79492b`,
37191 bytes, with the corrected short IRQ branch, resident end `$BD98` and
616 bytes free within the existing envelope. Branch is
`codex/r0f-successor-physical-exact-carrier`, HEAD
`9e2ffdb4786e4794119933a5edd4b1cf79f653f0`, plus retained uncommitted inputs.

The [preceding source/build freeze](../2026-09-30-six-order-corrected-ntsc/README.md)
pins all 79 source/tooling inputs and earlier baselines. Its 108-file manifest,
the [complete NTSC freeze](../2026-09-30-six-order-ntsc-120s/README.md)'s 61-file
manifest, the active PRG/symbols and all retained inputs matched before PAL.
Neither previous image was reused or modified.

The approved Group 1 Build Intent, measurement matrix, Main Concept v1.6
sections 4/17, private trace/export contracts and root D81 workflow govern.
Registers/clobbers, CPU-visible and physical memory, MAP/base-page, DMA,
timing/deadline semantics and IRQ/NMI behavior are unchanged. Only the fresh
disposable fixture, video standard and wall-clock allowance changed.

## Run and independent validation

From the repository root:

```sh
python3 -B tools/diagnostics/r0f_group1_run.py --out build/r0f/group1/integration/six-order-corrected-pal-01 --mode 0 --timeout-seconds 120
python3 -B tools/diagnostics/test_r0f_group1_reduce.py build/r0f/group1/integration/six-order-corrected-pal-01/trace.bin
```

Both commands exited 0. Xemu exited 0 after the scheduled 120-second SIGTERM;
this is the observation boundary, not the exact export completion time.
Execution was 19:27:39.668630 through 19:29:39.810104 UTC. Export status was 4,
file count 20 and error 0. A fresh single-session development D81 and direct
PRG injection were used, not a release-carrier boot. The disposable 4 GiB
emulator SD fixture is omitted from this freeze.

Pinned-tool extraction and the independent geometry/directory/BAM/chain parser
agreed on every payload. All chunks have correct framing/length, TOKEN is
unchanged, and the actual 34-byte RSSTATE matches its linked address and
independently calculated SAVE bytes. Full-trace CRC, stage/input/AI lineage,
storage continuation, clocks, snapshot/world events, stack, DMA/IRQ and
rolling-window checks passed.

- Trace: 314620 bytes, SHA-256
  `7f032d917a3202f89523e02a8c2deafae8b09e707878bc5b770958866bf452a1`.
- Post-run D81: 819200 bytes, SHA-256
  `1c7665fed685382cd92fe5262686e1eda0ec0b22bbc31fbc882c75dfdd46f043`.
- Result: fault 0, stage 127, lifecycle 9, ticks 1600/3200, lineage
  `6B765FDB`/`607348BD`, CRC `435801C3`; reserve and low/DOS memory checks
  unchanged, original context invalidated, resumed service mask 31.
- Both epochs have input/audio/display start-bin masks `FFFF` and completed
  service-order mask `3F`, establishing the declared aggregate PAL sampled scope.
- All 32 cohorts pass existing nominal deadline/cadence checks; 831 complete
  world events retained. Exercised hardware/software stack high-water is
  79/87 bytes. Read/capture maxima are 32/705 CIA counts.
- All 22 repaired/truncated corruption cases reject against the complete
  actual PAL trace, including incomplete phase and pre/post order masks.

`pal-01/execution.json`, `post-disk.json` and `reduction.json` retain detailed
results. `validation.json` records commands; `sha256.json` pins this freeze and
references the unchanged source/build manifest.

## Remaining boundary and next action

IRQ samples 782/786 contain no nonzero body-read interval in pinned Xemu.
Emulator resolution, whole-ISR cost, entry latency and physical SI uncertainty
remain unresolved. Aggregate masks do not prove every relative service-phase
combination or external input/audio latency. This PAL result and the preceding
NTSC result establish local declared sampled coverage, not physical acceptance.

Continue the remaining view/registration/occlusion/LOD and applicable pool
observations, integrated near-capacity trace, compact operator summary and
exact-name carrier gates. No SD write, physical run, commit or push occurred.
No hardware-ready, full Group 1 or R0-F acceptance claim is made.
