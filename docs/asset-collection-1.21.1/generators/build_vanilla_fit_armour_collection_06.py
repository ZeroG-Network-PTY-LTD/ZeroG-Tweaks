"""Green-box vanilla fitting geometry; own ZeroG style textures, no Mojang pixels."""
import base64, copy, hashlib, io, json, math, uuid
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import build_armour_collection_02 as c

ROOT = c.ROOT
OUT = ROOT / 'outputs/ZeroG_Vanilla_Fit_Armour_06'
REF = ROOT / 'outputs/ZeroG_Armour_Vanilla_Reference_05/vanilla_trimmed_netherite_player.bbmodel'
ANIMATED = {'nullifite','moonsteel','cerulite','wraithsteel','eidolite','astrium','radiantine','solvanite'}

def tex_record(im, name, animated=False):
    raw=io.BytesIO();im.save(raw,format='PNG')
    t=c.texture_record(im,name)
    t.update(source='data:image/png;base64,'+base64.b64encode(raw.getvalue()).decode(),
             width=im.width,height=im.height,uv_width=256,uv_height=256)
    if animated:t.update(frame_time=4,frame_order_type='loop',frame_order='',frame_interpolate=False)
    return t

def paint(spec):
    name,shell,trim,light,theme=spec
    # Aurelion is gold in the newly supplied lineup, not pale ivory.
    if name=='Aurelion':shell,trim,light='#9d8a31','#d8c474','#fff4b5'
    metal=c.ramp(shell);edge=c.ramp(trim);shine=c.ramp(light)
    image=Image.new('RGBA',(256,256));glow=Image.new('RGBA',(256,256))
    draw=ImageDraw.Draw(image);gdraw=ImageDraw.Draw(glow)
    # Independently painted player study, not Minecraft's Steve texture.
    skin=c.ramp('#b98261');cloth=c.ramp('#263842');hair=c.ramp('#553825')
    draw.rectangle((0,0,127,127),fill=skin[2])
    for y in range(128):
        for x in range(128):
            if (x//2+y//2)%9==0:draw.point((x,y),fill=skin[1])
    # Vanilla-format head box UV; eyes and mouth are explicit on its front.
    draw.rectangle((0,0,63,15),fill=hair[2])
    draw.rectangle((0,16,15,31),fill=hair[2])
    draw.rectangle((32,16,63,31),fill=hair[2])
    draw.rectangle((16,16,31,18),fill=hair[2])
    for x in [19,27]:
        draw.rectangle((x,23,x+2,25),fill='#e7ecee');draw.rectangle((x+1,23,x+1,25),fill='#557484')
    draw.rectangle((22,29,26,30),fill='#744936')
    draw.rectangle((32,32,79,63),fill=cloth[2])
    # Player legs are dark fabric, arms remain exposed brown below shoulder cuffs.
    draw.rectangle((0,32,31,63),fill=cloth[1])
    draw.rectangle((32,96,63,127),fill=cloth[1])
    # Paint original 64x32 armour box-UV templates at 2px/unit.
    # Each face gets deliberate clusters, bevels and continuous local border trim.
    def face(rect,kind,layer,side='north'):
        x0,y0,x1,y1=rect
        x0*=2;x1*=2;y0=(y0+(64 if layer==1 else 96))*2;y1=(y1+(64 if layer==1 else 96))*2
        if x1<=x0 or y1<=y0:return
        draw.rectangle((x0,y0,x1-1,y1-1),fill=metal[2])
        w,h=x1-x0,y1-y0
        for y in range(y0,y1):
            for x in range(x0,x1):
                # Paired four-pixel clusters; no random white speckle noise.
                sx=min(x-x0,x1-1-x)
                value=(sx//2+(y-y0)//2*3)%11
                tone=metal[1] if value in [0,1] else (metal[3] if value==5 else metal[2])
                draw.point((x,y),fill=tone)
        draw.line((x0,y0,x1-1,y0),fill=metal[4])
        draw.line((x0,y1-1,x1-1,y1-1),fill=metal[0])
        draw.line((x0,y0,x0,y1-1),fill=metal[3])
        draw.line((x1-1,y0,x1-1,y1-1),fill=metal[0])
        if kind=='helmet' and side=='north':
            # Broad green-box face opening; neither mouth nor eyes covered.
            draw.rectangle((x0+2,y0+4,x1-3,y1-1),fill=(0,0,0,0))
            # Narrow central nasal ridge, stopping above the mouth.
            cx=(x0+x1)//2
            draw.rectangle((cx-1,y0+2,cx,y0+8),fill=edge[2])
            draw.line((x0+1,y0+2,x1-2,y0+2),fill=edge[4])
        elif kind=='arm' and side not in ['up','down']:
            # Vanilla-like upper-arm cuff, uncovered forearm and visible hand.
            cutoff=y0+10
            draw.rectangle((x0,cutoff,x1-1,y1-1),fill=(0,0,0,0))
            draw.line((x0,cutoff-2,x1-1,cutoff-2),fill=edge[3],width=2)
        elif kind=='arm' and side=='down':
            draw.rectangle((x0,y0,x1-1,y1-1),fill=(0,0,0,0))
        elif kind=='boot' and side not in ['up','down']:
            draw.rectangle((x0,y0,x1-1,y0+13),fill=(0,0,0,0))
            draw.line((x0,y0+14,x1-1,y0+14),fill=edge[3],width=2)
        elif kind=='boot' and side=='up':
            draw.rectangle((x0,y0,x1-1,y1-1),fill=(0,0,0,0))
        elif kind=='body' and side in ['north','south']:
            draw.line((x0+1,y0+2,x1-2,y0+2),fill=edge[3],width=2)
            draw.line((x0+1,y1-3,x1-2,y1-3),fill=edge[2],width=2)
            # A continuous yoke and vertical inlay, not a floating chest block.
            cx=(x0+x1)//2
            draw.line((cx,y0+5,cx,y1-4),fill=edge[1],width=2)
            if side=='north':
                draw.rectangle((cx-2,y0+7,cx+1,y0+10),fill=shine[2])
                gdraw.rectangle((cx-2,y0+7,cx+1,y0+10),fill=shine[2])
        elif kind=='leg' and side not in ['up','down']:
            draw.line((x0+1,y0+1,x1-2,y0+1),fill=edge[3],width=2)
            draw.line((x0+1,y0+12,x1-2,y0+12),fill=edge[2],width=2)
        # Subtle luminous paired trim fasteners use the supplied family light.
        if kind=='helmet' and side in ['east','west']:
            draw.rectangle((x0+3,y0+3,x0+4,y0+4),fill=shine[2])
            gdraw.rectangle((x0+3,y0+3,x0+4,y0+4),fill=shine[2])
        if theme in ['industrial','salvage'] and kind=='body' and side in ['east','west']:
            for y in range(y0+5,y1-3,4):draw.line((x0+2,y,x1-3,y),fill=metal[0])
        if kind=='body' and side in ['north','south']:
            # Material-specific surface vocabulary, not twenty palette swaps.
            cx=(x0+x1)//2
            if theme in ['aqua','deep_aqua','cold','mist']:
                for yy in [y0+14,y0+18]:
                    draw.line((x0+2,yy,cx-3,yy-2),fill=edge[2])
                    draw.line((cx+2,yy-2,x1-3,yy),fill=edge[2])
            elif theme in ['lunar','cobalt','silver']:
                for xx in [x0+3,x1-4]:
                    draw.line((xx,y0+7,xx,y0+15),fill=edge[2])
                    draw.point((xx,y0+17),fill=shine[3])
            elif theme in ['copper','rose','rust','forge']:
                for xx in [x0+3,x1-4]:
                    draw.rectangle((xx,y0+13,xx+1,y0+14),fill=metal[1])
                    draw.point((xx,y0+12),fill=edge[3])
            elif theme=='astral':
                for xx,yy in [(x0+3,y0+7),(x1-4,y0+14)]:
                    draw.line((xx-1,yy,xx+1,yy),fill=edge[3])
                    draw.line((xx,yy-1,xx,yy+1),fill=edge[3])
            elif theme in ['solar','radiant','gold','pale_gold','ivory']:
                for xx in [x0+3,x1-4]:
                    draw.line((xx,y0+14,xx,y0+19),fill=edge[3])
                    draw.point((xx,y0+12),fill=shine[3])
            elif theme=='violet':
                for xx in [x0+3,x1-4]:
                    draw.line((xx,y0+13,xx,y0+17),fill=edge[1])
                    draw.point((xx,y0+11),fill=edge[3])
    def box(uv, dims, kind, layer):
        u,v=uv;dx,dy,dz=dims
        maps={'north':[u+dz,v+dz,u+dz+dx,v+dz+dy],
              'south':[u+dz+dx+dz,v+dz,u+dz+dx+dz+dx,v+dz+dy],
              'west':[u,v+dz,u+dz,v+dz+dy],
              'east':[u+dz+dx,v+dz,u+dz+dx+dz,v+dz+dy],
              'up':[u+dz,v,u+dz+dx,v+dz],
              'down':[u+dz+dx,v,u+dz+dx+dx,v+dz]}
        for side,rect in maps.items():face(rect,kind,layer,side)
    box((0,0),(8,8,8),'helmet',1)
    box((16,16),(8,12,4),'body',1)
    box((40,16),(4,12,4),'arm',1)
    box((0,16),(4,12,4),'boot',1)
    box((16,16),(8,12,4),'body',2)
    box((0,16),(4,12,4),'leg',2)
    # Inner torso is largely hidden but remains independently mapped and solid.
    return image,glow

def build(spec):
    name=spec[0];key=name.lower();folder=OUT/key;folder.mkdir(parents=True,exist_ok=True)
    model=json.loads(REF.read_text())
    texture,glow=paint(spec)
    ids={}
    for e in model['elements']:ids[e['uuid']]=str(uuid.uuid5(uuid.NAMESPACE_URL,'zerog:green-fit:'+key+e['uuid']))
    for g in c.walk_groups(model['outliner']):ids[g['uuid']]=str(uuid.uuid5(uuid.NAMESPACE_URL,'zerog:green-fit:'+key+g['uuid']))
    for e in model['elements']:
        e['uuid']=ids[e['uuid']]
        is_skin=e['name'].startswith('vanilla_player_')
        e['name']=e['name'].replace('vanilla_player_', 'PLAYER_REFERENCE_').replace('netherite_', key+'_')
        e['export']=not is_skin
        # Retain the vanilla outer silhouette; only shorten hidden inner walls
        # which otherwise overlap at neutral leg spacing and z-fight.
        if not is_skin and e['name'].endswith(('leggings_right_leg','boots_right_leg')):
            e['to'][0]=-.05
        if not is_skin and e['name'].endswith(('leggings_left_leg','boots_left_leg')):
            e['from'][0]=.05
        faces={}
        for f,face in e['faces'].items():
            face['uv']=[v*2 for v in face['uv']]
            u,v,u1,v1=face['uv'];x0,x1=sorted((u,u1));y0,y1=sorted((v,v1))
            if texture.crop((x0,y0,x1,y1)).getbbox():faces[f]=face
        e['faces']=faces
    for g in c.walk_groups(model['outliner']):
        g['uuid']=ids[g['uuid']]
        g['children']=[ids[v] if isinstance(v,str) else v for v in g['children']]
        g['export']=True
        g['rotation']=[0,0,0]
    for clip in model.get('animations',[]):
        clip['uuid']=str(uuid.uuid5(uuid.NAMESPACE_URL,key+clip['uuid']))
        clip['name']=clip['name'].replace('vanilla_reference',key)
        clip['animators']={ids[k]:v for k,v in clip['animators'].items()}
    model.update(name=name+' — green-box vanilla fit / ZeroG texture 06',
         model_identifier='zerog_tweaks:'+key+'_armour', textures=[tex_record(texture,key+'_atlas_256.png')])
    model['design_notes']={'revision':'06 replaces orange-box geometry in active collection',
         'geometry':'User-approved vanilla-style green-box armour. No old visor cage, floating chest core, bracer stacks or pauldron blocks.',
         'player_reference':'Own procedural skin, not copied Steve art',
         'style_reference':'User supplied twenty-material lineup: palette, clustered metal shading, surface inlays and glow colours',
         'fit':'Vanilla six joints, zero neutral arm spread; outer 1.0, inner .5, boots .9, leggings .4',
         'medial_leg_clearance':'Hidden leg-shell walls trimmed to +/-0.05; outer silhouette preserved',
         'openings':'Transparent mouth/eye opening; forearms and hands exposed',
         'runtime':'Design study only; not equipped or tested in a Minecraft client',
         'effects':'No detached halo cubes. Dedicated glow mask for future renderer; Solvanite aura remains future work.'}
    path=folder/(key+'_player_fitted.bbmodel');path.write_text(json.dumps(model,indent=2))
    texture.save(folder/(key+'_atlas_256.png'));glow.save(folder/(key+'_glowmask_256.png'))
    validation=c.b.check(path)
    for view in ['front','threequarter']:
        c.b.render(model,(360,460),view=view).save(folder/(view+'.png'))
    if key in ANIMATED:
        frames=[];gf=[];array=np.array(texture);selected=np.array(glow)[:,:,3]>0
        for i in range(12):
            a=array.copy();a[selected,:3]=(a[selected,:3]*(.84+.16*math.cos(2*math.pi*i/12))).astype('uint8')
            assert np.array_equal(a[:,:,3],array[:,:,3])
            frames.append(Image.fromarray(a));mask=np.zeros_like(a);mask[selected]=a[selected];gf.append(Image.fromarray(mask))
        for suffix,images in [('flipbook_12',frames),('glowmask_flipbook_12',gf)]:
            strip=Image.new('RGBA',(256,3072))
            for i,f in enumerate(images):strip.paste(f,(0,i*256))
            strip.save(folder/(key+'_'+suffix+'.png'))
            (folder/(key+'_'+suffix+'.png.mcmeta')).write_text(json.dumps({'animation':{'width':256,'height':256,'frametime':4,'interpolate':False,'frames':list(range(12))}},indent=2))
            if suffix=='flipbook_12':
                animated=copy.deepcopy(model);animated['textures']=[tex_record(strip,key+'_'+suffix+'.png',True)]
                animated['name']=name+' — green-box fit / animated PNG preview'
                (folder/(key+'_animated_textures.bbmodel')).write_text(json.dumps(animated,indent=2))
        validation['animated_frames']=12
    validation['copied_mojang_pixels']=False
    (folder/'verification.json').write_text(json.dumps(validation,indent=2))
    print(name+': green-box geometry, one texture, independent ZeroG palette',flush=True)
    return model

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    models=[build(spec) for spec in c.SPECS]
    atlas=Image.new('RGBA',(2048,2048))
    showcase={'meta':models[0]['meta'],'name':'ZeroG — all 20 green-box vanilla-fit armours 06',
        'resolution':{'width':2048,'height':2048},'elements':[],'outliner':[],'animations':[]}
    for i,(spec,model) in enumerate(zip(c.SPECS,models)):
        ox,oy=(i%8)*256,(i//8)*256
        atlas.paste(Image.open(OUT/spec[0].lower()/(spec[0].lower()+'_atlas_256.png')),(ox,oy))
        dx,dz=(i%10)*24,(i//10)*28
        group=copy.deepcopy(model['outliner'][0]);group['name']=spec[0]
        for g in c.walk_groups([group]):g['origin'][0]+=dx;g['origin'][2]+=dz
        showcase['outliner'].append(group)
        for e in copy.deepcopy(model['elements']):
            for field in ['from','to','origin']:e[field][0]+=dx;e[field][2]+=dz
            for face in e['faces'].values():face['uv']=[v+(ox if n%2==0 else oy) for n,v in enumerate(face['uv'])]
            showcase['elements'].append(e)
    t=tex_record(atlas,'all_20_atlas.png');t.update(uv_width=2048,uv_height=2048)
    showcase['textures']=[t]
    path=OUT/'all_20_green_box_armour.bbmodel';path.write_text(json.dumps(showcase,separators=(',',':')))
    atlas.save(OUT/'all_20_atlas.png')
    c.b.check(path)
    lineup=Image.new('RGB',(1800,550),'#18202b');d=ImageDraw.Draw(lineup)
    for i,spec in enumerate(c.SPECS):
        pic=Image.open(OUT/spec[0].lower()/'threequarter.png').convert('RGB').resize((180,230))
        x=(i%10)*180;y=(i//10)*275
        lineup.paste(pic,(x,y+10));d.text((x+16,y+245),spec[0],fill='white')
    lineup.save(OUT/'lineup.png')
    (OUT/'README.md').write_text('# Green-box vanilla-fit armour — revision 06\n\nThe user explicitly replaced the orange-box custom silhouette with the green-box vanilla-fitting armour. All twenty sets use that fitting geometry and their own independently painted style palettes. Earlier orange-box files remain local backups and are excluded from the active collection.\n\nOne atlas per project; exposed forearms/hands and transparent eye/mouth opening. Classic vanilla pivots, zero neutral arm spread. Individual projects retain fit-check clips; eight include PNG pulse studies. Glow masks and texture animations require runtime renderers; no detached effect geometry or guaranteed in-game animation. No extracted Minecraft texture pixels are published.\n')
    print('All 20 replacement sets and single-atlas showcase completed.',flush=True)

if __name__=='__main__':main()
