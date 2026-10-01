import os, zipfile
from PIL import Image, ImageDraw, ImageFont
import terrain as T, blocks as K
from tex import stone
from data import STONES
Fp='/usr/share/fonts/truetype/dejavu/'; FB=lambda s:ImageFont.truetype(Fp+'DejaVuSans-Bold.ttf',s); FR=lambda s:ImageFont.truetype(Fp+'DejaVuSans.ttf',s); FM=lambda s:ImageFont.truetype(Fp+'DejaVuSansMono.ttf',s)
BG=(246,245,242,255); INK=(34,32,40,255); SUB=(110,108,118,255); BORDER=(214,212,222,255); PANEL=(235,233,243,255)
OUT='out/assets/zerog_tweaks/textures/block'; os.makedirs(OUT,exist_ok=True)
from sheet2 import cube, up
def checker(n,c=4):
    im=Image.new('RGBA',(n,n),(255,255,255,255)); d=ImageDraw.Draw(im)
    for y in range(0,n,c):
        for x in range(0,n,c):
            if (x//c+y//c)%2: d.rectangle([x,y,x+c-1,y+c-1],fill=(238,236,244,255))
    return im
def B(id,name,typ,top,side=None,bottom=None,kind='cube'): return dict(id=id,name=name,typ=typ,top=top,side=side or top,bottom=bottom or top,kind=kind)
def building(id,name,p,s):
    return [B(f'polished_{id}',f'Polished {name}','building',T.polished(p,s)),B(f'{id}_bricks',f'{name} Bricks','building · stairs, slab, wall',T.bricks(p,s+1)),
            B(f'chiseled_{id}',f'Chiseled {name}','building',T.chiseled(p,s+2))]
def wood(pre,name,bark,wood_p,leaf,s,acc=None):
    return [B(f'{pre}_log',f'{name} Log','wood',T.log_top(bark,wood_p,s),T.log_side(bark,s),kind='column'),
            B(f'{pre}_planks',f'{name} Planks','wood · full wood set',T.planks(wood_p,s)),
            B(f'{pre}_leaves',f'{name} Leaves','leaves',T.leaves(leaf,s,acc))]
S=STONES; W={}
lun=S['lunar_stone']; mare=['#1c1c22','#2a2a32','#383842','#484852']; mar=S['martian_stone']
W['moon_mars']=('Moon and Mars',[B('lunar_stone','Lunar Stone','terrain',stone(lun,101)),B('regolith','Regolith','terrain · falls like sand',T.sand(['#7a7a7e','#96969a','#aeaeb2','#c8c8ca'],3)),
 B('mare_basalt','Mare Basalt','terrain',stone(mare,4)),B('crater_ice','Crater Ice','terrain',T.ice(['#5a7a90','#7a9cb2','#a6c4d6','#d8ecf6'],5)),
 B('lunar_lichen','Lunar Lichen','plant',T.plant('bush',['#3a3a3a','#8a9a8a','#a8b8a8','#d0dcd0'],None,6),kind='cross'),
 B('selenite_lamp','Selenite Lamp','light',T.lamp(['#3a3f52','#5a6078','#7a82a0','#9aa2c0'],['#8f9ab8','#c2cbe6','#ffffff'],7))]
 +building('lunar_stone','Lunar Stone',lun,8)+building('mare_basalt','Mare Basalt',mare,11)
 +[B('martian_stone','Martian Stone','terrain',stone(mar,102)),B('rustsand','Rustsand','terrain · falls like sand',T.sand(['#7a2e16','#9a3e1e','#b8522a','#d06a38'],14)),
 B('oxide_crust','Oxide Crust','terrain',T.cracked(mar,15,'#e0884a',4)),B('polar_frost','Polar Frost','terrain · slows and chills',T.ice(['#b8c4cc','#cdd6dc','#e2e8ec','#f6f8fa'],16)),
 B('rust_lichen','Rust Lichen','plant',T.plant('bush',['#2a0e08','#8a3a1e','#b85a30','#e08a5a'],None,17),kind='cross'),
 B('olympium_plating','Olympium Plating','decor',K.casing_block('olympium',18)['top'])]+building('martian_stone','Martian Stone',mar,19))
cer=S['cerulean_stone']; sw=(['#1a2a3a','#2a3e52','#3a526a','#4c6682'],['#2a5a7a','#3a7a9a','#5a9aba','#7ab8d4'],['#1a4a7a','#2a6aa8','#4a8ad0','#8ac0f0'])
W['cerulon']=('Cerulon',[B('cerulean_stone','Cerulean Stone','terrain',stone(cer,103)),B('crystal_sand','Crystal Sand','terrain · smelts to Crystal Glass',T.speck(T.sand(['#6a8aa8','#86a6c2','#a2c0d8','#c0d8ea'],20),21,['#ffffff','#9ff0ff'],12)),
 B('azure_moss','Azure Moss','terrain',T.noise(['#14385a','#1e5a88','#2e7ab0','#5aa8d8'],22),T.side_cover(cer,['#14385a','#1e5a88','#2e7ab0','#5aa8d8'],23),stone(cer,103)),
 B('cerulean_geode_shell','Geode Shell','terrain',T.speck(stone(['#20304a','#2e425e','#3c5474','#4e688a'],24),25,['#1592b8'],8)),
 B('budding_cerulite','Budding Crystal','terrain · grows clusters',T.speck(T.noise(['#0d5f7c','#1592b8','#3fc9e8','#b0f2ff'],26),27,['#ffffff'],6)),
 B('cerulite_cluster','Crystal Cluster','plant · glows',T.plant('crystal',['#0d5f7c','#1592b8','#3fc9e8','#e8ffff'],None,28),kind='cross'),
 B('starbloom','Starbloom','flower · dye',T.plant('flower',['#2a3a6a','#3c3c9a','#9696f0','#fff4a0'],None,29),kind='cross')]
 +wood('shardwood','Shardwood',*sw,30,'#b0f2ff')+[B('pulsar_lamp','Pulsar Lamp','light · pulses',T.lamp(['#0f1b33','#1c2e4e','#2b4a7c','#3f68a8'],['#2f7fd0','#5fb6ff','#e8f8ff'],31))]
 +building('cerulean_stone','Cerulean Stone',cer,32))
sk=S['skarn_rock']; marble=['#8a7a70','#b0a296','#cfc2b6','#e6ddd2']; cw=(['#0a0808','#161212','#221c1a','#302826'],['#2a1a14','#3e2a20','#523a2c','#6a4c3a'],['#3a1a0a','#6a2a0e','#a04a1a','#e07a2a'])
W['skarn']=('Skarn',[B('skarn_rock','Skarn Rock','terrain',stone(sk,104)),B('scorched_marble','Scorched Marble','terrain',T.cracked(marble,40,'#e8661e',4)),
 B('slag','Slag','terrain · gravel-like',T.noise(['#1a1412','#2e2420','#4a3a32','#6a564a'],41,(.25,.55,.85))),
 B('ember_crust','Ember Crust','terrain · hurts to stand on',T.cracked(sk,42,'#ff8a2a',7)),B('rift_glass','Rift Glass','terrain · translucent',T.glass('#3a1f52','#5e3a80',43,140)),
 B('emberthorn','Emberthorn','plant · damages on touch',T.plant('bush',['#1a0e08','#4a2a18','#6a3a20','#ff8a2a'],None,44),kind='cross'),
 B('cinder_cap','Cinder Cap','fungus · glows',T.plant('fungus',['#3a2a24','#c05a10','#f08a28','#ffd08a'],None,45),kind='cross')]
 +wood('charwood','Charwood',*cw,46,'#ff8a2a')+[B('tremor_lamp','Tremor Lamp','light · flickers',T.lamp(['#151312','#2a2420','#3e3834','#5c5550'],['#c05a10','#f08a28','#fff0c0'],47))]
 +building('skarn_rock','Skarn Rock',sk,48)+building('scorched_marble','Scorched Marble',marble,51))
pf=S['permafrost']; hw=(['#4a5a66','#6a7a86','#8a9aa6','#b0c0ca'],['#8a9aa6','#a6b6c0','#c2d0d8','#dce6ec'],['#5a7a8a','#8ab0c0','#b8d8e4','#eaf8ff'])
hull=K.casing(['#2a3036','#4a525a','#6a747e','#8a949e','#aeb8c2'],60,'#9ff0f0').im
cor=T.speck(hull,61,['#d49a5a','#a86a3a','#6a4a2a'],22)
con=K.F(hull); con.r(3,4,12,11,'#0c1418'); con.r(4,5,11,10,'#12303a'); [con.p(x,7,'#7ae8ff') for x in range(4,11,3)]; con.p(9,9,'#ff5a5a'); con.p(5,9,'#7ae8ff')
pod=K.F(hull); pod.r(4,2,11,13,'#9aa8b8'); pod.r(5,3,10,12,'#1a3a4a'); pod.r(6,4,9,11,'#5cb4d0'); pod.r(7,5,8,6,'#e8ffff')
W['eidolon']=('Eidolon',[B('permafrost','Permafrost','terrain',stone(pf,105)),B('frozen_regolith','Frozen Regolith','terrain',T.speck(T.sand(['#9aaab4','#b4c2ca','#ccd8de','#e4ecf0'],62),63,['#ffffff'],10)),
 B('phantom_ice','Phantom Ice','terrain · glows faintly',T.glass('#8ab0c0','#bff0ff',64,170)),B('hull_plating','Hull Plating','derelict',hull),
 B('corroded_hull','Corroded Hull','derelict',cor),B('broken_console','Broken Console','derelict · lore block',hull,con.im),
 B('cryo_pod','Cryo Pod','derelict · loot',hull,pod.im),
 B('frostfern','Frostfern','plant',T.plant('fern',['#3a5a66','#8ab0c0','#c4e0ec','#f4fcff'],None,65),kind='cross'),
 B('ghostbloom','Ghostbloom','flower · glows',T.plant('flower',['#46687e','#90b4c4','#d0fbfb','#ffffff'],'frost',66),kind='cross')]
 +wood('hoarwood','Hoarwood',*hw,67,'#ffffff')+[B('spectral_lantern','Spectral Lantern','light',T.lamp(['#1c2226','#3a464c','#5e6e74','#8ea2a8'],['#3aa4ac','#78dde0','#e8ffff'],68))]
 +building('permafrost','Permafrost',pf,69)+building('hull','Hull',['#2a3036','#4a525a','#6a747e','#8a949e'],72))
so=S['solar_stone']; gw=(['#5a3a0a','#8a5a10','#b07a1a','#d8a030'],['#6a3a1a','#8a5226','#a86a32','#c88a48'],['#8a3a0a','#c4600e','#f08a14','#ffd060'])
vent=T.cracked(['#2a0e06','#3a1408','#4a1c0c','#5a2410'],80,'#ffb040',3); vf=K.F(vent); vf.r(6,6,9,9,'#1a0804'); vf.r(7,7,8,8,'#ff7a1a')
W['solvane']=('Solvane',[B('solar_stone','Solar Stone','terrain',stone(so,106)),B('corona_crust','Corona Crust','terrain · burns, glows',T.cracked(['#c4600e','#e08018','#f0a030','#ffd060'],81,'#ffffff',6)),
 B('sunspot_rock','Sunspot Rock','terrain · safe to stand on',stone(['#1a0c08','#26120c','#321a12','#402418'],82)),
 B('slag_glass','Slag Glass','terrain',T.glass('#5a2a14','#a04a1a',83,170)),B('flare_vent','Flare Vent','terrain · fire geysers',vf.im,vent),
 B('solflower','Solflower','flower · heat-proof',T.plant('flower',['#6a3a0a','#e0a010','#ffd040','#ffffff'],None,84),kind='cross'),
 B('pyrevine','Pyrevine','vine · glows',T.plant('vine',['#3a1a08','#c4600e','#ff9a30','#fff0a0'],None,85),kind='cross')]
 +wood('gildwood','Gildwood',*gw,86,'#fff4a8')+[B('radiant_bricks','Radiant Bricks','decor · glows softly',T.speck(T.bricks(['#6a3a10','#a86a00','#e0a010','#ffd040'],87),88,['#fff4a8'],6)),
 B('fusion_lamp','Fusion Lamp','light · brightest',T.lamp(['#3a0a04','#6a1a08','#a02a08','#c44a10'],['#ffa030','#fff0a0','#ffffff'],89))]
 +building('solar_stone','Solar Stone',so,90))
g=['#3a3a3a','#5a5a5a','#7a7a7a','#9a9a9a']; gl=['#6a6a6a','#8a8a8a','#aaaaaa','#cacaca']
W['wastelands']=('Wasteland blocks (grayscale, tinted per galaxy)',[
 B('abyssal_stone','Abyssal Stone','ocean',stone(g,120)),B('tidesand','Tidesand','ocean',T.sand(gl,121)),B('brine_crystal','Brine Crystal','ocean · signature',T.plant('crystal',g[:3]+['#ffffff'],None,122),kind='cross'),
 B('glowkelp','Glowkelp','ocean · plant',T.plant('vine',g[:3]+['#ffffff'],None,123),kind='cross'),
 B('sunbaked_stone','Sunbaked Stone','desert',stone(gl,124)),B('dunesand','Dunesand','desert',T.sand(gl,125)),B('salt_crust','Salt Crust','desert',T.cracked(['#b0b0b0','#c4c4c4','#d8d8d8','#ececec'],126,'#8a8a8a',4)),
 B('ruinstone','Ruinstone','desert · signature',T.cracked(T.bricks(g,127) and g,127,'#2a2a2a',3) if False else T.bricks(gl,127)),
 B('scoria','Scoria','volcanic',T.noise(['#1a1a1a','#2e2e2e','#444444','#5a5a5a'],128,(.3,.6,.85))),B('ashfall','Ashfall','volcanic · layer',T.sand(['#4a4a4a','#5e5e5e','#727272','#888888'],129)),
 B('vent_rock','Vent Rock','volcanic · signature',T.cracked(g,130,'#e0e0e0',5)),B('glassy_obsidian','Glassy Obsidian','volcanic',T.speck(T.noise(['#0a0a0a','#141414','#1e1e1e','#2a2a2a'],131),132,['#6a6a6a'],8)),
 B('frostrock','Frostrock','frozen',stone(gl,133)),B('snowpack','Snowpack','frozen · layer',T.sand(['#c8c8c8','#d8d8d8','#e8e8e8','#f6f6f6'],134)),
 B('glacial_ice','Glacial Ice','frozen · slippery',T.ice(['#8a8a8a','#a6a6a6','#c4c4c4','#e4e4e4'],135)),B('frost_crystal','Frost Crystal','frozen · signature',T.plant('crystal',gl[:3]+['#ffffff'],None,136),kind='cross'),
 B('sludgestone','Sludgestone','toxic',stone(g,137)),B('toxic_mud','Toxic Mud','toxic',T.noise(['#2a2a2a','#3a3a3a','#4a4a4a','#5e5e5e'],138)),
 B('blightmoss','Blightmoss','toxic',T.noise(gl,139),T.side_cover(g,gl,140),stone(g,137)),B('acid_still','Acid (fluid)','toxic · signature',T.glass('#8a8a8a','#bbbbbb',141,200)),
 B('prismstone','Prismstone','crystal',stone(gl,142)),B('prism_cluster','Prism Cluster','crystal · signature',T.plant('crystal',gl[:3]+['#ffffff'],None,143),kind='cross'),
 B('shimmer_sand','Shimmer Sand','crystal',T.speck(T.sand(gl,144),145,['#ffffff'],14)),B('refracting_glass','Refracting Glass','crystal',T.glass('#aaaaaa','#dddddd',146,110)),
 B('craterstone','Craterstone','barren',stone(g,147)),B('crater_dust','Dust','barren · layer',T.sand(g,148)),
 B('meteorite_fragment','Meteorite Fragment','barren · signature',T.speck(stone(['#1a1a1a','#2a2a2a','#3a3a3a','#4a4a4a'],149),150,['#cfcfcf','#9a9a9a'],12))])

CWd,CHt=300,200
def card(b):
    im=Image.new('RGBA',(CWd,CHt),(255,255,255,255)); d=ImageDraw.Draw(im); d.rectangle([0,0,CWd-1,CHt-1],outline=BORDER)
    d.rounded_rectangle([8,8,142,142],6,fill=PANEL)
    if b['kind']=='cross':
        c=b['top'].resize((96,96),Image.NEAREST); im.alpha_composite(c,(27,27))
    else:
        c=cube(b['top'],b['side'],b['side'],s=4); im.alpha_composite(c,(8+(134-c.width)//2,8+(134-c.height)//2))
    ch=checker(64); ch.alpha_composite(up(b['side'] if b['kind']!='cross' else b['top'],4)); im.alpha_composite(ch,(158,10)); d.rectangle([158,10,221,73],outline=BORDER)
    d.text((158,76),'SIDE' if b['kind']!='cross' else 'CROSS',font=FB(8),fill=SUB)
    if b['top'] is not b['side'] and b['kind']!='cross':
        ch=checker(64); ch.alpha_composite(up(b['top'],4)); im.alpha_composite(ch,(228,10)); d.rectangle([228,10,291,73],outline=BORDER); d.text((228,76),'TOP',font=FB(8),fill=SUB)
    x=158
    for s in (1,2):
        ch=checker(16*s,2); ch.alpha_composite(up(b['top'] if b['kind']=='cross' else b['side'],s)); im.alpha_composite(ch,(x,126-16*s)); x+=16*s+8
    d.text((10,150),b['name'],font=FB(13),fill=INK); d.text((10,168),b['typ'],font=FR(10),fill=SUB); d.text((10,182),'zerog_tweaks:'+b['id'],font=FM(9),fill=SUB)
    return im
def save(b):
    if b['kind']=='column' or b['top'] is not b['side']:
        b['side'].save(f"{OUT}/{b['id']}.png" if b['kind']!='column' else f"{OUT}/{b['id']}.png"); b['top'].save(f"{OUT}/{b['id']}_top.png")
    else: b['top'].save(f"{OUT}/{b['id']}.png")
n=9
for key,(title,lst) in W.items():
    for b in lst: save(b)
    cols=5; gap=10; M0=28; top=96; nr=(len(lst)+cols-1)//cols
    Wd=M0*2+cols*CWd+(cols-1)*gap; H=top+nr*(CHt+gap)+20
    im=Image.new('RGBA',(Wd,H),(246,245,242,255)); d=ImageDraw.Draw(im)
    d.text((M0,24),f'{title}  —  terrain, plants and building blocks',font=FB(28),fill=INK)
    sub='Grayscale textures; the game tints them per galaxy with a block color handler.' if key=='wastelands' else 'Cubes show the side face; blocks with a different top show both. Plants use the cross model. Building sets add stairs, slab and wall.'
    d.text((M0,64),sub,font=FR(13),fill=SUB)
    for i,b in enumerate(lst): im.alpha_composite(card(b),(M0+(i%cols)*(CWd+gap),top+(i//cols)*(CHt+gap)))
    im.convert('RGB').save(f'sheets/{n:02d}_{key}_blocks.png'); n+=1
with zipfile.ZipFile('zerog_tweaks_textures.zip','w') as z:
    for root,_,files in os.walk('out'):
        for f in files: z.write(os.path.join(root,f),os.path.relpath(os.path.join(root,f),'out'))
print(sum(len(f) for _,_,f in os.walk('out')))
