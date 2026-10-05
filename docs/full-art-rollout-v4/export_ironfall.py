"""Faithful runtime export of the repository's existing Ironfall source.

Uses reviewed project-local codec functions; no new artwork or provider job.
"""
import argparse, ast, base64, hashlib, io, json
from pathlib import Path
from PIL import Image

parser=argparse.ArgumentParser()
parser.add_argument('--code',type=Path,required=True)
args=parser.parse_args()
base=Path(__file__).resolve().parent
source=base.parent/'shattered-skies/blockbench/meteor_maw_ironfall.bbmodel'
codec=base.parent/'zero-g-tweaks-bundle/generators/export_approved_tidewraiths.py'
tree=ast.parse(codec.read_text())
names={'point','angles','export_geo','negate','vector','export_animations','texture'}
ns={'base64':base64}
exec(compile(ast.Module(body=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in names],type_ignores=[]),str(codec),'exec'),ns)
obj=json.loads(source.read_text());key='meteor_maw_ironfall'
geo=ns['export_geo'](obj,key);animations=ns['export_animations'](obj,key);png=ns['texture'](obj)
image=Image.open(io.BytesIO(png));assert image.size==(obj['resolution']['width'],obj['resolution']['height'])
bone_names={bone['name'] for bone in geo['minecraft:geometry'][0]['bones']}
for clip in animations['animations'].values():
    assert set(clip['bones']).issubset(bone_names)
    for channels in clip['bones'].values():
        assert set(channels).issubset({'rotation','position','scale'})
files={f'assets/zerog_tweaks/geo/{key}.geo.json':(json.dumps(geo,indent=2)+'\n').encode(),
       f'assets/zerog_tweaks/animations/{key}.animation.json':(json.dumps(animations,indent=2)+'\n').encode(),
       f'assets/zerog_tweaks/textures/entity/{key}.png':png}
for rel,data in files.items():
    for folder in [base/'source',args.code/'src/main/resources']:
        dst=folder/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
receipt={'source':str(source.relative_to(base.parent.parent)),
         'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
         'codec':str(codec.relative_to(base.parent.parent)),
         'codec_sha256':hashlib.sha256(codec.read_bytes()).hexdigest(),
         'authored_scale_multiplier':1,'texture_size':list(image.size),
         'bones':sorted(bone_names),'cube_count':len(obj['elements']),
         'clips':list(animations['animations']),
         'conversion':'Existing codec: X reflection, XY rotation sign conversion, up/down UV-direction reversal; no geometry redesign.',
         'files':{key:hashlib.sha256(data).hexdigest() for key,data in files.items()},
         'gpu_verified':False,'canonical_package_admission':False}
(base/'ironfall-export-manifest.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'cubes':receipt['cube_count'],'bones':len(bone_names),'texture':receipt['texture_size'],'clips':receipt['clips']}))
