# Physics v4 adoption validation - 4 October 2026

Local adoption on codex/physics-v4-review-revisions; no commit, push or merge.

- Corpus verification: all 24 present manifest identities match disk, including separate canonical Physics Markdown and generated PDF identities.
- Preservation: all 18 original corpus hashes match the HEAD baseline. All 10 hashed R1 review-package artifacts remain unchanged. Historical evidence, interfaces, memory ledgers and implementation were not modified.
- Current authority order: Main v1.7, Gameplay v1.1, Runtime v1.1 candidate, Physics v4.0, Graphics v2.1, Audio v1.0, SensorAndTrack v1.0, AI v1.1.
- Runtime/AI incorporated base keys resolve to preserved source PDFs. Superseded standalone revisions are provenance, not competing current authorities.
- Gameplay's current parent hash matches adopted Main v1.7.
- Markdown links, new-current-document whitespace and `git diff --check`: PASS.
- Physics's 126 inherited math expressions retain the original expression digest. Strict KaTeX generation reports no errors or overflowing display equations.
- Final PDF: 41 pages, embedded canonical source hash verified, approved status present, no obsolete unapproved cover label or replacement glyphs. All pages rasterized using `pdftoppm -r 50 -png` and visually inspected; no observed clipping or overlap.
- PDF build command: `node tools/docs/render_physics.cjs spec/subsystems/F65_Flight_Physics_and_Simulation_Engineering_v4.0.md spec/subsystems/F65_Flight_Physics_and_Simulation_Engineering_v4.0.pdf <runtime-node-modules> <katex-package-root>`. Used bundled Node/marked/playwright, KaTeX 0.16.22 and installed Chrome. PDF metadata is not claimed byte-reproducible.
- Read-only hash/link/scope checks were performed with Python hashlib/json/re, pypdf and Git. Final exact identities are in spec/manifests/spec-corpus.json.

Original/current distinction: original v3.3 references remain in retained provenance, historical evidence and original review inputs. Current authority/navigation references now select v4. No mass replacement of historical text was performed.

Documentation/configuration evidence only. No target compile, Xemu, physical test, pilot acceptance, production data, measured budget, R0-F acceptance or phase-entry approval is claimed. Runtime remains candidate, not FINAL. Main/GitHub remain unchanged until separately authorized publication/integration.

Next action: inspect the local adoption diff; publication requires a separate instruction.

## Publication readiness recheck

The founder authorized commit, push and merge after consistency verification. Corrected inherited end-of-document version labels; explicitly labeled Main's v1.6 gate snapshot and rewrite obligations as historical. Updated current Main/Gameplay identities and the parent hash. The earlier local-only statements record the pre-publication validation checkpoint. Current live references resolve to Physics v4; retained v3.3 references are provenance, inherited-model attribution or amendment source text. Phase-1 entry remains gated pending the next review.
