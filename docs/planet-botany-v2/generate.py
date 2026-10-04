"""Original 32px pixel botany; no PNGs copied/recoloured from previous artwork.

Explicit 50-family catalogue, new source overlay, stable old IDs, native geometry.
Run --code against 1.21.x. Design source/archive is never overwritten by runtime.
"""
import argparse, base64, colorsys, hashlib, json, math, random, uuid
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
p=argparse.ArgumentParser();p.add_argument('--code',type=Path,required=True);a=p.parse_args()
base=Path(__file__).resolve().parent;res=a.code/'src/main/resources';ns='zerog_tweaks'
themes=['moon','mars','cerulon','skarn','eidolon','solvane']
leaves=[(99,166,155),(76,156,120),(65,161,150),(103,146,118),(100,164,184),(153,167,90)]
fruits=[(172,128,235),(240,141,81),(239,129,174),(245,147,68),(245,180,102),(213,128,211)]
catalog={
 'moon':{'flowers':['selenite_bell','lunar_lotus','crater_daisy'],'shrubs':['silverfern','moon_thistle'],'fruits':['moon_plum','selenite_fig'],'crop':'lunar_snap_pea'},
 'mars':{'flowers':['copper_poppy','dust_orchid','rust_lily'],'shrubs':['red_dune_brush','filter_fern'],'fruits':['ares_apricot','dust_date'],'crop':'martian_okra'},
 'cerulon':{'flowers':['tidal_iris','coral_lantern','reef_anemone'],'shrubs':['azure_coral_bush','pearl_fern'],'fruits':['lagoon_pear','cerulite_cherry'],'crop':'reef_artichoke'},
 'skarn':{'flowers':['ember_torchflower','cinder_dahlia','basalt_bloom'],'shrubs':['ash_fan','scorched_heather'],'fruits':['ember_guava','coalberry'],'crop':'cinder_asparagus'},
 'eidolon':{'flowers':['frost_snowdrop','ghost_camellia','rime_bell'],'shrubs':['frostlace','winter_fan'],'fruits':['rime_apple','ghost_persimmon'],'crop':'glacier_broccoli'},
 'solvane':{'flowers':['sun_crown','corona_hibiscus','flare_tulip'],'shrubs':['golden_brush','aurora_fern'],'fruits':['solar_mango','corona_pomegranate'],'crop':'sunroot_beet'}}
oldgroups={'moon':['lunar_turnip','pearl_carrot','orbit_pea'],'mars':['rust_beet','ares_chili','copper_onion'],
 'cerulon':['tidal_cucumber','reef_lettuce','azure_bean'],'skarn':['ember_radish','cinder_pepper','obsidian_aubergine'],
 'eidolon':['frost_cabbage','rime_parsnip','ghost_garlic'],'solvane':['solar_tomato','corona_corn','sunburst_squash']}
gourds={'nebula_melon':'cerulon','eclipse_pumpkin':'moon','aurora_melon':'eidolon','solar_melon':'solvane'}
files=[];families=[]
def write(rel,obj):
 path=res/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
def texture(id,im,kind='block'):
 rel=f'{kind}/{id}.png';path=base/'source'/rel;path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
 dest=res/f'assets/{ns}/textures'/rel;dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest)
 pack=res/'resourcepacks/visual_refresh'/f'assets/{ns}/textures'/rel
 if pack.exists():im.save(pack)
 files.append({'path':rel,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'size':list(im.size)})
def rgb(c,k=1):return tuple(max(0,min(255,round(v*k))) for v in c)+(255,)
def palette(theme):i=themes.index(theme);return leaves[i],fruits[i]
def title(id):return id.replace('_',' ').title()
def shade(im,seed):
 # Clustered pixel ramps, restrained grain and an upper-left highlight convention.
 source=im.copy();rng=random.Random(seed)
 for y in range(im.height):
  for x in range(im.width):
   c=source.getpixel((x,y))
   if not c[3]:continue
   light=.77+.27*(1-y/im.height)+.05*(1-x/im.width)
   if x>0 and y>0 and not source.getpixel((x-1,y-1))[3]:light+=.20
   if x<im.width-1 and y<im.height-1 and not source.getpixel((x+1,y+1))[3]:light-=.17
   light+=rng.choice([-.018,0,0,.018]);im.putpixel((x,y),rgb(c[:3],light))
 return im
def leaf(d,x,y,spread,c,right=True):
 sign=1 if right else -1
 d.polygon([(x,y),(x+sign*spread,y-6),(x+sign*(spread+2),y-3),(x+sign*2,y+1)],fill=rgb(c))
 d.line([(x,y),(x+sign*(spread-1),y-3)],fill=rgb(c,1.26),width=1)
def bud(d,x,y,c,size=3,kind='round'):
 if kind=='pod':
  d.rounded_rectangle((x-2,y-1,x+2,y+size*3),radius=2,fill=rgb(c,.68))
  for sy in range(y+1,y+size*3,3):d.ellipse((x-1,sy,x+1,sy+2),fill=rgb(c,1.2))
 elif kind=='chili':
  d.polygon([(x-2,y),(x+3,y),(x+2,y+6),(x-2,y+10),(x,y+5)],fill=rgb(c))
  d.line([(x,y+1),(x,y+5)],fill=rgb(c,1.3))
 else:
  d.ellipse((x-size,y-size,x+size,y+size+1),fill=rgb(c,.94))
  d.line((x-1,y-size+1,x-2,y),fill=rgb(c,1.4),width=1)
  d.point((x+2,y+2),fill=rgb(c,.55))
def flower(theme,index,id):
 green,c=palette(theme);im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
 d.line([(15,31),(16,24),(14,17),(16,10)],fill=rgb(green,.7),width=2)
 leaf(d,15,27,8,green,False);leaf(d,15,23,8,green,True)
 style=0 if any(s in id for s in ['bell','snowdrop','lantern']) else 3 if 'torchflower' in id else 5 if any(s in id for s in ['tulip','lily','iris']) else 4 if any(s in id for s in ['dahlia','camellia','hibiscus']) else 2 if any(s in id for s in ['daisy','anemone','crown']) else 1
 if style==0:
  for x,y in [(11,14),(21,9)]:
   d.line((15,22,x,y-4),fill=rgb(green,.8));d.polygon([(x-4,y-5),(x+3,y-5),(x+5,y+3),(x-4,y+3),(x-5,y)],fill=rgb(c))
   d.line((x-2,y-3,x-2,y+1),fill=rgb(c,1.35));d.rectangle((x-3,y+2,x+3,y+3),fill=rgb(c,.58))
 elif style in [1,2,4]:
  petals=4 if 'poppy' in id else 5 if 'orchid' in id else 6 if style==1 else 8
  for n in range(petals):
   angle=n*math.tau/petals;px=16+round(math.cos(angle)*6);py=10+round(math.sin(angle)*6)
   d.ellipse((px-4,py-3,px+4,py+3),fill=rgb(c,.9+n%2*.16))
   d.line((16,10,px,py),fill=rgb(c,.64))
  d.ellipse((13,7,19,13),fill=(247,204,104,255));d.point((14,8),fill=(255,248,201,255))
  if style==4:
   d.ellipse((12,6,20,14),fill=rgb(c,.65));d.arc((13,7,19,13),20,270,fill=rgb(c,1.35))
 elif style==3:
  for y,w in [(15,5),(10,4),(5,2)]:
   d.polygon([(16-w,y),(16,y-5),(16+w,y),(19,y+3),(13,y+3)],fill=rgb(c))
   d.line((16,y-3,16,y+1),fill=(255,225,149,255))
 else:
  d.polygon([(8,9),(12,4),(16,9),(21,3),(25,9),(22,18),(13,18)],fill=rgb(c))
  d.line((13,9,15,15),fill=rgb(c,1.35),width=2)
 return shade(im,theme+str(index))
def shrub(theme,index):
 green,c=palette(theme);im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
 for j in range(5):
  x=5+j*5;top=7+(j*3+index*2)%9;d.line((16,31,x,top),fill=rgb(green,.56),width=2)
  for y in range(top+4,29,5):leaf(d,x,y,3+(index+j)%3,green,j%2==0)
  if index%2:bud(d,x,top,c,1+(j%2))
 return shade(im,theme+str(index))
def crop(theme,id,age):
 green,c=palette(theme);im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
 root=any(k in id for k in ['turnip','carrot','radish','beet','onion','garlic','parsnip','sunroot'])
 leafy=any(k in id for k in ['lettuce','cabbage','broccoli','artichoke'])
 legume='pea' in id or 'bean' in id;corn='corn' in id
 height=[7,15,23,29][age]
 for j,x in enumerate([9,21] if not leafy else [12,19]):
  d.line((x,31,x+(1 if j else -1),32-height),fill=rgb(green,.6),width=2)
  for y in range(29,32-height+2,-6):
   leaf(d,x,y,3+age,green,j%2==0);leaf(d,x,y-2,3+age,green,j%2!=0)
  if age==1:bud(d,x,32-height,c,1)
  if age>=2:
   if root:
    bud(d,x,28,c,3+int(age==3));d.line((x,28,x-1,31),fill=rgb(c,.7))
   elif leafy:
    for xx,yy in [(x-3,22),(x+2,19),(x,26)]:
     d.ellipse((xx-4,yy-4,xx+4,yy+4),fill=rgb(c,.75 if age==2 else 1))
     d.arc((xx-3,yy-3,xx+3,yy+3),170,330,fill=rgb(c,1.3))
   elif legume:
    for yy in [12,22] if age==3 else [20]:bud(d,x+3,yy,c if age==3 else green,2,'pod')
    d.line([(x,8),(x-4,4),(x-6,8)],fill=rgb(green,1.2))
   elif 'asparagus' in id:
    tip=6 if age==3 else 13
    d.rectangle((x+2,tip+4,x+4,29),fill=rgb(c));d.line((x+2,tip+5,x+2,28),fill=rgb(c,1.3))
    d.polygon([(x+1,tip+5),(x+3,tip),(x+5,tip+5)],fill=rgb(green,1.2))
   elif corn:
    for yy in range(6,18,3):d.rectangle((x-2,yy,x+3,yy+1),fill=rgb(c,1.12))
   else:
    for yy in [12,24] if age==3 else [22]:bud(d,x+3,yy,c,3,'chili' if 'chili' in id or 'okra' in id else 'round')
 return shade(im,id+str(age))
def fruiticon(theme,id,seed=False):
 green,c=palette(theme);im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
 if seed:
  for x,y in [(9,21),(17,12),(23,22)]:bud(d,x,y,c,3)
 elif 'slice' in id:
  d.polygon([(4,9),(28,9),(24,23),(16,29),(7,23)],fill=rgb(green,.8))
  d.polygon([(6,10),(26,10),(22,21),(16,25),(9,21)],fill=rgb(c));d.line((8,11,24,11),fill=rgb(c,1.4),width=2)
  for x,y in [(11,16),(19,17),(16,21)]:d.rectangle((x,y,x+1,y+2),fill=rgb(c,.35))
 else:
  kind='pod' if 'pea' in id or 'bean' in id else 'chili' if 'okra' in id or 'chili' in id else 'round'
  if 'asparagus' in id:
   for x,top in [(9,8),(15,4),(22,10)]:
    d.rectangle((x-1,top+4,x+2,28),fill=rgb(c));d.line((x,top+5,x,27),fill=rgb(c,1.3))
    d.polygon([(x-2,top+5),(x,top),(x+3,top+5)],fill=rgb(green))
  elif any(s in id for s in ['cherry','coalberry']):
   for x,y in [(10,23),(22,24)]:bud(d,x,y,c,5)
   d.line([(10,19),(16,6),(22,20)],fill=rgb(green,.7),width=2)
  elif 'pear' in id or 'fig' in id:
   d.polygon([(13,6),(19,6),(20,15),(25,22),(23,28),(9,28),(6,22),(12,15)],fill=rgb(c))
   d.line((12,15,10,22),fill=rgb(c,1.35),width=2)
  elif 'date' in id or 'mango' in id:
   d.ellipse((8,6,23,29),fill=rgb(c));d.arc((10,8,20,27),130,270,fill=rgb(c,1.4),width=2)
   d.line((16,10,16,26),fill=rgb(c,.65))
  elif kind=='round':
   d.ellipse((6,9,26,28),fill=rgb(c));d.arc((9,11,22,26),145,250,fill=rgb(c,1.4),width=2)
   if any(s in id for s in ['broccoli','artichoke','cabbage','lettuce']):
    for x,y in [(11,13),(19,12),(15,19)]:bud(d,x,y,c,5)
   if 'corn' in id or 'asparagus' in id:
    for y in range(12,26,4):d.line((9,y,23,y),fill=rgb(c,.5));d.line((12,y,12,y+3),fill=rgb(c,1.4))
  else:
   for x,y in [(10,9),(19,6)]:bud(d,x,y,c,5,kind)
  d.line((16,10,16,5),fill=rgb(green,.65),width=2);leaf(d,16,10,7,green,True)
  if 'pomegranate' in id:d.polygon([(12,10),(11,4),(15,6),(18,3),(20,9)],fill=rgb(c,.8))
 return shade(im,id)
def cross(id):write(f'assets/{ns}/models/block/{id}.json',{'parent':'minecraft:block/cross','render_type':'minecraft:cutout','textures':{'cross':ns+':block/'+id}})
def icon(id):write(f'assets/{ns}/models/item/{id}.json',{'parent':'minecraft:item/generated','textures':{'layer0':ns+':item/'+id}})
def states(id,variants):write(f'assets/{ns}/blockstates/{id}.json',{'variants':variants})
def drop(block,item,count=1,condition=None):
 entry={'type':'minecraft:item','name':ns+':'+item,'functions':[{'function':'minecraft:set_count','count':count}]}
 if condition:entry['conditions']=[condition]
 return {'rolls':1,'entries':[entry]}
def loot(block,pools):write(f'data/{ns}/loot_table/blocks/{block}.json',{'type':'minecraft:block','pools':pools})
def recipe(id,ingredients,result,count=1):write(f'data/{ns}/recipe/{id}.json',{'type':'minecraft:crafting_shapeless','ingredients':[{'item':ns+':'+x} for x in ingredients],'result':{'id':result if ':' in result else ns+':'+result,'count':count}})
def mature(id,age):return {'condition':'minecraft:block_state_property','block':ns+':'+id,'properties':{'age':str(age)}}
lang=json.loads((res/f'assets/{ns}/lang/en_us.json').read_text())
for theme in themes:
 row=catalog[theme]
 for category in ['flowers','shrubs']:
  for i,id in enumerate(row[category]):
   texture(id,flower(theme,themes.index(theme)*3+i,id) if category=='flowers' else shrub(theme,i))
   cross(id);states(id,{'':{'model':ns+':block/'+id}})
   write(f'assets/{ns}/models/item/{id}.json',{'parent':'minecraft:item/generated','textures':{'layer0':ns+':block/'+id}})
   loot(id,[drop(id,id)]);lang['block.'+ns+'.'+id]=title(id);families.append({'id':id,'category':category,'home':theme})
   if category=='flowers':recipe(id+'_dye',[id],'minecraft:'+['purple','orange','pink','yellow','light_blue','magenta'][themes.index(theme)]+'_dye')
 for id in row['fruits']:
  fruit=id+'_buds';texture(id,fruiticon(theme,id),'item');icon(id)
  variants={}
  for age in range(3):
   green,c=palette(theme);skin=Image.new('RGBA',(32,32));sd=ImageDraw.Draw(skin)
   basecolour=c if age==2 else green
   for yy in range(32):
    for xx in range(32):
     ramp=.56+.31*(1-abs(xx-11)/24)+.18*(1-yy/32)
     if xx%7==0:ramp-=.12
     skin.putpixel((xx,yy),rgb(basecolour,ramp))
   sd.line((6,5,6,20),fill=rgb(basecolour,1.3),width=2);sd.line((25,13,25,28),fill=rgb(basecolour,.5))
   texture(fruit+f'_stage{age}',skin)
   tex=ns+':block/'+fruit+f'_stage{age}';w=2+age;bottom=7-age*2
   faces={face:{'uv':[0,0,16,16],'texture':'#fruit'} for face in ['north','east','south','west','up','down']}
   # Original miniature fruit block plus thin attachment stalk, matching cocoa pivots.
   model={'textures':{'fruit':tex,'particle':tex},'texture_size':[32,32],'render_type':'minecraft:cutout',
    'elements':[{'from':[8-w,bottom,1],'to':[8+w,12,1+2*w],'faces':faces},
                {'from':[7.5,12,0],'to':[8.5,13,3],'faces':faces}]}
   write(f'assets/{ns}/models/block/{fruit}_stage{age}.json',model)
   for facing,rot in [('north',0),('east',90),('south',180),('west',270)]:variants[f'age={age},facing={facing}']={'model':ns+':block/'+fruit+f'_stage{age}','y':rot}
  states(fruit,variants);loot(fruit,[drop(fruit,id),drop(fruit,id,2,mature(fruit,2))])
  lang['item.'+ns+'.'+id]=title(id);lang['block.'+ns+'.'+fruit]=title(id)+' Buds';families.append({'id':id,'category':'tree_fruit','home':theme})
 for id in oldgroups[theme]+[row['crop']]:
  variants={}
  for age in range(4):
   tex=id+f'_stage{age}';texture(tex,crop(theme,id,age));cross(tex);variants[f'age={age}']={'model':ns+':block/'+tex}
  states(id+'_crop',variants)
  if id==row['crop']:
   texture(id,fruiticon(theme,id),'item');texture(id+'_seeds',fruiticon(theme,id,True),'item');icon(id);icon(id+'_seeds')
  loot(id+'_crop',[drop(id+'_crop',id+'_seeds'),drop(id+'_crop',id,2,mature(id+'_crop',3)),drop(id+'_crop',id+'_seeds',2,mature(id+'_crop',3))])
  recipe(id+'_to_seeds',[id],id+'_seeds',2)
  lang['item.'+ns+'.'+id]=title(id);lang['item.'+ns+'.'+id+'_seeds']=title(id)+' Seeds';lang['block.'+ns+'.'+id+'_crop']=title(id)+' Crop'
  if id==row['crop']:families.append({'id':id,'category':'crop','home':theme})
for id,theme in gourds.items():
 green,c=palette(theme)
 for face in ['side','top']:
  im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
  for y in range(32):
   for x in range(32):
    stripe=(math.cos(x/32*math.tau*6)+1)*.5 if face=='side' else (math.cos(math.atan2(y-15.5,x-15.5)*6)+1)*.5
    im.putpixel((x,y),rgb(c,.52+stripe*.35+(31-y)*.008))
  if face=='top':d.rectangle((14,14,17,17),fill=rgb(green,.5));d.point((14,14),fill=rgb(green,1.25))
  texture(id+'_'+face,im)
 write(f'assets/{ns}/models/block/{id}.json',{'parent':'minecraft:block/cube_bottom_top','textures':{'side':ns+':block/'+id+'_side','top':ns+':block/'+id+'_top','bottom':ns+':block/'+id+'_top'}})
 states(id,{'':{'model':ns+':block/'+id}});write(f'assets/{ns}/models/item/{id}.json',{'parent':ns+':block/'+id})
 for suffix in ['_slice','_seeds']:texture(id+suffix,fruiticon(theme,id+suffix,suffix=='_seeds'),'item');icon(id+suffix);lang['item.'+ns+'.'+id+suffix]=title(id+suffix)
 for suffix in ['_stem','_attached_stem']:texture(id+suffix,crop(theme,id,3))
 for age in range(8):write(f'assets/{ns}/models/block/{id}_stem{age}.json',{'parent':f'minecraft:block/stem_growth{age}','render_type':'minecraft:cutout','textures':{'stem':ns+':block/'+id+'_stem'}})
 states(id+'_stem',{f'age={age}':{'model':ns+':block/'+id+f'_stem{age}'} for age in range(8)})
 write(f'assets/{ns}/models/block/{id}_attached_stem.json',{'parent':'minecraft:block/stem_fruit','render_type':'minecraft:cutout','textures':{'stem':ns+':block/'+id+'_stem','upperstem':ns+':block/'+id+'_attached_stem'}})
 states(id+'_attached_stem',{f'facing={face}':{'model':ns+':block/'+id+'_attached_stem','y':rotation} for face,rotation in [('north',0),('east',90),('south',180),('west',270)]})
 loot(id,[drop(id,id+'_slice',4)]);loot(id+'_stem',[drop(id+'_stem',id+'_seeds')]);loot(id+'_attached_stem',[drop(id+'_attached_stem',id+'_seeds')])
 recipe(id+'_slices_to_seeds',[id+'_slice'],id+'_seeds');recipe(id+'_slices_to_block',[id+'_slice']*9,id)
 lang['block.'+ns+'.'+id]=title(id)
 if id in ['aurora_melon','solar_melon']:families.append({'id':id,'category':'gourd','home':theme})
# Full 64px continuous tall silhouette, sliced into matching 32px native lower/upper sprites.
dimthemes=json.loads((a.code/'tools/planet_materials.json').read_text())['dimension_themes']
for dim,theme in dimthemes.items():
 green,c=palette(theme);rng=random.Random(dim)
 for tall in [False,True]:
  h=64 if tall else 32;im=Image.new('RGBA',(32,h));d=ImageDraw.Draw(im)
  for n in range(13):
   x=2+n*2;top=rng.randint(3,25 if tall else 20);lean=rng.randint(-6,6)
   d.polygon([(x-1,h-1),(x+1,h-1),(x+lean,top),(x+lean-1,top+8)],fill=rgb(green,.75+n%4*.1))
   d.line((x,h-2,x+lean,top+2),fill=rgb(green,1.2))
   if n%4==0:
    for yy in range(top+5,h-10,9):leaf(d,x+lean//2,yy,3,green,n%2==0)
   if tall and n%5==0:
    for yy in range(top,top+7,2):d.rectangle((x+lean-1,yy,x+lean+1,yy+1),fill=rgb(c,1.15))
  im=shade(im,dim+str(tall))
  if tall:texture(dim+'_tall_grass',im.crop((0,32,32,64)));texture(dim+'_tall_grass_top',im.crop((0,0,32,32)))
  else:texture(dim+'_short_grass',im)
write(f'assets/{ns}/lang/en_us.json',lang)
def merge_tag(path,ids):
 old=json.loads((res/path).read_text()) if (res/path).exists() else {'values':[]}
 old['values']=list(dict.fromkeys(old.get('values',[])+ids));write(path,old)
flowers=[ns+':'+id for row in catalog.values() for id in row['flowers']]
for tag in ['flowers','small_flowers']:merge_tag(f'data/minecraft/tags/block/{tag}.json',flowers);merge_tag(f'data/minecraft/tags/item/{tag}.json',flowers)
newseeds=[ns+':'+row['crop']+'_seeds' for row in catalog.values()]+[ns+':aurora_melon_seeds',ns+':solar_melon_seeds']
merge_tag('data/minecraft/tags/item/villager_plantable_seeds.json',newseeds)
compost=json.loads((res/'data/neoforge/data_maps/item/compostables.json').read_text())
for row in families:
 id=row['id'];compost['values'][ns+':'+id]={'chance':.65}
 if row['category'] in ['crop','gourd']:compost['values'][ns+':'+id+'_seeds']={'chance':.3}
write('data/neoforge/data_maps/item/compostables.json',compost)
for chest in (res/f'data/{ns}/loot_table/chests').glob('*.json'):
 data=json.loads(chest.read_text());data['pools']=[pool for pool in data.get('pools',[]) if pool.get('name')!='planet_botany_seeds_v2']
 data['pools'].append({'name':'planet_botany_seeds_v2','rolls':1,'entries':[{'type':'minecraft:item','name':id,'functions':[{'function':'minecraft:set_count','count':2}]} for id in newseeds]})
 write(str(chest.relative_to(res)),data)
assert len(families)==50
# Editable native Java-block projects, embedded original texture, no fragile file paths.
bbdir=base/'blockbench';bbdir.mkdir(exist_ok=True)
for row in families:
 id=row['id'];category=row['category'];texid=id
 if category=='tree_fruit':texid=id+'_buds_stage2'
 elif category=='crop':texid=id+'_stage3'
 elif category=='gourd':texid=id+'_side'
 raw=(base/'source/block'/f'{texid}.png').read_bytes()
 texuuid=str(uuid.uuid5(uuid.NAMESPACE_URL,'zerog-botany-texture/'+id))
 def cube(label,lo,hi,rotation=None):
  el={'name':label,'uuid':str(uuid.uuid5(uuid.NAMESPACE_URL,'zerog-botany-cube/'+id+'/'+label)),
      'type':'cube','from':lo,'to':hi,'origin':[8,8,8],
      'faces':{f:{'uv':[0,0,32,32],'texture':0} for f in ['north','east','south','west','up','down']}}
  if rotation:el['rotation']=rotation
  return el
 if category=='tree_fruit':
  native=json.loads((res/f'assets/{ns}/models/block/{id}_buds_stage2.json').read_text())
  elements=[cube('mature_fruit' if n==0 else 'attachment_stalk',c['from'],c['to']) for n,c in enumerate(native['elements'])]
 elif category=='gourd':elements=[cube('ribbed_melon',[0,0,0],[16,16,16])]
 else:
  elements=[cube('foliage_plane_a',[.7,0,8],[15.3,16,8],[0,45,0]),cube('foliage_plane_b',[.7,0,8],[15.3,16,8],[0,-45,0])]
 textures=[{'name':texid+'.png','uuid':texuuid,'id':'0','width':32,'height':32,
            'source':'data:image/png;base64,'+base64.b64encode(raw).decode()}]
 if category=='gourd':
  top=(base/'source/block'/f'{id}_top.png').read_bytes()
  textures.append({'name':id+'_top.png','uuid':str(uuid.uuid5(uuid.NAMESPACE_URL,'zerog-botany-top/'+id)),
                   'id':'1','width':32,'height':32,'source':'data:image/png;base64,'+base64.b64encode(top).decode()})
  for face in ['up','down']:elements[0]['faces'][face]['texture']=1
 project={'meta':{'format_version':'4.10','model_format':'java_block','box_uv':False},
          'name':id,'model_identifier':id,'resolution':{'width':32,'height':32},
          'elements':elements,'outliner':[el['uuid'] for el in elements],
          'textures':textures}
 (bbdir/(id+'.bbmodel')).write_text(json.dumps(project,indent=2)+'\n')
(base/'manifest.json').write_text(json.dumps({'original_art':True,'license':'All Rights Reserved','resolution':32,'new_families':families,'textures':files,'catalogue':catalog,'gourds':gourds},indent=2)+'\n')
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf' if Path('C:/Windows/Fonts/segoeui.ttf').exists() else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
def sheet(rows,file,cols=6):
 width=cols*190;height=math.ceil(len(rows)/cols)*150+50;im=Image.new('RGB',(width,height),(16,25,34));d=ImageDraw.Draw(im)
 d.text((15,12),file.replace('-',' ').replace('.png','').title()+' | Original source art, not game capture',font=font,fill=(222,235,239))
 for i,(label,tex) in enumerate(rows):
  x=i%cols*190;y=i//cols*150+48;art=Image.open(base/'source'/tex).resize((96,96),Image.Resampling.NEAREST)
  im.paste(art,(x+45,y),art);d.text((x+8,y+107),label,font=font,fill=(202,225,231))
 im.save(base/file)
sheet([(title(row['id']),('item/' if row['category'] in ['tree_fruit','crop','gourd'] else 'block/')+row['id']+('_slice' if row['category']=='gourd' else '')+'.png') for row in families],'fifty-new-varieties.png')
sheet([(title(id)+' '+str(age),'block/'+id+f'_stage{age}.png') for id in ['orbit_pea','lunar_snap_pea','solar_tomato','glacier_broccoli','reef_artichoke','corona_corn'] for age in range(4)],'crop-growth-stages.png',4)
sheet([(title(theme)+' grass','block/'+theme+'_short_grass.png') for theme in themes]+[(title(theme)+' tall top','block/'+theme+'_tall_grass_top.png') for theme in themes],'grass-and-tall-grass.png')
frames=[]
for age in range(4):
 frame=Image.new('RGB',(600,180),(16,25,34));d=ImageDraw.Draw(frame);d.text((10,8),'Growth '+str(age)+' / 3 — original texture preview',font=font,fill=(220,235,238))
 for i,id in enumerate(['orbit_pea','solar_tomato','glacier_broccoli','reef_artichoke']):
  art=Image.open(base/'source/block'/f'{id}_stage{age}.png').resize((128,128),Image.Resampling.NEAREST);frame.paste(art,(i*150+10,30),art)
 frames.append(frame)
frames[0].save(base/'budding-growth.gif',save_all=True,append_images=frames[1:],duration=850,loop=0)
print(f'Built {len(families)} new botany families, {len(files)} original PNG sources and growth previews.')
