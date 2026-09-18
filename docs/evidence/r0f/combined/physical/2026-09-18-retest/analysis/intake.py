import pathlib, subprocess, json, hashlib, shutil
root=pathlib.Path('/Users/slice/Documents/ChatGPT/F65 Megawing')
out=root/'docs/evidence/r0f/combined/physical/2026-09-18-retest'
tmp=pathlib.Path('/tmp/r0f-retest.04pg2B')
ids='''1FCCB83F-F154-4D4D-AF46-DEAAC768A429
FC1434EF-0983-4F63-A1A6-2DBBEED40B85
182286BA-B631-4332-843B-CBB28F81A753
D85664BA-13BC-4685-A670-77A029895E24
941FFCE7-2635-41FB-B90A-9CAEBC45D565
446A68EB-4005-4D60-9772-B4C2353660BE
7916F0A1-76F2-40DB-810C-447774C68439
8A72C7D2-47A6-4AB0-981E-FFFF7907D569
34412F4A-13E7-48A4-9EB4-B83960F49799
09939797-E709-48EB-999D-80B1437B5271
0FF3797A-E320-4D19-B0AE-57270A061584
B0AF8A96-6232-4845-A889-32E6A5E0964C
407CDE0F-20B1-4921-9A5E-134E7265A6F7
EA124D96-9EDA-4A37-B5CA-0A1C5CA4DD6D
3DDC0788-6DDE-4EF1-92B9-89D7F04C42EF
9FA90132-85E2-4C40-8EA1-26F99CDD2E79
CE91AF43-95AC-4A83-8BEA-9AFADF509478'''.splitlines()
(out/'originals').mkdir(parents=True,exist_ok=True)
manifest=[]
for i,id in enumerate(ids,1):
    src=pathlib.Path('/Users/slice/Pictures/Photos Library.photoslibrary/originals')/id[0]/(id+'.heic')
    dest=out/'originals'/src.name
    if not dest.exists():shutil.copyfile(src,dest)
    digest=hashlib.sha256(src.read_bytes()).hexdigest()
    assert hashlib.sha256(dest.read_bytes()).hexdigest()==digest
    png=tmp/f'{i:02}.png'
    if not png.exists():subprocess.run(['sips','-s','format','png',str(src),'--out',str(png)],check=True,capture_output=True)
    ocr=out/f'ocr-{i:02}.json'
    if not ocr.exists():
        r=subprocess.run(['swift','-module-cache-path',str(tmp/'module-cache'),str(root/'docs/evidence/r0f/capture/physical/r0f-photo-ocr.swift'),str(png)],check=True,capture_output=True,text=True)
        data=json.loads(r.stdout);data['source_original']=str(src);ocr.write_text(json.dumps(data,indent=2)+'\n')
    manifest.append({'index':i,'source':str(src),'retained':str(dest.relative_to(out)),'sha256':digest})
    print(i,id,flush=True)
(out/'originals.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Originals copied byte-for-byte; decoded previews and unvalidated OCR complete',flush=True)
