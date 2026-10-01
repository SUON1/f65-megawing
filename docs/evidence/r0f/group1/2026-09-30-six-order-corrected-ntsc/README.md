# Corrected six-order Group 1: one focused NTSC run

The requested rebuild and single NTSC acquisition were performed on
2026-09-30. Acquisition reached all 3200 records with target fault 0 and IRQ
error 0. The selected 60-second wall-clock limit interrupted terminal export
after four complete trace chunks. This evidence is incomplete; no full trace
reduction, six-order coverage acceptance or Group 1 acceptance follows.

## Identity and preserved baselines

- Branch: `codex/r0f-successor-physical-exact-carrier`.
- Source HEAD: `9e2ffdb4786e4794119933a5edd4b1cf79f653f0`, with retained
  uncommitted inputs in `source-inputs/`; this is not a published source freeze.
- Six-order PRG: 37191 bytes, SHA-256
  `c249f4e4da972cdc0c5d0958a1a3a148387eb1ad4de602404c6b79fb7c79492b`.
- Resident high-water exclusive: `$BD98`; 616 bytes remain within the
  unchanged `$C000` envelope, with no reserve borrowing.
- Corrected pre-variant baseline: `0d96a1b21eb36680b05689b659ac8c6f73cc2b61e647c060ab2f369c2bbfc244`,
  retained in `baseline/` with its build metadata. The earlier passing
  `ec259fc7611d8bb5809d15f6c333f5b224df4c945a8e9ffca5b2402d8444cb30`
  remains in the preceding evidence freezes.
- Ordinary successor rebuilt byte-identically:
  `cf605bd377ddcee2c72cdc4abfd20c3ae9eee350b7b78b36cbde8ff1adf8fc23`.
- Xemu: version `20260129235930`, source
  `40dfef0d1d5f56be2469492715c12bdb32c75b67`, executable
  `dd37baf7846b9696adcb662ffe5da040031b07214c66aef9a7f48cc30040b738`.

## Implementation and contract effects

The retained six-order phase recorder and service sweep were reapplied without
reapplying its experimental IRQ failure instrumentation. The short `BNE; RTS`
correction remains at `$3298`. The static IRQ validator rejects long branches.
The version-4 private trace contract generates the new header bindings; no
public ABI or physical allocation changes. The independent reducer now requires
all sixteen phase bins, rather than merely a nonzero mask, and all six orders
in each epoch.

Main Concept v1.6 §§4 and 17, the approved Group 1 Build Intent, measurement
matrix, terminal-export amendment and generated trace/export contracts govern.
Measurement still reads existing CIA1 counters; resident state grows within
the existing envelope. Service order and measured instrumentation cost change.
Register/clobber ownership, MAP/base-page, DMA and IRQ/NMI ownership are
unchanged. Acquisition includes measurement cost; terminal export remains
outside workload deadlines.

## Single run and actual observations

From the repository root:

```sh
python3 -B tools/diagnostics/r0f_group1_run.py --out build/r0f/group1/integration/six-order-corrected-ntsc-01 --mode 1 --timeout-seconds 60
```

The host runner exited 1 because complete export was unavailable at termination.
Pinned Xemu exited 0 after the timed SIGTERM. The development image was freshly
formatted and populated with TOKEN in one pinned `c1541` session; it was a
disposable direct-PRG fixture, not a release carrier. Its pre-run extraction
and structure/content checks passed. The 4 GiB disposable SD fixture is omitted.

`ntsc-01/inspection.json` records the frozen observations:

- All 3200 records; target fault 0; private IRQ error 0.
- Input/audio/display start masks `FFFF` in each epoch; order masks `3F`/`3F`.
- IRQ samples 916/912, with zero nonzero intervals observed. Timing resolution,
  whole-ISR cost and entry latency remain unresolved in pinned Xemu.
- Independent 512-byte result validation passed: stage 127, lifecycle 9,
  ticks 1600/3200, lineage `6B765FDB`/`607348BD`, CRC `6ED11C16`, unchanged
  reserve/low/DOS checks and advancing resumed IRQ/DMA/input/audio counts.
- The actual extracted 34-byte RSSTATE matches its linked address and independent
  expected SAVE bytes. Four complete chunks have correct length/framing; their
  first header equals the frozen target header.
- Export status 3, error 0, four completed chunks; declared trace 315780 bytes,
  250244 bytes remaining at the chunk boundary. Directory contains open `G1T04`.
- Complete-image validation rejects file type `02`; partial reduction rejects
  `trace length`. Full CRC, deadline/window/cadence and complete-trace validation
  were not possible. Resident/header masks alone are not accepted phase proof.

The partial image is retained as `INVALID — DO NOT USE` for further testing.
Do not repair or resume it. The earlier pre-acquisition stall and invalid IRQ
interval did not recur in this one acquisition; this is not a general absence
proof. A longer fresh run is required for complete export/reduction.

## Validation and next action

`validation.json` records host/static checks. Pure timing/export checks pass
sanitizers, one million release comparisons and independent phase-edge/wrap
cases. Target linking/static boundaries, seven trace-contract tests and host
lineage checks pass. A synthetic HOST-only fixture based on the preceding
actual fixed-order trace, with order masks changed and CRC repaired only to
exercise the validator, rejects 22 corruption cases including incomplete
phase coverage and missing pre/post order bits. It is not target evidence.
The long-branch guard rejects an injected BEQ16, and the ordinary successor
regressions pass with unchanged PRG bytes.

Next run this unchanged six-order PRG once in a fresh disposable NTSC directory
with a 120-second export allowance. Require status 4, 20 closed chunks and full
independent extraction/structure/SAVE/reduction before proceeding to PAL.
This turn performed exactly one emulator acquisition. No SD write, physical
execution, exact-name release-carrier gate, commit or push was performed.
