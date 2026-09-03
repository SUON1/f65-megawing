#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)

if test "$#" -ne 3; then
  echo "usage: d81_sd_transfer.sh SOURCE.D81 /Volumes/MEGA65FDISK EXPECTED_SHA256" >&2
  exit 2
fi

source_image=$1
requested_mount=$2
expected_sha=$3
filename=$(basename -- "$source_image")
test -d "$requested_mount" || { echo "SD mount is absent" >&2; exit 2; }
sd_mount=$(CDPATH= cd -- "$requested_mount" && pwd -P)
target="$sd_mount/$filename"
staging="$sd_mount/.$filename.COPYING"
report_dir="$root/build/d81-sd-transfer"

test -f "$source_image" || { echo "source D81 is absent" >&2; exit 2; }
test "$(stat -f '%z' "$source_image")" = "819200" || { echo "source D81 is not exactly 819200 bytes" >&2; exit 2; }
printf '%s\n' "$filename" | rg -q '^[A-Z0-9][A-Z0-9._-]*\.D81$' || { echo "final filename is not an uppercase ASCII-safe .D81 name" >&2; exit 2; }
printf '%s\n' "$expected_sha" | rg -q '^[0-9a-f]{64}$' || { echo "expected SHA-256 is not 64 lowercase hexadecimal characters" >&2; exit 2; }
test "$(dirname -- "$target")" = "$sd_mount" || { echo "target is not at the SD root" >&2; exit 2; }
test ! -e "$target" || { echo "final target already exists; failed identities are never overwritten" >&2; exit 2; }
test ! -e "$staging" || { echo "staging target already exists; inspect it before continuing" >&2; exit 2; }

actual_sha=$(shasum -a 256 "$source_image" | awk '{print $1}')
test "$actual_sha" = "$expected_sha" || { echo "source SHA-256 does not match the authorized identity" >&2; exit 2; }

mkdir -p "$report_dir"
/bin/cp -X "$source_image" "$staging"
sync
python3 "$root/tools/diagnostics/d81_sd_contiguity.py" "$staging" --expected-sha256 "$expected_sha" --json "$report_dir/$filename.staging.json"
mv -n "$staging" "$target"
sync
python3 "$root/tools/diagnostics/d81_sd_contiguity.py" "$target" --expected-sha256 "$expected_sha" --json "$report_dir/$filename.final.json"
/usr/sbin/diskutil eject "$sd_mount"

printf '%s\n' "D81 SD TRANSFER PASS" "filename=$filename" "sha256=$expected_sha" "extent_count=1" "safe_eject=PASS"
