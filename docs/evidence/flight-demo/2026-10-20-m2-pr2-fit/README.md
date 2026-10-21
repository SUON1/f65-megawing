# M2 PR2 integrated-fit evidence

Fresh compile-only fit attempt and unchanged PR1 regression rerun from main
`a9d3f796291f2941002b4d1f4c8fc48a9dba3c89`. See the
[handoff](../../../reports/M2_PR2_INTEGRATED_FIT.md).

- `fit.json`, `FIT.map`, `FIT.symbols`, `FIT.disassembly`, `compile.txt`: compiler
  succeeded, resident admission failed at `$9335` (4,917 bytes excess).
- `regression-*`: fresh unchanged PR1 host/oracle and standalone target results;
  these do not establish PR2 integrated fit.
- `preservation.json`: 790 unchanged fingerprints and the 20 unrelated entries.
- `inventory.json`: SHA-256 hashes of all other packet files.

Raw outputs retained at `build/flight-demo/m2-pr2-fit-1792542030866784000/`
and `build/flight-demo/m2-pr1-1792542041697467000/`. Binaries are local build
artifacts, not published evidence. Neither candidate was executed on target.
No Xemu, D81, SD or physical testing. No PR2 rendering/scanout acceptance.
