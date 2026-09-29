from PIL import Image, ImageDraw, ImageFont
Fp='/usr/share/fonts/truetype/dejavu/'; FB=lambda s:ImageFont.truetype(Fp+'DejaVuSans-Bold.ttf',s); FR=lambda s:ImageFont.truetype(Fp+'DejaVuSans.ttf',s)
TB='out/assets/zerog_tweaks/textures/block'; TI='out/assets/zerog_tweaks/textures/item'
BG=(246,245,242,255); INK=(34,32,40,255); SUB=(110,108,118,255); BORDER=(214,212,222,255)
def L(p): return Image.open(p).convert('RGBA')
def checker(n,c=8):
    im=Image.new('RGBA',(n,n),(255,255,255,255)); d=ImageDraw.Draw(im)
    for y in range(0,n,c):
        for x in range(0,n,c):
            if (x//c+y//c)%2: d.rectangle([x,y,x+c-1,y+c-1],fill=(238,236,244,255))
    return im
rows=[]
for w,n in [('shardwood','Shardwood'),('charwood','Charwood'),('hoarwood','Hoarwood'),('gildwood','Gildwood')]:
    rows.append((f'{n} wood set',[(f'{TB}/{w}_log.png','Log'),(f'{TB}/{w}_log_top.png','Log top'),(f'{TB}/stripped_{w}_log.png','Stripped'),(f'{TB}/stripped_{w}_log_top.png','Stripped top'),
        (f'{TB}/{w}_planks.png','Planks'),(f'{TB}/{w}_leaves.png','Leaves'),(f'{TB}/{w}_sapling.png','Sapling'),(f'{TB}/{w}_door_top.png','Door top'),(f'{TB}/{w}_door_bottom.png','Door bottom'),
        (f'{TI}/{w}_door.png','Door item'),(f'{TB}/{w}_trapdoor.png','Trapdoor')]))
rows.append(('Crops',[(f'{TB}/rust_tuber_crop_stage{s}.png',f'Rust Tuber {s}') for s in range(4)]+[(f'{TB}/skyberry_bush_stage{s}.png',f'Skyberry {s}') for s in range(4)]))
EMI=['nebulite_ore','pulsar_dust_ore','emberite_ore','rift_opal_ore','coronite_ore','ember_crust','corona_crust','fusion_lamp']
rows.append(('Emissive overlays (texture, then glow layer)',sum([[(f'{TB}/{e}.png',e.replace('_',' ')),(f'{TB}/{e}_emissive.png','glow')] for e in EMI[:5]],[])))
rows.append(('',sum([[(f'{TB}/{e}.png',e.replace('_',' ')),(f'{TB}/{e}_emissive.png','glow')] for e in EMI[5:]],[])+[(f'{TB}/acid_still.png','acid fluid')]))
rows.append(('Upgrade smithing templates',[(f'{TI}/{k}_upgrade_smithing_template.png',k.capitalize()) for k in ['olympium','cerulite','skarnite','eidolite','solvanite']]))
CW=128; W=28*2+11*(CW+10); H=100+len(rows)*190
im=Image.new('RGBA',(W,H),BG); d=ImageDraw.Draw(im)
d.text((28,24),'Wood sets, crops, glow layers and templates',font=FB(28),fill=INK)
d.text((28,62),'Every tree gets logs, stripped logs, wood, planks, stairs, slab, fence, gate, door, trapdoor, button, pressure plate, leaves and sapling. Fences and buttons reuse the planks texture.',font=FR(13),fill=SUB)
y=96
for title,items in rows:
    if title: d.text((28,y),title,font=FB(15),fill=INK)
    for i,(p,lab) in enumerate(items):
        x=28+i*(CW+10); c=checker(CW); c.alpha_composite(L(p).resize((CW,CW),Image.NEAREST)); im.alpha_composite(c,(x,y+24)); d.rectangle([x,y+24,x+CW-1,y+24+CW-1],outline=BORDER)
        d.text((x,y+24+CW+4),lab,font=FR(11),fill=INK)
    y+=190
im.convert('RGB').save('sheets/26_wood_crops_glow.png')
