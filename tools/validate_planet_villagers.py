"""Validate original villager geometry/animation admission and runtime textures."""
import argparse,hashlib,json,zipfile,io
from pathlib import Path
from PIL import Image

parser=argparse.ArgumentParser()
parser.add_argument('--design',type=Path,required=True)
parser.add_argument('--jar',type=Path,required=True)
args=parser.parse_args()
root=args.design/'docs/zero-g-tweaks-bundle/blockbench/villagers'
species=['lunari','rustborn','glintfolk','ashwright','hollow_kin','sunwarden']
prefix='assets/zerog_tweaks/'
with zipfile.ZipFile(args.jar) as jar:
    names=set(jar.namelist())
    assert not any('GameTests.class' in n for n in names),'Test classes shipped'
    for mob in species:
        for suffix,target in [('geo.json','geo'),('animation.json','animations')]:
            assert jar.read(prefix+f'{target}/villagers/{mob}.{suffix}')==(root/mob/f'{mob}.{suffix}').read_bytes()
        model=json.loads(jar.read(prefix+f'geo/villagers/{mob}.geo.json'))['minecraft:geometry'][0]
        bones={b['name'] for b in model['bones']}
        assert len(bones)==len(model['bones'])
        for bone in model['bones']:
            assert not bone.get('parent') or bone['parent'] in bones
            for cube in bone.get('cubes',[]):
                assert len(cube['size'])==3 and all(v>=0 for v in cube['size'])
        animation=json.loads(jar.read(prefix+f'animations/villagers/{mob}.animation.json'))['animations']
        for required in ['idle','walk','no']:
            assert f'animation.{mob}.{required}' in animation
        if mob=='sunwarden':assert 'animation.sunwarden.halo_spin' in animation
        for anim in animation.values():assert set(anim.get('bones',{}))<=bones
        textures=[n for n in names if n.startswith(prefix+f'textures/entity/villager/{mob}/style_') and n.endswith('.png')]
        assert len(textures)==84,(mob,len(textures))
        size=(model['description']['texture_width'],model['description']['texture_height'])
        for texture in textures:
            image=Image.open(io.BytesIO(jar.read(texture)))
            assert image.size==size and image.mode=='RGBA'
        egg=json.loads(jar.read(prefix+f'models/item/{mob}_spawn_egg.json'))
        assert egg['parent']=='minecraft:item/template_spawn_egg'
print('PASS: six unchanged original geometries/animations, 504 RGBA textures, bone references, six native egg models; no shipped test classes.')
