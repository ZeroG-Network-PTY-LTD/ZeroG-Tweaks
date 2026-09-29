import os, json, random, math, zipfile
from PIL import Image, ImageDraw, ImageFont
import terrain as T
from tex import hx, stone
from data import STONES
NS='zerog_tweaks'; A=f'out/assets/{NS}'; D=f'out/data/{NS}'
for p in ['textures/block','blockstates','models/block','models/item']: os.makedirs(f'{A}/{p}',exist_ok=True)
for p in ['recipe','loot_table/blocks']: os.makedirs(f'{D}/{p}',exist_ok=True)
os.makedirs('out/data/minecraft/tags/block/mineable',exist_ok=True); os.makedirs('out/data/minecraft/tags/item',exist_ok=True)
def mix(c,t,f):
    a=hx(c); b=hx(t); return '#%02x%02x%02x'%tuple(int(a[i]*(1-f)+b[i]*f) for i in range(3))
def black(p): return [mix(c,'#0a090e',.72) for c in p]
def cobbled(p,s):
    r=random.Random(s); pts=[(r.uniform(0,16),r.uniform(0,16)) for _ in range(9)]; im=Image.new('RGBA',(16,16)); px=im.load()
    cols=[r.choice(p[1:4]) for _ in pts]
    def near(x,y):
        ds=sorted(((min(abs(x-a),16-abs(x-a))**2+min(abs(y-b),16-abs(y-b))**2,i) for i,(a,b) in enumerate(pts)))
        return ds[0][1], math.sqrt(ds[1][0])-math.sqrt(ds[0][0])
    for y in range(16):
        for x in range(16):
            i,g=near(x+.5,y+.5); px[x,y]=hx(p[0] if g<.9 else cols[i])
            if g>=.9 and r.random()<.12: px[x,y]=hx(p[3])
    return im
def smooth(p,s):
    im=T.noise([p[2],p[2],p[2],p[3]],s,(.3,.6,.93)); px=im.load()
    for i in range(16): px[i,0]=hx(p[3]); px[0,i]=hx(p[3]); px[i,15]=hx(p[1]); px[15,i]=hx(p[1])
    return im
def smooth_side(p,s):
    im=smooth(p,s); px=im.load()
    for i in range(16): px[i,7]=hx(p[1]); px[i,8]=hx(p[3])
    return im
def cracked_bricks(p,s):
    im=T.bricks(p,s); px=im.load(); r=random.Random(s)
    for _ in range(3):
        x,y=r.randrange(16),r.randrange(16)
        for _ in range(5): px[x%16,y%16]=hx(p[0]); x+=r.choice([-1,0,1]); y+=1
    return im
FAM=[('lunar_stone','Lunar Stone',STONES['lunar_stone'],False),('mare_basalt','Mare Basalt',['#1c1c22','#2a2a32','#383842','#484852'],False),
('martian_stone','Martian Stone',STONES['martian_stone'],False),('cerulean_stone','Cerulean Stone',STONES['cerulean_stone'],False),
('skarn_rock','Skarn Rock',STONES['skarn_rock'],False),('scorched_marble','Scorched Marble',['#8a7a70','#b0a296','#cfc2b6','#e6ddd2'],False),
('permafrost','Permafrost',STONES['permafrost'],False),('solar_stone','Solar Stone',STONES['solar_stone'],False),
('abyssal_stone','Abyssal Stone',['#3a3a3a','#5a5a5a','#7a7a7a','#9a9a9a'],True),('sunbaked_stone','Sunbaked Stone',['#6a6a6a','#8a8a8a','#aaaaaa','#cacaca'],True),
('scoria','Scoria',['#1a1a1a','#2e2e2e','#444444','#5a5a5a'],True),('frostrock','Frostrock',['#6a6a6a','#8a8a8a','#aaaaaa','#cacaca'],True),
('sludgestone','Sludgestone',['#3a3a3a','#5a5a5a','#7a7a7a','#9a9a9a'],True),('prismstone','Prismstone',['#6a6a6a','#8a8a8a','#aaaaaa','#cacaca'],True),
('craterstone','Craterstone',['#3a3a3a','#5a5a5a','#7a7a7a','#9a9a9a'],True)]
LANG={}; TAGS={'mineable/pickaxe':[],'stairs':[],'slabs':[],'walls':[]}; FAMS={}
def wj(path,obj): json.dump(obj,open(path,'w'),indent=2)
def tx(n): return f'{NS}:block/{n}'
def cube(id,tex=None,render=None):
    wj(f'{A}/blockstates/{id}.json',{'variants':{'':{'model':f'{NS}:block/{id}'}}})
    m={'parent':'minecraft:block/cube_all','textures':{'all':tx(tex or id)}}
    if render: m['render_type']=render
    wj(f'{A}/models/block/{id}.json',m); wj(f'{A}/models/item/{id}.json',{'parent':f'{NS}:block/{id}'})
def stairs(id,t):
    for suf,par in [('','stairs'),('_inner','inner_stairs'),('_outer','outer_stairs')]:
        wj(f'{A}/models/block/{id}{suf}.json',{'parent':f'minecraft:block/{par}','textures':{'bottom':tx(t),'top':tx(t),'side':tx(t)}})
    V={}; rot={'east':0,'south':90,'west':180,'north':270}
    for f in rot:
        for half in ('bottom','top'):
            for sh in ('straight','inner_left','inner_right','outer_left','outer_right'):
                m=f'{NS}:block/{id}'+('_inner' if 'inner' in sh else '_outer' if 'outer' in sh else '')
                y=rot[f]
                if half=='bottom' and sh.endswith('left'): y=(y+270)%360
                if half=='top' and sh.endswith('right'): y=(y+90)%360
                v={'model':m}
                if half=='top': v['x']=180
                if y: v['y']=y
                if half=='top' or y: v['uvlock']=True
                V[f'facing={f},half={half},shape={sh}']=v
    wj(f'{A}/blockstates/{id}.json',{'variants':V}); wj(f'{A}/models/item/{id}.json',{'parent':f'{NS}:block/{id}'})
def slab(id,full,t,side=None):
    s=side or t
    wj(f'{A}/models/block/{id}.json',{'parent':'minecraft:block/slab','textures':{'bottom':tx(t),'top':tx(t),'side':tx(s)}})
    wj(f'{A}/models/block/{id}_top.json',{'parent':'minecraft:block/slab_top','textures':{'bottom':tx(t),'top':tx(t),'side':tx(s)}})
    dbl=f'{NS}:block/{full}' if not side else f'{NS}:block/{id}_double'
    if side: wj(f'{A}/models/block/{id}_double.json',{'parent':'minecraft:block/cube_column','textures':{'end':tx(t),'side':tx(s)}})
    wj(f'{A}/blockstates/{id}.json',{'variants':{'type=bottom':{'model':f'{NS}:block/{id}'},'type=top':{'model':f'{NS}:block/{id}_top'},'type=double':{'model':dbl}}})
    wj(f'{A}/models/item/{id}.json',{'parent':f'{NS}:block/{id}'})
def wall(id,t):
    for suf,par in [('_post','template_wall_post'),('_side','template_wall_side'),('_side_tall','template_wall_side_tall'),('_inventory','wall_inventory')]:
        wj(f'{A}/models/block/{id}{suf}.json',{'parent':f'minecraft:block/{par}','textures':{'wall':tx(t)}})
    mp=[{'when':{'up':'true'},'apply':{'model':f'{NS}:block/{id}_post'}}]
    for d,y in [('north',0),('east',90),('south',180),('west',270)]:
        for h,s in [('low','_side'),('tall','_side_tall')]:
            a={'model':f'{NS}:block/{id}{s}','uvlock':True}
            if y: a['y']=y
            mp.append({'when':{d:h},'apply':a})
    wj(f'{A}/blockstates/{id}.json',{'multipart':mp}); wj(f'{A}/models/item/{id}.json',{'parent':f'{NS}:block/{id}_inventory'})
def I(i): return {'item':f'{NS}:{i}'}
def R(n,o): wj(f'{D}/recipe/{n}.json',o)
def shaped(n,pat,key,res,c=1): R(n,{'type':'minecraft:crafting_shaped','category':'building','pattern':pat,'key':{k:I(v) for k,v in key.items()},'result':{'id':f'{NS}:{res}','count':c}})
def smelt(n,a,b): R(n,{'type':'minecraft:smelting','category':'blocks','ingredient':I(a),'result':{'id':f'{NS}:{b}'},'experience':0.1,'cookingtime':200})
def cut(src,res,c=1): R(f'{res}_from_{src}_stonecutting',{'type':'minecraft:stonecutting','ingredient':I(src),'result':{'id':f'{NS}:{res}','count':c}})
def loot(id,drop=None,slab_=False,silk=None):
    e={'type':'minecraft:item','name':f'{NS}:{drop or id}'}
    if slab_: e['functions']=[{'function':'minecraft:set_count','count':2,'conditions':[{'condition':'minecraft:block_state_property','block':f'{NS}:{id}','properties':{'type':'double'}}]},{'function':'minecraft:explosion_decay'}]
    if silk: e={'type':'minecraft:alternatives','children':[{'type':'minecraft:item','name':f'{NS}:{id}','conditions':[{'condition':'minecraft:match_tool','predicate':{'predicates':{'minecraft:enchantments':[{'enchantments':'minecraft:silk_touch','levels':{'min':1}}]}}}]},{'type':'minecraft:item','name':f'{NS}:{silk}'}]}
    pool={'rolls':1,'bonus_rolls':0,'entries':[e]}
    if not slab_: pool['conditions']=[{'condition':'minecraft:survives_explosion'}]
    wj(f'{D}/loot_table/blocks/{id}.json',{'type':'minecraft:block','pools':[pool]})
TX=f'{A}/textures/block'
for n,(k,name,p,tint) in enumerate(FAM):
    s=500+n*13; bp=black(p)
    if not os.path.exists(f'{TX}/{k}.png'): stone(p,s).save(f'{TX}/{k}.png')
    texs={f'cobbled_{k}':cobbled(p,s),f'smooth_{k}':smooth(p,s+1),f'smooth_{k}_slab_side':smooth_side(p,s+1),
          f'polished_{k}':T.polished(p,s+2),f'{k}_bricks':T.bricks(p,s+3),f'cracked_{k}_bricks':cracked_bricks(p,s+3),f'chiseled_{k}':T.chiseled(p,s+4),
          f'polished_black_{k}':T.polished(bp,s+5),f'polished_black_{k}_bricks':T.bricks(bp,s+6),f'chiseled_polished_black_{k}':T.chiseled(bp,s+7)}
    for t,im in texs.items(): im.save(f'{TX}/{t}.png')
    full=[k,f'cobbled_{k}',f'smooth_{k}',f'polished_{k}',f'{k}_bricks',f'cracked_{k}_bricks',f'chiseled_{k}',f'polished_black_{k}',f'polished_black_{k}_bricks',f'chiseled_polished_black_{k}']
    names=[name,f'Cobbled {name}',f'Smooth {name}',f'Polished {name}',f'{name} Bricks',f'Cracked {name} Bricks',f'Chiseled {name}',f'Polished Black {name}',f'Polished Black {name} Bricks',f'Chiseled Polished Black {name}']
    shapes=[]
    for b,nm in zip(full,names):
        cube(b); LANG[f'block.{NS}.{b}']=nm; TAGS['mineable/pickaxe'].append(b)
        loot(b,silk=f'cobbled_{k}' if b==k else None)
    for b,nm in zip(full,names):
        base=b[:-7] if b.endswith('_bricks') else b; bn=nm
        sid=b[:-1] if b.endswith('_bricks') else b
        st,sl,wl=f'{sid}_stairs',f'{sid}_slab',f'{sid}_wall'
        stairs(st,b); slab(sl,b,b,f'smooth_{k}_slab_side' if b==f'smooth_{k}' else None)
        LANG[f'block.{NS}.{st}']=nm.removesuffix('s')+' Stairs' if nm.endswith('Bricks') else nm+' Stairs'
        LANG[f'block.{NS}.{sl}']=(nm[:-1] if nm.endswith('Bricks') else nm)+' Slab'
        LANG[f'block.{NS}.{st}']=(nm[:-1] if nm.endswith('Bricks') else nm)+' Stairs'
        TAGS['stairs'].append(st); TAGS['slabs'].append(sl); TAGS['mineable/pickaxe']+= [st,sl]
        loot(st); loot(sl,slab_=True)
        shaped(st,['#  ','## ','###'],{'#':b},st,4); shaped(sl,['###'],{'#':b},sl,6); cut(b,st); cut(b,sl,2)
        if True:
            wall(wl,b); LANG[f'block.{NS}.{wl}']=(nm[:-1] if nm.endswith('Bricks') else nm)+' Wall'
            TAGS['walls'].append(wl); TAGS['mineable/pickaxe'].append(wl); loot(wl)
            shaped(wl,['###','###'],{'#':b},wl,6); cut(b,wl)
        shapes.append(sid)
    smelt(f'{k}_from_smelting_cobbled',f'cobbled_{k}',k); smelt(f'smooth_{k}',k,f'smooth_{k}'); smelt(f'cracked_{k}_bricks',f'{k}_bricks',f'cracked_{k}_bricks')
    shaped(f'polished_{k}',['##','##'],{'#':k},f'polished_{k}',4); shaped(f'{k}_bricks',['##','##'],{'#':f'polished_{k}'},f'{k}_bricks',4)
    shaped(f'chiseled_{k}',['#','#'],{'#':f'polished_{k}_slab'},f'chiseled_{k}')
    shaped(f'polished_black_{k}',['###','#N#','###'],{'#':f'polished_{k}','N':'nullifite_nugget'},f'polished_black_{k}',8)
    shaped(f'polished_black_{k}_bricks',['##','##'],{'#':f'polished_black_{k}'},f'polished_black_{k}_bricks',4)
    shaped(f'chiseled_polished_black_{k}',['#','#'],{'#':f'polished_black_{k}_slab'},f'chiseled_polished_black_{k}')
    for t in [f'polished_{k}',f'{k}_bricks',f'chiseled_{k}']: cut(k,t)
    for t in [f'polished_black_{k}_bricks',f'chiseled_polished_black_{k}']: cut(f'polished_black_{k}',t)
    FAMS[k]=(name,full,names,shapes,tint)

EXTRA=[('hull_plating','Hull Plating'),('corroded_hull','Corroded Hull'),('radiant_bricks','Radiant Bricks'),('olympium_plating','Olympium Plating'),
('sunspot_rock','Sunspot Rock'),('oxide_crust','Oxide Crust'),('ruinstone','Ruinstone'),('salt_crust','Salt Crust'),('slag','Slag'),('frozen_regolith','Frozen Regolith')]
for b,nm in EXTRA:
    if not os.path.exists(f'{A}/blockstates/{b}.json'): cube(b); LANG[f'block.{NS}.{b}']=nm; loot(b); TAGS['mineable/pickaxe'].append(b)
    sid=b[:-1] if b.endswith('_bricks') else b; bn=nm[:-1] if nm.endswith('Bricks') else nm
    st,sl,wl=f'{sid}_stairs',f'{sid}_slab',f'{sid}_wall'
    stairs(st,b); slab(sl,b,b); wall(wl,b)
    for i,suf in ((st,'Stairs'),(sl,'Slab'),(wl,'Wall')): LANG[f'block.{NS}.{i}']=f'{bn} {suf}'
    TAGS['stairs'].append(st); TAGS['slabs'].append(sl); TAGS['walls'].append(wl); TAGS['mineable/pickaxe']+=[st,sl,wl]
    loot(st); loot(sl,slab_=True); loot(wl)
    shaped(st,['#  ','## ','###'],{'#':b},st,4); shaped(sl,['###'],{'#':b},sl,6); shaped(wl,['###','###'],{'#':b},wl,6)
    cut(b,st); cut(b,sl,2); cut(b,wl)
# glass from sands
GL=[('lunar_glass','Lunar Glass','regolith','#c8c8cc','#e6e6ea'),('rust_glass','Rust Glass','rustsand','#9a3e1e','#d06a38'),('crystal_glass','Crystal Glass','crystal_sand','#3f68a8','#9ff0ff'),
('frost_glass','Frost Glass','frozen_regolith','#8ab0c0','#e4f4fa'),('tide_glass','Tide Glass','tidesand','#8a8a8a','#bdbdbd'),('dune_glass','Dune Glass','dunesand','#9a9a9a','#cacaca'),('shimmer_glass','Shimmer Glass','shimmer_sand','#aaaaaa','#e0e0e0')]
for id,nm,src,fr,tn in GL:
    T.glass(fr,tn,1,90).save(f'{TX}/{id}.png'); cube(id,render='minecraft:translucent'); LANG[f'block.{NS}.{id}']=nm; loot(id)
    smelt(id,src,id)
# wood stairs/slabs
for w,nm in [('shardwood','Shardwood'),('charwood','Charwood'),('hoarwood','Hoarwood'),('gildwood','Gildwood')]:
    b=f'{w}_planks'; stairs(f'{w}_stairs',b); slab(f'{w}_slab',b,b); LANG[f'block.{NS}.{w}_stairs']=f'{nm} Stairs'; LANG[f'block.{NS}.{w}_slab']=f'{nm} Slab'
    shaped(f'{w}_stairs',['#  ','## ','###'],{'#':b},f'{w}_stairs',4); shaped(f'{w}_slab',['###'],{'#':b},f'{w}_slab',6); loot(f'{w}_stairs'); loot(f'{w}_slab',slab_=True)
    TAGS['stairs'].append(f'{w}_stairs'); TAGS['slabs'].append(f'{w}_slab')
json.dump(LANG,open(f'{A}/lang/en_us.json','w') if os.makedirs(f'{A}/lang',exist_ok=True) is None else None,indent=2)
wj('out/data/minecraft/tags/block/mineable/pickaxe.json',{'replace':False,'values':[f'{NS}:{v}' for v in TAGS['mineable/pickaxe']]})
for t in ('stairs','slabs','walls'):
    wj(f'out/data/minecraft/tags/block/{t}.json',{'replace':False,'values':[f'{NS}:{v}' for v in TAGS[t]]})
    wj(f'out/data/minecraft/tags/item/{t}.json',{'replace':False,'values':[f'{NS}:{v}' for v in TAGS[t]]})
wj('out/pack.mcmeta',{'pack':{'pack_format':34,'description':'ZeroG Tweaks assets and data (placeholder art)'}})
import pickle; pickle.dump({k:(v[0],v[1],v[2],v[3],v[4]) for k,v in FAMS.items()},open('fams.pkl','wb')); pickle.dump(GL,open('glass.pkl','wb'))
print(len(LANG),'lang entries;',sum(len(f) for _,_,f in os.walk('out')),'files')
