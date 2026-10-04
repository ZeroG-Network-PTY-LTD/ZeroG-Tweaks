"""Read-only latest botanical overlay, growth geometry and packaged identity audit."""
import argparse, base64, hashlib, io, json
from collections import Counter
from pathlib import Path
from zipfile import ZipFile
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--design-root',type=Path,required=True);p.add_argument('--jar',type=Path,required=True);a=p.parse_args()
source=a.design_root/'docs/planet-botany-v2';m=json.loads((source/'manifest.json').read_text())
root=Path(__file__).resolve().parents[1]/'src/main/resources'
families=m['new_families'];assert len(families)==len({r['id'] for r in families})==50
assert Counter(r['category'] for r in families)=={'flowers':18,'shrubs':12,'tree_fruit':12,'crop':6,'gourd':2}
assert m['original_art'] and m['resolution']==32
projects=list((source/'blockbench').glob('*.bbmodel'));assert len(projects)==50
for path in projects:
 model=json.loads(path.read_text());ids={el['uuid'] for el in model['elements']}
 assert set(model['outliner'])==ids and model['resolution']=={'width':32,'height':32}
 for texture in model['textures']:
  with Image.open(io.BytesIO(base64.b64decode(texture['source'].split(',')[1]))) as im:assert im.size==(32,32)
 for el in model['elements']:
  assert all(x<=y for x,y in zip(el['from'],el['to']))
  for face in el['faces'].values():assert all(0<=v<=32 for v in face['uv']) and 0<=face['texture']<len(model['textures'])
with ZipFile(a.jar) as jar:
 for row in m['textures']:
  data=(source/'source'/row['path']).read_bytes();assert hashlib.sha256(data).hexdigest()==row['sha256']
  name='assets/zerog_tweaks/textures/'+row['path'];assert data==jar.read(name)==(root/name).read_bytes(),name
  im=Image.open(io.BytesIO(data));assert im.size==(32,32) and im.getbbox(),name
 for row in families:
  id=row['id'];assert f'assets/zerog_tweaks/models/item/{id}.json' in jar.namelist(),id
  if row['category']=='tree_fruit':
   states=json.loads(jar.read(f'assets/zerog_tweaks/blockstates/{id}_buds.json'))['variants'];assert len(states)==12
   for age in range(3):
    model=json.loads(jar.read(f'assets/zerog_tweaks/models/block/{id}_buds_stage{age}.json'))
    assert len(model['elements'])==2
    for cube in model['elements']:
     assert all(x<=y for x,y in zip(cube['from'],cube['to']))
     for face in cube['faces'].values():assert all(0<=v<=16 for v in face['uv'])
  if row['category']=='flowers':assert f'data/zerog_tweaks/recipe/{id}_dye.json' in jar.namelist()
 seeds=json.loads(jar.read('data/minecraft/tags/item/villager_plantable_seeds.json'))['values'];assert len(seeds)==len(set(seeds))==37
 assert not any('/gametest/' in name for name in jar.namelist()),'Test class leaked'
with Image.open(source/'budding-growth.gif') as gif:assert gif.n_frames==4 and gif.info['loop']==0
print(f'PASS: 50 unique botany families; {len(m["textures"])} source/runtime/JAR PNG identities; 12 three-stage tree fruits, 37 plantable seeds; preview loop; no test classes.')
