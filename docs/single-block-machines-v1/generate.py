"""Original native 32px machine faces and use-specific GUI layouts.
Single-cube replacements supersede, but never overwrite, historical design models.
Run with --code pointing at the 1.21.x checkout. No paid providers/game launch.
"""
import argparse,base64,hashlib,json,math,uuid
from zipfile import ZipFile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--code',type=Path,required=True);a=p.parse_args()
BASE=Path(__file__).resolve().parent;SOURCE=BASE/'source';RES=a.code/'src/main/resources'
FILES=[];PROJECTS=[]
PROFILES={
 'stardust_smelter':(['Comb','Fuel','Dust output'],2,'Smelt combs into stardust with fuel.',False),
 'starmetal_smelter':(['Alloy input','Alloy input','Flux','Alloy output'],3,'Combine metal inputs with flux.',False),
 'silk_weaver':(['Fibre','Fibre','Pattern','Silk output'],3,'Weave fibres using a pattern.',False),
 'gravitational_centrifuge':(['Comb']+['Product output']*6,1,'Separate combs into multiple products.',False),
 'centrifuge':(['Comb']+['Product output']*6,1,'Separate combs into multiple products.',False),
 'frame_assembler':(['Untreated frame','Frame material','Frame output'],2,'Assemble a frame using the installed recipe.',False),
 'frame_component_assembler':(['Untreated frame','Frame material','Frame output'],2,'Assemble frame components using the installed recipe.',False),
 'frame_infusion_altar':(['Frame','Infusion reagent','Infusion reagent','Frame output'],3,'Infuse a frame with a reagent.',False),
 'infusion_altar':(['Frame','Infusion reagent','Frame output'],2,'Infuse a frame with a reagent.',False),
 'genetic_splicer':(['Queen-like bee','Drone','Frame','Legacy output'],3,'Planned: bee + trait serum + catalyst -> spliced bee and vial.',True),
 'geno_station':(['Comb (legacy)','Legacy output'],1,'Planned: analyse a bee and sample a gene into a trait serum.',True),
}
PLANNED={
 'alloy_forge':(['Metal A','Metal B','Catalyst','Alloy output'],3,'Alloy two metals; optional catalyst and tier casing upgrades.'),
 'combustion_generator':(['Fuel','Residue output'],1,'Burn fuel to generate FE; show fuel burn time and energy buffer.'),
 'solar_array':([],0,'Generate FE from daylight, with output depending on the planet.'),
 'fusion_reactor':(['Fuel A','Fuel B','Catalyst','Residue output'],3,'Combine fusion fuels; monitor energy and reactor stability.'),
 'salvage_station':(['Salvage input']+['Recovered output']*6,1,'Break salvage into recovered materials; show energy and processing.'),
 'crystal_growth_chamber':(['Crystal seed','Feed material','Crystal output'],2,'Grow crystals from seed and feed; monitor FE and growth progress.'),
}
def title(id):return id.replace('_',' ').title()
def emit(rel,obj):
 path=SOURCE/rel;path.parent.mkdir(parents=True,exist_ok=True)
 if isinstance(obj,Image.Image):obj.save(path)
 else:path.write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
 data=path.read_bytes()
 for root in (RES,RES/'resourcepacks/visual_refresh'):
  target=root/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 FILES.append({'path':rel,'sha256':hashlib.sha256(data).hexdigest()})
def ramp(c,k):
 target=(38,31,62) if k<1 else (255,235,190);f=min(.28,abs(k-1)*.42)
 return tuple(max(0,min(255,round(v*k*(1-f)+t*f))) for v,t in zip(c,target))+(255,)
STEEL=(74,80,96);BRASS=(201,154,58);CYAN=(95,225,241);VIOLET=(166,111,228)
def panel(d,box,c):
 x,y,x2,y2=box;d.rectangle(box,fill=ramp(c,.72))
 d.line((x,y,x2,y),fill=ramp(c,1.25));d.line((x,y,x,y2),fill=ramp(c,1.1))
 d.line((x,y2,x2,y2),fill=ramp(c,.4));d.line((x2,y,x2,y2),fill=ramp(c,.48))
def surface(face,id,frame=0):
 im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
 for y in range(32):
  for x in range(32):im.putpixel((x,y),ramp(STEEL,.78+.25*(1-y/32)+.12*(1-x/32)+(.025 if (x//3+y//3)%3==0 else 0)))
 panel(d,(0,0,31,31),STEEL);panel(d,(2,2,29,29),STEEL)
 for x,y in [(3,3),(27,3),(3,27),(27,27)]:
  d.rectangle((x,y,x+1,y+1),fill=ramp(BRASS,1.2));d.point((x+1,y+1),fill=ramp(BRASS,.45))
 d.line((5,4,26,4),fill=ramp(BRASS,1.1));d.line((5,5,26,5),fill=ramp(BRASS,.55))
 if face=='front':
  panel(d,(5,7,26,23),BRASS);panel(d,(7,9,24,21),(26,43,60))
  colour=VIOLET if id=='genetic_splicer' else CYAN
  if id=='genetic_splicer':
   for yy in range(10,21):
    off=round(3*math.sin((yy+frame)*.65));x=15+off
    d.point((x,yy),fill=ramp(colour,1.15));d.point((30-x,yy),fill=ramp(CYAN,1.04))
    if yy%3==1:d.line((min(x,30-x),yy,max(x,30-x),yy),fill=ramp(BRASS,.75))
  else:
   for i,h in enumerate([3,7,5,9,4]):
    x=10+i*3;d.rectangle((x,20-h,x+1,20),fill=ramp(colour,.73+i*.1))
   d.line((8,11+frame*2,23,11+frame*2),fill=ramp(VIOLET,1.15))
  d.line((8,10,22,10),fill=ramp(CYAN,.5));d.point((8,11),fill=(207,255,255,255))
  for x,c in [(9,CYAN),(15,BRASS),(21,VIOLET)]:
   panel(d,(x,25,x+2,27),c);d.point((x,25),fill=ramp(c,1.32))
 elif face in ('left','right','back'):
  panel(d,(6,8,25,23),STEEL)
  for y in range(10,23,3):
   d.line((8,y,23,y),fill=ramp(STEEL,.35));d.line((8,y+1,23,y+1),fill=ramp(STEEL,1.08))
  d.line((5,25,25,25),fill=ramp(BRASS,.8))
 else:
  panel(d,(6,7,25,24),BRASS)
  for y in range(10,22,4):
   for x in range(9,24,5):
    d.polygon([(x,y-1),(x+2,y),(x+2,y+2),(x,y+3),(x-2,y+2),(x-2,y)],outline=ramp(STEEL,.48))
 return im
def slots(roles,start):
 n=len(roles);positions=[]
 for i in range(n):
  if i<start:
   positions.append(([48,76,62][i] if start>1 else 62,38 if i<2 else 62))
  else:
   j=i-start;positions.append((188,50) if n-start==1 else (170+j%3*18,38+j//3*18))
 return positions
def gui(roles,start,accent):
 im=Image.new('RGBA',(256,256));d=ImageDraw.Draw(im)
 panel(d,(0,0,255,235),(198,198,198));d.line((3,2,251,2),fill=ramp(BRASS,1.08),width=2)
 panel(d,(8,19,113,75),(155,150,141));panel(d,(145,19,247,75),(155,150,141))
 for x,y in slots(roles,start):panel(d,(x-1,y-1,x+16,y+16),(110,106,98))
 panel(d,(12,79,243,85),(75,67,60));d.rectangle((128,30,135,64),fill=ramp(accent,.35))
 d.polygon([(124,45),(136,45),(136,39),(143,51),(136,63),(136,56),(124,56)],fill=ramp(accent,1.08))
 panel(d,(8,90,247,135),(167,163,153))
 for i in range(36):
  x=47+i%9*18;y=154+i//9*18 if i<27 else 212
  panel(d,(x-1,y-1,x+16,y+16),(110,106,98))
 return im
profiles={}
for id,(roles,start,purpose,pending) in PROFILES.items():
 profiles['aeroapiary:'+id]={'id':id,'namespace':'aeroapiary','slots':roles,'outputStart':start,'purpose':purpose,'pending':pending,'designOnly':False,'positions':slots(roles,start)}
for id,(roles,start,purpose) in PLANNED.items():
 profiles['zerog_tweaks:'+id]={'id':id,'namespace':'zerog_tweaks','slots':roles,'outputStart':start,'purpose':purpose,'pending':True,'designOnly':True,'positions':slots(roles,start)}
addon=a.code.parent/'zerog-docs-integrated/docs/jars/zerog-binnie-expansion-1.21.1-1.0.0.jar'
with ZipFile(addon) as jar:
 for path in jar.namelist():
  if not path.startswith('assets/aeroapiary/blockstates/') or not path.endswith('.json'):continue
  id=Path(path).stem
  if not id.startswith('tier') or not id.endswith(('_hatch','_port')):continue
  kind='Energy' if 'energy' in id else 'Honey' if 'honey' in id else 'Fluid' if 'fluid' in id else 'Pressure' if 'pressure' in id else 'Items'
  direction='Output' if 'output' in id else 'Input' if 'input' in id else 'Service'
  purpose=f'{kind} {direction.lower()} module. Planned: side routing, controller binding and buffer inspection.'
  profiles['aeroapiary:'+id]={'id':id,'namespace':'aeroapiary','slots':[],'outputStart':0,'purpose':purpose,'pending':True,'designOnly':True,'positions':[],'metrics':[kind+' buffer','Side mode','Controller']}
METRICS={'alloy_forge':['FE buffer','Tier bonus','Process time'],
 'combustion_generator':['Fuel burn','FE stored','FE output'],
 'solar_array':['Daylight','Planet factor','FE output'],
 'fusion_reactor':['Fuel mix','Stability','FE stored'],
 'salvage_station':['FE buffer','Recovery','Process time'],
 'crystal_growth_chamber':['FE buffer','Growth','Feed level']}
for key,profile in profiles.items():
 accent=VIOLET if 'gen' in profile['id'] or profile['designOnly'] else BRASS
 profile['metrics']=profile.get('metrics',METRICS.get(profile['id'],[]))
 image=gui(profile['slots'],profile['outputStart'],accent)
 if profile['designOnly']:
  d=ImageDraw.Draw(image);d.rectangle((43,150,214,231),fill=(167,163,153,255))
  for i in range(3):panel(d,(12+i*80,153,83+i*80,190),(103,103,115))
 emit('assets/zerog_tweaks/textures/gui/workbench/'+profile['id']+'.png',image)
emit('assets/zerog_tweaks/gui/machine_profiles.json',profiles)
lang_path=RES/'assets/zerog_tweaks/lang/en_us.json';lang=json.loads(lang_path.read_text(encoding='utf-8'))
for key,value in {
 'inputs':'Inputs','outputs':'Outputs','cycle':'Cycle: %s','legacy_cycle':'Legacy cycle: %s',
 'pending':'Backend pending','genetics_pending':'Genetics processing is not implemented. The displayed slots keep the installed legacy filters; no trait sampling or splicing is performed by this screen.',
 'blueprint':'Read-only plan — processing not implemented','inventory_diagram':'Inventory layout (planned)',
 'no_storage':'No live storage or processing','planned_metrics':'Planned monitoring (not live)'}.items():lang['screen.zerog_tweaks.workbench.'+key]=value
emit('assets/zerog_tweaks/lang/en_us.json',lang)
for id in ['genetic_splicer','geno_station']:
 face_names=['front','back','left','right','top','bottom'];textures={}
 for face in face_names:
  rel=f'assets/aeroapiary/textures/block/single_block/{id}_{face}.png'
  if face=='front':
   im=Image.new('RGBA',(32,128))
   for i in range(4):im.alpha_composite(surface(face,id,i),(0,i*32))
   emit(rel,im);emit(rel+'.mcmeta',{'animation':{'frametime':4,'interpolate':False}})
  else:emit(rel,surface(face,id))
  textures[face]=f'aeroapiary:block/single_block/{id}_{face}'
 textures['particle']=textures['left']
 mapping={'north':'front','south':'back','west':'left','east':'right','up':'top','down':'bottom'}
 element={'from':[0,0,0],'to':[16,16,16],'faces':{direction:{'uv':[0,0,16,16],'texture':'#'+face,'cullface':direction} for direction,face in mapping.items()}}
 model={'parent':'minecraft:block/block','textures':textures,'elements':[element]}
 emit(f'assets/aeroapiary/models/block/other/{id}.json',model)
 emit(f'assets/aeroapiary/models/item/{id}.json',{'parent':f'aeroapiary:block/other/{id}'})
 emit(f'assets/aeroapiary/blockstates/{id}.json',{'variants':{f'facing={name}':{'model':f'aeroapiary:block/other/{id}','y':rot,'uvlock':False} for name,rot in [('north',0),('east',90),('south',180),('west',270)]}})
 images=[surface(face,id) for face in face_names];uid=str(uuid.uuid5(uuid.NAMESPACE_URL,'zerog/'+id+'/single-cube'))
 cube={'name':title(id),'type':'cube','uuid':uid,'from':[0,0,0],'to':[16,16,16],'autouv':0,'faces':{direction:{'uv':[0,0,32,32],'texture':face_names.index(face),'cullface':direction} for direction,face in mapping.items()}}
 embedded=[]
 import io
 for face,im in zip(face_names,images):
  stream=io.BytesIO();im.save(stream,format='PNG');embedded.append({'name':id+'_'+face+'.png','uuid':str(uuid.uuid5(uuid.NAMESPACE_URL,id+face)),'source':'data:image/png;base64,'+base64.b64encode(stream.getvalue()).decode(),'width':32,'height':32,'uv_width':32,'uv_height':32})
 obj={'meta':{'format_version':'4.10','model_format':'java_block','box_uv':False},'name':title(id),'resolution':{'width':32,'height':32},'elements':[cube],'outliner':[uid],'textures':embedded}
 path=BASE/'blockbench'/f'{id}.bbmodel';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2)+'\n');PROJECTS.append(path.relative_to(BASE).as_posix())
# Unambiguous contact sheet of native face pixels; no claim of in-game rendering.
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16) if Path('C:/Windows/Fonts/consola.ttf').exists() else ImageFont.load_default()
sheet=Image.new('RGB',(960,290),(27,28,35));d=ImageDraw.Draw(sheet)
for row,id in enumerate(['genetic_splicer','geno_station']):
 d.text((12,row*140+6),title(id)+' — single cube, native 32px faces',font=font,fill=(232,220,183))
 for col,face in enumerate(['front','left','right','back','top','bottom']):
  sheet.paste(surface(face,id).resize((96,96),Image.Resampling.NEAREST),(12+col*158,row*140+30));d.text((12+col*158,row*140+126),face,font=font,fill=(185,192,209))
sheet.save(BASE/'single-block-faces.png')
for id in ['genetic_splicer','geno_station']:
 frames=[surface('front',id,i).resize((256,256),Image.Resampling.NEAREST).convert('RGB') for i in range(4)]
 frames[0].save(BASE/(id+'-terminal.gif'),save_all=True,append_images=frames[1:],duration=200,loop=0,disposal=2)
for id in ['genetic_splicer','geno_station','gravitational_centrifuge','alloy_forge']:
 profile=next(v for v in profiles.values() if v['id']==id);im=gui(profile['slots'],profile['outputStart'],VIOLET);d=ImageDraw.Draw(im)
 d.text((8,5),title(id),fill=(55,48,41));d.text((15,23),'INPUTS',fill=(55,48,41));d.text((155,23),'OUTPUTS',fill=(55,48,41))
 d.text((12,94),'Design / backend pending' if profile['pending'] else 'Existing recipe processing',fill=(55,48,41));d.text((47,143),'Inventory',fill=(55,48,41))
 im.crop((0,0,256,236)).resize((768,708),Image.Resampling.NEAREST).save(BASE/(id+'-gui-preview.png'))
 (BASE/(id+'-layout.json')).write_text(json.dumps(profile,indent=2)+'\n')
(BASE/'manifest.json').write_text(json.dumps({'original_art':True,'single_block_ids':['genetic_splicer','geno_station'],'files':FILES,'projects':PROJECTS,'profiles':profiles,'evidence':'native sources and offline previews; GPU review pending'},indent=2)+'\n')
print('Generated two single-cube models; 11 live-menu, six core-machine and 20 service-module GUI designs.')
