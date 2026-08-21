#!/usr/bin/env python3
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
artifacts = root / "build/r0b/artifacts"
reports = root / "build/r0b/reports"
d81 = artifacts / "F65-R0B-FCM-VISIBLE.d81"
if d81.stat().st_size != 819200:
    raise SystemExit("R0B-FCM-VIS-BOOT-001 FAIL: D81 byte size")
launcher = artifacts.joinpath("AUTOBOOT-FCM-VISIBLE.C65").read_bytes()
known_good = b"\x01\x20\x17\x20\x0a\x00\x93\x20\x22F65-R0A-PROOF\x22\x00\x1d\x20\x14\x00\x8a\x00\x00\x00"
if launcher != known_good:
    raise SystemExit("R0B-FCM-VIS-BOOT-001 FAIL: launcher differs from R0-A-proven bytes")
listing = (reports / "F65-R0B-FCM-VISIBLE.d81-list.txt").read_text()
for filename in ("autoboot.c65", "f65-r0a-proof"):
    if filename not in listing:
        raise SystemExit(f"R0B-FCM-VIS-BOOT-001 FAIL: PETSCII D81 listing lacks {filename}")
print("R0B-FCM-VIS-BOOT-001 PASS: byte-identical R0-A-proven boot launcher and payload alias")
