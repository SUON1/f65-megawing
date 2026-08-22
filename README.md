# F-65 Megawing

F-65 Megawing is a cockpit-primary combat-flight simulator for the MEGA65. The production target implementation model is C-primary with LLVM-MOS for the MEGA65/45GS02 target; narrowly admitted handwritten 45GS02 remains available for platform-critical or measured work. Java is the independent host-tool, generator, and oracle language.

The project is currently at repository bootstrap and bounded pre-R0/R0-A foundation work. This repository does not authorize gameplay, flight, radar, weapons, tactical AI, campaign, audio, or production-renderer implementation.

Start with the approved [Read-First supplement](spec/alignment/F-65_Technical_Alignment_and_Read_First_Supplement_v1.0.md), then [F65_OFFICIAL_RECORD.md](F65_OFFICIAL_RECORD.md). The approved [AD-001](docs/decisions/F-65_Architecture_Decision_AD-001_R0_Program_Development_Authorization.md) authorizes bounded R0-A–F proof development, but no R0 gate has passed and candidate Architecture 1.5.1, Gameplay 0.2, and Engine 0.2 are not thereby approved or frozen. Exact source documents and their manifest are under [`spec/`](spec/), with corpus metadata in [`spec/manifests/spec-corpus.json`](spec/manifests/spec-corpus.json).

## Repository layout

- `spec/`: preserved baseline, approved Read-First control, and candidate architecture/gameplay/engine documents.
- `docs/`: decisions, plans, evidence, and reports.
- `interfaces/` and `memory/`: future machine-readable contracts and ledgers.
- `src/`: reserved C-primary target and narrow platform-wrapper ownership; currently contains no implementation.
- `tools/`: reserved host schemas, generators, build tools, and diagnostics.
- `tests/`: host, target, fixture, and retained-evidence areas.
- `assets/`, `missions/`, `toolchain/`, `build/`, and `dist/`: controlled project support areas.

Repository-wide instructions for coding agents are in [AGENTS.md](AGENTS.md).
