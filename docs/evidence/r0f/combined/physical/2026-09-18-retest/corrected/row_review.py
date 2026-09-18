import json,numpy as np
from pathlib import Path
from PIL import Image,ImageOps
T=Path('/tmp/r0f-corrected.3qt691');S=Path('/tmp/r0f-retest.04pg2B')
n=15;r=15;co=np.array(json.loads((T/f'{n:02}-coords.json').read_text()))[r]
im=ImageOps.exif_transpose(Image.open(S/f'{n:02}.png')).convert('RGB');im.thumbnail((3200,4800))
box=(int(co[:,0].min())-20,int(co[:,1].min())-85,int(co[:,2].max())+20,int(co[:,3].max())+45)
im.crop(box).save(T/'photo15-lastrows.png')
