import os, json, random, math, zipfile
from PIL import Image
from data import M, PL
import terrain as TR
NS='zerog_tweaks'; A=f'out/assets/{NS}'; D=f'out/data/{NS}'; TB=f'{A}/textures/block'; TI=f'{A}/textures/item'
def wj(p,o): os.makedirs(os.path.dirname(p),exist_ok=True); json.dump(o,open(p,'w'),indent=2)
def tx(n,kind='block'): return f'{NS}:{kind}/{n}'
lang=json.load(open(f'{A}/lang/en_us.json'))
def pretty(k): return ' '.join(w.capitalize() for w in k.split('_'))
TAG={}
def tag(t,*ids):
    TAG.setdefault(t,[]); TAG[t]+= [i if ':' in i else f'{NS}:{i}' for i in ids]
def itemblock(id,model=None): wj(f'{A}/models/item/{id}.json',{'parent':model or f'{NS}:block/{id}'})
def selfloot(id,drop=None): wj(f'{D}/loot_table/blocks/{id}.json',{'type':'minecraft:block','pools':[{'rolls':1,'bonus_rolls':0,'entries':[{'type':'minecraft:item','name':f'{NS}:{drop or id}'}],'conditions':[{'condition':'minecraft:survives_explosion'}]}]})
SILK={'condition':'minecraft:match_tool','predicate':{'predicates':{'minecraft:enchantments':[{'enchantments':'minecraft:silk_touch','levels':{'min':1}}]}}}
def oreloot(id,drop,lo=1,hi=1):
    fn=[]
    if (lo,hi)!=(1,1): fn.append({'function':'minecraft:set_count','count':{'type':'minecraft:uniform','min':lo,'max':hi}})
    fn+= [{'function':'minecraft:apply_bonus','enchantment':'minecraft:fortune','formula':'minecraft:ore_drops'},{'function':'minecraft:explosion_decay'}]
    wj(f'{D}/loot_table/blocks/{id}.json',{'type':'minecraft:block','pools':[{'rolls':1,'bonus_rolls':0,'entries':[{'type':'minecraft:alternatives','children':[
        {'type':'minecraft:item','name':f'{NS}:{id}','conditions':[SILK]},{'type':'minecraft:item','name':f'{NS}:{drop}','functions':fn}]}]}]})
def cube(id,render=None,parent='minecraft:block/cube_all',textures=None):
    m={'parent':parent,'textures':textures or {'all':tx(id)}}
    if render: m['render_type']=render
    wj(f'{A}/models/block/{id}.json',m); wj(f'{A}/blockstates/{id}.json',{'variants':{'':{'model':f'{NS}:block/{id}'}}}); itemblock(id)
def name(id,n=None): lang[f'block.{NS}.{id}']=n or pretty(id)
existing=set(f[:-5] for f in os.listdir(f'{A}/blockstates'))
tex=sorted(f[:-4] for f in os.listdir(TB)); done=set()
# ---------------- machine-style multi-face
DIRECTIONAL={'gate_controller','gate_lens_housing','combustion_generator','fusion_reactor','ore_refinery','alloy_forge','crystal_growth_chamber','salvage_station'}
for base in sorted({t[:-6] for t in tex if t.endswith('_front')}):
    t={f:tx(f'{base}_{f}') for f in('front','side','top','bottom')}
    if base in DIRECTIONAL:
        wj(f'{A}/models/block/{base}.json',{'parent':'minecraft:block/orientable_with_bottom','textures':{'front':t['front'],'side':t['side'],'top':t['top'],'bottom':t['bottom']}})
        wj(f'{A}/blockstates/{base}.json',{'variants':{f'facing={f}':({'model':f'{NS}:block/{base}','y':y} if y else {'model':f'{NS}:block/{base}'}) for f,y in(('north',0),('east',90),('south',180),('west',270))}})
    else:
        wj(f'{A}/models/block/{base}.json',{'parent':'minecraft:block/cube_bottom_top','textures':{'top':t['top'],'bottom':t['bottom'],'side':t['side']}})
        wj(f'{A}/blockstates/{base}.json',{'variants':{'':{'model':f'{NS}:block/{base}'}}})
    itemblock(base); name(base); selfloot(base); tag('minecraft:mineable/pickaxe',base); done|={f'{base}_{f}' for f in('front','side','top','bottom')}; done.add(base)
# ---------------- plants (cross)
CROSS=['lunar_lichen','rust_lichen','cerulite_cluster','starbloom','emberthorn','cinder_cap','frostfern','ghostbloom','solflower','pyrevine','brine_crystal','glowkelp','frost_crystal','prism_cluster']
for p in CROSS:
    wj(f'{A}/models/block/{p}.json',{'parent':'minecraft:block/cross','textures':{'cross':tx(p)},'render_type':'minecraft:cutout'})
    wj(f'{A}/blockstates/{p}.json',{'variants':{'':{'model':f'{NS}:block/{p}'}}})
    wj(f'{A}/models/item/{p}.json',{'parent':'minecraft:item/generated','textures':{'layer0':tx(p)}}); name(p); done.add(p)
    if p=='cerulite_cluster': oreloot(p,'cerulite')
    elif p=='pyrevine':
        wj(f'{D}/loot_table/blocks/pyrevine.json',{'type':'minecraft:block','pools':[{'rolls':1,'bonus_rolls':0,'entries':[{'type':'minecraft:alternatives','children':[{'type':'minecraft:item','name':f'{NS}:pyrevine','conditions':[{'condition':'minecraft:match_tool','predicate':{'items':'minecraft:shears'}}]},{'type':'minecraft:item','name':f'{NS}:pyrefruit','conditions':[{'condition':'minecraft:random_chance','chance':0.4}]}]}]}]})
    elif p=='solflower':
        selfloot(p); wj(f'{D}/loot_table/blocks/solflower.json',{'type':'minecraft:block','pools':[{'rolls':1,'bonus_rolls':0,'entries':[{'type':'minecraft:item','name':f'{NS}:solflower'}]},{'rolls':1,'bonus_rolls':0,'entries':[{'type':'minecraft:item','name':f'{NS}:solflower_seeds','functions':[{'function':'minecraft:set_count','count':{'type':'minecraft:uniform','min':1,'max':3}}]}]}]})
    else: selfloot(p)
    tag('minecraft:replaceable_by_trees' if False else f'{NS}:plants',p)
    if p in('starbloom','ghostbloom','solflower'): tag('minecraft:small_flowers',p); tag('minecraft:flowers',p)
    tag('minecraft:mineable/hoe',p)
# ---------------- layers (snow-style)
for L in ['ashfall','snowpack','crater_dust']:
    for n in range(1,8):
        wj(f'{A}/models/block/{L}_height{2*n}.json',{'parent':f'minecraft:block/snow_height{2*n}','textures':{'texture':tx(L),'particle':tx(L)}})
    wj(f'{A}/models/block/{L}_block.json',{'parent':'minecraft:block/cube_all','textures':{'all':tx(L)}})
    wj(f'{A}/blockstates/{L}.json',{'variants':{f'layers={n}':{'model':f'{NS}:block/{L}_height{2*n}' if n<8 else f'{NS}:block/{L}_block'} for n in range(1,9)}})
    itemblock(L,f'{NS}:block/{L}_height2'); name(L); tag('minecraft:mineable/shovel',L); done.add(L)
    wj(f'{D}/loot_table/blocks/{L}.json',{'type':'minecraft:block','pools':[{'rolls':1,'bonus_rolls':0,'entries':[{'type':'minecraft:item','name':f'{NS}:{L}','functions':[{'function':'minecraft:set_count','count':n,'conditions':[{'condition':'minecraft:block_state_property','block':f'{NS}:{L}','properties':{'layers':str(n)}}]} for n in range(1,9)]}]}]})
# ---------------- top-textured blocks
BOTTOM={'azure_moss':'cerulean_stone','blightmoss':'sludgestone'}
for base in sorted({t[:-4] for t in tex if t.endswith('_top')}):
    if base in done or base in existing or base.endswith('_log'): continue
    if not os.path.exists(f'{TB}/{base}.png'): continue
    bot=tx(BOTTOM[base]) if base in BOTTOM else (tx(base) if base=='flare_vent' else tx(f'{base}_top'))
    cube(base,parent='minecraft:block/cube_bottom_top',textures={'top':tx(f'{base}_top'),'side':tx(base),'bottom':bot}); name(base)
    if base in BOTTOM: oreloot(base,BOTTOM[base]); tag('minecraft:mineable/shovel',base)
    else: selfloot(base); tag('minecraft:mineable/pickaxe',base)
    done|={base,f'{base}_top'}
# ---------------- materials: ores and storage
GLOW=set()
mats=['nullifite','regolith','moonsteel','selenite','ferrox','olympium','aresite']+[x[0] for _,(_,_,_,l) in PL.items() for x in l]
ROLE={k:M[k]['role'] for k in mats}
for k in mats:
    r=ROLE[k]; ore=f'deepslate_{k}_ore' if k=='nullifite' else f'{k}_ore'
    if ore in tex:
        cube(ore); name(ore); tag('minecraft:mineable/pickaxe',ore); tag('c:ores',ore); tag(f'c:ores/{k}',ore)
        if r=='metal': oreloot(ore,f'raw_{k}')
        elif r=='dust': oreloot(ore,k,4,5)
        elif r=='orb': oreloot(ore,k,4,8)
        else: oreloot(ore,k)
        done.add(ore)
    for b in [f'{k}_block',f'raw_{k}_block']:
        if b in tex and b not in existing:
            cube(b); name(b,('Block of Raw '+M[k]['name']) if b.startswith('raw_') else 'Block of '+M[k]['name']); selfloot(b); tag('minecraft:mineable/pickaxe',b)
            tag('c:storage_blocks',b); tag(f"c:storage_blocks/{'raw_' if b.startswith('raw_') else ''}{k}",b); done.add(b)
# ---------------- remaining singles
TRANS={'rift_glass','phantom_ice','slag_glass','refracting_glass'}
SHOVEL={'regolith','rustsand','crystal_sand','tidesand','dunesand','shimmer_sand','frozen_regolith','toxic_mud','slag'}
for t in tex:
    if t in done or t in existing or t.endswith(('_slab_side','_top')) or t in('acid_still',) or t.endswith(('_log','_leaves')): continue
    if t.endswith(('_front','_side','_bottom')): continue
    cube(t,render='minecraft:translucent' if t in TRANS else None); name(t); selfloot(t)
    tag('minecraft:mineable/shovel' if t in SHOVEL else 'minecraft:mineable/pickaxe',t)
    if t=='budding_cerulite': wj(f'{D}/loot_table/blocks/budding_cerulite.json',{'type':'minecraft:block','pools':[]})
    done.add(t)
# ---------------- full wood sets
WOODS={'shardwood':'Shardwood','charwood':'Charwood','hoarwood':'Hoarwood','gildwood':'Gildwood'}
def load(n): return Image.open(f'{TB}/{n}.png').convert('RGBA')
def lighten(im,f):
    px=im.load(); o=im.copy(); q=o.load()
    for y in range(16):
        for x in range(16):
            c=px[x,y]; q[x,y]=(min(255,int(c[0]*f)),min(255,int(c[1]*f)),min(255,int(c[2]*f)),c[3])
    return o
from tex import hx
def door_tex(pl,half):
    im=pl.copy(); px=im.load(); dark=tuple(int(v*.55) for v in px[0,3][:3])+(255,)
    for i in range(16): px[i,0 if half=='top' else 15]=dark; px[0,i]=dark; px[15,i]=dark
    if half=='top':
        for y in range(3,8):
            for x in range(4,12): px[x,y]=(0,0,0,0)
        for y in range(3,8): px[7,y]=dark; px[8,y]=dark
    else: px[12,6]=(40,40,40,255); px[12,7]=(40,40,40,255)
    return im
for w,nm in WOODS.items():
    side=load(f'{w}_log'); top=load(f'{w}_log_top'); pl=load(f'{w}_planks')
    lighten(pl,1.1).save(f'{TB}/stripped_{w}_log.png'); t2=top.copy(); p2=t2.load(); pp=pl.load()
    for y in range(16):
        for x in range(16):
            if math.hypot(x-7.5,y-7.5)>6.6: p2[x,y]=pp[x,y]
    t2.save(f'{TB}/stripped_{w}_log_top.png')
    door_tex(pl,'top').save(f'{TB}/{w}_door_top.png'); door_tex(pl,'bottom').save(f'{TB}/{w}_door_bottom.png')
    td=pl.copy(); q=td.load()
    for y in (4,5,10,11):
        for x in range(3,13): q[x,y]=(0,0,0,0)
    td.save(f'{TB}/{w}_trapdoor.png')
    di=Image.new('RGBA',(16,16),(0,0,0,0)); di.alpha_composite(door_tex(pl,'top').resize((8,8),Image.NEAREST),(4,0)); di.alpha_composite(door_tex(pl,'bottom').resize((8,8),Image.NEAREST),(4,8)); di.save(f'{TI}/{w}_door.png')
    leafc=load(f'{w}_leaves').getpixel((8,8)); sap=TR.plant('bush',['#3a2a1a','#%02x%02x%02x'%leafc[:3],'#%02x%02x%02x'%tuple(min(255,int(c*1.2)) for c in leafc[:3]),'#ffffff'],None,hash(w)%100); sap.save(f'{TB}/{w}_sapling.png')
    # logs / wood
    for lid,s,tp,lab in [(f'{w}_log',f'{w}_log',f'{w}_log_top',f'{nm} Log'),(f'stripped_{w}_log',f'stripped_{w}_log',f'stripped_{w}_log_top',f'Stripped {nm} Log'),
                         (f'{w}_wood',f'{w}_log',f'{w}_log',f'{nm} Wood'),(f'stripped_{w}_wood',f'stripped_{w}_log',f'stripped_{w}_log',f'Stripped {nm} Wood')]:
        wj(f'{A}/models/block/{lid}.json',{'parent':'minecraft:block/cube_column','textures':{'end':tx(tp),'side':tx(s)}})
        wj(f'{A}/models/block/{lid}_horizontal.json',{'parent':'minecraft:block/cube_column_horizontal','textures':{'end':tx(tp),'side':tx(s)}})
        wj(f'{A}/blockstates/{lid}.json',{'variants':{'axis=y':{'model':f'{NS}:block/{lid}'},'axis=z':{'model':f'{NS}:block/{lid}_horizontal','x':90},'axis=x':{'model':f'{NS}:block/{lid}_horizontal','x':90,'y':90}}})
        itemblock(lid); name(lid,lab); selfloot(lid); tag('minecraft:mineable/axe',lid); tag('minecraft:logs_that_burn',lid); tag(f'{NS}:{w}_logs',lid)
    tag('minecraft:logs',f'#{NS}:{w}_logs')
    cube(f'{w}_planks'); name(f'{w}_planks',f'{nm} Planks'); selfloot(f'{w}_planks'); tag('minecraft:planks',f'{w}_planks'); tag('minecraft:mineable/axe',f'{w}_planks',f'{w}_stairs',f'{w}_slab')
    tag('minecraft:wooden_stairs',f'{w}_stairs'); tag('minecraft:wooden_slabs',f'{w}_slab')
    lf=f'{w}_leaves'; cube(lf,render='minecraft:cutout_mipped'); name(lf,f'{nm} Leaves'); tag('minecraft:leaves',lf); tag('minecraft:mineable/hoe',lf)
    wj(f'{D}/loot_table/blocks/{lf}.json',{'type':'minecraft:block','pools':[{'rolls':1,'bonus_rolls':0,'entries':[{'type':'minecraft:alternatives','children':[
        {'type':'minecraft:item','name':f'{NS}:{lf}','conditions':[{'condition':'minecraft:any_of','terms':[{'condition':'minecraft:match_tool','predicate':{'items':'minecraft:shears'}},SILK]}]},
        {'type':'minecraft:item','name':f'{NS}:{w}_sapling','conditions':[{'condition':'minecraft:survives_explosion'},{'condition':'minecraft:table_bonus','enchantment':'minecraft:fortune','chances':[0.05,0.0625,0.083,0.1]}]}]}]},
        {'rolls':1,'bonus_rolls':0,'entries':[{'type':'minecraft:item','name':'minecraft:stick','functions':[{'function':'minecraft:set_count','count':{'type':'minecraft:uniform','min':1,'max':2}}]}],
         'conditions':[{'condition':'minecraft:inverted','term':{'condition':'minecraft:any_of','terms':[{'condition':'minecraft:match_tool','predicate':{'items':'minecraft:shears'}},SILK]}},{'condition':'minecraft:table_bonus','enchantment':'minecraft:fortune','chances':[0.02,0.022,0.025,0.033,0.1]}]}]})
    sp=f'{w}_sapling'; wj(f'{A}/models/block/{sp}.json',{'parent':'minecraft:block/cross','textures':{'cross':tx(sp)},'render_type':'minecraft:cutout'})
    wj(f'{A}/blockstates/{sp}.json',{'variants':{'':{'model':f'{NS}:block/{sp}'}}}); wj(f'{A}/models/item/{sp}.json',{'parent':'minecraft:item/generated','textures':{'layer0':tx(sp)}})
    name(sp,f'{nm} Sapling'); selfloot(sp); tag('minecraft:saplings',sp)
    P=tx(f'{w}_planks')
    # fence
    fe=f'{w}_fence'
    wj(f'{A}/models/block/{fe}_post.json',{'parent':'minecraft:block/fence_post','textures':{'texture':P}}); wj(f'{A}/models/block/{fe}_side.json',{'parent':'minecraft:block/fence_side','textures':{'texture':P}})
    wj(f'{A}/models/block/{fe}_inventory.json',{'parent':'minecraft:block/fence_inventory','textures':{'texture':P}})
    mp=[{'apply':{'model':f'{NS}:block/{fe}_post'}}]+[{'when':{d:'true'},'apply':dict({'model':f'{NS}:block/{fe}_side','uvlock':True},**({'y':y} if y else {}))} for d,y in(('north',0),('east',90),('south',180),('west',270))]
    wj(f'{A}/blockstates/{fe}.json',{'multipart':mp}); itemblock(fe,f'{NS}:block/{fe}_inventory'); name(fe,f'{nm} Fence'); selfloot(fe); tag('minecraft:wooden_fences',fe); tag('minecraft:mineable/axe',fe)
    # fence gate
    fg=f'{w}_fence_gate'
    for suf,par in(('','template_fence_gate'),('_open','template_fence_gate_open'),('_wall','template_fence_gate_wall'),('_wall_open','template_fence_gate_wall_open')):
        wj(f'{A}/models/block/{fg}{suf}.json',{'parent':f'minecraft:block/{par}','textures':{'texture':P}})
    V={}
    for f,y in(('south',0),('west',90),('north',180),('east',270)):
        for iw in('false','true'):
            for op in('false','true'):
                suf=('_wall' if iw=='true' else '')+('_open' if op=='true' else ''); v={'model':f'{NS}:block/{fg}{suf}','uvlock':True}
                if y: v['y']=y
                V[f'facing={f},in_wall={iw},open={op}']=v
    wj(f'{A}/blockstates/{fg}.json',{'variants':V}); itemblock(fg); name(fg,f'{nm} Fence Gate'); selfloot(fg); tag('minecraft:fence_gates',fg); tag('minecraft:mineable/axe',fg)
    # door
    dr=f'{w}_door'; tt={'top':tx(f'{w}_door_top'),'bottom':tx(f'{w}_door_bottom')}
    for part in('bottom_left','bottom_left_open','bottom_right','bottom_right_open','top_left','top_left_open','top_right','top_right_open'):
        wj(f'{A}/models/block/{dr}_{part}.json',{'parent':f'minecraft:block/door_{part}','textures':tt,'render_type':'minecraft:cutout'})
    V={}; base={'east':0,'south':90,'west':180,'north':270}
    for f,b in base.items():
        for half,hp in(('lower','bottom'),('upper','top')):
            for hinge in('left','right'):
                for op in('false','true'):
                    y=b if op=='false' else (b+90)%360 if hinge=='left' else (b+270)%360
                    v={'model':f'{NS}:block/{dr}_{hp}_{hinge}'+('_open' if op=='true' else '')}
                    if y: v['y']=y
                    V[f'facing={f},half={half},hinge={hinge},open={op}']=v
    wj(f'{A}/blockstates/{dr}.json',{'variants':V}); wj(f'{A}/models/item/{dr}.json',{'parent':'minecraft:item/generated','textures':{'layer0':tx(dr,'item')}})
    name(dr,f'{nm} Door'); tag('minecraft:wooden_doors',dr); tag('minecraft:mineable/axe',dr)
    wj(f'{D}/loot_table/blocks/{dr}.json',{'type':'minecraft:block','pools':[{'rolls':1,'bonus_rolls':0,'entries':[{'type':'minecraft:item','name':f'{NS}:{dr}','conditions':[{'condition':'minecraft:block_state_property','block':f'{NS}:{dr}','properties':{'half':'lower'}}]}],'conditions':[{'condition':'minecraft:survives_explosion'}]}]})
    # trapdoor
    td=f'{w}_trapdoor'
    for suf in('bottom','top','open'): wj(f'{A}/models/block/{td}_{suf}.json',{'parent':f'minecraft:block/template_orientable_trapdoor_{suf}','textures':{'texture':tx(td)},'render_type':'minecraft:cutout'})
    V={}
    for f,y in(('north',0),('east',90),('south',180),('west',270)):
        for half in('bottom','top'):
            for op in('false','true'):
                if op=='false': v={'model':f'{NS}:block/{td}_{half}'}; yy=y
                else:
                    v={'model':f'{NS}:block/{td}_open'}; yy=y
                    if half=='top': v['x']=180; yy=(y+180)%360
                if yy: v['y']=yy
                V[f'facing={f},half={half},open={op}']=v
    wj(f'{A}/blockstates/{td}.json',{'variants':V}); itemblock(td,f'{NS}:block/{td}_bottom'); name(td,f'{nm} Trapdoor'); selfloot(td); tag('minecraft:wooden_trapdoors',td); tag('minecraft:mineable/axe',td)
    # button
    bt=f'{w}_button'
    for suf,par in(('','button'),('_pressed','button_pressed'),('_inventory','button_inventory')): wj(f'{A}/models/block/{bt}{suf}.json',{'parent':f'minecraft:block/{par}','textures':{'texture':P}})
    V={}; fy={'east':90,'north':0,'south':180,'west':270}; cy={'east':270,'north':180,'south':0,'west':90}
    for face,x in(('floor',0),('wall',90),('ceiling',180)):
        for f in fy:
            for pw in('false','true'):
                v={'model':f'{NS}:block/{bt}'+('_pressed' if pw=='true' else '')}
                if x: v['x']=x
                y=cy[f] if face=='ceiling' else fy[f]
                if y: v['y']=y
                if face=='wall': v['uvlock']=True
                V[f'face={face},facing={f},powered={pw}']=v
    wj(f'{A}/blockstates/{bt}.json',{'variants':V}); itemblock(bt,f'{NS}:block/{bt}_inventory'); name(bt,f'{nm} Button'); selfloot(bt); tag('minecraft:wooden_buttons',bt); tag('minecraft:mineable/axe',bt)
    pp_=f'{w}_pressure_plate'
    wj(f'{A}/models/block/{pp_}.json',{'parent':'minecraft:block/pressure_plate_up','textures':{'texture':P}}); wj(f'{A}/models/block/{pp_}_down.json',{'parent':'minecraft:block/pressure_plate_down','textures':{'texture':P}})
    wj(f'{A}/blockstates/{pp_}.json',{'variants':{'powered=false':{'model':f'{NS}:block/{pp_}'},'powered=true':{'model':f'{NS}:block/{pp_}_down'}}}); itemblock(pp_); name(pp_,f'{nm} Pressure Plate'); selfloot(pp_)
    tag('minecraft:wooden_pressure_plates',pp_); tag('minecraft:mineable/axe',pp_)
    # recipes
    def S(n,pat,key,c): wj(f'{D}/recipe/{n}.json',{'type':'minecraft:crafting_shaped','category':'building','pattern':pat,'key':{k:({'tag':v[1:]} if v.startswith('#') else {'item':v if ':' in v else f'{NS}:{v}'}) for k,v in key.items()},'result':{'id':f'{NS}:{n}','count':c}})
    wj(f'{D}/recipe/{w}_planks.json',{'type':'minecraft:crafting_shapeless','category':'building','ingredients':[{'tag':f'{NS}:{w}_logs'}],'result':{'id':f'{NS}:{w}_planks','count':4}})
    S(f'{w}_wood',['##','##'],{'#':f'{w}_log'},3); S(f'stripped_{w}_wood',['##','##'],{'#':f'stripped_{w}_log'},3)
    S(fe,['W#W','W#W'],{'W':f'{w}_planks','#':'minecraft:stick'},3); S(fg,['#W#','#W#'],{'W':f'{w}_planks','#':'minecraft:stick'},1)
    S(dr,['##','##','##'],{'#':f'{w}_planks'},3); S(td,['###','###'],{'#':f'{w}_planks'},2); S(pp_,['##'],{'#':f'{w}_planks'},1)
    wj(f'{D}/recipe/{bt}.json',{'type':'minecraft:crafting_shapeless','category':'redstone','ingredients':[{'item':f'{NS}:{w}_planks'}],'result':{'id':f'{NS}:{bt}','count':1}})
# ---------------- crops
def crop_tex(stage,kind):
    from terrain import plant
    im=Image.new('RGBA',(16,16),(0,0,0,0)); px=im.load(); r=random.Random(stage*7+len(kind))
    h=[3,6,9,12][stage]
    for x in (3,6,9,12):
        hh=h-r.randrange(0,2)
        for y in range(16-hh,16): px[x,y]=hx('#4a6a2a' if kind=='tuber' else '#2e6a4a'); 
        for y in range(16-hh,16,2): px[x+1,y]=hx('#6a8a3a' if kind=='tuber' else '#3e8a5a')
        if stage==3:
            c=hx('#c86a3a') if kind=='tuber' else hx('#5a8ad0'); px[x,16-hh]=c; px[x+1,17-hh]=c
    return im
for kind,cid,item_,nm in (('tuber','rust_tuber_crop','rust_tuber','Rust Tuber'),('berry','skyberry_bush','skyberries','Skyberry Bush')):
    V={}
    for s in range(4):
        crop_tex(s,kind).save(f'{TB}/{cid}_stage{s}.png')
        wj(f'{A}/models/block/{cid}_stage{s}.json',{'parent':'minecraft:block/crop' if kind=='tuber' else 'minecraft:block/cross','textures':({'crop':tx(f'{cid}_stage{s}')} if kind=='tuber' else {'cross':tx(f'{cid}_stage{s}')}),'render_type':'minecraft:cutout'})
        V[f'age={s}']={'model':f'{NS}:block/{cid}_stage{s}'}
    wj(f'{A}/blockstates/{cid}.json',{'variants':V}); name(cid,nm+(' Crop' if kind=='tuber' else '')); tag('minecraft:crops' if kind=='tuber' else 'minecraft:mineable/hoe',cid)
    wj(f'{D}/loot_table/blocks/{cid}.json',{'type':'minecraft:block','pools':[{'rolls':1,'bonus_rolls':0,'entries':[{'type':'minecraft:item','name':f'{NS}:{item_}'}]},
        {'rolls':1,'bonus_rolls':0,'entries':[{'type':'minecraft:item','name':f'{NS}:{item_}','functions':[{'function':'minecraft:apply_bonus','enchantment':'minecraft:fortune','formula':'minecraft:binomial_with_bonus_count','parameters':{'extra':3,'probability':0.5714286}}]}],
         'conditions':[{'condition':'minecraft:block_state_property','block':f'{NS}:{cid}','properties':{'age':'3'}}]}]})
# acid fluid textures
acid=load('acid_still'); acid.save(f'{TB}/acid_flow.png')
# ---------------- emissive overlays for glowing blocks
EMI=['deepslate_nullifite_ore','nebulite_ore','pulsar_dust_ore','starlite_ore','emberite_ore','tremor_dust_ore','rift_opal_ore','cryocite_ore','spectral_dust_ore','remnant_shard_ore','coronite_ore','fusion_dust_ore','nova_pearl_ore',
     'ember_crust','corona_crust','cerulite_cluster','budding_cerulite','pulsar_lamp','tremor_lamp','spectral_lantern','fusion_lamp','selenite_lamp','radiant_bricks','flare_vent']
for e in EMI:
    src=f'{TB}/{e}_top.png' if e=='flare_vent' else f'{TB}/{e}.png'
    if not os.path.exists(src): continue
    im=Image.open(src).convert('RGBA'); px=im.load(); o=Image.new('RGBA',(16,16),(0,0,0,0)); q=o.load()
    for y in range(16):
        for x in range(16):
            c=px[x,y]
            if c[3] and max(c[:3])>=190 and (max(c[:3])-min(c[:3])>50 or min(c[:3])>225): q[x,y]=c
    o.save(f'{TB}/{e}_emissive.png')
    if e in CROSS or e=='flare_vent': continue
    wj(f'{A}/models/block/{e}.json',{'parent':'minecraft:block/block','textures':{'particle':tx(e),'all':tx(e),'glow':tx(f'{e}_emissive')},
        'elements':[{'from':[0,0,0],'to':[16,16,16],'faces':{f:{'texture':'#all','cullface':f} for f in('north','east','south','west','up','down')}},
                    {'from':[0,0,0],'to':[16,16,16],'neoforge_data':{'block_light':15,'sky_light':15},'faces':{f:{'texture':'#glow','cullface':f} for f in('north','east','south','west','up','down')}}],'render_type':'minecraft:cutout'})
# ---------------- material recipes and tags
def R(n,o): wj(f'{D}/recipe/{n}.json',o)
def I(i): return {'item':i if ':' in i else f'{NS}:{i}'}
def pack(small,big,n9=True):
    R(f'{big}_from_{small}',{'type':'minecraft:crafting_shaped','category':'misc','pattern':['###','###','###'],'key':{'#':I(small)},'result':{'id':f'{NS}:{big}','count':1}})
    R(f'{small}_from_{big}',{'type':'minecraft:crafting_shapeless','category':'misc','ingredients':[I(big)],'result':{'id':f'{NS}:{small}','count':9}})
def smelt2(n,a,b,xp=0.7):
    R(n,{'type':'minecraft:smelting','category':'misc','ingredient':I(a),'result':{'id':f'{NS}:{b}'},'experience':xp,'cookingtime':200})
    R(n+'_blasting',{'type':'minecraft:blasting','category':'misc','ingredient':I(a),'result':{'id':f'{NS}:{b}'},'experience':xp,'cookingtime':100})
for k in mats:
    r=ROLE[k]; ore=f'deepslate_{k}_ore' if k=='nullifite' else f'{k}_ore'
    if r=='metal':
        pack(f'{k}_ingot',f'{k}_block'); pack(f'{k}_nugget',f'{k}_ingot'); pack(f'raw_{k}',f'raw_{k}_block')
        smelt2(f'{k}_ingot_from_raw',f'raw_{k}',f'{k}_ingot'); smelt2(f'{k}_ingot_from_ore',ore,f'{k}_ingot')
        tag(f'c:ingots/{k}',f'{k}_ingot'); tag('c:ingots',f'{k}_ingot'); tag(f'c:nuggets/{k}',f'{k}_nugget'); tag('c:nuggets',f'{k}_nugget'); tag(f'c:raw_materials/{k}',f'raw_{k}'); tag('c:raw_materials',f'raw_{k}')
    else:
        pack(k,f'{k}_block'); smelt2(f'{k}_from_ore',ore,k,1.0)
        grp={'dust':'dusts','fuel':'fuels' if False else 'gems','orb':'gems','diamond':'gems','crystal':'gems'}[r]
        if r!='fuel': tag(f'c:{grp}/{k}',k); tag(f'c:{grp}',k)
# ---------------- gear recipes
from gear_sets import S as GS
GEM_CHAIN=['nullifite','olympium','cerulite','skarnite','eidolite','solvanite']
PAT={'sword':['#','#','|'],'pickaxe':['###',' | ',' | '],'axe':['##','#|',' |'],'shovel':['#','|','|'],'hoe':['##',' |',' |'],
     'helmet':['###','# #'],'chestplate':['# #','###','###'],'leggings':['###','# #','# #'],'boots':['# #','# #']}
def mat_of(k): return f'{k}_ingot' if M[k]['role']=='metal' else k
for k in GS:
    if k in GEM_CHAIN[1:]:
        prev=GEM_CHAIN[GEM_CHAIN.index(k)-1]; tpl=f'{k}_upgrade_smithing_template'
        for pc in PAT: R(f'{k}_{pc}_smithing',{'type':'minecraft:smithing_transform','template':I(tpl),'base':I(f'{prev}_{pc}'),'addition':I(mat_of(k)),'result':{'id':f'{NS}:{k}_{pc}'}})
    else:
        for pc,pat in PAT.items():
            key={'#':I(mat_of(k))}
            if '|' in ''.join(pat): key['|']={'item':'minecraft:stick'}
            R(f'{k}_{pc}',{'type':'minecraft:crafting_shaped','category':'equipment','pattern':pat,'key':key,'result':{'id':f'{NS}:{k}_{pc}','count':1}})
# smithing templates (items)
from foodtex import render
for i,k in enumerate(GEM_CHAIN[1:]):
    p=M[k]['pal']; it=dict(k=f'{k}_upgrade_smithing_template',mask='plate',H='#2a2a34',A=p[3],G=p[2],W=p[2])
    render(it).save(f'{TI}/{it["k"]}.png'); wj(f'{A}/models/item/{it["k"]}.json',{'parent':'minecraft:item/generated','textures':{'layer0':tx(it['k'],'item')}})
    lang[f'item.{NS}.{it["k"]}']=f"{M[k]['name']} Upgrade Smithing Template"
# tier tags: rare ores need previous tier tool
NEED={'aresite_ore':'nullifite','cerulite_ore':'olympium','skarnite_ore':'cerulite','eidolite_ore':'skarnite','solvanite_ore':'eidolite'}
for ore,t in NEED.items(): tag(f'{NS}:needs_{t}_tool',ore)
tag('minecraft:needs_diamond_tool','deepslate_nullifite_ore')
# ---------------- write tags (merge with existing)
for t,vals in TAG.items():
    nsp,path=t.split(':')
    for kind in ('block','item'):
        if kind=='item' and (path.startswith('mineable') or path.startswith('needs') or path in('crops','replaceable_by_trees') or path.startswith('c:')): continue
        is_item_tag=nsp=='c' and path.split('/')[0] in('ingots','nuggets','raw_materials','gems','dusts')
        if is_item_tag and kind=='block': continue
        p=f'out/data/{nsp}/tags/{kind}/{path}.json'
        cur=json.load(open(p))['values'] if os.path.exists(p) else []
        wj(p,{'replace':False,'values':sorted(set(cur+vals))})
json.dump(lang,open(f'{A}/lang/en_us.json','w'),indent=2,ensure_ascii=False)
print('blockstates',len(os.listdir(f'{A}/blockstates')),'lang',len(lang))
