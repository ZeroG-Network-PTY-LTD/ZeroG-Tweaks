"""Read-only packaged artifact checks, NOT gameplay/server tests."""
import argparse, base64, hashlib, io, json
from pathlib import Path
from zipfile import ZipFile
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--design-root',type=Path,required=True);p.add_argument('--jar',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[1];res=root/'src/main/resources';revision=a.design_root/'docs/asset-collection-1.21.1/planet-art-refresh-v1'
spec=json.loads((root/'tools/planet_materials.json').read_text());manifest=json.loads((revision/'manifest.json').read_text());materials=json.loads((root/'tools/planet_material_art_manifest.json').read_text())
def read(relative):return json.loads((res/relative).read_text())
assert len(spec['dimension_themes'])==34 and len(materials)==12
with ZipFile(a.jar) as jar:
 for row in manifest['files']:
  source=(revision/'resource-source'/row['path']).read_bytes();assert hashlib.sha256(source).hexdigest()==row['sha256']
  overlay=a.design_root/'docs/planet-botany-v2/source'/row['path'].removeprefix('assets/zerog_tweaks/textures/')
  if row['path'].startswith('assets/zerog_tweaks/textures/') and overlay.exists():source=overlay.read_bytes()
  assert source==jar.read(row['path'])==(res/row['path']).read_bytes(),row['path']
  im=Image.open(io.BytesIO(source));assert list(im.size)==row['size'];assert im.getbbox(),row['path']
  if im.height>32:
   meta=json.loads(jar.read(row['path']+'.mcmeta'))['animation'];assert im.height%im.width==0 and meta['frametime']==4 and meta['interpolate']
 for path in (res/'resourcepacks/visual_refresh').rglob('*'):
  if path.is_file():assert path.read_bytes()==jar.read('resourcepacks/visual_refresh/'+path.relative_to(res/'resourcepacks/visual_refresh').as_posix())
 assert not any('/gametest/' in n or '/tidewraithgametest/' in n for n in jar.namelist())
 for rec in materials:
  for id in rec['blocks']:
   assert f'assets/zerog_tweaks/blockstates/{id}.json' in jar.namelist()
   assert f'data/zerog_tweaks/loot_table/blocks/{id}.json' in jar.namelist()
  feature='ore_'+rec['id'];cfg=json.loads(jar.read(f'data/zerog_tweaks/worldgen/configured_feature/{feature}.json'))
  assert cfg['config']['size']==(3 if rec['gem'] else 8)
 for planet,family in spec['families'].items():
  modifier=read(f'data/zerog_tweaks/neoforge/biome_modifier/planet_minerals_{planet}.json')
  for dim,theme in spec['dimension_themes'].items():
   if theme!=planet:continue
   definition=read('data/zerog_tweaks/dimension/'+dim+'.json');biomes={v['biome'] for v in definition['generator']['biome_source']['biomes']}
   assert biomes<=set(modifier['biomes']),dim
  crop=family['crop'];states=read('assets/zerog_tweaks/blockstates/'+crop+'_crop.json')
  assert set(states['variants'])=={f'age={x}' for x in range(4)}
  assert read('data/zerog_tweaks/recipe/'+crop+'_seeds_from_harvest.json')['result']['id']=='zerog_tweaks:'+crop+'_seeds'
 for path in (res/'data/zerog_tweaks/neoforge/biome_modifier').glob('*blaze*.json'):
  obj=json.loads(path.read_text());assert all(s['weight']==1 and s['minCount']==s['maxCount']==1 for s in obj['spawners'])
for path in (revision/'blockbench').glob('*.bbmodel'):
 obj=json.loads(path.read_text());w,h=obj['resolution']['width'],obj['resolution']['height']
 for tex in obj['textures']:
  im=Image.open(io.BytesIO(base64.b64decode(tex['source'].split(',')[1])));assert im.size==(tex['width'],tex['height'])
 for cube in obj['elements']:
  assert all(x<=y for x,y in zip(cube['from'],cube['to']))
  for face in cube['faces'].values():
   u,v,u2,v2=face['uv'];assert 0<=u<=w and 0<=u2<=w and 0<=v<=h and 0<=v2<=h
print(f'PASS: {len(manifest["files"])} packaged PNG hashes, animated strips, built-in repair pack, {len(materials)} mineral families, 34 dimension bindings, crop stage/seed recipes, rare Blaze data, editable UVs; no test classes.')
