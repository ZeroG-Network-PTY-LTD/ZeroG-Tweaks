"""Targeted 32px crystal artwork generator; no registry, growth or lighting edits.

Use: python crystals_v2.py --code-root PATH
Authored palettes come from data.py. Tinted wasteland clusters remain grayscale.
The historical collection and hash roster are never rewritten.
"""
import argparse
import base64
import hashlib
import io
import json
import random
import math
import re
import uuid
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from data import M, STONES
from tex import stone

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'docs/asset-collection-1.21.1/crystals-amethyst-style-v2'
GRAY = ['#252525', '#555555', '#898989', '#bdbdbd', '#eeeeee', '#ffffff']
CLUSTERS = {
    'cerulite_cluster': (M['cerulite']['pal'], None),
    'brine_crystal': (GRAY, 0x6486B2),
    'frost_crystal': (GRAY, 0xB2C9EB),
    'prism_cluster': (GRAY, 0x9F96DF),
}

def rgba(c):
    return tuple(bytes.fromhex(c.lstrip('#'))) + (255,)

def facet(draw, points, palette):
    """Prismatic shaft with a cap, lit left bevel and darker right face."""
    x, tip, w, bottom = points
    cx = x + w // 2
    shoulder = min(bottom - 2, tip + max(2, w // 2))
    draw.polygon([(cx, tip), (x+w, shoulder), (x+w, bottom-2),
                  (cx, bottom), (x, bottom-2), (x, shoulder)], fill=palette[0])
    draw.polygon([(cx, tip+1), (x+1, shoulder), (cx-1, shoulder+1),
                  (cx-1, bottom-2), (x+1, bottom-3)], fill=palette[3])
    draw.polygon([(cx, tip+1), (x+w-1, shoulder), (cx, shoulder+1)], fill=palette[4])
    draw.polygon([(cx, shoulder+1), (x+w-1, shoulder+1), (x+w-1, bottom-3),
                  (cx, bottom-1)], fill=palette[2])
    draw.line([(x+1, shoulder+1), (x+1, bottom-4)], fill=palette[4])
    draw.line([(cx, shoulder+2), (cx, bottom-3)], fill=palette[1])
    draw.line([(x+2, bottom-5), (max(x+2, cx-1), bottom-3)], fill=palette[2])

def cluster(pal):
    im = Image.new('RGBA', (32,32))
    d = ImageDraw.Draw(im)
    for shape in [(4,11,8,29), (21,9,7,29), (11,2,10,30), (1,19,7,30), (23,18,7,30)]:
        facet(d, shape, pal)
    d.line([(5,30),(25,30)], fill=pal[1])
    result=Image.new('RGBA',(32,32))
    result.alpha_composite(im.resize((32,16),Image.Resampling.NEAREST),(0,16))
    return result

def shard(pal, cut=False):
    im = Image.new('RGBA',(32,32)); d = ImageDraw.Draw(im)
    if not cut:
        facet(d, (8,2,15,29), pal)
        d.line([(13,9),(17,6)], fill=pal[5])
    else:
        d.polygon([(8,5),(23,5),(29,13),(16,29),(2,13)], fill=pal[0])
        d.polygon([(9,6),(15,6),(10,12),(4,12)], fill=pal[4])
        d.polygon([(16,6),(22,6),(27,12),(11,12)], fill=pal[3])
        d.polygon([(4,14),(14,14),(15,26)], fill=pal[3])
        d.polygon([(16,14),(27,14),(17,26)], fill=pal[1])
        d.line([(4,13),(27,13)], fill=pal[4])
        d.line([(16,7),(11,11)], fill=pal[5])
    return im

def crystalline(pal, seed):
    """Seamless, irregular mineral grains; deliberately no tiled diamond grid."""
    rng = random.Random(seed)
    seeds=[(rng.randrange(32),rng.randrange(32),rng.choice([1,2,2,3]),rng.random()) for _ in range(23)]
    im = Image.new('RGBA',(32,32)); px=im.load()
    def blend(a,b,t):
        return tuple(round(a[i]*(1-t)+b[i]*t) for i in range(3))+(255,)
    colours=[rgba(c) for c in pal]
    for y in range(32):
        for x in range(32):
            distances=sorted((min(abs(x-sx),32-abs(x-sx))**2+min(abs(y-sy),32-abs(y-sy))**2,i) for i,(sx,sy,_,_) in enumerate(seeds))
            nearest,second=distances[:2]; sx,sy,tone,phase=seeds[nearest[1]]
            dx=(x-sx+16)%32-16; dy=(y-sy+16)%32-16
            shade=max(0,min(1,.45-(dx+dy)/26))
            colour=blend(colours[tone],colours[min(tone+1,4)],shade*.55)
            # Thin discontinuous seams and local stepped highlights, not white outlines.
            if second[0]-nearest[0]<5 and phase>.38:
                colour=blend(colour,colours[1],.48)
            elif dx+dy<-4 and phase>.7 and nearest[0]<28:
                colour=blend(colour,colours[4],.22)
            if rng.random()<.15: colour=blend(colour,colours[rng.choice([1,2,3])],.14)
            px[x,y]=colour
    d=ImageDraw.Draw(im)
    for _ in range(6):
        x,y=rng.randrange(2,29),rng.randrange(2,29)
        d.line([(x,y),(x+1,y)],fill=blend(px[x,y],colours[4],.35))
    return im

def ore(material, seed):
    p=M[material]['pal']
    im=stone(STONES[M[material]['stone']],seed).resize((32,32),Image.Resampling.NEAREST)
    d=ImageDraw.Draw(im)
    for x,y,w,h in [(3,3,6,7),(20,3,7,6),(12,12,6,7),(3,21,7,6),(23,21,6,8)]:
        facet(d,(x,y,w,y+h),p)
    return im

def glow(im):
    mask=Image.new('RGBA', im.size)
    for y in range(im.height):
        for x in range(im.width):
            c=im.getpixel((x,y))
            if c[3] and min(c[:3])>=175 and max(c[:3])>=235: mask.putpixel((x,y),c)
    return mask

def ingot(pal):
    im=Image.new('RGBA',(32,32)); d=ImageDraw.Draw(im)
    d.polygon([(2,15),(11,8),(26,8),(30,14),(27,22),(6,24),(2,20)],fill=pal[0])
    d.polygon([(4,15),(12,9),(25,9),(28,14),(20,17),(6,17)],fill=pal[3])
    d.polygon([(4,17),(20,19),(26,16),(26,21),(7,22),(4,19)],fill=pal[2])
    d.polygon([(28,15),(27,20),(22,22),(22,19)],fill=pal[1])
    d.line([(6,14),(13,10),(24,10)],fill=pal[4],width=2)
    d.line([(7,18),(19,19)],fill=pal[4])
    for x,y in [(10,12),(11,12),(14,11),(15,11),(21,13),(22,13)]: d.point((x,y),fill=pal[5])
    d.line([(8,21),(15,22)],fill=pal[1])
    return im

def raw_metal(pal,seed):
    im=Image.new('RGBA',(32,32)); d=ImageDraw.Draw(im); rng=random.Random(seed)
    lumps=[[(5,11),(10,6),(18,7),(22,13),(18,21),(8,20),(3,16)],
           [(16,15),(22,10),(28,14),(30,23),(24,28),(16,27),(13,21)],
           [(4,21),(10,18),(15,22),(14,28),(5,29),(2,25)]]
    for poly in lumps:
        d.polygon(poly,fill=pal[0]); cx=sum(p[0] for p in poly)//len(poly); cy=sum(p[1] for p in poly)//len(poly)
        inner=[((x*4+cx)//5,(y*4+cy)//5) for x,y in poly]
        d.polygon(inner,fill=pal[2])
        d.polygon([inner[0],inner[1],inner[2],(cx,cy)],fill=pal[3])
        d.line(inner[:3],fill=pal[4],width=2)
        for _ in range(7):
            x=cx+rng.randrange(-3,4); y=cy+rng.randrange(-2,4)
            if im.getpixel((x,y))[3]: d.rectangle((x,y,x+1,y+1),fill=rng.choice([pal[1],pal[3],pal[4]]))
    return im

def star_glass_frames(colour='purple'):
    frames=[]
    for frame in range(16):
        im=Image.new('RGBA',(64,64)); px=im.load()
        for y in range(64):
            for x in range(64):
                nx=(x-31.5)/28; ny=(y-31.5)/28
                radius=math.hypot(nx,ny); a=math.atan2(ny,nx)+radius*4-frame*math.tau/16
                band=(math.cos(a*2)+1)/2
                intensity=max(0,1-radius)*band
                colours={'purple':(65+105*intensity,30+55*intensity,100+105*intensity),
                         'blue':(30+70*intensity,45+105*intensity,95+95*intensity),
                         'teal':(20+45*intensity,65+115*intensity,80+120*intensity)}
                # Separate brighter spiral projection above the 15%-opaque pane.
                projection=max(0,band-.65)*max(0,1-radius)*2.5
                opacity=min(155,38+int(155*projection))
                px[x,y]=tuple(int(v) for v in colours[colour])+(opacity,)
        d=ImageDraw.Draw(im)
        d.rectangle((0,0,63,63),outline='#666677',width=2)
        d.rectangle((2,2,61,61),outline='#d8d8e2',width=1)
        for x,y in [(3,3),(60,3),(3,60),(60,60)]:
            d.rectangle((x-1,y-1,x+1,y+1),fill='#f8f3ff')
        rng=random.Random(714)
        for i in range(34):
            x,y=rng.randrange(5,59),rng.randrange(5,59)
            lum=int(135+100*(math.sin(frame*math.tau/16+i*1.9)+1)/2)
            d.point((x,y),fill=(lum,lum,255,210))
            if i%9==0:
                d.line([(x-1,y),(x+1,y)],fill=(155,210,255,160))
                d.line([(x,y-1),(x,y+1)],fill=(155,210,255,160))
        # The dark core is a projection in the pane, not a full opaque cube.
        d.ellipse((28,28,35,35),fill=(10,14,35,100),outline=(145,220,255,185))
        frames.append(im)
    return frames

def embedded_project(name, im, kind):
    buffer=io.BytesIO(); im.save(buffer,format='PNG')
    source='data:image/png;base64,'+base64.b64encode(buffer.getvalue()).decode()
    faces=lambda dirs:{v:{'uv':[0,0,32,32],'texture':0} for v in dirs}
    elements=[]
    if kind=='cross':
        for angle in [-45,45]:
            elements.append({'name':'crystal_plane','from':[0,0,8],'to':[16,16,8],
                'origin':[8,8,8], 'rotation':[0,angle,0], 'faces':faces(['north','south'])})
    elif kind=='item':
        elements.append({'name':'inventory_sprite','from':[0,0,8],'to':[16,16,8],
                         'faces':faces(['north','south'])})
    else:
        elements.append({'name':'crystal_block','from':[0,0,0],'to':[16,16,16],
                         'faces':faces(['north','south','east','west','up','down'])})
    for el in elements:
        el['uuid']=str(uuid.uuid5(uuid.NAMESPACE_URL,name+str(len(elements))+str(el)))
    return {'meta':{'format_version':'4.10','model_format':'java_block','box_uv':False},
            'name':name,'resolution':{'width':32,'height':32},'elements':elements,
            'outliner':[el['uuid'] for el in elements], 'textures':[{
                'name':name+'.png','id':'0','uuid':str(uuid.uuid5(uuid.NAMESPACE_URL,name)),
                'source':source,'mode':'bitmap','uv_width':32,'uv_height':32,
                'width':32,'height':32}], 'animations':[]}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--code-root',type=Path,required=True)
    args=parser.parse_args(); code=args.code_root.resolve()
    if not (code/'src/main/resources/assets/zerog_tweaks').is_dir():
        parser.error('Expected a separate existing ZeroG code checkout')
    assets={}; projects={}; resources={}; additions={}
    def add(path,im,kind=None):
        assets[path]=im
        if kind: projects[path.replace('/','_')]=embedded_project(Path(path).stem,im,kind)
    for i,(name,(pal,_)) in enumerate(CLUSTERS.items()):
        add('block/'+name+'.png',cluster(pal),'cross')
    keys=[k for k,v in M.items() if v['role'] in ('crystal','diamond')]
    for i,k in enumerate(keys):
        add('item/'+k+'.png',shard(M[k]['pal'],M[k]['role']=='diamond'),'item')
        add('block/'+k+'_block.png',crystalline(M[k]['pal'],100+i),'cube')
        add('block/'+k+'_ore.png',ore(k,200+i))
        if k=='rimeglass':
            # Glass must retain translucency after replacing its facet artwork.
            glass=assets['block/rimeglass_block.png']
            glass.putalpha(70)
            projects['block_rimeglass_block.png']=embedded_project('rimeglass_block',glass,'cube')
    metals=[k for k,v in M.items() if v['role']=='metal']
    for i,k in enumerate(metals):
        add('item/'+k+'_ingot.png',ingot(M[k]['pal']),'item')
        add('item/raw_'+k+'.png',raw_metal(M[k]['pal'],700+i),'item')
    budding=crystalline(M['cerulite']['pal'],79)
    d=ImageDraw.Draw(budding)
    for x,y in [(6,6),(23,7),(16,24)]:
        d.line([(x-3,y),(x+3,y)],fill=M['cerulite']['pal'][0],width=2)
        d.line([(x,y-3),(x,y+3)],fill=M['cerulite']['pal'][0],width=2)
        d.point((x,y),fill=M['cerulite']['pal'][4])
    add('block/budding_cerulite.png',budding,'cube')
    add('block/cerulean_geode_shell.png',crystalline(['#152738','#233e54','#385b72','#688da3','#b1d8e4','#d4f4ff'],91),'cube')
    for name in ['budding_cerulite','cerulite_cluster']:
        mask=glow(assets['block/'+name+'.png'])
        for suffix in ['_emissive','_glowmask']: add('block/'+name+suffix+'.png',mask)
    family_cluster={'cerulite':'cerulite_cluster','brine':'brine_crystal','frost':'frost_crystal','prism':'prism_cluster'}
    orientations={'up':{},'down':{'x':180},'north':{'x':90},'east':{'x':90,'y':90},'south':{'x':90,'y':180},'west':{'x':90,'y':270}}
    def block_resources(name,tinted=False,cross=False):
        model={'parent':'minecraft:block/'+('tinted_cross' if tinted else 'cross') if cross else 'minecraft:block/cube_all',
               'textures':{('cross' if cross else 'all'):'zerog_tweaks:block/'+name},'render_type':'minecraft:cutout'}
        if tinted and not cross: model['parent']='zerog_tweaks:block/parent/tinted_cube_all'
        resources['assets/zerog_tweaks/models/block/'+name+'.json']=model
        resources['assets/zerog_tweaks/models/item/'+name+'.json']={'parent':'zerog_tweaks:block/'+name}
        resources['assets/zerog_tweaks/blockstates/'+name+'.json']={'variants':{
            'facing='+face:{'model':'zerog_tweaks:block/'+name,**rotation} for face,rotation in orientations.items()
        }} if cross else {'variants':{'':{'model':'zerog_tweaks:block/'+name}}}
        additions['block.zerog_tweaks.'+name]=name.replace('_',' ').title()
    for family, mature in family_cluster.items():
        pal=CLUSTERS[mature][0]; tinted=family!='cerulite'
        for size,scale in [('small',0.4),('medium',0.55),('large',0.7)]:
            name=size+'_'+family+'_bud'; base=cluster(pal)
            sprite=Image.new('RGBA',(32,32)); width=int(32*scale); height=int(32*scale)
            sprite.alpha_composite(base.resize((width,height),Image.Resampling.NEAREST),((32-width)//2,32-height))
            add('block/'+name+'.png',sprite,'cross'); block_resources(name,tinted,True)
            resources['data/zerog_tweaks/loot_table/blocks/'+name+'.json']={'type':'minecraft:block','pools':[
                {'rolls':1,'entries':[{'type':'minecraft:item','name':'zerog_tweaks:'+name}],
                 'conditions':[{'condition':'minecraft:match_tool','predicate':{'predicates':{
                     'minecraft:enchantments':[{'enchantments':'minecraft:silk_touch','levels':{'min':1}}]}}}]}]}
        if tinted:
            name='budding_'+family+'_crystal'; im=crystalline(GRAY,82)
            d=ImageDraw.Draw(im)
            for x,y in [(6,6),(23,7),(16,24)]:
                d.line([(x-3,y),(x+3,y)],fill=GRAY[0],width=2); d.line([(x,y-3),(x,y+3)],fill=GRAY[0],width=2)
            add('block/'+name+'.png',im,'cube'); block_resources(name,True)
            resources['data/zerog_tweaks/loot_table/blocks/'+name+'.json']={'type':'minecraft:block','pools':[]}
            feature='worldgen/configured_feature/'+mature+'_scatter.json'
            feature_path=code/'src/main/resources/data/zerog_tweaks'/feature
            # Replace the old underground cluster ore patches with solid budding roots.
            if feature_path.exists():
                feature_data=json.loads(feature_path.read_text())
                for target in feature_data['config']['targets']: target['state']={'Name':'zerog_tweaks:'+name}
                resources['data/zerog_tweaks/'+feature]=feature_data
    frames=star_glass_frames(); strip=Image.new('RGBA',(64,64*len(frames)))
    for i,im in enumerate(frames): strip.paste(im,(0,64*i))
    add('block/star_glass.png',strip)
    project=embedded_project('star_glass',frames[0],'cube')
    project['resolution']={'width':64,'height':64}
    for el in project['elements']:
        for face in el['faces'].values(): face['uv']=[0,0,64,64]
    project['textures'][0].update({'uv_width':64,'uv_height':64,'width':64,'height':64})
    projects['block_star_glass.png']=project
    block_resources('star_glass')
    resources['assets/zerog_tweaks/models/block/star_glass.json']['render_type']='minecraft:translucent'
    resources['assets/zerog_tweaks/blockstates/star_glass.json']={'variants':{
        'nebula='+colour:{'model':'zerog_tweaks:block/star_glass'+('' if colour=='purple' else '_'+colour)}
        for colour in ['purple','blue','teal']}}
    for colour in ['blue','teal']:
        other=star_glass_frames(colour); other_strip=Image.new('RGBA',(64,64*len(other)))
        for i,im in enumerate(other): other_strip.paste(im,(0,64*i))
        add('block/star_glass_'+colour+'.png',other_strip)
        resources['assets/zerog_tweaks/models/block/star_glass_'+colour+'.json']={
            'parent':'minecraft:block/cube_all','textures':{'all':'zerog_tweaks:block/star_glass_'+colour},'render_type':'minecraft:translucent'}
    additions['block.zerog_tweaks.star_glass']='Star Glass: Block of Cosmic Transparency'
    resources['data/zerog_tweaks/loot_table/blocks/star_glass.json']={'type':'minecraft:block','pools':[
        {'rolls':1,'entries':[{'type':'minecraft:item','name':'zerog_tweaks:star_glass'}],
         'conditions':[{'condition':'minecraft:match_tool','predicate':{'predicates':{
             'minecraft:enchantments':[{'enchantments':'minecraft:silk_touch','levels':{'min':1}}]}}}]}]}
    planets={'moon':['#747584','#b3b4c3','#d4d5df','#f2f3fa'],
             'mars':['#6d352b','#9b503b','#c77655','#eaa278'],
             'cerulon':['#365775','#6599b9','#8ec9e0','#cff4fb'],
             'skarn':['#332b2b','#513e38','#704f46','#aa7560'],
             'eidolon':['#7f9ba9','#aac5d2','#d2e6f0','#f2fcff'],
             'solvane':['#8f512c','#cb8b47','#f5bc70','#ffe9b3']}
    for index,(planet,pal) in enumerate(planets.items()):
        rng=random.Random(831+index); sand=Image.new('RGBA',(32,32)); sp=sand.load()
        for y in range(32):
            for x in range(32):
                r=rng.random(); sp[x,y]=rgba(pal[1] if r<.22 else pal[3] if r>.93 else pal[2])
        name=planet+'_star_sand'; add('block/'+name+'.png',sand,'cube'); block_resources(name)
        additions['block.zerog_tweaks.'+name]=planet.title()+' Star Sand'
        resources['data/zerog_tweaks/recipe/'+name+'_to_star_glass.json']={
            'type':'minecraft:smelting','category':'blocks','ingredient':{'item':'zerog_tweaks:'+name},
            'result':{'id':'zerog_tweaks:star_glass','count':1},'experience':0.1,'cookingtime':200}
        resources['data/zerog_tweaks/loot_table/blocks/'+name+'.json']={'type':'minecraft:block','pools':[
            {'rolls':1,'entries':[{'type':'minecraft:item','name':'zerog_tweaks:'+name}],
             'conditions':[{'condition':'minecraft:survives_explosion'}]}]}
    records=[]
    texroot=code/'src/main/resources/assets/zerog_tweaks/textures'
    for path,im in assets.items():
        target=texroot/path
        old=target.read_bytes() if target.is_file() else None
        dst=OUT/'textures'/path; dst.parent.mkdir(parents=True,exist_ok=True)
        backup=OUT/'before'/path; backup.parent.mkdir(parents=True,exist_ok=True)
        if old is not None and not backup.exists(): backup.write_bytes(old)
        im.save(dst); target.write_bytes(dst.read_bytes())
        records.append({'path':path,'size':list(im.size),'before_sha256':hashlib.sha256(backup.read_bytes()).hexdigest() if backup.exists() else None,
                        'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
    metadata={'animation':{'width':64,'height':64,'frametime':3,'interpolate':True}}
    for colour in ['purple','blue','teal']:
        name='star_glass'+('' if colour=='purple' else '_'+colour)+'.png.mcmeta'
        for target in [texroot/'block'/name,OUT/'textures/block'/name]:
            target.write_text(json.dumps(metadata,indent=2)+'\n')
    for name,j in resources.items():
        for target in [code/'src/main/resources'/name, OUT/'resource-source'/name]:
            target.parent.mkdir(parents=True,exist_ok=True); target.write_text(json.dumps(j,indent=2)+'\n')
    language=code/'src/main/resources/assets/zerog_tweaks/lang/en_us.json'
    lang=json.loads(language.read_text()); lang.update(additions)
    language.write_text(json.dumps(lang,ensure_ascii=False,indent=2)+'\n')
    (OUT/'lang-additions.json').write_text(json.dumps(additions,indent=2)+'\n')
    # Targeted append preserves every unrelated upstream creative-tab entry.
    tabs=code/'src/main/java/net/zerog/tweaks/registry/ZGCreativeTabContents.java'
    tab_text=tabs.read_text()
    natural=[size+'_'+family+'_bud' for family in family_cluster for size in ['small','medium','large']]
    natural += ['budding_'+family+'_crystal' for family in ['brine','frost','prism']]
    natural += [planet+'_star_sand' for planet in planets]
    for category,ids in [('NATURAL_BLOCKS',natural),('BUILDING_BLOCKS',['star_glass'])]:
        pattern=r'(public static final String\[\] '+category+r' = \{)(.*?)(\n    \};)'
        def append_entries(match):
            body=match.group(2); existing=set(re.findall(r'"([a-z0-9_]+)"',body))
            extra=[id for id in ids if id not in existing]
            if not extra:return match.group(0)
            return match.group(1)+body.rstrip()+',\n            '+', '.join(json.dumps(id) for id in extra)+match.group(3)
        tab_text=re.sub(pattern,append_entries,tab_text,flags=re.S)
    tabs.write_text(tab_text)
    # Vanilla sand glass-tool tags for the added planet sands.
    resources_tags={'data/minecraft/tags/block/mineable/shovel.json':["zerog_tweaks:"+p+"_star_sand" for p in planets],
                    'data/minecraft/tags/block/sand.json':["zerog_tweaks:"+p+"_star_sand" for p in planets],
                    'data/minecraft/tags/item/sand.json':["zerog_tweaks:"+p+"_star_sand" for p in planets]}
    for name,ids in resources_tags.items():
        target=code/'src/main/resources'/name
        obj=json.loads(target.read_text()) if target.exists() else {'replace':False,'values':[]}
        obj['values'] += [id for id in ids if id not in obj['values']]
        target.parent.mkdir(parents=True,exist_ok=True); target.write_text(json.dumps(obj,indent=2)+'\n')
    for name,project in projects.items():
        path=OUT/'blockbench'/(name.removesuffix('.png')+'.bbmodel')
        path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(project,indent=2)+'\n')
    tiles=[(p,im if not p.startswith('block/star_glass') else im.crop((0,0,64,64))) for p,im in assets.items() if not any(s in p for s in ['_glowmask','_emissive'])]
    sheet=Image.new('RGB',(1000,80+((len(tiles)+4)//5)*185),'#171d28'); draw=ImageDraw.Draw(sheet)
    draw.text((20,18),'ZeroG crystals v2 - 32px authored facets / existing material palettes',fill='white')
    draw.text((20,42),'Art only. Wasteland cluster previews use Galaxy 2 tint; runtime PNGs stay grayscale.',fill='#aebacf')
    for i,(name,im) in enumerate(tiles):
        x=20+(i%5)*195; y=80+(i//5)*185
        display=im.copy(); cluster_id=Path(name).stem
        if cluster_id in CLUSTERS and CLUSTERS[cluster_id][1]:
            tint=CLUSTERS[cluster_id][1]; rgb=[tint>>16,(tint>>8)&255,tint&255]
            for yy in range(display.height):
                for xx in range(display.width):
                    c=display.getpixel((xx,yy))
                    display.putpixel((xx,yy),tuple(c[j]*rgb[j]//255 for j in range(3))+(c[3],))
        sheet.paste(display.resize((128,128),Image.Resampling.NEAREST),(x+20,y),
                    display.resize((128,128),Image.Resampling.NEAREST))
        draw.text((x,y+134),Path(name).stem,fill='white')
    sheet.save(OUT/'crystals_v2_preview.png')
    # Smaller review sheets keep individual material pairs legible.
    metal_sheet=Image.new('RGBA',(1000,90+len(metals)*105),'#171d28'); md=ImageDraw.Draw(metal_sheet)
    md.text((20,20),'ZeroG: modern vanilla-style ingots and raw metals - all 16 families',fill='white')
    md.text((260,52),'INGOT',fill='#a6bed5'); md.text((450,52),'RAW MATERIAL',fill='#a6bed5')
    for i,k in enumerate(metals):
        y=90+i*105; md.text((20,y+35),M[k]['name'],fill='white')
        for x,path in [(260,'item/'+k+'_ingot.png'),(450,'item/raw_'+k+'.png')]:
            metal_sheet.alpha_composite(assets[path].resize((96,96),Image.Resampling.NEAREST),(x,y))
        md.text((620,y+35),'Vanilla generated item / held & dropped sprite',fill='#a3b2c9')
    metal_sheet.convert('RGB').save(OUT/'ingots_raw_reference.png')
    sand_sheet=Image.new('RGBA',(900,480),'#171d28'); sd=ImageDraw.Draw(sand_sheet)
    sd.text((20,20),'Six planet Star Sands -> furnace (200 ticks) -> Star Glass',fill='white')
    for i,planet in enumerate(planets):
        x=25+(i%3)*295; y=65+(i//3)*200
        sand_sheet.alpha_composite(assets['block/'+planet+'_star_sand.png'].resize((128,128),Image.Resampling.NEAREST),(x,y))
        sd.text((x,y+138),planet.title()+' Star Sand',fill='white')
    sand_sheet.convert('RGB').save(OUT/'planet_sands_reference.png')
    gallery_frames=[]
    for index,frame in enumerate(frames):
        card=Image.new('RGBA',(720,350),'#141c2b'); dc=ImageDraw.Draw(card)
        dc.text((20,15),'Star Glass - quartz frame, translucent nebula, 3-tick glisten',fill='white')
        for x in range(32,305,16):
            for y in range(55,320,16):
                dc.rectangle((x,y,x+15,y+15),fill='#304153' if (x//16+y//16)%2 else '#172737')
        card.alpha_composite(frame.resize((256,256),Image.Resampling.NEAREST),(40,60))
        dc.text((355,50),'Crystal growth stages (reference)',fill='white')
        for i,(size,scale) in enumerate([('small',0.4),('medium',0.55),('large',0.7),('cluster',1.0)]):
            sprite=assets['block/'+(size+'_cerulite_bud' if i<3 else 'cerulite_cluster')+'.png']
            card.alpha_composite(sprite.resize((72,72),Image.Resampling.NEAREST),(350+i*87,85))
            dc.text((350+i*87,168),size,fill='white')
        dc.text((355,190),'Light: 1 -> 2 -> 4 -> 5 / Glass: 12',fill='#9eddf4')
        dc.text((355,208),'Pane opacity: 15% / animation: 3 ticks',fill='#b8c9dc')
        width=max(2,int(abs(math.cos(index*math.tau/16))*72))
        sprite=assets['item/moonsteel_ingot.png'].resize((width,64),Image.Resampling.NEAREST)
        if math.cos(index*math.tau/16)<0:sprite=sprite.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        card.alpha_composite(sprite,(370+(72-width)//2,230))
        card.alpha_composite(assets['item/raw_moonsteel.png'].resize((64,64),Image.Resampling.NEAREST),(475,230))
        dc.text((355,305),'Offline asset reference, not an in-game capture',fill='#a0b0c4')
        gallery_frames.append(card.convert('RGB'))
    gallery_frames[0].save(OUT/'animated_updates.gif',save_all=True,append_images=gallery_frames[1:],duration=150,loop=0)
    gallery_frames[0].save(OUT/'star_glass_reference.png')
    manifest={'schema':1,'generator':'crystals_v2.py','texture_count':len(records),
              'editable_projects':len(projects),'materials':keys,'metal_families':metals,'textures':records,
              'lighting_changed':True,'growth_changed':True,'game_import_verified':False}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k!='textures'},indent=2))

if __name__=='__main__': main()
