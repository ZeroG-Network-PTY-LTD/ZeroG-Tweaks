"""Read-only source/runtime/JAR validation for the approved native art overlay."""
import argparse, hashlib, io, json
from pathlib import Path
from zipfile import ZipFile
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--design-root',type=Path,required=True);p.add_argument('--jar',type=Path,required=True);a=p.parse_args()
source=a.design_root/'docs/wood-dust-art-v2';m=json.loads((source/'manifest.json').read_text())
res=Path(__file__).resolve().parents[1]/'src/main/resources';assert m['resolution']==32 and m['original_art']
assert len(m['wood_families'])==4;paths=[r['path'] for r in m['textures']];assert len(paths)==len(set(paths))
assert {p.name for p in (res/'assets/zerog_tweaks/textures/item').glob('*dust.png')}=={Path(p).name for p in paths if p.startswith('item/')}
with ZipFile(a.jar) as jar:
 for row in m['textures']:
  data=(source/'source'/row['path']).read_bytes();assert hashlib.sha256(data).hexdigest()==row['sha256']
  name='assets/zerog_tweaks/textures/'+row['path'];assert data==(res/name).read_bytes()==jar.read(name),name
  im=Image.open(io.BytesIO(data)).convert('RGBA');assert im.size==(32,32) and im.getbbox()
  # Clean ring faces intentionally use five stepped shades, not random noise.
  colors={p[:3] for p in im.getdata() if p[3]};assert len(colors)>=5,row['path']
  if '_leaves.png' in row['path']:
   transparent=sum(p[3]==0 for p in im.getdata());assert 50<transparent<800,(row['path'],transparent)
   model=json.loads(jar.read('assets/zerog_tweaks/models/block/'+Path(row['path']).stem+'.json'))
   assert model.get('render_type')=='minecraft:cutout_mipped'
  if row['path'].startswith('item/'):
   assert im.getpixel((0,0))[3]==0 and im.getpixel((31,31))[3]==0
   assert any(max(c)-min(c)>12 for c in colors),'Dust has no material color'
 for wood in m['wood_families']:
  model=json.loads(jar.read(f'assets/zerog_tweaks/models/item/{wood}_log.json'))
  assert model['parent']==f'zerog_tweaks:block/{wood}_log'
  log=json.loads(jar.read(f'assets/zerog_tweaks/models/block/{wood}_log.json'))
  assert log['textures']['side']==f'zerog_tweaks:block/{wood}_log'
  assert log['textures']['end']==f'zerog_tweaks:block/{wood}_log_top'
 assert not any('/gametest/' in n and n.endswith('.class') for n in jar.namelist())
print(f'PASS: {len(paths)} original 32px texture identities; all dust coverage; leaf cutouts; inventory/placed log bindings; no test classes.')
