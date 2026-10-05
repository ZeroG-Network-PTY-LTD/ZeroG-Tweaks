"""Targeted native transport revision. No resizing, provider jobs or model rewrites."""
import argparse,ast,hashlib,json,math,random
from pathlib import Path
from PIL import Image,ImageDraw

p=argparse.ArgumentParser();p.add_argument('--code',type=Path,required=True);a=p.parse_args()
base=Path(__file__).resolve().parent;legacy=base.parent/'full-art-rollout-v4';source=legacy/'transport-source/transport.py'
names={'hx','P','pipe_texture','cell_side','cell_top','gauge'}
nodes=[]
for node in ast.parse(source.read_text()).body:
    if isinstance(node,ast.FunctionDef) and node.name in names:nodes.append(node)
    elif isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'TIERS','TYPES'} for t in node.targets):nodes.append(node)
ctx={'Image':Image,'ImageDraw':ImageDraw,'math':math,'random':random}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),ctx)
textures={}
for i,tier in enumerate(ctx['TIERS']):
    for suffix,function in [('item_tube',lambda n:ctx['pipe_texture']('item',n)),('energy_cell_side',ctx['cell_side']),('energy_cell_top',ctx['cell_top'])]:textures[tier[0]+'_'+suffix]=function(i)
for i in range(9):textures['energy_cell_gauge_'+str(i)]=ctx['gauge'](i)
res=a.code/'src/main/resources';rows=[]
old=json.loads((legacy/'manifest.json').read_text());bindings={r['path']:r for r in old['files']}
for name,im in textures.items():
    relative='assets/zerog_tweaks/textures/block/transport/'+name+'.png'
    assert im.size==(32,32) and im.mode=='RGBA' and im.getbbox(),name
    if name.endswith('item_tube'):assert im.getextrema()[3]==(0,255) and 0<im.getpixel((10,24))[3]<128
    output=base/'source'/relative;output.parent.mkdir(parents=True,exist_ok=True);im.save(output)
    payload=output.read_bytes();sha=hashlib.sha256(payload).hexdigest()
    targets=[res/relative,legacy/'source'/relative]
    targets.extend(pack/relative for pack in (res/'resourcepacks').glob('*') if (pack/relative).exists())
    for target in targets:assert target.exists(),target;target.write_bytes(payload)
    row={'path':relative,'sha256':sha,'size':[32,32],'native_drawing':True}
    rows.append(row)
    bindings[relative].update(sha256=sha,size=[32,32],alpha_bounds=im.getbbox(),contract={'verified_uv_size':16,'native_size':32,'native_source':str(source.relative_to(base.parent.parent))})
    assert all(target.read_bytes()==payload for target in targets)
# Model/UV contract remains 0..16 regardless of raster resolution.
checked=0
for model in (res/'assets/zerog_tweaks/models/block/transport').glob('*.json'):
    obj=json.loads(model.read_text())
    if not any(str(t).split('/')[-1] in textures for t in obj.get('textures',{}).values()):continue
    for cube in obj.get('elements',[]):
        for face in cube.get('faces',{}).values():assert all(0<=v<=16 for v in face.get('uv',[0,0,16,16])),model
    checked+=1
assert checked>0
(legacy/'manifest.json').write_text(json.dumps(old,indent=2)+'\n')
manifest={'generator':str(Path(__file__).relative_to(base.parent.parent)),'source_generator':str(source.relative_to(base.parent.parent)),'original_art':True,'native_resolution':32,'uv_units':16,'models_checked':checked,'files':rows,'gpu_approved':False}
(base/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
gallery=Image.new('RGBA',(960,590),'#14232e');d=ImageDraw.Draw(gallery)
d.text((12,12),'ZeroG: native item-pipe frames / energy cells / real charge gauge — NOT a client render',fill='#dcecff')
for col,tier in enumerate(ctx['TIERS']):
    d.text((col*160+8,38),tier[1],fill='#dcecff')
    for row,suffix in enumerate(('item_tube','energy_cell_side','energy_cell_top')):
        im=textures[tier[0]+'_'+suffix];xx=col*160+16;yy=60+row*160
        d.rectangle((xx,yy,xx+127,yy+127),fill='#344654');gallery.alpha_composite(im.resize((128,128),Image.Resampling.NEAREST),(xx,yy))
    gallery.alpha_composite(textures['energy_cell_gauge_8'].resize((128,128),Image.Resampling.NEAREST),(col*160+16,220))
gallery.convert('RGB').save(base/'native-preview.png')
print(f'PASS: {len(rows)} native textures, {checked} unchanged model UV contracts, source/runtime/active-layer byte identity')
