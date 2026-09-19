# PF001 development evidence

See `docs/reports/R0-F_PLATFORM_HANDOFF.md` for scope, exact commands, impacts,
observations, failed experiments and remaining full-combined dependencies.

`boot-1/` and `boot-2/` retain the final normal-speed direct-PRG Xemu runs.
Original build-directory identities and command arguments remain unchanged in
`evidence.json` and top-level `xemu.json`; only these archival paths differ.
Both results pass the independent Java oracle and its 316 rejection tests.
Screenshots were visually reviewed. `accounting.json` is the pre-run build
snapshot, with per-input hashes; use `xemu.json` for subsequent run status.
Top-level PRG/ELF/map/symbol/disassembly and native output belong to this final
build. `SHA256SUMS` covers retained artifact bytes relative to this directory.

`development-port-failure/` and `development-audio-failure/` preserve earlier
failed observations. They are **not** executions of the final top-level PRG.
Their original transient PRG paths have subsequently been rebuilt; do not
associate the final PRG hash with those failures. The port experiment exposed
base-page linker relaxation; the audio experiment used accelerated Xemu and
failed progress while its audio callback followed real time. Neither assigned
a D81 identity or reached SD/hardware.

No D81, physical-card dump or disposable 4GB Xemu SD clone is packaged here.
No artifact establishes calibrated time, full workload, exact-D81 loadability,
physical correctness, R0-F acceptance or production authority.
