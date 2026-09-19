"""Image-only segmentation; no expected data or checksum inputs."""
import json,re,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps
TMP=Path('/tmp/r0f-retest.04pg2B')
OUT=Path('/Users/slice/Documents/ChatGPT/F65 Megawing/docs/evidence/r0f/combined/physical/2026-09-18-retest')
def segment(n):
    im=ImageOps.exif_transpose(Image.open(TMP/f'{n:02}.png')).convert('RGB')
    im.thumbnail((3200,4800));a=np.asarray(im)[:,:,1].astype(float);h,w=a.shape
    bs=json.loads((OUT/f'ocr-{n:02}.json').read_text())['lines']
    data=[b for b in bs if len(re.sub('[^0-9A-F]','',b['text']))>45]
    data.sort(key=lambda b:-(b['y']+b['h']/2))
    top=(1-data[0]['y']-data[0]['h']/2)*h
    # Lowest detected row, allowing OCR fragments.
    bottom=max((1-b['y']-b['h']/2)*h for b in bs)
    pitch=(bottom-top)/15
    left=np.median([b['x'] for b in data])*w
    right=np.median([b['x']+b['w'] for b in data])*w
    xx=np.arange(int(left-12),int(right+12));knots=np.linspace(left+40,right-40,23)
    cells=[];coords=[];strips=[]
    for row in range(16):
        guess=top+row*pitch
        curves=[]
        for boundary in (guess-pitch/2,guess+pitch/2):
            vals=[]
            for x in knots:
                lo=int(boundary-pitch*.4);hi=int(boundary+pitch*.4)
                p=a[lo:hi,int(x-36):int(x+37)].mean(axis=1)
                p=np.convolve(p,np.ones(5)/5,'same')
                vals.append(lo+4+np.argmin(p[4:-4]))
            vals=np.array(vals);fit=np.polyfit(knots-left,vals,2)
            good=np.abs(np.polyval(fit,knots-left)-vals)<pitch*.15
            if good.sum()>8:fit=np.polyfit(knots[good]-left,vals[good],2)
            curves.append(np.polyval(fit,xx-left))
        yy=curves[0][None,:]+np.linspace(0,1,80)[:,None]*(curves[1]-curves[0])[None,:]
        yi=np.floor(yy).astype(int);f=yy-yi
        strip=(1-f)*a[yi,xx]+f*a[yi+1,xx];p=strip.mean(axis=0)
        p-=np.percentile(p,10);inds=np.flatnonzero(p>p.max()*.25)
        xs=xx[inds[0]]-4;xe=xx[inds[-1]]+4
        gx=np.linspace(xs,xe,65);ci=np.arange(65)
        cand=[]
        for curve in np.linspace(-20,20,81):
            trial=gx+curve*ci*(64-ci)/(64*64/4)
            cand.append((np.interp(trial,xx,p).mean(),trial))
        gx=min(cand,key=lambda t:t[0])[1]
        gaps=[]
        for g in gx:
            lo=max(0,int(g)-4-xx[0]);hi=min(len(p),int(g)+5-xx[0]);gaps.append(xx[0]+lo+np.argmin(p[lo:hi]))
        rowcells=[];rowcoords=[]
        for xa,xb in zip(gaps,gaps[1:]):
            cell=strip[:,xa-xx[0]:xb-xx[0]+1].copy();cell-=np.percentile(cell,10);cell=np.clip(cell/max(cell.max(),1),0,1)
            ys,zs=np.where(cell>.25)
            if len(ys):cell=cell[ys.min():ys.max()+1,zs.min():zs.max()+1]
            glyph=np.asarray(Image.fromarray((255*cell).astype('uint8')).resize((16,28),Image.Resampling.BILINEAR))/255
            rowcells.append(glyph);rowcoords.append([int(xa),float(np.interp(xa,xx,curves[0])),int(xb),float(np.interp(xb,xx,curves[1]))])
        cells.append(rowcells);coords.append(rowcoords);strips.append(strip)
    np.save(TMP/f'{n:02}-cells.npy',cells)
    (TMP/f'{n:02}-coords.json').write_text(json.dumps(coords))
    Image.fromarray((np.block(cells)*255).astype('uint8')).save(TMP/f'{n:02}-cells.png')
    print(n,round(top,1),round(bottom,1),round(pitch,1),round(left,1),round(right,1),flush=True)
for n in map(int,sys.argv[1:] or range(4,18)):segment(n)
