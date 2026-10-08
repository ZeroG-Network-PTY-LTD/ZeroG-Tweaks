"""Original ZeroG 32px gold admin cell. Runtime models/animated atlas plus truthful preview.
Usage: python3 generate.py CODE/assets/zerog_tweaks
"""
import json, math, sys
from pathlib import Path
from PIL import Image, ImageDraw

assets=Path(sys.argv[1]);root=Path(__file__).resolve().parent
# Locked solvanite gold ramp: hue-shifted brown shadows and pale highlights.
gold=['#1f0e05','#5a2b0a','#a3570f','#e09a1c','#ffd04a','#fff4c0']
core=['#2a0e4a','#5a22a0','#9a4ef0','#c48cff','#e8ccff','#ffffff']
frames=[]
for frame in range(8):
    im=Image.new('RGBA',(32,32),gold[0]);d=ImageDraw.Draw(im)
    d.rectangle((1,1,30,30),fill=gold[2]);d.rectangle((2,2,29,29),fill=gold[3])
    d.line((2,2,29,2),fill=gold[5]);d.line((2,2,2,29),fill=gold[4])
    d.line((3,29,29,29),fill=gold[1]);d.line((29,3,29,29),fill=gold[1])
    d.rectangle((5,5,26,26),fill=gold[0]);d.rectangle((6,6,25,25),fill=gold[1])
    d.rectangle((8,8,23,23),fill=gold[2]);d.rectangle((9,9,22,22),fill=gold[3])
    pulse=3+int(frame in (2,3,4,5));d.ellipse((10,10,21,21),fill=core[1])
    d.ellipse((12,12,19,19),fill=gold[pulse]);d.rectangle((15,13,16,18),fill=gold[5])
    d.line([(11,16),(14,16),(14,14),(17,14),(17,18),(20,18)],fill=core[5])
    for y in (9,13,17,21):
        d.rectangle((3,y,4,y+1),fill=gold[4 if (y//4+frame)%3==0 else 2])
        d.rectangle((27,y,28,y+1),fill=gold[5 if (y//4+frame)%3==0 else 3])
    for x,y in ((3,3),(27,3),(3,27),(27,27)):
        d.rectangle((x,y,x+1,y+1),fill=gold[5]);d.point((x+1,y+1),fill=gold[1])
    frames.append(im)
strip=Image.new('RGBA',(32,256))
for i,im in enumerate(frames):strip.paste(im,(0,i*32))
def write(path,data):
    p=assets/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2)+'\n')
path=assets/'textures/block/transport/creative_energy_cell.png';path.parent.mkdir(parents=True,exist_ok=True);strip.save(path)
write('textures/block/transport/creative_energy_cell.png.mcmeta',{'animation':{'frametime':3,'interpolate':True}})
write('models/block/transport/creative_energy_cell.json',{'parent':'minecraft:block/cube_all','textures':{'all':'zerog_tweaks:block/transport/creative_energy_cell'}})
write('models/item/creative_energy_cell.json',{'parent':'zerog_tweaks:block/transport/creative_energy_cell'})
write('blockstates/creative_energy_cell.json',{'variants':{'':{'model':'zerog_tweaks:block/transport/creative_energy_cell'}}})
frames[0].resize((256,256),Image.Resampling.NEAREST).save(root/'texture-preview.png')
frames[0].resize((256,256),Image.Resampling.NEAREST).save(root/'pulse-preview.gif',save_all=True,append_images=[f.resize((256,256),Image.Resampling.NEAREST) for f in frames[1:]],duration=150,loop=0)
print('Generated original 32x32, eight-frame gold cell texture and shared item/block model.')
