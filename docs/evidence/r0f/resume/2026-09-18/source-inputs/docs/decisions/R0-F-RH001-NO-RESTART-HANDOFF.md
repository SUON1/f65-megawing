# R0-F RH001 — same-run ROM/storage handoff development

2026-09-18. Owner decision: the application must resume **without restarting
or reloading**. The subsequent instruction authorizes continued development.
This is a private R0 proof under the existing additive platform approval, not
a production ABI promotion, parent-spec approval, or R0-F acceptance.

## Inspected authority and contracts

Official record first; complete frozen Architecture 1.4.1 and MemoryAccessABI;
approved Read-First, AD-001 and current approval; current memory/interface
registries and B-register calling convention; candidate Architecture 1.5.1,
Engine 0.2 and Gameplay 0.2; R0-C ROM research and deferred contract; R0-F
full-closure plan, stage records, CF001 contract, C/platform/model/assembly,
linker/build/oracle and verified physical retest; root D81 gate.

No usable returning ROM/storage wrapper exists in those contracts. RH001 is
an additive qualification of that missing boundary, not a claim that CF001
already implemented it. Existing CF001 source, generated target and evidence
are not changed by this experiment.

## Source-bound approach

Official MEGA65 developer-guide source pinned at
`0210345cd9cf19629010277732280e9e7248771e`:

- [KERNAL jump table](https://github.com/MEGA65/mega65-user-guide/blob/0210345cd9cf19629010277732280e9e7248771e/appendix-kernal-jumptable.tex):
  prerequisites require bank-0 low memory, B=0 and E000–FFFF mapping to
  03E000–03FFFF. Calls may clobber all registers. RAMTAS initializes KERNAL
  variables; IOINIT initializes peripherals and DOS; RESTOR installs KERNAL
  vectors; CINT initializes the editor; CLRCH establishes default channels.
  These return to their caller.
  RAMTAS prevents a clean return to the old BASIC program; RH001 never makes
  that return. The running C application continues on its existing stack.
- [Memory chapter](https://github.com/MEGA65/mega65-user-guide/blob/0210345cd9cf19629010277732280e9e7248771e/memory.tex):
  KERNAL workspace 0002–15FF, DOS workspace 010000–011FFF. D030 ROM banking
  accesses bank 2, NOT native bank-3 KERNAL. Native calls require MAP, and
  D030 ROMC enables the bank-2 C000 interface used by KERNAL. Private
  KERNAL variables are not an API: RH001 uses public initialization instead
  of writing guessed internal fields.
- CF001's pinned core ROM-protection implementation and immutable backup
  remain the source for the reclaim/inverse byte operations. Initialization
  is attempted only after every ROM byte and protection state are verified.

The public LOAD/SAVE interface uses SETBNK/SETLFS/SETNAM. A disposable,
fresh-formatted, host-gated Xemu fixture contains a known 32-byte PRG token.
RH001 loads it, saves a 32-byte application-derived record under a new name,
then loads that record into a different buffer. A host checker extracts and
compares the saved file independently. No replace prefix, arbitrary pathname,
SD operation, ROM upgrade, RESET_RUN, reset trap or program reload is allowed.

## Memory, registers and lifecycle

Machine-readable private layout: `interfaces/r0f_resume_contract.json`.
Standalone overlay only; not co-resident with CF001 or production. Linked
code/data/static stack 002001–007FFF; dynamic C stack C000–CFFF, hardware
stack 0100–01FF. C follows the pinned LLVM-MOS A/X/Y/Z/P/scratch convention.
Base page 0200–02FF is saved to linked storage in assembly before any ROM
call and restored before returning to C. Q is not separately preserved when
A is the return status. The helper saves/restores X/Y/Z/B/P/SP; entry requires
canonical B=2 with IRQs already masked. No C callback occurs with B=0.

Low-memory hot/capture bytes 0300–1FFF are copied into resource staging
050000–051CFF before KERNAL initialization, then restored. DOS temporarily
uses 010000–011FFF: the platform first copies its synthetic application
contents to 01D000–01EFFF (8 KiB of the existing shared transient workspace),
then restores every byte after the transaction. The independent checker
recomputes the address-derived pattern CRC. This is a quiescent proof-only
overlay, not a change of production ownership or permission to share that
scratch concurrently. Full combined-workload integration remains outstanding.
No production allocation or ownership is changed. The synthetic retained
model is linked C BSS. ROM 020000–03FFFF and immutable Attic backup
08000000–0801FFFF use the existing bounded CPU-copy implementation. Reserve
058000–05FFFF is read only. No reserve borrowing. Final screen uses the
existing HUD/color slices. KERNAL may reset video state during the call.

No application DMA is outstanding/submitted during handoff. KERNAL can use
its own DMA internally, so this is an exclusive platform/storage phase, not
a concurrent DMAService test. IRQs remain masked during initialization and
the private transaction; CIA interrupt masks are disabled again on exit.
NMI/RESTORE interference invalidates evidence. Canonical MAP offsets and MB
selectors zero/EOM, MEGA65 I/O, port 35, B=2 and resident vectors are restored
before C resumes. During a ROM call, MAP maps E000–FFFF to 03E000–03FFFF
(upper offset 30000, only uppermost 8 KiB selected). This is necessary because
IOINIT itself changes D030 while executing: a D030 ROME-only overlay is not
a stable call environment. The first prototypes exposed this in Xemu and
were rejected, including their apparent file-operation completion. Each call
re-establishes the documented mapping/base-page prerequisites. No temporary
8000–BFFF mapping scope is used by our wrapper. KERNAL's internal mappings
are not exposed as public C state.

The storage gate rejects calls while ROM is reclaimed. Failed restoration
never enables KERNAL calls. A returned storage error is recorded and not
reported as resume success. A hung KERNAL/hypervisor call cannot be bounded by
a polling timeout on the same CPU; the Xemu process timeout is a harness
failure, not recovery proof. No tick/deadline guarantee applies to this
explicitly quiescent lifecycle transition.

## Validation and non-promotions

Follow-up diagnosis: preserving ROM alone does not preserve KERNAL's RAM
context. In particular, the proof's stack seeding destroys RAM content in
page 1. RH001 now snapshots 0000–15FF opaquely into linked `.noinit` in a
startup-only assembly path before relocating B or initializing C state. It
does not reconstruct or patch individual KERNAL fields. The wrapper saves
the complete application page-1 stack and SP in linked BSS, restores the
saved KERNAL context (excluding CPU ports), switches to its own SP=01FF,
and restores the application stack/SP/B=2 context before returning. The C
continuation is not restarted. DOS entry context is similarly saved to
054000–055FFF, separately from the application's DOS-overlay state backup.
KERNAL calls remain exclusive, with IRQs masked. These additional private
scratch ranges are recorded in the RH001 ledger; production ownership and
reserve remain unchanged. The temporary call-index markers at 1F10–1F11
are removed by restoration of application low memory. A full physical
stack-depth and repeated/faulted transition qualification is still required.

Measured wrapper assembler gap: the pinned assembler relaxed the snapshot
loop's BNE to bytes `D3 79 FF` at 20A1. Xemu stopped on a BRK at 201C (monitor
PC 201D), one byte before the intended 201D loop head. No source or memory
corruption was present in that instruction sequence. RH001 uses short
inverse branches plus absolute JMP for out-of-range assembly branches and
rejects all 16-bit branch encodings in its startup/storage code. This is a
bounded platform-wrapper workaround, not permission to replace C workload
code with handwritten assembly. Earlier apparent progress that passed through
relaxed long branches is rejected, not accepted as KERNAL behavior evidence.

Commands: `python3 tools/diagnostics/r0f_resume_build.py build`, then
`python3 tools/diagnostics/r0f_resume_build.py xemu 1` and `... xemu 0`;
`git diff --check`. Build emits PRG/ELF/map/symbols/disassembly/input hashes;
native sanitizer tests cover the admission state machine. The independent
Java checker checks result CRC, restoration and retained-state evidence.
Each Xemu run freshly constructs its own disposable RH001IO.D81 in one
pinned c1541 invocation and checks structure and every extracted payload
before mounting. Its intentional SAVE mutation is retained as test output,
never as a releasable carrier. No SD transfer command exists in this runner.

Physical tier is NOT RUN. RH001 is not the requested final combined hardware
carrier. Full renderer/input/cadence/IRQ/window coverage, physical clock
uncertainty, full combined-workload integration, storage faults and
the corresponding hardware acceptance remain obligations.
