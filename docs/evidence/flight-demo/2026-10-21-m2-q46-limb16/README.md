# M2 PR2 bounded Q46 limb experiment evidence

[Handoff](../../../reports/M2_PR2_Q46_LIMB16_EXPERIMENT.md).
Baseline `8ee5214ea9c63b86e92ca9bc4fa0779115dbd57f`.

- `before/`, `source/`: exact old/new helper and changed test bytes.
- `proof/`: sanitizer equivalence, independent integer/carry checks and exact commands.
- `relink/`: host PASS, composed compile/link PASS, resident fit FAIL at `$ADC6`.
- `regression/`: independent Decimal/near-far/standalone target results.
- `comparison.json`: exact function, section, resident, scratch and identity changes.
- `cost-and-stack.json`, `analyze.py`: reproducible static helper closure analysis;
  structural instruction bounds only, no cycle/timing or full-renderer admission.
- `regression-extra-inputs.json`: private-header hash supplements older builder inventory.
- `preservation.json`, `inventory.json`: preserved scope and packet identities.

Helper saves 103 code bytes; total resident saves 101 bytes. Deficit remains
11,718. Both failed-fit identities and all earlier evidence are retained.
No Xemu, D81, SD, physical testing, publication or further optimization.
