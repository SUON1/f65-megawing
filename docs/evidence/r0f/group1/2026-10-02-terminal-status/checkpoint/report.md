# Group 1 terminal-only status diagnostic — 2026-10-02

The owner approved exposing the P06 terminal failure through a smaller status
byte while preserving every integrity check. This new copied-source diagnostic
fits; the previous [return-code experiments](R0-F_GROUP1_TERMINAL_DIAGNOSTIC.md)
remain failed and preserved. Physical P06's actual inner cause remains unknown.

## Design and authority

Inspected current state/WIP, repository workflow/programming/C standards,
Group 1 Build Intent and export amendment, private capture/transport policy and
interfaces, generated memory bounds, qualified P06 source, existing build and
native/emulator validators. Remote main remains
`c27d89787d1d5c4472e24262e0181c47943d46be`; work continues on
`codex/r0f-group1-resume-clock`. Source is a fresh copy of qualified P06,
not a root-source rebuild. No publication, SD write or physical retest is
included. Group 2 remains pending.

Reuse `r0fg1_export_status`, the existing protected byte at $2F98. It is
initialized to 6B, incremented at four terminal boundaries, and read by the
existing final lockout display. The pure export-policy state is separate and
unchanged. The nonreturning exporter replaces this byte with EXPORTING on
entry, then EXPORTED or FAILED as before. Its error byte and permit are unchanged.
The marker is observational. Export permission remains controlled by the
original policy, and the marker is not encoded into a successful trace.

| Final fault at tick 3200 | Preparation interval that rejected |
| --- | --- |
| 6B | DOS-context restoration before capture finalization |
| 6C | Capture preconditions and header/result writes |
| 6D | Acquired-region readback/CRC, capacity-tail verification or final CRC write |
| 6E | Transport preconditions, whole-trace readback/CRC or freeze |
| 6F | Stopped-service, capsule and terminal-entry readiness |

These are terminal-only markers. Earlier acquisition faults with the same
numeric values keep their existing meanings; interpret the tick, service mask and context.
A marker narrows the rejecting interval; several intervals contain multiple
inner conditions. No new
marker has been observed physically. P06 remains retired after 6B at tick3200,
with its actual SAVE verified and no trace files.

## Fit and hardware impact

The bounded new experiment used two target variants. Both were completed
within about four minutes; subsequent work qualifies the fitting identity.
The first new variant uses ordinary volatile C increments. It links to $C00E,
14 bytes over; it was never executed. Disassembly shows each increment uses
seven bytes (load/increment/store). The second uses one three-byte absolute INC
at each of the four points, saving 16 bytes. It fits at $BFFE, **2 bytes free**,
13 bytes larger than P06. No capacity, reserve or validation comparison changes.

The narrow inline helper declares compiler condition-code and memory clobbers.
INC changes N/Z and the named byte, preserves A/X/Y/Z/B, and accesses admitted
resident RAM. There are no new hardware-register accesses, MAP/base-page
changes, DMA operations, allocations or IRQ/NMI policy changes. Markers occur
after acquisition and IRQ shutdown. Boolean interfaces remain unchanged.
Protected placement is identical; only the existing byte's initial value
changes. Generated/public interfaces and both reserves remain unchanged.

Qualified PRG: 37518 bytes, SHA-256
`35f51114c5016b0e29962e038c48d7f48b9e8abca2136bdb0fe889f4c7570bae`.
Exact source: `build/r0f/group1/terminal-recovery/status-02/source-inputs/`.
The [patch](../../tools/diagnostics/r0f_group1_terminal_status.patch) applies
only to a fresh copy of P06's isolated source. The
[controller](../../tools/diagnostics/r0f_group1_terminal_status.py) reuses the
existing resume/capacity/carrier gates and pins the new diagnostic tools.

## Validation and boundaries

The existing builder linked both variants with exact input hashes and checked
protected IRQ/terminal disassembly. Only the fitting second variant executed.
Native ASan/UBSan owner/scene/workload/audio/display/pool/CRC checks pass,
including existing capture corruption/copy-failure cases and 83 codec rejects.
The resume-boundary host test still passes against the original P05 model.

`python3 -B tools/diagnostics/r0f_group1_terminal_status_validate.py build/r0f/group1/terminal-recovery/status-02`
passes: removing only marker calls/comments leaves capture and transport
executable token streams exactly equal to P06; four absolute INC instructions
and the initial 6B byte are verified. Seventeen extracted transport cases
exercise success, preconditions, read failure, CRC failure, all four audio
channels, display, IRQ masking, capsule guard/CRC/copy failure and NMI. They
check exact 6E/6F markers and permit denial under ASan/UBSan. Physical edges
are mocked; this does not establish the P06 inner hardware cause.

Focused NTSC and PAL each pass 3200 records, actual returning SAVE and complete
327680-byte export in 20 chunks, version-7 reduction, corruption/capacity checks
and nominal timing WITHIN_OBSERVED_BOUNDS. Screens show S:4 E:00 F:14. These are
local emulator results, not physical timing or resumed-workload acceptance.

The unchanged-PRG collision test passes: it preserves the existing filename,
returns failure S:5 E:03 F:00, and does not retry. All 47 Group 1 Python
regressions pass. Generated-output identity and exact patch replay pass.
Symbol-size comparison shows only main grows, by 13 bytes.

Fresh `R0FG1P07.D81` construction and independent structure/content gates pass.
It is 819200 bytes, SHA-256
`138644c5066288ba5e635cced33633c6f2c75902482566e9a6f24ccfe5e8daf3`.
All four fresh exact-name clean boots pass: two NTSC and two PAL, each with
3200 records, actual SAVE, 20 complete chunks, nominal timing, independent
version-7 reduction and corruption/capacity checks. Their screenshots are
byte-identical to the inspected focused-mode success screenshots. Canonical
bytes remain unchanged. P07 is **XEMU_BOOT_VERIFIED only**; SD and physical
gates are NOT RUN. The [frozen evidence packet](../evidence/r0f/group1/2026-10-02-terminal-status/README.md)
retains the source, checks and actual extracted artifacts.
No card access, hardware run, commit, push, PR, merge or acceptance occurred.

## Reproduction and next step

Apply the zero-context patch with `patch --batch --fuzz=0 -p1` only in a fresh
copy of P06's isolated source. Both variants retain exact builder commands and
input hashes in `build/r0f/group1/terminal-recovery/status-*/runtime-01/build.json`.
The qualifying local commands were:

```sh
python3 -B tools/diagnostics/r0f_group1_terminal_status_validate.py build/r0f/group1/terminal-recovery/status-02
python3 -B tools/diagnostics/r0f_group1_terminal_status.py verify
python3 -B tools/diagnostics/r0f_group1_resume_recovery.py ntsc --experiment build/r0f/group1/terminal-recovery/status-02 --image-name G1STA01.D81
python3 -B tools/diagnostics/r0f_group1_resume_recovery.py pal --experiment build/r0f/group1/terminal-recovery/status-02 --image-name G1STA01.D81
python3 -B tools/diagnostics/r0f_group1_terminal_status.py negative-export
python3 -B tools/diagnostics/r0f_group1_terminal_status.py carrier-build --name R0FG1P07.D81
```

The four carrier boots use the same controller's `carrier-boot` action with
`--mode 1/0 --number 1/2`; each uses a fresh exact-name disposable copy.
`carrier-finish` requires all four reductions and screenshot reviews. These
commands are retained provenance; do not rerun into existing evidence paths.

Review the exact diagnostic and its two-byte fit margin. A later owner-approved
P07 delivery must pass live allocation, hash, safe-eject and physical chooser
checks. Preserve P06. The next physical photo can distinguish terminal intervals;
no specific CRC, capsule or hardware-register cause is established yet.
