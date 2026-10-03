# P07 physical terminal-readiness failure — 2026-10-03

Owner supplied this photo after the P07 delivery and physical-run instructions.
It reads **6F / 0A / 0C80 / 1F / 00**: tick 3200, all five resumed-service
advance bits, and a terminal readiness failure. Execution is visible. Exact
filename confirmation, video mode and fresh platform identities remain unrecorded.

For the qualified P07 source, `r0fg1_transport_prepare()` advances the status
byte to 6F only after complete trace readback/CRC and export freeze succeed.
It next checks stopped display/audio, IRQ masking, restored-ROM status,
protected capsule guards/copy/CRC and NMI status through `r0fg1_export_begin()`.
The exact rejecting predicate is unknown. The photo's NMI field is zero;
that does not prove every readiness predicate. Export permission is not reached
on this rejection. No physical trace or returning SAVE has yet been inspected
for this run, and no full-result or timing oracle PASS is claimed.

Source identity and gates remain in the unchanged
[terminal-status packet](../2026-10-02-terminal-status/README.md).
PRG SHA-256: `35f51114c5016b0e29962e038c48d7f48b9e8abca2136bdb0fe889f4c7570bae`.
Canonical D81 SHA-256: `138644c5066288ba5e635cced33633c6f2c75902482566e9a6f24ccfe5e8daf3`.
Retained installation records establish exact staged/final/mounted hash,
one 819200-byte extent at device offset 64745472, and safe eject.

Preserve P07 as **INVALID — DO NOT USE**; do not rerun, overwrite, rename or
repair it. Next: returned-card read-only snapshot/extraction, then a bounded
copied-source diagnostic to distinguish the readiness predicates while keeping
every integrity check. No new build, SD operation or target execution was
performed while recording this observation. Group 1 acceptance and Group 2
progression remain pending. CURRENT_STATE and prior freezes are unchanged.

Authority: current WIP and Group 1 Build Intent, repository workflow and D81
gate/workflow. This is off-card evidence preservation only. Registers/clobbers,
CPU-visible/physical memory, MAP/base-page, DMA, timing/deadline and IRQ/NMI
changes are non-applicable; generated/public interfaces are unchanged.
