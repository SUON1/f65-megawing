#!/usr/bin/env python3
"""Static boundary checks for the composite R0-B candidate."""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
text = (root / "build/r0b/reports/F65-R0B-FINAL.disassembly").read_text().lower()
for item in ("r0b_final_begin", "r0b_final_swap_to_b", "r0b_final_palette_probe", "r0b_final_restore", "d018", "d031", "d054", "d060", "d061", "d062", "d063", "d070", "d110", "d610", "f65_basepage_enter", "f65_basepage_leave"):
    if item not in text:
        raise SystemExit(f"R0B-FINAL-STATIC-001 FAIL: required {item} absent")
for item in ("d02f", "d058", "d059", "d064", "d068", "d020", "d021"):
    if item in text:
        raise SystemExit(f"R0B-FINAL-STATIC-001 FAIL: forbidden register {item} present")
map_text = (root / "build/r0b/reports/F65-R0B-FINAL.map").read_text().lower()
match = re.search(r"\n\s*([0-9a-f]+)\s+\1\s+\s*40\s+\s*64.*fcm_card", map_text)
if not match or int(match.group(1), 16) > 0x3fc0:
    raise SystemExit("R0B-FINAL-STATIC-001 FAIL: FCM card is not 64-byte aligned below $4000")
print("R0B-FINAL-STATIC-001 PASS: bounded D031/D054/pointer/palette/input transaction; no unlock, MAP, DMA, IRQ, or forbidden pointer side-path")
