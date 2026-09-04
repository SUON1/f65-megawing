#!/usr/bin/env python3
"""Fail-closed macOS extent gate for a D81 copied to a MEGA65 FAT32 card."""

import argparse
import fcntl
import hashlib
import json
import os
import pathlib
import plistlib
import struct
import subprocess
import sys
import tempfile

IMAGE_BYTES = 819200
F_LOG2PHYS_EXT = 65


def fail(message):
    raise SystemExit("D81 SD contiguity gate failed: " + message)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def mount_point(path):
    current = path.resolve()
    if current.is_file():
        current = current.parent
    while not os.path.ismount(current):
        parent = current.parent
        if parent == current:
            fail("could not identify containing mount point")
        current = parent
    return current


def disk_info(mount):
    result = subprocess.run(
        ["/usr/sbin/diskutil", "info", "-plist", str(mount)],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        fail("diskutil could not inspect mount point %s" % mount)
    try:
        info = plistlib.loads(result.stdout)
    except plistlib.InvalidFileException:
        fail("diskutil returned invalid plist data")
    filesystem = str(info.get("FilesystemType", "")).lower()
    filesystem_name = str(info.get("FilesystemName", ""))
    if filesystem not in ("msdos", "fat", "fat32") and "FAT32" not in filesystem_name.upper():
        fail("target filesystem is not FAT32/MS-DOS FAT32: %r / %r" % (filesystem, filesystem_name))
    return info


def merge_adjacent(extents):
    merged = []
    for extent in extents:
        if merged and merged[-1][0] + merged[-1][1] == extent[0] and merged[-1][2] + merged[-1][1] == extent[2]:
            merged[-1] = (merged[-1][0], merged[-1][1] + extent[1], merged[-1][2])
        else:
            merged.append(extent)
    return merged


def physical_extents(path):
    size = path.stat().st_size
    extents = []
    descriptor = os.open(path, os.O_RDONLY)
    try:
        offset = 0
        while offset < size:
            query = struct.pack("=Iqq", 0, size - offset, offset)
            try:
                answer = fcntl.fcntl(descriptor, F_LOG2PHYS_EXT, query)
            except OSError as error:
                fail("F_LOG2PHYS_EXT is unavailable: %s" % error)
            _, contiguous_bytes, device_offset = struct.unpack("=Iqq", answer)
            if contiguous_bytes <= 0:
                fail("extent length is unavailable at logical offset %d" % offset)
            length = min(contiguous_bytes, size - offset)
            extents.append((offset, length, device_offset))
            offset += length
    finally:
        os.close(descriptor)
    return merge_adjacent(extents)


def fat32_extents(info, filename, file_size, root_only=False):
    """Read the FAT32 cluster chain from the block device when macOS will not map it."""
    device = str(info.get("DeviceNode", ""))
    if not device.startswith("/dev/disk"):
        fail("diskutil did not provide a readable FAT32 device node")
    raw_device = device.replace("/dev/disk", "/dev/rdisk", 1)
    try:
        descriptor = os.open(raw_device, os.O_RDONLY)
    except PermissionError:
        fail(
            "macOS denied read-only access to %s; run this inspector from a user Terminal "
            "with sudo, or grant the invoking terminal Full Disk Access" % raw_device
        )
    try:
        boot = os.pread(descriptor, 512, 0)
        if len(boot) != 512 or boot[82:90] != b"FAT32   ":
            fail("raw device is not a recognizable FAT32 volume")
        bytes_per_sector = struct.unpack_from("<H", boot, 11)[0]
        sectors_per_cluster = boot[13]
        reserved_sectors = struct.unpack_from("<H", boot, 14)[0]
        fat_count = boot[16]
        fat_sectors = struct.unpack_from("<I", boot, 36)[0]
        root_cluster = struct.unpack_from("<I", boot, 44)[0]
        if not all((bytes_per_sector, sectors_per_cluster, reserved_sectors, fat_count, fat_sectors, root_cluster >= 2)):
            fail("FAT32 boot record contains invalid allocation geometry")
        cluster_bytes = bytes_per_sector * sectors_per_cluster
        fat_offset = reserved_sectors * bytes_per_sector
        data_offset = (reserved_sectors + fat_count * fat_sectors) * bytes_per_sector

        def cluster_offset(cluster):
            if cluster < 2:
                fail("FAT32 cluster chain contains reserved cluster %d" % cluster)
            return data_offset + (cluster - 2) * cluster_bytes

        def next_cluster(cluster):
            entry_offset = fat_offset + cluster * 4
            sector_offset = entry_offset - (entry_offset % bytes_per_sector)
            sector = os.pread(descriptor, bytes_per_sector, sector_offset)
            entry_in_sector = entry_offset - sector_offset
            entry = sector[entry_in_sector:entry_in_sector + 4]
            if len(sector) != bytes_per_sector or len(entry) != 4:
                fail("could not read FAT32 allocation table")
            return struct.unpack("<I", entry)[0] & 0x0FFFFFFF

        def chain(first):
            result, seen, current = [], set(), first
            while current < 0x0FFFFFF8:
                if current in seen:
                    fail("FAT32 cluster chain loops")
                seen.add(current)
                result.append(current)
                current = next_cluster(current)
            return result

        wanted = filename.upper().encode("ascii")
        if wanted.count(b".") > 1:
            fail("filename cannot be represented as a FAT 8.3 name")
        stem, _, suffix = wanted.partition(b".")
        if not stem or len(stem) > 8 or len(suffix) > 3:
            fail("filename cannot be represented as a FAT 8.3 name")
        wanted_short = stem.ljust(8, b" ") + suffix.ljust(3, b" ")

        def find_in_directory(first, visited):
            if first in visited:
                return None
            visited.add(first)
            for directory_cluster in chain(first):
                directory = os.pread(descriptor, cluster_bytes, cluster_offset(directory_cluster))
                for offset in range(0, len(directory), 32):
                    entry = directory[offset:offset + 32]
                    if not entry or entry[0] == 0x00:
                        return None
                    if entry[0] == 0xE5 or entry[11] == 0x0F:
                        continue
                    attributes = entry[11]
                    if entry[:11] == wanted_short and not (attributes & 0x10):
                        first_cluster = struct.unpack_from("<H", entry, 26)[0] | (struct.unpack_from("<H", entry, 20)[0] << 16)
                        return first_cluster, struct.unpack_from("<I", entry, 28)[0]
                    if not root_only and attributes & 0x10 and entry[:1] != b".":
                        child = struct.unpack_from("<H", entry, 26)[0] | (struct.unpack_from("<H", entry, 20)[0] << 16)
                        found = find_in_directory(child, visited)
                        if found:
                            return found
            return None

        found = find_in_directory(root_cluster, set())
        if not found:
            fail("could not locate %s in FAT32 directory entries" % filename)
        first_cluster, directory_size = found
        if directory_size != file_size:
            fail("FAT32 directory file size does not match copied D81")
        clusters = chain(first_cluster)
        expected_clusters = (file_size + cluster_bytes - 1) // cluster_bytes
        if len(clusters) != expected_clusters:
            fail("FAT32 cluster chain length does not match copied D81")
        extents, logical = [], 0
        start = previous = clusters[0]
        for cluster in clusters[1:]:
            if cluster != previous + 1:
                length = min((previous - start + 1) * cluster_bytes, file_size - logical)
                extents.append((logical, length, cluster_offset(start)))
                logical += length
                start = cluster
            previous = cluster
        extents.append((logical, file_size - logical, cluster_offset(start)))
        return extents
    finally:
        os.close(descriptor)


def write_report(path, report):
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


def self_test():
    assert merge_adjacent([(0, 100, 1000), (100, 100, 1100)]) == [(0, 200, 1000)]
    assert len(merge_adjacent([(0, 100, 1000), (100, 100, 1300)])) == 2
    if sys.platform != "darwin":
        fail("F_LOG2PHYS_EXT inspector requires macOS")
    with tempfile.NamedTemporaryFile(prefix="d81-extent-selftest-") as probe:
        probe.write(b"\0" * 8192)
        probe.flush()
        extents = physical_extents(pathlib.Path(probe.name))
        assert sum(extent[1] for extent in extents) == 8192
    print("D81-SD-CONTIGUITY self-test PASS")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("copied_d81", nargs="?", type=pathlib.Path)
    parser.add_argument("--expected-sha256")
    parser.add_argument("--json", type=pathlib.Path)
    parser.add_argument(
        "--fat32-root-only",
        action="store_true",
        help="require the raw FAT32 fallback to resolve the 8.3 name in the volume root",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if sys.platform != "darwin":
        fail("F_LOG2PHYS_EXT inspector requires macOS")
    if args.copied_d81 is None or args.expected_sha256 is None:
        parser.error("copied_d81 and --expected-sha256 are required")
    image = args.copied_d81.resolve()
    if not image.is_file() or image.stat().st_size != IMAGE_BYTES:
        fail("copied file is absent or not exactly 819200 bytes")
    actual_sha = sha256(image)
    if actual_sha != args.expected_sha256.lower():
        fail("copied-file SHA-256 mismatch: " + actual_sha)
    mount = mount_point(image)
    info = disk_info(mount)
    try:
        extents = physical_extents(image)
        inspector = "macOS F_LOG2PHYS_EXT via tools/diagnostics/d81_sd_contiguity.py"
    except SystemExit as error:
        if "F_LOG2PHYS_EXT is unavailable" not in str(error):
            raise
        extents = fat32_extents(
            info, image.name, image.stat().st_size, root_only=args.fat32_root_only
        )
        inspector = "raw FAT32 cluster-chain audit via tools/diagnostics/d81_sd_contiguity.py"
    report = {
        "D81_STATE": "SD_CONTIGUITY_VERIFIED" if len(extents) == 1 else "INVALID_FOR_MEGA65_FREEZER_MOUNT",
        "D81_PATH": str(image),
        "D81_BYTES": IMAGE_BYTES,
        "D81_SHA256": actual_sha,
        "SD_FILESYSTEM": info.get("FilesystemName") or info.get("FilesystemType"),
        "SD_DEVICE_IDENTIFIER": info.get("DeviceIdentifier"),
        "SD_INTERNAL": info.get("Internal"),
        "SD_REMOVABLE": info.get("RemovableMedia"),
        "SD_MOUNT_POINT": str(mount),
        "SD_EXTENT_COUNT": len(extents),
        "SD_EXTENTS": [
            {"logicalOffset": logical, "bytes": length, "deviceOffset": device}
            for logical, length, device in extents
        ],
        "SD_CONTIGUITY_RESULT": "PASS" if len(extents) == 1 else "FAIL",
        "INSPECTOR": inspector,
    }
    write_report(args.json, report)
    if len(extents) != 1 or extents[0][1] != IMAGE_BYTES:
        fail("copied D81 occupies %d physical extents" % len(extents))
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
