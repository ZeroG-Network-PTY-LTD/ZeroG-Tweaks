"""Original native joinery/storage/tank artwork; approved indexed palettes.

No external/provider artwork, upscaling, Java registration or vanilla ID changes.
Writes only new requested stable IDs. Original doors/trapdoors remain untouched.
"""
import argparse, base64, hashlib, importlib.util, json, math, uuid, zipfile, copy
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

p=argparse.ArgumentParser();p.add_argument('--code',type=Path,required=True);a=p.parse_args()
BASE=Path(__file__).resolve().parent;RES=a.code/'src/main/resources';NS='zerog_tweaks'
spec=importlib.util.spec_from_file_location('locked_style',BASE.parent/'art-direction/generator/style_kit.py')
style=importlib.util.module_from_spec(spec);spec.loader.exec_module(style)
R={k:[style.hx(h) for h in v] for k,v in style.RAMPS.items()}
WOODS={'shardwood':('cerulite','leaf'),'charwood':('wood','copper'),
       'hoarwood':('moonsteel','cerulite'),'gildwood':('solvanite','wood')}
TIERS={'copper':'copper','nullifite':'nullifite','cyrrium':'moonsteel',
       'tectium':'solvanite','wraithsteel':'rock','astrium':'cerulite'}
FILES=[];MODELS=[];PROJECTS=[];TILES=[]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def im():return Image.new('RGBA',(32,32))
def write(relative,payload):
    src=BASE/'source'/relative;src.parent.mkdir(parents=True,exist_ok=True);src.write_bytes(payload)
    dst=RES/relative;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(payload)
    layers=[relative]
    for pack in (RES/'resourcepacks').glob('*'):
        if (pack/relative).exists():
            (pack/relative).write_bytes(payload);layers.append((pack/relative).relative_to(RES).as_posix())
    FILES.append({'path':relative,'sha256':digest(src),'layers':layers});return src
def texture(key,image):
    import io
    b=io.BytesIO();image.save(b,format='PNG');write(f'assets/{NS}/textures/{key}.png',b.getvalue())
    TILES.append((key,image));return key
def data(path,obj):write(path,(json.dumps(obj,indent=2)+'\n').encode())
def model(id,obj):data(f'assets/{NS}/models/block/{id}.json',obj);MODELS.append((id,obj))
def item(id,parent):data(f'assets/{NS}/models/item/{id}.json',{'parent':f'{NS}:block/{parent}'})
def plank(r,horizontal=False):
    out=im();d=ImageDraw.Draw(out)
    for n in range(4):
        x=n*8
        d.rectangle((x,0,x+7,31),fill=r[2+(n%2)])
        d.line((x,0,x,31),fill=r[4]);d.line((x+7,0,x+7,31),fill=r[0])
        # A few long material-grain clusters, not random noise pixels.
        for yy in [5+n*2,18-n]:
            d.line([(x+3,yy),(x+2,yy+3),(x+3,yy+8)],fill=r[1])
            d.line([(x+4,yy+1),(x+3,yy+4),(x+4,yy+7)],fill=r[4])
    return out.transpose(Image.Transpose.ROTATE_90) if horizontal else out
def frame(d,r,box,width=3):
    x1,y1,x2,y2=box
    d.rectangle(box,outline=r[0],width=width)
    d.line((x1+1,y2-1,x1+1,y1+1,x2-1,y1+1),fill=r[4])
    d.line((x2-1,y1+2,x2-1,y2-1,x1+2,y2-1),fill=r[1])
def pin(d,x,y,r):
    d.rectangle((x,y,x+2,y+2),fill=r[1]);d.point((x,y),fill=r[5]);d.point((x+1,y+1),fill=r[3])
def door(r,trim,top):
    out=plank(r);d=ImageDraw.Draw(out);frame(d,r,(0,0,31,31),3)
    if top:
        # Two genuine transparent glazed slots, each with separate carved surrounds.
        for x in [6,18]:
            frame(d,trim,(x-1,4,x+7,23),2);d.rectangle((x+1,6,x+5,21),fill=(0,0,0,0))
            d.line((x,14,x+6,14),fill=trim[3],width=2)
        d.line((4,27,27,27),fill=r[4]);d.line((4,28,27,28),fill=r[1])
    else:
        for x in [5,18]:
            d.rectangle((x,5,x+8,25),fill=r[1]);d.rectangle((x+2,7,x+6,23),fill=r[3])
            d.line((x+1,6,x+7,6),fill=r[5]);d.line((x+1,7,x+1,24),fill=r[4])
        d.rectangle((24,11,28,15),fill=trim[1]);d.rectangle((25,12,27,14),fill=trim[4])
        d.line((2,29,29,29),fill=r[4])
    for x in [2,28]:pin(d,x,3,trim);pin(d,x,26,trim)
    return out
def lattice(r,trim):
    out=im();d=ImageDraw.Draw(out);frame(d,r,(0,0,31,31),4)
    # Open lattice has true transparent diamonds, not painted black windows.
    for k in [-18,-6,6,18,30]:
        d.line([(3,k),(28,k+25)],fill=r[1],width=4)
        d.line([(3,k-1),(28,k+24)],fill=r[4])
        d.line([(3,31-k),(28,6-k)],fill=r[2],width=3)
        d.line([(3,30-k),(28,5-k)],fill=r[5])
    frame(d,r,(0,0,31,31),4)
    for x,y in [(2,2),(27,2),(2,27),(27,27)]:pin(d,x,y,trim)
    d.rectangle((12,1,19,3),fill=trim[3]);return out
def chest_face(r,trim,face):
    out=plank(r,horizontal=face=='top');d=ImageDraw.Draw(out)
    frame(d,r,(0,0,31,31),2)
    if face not in ['top','bottom']:
        d.rectangle((1,8,30,10),fill=r[0]);d.line((2,7,29,7),fill=r[5]);d.line((2,11,29,11),fill=r[4])
        for x in [3,26]:
            d.rectangle((x,1,x+2,30),fill=trim[1]);d.line((x,2,x,29),fill=trim[4])
            for yy in [3,13,26]:pin(d,x,yy,trim)
        if face=='front':
            d.rectangle((13,7,18,16),fill=trim[0]);d.rectangle((14,8,17,15),fill=trim[4]);d.rectangle((15,10,16,12),fill=trim[0])
            d.line((8,22,23,22),fill=r[1]);d.line((9,23,22,23),fill=r[4])
    else:
        for y in [3,26]:d.rectangle((2,y,29,y+2),fill=trim[2]);d.line((3,y,28,y),fill=trim[4])
        for x in [4,25]:pin(d,x,4,trim);pin(d,x,25,trim)
    return out
def barrel_face(r,trim,front=False,opened=False):
    out=plank(r);d=ImageDraw.Draw(out)
    for y in [3,25]:
        d.rectangle((0,y,31,y+3),fill=trim[1]);d.line((0,y,31,y),fill=trim[4]);d.line((0,y+3,31,y+3),fill=trim[0])
        for x in [3,15,27]:pin(d,x,y,trim)
    if front:
        d.rounded_rectangle((3,3,28,28),radius=6,fill=trim[0])
        d.rounded_rectangle((4,4,27,27),radius=5,fill=trim[3])
        d.rounded_rectangle((6,6,25,25),radius=4,fill=r[0] if opened else r[3])
        if not opened:
            for x in [10,16,22]:d.line((x,7,x,24),fill=r[1]);d.line((x+1,8,x+1,23),fill=r[4])
            d.rectangle((13,14,18,18),fill=trim[1]);d.line((14,14,17,14),fill=trim[5])
        else:d.line((9,23,22,23),fill=r[1],width=2)
    return out
def tank_face(r,side=False,top=False,level=0):
    out=im();d=ImageDraw.Draw(out);d.rectangle((0,0,31,31),fill=r[1]);frame(d,r,(0,0,31,31),4)
    if top:
        for x,y in [(4,4),(25,4),(4,25),(25,25)]:pin(d,x,y,r)
        d.rectangle((9,9,22,22),fill=r[0]);frame(d,r,(10,10,21,21),2)
        d.rectangle((14,14,17,17),fill=R['glow'][3]);d.point((14,14),fill=R['glow'][5]);return out
    d.rectangle((5,5,24,25),fill=(0,0,0,0));frame(d,r,(4,4,25,26),2)
    # Leave the window genuinely clear. The block-entity renderer paints the
    # actual stored-fluid atlas sprite/tint behind it; no grey fake fill layer.
    # Discrete gauge reads levels while fluid GUI identifies the actual contents.
    d.rectangle((27,6,29,24),fill=r[0])
    for n in range(8):d.line((27,23-n*2,28,23-n*2),fill=R['glow'][4] if n<level else r[2])
    for x,y in [(2,2),(27,2),(2,27),(27,27)]:pin(d,x,y,r)
    d.line((7,7,7,12),fill=R['cerulite'][5][:3]+(90,));d.line((8,6,12,6),fill=R['cerulite'][4][:3]+(90,))
    return out
def cube_obj(textures,box=None,translucent=False):
    box=box or ([0,0,0],[16,16,16])
    faces={f:{'uv':[0,0,16,16],'texture':'#'+f} for f in ['north','south','east','west','up','down']}
    refs={f:f'{NS}:block/{key}' for f,key in textures.items()};refs['particle']=refs['up']
    return {'parent':'minecraft:block/block','textures':refs,
            'render_type':'minecraft:translucent' if translucent else 'minecraft:cutout',
            'elements':[{'from':box[0],'to':box[1],'faces':faces}],
            'display':{'gui':{'rotation':[30,225,0],'translation':[0,0,0],'scale':[.625,.625,.625]}}}
def copy_joinery(wood,old,new):
    for path in (RES/f'assets/{NS}/models/block').glob(old+'_*.json'):
        obj=json.loads(path.read_text());obj=json.loads(json.dumps(obj).replace(old,new))
        model(path.stem.replace(old,new),obj)
    states=json.loads((RES/f'assets/{NS}/blockstates/{old}.json').read_text())
    data(f'assets/{NS}/blockstates/{new}.json',json.loads(json.dumps(states).replace(old,new)))
def blockbench(id,obj):
    textures=[];indexes={};elements=[]
    for key,ref in obj['textures'].items():
        if not ref.startswith(NS+':'):continue
        path=BASE/'source'/f'assets/{NS}/textures/{ref.split(":",1)[1]}.png'
        if not path.exists():continue
        indexes[key]=len(textures);image=Image.open(path)
        textures.append({'name':path.name,'id':str(len(textures)),'uuid':str(uuid.uuid5(uuid.NAMESPACE_URL,id+'/'+key)),
                         'source':'data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode(),
                         'width':image.width,'height':image.height,'uv_width':image.width,'uv_height':image.height})
    for j,cube in enumerate(obj.get('elements',[])):
        faces={f:{'uv':[v*2 for v in face['uv']],'texture':indexes[face['texture'].lstrip('#')]} for f,face in cube['faces'].items()}
        elements.append({'name':id+'_'+str(j),'type':'cube','uuid':str(uuid.uuid5(uuid.NAMESPACE_URL,id+'/'+str(j))),
                         'from':cube['from'],'to':cube['to'],'origin':[8,8,8],'box_uv':False,'faces':faces})
    if not elements:return
    bb={'meta':{'format_version':'4.10','model_format':'java_block','box_uv':False},'name':id,
        'resolution':{'width':32,'height':32},'elements':elements,'outliner':[e['uuid'] for e in elements],'textures':textures}
    path=BASE/'blockbench'/f'{id}.bbmodel';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(bb,indent=2)+'\n')
    PROJECTS.append({'path':path.relative_to(BASE).as_posix(),'sha256':digest(path)})
def gui():
    out=Image.new('RGBA',(176,204));d=ImageDraw.Draw(out);r=R['rock'];metal=R['moonsteel']
    d.rectangle((0,0,175,203),fill=r[0]);d.rectangle((1,1,173,201),fill=r[3]);d.line((2,2,172,2),fill=metal[4]);d.line((2,2,2,200),fill=metal[4])
    d.rectangle((5,19,170,71),fill=r[1]);d.rectangle((7,57,168,68),fill=r[0]);d.line((8,58,167,58),fill=r[4])
    d.rectangle((5,74,170,117),fill=r[2]);d.line((7,119,168,119),fill=r[0])
    # Standard 18px slot surround, with slot interior left unfilled by item art.
    for y in [123,141,159,181]:
        for x in range(7,169,18):
            d.rectangle((x,y,x+17,y+17),fill=r[0]);d.rectangle((x+1,y+1,x+16,y+16),fill=r[2]);d.line((x+1,y+17,x+17,y+17,x+17,y+1),fill=r[5])
    texture('gui/fluid_tank',out)
def generator_gui():
    out=Image.new('RGBA',(176,184));d=ImageDraw.Draw(out);r=R['rock'];metal=R['moonsteel']
    d.rectangle((0,0,175,183),fill=r[0]);d.rectangle((1,1,173,181),fill=r[3]);d.line((2,2,172,2),fill=metal[4]);d.line((2,2,2,180),fill=metal[4])
    d.rectangle((5,19,170,61),fill=r[1]);d.rectangle((5,64,170,95),fill=r[2]);d.line((7,97,168,97),fill=r[0])
    # Author the receptacles, not a permanently burning flame or full FE bar.
    for x,y in [(47,35)]+[(x,y) for y in [101,119,137,159] for x in range(7,169,18)]:
        d.rectangle((x,y,x+17,y+17),fill=r[0]);d.rectangle((x+1,y+1,x+16,y+16),fill=r[2]);d.line((x+1,y+17,x+17,y+17,x+17,y+1),fill=r[5])
    d.rectangle((127,21,140,78),fill=r[0]);d.line((128,22,139,22),fill=metal[3])
    d.rectangle((71,36,86,52),outline=r[0]);d.line((72,53,85,53),fill=r[4])
    for x in [110,146]:d.line((x,31,x,47),fill=r[2]);d.point((x,31),fill=metal[3])
    texture('gui/combustion_generator',out)
def expansion_module(flux=False):
    out=im();d=ImageDraw.Draw(out);r=R['moonsteel'];accent=R['glow']
    d.polygon([(6,8),(12,3),(25,4),(28,9),(27,24),(21,29),(6,27),(3,22),(3,13)],fill=r[0])
    d.polygon([(7,9),(13,5),(24,6),(25,10),(24,23),(20,26),(7,25),(5,21),(5,14)],fill=r[3])
    d.line((7,9,13,5,24,6),fill=r[5],width=2);d.line((7,24,20,25,24,22),fill=r[1],width=2)
    if flux:
        d.rectangle((8,11,23,22),fill=r[1]);d.line((8,12,22,12),fill=r[4])
        for y in [13,17,21]:
            d.line((10,y,13,y-2,20,y-2,23,y+1),fill=R['copper'][1],width=3)
            d.line((10,y-1,13,y-3,20,y-3,23,y),fill=R['copper'][4])
        d.polygon([(17,10),(12,16),(17,16),(14,23),(21,14),(17,14)],fill=accent[3]);d.line((17,11,14,15),fill=accent[5])
    else:
        for x in [9,15,21]:
            d.rectangle((x,11,x+3,21),fill=r[1]);d.line((x+1,12,x+1,18),fill=r[4]);d.point((x+1,20),fill=accent[3])
    d.polygon([(11,7),(16,5),(20,8),(16,11)],fill=accent[1]);d.polygon([(13,7),(16,6),(18,8),(16,9)],fill=accent[4]);d.point((15,7),fill=accent[5])
    id='generator_flux_module' if flux else 'storage_expansion_module'
    texture('item/'+id,out)
    data(f'assets/{NS}/models/item/{id}.json',{'parent':'minecraft:item/generated','textures':{'layer0':f'{NS}:item/{id}'}})
    obj={'textures':{'north':f'{NS}:item/{id}'},'elements':[{'from':[0,0,8],'to':[16,16,8],'faces':{'north':{'uv':[0,0,16,16],'texture':'#north'},'south':{'uv':[16,0,0,16],'texture':'#north'}}}]}
    blockbench(id,obj)
def main():
    client=Path('C:/Users/jakem/.gradle/caches/neoformruntime/artifacts/minecraft_1.21.1_client.jar') if str(a.code).startswith('C:') else Path('/mnt/c/Users/jakem/.gradle/caches/neoformruntime/artifacts/minecraft_1.21.1_client.jar')
    jar=zipfile.ZipFile(client)
    for wood,(ramp,trim_ramp) in WOODS.items():
        r,t=R[ramp],R[trim_ramp];door_id=wood+'_panel_door';trap=wood+'_lattice_trapdoor'
        texture('block/'+door_id+'_top',door(r,t,True));texture('block/'+door_id+'_bottom',door(r,t,False));texture('block/'+trap,lattice(r,t))
        copy_joinery(wood,wood+'_door',door_id);copy_joinery(wood,wood+'_trapdoor',trap)
        # Native inventory outline, not resized from the 64px double-door faces.
        icon=im();d=ImageDraw.Draw(icon);d.rectangle((7,2,24,29),fill=r[1]);frame(d,r,(7,2,24,29),2)
        for x in [10,18]:frame(d,t,(x,5,x+3,13),1);d.rectangle((x+1,6,x+2,12),fill=(0,0,0,0))
        d.rectangle((10,17,21,25),fill=r[3]);d.line((10,17,21,17),fill=r[5]);d.rectangle((21,15,22,17),fill=t[4])
        for x in [12,18]:d.line((x,19,x,24),fill=r[1]);d.line((x+1,19,x+1,23),fill=r[4])
        texture('item/'+door_id,icon);data(f'assets/{NS}/models/item/{door_id}.json',{'parent':'minecraft:item/generated','textures':{'layer0':f'{NS}:item/{door_id}'}})
        item(trap,trap+'_bottom')
        for face in ['front','side','top','bottom']:texture('block/'+wood+'_chest_'+face,chest_face(r,t,face))
        chest=wood+'_chest';tex={'north':chest+'_front','south':chest+'_side','east':chest+'_side','west':chest+'_side','up':chest+'_top','down':chest+'_bottom'}
        obj=cube_obj(tex,([1,0,1],[15,14,15]));model(chest,obj);item(chest,chest);blockbench(chest,obj)
        data(f'assets/{NS}/blockstates/{chest}.json',{'variants':{f'facing={f}':{'model':f'{NS}:block/{chest}','y':j*90} for j,f in enumerate(['north','east','south','west'])}})
        for part,front,opened in [('side',False,False),('front',True,False),('front_open',True,True)]:texture('block/'+wood+'_barrel_'+part,barrel_face(r,t,front,opened))
        barrel=wood+'_barrel'
        for opened in [False,True]:
            tex={f:barrel+'_side' for f in ['north','south','east','west','up','down']};tex['north']=barrel+('_front_open' if opened else '_front')
            obj=cube_obj(tex);model(barrel+('_open' if opened else ''),obj)
            if not opened:blockbench(barrel,obj)
        item(barrel,barrel);variants={}
        for f,x,y in [('north',0,0),('east',0,90),('south',0,180),('west',0,270),('up',270,0),('down',90,0)]:
            for opened in [False,True]:variants[f'facing={f},open={str(opened).lower()}']={'model':f'{NS}:block/{barrel}'+('_open' if opened else ''),'x':x,'y':y}
        data(f'assets/{NS}/blockstates/{barrel}.json',{'variants':variants})
        # Editable original joinery, embedded textures, matching thin-door dimensions.
        door_obj={'textures':{'bottom':f'{NS}:block/{door_id}_bottom','top':f'{NS}:block/{door_id}_top'},'elements':[]}
        for half in ['bottom','top']:
            template=json.loads(jar.read(f'assets/minecraft/models/block/door_{half}_left.json'))
            for cube in template['elements']:
                cube=copy.deepcopy(cube)
                if half=='top':cube['from'][1]+=16;cube['to'][1]+=16
                door_obj['elements'].append(cube)
        blockbench(door_id,door_obj)
        template=json.loads(jar.read('assets/minecraft/models/block/template_orientable_trapdoor_bottom.json'))
        template['textures']={'texture':f'{NS}:block/{trap}'};blockbench(trap,template)
    for tier,ramp in TIERS.items():
        r=R[ramp];id=tier+'_fluid_tank';texture('block/'+id+'_top',tank_face(r,top=True))
        variants={}
        for level in range(9):
            key=id+'_level'+str(level);texture('block/'+key,tank_face(r,level=level))
            tex={f:key for f in ['north','south','east','west']};tex.update(up=id+'_top',down=id+'_top')
            obj=cube_obj(tex,translucent=True);model(key,obj)
            if level==0:blockbench(id,obj)
            for j,f in enumerate(['north','east','south','west']):variants[f'facing={f},level={level}']={'model':f'{NS}:block/{key}','y':j*90}
        data(f'assets/{NS}/blockstates/{id}.json',{'variants':variants});item(id,id+'_level0')
    jar.close();expansion_module();expansion_module(True);gui();generator_gui();validate()
def validate():
    errors=[]
    for row in FILES:
        for layer in row['layers']:
            if digest(RES/layer)!=row['sha256']:errors.append('hash mismatch '+layer)
        if row['path'].endswith('.png') and not Image.open(RES/row['path']).getbbox():errors.append('empty '+row['path'])
    for id,obj in MODELS:
        for ref in obj.get('textures',{}).values():
            if ref.startswith(NS+':') and not (RES/f'assets/{NS}/textures/{ref.split(":",1)[1]}.png').exists():errors.append('missing texture '+ref)
        for cube in obj.get('elements',[]):
            for face in cube['faces'].values():
                if any(v<0 or v>16 for v in face['uv']):errors.append('UV '+id)
    fontpath=Path('C:/Windows/Fonts/consola.ttf');font=ImageFont.truetype(str(fontpath),11) if fontpath.exists() else ImageFont.load_default()
    native=[(key,image) for key,image in TILES if image.size==(32,32)]
    for key,image in TILES:
        if image.size!=(32,32):
            name='fluid-tank-panel-native.png' if key=='gui/fluid_tank' else 'combustion-generator-panel-native.png'
            image.save(BASE/name)
    for page in range(math.ceil(len(native)/48)):
        batch=native[page*48:(page+1)*48];out=Image.new('RGB',(960,45+math.ceil(len(batch)/8)*130),(19,25,37));d=ImageDraw.Draw(out)
        d.text((8,10),'Native exported assets; not client captures — storage/joinery/tanks',font=font,fill=(220,229,245))
        for j,(key,image) in enumerate(batch):
            x=j%8*120;y=45+j//8*130
            small=image;large=image.resize((80,80),Image.Resampling.NEAREST)
            out.paste(small,(x+2,y+40),small);out.paste(large,(x+37,y),large)
            name=Path(key).name;d.text((x+2,y+84),name[:18],font=font,fill=(218,229,243));d.text((x+2,y+98),name[18:36],font=font,fill=(218,229,243))
        out.save(BASE/f'native-gallery-{page+1:02d}.png')
    receipt={'license':'All Rights Reserved, original repository-authored native source','paid_generation':False,'canonical_package_admission':False,
             'cli_limitation':'game-dev unavailable; approved repository-native source workflow, no provider/vendor import',
             'source_sha256':digest(Path(__file__)),'style_source_sha256':digest(BASE.parent/'art-direction/generator/style_kit.py'),
             'palettes':style.RAMPS,'wood_ramp_roles':WOODS,'tank_ramp_roles':TIERS,'files':FILES,'blockbench':PROJECTS,
             'vanilla_template_source_sha256':digest(a.code/'src/main/resources/assets/zerog_tweaks/models/block/shardwood_door_bottom_left.json'),
             'counts':{'textures':len(TILES),'models':len(MODELS),'blockbench':len(PROJECTS)},'validation_errors':errors,'client_verified':False}
    (BASE/'manifest.json').write_text(json.dumps(receipt,indent=2)+'\n')
    if errors:raise SystemExit('\n'.join(errors))
    print(json.dumps(receipt['counts']))
if __name__=='__main__':main()
