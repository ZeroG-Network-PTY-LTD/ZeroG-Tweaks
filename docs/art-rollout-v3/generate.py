"""Original 32px A/C art rollout, plus explicit addon terminal model bindings.

No paid providers, concept-sheet cropping, registry additions or gameplay changes.
Run after inventory_texture_refresh, planet-botany-v2 and wood-dust-art-v2.
Original PNG/JSON provenance is recorded; GPU review is not claimed.
"""
import argparse, base64, colorsys, copy, hashlib, io, json, math, random, sys, uuid
from pathlib import Path
from zipfile import ZipFile
from PIL import Image, ImageDraw

p=argparse.ArgumentParser();p.add_argument('--code',type=Path,required=True)
p.add_argument('--bee-jar',type=Path,required=True);a=p.parse_args()
base=Path(__file__).resolve().parent;res=a.code/'src/main/resources';source=base/'source'
sys.path.insert(0,str(base.parent/'zero-g-tweaks-bundle/generators'))
from data import M
rows=[];tiles=[];bindings=[]
def tint(c,k=1):
    target=(45,34,78) if k<1 else (255,240,200);blend=min(.25,abs(k-1)*.4)
    return tuple(round(max(0,min(255,v*k))*(1-blend)+t*blend) for v,t in zip(c,target))+(255,)
def save(rel,payload,category):
    src=source/rel;src.parent.mkdir(parents=True,exist_ok=True);src.write_bytes(payload)
    for dst in [res/rel,res/'resourcepacks/visual_refresh'/rel]:
        dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(payload)
    rows.append({'path':rel,'category':category,'sha256':hashlib.sha256(payload).hexdigest()})
def png(ns,key,im,category):
    out=io.BytesIO();im.save(out,format='PNG');save(f'assets/{ns}/textures/{key}.png',out.getvalue(),category)
    tiles.append((ns+':'+key,im.copy()))
def model(ns,key,obj,category):
    save(f'assets/{ns}/models/{key}.json',(json.dumps(obj,indent=2)+'\n').encode(),category)
def blank():return Image.new('RGBA',(32,32))
def mineral(c,kind,accent):
    im=blank();d=ImageDraw.Draw(im)
    if kind=='ingot':
        d.polygon([(3,13),(10,6),(25,7),(29,14),(26,24),(9,27),(3,21)],fill=tint(c,.35))
        d.polygon([(4,14),(11,8),(24,9),(27,14),(21,19),(9,20)],fill=tint(c,1.12))
        d.polygon([(4,15),(9,21),(9,25),(4,20)],fill=tint(c,.65))
        d.polygon([(10,21),(22,20),(27,15),(25,22),(10,25)],fill=tint(c,.83))
        d.line([(6,13),(12,9),(23,10)],fill=tint(c,1.4))
        d.line([(11,22),(21,21)],fill=tint(c,.5))
        d.line([(16,11),(19,12),(17,14)],fill=tint(accent,1.1))
    elif kind in ['raw','nugget']:
        for x,y,r in ([(10,17,6),(21,13,7),(20,25,4)] if kind=='raw' else [(16,17,8)]):
            d.polygon([(x-r,y-2),(x-2,y-r),(x+r-2,y-r+2),(x+r,y+3),(x+2,y+r),(x-r,y+4)],fill=tint(c,.45))
            d.polygon([(x-r+1,y-2),(x-2,y-r+1),(x+r-3,y-r+3),(x+1,y+1)],fill=tint(c,1.2))
            d.polygon([(x+1,y+1),(x+r-1,y-1),(x+r-1,y+3),(x+2,y+r-1)],fill=tint(c,.88))
            d.line([(x-r+2,y-2),(x-2,y-r+2)],fill=tint(c,1.5))
            d.line([(x-2,y+4),(x+2,y+2),(x+4,y+3)],fill=tint(accent,.9))
    elif kind=='orb':
        d.ellipse((5,5,27,27),fill=tint(c,.39));d.ellipse((6,5,26,24),fill=tint(c,.85))
        d.arc((7,6,24,23),160,275,fill=tint(c,1.5),width=2)
        d.polygon([(16,9),(18,14),(23,16),(18,18),(16,23),(14,18),(9,16),(14,14)],fill=tint(accent,1.1))
        d.point((16,16),fill=(255,249,227,255));d.line((20,24,24,21),fill=tint(c,.55))
    else:
        points=[(9,4),(22,4),(28,12),(18,29),(13,29),(4,13)]
        d.polygon(points,fill=tint(c,.35))
        d.polygon([(10,5),(21,5),(19,13),(10,14),(6,12)],fill=tint(c,1.17))
        d.polygon([(21,5),(26,12),(19,13)],fill=tint(c,.84))
        d.polygon([(10,14),(19,14),(17,27),(14,27)],fill=tint(c,1.0))
        d.polygon([(6,14),(10,15),(13,26)],fill=tint(c,.63))
        d.polygon([(20,15),(26,14),(18,27)],fill=tint(c,.52))
        d.line((11,6,18,6),fill=tint(c,1.55));d.line((12,15,14,21),fill=tint(accent,1.12))
    return im
def berry(c,seed):
    im=blank();d=ImageDraw.Draw(im);variant=seed%3
    for x,y,r in ([(10,17,6),(21,15,6),(17,25,5)] if variant==0 else
                  [(12,14,6),(21,22,7)] if variant==1 else [(10,22,5),(17,15,6),(24,23,5)]):
        d.ellipse((x-r,y-r,x+r,y+r),fill=tint(c,.42))
        d.ellipse((x-r+1,y-r,x+r-1,y+r-2),fill=tint(c,.94))
        d.line((x-r+3,y-r+2,x-r+2,y-1),fill=tint(c,1.35),width=2)
        d.point((x+2,y+3),fill=tint(c,.57))
    green=(70,145,119)
    d.line([(17,12),(16,7),(20,3)],fill=tint(green,.7),width=2)
    d.polygon([(16,9),(8,3),(8,7),(13,11)],fill=tint(green));d.line((9,5,14,9),fill=tint(green,1.3))
    d.polygon([(17,8),(26,4),(23,9),(17,12)],fill=tint(green,.8));d.point((11,14),fill=tint(c,1.55))
    return im
def rind(c,top,seed):
    im=blank();d=ImageDraw.Draw(im)
    for y in range(32):
        for x in range(32):
            angle=math.atan2(y-15.5,x-15.5) if top else x/32*math.tau
            rib=(math.cos(angle*6+seed%3*.2)+1)/2
            light=.54+.45*rib+.12*(1-y/32)
            im.putpixel((x,y),tint(c,light))
    # Fine botanical striations, not ore seams or random checkerboard noise.
    if top:
        for n in range(6):
            t=n*math.tau/6;d.line([(16,16),(round(16+14*math.cos(t)),round(16+14*math.sin(t)))],fill=tint(c,.48))
        d.rectangle((13,12,18,18),fill=(43,86,64,255));d.line((14,13,16,13),fill=(131,176,117,255))
    else:
        for x in [4,10,15,21,27]:
            for y in range(3+(x%4),30,6):d.line((x,y,x,y+2),fill=tint(c,1.15))
    return im
def stone(c,seed):
    # Wrapped irregular rock patches, never masonry rows or square checker noise.
    im=blank();d=ImageDraw.Draw(im);rng=random.Random(seed)
    centres=[(rng.randrange(32),rng.randrange(32),rng.choice([.54,.61,.69,.76,.82])) for _ in range(11)]
    for y in range(32):
        for x in range(32):
            distances=sorted((min(abs(x-cx),32-abs(x-cx))**2+min(abs(y-cy),32-abs(y-cy))**2,k,cx,cy) for cx,cy,k in centres)
            _,k,cx,cy=distances[0];edge=distances[1][0]-distances[0][0]
            if edge<7:k-=.10
            elif x<cx and y<cy:k+=.08
            im.putpixel((x,y),tint(c,k))
    for x,y in [(5,3),(18,16),(28,7)]:d.line([(x,y),(x-2,y+5),(x,y+11)],fill=tint(c,.36))
    return im
def point(c,direction,thickness):
    im=blank();width={'tip':7,'tip_merge':7,'frustum':10,'middle':11,'base':14}[thickness]
    for y in range(32):
        factor=(.04+y/31) if thickness=='tip' else (.20+.65*y/31) if thickness=='tip_merge' else (.60+.40*y/31) if thickness=='frustum' else (.75+.25*y/31) if thickness=='base' else .88
        w=max(1,round(width*factor))
        for x in range(16-w,17+w):
            if 0<=x<32:
                side=(x-16)/max(1,w);ridge=.2 if (x+y//9)%5==0 else 0
                k=.48+.43*(1-abs(side+.25))-ridge
                im.putpixel((x,y),tint(c,k))
    if direction=='down':im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return im
def vent(c,top=False):
    im=stone(c,'vent');d=ImageDraw.Draw(im)
    if top:
        for r,k in [(12,.4),(10,.9),(8,.26),(5,.6),(3,1.2)]:
            d.ellipse((16-r,16-r,15+r,15+r),fill=tint(c,k))
        for x,y in [(10,12),(17,9),(20,17),(13,21)]:d.point((x,y),fill=tint(c,1.45))
    else:
        for x in [7,15,23]:
            d.line([(x,4),(x-2,11),(x+1,20),(x-1,28)],fill=tint(c,.32),width=3)
            d.line([(x,5),(x-1,11),(x+2,20),(x,27)],fill=tint(c,1.05),width=1)
    return im
def terminal(c,tier=1):
    im=Image.new('RGBA',(32,32),(28,34,48,255));d=ImageDraw.Draw(im)
    d.rectangle((1,1,30,30),outline=(77,95,113,255));d.line((2,2,29,2),fill=(139,163,180,255))
    d.rectangle((4,4,27,21),fill=(8,21,33,255),outline=tint(c,.8))
    d.line((6,7,23,7),fill=tint(c,1.12));d.line((6,10,16,10),fill=tint(c,.78))
    d.line([(6,17),(10,17),(12,13),(15,19),(18,14),(24,14)],fill=tint(c,1.2))
    for x in [6,11,16,21]:d.rectangle((x,25,x+2,27),fill=tint(c,.9))
    d.rectangle((25,24,27,27),fill=(123,216,151,255))
    for x in range(min(7,tier)):d.point((6+x*3,20),fill=tint(c,1.3))
    return im
def machine_side(c,face):
    im=Image.new('RGBA',(32,32),(35,43,56,255));d=ImageDraw.Draw(im)
    d.rectangle((1,1,30,30),outline=(93,112,131,255));d.rectangle((4,4,27,27),outline=(21,27,38,255))
    if face in ['left','right','back']:
        for y in range(8,24,3):d.line((8,y,23,y),fill=(18,26,37,255));d.point((8,y),fill=tint(c,.64))
    else:
        d.rectangle((9,9,22,22),outline=tint(c,.83));d.line((10,10,20,10),fill=(120,144,161,255))
    for x,y in [(3,3),(28,3),(3,28),(28,28)]:d.point((x,y),fill=(164,177,185,255))
    return im

materials={key:(tuple(bytes.fromhex(v['pal'][2][1:])),tuple(bytes.fromhex(v['pal'][5][1:])),v['role']) for key,v in M.items()}
for row in json.loads((a.code/'tools/planet_material_art_manifest.json').read_text()):
    c=tuple(bytes.fromhex(row['colour'].lstrip('#')));materials[row['id']]=(c,(124,221,238),'diamond' if row['gem'] else 'metal')
for key,(c,accent,role) in materials.items():
    candidates={key+'_ingot':'ingot',key+'_nugget':'nugget','raw_'+key:'raw',key+'_raw':'raw',key+'_gem':'gem'}
    if role in ['diamond','crystal','orb']:candidates[key]='orb' if role=='orb' else 'gem'
    for id,kind in candidates.items():
        if (res/f'assets/zerog_tweaks/textures/item/{id}.png').exists():png('zerog_tweaks','item/'+id,mineral(c,kind,accent),'materials')

cavepal={'moon':(145,115,231),'mars':(70,199,178),'cerulon':(241,136,179),'skarn':(124,196,246),'eidolon':(242,153,76),'solvane':(124,99,230)}
themes=json.loads((a.code/'tools/planet_materials.json').read_text())['dimension_themes']
for dim,home in sorted(themes.items()):
    c=cavepal[home];h,s,v=colorsys.rgb_to_hsv(*(x/255 for x in c));seed=int(hashlib.sha256(dim.encode()).hexdigest()[:4],16)
    c=tuple(round(x*255) for x in colorsys.hsv_to_rgb((h+(seed%17-8)/100)%1,s,v))
    png('zerog_tweaks','item/'+dim+'_cave_berry',berry(c,seed),'cave_berries')
    png('zerog_tweaks','block/'+dim+'_dripstone_block',stone(c,seed),'dripstone')
    for direction in ['up','down']:
        for thickness in ['tip','tip_merge','frustum','middle','base']:
            png('zerog_tweaks',f'block/{dim}_pointed_dripstone_{direction}_{thickness}',point(c,direction,thickness),'dripstone')
    # Inventory stalactite is the pointed mineral, not a round food blob.
    item=point(c,'up','tip');png('zerog_tweaks','item/'+dim+'_pointed_dripstone',item,'dripstone_items')
vinefruit={'moon':(185,172,234),'mars':(236,156,87),'cerulon':(92,220,206),
           'skarn':(239,123,85),'eidolon':(156,223,245),'solvane':(249,213,99)}
for index,(home,c) in enumerate(vinefruit.items()):
    png('zerog_tweaks','item/'+home+'_vine_fruit',berry(c,index),'vine_fruits')
for index,(id,home) in enumerate({'nebula_melon':'cerulon','eclipse_pumpkin':'moon','aurora_melon':'eidolon','solar_melon':'solvane'}.items()):
    c=cavepal[home]
    for face in ['side','top']:png('zerog_tweaks','block/'+id+'_'+face,rind(c,face=='top',index),'gourds')
for id,home in [(home+'_gas_vent',home) for home in cavepal]+[('flare_vent','solvane'),('flare_vent_top','solvane'),('vent_rock','skarn')]:
    if (res/f'assets/zerog_tweaks/textures/block/{id}.png').exists():png('zerog_tweaks','block/'+id,vent(cavepal[home],id.endswith('_top') or 'gas_vent' in id),'vents')

with ZipFile(a.bee_jar) as addon:
    def project(id,obj):
        # Embedded editable Blockbench snapshot of the exact Java model.
        refs={k:v for k,v in obj['textures'].items() if k!='particle'};textures=[]
        for key,ref in refs.items():
            ns,path=ref.split(':');relative=f'assets/{ns}/textures/{path}.png'
            data=(res/relative).read_bytes() if (res/relative).exists() else addon.read(relative)
            image=Image.open(io.BytesIO(data));textures.append({'name':Path(path).name+'.png',
                'id':str(len(textures)),'uuid':str(uuid.uuid5(uuid.NAMESPACE_URL,id+'/'+key)),
                'width':image.width,'height':image.height,'source':'data:image/png;base64,'+base64.b64encode(data).decode()})
        size=max(t['width'] for t in textures);indices={key:i for i,key in enumerate(refs)}
        for t in textures:t['uv_width']=size;t['uv_height']=size
        elements=[]
        cubes=obj.get('elements') or [{'from':[0,0,0],'to':[16,16,16],
            'faces':{face:{'texture':'#'+slot,'uv':[0,0,16,16]} for face,slot in
                     [('north','north'),('south','south'),('east','east'),('west','west'),('up','up'),('down','down')]}}]
        for i,cube in enumerate(cubes):
            elements.append({'name':'terminal_panel' if cube['from']==[4,5,1.4] else f'body_{i}',
                'type':'cube','uuid':str(uuid.uuid5(uuid.NAMESPACE_URL,id+'/'+str(i))),
                'from':cube['from'],'to':cube['to'],'origin':[8,8,8],'box_uv':False,
                'faces':{face:{'texture':indices[value['texture'].removeprefix('#')],
                               'uv':[u*size/16 for u in value.get('uv',[0,0,16,16])]}
                         for face,value in cube['faces'].items()}})
        result={'meta':{'format_version':'4.10','model_format':'java_block','box_uv':False},
                'name':id,'resolution':{'width':size,'height':size},'elements':elements,
                'textures':textures,'outliner':[e['uuid'] for e in elements]}
        dest=base/'blockbench'/(id+'.bbmodel');dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(result,indent=2)+'\n')
    for tier,c in enumerate([(108,204,218),(164,185,240),(122,225,180),(239,171,110),(216,148,241),(245,213,106),(242,153,198)],1):
        obj=json.loads(addon.read(f'assets/aeroapiary/models/block/tier{tier}/controller.json'))
        for face in ['front','back','left','right','top','bottom']:
            png('aeroapiary',f'block/tier{tier}/controller_{face}',terminal(c,tier) if face=='front' else machine_side(c,face),'controllers')
        model('aeroapiary',f'block/tier{tier}/controller',obj,'controller_models')
        project(f'tier{tier}_controller',obj)
        bindings.append({'id':f'tier{tier}_controller','front':'north','model':f'block/tier{tier}/controller','facing_from_existing_blockstate':True})
    for id,c in [('apiary_controller',(112,218,225)),('genetic_splicer',(189,139,239))]:
        obj=json.loads(addon.read(f'assets/aeroapiary/models/block/other/{id}.json'))
        ref=f'aeroapiary:block/machines/{id}_terminal';obj['textures']['terminal']=ref
        png('aeroapiary',f'block/machines/{id}_terminal',terminal(c),'controllers')
        screens=[e for e in obj['elements'] if e['from']==[4,5,1.4] and e['to']==[12,11,2]]
        assert len(screens)==1,id
        screens[0]['faces']['north']={'uv':[0,0,16,16],'texture':'#terminal'}
        model('aeroapiary','block/other/'+id,obj,'controller_models')
        project(id,obj)
        bindings.append({'id':id,'front':'north','model':'block/other/'+id,'geometry_preserved':True})

updated_projects=[]
latest_images={Path(row['path']).name:source/row['path'] for row in rows if row['path'].endswith('.png') and row['path'].startswith('assets/zerog_tweaks/')}
for folder in [base.parent/'planet-botany-v2/blockbench',base.parent/'asset-collection-1.21.1/planet-art-refresh-v1/blockbench']:
    for file in sorted(folder.glob('*.bbmodel')):
        obj=json.loads(file.read_text());changed=False
        for texture in obj['textures']:
            image_path=latest_images.get(texture['name'])
            if not image_path:continue
            image=Image.open(image_path)
            assert image.size==(texture['width'],texture['height']),file
            texture['source']='data:image/png;base64,'+base64.b64encode(image_path.read_bytes()).decode();changed=True
        if changed:
            file.write_text(json.dumps(obj,indent=2)+'\n')
            updated_projects.append({'path':file.relative_to(base.parent.parent).as_posix(),'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
manifest={'original_art':True,'license':'All Rights Reserved','resolution':32,
          'style':'A natural volume and C selective hue-shifted accents',
          'generator':'docs/art-rollout-v3/generate.py','files':rows,'controller_bindings':bindings,
          'gpu_verified':False,'world_light_changed':False,
          'bee_addon_sha256':hashlib.sha256(a.bee_jar.read_bytes()).hexdigest(),
          'updated_existing_projects':updated_projects,
          'controller_projects':[str(file.relative_to(base.parent.parent)) for file in sorted((base/'blockbench').glob('*.bbmodel'))]}
item_projects=[]
for row in rows:
    if '/textures/item/' not in row['path'] or not row['path'].endswith('.png'):continue
    name=Path(row['path']).stem;data=(source/row['path']).read_bytes()
    element={'name':name,'type':'cube','uuid':str(uuid.uuid5(uuid.NAMESPACE_URL,'zerog:item/'+name)),
             'from':[0,0,8],'to':[16,16,8],'origin':[8,8,8],'box_uv':False,
             'faces':{'north':{'uv':[0,0,32,32],'texture':0},'south':{'uv':[32,0,0,32],'texture':0}}}
    obj={'meta':{'format_version':'4.10','model_format':'java_block','box_uv':False},
         'name':name,'resolution':{'width':32,'height':32},'elements':[element],
         'outliner':[element['uuid']],
         'textures':[{'name':name+'.png','id':'0','uuid':str(uuid.uuid5(uuid.NAMESPACE_URL,name+'/texture')),
                     'width':32,'height':32,'uv_width':32,'uv_height':32,
                     'source':'data:image/png;base64,'+base64.b64encode(data).decode()}]}
    file=base/'item-blockbench'/(name+'.bbmodel');file.parent.mkdir(parents=True,exist_ok=True)
    file.write_text(json.dumps(obj,indent=2)+'\n');item_projects.append(file.relative_to(base.parent.parent).as_posix())
manifest['item_preview_projects']=item_projects
(base/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
def preview(category,name):
    chosen=[v for v in tiles if v[0].startswith('aeroapiary:') or category in v[0]] if category else tiles
    if category=='materials':chosen=[v for v in tiles if ':item/' in v[0] and not any(s in v[0] for s in ['cave_berry','pointed_dripstone'])]
    if category=='controllers':chosen=[v for v in tiles if 'controller_front' in v[0] or '_terminal' in v[0]]
    if category=='environment':chosen=[v for v in tiles if any(s in v[0] for s in ['melon','vent','moon_pointed_dripstone','moon_dripstone','cerulon_cave_berry','eidolon_cave_berry'])]
    cols=6;sheet=Image.new('RGB',(cols*164,40+math.ceil(len(chosen)/cols)*148),(19,26,37));d=ImageDraw.Draw(sheet)
    d.text((12,12),'Native 32px source art - not an in-game capture',fill=(222,233,245))
    for index,(id,im) in enumerate(chosen):
        x=index%cols*164;y=40+index//cols*148;tile=im.resize((96,96),Image.Resampling.NEAREST);sheet.paste(tile,(x+34,y),tile)
        label=id.split('/')[-1];d.text((x+4,y+101),label[:25],fill=(202,220,236));d.text((x+4,y+115),label[25:50],fill=(202,220,236))
    sheet.save(base/name)
preview('controllers','controller-terminals-preview.png');preview('materials','material-sprites-preview.png');preview('environment','environment-preview.png')
print(json.dumps({'files':len(rows),'controller_families':len(bindings),'output':str(base)}))
