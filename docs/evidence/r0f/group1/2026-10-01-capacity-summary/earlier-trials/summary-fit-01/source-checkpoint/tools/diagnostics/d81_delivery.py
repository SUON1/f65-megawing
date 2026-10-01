#!/usr/bin/env python3
"""Shared host delivery invariants. No raw-device writes."""

import argparse
import ctypes
import fcntl
import hashlib
import os
from pathlib import Path
import re
import struct

IMAGE_BYTES = 819200


def require_name(name):
    if not re.fullmatch(r"[A-Z0-9]{1,8}\.D81", name, flags=re.ASCII):
        raise ValueError(f"{name!r}: require 1-8 uppercase letters/digits plus .D81")
    return name


def rename_exclusive(source, destination):
    """Darwin renamex_np(RENAME_EXCL), never overwrite an existing identity."""
    libc = ctypes.CDLL('/usr/lib/libSystem.B.dylib', use_errno=True)
    rename = libc.renamex_np
    rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int
    if rename(os.fsencode(source), os.fsencode(destination), 0x4):
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), str(destination))


def contiguous_copy(source, destination, expected_sha=None):
    """Create only a new staging file; ask the OS for one complete extent.

    Darwin F_PREALLOCATE/fstore_t from the installed SDK sys/fcntl.h.
    Request F_ALLOCATECONTIG | F_ALLOCATEALL, without a caller-side fallback.
    Apple's FSKit FAT implementation ignores the contiguous flag and uses
    best-effort allocation. Success is NOT proof of one extent or even of
    filesystem support for the flag; independent FAT inspection is mandatory.
    """
    payload = source.read_bytes()
    if len(payload) != IMAGE_BYTES:
        raise ValueError("source must be exactly 819200 bytes")
    if expected_sha is not None and hashlib.sha256(payload).hexdigest() != expected_sha:
        raise ValueError('source changed before allocation; no destination created')
    fd = os.open(destination, os.O_RDWR | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        request = struct.pack("@Iiqqq", 0x02 | 0x04, 3, 0, IMAGE_BYTES, 0)
        answer = fcntl.fcntl(fd, 42, request)
        allocated = struct.unpack("@Iiqqq", answer)[4]
        if allocated < IMAGE_BYTES:
            raise ValueError(f"OS allocated only {allocated} bytes")
        os.ftruncate(fd, IMAGE_BYTES)
        remaining = memoryview(payload)
        while remaining:
            count = os.write(fd, remaining)
            if count <= 0:
                raise OSError("short staging write")
            remaining = remaining[count:]
        os.fsync(fd)
    except BaseException:
        os.close(fd)
        destination.unlink()  # Only the file created by O_EXCL above.
        raise
    else:
        os.close(fd)
    print(f"OS reported {allocated} bytes allocated; contiguity UNVERIFIED; FAT audit required")


def allocation_probe(destination):
    """Test request acceptance, not contiguity support; remove the temporary file."""
    fd = os.open(destination, os.O_RDWR | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        request = struct.pack('@Iiqqq', 6, 3, 0, IMAGE_BYTES, 0)
        answer = fcntl.fcntl(fd, 42, request)
        allocated = struct.unpack('@Iiqqq', answer)[4]
        print(f'F_PREALLOCATE accepted; bytes allocated={allocated}; contiguity support NOT PROVEN')
    finally:
        os.close(fd)
        destination.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    name = sub.add_parser("name")
    name.add_argument("filename")
    copy = sub.add_parser("contiguous-copy")
    copy.add_argument("source", type=Path)
    copy.add_argument("staging", type=Path)
    copy.add_argument("expected_sha256")
    rename = sub.add_parser("rename-exclusive")
    rename.add_argument("source", type=Path)
    rename.add_argument("destination", type=Path)
    probe = sub.add_parser('allocation-probe')
    probe.add_argument('destination', type=Path)
    args = parser.parse_args()
    if args.command == "name":
        require_name(args.filename)
    elif args.command == 'rename-exclusive':
        rename_exclusive(args.source, args.destination)
    elif args.command == 'allocation-probe':
        allocation_probe(args.destination)
    else:
        require_name(args.source.name)
        contiguous_copy(args.source, args.staging, args.expected_sha256)


if __name__ == "__main__":
    main()
