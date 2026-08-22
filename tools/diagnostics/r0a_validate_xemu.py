#!/usr/bin/env python3
"""Validate the retained R0-A Xemu proof output."""
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
reports = root / "build" / "r0a" / "reports"
memory = (reports / "R0A-XEMU.memory.bin").read_bytes()
screen = (reports / "R0A-XEMU.screen.txt").read_text(errors="replace")
screen_text = screen.replace("{", "").replace("}", "")
result = memory[0x1800:0x180b]
expected = b"R0A1\x01\x01\x5a\x02\x01\x04\x57"
if result != expected:
    raise SystemExit(f"R0A-BP-001 FAIL: result block {result.hex()} != {expected.hex()}")
if "R0A-BP-001 PASS" not in screen_text or "R0A-PTR-001 PASS" not in screen_text:
    raise SystemExit("R0A-BP-001 FAIL: expected PASS markers absent from Xemu screen capture")
print("R0A-XEMU-001 PASS: D81 AUTOBOOT result block and screen capture verified")
