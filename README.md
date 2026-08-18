# F-65 Megawing

F-65 Megawing is a cockpit-primary combat-flight simulator for the MEGA65. Production target code is planned in 45GS02 assembly; Java is reserved for host tooling, generators, and reference models.

The project is currently at repository bootstrap and bounded pre-R0/R0-A foundation work. This repository does not authorize gameplay, flight, radar, weapons, tactical AI, campaign, audio, or production-renderer implementation.

Start with [F65_OFFICIAL_RECORD.md](F65_OFFICIAL_RECORD.md). It records the current specification authority, open issues, authorized milestone, and hard gates. Exact source documents and their manifest are under [`spec/`](spec/), with corpus metadata in [`spec/manifests/spec-corpus.json`](spec/manifests/spec-corpus.json).

## Repository layout

- `spec/`: preserved architecture, gameplay, engine, and alignment documents.
- `docs/`: decisions, plans, evidence, and reports.
- `interfaces/` and `memory/`: future machine-readable contracts and ledgers.
- `src/`: reserved assembly module ownership; currently contains no implementation.
- `tools/`: reserved host schemas, generators, build tools, and diagnostics.
- `tests/`: host, target, fixture, and retained-evidence areas.
- `assets/`, `missions/`, `toolchain/`, `build/`, and `dist/`: controlled project support areas.

Repository-wide instructions for coding agents are in [AGENTS.md](AGENTS.md).
