# RH001 — no-restart handoff development, 2026-09-18

Owner direction: resume the same application without restarting or reloading.
That decision is implemented in a private, standalone returning-handoff proof.
**This is not the full combined R0-F closeout harness or a hardware release.**

## Implemented sequence

1. Preserve the original KERNAL RAM context before C startup and preserve DOS
   context before application takeover. Use opaque snapshots, not guessed
   private-variable reconstruction.
2. Back up all 128 KiB of ROM, reclaim and overwrite it with a deterministic
   pattern, and run the existing C synthetic model to tick 33.
3. Reject storage admission while ROM is reclaimed.
4. Quiesce application services; restore and verify every ROM byte and ROM
   protection. Back up application low-memory and DOS-overlay contents.
5. Swap to KERNAL low-memory/base-page/hardware-stack context; initialize via
   public APIs, load a known token, save an application-derived record, and
   reload that record into a separate buffer.
6. Restore application memory, base page, hardware stack/SP and canonical
   MAP/port/IRQ state. Check all contents and advance the **existing model**
   to tick 34. No reset trap, jump to startup, application reload, or model
   reset occurs at the handoff.

## Reviewed authority and impacts

Inspected: `F65_OFFICIAL_RECORD.md`; complete frozen
`spec/architecture/F-65 Megawing Revision 1.4.1.md`, including MemoryAccessABI;
approved Read-First, AD-001 and current approval record; current `memory/`
and `interfaces/` contracts/calling convention; relevant candidate architecture,
gameplay and engine documents; R0-C ROM research; R0-F full-closure plan,
stage/CF001/platform contracts, sources, linker, builder and oracle; root D81
gate. Source-bound rationale and rejected prototypes are recorded in
`docs/decisions/R0-F-RH001-NO-RESTART-HANDOFF.md`.

New paths: `src/diagnostics/r0f/resume{,_model}.c`, `resume_model.h`,
`src/platform/r0f/resume_45gs02.s`, `interfaces/r0f_resume_contract.json`, its
generated header, `memory/r0f-resume-memory-ledger.json`,
`tools/diagnostics/r0f_resume_build.py`, `r0f_resume_host_test.c`, and
`tools/generators/src/main/java/f65/tools/R0FResumeOracle.java`.
Existing CF001 implementation and physical evidence are preserved.

C remains the workload/model language. Assembly is confined to startup and
the platform/ROM boundary. A/X/Y/Z/P/B follow the documented private wrapper;
X/Y/Z/B/P and the application stack/SP are preserved, A returns status. Q is
not independently preserved. B=0 exists only inside KERNAL scope; C resumes
with B=2, port 35, zero MAP offsets/MB selectors and resident vectors.
Native KERNAL uses MAP E000–FFFF → 03E000–03FFFF; ROMC supplies 02C000.
D030 ROME alone is the wrong bank for native KERNAL.

Linked code/data/BSS/noinit remain below 8000; the map includes the 5632-byte
opaque KERNAL snapshot, C runtime and stack/storage buffers. C stack is
C000–CFFF. ROM/Attic backup retain the CF001 ranges. Temporary application
low-memory backup is 050000–051CFF; original DOS context is 054000–055FFF;
application DOS-overlay backup uses 01D000–01EFFF. Reserve 058000–05FFFF
is read-only and CRC checked. No production ownership/capacity/ABI changes.

Application DMA/audio/IRQ are quiescent throughout the transition. KERNAL
owns any internal DMA during storage; this is not concurrent DMAService
qualification. IRQs are masked. No storage-time deadline is claimed, and
a hung KERNAL call is not recoverable by a same-CPU polling timeout. NMI/
RESTORE injection, storage-error recovery, repeated transitions and physical
stack-depth behavior still need qualification. The final display is a result
screen, not a claim that full rendering/audio scheduling has been resumed.

## Verification

- `python3 tools/diagnostics/r0f_resume_build.py build`: PASS; 16,842,752
  sanitized admission/invalid-state/lockout checks; compile/link/map/symbols/
  disassembly; ROM-call allowlist; startup-order and branch-encoding gates;
  independent Java model golden `D9EEAB81` (33) → `400B181F` (34).
- First successful clean NTSC run: `xemu-1-1789767957888359000`; zero faults,
  resumed state 05, I/O phase 05, tick 0022, result CRC `C02E663B`. Actual
  ROM bytes and saved file were independently compared; screenshot reviewed.
- Final strengthened NTSC: `xemu-1-1789768133106605000`, result CRC
  `32ECFBA6`, PASS. PAL: `xemu-0-1789768137122746000`, result CRC
  `8B769569`, PASS. Both have fault 00, state 05, phase 05, tick 0022,
  actual independently extracted SAVE bytes and 68 rejected corruptions.
  Both screenshots were inspected and are legible/correct.
- `PYTHONPYCACHEPREFIX=/tmp/f65-rh001-pycache python3 -m py_compile tools/diagnostics/r0f_resume_build.py`:
  PASS. `git diff --check`: PASS.
- Generated PRG/ELF/map/symbols/disassembly and exact per-input hashes:
  `build/r0f/resume/`. PRG SHA-256:
  `b856ad29b0ac06939083dd54140136d438037ce41c3f49f00163d6b2c52efcc9`.

Retained evidence and exact source snapshots:
`docs/evidence/r0f/resume/2026-09-18/`. Current source baseline is
`82df3dbffdfc562c496a8fffe768434d169d7698` plus the hashed working-tree inputs.
The preliminary debugger helper was removed after diagnosis; rejected run
dumps remain under `build/r0f/resume/` and are not acceptance evidence.

Each run fresh-formats and populates a separate disposable RH001IO.D81 in one
pinned c1541 invocation. Header/BAM/directory/chains/allocation/free count and
every extracted payload are checked before Xemu. The intentional target SAVE
is followed by independent extraction/content/structure validation, retaining
both initial and post-transaction hashes. These are Xemu-only writable test
fixtures, **not SD or physical carrier candidates**. No SD card was touched.

## Remaining work / next development entry point

Integrate this lifecycle into the full combined workload, including resuming
active display/audio/IRQ/DMA scheduling rather than only the retained C model.
Reconcile the linked footprint and transient ownership for that combined
candidate; do not simply concatenate CF001 and RH001 allocations. Complete
the outstanding renderer/input/cadence/window/fault/measurement matrix in the
full-closure plan, then run the exact combined candidate in Xemu before any
SD/physical preparation. Physical measurement and owner acceptance remain
mandatory. Do not ask the owner to choose restart versus resume again.

No commit or push was performed. No user hardware action is requested yet.
