exec(open('/tmp/r0f-corrected.3qt691/uncertain.py').read().split('items=[]')[0])
items=[]
for n in range(7,18):
 sc=np.load(T/f'{n:02}-scores.npy')
 for r in range(16):
  if (n,r) in [(12,4),(15,15)]:continue
  for c in range(64):
   if (n-4)*512+r*32<1792:continue
   items.append((float(sc[r,c].max()),n,r,c,alpha[sc[r,c].argmax()]))
items.sort();items=items[:100]
out=Image.new('RGB',(1250,1300),'#111');d=ImageDraw.Draw(out);cache={}
for idx,(score,n,r,c,best) in enumerate(items):
 if n not in cache:
  im=ImageOps.exif_transpose(Image.open(S/f'{n:02}.png')).convert('RGB');im.thumbnail((3200,4800));cache[n]=im
 box=tuple(map(int,json.loads((T/f'{n:02}-coords.json').read_text())[r][c]));crop=cache[n].crop(box);crop.thumbnail((80,90))
 x=idx%10*125;y=idx//10*130;out.paste(crop,(x+20,y+30));d.text((x,y),f'{n}/{r}/{c} {best} {score:.3f}',fill='white')
out.save(T/'absolute-review.png')
