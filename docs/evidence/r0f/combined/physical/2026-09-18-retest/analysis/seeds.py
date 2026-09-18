from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
T=Path('/tmp/r0f-retest.04pg2B')
# Transcribed from enlarged original photos; no expected target values used.
seeds=[(4,0,'52434631017F00028760023502002B3500527A9600527A96D8607D3CD8607D3C'),
 (17,0,'8611F710F6100F11F410F5108911F3105D11F710FD105C11F81083115E11F510'),
 (17,1,'0B111311F610EC11F5105B11F41085115D111511FD10F410F510E111F3104B11'),
 (17,2,'F61081115E11F8100E11F410F6108A11F5105B11F610FC10F610F51084115A11'),
 (17,3,'F710851113111710EF11F510F410F71085115D111511FE10F310F510E111F210')]
alpha='0123456789ABCDEF';train=[];lab=[]
for n,r,s in seeds:
 assert len(s)==64
 train.extend(np.load(T/f'{n:02}-cells.npy')[r]);lab.extend(s)
train=np.array(train);lab=np.array(lab)
out=Image.new('L',(16*32,16*36))
for i,c in enumerate(alpha):
 a=train[lab==c]
 for j,g in enumerate(a[:16]):out.paste(Image.fromarray((255*g).astype('uint8')).resize((32,32)),(j*32,i*36))
ImageDraw.Draw(out).text((0,0),'',fill=255);out.save(T/'prototypes.png')
def norm(a):
 a=a.reshape(-1,448).astype('float32');a-=a.mean(axis=1,keepdims=True);return a/np.maximum(np.linalg.norm(a,axis=1,keepdims=True),1e-6)
tr=norm(train)
for n in range(4,18):
 d=norm(np.load(T/f'{n:02}-cells.npy'))@tr.T
 scores=np.stack([np.sort(d[:,lab==c],axis=1)[:,-min(3,sum(lab==c)):].mean(axis=1) for c in alpha],axis=1)
 # Nearest manually labelled glyph per class.
 scores=np.stack([d[:,lab==c].max(axis=1) for c in alpha],axis=1)
 choices=scores.argmax(axis=1).reshape(16,64)
 (T/f'{n:02}-rows.txt').write_text('\n'.join(''.join(alpha[c] for c in row) for row in choices)+'\n')
 np.save(T/f'{n:02}-scores.npy',scores.reshape(16,64,16))
 print(n,'low margin',sum((np.sort(scores,axis=1)[:,-1]-np.sort(scores,axis=1)[:,-2])<.04),flush=True)
(T/'manual-training.json').write_text(json.dumps(seeds,indent=2)+'\n')
