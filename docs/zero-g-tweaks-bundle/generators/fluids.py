import os, json, math, random
from PIL import Image, ImageDraw, ImageFont
from foodtex import render
from food_data import MASK
from tex import hx
A='out/assets/zerog_tweaks'; TB=f'{A}/textures/block'; TI=f'{A}/textures/item'
FL=[
 dict(k='acid',n='Acid',where='Toxic wastelands',pal=['#3a5a10','#6a9a18','#8ac040','#c8ff60'],spark='#e8ff80',style='bubble',alpha=220,light=4,fog='#73A01F',
      props=['Poison II while inside','Corrodes armor durability (Neutralizer blocks it)','Destroys dropped items after 5 s'],mix=[('water','sludgestone'),('lava','toxic_mud')],use='Bog Lurker habitat; Neutralizer crafting'),
 dict(k='liquid_starlight',n='Liquid Starlight',where='Cerulon crystal caves',pal=['#0a1440','#1a2a80','#2e4ac0','#6a8af0'],spark='#ffffff',style='stars',alpha=210,light=12,fog='#2E4AC0',
      props=['Glows (light 12)','Slow Falling and Night Vision while swimming'],mix=[('water','crystal_sand'),('lava','prismstone')],use='Crystal Growth Chamber input (faster gem growth)'),
 dict(k='magma_slag',n='Magma Slag',where='Skarn lava fields',pal=['#2a0a04','#6a1a06','#b8400c','#f08020'],spark='#ffd070',style='crust',alpha=255,light=12,fog='#8A2A08',
      props=['Sets you on fire; slower and thicker than lava','Flows only 3 blocks'],mix=[('water','slag'),('liquid starlight','rift_glass')],use='Alloy Forge heat source; Skarn lava lakes'),
 dict(k='cryo_fluid',n='Cryo Fluid',where='Eidolon and frozen wastelands',pal=['#3a7a96','#6ab4d0','#a8e0f0','#e8fbff'],spark='#ffffff',style='ice',alpha=200,light=2,fog='#8FD0E6',
      props=['Slowness II and freezing (Freeze Ward blocks it)','Turns water it touches into ice'],mix=[('water','glacial_ice'),('lava','frostrock')],use='Machine coolant (Cryo Core); Frost Warden arena moat'),
 dict(k='solar_plasma',n='Solar Plasma',where='Solvane molten flows',pal=['#c43a06','#f07a14','#ffc040','#fff6c8'],spark='#ffffff',style='swirl',alpha=255,light=15,fog='#FFB040',
      props=['Burns through Fire Resistance','Safe only with Heatproof Plating or Skarnite+ armor','Light 15'],mix=[('water','slag_glass'),('cryo fluid','sunspot_rock')],use='Fusion Reactor fuel'),
 dict(k='null_fluid',n='Null Fluid',where='Deep Dark pools (Earth), Moon craters',pal=['#06040c','#140c24','#2a1a48','#5a3a90'],spark='#d9c8ff',style='ripple',alpha=230,light=6,fog='#1A1030',
      props=['Low gravity inside: you slowly float upward','Nullifite ore glows brighter nearby'],mix=[('water','none'),('lava','deepslate_nullifite_ore')],use='Teleporter coolant (faster charging); T1 hint'),
]
def frame(f,size,t,flow):
    im=Image.new('RGBA',(size,size)); px=im.load(); P=[hx(c) for c in f['pal']]; r=random.Random(t*7+len(f['k']))
    for y in range(size):
        for x in range(size):
            yy=(y+(t*2 if flow else 0))%size
            s=f['style']
            if s=='ripple': v=math.sin(math.hypot(x-size/2,yy-size/2)*0.9-t*0.4)*.5+.5
            elif s=='swirl': a=math.atan2(yy-size/2,x-size/2); v=math.sin(a*3+math.hypot(x-size/2,yy-size/2)*.6-t*.5)*.5+.5
            elif s=='crust': v=(math.sin(x*.5+t*.15)+math.sin(yy*.45-t*.1)+math.sin((x+yy)*.3))/6+.5
            else: v=(math.sin(x*.7+t*.4)+math.sin(yy*.55-t*.3)+.8*math.sin((x+yy)*.3+t*.2))/5.6+.5
            i=min(3,int(v*4)); c=P[i]
            if s=='crust' and v<.3: c=P[0]
            px[x,y]=(c[0],c[1],c[2],f['alpha'])
    sp=hx(f['spark']); n={'stars':5,'bubble':3,'ice':4,'swirl':3,'ripple':2,'crust':3}[f['style']]*(size//16)**2
    rr=random.Random(len(f['k'])*13)
    pts=[(rr.randrange(size),rr.randrange(size)) for _ in range(n)]
    for i,(x,y) in enumerate(pts):
        if (t+i)%4 in (0,1): px[x,(y+(t*2 if flow else 0))%size]=(sp[0],sp[1],sp[2],255)
    return im
MASK['bucket']=["................","....WWWWWWWW....","...W........W...","..WWWWWWWWWWWW..","..WHHHHHHHHHHW..","..WHHAHHHHAHHW..","..WHHHHHAHHHHW..","...WWWWWWWWWW...","...WWWWWWWWWW...","....WWWWWWWW....","....WWWWWWWW....",".....WWWWWW....."]
lang=json.load(open(f'{A}/lang/en_us.json'))
def wj(p,o): os.makedirs(os.path.dirname(p),exist_ok=True); json.dump(o,open(p,'w'),indent=2)
for f in FL:
    for name,size,flow in ((f"{f['k']}_still",16,False),(f"{f['k']}_flow",32,True)):
        sheet=Image.new('RGBA',(size,size*16))
        for t in range(16): sheet.paste(frame(f,size,t,flow),(0,t*size))
        sheet.save(f'{TB}/{name}.png'); json.dump({'animation':{'frametime':2 if f['k']!='magma_slag' else 4}},open(f'{TB}/{name}.png.mcmeta','w'))
    render(dict(mask='bucket',H=f['pal'][2],A=f['spark'],G=f['pal'][2],W='#9aa0a8')).save(f"{TI}/{f['k']}_bucket.png")
    wj(f"{A}/models/block/{f['k']}.json",{'textures':{'particle':f"zerog_tweaks:block/{f['k']}_still"}})
    wj(f"{A}/blockstates/{f['k']}.json",{'variants':{'':{'model':f"zerog_tweaks:block/{f['k']}"}}})
    wj(f"{A}/models/item/{f['k']}_bucket.json",{'parent':'minecraft:item/generated','textures':{'layer0':f"zerog_tweaks:item/{f['k']}_bucket"}})
    lang[f"block.zerog_tweaks.{f['k']}"]=f['n']; lang[f"item.zerog_tweaks.{f['k']}_bucket"]=f"{f['n']} Bucket"; lang[f"fluid_type.zerog_tweaks.{f['k']}"]=f['n']
json.dump(lang,open(f'{A}/lang/en_us.json','w'),indent=2,ensure_ascii=False)
json.dump(FL,open('fluids.json','w'),indent=1)
# ---------------- reference sheet
import sys; sys.argv=['x']
from sheet2 import cube
Fp='/usr/share/fonts/truetype/dejavu/'; FB=lambda s:ImageFont.truetype(Fp+'DejaVuSans-Bold.ttf',s); FR=lambda s:ImageFont.truetype(Fp+'DejaVuSans.ttf',s); FM=lambda s:ImageFont.truetype(Fp+'DejaVuSansMono.ttf',s)
BG=(246,245,242,255); INK=(34,32,40,255); SUB=(110,108,118,255); BORDER=(214,212,222,255); PANEL=(235,233,243,255)
def checker(w,h,c=6):
    im=Image.new('RGBA',(w,h),(255,255,255,255)); d=ImageDraw.Draw(im)
    for y in range(0,h,c):
        for x in range(0,w,c):
            if (x//c+y//c)%2: d.rectangle([x,y,x+c-1,y+c-1],fill=(238,236,244,255))
    return im
def up(im,s): return im.resize((im.width*s,im.height*s),Image.NEAREST)
def extrude(tex,s=7,depth=2):
    W=16*s+depth*s+4; im=Image.new('RGBA',(W,W),(0,0,0,0)); px=tex.load(); d=ImageDraw.Draw(im)
    for k in range(depth*s,0,-1):
        for y in range(16):
            for x in range(16):
                c=px[x,y]
                if c[3]: d.rectangle([x*s+k,y*s+depth*s-k,x*s+k+s-1,y*s+depth*s-k+s-1],fill=(int(c[0]*.55),int(c[1]*.55),int(c[2]*.55),255))
    im.alpha_composite(up(tex,s),(0,depth*s)); return im
CW,CH=1540,360
W=56+CW; H=110+len(FL)*(CH+14)+10
sh=Image.new('RGBA',(W,H),BG); d=ImageDraw.Draw(sh)
d.text((28,22),'Liquids  —  texture reference',font=FB(30),fill=INK)
d.text((28,64),'Six liquids, one per world. Still texture 16×16 and flowing 32×32, 16 animation frames each (.mcmeta), plus a bucket and an underwater fog colour.',font=FR(13),fill=SUB)
for i,f in enumerate(FL):
    y=100+i*(CH+14); x=28
    card=Image.new('RGBA',(CW,CH),(255,255,255,255)); cd=ImageDraw.Draw(card); cd.rectangle([0,0,CW-1,CH-1],outline=BORDER)
    cd.text((14,12),f['n'],font=FB(17),fill=INK); cd.text((14,36),f"Fluid · {f['where']} · zerog_tweaks:{f['k']} · light {f['light']}",font=FM(10),fill=SUB)
    # in-world pool
    cd.rounded_rectangle([14,58,234,300],8,fill=PANEL)
    still=Image.open(f"{TB}/{f['k']}_still.png").convert('RGBA'); flow=Image.open(f"{TB}/{f['k']}_flow.png").convert('RGBA')
    fr0=still.crop((0,0,16,16)); side=fr0.copy()
    pool=cube(fr0,side,side,s=6); card.alpha_composite(pool,(14+(220-pool.width)//2,58+(242-pool.height)//2)); cd.text((22,284),'in world (source block)',font=FR(9),fill=SUB)
    # still frames
    cd.text((252,58),'STILL · 16 frames (first 8 shown)',font=FB(10),fill=INK)
    for t in range(8):
        fx=252+t*70; card.alpha_composite(checker(64,64),(fx,76)); card.alpha_composite(up(still.crop((0,t*16,16,t*16+16)),4),(fx,76)); cd.rectangle([fx,76,fx+63,139],outline=BORDER)
    cd.text((252,150),'FLOWING · 32×32',font=FB(10),fill=INK)
    for t in range(3):
        fx=252+t*104; card.alpha_composite(checker(96,96),(fx,168)); card.alpha_composite(up(flow.crop((0,t*4*32,32,t*4*32+32)),3),(fx,168)); cd.rectangle([fx,168,fx+95,263],outline=BORDER)
    # bucket
    b=Image.open(f"{TI}/{f['k']}_bucket.png").convert('RGBA'); e=extrude(b); cd.rounded_rectangle([580,150,780,300],8,fill=PANEL)
    card.alpha_composite(e.resize((int(e.width*.95),int(e.height*.95)),Image.NEAREST),(598,156)); cd.text((588,284),f"{f['n']} Bucket",font=FR(9),fill=SUB)
    xx=800
    for s_ in (1,2,4):
        c=checker(16*s_,16*s_,3); c.alpha_composite(up(b,s_)); card.alpha_composite(c,(xx,280-16*s_)); xx+=16*s_+10
    cd.text((800,284),'in slot 1x 2x 4x',font=FR(9),fill=SUB)
    # fog + palette
    cd.text((920,58),'Underwater fog',font=FB(11),fill=INK); cd.rectangle([920,76,1000,116],fill=hx(f['fog']),outline=(120,120,120)); cd.text((1008,90),f['fog'],font=FM(10),fill=SUB)
    cd.text((920,128),'Palette',font=FB(11),fill=INK)
    for j,c in enumerate(f['pal']+[f['spark']]):
        cd.rectangle([920+j*44,146,952+j*44,178],fill=hx(c),outline=(120,120,120)); cd.text((920+j*44,182),c,font=FM(8),fill=SUB)
    # properties & mixing
    cd.text((1160,58),'In the world',font=FB(11),fill=INK); yy=76
    for p in f['props']: cd.text((1160,yy),'• '+p,font=FR(11),fill=INK); yy+=18
    cd.text((1160,yy+8),'Mixing',font=FB(11),fill=INK); yy+=28
    for other,res in f['mix']:
        if res=='none': cd.text((1160,yy+4),f'+ {other}: nothing',font=FR(11),fill=INK); yy+=28; continue
        tex=Image.open(f'{TB}/{res}.png').convert('RGBA').crop((0,0,16,16)); card.alpha_composite(up(tex,2),(1160,yy)); cd.rectangle([1160,yy,1191,yy+31],outline=BORDER)
        cd.text((1200,yy+8),f"+ {other} → {res.replace('_',' ').title()}",font=FR(11),fill=INK); yy+=38
    cd.text((1160,yy-4),'(wasteland results show grey here; they are tinted in game)',font=FR(9),fill=SUB) if any(r in ('sludgestone','toxic_mud','prismstone','frostrock','glacial_ice') for _,r in f['mix']) else None
    cd.text((1160,yy+6),'Used for',font=FB(11),fill=INK); cd.text((1160,yy+24),f['use'],font=FR(11),fill=INK)
    sh.alpha_composite(card,(x,y))
sh.convert('RGB').save('sheets/31_liquids.png'); print('ok')
