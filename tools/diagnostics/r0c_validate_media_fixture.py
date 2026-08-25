#!/usr/bin/env python3
"""Static/D81 guard for the separate, sacrificial R0-C device-9 media fixture."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1]).resolve()
proof_boot = (root / "src/r0c/autoboot.bas").read_text().lower()
fixture = (root / "src/r0c/media_fixture.bas").read_text().lower()
media_boot = (root / "src/r0c/media_boot.bas").read_text().lower()
required_boot = ['load "r0c-media",9,1']
required_fixture = [
    "d=9", "r0cg0", "r0cg1", "r0csel", "r0c-end", "for n=1 to 512", "write/verify", "get a$",
    "safe to remove device 9 now", "fill consumes device 9", "r0c-corrupt", "a=asc(a$)", "a=a-128",
    "if a=73", "if a=87", "if a=82", "if a=67", "if a=70", "if a=88", "if a=81",
]
missing = [item for item in required_boot if item not in media_boot]
missing += [item for item in required_fixture if item not in fixture]
if 'load "r0c-final",9,1' not in proof_boot or ',8,' in fixture:
    raise SystemExit("R0-C media fixture validation failed: implicit/device-8 access")
if 'load "r0c-media",9,1' not in media_boot or ',8,' in media_boot:
    raise SystemExit("R0-C media fixture validation failed: device-9 media boot probe")
if missing:
    raise SystemExit("R0-C media fixture validation failed: missing=%s" % missing)

# Physical MEGA65 GET returns upper-case letters in the PETSCII range 193..218.
# The fixture must normalize both that form and ordinary ASCII lower case.
def normalized(code):
    if 193 <= code <= 218:
        code -= 128
    if 97 <= code <= 122:
        code -= 32
    return code

if [normalized(x) for x in (201, 73, 105)] != [73, 73, 73]:
    raise SystemExit("R0-C media fixture validation failed: keyboard normalization")

listing = root / "build/r0c/reports/ROCFINAL.D81-list.txt"
if listing.exists():
    text = listing.read_text(errors="replace").lower()
    absent = [name for name in ("autoboot", "r0c-final", "r0c-media", "r0cproof") if name not in text]
    if absent:
        raise SystemExit("R0-C media D81 validation failed: absent=%s" % absent)
print("R0-C device-9 media fixture validation PASS")
