#!/usr/bin/env python3
"""Read-only reproduction of the reviewed photographic transcription."""
import hashlib
import json
from pathlib import Path
import zlib

HERE = Path(__file__).resolve().parent
rows = {n: (HERE / f'{n:02}-rows.txt').read_text().splitlines()
        for n in range(4, 18)}
fixes = json.loads((HERE / 'corrections.json').read_text())
for item in fixes['rows']:
    rows[item['photo']][item['row']] = item['text']
for item in fixes['cells']:
    line = list(rows[item['photo']][item['row']])
    line[item['column']] = item['value']
    rows[item['photo']][item['row']] = ''.join(line)
stream = bytearray()
for photo, lines in rows.items():
    page = photo - 3
    assert len(lines) == 16 and all(len(s) == 64 for s in lines)
    expected_header = (f'{page:02X} {(page-1)*512:04X} '
                       f'{416 if page == 14 else 512:04X} 32B8A599 105995A3')
    retained = (HERE / 'transcripts' / f'page-{page:02X}.txt').read_text().splitlines()
    assert retained == [expected_header] + lines
    block = bytes.fromhex(''.join(lines))
    if page == 14:
        assert block[416:] == bytes(96)
        block = block[:416]
    stream.extend(block)
assert len(stream) == 7072
assert stream == (HERE / 'transcripts/capture.bin').read_bytes()
result, raw = stream[:1792], stream[1792:]
assert result == (HERE / 'result.bin').read_bytes()
assert raw == (HERE / 'durations.bin').read_bytes()
assert zlib.crc32(result[:1788]) == int.from_bytes(result[1788:], 'little') == 0x32B8A599
assert zlib.crc32(raw) == int.from_bytes(result[72:76], 'little') == 0x105995A3
assert int.from_bytes(result[88:92], 'little') == 4
assert int.from_bytes(result[1668:1672], 'little') == 4
print('Photographic transcription PASS: 14 pages, 7072 bytes; CRC32 32B8A599 / 105995A3; real edges 4 detected / 4 consumed')
print('Capture SHA256:', hashlib.sha256(stream).hexdigest())
