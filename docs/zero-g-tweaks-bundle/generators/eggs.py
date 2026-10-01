import os, json
from PIL import Image, ImageDraw, ImageFont
from mobs_data import MOBS
from mobs_food import M2
from tex import hx
A='out/assets/zerog_tweaks'
ALL=list(MOBS.items())+list(M2.items())
lang=json.load(open(f'{A}/lang/en_us.json'))
rows=[]
OVR={'crystal_stag':('#2c3d57','#3fc9e8'),'prismling':('#1592b8','#e8ffff'),'prism_sentinel':('#3fc9e8','#e0dcb8'),
'dust_grazer':('#c4683a','#e8d0b0'),'rust_beetle':('#9c4424','#e89a62'),'moon_hopper':('#eceef2','#e8a0b0'),'frost_yak':('#a6b6c0','#3a464c'),
'rime_stalker':('#dce6ec','#7ae8ff'),'eidolon_captain':('#2a4050','#c4e0ec'),'crater_drifter':('#3a3a3a','#cfcfcf'),'ash_strider':('#1a1a1a','#ff8a2a'),
'cinder_hound':('#221c1a','#ffd070'),'slag_boar':('#3e2a20','#8a8a8a'),'deep_eel':('#5a6a7a','#9ff0f0'),'frost_warden':('#5e6e74','#9ff0f0')}
for k,m in ALL:
    main=m['boxes'][0][7]; pal=m['pal']
    glow=[b[7] for b in m['boxes'] if b[8]=='glow']
    acc=glow[0] if glow else [c for c in pal if c!=main][-1]
    p,s=pal[main],pal[acc]
    if p==s: s=list(pal.values())[1]
    p,s=OVR.get(k,(p,s))
    rows.append((k,m['name'],p,s))
    json.dump({'parent':'minecraft:item/template_spawn_egg'},open(f'{A}/models/item/{k}_spawn_egg.json','w'),indent=2)
    lang[f'item.zerog_tweaks.{k}_spawn_egg']=f"{m['name']} Spawn Egg"
json.dump(lang,open(f'{A}/lang/en_us.json','w'),indent=2,ensure_ascii=False)
# Java
BOSS={'prism_sentinel','rift_tyrant','eidolon_captain','dying_star','frost_warden','sun_colossus'}
lines=[f'    public static final DeferredItem<DeferredSpawnEggItem> {k.upper()}_SPAWN_EGG = egg("{k}", ZGEntities.{k.upper()}, 0x{p[1:].upper()}, 0x{s[1:].upper()});'+('  // boss' if k in BOSS else '') for k,_,p,s in rows]
java='''package net.zerog.tweaks.item;

import java.util.function.Supplier;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.item.Item;
import net.neoforged.neoforge.common.DeferredSpawnEggItem;
import net.neoforged.neoforge.registries.DeferredItem;
import net.zerog.tweaks.registry.ZGEntities;
import net.zerog.tweaks.registry.ZGItems;

/**
 * Spawn eggs for all 28 ZeroG mobs. Colours come from each mob's palette (base, spots).
 * DeferredSpawnEggItem registers its own colour handler, and the item models use
 * minecraft:item/template_spawn_egg, so no textures are needed.
 * Add them to a creative tab (e.g. the vanilla Spawn Eggs tab via BuildCreativeModeTabContentsEvent).
 */
public final class ZGSpawnEggs {
    private ZGSpawnEggs() {}

    private static DeferredItem<DeferredSpawnEggItem> egg(String id, Supplier<? extends EntityType<? extends Mob>> type, int base, int spots) {
        return ZGItems.ITEMS.register(id + "_spawn_egg", () -> new DeferredSpawnEggItem(type, base, spots, new Item.Properties()));
    }

''' + '\n'.join(lines) + '''

    /** Call from your mod constructor so the class loads before registration. */
    public static void init() {}
}
'''
os.makedirs('out_java/item',exist_ok=True); open('out_java/item/ZGSpawnEggs.java','w').write(java)
# preview sheet
MASK=["......oooo......",".....oBBBBo.....","....oBBBBBBo....","...oBBSSBBBBo...","...oBBSSBBBBo...","..oBBBBBBBSSBo..","..oBBBBBBBSSBo..","..oBSSBBBBBBBo..","..oBSSBBBBBBBo..","..oBBBBBSSBBBo..","..oBBBBBSSBBBo..","...oBBBBBBBBo...","....oBBBBBBo....",".....oooooo....."]
def egg(p,s):
    im=Image.new('RGBA',(16,16),(0,0,0,0)); px=im.load(); P,Sp=hx(p),hx(s)
    for y,r in enumerate(MASK):
        for x,c in enumerate(r):
            if c=='o': px[x,y+1]=tuple(int(v*.35) for v in P[:3])+(255,)
            elif c=='B': px[x,y+1]=tuple(min(255,int(v*(1.15 if x<7 and y<6 else .95))) for v in P[:3])+(255,)
            elif c=='S': px[x,y+1]=Sp
    return im
Fp='/usr/share/fonts/truetype/dejavu/'; FB=lambda s:ImageFont.truetype(Fp+'DejaVuSans-Bold.ttf',s); FR=lambda s:ImageFont.truetype(Fp+'DejaVuSans.ttf',s); FM=lambda s:ImageFont.truetype(Fp+'DejaVuSansMono.ttf',s)
cols=7; cw,ch=212,190; W=56+cols*cw; H=110+((len(rows)+cols-1)//cols)*ch
sh=Image.new('RGBA',(W,H),(246,245,242,255)); d=ImageDraw.Draw(sh)
d.text((28,22),'Spawn eggs',font=FB(28),fill=(34,32,40)); d.text((28,60),'Vanilla egg template tinted with two colours from each mob’s palette (base and spots). Preview only; the game draws the real template.',font=FR(13),fill=(110,108,118))
for i,(k,n,p,s) in enumerate(rows):
    x=28+(i%cols)*cw; y=100+(i//cols)*ch; d.rounded_rectangle([x,y,x+cw-12,y+ch-12],8,fill=(255,255,255),outline=(214,212,222))
    sh.alpha_composite(egg(p,s).resize((96,96),Image.NEAREST),(x+(cw-12-96)//2,y+10))
    d.text((x+10,y+112),n,font=FB(12),fill=(34,32,40))
    d.rectangle([x+10,y+134,x+24,y+148],fill=hx(p),outline=(120,120,120)); d.text((x+30,y+134),p,font=FM(10),fill=(110,108,118))
    d.rectangle([x+100,y+134,x+114,y+148],fill=hx(s),outline=(120,120,120)); d.text((x+120,y+134),s,font=FM(10),fill=(110,108,118))
    d.text((x+10,y+154),f'{k}_spawn_egg',font=FM(9),fill=(110,108,118))
sh.convert('RGB').save('sheets/30_spawn_eggs.png'); print(len(rows))
