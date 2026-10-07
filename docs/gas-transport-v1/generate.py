"""Original native 32px ZeroG gas art. Design sources only until gas bindings pass tests."""
from pathlib import Path
import hashlib
import json
import math
from PIL import Image, ImageDraw
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('--code',type=Path)
parser.add_argument('--repair-language-encoding',action='store_true',help='One-time repair of Windows legacy punctuation bytes; keep valid UTF-8 intact')
args=parser.parse_args()

ROOT = Path(__file__).resolve().parent
STEEL = ['#141326', '#2b2a4a', '#454a78', '#6a7bb0', '#9fb6d8', '#e6f4ff']
GASES = {
    'oxygen': ['#06141f', '#0e3550', '#14648a', '#1fa2c4', '#5fe0f0', '#dcffff'],
    'hydrogen': ['#0b0712', '#231536', '#3f2766', '#6a45a8', '#a07ee0', '#e2d4ff'],
}
TIERS = ['copper', 'nullifite', 'cyrrium', 'tectium', 'wraithsteel', 'astrium']
ACCENTS = ['#eb9a52', '#a07ee0', '#5fe0f0', '#ff9a4a', '#a8e6c0', '#ffd04a']
FILES = []

def save(name, image, animation=False):
    target = ROOT / 'source/assets/zerog_tweaks/textures' / (name + '.png')
    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target)
    FILES.append({'path': str(target.relative_to(ROOT)), 'size': list(image.size),
                  'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
    if animation:
        target.with_suffix('.png.mcmeta').write_text(json.dumps({'animation': {
            'frametime': 3, 'width': 32, 'height': 32, 'interpolate': False}}, indent=2) + '\n')

def tube(accent):
    # Six-pixel pipe geometry: end cap UV 0..6, side UV y=10..16, doubled raster.
    image = Image.new('RGBA', (32, 32))
    d = ImageDraw.Draw(image)
    d.rectangle((0, 0, 11, 11), fill=STEEL[0])
    d.rectangle((1, 1, 10, 10), outline=STEEL[3])
    d.rectangle((3, 3, 8, 8), fill=(95, 224, 240, 38))
    d.line((3, 3, 8, 3), fill=STEEL[5])
    d.rectangle((0, 20, 31, 31), fill=(159, 182, 216, 28))
    for y, colour in [(20, STEEL[4]), (21, STEEL[2]), (30, STEEL[1]), (31, STEEL[0])]:
        d.line((0, y, 31, y), fill=colour)
    for x in [0, 8, 16, 24]:
        d.rectangle((x, 20, x+2, 31), fill=STEEL[1])
        d.line((x+1, 22, x+1, 29), fill=accent)
        d.point((x+1, 21), fill=STEEL[5])
    d.line((3, 23, 30, 23), fill=(230, 244, 255, 80))
    # Two tiny pressure marks distinguish gas chambers from ordinary liquid pipes.
    for x in [5, 21]:
        d.point((x, 26), fill=accent)
        d.point((x+1, 25), fill=accent)
    return image

def canister(ramp):
    image = Image.new('RGBA', (32, 32)); d = ImageDraw.Draw(image)
    d.rectangle((11, 2, 20, 4), fill=STEEL[0])
    d.rectangle((12, 2, 19, 3), fill=STEEL[4])
    d.rectangle((14, 5, 17, 7), fill=STEEL[2])
    d.polygon([(10, 8), (21, 8), (24, 11), (24, 27), (21, 30), (10, 30), (7, 27), (7, 11)], fill=STEEL[0])
    d.rectangle((9, 11, 22, 27), fill=STEEL[2])
    d.rectangle((10, 9, 21, 10), fill=STEEL[3])
    d.rectangle((10, 28, 21, 28), fill=STEEL[1])
    d.line((10, 11, 10, 26), fill=STEEL[5])
    d.line((11, 11, 11, 26), fill=STEEL[4])
    d.line((21, 11, 21, 27), fill=STEEL[1])
    d.rectangle((13, 13, 18, 24), fill=ramp[0])
    d.rectangle((14, 14, 17, 23), fill=ramp[2])
    d.line((14, 14, 14, 22), fill=ramp[4])
    d.point((15, 14), fill=ramp[5])
    for y in [16, 19, 22]: d.point((19, y), fill=STEEL[4])
    d.line((12, 26, 18, 26), fill=STEEL[4])
    return image

def wisps(ramp):
    atlas = Image.new('RGBA', (32, 256))
    for frame in range(8):
        image = Image.new('RGBA', (32, 32)); d = ImageDraw.Draw(image)
        for band in range(3):
            points = [(x, round(8+band*7+2*math.sin(x*.32-frame*math.pi/4+band))) for x in range(2, 30)]
            d.line(points, fill=ramp[2+band], width=2)
            for x, y in points[::4]: d.point((x, y-1), fill=ramp[5])
        atlas.alpha_composite(image, (0, frame*32))
    return atlas

gallery = Image.new('RGBA', (640, 390), '#14232e'); gd = ImageDraw.Draw(gallery)
gd.text((12, 12), 'ZeroG original gas artwork / native 32px / design preview, NOT in-game', fill='#e6f4ff')
for index, tier in enumerate(TIERS):
    image = tube(ACCENTS[index]); save('block/transport/'+tier+'_gas_tube', image)
    gallery.alpha_composite(image.resize((96, 96), Image.Resampling.NEAREST), (12+index*104, 55))
    gd.text((12+index*104, 38), tier, fill='#e6f4ff')
for index, (gas, ramp) in enumerate(GASES.items()):
    image = canister(ramp); save('item/'+gas+'_canister', image)
    animation = wisps(ramp); save('block/transport/'+gas+'_wisp', animation, True)
    gallery.alpha_composite(image.resize((128, 128), Image.Resampling.NEAREST), (20+index*300, 210))
    gallery.alpha_composite(animation.crop((0, 0, 32, 32)).resize((128, 128), Image.Resampling.NEAREST), (150+index*300, 210))
    gd.text((20+index*300, 185), gas+' / canister + animated gas chamber', fill='#e6f4ff')
save('item/gas_canister',canister(STEEL))
if args.code:
    resource=args.code/'src/main/resources'
    source=ROOT/'source'
    def write(relative,data):
        path=source/relative;path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(data,indent=2)+'\n')
    for tier in TIERS:
        old=tier+'_fluid_pipe';new=tier+'_gas_tube'
        for suffix in ('core','arm'):
            relative=f'assets/zerog_tweaks/models/block/transport/{old}_{suffix}.json'
            model=json.loads((resource/relative).read_text())
            model=json.loads(json.dumps(model).replace(old,new))
            write(relative.replace(old,new),model)
            for cube in model.get('elements',[]):
                for face in cube['faces'].values():assert all(0<=n<=16 for n in face['uv'])
        state=json.loads((resource/f'assets/zerog_tweaks/blockstates/{old}.json').read_text())
        write(f'assets/zerog_tweaks/blockstates/{new}.json',json.loads(json.dumps(state).replace(old,new)))
        item=json.loads((resource/f'assets/zerog_tweaks/models/item/{old}.json').read_text())
        write(f'assets/zerog_tweaks/models/item/{new}.json',json.loads(json.dumps(item).replace(old,new)))
        write(f'data/zerog_tweaks/loot_table/blocks/{new}.json',{
            'type':'minecraft:block','pools':[{'rolls':1,'entries':[{'type':'minecraft:item','name':'zerog_tweaks:'+new}],
                'conditions':[{'condition':'minecraft:survives_explosion'}]}]})
    write('assets/zerog_tweaks/models/item/gas_canister.json',{
        'parent':'minecraft:item/generated','textures':{'layer0':'zerog_tweaks:item/gas_canister'},
        'overrides':[{'predicate':{'zerog_tweaks:gas':1},'model':'zerog_tweaks:item/oxygen_canister'},
                     {'predicate':{'zerog_tweaks:gas':2},'model':'zerog_tweaks:item/hydrogen_canister'}]})
    for gas in GASES:
        write(f'assets/zerog_tweaks/models/item/{gas}_canister.json',{
            'parent':'minecraft:item/generated','textures':{'layer0':f'zerog_tweaks:item/{gas}_canister'}})
    for namespace in ('c','zerog_tweaks'):
        write(f'data/{namespace}/tags/fluid/gases.json',{'replace':False,'values':['zerog_tweaks:'+gas for gas in GASES]})
    import shutil
    for path in source.rglob('*'):
        if path.is_file():
            target=resource/path.relative_to(source);target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(path,target)
    lang=resource/'assets/zerog_tweaks/lang/en_us.json'
    raw=lang.read_bytes().decode('utf-8',errors='surrogateescape' if args.repair_language_encoding else 'strict')
    if args.repair_language_encoding:
        raw=''.join(bytes([ord(ch)-0xdc00]).decode('cp1252') if 0xdc80<=ord(ch)<=0xdcff else ch for ch in raw)
    text=json.loads(raw)
    text.update({'item.zerog_tweaks.gas_canister':'Refillable Gas Canister',
        'fluid_type.zerog_tweaks.oxygen':'Oxygen','fluid_type.zerog_tweaks.hydrogen':'Hydrogen',
        'tooltip.zerog_tweaks.gas_empty':'Empty — contained gases only',
        'tooltip.zerog_tweaks.gas_contents':'%s: %s / %s mB'})
    for tier in TIERS:text[f'block.zerog_tweaks.{tier}_gas_tube']=tier.title()+' Gas Tube'
    lang.write_text(json.dumps(text,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\r\n')
    mineable=resource/'data/minecraft/tags/block/mineable/pickaxe.json'
    tag=json.loads(mineable.read_text())
    for tier in TIERS:
        name='zerog_tweaks:'+tier+'_gas_tube'
        if name not in tag['values']:tag['values'].append(name)
    mineable.write_text(json.dumps(tag,indent=2)+'\n',encoding='utf-8',newline='\r\n')
gallery.convert('RGB').save(ROOT/'native-preview.png')
(ROOT/'manifest.json').write_text(json.dumps({'original_art': True, 'native_resolution': 32,
    'style': 'C magitech, hue-shifted steel; cyan oxygen / violet hydrogen',
    'runtime_installed': False, 'runtime_sources_generated':bool(args.code), 'files': FILES}, indent=2)+'\n')
print('Created', len(FILES), 'original gas textures; runtime integration pending.')
