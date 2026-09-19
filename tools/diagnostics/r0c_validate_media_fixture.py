#!/usr/bin/env python3
"""Validate the R0-C fixture and its freshly-built, loadable D81 carrier."""
import hashlib
import pathlib
import subprocess
import sys
import tempfile

SECTOR = 256
TRACKS = 80
SECTORS = 40
IMAGE_BYTES = TRACKS * SECTORS * SECTOR

def die(message):
    raise SystemExit("R0-C media fixture validation failed: " + message)

root = pathlib.Path(sys.argv[1]).resolve()
proof_boot = (root / "src/r0c/autoboot.bas").read_text().lower()
fixture = (root / "src/r0c/media_fixture.bas").read_text().lower()
media_boot = (root / "src/r0c/media_boot.bas").read_text().lower()
if 'load "r0c-final",8,1' not in proof_boot:
    die("proof carrier does not boot from device 8")
if 'load "r0c-media",8,1' not in media_boot or ',9,' in media_boot:
    die("media harness must load from device 8")
required = ("d=9", "r0csel", "r0cg0", "r0cg1", "r0c-end", "for n=1 to 512",
            "write/verify", "get a$", "safe to remove device 9 now", "fill consumes device 9",
            "r0c-corrupt", "a=asc(a$)", "a=a-128", "if a=73", "if a=87", "if a=82",
            "if a=67", "if a=70", "if a=88", "if a=81", "trap 9000", "blank media is valid",
            "initialize writes only", '5120 open 2,d,2,"r0csel,s,r"',
            '5130 input#2,m$,aa,bb,c$', '5140 close 2', "for n=1 to 512:input#2,x$,xn", "goto 40")
missing = [item for item in required if item not in fixture]
if missing:
    die("fixture missing=" + repr(missing))
for forbidden in ("trap 0", "sg=", "gg=", "s0:r0cg0", "s0:r0cg1", "s0:r0csel", 'r0csel,s,r":input'):
    if forbidden in fixture:
        die("obsolete unsafe form=" + forbidden)

def normalized(code):
    if 193 <= code <= 218:
        code -= 128
    if 97 <= code <= 122:
        code -= 32
    return code
if [normalized(x) for x in (201, 73, 105)] != [73, 73, 73]:
    die("keyboard normalization")

candidate = root / "build/r0c/artifacts/F65-R0C-MEDIA.D81"
if not candidate.exists() or candidate.stat().st_size != IMAGE_BYTES:
    die("carrier is not exactly 819200 bytes")
data = candidate.read_bytes()

def sector(track, number):
    if not (1 <= track <= TRACKS and 0 <= number < SECTORS):
        die("out-of-range T/S %d/%d" % (track, number))
    start = ((track - 1) * SECTORS + number) * SECTOR
    return data[start:start + SECTOR]

directory = sector(40, 3)
if directory[0] != 0:
    die("unexpected directory link")
entries = []
for offset in range(2, SECTOR, 32):
    entry = directory[offset:offset + 32]
    if entry[0] == 0:
        continue
    if entry[0] != 0x82:
        die("directory entry is not a closed PRG/SEQ file")
    raw = bytes(value & 0x7f for value in entry[3:19])
    name = raw.decode("ascii", "replace").rstrip("\xa0 ").lower()
    entries.append((name, entry[0], entry[1], entry[2]))
if [name for name, *_ in entries] != ["autoboot.c65", "r0c-final", "r0cproof", "r0c-media"]:
    die("unexpected directory order=%r" % entries)

used = set()
def walk(name, track, number):
    result = bytearray()
    while track:
        key = (track, number)
        if key in used:
            die("cross-linked or looping chain at %s T/S %s" % (name, key))
        used.add(key)
        block = sector(track, number)
        next_track, next_sector = block[0], block[1]
        if next_track == 0:
            count = next_sector
            if count < 2 or count > 255:
                die("invalid terminal byte count for %s" % name)
            result.extend(block[2:1 + count])
        else:
            if not (0 <= next_sector < SECTORS):
                die("invalid chain link for %s" % name)
            result.extend(block[2:])
        track, number = next_track, next_sector
    return bytes(result)

payloads = {name: walk(name, track, number) for name, _, track, number in entries}

c1541 = root / "toolchain/vice/VICE.app/Contents/Resources/bin/c1541"
if not c1541.exists():
    die("pinned c1541 is unavailable")
listing = subprocess.run([str(c1541), str(candidate), "-list"], check=True,
                         capture_output=True, text=True).stdout.lower()
for name in ("autoboot", "r0c-final", "r0cproof", "r0c-media"):
    if name not in listing:
        die("c1541 listing missing " + name)
expected = {"autoboot.c65": root / "build/r0c/artifacts/AUTOBOOT.C65",
            "r0c-final": root / "build/r0c/artifacts/F65-R0C-PROOF.prg",
            "r0cproof": root / "build/r0c/R0CPROOF.PKG",
            "r0c-media": root / "build/r0c/artifacts/R0C-MEDIA.C65"}
with tempfile.TemporaryDirectory(prefix="r0c-d81-") as tmp:
    for name, source in expected.items():
        extracted = pathlib.Path(tmp) / name
        subprocess.run([str(c1541), str(candidate), "-read", name, str(extracted)], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if not extracted.exists() or extracted.read_bytes() != source.read_bytes():
            die("extracted bytes differ for " + name)
        if payloads[name] != source.read_bytes():
            die("raw chain bytes differ for " + name)

report = root / "build/r0c/reports/R0C-MEDIA-D81-LOADABILITY.md"
report.parent.mkdir(parents=True, exist_ok=True)
digest = hashlib.sha256(data).hexdigest()
report.write_text("# R0-C D81 Loadability\n\n"
                  "State: `HOST_CONTENT_VERIFIED`\n\n"
                  "Carrier: `F65-R0C-MEDIA.D81`\n"
                  "Exact bytes: `819200`\n"
                  "SHA-256: `" + digest + "`\n"
                  "Construction: fresh format and all four files in one c1541 invocation.\n"
                  "Boot: selected carrier at device 8; fixture operations at device 9.\n")
print("R0-C fresh D81 structural/content validation PASS sha256=" + digest)
