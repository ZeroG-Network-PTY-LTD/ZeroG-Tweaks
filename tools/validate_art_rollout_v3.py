"""Source/runtime/JAR identity and terminal-facing/art coverage, not GPU proof."""
import argparse, base64, collections, hashlib, io, json
from pathlib import Path
from zipfile import ZipFile
from PIL import Image
from art_source_layers import effective_art_sources

p=argparse.ArgumentParser();p.add_argument('--design-root',type=Path,required=True)
p.add_argument('--jar',type=Path,required=True);p.add_argument('--bee-jar',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[1]/'src/main/resources'
base=a.design_root/'docs/art-rollout-v3';manifest=json.loads((base/'manifest.json').read_text())
effective=effective_art_sources(a.design_root)
assert manifest['original_art'] and manifest['resolution']==32
assert len(manifest['controller_bindings'])==9
counts=collections.Counter(row['category'] for row in manifest['files'])
assert counts['cave_berries']==34 and counts['dripstone']==374 and counts['dripstone_items']==34
assert counts['gourds']==8 and counts['materials']>=80 and counts['vine_fruits']==6
with ZipFile(a.jar) as jar,ZipFile(a.bee_jar) as addon:
    for relative,data in effective.items():
        assert (root/relative).read_bytes()==jar.read(relative)==data,relative
        if (root/'resourcepacks/visual_refresh'/relative).exists():
            assert jar.read('resourcepacks/visual_refresh/'+relative)==data,relative
    for row in manifest['files']:
        name=row['path'];data=(base/'source'/name).read_bytes()
        assert hashlib.sha256(data).hexdigest()==row['sha256'],name
        if name.endswith('.png'):
            with Image.open(io.BytesIO(data)) as im:
                assert im.size==(32,32) and im.getbbox(),name
                assert len(im.getcolors(1024) or [])>=5,name
                if '/item/' in name or 'pointed_dripstone_' in name:
                    assert im.getextrema()[3]==(0,255),name
    for row in manifest['controller_bindings']:
        relative='assets/aeroapiary/models/'+row['model']+'.json'
        obj=json.loads(jar.read(relative));old=json.loads(addon.read(relative))
        if row.get('geometry_preserved'):
            assert len(obj['elements'])==len(old['elements'])
            for new_cube,old_cube in zip(obj['elements'],old['elements']):
                assert new_cube['from']==old_cube['from'] and new_cube['to']==old_cube['to']
            screen=next(c for c in obj['elements'] if c['from']==[4,5,1.4])
            assert screen['faces']['north']=={'uv':[0,0,16,16],'texture':'#terminal'}
        else:
            assert obj['textures']['north'].endswith('/controller_front')
            state=json.loads(addon.read('assets/aeroapiary/blockstates/'+row['id']+'.json'))['variants']
            assert {key:value.get('y',0) for key,value in state.items()}=={
                'facing=north':0,'facing=east':90,'facing=south':180,'facing=west':270}
        item=json.loads(addon.read('assets/aeroapiary/models/item/'+row['id']+'.json'))
        assert item['parent']=='aeroapiary:'+row['model']
    assert not any('/gametest/' in path and path.endswith('.class') for path in jar.namelist())
for relative in manifest['controller_projects']:
    obj=json.loads((a.design_root/relative).read_text());assert obj['meta']['model_format']=='java_block'
    assert set(obj['outliner'])=={e['uuid'] for e in obj['elements']}
    size=obj['resolution']['width']
    for cube in obj['elements']:
        for face in cube['faces'].values():
            assert all(0<=v<=size for v in face['uv'])
            assert 0<=face['texture']<len(obj['textures'])
    for texture in obj['textures']:
        with Image.open(io.BytesIO(base64.b64decode(texture['source'].split(',')[1]))) as im:
            assert im.size==(texture['width'],texture['height'])
for row in manifest['updated_existing_projects']:
    assert hashlib.sha256((a.design_root/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
print(f'PASS: {len(manifest["files"])} v3 payloads, nine terminal models/projects, {len(manifest["updated_existing_projects"])} refreshed editable projects; source/pack/runtime/JAR hashes. GPU/activation review is still required.')
