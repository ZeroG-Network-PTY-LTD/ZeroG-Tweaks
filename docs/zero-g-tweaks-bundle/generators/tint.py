import os, json
from PIL import Image
NS='zerog_tweaks'; A=f'out/assets/{NS}'; MB=f'{A}/models/block'
def wj(p,o): os.makedirs(os.path.dirname(p),exist_ok=True); json.dump(o,open(p,'w'),indent=2)
F6=('down','up','north','south','west','east')
def face(tex,cull=None):
    f={'texture':tex,'tintindex':0}
    if cull: f['cullface']=cull
    return f
def box(fr,to,tex,cull_all=False):
    faces={}
    for d in F6:
        t=tex[d] if isinstance(tex,dict) else tex
        edge={'down':fr[1]==0,'up':to[1]==16,'north':fr[2]==0,'south':to[2]==16,'west':fr[0]==0,'east':to[0]==16}[d]
        faces[d]=face(t,d if edge else None)
    return {'from':fr,'to':to,'faces':faces}
# tinted parent models (inherit display transforms from the vanilla parent; elements override)
P={}
P['tinted_cube_all']=('minecraft:block/cube_all',[box([0,0,0],[16,16,16],'#all')])
P['tinted_cube_bottom_top']=('minecraft:block/cube_bottom_top',[box([0,0,0],[16,16,16],{'down':'#bottom','up':'#top','north':'#side','south':'#side','west':'#side','east':'#side'})])
sl={'down':'#bottom','up':'#top','north':'#side','south':'#side','west':'#side','east':'#side'}
P['tinted_slab']=('minecraft:block/slab',[box([0,0,0],[16,8,16],sl)])
P['tinted_slab_top']=('minecraft:block/slab_top',[box([0,8,0],[16,16,16],sl)])
P['tinted_stairs']=('minecraft:block/stairs',[box([0,0,0],[16,8,16],sl),box([8,8,0],[16,16,16],sl)])
P['tinted_inner_stairs']=('minecraft:block/inner_stairs',[box([0,0,0],[16,8,16],sl),box([8,8,0],[16,16,16],sl),box([0,8,8],[8,16,16],sl)])
P['tinted_outer_stairs']=('minecraft:block/outer_stairs',[box([0,0,0],[16,8,16],sl),box([8,8,8],[16,16,16],sl)])
P['tinted_wall_post']=('minecraft:block/template_wall_post',[box([4,0,4],[12,16,12],'#wall')])
P['tinted_wall_side']=('minecraft:block/template_wall_side',[box([5,0,0],[11,14,8],'#wall')])
P['tinted_wall_side_tall']=('minecraft:block/template_wall_side_tall',[box([5,0,0],[11,16,8],'#wall')])
P['tinted_wall_inventory']=('minecraft:block/wall_inventory',[box([4,0,4],[12,16,12],'#wall'),box([5,0,0],[11,13,16],'#wall')])
for n in range(1,8): P[f'tinted_snow_height{2*n}']=(f'minecraft:block/snow_height{2*n}',[box([0,0,0],[16,2*n,16],'#texture')])
for k,(par,els) in P.items():
    for e in els:
        for f in e['faces'].values():
            if f.get('cullface')=='up' and k.startswith('tinted_snow'): f.pop('cullface')
    wj(f'{MB}/parent/{k}.json',{'parent':par,'elements':els})
MAP={'minecraft:block/cube_all':'tinted_cube_all','minecraft:block/cube_bottom_top':'tinted_cube_bottom_top','minecraft:block/slab':'tinted_slab','minecraft:block/slab_top':'tinted_slab_top',
'minecraft:block/stairs':'tinted_stairs','minecraft:block/inner_stairs':'tinted_inner_stairs','minecraft:block/outer_stairs':'tinted_outer_stairs',
'minecraft:block/template_wall_post':'tinted_wall_post','minecraft:block/template_wall_side':'tinted_wall_side','minecraft:block/template_wall_side_tall':'tinted_wall_side_tall',
'minecraft:block/wall_inventory':'tinted_wall_inventory','minecraft:block/cross':'minecraft:block/tinted_cross','minecraft:block/cube_column':'tinted_cube_bottom_top'}
for n in range(1,8): MAP[f'minecraft:block/snow_height{2*n}']=f'tinted_snow_height{2*n}'
# which blocks are wasteland (grayscale)
TYPE={}
STONES={'abyssal_stone':'ocean','sunbaked_stone':'desert','scoria':'volcanic','frostrock':'frozen','sludgestone':'toxic','prismstone':'crystal','craterstone':'barren'}
TERRAIN={'tidesand':'ocean','brine_crystal':'ocean','glowkelp':'ocean','dunesand':'desert','salt_crust':'desert','ruinstone':'desert','ashfall':'volcanic','vent_rock':'volcanic',
'glassy_obsidian':'volcanic','snowpack':'frozen','glacial_ice':'frozen','frost_crystal':'frozen','toxic_mud':'toxic','blightmoss':'toxic','prism_cluster':'crystal','shimmer_sand':'crystal',
'refracting_glass':'crystal','crater_dust':'barren','meteorite_fragment':'barren','tide_glass':'ocean','dune_glass':'desert','shimmer_glass':'crystal'}
bs_dir=f'{A}/blockstates'
for f in os.listdir(bs_dir):
    b=f[:-5]
    for s,t in STONES.items():
        if s in b: TYPE[b]=t
    for s,t in TERRAIN.items():
        if b==s or b.startswith(s+'_'): TYPE[b]=t
    if b.startswith('ruinstone_') or b.startswith('salt_crust_'): TYPE[b]='desert'
changed=0
for b in TYPE:
    s=open(f'{bs_dir}/{b}.json').read()
    import re
    for m in set(re.findall(r'zerog_tweaks:block/([a-z0-9_]+)',s)):
        p=f'{MB}/{m}.json'
        if not os.path.exists(p): continue
        j=json.load(open(p)); par=j.get('parent')
        if par in MAP:
            np=MAP[par]; j['parent']=np if np.startswith('minecraft:') else f'{NS}:block/parent/{np}'; wj(p,j); changed+=1
json.dump(TYPE,open('tint_types.json','w'),indent=1)
print(len(TYPE),'blocks tinted,',changed,'models')
