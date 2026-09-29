import os, zipfile, random
from PIL import Image, ImageDraw, ImageFont
from tex import hx
from data import M
G={
'sword':[".............ooo","............ohho","...........ohlmo","..........ohlmo.",".........ohlmo..","........ohlmo...",
".......ohlmo....","..oo..ohlmo.....","..oaoohlmo......","...oaalmo.......","....oaao........","...owoaao.......",
"..owo..oao......",".owo....oo......","oao.............",".o.............."],
'pickaxe':["................","...oooooo.......","..ohhllllmoo....","...oommmmlddo...",".....oo.ohlddo..",".......owoolmdo.",
"......owo..omdo.",".....owo....omo.","....owo.....omo.","...owo.......o..","..owo...........",".owo............",
".oo.............","................","................","................"],
'axe':["................","........oooo....",".......ohhlmo...","......ohllmmdo..","......olllmmdo..",".......oollmdo..",
"......owooamdo..",".....owo..odo...","....owo....o....","...owo..........","..owo...........",".owo............",
".oo.............","................","................","................"],
'shovel':["................","...........ooo..","..........ohhlo.",".........ohllmdo",".........olmmddo","..........oamdo.",
".........owooo..","........owo.....",".......owo......","......owo.......",".....owo........","....owo.........",
"...owo..........","..owo...........","..oo............","................"],
'hoe':["................","........oooooo..",".......ohhllmdo.","........ooowoo..",".........owo....","........owo.....",
".......owo......","......owo.......",".....owo........","....owo.........","...owo..........","..owo...........",
"..oo............","................","................","................"],
'helmet':["................","................","................","....oooooooo....","...ohhhhlllmo...","..ohllllllmmdo..",
"..oaaaaaaaaaao..","..olmoooooomdo..","..olmo....omdo..","..odmo....omdo..","..oooo....oooo..","................",
"................","................","................","................"],
'chestplate':["................",".oooo......oooo.","ohhlmoooooolmmdo","ohllllllllllmmdo","ooolllllllllmooo","..olllllalllmo..",
"..ollllamalmmo..","..olllllallmmo..","..ollllllllmdo..","..ollllllllmdo..","..olmmmmmmmmdo..","..oaaaaaaaaaao..",
"..oooooooooooo..","................","................","................"],
'leggings':["................","................","...oooooooooo...","...oaaaaaaaao...","...ohlllllmdo...","...ohllmmlmdo...",
"...ohlmoolmdo...","...ohlo..omdo...","...ohlo..omdo...","...ohlo..omdo...","...ohlo..omdo...","...oddo..oddo...",
"...oooo..oooo...","................","................","................"],
'boots':["................","................","................","................","................","................",
"................","................","..oooo....oooo..","..oaao....oaao..","..ohlo....olmo..","..ohlmo...olmdo.",
".ohllmo..ohlmmdo",".odddddo.oddddo.",".oooooo..oooooo.","................"]}
for k,v in G.items(): assert len(v)==16 and all(len(r)==16 for r in v),(k,[len(r) for r in v])
GROUPS=[('sol','Sol',[('nullifite','Nullifite','Null Step: no fall damage'),('moonsteel','Moonsteel','Lunar Stride: 50% less fall damage'),
  ('ferrox','Ferrox','Sturdy: +1 armor toughness'),('olympium','Olympium','Dust Shield: storm and dust immunity')]),
 ('cerulon','Cerulon',[('cobaltium','Cobaltium','Quick Hands: +10% mining speed'),('cyrrium','Cyrrium','Tempered: +20% durability'),
  ('aurelion','Aurelion','Silver Tongue: better alien trader prices'),('cerulite','Cerulite','Crystal Sight: night vision, ores glow')]),
 ('skarn','Skarn',[('ruskite','Ruskite','Heat Scale: 25% less fire damage'),('tectium','Tectium','Anchored: knockback resistance'),
  ('pyrium','Pyrium','Kindled: tools auto-smelt ores 20% of the time'),('skarnite','Skarnite','Ember Walk: fire immunity, safe on Ember Crust')]),
 ('eidolon','Eidolon',[('salvium','Salvium','Scrapper: extra Salvium from wrecks'),('wraithsteel','Wraithsteel','Chill Guard: slowness immunity'),
  ('palladine','Palladine','Lucky: +1 Fortune and Looting'),('eidolite','Eidolite','Phantom Veil: freeze immunity, invisible sneaking')]),
 ('solvane','Solvane',[('photium','Photium','Glow: lights the area around you'),('astrium','Astrium','Star Forged: +2 max health'),
  ('radiantine','Radiantine','Radiant: +20% vs undead and Splinter'),('solvanite','Solvanite','Starborne: flight, immune to all planet hazards')])]
SETS=[x for _,_,l in GROUPS for x in l]
ROLE={'nullifite':'T1 set','olympium':'T2 set','cerulite':'T3 set','skarnite':'T4 set','eidolite':'T5 set','solvanite':'T6 set'}
def _dk(c,f):
    c=c.lstrip('#'); return '#%02x%02x%02x'%tuple(int(int(c[i:i+2],16)*f) for i in (0,2,4))
HANDLE={k:(M[k]['pal'][0],_dk(M[k]['pal'][1],.8),M[k]['pal'][1]) for k,_,_ in SETS}
def icon(tpl,key):
    p=M[key]['pal']; h=HANDLE[key]; im=Image.new('RGBA',(16,16),(0,0,0,0)); px=im.load()
    m={'o':p[0],'d':p[1],'m':p[2],'l':p[3],'h':p[4],'a':p[5],'w':h[1],'W':h[2]}
    for y,r in enumerate(G[tpl]):
        for x,c in enumerate(r):
            if c in m: px[x,y]=hx(m[c] if not (c=='o' and tpl in('sword','pickaxe','axe','shovel','hoe') and _handle(tpl,x,y)) else h[0])
    return im
def _handle(t,x,y): return x+y>=13 and x<8 and y>5
def layer(key,n):
    p=M[key]['pal']; rnd=random.Random(hash(key)+n); im=Image.new('RGBA',(64,32),(0,0,0,0)); px=im.load()
    regs=[(0,0,32,16),(16,16,40,32),(40,16,56,32),(0,16,16,32)] if n==1 else [(0,16,16,32),(16,16,40,32)]
    for (x0,y0,x1,y1) in regs:
        for y in range(y0,y1):
            for x in range(x0,x1):
                c=p[3] if rnd.random()<.55 else p[2] if rnd.random()<.7 else p[4]
                if y in (y0,y1-1) or x in (x0,x1-1): c=p[1]
                px[x,y]=hx(c)
    for x in range(0,32): px[x,12]=hx(p[5]) if n==1 else px[x,12] if px[x,12][3] else (0,0,0,0)
    for x in range(16,40): px[x,20 if n==1 else 26]=hx(p[5])
    return im
os.makedirs('out/assets/zerog_tweaks/textures/item',exist_ok=True); os.makedirs('out/assets/zerog_tweaks/textures/models/armor',exist_ok=True)
ICONS={}
for k,_,_ in SETS:
    for t in G:
        ICONS[(k,t)]=Image.open(f'out/assets/zerog_tweaks/textures/item/{k}_{t}.png').convert('RGBA')
    for n in (1,2): layer(k,n).save(f'out/assets/zerog_tweaks/textures/models/armor/{k}_layer_{n}.png')
# sheet
Fp='/usr/share/fonts/truetype/dejavu/'; FB=lambda s:ImageFont.truetype(Fp+'DejaVuSans-Bold.ttf',s); FR=lambda s:ImageFont.truetype(Fp+'DejaVuSans.ttf',s); FM=lambda s:ImageFont.truetype(Fp+'DejaVuSansMono.ttf',s)
BG=(246,245,242,255); INK=(34,32,40,255); SUB=(110,108,118,255); BORDER=(214,212,222,255)
def checker(n,c=8):
    im=Image.new('RGBA',(n,n),(250,250,252,255)); d=ImageDraw.Draw(im)
    for y in range(0,n,c):
        for x in range(0,n,c):
            if (x//c+y//c)%2: d.rectangle([x,y,x+c-1,y+c-1],fill=(238,236,244,255))
    return im
if os.path.exists('sheets/08_gear_sets.png'): os.remove('sheets/08_gear_sets.png')
M0=28; LW=150; CW=190; IS=128; RH=158; rows=list(G)
for gi,(gk,gname,sets) in enumerate(GROUPS):
    W=M0*2+LW+len(sets)*CW; H=150+len(rows)*RH+600
    im=Image.new('RGBA',(W,H),BG); d=ImageDraw.Draw(im)
    d.text((M0,24),f'{gname} gear  \u2014  tools and armor',font=FB(30),fill=INK)
    d.text((M0,64),'ZeroG Tweaks \u00b7 every set has its own silhouettes: blade, guard, head and helmet shapes differ per set, plus a surface motif. 16\u00d716 at 8\u00d7.',font=FR(13),fill=SUB)
    for i,(k,n,_) in enumerate(sets):
        x=M0+LW+i*CW; p=M[k]['pal']; lab=n+'  \u00b7  '+(ROLE.get(k) or M[k]['role'] and {'metal':'metal set'}['metal'])
        d.text((x,100),n,font=FB(13),fill=INK); d.text((x+d.textlength(n,font=FB(13))+8,102),ROLE.get(k,'metal set'),font=FR(10),fill=SUB)
        d.rectangle([x,122,x+IS,127],fill=hx(p[3]))
    for r,t in enumerate(rows):
        y=140+r*RH; d.text((M0,y+IS//2-8),t.capitalize(),font=FB(14),fill=INK)
        for i,(k,_,_) in enumerate(sets):
            x=M0+LW+i*CW; im.alpha_composite(checker(IS),(x,y)); im.alpha_composite(ICONS[(k,t)].resize((IS,IS),Image.NEAREST),(x,y))
            d.text((x,y+IS+4),f'{k}_{t}',font=FM(9),fill=SUB)
    y=140+len(rows)*RH+10
    d.text((M0,y),'Worn armor layers',font=FB(18),fill=INK); d.text((M0,y+26),'models/armor/<set>_layer_1.png and _layer_2.png, vanilla 64\u00d732 UV layout, shown at 2\u00d7.',font=FR(12),fill=SUB)
    y+=54
    for i,(k,n,_) in enumerate(sets):
        x=M0+(i%2)*(W-2*M0)//2; yy=y+(i//2)*110; d.text((x,yy),n,font=FB(12),fill=INK)
        for j in (1,2):
            L=Image.open(f'out/assets/zerog_tweaks/textures/models/armor/{k}_layer_{j}.png').resize((128,64),Image.NEAREST)
            bx=x+(j-1)*140; im.alpha_composite(checker(128,8).crop((0,0,128,64)),(bx,yy+18)); im.alpha_composite(L,(bx,yy+18)); d.rectangle([bx,yy+18,bx+127,yy+81],outline=BORDER)
            d.text((bx,yy+84),f'layer_{j}',font=FM(9),fill=SUB)
    y+=240
    d.text((M0,y),'Full-set perks',font=FB(18),fill=INK); y+=34
    for i,(k,n,b) in enumerate(sets):
        if i%2: d.rectangle([M0,y-4,W-M0,y+20],fill=(250,249,247,255))
        im.alpha_composite(ICONS[(k,'chestplate')],(M0+6,y)); d.text((M0+30,y),n,font=FB(12),fill=INK); d.text((M0+160,y+1),b,font=FR(12),fill=INK); y+=26
    im=im.crop((0,0,W,y+24)); im.convert('RGB').save(f'sheets/{15+gi}_gear_{gk}.png')
with zipfile.ZipFile('zerog_tweaks_resources.zip','w') as z:
    for root,_,files in os.walk('out'):
        for f in files: z.write(os.path.join(root,f),os.path.relpath(os.path.join(root,f),'out'))
print(sum(len(f) for _,_,f in os.walk('out')))
