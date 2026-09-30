"""Concept-first Tidewraith rebuild. Smaller connected cuboids, not slab masses.

This supersedes the rejected micro study visually, without deleting its source.
32x32 shared UVs remain; prior table proportions are intentionally superseded.
"""
import argparse
import base64
import copy
import hashlib
import io
import json
import math
from pathlib import Path

import build_tidewraith_micro as codec
from PIL import Image
from review_mob_assets import check, render

ROOT = codec.ROOT
OUT = ROOT/'docs/shattered-skies/tidewraith-concept'
CONCEPT = ROOT/'docs/zero-g-tweaks-bundle/blockbench/references/codex-clipboard-3c2846ca-efea-4721-9c8c-b0880468c70a.png'
SHEET = codec.REFERENCE
FACTOR = .1  # Authored span 80 units -> 8 units (half a block).
BODY_RX = 16
BODY_RZ = 19
BODY_CZ = 5
FLIGHT_PERIOD = round(360/7.448451/20, 3)  # Prior Phantom-inspired cadence.
OUTER_WING_AMPLITUDE = 3.0
TIP_WING_AMPLITUDE = 4.0
TOOTH_Z = -12.72  # 0.02 in front of the blue gum band's z=-12.7 face.


def wing_roof(x):
    """Drooping manta/Phantom-style distal profile, in authored coordinates."""
    u = max(0, min(1, (x-12)/28))
    return 26-2.2*math.sin(math.pi*u)-8*u**3
PALETTES = {
    'standard': ['#041b24', '#07383d', '#0e5558', '#1b7e80', '#39adaa', '#7fe0d4', '#baffed', '#326c9e', '#5395ca'],
    'abyssal': ['#060f21', '#122a3b', '#1b465a', '#32748e', '#52a6c5', '#82d5e9', '#c4f7ff', '#3b537f', '#647aaf'],
    'pearl': ['#304956', '#547c87', '#82a9af', '#b3d9d6', '#bbefdf', '#d4fcef', '#f2fff9', '#779bb7', '#abc9e0'],
    'storm': ['#111e2b', '#234151', '#356477', '#52899e', '#75bdd6', '#a6e6f3', '#e4fcff', '#536798', '#788aba'],
}
UV = {'wing_top': [0, 0, 16, 8], 'wing_bottom': [0, 9, 16, 17],
      'skin': [16, 0, 24, 8], 'belly': [16, 9, 24, 17],
      'lobe': [24, 0, 32, 8], 'tentacle': [24, 9, 32, 17],
      'dark': [0, 20, 8, 24], 'blue': [8, 20, 16, 24],
      'teal': [16, 20, 24, 24],
      'mint': [24, 24, 28, 25], 'cyan': [24, 25, 28, 26],
      'white': [29, 24, 31, 26], 'eye': [30, 30, 32, 32],
      'tip': [24, 30, 28, 32], 'tooth': [24, 27, 27, 29]}
GLOW = {'mint', 'cyan', 'white', 'eye', 'tip', 'tooth'}
GUIDES = ['https://blockbench.net/wiki/guides/minecraft-style-guide/',
          'https://blockbench.net/wiki/guides/blockbench-overview-tips/']


def uid(name):
    return codec.uid('concept-rebuild/'+name)


def textures(palette):
    base = Image.new('RGBA', (32, 32)); glow = Image.new('RGBA', (32, 32))
    colours = [tuple(bytes.fromhex(c[1:]))+(255,) for c in palette]
    wing = ['3322223332223445', '2100233202233304', '2110033323300234',
            '2320032332000324', '3321033332310334', '2322302333212334',
            '3233332332333334', '3444443444344445']
    skin = ['21122212', '12232321', '22322232', '23211223',
            '22233232', '23322322', '22322232', '12222221']
    for name, rect in UV.items():
        x0, y0, x1, y1 = rect
        for y in range(y1-y0):
            for x in range(x1-x0):
                if name == 'wing_top': tone = int(wing[y][x])
                elif name == 'wing_bottom': tone = 1 if x < 4 and y in (1, 3, 5) else 2+(x+y in (8, 13))
                elif name == 'skin': tone = int(skin[y][x])
                elif name == 'belly': tone = 1 if y in (1, 3, 5, 7) and x in (1, 2, 5, 6) else 2
                elif name == 'lobe': tone = 3 if (x+y//2) % 3 else 1
                elif name == 'tentacle': tone = 3 if (x//2+y)%4 in (0, 1) else 1
                elif name == 'dark': tone = 0
                elif name == 'blue': tone = 7 if y < 2 else 8
                elif name == 'teal': tone = 3 if y < 2 else 4
                elif name == 'mint': tone = 5 if y else 6
                elif name == 'cyan': tone = 4 if y else 5
                elif name == 'white': tone = 6
                elif name == 'eye': tone = 6 if (x, y) == (0, 0) else 5
                elif name == 'tooth':
                    # Plane/alpha silhouette: broad root, narrow pixel tip.
                    # Transparent pixels are transparent in BOTH base and glow.
                    if y==1 and x!=1: continue
                    tone=6 if y==0 else 5
                else: tone = min(6, 3+x)
                base.putpixel((x+x0, y+y0), colours[tone])
                if name in GLOW: glow.putpixel((x+x0, y+y0), colours[tone])
    return base, glow


def geometry():
    elements, bones, parents = [], {}, {}

    def bone(name, parent, pivot):
        bones[name] = {'name': name, 'uuid': uid('bone/'+name), 'origin': list(pivot),
                       'rotation': [0, 0, 0], 'children': [], 'export': True, 'visibility': True}
        parents[name] = parent

    def box(name, group, lo, hi, kind='skin', custom=None):
        faces = {f: list(UV[kind]) for f in ('north', 'south', 'east', 'west', 'up', 'down')}
        if kind == 'skin':
            # Continuous global UVs, not an entire texture repeated per voxel.
            def interval(a, b, extent):
                if b <= 0: a, b = abs(a), abs(b)
                elif a < 0: a, b = 0, max(abs(a), b)
                return 16+8*a/extent, 16+8*b/extent
            u0, u1 = interval(lo[0], hi[0], BODY_RX)
            v0, v1 = 8*(34-hi[1])/20, 8*(34-lo[1])/20
            z0, z1 = 8*(BODY_CZ+BODY_RZ-hi[2])/(2*BODY_RZ), 8*(BODY_CZ+BODY_RZ-lo[2])/(2*BODY_RZ)
            def bounded(values):
                result = [max(16, min(24, values[0])), max(0, min(8, values[1])),
                          max(16, min(24, values[2])), max(0, min(8, values[3]))]
                if abs(result[0]-result[2]) < .001: result[2] = min(24, result[0]+.1); result[0] = max(16, result[2]-.1)
                if abs(result[1]-result[3]) < .001: result[3] = min(8, result[1]+.1); result[1] = max(0, result[3]-.1)
                return result
            faces['north'] = faces['south'] = bounded([u0, v0, u1, v1])
            faces['up'] = bounded([u0, z0, u1, z1])
            faces['east'] = faces['west'] = bounded([16+z0, v0, 16+z1, v1])
            faces['down'] = list(UV['belly'])
        if custom: faces.update(custom)
        element = {'name': name, 'type': 'cube', 'uuid': uid('cube/'+name), 'from': list(lo), 'to': list(hi),
                   'origin': list(bones[group]['origin']), 'rotation': [0, 0, 0], 'box_uv': False,
                   'faces': {f: {'uv': uv, 'texture': 0, 'rotation': 0} for f, uv in faces.items()}}
        if lo[2] == hi[2]: element['faces'] = {f: element['faces'][f] for f in ('north', 'south')}
        elements.append(element); bones[group]['children'].append(element['uuid'])

    bone('root', None, [0, 0, 0]); bone('body_main', 'root', [0, 24, 0])
    bone('head', 'body_main', [0, 24, -9]); bone('mouth', 'head', [0, 22, -12])
    bone('jaw_upper', 'mouth', [0, 26.5, TOOTH_Z]); bone('jaw_lower', 'mouth', [0, 17.5, TOOTH_Z])
    bone('tail_base', 'body_main', [0, 16, 6])

    # Closed elongated manta volume. The original z<-4 carve removed the cheek
    # beside the mouth. Limit the recess to the FRONT and terminate it at the
    # dark throat; do not cut a hole through the flanks or belly.
    inside = set()
    for x in range(-BODY_RX, BODY_RX):
        for y in range(14, 34):
            for z in range(BODY_CZ-BODY_RZ, BODY_CZ+BODY_RZ):
                if ((x+.5)/BODY_RX)**2+((y+.5-24)/10)**2+((z+.5-BODY_CZ)/BODY_RZ)**2 <= 1:
                    inside.add((x, y, z))
    solid={p for p in inside if not (p[2] < -10 and ((p[0]+.5)/10.0)**2+((p[1]+.5-22)/5.4)**2 < 1)}
    boundary=set()
    for x,y,z in solid:
        if not all((x+dx,y+dy,z+dz) in solid for dx,dy,dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))):
            boundary.add((x,y,z))
    for x, y, z in sorted(boundary):
        box(f'dome_{x}_{y}_{z}', 'body_main', [x, y, z], [x+1, y+1, z+1])
    # Fill hidden interior runs, preserving small exterior blocks. This prevents
    # a side-view ray finding an empty torso through any small join mismatch.
    interior=solid-boundary
    for x in range(-BODY_RX,BODY_RX):
        for y in range(14,34):
            zs=sorted(z for xx,yy,z in interior if xx==x and yy==y)
            if not zs:continue
            start=last=zs[0]
            for z in zs[1:]+[zs[-1]+2]:
                if z==last+1:last=z;continue
                box(f'body_fill_{x}_{y}_{start}','body_main',[x,y,start],[x+1,y+1,last+1])
                start=last=z

    # Elliptical concentric mouth rings: each inner band recedes towards throat.
    def ring(name, rx, ry, inner_x, inner_y, z, kind, thickness=.65, step=.7, group='mouth'):
        n = math.ceil(rx/step)
        m = math.ceil(ry/step)
        for i in range(-n, n):
            for j in range(-m, m):
                x, y = (i+.5)*step, (j+.5)*step
                if (x/rx)**2+(y/ry)**2 <= 1 and (x/inner_x)**2+(y/inner_y)**2 >= 1:
                    box(f'{name}_{i}_{j}', group, [i*step,22+j*step,z], [(i+1)*step,22+(j+1)*step,z+thickness], kind)
    # The socket connects the projecting rim to the dome, including its unseen
    # side walls. Without this collar the ring floats visibly in a side view.
    # Fixed collar belongs to the head. The rim, throat and BOTH tooth rows
    # share the mouth control; do not rotate unattached tooth rows independently.
    ring('mouth_socket', 12.1, 7.8, 10.0, 5.5, -13.6, 'skin', thickness=6, group='head')
    ring('mouth_outer', 11.2, 7.0, 9.9, 5.8, -14.2, 'mint')
    ring('mouth_teal', 9.9, 5.8, 9.0, 4.8, -13.5, 'teal')
    ring('mouth_blue', 9.0, 4.8, 8.1, 3.9, -12.7, 'blue')
    ring('mouth_inner', 8.1, 3.9, 6.9, 2.9, -11.8, 'cyan')
    for i in range(-7, 7):
        for j in range(-4, 4):
            if ((i+.5)/7.2)**2+((j+.5)/3.5)**2 <= 1:
                box(f'throat_{i}_{j}', 'mouth', [i,22+j,-10.1], [i+1,23+j,-9.7], 'dark')
    def gum_y(x, desired_y):
        # The voxel ring is not a continuous mathematical ellipse. Seat the
        # root on its ACTUAL band tile, not in a small stair-step gap beside it.
        candidates=[e for e in elements if e['name'].startswith('mouth_blue')
                    and e['from'][0]-1e-6<=x<=e['to'][0]+1e-6]
        values=[max(e['from'][1]+.01,min(e['to'][1]-.01,desired_y)) for e in candidates]
        assert values, ('tooth requires gum support',x)
        return min(values,key=lambda y:abs(y-desired_y))
    for i, x in enumerate(range(-7, 8)):
        curve = math.sqrt(max(0, 1-(x/8.4)**2))
        upper_y = gum_y(x,22+4.65*curve)
        box(f'upper_tooth_{i}', 'jaw_upper', [x-.26, upper_y-1.4, TOOTH_Z], [x+.26, upper_y, TOOTH_Z], 'tooth')
        lower_y = gum_y(x,22-4.25*curve)
        reversed_uv=[UV['tooth'][0],UV['tooth'][3],UV['tooth'][2],UV['tooth'][1]]
        box(f'lower_tooth_{i}', 'jaw_lower', [x-.23, lower_y, TOOTH_Z], [x+.23, lower_y+.7, TOOTH_Z],
            'tooth',custom={'north':reversed_uv,'south':reversed_uv})

    # Full-thickness wing fan with downward-curled distal sections. Two child
    # hinges give the tips a delayed response instead of one rigid wing slab.
    for side, label in ((1, 'left'), (-1, 'right')):
        bone('wing_'+label, 'body_main', [side*12, 26, 1])
        bone('wing_'+label+'_outer', 'wing_'+label, [side*28, wing_roof(28)-1, 2+3*16/28])
        bone('wing_'+label+'_tip', 'wing_'+label+'_outer', [side*35, wing_roof(35)-.8, 2+3*23/28])
        for x in range(12, 40):
            u = (x+.5-12)/28
            centre_y = wing_roof(x+.5)
            previous_y = wing_roof(x-.5)
            depth = 12-7*u
            centre_z = 2+3*u
            low_z, high_z = centre_z-depth/2, centre_z+depth/2
            for index in range(math.ceil(depth/2)):
                za, zb = low_z+2*index, min(high_z, low_z+2*(index+1))
                if zb <= za: continue
                v = (index+.5)*2/depth
                y = centre_y-.7*(2*v-1)**2
                thick = 2.8-1.5*u
                xa, xb = (x, x+1) if side > 0 else (-x-1, -x)
                uv = [16*(x-12)/28, 8*(za-low_z)/depth, 16*(x+1-12)/28, 8*(zb-low_z)/depth]
                if side < 0: uv = [uv[2], uv[1], uv[0], uv[3]]
                bottom = [uv[0], 9+uv[1], uv[2], 9+uv[3]]
                group = 'wing_'+label+('_tip' if x>=35 else '_outer' if x >= 28 else '')
                # Adjacent thick columns overlap across the downward curve.
                bottom_y = min(y-thick, previous_y-.7*(2*v-1)**2-.2)
                box(f'wing_{label}_{x}_{index}', group, [xa,bottom_y,za], [xb,y,zb], 'teal',
                    custom={'up':uv, 'down':bottom})
                if index == 0:
                    box(f'wing_trim_{label}_{x}', group, [xa,y-.25,za-.08], [xb,y+.08,za+.2], 'cyan' if x>=36 else 'teal')
                if x >= 38:
                    box(f'wing_tip_{label}_{x}_{index}', group, [xa,bottom_y,za], [xb,y+.02,zb], 'mint')
                if x in (27,34):
                    # Rounded/thickened hinge cover bridges the two separately
                    # moving bone groups instead of exposing a slit on a flap.
                    hinge=x+1
                    ha,hb=(hinge-.35,hinge+.35) if side>0 else (-hinge-.35,-hinge+.35)
                    cover_group='wing_'+label+('_outer' if x==34 else '')
                    box(f'wing_hinge_{label}_{hinge}_{index}',cover_group,[ha,bottom_y-.12,za-.05],
                        [hb,y+.12,zb+.05],'teal',custom={'up':uv,'down':bottom})

    def tube(name, group, path, width, kind='lobe', glowing_tip=False):
        counter = 0
        for index, (a, b) in enumerate(zip(path, path[1:])):
            distance = math.dist(a, b)
            samples = max(1, math.ceil(distance/.7))
            for i in range(samples+1):
                t = i/samples
                p = [a[j]*(1-t)+b[j]*t for j in range(3)]
                progress = (index+t)/(len(path)-1)
                radius = width*(1-.36*progress)/2
                material = 'tip' if glowing_tip and progress > .91 else kind
                box(f'{name}_{counter}', group, [v-radius for v in p], [v+radius for v in p], material)
                counter += 1

    # Inward-curled cephalic lobes, not two rectangular horns.
    for side, label in ((1,'left'),(-1,'right')):
        bone('lobe_'+label, 'head', [side*12, 25, -11])
        path = [[side*x,y,z] for x,y,z in ((12,25,-11),(14,23,-12),(15,19,-13),
                (15,15,-13.5),(14,12,-14),(11.5,11.5,-14.7),(9.5,13,-15),(9.5,15,-14.5))]
        tube('lobe_'+label,'lobe_'+label,path,3.2,'lobe',True)

    # Four long curves, each with FIVE true parented articulation segments.
    for number, (side, outer) in enumerate(((-1,False),(1,False),(-1,True),(1,True)), 1):
        raw = ((2,15,4),(3,11,5),(4,6,4),(5,1,1),(8,-2,-4),(12,0,-8)) if not outer else \
              ((6,14,3),(8,10,3),(9,6,1),(10,2,-2),(13,-1,-8),(17,2,-12))
        path = [[side*x,y,z] for x,y,z in raw]
        a=path[0]
        box(f'tentacle_mount_{number}','tail_base',[a[0]-.9,a[1]-.15,a[2]-.9],
            [a[0]+.9,16.8,a[2]+.9],'skin')
        parent = 'tail_base'
        for segment, (a, b) in enumerate(zip(path,path[1:]), 1):
            name = f'tentacle_{number}'+('' if segment==1 else f'_seg{segment}')
            bone(name,parent,a)
            tube(name,name,[a,b],1.7-.16*(segment-1),'tentacle',segment==5)
            parent = name

    # Eyes sit ON the exposed voxel surface; derive front Z from the actual shell
    # to avoid the earlier floating/occluded eye placement errors.
    for pair, (x,y) in enumerate(((3,31.5),(6.5,30.1),(9.6,28.8),(11.8,27.7))):
        for side,label in ((1,'left'),(-1,'right')):
            eye_x = side*x
            candidates = [e['from'][2] for e in elements if e['name'].startswith('dome_')
                          and e['from'][0] <= eye_x <= e['to'][0] and e['from'][1] <= y <= e['to'][1]]
            assert candidates, ('eye must have supporting dome', eye_x,y)
            z = min(candidates)-.05
            name = f'eye_{pair}_{label}'
            bone(name,'head',[eye_x,y,z])
            box(name,name,[eye_x-.62,y-.47,z],[eye_x+.62,y+.47,z],'eye')

    for name,parent in parents.items():
        if parent: bones[parent]['children'].append(bones[name])
    return elements, [bones['root']], bones, parents


def animations(bones):
    clips, exported = codec.animations(bones)
    for clip in clips:
        clip['name'] = clip['name'].replace('tidewraith_micro','tidewraith_concept')
        action = clip['name'].split('.')[-1]
        if action=='mouth_open':
            # A soft suction/open-close motion suits the oval manta mouth.
            # One shared deformation preserves tooth-root/rim alignment. Jaw
            # bones remain independently selectable but have no stray rotation.
            clip['length']=1.6
            keys=[]
            for i in range(33):
                opening=math.sin(math.pi*i/32)**2
                values=[1+.025*opening,1+.14*opening,1]
                keys.append({'channel':'scale','data_points':[dict(zip(('x','y','z'),values))],
                             'uuid':uid(f'mouth_open/mouth/{i}'),'time':round(1.6*i/32,4),
                             'color':-1,'interpolation':'linear'})
            clip['animators']={bones['mouth']['uuid']:{'name':'mouth','type':'bone','keyframes':keys}}
        if action not in ('idle','fly','glide'): continue
        old_length=clip['length']
        clip['length']=FLIGHT_PERIOD if action=='fly' else 4.0
        length = clip['length']
        for animator in clip['animators'].values():
            for key in animator['keyframes']:key['time']=round(key['time']*length/old_length,4)
        def set_rotation(name,axis,amplitude,phase=0):
            keys=[]
            for i in range(33):
                values=[0,0,0]; values[axis]=amplitude*math.cos(i/32*math.tau-phase)
                keys.append({'channel':'rotation','data_points':[dict(zip(('x','y','z'),values))],
                             'uuid':uid(f'{action}/{name}/{i}'),'time':round(length*i/32,4),
                             'color':-1,'interpolation':'linear'})
            clip['animators'][bones[name]['uuid']]={'name':name,'type':'bone','keyframes':keys}
        for name,side in (('wing_left',1),('wing_right',-1)):
            set_rotation(name,2,side*(6 if action=='fly' else 2 if action=='idle' else .75))
        for number in range(1,5):
            set_rotation(f'tentacle_{number}',0,2,number*.35)
        for name in bones:
            if '_seg' not in name and not name.endswith(('_outer','_tip')) and not name.startswith('lobe_'): continue
            side = -1 if ('right' in name) else 1
            if '_seg' in name:
                segment = int(name.rsplit('seg',1)[1]); axis, amplitude, phase = 0, 1.5/math.sqrt(segment), segment*.35
            elif name.endswith('_outer'): axis, amplitude, phase = 2, side*(OUTER_WING_AMPLITUDE if action=='fly' else 1 if action=='idle' else .5), .4
            elif name.endswith('_tip'): axis, amplitude, phase = 2, side*(TIP_WING_AMPLITUDE if action=='fly' else 1.5 if action=='idle' else .75), .8
            else: axis, amplitude, phase = 2, side*.75, .2
            set_rotation(name,axis,amplitude,phase)
    result={}
    for clip in clips:
        channels={}
        for animator in clip['animators'].values():
            entry=channels.setdefault(animator['name'],{})
            for key in animator['keyframes']:
                entry.setdefault(key['channel'],{})[str(key['time'])]=[key['data_points'][0][axis] for axis in ('x','y','z')]
        result[clip['name']]={'loop':clip['loop']=='loop','animation_length':clip['length'],'bones':channels}
    return clips, {'format_version':'1.8.0','animations':result}


def validate(model,path,bones):
    result=check(path)
    assert result['texture']==[32,32]
    assert len([n for n in bones if n.startswith('eye_')])==8
    assert len([n for n in bones if n.startswith('tentacle_')])==20
    lookup={e['name']:e for e in model['elements']}
    for element in model['elements']:
        name=element['name']
        target=name.replace('left','right') if 'left' in name else None
        if target and target in lookup:
            mirrored=lookup[target]
            assert abs(element['from'][0]+mirrored['to'][0])<1e-6, name
            assert abs(element['to'][0]+mirrored['from'][0])<1e-6, name
            assert element['from'][1:]==mirrored['from'][1:],name
            assert element['to'][1:]==mirrored['to'][1:],name
    debug={}
    front=render(model,(720,560),view='front',debug=debug)
    front.save(OUT/'previews'/f'{path.stem}_front.png')
    counts={name:debug['visible_pixels'].get(name,0) for name in lookup if name.startswith('eye_')}
    assert all(counts.values()), ('occluded eyes',counts)
    result.update({'eye_visible_pixels':counts,'bilateral_parts':'PASS','articulated_tentacles':4,
                   'segments_per_tentacle':5,'reference_appearance_approved':False})
    return result


def animation_preview(model, action='fly', view='threequarter'):
    """Actual numeric clip playback; no GPU/emissive/in-game claim."""
    import numpy as np
    from preview_mob_animation import rotation, translate, sample
    clip=next(a for a in model['animations'] if a['name'].endswith('.'+action))
    bones={};members={}
    def walk(nodes,parent=None):
        for node in nodes:
            if isinstance(node,str): members[node]=parent
            else: bones[node['uuid']]={**node,'parent':parent};walk(node['children'],node['uuid'])
    walk(model['outliner'])
    frames=[]
    for frame in range(16):
        t=frame*clip['length']/16; matrices={}
        def matrix(key):
            if key is None:return np.eye(4)
            if key not in matrices:
                b=bones[key];keys=clip['animators'].get(key,{}).get('keyframes',[])
                rot=sample([k for k in keys if k['channel']=='rotation'],t,[0,0,0])
                pos=sample([k for k in keys if k['channel']=='position'],t,[0,0,0])
                scale=sample([k for k in keys if k['channel']=='scale'],t,[1,1,1])
                p=np.array(b['origin'])
                matrices[key]=matrix(b['parent'])@translate(p+pos)@rotation(rot)@np.diag([*scale,1])@translate(-p)
                assert np.isfinite(matrices[key]).all()
            return matrices[key]
        def vertex(cube,p):return (matrix(members[cube['uuid']])@np.array([*p,1]))[:3].tolist()
        frames.append(render(model,(480,400),vertex_transform=vertex,view=view).convert('RGB'))
    frames[0].save(OUT/f'previews/{action}.gif',save_all=True,append_images=frames[1:],
                   duration=round(clip['length']*1000/16),loop=0)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--all',action='store_true')
    parser.add_argument('--resume',action='store_true',help='Reuse completed previews only when their model is exactly current and they postdate it; rerun all validations.')
    args=parser.parse_args()
    (OUT/'previews').mkdir(parents=True,exist_ok=True)
    assert CONCEPT.exists() and SHEET.exists()
    codec.FACTOR=FACTOR
    elements,outliner,bones,parents=geometry()
    clips,anim=animations(bones)
    for scaled in (False,True):
        name='tidewraith_concept'+('_scaled' if scaled else '')
        geo=codec.export_geo(elements,bones,parents,scaled)
        geo['minecraft:geometry'][0]['description'].update({
            'identifier':'geometry.shatteredskies.'+name,'visible_bounds_width':6*(FACTOR if scaled else 1),
            'visible_bounds_height':4*(FACTOR if scaled else 1),
            'visible_bounds_offset':[0,1*(FACTOR if scaled else 1),0]})
        codec.write(OUT/f'{name}.geo.json',geo)
        exported=copy.deepcopy(anim)
        if scaled:
            for clip in exported['animations'].values():
                for entry in clip['bones'].values():
                    for t,v in entry.get('position',{}).items(): entry['position'][t]=[n*FACTOR for n in v]
        codec.write(OUT/f'{name}.animation.json',exported)
    reports=[];cards=[]
    for style,palette in PALETTES.items():
        if style!='standard' and not args.all: continue
        name='tidewraith_concept'+('' if style=='standard' else '_'+style)
        base,glow=textures(palette);base.save(OUT/f'{name}.png');glow.save(OUT/f'{name}_glowmask.png')
        buf=io.BytesIO();base.save(buf,format='PNG')
        model={'meta':{'format_version':'4.10','model_format':'bedrock','box_uv':False},'name':name,
               'model_identifier':'shatteredskies.tidewraith_concept','resolution':{'width':32,'height':32},
               'elements':elements,'outliner':outliner,'animations':clips,
               'textures':[{'id':'0','uuid':uid('texture/'+style),'path':str(OUT/f'{name}.png'),
                            'name':name+'.png','visible':True,'mode':'bitmap','saved':True,
                            'source':'data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()}]}
        path=OUT/f'{name}.bbmodel'
        previous_stamp=path.stat().st_mtime if path.exists() else math.inf
        reusable=args.resume and path.exists() and json.loads(path.read_text())==model
        def completed_preview(filename):
            p=OUT/'previews'/filename
            return reusable and p.exists() and p.stat().st_mtime>=previous_stamp
        codec.write(path,model)
        codec.write(OUT/f'{name}_scaled.bbmodel',codec.scale_bb(model))
        reports.append(validate(model,path,bones))
        for view in ('threequarter','hero','top','right','left','bottom'):
            if not completed_preview(f'{name}_{view}.png'):
                render(model,(720,560),view=view).save(OUT/'previews'/f'{name}_{view}.png')
        if style=='standard':
            if not completed_preview('fly.gif'): animation_preview(model)
            if not completed_preview('mouth_open.gif'): animation_preview(model, 'mouth_open', 'front')
        base.resize((320,320),Image.Resampling.NEAREST).save(OUT/'previews'/f'{name}_atlas.png')
        cards.append(f'<h2>{style.title()}</h2><img src="previews/{name}_front.png"><img src="previews/{name}_threequarter.png"><img src="previews/{name}_right.png"><p><a href="previews/{name}_top.png">Top view</a> · <a href="previews/{name}_left.png">Left view</a> · <a href="previews/{name}_bottom.png">Underside</a></p><p><a href="{name}_scaled.bbmodel">Companion-sized Blockbench model</a> · <a href="{name}.bbmodel">Large editable model</a></p>')
        print(json.dumps({'style':style,'cubes':len(elements),'checks':'PASS'}),flush=True)
    html='<!doctype html><meta charset="utf-8"><title>Tidewraith concept rebuild</title><style>body{background:#141f28;color:#ddf9f6;font:16px system-ui;margin:24px}img{width:32%;vertical-align:top;image-rendering:pixelated}.reference{width:800px;max-width:100%}a{color:#84efdc}</style><h1>Tidewraith · concept-first rebuild</h1><p>Latest repair: downward-curled tips with delayed inner/outer/tip articulation; gentle 2.417-second flight; a coherent 1.6-second mouth opening with all teeth attached to the moving rim. In Blockbench: Animate → select fly or mouth_open → Play.</p><p>Replaces the rejected flat micro study visually. Concept proportions override the earlier cube table. Textures remain 32×32; that budget cannot reproduce all of the reference’s fine texture detail. Back/underside are inferred. Static/software checks do not mean exact visual approval or verified game import.</p><img class="reference" src="../../zero-g-tweaks-bundle/blockbench/references/'+CONCEPT.name+'"><h2>Actual keyframe playback (software preview)</h2><p>Flight · Mouth opening (front view)</p><img src="previews/fly.gif"><img src="previews/mouth_open.gif">'+''.join(cards)
    (OUT/'review.html').write_text(html,encoding='utf-8')
    receipt={'concept':str(CONCEPT.relative_to(ROOT)),'concept_sha256':hashlib.sha256(CONCEPT.read_bytes()).hexdigest(),
             'texture_reference':str(SHEET.relative_to(ROOT)),'texture_sha256':hashlib.sha256(SHEET.read_bytes()).hexdigest(),
             'prompt':'Retain Tidewraith concept body, face, palettes and 32px atlas. Latest user repair: coherent mouth/teeth motion, downward-curled wing tips with delayed Phantom-inspired outer/tip articulation; keep the base flap gentle.',
             'negative_prompt':'No flat slab torso, no rectangular mouth, no straight horns, no rigid stub tentacles, no painted black fake cavity.',
             'proportion_authority':'Latest user: it should look exactly like the concept; previous table no longer constrains geometry.',
             'texture_resolution':[32,32],'scale_factor':FACTOR,'provider':None,'paid_calls':0,
             'body_envelope_units':[BODY_RX*2,20,BODY_RZ*2],
             'body_repair':'Closed occupied volume; recess terminates at z=-10. Hidden interior runs filled, cheeks retained.',
             'flight':{'period_seconds':FLIGHT_PERIOD,'base_wing_degrees':6,'relative_outer_degrees':OUTER_WING_AMPLITUDE,
                       'relative_tip_degrees':TIP_WING_AMPLITUDE,'outer_phase_radians':.4,'tip_phase_radians':.8,
                       'curve':'Down-curled geometry; 32-interval cosine, mirrored inner/outer/tip chain'},
             'mouth':{'duration_seconds':1.6,'maximum_scale':[1.025,1.14,1],
                      'motion':'Shared rim/throat/tooth deformation. Head-mounted fixed collar; no independent tooth-row rotation.',
                      'tooth_plane_z':TOOTH_Z,'gum_surface_z':-12.7},
             'vanilla_reference':{'version':'1.21.1','source':'Local NeoForm sourcesAndCompiledWithNeoForge cache, net/minecraft/client/model/PhantomModel.java',
                                  'observed':'Nested base/tip bones, mirrored cosine rotation, 7.448451 degrees per tick; vanilla amplitude is 16 degrees. Delayed three-joint Tidewraith articulation is a custom adaptation.'},
             'teeth':'30 two-sided alpha-cutout planes, jaw-attached under shared mouth control; lower tips use vertically mirrored UV.',
             'guides':GUIDES,
             'license':'User-supplied reference; no additional rights asserted.','validation':reports,
             'native_import_verified':False,'runtime_verified':False,'human_visual_approval':False}
    receipt['files']={str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='manifest.json'}
    codec.write(OUT/'manifest.json',receipt)


if __name__=='__main__': main()
