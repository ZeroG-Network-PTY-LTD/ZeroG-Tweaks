"""Original native 32px wood/leaf and dust artwork, preserving registered IDs.

No concept-sheet crops or commercial PNGs. Original deterministic drawing.
Run after planet_art_refresh and botany; this is the final dust overlay.
"""
import argparse, colorsys, hashlib, json, math, random, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

p=argparse.ArgumentParser();p.add_argument('--code',type=Path,required=True);a=p.parse_args()
base=Path(__file__).resolve().parent;res=a.code/'src/main/resources';out=base/'source'
sys.path.insert(0,str(base.parent/'zero-g-tweaks-bundle/generators'))
from data import M
WOODS={
 'shardwood':{'bark':(45,79,89),'wood':(81,154,157),'leaf':(45,144,126),'bud':(180,123,230)},
 'charwood':{'bark':(49,36,37),'wood':(125,68,53),'leaf':(103,69,74),'bud':(244,154,71)},
 'hoarwood':{'bark':(100,103,142),'wood':(166,164,194),'leaf':(149,165,185),'bud':(151,218,228)},
 'gildwood':{'bark':(130,83,43),'wood':(192,148,78),'leaf':(151,164,64),'bud':(247,197,97)},
}
records=[];tiles=[]
def ramp(c,f):
 value=tuple(max(0,min(255,round(v*f))) for v in c)
 target=(47,36,78) if f<1 else (255,240,197);amount=min(.24,abs(f-1)*.38)
 return tuple(round(v*(1-amount)+t*amount) for v,t in zip(value,target))+(255,)
def save(id,im,kind='block',palette=None):
 rel=f'{kind}/{id}.png';src=out/rel;dst=res/'assets/zerog_tweaks/textures'/rel
 assert dst.exists(),f'Refuse to invent an unregistered texture binding: {rel}'
 src.parent.mkdir(parents=True,exist_ok=True);im.save(src);dst.write_bytes(src.read_bytes())
 pack=res/'resourcepacks/visual_refresh/assets/zerog_tweaks/textures'/rel
 if pack.exists():pack.write_bytes(src.read_bytes())
 records.append({'path':rel,'size':list(im.size),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'palette':palette})
 tiles.append((id,im))
def bark(c,seed,stripped=False):
 rng=random.Random(seed);im=Image.new('RGBA',(32,32),ramp(c,.86));d=ImageDraw.Draw(im)
 for x in range(0,32,4):
  bend=rng.choice([-1,0,1]);shade=rng.choice([.69,.8,.96,1.08])
  d.rectangle((x,0,x+2,31),fill=ramp(c,shade))
  for y in range(-5,32,9):
   yy=y+rng.randrange(4);points=[(x,yy),(x+bend,yy+5),(x,yy+10)]
   d.line(points,fill=ramp(c,.55 if not stripped else .78),width=1)
   d.line([(xx+1,y0) for xx,y0 in points],fill=ramp(c,1.18),width=1)
 if not stripped:
  for x,y in [(7,10),(23,24)]:
   d.polygon([(x-2,y),(x,y-4),(x+2,y),(x,y+5)],fill=ramp(c,.44))
   d.line([(x+1,y-3),(x+2,y),(x+1,y+3)],fill=ramp(c,1.16))
 return im
def rings(c,barkcolour,stripped):
 im=Image.new('RGBA',(32,32),ramp(c,.84));d=ImageDraw.Draw(im)
 for inset in range(2,15,3):
  d.rectangle((inset,inset,31-inset,31-inset),outline=ramp(c,.57))
  d.line((inset+1,inset+1,30-inset,inset+1),fill=ramp(c,1.16))
  d.line((inset+1,inset+1,inset+1,30-inset),fill=ramp(c,1.08))
 d.rectangle((14,14,17,17),fill=ramp(c,.61))
 if not stripped:
  d.rectangle((0,0,31,31),outline=ramp(barkcolour,.7),width=2)
 return im
def boards(c,seed):
 im=Image.new('RGBA',(32,32),ramp(c,.88));d=ImageDraw.Draw(im);rng=random.Random(seed)
 for row in range(4):
  y=row*8;shade=rng.choice([.86,.95,1.04]);d.rectangle((0,y+1,31,y+6),fill=ramp(c,shade))
  d.line((0,y,31,y),fill=ramp(c,.45));d.line((0,y+1,31,y+1),fill=ramp(c,1.2))
  joint=(7+row*11)%32;d.line((joint,y+1,joint,y+7),fill=ramp(c,.61))
  for sy,x,width in [(y+3,2+row*3,10),(y+5,17-row*2,8)]:
   d.line((x,sy,min(31,x+width),sy),fill=ramp(c,.8));d.line((x+1,sy-1,min(31,x+width-2),sy-1),fill=ramp(c,1.07))
 return im
def leaves(c,accent,seed):
 rng=random.Random(seed);im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
 # Wrapped clusters preserve cutout gaps and avoid a solid noisy cube.
 for row in range(5):
  for col in range(5):
   cx=(col*7+row%2*3+rng.randrange(3))%32;cy=(row*7+rng.randrange(3))%32
   shape=[(-4,0),(-1,-3),(3,-2),(4,0),(1,3),(-2,2)];shade=rng.choice([.7,.86,1])
   for dx in (-32,0,32):
    for dy in (-32,0,32):
     x,y=cx+dx,cy+dy;d.polygon([(x+xx,y+yy) for xx,yy in shape],fill=ramp(c,shade))
     d.line([(x-2,y-1),(x+1,y-2),(x+2,y-1)],fill=ramp(c,1.28))
     d.line([(x,y),(x+2,y+1)],fill=ramp(c,.54))
 # Small botanical buds: painted highlights, not an emitted-light claim.
 for x,y in [(8,9),(24,23)]:
  d.polygon([(x-2,y),(x,y-2),(x+2,y),(x,y+2)],fill=ramp(accent,.86))
  d.line((x-1,y-1,x,y-1),fill=ramp(accent,1.3))
 return im
def dust(c,seed):
 rng=random.Random(seed);im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
 # Irregular heap, visible volume, restrained grain; no generic white silhouette.
 d.polygon([(3,23),(6,19),(11,17),(15,11),(20,13),(23,18),(28,21),(29,25),(23,28),(8,28)],fill=ramp(c,.43))
 d.polygon([(5,22),(11,18),(15,12),(20,14),(22,19),(27,22),(24,25),(9,25)],fill=ramp(c,.94))
 d.polygon([(7,21),(12,18),(16,13),(18,15),(14,20),(10,23)],fill=ramp(c,1.25))
 d.line([(7,26),(22,26),(26,24)],fill=ramp(c,.64))
 for _ in range(24):
  x,y=rng.randrange(7,25),rng.randrange(18,25)
  d.rectangle((x,y,x+1,y+1),fill=ramp(c,rng.choice([.65,.82,1.12,1.38])))
 for x,y in [(7,12),(23,10),(12,6),(26,15)]:
  d.rectangle((x,y,x+1,y+1),fill=ramp(c,1.12));d.point((x,y),fill=ramp(c,1.45))
 return im

for index,(name,pal) in enumerate(WOODS.items()):
 for id,im in [(name+'_log',bark(pal['bark'],100+index)),(name+'_log_top',rings(pal['wood'],pal['bark'],False)),
               ('stripped_'+name+'_log',bark(pal['wood'],200+index,True)),('stripped_'+name+'_log_top',rings(pal['wood'],pal['bark'],True)),
               (name+'_planks',boards(pal['wood'],300+index)),(name+'_leaves',leaves(pal['leaf'],pal['bud'],400+index))]:save(id,im,palette=pal)

materials={row['id']:tuple(bytes.fromhex(row['colour'].lstrip('#'))) for row in json.loads((a.code/'tools/planet_material_art_manifest.json').read_text())}
for path in sorted((res/'assets/zerog_tweaks/textures/item').glob('*dust.png')):
 id=path.stem;key=id.removesuffix('_dust');rec=M.get(id,M.get(key));c=(169,129,230) if id=='stardust' else materials.get(key)
 if rec:c=tuple(bytes.fromhex(rec['pal'][2].lstrip('#')))
 assert c is not None,f'Unknown material palette needs an authored entry: {id}'
 save(id,dust(c,sum((i+1)*ord(x) for i,x in enumerate(id))),'item',list(c))

base.mkdir(parents=True,exist_ok=True)
(base/'manifest.json').write_text(json.dumps({'original_art':True,'license':'All Rights Reserved','resolution':32,
 'generator':'docs/wood-dust-art-v2/generate.py','style':'A natural wood/leaf forms plus C selective botanical and mineral accents',
 'gpu_verified':False,'world_light_changed':False,'wood_families':list(WOODS),'textures':records},indent=2)+'\n')
cols=6;w=cols*150;h=40+math.ceil(len(tiles)/cols)*145
sheet=Image.new('RGB',(w,h),(19,26,36));d=ImageDraw.Draw(sheet)
d.text((12,12),'Original 32px wood, leaves and dust sources - not a game capture',fill=(220,235,245))
for i,(id,im) in enumerate(tiles):
 x=i%cols*150;y=40+i//cols*145;tile=im.resize((96,96),Image.Resampling.NEAREST)
 sheet.paste(tile,(x+27,y),tile);d.text((x+4,y+100),id[:24],fill=(203,224,238))
sheet.save(base/'native-textures-preview.png')
print(f'Generated {len(records)} original 32px textures: four wood families and all {len(records)-24} dust sprites.')
