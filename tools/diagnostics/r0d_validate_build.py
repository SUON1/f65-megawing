#!/usr/bin/env python3
"""Extract R0-D code/data/stack accounting from the linked map without selecting limits."""
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
map_path = root / "build/r0d/reports/F65-R0D-CALIBRATION.map"
text = map_path.read_text()

def section(name):
    match = re.search(r"^\s*[0-9a-f]+\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+" + re.escape(name) + r"$", text, re.MULTILINE)
    if not match:
        raise SystemExit("R0-D build accounting failed: missing " + name)
    return int(match.group(1), 16)

stack = re.search(r"__stack = 0x([0-9a-f]+)", text)
if not stack:
    raise SystemExit("R0-D build accounting failed: stack symbol missing")
report = {"identity":"r0d-0.1.0-calibration-proof", "codeBytes":section(".text"), "rodataBytes":section(".rodata"), "dataBytes":section(".data"), "bssBytes":section(".bss"), "linkedStackAddress":"0x" + stack.group(1), "reserveBytes":0, "resultBlock":"0x1860-0x18df", "result":"PASS", "note":"Observed build accounting only; no measured limit selected."}
(root / "build/r0d/reports/r0d-build-accounting.json").write_text(json.dumps(report, indent=2) + "\n")
print("R0-D build accounting PASS")
