#!/usr/bin/env python3
"""Static/D81 guard for the separate, sacrificial R0-C device-9 media fixture."""
import hashlib
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

listing = root / "build/r0c/reports/F65-R0C-MEDIA.D81-list.txt"
if listing.exists():
    text = listing.read_text(errors="replace").lower()
    absent = [name for name in ("autoboot", "r0c-final", "r0c-media", "r0cproof") if name not in text]
    if absent:
        raise SystemExit("R0-C media D81 validation failed: absent=%s" % absent)

control_listing = root / "build/r0c/reports/F65-R0C-CONTROL.D81-list.txt"
if not control_listing.exists():
    raise SystemExit("R0-C media D81 validation failed: control listing absent")
control_text = control_listing.read_text(errors="replace").lower()
if any(name not in control_text for name in ("autoboot", "r0c-final", "r0cproof")) or "r0c-media" in control_text:
    raise SystemExit("R0-C media D81 validation failed: invalid control layout")
directory_lines = text.splitlines()
proof_line = next((n for n, line in enumerate(directory_lines) if '"r0cproof"' in line), -1)
media_line = next((n for n, line in enumerate(directory_lines) if '"r0c-media"' in line), -1)
if proof_line < 0 or media_line < 0 or proof_line > media_line:
    raise SystemExit("R0-C media D81 validation failed: media was not appended after control package")

candidate = root / "build/r0c/artifacts/F65-R0C-MEDIA.D81"
if not candidate.exists() or candidate.stat().st_size != 819200:
    raise SystemExit("R0-C media D81 validation failed: corrected carrier byte size")
candidate_bytes = candidate.read_bytes()
candidate_hash = hashlib.sha256(candidate_bytes).hexdigest()
if candidate_hash != "8826fc89706bcca0d9587f9bae80b5d12a8a1d35e3e0a92868c118e9ef204059":
    raise SystemExit("R0-C media D81 validation failed: corrected carrier hash/layout drift")

# Freezer compatibility regression guard. The historical control places
# AUTOBOOT, R0C-FINAL, and R0CPROOF consecutively at T39/S0, S1, and S9.
# The media program must be appended only at T39/S11; writing it before the
# package produced the physically rejected ROCFINAL.D81 carrier.
def sector(track, sector_number):
    start = ((track - 1) * 40 + sector_number) * 256
    return candidate_bytes[start:start + 256]

directory = sector(40, 3)
entries = []
for offset in range(2, 256, 32):
    entry = directory[offset:offset + 32]
    if entry[0] == 0:
        continue
    name = bytes(value & 0x7F for value in entry[3:19]).decode("ascii", "replace").rstrip("\xa0 ").lower()
    entries.append((name, entry[1], entry[2], entry[28] + 256 * entry[29]))
expected_entries = [
    ("autoboot.c65", 39, 0, 1),
    ("r0c-final", 39, 1, 8),
    ("r0cproof", 39, 9, 2),
    ("r0c-media", 39, 11, 22),
]
if entries != expected_entries:
    raise SystemExit("R0-C media D81 validation failed: physical-control layout=%s" % entries)
print("R0-C device-9 media fixture validation PASS")
