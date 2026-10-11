"""Original native 32px dimension-metal cogs and pressed plates; no fabrication costs.

Run with --code pointing at the 1.21.x checkout. Palette ramps are the approved
style kit, not multiplicative recolours. All source art is retained on Design.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
KIT = ROOT.parent / 'art-direction/generator/style_kit.py'
spec = importlib.util.spec_from_file_location('zg_style', KIT)
kit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kit)
GROUPS = {
    'moon': ('moonsteel', ['moonsteel', 'lunarium']),
    'mars': ('copper', ['ferrox', 'olympium', 'aresium']),
    'cerulon': ('cerulite', ['cobaltium', 'cyrrium', 'aurelion', 'azurium']),
    'skarn': ('copper', ['ruskite', 'tectium', 'pyrium', 'basaltine']),
    'eidolon': ('moonsteel', ['salvium', 'wraithsteel', 'palladine', 'rime_nickel']),
    'solvane': ('solvanite', ['photium', 'radiantine', 'astrium', 'helion']),
}

def sprite(kind, ramp):
    im = Image.new('RGBA', (32, 32))
    d = ImageDraw.Draw(im)
    r = kit.R[ ramp ]
    if kind == 'cog':
        # Eight broad, balanced teeth; a visible bore, dark extrusion and bevel.
        points = []
        for i in range(32):
            angle = i * math.tau / 32 - math.pi / 2
            radius = 13 if i % 4 in (0, 1) else 10
            points.append((round(15.5 + math.cos(angle)*radius),
                           round(14.5 + math.sin(angle)*radius)))
        d.polygon([(x,y+2) for x,y in points], fill=r[0])
        d.polygon(points, fill=r[2])
        for i, p in enumerate(points):
            q = points[(i+1)%len(points)]
            d.line([p,q], fill=r[5] if p[0]+p[1]<29 else r[1])
        d.ellipse((8,7,23,22), fill=r[4])
        d.ellipse((10,9,21,20), fill=r[1])
        d.ellipse((12,11,19,18), fill=(0,0,0,0))
        d.arc((8,7,23,22), 180, 280, fill=r[5], width=1)
        # Selective violet machined inlays, not a surrounding fake glow.
        for x,y in ((7,14),(23,14),(15,6),(15,23)):
            d.point((x,y),fill=kit.R['glow'][3])
    else:
        # Thin compressed metal slab in 3/4 perspective, no gems embedded.
        top=[(4,13),(20,7),(28,11),(12,17)]
        d.polygon([(4,13),(12,17),(12,24),(4,20)],fill=r[2])
        d.polygon([(12,17),(28,11),(28,18),(12,24)],fill=r[1])
        d.polygon(top,fill=r[4])
        d.line([(4,13),(20,7),(28,11)],fill=r[5])
        d.line([(4,14),(12,18),(28,12)],fill=r[3])
        d.line([(4,17),(12,21),(28,15)],fill=r[0])
        d.line([(12,23),(28,17)],fill=r[2])
        d.line([(8,13),(20,9)],fill=r[5])
        d.line([(14,15),(25,11)],fill=r[3])
    return im

def main():
    p=argparse.ArgumentParser();p.add_argument('--code',type=Path,required=True)
    args=p.parse_args();res=args.code/'src/main/resources'
    assets=res/'assets/zerog_tweaks'
    source=ROOT/'textures';source.mkdir(parents=True,exist_ok=True)
    textures=assets/'textures/item/manufacturing';textures.mkdir(parents=True,exist_ok=True)
    langpath=assets/'lang/en_us.json';lang=json.loads(langpath.read_text())
    manifest=[];sheet=Image.new('RGB',(640, len(GROUPS)*148),(23,25,35))
    draw=ImageDraw.Draw(sheet)
    for row,(planet,(ramp,metals)) in enumerate(GROUPS.items()):
        draw.text((8,row*148+4),planet.upper(),fill='#e6f4ff')
        for col,metal in enumerate(metals):
            draw.text((col*128+8,row*148+20),metal,fill='#9fb6d8')
            for pos,kind in enumerate(('cog','plate')):
                identifier=f'{metal}_{kind}';im=sprite(kind,ramp)
                im.save(source/f'{identifier}.png');im.save(textures/f'{identifier}.png')
                model={'parent':'minecraft:item/generated','textures':{'layer0':f'zerog_tweaks:item/manufacturing/{identifier}'}}
                (assets/f'models/item/{identifier}.json').write_text(json.dumps(model,indent=2)+'\n')
                lang[f'item.zerog_tweaks.{identifier}']=metal.replace('_',' ').title()+(' Cog' if kind=='cog' else ' Compressed Plate')
                x=col*128+pos*60+8;y=row*148+40
                sheet.paste(im.resize((56,56),Image.Resampling.NEAREST),(x,y),im.resize((56,56),Image.Resampling.NEAREST))
                small=im.resize((16,16),Image.Resampling.NEAREST);sheet.paste(small,(x+20,y+64),small)
                draw.text((x,y+84),kind,fill='#c48cff')
                manifest.append({'id':identifier,'metal':metal,'planet':planet,'palette':ramp,'crafting':'manual_bench_2_ingots_plate_4_ingots_cog'})
    # This resource has Windows line endings; preserve them to avoid a whole-file diff.
    langpath.write_text(json.dumps(lang,ensure_ascii=False,indent=2)+'\n', newline='\r\n')
    for kind,tag in (('cog','cogs'),('plate','plates')):
        values=[f'zerog_tweaks:{r["id"]}' for r in manifest if r['id'].endswith('_'+kind)]
        path=res/f'data/zerog_tweaks/tags/item/manufacturing/{tag}.json';path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps({'replace':False,'values':values},indent=2)+'\n')
        for r in manifest:
            if not r['id'].endswith('_'+kind):continue
            common=res/f'data/c/tags/item/{tag}/{r["metal"]}.json';common.parent.mkdir(parents=True,exist_ok=True)
            common.write_text(json.dumps({'replace':False,'values':[f'zerog_tweaks:{r["id"]}']},indent=2)+'\n')
    (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    sheet.save(ROOT/'manufacturing-preview.png')
    print(f'Generated {len(manifest)} component assets; run recipes.py for approved fabrication recipes.')

if __name__=='__main__':main()
