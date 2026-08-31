#!/usr/bin/env python3
"""Fail-closed host structural/content gate for the R0-D D81 carrier."""
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile

SECTOR_BYTES = 256
TRACKS = 80
SECTORS_PER_TRACK = 40
IMAGE_BYTES = TRACKS * SECTORS_PER_TRACK * SECTOR_BYTES
SYSTEM_SECTORS = {(40, sector) for sector in range(3)}


def fail(message):
    raise SystemExit("R0-D D81 loadability gate failed: " + message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def petscii_name(entry):
    return bytes(value & 0x7f for value in entry[3:19]).decode("ascii", "replace").rstrip("\xa0 ").lower()


root = pathlib.Path(sys.argv[1]).resolve()
candidate = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) == 3 else root / "build/r0d/artifacts/F65R0D2.D81"
artifacts = root / "build/r0d/artifacts"
reports = root / "build/r0d/reports"
manifests = root / "build/r0d/manifests"
c1541 = root / "toolchain/vice/VICE.app/Contents/Resources/bin/c1541"

if not candidate.is_file():
    fail("candidate is absent")
if candidate.stat().st_size != IMAGE_BYTES:
    fail("exact size is %d, expected %d" % (candidate.stat().st_size, IMAGE_BYTES))
if not c1541.is_file():
    fail("pinned c1541 is absent")

lock = json.loads((root / "toolchain/f65_toolchain.lock.json").read_text())
expected_c1541_sha = lock["vice"]["c1541_sha256"]
actual_c1541_sha = sha256(c1541)
if actual_c1541_sha != expected_c1541_sha:
    fail("pinned c1541 hash mismatch")

data = candidate.read_bytes()


def sector(track, number):
    if not (1 <= track <= TRACKS and 0 <= number < SECTORS_PER_TRACK):
        fail("out-of-range T/S %d/%d" % (track, number))
    offset = ((track - 1) * SECTORS_PER_TRACK + number) * SECTOR_BYTES
    return data[offset:offset + SECTOR_BYTES]


def checked_link(track, number, purpose):
    if track == 0:
        return None
    if not (1 <= track <= TRACKS and 0 <= number < SECTORS_PER_TRACK):
        fail("invalid %s link %d/%d" % (purpose, track, number))
    return (track, number)


header = sector(40, 0)
if header[:2] != bytes((40, 3)):
    fail("header does not identify directory 40/3")
if sector(40, 1)[:2] != bytes((40, 2)) or sector(40, 2)[0] != 0:
    fail("BAM chain is not the expected closed 40/1 -> 40/2 layout")
disk_label = bytes(value & 0x7f for value in header[4:20]).decode("ascii", "replace").rstrip("\xa0 ")
disk_id = bytes(value & 0x7f for value in header[22:24]).decode("ascii", "replace").rstrip("\xa0 ")
if disk_label != "F65 R0-D" or disk_id != "65":
    fail("disk header profile mismatch label=%r id=%r" % (disk_label, disk_id))

# A 1581 D81 records one free-block count followed by five 8-bit maps for each
# 40-sector track. Tracks 1-40 are in 40/1 and tracks 41-80 are in 40/2.
free = set()
for track in range(1, TRACKS + 1):
    bam = sector(40, 1 if track <= 40 else 2)
    offset = 0x10 + ((track - 1) % 40) * 6
    declared = bam[offset]
    bitmap = bam[offset + 1:offset + 6]
    available = set()
    for number in range(SECTORS_PER_TRACK):
        if bitmap[number // 8] & (1 << (number % 8)):
            available.add((track, number))
    if declared != len(available):
        fail("BAM free count mismatch for track %d: %d != %d" % (track, declared, len(available)))
    free.update(available)

directory_sectors = set()
entries = []
cursor = (40, 3)
while cursor is not None:
    if cursor in directory_sectors:
        fail("directory chain loops at %d/%d" % cursor)
    directory_sectors.add(cursor)
    block = sector(*cursor)
    cursor = checked_link(block[0], block[1], "directory")
    for offset in range(2, SECTOR_BYTES, 32):
        entry = block[offset:offset + 32]
        if entry[0] == 0:
            continue
        if entry[0] != 0x82:
            fail("directory entry has non-closed-PRG type $%02X" % entry[0])
        start = checked_link(entry[1], entry[2], "file")
        if start is None:
            fail("file has no start sector")
        entries.append({"petscii": petscii_name(entry), "start": start,
                        "blocks": entry[28] | (entry[29] << 8)})

expected = [
    ("autoboot.c65", artifacts / "AUTOBOOT.C65"),
    ("r0d-calib", artifacts / "F65-R0D-CALIBRATION.prg"),
]
if [entry["petscii"] for entry in entries] != [name for name, _ in expected]:
    fail("unexpected directory order/names: %r" % [entry["petscii"] for entry in entries])

file_sectors = set()
payloads = {}
for entry in entries:
    payload = bytearray()
    cursor = entry["start"]
    chain_count = 0
    while cursor is not None:
        if cursor in file_sectors or cursor in directory_sectors or cursor in SYSTEM_SECTORS:
            fail("cross-link or reserved-sector ownership at %d/%d" % cursor)
        file_sectors.add(cursor)
        chain_count += 1
        if chain_count > TRACKS * SECTORS_PER_TRACK:
            fail("file chain does not terminate")
        block = sector(*cursor)
        next_track, next_sector = block[0], block[1]
        if next_track == 0:
            if not 2 <= next_sector <= 255:
                fail("invalid terminal byte count for " + entry["petscii"])
            payload.extend(block[2:next_sector + 1])
            cursor = None
        else:
            cursor = checked_link(next_track, next_sector, "file")
            payload.extend(block[2:])
    if chain_count != entry["blocks"]:
        fail("directory block count mismatch for " + entry["petscii"])
    payloads[entry["petscii"]] = bytes(payload)

owned = SYSTEM_SECTORS | directory_sectors | file_sectors
if SYSTEM_SECTORS & file_sectors or directory_sectors & file_sectors:
    fail("filesystem ownership sets overlap")
allocated = {(track, number) for track in range(1, TRACKS + 1)
             for number in range(SECTORS_PER_TRACK) if (track, number) not in free}
if allocated != owned:
    missing = sorted(allocated - owned)[:4]
    extra = sorted(owned - allocated)[:4]
    fail("BAM/ownership mismatch missing=%r extra=%r" % (missing, extra))

listing = subprocess.run([str(c1541), str(candidate), "-list"], capture_output=True, text=True)
if listing.returncode != 0:
    fail("pinned c1541 listing returned %d" % listing.returncode)
for petscii, source in expected:
    if not source.is_file():
        fail("source payload absent: " + str(source))
    if payloads[petscii] != source.read_bytes():
        fail("raw chain payload mismatch for " + petscii)
    with tempfile.TemporaryDirectory(prefix="r0d-d81-") as temporary:
        extracted = pathlib.Path(temporary) / petscii
        readback = subprocess.run([str(c1541), str(candidate), "-read", petscii, str(extracted)],
                                  capture_output=True, text=True)
        if readback.returncode != 0 or not extracted.is_file():
            fail("c1541 extraction failed for " + petscii)
        if extracted.read_bytes() != source.read_bytes():
            fail("c1541 extraction/hash mismatch for " + petscii)

branch = subprocess.run(["git", "branch", "--show-current"], cwd=root, capture_output=True,
                        check=True, text=True).stdout.strip()
commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True,
                        check=True, text=True).stdout.strip()
candidate_sha = sha256(candidate)
release = {
    "D81_STATE": "HOST_CONTENT_VERIFIED",
    "D81_FILENAME": candidate.name,
    "D81_SHA256": candidate_sha,
    "D81_BYTES": IMAGE_BYTES,
    "DISK_LABEL": disk_label,
    "DISK_ID": disk_id,
    "ENTRY_FILENAME": "AUTOBOOT.C65 -> R0D-CALIB",
    "SOURCE_BRANCH": branch,
    "SOURCE_COMMIT": commit,
    "BUILDER_IDENTITY": {"path": str(c1541), "sha256": actual_c1541_sha, "version": lock["vice"]["version"]},
    "STRUCTURAL_VALIDATOR_IDENTITY": "tools/diagnostics/r0d_d81_loadability_gate.py",
    "HOST_STRUCTURAL_RESULT": "PASS",
    "HOST_CONTENT_RESULT": "PASS",
    "XEMU_RESULT": "AWAITING REBUILD/PUBLICATION",
    "XEMU_EVIDENCE": None,
    "SD_COPY_SHA256": None,
    "PHYSICAL_CHOOSER_RESULT": "AWAITING HUMAN",
    "PHYSICAL_EVIDENCE": None,
    "payloads": [{"hostFilename": source.name, "petsciiFilename": petscii,
                  "bytes": source.stat().st_size, "sha256": sha256(source)}
                 for petscii, source in expected],
    "construction": "fresh-format and both payload writes in one pinned c1541 invocation",
    "c1541Listing": listing.stdout,
}
manifests.mkdir(parents=True, exist_ok=True)
reports.mkdir(parents=True, exist_ok=True)
(manifests / "r0d-d81-release.json").write_text(json.dumps(release, indent=2, sort_keys=True) + "\n")
(reports / "R0D-D81-LOADABILITY.md").write_text(
    "# R0-D D81 Loadability\n\n"
    "D81 state: `HOST_CONTENT_VERIFIED`\n\n"
    "- Candidate: `%s`\n- SHA-256: `%s`\n- Bytes: `819200`\n"
    "- Disk: `F65 R0-D`, ID `65`\n- Entry: `AUTOBOOT.C65 -> R0D-CALIB`\n"
    "- Construction: fresh format and both payloads in one pinned `c1541` invocation.\n"
    "- Host structural verification: `PASS`\n- Host content extraction/hash verification: `PASS`\n"
    "- Xemu: `AWAITING REBUILD/PUBLICATION`\n- Physical chooser: `AWAITING HUMAN`\n" % (candidate.name, candidate_sha)
)
print("R0-D D81 STRUCTURAL+CONTENT PASS sha256=" + candidate_sha)
