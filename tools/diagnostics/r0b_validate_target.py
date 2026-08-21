#!/usr/bin/env python3
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
reports = root / "build/r0b/reports"
text = (reports / "F65-R0B-PROOF.disassembly").read_text()
if "main" not in text:
    raise SystemExit("R0B-BLD-001 FAIL: target disassembly has no main")
if "f65_basepage_enter" not in text or "f65_basepage_leave" not in text:
    raise SystemExit("R0B-BLD-001 FAIL: accepted R0-A base-page transition is absent")
print("R0B-BLD-001 PASS: target links proof contract and R0-A base-page transition")
