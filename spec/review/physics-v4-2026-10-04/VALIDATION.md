# Validation and handoff

Status: READY FOR REVIEW. Documentation tier only. 4 October 2026.

## Commands and results

From this package directory, using Python with pypdf:

```sh
python3 verify-package.py
```

Checks: package SHA-256 identities; all 18 present corpus hashes; internal Markdown links; proposed Main parent hash; historical Main/Gameplay appendix content (only new-copy hard-break notation normalized); inherited math expressions; 40 PDF pages, revised section markers, embedded source hash and absence of replacement characters; tracked scope and whitespace including untracked new text files.

PDF generation uses the checked-in renderer with external dependencies:

```sh
node render-physics.cjs F65_Flight_Physics_and_Simulation_Engineering_v4.0_R1_REVIEW_DRAFT.md output/pdf/F65_Physics_v4.0_R1_REVIEW_DRAFT.pdf /path/to/runtime/node_modules /path/to/katex-package
```

Actual runtime: bundled Node/marked/playwright; KaTeX 0.16.22 downloaded into temporary storage; installed Google Chrome headless. Strict rendering succeeded for all 126 math expressions, with no overflowing display equations. The canonical Markdown and generated PDF are separately hashed in review-identities.json. PDF metadata may vary on regeneration; compare source and rendering rather than assuming byte-reproducible PDF metadata.

All 40 final pages were rasterized with `pdftoppm -r 55 -png` and visually inspected. Fixed the split Appendix A heading; final pages have readable math, tables, headers and footers without observed clipping/overlap. PDF content extraction found all added correction sections and no replacement glyphs. The source equations were not changed by this correction pass.

Full Main/Gameplay diffs were inspected against their approved bases. Runtime/AI revisions use exact base-plus-amendment form to avoid PDF transcription loss. Local links pass. Existing corpus, manifest, historical evidence, interfaces, ledgers and production code remain unchanged. Only isolated-worktree WIP and the new package change.

## Evidence limits and next action

No compiler/target build, Xemu, physical hardware, pilot handling or production budget validation was run or implied. No CI run was triggered; the local documentation checks include new untracked files. Current R0-F and measured-limit obligations remain open.

Founder should review the corrected Physics and coordinated successor drafts. Acceptance of these exact identities, deliberate manifest/project-truth adoption, publication and merge remain later decisions. The original checkout and Downloads inputs are preserved.
