"""Photographic grid extraction. No payload expectations or checksums used."""
import json,re,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps
SRC=Path('/tmp/r0f-retest.04pg2B');OUT=Path('/tmp/r0f-corrected.3qt691')
EVID=Path('/Users/slice/Documents/ChatGPT/F65 Megawing/docs/evidence/r0f/combined/physical/2026-09-18-retest')
def segment(n):
 im=ImageOps.exif_transpose(Image.open(SRC/f'{n:02}.png')).convert('RGB');im.thumbnail((3200,4800));a=np.asarray(im)[:,:,1].astype(float);h,w=a.shape
 bs=json.loads((EVID/f'ocr-{n:02}.json').read_text())['lines'];data=[b for b in bs if len(re.sub('[^0-9A-F]','',b['text']))>45];data.sort(key=lambda b:-(b['y']+b['h']/2))
 top=(1-data[0]['y']-data[0]['h']/2)*h;bottom=max((1-b['y']-b['h']/2)*h for b in bs)
 left=np.median([b['x'] for b in data])*w;right=np.median([b['x']+b['w'] for b in data])*w
 guess=(bottom-top)/15;xc=int((left+right)/2);lo=int(top-guess);hi=int(bottom+guess)
 p=a[lo:hi,xc-100:xc+100].mean(axis=1);p=np.convolve(p,np.ones(7)/7,'same')
 lags=np.arange(int(guess*.87),int(guess*1.1));pitch=lags[np.argmax([np.corrcoef(p[:-k],p[k:])[0,1] for k in lags])]
 # Refine spacing from repeated inter-line valleys at the central column.
 boundaries=[]
 for k in range(17):
  g=top+(k-.5)*pitch;start=int(g-pitch*.23)-lo;end=int(g+pitch*.23)-lo
  ix=start+np.argmin(p[start:end]);boundaries.append(ix+lo)
 fit=np.polyfit(np.arange(17),boundaries,2);boundaries=np.polyval(fit,np.arange(17))
 xx=np.arange(int(left-30),int(right+30));knots=np.linspace(left+60,right-60,35)
 strips=[];curves_all=[]
 for row in range(16):
  curves=[]
  for g in boundaries[row:row+2]:
   vals=[]
   for x in knots:
    low=int(g-pitch*.43);high=int(g+pitch*.43)
    v=a[low:high,int(x-50):int(x+51)].mean(axis=1);v=np.convolve(v,np.ones(7)/7,'same')
    vals.append(low+4+np.argmin(v[4:-4]))
   vals=np.array(vals);f=np.polyfit(knots-left,vals,2)
   for _ in range(3):
    good=abs(np.polyval(f,knots-left)-vals)<pitch*.13
    if good.sum()>10:f=np.polyfit(knots[good]-left,vals[good],2)
   curves.append(np.polyval(f,xx-left))
  yy=curves[0][None,:]+np.linspace(0,1,80)[:,None]*(curves[1]-curves[0])[None,:];yi=np.floor(yy).astype(int);f=yy-yi
  strips.append((1-f)*a[yi,xx]+f*a[yi+1,xx]);curves_all.append(curves)
 # Fit one shared fixed-pitch column grid rather than crop to individual digits.
 pp=np.array([s.mean(axis=0) for s in strips]);pp-=np.percentile(pp,10,axis=1)[:,None]
 p=pp.mean(axis=0);mask=np.flatnonzero(p>p.max()*.23);xs=xx[mask[0]]-4;xe=xx[mask[-1]]+4
 ci=np.arange(65);curve=ci*(64-ci)/1024
 def grid(params):return np.linspace(xs+params[0],xe+params[1],65)+params[2]*curve
 def optimize(p,params,span):
  params=list(params)
  for _ in range(3):
   for j in range(3):
    trial=[]
    for delta in np.arange(-3 if j<2 else -8,4 if j<2 else 9,1):
     q=params.copy();q[j]=delta;gx=grid(q)
     trial.append((np.interp(gx[1:-1],xx,p).mean(),q))
    params=min(trial,key=lambda x:x[0])[1]
  return params
 pars=optimize(p,[0,0,0],12)
 cells=[];coords=[]
 for row,(strip,curves) in enumerate(zip(strips,curves_all)):
  # Small perspective drift per row, with shared-grid anchor preventing half-cell jumps.
  params=optimize(pp[row],pars,3);gx=grid(params);gaps=[]
  for g in gx:
   lo=max(0,int(g)-1-xx[0]);hi=min(len(p),int(g)+2-xx[0]);gaps.append(xx[0]+lo+np.argmin(pp[row,lo:hi]))
  def components(threshold):
   mask=pp[row]>threshold*pp[row].max()
   runs=[];start=None
   for j,v in enumerate(mask):
    if v and start is None:start=j
    if start is not None and (not v or j==len(mask)-1):
     end=j if not v else j+1
     if end-start>=3:runs.append([start,end])
     start=None
   merged=[]
   for x0,x1 in runs:
    if merged and x0-merged[-1][1]<=3:merged[-1][1]=x1
    else:merged.append([x0,x1])
   return merged
  candidates=[]
  for threshold in np.arange(.08,.401,.01):
   runs=components(threshold)
   if len(runs)==64:
    centers=np.array([(x0+x1)/2 for x0,x1 in runs]);q=np.polyfit(np.arange(64),centers,2)
    loss=np.mean((np.polyval(q,np.arange(64))-centers)**2)
    candidates.append((loss,threshold,runs))
  if candidates:
   _,threshold,runs=min(candidates,key=lambda v:v[0]);ranges=[(xx[0]+x0-1,xx[0]+x1) for x0,x1 in runs]
  else:
   print('NO COMPONENT GRID',n,row,[(round(t,2),len(components(t))) for t in [.1,.15,.2,.25,.3]],flush=True)
   ranges=list(zip(gaps,gaps[1:]))
  rowcells=[];rowcoords=[]
  for xa,xb in ranges:
   cell=strip[:,xa-xx[0]:xb-xx[0]+1].copy();cell-=np.percentile(cell,10);cell=np.clip(cell/max(cell.max(),1),0,1)
   ys,zs=np.where(cell>.3)
   if len(ys):cell=cell[ys.min():ys.max()+1,zs.min():zs.max()+1]
   glyph=np.asarray(Image.fromarray((cell*255).astype('uint8')).resize((16,28),Image.Resampling.BILINEAR))/255
   rowcells.append(glyph);rowcoords.append([int(xa),float(np.interp(xa,xx,curves[0])),int(xb),float(np.interp(xb,xx,curves[1]))])
  cells.append(rowcells);coords.append(rowcoords)
 np.save(OUT/f'{n:02}-cells.npy',cells);(OUT/f'{n:02}-coords.json').write_text(json.dumps(coords))
 Image.fromarray((np.block(cells)*255).astype('uint8')).save(OUT/f'{n:02}-cells.png')
 print(n,'pitch',pitch,'column',pars,flush=True)
for n in map(int,sys.argv[1:] or range(4,18)):segment(n)
