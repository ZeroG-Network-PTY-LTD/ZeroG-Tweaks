"""Original pixel-art sources and additive runtime data. No vanilla PNGs copied.

32px tile budget, crisp clustered highlights, transparent plant silhouettes.
Run with --code pointing to a separate 1.21.x checkout; sources stay on Design.
"""
import argparse, colorsys, hashlib, json, math, random, re
from pathlib import Path
from PIL import Image, ImageDraw
p=argparse.ArgumentParser();p.add_argument('--code',type=Path,required=True);a=p.parse_args()
base=Path(__file__).resolve().parent;res=a.code/'src/main/resources';art=base/'source';art.mkdir(parents=True,exist_ok=True)
ns='zerog_tweaks';palettes={'moon':(145,115,231),'mars':(70,199,178),'cerulon':(241,136,179),'skarn':(124,196,246),'eidolon':(242,153,76),'solvane':(124,99,230)}
groups={'moon':['lunar_turnip','pearl_carrot','orbit_pea'],'mars':['rust_beet','ares_chili','copper_onion'],
 'cerulon':['tidal_cucumber','reef_lettuce','azure_bean'],'skarn':['ember_radish','cinder_pepper','obsidian_aubergine'],
 'eidolon':['frost_cabbage','rime_parsnip','ghost_garlic'],'solvane':['solar_tomato','corona_corn','sunburst_squash']}
manifest=[]
def write(rel,obj):
 path=res/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
def texture(id,im,kind='block'):
 path=art/kind/(id+'.png');path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
 dest=res/f'assets/{ns}/textures/{kind}/{id}.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest)
 manifest.append({'path':f'{kind}/{id}.png','size':list(im.size),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
def color(c,k):return tuple(max(0,min(255,int(v*k))) for v in c)+(255,)
def cross(id,tex):write(f'assets/{ns}/models/block/{id}.json',{'parent':'minecraft:block/cross','render_type':'minecraft:cutout','textures':{'cross':ns+':block/'+tex}})
def icon(id):write(f'assets/{ns}/models/item/{id}.json',{'parent':'minecraft:item/generated','textures':{'layer0':ns+':item/'+id}})
def state(id,variants):write(f'assets/{ns}/blockstates/{id}.json',{'variants':variants})
def itemloot(id,count=1,conditions=None):
 entry={'type':'minecraft:item','name':ns+':'+id}
 if count!=1:entry['functions']=[{'function':'minecraft:set_count','count':count}]
 if conditions:entry['conditions']=conditions
 return entry
def loot(block,entries):write(f'data/{ns}/loot_table/blocks/{block}.json',{'type':'minecraft:block','pools':[{'rolls':1,'entries':[e]} for e in entries]})
def title(id):return id.replace('_',' ').title()
langpath=res/f'assets/{ns}/lang/en_us.json';lang=json.loads(langpath.read_text())
def recipe(id,ingredients,result,count=1):write(f'data/{ns}/recipe/{id}.json',{'type':'minecraft:crafting_shapeless','ingredients':[{'item':ns+':'+s} for s in ingredients],'result':{'id':ns+':'+result,'count':count}})
def plant(c,age,index):
 im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im);h=7+age*7;stem=(78,125,117,255)
 for off in (-7,0,7) if index%3==0 else (-4,4):
  x=16+off;d.rectangle((x,32-h,x+1,31),fill=stem)
  for y in range(31,32-h,-5):
   spread=3+age;d.polygon([(x,y),(x-spread,y-3),(x-spread-1,y-5),(x,y-2)],fill=color(c,.6))
   d.polygon([(x+1,y-2),(x+spread,y-5),(x+spread+1,y-3),(x+1,y)],fill=color(c,.85))
  if age>=2:
   y=32-h;shape=index%4
   if shape==0:d.ellipse((x-3,y,x+4,y+6),fill=color(c,.9));d.rectangle((x-2,y+1,x,y+2),fill=color(c,1.3))
   elif shape==1:d.polygon([(x-3,y+2),(x+3,y),(x+2,y+8),(x,y+10)],fill=color(c,.95))
   elif shape==2:d.ellipse((x-4,y+1,x+4,y+7),fill=color(c,.7));d.line((x-2,y+2,x+2,y+5),fill=color(c,1.25),width=2)
   else:
    for sy in range(y,y+8,3):d.rectangle((x-3,sy,x+3,sy+1),fill=color(c,1.15 if sy%2 else .7))
 return im
def food(c,index,seed=False,name=''):
 im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
 if seed:
  for x,y in [(10,17),(17,11),(21,21)]:d.ellipse((x-3,y-3,x+3,y+3),fill=color(c,.65));d.rectangle((x-2,y-2,x,y),fill=color(c,1.3))
 elif name:
  dark=color(c,.48);mid=color(c,.82);light=color(c,1.17);shine=color(c,1.4);leaf=(84,145,120,255)
  if 'slice' in name:
   d.polygon([(4,9),(27,9),(23,23),(15,29),(8,23)],fill=dark)
   d.polygon([(6,9),(25,9),(21,21),(15,25),(10,21)],fill=mid)
   d.line((7,10,23,10),fill=shine,width=2)
   for x,y in [(11,15),(17,18),(21,13)]:d.rectangle((x,y,x+1,y+2),fill=(54,42,78,255))
  elif any(s in name for s in ['carrot','parsnip','radish']):
   d.polygon([(8,11),(24,10),(21,20),(13,29),(10,23)],fill=mid)
   d.line((10,12,13,21),fill=light,width=3)
   for y in [16,21]:d.line((16,y,20,y-1),fill=dark,width=1)
   d.polygon([(16,11),(8,5),(11,3),(17,7),(24,3),(25,6),(19,11)],fill=leaf)
  elif 'corn' in name:
   d.rounded_rectangle((10,5,22,28),radius=4,fill=dark)
   for x in [12,16,20]:
    for y in range(8,25,4):d.rectangle((x,y,x+2,y+2),fill=light if x==12 else mid)
   d.polygon([(10,27),(5,14),(11,20),(16,28),(24,17),(21,28)],fill=leaf)
  elif any(s in name for s in ['lettuce','cabbage']):
   for x,y,r in [(9,20,6),(21,20,6),(15,13,7),(16,22,7)]:d.ellipse((x-r,y-r,x+r,y+r),fill=mid);d.arc((x-r+1,y-r+1,x+r-1,y+r-1),180,350,fill=light,width=2)
   d.line((16,14,15,29),fill=shine,width=1)
  elif any(s in name for s in ['pea','bean']):
   d.polygon([(5,24),(10,12),(21,5),(27,8),(23,18),(12,28)],fill=dark)
   for x,y in [(10,22),(16,16),(22,10)]:d.ellipse((x-4,y-4,x+3,y+3),fill=mid);d.rectangle((x-2,y-2,x,y),fill=light)
   d.line((7,25,24,8),fill=shine,width=1)
  elif 'chili' in name:
   d.polygon([(18,8),(25,10),(25,18),(19,25),(8,28),(14,23),(18,16)],fill=mid)
   d.line((20,11,21,17),fill=light,width=2);d.line((21,8,16,4,11,5),fill=leaf,width=2)
  elif 'cucumber' in name:
   d.rounded_rectangle((9,4,22,28),radius=6,fill=dark);d.rounded_rectangle((10,4,18,27),radius=5,fill=mid)
   d.line((12,8,12,22),fill=light,width=2)
   for x,y in [(16,12),(19,19),(15,24)]:d.rectangle((x,y,x+1,y+1),fill=shine)
  elif 'aubergine' in name:
   d.ellipse((7,11,24,29),fill=dark);d.ellipse((9,10,24,26),fill=mid);d.line((12,13,11,21),fill=light,width=2)
   d.polygon([(10,12),(10,6),(16,8),(22,5),(23,11),(18,13)],fill=leaf)
  elif 'garlic' in name:
   for x,y in [(10,21),(21,21),(15,18)]:d.ellipse((x-5,y-7,x+5,y+7),fill=mid);d.line((x-2,y-3,x-2,y+3),fill=light,width=2)
   d.polygon([(12,15),(14,5),(18,5),(19,15)],fill=light)
  elif 'onion' in name:
   d.ellipse((6,11,25,28),fill=mid);d.arc((8,12,22,27),100,270,fill=light,width=2);d.arc((10,12,23,27),270,80,fill=dark,width=2)
   d.line((15,11,16,5,21,2),fill=leaf,width=2);d.line((13,28,12,30),fill=light)
  elif any(s in name for s in ['squash','pepper']):
   for x in [10,16,22]:d.ellipse((x-5,10,x+5,28),fill=dark);d.ellipse((x-4,10,x+4,25),fill=mid)
   d.line((13,12,12,20),fill=light,width=2);d.rectangle((14,6,17,11),fill=leaf)
  else:
   d.ellipse((6,10,25,27),fill=dark);d.ellipse((7,9,25,24),fill=mid);d.rectangle((10,12,14,15),fill=light)
   d.polygon([(16,11),(9,7),(16,8),(21,5),(20,9),(25,10),(19,13)],fill=leaf)
   if any(s in name for s in ['turnip','beet']):d.line((16,25,15,30),fill=light,width=2)
 else:
  if index%4==0:d.ellipse((6,10,25,28),fill=color(c,.65));d.ellipse((8,10,24,24),fill=color(c,.95));d.rectangle((10,12,14,15),fill=color(c,1.35))
  elif index%4==1:d.polygon([(8,9),(24,8),(21,19),(13,29),(10,21)],fill=color(c,.9));d.line((10,12,13,21),fill=color(c,1.3),width=3)
  elif index%4==2:
   for x,y in [(11,17),(17,13),(20,21)]:d.ellipse((x-6,y-4,x+5,y+7),fill=color(c,.85));d.rectangle((x-3,y-1,x-1,y+1),fill=color(c,1.3))
  else:
   d.rounded_rectangle((8,9,24,28),radius=4,fill=color(c,.75))
   for y in range(12,27,4):d.line((10,y,22,y-1),fill=color(c,1.1),width=2)
  d.polygon([(16,10),(10,5),(15,4),(18,8),(24,4),(25,7),(19,11)],fill=(83,139,109,255))
 return im
for home,ids in groups.items():
 for i,id in enumerate(ids):
  c=palettes[home];c=tuple(min(255,int(v*(.85+i*.12))) for v in c)
  texture(id,food(c,i,name=id),'item');texture(id+'_seeds',food(c,i,True),'item');icon(id);icon(id+'_seeds')
  variants={}
  for age in range(4):texture(id+f'_stage{age}',plant(c,age,i));cross(id+f'_stage{age}',id+f'_stage{age}');variants[f'age={age}']={'model':ns+':block/'+id+f'_stage{age}'}
  state(id+'_crop',variants)
  mature={'condition':'minecraft:block_state_property','block':ns+':'+id+'_crop','properties':{'age':'3'}}
  loot(id+'_crop',[itemloot(id+'_seeds'),itemloot(id,2,[mature]),itemloot(id+'_seeds',2,[mature])])
  recipe(id+'_to_seeds',[id],id+'_seeds',2)
  lang['item.'+ns+'.'+id]=title(id);lang['item.'+ns+'.'+id+'_seeds']=title(id)+' Seeds';lang['block.'+ns+'.'+id+'_crop']=title(id)+' Crop'
for i,(id,home) in enumerate([('nebula_melon','cerulon'),('eclipse_pumpkin','moon')]):
 c=palettes[home];rng=random.Random(id)
 for face in ['side','top']:
  im=Image.new('RGBA',(32,32));px=im.load()
  for y in range(32):
   for x in range(32):
    ring=(x//4)%2 if face=='side' else int(math.hypot(x-15.5,y-15.5)/3)%2
    px[x,y]=color(c,.55+ring*.24+(31-y)*.003+rng.uniform(-.06,.06))
  d=ImageDraw.Draw(im)
  if face=='top':d.rectangle((13,13,18,18),fill=(78,106,106,255))
  texture(id+'_'+face,im)
 write(f'assets/{ns}/models/block/{id}.json',{'parent':'minecraft:block/cube_bottom_top','textures':{'side':ns+':block/'+id+'_side','top':ns+':block/'+id+'_top','bottom':ns+':block/'+id+'_top'}});state(id,{'':{'model':ns+':block/'+id}})
 write(f'assets/{ns}/models/item/{id}.json',{'parent':ns+':block/'+id})
 texture(id+'_slice',food(c,i,name=id+'_slice'),'item');texture(id+'_seeds',food(c,i,True),'item');icon(id+'_slice');icon(id+'_seeds')
 # Native stem geometry, but coloured source art rather than vanilla green tint.
 texture(id+'_stem',plant((101,157,150),3,1));texture(id+'_attached_stem',plant((101,157,150),3,1))
 for age in range(8):write(f'assets/{ns}/models/block/{id}_stem{age}.json',{'parent':f'minecraft:block/stem_growth{age}','render_type':'minecraft:cutout','textures':{'stem':ns+':block/'+id+'_stem'}})
 state(id+'_stem',{f'age={age}':{'model':ns+':block/'+id+f'_stem{age}'} for age in range(8)})
 write(f'assets/{ns}/models/block/{id}_attached_stem.json',{'parent':'minecraft:block/stem_fruit','render_type':'minecraft:cutout','textures':{'stem':ns+':block/'+id+'_stem','upperstem':ns+':block/'+id+'_attached_stem'}})
 state(id+'_attached_stem',{f'facing={direction}':{'model':ns+':block/'+id+'_attached_stem','y':rotation} for direction,rotation in [('north',0),('east',90),('south',180),('west',270)]})
 loot(id,[itemloot(id+'_slice',4)]);loot(id+'_stem',[itemloot(id+'_seeds')]);loot(id+'_attached_stem',[itemloot(id+'_seeds')])
 recipe(id+'_slices_to_seeds',[id+'_slice'],id+'_seeds');recipe(id+'_slices_to_block',[id+'_slice']*9,id)
 for item in [id+'_slice',id+'_seeds']:lang['item.'+ns+'.'+item]=title(item)
 lang['block.'+ns+'.'+id]=title(id)
# Dimension-theme assignments are runtime's locked material manifest.
themes=json.loads((a.code/'tools/planet_materials.json').read_text())['dimension_themes']
if isinstance(themes,list):raise ValueError('Expected dimension theme mapping')
for dimension,home in sorted(themes.items()):
 dim=dimension.split(':')[-1];home=home if isinstance(home,str) else home['theme'];basecolor=palettes[home]
 hue,sat,val=colorsys.rgb_to_hsv(*(v/255 for v in basecolor));offset=(int(hashlib.sha256(dim.encode()).hexdigest()[:4],16)%17-8)/100
 c=tuple(int(v*255) for v in colorsys.hsv_to_rgb((hue+offset)%1,sat,val))
 rng=random.Random(dim);vines=[]
 for body in [False,True]:
  for berry in [False,True]:
   id=dim+('_cave_vines_plant' if body else '_cave_vines')+('_berries' if berry else '')
   im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
   d.line([(16,0),(14,9),(18,18),(15,31)],fill=color(c,.45),width=2)
   for y in [3,11,21]:
    d.polygon([(15,y+3),(7,y),(8,y+5),(14,y+7)],fill=color(c,.65));d.line((9,y+2,13,y+4),fill=color(c,1.05),width=2)
    d.polygon([(16,y+5),(25,y+1),(24,y+6),(17,y+9)],fill=color(c,.85))
    if berry:d.ellipse((7,y+6,12,y+11),fill=color(c,1.1));d.rectangle((8,y+7,9,y+8),fill=(246,244,230,255))
   texture(id,im);cross(id,id)
  block=dim+('_cave_vines_plant' if body else '_cave_vines')
  state(block,{'berries=false':{'model':ns+':block/'+block},'berries=true':{'model':ns+':block/'+block+'_berries'}})
  loot(block,[itemloot(dim+'_cave_berry',1,[{'condition':'minecraft:block_state_property','block':ns+':'+block,'properties':{'berries':'true'}}])])
 texture(dim+'_cave_berry',food(c,2),'item');icon(dim+'_cave_berry');lang['item.'+ns+'.'+dim+'_cave_berry']=title(dim)+' Cave Berry'
 im=Image.new('RGBA',(32,32));px=im.load()
 for y in range(32):
  for x in range(32):px[x,y]=color(c,.38+rng.random()*.18+((x+y)//5%2)*.12)
 texture(dim+'_dripstone_block',im)
 write(f'assets/{ns}/models/block/{dim}_dripstone_block.json',{'parent':'minecraft:block/cube_all','textures':{'all':ns+':block/'+dim+'_dripstone_block'}})
 state(dim+'_dripstone_block',{'':{'model':ns+':block/'+dim+'_dripstone_block'}})
 write(f'assets/{ns}/models/item/{dim}_dripstone_block.json',{'parent':ns+':block/'+dim+'_dripstone_block'})
 loot(dim+'_dripstone_block',[itemloot(dim+'_dripstone_block')])
 variants={}
 for direction in ['up','down']:
  for thickness in ['tip','tip_merge','frustum','middle','base']:
   id=dim+'_pointed_dripstone_'+direction+'_'+thickness;im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
   width={'tip':7,'tip_merge':7,'frustum':10,'middle':11,'base':14}[thickness]
   for y in range(32):
    w=int(width*(.15+y/32)) if thickness=='tip' else width
    for x in range(16-w,16+w+1):
     if 0<=x<32:im.putpixel((x,y),color(c,.35+(.45*(1-abs(x-14)/max(width,1)))+rng.random()*.12))
   if direction=='down':im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
   texture(id,im);cross(id,id);variants[f'thickness={thickness},vertical_direction={direction}']={'model':ns+':block/'+id}
 state(dim+'_pointed_dripstone',variants);texture(dim+'_pointed_dripstone',food(c,1),'item');icon(dim+'_pointed_dripstone');loot(dim+'_pointed_dripstone',[itemloot(dim+'_pointed_dripstone')])
 for block in [dim+'_pointed_dripstone',dim+'_dripstone_block',dim+'_cave_vines',dim+'_cave_vines_plant']:lang['block.'+ns+'.'+block]=title(block)
write(f'assets/{ns}/lang/en_us.json',lang)
# Compostable items and discoverable seeds in generated structure chests.
compost=res/'data/neoforge/data_maps/item/compostables.json';data=json.loads(compost.read_text()) if compost.exists() else {'values':{}}
for home,ids in groups.items():
 for id in ids:data['values'][ns+':'+id]={'chance':.65};data['values'][ns+':'+id+'_seeds']={'chance':.3}
for dim in themes:data['values'][ns+':'+dim.split(':')[-1]+'_cave_berry']={'chance':.3}
write('data/neoforge/data_maps/item/compostables.json',data)
seeds=[ns+':'+id+'_seeds' for ids in groups.values() for id in ids]+[ns+':'+id+'_seeds' for id in ['nebula_melon','eclipse_pumpkin']]
seed_tag=res/'data/minecraft/tags/item/villager_plantable_seeds.json'
existing=json.loads(seed_tag.read_text()).get('values',[]) if seed_tag.exists() else []
original=[ns+':'+id for id in ['rust_tuber','solflower_seeds','moon_millet_seeds','rustgrain_seeds','azure_rice_seeds','ember_wheat_seeds','frost_barley_seeds','sunspike_seeds','rust_tuber_seeds']]
write('data/minecraft/tags/item/villager_plantable_seeds.json',{'replace':False,'values':list(dict.fromkeys(existing+original+seeds))})
write('data/neoforge/tags/block/villager_farmlands.json',{'replace':False,'values':[ns+':'+dim.split(':')[-1]+'_farmland' for dim in themes]})
for chest in (res/f'data/{ns}/loot_table/chests').glob('*.json'):
 data=json.loads(chest.read_text());data['pools']=[pool for pool in data.get('pools',[]) if pool.get('name')!='alien_crop_seeds_v1']
 data['pools'].append({'name':'alien_crop_seeds_v1','rolls':1,'entries':[itemloot(id+'_seeds',{'type':'minecraft:uniform','min':2,'max':5}) for ids in groups.values() for id in ids]+[itemloot(id+'_seeds',2) for id in ['nebula_melon','eclipse_pumpkin']]})
 write(str(chest.relative_to(res)),data)
(base/'manifest.json').write_text(json.dumps({'original_art':True,'native_resolution':32,'crop_families':20,'cave_families':len(themes),'textures':manifest},indent=2)+'\n')
# Offline source sheet, not an in-game render.
sheet=Image.new('RGB',(1000,600),(18,24,36));d=ImageDraw.Draw(sheet)
ids=[id for group in groups.values() for id in group]+['nebula_melon_slice','eclipse_pumpkin_slice']
for i,id in enumerate(ids):
 x=i%5*200;y=i//5*145;im=Image.open(art/'item'/f'{id}.png').resize((80,80),Image.Resampling.NEAREST);sheet.paste(im,(x+55,y+10),im);d.text((x+8,y+104),title(id),fill=(212,225,234))
sheet.save(base/'crop-reference.png');print(f'Created {len(manifest)} original 32px PNGs; 20 crop families and {len(themes)} cave families')
