# R0-D Test Guide

Stage 1 runs host generation, deterministic fixture tests, static target checks,
and a target build with map, symbols, and disassembly. The required host IDs
are `R0D-FIX-001`, `R0D-TICK-001`, `R0D-CLK-001`, `R0D-WORLD-001`,
`R0D-RENDER-001`, `R0D-AUDIO-001`, `R0D-SNAP-001`, `R0D-IO-001`,
`R0D-AI-001`, `R0D-MEM-001`, and `R0D-TARGET-STATIC-001`.

No Xemu command may be run in Stage 1. No physical procedure is authorized.
No R0-D D81 is required for this stage; if later packaging creates one, it must
be fresh-formatted and pass the full repository D81 gate before mounting.
