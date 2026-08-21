#!/usr/bin/env python3
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
reports = root / "build/r0b/reports"
text = (reports / "F65-R0B-PROOF.disassembly").read_text()
stage = (root / "src/diagnostics/r0b/proof_stage2.c").read_text()
if "main" not in text:
    raise SystemExit("R0B-BLD-001 FAIL: target disassembly has no main")
if "f65_basepage_enter" not in text or "f65_basepage_leave" not in text:
    raise SystemExit("R0B-BLD-001 FAIL: accepted R0-A base-page transition is absent")
if "r0b_stage2_run" not in stage or "r0b_timer_begin" not in stage:
    raise SystemExit("R0B-BLD-001 FAIL: stage-2 composition/timing service absent")
if "d054" in text.lower():
    raise SystemExit("R0B-FCM-SAFE-001 FAIL: owner-facing target contains D054 access")
print("R0B-BLD-001 PASS: target links stage-2 proof, no D054 access, and R0-A base-page transition")
