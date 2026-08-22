#!/usr/bin/env python3
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
artifacts = root / "build/r0b/artifacts"
reports = root / "build/r0b/reports"
d81 = artifacts / "F65-R0B-D031-SAFE.d81"
if d81.stat().st_size != 819200:
    raise SystemExit("R0B-D031-BOOT-001 FAIL: D81 byte size")
if artifacts.joinpath("AUTOBOOT-D031.C65").read_bytes()[:2] != b"\x01\x20":
    raise SystemExit("R0B-D031-BOOT-001 FAIL: BASIC-65 load address")
listing = (reports / "F65-R0B-D031-SAFE.d81-list.txt").read_text()
for filename in ("autoboot.c65", "f65-r0a-proof"):
    if filename not in listing:
        raise SystemExit(f"R0B-D031-BOOT-001 FAIL: PETSCII D81 listing lacks {filename}")
known_good = b"\x01\x20\x17\x20\x0a\x00\x93\x20\x22F65-R0A-PROOF\x22\x00\x1d\x20\x14\x00\x8a\x00\x00\x00"
if artifacts.joinpath("AUTOBOOT-D031.C65").read_bytes() != known_good:
    raise SystemExit("R0B-D031-BOOT-001 FAIL: launcher differs from physical-R0-A-proven byte sequence")
print("R0B-D031-BOOT-001 PASS: byte-identical PETSCII AUTOBOOT and isolated D031 PRG alias")
