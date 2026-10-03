"""Original, deterministic Minecraft-native pixel artwork; no imported Mojang PNGs.
32px minerals, seeds, four-stage crops, coherent soils and two-block grass.
Animated pixels change highlights only: PNG animation is not geometric wind sway.
"""
import argparse, hashlib, json, math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from dimension_ecology import PALETTES, grass_colour
from crystals_v2 import embedded_project
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/asset-collection-1.21.1/planet-art-refresh-v1'
def rgb(hex):return tuple(bytes.fromhex(hex.lstrip('#')))
def tint(col,f):return tuple(min(255,max(0,round(c*f))) for c in col)
def soil(col,seed):
 rng=random.Random(seed);im=Image.new('RGBA',(32,32),col+(255,));d=ImageDraw.Draw(im)
 # Clustered dirt grains, not independent bright noise at every pixel.
 for _ in range(150):
  x,y=rng.randrange(-2,32),rng.randrange(-2,32);w,h=rng.choice([(2,2),(3,2),(4,3),(1,2)])
  shade=rng.choice([.68,.78,.88,1.06,1.17]);d.rectangle((x,y,x+w,y+h),fill=tint(col,shade)+(255,))
  if w>2:d.line((x,y,x+w-1,y),fill=tint(col,shade+ .1)+(255,))
 for _ in range(10):
  x,y=rng.randrange(30),rng.randrange(30);d.rectangle((x,y,x+1,y+1),fill=tint(col,1.28)+(255,))
 return im
def farm(base,col,wet):
 im=base.copy();d=ImageDraw.Draw(im)
 if wet:
  for y in range(32):
   for x in range(32):r,g,b,a=im.getpixel((x,y));im.putpixel((x,y),(int(r*.64),int(g*.67),int(b*.7),a))
 for x in range(1,32,8):
  for dx,f in [(0,.48),(1,.57),(2,.72),(3,1.18)]:
   for y in range(32):
    old=base.getpixel(((x+dx)%32,y));c=tint(old[:3],f*(.68 if wet else 1));d.point(((x+dx)%32,y),fill=c+(255,))
 return im
def vegetation(col,seed,kind,upper=False):
 rng=random.Random(seed);leaf=grass_colour(col);im=Image.new('RGBA',(32,64 if kind=='tall' else 32));d=ImageDraw.Draw(im);height=im.height
 for index in range(11 if kind in ['tall','shrub'] else 7):
  root=12+index%8;tip=rng.randrange(2,30);y=rng.randrange(2,24 if kind=='tall' else 17)
  mid=(root+tip)//2;points=[(root,height-1),(mid,height//2),(tip,y)]
  d.line(points,fill=tint(leaf,.62)+(255,),width=2)
  d.line([(x+1,yy) for x,yy in points],fill=tint(leaf,1.22)+(255,))
  if kind in ['shrub','tall']:
   side=-1 if index%2 else 1;sy=height//2+rng.randrange(-8,8)
   d.polygon([(mid,sy),(mid+side*7,sy-7),(mid+side*5,sy-1)],fill=leaf+(255,))
  if kind=='shrub':d.rectangle((tip-1,y,tip+1,y+2),fill=tint(col,1.65)+(255,))
 return im
def flower(col,age=3):
 im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im);leaf=grass_colour(col);tip=27-age*6
 d.line((16,31,16,tip),fill=tint(leaf,.6)+(255,),width=2);d.line((17,31,17,tip),fill=tint(leaf,1.22)+(255,))
 for side,y in [(-1,27),(1,23),(-1,19)]:
  if y<tip+3:continue
  d.polygon([(16,y),(16+side*9,y-5),(16+side*6,y+1)],fill=leaf+(255,))
  d.line((16,y,16+side*7,y-3),fill=tint(leaf,1.3)+(255,))
 if age>=2:
  # Torch-lily-inspired stepped calyx, petal lobes, contrasting inner pollen.
  d.polygon([(12,tip+6),(10,tip),(13,tip-3),(16,tip+1),(20,tip-4),(23,tip),(20,tip+6)],fill=tint(col,.73)+(255,))
  d.rectangle((14,tip-1,19,tip+5),fill=tint(col,1.5)+(255,));d.rectangle((15,tip,17,tip+2),fill=(251,231,165,255))
 return im
def mineral(col,kind,seed):
 rng=random.Random(seed)
 if kind in ['ore','block','raw_block']:
  im=soil((80,76,83) if kind=='ore' else tint(col,.72),seed);d=ImageDraw.Draw(im)
  if kind=='block':
   d.rectangle((1,1,30,30),outline=tint(col,1.3)+(255,));d.line((2,3,28,3),fill=tint(col,1.15)+(255,));d.line((3,28,28,28),fill=tint(col,.45)+(255,))
  else:
   for x,y in ([(4,5),(18,2),(22,19),(9,23),(14,12)] if kind=='ore' else [(2,2),(15,1),(26,7),(5,20),(18,21),(13,11)]):
    d.polygon([(x,y+2),(x+4,y),(x+7,y+3),(x+5,y+6),(x+1,y+5)],fill=tint(col,.55)+(255,))
    d.polygon([(x+1,y+2),(x+4,y+1),(x+6,y+3),(x+3,y+4)],fill=col+(255,));d.line((x+1,y+2,x+4,y+1),fill=tint(col,1.4)+(255,))
  return im
 im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
 if kind=='ingot':
  d.polygon([(3,17),(10,8),(26,8),(29,15),(23,24),(6,24)],fill=tint(col,.45)+(255,))
  d.polygon([(4,16),(11,9),(25,9),(28,14),(21,19),(7,19)],fill=tint(col,1.25)+(255,))
  d.polygon([(7,20),(21,20),(21,23),(7,23)],fill=col+(255,));d.polygon([(22,19),(28,15),(23,23),(22,23)],fill=tint(col,.72)+(255,))
  d.line((11,10,24,10),fill=tint(col,1.6)+(255,))
 elif kind=='raw':
  for x,y,w in [(5,11,10),(15,5,10),(17,19,8)]:
   d.polygon([(x,y+2),(x+3,y),(x+w,y+2),(x+w-1,y+8),(x+4,y+10),(x-1,y+6)],fill=tint(col,.5)+(255,))
   d.polygon([(x+1,y+2),(x+3,y+1),(x+w-2,y+3),(x+4,y+6)],fill=tint(col,1.1)+(255,))
   d.line((x+1,y+2,x+3,y+1,x+w-2,y+3),fill=tint(col,1.5)+(255,))
 elif kind in ['gem','nugget']:
  pts=[(7,6),(18,3),(26,11),(24,23),(14,28),(5,21),(3,13)]
  if kind=='nugget':pts=[(x//2+8,y//2+7) for x,y in pts]
  d.polygon(pts,fill=tint(col,.5)+(255,));d.polygon([pts[0],pts[1],pts[2],(16,15)],fill=tint(col,1.35)+(255,));d.polygon([pts[2],pts[3],pts[4],(16,15)],fill=col+(255,));d.line([pts[0],pts[1],pts[2]],fill=tint(col,1.65)+(255,))
 else:
  for _ in range(40):
   x,y=rng.randrange(5,27),rng.randrange(16,26);d.rectangle((x,y,x+1,y+1),fill=tint(col,rng.choice([.65,1,1.45]))+(255,))
  d.polygon([(10,20),(17,10),(24,22)],fill=col+(255,));d.line((17,10,21,18),fill=tint(col,1.4)+(255,))
 return im
def seeds(col):
 im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
 for x,y in [(6,10),(16,5),(22,15),(12,19)]:
  d.polygon([(x,y+2),(x+4,y),(x+6,y+4),(x+3,y+8),(x,y+6)],fill=tint(col,.55)+(255,))
  d.line((x+2,y+2,x+4,y+4),fill=tint(col,1.6)+(255,),width=2)
 return im
def grain(col):
 im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
 for x,y in [(8,8),(15,4),(22,9)]:
  d.line((16,29,x,y+5),fill=tint(col,.6)+(255,),width=2)
  for n in range(4):
   sy=y+n*3;d.rectangle((x-2,sy,x,sy+2),fill=tint(col,.8)+(255,));d.rectangle((x+1,sy+1,x+3,sy+2),fill=tint(col,1.35)+(255,))
 d.line((12,24,19,24),fill=(211,185,126,255),width=2)
 return im
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--code-root',type=Path,required=True);args=ap.parse_args();code=args.code_root
 spec=json.loads((code/'tools/planet_materials.json').read_text());materials=json.loads((code/'tools/planet_material_art_manifest.json').read_text());records=[];tiles=[];projects=[]
 def save(id,im,folder='block',animate=False):
  rel=f'assets/zerog_tweaks/textures/{folder}/{id}.png';path=OUT/'resource-source'/rel;path.parent.mkdir(parents=True,exist_ok=True)
  display=im
  if animate:
   frames=[]
   for n in range(8):
    frame=im.copy()
    for y in range(im.height):
     for x in range(im.width):
      r,g,b,a=im.getpixel((x,y))
      if a and max(r,g,b)>170:
       c=tint((r,g,b),.9+.12*math.sin(n*math.tau/8));frame.putpixel((x,y),c+(a,))
    frames.append(frame)
   strip=Image.new('RGBA',(32,32*8))
   for n,frame in enumerate(frames):strip.paste(frame,(0,n*32))
   im=strip;path.with_suffix('.png.mcmeta').write_text(json.dumps({'animation':{'frametime':4,'interpolate':True}})+'\n')
  im.save(path);dst=code/'src/main/resources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(path.read_bytes())
  if id=='solflower_seeds':
   override=code/'src/main/resources/resourcepacks/visual_refresh'/rel
   override.parent.mkdir(parents=True,exist_ok=True);override.write_bytes(path.read_bytes())
  if animate:dst.with_suffix('.png.mcmeta').write_bytes(path.with_suffix('.png.mcmeta').read_bytes())
  records.append({'path':rel,'size':list(im.size),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
  return display
 for index,rec in enumerate(materials):
  col=rgb(rec['colour']);name=rec['id']
  for id in rec['blocks']:
   kind='ore' if id.endswith('_ore') else 'raw_block' if id.startswith('raw_') else 'block';im=save(id,mineral(col,kind,700+index))
   project=embedded_project(id,im,'cube');p=OUT/'blockbench'/f'{id}.bbmodel';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(project));projects.append(id)
  for id in rec['items']:
   kind='raw' if id.startswith('raw_') else id.split('_')[-1] if id.endswith(('_ingot','_dust','_nugget')) else 'gem'
   im=save(id,mineral(col,kind,900+index),'item');tiles.append((id,im))
 for dim,planet in spec['dimension_themes'].items():
  base=PALETTES[planet];seed=sum((i+1)*ord(c) for i,c in enumerate(dim));earth=soil(base,seed)
  save(dim+'_soil',earth);save(dim+'_farmland_dry',farm(earth,base,False));save(dim+'_farmland_wet',farm(earth,base,True))
  for suffix,im in [('soil',earth),('farmland',farm(earth,base,False)),('short_grass',vegetation(base,seed,'short'))]:
   name=dim+'_'+suffix;project=embedded_project(name,im,'cross' if suffix=='short_grass' else 'cube')
   if suffix=='farmland':
    project['elements'][0]['to'][1]=15
    ground=embedded_project(name+'_soil',earth,'cube')['textures'][0];ground['id']='1';project['textures'].append(ground)
    for face in project['elements'][0]['faces']:
     if face!='up':project['elements'][0]['faces'][face]['texture']=1
   p=OUT/'blockbench'/f'{name}.bbmodel';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(project));projects.append(name)
  leaf=grass_colour(base);top=soil(leaf,seed+9);side=earth.copy();sd=ImageDraw.Draw(side)
  for x in range(32):
   h=5+(x*13+seed)%5
   for y in range(h):side.putpixel((x,y),top.getpixel((x,y)))
  save(dim+'_grass_top',top);save(dim+'_grass_side',side)
  short=save(dim+'_short_grass',vegetation(base,seed,'short'))
  tall=vegetation(base,seed,'tall');save(dim+'_tall_grass',tall.crop((0,32,32,64)));save(dim+'_tall_grass_top',tall.crop((0,0,32,32)))
  if dim in spec['families']:tiles.extend([(dim+' dry soil',earth),(dim+' dry furrows',farm(earth,base,False)),(dim+' moist furrows',farm(earth,base,True)),(dim+' short grass',short),(dim+' tall upper',tall.crop((0,0,32,32))),(dim+' tall lower',tall.crop((0,32,32,64)))])
 for planet,family in spec['families'].items():
  col=PALETTES[planet];crop=family['crop']
  for id in [crop+'_seeds',crop]:tiles.append((id,save(id,seeds(tint(col,1.4)) if id.endswith('_seeds') else grain(tint(col,1.35)),'item')))
  for age in range(4):
   im=vegetation(col,200,'short');d=ImageDraw.Draw(im)
   # Trim the juvenile canopy; use a grain head only at the mature stage.
   if age<3:im.paste((0,0,0,0),(0,0,32,24-age*5))
   else:
    for x,y in [(10,9),(17,4),(23,10)]:d.rectangle((x,y,x+2,y+6),fill=tint(col,1.5)+(255,));d.line((x,y,x,y+5),fill=tint(col,.65)+(255,))
   save(crop+'_crop_stage'+str(age),im);tiles.append((crop+' stage '+str(age),im))
  for kind in ['glow_flower','glow_shrub']:
   im=flower(tint(col,1.2)) if kind=='glow_flower' else vegetation(col,201,'shrub');save(planet+'_'+kind,im,animate=True);tiles.append((planet+' '+kind,im))
  tall=Image.new('RGBA',(32,64));d=ImageDraw.Draw(tall);leaf=grass_colour(col)
  d.line((16,63,16,8),fill=tint(leaf,.65)+(255,),width=2)
  for y,side in [(56,-1),(45,1),(33,-1),(23,1)]:
   d.polygon([(16,y),(16+side*11,y-9),(16+side*8,y+1)],fill=leaf+(255,));d.line((16,y,16+side*8,y-6),fill=tint(leaf,1.3)+(255,))
  d.polygon([(13,21),(10,13),(11,5),(15,10),(17,2),(21,8),(22,16),(19,22)],fill=tint(col,.85)+(255,))
  d.rectangle((14,11,18,19),fill=tint(col,1.65)+(255,));d.rectangle((15,13,17,17),fill=(251,235,175,255))
  for half,y in [('upper',0),('lower',32)]:
   im=tall.crop((0,y,32,y+32));save(planet+'_tall_blossom_'+half,im,animate=True);tiles.append((planet+' blossom '+half,im))
  name=planet+'_tall_blossom';project=embedded_project(name,tall.crop((0,32,32,64)),'cross');upper=embedded_project(name+'_upper',tall.crop((0,0,32,32)),'cross')
  upper['textures'][0]['id']='1';project['textures'].append(upper['textures'][0])
  for el in upper['elements']:
   el['from'][1]+=16;el['to'][1]+=16;el['origin'][1]+=16
   for face in el['faces'].values():face['texture']=1
  project['elements']+=upper['elements'];project['outliner']+=upper['outliner']
  (OUT/'blockbench'/f'{name}.bbmodel').write_text(json.dumps(project));projects.append(name)
 for age in range(4):save('solflower_crop_stage'+str(age),flower((214,117,39),age))
 save('solflower_seeds',seeds((218,167,67)),'item');save('rust_tuber_seeds',seeds((180,105,73)),'item')
 # Existing aquatic and hanging growth models retain their Java behaviour and UV format.
 for id in ['glowkelp','glowkelp_plant','pyrevine','pyrevine_plant','pyrevine_lit','pyrevine_plant_lit']:
  im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im);kelp=id.startswith('glowkelp');col=(65,168,169) if kelp else (119,85,166)
  d.line((16,0,16,31),fill=tint(col,.65)+(255,),width=2)
  for y in [3,11,20,28]:
   for sign in [-1,1]:
    d.polygon([(16,y),(16+sign*9,y-4),(16+sign*7,y+3)],fill=col+(255,));d.line((16,y,16+sign*7,y-2),fill=tint(col,1.45)+(255,))
  if id.endswith('_lit'):
   for x,y in [(8,8),(22,22)]:d.rectangle((x,y,x+2,y+3),fill=(242,149,65,255))
  save(id,im,animate=True);tiles.append((id,im))
 cols=6;cellw,cellh=170,135
 sheet=Image.new('RGB',(cols*cellw,60+math.ceil(len(tiles)/cols)*cellh),(26,29,39));d=ImageDraw.Draw(sheet)
 d.text((15,15),'ZeroG 1.21.1 - original 32px minerals, seeds, crops, soil and vegetation',fill='white')
 for n,(label,im) in enumerate(tiles):
  x,y=(n%cols)*cellw,(n//cols)*cellh+55;sheet.paste(im.resize((96,96),Image.Resampling.NEAREST),(x+35,y),im.resize((96,96),Image.Resampling.NEAREST));d.text((x+5,y+100),label,fill='white')
 sheet.save(OUT/'planet-art-preview.png')
 for title,subset in [('mineral-items',tiles[:36]),('soil-and-grass',[t for t in tiles if any(s in t[0] for s in ['dry soil','furrows','short grass','tall upper','tall lower'])]),('seeds-and-flora',[t for t in tiles[36:] if not any(s in t[0] for s in ['dry soil','furrows','short grass','tall upper','tall lower'])])]:
  panel=Image.new('RGB',(cols*cellw,60+math.ceil(len(subset)/cols)*cellh),(26,29,39));pd=ImageDraw.Draw(panel);pd.text((15,15),'ZeroG: '+title+' - offline artwork reference',fill='white')
  for n,(label,im) in enumerate(subset):
   x,y=n%cols*cellw,n//cols*cellh+55;tile=im.resize((96,96),Image.Resampling.NEAREST);panel.paste(tile,(x+35,y),tile);pd.text((x+5,y+100),label,fill='white')
  panel.save(OUT/(title+'.png'))
 frames=[]
 for n in range(8):
  canvas=Image.new('RGB',(128*6,160),(26,29,39))
  for i,planet in enumerate(spec['families']):
   im=Image.open(OUT/f'resource-source/assets/zerog_tweaks/textures/block/{planet}_glow_flower.png').crop((0,n*32,32,(n+1)*32)).resize((128,128),Image.Resampling.NEAREST);canvas.paste(im,(i*128,0),im);ImageDraw.Draw(canvas).text((i*128+8,135),planet,fill='white')
  frames.append(canvas)
 frames[0].save(OUT/'flower-highlights.gif',save_all=True,append_images=frames[1:],duration=200,loop=0)
 (OUT/'manifest.json').write_text(json.dumps({'generator':str(Path(__file__).relative_to(ROOT)),'art_style':'original deterministic 32px pixel art','gpu_verified':False,'files':records,'blockbench_projects':projects},indent=2)+'\n')
 print(f'{len(records)} textures; {len(projects)} editable Blockbench projects; preview and highlight GIF')
if __name__=='__main__':main()
