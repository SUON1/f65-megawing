# R0-F Interface and Ledger Impact

## Current implementation — 2026-09-05

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
- CPU-visible writes: result $1900–$19FF, screen $0800–$0FCF, compiler base-page
  storage $0200–$02FF, hardware stack $0100–$01FF, linked code/data and software
  stack below $D000. Snapshot BSS is $3255–$3314 (192 bytes) in this build.
- Physical/MAP: inherited ROM-hosted low-memory context, no MAP/EOM/$01 or
  mapping changes. This is not evidence of production canonical MemoryAccessABI
  entry/exit. Protected $050000–$05FFFF is not allocated or accessed by the proof.
- DMA: no jobs, lists, buffers or register accesses. NOT EXECUTED.
- Timing: read-only $D012; at most 65,535 reads per acquisition, 80 acquisitions,
  33 unpaced model ticks per sample. Reset now precedes acquisition. Raw modulo
  bytes remain in phase order with separate validity masks; wraps are unresolved.
  No CPU-cycle/deadline/latency/real-100Hz claim.
- IRQ/NMI: no vector, mask, CIA or source changes; ROM interrupt context inherited.
  IRQ latency/restoration and NMI behavior are not measured. No new NMI source.
- Runtime/stack: emitted map includes compiler support; dynamic stack high-water
  is NOT MEASURED. No fit, safety-margin or R0-F closure claim follows from linking.
- Validation: `sh tools/build/r0f.sh host-test`, `build`, `package`, `xemu`.
  Native sanitizer tests and target link passed; D81 host structural/content
  checks passed. Xemu preflight failed closed for missing emulator and owner ROM.
  Physical testing is NOT VERIFIED. See `R0-F_BUILD_HANDOFF.md`.

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
