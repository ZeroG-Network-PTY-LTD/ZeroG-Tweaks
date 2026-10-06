"""Dress the GeckoLib chunky-shell armour (Moonsteel, Olympium) in the vanilla-layout worn art.

The worn art is textures/models/armor/<set>_layer_1.png (helmet, chestplate, boots) and _layer_2.png (leggings), each
the vanilla 64x32 armour layout at 2x (128x64). This script:
  * stacks layer 1 over layer 2 into textures/item/armor/<set>.png (128x128) and gives the shell a 64x64 UV space, so
    vanilla armour UV offsets apply directly at the art's 2x resolution;
  * gives every shell cube per-face UVs: each face samples the matching face of its body part's vanilla armour box,
    cropped to where the cube sits on that box (main cubes get the whole face, plates and pauldrons a patch of it);
    left limbs mirror the right ones like vanilla;
  * derives <set>_glowmask.png from the art's saturated accent pixels (cyan inlays, violet gems).
Geometry, bones, pivots and inflate are unchanged.

Box-UV net (Blockbench/GeckoLib): east at u, north at u+d, west at u+d+w, south at u+2d+w (all v+d), up at (u+d, v),
down at (u+d+w, v) drawn flipped. Face orientation, seen from outside: north u along -x, south +x, east -z, west +z,
up/down u along -x; v runs down the face (-y), up's v along -z, down's along +z.

usage: python armor_shell_retexture.py <code-branch assets/zerog_tweaks dir> [set ...]
"""
import colorsys
import json
import sys
from PIL import Image

ASSETS = sys.argv[1]
SETS = sys.argv[2:] or ['nullifite', 'ferrox', 'moonsteel', 'olympium']
L2 = 32  # layer 2 sits below layer 1 in UV units
# Sets without a designed chunky shell borrow another set's geometry (owner's call, 2026-10-06) until a designer
# shell exists: Ferrox's shell is only the eight vanilla boxes and Nullifite's adds four small pieces.
SHELL_FROM = {'nullifite': 'moonsteel', 'ferrox': 'moonsteel'}

# Vanilla HumanoidArmorModel boxes per shell bone: (origin, size, texOffs, mirrored)
PARTS = {
    'armorHead':      ((-4, 24, -4), (8, 8, 8), (0, 0), False),
    'armorBody':      ((-4, 12, -2), (8, 12, 4), (16, 16), False),
    'armorRightArm':  ((-8, 12, -2), (4, 12, 4), (40, 16), False),
    'armorLeftArm':   ((4, 12, -2), (4, 12, 4), (40, 16), True),
    'armorRightLeg':  ((-3.9, 0, -2), (4, 12, 4), (0, 16 + L2), False),
    'armorLeftLeg':   ((-0.1, 0, -2), (4, 12, 4), (0, 16 + L2), True),
    'armorRightBoot': ((-3.9, 0, -2), (4, 12, 4), (0, 16), False),
    'armorLeftBoot':  ((-0.1, 0, -2), (4, 12, 4), (0, 16), True),
}

def span(lo, hi, blo, bsize, flip):
    """Fraction range of [lo,hi] inside the box axis [blo, blo+bsize], clamped; flip measures from the far end."""
    a, b = (lo - blo) / bsize, (hi - blo) / bsize
    if flip: a, b = 1 - b, 1 - a
    a, b = max(0.0, min(1.0, a)), max(0.0, min(1.0, b))
    if b - a < 1 / (2 * bsize):          # cube sits outside the box on this axis: sample a thin strip at the edge
        c = max(0.0, min(1.0, (a + b) / 2)); half = 1 / (4 * bsize)
        a, b = max(0.0, c - half), min(1.0, c + half)
    return a, b

def faces_for(origin, size, part):
    (bo, bs, (u, v), mirrored) = part
    x0, y0, z0 = origin; x1, y1, z1 = x0 + size[0], y0 + size[1], z0 + size[2]
    if mirrored:  # work in the right limb's frame, then mirror the result back
        cx = bo[0] + bs[0] / 2; x0, x1 = 2 * cx - x1, 2 * cx - x0
    w, h, d = bs
    def rect(fu, fv, fw, fh, xs, ys):
        (a, b), (c, e) = xs, ys
        return [fu + a * fw, fv + c * fh], [(b - a) * fw, (e - c) * fh]
    X = lambda flip: span(x0, x1, bo[0], w, flip)
    Y = span(y0, y1, bo[1], h, True)               # v runs downwards
    Z = lambda flip: span(z0, z1, bo[2], d, flip)
    out = {
        'north': rect(u + d, v + d, w, h, X(True), Y),
        'south': rect(u + 2 * d + w, v + d, w, h, X(False), Y),
        'east': rect(u, v + d, d, h, Z(True), Y),
        'west': rect(u + d + w, v + d, d, h, Z(False), Y),
        'up': rect(u + d, v, w, d, X(True), Z(True)),
    }
    (a, b), (c, e) = X(True), Z(False)              # down: drawn flipped, from the bottom of its strip
    out['down'] = [u + d + w + a * w, v + d - c * d], [(b - a) * w, -(e - c) * d]
    if mirrored:  # mirror: swap east/west and flip every face horizontally
        out['east'], out['west'] = out['west'], out['east']
        out = {k: ([uv[0] + sz[0], uv[1]], [-sz[0], sz[1]]) for k, (uv, sz) in out.items()}
    return {k: {'uv': [round(c, 4) for c in uv], 'uv_size': [round(c, 4) for c in sz]} for k, (uv, sz) in out.items()}

def opaque(img, face):
    """Fraction of painted (alpha > 0) texels under a face's UV rect (UV units are half-texels of the 2x art)."""
    (u, v), (w, h) = face['uv'], face['uv_size']
    xs, ys = sorted([u, u + w]), sorted([v, v + h])
    cells = [(x, y) for x in range(int(xs[0] * 2), max(int(xs[0] * 2) + 1, int(xs[1] * 2)))
             for y in range(int(ys[0] * 2), max(int(ys[0] * 2) + 1, int(ys[1] * 2)))]
    return sum(img.getpixel((min(127, x), min(127, y)))[3] > 0 for x, y in cells) / len(cells)

def patch_holes(img, faces, part):
    """Decorative cubes (plates, pauldrons, cuffs, flares) must not show see-through faces where the flat art is cut
    away: move such a face's patch to a painted one -- further down the same face, then the part's front face."""
    (bo, bs, (u, v), mirrored) = part
    w, h, d = bs
    front = (u + d, v + d, w, h)
    for name, face in faces.items():
        if opaque(img, face) > .5: continue
        (fu, fv), (fw, fh) = face['uv'], face['uv_size']
        aw, ah = abs(fw), abs(fh)
        candidates = [(fu, front[1] + front[3] * f) for f in (.35, .5, .2, .65)] if name not in ('up', 'down') else []
        candidates += [(front[0] + (front[2] - aw) / 2 + (aw if fw < 0 else 0), front[1] + front[3] * f) for f in (.35, .5, .2)]
        for cu, cv in candidates:
            trial = {'uv': [round(cu, 4), round(cv + (ah if fh < 0 else 0), 4)], 'uv_size': face['uv_size']}
            if opaque(img, trial) > .5: faces[name] = trial; break
    return faces

def glowmask(img):
    out = Image.new('RGBA', img.size, (0, 0, 0, 0)); px, gp = img.load(), out.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a < 128: continue
            hue, s, val = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if s >= .5 and val >= .55 and (165 <= hue * 360 <= 200 or 255 <= hue * 360 <= 300):  # cyan inlays, violet gems
                gp[x, y] = (r, g, b, 255)
    return out

for s in SETS:
    l1 = Image.open(f'{ASSETS}/textures/models/armor/{s}_layer_1.png').convert('RGBA')
    l2 = Image.open(f'{ASSETS}/textures/models/armor/{s}_layer_2.png').convert('RGBA')
    assert l1.size == l2.size == (128, 64), (s, l1.size, l2.size)
    tex = Image.new('RGBA', (128, 128), (0, 0, 0, 0)); tex.paste(l1, (0, 0)); tex.paste(l2, (0, 64))
    tex.save(f'{ASSETS}/textures/item/armor/{s}.png'); glowmask(tex).save(f'{ASSETS}/textures/item/armor/{s}_glowmask.png')
    # GeckoLib "glowsections" in a texture's .mcmeta name pixels of the old shell art; the glowmask replaces them.
    meta = f'{ASSETS}/textures/item/armor/{s}.png.mcmeta'
    try:
        m = json.load(open(meta, encoding='utf-8'))
        if m.pop('glowsections', None) is not None: json.dump(m, open(meta, 'w', encoding='utf-8', newline='\n'), indent=2)
    except FileNotFoundError:
        pass
    path = f'{ASSETS}/geo/item/armor/{s}.geo.json'
    geo = json.load(open(f'{ASSETS}/geo/item/armor/{SHELL_FROM.get(s, s)}.geo.json', encoding='utf-8'))
    g = geo['minecraft:geometry'][0]
    if s in SHELL_FROM: g['description']['identifier'] = g['description']['identifier'].replace(SHELL_FROM[s], s)
    g['description']['texture_width'] = g['description']['texture_height'] = 64
    n = 0
    for bone in g['bones']:
        part = PARTS.get(bone['name'])
        for cube in bone.get('cubes', []):
            assert part, f'{s}: cube in unmapped bone {bone["name"]}'
            cube.pop('mirror', None); faces = faces_for(cube['origin'], cube['size'], part)
            # Main armour boxes keep vanilla's open top/bottom faces; decorative cubes get no see-through faces.
            main = list(cube['origin']) == list(part[0]) and list(cube['size']) == list(part[1])
            cube['uv'] = faces if main else patch_holes(tex, faces, part); n += 1
    json.dump(geo, open(path, 'w', encoding='utf-8', newline='\n'), indent=2)
    print(f'{s}: {n} cubes remapped; texture 128x128 from layer_1 + layer_2; glowmask from accents')
