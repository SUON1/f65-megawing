# M2 PR2 fit-overrun correction evidence

[Handoff](../../../reports/M2_PR2_FIT_OVERRUN_FIX.md).
Base `0d42a8ce271a98abbffada019c403e31e7590e5d`.

- `fit.json`, `FIT.*`, compile/cursor logs: restored provisional integrated gate,
  resident end `$7FDC`, 36 bytes spare.
- `regression-*`: fresh independent oracle, sanitizer and standalone target checks.
- `prepared-*`: exact host commands, contract tests and registration regressions.
- `*.before.c`, `preservation.json`: original modified-source bytes and preservation check.
- `inventory.json`: hashes of every other packet file.

Fresh raw output identities are recorded in the handoff. The failed `$8014`
packet is preserved unchanged. No target execution or full-composition claim.
