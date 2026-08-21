#!/usr/bin/env python3
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
artifacts = root / "build/r0b/artifacts"
reports = root / "build/r0b/reports"
d81 = artifacts / "F65-R0B-PROOF.d81"
if d81.stat().st_size != 819200:
    raise SystemExit("R0B-BOOT-001 FAIL: D81 byte size")
if artifacts.joinpath("AUTOBOOT.C65").read_bytes()[:2] != b"\x01\x20":
    raise SystemExit("R0B-BOOT-001 FAIL: BASIC-65 load address")
listing = (reports / "F65-R0B-PROOF.d81-list.txt").read_text()
for filename in ("autoboot.c65", "f65-r0b-proof"):
    if filename not in listing:
        raise SystemExit(f"R0B-BOOT-001 FAIL: PETSCII D81 listing lacks {filename}")
print("R0B-BOOT-001 PASS: D81 contains PETSCII AUTOBOOT.C65 and proof PRG")
