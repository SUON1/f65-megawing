"""Assess unmodified OCR candidates; never repair bytes using expected results."""
import json, re, sys, zlib

results = []
for record in map(json.loads, open(sys.argv[1])):
    texts = [line['text'] for line in record['lines']]
    header = next((s for s in texts if s.startswith('PAGE ')), '')
    match = re.fullmatch(r'PAGE ([0-9A-F]{4}) OF 0016 OFFSET ([0-9A-F]{4}) BYTES ([0-9A-F]{4})', header)
    if not match:
        results.append({'photo': record['path'], 'status': 'NO_STRICT_PAGE_HEADER', 'header': header})
        continue
    page, offset, size = (int(s, 16) for s in match.groups())
    crc_line = next((s for s in texts if s.startswith('TOTAL ')), '')
    crc_match = re.fullmatch(r'TOTAL 2B80 CRC32 ([0-9A-F]{8}) PAGECRC ([0-9A-F]{8})', crc_line)
    rows = [s for s in texts if re.fullmatch(r'[0-9A-F]{4}:[0-9A-F]{64}', s)]
    offsets = [int(s[:4], 16) for s in rows]
    ordered = offsets == list(range(offset, offset + 512, 32))
    entry = {'photo': record['path'], 'pageHex': f'{page:04X}', 'strictDataRows': len(rows), 'orderedOffsets': ordered, 'status': 'TRANSCRIPTION_INCOMPLETE'}
    if ordered and crc_match:
        data = b''.join(bytes.fromhex(s[5:]) for s in rows)[:size]
        observed = zlib.crc32(data)
        expected = int(crc_match[2],16)
        entry.update(calculatedPageCrc=f'{observed:08X}', ocrPageCrc=f'{expected:08X}', status='PAGE_CRC_MATCH' if observed == expected else 'TRANSCRIPTION_CRC_MISMATCH')
    results.append(entry)
print(json.dumps({'method':'strict OCR only; no character repair, guessed bytes, CRC-guided correction or inferred values', 'results':results}, indent=2))
