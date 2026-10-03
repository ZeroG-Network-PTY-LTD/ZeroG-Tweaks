"""Admit original Design villagers to GeckoLib 4 runtime paths; no source art edits."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--code-root',type=Path,required=True)
    args=parser.parse_args()
    source=Path(__file__).resolve().parents[2]/'blockbench'/'villagers'
    assets=args.code_root/'src/main/resources/assets/zerog_tweaks'
    receipts=[]
    lang_path=assets/'lang/en_us.json'
    lang=json.loads(lang_path.read_text(encoding='utf-8'))
    names={'lunari':'Lunari','rustborn':'Rustborn','glintfolk':'Glintfolk','ashwright':'Ashwright',
           'hollow_kin':'Hollow Kin','sunwarden':'Sunwarden'}
    for species,name in names.items():
        folder=source/species
        geo=json.loads((folder/f'{species}.geo.json').read_text())
        animation=json.loads((folder/f'{species}.animation.json').read_text())
        bones={b['name'] for b in geo['minecraft:geometry'][0]['bones']}
        for anim in animation['animations'].values():
            assert set(anim.get('bones',{}))<=bones,(species,'missing animation bone')
        for suffix,target in [('geo.json','geo'),('animation.json','animations')]:
            src=folder/f'{species}.{suffix}'
            dest=assets/target/'villagers'/src.name
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(src,dest)
        variants=[folder/f'{species}.png']+sorted(p for p in folder.glob(f'{species}_*.png') if not p.name.endswith('_glowmask.png'))
        assert len(variants)==3,(species,variants)
        texture_folder=assets/'textures/entity/villager'/species
        texture_folder.mkdir(parents=True,exist_ok=True)
        mask=Image.open(folder/f'{species}_glowmask.png').convert('RGBA')
        for style,base_path in enumerate(variants):
            base=Image.open(base_path).convert('RGBA')
            description=geo['minecraft:geometry'][0]['description']
            assert base.size==(description['texture_width'],description['texture_height'])
            for job in ['none','armorer','butcher','cartographer','cleric','farmer','fisherman','fletcher',
                        'leatherworker','librarian','mason','shepherd','toolsmith','weaponsmith']:
                texture=base.copy()
                if job!='none':texture=Image.alpha_composite(texture,Image.open(folder/'professions'/f'{job}.png').convert('RGBA'))
                filename=f'style_{style}_{job}'
                texture.save(texture_folder/f'{filename}.png')
                mask.save(texture_folder/f'{filename}_glowmask.png')
        egg=assets/'models/item'/f'{species}_spawn_egg.json'
        egg.write_text(json.dumps({'parent':'minecraft:item/template_spawn_egg'},indent=2)+'\n')
        lang[f'entity.zerog_tweaks.{species}']=name
        lang[f'item.zerog_tweaks.{species}_spawn_egg']=name+' Spawn Egg'
        receipts.append({'species':species,'texture_size':base.size,'styles':3,'native_professions':13,
                         'source_geometry_sha256':hashlib.sha256((folder/f'{species}.geo.json').read_bytes()).hexdigest(),
                         'source_animation_sha256':hashlib.sha256((folder/f'{species}.animation.json').read_bytes()).hexdigest()})
    lang_path.write_text(json.dumps(lang,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (Path(__file__).parent/'runtime-admission.json').write_text(json.dumps({'format':'GeckoLib 4 / Minecraft Java 1.21.1','sources_unchanged':True,
          'species':receipts,'runtime_pngs':504,'gpu_visual_review':'pending','signature_professions':'not implemented'},indent=2)+'\n')
    print('Six original geometries/animations, 504 runtime textures, six native spawn eggs exported.')

if __name__=='__main__':main()
