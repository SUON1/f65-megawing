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

cleanup() {
  cleanup_exit=$?
  trap - EXIT HUP INT TERM
  if test "$cleanup_exit" -ne 0 && test "$staging_created" -eq 1 && test -e "$staging"; then
    rm -f -- "$staging"
  fi
  exit "$cleanup_exit"
}
trap cleanup EXIT HUP INT TERM

test -f "$source_image" || { echo "source D81 is absent" >&2; exit 2; }
test "$(stat -f '%z' "$source_image")" = "819200" || { echo "source D81 is not exactly 819200 bytes" >&2; exit 2; }
printf '%s\n' "$filename" | rg -q '^[A-Z0-9][A-Z0-9]{0,7}\.D81$' || { echo "final filename is not an uppercase FAT 8.3 .D81 name" >&2; exit 2; }
printf '%s\n' "$expected_sha" | rg -q '^[0-9a-f]{64}$' || { echo "expected SHA-256 is not 64 lowercase hexadecimal characters" >&2; exit 2; }
test "$(dirname -- "$target")" = "$sd_mount" || { echo "target is not at the SD root" >&2; exit 2; }
test ! -e "$target" || { echo "final target already exists; failed identities are never overwritten" >&2; exit 2; }
test ! -e "$staging" || { echo "staging target already exists; inspect it before continuing" >&2; exit 2; }

actual_sha=$(shasum -a 256 "$source_image" | awk '{print $1}')
test "$actual_sha" = "$expected_sha" || { echo "source SHA-256 does not match the authorized identity" >&2; exit 2; }

mkdir -p "$report_dir"
/bin/cp -X "$source_image" "$staging"
staging_created=1
sync
python3 "$root/tools/diagnostics/d81_sd_contiguity.py" "$staging" --expected-sha256 "$expected_sha" --json "$report_dir/$filename.staging.json"
mv -n "$staging" "$target"
staging_created=0
sync
python3 "$root/tools/diagnostics/d81_sd_contiguity.py" "$target" --expected-sha256 "$expected_sha" --json "$report_dir/$filename.final.json"
/usr/sbin/diskutil eject "$sd_mount"

printf '%s\n' "D81 SD TRANSFER PASS" "filename=$filename" "sha256=$expected_sha" "extent_count=1" "safe_eject=PASS"
