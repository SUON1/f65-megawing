# Bounded interpolation experiment evidence

**FAILED I5 prerequisite stack gate; no composed candidate relink.**

See the [result report](../../../reports/M2_PR2_INTERPOLATION_BITWALK_EXPERIMENT.md)
for scope, measurements and limitations. I1–I6 approval is in the current task
prompt; the copied planning intent is historical provenance.

- `00-reference/`: one fresh exact 34,149-byte reconstructed reference, including
  raw builder report. Known full-fit FAIL retained.
- `01-direct/`: frozen direct-helper old/new/independent integer comparison,
  457,334 cases and 29,269,376 bit-state steps, ASan/UBSan PASS.
- `02-projection/`: unchanged 799,886 cases +34 contracts, ASan/UBSan PASS.
- `03-standalone/`: host/oracles PASS, target compile/link artifacts and stack
  failure. There is deliberately no success `build.json`. Recovered command
  record is labeled separately. Read-only ELF accounting does not bypass the
  failed admission gate.
- `04-renderer-host/`: host only, three successful commands and five exact images;
  no backend/target command or candidate composed artifact.
- `reference_geometry.c`, `reference_interpolate.inc`, `pre-edit-freeze.json`,
  `corpus-identity.json`, `bit-state-proof.md`: reference and corpus frozen before
  editing; independent expectations and inductive arithmetic/bit proof.
- `source/`, `candidate.patch`, `source-freeze.json`, `reconstruction.json`:
  restored source identities and exact two-statement candidate boundary.
- `comparison.json`, `artifact-identities.json`: all allocated ELF sections,
  raw artifact bytes/hashes and explicitly unmeasured composed candidate.
- `preservation-before.json`, `preservation.json`, `inventory.json`: original
  checkouts and historical evidence protection; this packet's final identities.
- `run_recipe.py`: exact recipe split into host/link phases; only host phase used
  for the candidate. `collect.py` only preserves/inspects existing artifacts.

Fresh ignored raw directories are pinned in `artifact-identities.json`. They
retain executables, corpora and PRG/ELF bytes; no old output was overwritten.
The previously generated projection corpus was reused read-only after exact
hash verification. No Xemu, D81, SD, physical or target execution took place.
