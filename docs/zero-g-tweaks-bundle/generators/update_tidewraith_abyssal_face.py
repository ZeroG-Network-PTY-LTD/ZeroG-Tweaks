"""Face-only repair of the user-selected Abyssal project; never overwrite source.

Samples the Abyssal 16x12 front tile from the supplied four-style concept sheet.
No paid generation. All non-facial geometry/rigging/animation is preserved.
"""
import argparse
import base64
import copy
import hashlib
import io
import json
import math
import shutil
import uuid
from pathlib import Path

import numpy as np
from PIL import Image
from review_mob_assets import ROOT, image_from_model, render, check
from preview_mob_animation import rotation, translate, sample

OUT = ROOT/'docs/shattered-skies/abyssal-face-repair'
STEP_X = 11/16
STEP_Y = 8.2/12
FRONT_Z = -23.35
ATLAS_OFFSET = 3968
HEAD_SHIFT_Z = 2.25
FACE_PREFIXES = ('head_', 'jaw_', 'upper_tooth_', 'mouth_', 'eyes_', 'fin_', 'splinter_')


def uid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL,'zerog/abyssal-face-repair/'+name))


def write(path, data):
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')


def face_uv(lo, hi):
    return [(lo[0]+5.5)/STEP_X*8,(24.5-hi[1])/STEP_Y*8,
            (hi[0]+5.5)/STEP_X*8,(24.5-lo[1])/STEP_Y*8]


def face_texture(reference):
    image=Image.open(reference).convert('RGBA')
    assert image.size==(1568,583), 'Reference sheet dimensions changed; inspect crop first.'
    grid=Image.new('RGBA',(16,12))
    # Pixel CENTRES, not a scaled screenshot pasted wholesale. The exact crop
    # coordinates are recorded in the manifest; back/side details are untouched.
    for y in range(12):
        for x in range(16):
            grid.putpixel((x,y),image.getpixel((round(802+(x+.5)*175/16),round(401+(y+.5)*132/12))))
    base=grid.copy()
    atlas=Image.new('RGBA',(128,128))
    glow=Image.new('RGBA',atlas.size)
    for side,x0,dest_x in (('left',1,0),('right',11,32)):
        eye=grid.crop((x0,3,x0+4,6))
        for y in range(3):
            for x in range(4):
                r,g,b,a=eye.getpixel((x,y))
                if g>50 and b>70 and b>r*1.2 and g>r*1.7:
                    base.putpixel((x0+x,3+y),(13,21,39,255))
                else:eye.putpixel((x,y),(0,0,0,0))
        eye=eye.resize((32,24),Image.Resampling.NEAREST)
        atlas.paste(eye,(dest_x,96));glow.paste(eye,(dest_x,96))
    columns=(3,5,7,8,10,12)
    for i,column in enumerate(columns):
        tooth=grid.crop((column,8,column+1,10)).resize((8,16),Image.Resampling.NEAREST)
        atlas.paste(tooth,(80+8*i,96))
        for y in (8,9):base.putpixel((column,y),(3,5,9,255))
    atlas.paste(base.resize((128,96),Image.Resampling.NEAREST),(0,0))
    fin_colour=grid.getpixel((2,0))
    violet=grid.getpixel((8,0))
    for rect,colour in (((64,96,72,104),fin_colour),((72,96,80,104),violet)):
        atlas.paste(colour,rect)
    glow.paste(violet,(72,96,80,104))
    # Emissive stripe pixels only; not a whole glowing head.
    for y in range(4):
        for x in (7,8):
            r,g,b,a=grid.getpixel((x,y))
            if r>70 and b>r*1.2 and g<r:
                glow.paste((r,g,b,a),(x*8,y*8,(x+1)*8,(y+1)*8))
    return grid,atlas,glow


def replace_front(element, uv, all_faces=False):
    for face,data in element['faces'].items():
        if all_faces or face=='north':data.update(uv=[v+ATLAS_OFFSET for v in uv],texture=0,rotation=0)


def plane_faces(uv):
    return {f:{'uv':[v+ATLAS_OFFSET for v in uv],'texture':0,'rotation':0} for f in ('north','south')}


def set_bounds(element, lo, hi):
    element['from']=list(lo);element['to']=list(hi)
    element['origin']=[(a+b)/2 for a,b in zip(lo,hi)]


def repair(source, atlas):
    model=copy.deepcopy(source)
    model['name']='tidewraith_abyssal_concept_face'
    combined=image_from_model(source)
    assert combined.size==(4096,4096)
    # A single combined atlas avoids per-texture UV-size ambiguity in Blockbench
    # and GeckoLib. Reserve an unused corner; never overwrite another part's UV.
    for element in source['elements']:
        for face in element['faces'].values():
            u0,v0,u1,v1=face['uv']
            assert not (max(u0,u1)>ATLAS_OFFSET and max(v0,v1)>ATLAS_OFFSET), element['name']
    combined.paste(atlas,(ATLAS_OFFSET,ATLAS_OFFSET))
    buf=io.BytesIO();combined.save(buf,format='PNG')
    model['textures'][0].update(name='tidewraith_abyssal_concept_face.png',
                               path=str(OUT/'tidewraith_abyssal_concept_face.png'),
                               source='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode())
    nodes={}
    def walk(items):
        for n in items:
            if isinstance(n,dict):nodes[n['name']]=n;walk(n['children'])
    walk(model['outliner'])
    for e in model['elements']:
        name=e['name']
        if name.startswith(('head_05','head_brow','jaw_09')):replace_front(e,face_uv(e['from'],e['to']))
        if name.startswith('mouth_'):
            lo=[-4.125,24.5-11*STEP_Y,-23.32]
            hi=[4.125,24.5-7*STEP_Y,-23.32]
            set_bounds(e,lo,hi)
            uv=[16,56,112,88]
            e['faces']=plane_faces(uv)
            nodes['mouth']['origin']=[0,hi[1],-23.32]
        elif name.startswith('upper_tooth_'):
            label=name.split('_')[2]
            column={'l2':3,'l1':5,'l0':7,'r0':8,'r1':10,'r2':12}[label]
            slot=(3,5,7,8,10,12).index(column)
            lo=[-5.5+column*STEP_X,24.5-10*STEP_Y,FRONT_Z]
            hi=[lo[0]+STEP_X,24.5-8*STEP_Y,FRONT_Z]
            set_bounds(e,lo,hi)
            uv=[80+8*slot,96,88+8*slot,112]
            e['faces']=plane_faces(uv)
        elif name.startswith('jaw_lower_rim'):
            set_bounds(e,[-5.5,16.3,-23.34],[5.5,24.5-10*STEP_Y,-23.26])
            replace_front(e,[0,80,128,96])
        elif name.startswith('jaw_rim_corner'):
            left='_l_' in name
            xa,xb=(-5.5,-4.125) if left else (4.125,5.5)
            set_bounds(e,[xa,24.5-10*STEP_Y,-23.33],[xb,24.5-7*STEP_Y,-23.25])
            replace_front(e,face_uv(e['from'],e['to']))
        elif name.startswith('eyes_'):
            left=e['from'][0]<0
            x0=1 if left else 11
            lo=[-5.5+x0*STEP_X,24.5-6*STEP_Y,-23.40]
            hi=[lo[0]+4*STEP_X,24.5-3*STEP_Y,-23.40]
            set_bounds(e,lo,hi)
            uv=[0 if left else 32,96,32 if left else 64,120]
            e['faces']=plane_faces(uv)
            nodes['eye_'+name.split('_')[1]]['origin']=e['origin'].copy()
        elif name.startswith('fin_'):replace_front(e,[64,96,72,104],True)
        elif name.startswith('splinter_'):replace_front(e,[72,96,80,104],True)
    for clip in model['animations']:
        if not clip['name'].endswith('.mouth_open'):continue
        for animator in clip['animators'].values():
            for key in animator['keyframes']:
                point=key['data_points'][0]
                if animator['name']=='jaw':point['x']=-8 if key['time'] in (.2,.6) else 0
                elif animator['name']=='mouth':
                    key['channel']='scale'
                    # Keep the extended cavity above the lowered jaw's upper
                    # edge, rather than letting a black plane cover the lip.
                    point.update(x=1,y=1.12 if key['time'] in (.2,.6) else 1,z=1)
    # Close the original two-unit neck gap. All head descendants and pivots
    # move together, not just the visible face decal. Torso/wings remain fixed.
    head_members=set()
    def move_head(node):
        node['origin'][2]+=HEAD_SHIFT_Z
        for child in node['children']:
            if isinstance(child,str):head_members.add(child)
            else:move_head(child)
    move_head(nodes['head'])
    for e in model['elements']:
        if e['uuid'] in head_members:
            for field in ('from','to','origin'):e[field][2]+=HEAD_SHIFT_Z
    return model


def motion_preview(model, action):
    clip=next(a for a in model['animations'] if a['name'].endswith('.'+action))
    nodes={};members={}
    def walk(items,parent=None):
        for n in items:
            if isinstance(n,str):members[n]=parent
            else:nodes[n['uuid']]={**n,'parent':parent};walk(n['children'],n['uuid'])
    walk(model['outliner'])
    face=copy.deepcopy(model)
    face['elements']=[e for e in face['elements'] if e['name'].startswith(FACE_PREFIXES)]
    # Transparent preview-only anchor fixes the camera bounds across poses.
    # Never exported to the editable project; avoids apparent whole-face motion
    # from auto-fitting the view when the jaw lowers.
    empty=[ATLAS_OFFSET+120,ATLAS_OFFSET+120,ATLAS_OFFSET+121,ATLAS_OFFSET+121]
    face['elements'].append({'name':'preview_camera_bounds','uuid':uid('preview-camera'),
                             'from':[-8,15,FRONT_Z+HEAD_SHIFT_Z],
                             'to':[8,26.5,FRONT_Z+HEAD_SHIFT_Z],
                             'faces':{f:{'uv':empty,'texture':0} for f in ('north','south')}})
    frames=[]
    for frame in range(12):
        t=clip['length']*frame/12;matrices={}
        def matrix(key):
            if key is None:return np.eye(4)
            if key not in matrices:
                node=nodes[key];keys=clip['animators'].get(key,{}).get('keyframes',[])
                pos=sample([k for k in keys if k['channel']=='position'],t,[0,0,0])
                rot=sample([k for k in keys if k['channel']=='rotation'],t,[0,0,0])+np.array(node.get('rotation',[0,0,0]))
                scale=sample([k for k in keys if k['channel']=='scale'],t,[1,1,1]);p=np.array(node['origin'])
                matrices[key]=matrix(node['parent'])@translate(p+pos)@rotation(rot)@np.diag([*scale,1])@translate(-p)
            return matrices[key]
        frames.append(render(face,(480,400),view='front',vertex_transform=lambda e,p:p if e['name']=='preview_camera_bounds' else (matrix(members[e['uuid']])@np.array([*p,1]))[:3].tolist()).convert('RGB'))
    frames[0].save(OUT/f'{action}.gif',save_all=True,append_images=frames[1:],duration=round(clip['length']*1000/12),loop=0)


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--reference',type=Path,required=True);args=p.parse_args()
    original=args.source.read_bytes();source=json.loads(original)
    assert source['name']=='tidewraith_abyssal' and len(source['textures'])==1
    OUT.mkdir(parents=True,exist_ok=True)
    shutil.copy2(args.source,OUT/'source_model.bbmodel');shutil.copy2(args.reference,OUT/'face_concept.png')
    grid,atlas,glow=face_texture(args.reference)
    grid.resize((640,480),Image.Resampling.NEAREST).save(OUT/'reference_face_pixels.png')
    atlas.save(OUT/'tidewraith_abyssal_face.png');glow.save(OUT/'tidewraith_abyssal_face_glowmask.png')
    model=repair(source,atlas)
    image_from_model(model).save(OUT/'tidewraith_abyssal_concept_face.png')
    full_glow=Image.new('RGBA',(4096,4096));full_glow.paste(glow,(ATLAS_OFFSET,ATLAS_OFFSET))
    full_glow.save(OUT/'tidewraith_abyssal_concept_face_glowmask.png')
    # Keep the original body texture bytes and all non-facial geometry exactly.
    png=base64.b64decode(source['textures'][0]['source'].split(',',1)[1])
    (OUT/'tidewraith_abyssal_body.png').write_bytes(png)
    for before,after in zip(source['elements'],model['elements']):
        if not before['name'].startswith(FACE_PREFIXES):assert before==after,before['name']
    for a,b in zip(source['animations'],model['animations']):
        if not a['name'].endswith('.mouth_open'):assert a==b,a['name']
    for prefix in ('wing','tail','tendril','gill','body','keel','rib'):
        assert [e for e in source['elements'] if e['name'].startswith(prefix)]==[e for e in model['elements'] if e['name'].startswith(prefix)],prefix
    torso=next(e for e in model['elements'] if e['name']=='body_00')
    head=next(e for e in model['elements'] if e['name']=='head_05')
    overlap=head['to'][2]-torso['from'][2]
    assert abs(overlap-.25)<1e-6,('head/torso overlap',overlap)
    path=OUT/'tidewraith_abyssal_concept_face.bbmodel';write(path,model)
    result=check(path)
    for view in ('front','threequarter','right'):
        render(model,(900,700),view=view).save(OUT/f'updated_{view}.png')
        render(source,(900,700),view=view).save(OUT/f'before_{view}.png')
    face=copy.deepcopy(model);face['elements']=[e for e in model['elements'] if e['name'].startswith(FACE_PREFIXES)]
    debug={};render(face,(720,560),view='front',debug=debug).save(OUT/'face_closeup.png')
    eyes={e['name']:debug['visible_pixels'].get(e['name'],0) for e in face['elements'] if e['name'].startswith('eyes_')}
    assert len(eyes)==2 and all(eyes.values()),eyes
    for action in ('blink','mouth_open'):motion_preview(model,action)
    (OUT/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>Abyssal face and head joint</title><style>body{background:#19222c;color:#e3f4ff;font:16px system-ui;margin:24px}img{max-width:48%;image-rendering:pixelated}a{color:#92e9ff}</style><h1>Selected Abyssal model: concept face and closed head joint</h1><p>Original body, wings and tendrils preserved. Original file untouched. Head moved 2.25 units toward torso, with 0.25-unit overlap. Software views, not native/in-game captures.</p><p><a href="tidewraith_abyssal_concept_face.bbmodel">Updated Blockbench project</a> · <a href="README.md">Details</a></p><h2>Reference pixels and new face</h2><img src="reference_face_pixels.png"><img src="face_closeup.png"><h2>Before / after</h2><img src="before_threequarter.png"><img src="updated_threequarter.png"><h2>Head joint in profile</h2><img src="before_right.png"><img src="updated_right.png"><h2>Blink / mouth opening</h2><img src="blink.gif"><img src="mouth_open.gif"><p>Animate → select blink or mouth_open → Play.</p>',encoding='utf-8')
    assert args.source.read_bytes()==original,'Source was modified.'
    write(OUT/'manifest.json',{'source_sha256':hashlib.sha256(original).hexdigest(),'source_preserved':True,
                             'reference_sha256':hashlib.sha256(args.reference.read_bytes()).hexdigest(),
                             'reference_tile':{'origin':[802,401],'size':[175,132],'sample_grid':[16,12]},
                             'prompt':'Face only: match the supplied Abyssal face tile, cyan diagonal eyes, violet central splinter, dark rectangular tooth mouth. Preserve original Phantom body and non-facial rigging.',
                             'negative_prompt':'No eight-eye oval manta face; no body/wings/tendrils replacement; no duplicate painted eyes behind animated eyes.',
                             'provider':None,'paid_calls':0,'validation':result,'eye_visible_pixels':eyes,
                             'non_facial_geometry_preserved':True,'non_mouth_clips_preserved':True,
                             'head_shift_z_units':HEAD_SHIFT_Z,'head_torso_overlap_units':overlap,
                             'native_import_verified':False,'runtime_verified':False,
                             'files':{q.name:hashlib.sha256(q.read_bytes()).hexdigest() for q in OUT.iterdir() if q.is_file() and q.name!='manifest.json'}})
    print(json.dumps({'model':str(path),'validation':'PASS','eyes':eyes,'original':'PRESERVED'}),flush=True)


if __name__=='__main__':main()
