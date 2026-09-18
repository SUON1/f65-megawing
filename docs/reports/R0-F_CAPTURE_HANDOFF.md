# R0-F5 capture-viewer build handoff — 2026-09-17

Subsequent physical evidence: F5 SD hash/unchanged single extent/safe eject
PASS; owner summary and all 22 pages retained. Photographic reconstruction
passes all page/full CRCs and independent Java raw reduction (2640 samples,
80 spans). See `../evidence/r0f/capture/physical/REVIEW.md`. This validates the
bounded raw-count capture, not calibration or full R0-F. The build-time
handoff below is retained as history; no repeat SD run is requested.

**F65R0F5.D81: XEMU_BOOT_VERIFIED.** The RC-1 screen-capture slice is built;
full RC-1 calibration, combined-load implementation and R0-F acceptance are
not complete. No SD operation, physical run, commit or push performed.

## Artifact and retained evidence

- `build/r0f/capture/F65R0F5.D81`, 819200 bytes, SHA-256
  `67183150719f1bbba01b862532c5996953e1d6c10cc38e1f9352b281895cc627`.
- Disk `F65 R0-F5`, ID `65`; `AUTOBOOT.C65 -> R0F-PROOF`.
- PRG: 12641 bytes, SHA-256
  `e68527b6db89882a49fbb4b7fb1b48f5f54fedd62cd98fc3176bce5340517c2d`.
- Working tree on `codex/r0-f-development`, HEAD
  `744920dd76d008fbc0ccce82e006cc0b647f477e`; not a clean-commit release.
  Exact source/toolchain input hashes are in `build-accounting.json` and the
  packaged `R0F-EVID` payload. Build-time Xemu/D81 fields are historical;
  the later release manifest controls current gate state.
- Reports, maps/symbols/disassembly, two raw captures, rendered page sets,
  independent reductions, screenshots/logs and release record retained in
  `docs/evidence/r0f/capture/`. Full emulator memory dumps remain in
  `build/r0f/capture/xemu/`.

F2 and F4 remain byte-identical to their retained hashes
(`24fabf16...548297` and `a30880f8...ff39d`). They were not rebuilt or copied.
F3 and the physical SD were not operated on.

## Implemented

New target files: `src/diagnostics/r0f/capture_view.c` and
`src/platform/r0f/capture_key.c`. Updates to `src/r0f/main.c` and
`src/diagnostics/r0f/timing_sweep.c` connect the new isolated `capture` variant.
The inherited timer/sweep protocol is unchanged; the successor's code layout
and observed counts are build-specific, not interchangeable with F4.

After timer stop, the viewer exposes the 256-byte result and 10880 raw bytes
as 22 numbered hexadecimal pages, with per-page and whole-stream CRC-32.
N/space, P, S and C navigate pages/summary. No measurement rerun or media write.
The payload itself is not copied or modified.

`R0FCapturePages.java` independently decodes complete screen transcripts,
checks offsets/lengths/padding/CRCs and rejects missing, duplicate or mixed
pages. It then invokes the timing oracle. Existing output files are never
overwritten. `R0FTimingOracle.java` now also checks previously omitted fixed
header/profile/reserved fields, raw-pointer bounds and frame-count guards.
These are integrity checks, not calibration or performance thresholds.

Builder, private JSON contract/generated header and memory ledger include the
new variant. New host test: `tools/diagnostics/r0f_capture_host_test.c`.
No preserved specifications, production ABI, upstream implementation, tick
order, pool capacity or reserve was changed. Existing unrelated working-tree
changes were preserved.

## Contract and impact

Inspected sources/requirements and precise wire protocol are in
`R0-F_CAPTURE_CONTRACT.md`: full frozen architecture and its MemoryAccessABI,
current memory/interface registries, B-register convention, approved control
records, relevant candidate ABI/evidence requirements, F4 implementation and
tests, official `$D610` map, and root D81 gate.

New hardware access is post-acquisition `$D610` read/acknowledge only. C ABI
clobbers A/X/Y/Z/P and pseudo-registers; B=$02 and inherited ROM-hosted mapping
remain. No new MAP/EOM, ROM call, DMA, IRQ-vector/ICR/CIA2 or NMI-source change.
Startup SEI remains; the fini CLI is not reached by the nonreturning main.
Reset required. Viewer CRC/render time occurs after timers stop, outside
measurements. It is not an input-latency service.

Result $1900–$19FF and screen $0800–$0FCF retain their existing owners.
BSS is 12157 bytes at $5160–$80DC; compiler static stack is 115 bytes at
$80DD–$814F; raw capture is $5162–$7BE1. Text 10955, rodata 1662, BASIC
header 22, data 0; total linked resident accounting 24911 bytes. Hardware
stack/base page remain $0100/$0200; software-stack top $D000. No target page
buffer, capture copy, DMA bytes or reserve allocation. Dynamic stack high-water
and production canonical MemoryAccessABI remain unproved.

## Verification

Commands executed from the repository root:

```sh
F65_R0F_VARIANT=capture sh tools/build/r0f.sh build
F65_R0F_VARIANT=capture sh tools/build/r0f.sh audit
F65_R0F_VARIANT=capture sh tools/build/r0f.sh package
F65_R0F_VARIANT=capture \
F65_MEGA65_ROM='/Users/slice/Documents/Codex/f65-megawing/MEGA65.ROM' \
F65_MEGA65_SD_IMAGE='/Users/slice/Library/Application Support/xemu-lgb/mega65/mega65.img' \
sh tools/build/r0f.sh xemu
git diff --check
```

- Build/static PASS: pinned LLVM-MOS compile/link, maps, symbols, disassembly,
  ledger reconciliation, B startup and no new MAP/EOM/direct-ROM transfers.
- Host PASS: native ASan/UBSan; 358 legacy corruption rejections; six timing
  faults, byte/cascade/32-bit wraps and precondition guards; injected overload
  reports 16 misses per case rather than a false deadline PASS.
- Capture host PASS: all 22 pages reconstruct exact 11136 bytes; controls and
  bounds, read/ack behavior, no source mutation; Java rejects 14 malformed page
  sets and verifies text import and output-overwrite refusal.
- Independent timing PASS: 2640 raw samples/80 cohort spans per accepted
  capture; 35 summary plus 163 fixed-field corruptions rejected even with a
  recomputed result checksum.
- Package PASS: fresh format/all payloads in one pinned c1541 session;
  structural/BAM/ownership/content extraction and hash checks passed.
- Exact-D81 Xemu PASS: two fresh processes, separate disposable emulator SD
  copies, 40 seconds each. Both raw captures passed independent reduction;
  first-page target memory exactly matched the host-tested formatter. Both
  screenshots were visually inspected; both have SHA-256
  `9e3fcec7f5d8c4a79668303a655caad3ec83d33a0c865b9a3138336b52591fb5`.
  Navigation beyond the first page was host-tested, not exercised by these
  headless Xemu runs. Physical navigation and photographic import remain open.
- Preliminary direct-PRG Xemu boots also passed before the final explanatory
  screen line/oracle changes; those are not substituted for the final D81 runs.
- Final integrity PASS: recorded build-input hashes match current sources;
  carrier and both Xemu evidence identities match; retained evidence copies
  are byte-identical and JSON records parse. F2 and F4 hashes are unchanged.
- Carrier overwrite guard PASS: repeating the `package` command above returned
  the expected exit 2 (`carrier identity already exists; never overwrite or
  silently rebuild`) before mutation. This is a negative test, not a carrier
  failure. `git diff --check` also passed.

The inherited `host-test.json` field `javaOracle: NOT RUN; pinned JDK unavailable`
is stale descriptive wording for the legacy REV1 subtest, not the timing or
capture result. The full pinned JDK was available and its identity plus actual
timing/capture Java outputs are retained separately. No built manifest was
silently patched to conceal that reporting defect.

## Clock-source audit carried forward

At the photo-attributed core commit
`b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f`, source tracing found:

- [iomapper.vhdl](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/vhdl/iomapper.vhdl)
  routes its PHI input to CIA1.
- [machine.vhdl](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/vhdl/machine.vhdl)
  connects that input to `pixel_driver.phi_1mhz_out`.
- [pixel_driver.vhdl](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/vhdl/pixel_driver.vhdl)
  selects PAL/VGA/NTSC timing-generator outputs, then registers the selected
  signal in the CPU clock domain. `frame_generator` and board clock generation
  still need full analysis and reference/tolerance validation.

Consequently, the label “1 MHz” and a matching frame-count ratio do not alone
establish calibrated SI time. This source attribution is not installed
bitstream identity verification. No physical counts were converted or limits
selected in this build.

## Next work / owner action

Continue RC-1 clock calibration/coherence/overhead and the RC-2 combined-workload
admission. This build is the capture component only. Full phase/window,
renderer/input/audio/DMA/IRQ, protected workload, dynamic high-waters,
platform matrix and human acceptance remain open.

**No SD test requested now.** The screen transport is a fallback requiring 22
pages for a full capture; physical suitability is not yet proved. Keep the
existing card/configuration unchanged. F5 SD byte/extent/eject/chooser fields
remain pending; do not infer them from earlier carriers.
