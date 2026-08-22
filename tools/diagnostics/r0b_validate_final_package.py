#!/usr/bin/env python3
"""Package checks for the final composite R0-B candidate."""
from pathlib import Path
import sys

root = Path(sys.argv[1])
listing = (root / "build/r0b/reports/AUTOBOOT-FINAL.C65.listing").read_text().upper()
directory = (root / "build/r0b/reports/R0BFINAL.D81-list.txt").read_text().upper()
if 'LOAD "F65-R0B-FINAL"' not in listing:
    raise SystemExit("R0B-FINAL-PACKAGE-001 FAIL: AUTOBOOT does not load final binary")
if 'F65-R0B-FINAL' not in directory or 'AUTOBOOT' not in directory:
    raise SystemExit("R0B-FINAL-PACKAGE-001 FAIL: D81 missing final program or AUTOBOOT")
print("R0B-FINAL-PACKAGE-001 PASS: PETSCII AUTOBOOT and final PRG are packaged")
