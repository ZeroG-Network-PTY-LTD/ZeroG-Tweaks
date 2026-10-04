"""Read-only admission check; shader/GUI appearance still requires a client review."""
import argparse, io, json, zipfile
from pathlib import Path
from PIL import Image
from art_source_layers import effective_art_sources
p=argparse.ArgumentParser();p.add_argument('--jar',type=Path,required=True);p.add_argument('--design',type=Path,required=True);a=p.parse_args()
source=a.design/'docs/alien-vines-weather-v1';manifest=json.loads((source/'manifest.json').read_text())
prefix='assets/zerog_tweaks/'
effective=effective_art_sources(a.design)
with zipfile.ZipFile(a.jar) as jar:
    names=set(jar.namelist());assert not any('/gametest/' in name for name in names),'Test classes shipped'
    for row in manifest['vines']:
        id=row['id'];state=json.loads(jar.read(prefix+'blockstates/'+id+'.json'))
        assert 'multipart' in state and len(state['multipart'])>4
        textures=[id,id+'_ripe'] if id.endswith('fruit_ivy') else [id]
        for texture in textures:
            blob=jar.read(prefix+'textures/block/'+texture+'.png')
            assert blob==(source/'textures'/(texture+'.png')).read_bytes()
            image=Image.open(io.BytesIO(blob));assert image.mode=='RGBA' and image.size==(32,32)
            assert image.getextrema()[3]==(0,255),'Vine transparency missing'
            model=json.loads(jar.read(prefix+'models/block/'+texture+'.json'))
            assert model['render_type']=='minecraft:cutout'
            assert all('tintindex' not in face for element in model['elements'] for face in element['faces'].values())
        assert 'data/zerog_tweaks/loot_table/blocks/'+id+'.json' in names
    climbers=json.loads(jar.read('data/minecraft/tags/block/climbable.json'))['values']
    assert {'zerog_tweaks:pyrevine','zerog_tweaks:pyrevine_plant'}.issubset(climbers),'Existing climbing tags removed'
    assert len(climbers)==len(set(climbers))
    for row in manifest['vines']:assert 'zerog_tweaks:'+row['id'] in climbers
    for theme in manifest['palette_row_order']:
        relative=prefix+'textures/item/'+theme+'_vine_fruit.png'
        assert jar.read(relative)==effective.get(relative,(source/'textures'/(theme+'_vine_fruit.png')).read_bytes())
        assert prefix+'blockstates/'+theme+'_ambient_vent.json' in names
    panorama=jar.read(prefix+'textures/environment/universe_v3.png')
    assert panorama==(a.design/'docs/planet-worldgen-overhaul/source/universe_v3.png').read_bytes()
    assert Image.open(io.BytesIO(panorama)).size==(1774,887)
    assert json.loads(jar.read(prefix+'textures/environment/universe_v3.png.mcmeta'))['texture']['blur']
    assert json.loads(jar.read(prefix+'models/item/weather_tester.json'))['textures']['layer0']=='minecraft:item/clock_00'
print('PASS: 24 transparent native-plane vine models, six fruits/safe vent IDs, climbing tag preservation, panorama/source identity, weather item icon, no test-class leaks.')
