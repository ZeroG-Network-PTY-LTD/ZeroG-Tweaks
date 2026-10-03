"""Local 32px dimension soils/grass, farmland, sands, plants and animated fluids.

Generates resources only. Actual block/fluid/entity logic lives on 1.21.x.
Existing IDs and terrain settings are preserved. Run with --code-root PATH.
"""
import argparse, base64, colorsys, hashlib, io, json, math, random, re, uuid
from pathlib import Path
from PIL import Image, ImageDraw
from crystals_v2 import embedded_project

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'docs/asset-collection-1.21.1/dimension-ecology-v1'
PALETTES = {
    'moon': (139, 131, 153), 'mars': (164, 86, 57), 'cerulon': (66, 114, 153),
    'skarn': (91, 61, 48), 'eidolon': (117, 155, 172), 'solvane': (184, 119, 48),
    'ocean': (79, 113, 141), 'desert': (174, 143, 91), 'volcanic': (100, 65, 59),
    'frozen': (138, 173, 186), 'toxic': (94, 119, 51), 'crystal': (137, 100, 170), 'barren': (125, 119, 132),
}
FLUIDS = {
    'acid': (['3a5a10','6a9a18','8ac040','c8ff60'], 220, 4, 'toxic'),
    'magma_slag': (['2a0a04','6a1a06','b8400c','f08020'], 255, 12, 'volcanic'),
    'cryo_fluid': (['3a7a96','6ab4d0','a8e0f0','e8fbff'], 200, 2, 'frozen'),
    'solar_plasma': (['c43a06','f07a14','ffc040','fff6c8'], 255, 15, 'solvane'),
    'null_fluid': (['06040c','140c24','2a1a48','5a3a90'], 230, 6, 'barren'),
}

def adjust(c, value): return tuple(max(0, min(255, round(v * value))) for v in c)
def soil(colour, seed):
    rng = random.Random(seed); image = Image.new('RGBA', (32,32)); draw = ImageDraw.Draw(image)
    for y in range(32):
        for x in range(32): image.putpixel((x,y), adjust(colour, rng.choice([.65,.78,.9,1,1.12,1.25])) + (255,))
    for i in range(30):
        x, y = rng.randrange(31), rng.randrange(31)
        draw.rectangle((x,y,x+1,y+1), fill=adjust(colour,.65)+(255,))
        draw.point((x,y), fill=adjust(colour,1.25)+(255,))
    return image
def farm(image, wet):
    im = image.copy(); draw = ImageDraw.Draw(im)
    for x in range(1,32,4):
        draw.line((x,0,x,31), fill=(20,24,35,255) if wet else (50,42,50,255))
        draw.line((x+1,0,x+1,31), fill=(70,80,99,255) if wet else im.getpixel((x+1,0)))
    if wet:
        im = im.point(lambda v: v) # keep alpha; darken soil outside furrows independently
        for y in range(32):
            for x in range(32):
                r,g,b,a = im.getpixel((x,y)); im.putpixel((x,y),(int(r*.65),int(g*.65),int(b*.75),a))
    return im
def grass_colour(base):
    h,s,v = colorsys.rgb_to_hsv(*(x/255 for x in base)); h=(h+.13)%1
    return tuple(round(x*255) for x in colorsys.hsv_to_rgb(h,max(.35,s), min(.8,v+.15)))
def plant(base, seed, kind):
    rng=random.Random(seed); im=Image.new('RGBA',(32,32)); d=ImageDraw.Draw(im)
    leaf=grass_colour(base); stem=adjust(leaf,.7)+(255,); bright=adjust(base,1.6)+(255,)
    if kind=='glow_mushroom':
        d.rectangle((14,14,17,29),fill=adjust(base,1.2)+(255,))
        d.polygon([(4,15),(8,8),(12,5),(20,5),(25,9),(29,15)],fill=adjust(base,.8)+(255,))
        d.line((4,16,29,16),fill=bright,width=2)
        for x,y in [(11,9),(17,8),(23,12),(8,13)]: d.rectangle((x,y,x+2,y+1),fill=bright)
    elif kind=='glow_flower':
        d.line((16,28,16,11),fill=stem,width=2)
        d.polygon([(16,20),(7,15),(9,23)],fill=leaf+(255,))
        d.polygon([(16,17),(26,13),(24,21)],fill=leaf+(255,))
        for x,y in [(9,7),(15,4),(21,7),(12,12),(19,12)]: d.rectangle((x,y,x+4,y+4),fill=bright)
        d.rectangle((15,8,19,12),fill=(255,244,182,255))
    else:
        for n in range(11 if kind=='glow_shrub' else 7):
            x=rng.randrange(5,27); top=rng.randrange(3,20)
            d.line((16,31,x,top),fill=stem,width=2)
            d.line((16,30,x+2,max(1,top-3)),fill=leaf+(255,))
            if kind=='glow_shrub': d.rectangle((x,top,x+1,top+2),fill=bright)
    return im
def fluid_frame(key, size, tick, flowing):
    pal, alpha, _, _ = FLUIDS[key]; pal=[tuple(bytes.fromhex(x)) for x in pal]
    im=Image.new('RGBA',(size,size)); phase=2*math.pi*tick/16
    for y in range(size):
        for x in range(size):
            u=2*math.pi*x/size; v=2*math.pi*y/size + (phase if flowing else 0)
            wave=(math.sin(u*3+phase)+math.sin(v*2-phase)+.7*math.sin((u+v)*2+phase))/5.4+.5
            index=max(0,min(3,int(wave*4))); colour=pal[index]
            if key=='magma_slag' and wave < .35: colour=pal[0]
            im.putpixel((x,y),colour+(alpha,))
    d=ImageDraw.Draw(im); rng=random.Random(len(key)*17)
    for n in range(size//4):
        x,y=rng.randrange(size),rng.randrange(size)
        if (tick+n)%4 < 2: d.point((x,(y+tick*(2 if flowing else 0))%size),fill=pal[-1]+(255,))
    return im
def bucket(base):
    im=Image.new('RGBA',(32,32)); d=ImageDraw.Draw(im)
    d.polygon([(5,8),(27,8),(25,24),(21,29),(11,29),(7,24)],fill=(39,44,56,255))
    d.polygon([(7,11),(25,11),(23,23),(20,26),(12,26),(9,23)],fill=(151,164,180,255))
    d.polygon([(6,9),(12,5),(22,5),(28,9),(23,13),(11,13)],fill=adjust(base,1.1)+(255,))
    d.line([(6,9),(12,5),(22,5),(28,9)],fill=(226,233,246,255),width=2)
    d.line((9,15,11,23),fill=(228,235,245,255),width=2)
    return im

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--code-root',type=Path,required=True); args=parser.parse_args()
    code=args.code_root.resolve(); res=code/'src/main/resources'; asset=res/'assets/zerog_tweaks'; data=res/'data/zerog_tweaks'
    lore=json.loads((ROOT/'docs/zero-g-tweaks-bundle/data-manifest.json').read_text())
    dimensions=sorted(path.stem for path in (data/'dimension').glob('*.json'))
    records=[]; projects=[]; images={}; naturals=[]
    def write(path,obj): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,indent=2)+'\n')
    def resource(relative,obj):
        write(res/relative,obj); write(OUT/'resource-source'/relative,obj)
    def texture(path,im):
        dst=asset/'textures'/path; preview=OUT/'textures'/path; preview.parent.mkdir(parents=True,exist_ok=True)
        if dst.exists() and not (OUT/'before'/path).exists():
            old=OUT/'before'/path; old.parent.mkdir(parents=True,exist_ok=True); old.write_bytes(dst.read_bytes())
        dst.parent.mkdir(parents=True,exist_ok=True); im.save(dst); preview.write_bytes(dst.read_bytes())
        images[path]=im; records.append({'path':path,'size':list(im.size),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
    def model(name,model,states=None,item=True):
        resource(f'assets/zerog_tweaks/models/block/{name}.json',model)
        resource(f'assets/zerog_tweaks/blockstates/{name}.json',states or {'variants':{'':{'model':'zerog_tweaks:block/'+name}}})
        if item: resource(f'assets/zerog_tweaks/models/item/{name}.json',{'parent':'zerog_tweaks:block/'+name})
    def loot(name,drop=None,plant_type=None):
        entry={'type':'minecraft:item','name':'zerog_tweaks:'+(drop or name)}
        conditions=[]
        if plant_type:
            if plant_type=='tall': conditions.append({'condition':'minecraft:block_state_property','block':'zerog_tweaks:'+name,'properties':{'half':'lower'}})
            # Shears/Silk Touch returns the plant; otherwise vanilla wheat-seed chance.
            entry={'type':'minecraft:alternatives','children':[
                {'type':'minecraft:item','name':'zerog_tweaks:'+name,'conditions':[{'condition':'minecraft:any_of','terms':[
                    {'condition':'minecraft:match_tool','predicate':{'items':'minecraft:shears'}},
                    {'condition':'minecraft:match_tool','predicate':{'predicates':{'minecraft:enchantments':[{'enchantments':'minecraft:silk_touch','levels':{'min':1}}]}}}]}]},
                {'type':'minecraft:item','name':'minecraft:wheat_seeds','conditions':[{'condition':'minecraft:random_chance','chance':.125}]}]}
        resource(f'data/zerog_tweaks/loot_table/blocks/{name}.json',{'type':'minecraft:block','pools':[{'rolls':1,'conditions':conditions+[{'condition':'minecraft:survives_explosion'}],'entries':[entry]}]})
    def project(name,im,kind='cube',top=None):
        project=embedded_project(name,im,kind)
        if top is not None:
            other=embedded_project(name+'_top',top,'cube')['textures'][0]; other['id']='1'; project['textures'].append(other)
            project['elements'][0]['faces']['up']['texture']=1
        if name.endswith('_farmland'): project['elements'][0]['to'][1]=15
        write(OUT/'blockbench'/f'{name}.bbmodel',project); projects.append(name)
    for index,dim in enumerate(dimensions):
        kind=lore['galaxy_slots_default_type'].get(dim,dim); base=PALETTES[kind]
        if dim.startswith('g'):
            shift=(int(dim[1])-2)*.05; h,s,v=colorsys.rgb_to_hsv(*(x/255 for x in base))
            base=tuple(round(x*255) for x in colorsys.hsv_to_rgb((h+shift)%1,s,v))
        earth=soil(base,811+index); dry=farm(earth,False); wet=farm(earth,True); grass=soil(grass_colour(base),1011+index)
        side=earth.copy(); side.paste(grass.crop((0,0,32,7)),(0,0))
        for suffix,im in [('soil',earth),('farmland_dry',dry),('farmland_wet',wet),('grass_top',grass),('grass_side',side)]: texture('block/'+dim+'_'+suffix+'.png',im)
        soil_id=dim+'_soil'; farm_id=dim+'_farmland'; grass_id=dim+'_grass_block'
        model(soil_id,{'parent':'minecraft:block/cube_all','textures':{'all':'zerog_tweaks:block/'+soil_id}})
        loot(soil_id); project(soil_id,earth)
        for stage,top in [('dry',dry),('wet',wet)]:
            resource(f'assets/zerog_tweaks/models/block/{farm_id}_{stage}.json',{'parent':'minecraft:block/template_farmland','textures':{'dirt':'zerog_tweaks:block/'+soil_id,'top':'zerog_tweaks:block/'+dim+'_farmland_'+stage}})
        resource(f'assets/zerog_tweaks/blockstates/{farm_id}.json',{'variants':{'moisture='+str(n):{'model':'zerog_tweaks:block/'+farm_id+('_wet' if n==7 else '_dry')} for n in range(8)}})
        resource(f'assets/zerog_tweaks/models/item/{farm_id}.json',{'parent':'zerog_tweaks:block/'+farm_id+'_dry'}); loot(farm_id,soil_id); project(farm_id,earth,top=dry)
        model(grass_id,{'parent':'minecraft:block/cube_bottom_top','textures':{'bottom':'zerog_tweaks:block/'+soil_id,'top':'zerog_tweaks:block/'+dim+'_grass_top','side':'zerog_tweaks:block/'+dim+'_grass_side'}},
              {'variants':{'snowy=false':{'model':'zerog_tweaks:block/'+grass_id},'snowy=true':{'model':'zerog_tweaks:block/'+grass_id+'_snow'}}})
        resource(f'assets/zerog_tweaks/models/block/{grass_id}_snow.json',{'parent':'minecraft:block/cube_bottom_top','textures':{'bottom':'zerog_tweaks:block/'+soil_id,'top':'minecraft:block/snow','side':'minecraft:block/grass_block_snow'}})
        resource(f'data/zerog_tweaks/loot_table/blocks/{grass_id}.json',{'type':'minecraft:block','pools':[{'rolls':1,'conditions':[{'condition':'minecraft:survives_explosion'}],
            'entries':[{'type':'minecraft:alternatives','children':[
                {'type':'minecraft:item','name':'zerog_tweaks:'+grass_id,'conditions':[{'condition':'minecraft:match_tool','predicate':{'predicates':{'minecraft:enchantments':[{'enchantments':'minecraft:silk_touch','levels':{'min':1}}]}}}]},
                {'type':'minecraft:item','name':'zerog_tweaks:'+soil_id}]}]}]});project(grass_id,side,top=grass)
        for plant_kind in ['short','tall']:
            name=dim+'_'+plant_kind+'_grass'; im=plant(base,1500+index,'grass'); texture('block/'+name+'.png',im)
            if plant_kind=='short': model(name,{'parent':'minecraft:block/cross','textures':{'cross':'zerog_tweaks:block/'+name},'render_type':'minecraft:cutout'})
            else:
                upper=im.copy(); upper.paste((0,0,0,0),(0,24,32,32)); texture('block/'+name+'_top.png',upper)
                model(name,{'parent':'minecraft:block/cross','textures':{'cross':'zerog_tweaks:block/'+name},'render_type':'minecraft:cutout'},
                      {'variants':{'half=lower':{'model':'zerog_tweaks:block/'+name},'half=upper':{'model':'zerog_tweaks:block/'+name+'_top'}}})
                resource(f'assets/zerog_tweaks/models/block/{name}_top.json',{'parent':'minecraft:block/cross','textures':{'cross':'zerog_tweaks:block/'+name+'_top'},'render_type':'minecraft:cutout'})
            loot(name,plant_type=plant_kind); project(name,im,'cross'); naturals.append(name)
        naturals += [soil_id,farm_id,grass_id]
        if dim.startswith('g'):
            sand_id=dim+'_star_sand'; sand=soil(adjust(base,1.4),2400+index); texture('block/'+sand_id+'.png',sand)
            model(sand_id,{'parent':'minecraft:block/cube_all','textures':{'all':'zerog_tweaks:block/'+sand_id}}); loot(sand_id); project(sand_id,sand); naturals.append(sand_id)
            resource(f'data/zerog_tweaks/recipe/{sand_id}_to_star_glass.json',{'type':'minecraft:smelting','category':'blocks','ingredient':{'item':'zerog_tweaks:'+sand_id},'result':{'id':'zerog_tweaks:star_glass','count':1},'experience':.1,'cookingtime':200})
    for index,planet in enumerate(['moon','mars','cerulon','skarn','eidolon','solvane']):
        vent_name=planet+'_gas_vent'; vent=soil(adjust(PALETTES[planet],.7),4000+index); d=ImageDraw.Draw(vent)
        d.polygon([(8,6),(22,6),(27,15),(23,24),(8,25),(4,15)],fill=(20,19,27,255));d.line([(8,6),(22,6),(27,15)],fill=adjust(PALETTES[planet],1.6)+(255,),width=2)
        texture('block/'+vent_name+'.png',vent);model(vent_name,{'parent':'minecraft:block/cube_all','textures':{'all':'zerog_tweaks:block/'+vent_name}});loot(vent_name);project(vent_name,vent);naturals.append(vent_name)
        resource('assets/zerog_tweaks/particles/'+planet+'_gas_smoke.json',{'textures':['minecraft:big_smoke_'+str(i) for i in range(12)]})
        # Original painting on vanilla Java BeeModel UV layout (64px); no Mojang texture bytes copied.
        skin=Image.new('RGBA',(64,64)); draw=ImageDraw.Draw(skin); base=grass_colour(PALETTES[planet])
        for y in range(17):
            for x in range(34): skin.putpixel((x,y),adjust(base,.6+.045*y if (x//3)%2 else 1.05)+(255,))
        draw.rectangle((10,10,16,16),fill=adjust(base,.8)+(255,))
        for x in [11,15]:
            draw.rectangle((x,11,x+1,13),fill=(16,17,31,255));draw.point((x,11),fill=(224,250,255,255))
        draw.line((13,15,14,15),fill=(20,20,32,255))
        draw.rectangle((6,18,23,23),fill=(164,224,245,130));draw.line((6,18,23,18),fill=(208,242,255,230))
        for y in [1,3,5]:
            for x in [26,29,32]: draw.rectangle((x,y,x,y+1),fill=(38,30,47,255))
        mask=Image.new('RGBA',(64,64));md=ImageDraw.Draw(mask)
        for x in [11,15]:md.point((x,11),fill=(224,250,255,255))
        md.line((6,18,23,18),fill=adjust(base,1.7)+(255,))
        texture('entity/'+planet+'_glowbug.png',skin);texture('entity/'+planet+'_glowbug_glowmask.png',mask)
        blink=skin.copy();bd=ImageDraw.Draw(blink)
        for x in [11,15]:bd.rectangle((x,11,x+1,13),fill=adjust(base,.8)+(255,));bd.line((x,13,x+1,13),fill=(16,17,31,255))
        texture('entity/'+planet+'_glowbug_blink.png',blink)
        # Editable rig study matching the vanilla body's UV rectangles and bilateral wing pivots.
        body_id=str(uuid.uuid5(uuid.NAMESPACE_URL,planet+'bugbody'));left_id=str(uuid.uuid5(uuid.NAMESPACE_URL,planet+'bugleft'));right_id=str(uuid.uuid5(uuid.NAMESPACE_URL,planet+'bugright'))
        cubes=[]
        def cube(label,start,end,uvs):
            identity=str(uuid.uuid5(uuid.NAMESPACE_URL,planet+label));cubes.append({'name':label,'uuid':identity,'from':start,'to':end,
                'faces':{face:{'uv':uv,'texture':0} for face,uv in uvs.items()}});return identity
        body=cube('body',[-3.5,0,-5],[3.5,7,5],{'north':[10,10,17,17],'south':[27,10,34,17],'east':[0,10,10,17],'west':[17,10,27,17],'up':[10,0,17,10],'down':[17,0,24,10]})
        left=cube('left_wing',[1.5,7,-3],[10.5,7,3],{'up':[6,18,15,24],'down':[15,18,24,24]})
        right=cube('right_wing',[-10.5,7,-3],[-1.5,7,3],{'up':[15,18,6,24],'down':[24,18,15,24]})
        details=[]
        for label,x,oy in [('left_antenna',1.5,0),('right_antenna',-2.5,3)]:
            details.append(cube(label,[x,3,-8],[x+1,5,-5],{'east':[2,oy+3,5,oy+5],'north':[5,oy+3,6,oy+5],'west':[6,oy+3,9,oy+5],
                'south':[9,oy+3,10,oy+5],'up':[5,oy,6,oy+3],'down':[6,oy,7,oy+3]}))
        details.append(cube('stinger',[0,3,5],[0,4,7],{'east':[26,9,28,10],'west':[28,9,30,10]}))
        for label,z,oy in [('front_legs',-2,1),('middle_legs',0,3),('back_legs',2,5)]:
            details.append(cube(label,[-3.5,-2,z],[3.5,0,z],{'north':[26,oy,33,oy+2],'south':[33,oy,26,oy+2]}))
        buf=io.BytesIO();skin.save(buf,format='PNG');source='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
        rig={'meta':{'format_version':'4.10','model_format':'bedrock','box_uv':False},'name':planet+'_glowbug','model_identifier':'geometry.'+planet+'_glowbug',
            'resolution':{'width':64,'height':64},'elements':cubes,'textures':[{'name':planet+'_glowbug.png','id':'0','uuid':body_id,'mode':'bitmap','source':source,'width':64,'height':64,'uv_width':64,'uv_height':64}],
            'outliner':[{'name':'body','uuid':body_id,'origin':[0,4,0],'children':[body]+details+[{'name':'left_wing','uuid':left_id,'origin':[1.5,7,-3],'children':[left]},
                {'name':'right_wing','uuid':right_id,'origin':[-1.5,7,-3],'children':[right]}]}],
            'animations':[{'name':'animation.'+planet+'_glowbug.flight','uuid':str(uuid.uuid5(uuid.NAMESPACE_URL,planet+'bugflight')),'loop':'loop','length':1.2,'animators':{}}]}
        for bone,sign in [(left_id,1),(right_id,-1)]:
            rig['animations'][0]['animators'][bone]={'type':'bone','name':'wing','keyframes':[{'channel':'rotation','time':t,'data_points':[{'x':'0','y':'0','z':str(sign*angle)}],'interpolation':'linear'} for t,angle in [(0,15),(.3,-15),(.6,15),(.9,-15),(1.2,15)]]}
        write(OUT/'blockbench'/f'{planet}_glowbug.bbmodel',rig);projects.append(planet+'_glowbug')
        resource('assets/zerog_tweaks/models/item/'+planet+'_glowbug_spawn_egg.json',{'parent':'minecraft:item/template_spawn_egg'})
        resource('data/zerog_tweaks/loot_table/entities/'+planet+'_glowbug.json',{'type':'minecraft:entity','pools':[]})
        # Vanilla-compatible natural spawn entries in the named world's existing biomes.
        biome_ids=lore['planets'][planet]['biomes']+(['starbloom_meadow','concord_quarries'] if planet=='cerulon' else [])
        resource('data/zerog_tweaks/neoforge/biome_modifier/'+planet+'_glowbugs.json',{'type':'neoforge:add_spawns','biomes':['zerog_tweaks:'+b for b in biome_ids],
            'spawners':[{'type':'zerog_tweaks:'+planet+'_glowbug','weight':4,'minCount':1,'maxCount':2}]})
        for kind in ['glow_shrub','glow_flower','glow_mushroom']:
            name=planet+'_'+kind; im=plant(PALETTES[planet],2800+index,kind); texture('block/'+name+'.png',im)
            model(name,{'parent':'minecraft:block/cross','textures':{'cross':'zerog_tweaks:block/'+name},'render_type':'minecraft:cutout'}); loot(name); project(name,im,'cross'); naturals.append(name)
    for key,(palette,alpha,light,habitat) in FLUIDS.items():
        for mode,size in [('still',32),('flow',64)]:
            strip=Image.new('RGBA',(size,size*16))
            for t in range(16): strip.paste(fluid_frame(key,size,t,mode=='flow'),(0,t*size))
            texture('block/'+key+'_'+mode+'.png',strip)
            resource('assets/zerog_tweaks/textures/block/'+key+'_'+mode+'.png.mcmeta',{'animation':{'frametime':4 if key=='magma_slag' else 2,'width':size,'height':size,'interpolate':True}})
        icon=bucket(tuple(bytes.fromhex(palette[2]))); texture('item/'+key+'_bucket.png',icon); project(key+'_bucket',icon,'item')
        model(key,{'textures':{'particle':'zerog_tweaks:block/'+key+'_still'}},item=False)
        resource('assets/zerog_tweaks/models/item/'+key+'_bucket.json',{'parent':'minecraft:item/generated','textures':{'layer0':'zerog_tweaks:item/'+key+'_bucket'}})
        resource('data/zerog_tweaks/tags/fluid/'+key+'.json',{'replace':False,'values':['zerog_tweaks:'+key,'zerog_tweaks:flowing_'+key]})
    resource('data/zerog_tweaks/damage_type/solar_plasma.json',{'message_id':'solar_plasma','scaling':'never','exhaustion':.1})
    resource('data/zerog_tweaks/worldgen/configured_feature/dimension_ecology.json',{'type':'zerog_tweaks:dimension_ecology','config':{}})
    resource('data/zerog_tweaks/worldgen/placed_feature/dimension_ecology.json',{'feature':'zerog_tweaks:dimension_ecology','placement':[
        {'type':'minecraft:rarity_filter','chance':3},{'type':'minecraft:in_square'},{'type':'minecraft:heightmap','heightmap':'WORLD_SURFACE_WG'},{'type':'minecraft:biome'}]})
    # Same feature order across all planetary biomes prevents shared-feature cycles.
    for path in (data/'worldgen/biome').glob('*.json'):
        obj=json.loads(path.read_text()); feature='zerog_tweaks:dimension_ecology'
        if feature not in obj['features'][9]: obj['features'][9].insert(0,feature)
        resource('data/zerog_tweaks/worldgen/biome/'+path.name,obj)
    # Pools, not planet-wide ocean replacement. Existing Starlight cave lakes are preserved.
    habitat_biomes={
        'acid':['wasteland_acid_swamps','wasteland_mud_flats','wasteland_moss_bogs'],
        'magma_slag':['ember_fields','marble_contact_zone','charwood_barrens','wasteland_basalt_fields','wasteland_ash_plains','wasteland_lava_lakes'],
        'cryo_fluid':['frozen_graveyard','phantom_ice_sheets','hoarwood_taiga','wasteland_glaciers','wasteland_ice_spike_forest','wasteland_frozen_canyons'],
        'solar_plasma':['corona_flats','sunspot_plateaus','gildwood_oasis'],
        'null_fluid':['lunar_highlands','lunar_mare','shadowed_craters','wasteland_cratered_plains','wasteland_dust_badlands','wasteland_canyon_scars'],
    }
    for key,biomes in habitat_biomes.items():
        barrier={'acid':'sludgestone','magma_slag':'skarn_rock','cryo_fluid':'permafrost','solar_plasma':'solar_stone','null_fluid':'lunar_stone'}[key]
        resource(f'data/zerog_tweaks/worldgen/configured_feature/lake_{key}.json',{'type':'minecraft:lake','config':{'fluid':{'type':'minecraft:simple_state_provider','state':{'Name':'zerog_tweaks:'+key,'Properties':{'level':'0'}}},'barrier':{'type':'minecraft:simple_state_provider','state':{'Name':'zerog_tweaks:'+barrier}}}})
        resource(f'data/zerog_tweaks/worldgen/placed_feature/lake_{key}_surface.json',{'feature':'zerog_tweaks:lake_'+key,'placement':[{'type':'minecraft:rarity_filter','chance':24},{'type':'minecraft:in_square'},{'type':'minecraft:heightmap','heightmap':'WORLD_SURFACE_WG'},{'type':'minecraft:biome'}]})
        for biome in biomes:
            path=data/'worldgen/biome'/f'{biome}.json'; obj=json.loads(path.read_text()); feature='zerog_tweaks:lake_'+key+'_surface'
            if feature not in obj['features'][1]: obj['features'][1].append(feature)
            resource('data/zerog_tweaks/worldgen/biome/'+biome+'.json',obj)
    def tag(relative,entries):
        path=res/relative; obj=json.loads(path.read_text()) if path.exists() else {'replace':False,'values':[]}
        obj['values']=list(dict.fromkeys(obj['values']+['zerog_tweaks:'+x for x in entries])); resource(relative,obj)
    tag('data/minecraft/tags/block/dirt.json',[d+'_soil' for d in dimensions]+[d+'_grass_block' for d in dimensions])
    tag('data/minecraft/tags/block/mineable/shovel.json',[d+s for d in dimensions for s in ['_soil','_farmland','_grass_block']]+[d+'_star_sand' for d in dimensions])
    for category in ['block','item']: tag('data/minecraft/tags/'+category+'/sand.json',[d+'_star_sand' for d in dimensions])
    for category in ['block','item']: tag('data/minecraft/tags/'+category+'/flowers.json',[n for n in naturals if 'glow_' in n])
    tag('data/minecraft/tags/block/animals_spawnable_on.json',[d+'_grass_block' for d in dimensions])
    creative=code/'src/main/java/net/zerog/tweaks/registry/ZGCreativeTabContents.java'; text=creative.read_text()
    for section,ids in [('NATURAL_BLOCKS',naturals),('TOOLS_AND_UTILITIES',[k+'_bucket' for k in FLUIDS]),('SPAWN_EGGS',[p+'_glowbug_spawn_egg' for p in lore['planets']])]:
        pattern=r'(public static final String\[\] '+section+r' = \{)(.*?)(\n    \};)'; match=re.search(pattern,text,re.S)
        existing=set(re.findall(r'"([^"]+)"',match[2])); additions=[n for n in ids if n not in existing]
        if additions: text=text[:match.start()]+match[1]+match[2].rstrip()+',\n            '+', '.join('"'+n+'"' for n in additions)+match[3]+text[match.end():]
    creative.write_text(text)
    lang_path=asset/'lang/en_us.json'; lang=json.loads(lang_path.read_text())
    for name in naturals: lang['block.zerog_tweaks.'+name]=name.replace('_',' ').title()
    for key in FLUIDS:
        title=key.replace('_',' ').title(); lang['block.zerog_tweaks.'+key]=title; lang['fluid_type.zerog_tweaks.'+key]=title; lang['item.zerog_tweaks.'+key+'_bucket']=title+' Bucket'
    for planet in lore['planets']:
        lang['entity.zerog_tweaks.'+planet+'_glowbug']=planet.title()+' Glowbug'
        lang['item.zerog_tweaks.'+planet+'_glowbug_spawn_egg']=planet.title()+' Glowbug Spawn Egg'
    lang['death.attack.solar_plasma']='%1$s was consumed by solar plasma'; resource('assets/zerog_tweaks/lang/en_us.json',lang)
    # Native texture cards plus full-size references; all labelled as offline art.
    columns=6; sheet=Image.new('RGB',(1200,60+len(dimensions)*115),(21,29,42)); d=ImageDraw.Draw(sheet)
    d.text((20,20),'34 dimensions - soil / dry farmland / wet farmland / grass / short grass / tall grass',fill='white')
    for i,dim in enumerate(dimensions):
        d.text((20,60+i*115),dim,fill='white')
        paths=[dim+'_soil',dim+'_farmland_dry',dim+'_farmland_wet',dim+'_grass_top',dim+'_short_grass',dim+'_tall_grass']
        for n,path in enumerate(paths):
            tile=images['block/'+path+'.png'].resize((80,80),Image.Resampling.NEAREST); sheet.paste(tile,(210+n*150,60+i*115),tile)
    sheet.save(OUT/'dimension_soils_reference.png')
    frames=[]; keys=['liquid_starlight']+list(FLUIDS)
    for t in range(16):
        card=Image.new('RGB',(1080,440),(21,29,42)); draw=ImageDraw.Draw(card)
        draw.text((18,15),'Six dimensional fluids - offline animation reference, not an in-game capture',fill='white')
        for i,key in enumerate(keys):
            still=Image.open(asset/'textures/block'/f'{key}_still.png').convert('RGBA'); size=still.width
            tile=still.crop((0,t*size,size,(t+1)*size)).resize((128,128),Image.Resampling.NEAREST)
            x=25+(i%3)*355; y=55+(i//3)*190; card.paste(tile,(x,y),tile); draw.text((x+142,y+40),key.replace('_',' ').title(),fill='white')
            icon=Image.open(asset/'textures/item'/f'{key}_bucket.png').convert('RGBA').resize((48,48),Image.Resampling.NEAREST); card.paste(icon,(x+142,y+70),icon)
        frames.append(card)
    frames[0].save(OUT/'dimension_fluids_reference.png'); frames[0].save(OUT/'dimension_fluids_reference.gif',save_all=True,append_images=frames[1:],duration=150,loop=0)
    extra=Image.new('RGB',(1080,850),(21,29,42));draw=ImageDraw.Draw(extra)
    draw.text((20,15),'Planet glowing flora, gas vents and glowbug UV artwork - offline asset reference',fill='white')
    for row,planet in enumerate(lore['planets']):
        y=55+row*130;draw.text((20,y+20),planet.title(),fill='white')
        for col,kind in enumerate(['glow_shrub','glow_flower','glow_mushroom','gas_vent']):
            tile=images['block/'+planet+'_'+kind+'.png'].resize((80,80),Image.Resampling.NEAREST);extra.paste(tile,(150+col*160,y),tile)
            draw.text((150+col*160,y+84),kind.replace('_',' '),fill='white')
        skin=images['entity/'+planet+'_glowbug.png'];tile=skin.crop((10,10,17,17)).resize((70,70),Image.Resampling.NEAREST)
        extra.paste(tile,(830,y),tile);draw.text((820,y+84),'Glowbug face UV',fill='white')
    extra.save(OUT/'glowing_ecology_reference.png')
    write(OUT/'manifest.json',{'schema':1,'generator':'dimension_ecology.py','dimensions':dimensions,'texture_count':len(records),'editable_projects':len(projects),'textures':records,'pool_biomes':habitat_biomes,'tests_executed':False})
    print(f'{len(dimensions)} dimensions; {len(records)} textures; {len(projects)} Blockbench projects; five fluid pool families')

if __name__=='__main__': main()
