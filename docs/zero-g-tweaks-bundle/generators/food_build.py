import os, json, re, zipfile
from PIL import Image, ImageDraw, ImageFont
import foodtex as T
from food_data import F, MAT, REW
from mobs_food import M2
from mobs_data import MOBS
NS='zerog_tweaks'; A=f'out/assets/{NS}'; D=f'out/data/{NS}'
IT=f'{A}/textures/item'; os.makedirs(IT,exist_ok=True)
TEX={}
for it in F+MAT+REW:
    im=T.render(it); im.save(f'{IT}/{it["k"]}.png'); TEX[it['k']]=im
def wj(p,o): os.makedirs(os.path.dirname(p),exist_ok=True); json.dump(o,open(p,'w'),indent=2)
# ---- item models + lang for every item texture
lang=json.load(open(f'{A}/lang/en_us.json'))
NAMES={it['k']:it['n'] for it in F+MAT+REW}
def pretty(k): return ' '.join(w.capitalize() for w in k.split('_'))
TOOLS=('_sword','_pickaxe','_axe','_shovel','_hoe')
for fn in sorted(os.listdir(IT)):
    k=fn[:-4]
    wj(f'{A}/models/item/{k}.json',{'parent':'minecraft:item/handheld' if k.endswith(TOOLS) else 'minecraft:item/generated','textures':{'layer0':f'{NS}:item/{k}'}})
    lang[f'item.{NS}.{k}']=NAMES.get(k,pretty(k))
for k,m in list(MOBS.items())+list(M2.items()): lang[f'entity.{NS}.{k}']=m['name']
json.dump(lang,open(f'{A}/lang/en_us.json','w'),indent=2)
# ---- recipes
def I(i): return {'item':i if ':' in i else f'{NS}:{i}'}
def R(n,o): wj(f'{D}/recipe/{n}.json',o)
def cook(src,dst):
    for t,time,suf in (('smelting',200,''),('smoking',100,'_from_smoking'),('campfire_cooking',600,'_from_campfire_cooking')):
        R(f'{dst}{suf}',{'type':f'minecraft:{t}','category':'food','ingredient':I(src),'result':{'id':f'{NS}:{dst}'},'experience':0.35,'cookingtime':time})
raws=[it for it in F if it['kind']=='raw']; cooked=[it for it in F if it['kind']=='cooked']
for it in F:
    if it['kind']=='cooked' and it['src'].startswith('Cook '):
        srcname=it['src'][5:]; src=next((x['k'] for x in F if x['n']==srcname),None)
        if src: cook(src,it['k'])
cook('lunar_lichen','lichen_crisps')
def shapeless(n,ings,c=1): R(n,{'type':'minecraft:crafting_shapeless','category':'misc','ingredients':[I(i) for i in ings],'result':{'id':f'{NS}:{n}','count':c}})
shapeless('astronaut_ration',['baked_tuber','seared_grazer_steak','lichen_crisps'],2)
shapeless('orbit_burger',['minecraft:bread','seared_grazer_steak','skyberries'])
shapeless('nebula_pie',['skyberries','skyberries','blue_egg','shardwood_syrup','minecraft:sugar'])
shapeless('ember_chili',['smoked_boar_chop','grilled_scorch_tail','cinder_cap','minecraft:bowl'])
shapeless('cryo_chowder',['yak_roast','frost_milk','frostfern','minecraft:bowl'])
shapeless('starfall_feast',['cooked_gildcrab','pyrefruit','roasted_solflower_seeds','minecraft:bowl'])
shapeless('cinder_cap_stew',['cinder_cap','cinder_cap','minecraft:bowl'])
shapeless('frostfern_tea',['frostfern','frostfern','minecraft:glass_bottle','minecraft:snowball'])
shapeless('low_g_jelly',['leech_gel','stardust','minecraft:sugar'],2)
shapeless('ration_pack',['yak_roast','baked_tuber','salvium_nugget'],2)
shapeless('capacity_coil',['cyrrium_ingot','pulsar_dust','pulsar_dust','cyrrium_ingot'])
# ---- entity loot tables
def pool(item,lo,hi,chance=None,smelt=None,looting=True):
    fn=[{'function':'minecraft:set_count','count':{'type':'minecraft:uniform','min':lo,'max':hi}}]
    if smelt: fn.append({'function':'minecraft:furnace_smelt','conditions':[{'condition':'minecraft:entity_properties','entity':'this','predicate':{'flags':{'is_on_fire':True}}}]})
    if looting: fn.append({'function':'minecraft:enchanted_count_increase','enchantment':'minecraft:looting','count':{'type':'minecraft:uniform','min':0,'max':1}})
    p={'rolls':1,'bonus_rolls':0,'entries':[{'type':'minecraft:item','name':f'{NS}:{item}','functions':fn}]}
    if chance: p['conditions']=[{'condition':'minecraft:killed_by_player'},{'condition':'minecraft:random_chance_with_enchanted_bonus','enchantment':'minecraft:looting','unenchanted_chance':chance,'enchanted_chance':{'type':'minecraft:linear','base':chance+0.02,'per_level_above_first':0.02}}]
    return p
def loot(mob,pools): wj(f'{D}/loot_table/entities/{mob}.json',{'type':'minecraft:entity','pools':pools})
L={'regolith_crawler':[pool('crawler_leg',0,2,smelt=1),pool('regolith',1,3),pool('selenite',1,1,chance=.05,looting=False)],
'rust_beetle':[pool('beetle_grub',0,1,smelt=1),pool('ferrox_nugget',1,2),pool('rust_shell',1,1,chance=.15,looting=False)],
'crystal_stag':[pool('stag_venison',1,3,smelt=1),pool('crystal_hide',0,2)],
'prismling':[pool('cerulite_nugget' if False else 'pulsar_dust',1,3)],
'cinder_hound':[pool('cinder_pelt',0,1),pool('emberite',0,2)],
'frost_warden':[pool('wraithsteel_ingot',3,5,looting=False),pool('remnant_shard',1,2)],
'flare_sprite':[pool('fusion_dust',0,1),pool('solar_spark',0,1)],
'sun_colossus':[pool('astrium_ingot',4,6,looting=False),pool('coronite',6,10),pool('colossus_core',1,1,looting=False)],
'dune_burrower':[pool('burrower_steak',1,3,smelt=1),pool('burrower_scale',0,1),pool('star_map_fragment',1,1,chance=.05,looting=False)],
'ash_strider':[pool('heatproof_plating',1,1,chance=.08,looting=False)],
'rime_stalker':[pool('frost_pelt',0,1),pool('cryo_core',1,1,chance=.06,looting=False)],
'bog_lurker':[pool('lurker_leg',1,2,smelt=1),pool('venom_gland',0,1),pool('neutralizer',1,1,chance=.06,looting=False)],
'crater_drifter':[pool('stardust',1,2)],
'prism_sentinel':[pool('galaxy_3_gate_key',1,1,looting=False),pool('cerulite',4,6,looting=False),pool('sentinel_prism',1,1,looting=False)],
'rift_tyrant':[pool('galaxy_4_gate_key',1,1,looting=False),pool('skarnite',4,6,looting=False),pool('rift_heart',1,1,looting=False)],
'eidolon_captain':[pool('galaxy_5_gate_key',1,1,looting=False),pool('eidolite',4,6,looting=False)],
'dying_star':[pool('heart_of_solvane',1,1,looting=False),pool('solvanite',6,8,looting=False)],
'moon_hopper':[pool('hopper_meat',0,2,smelt=1),pool('hopper_fluff',1,2)],
'dust_grazer':[pool('grazer_steak',1,3,smelt=1),pool('grazer_hide',0,2)],
'azure_fowl':[pool('fowl',1,1,smelt=1),pool('azure_feather',0,2)],
'glimmerfish':[pool('glimmerfish',1,1,smelt=1,looting=False),pool('glimmer_scale',1,1,chance=.1,looting=False)],
'slag_boar':[pool('boar_chop',1,3,smelt=1),pool('boar_tusk',0,1)],
'scorch_wyrmling':[pool('scorch_tail',1,1,smelt=1,looting=False),pool('scorch_scale',0,2)],
'frost_yak':[pool('yak_meat',1,3,smelt=1),pool('yak_wool',1,2)],
'ice_leech':[pool('leech_gel',1,3)],
'gildcrab':[pool('gildcrab_meat',1,2,smelt=1),pool('gildcrab_shell',0,1)],
'deep_eel':[pool('eel_fillet',1,2,smelt=1),pool('eel_skin',0,1)],
'sand_skitter':[pool('skitter_leg',1,2,smelt=1),pool('skitter_carapace',0,1),pool('venom_gland',1,1,chance=.3)]}
for k,p in L.items(): loot(k,p)
# fix: smelt target mapping handled by furnace_smelt using smelting recipes
# ---- sheets (materials card layout)
Fp='/usr/share/fonts/truetype/dejavu/'; FB=lambda s:ImageFont.truetype(Fp+'DejaVuSans-Bold.ttf',s); FR=lambda s:ImageFont.truetype(Fp+'DejaVuSans.ttf',s); FM=lambda s:ImageFont.truetype(Fp+'DejaVuSansMono.ttf',s)
BG=(246,245,242,255); PANEL=(235,233,243,255); BORDER=(214,212,222,255); INK=(34,32,40,255); SUB=(110,108,118,255)
def checker(w,h,c=6):
    im=Image.new('RGBA',(w,h),(255,255,255,255)); d=ImageDraw.Draw(im)
    for y in range(0,h,c):
        for x in range(0,w,c):
            if (x//c+y//c)%2: d.rectangle([x,y,x+c-1,y+c-1],fill=(238,236,244,255))
    return im
def up(im,s): return im.resize((16*s,16*s),Image.NEAREST)
def shade(c,f): return (int(c[0]*f),int(c[1]*f),int(c[2]*f),c[3])
def extrude(tex,s=9,depth=2):
    W=16*s+depth*s+4; im=Image.new('RGBA',(W,W),(0,0,0,0)); px=tex.load(); d=ImageDraw.Draw(im)
    for k in range(depth*s,0,-1):
        for y in range(16):
            for x in range(16):
                c=px[x,y]
                if c[3]: d.rectangle([x*s+k,y*s+depth*s-k,x*s+k+s-1,y*s+depth*s-k+s-1],fill=shade(c,.55))
    im.alpha_composite(up(tex,s),(0,depth*s)); return im
def wrap(s,f,w,d):
    out=[];line=''
    for word in s.split():
        t=(line+' '+word).strip()
        if d.textlength(t,font=f)>w: out.append(line); line=word
        else: line=t
    return out+[line]
CW,CH=512,300
def card(it,line2):
    tex=TEX[it['k']]; im=Image.new('RGBA',(CW,CH),(255,255,255,255)); d=ImageDraw.Draw(im); d.rectangle([0,0,CW-1,CH-1],outline=BORDER)
    d.text((12,10),it['n'],font=FB(15),fill=INK); d.text((12,30),f"Item · {it.get('kind','material')}   ·   {NS}:{it['k']}",font=FM(10),fill=SUB)
    d.rounded_rectangle([10,50,215,250],8,fill=PANEL); e=extrude(tex,s=8); im.alpha_composite(e,(10+(205-e.width)//2,50+(200-e.height)//2))
    im.alpha_composite(checker(128,128),(230,52)); im.alpha_composite(up(tex,8),(230,52)); d.rectangle([230,52,357,179],outline=BORDER)
    d.rectangle([230,52,262,62],fill=INK); d.text((232,52),'FRONT',font=FB(8),fill=(255,255,255,255))
    x=372
    for s in (1,2,4):
        cb=checker(16*s,16*s,3); cb.alpha_composite(up(tex,s)); im.alpha_composite(cb,(x,178-16*s)); x+=16*s+8
    yy=190
    for ln in wrap(line2,FR(11),CW-240,d)[:4]: d.text((230,yy),ln,font=FR(11),fill=INK); yy+=15
    yy=258
    for ln in wrap(it['src'],FR(11),CW-24,d)[:2]: d.text((12,yy),ln,font=FR(11),fill=SUB); yy+=15
    return im
def sheet(fname,title,sub,items,line_fn,cols3):
    gap=12; M0=28; top=96; nr=(len(items)+2)//3; W=M0*2+3*CW+2*gap
    th=40+26*(len(items)+1); H=top+nr*(CH+gap)+30+th+20
    im=Image.new('RGBA',(W,H),BG); d=ImageDraw.Draw(im); d.text((M0,24),title,font=FB(30),fill=INK); d.text((M0,64),sub,font=FR(13),fill=SUB)
    for i,it in enumerate(items): im.alpha_composite(card(it,line_fn(it)),(M0+(i%3)*(CW+gap),top+(i//3)*(CH+gap)))
    y=top+nr*(CH+gap)+18; d.text((M0,y),'Recipes & uses',font=FB(18),fill=INK); y+=36
    cx=[M0,M0+330,M0+900]; d.rectangle([M0,y,W-M0,y+26],fill=(232,230,240,255))
    for x,h_ in zip(cx,cols3): d.text((x+8,y+6),h_,font=FB(12),fill=INK)
    y+=26
    for j,it in enumerate(items):
        if j%2: d.rectangle([M0,y,W-M0,y+25],fill=(250,249,247,255))
        im.alpha_composite(TEX[it['k']],(M0+8,y+4)); d.text((M0+30,y+5),it['n'],font=FB(12),fill=INK)
        d.text((cx[1]+8,y+6),it['src'][:80],font=FR(11),fill=INK); d.text((cx[2]+8,y+6),line_fn(it)[:95],font=FR(11),fill=INK); y+=26
    im.crop((0,0,W,y+20)).convert('RGB').save(fname)
def nut(it):
    s=f"{it['hun']} hunger ({it['hun']/2:g} drumsticks) · saturation {it['sat']:g}" if it['hun'] else 'Not eaten directly'
    return s+(f" · {it['eff']}" if it['eff'] else '')
os.makedirs('sheets',exist_ok=True)
meats=[it for it in F if it['kind'] in('raw','cooked') and it['src'].startswith(('Drops','Cook')) and not it['k'] in ('baked_tuber','lichen_crisps','roasted_solflower_seeds')]
other=[it for it in F if it not in meats]
sheet('sheets/22_food_meats.png','Meats  —  raw and cooked','Every hunted mob drops a meat; cook it in a furnace, smoker or campfire. Mobs killed while on fire drop it cooked.',meats,nut,['Item','Comes from','Food value and effect'])
sheet('sheets/23_food_crops_dishes.png','Crops, drinks and dishes','Forage and farm on each world, then combine ingredients from several worlds into dishes with long-lasting effects.',other,nut,['Item','Comes from','Food value and effect'])
sheet('sheets/24_mob_materials.png','Mob materials','Non-food drops from the new and existing mobs.',MAT,lambda it:it['use'],['Item','Comes from','Used for'])
sheet('sheets/25_rewards_and_boss_drops.png','Wasteland rewards and boss drops','Upgrade items from wasteland structures and mobs, plus boss trophies and gate keys.',REW,lambda it:it['use'],['Item','Comes from','Used for'])
with zipfile.ZipFile('zerog_tweaks_resources.zip','w') as z:
    for root,_,files in os.walk('out'):
        for f in files: z.write(os.path.join(root,f),os.path.relpath(os.path.join(root,f),'out'))
print(len(os.listdir(IT)),'item textures;',sum(len(f) for _,_,f in os.walk('out')),'files')
