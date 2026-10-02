#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)

if test "$#" -ne 3; then
  echo "usage: d81_sd_transfer.sh SOURCE.D81 /Volumes/MEGA65FDISK EXPECTED_SHA256" >&2
  exit 2
fi

# On macOS, the independent FAT32 chain inspection normally needs raw-device
# access. Refuse before creating a staging file: a non-privileged invocation
# used to copy first and fail later, leaving an unaudited file on the card.
if test "$(id -u)" -ne 0; then
  echo "run this fail-closed transfer helper with sudo; raw FAT32 inspection is required before any SD write" >&2
  exit 2
fi

source_image=$1
requested_mount=$2
expected_sha=$3
filename=$(basename -- "$source_image")
test -d "$requested_mount" || { echo "SD mount is absent" >&2; exit 2; }
sd_mount=$(CDPATH= cd -- "$requested_mount" && pwd -P)
target="$sd_mount/$filename"
# The raw FAT32 fallback deliberately resolves a conventional 8.3 entry rather
# than trusting macOS logical extents. Keep the temporary file non-D81 and 8.3
# compatible so both staging and final allocation chains can be audited.
stem=${filename%.D81}
stage_stem=$(printf '%s' "$stem" | cut -c 1-7)
staging="$sd_mount/S${stage_stem}.TMP"
report_dir="$root/build/d81-sd-transfer"
staging_created=0
final_created=0

cleanup() {
  cleanup_exit=$?
  trap - EXIT HUP INT TERM
  if test "$cleanup_exit" -ne 0 && test "$staging_created" -eq 1 && test -e "$staging"; then
    rm -f -- "$staging"
  fi
  if test "$cleanup_exit" -ne 0 && test "$final_created" -eq 1 && test -e "$target"; then
    echo "final file retained for diagnosis; NOT RELEASED: $target" >&2
  fi
  exit "$cleanup_exit"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

test -f "$source_image" || { echo "source D81 is absent" >&2; exit 2; }
test "$(stat -f '%z' "$source_image")" = "819200" || { echo "source D81 is not exactly 819200 bytes" >&2; exit 2; }
python3 "$root/tools/diagnostics/d81_delivery.py" name "$filename"
printf '%s\n' "$expected_sha" | /usr/bin/grep -Eq '^[0-9a-f]{64}$' || { echo "expected SHA-256 is not 64 lowercase hexadecimal characters" >&2; exit 2; }
test "$(dirname -- "$target")" = "$sd_mount" || { echo "target is not at the SD root" >&2; exit 2; }
test ! -e "$target" || { echo "final target already exists; failed identities are never overwritten" >&2; exit 2; }
test ! -e "$staging" || { echo "staging target already exists; inspect it before continuing" >&2; exit 2; }

actual_sha=$(shasum -a 256 "$source_image" | awk '{print $1}')
test "$actual_sha" = "$expected_sha" || { echo "source SHA-256 does not match the authorized identity" >&2; exit 2; }

mkdir -p "$report_dir"
# Validate the intended removable FAT32 volume before any creation, and prove
# raw-device read access up front. Do not discover a wrong volume after copying.
python3 - "$sd_mount" "$root" "$filename" "$(basename -- "$staging")" <<'PY'
import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(sys.argv[2]) / 'tools/diagnostics'))
from d81_sd_contiguity import disk_info
from d81_fat32_audit import Fat32
mount = Path(sys.argv[1])
if not os.path.ismount(mount):
    raise SystemExit('destination must be the volume root')
info = disk_info(mount)
if info.get('RemovableMedia') is not True:
    raise SystemExit('removable FAT32 media required')
device = info.get('DeviceNode', '')
if not device.startswith('/dev/disk'):
    raise SystemExit('missing raw device identity')
fd = os.open(device.replace('/dev/disk', '/dev/rdisk', 1), os.O_RDONLY)
try:
    # Validate geometry, FAT mirrors and the root before allocation. Existing
    # unrelated file payloads are not inputs to this candidate's release gate.
    volume = Fat32(fd)
    forbidden = {name.upper() for name in sys.argv[3:]}
    for entry in volume.root_entries():
        if entry['name'].upper() in forbidden or entry['shortName'].upper() in forbidden:
            raise SystemExit('raw FAT target/staging name already exists; no overwrite')
finally:
    os.close(fd)
PY
python3 "$root/tools/diagnostics/d81_delivery.py" contiguous-copy "$source_image" "$staging" "$expected_sha"
staging_created=1
sync
python3 "$root/tools/diagnostics/d81_sd_contiguity.py" "$staging" --expected-sha256 "$expected_sha" --fat32-root-only --json "$report_dir/$filename.staging.json"
python3 "$root/tools/diagnostics/d81_delivery.py" rename-exclusive "$staging" "$target"
staging_created=0
final_created=1
sync
python3 "$root/tools/diagnostics/d81_sd_contiguity.py" "$target" --expected-sha256 "$expected_sha" --fat32-root-only --json "$report_dir/$filename.final.json"
/usr/sbin/diskutil eject "$sd_mount"
final_created=0
python3 - "$report_dir/$filename.final.json" <<'PY'
import json
from pathlib import Path
import sys
path = Path(sys.argv[1])
report = json.loads(path.read_text())
report.update(SD_SAFE_EJECT_RESULT='PASS', SD_TRANSFER_METHOD='macOS F_PREALLOCATE contiguous/all, staged copy, exclusive rename',
              D81_STATE='AWAITING_PHYSICAL_CHOOSER_VERIFICATION', PHYSICAL_CHOOSER_RESULT='AWAITING HUMAN')
path.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
PY

printf '%s\n' "D81 SD TRANSFER PASS" "filename=$filename" "sha256=$expected_sha" "extent_count=1" "safe_eject=PASS"
