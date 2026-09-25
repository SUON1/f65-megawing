#!/bin/sh
# MANDATORY D81 LOADABILITY GATE
#
# Before creating, modifying, copying, renaming, packaging, mounting, testing,
# or releasing any D81, read and obey 00_D81_LOADABILITY_GATE.md.
# This wrapper validates the immutable T06 host/Xemu record before delegating
# the raw FAT32, contiguous-allocation, exact-hash and safe-eject gates.
set -eu

# Retired after the owner's 2026-09-22 chooser failure. In particular, an
# existing filename is not evidence of an empty, owner-created native slot.
# Stop before preflight, media access, or automatic slot-fill selection.
echo 'R0FDIAG2.D81 is retired after physical chooser failure; no transfer or slot fill permitted.' >&2
exit 2

root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
cd "$root"

mount=/Volumes/MEGA65FDISK
image="$root/build/r0f/successor-t06-diagnostic/canonical/R0FDIAG2.D81"
record="$root/docs/evidence/r0f/successor/2026-09-21-recovery/R0FDIAG2/release.json"
hash=912df16828f1c60127e4fcdd8d545dfca0c2ad8fe6a24a64ae01b4ac280df17d

case ${1-} in
  '') ;;
  --host-preflight) ;;
  *) echo 'usage: sudo tools/diagnostics/r0f_t06_sd.sh' >&2; exit 2 ;;
esac

/usr/bin/python3 -B - "$root" "$image" "$record" "$hash" <<'PY'
import hashlib
import json
from pathlib import Path
import sys

root, image, record = map(Path, sys.argv[1:4])
expected_hash = sys.argv[4]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = json.loads(record.read_text())
if (manifest['D81_STATE'] != 'XEMU_BOOT_VERIFIED'
        or manifest['D81_FILENAME'] != 'R0FDIAG2.D81'
        or manifest['D81_SHA256'] != expected_hash
        or manifest['D81_BYTES'] != 819200
        or manifest['HOST_STRUCTURAL_RESULT'] != 'PASS'
        or manifest['HOST_CONTENT_RESULT'] != 'PASS'
        or manifest['XEMU_RESULT'] != 'PASS'
        or image.name != manifest['D81_FILENAME']
        or image.stat().st_size != manifest['D81_BYTES']
        or digest(image) != expected_hash):
    raise SystemExit('T06 candidate identity or host/Xemu gate mismatch')
runs = manifest['XEMU_EVIDENCE']
if [run['run'] for run in runs] != ['ntsc-1', 'ntsc-2', 'pal-1', 'pal-2']:
    raise SystemExit('T06 exact-carrier repetitions are incomplete')
for run in runs:
    if (run['mountedD81Filename'] != image.name
            or run['preRunD81Sha256'] != expected_hash):
        raise SystemExit('T06 exact-name/hash Xemu evidence mismatch')
tool_hashes = {
    'd81_delivery.py': '1c3bf862cbbf5a826b7cf1d666b4239f9a7a086a69ad405201f0921f4e10b055',
    'd81_sd_transfer.sh': '3e116c94b433ffb2c554fc1a14ecf066ca7c1d70600469c54fdf0d5659a46339',
    'd81_sd_fill_mega65_slot.sh': 'b2880d97bd9681a8b60a45c5fde35bbddd96497beb1b5f64afdf91aa2d82187e',
    'd81_sd_contiguity.py': '7c97d0fd58535c26b05872a4a10010f86b2a966d3b7158b9b6e22213759f2e5e',
    'd81_fat32_audit.py': 'd0325c6fa6284ede5e3a7ae7fe38a01a7ae5bea5b49c0f21a27fed20e0ca922a',
}
for name, expected in tool_hashes.items():
    path = root / 'tools/diagnostics' / name
    if digest(path) != expected:
        raise SystemExit('delivery tooling changed; rebuild/revalidate: ' + name)
PY

if test "${1-}" = --host-preflight; then
  echo 'T06 immutable host/Xemu identity preflight PASS'
  exit 0
fi

test "$(id -u)" -eq 0 || {
  echo 'Run with sudo; raw FAT32 inspection is mandatory.' >&2
  exit 2
}
test -d "$mount" || { echo 'MEGA65 card is not mounted.' >&2; exit 2; }

target="$mount/$(basename -- "$image")"
if test -e "$target"; then
  echo 'Matching root entry found; validating and filling it only as a MEGA65-created native slot.'
  tools/diagnostics/d81_sd_fill_mega65_slot.sh "$image" "$mount" "$hash"
else
  tools/diagnostics/d81_sd_transfer.sh "$image" "$mount" "$hash"
fi
