"""Read-only original art, crop data and cave-family identity checks."""
import argparse,hashlib,json
from pathlib import Path
from zipfile import ZipFile
p=argparse.ArgumentParser();p.add_argument('--design',type=Path,required=True);p.add_argument('--jar',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[1];res=root/'src/main/resources';manifest=json.loads((a.design/'manifest.json').read_text())
assert manifest['crop_families']==20 and manifest['cave_families']==34
with ZipFile(a.jar) as jar:
 for row in manifest['textures']:
  name='assets/zerog_tweaks/textures/'+row['path'];data=(a.design/'source'/row['path']).read_bytes()
  assert hashlib.sha256(data).hexdigest()==row['sha256'],name
  assert data==jar.read(name)==(res/name).read_bytes(),name
 assert not any('/gametest/' in name for name in jar.namelist()),'Test classes leaked'
 themes=json.loads((root/'tools/planet_materials.json').read_text())['dimension_themes']
 for dim in themes:
  for suffix in ['_cave_vines','_cave_vines_plant','_pointed_dripstone','_dripstone_block']:
   assert f'assets/zerog_tweaks/blockstates/{dim}{suffix}.json' in jar.namelist()
  assert f'assets/zerog_tweaks/models/item/{dim}_cave_berry.json' in jar.namelist()
 seeds=json.loads(jar.read('data/minecraft/tags/item/villager_plantable_seeds.json'))['values'];assert len(seeds)==len(set(seeds))==29
 assert {'zerog_tweaks:rust_tuber_seeds','zerog_tweaks:solflower_seeds','zerog_tweaks:moon_millet_seeds'}.issubset(seeds),'Original seed registrations lost'
 for id in seeds:
  assert f'assets/zerog_tweaks/models/item/{id.split(":")[1]}.json' in jar.namelist()
print(f'PASS: {len(manifest["textures"])} original PNG hashes/packaged payloads; 20 seeds, 34 cave families; no test classes.')
