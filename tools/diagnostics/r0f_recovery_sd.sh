#!/bin/sh
# One local authentication for forensic audit and both approved delivery paths.
# Read 00_D81_LOADABILITY_GATE.md first. Never touches the retired failed file.
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
cd "$root"
test "$(id -u)" -eq 0 || { echo 'Run with sudo for the read-only raw FAT audit.' >&2; exit 2; }
mount=/Volumes/MEGA65FDISK
out="$root/build/r0f/successor-t05-recovery"
hash=3721dff9b84cfb7842cc154f6885861e0c7cbd3c3408c8ecec190bf6b405d461
test -d "$mount" || { echo 'MEGA65 card is not mounted.' >&2; exit 2; }
# Manifest and evidence validation happens before any media write. It also
# records the currently resolved volume/device so a remount cannot switch cards.
/usr/bin/python3 -B - "$root" "$mount" <<'PY'
import hashlib
import json
from pathlib import Path
import sys
root, mount = map(Path, sys.argv[1:])
sys.path.insert(0, str(root / 'tools/diagnostics'))
from d81_sd_contiguity import disk_info
info = disk_info(mount)
if not info.get('RemovableMedia') or info.get('VolumeUUID') != '83FFC12E-67E1-307F-91AD-E584C2E01E87':
    raise SystemExit('not the inspected MEGA65 card')
for stem in ('R0FHOST1', 'R0FSUC10'):
    directory = root / 'build/r0f/successor-t05-recovery' / stem
    manifest = json.loads((directory / 'release.json').read_text())
    image = directory / (stem + '.D81')
    if (manifest['D81_STATE'] != 'XEMU_BOOT_VERIFIED' or manifest['XEMU_RESULT'] != 'PASS'
            or manifest['HOST_STRUCTURAL_RESULT'] != 'PASS' or manifest['HOST_CONTENT_RESULT'] != 'PASS'
            or manifest['D81_FILENAME'] != image.name or len(manifest['XEMU_EVIDENCE']) != 4
            or image.stat().st_size != 819200
            or hashlib.sha256(image.read_bytes()).hexdigest() != manifest['D81_SHA256']):
        raise SystemExit('candidate identity/Gate-3 evidence not verified: ' + stem)
    for run in manifest['XEMU_EVIDENCE']:
        if run['mountedD81Filename'] != image.name or run['preRunD81Sha256'] != manifest['D81_SHA256']:
            raise SystemExit('exact-name Gate-3 mismatch')
    if [run['run'] for run in manifest['XEMU_EVIDENCE']] != ['ntsc-1', 'ntsc-2', 'pal-1', 'pal-2']:
        raise SystemExit('missing unique NTSC/PAL boot repetitions')
    if stem == 'R0FHOST1':
        identities = manifest.get('CURRENT_DELIVERY_TOOL_SHA256', {})
        required = ['d81_delivery.py', 'd81_sd_transfer.sh', 'd81_sd_contiguity.py', 'd81_fat32_audit.py']
        for name in required:
            path = root / 'tools/diagnostics' / name
            if identities.get(str(path.relative_to(root))) != hashlib.sha256(path.read_bytes()).hexdigest():
                raise SystemExit('delivery tooling changed since fresh host/Xemu revalidation: ' + name)
if (mount / 'R0FHOST1.D81').exists():
    raise SystemExit('R0FHOST1.D81 already exists; inspect, never overwrite or rerun blindly')
PY
/usr/bin/python3 -B tools/diagnostics/d81_fat32_audit.py "$mount" \
  R0FSUCC10.D81 R0FSUC10.D81 --json "$out/sd-before.json"
# The preserved sd-diagnostic.json includes the unrelated F65BLK02 anomaly.
# It is not a release input or a known-good current on-card control. Do not
# repair it or make this candidate depend on reading its contents. Raw volume
# metadata and the actual candidate still pass the strict transfer gates.

slot_present=0
if test -f "$mount/R0FSUC10.D81"; then
  # Reject a nonblank image before any native-slot fill. Owner attested this
  # slot was created by the MEGA65; bytes alone cannot establish its provenance.
  /usr/bin/python3 -B - "$mount/R0FSUC10.D81" <<'PY'
from pathlib import Path
import sys
data = Path(sys.argv[1]).read_bytes()
if len(data) != 819200:
    raise SystemExit('native slot size mismatch')
track, sector = data[399360:399362]
seen = set()
while track:
    if track != 40 or not 3 <= sector < 40 or (track, sector) in seen:
        raise SystemExit('native slot directory is invalid')
    seen.add((track, sector))
    offset = ((track - 1) * 40 + sector) * 256
    block = data[offset:offset + 256]
    if any(block[i] for i in range(2, 256, 32)):
        raise SystemExit('native slot is not blank; refusing overwrite')
    track, sector = block[:2]
if not seen:
    raise SystemExit('missing native slot directory')
PY
  slot_present=1
  tools/diagnostics/d81_sd_fill_mega65_slot.sh "$out/R0FSUC10/R0FSUC10.D81" "$mount" "$hash"
  # Slot helper has already flushed/ejected successfully. Reidentify by the
  # captured partition and check UUID again before the separate host transfer.
  device=$(/usr/bin/python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["device"]["DeviceIdentifier"])' "$out/sd-before.json")
  /usr/sbin/diskutil mount "$device"
  /usr/bin/python3 -B - "$root" "$mount" <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, str(Path(sys.argv[1]) / 'tools/diagnostics'))
from d81_sd_contiguity import disk_info
if disk_info(Path(sys.argv[2])).get('VolumeUUID') != '83FFC12E-67E1-307F-91AD-E584C2E01E87':
    raise SystemExit('card changed after remount')
PY
else
  echo 'R0FSUC10.D81 native slot ABSENT: not filled; continuing authorized host-created candidate.'
fi
tools/diagnostics/d81_sd_transfer.sh "$out/R0FHOST1/R0FHOST1.D81" "$mount" "$hash"
echo "RECOVERY HOST TRANSFER PASS; native_slot_filled=$slot_present; safe_eject=PASS"
