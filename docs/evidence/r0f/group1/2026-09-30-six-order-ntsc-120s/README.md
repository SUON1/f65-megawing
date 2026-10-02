# Unchanged six-order PRG: complete NTSC export and reduction

The owner-authorized fresh NTSC run with a 120-second allowance passed complete
acquisition, terminal export and independent reduction on 2026-09-30. All 3200
records, 20 closed trace chunks and the actual SAVE validated. Nominal timing is
`WITHIN_OBSERVED_BOUNDS`: zero deadline misses, zero boundary-uncertain cases
and zero cohorts below the 20 Hz floor.

## Exact identity and authority

No rebuild or target-source change occurred. PRG SHA-256 remains
`c249f4e4da972cdc0c5d0958a1a3a148387eb1ad4de602404c6b79fb7c79492b`,
37191 bytes, with the corrected short IRQ branch, resident end `$BD98` and
616 bytes free within the existing envelope. Branch is
`codex/r0f-successor-physical-exact-carrier`, HEAD
`9e2ffdb4786e4794119933a5edd4b1cf79f653f0`, plus the retained uncommitted
source inputs. This is local evidence, not a published source commit.

The [preceding source/build freeze](../2026-09-30-six-order-corrected-ntsc/README.md)
pins all 79 source/tooling inputs and both earlier baselines. Its 108-file
manifest, the active PRG and all retained inputs were verified unchanged before
this run. The incomplete 60-second image remains preserved and was not reused.

Main Concept v1.6 §§4 and 17, the approved Group 1 Build Intent, measurement
matrix, private trace/export contracts and root D81 workflow govern. Registers,
CPU-visible/physical memory, MAP/base-page, DMA, timing/deadline semantics and
IRQ/NMI behavior are unchanged from the preceding build. Only a new disposable
fixture and its wall-clock allowance changed.

## Run and independent validation

From the repository root:

```sh
python3 -B tools/diagnostics/r0f_group1_run.py --out build/r0f/group1/integration/six-order-corrected-ntsc-02 --mode 1 --timeout-seconds 120
python3 -B tools/diagnostics/test_r0f_group1_reduce.py build/r0f/group1/integration/six-order-corrected-ntsc-02/trace.bin
```

Both commands exited 0. Xemu exited 0 after the scheduled 120-second SIGTERM;
that termination is the observation boundary, not the exact completion time.
Export status was 4, file count 20 and error 0. The development D81 was freshly
formatted and populated in one pinned `c1541` session, then used with direct
PRG injection. This is a development fixture, not an exact-name release-carrier
boot gate. The disposable 4 GiB Xemu SD fixture is omitted from this freeze.

Pinned-tool extraction and the independent geometry/directory/BAM/chain parser
agreed on every payload. All trace chunks have correct framing/length, TOKEN
is unchanged, and the actual 34-byte RSSTATE matches its linked address and
independently calculated SAVE bytes. The complete trace CRC, record order,
stage/input/AI lineage, storage continuation, clocks, snapshot/world events,
stack, DMA/IRQ observations and rolling-window checks passed.

- Trace: 315780 bytes, SHA-256
  `cf54688d281d058e25b4fc73778d39b20d28319e1c446b9b6f272b4ac90503e7`.
- Post-run D81: 819200 bytes, SHA-256
  `9078d8b527832f0b3e6bfc7c426aecbc939b700766e7c302f10cc24ec5f91451`.
- Result: fault 0, stage 127, lifecycle 9, ticks 1600/3200, lineage
  `6B765FDB`/`607348BD`, CRC `18D750C5`; reserves and low/DOS memory checks
  unchanged, original storage context invalidated, resumed services observed.
- Each epoch has input/audio/display start-bin masks `FFFF` and service-order
  mask `3F`. This establishes the declared aggregate NTSC sampled coverage.
- All 32 cohorts satisfy the existing nominal deadline/cadence checks;
  976 completed-world events retained. Exercised hardware/software stack
  high-water is 79/87 bytes.
- The actual complete trace rejected all 22 repaired/truncated corruption
  cases, including incomplete phase masks and missing pre/post order bits.
  These checks now use real complete acquisition bytes, not the prior synthetic
  host fixture.

`ntsc-02/execution.json`, `post-disk.json` and `reduction.json` retain detailed
results. `validation.json` records commands and `sha256.json` pins this freeze.

## Remaining boundary and next action

The IRQ probe has 912/919 samples, but all measured body-read intervals are
zero in pinned Xemu. This retains the unresolved emulator timing-resolution,
whole-ISR-cost and entry-latency boundary. SI uncertainty remains unresolved.
Aggregate masks do not prove every relative service phase combination or
external input/audio latency. PAL six-order coverage remains unrun.

Next run this same PRG in a fresh PAL fixture with a 120-second allowance and
require the same complete independent export/reduction. The remaining view,
registration/occlusion/LOD/pool observations, near-capacity integrated trace,
operator summary and exact-carrier gates remain open. No SD write, physical
run, commit or push occurred, and no full Group 1 or R0-F acceptance is claimed.
