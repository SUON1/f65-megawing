import sys
import numpy as np
from PIL import Image,ImageDraw
from pathlib import Path
root=Path('/tmp/r0f-glyphs')
photos=Path('/Users/slice/Documents/ChatGPT/F65 Megawing/docs/evidence/r0f/capture/physical/photos')
for n in map(int,sys.argv[1:]):
    scores=np.load(root/f'{n}-scores.npy')
    coords=np.load(root/f'{n}-coords.npy')
    order=scores.argsort(axis=2)
    margin=np.sort(scores,axis=2)[:,:,-1]-np.sort(scores,axis=2)[:,:,-2]
    candidates=sorted((margin[r,c],r,c) for r in range(16) for c in range(5,69))[:40]
    im=Image.open(photos/f'{n}-Photo-{n}.jpg')
    sheet=Image.new('RGB',(1000,800),'white');draw=ImageDraw.Draw(sheet)
    for i,(m,r,c) in enumerate(candidates):
        xa,ya,xb,yb=coords[r,c];x=(i%10)*100;y=(i//10)*200
        patch=im.crop((xa-2,ya-2,xb+3,yb+3));patch=patch.resize((80,130),Image.Resampling.NEAREST)
        sheet.paste(patch,(x,y+25))
        pred=''.join('0123456789ABCDEF'[v] for v in order[r,c][-3:][::-1])
        draw.text((x,y),f'{r:02}:{c:02} {pred}',fill='black')
        draw.text((x,y+160),f'm={m:.3f}',fill='black')
    sheet.save(root/f'{n}-uncertain.png')
