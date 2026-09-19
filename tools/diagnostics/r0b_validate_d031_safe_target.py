#!/usr/bin/env python3
"""Static admission checks for the D031-only transition/restore disk."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
text = (root / "build/r0b/reports/F65-R0B-D031-SAFE.disassembly").read_text().lower()
if "r0b_d031_restore_probe" not in text:
    raise SystemExit("R0B-D031-SAFE-001 FAIL: D031 restore wrapper missing")
if "d018" not in text or "d031" not in text:
    raise SystemExit("R0B-D031-SAFE-001 FAIL: expected context/D031 registers missing")
forbidden = ("d02f", "d054", "d058", "d059", "d060", "d061", "d062", "d063", "d064", "d068", "d070", "d020", "d021")
if any(register in text for register in forbidden):
    raise SystemExit("R0B-D031-SAFE-001 FAIL: isolated D031 target touched forbidden VIC controls")
if "f65_basepage_enter" not in text or "f65_basepage_leave" not in text:
    raise SystemExit("R0B-D031-SAFE-001 FAIL: accepted R0-A base-page transition absent")
print("R0B-D031-SAFE-001 PASS: isolated D031 save/clear-H640/readback/exact-restore target")
