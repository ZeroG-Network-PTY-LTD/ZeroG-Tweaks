"""Read-only validation of layered ecology/bee artwork, UVs and jar packaging."""
import argparse,base64,hashlib,io,json
from pathlib import Path
from zipfile import ZipFile
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--design-root',type=Path,required=True);p.add_argument('--jar',type=Path,required=True);a=p.parse_args()
code=Path(__file__).resolve().parents[1];res=code/'src/main/resources';base=a.design_root/'docs/asset-collection-1.21.1';latest={};count=0
for revision in ['dimension-ecology-v1','miniature-planet-bees-v1','planet-blazes-v1','vanilla-liquid-buckets-v1']:
    root=base/revision;manifest=json.loads((root/'manifest.json').read_text())
    for row in manifest['textures']:
        data=(root/'textures'/row['path']).read_bytes();assert hashlib.sha256(data).hexdigest()==row['sha256'],row['path']
        with Image.open(io.BytesIO(data)) as im:assert list(im.size)==row['size']
        latest[row['path']]=data
    for path in (root/'blockbench').glob('*.bbmodel'):
        model=json.loads(path.read_text());width=model['resolution']['width'];height=model['resolution']['height'];ids={el['uuid'] for el in model['elements']}
        def check(nodes):
            for node in nodes:
                if isinstance(node,str):assert node in ids,(path.name,node)
                else:check(node.get('children',[]))
        check(model['outliner'])
        for t in model['textures']:
            with Image.open(io.BytesIO(base64.b64decode(t['source'].split(',',1)[1]))) as im:assert im.size==(t['width'],t['height']),path.name
        for el in model['elements']:
            assert all(el['from'][i]<=el['to'][i] for i in range(3)),path.name
            for face in el['faces'].values():
                u,v,u2,v2=face['uv'];assert 0<=u<=width and 0<=u2<=width and 0<=v<=height and 0<=v2<=height,path.name
                assert 0<=int(face['texture'])<len(model['textures']),path.name
        count+=1
with ZipFile(a.jar) as jar:
    for name,data in latest.items():
        relative='assets/zerog_tweaks/textures/'+name
        assert data==(res/relative).read_bytes()==jar.read(relative),relative
    assert not any('/gametest/' in n or '/tidewraithgametest/' in n or 'AssetReview' in n for n in jar.namelist()),'Test class leak'
    for path in (base/'miniature-planet-bees-v1/textures/block').glob('*.mcmeta'):
        relative='assets/zerog_tweaks/textures/block/'+path.name;assert path.read_bytes()==jar.read(relative)
        meta=json.loads(path.read_text())['animation'];assert meta['frametime']==3
    for key in json.loads((base/'miniature-planet-bees-v1/manifest.json').read_text())['families']:
        for frame in range(8):
            with Image.open(res/f'assets/zerog_tweaks/textures/entity/{key}_glowbug_frame_{frame}.png') as im:
                for x in [6,15]:assert any(im.getpixel((xx,yy))[3]>0 for xx in range(x,x+9) for yy in range(18,24)),(key,'Missing wing UV')
    for path in (res/'data/zerog_tweaks/recipe').glob('*_star_sand_to_star_glass.json'):
        recipe=json.loads(path.read_text());assert recipe['result']['id']=='zerog_tweaks:star_glass' and recipe['cookingtime']==200
    assert len(list((res/'data/zerog_tweaks/recipe').glob('*_star_sand_to_star_glass.json')))==34
    for row in json.loads((base/'vanilla-liquid-buckets-v1/manifest.json').read_text())['textures']:
        model_path='assets/zerog_tweaks/models/item/'+Path(row['path']).stem+'.json'
        model=json.loads(jar.read(model_path));assert model['textures']['layer0']=='minecraft:item/water_bucket'
        assert model['textures']['layer1']=='zerog_tweaks:item/'+Path(row['path']).stem
        assert row['liquid_pixels']>8
for name in ['dimension_fluids_reference.gif','../miniature-planet-bees-v1/miniature_bees_texture_animation.gif']:
    with Image.open(base/'dimension-ecology-v1'/name) as im:assert im.n_frames>=8 and im.info['loop']==0
print(f'PASS: {len(latest)} final texture payloads and jar hashes; {count} editable projects/UVs; both bee wing faces; 34 furnace recipes; PNG metadata/GIF loops; no test classes.')
