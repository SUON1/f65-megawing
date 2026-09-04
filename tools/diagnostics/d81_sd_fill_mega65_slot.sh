#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)

if test "$#" -ne 3; then
  echo "usage: d81_sd_fill_mega65_slot.sh SOURCE.D81 /Volumes/MEGA65FDISK EXPECTED_SHA256" >&2
  exit 2
fi

# The raw FAT32 audit normally requires direct device access on macOS. Refuse
# before inspecting or changing the card when the invocation is not privileged.
if test "$(id -u)" -ne 0; then
  echo "run this fail-closed slot-fill helper with sudo; raw FAT32 inspection is required before any SD write" >&2
  exit 2
fi

source_image=$1
requested_mount=$2
expected_sha=$3
filename=$(basename -- "$source_image")
test -d "$requested_mount" || { echo "SD mount is absent" >&2; exit 2; }
sd_mount=$(CDPATH= cd -- "$requested_mount" && pwd -P)
target="$sd_mount/$filename"
report_dir="$root/build/d81-sd-transfer"
backup_dir="$report_dir/slot-backups"
slot_modified=0
backup=
preimage_sha=

rollback() {
  rollback_exit=$?
  trap - EXIT HUP INT TERM
  if test "$rollback_exit" -ne 0 && test "$slot_modified" -eq 1; then
    echo "slot fill failed after writing began; restoring the MEGA65-created slot in place" >&2
    if /bin/dd if="$backup" of="$target" bs=819200 count=1 conv=notrunc >/dev/null 2>&1; then
      sync
      restored_sha=$(shasum -a 256 "$target" | awk '{print $1}')
      if test "$restored_sha" = "$preimage_sha"; then
        echo "slot rollback PASS: original bytes restored; card remains mounted" >&2
      else
        echo "slot rollback FAILED: restored SHA-256 does not match; stop using this card until inspected" >&2
      fi
    else
      echo "slot rollback FAILED: in-place restore could not be written; stop using this card until inspected" >&2
    fi
  fi
  exit "$rollback_exit"
}
trap rollback EXIT HUP INT TERM

test -f "$source_image" || { echo "source D81 is absent" >&2; exit 2; }
test "$(stat -f '%z' "$source_image")" = "819200" || { echo "source D81 is not exactly 819200 bytes" >&2; exit 2; }
printf '%s\n' "$filename" | grep -Eq '^[A-Z0-9][A-Z0-9]{0,7}\.D81$' || { echo "source filename is not an uppercase FAT 8.3 .D81 slot name" >&2; exit 2; }
printf '%s\n' "$expected_sha" | grep -Eq '^[0-9a-f]{64}$' || { echo "expected SHA-256 is not 64 lowercase hexadecimal characters" >&2; exit 2; }
test "$(dirname -- "$target")" = "$sd_mount" || { echo "slot target is not at the SD root" >&2; exit 2; }
test -f "$target" || { echo "matching MEGA65-created root slot is absent: $target" >&2; exit 2; }
test ! -L "$target" || { echo "slot target must not be a symbolic link" >&2; exit 2; }
test "$(stat -f '%z' "$target")" = "819200" || { echo "MEGA65-created slot is not exactly 819200 bytes" >&2; exit 2; }

actual_sha=$(shasum -a 256 "$source_image" | awk '{print $1}')
test "$actual_sha" = "$expected_sha" || { echo "source SHA-256 does not match the authorized identity" >&2; exit 2; }
preimage_sha=$(shasum -a 256 "$target" | awk '{print $1}')
test "$preimage_sha" != "$expected_sha" || { echo "slot already contains the authorized image; refusing an unnecessary rewrite" >&2; exit 2; }

mkdir -p "$backup_dir"
python3 "$root/tools/diagnostics/d81_sd_contiguity.py" "$target" \
  --expected-sha256 "$preimage_sha" \
  --fat32-root-only \
  --json "$report_dir/$filename.slot-pre.json"

backup="$backup_dir/$filename.$preimage_sha.D81"
if test -e "$backup"; then
  backup_sha=$(shasum -a 256 "$backup" | awk '{print $1}')
  test "$(stat -f '%z' "$backup")" = "819200" && test "$backup_sha" = "$preimage_sha" || {
    echo "existing slot backup does not match the current preimage" >&2
    exit 2
  }
else
  /bin/cp -X "$target" "$backup"
  backup_sha=$(shasum -a 256 "$backup" | awk '{print $1}')
  test "$(stat -f '%z' "$backup")" = "819200" && test "$backup_sha" = "$preimage_sha" || {
    echo "slot backup verification failed" >&2
    exit 2
  }
fi

# Set the rollback flag before opening the target for writing. notrunc and the
# exact-size preconditions preserve the directory entry and FAT cluster chain.
slot_modified=1
/bin/dd if="$source_image" of="$target" bs=819200 count=1 conv=notrunc
sync
test "$(stat -f '%z' "$target")" = "819200" || { echo "slot size changed after in-place write" >&2; exit 2; }
post_sha=$(shasum -a 256 "$target" | awk '{print $1}')
test "$post_sha" = "$expected_sha" || { echo "slot SHA-256 mismatch after in-place write" >&2; exit 2; }
python3 "$root/tools/diagnostics/d81_sd_contiguity.py" "$target" \
  --expected-sha256 "$expected_sha" \
  --fat32-root-only \
  --json "$report_dir/$filename.slot-post.json"
sync
/usr/sbin/diskutil eject "$sd_mount"
slot_modified=0

printf '%s\n' \
  "D81 MEGA65 SLOT FILL PASS" \
  "filename=$filename" \
  "sha256=$expected_sha" \
  "extent_count=1" \
  "safe_eject=PASS"
