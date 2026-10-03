"""Read-only audit of all current colour/family liquid IDs and bucket/animation art."""
import argparse, hashlib, json, struct
from zipfile import ZipFile
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--jar',type=Path,required=True);p.add_argument('--design',type=Path,required=True);a=p.parse_args()
manifest=json.loads((a.design/'manifest.json').read_text())
assert len(manifest['textures'])==18
with ZipFile(a.jar) as jar:
 for row in manifest['textures']:
  bucket=Path(row['path']).stem;id=bucket.removesuffix('_bucket')
  prefix='assets/zerog_tweaks/'
  data=jar.read(prefix+'textures/'+row['path'])
  assert hashlib.sha256(data).hexdigest()==row['sha256'],bucket
  model=json.loads(jar.read(prefix+'models/item/'+bucket+'.json'))
  assert model['parent']=='minecraft:item/generated'
  assert model['textures']=={'layer0':'minecraft:item/water_bucket','layer1':'zerog_tweaks:item/'+bucket},bucket
  assert prefix+'blockstates/'+id+'.json' in jar.namelist(),id
  for suffix in ['still','flow']:
   image=jar.read(prefix+'textures/block/'+id+'_'+suffix+'.png')
   width,height=struct.unpack('>II',image[16:24]);assert height>width and height%width==0,(id,suffix)
   meta=json.loads(jar.read(prefix+'textures/block/'+id+'_'+suffix+'.png.mcmeta'))['animation']
   frameheight=meta.get('height',width);assert height%frameheight==0,(id,suffix)
   for frame in meta.get('frames',range(height//frameheight)):
    index=frame['index'] if isinstance(frame,dict) else frame
    assert 0<=index<height//frameheight,(id,suffix,index)
 print('PASS: 18 distinct liquid block IDs, 18 exact vanilla-base bucket overlays, 36 still/flow animated texture strips.')
