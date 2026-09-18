"""Local photo analysis. Original images remain unchanged; CRCs never guide OCR."""
import json, sys, os
from pathlib import Path
import numpy as np
from PIL import Image

ROOT=Path('/Users/slice/Documents/ChatGPT/F65 Megawing/docs/evidence/r0f/capture/physical')
OUT=Path(os.environ.get('R0F_GLYPH_OUT','/tmp/r0f-glyphs'))
OUT.mkdir(exist_ok=True)
records={int(Path(r['path']).name.split('-')[0]):r for r in map(json.loads,(ROOT/'ocr-unvalidated.jsonl').read_text().splitlines())}

def data_boxes(n):
    # OCR only locates the text; none of its recognized payload is trusted.
    r=records[n]
    boxes=[b for b in r['lines'] if ':' in b['text'][:7] and b['w']>.45]
    boxes.sort(key=lambda b:-b['y'])
    return boxes

def warp(n):
    a=np.array(Image.open(ROOT/'photos'/f'{n}-Photo-{n}.jpg'))[:,:,1].astype(float)
    h,w=a.shape
    boxes=records[n]['lines']
    hdr=next((b for b in boxes if 'FIELDS' in b['text']),None)
    foot=next(b for b in boxes if 'ONLY' in b['text'] or 'COUNTS' in b['text'])
    left=int(min(b['x'] for b in boxes[:6])*w)
    top=int((1-hdr['y'])*h) if hdr else 355
    bottom=int((1-foot['y']-foot['h'])*h)
    # Keep analysis overlays separate from immutable originals.
    im=Image.open(ROOT/'photos'/f'{n}-Photo-{n}.jpg')
    from PIL import ImageDraw
    d=ImageDraw.Draw(im)
    d.rectangle((left,top,left+550,bottom),outline='red',width=1)
    proj=np.mean(a[top:bottom,left+50:left+500],axis=1)
    smooth=np.convolve(proj,np.ones(5)/5,'same')
    minima=[i for i in range(3,len(proj)-3) if smooth[i]==min(smooth[i-3:i+4])]
    boundaries=[m+top for m in minima]
    if len(boundaries)!=15:
        print('BAD ROWS',n,left,top,bottom,boundaries)
        return None
    boundaries=[2*boundaries[0]-boundaries[1]]+boundaries+[2*boundaries[-1]-boundaries[-2]]
    cells=[]; coordinates=[]
    for row,(ya,yb) in enumerate(zip(boundaries,boundaries[1:])):
        xbase=left-5
        # Estimate inter-line valleys over wider strips, not inside one glyph.
        knots=np.arange(xbase,left+571,25)
        ys=[]
        for boundary in (ya,yb):
            vals=[]
            for x in knots:
                yp=a[boundary-7:boundary+8,max(left,x-20):min(left+570,x+21)].mean(axis=1)
                yp=np.convolve(yp,np.ones(3)/3,'same')
                vals.append(boundary-7+int(np.argmin(yp[2:-2]))+2)
            vals=np.array(vals)
            use=(knots>left+35)&(knots<left+490)
            fit=np.polyfit(knots[use]-left,vals[use],2)
            residual=abs(np.polyval(fit,knots-left)-vals)
            use=use&(residual<2)
            fit=np.polyfit(knots[use]-left,vals[use],2)
            ys.append(np.polyval(fit,knots-left) if os.environ.get('R0F_GLYPH_SMOOTH')=='1' else vals)
        xx=np.arange(xbase,left+570)
        ytop=np.interp(xx,knots,ys[0]);ybottom=np.interp(xx,knots,ys[1])
        yy=ytop[None,:]+np.linspace(0,1,24)[:,None]*(ybottom-ytop)[None,:]
        yfloor=np.floor(yy).astype(int); frac=yy-yfloor
        strip=(1-frac)*a[yfloor,xx]+frac*a[yfloor+1,xx]
        p=strip.mean(axis=0)
        p=p-np.percentile(p,10)
        inds=np.flatnonzero(p>max(p)*.3)
        xstart=inds[0]+xbase-1
        xend=inds[-1]+xbase+1
        # Find inter-character valleys from the pitch estimate; no payload values.
        gx=np.linspace(xstart,xend,70)
        ci=np.arange(70)
        # Correct nonlinear horizontal pitch from camera/screen geometry.
        candidates=[]
        for curve in np.linspace(-8,8,65):
            trial=gx+curve*ci*(69-ci)/(69*69/4)
            loss=np.interp(trial-xbase,np.arange(len(p)),p).mean()
            candidates.append((loss,trial))
        gx=min(candidates,key=lambda v:v[0])[1]
        gaps=[]
        for guess in gx:
            lo=max(0,int(guess)-1-xbase); hi=min(len(p),int(guess)+3-xbase)
            gaps.append(np.argmin(p[lo:hi])+lo+xbase)
        rowcells=[]; rowcoords=[]
        for col,(xa,xb) in enumerate(zip(gaps,gaps[1:])):
            # Local row boundary search handles photographed line tilt.
            y0=int(np.interp(xa,xx,ytop));y1=int(np.interp(xa,xx,ybottom))
            cell=strip[:,xa-xbase:xb-xbase+1]
            cell=cell-np.percentile(cell,10)
            peak=cell.max()
            cell=np.clip(cell/max(peak,1),0,1)
            ys,xs=np.where(cell>.32)
            if not len(xs): raise ValueError((n,row,col))
            cell=cell[ys.min():ys.max()+1,xs.min():xs.max()+1]
            glyph=np.array(Image.fromarray((cell*255).astype('uint8')).resize((12,20),Image.Resampling.BILINEAR))/255
            rowcells.append(glyph)
            rowcoords.append([xa,y0,xb,y1])
            if col<4:d.rectangle((xa,y0,xb,y1),outline='red',width=1)
        cells.append(rowcells)
        coordinates.append(rowcoords)
    im.save(OUT/f'{n}-roi.png')
    montage=np.block([[c for c in row] for row in cells])
    Image.fromarray((montage*255).astype('uint8')).save(OUT/f'{n}-cells.png')
    np.save(OUT/f'{n}-cells.npy',cells)
    np.save(OUT/f'{n}-coords.npy',coordinates)
    print(n,'cells extracted')
    return np.array(cells)

if __name__=='__main__':
    for n in map(int,sys.argv[1:] or range(2,24)):warp(n)
