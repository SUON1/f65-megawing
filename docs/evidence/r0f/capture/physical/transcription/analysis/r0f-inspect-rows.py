from PIL import Image,ImageDraw
from pathlib import Path
root=Path('/Users/slice/Documents/ChatGPT/F65 Megawing/docs/evidence/r0f/capture/physical/photos')
sheet=Image.new('RGB',(1600,450),'white');d=ImageDraw.Draw(sheet)
for i,(n,box) in enumerate([(5,(185,432,755,469)),(22,(195,365,760,393))]):
    im=Image.open(root/f'{n}-Photo-{n}.jpg').crop(box).resize((1600,135),Image.Resampling.NEAREST)
    sheet.paste(im,(0,i*220+30));d.text((0,i*220),f'Photo {n}: original pixels, not OCR',fill='black')
sheet.save('/tmp/r0f-rows-review.png')
