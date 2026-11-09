# Work in Progress

- **Status** BLOCKED at the M2 throughput estimate gate.
- **Task** M2 Throughput Architecture Correction. Successor branch `codex/65aero-m2-throughput-architecture` starts at `a46279c15b2e7604a93e7ad8a78cabf58e1f576d`.
- **Authority** The 9 November founder direction approves a private development display representation, exact numerical throughput work subject to the estimate gate, and a separate restricted boot trace.
- **Renderer** Within-store tile reuse fits the existing allocations and reconstructs the sealed default image exactly in the host model. The cold and moving-camera exact arithmetic path has no credible complete 20 Hz budget. The estimate gate stopped implementation before a renderer relink.
- **Boot diagnostic** `65AERO-M2-BOOT-TRACE-1` passed restricted PAL and NTSC Xemu traces through CF001 and the reset-only terminal. It has no reachable runtime clock, display construction or ticks. Full renderer Xemu was not run.
- **Handoff** [Measured blockers and sealed boot traces](docs/reports/M2_THROUGHPUT_ARCHITECTURE_CORRECTION.md). The next decision is the bounded exact arithmetic backend and its Platform ownership.
