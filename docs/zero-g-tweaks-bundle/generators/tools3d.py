"""3D (Draconic-Evolution-style) item models for a ZeroG tool set.
Builds Java item models with elements (opens directly in Blockbench as a Java Block/Item model), a 64x64 HD
material texture, glowing inlays (NeoForge per-element light), preview renders and a sheet.
Usage: python3 tools3d.py <out_dir> [flat_sprite_dir]"""
import json, math, os, sys, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = sys.argv[1]; SPR = sys.argv[2] if len(sys.argv) > 2 else None
SET = 'moonsteel'
H = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
C = dict(outline=H('#1d2126'), dark=H('#5b6470'), mid=H('#8a95a3'), light=H('#b8c3cf'), hi=H('#eef4fa'),
         acc=H('#a8d8ff'), acc_hi=H('#eef8ff'), handle=H('#56606e'), deep=H('#2a4a66'), blue=H('#5a8ab0'))

# ---------------- texture: 64x64, 4x4 grid of 16x16 material swatches ----------------
MATS = ['light', 'mid', 'dark', 'edge', 'grip', 'wrap', 'glow', 'gem', 'plate', 'trim', 'socket', 'core']
def lerp(a, b, t): return tuple(int(x + (y - x) * t) for x, y in zip(a, b))
def swatch(kind, rnd):
    """Approved v4 native material cells, identical to the final runtime atlas.

    Keep cells/UVs and every model/display value unchanged. No random RGB noise.
    """
    im = Image.new('RGBA', (16, 16)); draw = ImageDraw.Draw(im)
    metal, accent = (161, 175, 198), (174, 107, 236)
    def hue(c, level):
        ramps={'moonsteel':['141326','2b2a4a','454a78','6a7bb0','9fb6d8','e6f4ff'],
               'glow':['2a0e4a','5a22a0','9a4ef0','c48cff','e8ccff','ffffff'],
               'cerulite':['06141f','0e3550','14648a','1fa2c4','5fe0f0','dcffff'],
               'wood':['1a0e0a','3c2216','5e3a24','875a36','b0824e','dcb27a']}
        name='moonsteel' if c==metal else 'glow' if c==accent else 'cerulite' if c==(101,224,242) else 'wood'
        index=0 if level<.43 else 1 if level<.7 else 2 if level<.91 else 3 if level<1.15 else 4 if level<1.4 else 5
        return tuple(bytes.fromhex(ramps[name][index]))+(255,)
    for y in range(16):
        for x in range(16):
            if kind in ('glow', 'gem', 'core'):
                dist = ((abs(x - 7.5) + abs(y - 7.5)) / 15 if kind != 'glow'
                        else abs(x - 7.5) / 7.5)
                c = hue((101, 224, 242) if kind == 'glow' else accent,
                        1.65 if dist < .22 else 1.1 if dist < .6 else .64)
            elif kind in ('grip', 'wrap'):
                c = hue((78, 72, 92), .52 if (x + y) % 6 < 2 else 1.1)
            else:
                level = {'light': 1.12, 'mid': .91, 'dark': .59, 'edge': 1.25,
                         'plate': .84, 'trim': .5, 'socket': .83}[kind]
                level += (.22 if x == 0 or y == 0 else -.23 if x == 15 or y == 15
                          else .1 if x < 5 else -.09 if x > 11 else 0)
                c = hue(metal, level)
            im.putpixel((x, y), c)
    if kind in ('mid', 'light', 'plate'):
        draw.line((3, 4, 12, 4), fill=hue(metal, .68))
        draw.line((3, 5, 11, 5), fill=hue(metal, 1.18))
    if kind in ('socket', 'plate'):
        for x, y in [(2, 2), (13, 2), (2, 13), (13, 13)]:
            draw.point((x, y), fill=hue(metal, 1.57))
    return im
rnd = random.Random(7)
TEX = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
for i, m in enumerate(MATS):
    TEX.paste(swatch(m, rnd), ((i % 4) * 16, (i // 4) * 16))
def region(m):  # uv units (0-16 over the whole texture)
    i = MATS.index(m); return ((i % 4) * 4, (i // 4) * 4)
GLOWMATS = {'glow', 'gem', 'core'}

# ---------------- model builder ----------------
class Tool:
    def __init__(self): self.el = []
    def box(self, name, x0, y0, z0, x1, y1, z1, mat, side=None):
        """side: material for the 4 side faces when different from front/back (e.g. 'edge' on blades)"""
        self.el.append(dict(name=name, f=[x0, y0, z0], t=[x1, y1, z1], mat=mat, side=side or mat))
    def cbox(self, name, cx, y0, y1, w, d, mat, cz=8, side=None, x_off=0):
        self.box(name, cx - w / 2 + x_off, y0, cz - d / 2, cx + w / 2 + x_off, y1, cz + d / 2, mat, side)

def faces_for(e):
    u, v = region(e['mat']); su, sv = region(e['side'])
    def fb(m): return [u + .1, v + .1, u + 3.9, v + 3.9]
    def sd(m): return [su + .1, sv + .1, su + 3.9, sv + 3.9]
    out = {}
    for f in ('north', 'south'): out[f] = {'uv': fb(e['mat']), 'texture': '#0'}
    for f in ('east', 'west', 'up', 'down'): out[f] = {'uv': sd(e['side']), 'texture': '#0'}
    return out

ROT = -45  # whole tool rotated so it lies on the same diagonal as the flat sprite (handle bottom-left)
# Hand contexts are exactly vanilla item/handheld: the geometry lies on the flat sprite's diagonal, so no extra turn.
# (2026-10-06: the earlier X half-turn held every tool upside down in game -- by the head, sticking out sideways.)
# Preserve authored translation/scale and all non-hand presentation contexts.
DISPLAY = {
    "thirdperson_righthand": {
        "rotation": [
            0,
            -90,
            55
        ],
        "translation": [
            0,
            4,
            0.5
        ],
        "scale": [
            0.85,
            0.85,
            0.85
        ]
    },
    "thirdperson_lefthand": {
        "rotation": [
            0,
            90,
            -55
        ],
        "translation": [
            0,
            4,
            0.5
        ],
        "scale": [
            0.85,
            0.85,
            0.85
        ]
    },
    "firstperson_righthand": {
        "rotation": [
            0,
            -90,
            25
        ],
        "translation": [
            1.13,
            3.2,
            1.13
        ],
        "scale": [
            0.68,
            0.68,
            0.68
        ]
    },
    "firstperson_lefthand": {
        "rotation": [
            0,
            90,
            -25
        ],
        "translation": [
            1.13,
            3.2,
            1.13
        ],
        "scale": [
            0.68,
            0.68,
            0.68
        ]
    },
    "ground": {
        "rotation": [
            0,
            0,
            0
        ],
        "translation": [
            0,
            2,
            0
        ],
        "scale": [
            0.5,
            0.5,
            0.5
        ]
    },
    "head": {
        "rotation": [
            0,
            180,
            0
        ],
        "translation": [
            0,
            13,
            7
        ],
        "scale": [
            1,
            1,
            1
        ]
    },
    "fixed": {
        "rotation": [
            0,
            180,
            0
        ],
        "scale": [
            1,
            1,
            1
        ]
    }
}
def to_json(tool):
    els = []
    for e in tool.el:
        j = {'name': e['name'], 'from': [round(c, 3) for c in e['f']], 'to': [round(c, 3) for c in e['t']],
             'rotation': {'angle': ROT, 'axis': 'z', 'origin': [8, 8, 8]}, 'faces': faces_for(e)}
        if e['mat'] in GLOWMATS:
            j['neoforge_data'] = {'block_light': 15, 'sky_light': 15}
            j['shade'] = False
        els.append(j)
    return {'credit': 'ZeroG Tweaks - 3D Moonsteel tool (generators/tools3d.py)', 'parent': 'minecraft:item/handheld',
            'texture_size': [64, 64], 'textures': {'0': f'zerog_tweaks:item/3d/{SET}_tools', 'particle': f'zerog_tweaks:item/{SET}_ingot'},
            'elements': els, 'display': DISPLAY}

def handle(t, top, cap=True):
    # pommel moon-gem, grip with cord wraps, steel ferrule; centred on x=8, from y=-3
    t.cbox('pommel', 8, -3.0, -1.6, 2.2, 2.2, 'mid', side='light')
    t.cbox('pommel gem', 8, -3.5, -3.0, 1.2, 1.2, 'gem')
    t.cbox('grip', 8, -1.6, top, 1.6, 1.6, 'grip')
    y = -0.6
    while y < top - 1.4:
        t.cbox('wrap', 8, y, y + .7, 1.9, 1.9, 'wrap'); y += 2.2
    if cap: t.cbox('ferrule', 8, top - 1.2, top, 2.1, 2.1, 'socket')

def sword():
    t = Tool(); handle(t, 4.6)
    t.cbox('guard', 8, 4.6, 6.0, 7.4, 2.2, 'mid', side='light')
    t.cbox('guard core', 8, 4.75, 5.85, 2.0, 2.5, 'core')
    for s in (-1, 1): t.cbox('guard cap', 8 + s * 4.0, 4.2, 6.4, 1.2, 2.6, 'dark', side='mid')
    t.cbox('ricasso', 8, 6.0, 7.2, 2.6, 1.4, 'dark', side='mid')
    t.cbox('blade', 8, 7.2, 17.2, 2.4, 1.1, 'light', side='edge')
    for s in (-1, 1): t.cbox('blade bevel', 8 + s * 1.55, 7.2, 16.4, .7, .55, 'edge')
    t.cbox('fuller', 8, 7.8, 15.6, .55, 1.2, 'glow')
    t.cbox('tip', 8, 17.2, 18.4, 1.7, .9, 'light', side='edge')
    t.cbox('tip 2', 8, 18.4, 19.2, .9, .6, 'edge')
    return t

def pickaxe():
    t = Tool(); handle(t, 12.4)
    t.cbox('socket', 8, 11.6, 15.2, 2.8, 2.6, 'socket')
    t.cbox('moon core', 8, 12.6, 14.2, 1.6, 2.8, 'core')
    # pick arm (right) curving down, tapering
    segs = [(9.4, 11.6, 12.9, 14.9, .95), (11.6, 13.4, 12.4, 14.4, .85), (13.4, 15.0, 11.7, 13.6, .75), (15.0, 16.3, 10.9, 12.7, .62), (16.3, 17.3, 10.1, 11.7, .5)]
    for n, (x0, x1, y0, y1, hz) in enumerate(segs):
        t.box(f'pick {n + 1}', x0, y0, 8 - hz, x1, y1, 8 + hz, 'mid' if n < 3 else 'light', 'light' if n < 3 else 'edge')
    t.box('pick tip', 17.3, 9.4, 7.65, 18.1, 10.7, 8.35, 'edge')
    t.box('pick inlay', 10.0, 13.55, 7.0, 15.2, 13.95, 9.0, 'glow')
    # hammer back (left), chunky with a plated face
    t.box('hammer', 3.6, 11.8, 6.5, 6.6, 15.6, 9.5, 'dark', 'mid')
    t.box('hammer face', 2.8, 12.2, 6.8, 3.6, 15.2, 9.2, 'plate')
    t.box('hammer band', 4.8, 11.6, 6.3, 5.4, 15.8, 9.7, 'trim')
    return t

def axe():
    t = Tool(); handle(t, 13.0)
    t.cbox('socket', 8, 9.0, 14.6, 2.6, 2.6, 'socket')
    t.cbox('cap', 8, 14.6, 15.6, 2.0, 2.0, 'mid', side='light')
    t.cbox('cap gem', 8, 15.6, 16.4, 1.0, 1.0, 'gem')
    t.box('cheek', 9.3, 9.6, 7.25, 12.0, 14.2, 8.75, 'mid', 'light')
    t.box('blade', 12.0, 8.2, 7.4, 14.2, 15.6, 8.6, 'mid', 'light')
    t.box('bit', 14.2, 7.6, 7.6, 15.2, 16.2, 8.4, 'light', 'edge')
    t.box('bit edge', 15.2, 8.4, 7.75, 15.8, 15.4, 8.25, 'edge')
    t.box('horn top', 13.4, 15.6, 7.55, 14.8, 16.8, 8.45, 'light', 'edge')
    t.box('beard', 13.4, 6.8, 7.55, 14.8, 8.2, 8.45, 'light', 'edge')
    t.box('inlay', 12.6, 9.2, 7.3, 13.1, 14.6, 8.7, 'glow')
    t.box('poll', 5.0, 10.6, 6.9, 6.7, 13.6, 9.1, 'dark', 'mid')
    t.box('poll face', 4.4, 11.0, 7.1, 5.0, 13.2, 8.9, 'plate')
    return t

def shovel():
    t = Tool(); handle(t, 11.4)
    t.cbox('collar', 8, 10.6, 12.4, 2.4, 2.4, 'socket')
    t.cbox('neck', 8, 12.4, 13.4, 1.8, 1.4, 'dark', side='mid')
    t.cbox('blade', 8, 13.4, 18.6, 5.2, 1.0, 'light', side='edge')
    for s in (-1, 1): t.cbox('blade rim', 8 + s * 2.85, 13.6, 18.2, .5, .7, 'edge')
    t.cbox('blade lip', 8, 18.6, 19.4, 4.2, .7, 'edge')
    t.cbox('rib', 8, 13.6, 17.8, .6, 1.15, 'glow')
    t.cbox('shoulder', 8, 13.2, 13.8, 5.6, 1.3, 'mid', side='dark')
    return t

def hoe():
    t = Tool(); handle(t, 13.6)
    t.cbox('socket', 8, 12.4, 15.4, 2.6, 2.6, 'socket')
    t.cbox('moon core', 8, 13.2, 14.6, 1.4, 2.7, 'core')
    t.box('arm', 9.3, 13.2, 7.2, 14.6, 14.8, 8.8, 'mid', 'light')
    t.box('arm inlay', 9.8, 13.85, 7.05, 14.2, 14.2, 8.95, 'glow')
    t.box('blade', 13.6, 9.6, 7.45, 15.4, 13.2, 8.55, 'light', 'edge')
    t.box('blade edge', 13.8, 8.6, 7.6, 15.2, 9.6, 8.4, 'edge')
    t.box('spike', 5.2, 13.5, 7.4, 6.7, 14.5, 8.6, 'dark', 'mid')
    t.box('spike tip', 4.0, 13.7, 7.6, 5.2, 14.3, 8.4, 'edge')
    return t

TOOLS = [('sword', 'Sword', sword), ('pickaxe', 'Pickaxe', pickaxe), ('axe', 'Axe', axe), ('shovel', 'Shovel', shovel), ('hoe', 'Hoe', hoe)]

# ---------------- renderer for Java item models ----------------
def rotz(p, ang, o):
    a = math.radians(ang); c, s = math.cos(a), math.sin(a)
    x, y = p[0] - o[0], p[1] - o[1]
    return (o[0] + x * c - y * s, o[1] + x * s + y * c, p[2])
FACE = {  # corner order (a, b, c, d) as offsets from 'from', u along a->b, v along a->d ; normal
    'south': (lambda f, t: [(f[0], t[1], t[2]), (t[0], t[1], t[2]), (t[0], f[1], t[2]), (f[0], f[1], t[2])], (0, 0, 1)),
    'north': (lambda f, t: [(t[0], t[1], f[2]), (f[0], t[1], f[2]), (f[0], f[1], f[2]), (t[0], f[1], f[2])], (0, 0, -1)),
    'east':  (lambda f, t: [(t[0], t[1], t[2]), (t[0], t[1], f[2]), (t[0], f[1], f[2]), (t[0], f[1], t[2])], (1, 0, 0)),
    'west':  (lambda f, t: [(f[0], t[1], f[2]), (f[0], t[1], t[2]), (f[0], f[1], t[2]), (f[0], f[1], f[2])], (-1, 0, 0)),
    'up':    (lambda f, t: [(f[0], t[1], f[2]), (t[0], t[1], f[2]), (t[0], t[1], t[2]), (f[0], t[1], t[2])], (0, 1, 0)),
    'down':  (lambda f, t: [(f[0], f[1], t[2]), (t[0], f[1], t[2]), (t[0], f[1], f[2]), (f[0], f[1], f[2])], (0, -1, 0)),
}
LIGHT = (-.45, .7, .55); LN = math.sqrt(sum(c * c for c in LIGHT)); LIGHT = tuple(c / LN for c in LIGHT)

def render_model(model, tex, yaw=0, pitch=0, roll=0, scale=24, sub=4, bloom=True):
    T = tex.load(); TW = tex.width
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    cr, sr = math.cos(math.radians(roll)), math.sin(math.radians(roll))
    def view(p):
        x, y, z = p[0] - 8, p[1] - 8, p[2] - 8
        x, y = x * cr - y * sr, x * sr + y * cr
        x, z = x * cy + z * sy, -x * sy + z * cy
        y, z = y * cp - z * sp, y * sp + z * cp
        return x, y, z
    polys = []
    for e in model['elements']:
        f, t = e['from'], e['to']; r = e.get('rotation'); glow = 'neoforge_data' in e
        for fname, fd in e['faces'].items():
            corners_fn, n = FACE[fname]
            cs = corners_fn(f, t)
            if r: cs = [rotz(c, r['angle'], r['origin']) for c in cs]; n = rotz(n, r['angle'], (0, 0, 0))
            vn = view(n); vn0 = view((0, 0, 0)); vn = tuple(a - b for a, b in zip(vn, vn0))
            if vn[2] <= 1e-6: continue                           # facing away (camera looks along -z)
            nn = view((0, 0, 0))
            shade = 1.0 if glow else .62 + .5 * max(0, sum(a * b for a, b in zip(rotate_normal(n, yaw, pitch, roll), LIGHT)))
            u0, v0, u1, v1 = fd['uv']; a, b, c_, d = cs
            nu = max(1, int(math.dist(a, b) * sub)); nv = max(1, int(math.dist(a, d) * sub))
            for j in range(nv):
                for i in range(nu):
                    def P(ii, jj):
                        s_, t_ = ii / nu, jj / nv
                        return tuple(a[k] + (b[k] - a[k]) * s_ + (d[k] - a[k]) * t_ for k in range(3))
                    tu = (u0 + (u1 - u0) * (i + .5) / nu) / 16 * TW; tv = (v0 + (v1 - v0) * (j + .5) / nv) / 16 * TW
                    col = T[min(TW - 1, int(tu)), min(TW - 1, int(tv))]
                    q = [view(P(i, j)), view(P(i + 1, j)), view(P(i + 1, j + 1)), view(P(i, j + 1))]
                    depth = sum(p[2] for p in q) / 4
                    polys.append((depth, q, tuple(min(255, int(ch * shade)) for ch in col[:3]), glow))
    xs = [p[0] for _, q, _, _ in polys for p in q]; ys = [p[1] for _, q, _, _ in polys for p in q]
    pad = 2.5
    X0, X1, Y0, Y1 = min(xs) - pad, max(xs) + pad, min(ys) - pad, max(ys) + pad
    W, Hh = int((X1 - X0) * scale), int((Y1 - Y0) * scale)
    im = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); gl = Image.new('RGBA', (W, Hh), (0, 0, 0, 0))
    d = ImageDraw.Draw(im); dg = ImageDraw.Draw(gl)
    for depth, q, col, glow in sorted(polys, key=lambda p: p[0]):
        pts = [((p[0] - X0) * scale, (Y1 - p[1]) * scale) for p in q]
        d.polygon(pts, fill=col + (255,), outline=col + (255,))
        if glow: dg.polygon(pts, fill=(150, 210, 255, 255))
    if bloom:
        b = gl.filter(ImageFilter.GaussianBlur(scale * 1.1)); b2 = gl.filter(ImageFilter.GaussianBlur(scale * .35))
        out = Image.new('RGBA', im.size, (0, 0, 0, 0))
        b.putalpha(b.split()[3].point(lambda v: min(255, int(v * 1.6)))); b2.putalpha(b2.split()[3].point(lambda v: int(v * .9)))
        out.alpha_composite(b); out.alpha_composite(im); out.alpha_composite(b2); return out
    return im

def rotate_normal(n, yaw, pitch, roll):
    x, y, z = n
    cr, sr = math.cos(math.radians(roll)), math.sin(math.radians(roll)); x, y = x * cr - y * sr, x * sr + y * cr
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)); x, z = x * cy + z * sy, -x * sy + z * cy
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch)); y, z = y * cp - z * sp, y * sp + z * cp
    return x, y, z

if __name__ == '__main__':
    os.makedirs(f'{OUT}/models/item', exist_ok=True); os.makedirs(f'{OUT}/textures/item/3d', exist_ok=True); os.makedirs(f'{OUT}/renders', exist_ok=True)
    TEX.save(f'{OUT}/textures/item/3d/{SET}_tools.png')
    models = {}
    for k, name, fn in TOOLS:
        m = to_json(fn()); models[k] = m
        json.dump(m, open(f'{OUT}/models/item/{SET}_{k}.json', 'w'), indent=2)
        for tag, (yw, pt) in {'gui': (0, 0), 'angle': (-38, -22), 'side': (-75, -12)}.items():
            render_model(m, TEX, yw, pt).save(f'{OUT}/renders/{SET}_{k}_{tag}.png')
        print(k, len(m['elements']), 'elements')
