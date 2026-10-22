# M2 PR2 bounded local-forward guard correction

**READY FOR REVIEW — bounded size PASS; full resident fit FAIL.**

See [the report](../../../reports/M2_PR2_PROJECTION_FORWARD_GUARD.md).
The prior failed projection packet and report remain unchanged.

- `authority.md`: exact approved correction and stop boundary.
- `before/`: original failed-candidate source and task WIP before edits.
- `guard-only.diff`: the sole new production delta.
- `00-reference/`: copied identity-verified 34,221-byte reference evidence;
  no new reference target build. Raw artifacts retain their original paths.
- `02-equivalence/`: frozen 799,886-case sanitizer comparison and 34 contract
  checks, with exact compile/run commands in `comparison-checks.json`.
- `03-standalone/`: fresh host/Decimal/clipping/target compile-link/static proof.
- `04-candidate/`: fresh renderer host and single composed target relink,
  underlying command logs, maps, symbols, disassembly and five identical images.
- `comparison.json`: independently enumerated allocated ELF sections, gaps,
  owner-size checks, symbol costs, physical tool and raw artifact identities.
- `static-analysis.json`: unchanged stack-checker rejection, helper closure and
  loose instruction accounting; no integrated stack/timing or runtime admission.
- `preservation-before.json` and `preservation.json`: path/content preservation,
  historical inventories, generated files/ledgers and unrelated entries.
- `commands.json`: exact invocations and exits. The full-fit wrapper exits 1;
  bounded improvement is 72 bytes against the reference, not full admission.

Raw PRG/ELF/backend binaries remain in fresh ignored build directories recorded
in the comparison. Frozen corpus bytes remain in the prior ignored comparison
input path; identity is retained, with no regeneration or overwrite. No builds
or implementation followed the candidate relink. No Xemu, D81, SD, physical
testing, further optimization or publication occurred.
