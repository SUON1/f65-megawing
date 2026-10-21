# M2 full-composition prepared-context gate evidence

[Handoff](../../../reports/M2_PR2_FULL_COMPOSITION_GATE.md).
Base `0d42a8ce271a98abbffada019c403e31e7590e5d`.

- `fit.json`, `FIT.*`, `compile.txt`: integrated regression links but fails
  resident admission at `$8014`, 20 bytes over the existing ceiling.
- `regression-*`: fresh standalone host/oracle/target results; not full-composition evidence.
- `prepared-*`: new contract/context tests and exact commands.
- `generated-target-syntax.json`: include-only target syntax check.
- `current-inputs.json`: hashes for new contract/context/check source.
- `before/`, `preservation-before.json`: unchanged baseline identities and original
  modified-source bytes. Historical packets retain their own identities.
- `inventory.json`: hashes of every other file in this packet.

Raw outputs are retained under `build/flight-demo/m2-pr1-1792582284356607000/`,
`build/flight-demo/m2-pr2-fit-1792582301133356000/` and
`build/flight-demo/m2-full-host-1792582371186260000/`.
No target execution, Xemu, D81, SD or physical testing. Full renderer not built.
