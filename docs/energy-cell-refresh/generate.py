"""Original native-32px energy-cell artwork. Run AFTER the transport generator.
Usage: python generate.py [code_checkout]; preserves geometry and charge-level mapping.
"""
from pathlib import Path
import sys, json, hashlib
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
TIERS=['copper','nullifite','cyrrium','tectium','wraithsteel','astrium']
ACCENTS=['#eb9a52','#a07ee0','#5fe0f0','#85899c','#9fb6d8','#ffd04a']
BASE='#141326'; SHADOW='#2b2a4a'; STEEL='#454a78'; LIGHT='#9fb6d8'; WHITE='#e6f4ff'
files=[]
def save(name,im,animation=False):
    rel=Path('assets/zerog_tweaks/textures/block/transport')/name
    dest=ROOT/'source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest)
    files.append({'path':rel.as_posix(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
    if animation:
        meta=dest.with_suffix('.png.mcmeta');meta.write_text(json.dumps({'animation':{'frametime':3,'interpolate':False,'width':32,'height':32}},indent=2)+'\n')
        files.append({'path':rel.as_posix()+'.mcmeta','sha256':hashlib.sha256(meta.read_bytes()).hexdigest()})
    if len(sys.argv)>1:
        code=Path(sys.argv[1])
        for layer in ('src/main/resources','src/main/resources/resourcepacks/visual_refresh'):
            target=code/layer/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(dest.read_bytes())
            if animation:target.with_suffix('.png.mcmeta').write_bytes(meta.read_bytes())

sides=[]
for tier,accent in zip(TIERS,ACCENTS):
    im=Image.new('RGBA',(32,32),BASE);d=ImageDraw.Draw(im)
    d.rectangle((1,1,30,30),outline=LIGHT);d.rectangle((2,2,29,29),outline=STEEL)
    d.rectangle((4,4,27,27),fill=SHADOW);d.line((4,4,27,4),fill=WHITE)
    d.rectangle((6,7,21,24),fill=BASE,outline=STEEL)
    d.rectangle((9,10,18,21),fill=STEEL);d.line((10,10,17,10),fill=LIGHT)
    d.rectangle((12,12,15,19),fill=accent);d.line((12,12,15,12),fill=WHITE)
    d.rectangle((23,6,27,25),fill=BASE,outline=STEEL)
    for x,y in ((3,3),(28,3),(3,28),(28,28)):d.point((x,y),fill=WHITE)
    for y in (8,12,16,20):d.line((5,y,7,y),fill=accent)
    save(tier+'_energy_cell_side.png',im);sides.append(im)
    top=Image.new('RGBA',(32,32),BASE);dt=ImageDraw.Draw(top)
    for inset,color in ((1,LIGHT),(2,STEEL),(5,SHADOW),(8,STEEL),(11,accent)):
        dt.rectangle((inset,inset,31-inset,31-inset),outline=color)
    dt.line((12,11,19,11),fill=WHITE);save(tier+'_energy_cell_top.png',top)

gauges=[]
for level in range(9):
    strip=Image.new('RGBA',(32,256));frames=[]
    color='#eb9a52' if level<=2 else '#5fe0f0' if level<=5 else '#58b894'
    for frame in range(8):
        im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
        for i in range(8):
            y=22-2*i;lit=i<level
            d.rectangle((24,y,25,y+1),fill=color if lit else SHADOW)
            if lit and i==frame:d.point((24,y),fill=WHITE)
        strip.paste(im,(0,frame*32));frames.append(im)
    gauges.append(frames);save('energy_cell_gauge_'+str(level)+'.png',strip,True)

previews=[]
for frame in range(8):
    preview=Image.new('RGBA',(6*160,4*144),'#141326');d=ImageDraw.Draw(preview)
    for col,(tier,side) in enumerate(zip(TIERS,sides)):
        for row,level in enumerate((0,2,4,8)):
            cell=side.copy();cell.alpha_composite(gauges[level][frame]);cell=cell.resize((128,128),Image.Resampling.NEAREST)
            preview.paste(cell,(col*160+16,row*144+14));d.text((col*160+4,row*144),tier+' '+str(level)+'/8',fill=WHITE)
    previews.append(preview.convert('RGB'))
previews[0].save(ROOT/'preview.png')
previews[0].save(ROOT/'preview.gif',save_all=True,append_images=previews[1:],duration=150,loop=0)
(ROOT/'manifest.json').write_text(json.dumps({'description':'Original approved-ramp 32px cell casings and charge-driven scanning gauges; run last after transport.py','files':files},indent=2)+'\n')
print('Generated',len(files),'bindings; geometry, capacity and ports unchanged.')
