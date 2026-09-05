# R0-F first bounded test build — 2026-09-05

Implemented and compiled; **two clean Xemu boots now pass**. The exact candidate
may proceed to gated native-slot SD transfer, not directly to hardware testing.
This is the owner-requested first functional/raster proxy slice, not completion
of the physical R0-F measurement program.

## Exact candidate

- Filename: `build/r0f/F65R0F1.D81` (819,200 bytes).
- SHA-256: `9b539a14f08d671195ef71e54bbacb3eacd5258634f7a29396bf00a068cddd89`.
- Current state: `XEMU_BOOT_VERIFIED`; label `F65 R0-F1`, ID `65`.
- Entry: `AUTOBOOT.C65` loads `R0F-PROOF` from device 8.
- Target PRG: 4,694 bytes; SHA-256
  `510c2bfc8686f86b5fd934edd0b9863c0a176951a2871eaa0f990c8e0cec106e`.
- Source base: `b5b54bd0af18f899c78857fd2f69ba7b969fe856` plus the working-tree
  inputs identified by SHA-256 in `host/build-accounting.json`. The build does
  not falsely identify these changes as already present in that base commit.
- No previous D81 was copied, reopened to append, or used as a payload source.
  Format and all three writes occurred in one pinned clean-c1541 invocation.
- This filename is reserved locally; absence from the physical card has not
  been checked. A collision must be resolved before delivery, never by renaming
  this candidate or overwriting a prior tested card identity.

## Implementation and inspected contracts

Inspected requirements, registers/clobbers, CPU/physical memory, inherited
MAP/base-page/IRQ context, DMA/NMI non-applicability and risks are recorded in
`R0-F_INTERFACE_LEDGER_IMPACT.md`. No preserved specification was changed.

New paths: `src/r0f/`, `src/diagnostics/r0f/`, `src/platform/r0f/`,
`interfaces/r0f_proof_contract.json`, generated `r0f_interfaces.h`,
`memory/r0f-memory-ledger.json`, `tools/build/r0f.sh`, and
`tools/diagnostics/r0f_*`. R0-F control/evidence records and the official index
were updated; R0-A–E source/evidence and the root D81 gate were preserved.

The five inherited functional cases retain the checksum `393387319`, lag
publication/skipping counts `202/798`, shedding mask `63`, one synthetic fault,
and pressure input/audio counts `2000/2000`. These are model checks, not actual
entity processing, hardware input/audio, real overflow, or concurrency proof.

The diagnostic now retains 80 raw raster deltas in requested phase order with
five validity masks. Reset precedes phase acquisition. Timeout is explicit,
zero remains a valid modulo observation, and the banner is conditional rather
than an unconditional PASS. Wraps remain unresolved. No percentile, latency,
cycle, real scheduler or physical-limit claim is made.

## Generated artifacts and accounting

`build/r0f/` contains source-built PRG/ELF, generated map, symbols, disassembly,
tokenized BASIC plus listing, host-test report, accounting, construction logs,
D81 candidate and release manifest. Reproducible generation is available;
`package` refuses an existing identity and must not be bypassed by deleting it.

Linked text: 4,119 bytes; rodata: 551; data: 0; BSS: 192. Snapshot records occupy
$3255–$3314. Compiler/runtime startup is included in the linked output. Result
storage is $1900–$19FF; software stack top is $D000. Dynamic software/hardware
stack high-water remains NOT MEASURED. Reserve allocation is zero; no new DMA,
MAP, IRQ or NMI operation was added.

## Commands and observed results

| Command | Result |
|---|---|
| `sh tools/build/r0f.sh host-test` | PASS: native C, address/undefined sanitizers; five cases; 80 non-monotonic/wrapping mock samples; injected acquisition timeout; rejection of forged functional PASS |
| `sh tools/build/r0f.sh build` | PASS: pinned LLVM-MOS compile/link and map bounds; symbols/disassembly emitted |
| `sh tools/build/r0f.sh package` | PASS: source build, pinned tokenizer, one-session fresh construction, automatic host gates |
| `python3 tools/diagnostics/r0f_d81_loadability_gate.py . build/r0f/F65R0F1.D81` | PASS: independent geometry/header/BAM/directory/ownership/chain/block accounting and raw/extracted payload equality |
| `sh tools/build/r0f.sh package` (second invocation) | Expected exit 2: refuses existing identity; bytes unchanged |
| `sh tools/build/r0f.sh xemu` | Exit 2, NOT VERIFIED: pinned Xemu binary and owner ROM path unavailable |
| `git diff --check` | PASS |

Native C/Python regression tooling is supplementary. The full Java R0-F oracle
is not implemented/run; pinned JDK is absent. No host test substitutes for Xemu
or hardware. The two-boot runner subsequently executed successfully; see the update below.

## Next required input and unresolved obligations

**Update:** the owner supplied the other checkout location. Its ROM and Xemu
matched the lock, and prior logs located the initialized emulator SD image.
The previously blocked command then passed both clean boots. Evidence:
`docs/evidence/r0f/xemu/R0F-XEMU-VERIFICATION.md`. The location request below is
historical and resolved. Next is the gated physical-card native-slot workflow;
all physical measurement obligations remain pending.

Provide the location of the owner MEGA65 ROM matching the toolchain lock and,
if already installed, the pinned Xemu binary and initialized emulator SD image.
Use `F65_MEGA65_ROM` and `F65_MEGA65_SD_IMAGE` for emulator inputs. Do not supply
the physical SD card yet. The runner uses disposable emulator-SD copies.

After two exact-image Xemu boots pass, use only the previously agreed MEGA65
native contiguous-slot workflow, with raw FAT32 one-extent/hash/safe-eject gates.
No physical chooser or runtime test has occurred. Full platform identity,
independent scheduling/phase sweep, calibration, rolling deadlines, actual
input/audio latency, high-water and separately admitted DMA/IRQ work remain
pending. R0-F, measured limits and Phase 1 remain unopened/unpassed.
