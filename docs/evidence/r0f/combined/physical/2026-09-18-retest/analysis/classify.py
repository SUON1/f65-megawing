"""Image-only glyph recognition, no CRC-directed corrections or fixture bytes."""
from pathlib import Path
import json,re
import numpy as np
from PIL import Image,ImageOps
TMP=Path('/tmp/r0f-retest.04pg2B');OUT=Path('/Users/slice/Documents/ChatGPT/F65 Megawing/docs/evidence/r0f/combined/physical/2026-09-18-retest')
alpha='0123456789ABCDEF'
def norm(a):
    a=a.reshape(-1,448).astype('float32');a-=a.mean(axis=1,keepdims=True);return a/np.maximum(np.linalg.norm(a,axis=1,keepdims=True),1e-6)
cells={n:np.load(TMP/f'{n:02}-cells.npy') for n in range(4,18)}
train=[];labels=[];sources=[];records=[]
for n,cs in cells.items():
    coords=np.array(json.loads((TMP/f'{n:02}-coords.json').read_text()))
    centers=coords[:,:,[1,3]].mean(axis=(1,2));pitch=np.median(np.diff(centers))
    im=ImageOps.exif_transpose(Image.open(TMP/f'{n:02}.png'));h=round(im.height*3200/im.width)
    boxes=json.loads((OUT/f'ocr-{n:02}.json').read_text())['lines']
    for b in boxes:
        text=b['text'].replace(' ','').upper()
        if not re.fullmatch('[0-9A-F]{64}',text):continue
        y=(1-b['y']-b['h']/2)*h;r=int(np.argmin(abs(centers-y)))
        if abs(centers[r]-y)>pitch*.3:continue
        train.extend(cs[r]);labels.extend(alpha.index(c) for c in text);sources.extend([n]*64)
        records.append({'photo':n,'row':r,'text':text})
train=norm(np.array(train));labels=np.array(labels);sources=np.array(sources)
print('Training',len(train),{c:int((labels==i).sum()) for i,c in enumerate(alpha)},flush=True)
def classify(test,train,labels,source=None,sources=None):
    outputs=[]
    for start in range(0,len(test),512):
        d=test[start:start+512]@train.T
        if source is not None:d[:,sources==source]=-2
        scores=np.stack([d[:,labels==v].max(axis=1) for v in range(16)],axis=1)
        outputs.append(scores)
    return np.concatenate(outputs)
keep=np.zeros(len(train),bool)
for n in range(4,18):
    ix=sources==n
    if not ix.any():continue
    scores=classify(train[ix],train,labels,n,sources)
    keep[ix]=(scores.argmax(axis=1)==labels[ix])&(np.sort(scores,axis=1)[:,-1]-np.sort(scores,axis=1)[:,-2]>.035)
print('Clean',int(keep.sum()),{c:int(((labels==i)&keep).sum()) for i,c in enumerate(alpha)},flush=True)
can=Image.new('L',(512,16*32))
for i in range(16):
    v=train[keep&(labels==i)]
    for j,g in enumerate(v[:16]):
        g=g.reshape(28,16);g=(g-g.min())/max(float(g.max()-g.min()),1e-9)
        can.paste(Image.fromarray((g*255).astype('uint8')).resize((32,32)),(j*32,i*32))
can.save(TMP/'clean-prototypes.png')
(TMP/'training-rows.json').write_text(json.dumps(records,indent=2)+'\n')
for n,cs in cells.items():
    scores=classify(norm(cs),train[keep],labels[keep]);choices=scores.argmax(axis=1).reshape(16,64)
    margins=(np.sort(scores,axis=1)[:,-1]-np.sort(scores,axis=1)[:,-2]).reshape(16,64)
    rows=[''.join(alpha[c] for c in row) for row in choices]
    (TMP/f'{n:02}-rows.txt').write_text('\n'.join(rows)+'\n');np.save(TMP/f'{n:02}-scores.npy',scores.reshape(16,64,16))
    print(n,'uncertain <.04',int((margins<.04).sum()),'min',round(margins.min(),3),flush=True)
