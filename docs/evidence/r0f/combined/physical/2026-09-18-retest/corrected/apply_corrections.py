import json,zlib
from pathlib import Path
T=Path('/tmp/r0f-corrected.3qt691');o=T/'transcripts';o.mkdir(exist_ok=True)
rows={n:[list(r) for r in (T/f'{n:02}-rows.txt').read_text().splitlines()] for n in range(4,18)}
fix=json.loads((T/'corrections.json').read_text())
for f in fix['rows']:
 assert len(f['text'])==64;rows[f['photo']][f['row']]=list(f['text'])
for f in fix['cells']:rows[f['photo']][f['row']][f['column']]=f['value']
stream=b''
for n,rs in rows.items():
 p=n-3;text='\n'.join(''.join(r) for r in rs)+'\n';stream+=bytes.fromhex(text)
 (o/f'page-{p:02X}.txt').write_text(f'{p:02X} {(p-1)*512:04X} {416 if p==14 else 512:04X} 32B8A599 105995A3\n'+text)
stream=stream[:7072];(o/'capture.bin').write_bytes(stream)
print('RESULT',f'{zlib.crc32(stream[:1788]):08X}','expected 32B8A599')
print('RAW',f'{zlib.crc32(stream[1792:]):08X}','expected 105995A3')
