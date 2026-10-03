"""Read-only model/blockstate reference audit, including atlas-generated trim sprites."""
import argparse,json
from pathlib import Path
from zipfile import ZipFile
p=argparse.ArgumentParser();p.add_argument('--jar',type=Path,required=True);a=p.parse_args();root=Path(__file__).resolve().parents[1]
vanilla=next((root/'build/moddev/artifacts').glob('*client-extra*resources.jar'))
with ZipFile(vanilla) as v,ZipFile(a.jar) as j:
    names=set(v.namelist())|set(j.namelist());generated=set();errors=[];models=0;states=0
    def key(ref,kind,suffix):
        ns,path=ref.split(':',1) if ':' in ref else ('minecraft',ref)
        return f'assets/{ns}/{kind}/{path}{suffix}'
    def exists(ref,kind,suffix):
        target=key(ref,kind,suffix)
        if kind=='models' and '/builtin/' in target:return True
        return target in names or (kind=='textures' and target in generated)
    for jar in [v,j]:
        for name in jar.namelist():
            if '/atlases/' not in name or not name.endswith('.json'):continue
            for source in json.loads(jar.read(name)).get('sources',[]):
                if source.get('type','').removeprefix('minecraft:')!='paletted_permutations':continue
                for ref in [source['palette_key'],*source['textures'],*source['permutations'].values()]:
                    if not exists(ref,'textures','.png'):errors.append((name,ref))
                for texture in source['textures']:
                    for permutation in source['permutations']:generated.add(key(texture+'_'+permutation,'textures','.png'))
    def walk(obj,origin):
        if isinstance(obj,dict):
            for name,value in obj.items():
                if name=='model' and isinstance(value,str) and not exists(value,'models','.json'):errors.append((origin,value))
                else:walk(value,origin)
        elif isinstance(obj,list):
            for value in obj:walk(value,origin)
    for name in j.namelist():
        if not name.startswith('assets/zerog_tweaks/') or not name.endswith('.json'):continue
        if '/models/' in name:
            obj=json.loads(j.read(name));models+=1
            if 'parent' in obj and not exists(obj['parent'],'models','.json'):errors.append((name,obj['parent']))
            for ref in obj.get('textures',{}).values():
                if not ref.startswith('#') and not exists(ref,'textures','.png'):errors.append((name,ref))
            walk(obj.get('overrides',[]),name)
        elif '/blockstates/' in name:walk(json.loads(j.read(name)),name);states+=1
    if errors:
        for row in errors[:25]:print(row)
        raise SystemExit(f'FAIL: {len(errors)} unresolved references')
    print(f'PASS: {models} models, {states} blockstates, parent/direct texture and override references; {len(generated)} declared atlas-generated sprites with valid source/palette PNGs.')
