# Bounded prepared-projection experiment

**READY FOR REVIEW — bounded size gate FAILED.** One reference and one candidate
composed relink; no implementation or target builds after the candidate relink.
See [the report](../../../reports/M2_PR2_PROJECTION_EXPERIMENT.md).

- [Reconstruction](reconstruction.json) verifies all 79 inputs; 16 exact retained
  source restorations are experimental scaffolding, not integrated acceptance.
- [Reference verification](reference-verification.json) and `00-reference/`
  retain the exact fresh 34,221-byte PRG reconstruction. `raw-build.json` is the
  unmodified builder record; `build.json` adds independently parsed owner kinds
  for replay. Historical evidence is untouched.
- [Corpus identity](corpus-identity.json) and [pre-edit freeze](pre-edit-freeze.json)
  precede the candidate edit. The 44,793,616-byte input remains in the fresh
  ignored `build/flight-demo/projection-comparison/corpus.bin`; regenerate only
  as a separate authorized replay, with the archived generator and exact hash.
- [Command ledger](commands.json), `host.txt`, `03-standalone/` and `04-candidate/`
  retain host, oracle, sanitizer, target compile/link and five host images.
- [Comparison](comparison.json) independently enumerates ELF SHF_ALLOC sections,
  raw PRG/ELF identities, exact symbols, tools and owner objects.
- [Static analysis](static-analysis.json) records the fail-closed stack result,
  complete helper closure and loose instruction bounds. These are no cycle or
  service admission. The analyzer is read-only and never invokes the compiler.
- [Preservation](preservation.json) checks 31,267 paths across two prior checkouts,
  20 unrelated entries, generated files/ledgers and 12 historical inventories.
- `source/`, `reference_geometry.c` and `reference_project.inc` retain exact
  candidate/reference implementation and focused test source. No public ABI,
  compiler flags, ledger or memory ceiling changes.

Raw binaries remain under the distinct fresh output directories recorded in
`comparison.json`; archived logs/maps/disassemblies/images are review evidence.
No Xemu, D81, SD, physical testing, publication or later optimization occurred.
