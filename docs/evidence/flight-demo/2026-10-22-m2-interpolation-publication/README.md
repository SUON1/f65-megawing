# Bounded interpolation publication validation

Fresh checks from the isolated publication tree, integrating the reviewed
private helper and approved host verifier independently of renderer scaffolding.

- `proof/`: exact argv, exits, sanitized direct-helper/projection comparisons,
  regenerated corpus identities, standalone result and hygiene fixture tests.
- `standalone/`: fresh host, 3,857-case Decimal and 841-case clipping evidence;
  target compile/link logs, map, symbols, disassembly and input identities.
- `validation.json`: exact reviewed/fresh standalone comparison and corpus pins.
- `validate.py`: fresh validation recipe; never rebuilds the full composition.
- `preservation-before.json`, `preservation.json`: five unchanged original
  checkout digests, immutable packets, reviewed source scope, raw files,
  generated records and 20 unrelated entries.
- `whitespace-preflight.json`: the one exact archived font path needing a
  hash-bound whitespace exception; no evidence bytes are normalized.
- `verify.py`, `inventory.json`: publication seals and scope/link/syntax checks.

Raw binaries and fresh corpora remain in separate ignored build directories
recorded in `validation.json`. No target execution or composed relink occurred
during publication. Existing failure/verifier/relink packets remain unchanged.
See the [publication scope](../../../reports/M2_PR2_INTERPOLATION_PUBLICATION.md).
