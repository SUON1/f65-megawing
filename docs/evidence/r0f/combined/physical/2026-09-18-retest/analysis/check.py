import json,zlib,struct
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps,ImageDraw
T=Path('/tmp/r0f-retest.04pg2B')
rows=[];headers=[]
for n in range(4,18):
    r=(T/f'{n:02}-rows.txt').read_text().splitlines();rows+=r
    im=ImageOps.exif_transpose(Image.open(T/f'{n:02}.png')).convert('RGB');im.thumbnail((1600,2400))
    co=np.array(json.loads((T/f'{n:02}-coords.json').read_text()))/2;yc=co[:,:,[1,3]].mean(axis=(1,2));p=np.median(np.diff(yc))
    box=(int(co[0,0,0])-5,int(yc[0]-2.7*p),int(co[0,-1,2])+5,int(yc[0]-1.3*p))
    crop=im.crop(box);canvas=Image.new('RGB',(1200,70),'black');canvas.paste(crop,(60,0));ImageDraw.Draw(canvas).text((0,15),f'{n:02}',fill='white');headers.append(canvas)
stream=bytes.fromhex(''.join(rows))[:7072]
print('Result CRC',f'{zlib.crc32(stream[:1788]):08X}','embedded',stream[1788:1792].hex(),'expected 32B8A599')
print('Raw CRC',f'{zlib.crc32(stream[1792:]):08X}','embedded',stream[72:76].hex(),'expected 105995A3')
print('Input edges',struct.unpack_from('<I',stream,88)[0],'consumed',struct.unpack_from('<I',stream,1668)[0])
canvas=Image.new('RGB',(1200,70*len(headers)))
for i,im in enumerate(headers):canvas.paste(im,(0,i*70))
canvas.save(T/'headers.png')
(T/'unvalidated.bin').write_bytes(stream)
