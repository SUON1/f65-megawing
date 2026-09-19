# R0-F Interface and Ledger Impact

## Owner-approved platform qualification — 2026-09-17

`R0-F_PLATFORM_QUALIFICATION_CONTRACT.md` records PF-001 before implementation.
New private contract/generated constants and an additive platform-registry
entry authorize only the reset-only development PRG. C uses B=02/rc0–31;
entry sets MAP/EOM, real CPU port 35 with temporary B=00, and resident vectors.
Leaf raster IRQ preserves A/X/Y/Z/Q/B/P/SP without compiler-temporary access;
sticky NMI interference invalidates results. No C callback in IRQ.
Private flat-copy scratch is 0222–0229. A bounded 255-byte DMA copy uses
050000/050100 staging and the immutable 17-byte list at 056000. PCM channel 0
reads a pre-staged unsigned sample at 053000; progress and stop are observed,
not audible latency. Linked allocations and both stack categories are charged
in the generated PF-001 accounting; dynamic high-water remains unmeasured.
No ROM-storage, reserve, SD or filesystem writes. R0-C reclaim stays deferred.
Raw CIA observations are not SI, cycle or calibrated 100Hz evidence. Full
combined delivery remains blocked on its documented dependencies; no D81 is
packaged from this primitive-only PRG. See `R0-F_PLATFORM_HANDOFF.md`.

## Capture viewer — 2026-09-17

`R0-F_CAPTURE_CONTRACT.md` and `R0-F_CAPTURE_HANDOFF.md` govern the new isolated
F5 variant. Existing REV2 capture layout is unchanged. Additive generated
constants describe a 22-page screen transport; new post-acquisition $D610
read/ack wrapper controls only the viewer. BSS 12157 bytes; compiler static
stack 115 bytes, separately reconciled. No page/capture-copy buffer, production
ABI, MAP/base-page, IRQ/NMI, DMA, protected memory or reserve change. Viewer
runs after timer stop. Dynamic stack and clock calibration remain open.

## CIA-count diagnostic — 2026-09-17

Current contract and full impacts: `R0-F_CIA_TIMING_CONTRACT.md`; generated
accounting/evidence: `R0-F_CIA_TIMING_HANDOFF.md`. Private REV2 keeps the 256-byte
result owner and adds linked raw capture/sorting/state (total BSS 12,152 bytes),
158-byte compiler static stack, exclusive reset-only CIA1 timer ownership, and
raw-count release/deadline observations. IRQ stays masked; no service-latency
claim. No MAP, public ABI, DMA, CIA2/NMI source, or protected-reserve change.
Dynamic stack high-water and physical time calibration remain unresolved.

## Startup correction — 2026-09-17

The R0-F-only linker fragment removes the unused SDK `.init.250` ROM call.
Host/static checks and two fresh Xemu boots of F65R0F2.D81 pass. No shared
startup or public ABI changed. The new banner adds build identity. Current
snapshot BSS is $3278–$3337; compiler static stack is $3338–$33A2; byte counts
remain 192/107. Stock startup still masks IRQs and sets B=$02; no ROM IRQ-service
or physical timing claim is made. Full impacts and current evidence are in
`R0-F_STARTUP_FIX_HANDOFF.md`. The older findings below remain historical.

## Current implementation — 2026-09-05

Verification update: the owner supplied the missing runtime location. Two clean
Xemu boots now pass; retained evidence is under `docs/evidence/r0f/xemu/`.
The initial missing-tool disposition below is historical and resolved.
Step 3 (2026-09-16) changes host validation and descriptive contracts only;
the target PRG is byte-identical. Review corrected two omissions: 107 bytes of
compiler static stack in `.noinit`, and a startup KERNAL call after B=$02.
The latter blocks the static gate. See `R0-F_STEP3_AUDIT.md`.
Step 2 documented the bounded proxy; it did not complete calibration or provide
formal architecture/owner acceptance.

The owner requested the first bounded test-code build. `R0F1 REV1` is a
standalone C rebuild of the accepted R0-E functional proxy, not the complete
R0-F measurement program. Its private contract is
`interfaces/r0f_proof_contract.json`; generated constants are in
`interfaces/generated/r0f_interfaces.h`. No production public ABI changes.

Inspected: official record; both architecture sources including MemoryAccessABI;
Read-First/AD-001/approval record; current memory and interface registries;
R0-A–D handoffs; R0-E composite, raster helper, contract, ledger and accepted
evidence; R0-F admission/plan; root D81 gate and native-slot delivery rules.

- Registers: compiler-generated C uses A/X/Y/Z, processor flags and compiler
  pseudo-registers under the pinned ABI; not a preserve-all wrapper. No new
  handwritten assembly or Q contract. Existing startup sets B=$02 after ROM
  startup and restores B=$00 on program return; main deliberately never returns.
  The raster helper reads $D012 only and writes compiler temporaries/stack, not
  hardware registers. Result/screen writes belong to the composite. The linked
  startup's unwrapped KERNAL call has unresolved ROM clobbers and is not covered
  by the helper's read-only contract.
- CPU-visible writes: result $1900–$19FF, screen $0800–$0FCF, compiler base-page
  storage $0200–$02FF, hardware stack $0100–$01FF, linked code/data and software
  stack below $D000. Snapshot BSS is $3255–$3314 (192 bytes) in this build;
  compiler static stack is $3315–$337F (107 bytes). Dynamic stack bounds remain
  unmeasured; this accounting does not prove absence of runtime overlap.
- Physical/MAP: no new MAP/EOM operation. Existing stock startup writes
  $00=$2F, $01=$3E, $D030=$44 before B=$02; this was omitted from prior impact
  wording. The $FFD2 call at $2035 has no intervening B=$00 thunk. This is not
  evidence of production canonical MemoryAccessABI
  entry/exit. Protected $050000–$05FFFF is not allocated or accessed by the proof.
- DMA: no jobs, lists, buffers or register accesses. NOT EXECUTED.
- Timing: read-only $D012; at most 65,535 reads per acquisition, 80 acquisitions,
  33 unpaced model ticks per sample. Reset now precedes acquisition. Raw modulo
  bytes remain in phase order with separate validity masks; wraps are unresolved.
  No CPU-cycle/deadline/latency/real-100Hz claim.
- IRQ/NMI: the linked stock startup executes SEI; stock fini contains CLI, but
  main never returns. Post-ROM-call interrupt state is unverified; do not assume
  uninterrupted ROM IRQ service or assert end-to-end IRQ preservation. No new
  vector, CIA or NMI source change; IRQ/NMI timing is not measured.
- Runtime/stack: emitted map includes compiler support; dynamic stack high-water
  is NOT MEASURED. Compiler static stack is now charged in the private ledger.
  No fit, safety-margin or R0-F closure claim follows from linking.
- Validation: `sh tools/build/r0f.sh audit` invokes host tests and build. Native
  sanitizer/358 rejection tests and target link pass; static audit exits 2 for
  `R0F-STATIC-STARTUP-001`. Prior D81/Xemu/SD and owner-reported hardware load
  evidence remains historical; Step 3 performed no fresh media/emulator/hardware
  run. See `R0-F_STEP3_AUDIT.md` and `R0-F_BUILD_HANDOFF.md`.

## Historical admission-time disposition (superseded above)

R0-F currently changes no target implementation and no shared contract. The
existing R0-A through R0-E interfaces and ledgers were inspected as inputs only.
No `interfaces/` or `memory/` file is changed by this admission record.

| Area | Admission-time impact |
|---|---|
| 45GS02 registers and clobbers | `NOT_APPLICABLE`: no R0-F wrapper or target routine exists. |
| CPU-visible memory | `NOT_APPLICABLE`: no R0-F result block, stack, or base-page allocation exists. |
| Physical memory | `NOT_APPLICABLE`: no R0-F allocation exists; `$058000-$05FFFF` remains untouched. |
| MAP / EOM / base page | `NOT_APPLICABLE`: no R0-F mapping exists; canonical requirements remain controlling. |
| DMA | `DMA_HARDWARE_PROBE_NOT_EXECUTED`: no request, list, register write, or ownership change exists. |
| Timing / deadlines | No code change; R0-F must measure rather than select any value. |
| IRQ / NMI | `IRQ_MEASUREMENT_NOT_EXECUTED`; no NMI source is enabled. |
| Public ABI / generated records | No change. A future physical result record must be generated from one canonical source. |
| Ledger / reserve | No change; zero R0-F allocation and no reserve use. |

## Required update trigger

Before a platform wrapper, target diagnostic, result record, or D81 payload is
implemented, create an R0-F machine-readable contract and ledger. It must name
the exact registers, save/restore sequence, clobbers, CPU/physical ranges,
MAP/base-page behavior, DMA request/list ownership, IRQ masking/latency effect,
NMI disposition, timeout/failure handling, stack charge, and validation
commands. A missing fact blocks that implementation; it is not an invitation to
reuse R0-A/R0-E behavior by assumption.
