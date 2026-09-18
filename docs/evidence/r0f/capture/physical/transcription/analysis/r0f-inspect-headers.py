from pathlib import Path
from PIL import Image,ImageDraw
import json
root=Path('/Users/slice/Documents/ChatGPT/F65 Megawing/docs/evidence/r0f/capture/physical')
records={int(Path(r['path']).name.split('-')[0]):r for r in map(json.loads,(root/'ocr-unvalidated.jsonl').read_text().splitlines())}
sheet=Image.new('RGB',(1200,160*6),'white');draw=ImageDraw.Draw(sheet)
for i,n in enumerate([4,5,10,11,22,23]):
    im=Image.open(root/'photos'/f'{n}-Photo-{n}.jpg')
    lines=records[n]['lines']; b=next(b for b in lines if 'PAGECRC' in b['text'])
    y=int((1-b['y']-b['h'])*1280)
    crop=im.crop((180,y-4,800,y+30)).resize((1200,100))
    sheet.paste(crop,(0,i*160+30)); draw.text((10,i*160+10),f'Photo {n}',fill='black')
sheet.save('/tmp/r0f-headers.png')
