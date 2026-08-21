#!/usr/bin/env python3
"""Validate the reproducible D81 container, not its emulator/hardware execution."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
artifacts = root / "build" / "r0a" / "artifacts"
reports = root / "build" / "r0a" / "reports"
d81 = artifacts / "F65-R0A-PROOF.d81"
autoboot = artifacts / "AUTOBOOT.C65"
listing = (reports / "F65-R0A-PROOF.d81-list.txt").read_text()
autoboot_listing = (reports / "AUTOBOOT.C65.listing").read_text()

if d81.stat().st_size != 819200:
    raise SystemExit(f"R0A-D81-001 FAIL: D81 byte size is {d81.stat().st_size}, expected 819200")
if autoboot.read_bytes()[:2] != b"\x01\x20":
    raise SystemExit("R0A-D81-001 FAIL: AUTOBOOT.C65 does not have the C65 BASIC load address $2001")
if '10 load "F65-R0A-PROOF"' not in autoboot_listing or '20 run' not in autoboot_listing:
    raise SystemExit("R0A-D81-001 FAIL: AUTOBOOT.C65 does not round-trip as the approved BASIC-65 launcher")
for filename in ("AUTOBOOT.C65", "F65-R0A-PROOF"):
    if filename not in listing:
        raise SystemExit(f"R0A-D81-001 FAIL: D81 listing lacks {filename}")
print("R0A-D81-001 PASS: 80-track D81 contains BASIC-65 AUTOBOOT.C65 and proof PRG")
