import numpy as np,json,zlib
from pathlib import Path
T=Path('/tmp/r0f-corrected.3qt691');alpha='0123456789ABCDEF'
seeds=json.loads((T/'manual-training.json').read_text())[:2];train=[];lab=[]
for n,r,s in seeds:train.extend(np.load(T/f'{n:02}-cells.npy')[r]);lab.extend(s)
def norm(a):
 a=a.reshape(-1,448).astype('float32');a-=a.mean(axis=1,keepdims=True);return a/np.maximum(np.linalg.norm(a,axis=1,keepdims=True),1e-6)
train=norm(np.array(train));lab=np.array(lab)
for n in range(4,18):
 x=norm(np.load(T/f'{n:02}-cells.npy'));d=x@train.T
 scores=np.stack([d[:,lab==c].max(axis=1) for c in alpha],axis=1)
 rows=[''.join(alpha[i] for i in r) for r in scores.argmax(axis=1).reshape(16,64)]
 (T/f'{n:02}-rows.txt').write_text('\n'.join(rows)+'\n');np.save(T/f'{n:02}-scores.npy',scores.reshape(16,64,16))
stream=bytes.fromhex(''.join((T/f'{n:02}-rows.txt').read_text().replace('\n','') for n in range(4,18)))[:7072]
print('CRC',f'{zlib.crc32(stream[:1788]):08X}',f'{zlib.crc32(stream[1792:]):08X}')
print((T/'04-rows.txt').read_text()[:520])
