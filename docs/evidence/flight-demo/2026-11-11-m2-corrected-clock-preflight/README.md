# CC3 host-only checkpoint evidence

Analysis identity `65AERO-M2-FIXED-KERNEL-PREFLIGHT-3`, from source `fcba7cf`.
See [report](../../../reports/M2_CORRECTED_CLOCK_PREFLIGHT.md).

- `run-0/`: initial 18-test run, exit 1, original failed test/tool source.
  Fixture path alias and sampler-exclusion mistakes are preserved.
- `run-1/`: corrected fixtures, 18 tests, exit 0; exact source retained.
- `run-2/`: final 18 tests, exit 0; source-pinned preflight, exit 2.
  Complete commands, stdout/stderr and exact tool/test source are retained.
- `baseline-before.json`, `related-before.json`: preservation snapshots taken
  before implementation. The eight related checkouts remain untouched.
- `historical-preservation.*`: original read-only checker and its exit 0 result;
  480 unrelated paths and explicit Git-worktree provenance limitations.
- `check_scope.py`, `static-preservation.json`, `static-command.json`: focused
  ancestry, syntax, link, whitespace, JSON/contract and preservation checks.
- `host-tool.json`, `source-identities.json`, `final-source.tar.gz`: Python/tool
  identities and reproducible host sources. No SDK binaries or ROMs.
- `seal.json`: exact final packet membership, sizes and SHA-256 hashes.

All cost values for the actual changed executable are unknown. Synthetic host
fixtures establish model behavior only. No target compilation/relink, runtime
execution, rendering/oracle campaign, Xemu or physical testing was performed.
No sealed historical evidence, source or checker was rewritten.
