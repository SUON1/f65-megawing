#!/usr/bin/env python3
"""Import the two CAP12 photographed pages after manual transcription.

Input: exactly 32 ordered rows, each a four-digit offset and 16 byte pairs.
Never invent missing bytes or substitute an expected SAVE for physical data.
"""
import argparse
import json
from pathlib import Path
import re

from r0f_successor_emulator import validate_success_result


def parse_rows(text):
    rows = text.splitlines()
    if len(rows) != 32:
        raise ValueError('exactly 32 rows required')
    result = bytearray()
    for row, line in enumerate(rows):
        if not re.fullmatch(r'[0-9A-Fa-f]{4}(?: [0-9A-Fa-f]{2}){16}', line):
            raise ValueError('invalid row format')
        fields = line.split(' ')
        if int(fields[0], 16) != row * 16:
            raise ValueError('missing, duplicate or reordered row')
        result.extend(int(value, 16) for value in fields[1:])
    validate_success_result(result)
    return bytes(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('transcript', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = parse_rows(args.transcript.read_text())
    args.out.mkdir(exist_ok=False, parents=True)
    (args.out / 'result.bin').write_bytes(result)
    (args.out / 'decoded.json').write_text(json.dumps({
        'state': 'RESULT_CRC_AND_SEMANTICS_VERIFIED_ONLY',
        'decoded': validate_success_result(result),
        'physicalSavedFile': 'NOT VERIFIED',
        'independentJavaReduction': 'NOT RUN',
        'fullR0FAcceptance': False,
    }, indent=2) + '\n')


if __name__ == '__main__':
    main()
