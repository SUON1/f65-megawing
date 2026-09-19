import numpy as np,json
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
T=Path('/tmp/r0f-corrected.3qt691');S=Path('/tmp/r0f-retest.04pg2B');alpha='0123456789ABCDEF'
items=[]
for n in range(4,18):
 sc=np.load(T/f'{n:02}-scores.npy');order=sc.argsort(axis=2);margin=np.sort(sc,axis=2)[:,:,-1]-np.sort(sc,axis=2)[:,:,-2]
 for r in range(16):
  for c in range(64):
   if (n-4)*512+r*32<1792:continue
   if n==12 and r==4:continue
   items.append((float(margin[r,c]),n,r,c,alpha[order[r,c,-1]],alpha[order[r,c,-2]]))
items.sort();items=items[:80]
out=Image.new('RGB',(10*125,8*130),'#111111');d=ImageDraw.Draw(out)
cache={}
for idx,(m,n,r,c,best,other) in enumerate(items):
 if n not in cache:
  im=ImageOps.exif_transpose(Image.open(S/f'{n:02}.png')).convert('RGB');im.thumbnail((3200,4800));cache[n]=im
 box=json.loads((T/f'{n:02}-coords.json').read_text())[r][c];box=tuple(map(int,box));crop=cache[n].crop(box);crop.thumbnail((80,90))
 x=(idx%10)*125;y=(idx//10)*130;out.paste(crop,(x+20,y+30));d.text((x,y),f'{n}/{r}/{c} {best}:{other}',fill='white');d.text((x,y+14),f'{m:.3f}',fill='white')
out.save(T/'uncertain-raw.png');(T/'uncertain-raw.json').write_text(json.dumps(items,indent=2)+'\n')
n=12;r=4;co=np.array(json.loads((T/f'{n:02}-coords.json').read_text()))[r]
im=cache[n];box=(int(co[:,0].min())-20,int(co[:,1].min())-10,int(co[:,2].max())+20,int(co[:,3].max())+10)
im.crop(box).save(T/'photo12-row4.png')
