"""Original 32px ZeroG card sprites. Separate source art, runtime bindings and gallery.
Run after earlier art generators. No registration, balancing or gameplay changes.
"""
import argparse, hashlib, json, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
TIERS=[('Copper',['35202b','713c37','b5704a','e8ac71','ffe8ba']),
       ('Verdant',['122a32','235945','459a61','8fe29c','e2ffcd']),
       ('Cyan',['13243d','245576','35a6bb','7dedee','e4ffff']),
       ('Azure',['211d40','354a88','527fda','95c5ff','eef8ff']),
       ('Violet',['27173d','633a8c','a060d6','dda1ff','fff0ff']),
       ('Gold',['352035','806025','cfa137','ffe580','fffbd7'])]
FAMILIES=['acceleration','energy_coil','item_compact']
METAL=['101427','222b43','40516b','6c87a0','c5e0e9']
def color(hexcode):return '#'+hexcode
def sprite(family,tier):
    ramp=TIERS[tier-1][1] if tier else ['221331','422447','744886','bc8fde','efe0ff']
    im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
    d.polygon([(5,2),(24,2),(28,6),(28,28),(7,28),(3,24),(3,4)],fill=color(METAL[0]))
    d.polygon([(5,3),(23,3),(27,7),(27,26),(7,26),(4,23),(4,5)],fill=color(METAL[2]))
    d.polygon([(5,3),(23,3),(25,5),(6,5),(6,23),(4,21),(4,5)],fill=color(METAL[4]))
    d.polygon([(27,7),(27,26),(7,26),(7,25),(25,25),(25,7)],fill=color(METAL[1]))
    d.rectangle((8,6,23,21),fill=color(ramp[0]));d.line((8,6,23,6),fill=color(ramp[2]));d.line((8,6,8,20),fill=color(ramp[1]))
    # Shaped circuitry; no blurred glow, mixed pixel sizes or painted background aura.
    d.line([(6,8),(6,15),(7,16)],fill=color(ramp[3]));d.line([(25,11),(25,20),(23,22)],fill=color(ramp[2]))
    d.point((25,9),fill=color(ramp[4]));d.rectangle((7,27,25,28),fill=color(METAL[0]))
    for x in range(8,25,3):d.rectangle((x,27,x+1,28),fill=color(TIERS[0][1][3]))
    if family=='acceleration':
        for x in (10,16):
            points=[(x,9),(x+3,9),(x+6,14),(x+2,19),(x-1,19),(x+3,14)]
            d.polygon(points,fill=color(ramp[2]));d.line([(x,9),(x+3,9),(x+6,14)],fill=color(ramp[4]),width=1)
            d.line([(x+2,19),(x-1,19)],fill=color(ramp[1]))
    elif family=='energy_coil':
        for y in (9,12,15,18):
            d.rectangle((10,y,20,y+1),fill=color(ramp[2]));d.line((10,y,18,y),fill=color(ramp[4]))
        d.line((10,10,10,18),fill=color(ramp[1]));d.line((20,9,20,19),fill=color(ramp[3]))
        d.polygon([(18,8),(14,14),(17,14),(14,20),(21,12),(18,12)],fill=color(ramp[4]))
    elif family=='item_compact':
        for y in (10,15):
            d.polygon([(10,y+1),(16,y-1),(21,y+1),(16,y+3)],fill=color(ramp[4]))
            d.polygon([(10,y+1),(16,y+3),(16,y+6),(10,y+4)],fill=color(ramp[2]))
            d.polygon([(16,y+3),(21,y+1),(21,y+4),(16,y+6)],fill=color(ramp[1]))
    else:
        d.polygon([(13,8),(19,8),(23,12),(23,17),(19,21),(13,21),(9,17),(9,12)],fill=color(ramp[2]))
        d.polygon([(14,10),(19,10),(21,13),(21,17),(18,19),(13,18),(11,15),(12,12)],fill=color(ramp[1]))
        d.line([(12,11),(18,10),(21,13),(20,17)],fill=color(ramp[4]),width=1)
        d.rectangle((14,13,18,16),fill=color(METAL[0]));d.point((15,12),fill=color(ramp[3]))
    # Six visible tier positions; selected segments survive inventory downsampling.
    for i in range(6):
        x=8+i*3;d.rectangle((x,23,x+1,24),fill=color(ramp[3] if i<tier else METAL[1]))
    if tier==0:d.line((11,23,21,23),fill=color(ramp[3]))
    return im

def main():
    p=argparse.ArgumentParser();p.add_argument('--code',type=Path,required=True);p.add_argument('--gallery',type=Path);args=p.parse_args()
    tex=args.code/'src/main/resources/assets/zerog_tweaks/textures/item/upgrade_cards'
    models=args.code/'src/main/resources/assets/zerog_tweaks/models/item'
    source=ROOT/'textures';source.mkdir(parents=True,exist_ok=True);tex.mkdir(parents=True,exist_ok=True)
    rows=[];tiles=[]
    for family in FAMILIES+['void']:
        for tier in (range(1,7) if family!='void' else [0]):
            name=f'{family}_upgrade_card'+(f'_t{tier}' if tier else '')
            im=sprite(family,tier);target=source/(name+'.png');im.save(target);shutil.copyfile(target,tex/target.name)
            model={'parent':'minecraft:item/generated','textures':{'layer0':f'zerog_tweaks:item/upgrade_cards/{name}'}}
            (models/(name+'.json')).write_text(json.dumps(model,indent=2)+'\n')
            rows.append({'id':'zerog_tweaks:'+name,'tier':tier,'family':family,'size':[32,32],'sha256':hashlib.sha256(target.read_bytes()).hexdigest()});tiles.append((family,tier,im))
    sheet=Image.new('RGB',(920,430),'#101827');d=ImageDraw.Draw(sheet);font=ImageFont.load_default(size=18)
    d.text((20,12),'ZeroG - Original Upgrade Cards - 32x32',font=font,fill='#d7e8ff')
    for i,(name,ramp) in enumerate(TIERS):d.text((184+i*120,47),f'T{i+1} {name}',font=font,fill=color(ramp[3]))
    for family,tier,im in tiles:
        row=(FAMILIES+['void']).index(family);y=85+row*82
        d.text((15,y+22),family.replace('_',' ').title(),font=font,fill='#d7e8ff')
        sheet.paste(im.resize((64,64),Image.Resampling.NEAREST),(190+(tier-1 if tier else 0)*120,y),im.resize((64,64),Image.Resampling.NEAREST))
    d.text((300,350),'Void: un-tiered. Colours + marks identify tier;',font=font,fill='#c9b4ef')
    d.text((300,375),'centre symbols identify the job. No gameplay changes.',font=font,fill='#c9b4ef')
    sheet.save(ROOT/'preview.png')
    if args.gallery:args.gallery.parent.mkdir(parents=True,exist_ok=True);sheet.save(args.gallery)
    bindings=[{'path':'assets/zerog_tweaks/textures/item/upgrade_cards/'+r['id'].split(':')[1]+'.png','sha256':r['sha256']} for r in rows]
    (ROOT/'manifest.json').write_text(json.dumps({'source':'Original local pixel drawing; no external artwork','generator':'docs/upgrade-card-icons/generate.py','style':'C magitech; hue-shifted clustered shading; transparent margin','tiers':[{'tier':i+1,'name':v[0],'ramp':v[1]} for i,v in enumerate(TIERS)],'assets':rows,'files':bindings},indent=2)+'\n')
    assert len({r['sha256'] for r in rows})==19,'Icons must be distinct'
    for _,_,im in tiles:assert im.size==(32,32) and im.getpixel((0,0))[3]==0
    print('19 distinct transparent 32px card sprites generated; bindings and gallery written.')
if __name__=='__main__':main()
