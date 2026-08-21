#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
reports = root / "build/r0b/reports"
memory = (reports / "R0B-XEMU.memory.bin").read_bytes()
screen = (reports / "R0B-XEMU.screen.txt").read_text(errors="replace").replace("{", "").replace("}", "")
result = memory[0x1800:0x180d]
if result[:6] != b"R0B1\x01\x01" or result[9] != 1 or result[11] != 1 or result[12] != 1:
    raise SystemExit(f"R0B-BLD-001 FAIL: result block {result.hex()}")
if "R0-B TEST RUN COMPLETE" not in screen or "R0B-BLD-001 PASS" not in screen or "R0B-FCM-REG-001 PASS" not in screen or "R0B-IN-001 FIXTURE PASS" not in screen or "R0B-AUD-003 MODEL PASS" not in screen:
    raise SystemExit("R0B-XEMU-001 FAIL: missing proof PASS markers")
print("R0B-XEMU-001 PASS: D81 booted the resident proof harness in Xemu")
