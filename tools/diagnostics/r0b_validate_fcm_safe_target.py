#!/usr/bin/env python3
"""Static admission checks for the separate, deliberately narrow FCM restore disk."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
reports = root / "build/r0b/reports"
text = (reports / "F65-R0B-FCM-SAFE.disassembly").read_text().lower()
if "r0b_fcm_restore_probe" not in text:
    raise SystemExit("R0B-FCM-SAFE-002 FAIL: restore wrapper missing from target")
if "d02f" in text:
    raise SystemExit("R0B-FCM-SAFE-002 FAIL: unsafe VIC key-register access present")
if "d054" not in text or "d018" not in text:
    raise SystemExit("R0B-FCM-SAFE-002 FAIL: expected context/control registers missing")
if "d031" in text or "d060" in text or "d058" in text:
    raise SystemExit("R0B-FCM-SAFE-002 FAIL: isolated probe touched unrelated VIC display controls")
if "f65_basepage_enter" not in text or "f65_basepage_leave" not in text:
    raise SystemExit("R0B-FCM-SAFE-002 FAIL: accepted R0-A base-page transition absent")
print("R0B-FCM-SAFE-002 PASS: isolated D054 restore target; no D02F, pointer, raster, DMA, or MAP path")
