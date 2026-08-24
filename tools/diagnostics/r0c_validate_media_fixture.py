#!/usr/bin/env python3
"""Static/D81 guard for the separate, sacrificial R0-C device-9 media fixture."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1]).resolve()
boot = (root / "src/r0c/autoboot.bas").read_text().lower()
fixture = (root / "src/r0c/media_fixture.bas").read_text().lower()
required_boot = ['load "r0c-final",9,1']
required_fixture = [
    "d=9", "r0cg0", "r0cg1", "r0csel", "r0c-end", "for n=1 to 512", "write/verify",
    "safe to remove device 9 now", "fill consumes device 9", "r0c-corrupt",
]
missing = [item for item in required_boot if item not in boot]
missing += [item for item in required_fixture if item not in fixture]
if 'load "r0c-final"\n' in boot or ',8,' in fixture:
    raise SystemExit("R0-C media fixture validation failed: implicit/device-8 access")
if missing:
    raise SystemExit("R0-C media fixture validation failed: missing=%s" % missing)

listing = root / "build/r0c/reports/R0CFINAL.D81-list.txt"
if listing.exists():
    text = listing.read_text(errors="replace").lower()
    absent = [name for name in ("autoboot", "r0c-final", "r0c-media", "r0cproof") if name not in text]
    if absent:
        raise SystemExit("R0-C media D81 validation failed: absent=%s" % absent)
print("R0-C device-9 media fixture validation PASS")
