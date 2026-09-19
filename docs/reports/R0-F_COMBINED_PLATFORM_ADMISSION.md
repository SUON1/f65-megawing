# R0-F combined calibration/workload build — admission review

2026-09-17 approval; 2026-09-18 update: **CF001 COMBINED EXPERIMENT IMPLEMENTED;
FULL R0-F NOT ACCEPTED.** Current contract and evidence are in
`R0-F_COMBINED_CONTRACT.md` and `R0-F_COMBINED_HANDOFF.md`. The original review
below is historical, not a renewed approval request or current build status.
The owner subsequently approved the request below, specifying Xemu first and
F65BLK01/02 as the eventual hardware destination. PF-001 documents the first
exact platform qualification contract and implementation. Approval is no longer
the blocker; implementation/qualification and full integration remain required.
The remainder records the original admission review and retained host work.
Owner request: combine clock calibration and the full combined workload in one
coordinated build. Full closure remains the selected direction. This record is
not another full-versus-bounded scope choice, a target ABI, or an acceptance.

## Implementation boundary requiring review

`docs/plans/r0-f-task-admission.json` explicitly prohibits public ABI,
CoreRuntime, and memory ownership changes. It permits separately justified
DMA/IRQ instrumentation only after its wrapper contract is documented.
`interfaces/f65_platform_abi.json5` still lists `r0a_dma`, `r0a_irq`, and the
MAP wrapper as unverified; its admitted Attic wrapper is CPU-copy-only and its
ROM-reclaim wrapper is deferred. `interfaces/r0b_proof_contract.json` explicitly
defers PCM pending a verified DMA-audio path. There is no combined IRQ/DMA/PCM
contract to implement or inherit. F5's reset-only masked-IRQ, ROM-hosted
contract cannot be silently changed into the canonical combined platform.

Engine candidate 0.2 §16.2 requires explicit human review and an invariant-impact
note for authorized core/cross-interface changes. AD-001 allows proof development
but does not bypass the generated Platform ABI. Accordingly, target integration
is held at this boundary; independent host work proceeds under AD-001.

Requested next approval: authorize **proof-only platform-contract development
and review** for the combined harness, including additive generated declarations
in `interfaces/f65_platform_abi.json5`, R0-F-owned wrappers, and their tests.
This does not authorize changing canonical state, physical ownership, tick
order, pools, reserves, production behavior, or any gate/limit. Exact contracts
must be reviewed before their target implementation; no unverified register
sequence is supplied by this admission request.

The review must close these specific entries:

| Entry | Required content before target integration |
|---|---|
| Clock/preflight | Pinned installed-platform attribution; clock chain; verified reference and uncertainty; read coherence and overhead; period generation; reject invalid/changed clocks. No 1 MHz assumption. |
| Canonical startup/exit | MAP/EOM, `$01=$35`, B=`$02`, resident vectors, ROM handoff/reclaim semantics, valid stack and compiler scratch. Reset-only diagnostic versus restored public exit must be explicit. |
| IRQ | Entry/exit preservation including compiler temporaries and A/X/Y/Z/Q/B/P/SP; sources, acknowledge, nesting, NMI interference, bounded masking, measured response; hostile-state vectors. |
| DMA | Core-owned validated normalized physical ranges; immutable resident list lifetime; completion/failure; CPU blocking; measured job bound; no direct consumer starts. |
| PCM/SID/input | Audio-cache staging, verified start/stop/preemption, protected service schedule, input sample/edge semantics and observable latency. No production rate/binding/content selection. |
| Combined capture | Versioned generated records for actual service events, independent phase coverage, rolling windows, missed deadlines, snapshot lifetime, stack/high-water/reserve; host/Xemu/physical identity. |

## Independent clock-preflight code now available

`R0FClockPreflight.java` builds a host-only model of the **PHI-toggle producer**
in the source attributed by the MEGAINFO prefix. It is deliberately not an
end-to-end CPU/CIA/clock-domain-crossing, instrument-overhead, or oscillator model.
It first verifies an externally supplied capture SHA-256 and invokes the
unchanged F5 Java raw-data validator. No model-generated data replaces physical
capture bytes. It never emits calibrated units or a combined-target pass.

Pinned primary sources:

- [frame_generator.vhdl](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/vhdl/frame_generator.vhdl):
  3 clocks/pixel, 2 rasters per PHI quota, default quota 63, accumulator,
  remaining quota, frame reset and CPU-domain toggle export.
- [pixel_driver.vhdl](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/vhdl/pixel_driver.vhdl):
  NTSC `frame60` is 858 by 526 with zero debug-height reduction and does not
  override that quota; selected PHI output follows PAL/VGA/NTSC selection.
- [cia6526.vhdl](https://github.com/MEGA65/mega65-core/blob/b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f/src/vhdl/cia6526.vhdl):
  Timer A PHI decrement; delayed underflow event feeding Timer B; hypervisor
  gating. A producer-only model cannot prove coherent CPU reads.

The profile is explicitly declared, not auto-detected from F5 bytes or taken
as proof of the installed bitstream. Model simulation retains VHDL old-state
reads and final-assignment precedence. It discards the initial partial frame
and three settling frames, then checks 32 complete frames independently of the
capture. Each source-model frame yields 16,569 pulses; 16 yield 265,104.
The retained physical capture reports 265,103 and 265,097. Residuals `-1` and
`-7` are observations only: no invented tolerance, SI conversion or calibration
pass. A nominal or inferred frame frequency is not an independent reference.

## Inspected authority and impact before the first edit

Official record; root AGENTS; frozen Architecture 1.4.1 in full including its
memory map/MemoryAccessABI; approved Read-First and approval record; AD-001;
Architecture candidate 1.5.1 §§1–3 and 6; Engine candidate 0.2 §§2.5, 4–5,
11–12, 14.4–17.2 and 19.1–19.2; all current memory ledgers; interface/platform
registries and R0-B–F proof contracts; R0-F timing contract, admission/ownership,
full-closure plan; existing CIA wrapper, host clock test, Java timing validator,
build tooling and toolchain lock. Candidate parents remain candidates.

Requirements: AD-001 RC-1/RC-2 dependencies; Architecture §6 timing and §2
MemoryAccessABI; Engine §5 independent clocks, §2.5 platform boundary and
§16.2 cross-interface review. No missing contract is deemed admitted here.

Changed scope: this report, R0-F host preflight Java/build script, and R0-F
control-state notes only. Java remains the independent host implementation.
No target C/assembly, generated target headers, existing validator, public ABI,
ledger, parent specification, or prior carrier is changed by this increment.
45GS02 registers/clobbers, CPU-visible/physical memory ranges, hardware/software
stack, MAP/base page, DMA, IRQ/NMI, timing/deadline behavior: **not applicable to
this host-only increment; no target changes**. Protected `$050000–$05FFFF`
and all reserves remain untouched. The model grants no permission to access
those ranges. Existing dirty work is preserved.

## Reproduce and review

```sh
python3 tools/diagnostics/r0f_clock_preflight.py \
  --java-home '/Users/slice/Documents/Codex/f65-megawing/toolchain/runtime/jdk-full/jdk-21.0.12+8/Contents/Home' \
  --capture docs/evidence/r0f/capture/physical/physical-capture.bin \
  --sha256 042b8155e16591864c6de5b5855fc28427b789b40b90b0c23623d2540815d700
git diff --check
```

The builder pins the retained Java binary and version, compiles with
`-Xlint:all -Werror`, reruns the existing independent raw-data oracle, runs
source-model/negative tests, and writes commands, input/source/tool/output
hashes under `build/r0f/clock-preflight/`. Successful host execution explicitly
reports `combinedHardwareReady=false` and `calibrationValid=false`.

Observed validation: Java compilation PASS with warnings as errors; existing
oracle PASS for 2,640 samples/80 spans and all 198 corruption rejections;
preflight PASS for 32 modeled frames, non-promotion checks and 13 bad inputs;
`git diff --check` PASS. Capture SHA-256 is the exact value in the command above.
Generated-artifact status: host classes, reports and manifest only. Target
headers, maps, symbols, listings and ledgers unchanged. The manifest records
the exact commands and per-source identities, not an implied new target build.

Target build, Xemu and new physical test: **not run; no combined target exists**.
No D81 creation/modification/mount/copy, SD operation, commit or push. Existing
F5 evidence is read-only and needs no repeat capture for this work. No action on
the MEGA65 or SD is requested until a target has passed its required gates.
