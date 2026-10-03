"""Original concept-inspired art on Minecraft 1.21.1 Java BeeModel UVs.

No Mojang PNGs are copied. Run after dimension_ecology.py with --code-root PATH.
Entity PNG animation is explicit renderer frame selection, NOT an entity mcmeta.
"""
import argparse,base64,hashlib,io,json,math,re,random,uuid
from pathlib import Path
from PIL import Image,ImageDraw
from crystals_v2 import embedded_project
from dimension_ecology import bucket,adjust

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/asset-collection-1.21.1/miniature-planet-bees-v1'
STYLES={
 'flora':((128,163,54),(241,220,80),(232,138,206)),
 'midnight':((21,18,73),(74,61,167),(62,208,243)),
 'crimson':((68,13,18),(169,32,24),(250,160,29)),
 'tropical':((45,147,133),(216,40,115),(250,190,69)),
 'gold_dust':((226,218,182),(255,253,235),(245,199,67)),
 'magma':((35,33,35),(74,64,60),(248,106,14)),
 'frost':((76,132,151),(187,224,235),(227,253,255))}
FAMILIES={'moon':'midnight','mars':'crimson','cerulon':'flora','skarn':'magma','eidolon':'frost','solvane':'gold_dust',
 'flora_bee':'flora','midnight_bee':'midnight','crimson_bee':'crimson','tropical_bee':'tropical','gold_dust_bee':'gold_dust','magma_bee':'magma'}
HOMES={'flora_bee':'cerulon','midnight_bee':'moon','crimson_bee':'mars','tropical_bee':'cerulon','gold_dust_bee':'solvane','magma_bee':'skarn'}
BODY={'north':(10,10,17,17),'east':(0,10,10,17),'west':(17,10,27,17),'south':(27,10,34,17),'up':(10,0,17,10),'down':(17,0,24,10)}
WINGS=[(6,18,15,24),(15,18,24,24)]
def painting(style,w,h,frame=0):
    base,secondary,accent=STYLES[style];im=Image.new('RGBA',(w,h));px=im.load()
    rng=random.Random(198+len(style));phase=math.tau*frame/8
    for y in range(h):
        for x in range(w):
            c=adjust(base,.8+.2*(1-y/max(h-1,1))+.05*rng.random())
            if style=='midnight':
                r=math.hypot(x-w/2,y-h/2);a=math.atan2(y-h/2,x-w/2)+r*.7
                if math.sin(a*2+phase)>.7:c=adjust(secondary,1.2)
            elif style in ('magma','crimson'):
                if abs(math.sin(x*.55+y*.29)+math.sin(y*.7-x*.22))<.24:c=accent
            elif style=='tropical':
                if x%max(3,w//4)==0 or y%max(3,h//3)==0:c=secondary
                if (x+y)%9==0:c=accent
            elif style=='gold_dust':
                if x in (0,w-1) or y in (0,h-1):c=accent
                elif rng.random()<.07:c=(255,255,235)
            else:
                if y%6==0:c=secondary
                if (x*3+y*5)%23==0:c=accent
            px[x,y]=c+(255,)
    return im
def skin(style,frame):
    im=Image.new('RGBA',(64,64));base,secondary,accent=STYLES[style]
    for face,(x,y,x2,y2) in BODY.items():im.alpha_composite(painting(style,x2-x,y2-y,frame),(x,y))
    d=ImageDraw.Draw(im)
    # Face occupies north island, never arbitrary pixels outside the actual rig.
    head=secondary if style in ('flora','tropical','gold_dust') else base
    d.rectangle((10,10,16,16),fill=head+(255,))
    for x in [11,15]:
        d.rectangle((x,11,x+1,13),fill=(10,12,23,255));d.point((x,11),fill=accent+(255,))
    d.line((13,15,14,15),fill=(26,19,24,255))
    for island in WINGS:
        x,y,x2,y2=island;wing=painting(style,9,6,frame);wd=ImageDraw.Draw(wing)
        if style=='flora':
            wd.rectangle((0,0,8,5),fill=(119,206,176,185));wd.line((1,4,7,1),fill=(201,255,218,225));wd.rectangle((3,2,5,3),fill=(237,145,195,255));wd.point((4,2),fill=(255,227,147,255))
        elif style=='gold_dust':
            wd.rectangle((0,0,8,5),fill=(255,230,124,225));wd.rectangle((2,1,6,4),fill=(255,251,207,255))
        elif style=='tropical':
            wd.rectangle((0,0,8,5),fill=(247,147,49,225));wd.rectangle((1,1,7,4),fill=(231,65,139,225));wd.line((2,4,6,1),fill=(121,222,209,230))
        for yy in range(6):
            for xx in range(9):
                c=wing.getpixel((xx,yy));wing.putpixel((xx,yy),c[:3]+(215 if 0<xx<8 and 0<yy<5 else 130,))
        wd.line((1,0,7,0),fill=accent+(255,));wd.point(((frame+2)%7+1,2),fill=(255,251,220,255))
        im.alpha_composite(wing,(x,y))
    # Antenna islands and the stinger/three leg planes are painted explicitly.
    for x,y,x2,y2 in [(2,0,10,5),(2,3,10,8),(26,7,30,10)]:d.rectangle((x,y,x2-1,y2-1),fill=adjust(base,.45)+(255,))
    for y in (1,3,5):
        for x in (26,29,32):d.line((x,y,x,y+1),fill=adjust(base,.4)+(255,))
    return im
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code-root',type=Path,required=True);args=p.parse_args()
    res=args.code_root/'src/main/resources';assets=res/'assets/zerog_tweaks';records=[];projects=[]
    def write(relative,obj):
        for root in [res,OUT/'resource-source']:
            target=root/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(obj,indent=2)+'\n')
    def tex(name,im):
        target=OUT/'textures'/name;target.parent.mkdir(parents=True,exist_ok=True);im.save(target)
        dst=assets/'textures'/name;dst.parent.mkdir(parents=True,exist_ok=True)
        before=OUT/'before'/name
        if dst.exists() and not before.exists():before.parent.mkdir(parents=True,exist_ok=True);before.write_bytes(dst.read_bytes())
        dst.write_bytes(target.read_bytes());records.append({'path':name,'size':list(im.size),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    def project(name,im,kind='item'):
        obj=embedded_project(name,im,kind);obj['resolution']={'width':im.width,'height':im.height}
        for el in obj['elements']:
            for face in el['faces'].values():face['uv']=[0,0,im.width,im.height]
        obj['textures'][0].update(width=im.width,height=im.height,uv_width=im.width,uv_height=im.height)
        target=OUT/'blockbench'/(name+'.bbmodel');target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(obj,indent=2)+'\n');projects.append(name)
    lang=json.loads((assets/'lang/en_us.json').read_text());lore=json.loads((ROOT/'docs/zero-g-tweaks-bundle/data-manifest.json').read_text())
    preview=Image.new('RGBA',(1200,80+len(FAMILIES)*150),'#171d28');draw=ImageDraw.Draw(preview)
    draw.text((20,18),'ZeroG miniature bee collection - original vanilla-UV art / both wing faces painted',fill='white')
    draw.text((20,42),'Offline texture and product review; model uses vanilla BeeModel, 0.5 renderer scale / .35 x .3 hitbox',fill='#aebad0')
    for index,(key,style) in enumerate(FAMILIES.items()):
        entity=key if key.endswith('bee') else key+'_glowbug';base,secondary,accent=STYLES[style]
        frames=[skin(style,n) for n in range(8)]
        for n,im in enumerate(frames):tex('entity/'+key+'_glowbug_frame_'+str(n)+'.png',im)
        tex('entity/'+key+'_glowbug.png',frames[0]);blink=frames[0].copy();bd=ImageDraw.Draw(blink)
        for x in [11,15]:bd.rectangle((x,11,x+1,13),fill=(secondary if style in ('flora','tropical','gold_dust') else base)+(255,));bd.line((x,13,x+1,13),fill=(10,12,23,255))
        tex('entity/'+key+'_glowbug_blink.png',blink)
        mask=Image.new('RGBA',(64,64));md=ImageDraw.Draw(mask)
        for x in [11,15]:md.point((x,11),fill=accent+(255,))
        for x,y,x2,y2 in WINGS:md.line((x+1,y,x2-2,y),fill=accent+(255,))
        tex('entity/'+key+'_glowbug_glowmask.png',mask)
        template=json.loads((ROOT/'docs/asset-collection-1.21.1/dimension-ecology-v1/blockbench/moon_glowbug.bbmodel').read_text())
        template['name']=entity;template['model_identifier']='geometry.'+entity
        buf=io.BytesIO();frames[0].save(buf,format='PNG');template['textures'][0]['source']='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
        template['textures'][0]['name']=entity+'.png'
        # Authored rig is also half scale; UVs remain unchanged.
        for el in template['elements']:
            for field in ['from','to','origin']:
                if field in el:el[field]=[v*.5 for v in el[field]]
        def scale_bones(nodes):
            for node in nodes:
                if isinstance(node,dict):
                    if 'origin' in node:node['origin']=[v*.5 for v in node['origin']]
                    scale_bones(node.get('children',[]))
        scale_bones(template['outliner'])
        path=OUT/'blockbench'/(entity+'.bbmodel');path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(template,indent=2)+'\n');projects.append(entity)
        hive=key+'_hive';top=painting(style,32,32);side=painting(style,32,32)
        # Hive surfaces are not enlarged copies of the entity's tiny wing motif.
        rng=random.Random(index+800);sd=ImageDraw.Draw(side)
        if style in ('midnight','magma','crimson'):
            for yy in range(32):
                for xx in range(32):side.putpixel((xx,yy),adjust(base,rng.choice([.7,.84,1,1.1]))+(255,))
            vein=accent if style!='midnight' else (40,146,205)
            for path in [[(0,5),(5,7),(9,3),(13,9),(10,15),(16,20),(14,27),(18,31)],[(31,8),(25,9),(23,16),(16,20)],[(0,25),(7,23),(10,15)],[(13,9),(21,6),(24,0)]]:
                sd.line(path,fill=adjust(vein,.65),width=2);sd.line(path,fill=vein,width=1)
        elif style=='tropical':
            for yy in range(32):
                for xx in range(32):side.putpixel((xx,yy),adjust(base,rng.choice([.74,.86,1,1.1]))+(255,))
            sd.rectangle((0,0,31,31),outline=secondary,width=3)
            for ox,oy in [(4,4),(18,4),(4,18),(18,18)]:sd.line([(ox,oy+9),(ox,oy),(ox+9,oy),(ox+9,oy+9),(ox+4,oy+9),(ox+4,oy+4),(ox+7,oy+4)],fill=adjust(base,1.55),width=2)
        elif style in ('flora','frost'):
            for yy in range(32):
                for xx in range(32):side.putpixel((xx,yy),adjust(base,rng.choice([.7,.82,.95,1.06]))+(255,))
            for yy in [5,13,21,29]:sd.line((0,yy,31,yy),fill=adjust(base,.55));sd.line((0,yy+1,31,yy+1),fill=adjust(base,1.15))
        td=ImageDraw.Draw(top);sd=ImageDraw.Draw(side)
        if style in ('flora','tropical'):
            for inset in [3,7,11]:td.rectangle((inset,inset,31-inset,31-inset),outline=accent if inset==3 else secondary,width=2)
        if style=='flora':
            for x,y in [(8,9),(22,20),(12,25)]:
                sd.line((x,y,x,y+4),fill=(65,101,41),width=2);sd.rectangle((x-2,y-2,x+2,y+1),fill=accent);sd.point((x,y),fill=(255,228,119))
        if style=='gold_dust':
            for image in [side,top]:
                dd=ImageDraw.Draw(image);dd.rectangle((1,1,30,30),outline=accent,width=3);dd.rectangle((10,9,21,22),fill=(43,67,163),outline=(251,243,196),width=2);dd.line((13,11,13,20),fill=(120,182,242),width=2)
        front=side.copy();fd=ImageDraw.Draw(front)
        fd.rectangle((8,14,23,17),fill=(13,13,23,255));fd.line((8,18,23,18),fill=accent+(255,))
        honey=front.copy();hd=ImageDraw.Draw(honey);hd.line((10,18,10,23),fill=accent+(255,),width=2);hd.line((21,18,21,26),fill=accent+(255,),width=2)
        for suffix,im in [('top',top),('side',side),('front',front),('front_honey',honey)]:tex('block/'+hive+'_'+suffix+'.png',im)
        honey_strip=Image.new('RGBA',(32,32*8))
        for n in range(8):
            frame=honey.copy();dd=ImageDraw.Draw(frame);dd.point((10,18+n%6),fill=(255,248,211));dd.point((21,18+(n+3)%8),fill=(255,248,211));honey_strip.paste(frame,(0,n*32))
        tex('block/'+hive+'_front_honey.png',honey_strip)
        for root in [assets/'textures/block',OUT/'textures/block']:(root/(hive+'_front_honey.png.mcmeta')).write_text(json.dumps({'animation':{'width':32,'height':32,'frametime':3,'interpolate':True}},indent=2)+'\n')
        for full in [False,True]:
            name=hive+('_honey' if full else '')
            write('assets/zerog_tweaks/models/block/'+name+'.json',{'parent':'minecraft:block/orientable_with_bottom','textures':{'top':'zerog_tweaks:block/'+hive+'_top','bottom':'zerog_tweaks:block/'+hive+'_side','side':'zerog_tweaks:block/'+hive+'_side','front':'zerog_tweaks:block/'+hive+('_front_honey' if full else '_front')}})
        write('assets/zerog_tweaks/blockstates/'+hive+'.json',{'variants':{'facing='+direction+',honey_level='+str(level):{'model':'zerog_tweaks:block/'+hive+('_honey' if level==5 else ''),'y':rotation} for direction,rotation in [('north',0),('east',90),('south',180),('west',270)] for level in range(6)}})
        write('assets/zerog_tweaks/models/item/'+hive+'.json',{'parent':'zerog_tweaks:block/'+hive})
        silk={'condition':'minecraft:match_tool','predicate':{'predicates':{'minecraft:enchantments':[{'enchantments':'minecraft:silk_touch','levels':{'min':1}}]}}}
        write('data/zerog_tweaks/loot_table/blocks/'+hive+'.json',{'type':'minecraft:block','pools':[{'rolls':1,'entries':[{'type':'minecraft:alternatives','children':[{'type':'minecraft:item','name':'zerog_tweaks:'+hive,'conditions':[silk],'functions':[{'function':'minecraft:copy_components','include':['minecraft:bees'],'source':'block_entity'},{'function':'minecraft:copy_state','block':'zerog_tweaks:'+hive,'properties':['honey_level']}]},{'type':'minecraft:item','name':'zerog_tweaks:'+hive}]}], 'conditions':[{'condition':'minecraft:survives_explosion'}]}]})
        project(hive,front,'cube')
        # Per-face embedded textures: top, side and front are not the same UV artwork.
        hivepath=OUT/'blockbench'/(hive+'.bbmodel');obj=json.loads(hivepath.read_text())
        for n,(label,im) in enumerate([('side',side),('top',top)]):
            buf=io.BytesIO();im.save(buf,format='PNG');t=dict(obj['textures'][0]);t.update(name=hive+'_'+label+'.png',id=str(n+1),uuid=str(uuid.uuid5(uuid.NAMESPACE_URL,hive+label)),source='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode());obj['textures'].append(t)
        for face in ['east','west','south','down']:obj['elements'][0]['faces'][face]['texture']=1
        obj['elements'][0]['faces']['up']['texture']=2;hivepath.write_text(json.dumps(obj,indent=2)+'\n')
        comb=Image.new('RGBA',(32,32));cd=ImageDraw.Draw(comb)
        for x,y in [(9,8),(20,8),(4,17),(15,17),(25,17),(10,26),(21,26)]:
            cd.polygon([(x-4,y-3),(x,y-5),(x+4,y-3),(x+4,y+2),(x,y+4),(x-4,y+2)],fill=adjust(accent,.55)+(255,));cd.polygon([(x-3,y-2),(x,y-4),(x+3,y-2),(x+3,y+1),(x,y+3),(x-3,y+1)],fill=accent+(255,));cd.line((x-2,y-2,x+1,y-3),fill=secondary+(255,))
        tex('item/'+key+'_honeycomb.png',comb);project(key+'_honeycomb',comb)
        bottle=Image.new('RGBA',(32,32));bd=ImageDraw.Draw(bottle);bd.rectangle((12,2,19,5),fill=(156,118,63,255));bd.rectangle((13,6,18,11),fill=(190,219,231,150));bd.rounded_rectangle((7,10,24,29),radius=3,fill=(179,209,230,140),outline=(230,250,255,255));bd.rectangle((9,16,22,26),fill=accent+(230,));bd.line((10,12,10,24),fill=(255,255,255,210),width=2)
        tex('item/'+key+'_honey_bottle.png',bottle);project(key+'_honey_bottle',bottle)
        honeybucket=bucket(accent);tex('item/'+key+'_honey_bucket.png',honeybucket);project(key+'_honey_bucket',honeybucket)
        for suffix in ['honeycomb','honey_bottle','honey_bucket']:
            write('assets/zerog_tweaks/models/item/'+key+'_'+suffix+'.json',{'parent':'minecraft:item/generated','textures':{'layer0':'zerog_tweaks:item/'+key+'_'+suffix}})
            lang['item.zerog_tweaks.'+key+'_'+suffix]=key.replace('_',' ').title()+' '+suffix.replace('_',' ').title()
        for size,suffix in [(32,'still'),(64,'flow')]:
            strip=Image.new('RGBA',(size,size*8))
            for n in range(8):
                im=painting(style,size,size,n);dd=ImageDraw.Draw(im)
                for xx in range(size):
                    yy=round(size*.5+math.sin(xx*math.tau/size+n*math.tau/8)*size*.12)
                    dd.point((xx,yy),fill=adjust(accent,1.12)+(240,))
                im.putalpha(225);strip.paste(im,(0,size*n))
            name=key+'_honey_'+suffix+'.png';tex('block/'+name,strip)
            for root in [assets/'textures/block',OUT/'textures/block']:(root/(name+'.mcmeta')).write_text(json.dumps({'animation':{'width':size,'height':size,'frametime':3,'interpolate':True}},indent=2)+'\n')
        write('assets/zerog_tweaks/models/block/'+key+'_honey.json',{'textures':{'particle':'zerog_tweaks:block/'+key+'_honey_still'}})
        write('assets/zerog_tweaks/blockstates/'+key+'_honey.json',{'variants':{'':{'model':'zerog_tweaks:block/'+key+'_honey'}}})
        write('assets/zerog_tweaks/models/item/'+entity+'_spawn_egg.json',{'parent':'minecraft:item/template_spawn_egg'})
        lang['entity.zerog_tweaks.'+entity]=entity.replace('_',' ').title();lang['item.zerog_tweaks.'+entity+'_spawn_egg']=entity.replace('_',' ').title()+' Spawn Egg';lang['block.zerog_tweaks.'+hive]=key.replace('_',' ').title()+' Hive';lang['fluid_type.zerog_tweaks.'+key+'_honey']=key.replace('_',' ').title()+' Honey'
        if key in HOMES:
            home=HOMES[key];biomes=lore['planets'][home]['biomes']+(['starbloom_meadow'] if home=='cerulon' else [])
            write('data/zerog_tweaks/neoforge/biome_modifier/'+entity+'_spawns.json',{'type':'neoforge:add_spawns','biomes':['zerog_tweaks:'+b for b in biomes],'spawners':[{'type':'zerog_tweaks:'+entity,'weight':3,'minCount':1,'maxCount':2}]})
        y=80+index*150;draw.text((20,y+5),entity,fill='white')
        for x,im in [(210,frames[0]),(390,front),(550,top),(710,comb),(870,honeybucket)]:preview.alpha_composite(im.resize((128,128),Image.Resampling.NEAREST),(x,y))
        draw.text((1040,y+30),HOMES.get(key,key),fill='#aebad0')
    (assets/'lang/en_us.json').write_text(json.dumps(lang,ensure_ascii=False,indent=2)+'\n')
    for path,ids in [('block/beehives',[k+'_hive' for k in FAMILIES]),('entity_type/beehive_inhabitors',[k if k.endswith('bee') else k+'_glowbug' for k in FAMILIES])]:
        relative='data/minecraft/tags/'+path+'.json';target=res/relative;obj=json.loads(target.read_text()) if target.exists() else {'replace':False,'values':[]};obj['values']+=['zerog_tweaks:'+i for i in ids if 'zerog_tweaks:'+i not in obj['values']];write(relative,obj)
    tabs=args.code_root/'src/main/java/net/zerog/tweaks/registry/ZGCreativeTabContents.java';text=tabs.read_text()
    for section,ids in [('NATURAL_BLOCKS',[k+'_hive' for k in FAMILIES]),('TOOLS_AND_UTILITIES',[k+'_honey_bucket' for k in FAMILIES]),('SPAWN_EGGS',[k+'_spawn_egg' for k in HOMES]),('INGREDIENTS',[k+'_honeycomb' for k in FAMILIES]),('FOOD_AND_DRINKS',[k+'_honey_bottle' for k in FAMILIES])]:
        pattern=r'(public static final String\[\] '+section+r' = \{)(.*?)(\n    \};)'
        def add(m):
            extra=[i for i in ids if '"'+i+'"' not in m.group(2)];return m.group(0) if not extra else m.group(1)+m.group(2).rstrip()+',\n            '+', '.join(json.dumps(i) for i in extra)+m.group(3)
        text=re.sub(pattern,add,text,flags=re.S)
    tabs.write_text(text);preview.convert('RGB').save(OUT/'miniature_bees_uv_reference.png')
    animation=[]
    for n in range(8):
        card=Image.new('RGBA',(1080,420),'#171d28');dd=ImageDraw.Draw(card)
        dd.text((20,15),'Six miniature concepts - animated texture UV reference (not an in-game capture)',fill='white')
        for i,key in enumerate(HOMES):
            x=20+i*175;im=skin(FAMILIES[key],n)
            card.alpha_composite(im.crop((10,10,17,17)).resize((112,112),Image.Resampling.NEAREST),(x,80))
            card.alpha_composite(im.crop((6,18,15,24)).resize((144,96),Image.Resampling.NEAREST),(x,225))
            dd.text((x,350),key.replace('_',' '),fill='white');dd.text((x,372),'north face / wing UV',fill='#aebad0')
        animation.append(card.convert('RGB'))
    animation[0].save(OUT/'miniature_bees_texture_animation.gif',save_all=True,append_images=animation[1:],duration=150,loop=0)
    records=list({r['path']:r for r in records}.values())
    (OUT/'manifest.json').write_text(json.dumps({'schema':1,'families':FAMILIES,'concept_homes':HOMES,'scale':.5,'textures':records,'projects':projects,'entity_animation':'eight explicit PNG frames at three ticks, plus blink and fullbright mask','client_verified':False},indent=2)+'\n')
    print(f'{len(FAMILIES)} bee families; {len(records)} textures; {len(projects)} projects')
if __name__=='__main__':main()
