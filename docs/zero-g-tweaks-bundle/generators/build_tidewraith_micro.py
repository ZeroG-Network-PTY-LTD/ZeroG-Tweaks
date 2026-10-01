"""32px, specification-first companion study. Does not replace the boss assets.

Local, deterministic generation; no provider or canonical package certification.
Run from any directory. Only writes the dedicated docs/shattered-skies/micro tree.
"""
from __future__ import annotations

import base64
import copy
import hashlib
import io
import json
import math
from pathlib import Path
import uuid

from PIL import Image, ImageDraw

from review_mob_assets import check, render

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'docs/shattered-skies/micro'
REFERENCE = ROOT / 'docs/zero-g-tweaks-bundle/blockbench/references/codex-clipboard-c7bb1678-125d-4884-9a48-77477d25d546.png'
FACTOR = 8 / 22
PALETTES = {
    'standard': ['#041a24', '#093c43', '#12585d', '#267d80', '#62c7c5', '#b9fff0'],
    'abyssal': ['#071321', '#142735', '#214856', '#35758b', '#65bcd9', '#bdedff'],
    'pearl': ['#314d61', '#668899', '#91b6c0', '#b1d6d9', '#cdf5eb', '#f0fff9'],
    'storm': ['#111f2d', '#273e50', '#386473', '#508b9f', '#7acfe9', '#dbfaff'],
}

# Exact user-specified bone pivots, parent names, and primary cube dimensions.
# Cubes are positioned relative to the stated attachment pivot, not assumed
# to be centred on that pivot. Left is +X here, as in the user's table.
SPEC = {
    'root': (None, [0, 0, 0], None, None),
    'body_main': ('root', [0, 4, 0], [-3, 3, -3], [6, 3, 6]),
    'jaw_upper': ('body_main', [0, 5, -3], [-2.5, 4.5, -5], [5, 1, 2]),
    'jaw_lower': ('body_main', [0, 3, -3], [-2.5, 2.5, -5], [5, 1, 2]),
    'wing_left': ('body_main', [3, 4, 0], [3, 3.5, -2.5], [8, 1, 5]),
    'wing_right': ('body_main', [-3, 4, 0], [-11, 3.5, -2.5], [8, 1, 5]),
    'lobe_left': ('body_main', [2, 4, -3], [2, 3, -6], [1, 2, 3]),
    'lobe_right': ('body_main', [-2, 4, -3], [-3, 3, -6], [1, 2, 3]),
    'tail_base': ('body_main', [0, 4, 3], [-1, 3, 3], [2, 2, 3]),
    'tentacle_1': ('tail_base', [-1, 4, 6], [-1.5, 3.5, 6], [1, 1, 4]),
    'tentacle_2': ('tail_base', [1, 4, 6], [.5, 3.5, 6], [1, 1, 4]),
    'tentacle_3': ('tail_base', [-1, 3, 6], [-1.5, 2.5, 6], [1, 1, 4]),
    'tentacle_4': ('tail_base', [1, 3, 6], [.5, 2.5, 6], [1, 1, 4]),
}
UV = {
    'wing_top': [0, 0, 8, 5], 'wing_bottom': [0, 6, 8, 11],
    'wing_edge': [8, 0, 16, 1], 'wing_root': [8, 2, 13, 3],
    'body_top': [0, 12, 6, 18], 'body_bottom': [7, 12, 13, 18],
    'body_front': [0, 19, 6, 22], 'body_side': [7, 19, 13, 22],
    'jaw_top': [14, 12, 19, 14], 'jaw_side': [14, 15, 16, 16],
    'lobe_front': [18, 0, 19, 2], 'lobe_side': [18, 4, 21, 6],
    'lobe_top': [18, 8, 19, 11],
    'tentacle_side': [22, 0, 26, 1], 'tentacle_end': [22, 3, 23, 4],
    'tail_side': [22, 6, 25, 8], 'tail_end': [22, 10, 24, 12],
    'throat': [14, 19, 19, 22],
    # Dedicated 8x8 emissive corner. Unused rows/columns are bleed gutters.
    'teeth': [24, 24, 29, 26], 'mouth_rim': [24, 26, 29, 27],
    'eye': [30, 24, 32, 26], 'tip': [24, 28, 28, 30],
    'lobe_tip': [30, 28, 32, 30],
}
GLOW = {'teeth', 'mouth_rim', 'eye', 'tip', 'lobe_tip'}


def uid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'zerog/tidewraith/micro/v1/' + name))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def atlas(palette):
    """Hand-clustered 32px interpretation, not a rescaled labelled sheet.

    Shared islands deliberately reuse texels. No stochastic/noise generation.
    """
    base = Image.new('RGBA', (32, 32))
    glow = Image.new('RGBA', (32, 32))
    rgb = [tuple(bytes.fromhex(c[1:])) + (255,) for c in palette]
    wing_rows = ['34322345', '21303234', '23021323', '23103234', '34444345']
    for name, (x0, y0, x1, y1) in UV.items():
        for y in range(y1-y0):
            for x in range(x1-x0):
                w, h = x1-x0, y1-y0
                if name == 'wing_top':
                    tone = int(wing_rows[y][x])
                elif name == 'wing_bottom':
                    tone = 1 if x < 2 and y in (1, 3) else 2 + (x+y == 6)
                elif name == 'body_top':
                    # Bilateral contour bands and a small dorsal scale pattern.
                    rows = ['122221', '233332', '232232', '233332', '232232', '122221']
                    tone = int(rows[y][x])
                elif name == 'body_bottom':
                    tone = 1 if y in (1, 3, 5) and x in (1, 4) else 2
                elif name == 'throat':
                    tone = 1 if y in (0, h-1) or x in (0, w-1) else 0
                elif name == 'teeth':
                    tone = (5 if x % 2 == 0 else 3) if y == 1 else 3
                elif name == 'mouth_rim':
                    tone = 4 if x in (0, w-1) else 5
                elif name == 'eye':
                    tone = 5 if (x, y) == (0, 0) else 4
                elif name in ('tip', 'lobe_tip'):
                    tone = 3 + min(2, x*3//w)
                elif name == 'tentacle_side':
                    tone = [2, 1, 3, 2][x]
                elif name == 'wing_edge':
                    tone = 3 + (x == w-1)
                else:
                    tone = 2 + (y == 0) - (y == h-1 and h > 1)
                base.putpixel((x0+x, y0+y), rgb[tone])
                if name in GLOW:
                    glow.putpixel((x0+x, y0+y), rgb[tone])
    return base, glow


def maps(kind):
    sides = ('north', 'south', 'east', 'west', 'up', 'down')
    if kind == 'body_main':
        names = ('body_front', 'body_front', 'body_side', 'body_side', 'body_top', 'body_bottom')
    elif kind.startswith('wing'):
        names = ('wing_edge', 'wing_edge', 'wing_root', 'wing_root', 'wing_top', 'wing_bottom')
    elif kind.startswith('jaw'):
        names = ('teeth', 'jaw_top', 'jaw_side', 'jaw_side', 'jaw_top', 'jaw_top')
    elif kind.startswith('lobe'):
        names = ('lobe_front', 'lobe_front', 'lobe_side', 'lobe_side', 'lobe_top', 'lobe_top')
    elif kind.startswith('tentacle'):
        names = ('tentacle_end', 'tip', 'tentacle_side', 'tentacle_side', 'tentacle_side', 'tentacle_side')
    elif kind == 'tail_base':
        names = ('tail_end', 'tail_end', 'tail_side', 'tail_side', 'tail_side', 'tail_side')
    else:
        names = (kind,) * 6
    return {face: list(UV[name]) for face, name in zip(sides, names)}


def mirrored(faces):
    # Reflect X: swap east/west and reverse horizontal U on all other faces.
    result = copy.deepcopy(faces)
    result['east'], result['west'] = result['west'], result['east']
    for name in ('north', 'south', 'up', 'down'):
        u0, v0, u1, v1 = result[name]
        result[name] = [u1, v0, u0, v1]
    return result


def geometry():
    bones = {name: {'name': name, 'origin': pivot, 'uuid': uid('bone/'+name),
                    'export': True, 'visibility': True, 'children': [], 'rotation': [0, 0, 0]}
             for name, (_, pivot, _, _) in SPEC.items()}
    parents = {name: data[0] for name, data in SPEC.items()}
    elements = []

    def cube(name, bone, origin, size, kind, mirror=False, plane=False):
        faces = maps(kind)
        if mirror:
            faces = mirrored(faces)
        if plane:
            faces = {f: faces[f] for f in ('north', 'south')}
        element = {'name': name, 'type': 'cube', 'uuid': uid('cube/'+name),
                   'from': origin, 'to': [a+b for a, b in zip(origin, size)],
                   'origin': list(bones[bone]['origin']), 'rotation': [0, 0, 0],
                   'box_uv': False, 'rescale': False, 'locked': False,
                   'faces': {f: {'uv': uv, 'texture': 0, 'rotation': 0} for f, uv in faces.items()}}
        elements.append(element)
        bones[bone]['children'].append(element['uuid'])

    for name, (_, _, origin, size) in SPEC.items():
        if size:
            if name == 'body_main':
                # A rounded 6x3x6 envelope made of connected small masses.
                parts = [([-2, 3, -2], [4, .5, 4]),
                         ([-2.5, 3.5, -3], [5, 2, 1]),
                         ([-2.5, 3.5, 2], [5, 2, 1]),
                         ([-3, 3.5, -2], [1.5, 2, 4]),
                         ([1.5, 3.5, -2], [1.5, 2, 4]),
                         ([-1.5, 3.5, -2], [3, 2, 4]),
                         ([-2.5, 5.5, -2.5], [5, .5, 5])]
                for index, (p, dimensions) in enumerate(parts):
                    cube(f'{name}_step_{index}', name, p, dimensions, name)
                continue
            if name.startswith('wing'):
                # Four tapered slices share sub-rectangles of ONE wing island.
                # Opposite wings are reflected geometry and reflected UVs.
                side = 1 if name.endswith('left') else -1
                for index, (y, height, z, depth) in enumerate(
                        ((3.5, 1, -2.5, 5), (3.7, .8, -2.5, 4.5),
                         (3.95, .55, -2.25, 3.5), (4.2, .3, -2, 2))):
                    x = 3+2*index if side > 0 else -5-2*index
                    cube(f'{name}_step_{index}', name, [x, y, z], [2, height, depth], name, mirror=side < 0)
                    # Preserve continuous wing-top and underside patterns.
                    for face, offset in (('up', 0), ('down', 6)):
                        u0, u1 = index*2, index*2+2
                        elements[-1]['faces'][face]['uv'] = [u0, offset, u1, offset+5] if side > 0 else [u1, offset, u0, offset+5]
                continue
            cube(name, name, origin, size, name,
                 mirror=name.endswith('_right') or name in ('tentacle_2', 'tentacle_4'))
            if name == 'jaw_lower':
                u0, v0, u1, v1 = elements[-1]['faces']['north']['uv']
                elements[-1]['faces']['north']['uv'] = [u0, v1, u1, v0]

    # Recessed throat sits two units behind the jaw front; side walls close gaps.
    cube('mouth_recess', 'body_main', [-2.5, 3.5, -3.025], [5, 1, 0], 'throat', plane=True)
    for side in (-1, 1):
        cube('mouth_corner_'+str(side), 'body_main', [2.25 if side > 0 else -2.5, 3.5, -5],
             [.25, 1, 2], 'mouth_rim', mirror=side < 0)
        # Tiny cyan tips stay within the listed lobe/wing extents.
        cube('lobe_tip_'+str(side), 'lobe_left' if side > 0 else 'lobe_right',
             [2.0 if side > 0 else -3.0, 3.0, -6.015], [1, .5, 0], 'lobe_tip', plane=True, mirror=side < 0)
        cube('wing_tip_'+str(side), 'wing_left' if side > 0 else 'wing_right',
             [10.7 if side > 0 else -11, 4.21, -2], [.3, .29, 2], 'tip', mirror=side < 0)

    # Eight front-facing spots are eight real blink controls (four pairs).
    # Positioned on the exposed forehead above the upper jaw, not on its mouth.
    for row, y in enumerate((5.61, 5.88)):
        for pair, x in enumerate((.65, 1.45)):
            for side in (-1, 1):
                name = f'eye_{row}_{pair}_{"left" if side > 0 else "right"}'
                p = [side*x, y, -2.54]
                bones[name] = {'name': name, 'origin': p, 'uuid': uid('bone/'+name),
                               'export': True, 'visibility': True, 'children': [], 'rotation': [0, 0, 0]}
                parents[name] = 'body_main'
                cube(name, name, [p[0]-.22, y-.1, p[2]], [.44, .2, 0], 'eye', plane=True, mirror=side < 0)

    for name, parent in parents.items():
        if parent:
            bones[parent]['children'].append(bones[name])
    for name, sign in (('wing_left', 1), ('wing_right', -1)):
        bones[name]['rotation'] = [0, 0, sign*6]
    for name, sign in (('lobe_left', 1), ('lobe_right', -1)):
        bones[name]['rotation'] = [15, sign*10, 0]
    for number in range(1, 5):
        bones[f'tentacle_{number}']['rotation'] = [25 if number < 3 else 35,
                                                  -8 if number % 2 else 8, 0]
    return elements, [bones['root']], bones, parents


def animations(bones):
    bb, exported = [], {}

    def clip(action, length, loop, targets):
        animators, geo = {}, {}
        for name, channels in targets.items():
            keys = []
            geo[name] = {}
            for channel, values in channels.items():
                geo[name][channel] = {str(t): vector for t, vector in values}
                for t, vector in values:
                    keys.append({'channel': channel, 'data_points': [dict(zip(('x', 'y', 'z'), vector))],
                                 'uuid': uid(f'{action}/{name}/{channel}/{t}'), 'time': t,
                                 'color': -1, 'interpolation': 'linear'})
            animators[bones[name]['uuid']] = {'name': name, 'type': 'bone', 'keyframes': keys}
        key = 'animation.shatteredskies.tidewraith_micro.'+action
        bb.append({'uuid': uid('animation/'+action), 'name': key, 'loop': 'loop' if loop else 'once',
                   'override': False, 'length': length, 'snapping': 100, 'animators': animators})
        exported[key] = {'loop': loop, 'animation_length': length, 'bones': geo}

    for action, duration, amplitude in (('idle', 3, 5), ('fly', 1.4, 18), ('glide', 4, 2)):
        targets = {}
        for name in ('wing_left', 'wing_right'):
            sign = 1 if name.endswith('left') else -1
            targets[name] = {'rotation': [(round(duration*i/16, 4), [0, 0, sign*amplitude*math.sin(math.tau*i/16)]) for i in range(17)]}
        targets['body_main'] = {'position': [(0, [0, 0, 0]), (duration/2, [0, .2, 0]), (duration, [0, 0, 0])]}
        for number in range(1, 5):
            name = f'tentacle_{number}'
            phase = .5*(number-1)
            targets[name] = {'rotation': [(round(duration*i/16, 4),
                             [7*math.sin(math.tau*i/16+phase), 0, 0]) for i in range(17)]}
        clip(action, duration, True, targets)
    clip('blink', .28, False, {name: {'scale': [(0, [1, 1, 1]), (.08, [1, .02, 1]),
         (.17, [1, .02, 1]), (.28, [1, 1, 1])]} for name in bones if name.startswith('eye_')})
    clip('mouth_open', .8, False, {
        'jaw_upper': {'rotation': [(0, [0, 0, 0]), (.25, [15, 0, 0]), (.55, [15, 0, 0]), (.8, [0, 0, 0])]},
        'jaw_lower': {'rotation': [(0, [0, 0, 0]), (.25, [-20, 0, 0]), (.55, [-20, 0, 0]), (.8, [0, 0, 0])]}})
    return bb, {'format_version': '1.8.0', 'animations': exported}


def export_geo(elements, bones, parents, scaled=False):
    factor = FACTOR if scaled else 1
    member = {child: name for name, bone in bones.items() for child in bone['children'] if isinstance(child, str)}
    result = []
    for name, bone in bones.items():
        entry = {'name': name, 'pivot': [v*factor for v in bone['origin']], 'cubes': []}
        if any(bone['rotation']):
            entry['rotation'] = bone['rotation']
        if parents[name]:
            entry['parent'] = parents[name]
        for element in elements:
            if member[element['uuid']] != name:
                continue
            entry['cubes'].append({'origin': [v*factor for v in element['from']],
                'size': [(hi-lo)*factor for lo, hi in zip(element['from'], element['to'])],
                'uv': {face: {'uv': data['uv'][:2], 'uv_size':
                       [data['uv'][2]-data['uv'][0], data['uv'][3]-data['uv'][1]]}
                       for face, data in element['faces'].items()}})
        result.append(entry)
    return {'format_version': '1.12.0', 'minecraft:geometry': [{
        'description': {'identifier': 'geometry.shatteredskies.tidewraith_micro'+('_scaled' if scaled else ''),
                        'texture_width': 32, 'texture_height': 32,
                        'visible_bounds_width': 2*factor, 'visible_bounds_height': 1.5*factor,
                        'visible_bounds_offset': [0, .25*factor, .1*factor]}, 'bones': result}]}


def scale_bb(model):
    model = copy.deepcopy(model)
    model['name'] += '_scaled'
    model['model_identifier'] += '_scaled'
    for cube in model['elements']:
        for field in ('from', 'to', 'origin'):
            cube[field] = [v*FACTOR for v in cube[field]]
    def walk(nodes):
        for node in nodes:
            if isinstance(node, dict):
                node['origin'] = [v*FACTOR for v in node['origin']]
                walk(node['children'])
    walk(model['outliner'])
    for clip in model['animations']:
        for animator in clip['animators'].values():
            for key in animator['keyframes']:
                if key['channel'] == 'position':
                    for point in key['data_points']:
                        for axis in ('x', 'y', 'z'):
                            point[axis] *= FACTOR
    return model


def validate(model, path, glow):
    report = check(path)
    assert report['texture'] == [32, 32]
    elements = {e['name']: e for e in model['elements']}
    bones, members = {}, {}
    def walk(nodes, parent=None):
        for node in nodes:
            if isinstance(node, str):
                members[node] = parent
            else:
                bones[node['name']] = {**node, 'parent_name': parent}
                walk(node['children'], node['name'])
    walk(model['outliner'])
    for name, (parent, pivot, _, size) in SPEC.items():
        assert bones[name]['origin'] == pivot and bones[name]['parent_name'] == parent
        if size:
            parts = [e for e in model['elements'] if e['name'] == name or e['name'].startswith(name+'_step_')]
            actual = [max(e['to'][a] for e in parts)-min(e['from'][a] for e in parts) for a in range(3)]
            assert all(abs(a-b) < 1e-8 for a, b in zip(actual, size)), (name, actual, size)
    for left, right in (('wing_left', 'wing_right'), ('lobe_left', 'lobe_right'),
                        ('tentacle_1', 'tentacle_2'), ('tentacle_3', 'tentacle_4')):
        names = [left+'_step_'+str(i) for i in range(4)] if left.startswith('wing') else [left]
        for n in names:
            l, r = elements[n], elements[n.replace(left, right)]
            assert abs(l['from'][0]+r['to'][0]) < 1e-8 and abs(l['to'][0]+r['from'][0]) < 1e-8
            assert l['from'][1:] == r['from'][1:] and l['to'][1:] == r['to'][1:]
            for face in ('north', 'south', 'up', 'down'):
                u0, v0, u1, v1 = l['faces'][face]['uv']
                assert r['faces'][face]['uv'] == [u1, v0, u0, v1]
    assert glow.getbbox() == (24, 24, 32, 30)
    blink = next(a for a in model['animations'] if a['name'].endswith('.blink'))
    assert len(blink['animators']) == 8
    report['spec_bone_pivots_parents_and_part_envelopes'] = 'PASS'
    report['bilateral_geometry_and_mirrored_shared_uv'] = 'PASS'
    report['animated_eyes'] = 8
    report['emissive_corner'] = [24, 24, 32, 32]
    debug = {}
    render(model, (768, 512), view='front', debug=debug).save(OUT/'previews'/f'{path.stem}_front.png')
    for name in elements:
        if name.startswith('eye_'):
            assert debug['visible_pixels'].get(name, 0) > 0, f'occluded eye: {name}'
    report['eight_eyes_visible_in_depth_tested_front_view'] = 'PASS'
    return report


def main():
    assert REFERENCE.exists(), 'Copy the user-provided source into references first.'
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'previews').mkdir(exist_ok=True)
    elements, outliner, bones, parents = geometry()
    bb_clips, anim = animations(bones)
    write(OUT/'tidewraith_micro.geo.json', export_geo(elements, bones, parents))
    write(OUT/'tidewraith_micro_scaled.geo.json', export_geo(elements, bones, parents, True))
    write(OUT/'tidewraith_micro.animation.json', anim)
    scaled_anim = copy.deepcopy(anim)
    for clip in scaled_anim['animations'].values():
        for bone in clip['bones'].values():
            for t, vector in bone.get('position', {}).items():
                bone['position'][t] = [v*FACTOR for v in vector]
    write(OUT/'tidewraith_micro_scaled.animation.json', scaled_anim)
    reports, cards = [], []
    for style, palette in PALETTES.items():
        key = 'tidewraith_micro'+('' if style == 'standard' else '_'+style)
        base, glow = atlas(palette)
        base.save(OUT/f'{key}.png')
        glow.save(OUT/f'{key}_glowmask.png')
        buffer = io.BytesIO(); base.save(buffer, format='PNG')
        model = {'meta': {'format_version': '4.10', 'model_format': 'bedrock', 'box_uv': False},
                 'name': key, 'model_identifier': 'shatteredskies.tidewraith_micro',
                 'resolution': {'width': 32, 'height': 32}, 'elements': elements, 'outliner': outliner,
                 'textures': [{'path': str(OUT/f'{key}.png'), 'name': key+'.png', 'id': '0',
                    'uuid': uid('texture/'+style), 'visible': True, 'mode': 'bitmap', 'saved': True,
                    'source': 'data:image/png;base64,'+base64.b64encode(buffer.getvalue()).decode()}],
                 'animations': bb_clips}
        path = OUT/f'{key}.bbmodel'
        write(path, model)
        scaled = scale_bb(model)
        write(OUT/f'{key}_scaled.bbmodel', scaled)
        report = validate(model, path, glow)
        report['scaled_project'] = check(OUT/f'{key}_scaled.bbmodel')
        reports.append(report)
        hero = render(model, (640, 440), view='threequarter')
        hero.save(OUT/'previews'/f'{key}.png')
        top = render(model, (640, 440), view='top')
        top.save(OUT/'previews'/f'{key}_top.png')
        base.resize((320, 320), Image.Resampling.NEAREST).save(OUT/'previews'/f'{key}_atlas.png')
        glow.resize((320, 320), Image.Resampling.NEAREST).save(OUT/'previews'/f'{key}_glowmask.png')
        cards.append(f'<section><h2>{style.title()}</h2><img src="previews/{key}.png"><img src="previews/{key}_front.png"><img src="previews/{key}_top.png"><p>32×32 base and glow mask (nearest-neighbour enlargement):</p><img class="atlas" src="previews/{key}_atlas.png"><img class="atlas" src="previews/{key}_glowmask.png"><p><a href="{key}.bbmodel">Editable dimensions</a> · <a href="{key}_scaled.bbmodel">Half-block companion</a></p></section>')

    # Standalone review: source is linked relatively, model renders are actual UVs.
    html = '<!doctype html><meta charset="utf-8"><title>Tidewraith micro review</title><style>body{background:#131c24;color:#e4fbfa;font:16px system-ui;margin:24px}section{border-top:1px solid #375360;padding:20px 0}img{width:31%;image-rendering:pixelated;vertical-align:top}.atlas{width:256px}a{color:#8affe8}header img{width:700px;max-width:100%}</style><h1>Tidewraith · strict 32×32 micro study</h1><p>Eight independently rigged animated eyes, four tail-mounted tentacles, mirrored shared UVs. Exact authoring dimensions retained; separately baked ×4/11 scale gives approximately half-block wingspan. No original boss models were replaced.</p><p>Static/software checks only. Native Blockbench import, NeoForge registration, renderer glow layer, auras and in-game animation playback are not verified.</p><header><h2>User texture reference</h2><img src="../../zero-g-tweaks-bundle/blockbench/references/'+REFERENCE.name+'"></header>'+''.join(cards)
    (OUT/'review.html').write_text(html, encoding='utf-8')
    source_spec = {name: {'parent': parent, 'pivot': pivot, 'cube_size': size} for name, (parent, pivot, _, size) in SPEC.items()}
    manifest = {'asset': 'tidewraith_micro', 'minecraft_target': 'Java 1.21.1 / NeoForge; Bedrock geometry authoring',
                'texture_resolution': [32, 32], 'specification': source_spec, 'uv_islands': UV,
                'nominal_wingspan_units': 22, 'micro_scale': FACTOR,
                'scale_note': 'Nominal 22 units = 1.375 blocks. Separate export bakes 4/11 into geometry, pivots and positional keyframes; do not apply renderer scale again.',
                'eye_decision': 'User explicitly approved animating all forehead spots; eight spots implemented as four bilateral pairs.',
                'texture_method': 'Original hand-clustered 32px interpretation of user sheet; not a crop or exact HD reproduction.',
                'source_reference': str(REFERENCE.relative_to(ROOT)),
                'source_sha256': hashlib.sha256(REFERENCE.read_bytes()).hexdigest(),
                'provider': None, 'paid_calls': 0, 'license': 'User-supplied reference; no additional rights asserted.',
                'validation': reports, 'native_import_verified': False, 'runtime_verified': False}
    manifest['files'] = {str(p.relative_to(OUT)): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in sorted(OUT.rglob('*')) if p.is_file() and p.name != 'manifest.json'}
    write(OUT/'manifest.json', manifest)
    print(json.dumps({'variants': len(reports), 'texture': [32, 32], 'eyes': 8,
                      'tentacles': 4, 'output': str(OUT), 'static_checks': 'PASS'}))


if __name__ == '__main__':
    main()
