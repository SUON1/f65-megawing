"""Assemble reviewed photographic transcripts; do not modify the Java importer."""
from pathlib import Path
import json,zlib

dest=Path('/Users/slice/Documents/ChatGPT/F65 Megawing/docs/evidence/r0f/capture/physical/transcription')
dest.mkdir(exist_ok=True)
raw=Path('/tmp/r0f-glyphs-reviewed')
crcs=['1947E857','7ED96198','F76254EE','29F01800','8EFCD67E','6076FED9','1120103D','603A6B13','D86B6DCC','65802B88','22DD7E39','0A2873D3','2E61532C','1BECED22','AD3287BF','8ADA5789','ED9D3432','05A27ED7','726262F9','DFDD7431','CEC53C4A','0D39992D']
address_corrections=[];data=bytearray();pages=[]
for page,expected_crc in enumerate(crcs,1):
    n=page+1;start=(page-1)*512;length=min(512,11136-start)
    rows=(raw/f'{n}-rows.txt').read_text().splitlines()
    assert len(rows)==16 and all(len(r)==69 for r in rows)
    payload=b''.join(bytes.fromhex(r[5:]) for r in rows)
    assert not any(payload[length:])
    assert f'{zlib.crc32(payload[:length]):08X}'==expected_crc
    data.extend(payload[:length])
    # Printed offset labels checked visually against the ordered photo rows.
    # This changes presentation labels only, never decoded measurement bytes.
    for r in range(16):
        address=f'{start+r*32:04X}'
        if rows[r][:4]!=address:
            address_corrections.append(dict(photo=n,row=r,ocr=rows[r][:4],observed=address))
        rows[r]=address+rows[r][4:]
    lines=['R0-F RAW CAPTURE - F65R0F5',
           f'PAGE {page:04X} OF 0016 OFFSET {start:04X} BYTES {length:04X}',
           f'TOTAL 2B80 CRC32 8D78FBC0 PAGECRC {expected_crc}',
           'FIELDS ARE HEX; PAGE COUNT 0016 MEANS 22 PAGES.',*rows,
           'RAW CIA COUNTS ONLY - NO CALIBRATED TIME OR R0-F ACCEPTANCE',
           'ACQUISITION COMPLETE / INHERITED FUNCTIONAL FIXTURE PASS','',
           'N/SPACE NEXT   P PREVIOUS   S SUMMARY   C CAPTURE',
           'NO DISK WRITES. TIMERS STOPPED. RESET REQUIRED AFTER TEST.']
    assert len(lines)==25
    with (dest/f'page-{page:04X}.txt').open('x') as f:f.write('\n'.join(lines)+'\n')
    pages.append(dict(photo=f'{n}-Photo-{n}.jpg',pageHex=f'{page:04X}',offsetHex=f'{start:04X}',bytes=length,displayedCrc32=expected_crc,calculatedCrc32=f'{zlib.crc32(payload[:length]):08X}'))
assert len(data)==11136 and zlib.crc32(data)==0x8d78fbc0
manifest=dict(status='ALL_PAGE_AND_STREAM_CRCS_PASS_AWAITING_JAVA',streamBytes=len(data),streamCrc32='8D78FBC0',pages=pages,addressLabelCorrections=address_corrections,notes='Payload from photographic glyph classification plus explicitly reviewed manual corrections. Static display text reconstructed from observed fixed layout. Offset labels visually checked; no payload bytes inferred from address labels or expected fixture values.')
with (dest/'transcription-manifest.json').open('x') as f:json.dump(manifest,f,indent=2);f.write('\n')
print('PASS: 22 exact page CRCs and full CRC 8D78FBC0; strict 25-line transcripts assembled')
