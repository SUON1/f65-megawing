# Bounded transform-sequence experiment

[Handoff](../../../reports/M2_PR2_TRANSFORM_SEQUENCE_EXPERIMENT.md).
Founder approved S1–S6 in the retained Build Intent. Main baseline:
`b3406ed8b9e141b50ca7ea7d3b5edd169c1ae310`.

- `00-reference/`, `reference-gate.json`: exact reconstructed failed composition;
  all 79 inputs, tools, sections, owners and PRG hash match the historical artifact.
- `before/`, `reference_transform.inc`, `source/`: archived expressions and exact
  candidate production/test source. No historical packet changed.
- `01-transform-proof/`: exhaustive ASan/UBSan equality, failure/alias coverage,
  independent integer equations and exact commands/logs.
- `02-q46-proof/`: unchanged arithmetic/carry equivalence and independent oracle.
- `03-standalone/`: host/Decimal/clipping and standalone target static checks.
- `04-candidate/`: single candidate relink, sections/owners, disassembly and images.
- `run_recipe.py`: exact reference command replay split into host and link phases;
  host images were compared before the one candidate target relink.
- `comparison.json`, `cost-and-stack.json`, `analyze.py`: actual resident result,
  direct-call/tail-jump stack analysis and conservative instruction-work bounds.
- `prelink-validation.json`, `preservation.json`, `inventory.json`: frozen inputs,
  preservation and packet identities.

**2,072 resident bytes saved; 9,646-byte deficit remains. Full fit FAIL.**
No target execution, Xemu, D81, SD, physical testing or publication.
Implementation stopped immediately after the relink and measured report;
only read-only accounting/evidence retention and handoff followed.
