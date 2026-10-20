# M2 PR1 host and compile-only evidence

Status: READY FOR REVIEW. See the [handoff](../../../reports/M2_PR1_GEOMETRY.md).

- `build.json`: exact source/tool hashes, commands, native/oracle results, target sections and owner symbols, stack analysis and non-execution boundary.
- `contract-tests.txt`, `host.txt`, `oracle.json`: actual validation results.
- `M2.map`, `M2.symbols`, `M2.disassembly`: linked probe accounting, not target execution.
- `target-build.txt`: compiler diagnostics (empty on success).
- `preservation-before.json`, `verification.json`: baseline fingerprints, unchanged unrelated entries, source identity and actual output directory.
- `inventory.json`: SHA-256 of every other packet file.

The raw probe, native executables and earlier attempts remain in fresh local build directories. No target program was run. No PR2, Xemu, D81, SD or physical testing. This packet does not claim a usable display mode, atomic hardware activation, target timing, physical high-water, flight or full-harness acceptance.
