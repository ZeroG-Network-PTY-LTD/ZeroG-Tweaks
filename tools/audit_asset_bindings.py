"""Read-only model/texture reference check against a built jar and installed mods.

Checks native PNG and animation metadata, but does not certify client visuals.
"""
import argparse
import hashlib
import io
import json
import tomllib
from pathlib import Path
from zipfile import ZipFile
from PIL import Image

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--jar',required=True,type=Path)
parser.add_argument('--mods',required=True,type=Path)
parser.add_argument('--report',required=True,type=Path)
parser.add_argument('--manifest',type=Path,help='Optional approved native source/hash manifest')
args=parser.parse_args()
resources={}; owned={}; errors=[]; external=set()
packaged={}
for path in sorted(args.mods.glob('*.jar')):
    with ZipFile(path) as jar:
        mod_meta=next((n for n in ['META-INF/neoforge.mods.toml','META-INF/mods.toml'] if n in jar.namelist()),None)
        if mod_meta and any(m.get('modId')=='zerog_tweaks' for m in tomllib.loads(jar.read(mod_meta).decode()).get('mods',[])):
            continue  # Installed Tweaks will be replaced; its stale assets must not mask omissions.
        for name in jar.namelist():
            if name.startswith('assets/') and name.endswith(('.json','.png','.mcmeta')):
                resources[name]=jar.read(name)
with ZipFile(args.jar) as jar:
    names=jar.namelist()
    packaged={name:jar.read(name) for name in names if name.endswith(('.json','.png','.mcmeta'))}
    tests=[n for n in names if '/gametest/' in n or n.startswith('data/zerog_tweaks/structure/equipment_empty')]
    if tests: errors.append({'test_classes_or_fixtures_in_production':tests[:8]})
    for name in names:
        if name.startswith('assets/') and name.endswith(('.json','.png','.mcmeta')):
            owned[name]=jar.read(name)
    resources.update(owned)
    # The active built-in overlay must resolve against the same complete asset set.
    overlay={n.removeprefix('resourcepacks/visual_refresh/'):jar.read(n) for n in names
             if n.startswith('resourcepacks/visual_refresh/assets/') and n.endswith(('.json','.png','.mcmeta'))}
    resources.update(overlay);owned.update(overlay)

def reference(source,ref,kind):
    if not isinstance(ref,str) or ref.startswith('#'):return
    ns,_,relative=ref.partition(':')
    if not _:ns,relative='minecraft',ref
    if ns=='minecraft':return
    target=f'assets/{ns}/{kind}/{relative}'+('.png' if kind=='textures' else '.json')
    if target not in resources:
        if ns in {'zerog_tweaks','aeroapiary','shatteredskies'}:errors.append({'source':source,'missing':target})
        else:external.add(target)

def models(source,data):
    if isinstance(data,dict):
        if 'model' in data:reference(source,data['model'],'models')
        for value in data.values():models(source,value)
    elif isinstance(data,list):
        for value in data:models(source,value)

counts={'models':0,'blockstates':0,'pngs':0,'animation_metadata':0,'source_byte_bindings':0}
if args.manifest:
    manifest=json.loads(args.manifest.read_text())
    for row in manifest.get('files',[])+manifest.get('models',[]):
        layers=set(row.get('layers',[row['path']]))
        layers.update(name for name in packaged if name.startswith('resourcepacks/') and name.endswith('/'+row['path']))
        for name in sorted(layers):
            counts['source_byte_bindings']+=1
            if name not in packaged:
                errors.append({'source':row['path'],'missing_packaged_source':name})
            elif hashlib.sha256(packaged[name]).hexdigest()!=row['sha256']:
                errors.append({'source':row['path'],'packaged_bytes_differ':name})
for name,raw in owned.items():
    try:
        if '/models/' in name and name.endswith('.json'):
            counts['models']+=1;data=json.loads(raw)
            reference(name,data.get('parent'),'models')
            for texture in data.get('textures',{}).values():reference(name,texture,'textures')
            for override in data.get('overrides',[]):reference(name,override.get('model'),'models')
        elif '/blockstates/' in name and name.endswith('.json'):
            counts['blockstates']+=1;models(name,json.loads(raw))
        elif name.endswith('.png'):
            counts['pngs']+=1
            with Image.open(io.BytesIO(raw)) as im:im.verify()
        elif name.endswith('.png.mcmeta'):
            meta=json.loads(raw).get('animation')
            if meta is None:continue
            counts['animation_metadata']+=1
            with Image.open(io.BytesIO(resources[name.removesuffix('.mcmeta')])) as im:
                width=meta.get('width',im.width);height=meta.get('height',width)
                if width<=0 or height<=0 or im.width%width or im.height%height:raise ValueError('Invalid animation grid')
                frames=im.width//width*(im.height//height)
                for frame in meta.get('frames',[]):
                    index=frame.get('index') if isinstance(frame,dict) else frame
                    if not isinstance(index,int) or not 0<=index<frames:raise ValueError('Animation index outside texture')
    except Exception as ex:errors.append({'source':name,'error':str(ex)})
result={'scope':'Reference, PNG and animation-grid audit; not GPU or in-game approval',
        'checked':counts,'errors':errors,'error_count':len(errors),'external_unverified':sorted(external)}
args.report.parent.mkdir(parents=True,exist_ok=True)
args.report.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checked':counts,'error_count':len(errors),'report':str(args.report)},indent=2))
raise SystemExit(bool(errors))
