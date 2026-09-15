from pathlib import Path
import json,hashlib,sys
R=Path(__file__).resolve().parents[1]; D=R/'diagrams'; O=R/'qa'/'visual-render'; O.mkdir(exist_ok=True)
try:
 import cairosvg
 from PIL import Image,ImageOps,ImageDraw
except Exception as e:
 print(json.dumps({'status':'NOT_RUN','reason':repr(e)},indent=2)); sys.exit(2)
entries=[]; ims=[]
for svg in sorted(D.glob('*.svg')):
 txt=svg.read_text(encoding='utf-8')
 title=bool(__import__('re').search(r'<title\b',txt)) and '</title>' in txt; desc=bool(__import__('re').search(r'<desc\b',txt)) and '</desc>' in txt
 png=O/(svg.stem+'.png')
 cairosvg.svg2png(bytestring=svg.read_bytes(),write_to=str(png),output_width=900,background_color='white')
 im=Image.open(png).convert('RGB'); bbox=ImageOps.invert(im.convert('L')).getbbox(); nonblank=bbox is not None
 entries.append({'svg':svg.name,'sha256':hashlib.sha256(svg.read_bytes()).hexdigest(),'png':png.name,'width':im.width,'height':im.height,'has_title':title,'has_desc':desc,'nonblank':nonblank,'ink_bbox':bbox})
 # thumbnail with filename label
 thumb=im.copy(); thumb.thumbnail((430,300)); canvas=Image.new('RGB',(450,340),'white'); canvas.paste(thumb,((450-thumb.width)//2,20)); ImageDraw.Draw(canvas).text((10,318),svg.name,fill='black'); ims.append(canvas)
w=900; h=((len(ims)+1)//2)*340
sheet=Image.new('RGB',(w,h),'white')
for i,im in enumerate(ims): sheet.paste(im,((i%2)*450,(i//2)*340))
sheet.save(O/'contact-sheet.png')
fail=[e for e in entries if not(e['has_title'] and e['has_desc'] and e['nonblank'])]
manifest={'status':'PASS' if not fail else 'FAIL','renderer':'CairoSVG local raster at 900 px width; white background','inspection_scope':'renderability/nonblank/title/desc machine checks; visual quality requires explicit human/self-review note','entries':entries,'contact_sheet':'qa/visual-render/contact-sheet.png','failures':fail}
(R/'qa'/'visual-render-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'status':manifest['status'],'diagram_count':len(entries),'contact_sheet':manifest['contact_sheet'],'failures':len(fail)},indent=2)); sys.exit(1 if fail else 0)
