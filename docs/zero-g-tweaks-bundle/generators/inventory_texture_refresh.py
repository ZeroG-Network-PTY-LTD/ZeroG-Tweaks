"""Reproducible Minecraft-native PNG/JSON refresh, not a GLB asset package.

Reuse the editable bee projects' default artwork, never their emissive slots.
Extend the existing food_data pixel-mask system with native 32px surface detail.
No provider calls, imported third-party artwork or game execution.
"""
import argparse, base64, hashlib, io, json, math, random
from pathlib import Path
from zipfile import ZipFile
from PIL import Image, ImageDraw, ImageFont
from food_data import F, MAT, REW, MASK

ROOT=Path(__file__).resolve().parents[2]
COLLECTION=ROOT/'asset-collection-1.21.1'
OUT=COLLECTION/'inventory-texture-refresh-v1'

def write_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2)+'\n')

def rgb(value):return tuple(int(value[i:i+2],16) for i in (1,3,5))
def shade(color,factor):
    # Approved C hue shifting: cooler shadows, warm highlights, readable clusters.
    value=tuple(max(0,min(255,round(c*factor))) for c in color)
    target=(43,34,77) if factor<1 else (255,240,205)
    mix=min(.24,abs(factor-1)*.4)
    return tuple(round(c*(1-mix)+t*mix) for c,t in zip(value,target))+(255,)

def sprite(spec):
    """Extend existing native mask shapes; four-step hue-preserving light ramps."""
    regions={}
    for y,row in enumerate(MASK[spec['mask']][:16]):
        for x,code in enumerate(row[:16]):
            if code!='.':
                for dx in range(2):
                    for dy in range(2):regions[x*2+dx,y*2+dy]=code
    if spec['mask']=='leg':
        # Jointed arthropod segment, not a one-pixel generic stick.
        regions={};mask=Image.new('L',(32,32));d=ImageDraw.Draw(mask)
        d.line([(7,26),(12,19),(18,16),(24,7)],fill=255,width=4)
        for x,y in [(12,19),(18,16)]:d.rectangle((x-2,y-2,x+2,y+2),fill=255)
        regions={(x,y):'H' for y in range(32) for x in range(32) if mask.getpixel((x,y))}
    if spec['mask']=='hide':
        mask=Image.new('L',(32,32));d=ImageDraw.Draw(mask)
        d.polygon([(8,6),(12,8),(20,8),(24,6),(26,10),(23,13),(25,19),
                   (27,23),(23,26),(20,23),(12,23),(9,26),(5,23),(8,19),(9,13),(6,10)],fill=255)
        regions={(x,y):'H' for y in range(32) for x in range(32) if mask.getpixel((x,y))}
    image=Image.new('RGBA',(32,32));palette={code:rgb(spec.get(code,spec['H']) if spec.get(code)!='GRILL' else spec['H']) for code in 'HGAW'}
    for (x,y),code in regions.items():
        upper=any((x+dx,y+dy) not in regions for dx,dy in [(-1,0),(0,-1)])
        lower=any((x+dx,y+dy) not in regions for dx,dy in [(1,0),(0,1)])
        base=palette[code]
        # Interior texture follows material, without noisy whole-image RGB grain.
        factor=.72 if lower and not upper else 1.23 if upper else [1.02,1.08,1.14][((x//2)*7+(y//2)*11)%3]
        image.putpixel((x,y),shade(base,factor))
    d=ImageDraw.Draw(image)
    def detail(x,y,color):
        if (x,y) in regions and regions[x,y]=='H':image.putpixel((x,y),color)
    shape=spec['mask'];raw=spec.get('kind')=='raw';cooked=spec.get('kind')=='cooked'
    for (x,y),code in regions.items():
        if code!='H':continue
        interior=all((x+dx,y+dy) in regions for dx,dy in [(2,0),(-2,0),(0,2),(0,-2)])
        if not interior:continue
        if cooked and shape in {'steak','loin','chop','slab','ribs','fillet','tail','drumstick'} and (x+y)%9 in (0,1):
            detail(x,y,shade(palette['H'],.64))
        elif raw and shape in {'steak','loin','chop','slab','ribs','fillet'} and (x+2*y)%17 in (0,1):
            detail(x,y,shade(palette.get('W',palette['A']),.94))
        elif shape in {'hide','skin','scale','shell','tail'} and (x+3*y)%11==0:
            detail(x,y,shade(palette['H'],1.35))
        elif shape in {'fluff','hide'} and x%5==2 and y%7 in (2,3):
            detail(x,y,shade(palette['H'],.76))
        elif shape in {'core','spark','dust','gel','gland'} and (x*7+y*3)%19==0:
            detail(x,y,shade(palette['H'],1.45))
    if 'grub' in spec['k']:
        for y in range(10,23,4):
            for x in range(8,25):detail(x,y,shade(palette['H'],.72))
    if shape=='fish':
        for x,y in [(7,13),(8,13),(7,14)]:detail(x,y,(25,43,59,255))
    # Uniform 2px safe inset, preserve ratio and center by alpha bounds.
    bounds=image.getbbox();body=image.crop(bounds)
    if max(body.size)>28:
        body.thumbnail((28,28),Image.Resampling.NEAREST)
    result=Image.new('RGBA',(32,32));result.alpha_composite(body,((32-body.width)//2,(32-body.height)//2))
    return result

def starlite_face(top=False):
    """Interlocking crystal facets and shallow bevels, not diagonal checker stripes."""
    im=Image.new('RGBA',(32,32),(104,97,166,255));d=ImageDraw.Draw(im)
    cells=[[(0,0),(13,0),(10,9),(0,12)],[(13,0),(31,0),(31,8),(21,12),(10,9)],
           [(0,12),(10,9),(17,17),(10,25),(0,23)],[(10,9),(21,12),(26,22),(17,17)],
           [(21,12),(31,8),(31,25),(26,22)],[(0,23),(10,25),(14,31),(0,31)],
           [(10,25),(17,17),(26,22),(22,31),(14,31)],[(26,22),(31,25),(31,31),(22,31)]]
    tones=[(150,143,202),(169,161,218),(130,123,184),(184,176,230),(121,113,175),(160,153,211),(143,135,196),(174,166,224)]
    for polygon,color in zip(cells,tones):
        d.polygon(polygon,fill=shade(color,1.06 if top else 1))
        d.line(polygon[:2],fill=shade(color,1.14),width=1)
    for x,y in [(5,4),(21,4),(5,17),(16,23),(27,16),(25,28)]:
        d.line((x,y,x+2,y),fill=(205,200,245,255),width=1)
    return im

def armor_icon(piece,cosmic):
    """Own pixel silhouette following vanilla inventory armour proportions."""
    mask=Image.new('L',(32,32));d=ImageDraw.Draw(mask)
    if piece=='helmet':
        d.polygon([(7,6),(24,6),(27,10),(27,25),(22,25),(22,15),(10,15),(10,25),(5,25),(5,10)],fill=255)
    elif piece=='chestplate':
        d.polygon([(5,7),(10,5),(12,9),(19,9),(22,5),(27,7),(29,13),(25,17),(22,15),
                   (22,27),(9,27),(9,15),(6,17),(2,13)],fill=255)
    elif piece=='leggings':
        d.rectangle((6,5,25,11),fill=255);d.rectangle((6,11,13,27),fill=255);d.rectangle((18,11,25,27),fill=255)
    else:
        d.rectangle((6,7,12,24),fill=255);d.rectangle((19,7,25,24),fill=255)
        d.rectangle((3,23,12,27),fill=255);d.rectangle((19,23,28,27),fill=255)
    base=(53,73,98) if cosmic else (180,146,81);trim=(93,221,231) if cosmic else (247,212,133)
    result=Image.new('RGBA',(32,32))
    for y in range(32):
        for x in range(32):
            if not mask.getpixel((x,y)):continue
            upper=x==0 or y==0 or not mask.getpixel((x-1,y)) or not mask.getpixel((x,y-1))
            lower=x==31 or y==31 or not mask.getpixel((x+1,y)) or not mask.getpixel((x,y+1))
            result.putpixel((x,y),shade(base,1.24 if upper else .72 if lower else 1.02))
            if y in ([11,12] if piece=='helmet' else [9,25]) or (piece=='chestplate' and x in [12,19] and 15<=y<=23):
                result.putpixel((x,y),trim+(255,))
    return result

def sheet(items,path,title):
    # Offline sprite catalogue, not a screenshot or engine capture.
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
    columns=6;rows=math.ceil(len(items)/columns);im=Image.new('RGB',(columns*170,60+rows*136),(25,31,43));d=ImageDraw.Draw(im)
    d.text((18,18),title,font=font,fill=(226,233,248))
    for n,(name,png) in enumerate(items):
        x=n%columns*170;y=60+n//columns*136
        d.rectangle((x+8,y+4,x+160,y+132),fill=(41,49,65))
        icon=Image.open(png).convert('RGBA');icon=icon.resize((96,96),Image.Resampling.NEAREST)
        im.paste(icon,(x+(170-icon.width)//2,y+8),icon)
        d.text((x+10,y+106),name.replace('_',' ')[:23],font=font,fill=(214,224,240))
    im.save(path)

def block_preview(side,top,path):
    """Offline orthographic voxel preview. No renderer/GPU evidence implied."""
    texture=side.resize((256,256),Image.Resampling.NEAREST)
    upper=top.resize((256,256),Image.Resampling.NEAREST)
    canvas=Image.new('RGBA',(560,585),(25,31,43,255))
    # Affine inverses map destination diamond/side coordinates into source UVs.
    faces=[(upper,(.5,1,-180,-.5,1,100)),
           (texture,(1,0,-24,-.5,1,-156)),
           (texture,(1,0,-280,.5,1,-436))]
    for index,(tex,transform) in enumerate(faces):
        # Faces are assembled from explicit quad regions, not arbitrary masks.
        if index==0:polygon=[(24,168),(280,40),(536,168),(280,296)]
        elif index==1:polygon=[(24,168),(280,296),(280,552),(24,424)]
        else:polygon=[(280,296),(536,168),(536,424),(280,552)]
        layer=tex.transform(canvas.size,Image.Transform.AFFINE,transform,Image.Resampling.NEAREST)
        mask=Image.new('L',canvas.size);ImageDraw.Draw(mask).polygon(polygon,fill=255)
        # Restrict each face to the authored quad so transparent borders stay clean.
        canvas.paste(layer,(0,0),mask)
    canvas.convert('RGB').save(path)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--bee-jar',type=Path,required=True)
    parser.add_argument('--code',type=Path,help='Separate 1.21.x checkout; ship normal fallback assets as well as the built-in pack')
    args=parser.parse_args()
    pack=OUT/'resourcepack';assets=pack/'assets';source=COLLECTION/'bees/blockbench_by_use/items'
    candidates={}
    for path in sorted(source.rglob('*.bbmodel')):
        model=json.loads(path.read_text())
        for texture in model.get('textures',[]):
            if texture.get('render_mode','default')=='emissive':continue
            name=texture['name'];data=base64.b64decode(texture['source'].split(',',1)[1])
            candidates.setdefault(name,(data,str(path.relative_to(COLLECTION))))
    restored=[];models=[];missing=[]
    with ZipFile(args.bee_jar) as jar:
        for name in sorted(jar.namelist()):
            if not name.startswith('assets/aeroapiary/models/item/') or not name.endswith('.json'):continue
            model=json.loads(jar.read(name));layers=model.get('textures',{})
            gui=None
            for layer,ref in layers.items():
                if not layer.startswith('layer') or not ref.startswith('aeroapiary:item/'):continue
                filename=ref.split('/')[-1]+'.png';entry=candidates.get(filename)
                if not entry:missing.append((name,filename));continue
                data,provenance=entry;im=Image.open(io.BytesIO(data)).convert('RGBA');colors={p[:3] for p in im.get_flattened_data() if p[3]>0}
                if not colors or all(min(c)>245 for c in colors):raise ValueError('Default art is white: '+filename)
                dst=assets/'aeroapiary/textures/item'/filename;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
                bounds=im.getbbox();cx=(bounds[0]+bounds[2])/2;cy=(bounds[1]+bounds[3])/2
                extent=max((bounds[2]-bounds[0])/im.width,(bounds[3]-bounds[1])/im.height)*16
                scale=round(min(1.125,13.5/extent),4)
                gui={'rotation':[0,0,0],'translation':[round((.5-cx/im.width)*16*scale,4),round((cy/im.height-.5)*16*scale,4),0],
                     'scale':[scale]*3}
                restored.append({'model':name,'texture':str(dst.relative_to(pack)),'source':provenance,'sha256':hashlib.sha256(data).hexdigest()})
            if gui:
                model.setdefault('display',{})['gui']=gui;write_json(pack/name,model);models.append(name)
    # Missing defaults are reported, never filled with generic placeholders.
    write_json(OUT/'unresolved-bee-layers.json',missing)
    revised_armor=[]
    for cosmic in [False,True]:
        family='cosmic_apiarist' if cosmic else 'apiarist'
        for piece in ['helmet','chestplate','leggings','boots']:
            filename=f'{family}_{piece}_inventory.png';png=assets/'aeroapiary/textures/item'/filename
            armor_icon(piece,cosmic).save(png);revised_armor.append(filename)
            model_path=assets/'aeroapiary/models/item'/f'{family}_{piece}.json'
            model=json.loads(model_path.read_text());model['display']['gui']={'rotation':[0,0,0],'translation':[0,0,0],'scale':[1,1,1]}
            write_json(model_path,model)
    for row in restored:
        row['runtime_sha256']=hashlib.sha256((pack/row['texture']).read_bytes()).hexdigest()
        if Path(row['texture']).name in revised_armor:row['revision']='New own vanilla-proportioned 32px inventory armor icon'
    foods=[]
    for spec in F+MAT+REW:
        png=assets/'zerog_tweaks/textures/item'/f"{spec['k']}.png";png.parent.mkdir(parents=True,exist_ok=True);sprite(spec).save(png)
        write_json(assets/'zerog_tweaks/models/item'/f"{spec['k']}.json",{'parent':'minecraft:item/generated',
            'textures':{'layer0':f"zerog_tweaks:item/{spec['k']}"}})
        foods.append((spec['k'],png))
    for name,top in [('starlite_block',False),('starlite_block_top',True)]:
        png=assets/'zerog_tweaks/textures/block'/f'{name}.png';png.parent.mkdir(parents=True,exist_ok=True);starlite_face(top).save(png)
    block_preview(starlite_face(),starlite_face(True),OUT/'starlite-block-offline-preview.png')
    write_json(assets/'zerog_tweaks/models/block/starlite_block.json',{'parent':'minecraft:block/cube_bottom_top','textures':{
        'side':'zerog_tweaks:block/starlite_block','bottom':'zerog_tweaks:block/starlite_block','top':'zerog_tweaks:block/starlite_block_top'}})
    write_json(pack/'pack.mcmeta',{'pack':{'pack_format':34,'description':'ZeroG inventory colour recovery and 32px material refresh'}})
    sheet(foods,OUT/'food-and-materials-preview.png','32px food and material refresh — offline pixel-art catalogue')
    bee_items=[(Path(row['model']).stem,pack/row['texture']) for row in restored]
    sheet(bee_items,OUT/'bee-icons-recovered-preview.png','Recovered default bee artwork — no emissive-slot overwrite')
    manifest={'format':'Minecraft Java 1.21.1 PNG/JSON resource pack (not canonical GLB)','bee_jar_sha256':hashlib.sha256(args.bee_jar.read_bytes()).hexdigest(),
              'restored_bee_layers':restored,'bee_models':models,'unresolved_bee_layers':missing,'updated_sprites':[name for name,_ in foods],
              'revised_armor_icons':revised_armor,
              'texture_budget':'32x32 newly rendered sprites; recovered original bee sprites retain their authored dimensions',
              'glow_policy':'Default artwork only. Emissive slots never export over visible texture names.',
              'preview_policy':'Offline sprite catalogues; no GPU/game visual approval claimed.'}
    manifest['files']=[{'path':file.relative_to(pack).as_posix(),
                       'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}
                      for file in sorted(assets.rglob('*')) if file.is_file()]
    write_json(OUT/'manifest.json',manifest)
    if args.code:
        # A saved selection can put mod_resources above the built-in refresh pack.
        # Ship the same pixels/models in our normal mod resources too; do not
        # silently rewrite the player's selected packs or the separate addon JAR.
        import shutil
        runtime=args.code/'src/main/resources'
        for file in assets.rglob('*'):
            if not file.is_file():continue
            relative=file.relative_to(pack)
            for destination in [runtime/relative,runtime/'resourcepacks/visual_refresh'/relative]:
                destination.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(file,destination)
    print(json.dumps({'restored_layers':len(restored),'sprites':len(foods),'unresolved_layers':missing,'output':str(OUT)}))
if __name__=='__main__':main()
