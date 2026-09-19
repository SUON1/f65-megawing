"""Image-only nearest-glyph classifier, trained on printed address labels."""
import numpy as np,os
from pathlib import Path
from PIL import Image,ImageDraw
OUT=Path(os.environ.get('R0F_GLYPH_OUT','/tmp/r0f-glyphs'))
alphabet='0123456789ABCDEF'
pages={n:np.load(OUT/f'{n}-cells.npy') for n in range(2,24)}
train=[]; labels=[]; sources=[]
for n,cells in pages.items():
    for row in range(16):
        address=f'{(n-2)*512+row*32:04X}'
        for col,char in enumerate(address):
            train.append(cells[row,col]);labels.append(alphabet.index(char));sources.append(n)
train=np.array(train).reshape(-1,240).astype(np.float32)
labels=np.array(labels);sources=np.array(sources)
train-=train.mean(axis=1,keepdims=True)
train/=np.maximum(np.linalg.norm(train,axis=1,keepdims=True),1e-6)
similar=train@train.T
similar[sources[:,None]==sources[None,:]]=-2
cvclasses=np.stack([similar[:,labels==v].max(axis=1) for v in range(16)],axis=1)
clean=(cvclasses.argmax(axis=1)==labels)&((np.sort(cvclasses,axis=1)[:,-1]-np.sort(cvclasses,axis=1)[:,-2])>.04)
print('Clean independent-address examples',int(clean.sum()),'of',len(clean))
train=train[clean];labels=labels[clean];sources=sources[clean]
for n,cells in pages.items():
    test=cells.reshape(-1,240).astype(np.float32)
    test-=test.mean(axis=1,keepdims=True)
    test/=np.maximum(np.linalg.norm(test,axis=1,keepdims=True),1e-6)
    distances=test@train.T
    # Exclude same photo when reporting address-label accuracy.
    classes=np.stack([np.sort(distances[:,labels==v],axis=1)[:,-3:].mean(axis=1) for v in range(16)],axis=1)
    choices=np.argmax(classes,axis=1).reshape(16,69)
    margin=np.sort(classes,axis=1)[:,-1]-np.sort(classes,axis=1)[:,-2]
    texts=[''.join(alphabet[c] for c in row[:4])+':'+''.join(alphabet[c] for c in row[5:]) for row in choices]
    (OUT/f'{n}-rows.txt').write_text('\n'.join(texts)+'\n')
    np.save(OUT/f'{n}-scores.npy',classes.reshape(16,69,16))
    foreign=np.stack([distances[:,(labels==v)&(sources!=n)].max(axis=1) for v in range(16)],axis=1).argmax(axis=1).reshape(16,69)
    wrong=[(r,c,alphabet[foreign[r,c]],f'{(n-2)*512+r*32:04X}'[c]) for r in range(16) for c in range(4) if alphabet[foreign[r,c]]!=f'{(n-2)*512+r*32:04X}'[c]]
    print(n,'address CV errors',len(wrong),wrong[:10],'min margin',margin.min())
