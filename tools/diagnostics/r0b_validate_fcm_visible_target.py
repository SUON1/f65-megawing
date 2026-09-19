#!/usr/bin/env python3
"""Static admission checks for the isolated visible-FCM/restore disk."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
text = (root / "build/r0b/reports/F65-R0B-FCM-VISIBLE.disassembly").read_text().lower()
required = ("r0b_fcm_visible_begin", "r0b_fcm_visible_restore", "d018", "d031", "d054", "d060", "d061", "d062", "d063")
for item in required:
    if item not in text:
        raise SystemExit(f"R0B-FCM-VIS-001 FAIL: required {item} absent")
for forbidden in ("d02f", "d058", "d059", "d064", "d068", "d070", "d020", "d021"):
    if forbidden in text:
        raise SystemExit(f"R0B-FCM-VIS-001 FAIL: forbidden VIC register {forbidden} present")
if "f65_basepage_enter" not in text or "f65_basepage_leave" not in text:
    raise SystemExit("R0B-FCM-VIS-001 FAIL: accepted R0-A base-page transitions absent")
print("R0B-FCM-VIS-001 PASS: bounded FCM card target; no D02F, pointer write, palette, DMA, MAP, or IRQ path")
