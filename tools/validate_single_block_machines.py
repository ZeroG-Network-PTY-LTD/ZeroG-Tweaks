"""Single-cube/UV/animation, GUI-contract and repacked-addon byte evidence, not GPU proof."""
import argparse,base64,hashlib,io,json
from pathlib import Path
from zipfile import ZipFile
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--design',type=Path,required=True);p.add_argument('--jar',type=Path,required=True)
p.add_argument('--addon',type=Path,required=True);p.add_argument('--old-addon',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[1];base=a.design/'docs/single-block-machines-v1';m=json.loads((base/'manifest.json').read_text())
counts={'stardust_smelter':3,'starmetal_smelter':4,'silk_weaver':4,'gravitational_centrifuge':7,'centrifuge':7,
 'frame_assembler':3,'frame_component_assembler':3,'frame_infusion_altar':4,'infusion_altar':3,'genetic_splicer':4,'geno_station':2}
with ZipFile(a.jar) as jar,ZipFile(a.addon) as addon,ZipFile(a.old_addon) as old:
 for row in m['files']:
  name=row['path'];data=(base/'source'/name).read_bytes();assert hashlib.sha256(data).hexdigest()==row['sha256'],name
  assert data==(root/'src/main/resources'/name).read_bytes()==jar.read(name)==jar.read('resourcepacks/visual_refresh/'+name),name
  if name.startswith('assets/aeroapiary/'):assert addon.read(name)==data,name
  if name.endswith('.png'):
   im=Image.open(io.BytesIO(data));assert im.getbbox(),name
   if '/single_block/' in name:
    assert im.size==((32,128) if '_front.png' in name else (32,32))
    assert im.getextrema()[3]==(255,255),name
    assert len(im.getcolors(4096) or [])>=12,name
   elif '/gui/workbench/' in name:assert im.size==(256,256),name
 for id in m['single_block_ids']:
  model=json.loads(jar.read(f'assets/aeroapiary/models/block/other/{id}.json'))
  assert len(model['elements'])==1
  cube=model['elements'][0];assert cube['from']==[0,0,0] and cube['to']==[16,16,16]
  assert set(cube['faces'])=={'north','south','west','east','up','down'}
  for direction,face in cube['faces'].items():assert face['uv']==[0,0,16,16] and face['cullface']==direction
  assert json.loads(jar.read(f'assets/aeroapiary/models/item/{id}.json'))['parent']==f'aeroapiary:block/other/{id}'
  variants=json.loads(jar.read(f'assets/aeroapiary/blockstates/{id}.json'))['variants']
  assert {k:v.get('y',0) for k,v in variants.items()}=={'facing=north':0,'facing=east':90,'facing=south':180,'facing=west':270}
  anim=json.loads(jar.read(f'assets/aeroapiary/textures/block/single_block/{id}_front.png.mcmeta'))['animation']
  assert anim['frametime']==4 and not anim['interpolate']
 assert 'assets/aeroapiary/geo/machines/genetic_splicer.geo.json' not in addon.namelist()
 assert 'assets/aeroapiary/animations/genetic_splicer.animation.json' not in addon.namelist()
 for name in old.namelist():
  if name.endswith('.class') or (not name.endswith('/') and name.startswith(('data/','META-INF/'))):assert old.read(name)==addon.read(name),name
 for key,profile in m['profiles'].items():
  if profile['namespace']=='aeroapiary' and not profile['designOnly']:assert len(profile['slots'])==counts[profile['id']]
  elif profile['namespace']=='aeroapiary':
   assert profile['id'].endswith(('_hatch','_port')) and profile['pending']
   assert 'assets/aeroapiary/blockstates/'+profile['id']+'.json' in old.namelist()
  else:assert profile['designOnly'] and profile['pending']
  positions=profile['positions']+[[47+j%9*18,154+j//9*18 if j<27 else 212] for j in range(36)]
  assert len(set(tuple(xy) for xy in positions))==len(positions),key
  assert all(0<x<240 and 0<y<220 for x,y in positions),key
  # Reject even partial slot overlaps, not just equal origins.
  for i,(x,y) in enumerate(positions):
   for x2,y2 in positions[i+1:]:assert not(x<x2+16 and x2<x+16 and y<y2+16 and y2<y+16),key
 for cls in ['MachineGuiProfile','MachineWorkbenchScreen','MachineBlueprintScreen','MachineBlueprintScreen$Opening']:
  assert 'net/zerog/tweaks/client/'+cls+'.class' in jar.namelist()
 assert not any('/gametest/' in n and n.endswith('.class') for n in jar.namelist())
for path in m['projects']:
 obj=json.loads((base/path).read_text());assert obj['meta']['model_format']=='java_block'
 assert len(obj['elements'])==1 and obj['elements'][0]['from']==[0,0,0] and obj['elements'][0]['to']==[16,16,16]
 assert len(obj['textures'])==6
 for tex in obj['textures']:
  assert Image.open(io.BytesIO(base64.b64decode(tex['source'].split(',')[1]))).size==(32,32)
print('PASS: two single cubes/UVs and animated terminal strips; 11 real inventory layouts + six core-machine/registered service-module plans; all new source/runtime/pack/JAR bytes; addon classes/data unchanged. GPU review remains manual.')
