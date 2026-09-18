from pathlib import Path
import json,hashlib,shutil,subprocess,zlib
T=Path('/tmp/r0f-retest.04pg2B')
R=Path('/Users/slice/Documents/ChatGPT/F65 Megawing')
O=R/'docs/evidence/r0f/combined/physical/2026-09-18-retest'
A=O/'analysis';A.mkdir(exist_ok=True)
for name in ['intake.py','segment.py','classify.py','seeds.py','check.py','retain.py','headers.png','training-rows.json','manual-training.json']:
    shutil.copyfile(T/name,A/name)
paths=[]
for n in range(4,18):
    shutil.copyfile(T/f'{n:02}-rows.txt',A/f'photo-{n:02}-unvalidated.txt')
    page=n-3;amount=416 if page==14 else 512
    path=A/f'page-{page:02X}-unvalidated.txt'
    path.write_text(f'{page:02X} {(page-1)*512:04X} {amount:04X} 32B8A599 105995A3\n'+(T/f'{n:02}-rows.txt').read_text())
    paths.append(path)
java='/Users/slice/Documents/Codex/f65-megawing/toolchain/runtime/jdk-full/jdk-21.0.12+8/Contents/Home/bin/java'
cmd=[java,'-cp',str(R/'build/r0f/combined/classes'),'f65.tools.R0FCombinedOracle','--pages',*map(str,paths)]
p=subprocess.run(cmd,capture_output=True,text=True)
(A/'oracle.txt').write_text(p.stdout+p.stderr)
assert p.returncode!=0,'Unexpected pass: review before promotion'
raw=bytes.fromhex(''.join((T/f'{n:02}-rows.txt').read_text().replace('\n','') for n in range(4,18)))[:7072]
checks={'status':'NOT_VERIFIED_TRANSCRIPTION_ERRORS','result_crc_displayed':'32B8A599','duration_crc_displayed':'105995A3',
        'unvalidated_result_crc_calculated':f'{zlib.crc32(raw[:1788]):08X}',
        'unvalidated_duration_crc_calculated':f'{zlib.crc32(raw[1792:]):08X}',
        'java_command':cmd,'java_exit':p.returncode,'originals_byte_hash_check':'PASS','header_coverage':'01-0E visually confirmed',
        'no_crc_guided_corrections':True,'no_model_bytes_substituted':True}
for item in json.loads((O/'originals.json').read_text()):
    src=Path(item['source']).read_bytes();dest=(O/item['retained']).read_bytes()
    assert src==dest and hashlib.sha256(dest).hexdigest()==item['sha256']
for f in O.glob('*.json'):json.loads(f.read_text())
(A/'validation.json').write_text(json.dumps(checks,indent=2)+'\n')
files=sorted(p for p in O.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
(O/'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(O)}\n' for p in files))
print(json.dumps({k:v for k,v in checks.items() if k!='java_command'},indent=2))
print(p.stdout+p.stderr)
print('Retained',len(files),'hashed files')
