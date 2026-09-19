#!/usr/bin/env python3
"""Static R0-D target guard: diagnostic-only workload and protected-range safety."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
text = (root / "src/diagnostics/r0d/composite.c").read_text()
required = ["R0D_RESULT_ADDRESS", "R0D_RESULT_BYTES", "R0D_STAGE_COUNT", "R0D_HISTORICAL_PROTECTED_CLOCKS", "R0D-FIX-001", "R0D-TICK-001", "R0D-CLK-001", "R0D-WORLD-001", "R0D-RENDER-001", "R0D-AUDIO-001", "R0D-SNAP-001", "R0D-IO-001", "R0D-AI-001", "R0D-MEM-001", "stage == 16u"]
forbidden = ["0x050", "0x053", "0x056", "0x057", "0x058", "fopen", "malloc", "D81", "r0a_dma("]
missing = [value for value in required if value not in text]
bad = [value for value in forbidden if value in text]
if missing or bad:
    raise SystemExit("R0-D target validation failed: missing=%s forbidden=%s" % (missing, bad))
print("R0-D static target validation PASS")
