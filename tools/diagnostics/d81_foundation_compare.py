#!/usr/bin/env python3
"""Read-only forensic comparison for D81 mountability investigations.

This tool does not declare a D81 mountable.  It establishes whether a candidate
is internally consistent and shows every byte-level difference from a known
physical-pass control, grouped by D81 filesystem component.
"""

import argparse
import hashlib
import json
from pathlib import Path
import sys


TRACKS = 80
SECTORS_PER_TRACK = 40
SECTOR_BYTES = 256
IMAGE_BYTES = TRACKS * SECTORS_PER_TRACK * SECTOR_BYTES
HEADER_SECTOR = (40, 0)
BAM_SECTORS = {(40, 1), (40, 2)}


def fail(message):
    raise SystemExit("D81 foundation comparison failed: " + message)


def petscii(raw):
    return bytes(value & 0x7F for value in raw).decode("ascii", "replace").rstrip(" \xA0")


class Image:
    def __init__(self, path):
        self.path = Path(path).resolve()
        if not self.path.is_file() or self.path.stat().st_size != IMAGE_BYTES:
            fail("%s is not an exact 819200-byte D81" % self.path)
        self.data = self.path.read_bytes()
        self.sha256 = hashlib.sha256(self.data).hexdigest()
        self.directory_sectors = set()
        self.file_sectors = {}
        self.entries = []
        self._parse()

    @staticmethod
    def offset(sector):
        track, sector_number = sector
        if not (1 <= track <= TRACKS and 0 <= sector_number < SECTORS_PER_TRACK):
            fail("out-of-range D81 sector %r" % (sector,))
        return ((track - 1) * SECTORS_PER_TRACK + sector_number) * SECTOR_BYTES

    def sector(self, location):
        offset = self.offset(location)
        return self.data[offset:offset + SECTOR_BYTES]

    def _next(self, block):
        return (block[0], block[1]) if block[0] else None

    def _chain(self, first, owner):
        result = []
        seen = set()
        current = first
        while current is not None:
            if current in seen:
                fail("%s: loop in %s chain" % (self.path.name, owner))
            seen.add(current)
            result.append(current)
            current = self._next(self.sector(current))
        return result

    def _parse(self):
        header = self.sector(HEADER_SECTOR)
        if tuple(header[:2]) != (40, 3):
            fail("%s: header directory pointer is not 40/3" % self.path.name)
        self.label = petscii(header[4:20])
        self.identifier = petscii(header[22:24])
        directory = self._chain((40, 3), "directory")
        self.directory_sectors.update(directory)
        occupied = {HEADER_SECTOR, *BAM_SECTORS, *directory}
        for directory_sector in directory:
            block = self.sector(directory_sector)
            for offset in range(2, SECTOR_BYTES, 32):
                entry = block[offset:offset + 32]
                if entry[0] == 0:
                    continue
                if entry[0] != 0x82:
                    fail("%s: unsupported directory file type %02x" % (self.path.name, entry[0]))
                name = petscii(entry[3:19]).lower()
                first = (entry[1], entry[2])
                chain = self._chain(first, "file " + name)
                collision = occupied.intersection(chain)
                if collision:
                    fail("%s: sector ownership collision in %s: %s" % (self.path.name, name, sorted(collision)))
                occupied.update(chain)
                self.file_sectors[name] = set(chain)
                raw = bytearray()
                for index, location in enumerate(chain):
                    block_data = self.sector(location)
                    if index == len(chain) - 1:
                        if block_data[0] != 0 or not (2 <= block_data[1] <= 255):
                            fail("%s: malformed terminal sector for %s" % (self.path.name, name))
                        raw.extend(block_data[2:block_data[1] + 1])
                    else:
                        if block_data[0] == 0:
                            fail("%s: early terminal sector for %s" % (self.path.name, name))
                        raw.extend(block_data[2:])
                blocks = entry[28] | (entry[29] << 8)
                if blocks != len(chain):
                    fail("%s: directory block count mismatch for %s" % (self.path.name, name))
                self.entries.append({
                    "name": name,
                    "type": entry[0],
                    "firstSector": {"track": first[0], "sector": first[1]},
                    "blocks": blocks,
                    "payloadBytes": len(raw),
                    "payloadSha256": hashlib.sha256(raw).hexdigest(),
                    "chain": [{"track": track, "sector": sector} for track, sector in chain],
                })
        self.occupied = occupied
        self._validate_bam()

    def _validate_bam(self):
        free = set()
        for track in range(1, TRACKS + 1):
            bam = self.sector((40, 1 if track <= 40 else 2))
            offset = 16 + ((track - 1) % 40) * 6
            bits = bam[offset + 1:offset + 6]
            available = {
                (track, sector)
                for sector in range(SECTORS_PER_TRACK)
                if bits[sector // 8] & (1 << (sector % 8))
            }
            if bam[offset] != len(available):
                fail("%s: BAM count mismatch on track %d" % (self.path.name, track))
            free.update(available)
        allocated = {
            (track, sector)
            for track in range(1, TRACKS + 1)
            for sector in range(SECTORS_PER_TRACK)
            if (track, sector) not in free
        }
        if allocated != self.occupied:
            fail("%s: BAM ownership does not match header, BAM, directory, and file chains" % self.path.name)
        self.free_blocks = len(free)

    def describe(self):
        return {
            "path": str(self.path),
            "sha256": self.sha256,
            "bytes": IMAGE_BYTES,
            "label": self.label,
            "identifier": self.identifier,
            "freeBlocks": self.free_blocks,
            "entries": self.entries,
        }

    def component_at(self, byte_offset):
        sector_index = byte_offset // SECTOR_BYTES
        location = (sector_index // SECTORS_PER_TRACK + 1, sector_index % SECTORS_PER_TRACK)
        if location == HEADER_SECTOR:
            return "header"
        if location in BAM_SECTORS:
            return "bam"
        if location in self.directory_sectors:
            return "directory"
        for name, sectors in self.file_sectors.items():
            if location in sectors:
                return "payload:" + name
        return "unallocated-or-unknown"


def difference_summary(control, candidate):
    counts = {}
    ranges = []
    start = None
    previous = None
    for index, (left, right) in enumerate(zip(control.data, candidate.data)):
        if left == right:
            if start is not None:
                ranges.append((start, previous))
                start = previous = None
            continue
        component = control.component_at(index)
        counts[component] = counts.get(component, 0) + 1
        if start is None or index != previous + 1:
            if start is not None:
                ranges.append((start, previous))
            start = index
        previous = index
    if start is not None:
        ranges.append((start, previous))
    samples = []
    for start, end in ranges[:32]:
        sector_index = start // SECTOR_BYTES
        samples.append({
            "startByte": start,
            "endByte": end,
            "component": control.component_at(start),
            "startSector": {
                "track": sector_index // SECTORS_PER_TRACK + 1,
                "sector": sector_index % SECTORS_PER_TRACK,
                "offset": start % SECTOR_BYTES,
            },
        })
    return {
        "differingBytes": sum(counts.values()),
        "differingRanges": len(ranges),
        "differencesByControlComponent": counts,
        "firstRanges": samples,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--control", required=True, type=Path, help="known physical-pass D81")
    parser.add_argument("--candidate", required=True, action="append", type=Path, help="candidate or failed D81; repeatable")
    parser.add_argument("--json", type=Path, help="write machine-readable report")
    args = parser.parse_args()
    control = Image(args.control)
    candidates = [Image(path) for path in args.candidate]
    report = {
        "tool": "tools/diagnostics/d81_foundation_compare.py",
        "state": "FORENSIC_COMPARISON_ONLY",
        "control": control.describe(),
        "candidates": [
            {"image": candidate.describe(), "differenceFromControl": difference_summary(control, candidate)}
            for candidate in candidates
        ],
        "limitations": [
            "A structural pass and byte comparison do not prove Freezer mountability.",
            "SD-card file allocation and physical chooser evidence are separate gates.",
            "The report identifies byte-level differences; it does not infer a cause from them.",
        ],
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
