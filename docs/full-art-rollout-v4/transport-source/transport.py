"""ZeroG Transport: energy conduits, fluid pipes, item tubes, ports, energy cells, Null Link.
One data source -> textures, block/item models, blockstates, previews and the written spec.
Usage: python3 transport.py <out_dir>"""
import os, sys, json, math, random
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
NS = 'zerog_tweaks'
FP = '/usr/share/fonts/truetype/dejavu/'
F = lambda s, b=False: ImageFont.truetype(FP + ('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'), s)
FM = lambda s: ImageFont.truetype(FP + 'DejaVuSansMono.ttf', s)
INK, SUB, ACC, BG = (34, 32, 40), (110, 108, 118), (124, 92, 230), (246, 245, 242)


def hx(h, a=255): h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def sh(c, k, a=None): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + ((c[3] if len(c) > 3 else 255) if a is None else a,)


def mix(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,)


# ------------------------------------------------------------------ DATA
TIERS = [  # id, name, where it comes from, dark, mid, light, glow
    ('copper', 'Copper', 'Overworld (vanilla copper)', '#6b3020', '#c86f45', '#f0a982', '#ffb070'),
    ('nullifite', 'Nullifite', 'Overworld deep dark (needs netherite pick)', '#1b1228', '#4a3670', '#9c7ae0', '#b48cff'),
    ('cyrrium', 'Cyrrium', 'Cerulon (Galaxy 2)', '#22323f', '#5f7f94', '#a9c9d9', '#9ff0ff'),
    ('tectium', 'Tectium', 'Skarn (Galaxy 3)', '#2c2826', '#6e6660', '#b5ada5', '#ff9a4a'),
    ('wraithsteel', 'Wraithsteel', 'Eidolon (Galaxy 4)', '#2c3a40', '#8ea2a8', '#d2e2e6', '#9ff0f0'),
    ('astrium', 'Astrium', 'Solvane (Galaxy 5)', '#2a2034', '#7a6c88', '#c9b8d8', '#ffd070'),
]
FE = [1_000, 8_000, 64_000, 512_000, 4_096_000, 32_768_000]                 # FE/t per conduit network
MB = [250, 1_000, 4_000, 16_000, 64_000, 256_000]                            # mB/t per fluid network
ITEMS = [(4, 20, 2), (8, 10, 4), (16, 5, 6), (32, 3, 8), (64, 2, 12), (64, 1, 20)]  # items per pull, ticks between pulls, travel speed blocks/s
CELL = [400_000, 2_000_000, 10_000_000, 50_000_000, 250_000_000, 1_250_000_000]   # energy cell capacity (fits in int)

TYPES = {  # key: block suffix, size s of the cross-section, connector plate (p0, p1), render type
    'energy': dict(suffix='energy_conduit', name='Energy Conduit', s=4, plate=(4, 12), rt='solid'),
    'fluid': dict(suffix='fluid_pipe', name='Fluid Pipe', s=6, plate=(3, 13), rt='translucent'),
    'item': dict(suffix='item_tube', name='Item Tube', s=8, plate=(2, 14), rt='translucent'),
}
MODES = ['none', 'pipe', 'normal', 'push', 'pull']          # per-side blockstate value
MODE_COL = {'normal': '#8b92a0', 'push': '#3f8fe0', 'pull': '#f08a2a'}
TYPE_COL = {'item': '#e9b23a', 'fluid': '#3fb3e0', 'energy': '#e2453a'}
HOT_FLUIDS = [('Liquid Starlight', 'copper'), ('Null Fluid', 'nullifite'), ('Acid', 'cyrrium'), ('Magma Slag', 'tectium'),
              ('Cryo Fluid', 'wraithsteel'), ('Solar Plasma', 'astrium')]

TEX = {}          # path -> Image
MODELS = {}       # path -> json
STATES = {}       # path -> json


def tex(path, img): TEX[path] = img; return f'{NS}:{path}'


def P(img, x, y, c):
    if 0 <= x < img.width and 0 <= y < img.height: img.putpixel((x, y), c)


# ------------------------------------------------------------------ TEXTURES
def pipe_texture(kind, t):
    """16 x 16. Band (side view of a run) along the bottom s rows; end cap s x s in the top-left."""
    tid, tname, _, dk, md, lt, gl = TIERS[t]; dk, md, lt, gl = hx(dk), hx(md), hx(lt), hx(gl)
    s = TYPES[kind]['s']; img = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); r = random.Random(kind + tid)
    b0 = 16 - s
    if kind == 'energy':
        jacket = (58, 61, 69, 255)
        for x in range(16):
            for j in range(s):
                c = jacket if j in (0, s - 1) else sh(jacket, 1.25)
                if j in (1, 2): c = mix(gl, (255, 255, 255), .25) if (x % 4) in (1, 2) else sh(md, .9)   # energy line in windows
                P(img, x, b0 + j, c)
            if x % 4 == 0:
                for j in range(s): P(img, x, b0 + j, md if j in (1, 2) else dk)                         # tier rings
        for j in range(s):
            for i in range(s):
                edge = i in (0, s - 1) or j in (0, s - 1)
                P(img, i, j, dk if edge else gl)
    elif kind == 'fluid':
        for x in range(16):
            for j in range(s):
                if j == 0: c = lt
                elif j == s - 1: c = dk
                else:
                    c = (200, 225, 235, 70 + (25 if j == 1 else 0))
                    if j == 1 and x % 3 == 0: c = (255, 255, 255, 150)                                   # glint
                P(img, x, b0 + j, c)
            if x % 5 == 2:
                for j in range(s): P(img, x, b0 + j, md if 0 < j < s - 1 else dk)                       # clamp rings
                P(img, x, b0, lt)
        for j in range(s):
            for i in range(s):
                ring = i in (0, s - 1) or j in (0, s - 1)
                P(img, i, j, md if ring else (200, 225, 235, 90))
        P(img, 1, 1, (255, 255, 255, 160))
    else:  # item tube
        for x in range(16):
            for j in range(s):
                if j in (0, s - 1): c = md if j == 0 else dk
                else:
                    c = (220, 230, 240, 55)
                    if j == 2 and x % 4 != 3: c = (255, 255, 255, 120)                                    # reflection streak
                P(img, x, b0 + j, c)
            if x % 8 in (0, 1):
                for j in range(s): P(img, x, b0 + j, (lt if x % 8 == 0 else md) if 0 < j < s - 1 else dk)  # rings
        for j in range(s):
            for i in range(s):
                ring = i in (0, s - 1) or j in (0, s - 1)
                ring2 = i in (1, s - 2) or j in (1, s - 2)
                P(img, i, j, dk if ring else (md if ring2 else (220, 230, 240, 70)))
        P(img, 2, 2, (255, 255, 255, 150))
    # free area: tier swatch (top-right), used by nothing; helps texture packs identify the tier
    for j in range(3):
        for i in range(13, 16): P(img, i, j, gl if (i + j) % 2 else md)
    return img


def connector_texture(kind, mode):
    """16 x 16: plate face in the middle, side strip (2 px) in rows 0-1."""
    p0, p1 = TYPES[kind]['plate']; img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    steel, steel_d, steel_l = (93, 99, 112, 255), (52, 56, 64, 255), (150, 158, 172, 255)
    ring = hx(MODE_COL[mode]); tc = hx(TYPE_COL[kind])
    for y in range(p0, p1):
        for x in range(p0, p1):
            c = steel
            if x == p0 or y == p0: c = steel_l
            if x == p1 - 1 or y == p1 - 1: c = steel_d
            if x in (p0 + 1, p1 - 2) and p0 + 1 <= y <= p1 - 2 or y in (p0 + 1, p1 - 2) and p0 + 1 <= x <= p1 - 2: c = ring
            P(img, x, y, c)
    m = (p0 + p1) / 2 - .5; rad = (p1 - p0) / 2 - 3
    for y in range(p0 + 2, p1 - 2):
        for x in range(p0 + 2, p1 - 2):
            dd = math.hypot(x - m, y - m)
            if dd <= rad - .4: P(img, x, y, (24, 24, 28, 255))
            elif dd <= rad + .5: P(img, x, y, sh(tc, .9))
    # mode marks: push = 4 arrows pointing out, pull = 4 pointing in
    cx = int(m + .5)
    if mode in ('push', 'pull'):
        for (dx, dy) in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            ex, ey = cx + dx * int(rad + 1.5), cx + dy * int(rad + 1.5)
            P(img, ex, ey, (255, 255, 255, 255))
            inner = -1 if mode == 'pull' else 1
            P(img, ex - dx * inner + (dy != 0), ey - dy * inner + (dx != 0), ring)
    for x in range(p0, p1):
        P(img, x, 0, steel_l); P(img, x, 1, ring if mode != 'normal' else steel)
    return img


def casing():
    img = Image.new('RGBA', (16, 16)); r = random.Random(7)
    for y in range(16):
        for x in range(16):
            n = r.randint(-4, 4); c = (62 + n, 66 + n, 74 + n, 255)
            if x in (0, 15) or y in (0, 15): c = (38, 41, 47, 255)
            elif x in (1,) or y in (1,): c = (92, 97, 108, 255)
            P(img, x, y, c)
    for (x, y) in ((2, 2), (13, 2), (2, 13), (13, 13)): P(img, x, y, (140, 146, 158, 255)); P(img, x + 1, y + 1, (30, 32, 36, 255))
    return img


GLYPH = {'item': ['.######.', '#......#', '#.####.#', '#.#..#.#', '#.####.#', '#......#', '.######.'],
         'fluid': ['...#...', '..###..', '.#####.', '#######', '#######', '.#####.', '..###..'],
         'energy': ['....##', '...##.', '..####', '...##.', '..##..', '.##...', '##....']}


def port_face(kind, mode):
    img = casing(); tc = hx(TYPE_COL[kind])
    for y in range(3, 13):
        for x in range(3, 13): P(img, x, y, (26, 27, 31, 255))
    ringc = {'input': hx('#3f8fe0'), 'output': hx('#f08a2a'), 'both': hx('#9a6ae0')}[mode]
    for i in range(3, 13):
        for (x, y) in ((i, 3), (i, 12), (3, i), (12, i)): P(img, x, y, ringc)
    g = GLYPH[kind]; gx = 8 - len(g[0]) // 2; gy = 8 - len(g) // 2
    for j, row in enumerate(g):
        for i, ch in enumerate(row):
            if ch == '#': P(img, gx + i, gy + j, tc)
    # arrows on the ring: input points in, output points out
    for (x, y, dx, dy) in ((8, 1, 0, 1), (8, 14, 0, -1), (1, 8, 1, 0), (14, 8, -1, 0)):
        if mode == 'output': dx, dy = -dx, -dy
        if mode == 'both': continue
        P(img, x, y, ringc); P(img, x + dx, y + dy, ringc); P(img, x - dy, y - dx, ringc); P(img, x + dy, y + dx, ringc)
    return img


def cell_side(t):
    tid, tname, _, dk, md, lt, gl = TIERS[t]; dk, md, lt, gl = hx(dk), hx(md), hx(lt), hx(gl)
    img = Image.new('RGBA', (16, 16))
    for y in range(16):
        for x in range(16):
            c = (44, 46, 54, 255)
            if x in (0, 15) or y in (0, 15): c = dk
            if (x < 4 and y < 4) or (x > 11 and y < 4) or (x < 4 and y > 11) or (x > 11 and y > 11):  # tier corner brackets
                c = md if (x in (0, 15) or y in (0, 15)) else (lt if (x in (1, 14) or y in (1, 14)) else c)
            P(img, x, y, c)
    for y in range(4, 12):
        for x in range(4, 10):
            dd = math.hypot(x - 6.5, y - 7.5)
            P(img, x, y, mix(gl, (20, 20, 26), min(1, dd / 4.2)))
    for y in range(3, 13): P(img, 11, y, (20, 20, 24, 255)); P(img, 13, y, (20, 20, 24, 255))
    P(img, 12, 3, (20, 20, 24, 255)); P(img, 12, 12, (20, 20, 24, 255))
    return img


def cell_top(t):
    tid, tname, _, dk, md, lt, gl = TIERS[t]; dk, md, lt, gl = hx(dk), hx(md), hx(lt), hx(gl)
    img = Image.new('RGBA', (16, 16))
    for y in range(16):
        for x in range(16):
            c = md
            if x in (0, 15) or y in (0, 15): c = dk
            elif x in (1, 14) or y in (1, 14): c = lt
            elif 5 <= x <= 10 and 5 <= y <= 10: c = gl if (x + y) % 2 else sh(gl, .8)
            elif (y % 3 == 0) and 3 <= x <= 12: c = sh(md, .7)
            P(img, x, y, c)
    return img


def gauge(level):
    """overlay: 8-segment bar in column 12, rows 4-11; segment lit from the bottom"""
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for i in range(8):
        y = 11 - i
        c = (60, 220, 90, 255) if i < level else (40, 52, 44, 255)
        if i < level and i >= 6: c = (240, 220, 80, 255)
        P(img, 12, y, c)
    return img


def null_link_frames():
    W, Hh, N = 16, 16, 8; img = Image.new('RGBA', (W, Hh * N))
    for f in range(N):
        for y in range(Hh):
            for x in range(W):
                dx, dy = x - 7.5, y - 7.5; r = math.hypot(dx, dy); a = math.atan2(dy, dx)
                swirl = math.sin(a * 3 + r * .9 - f * math.pi / 4)
                v = max(0, swirl) * max(0, 1 - r / 9)
                c = mix((12, 6, 20), (180, 140, 255), v)
                if r < 1.5: c = (235, 225, 255, 255)
                if x in (0, 15) or y in (0, 15): c = (46, 34, 70, 255)
                if (x in (1, 14) or y in (1, 14)) and (x + y + f) % 4 == 0: c = (156, 122, 224, 255)
                P(img, x, f * Hh + y, c)
    return img


def item_icon(kind):
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    if kind == 'wrench':
        rows = ['..........###...', '.........#ooo#..', '........#o###o#.', '........#o#..##.', '.......#o#......', '......#o#.......', '.....#o#........',
                '....#o#.........', '...#v#..........', '..#vvv#.........', '.#vvvvv#........', '..#vvv#.........', '...#v#..........', '................', '................', '................']
        cm = {'#': (40, 42, 48, 255), 'o': (170, 178, 190, 255), 'v': (156, 122, 224, 255)}
    else:
        col = {'item_filter': '#e9b23a', 'fluid_filter': '#3fb3e0', 'frequency': '#9c7ae0'}[kind]
        rows = ['................', '..###########...', '..#ccccccccc#...', '..#c.......c#...', '..#c.ggggg.c#...', '..#c.g...g.c#...', '..#c.g.k.g.c#...',
                '..#c.g...g.c#...', '..#c.ggggg.c#...', '..#c.......c#...', '..#c.y.y.y.c#...', '..#ccccccccc#...', '..###########...', '................', '................', '................']
        cm = {'#': (30, 30, 34, 255), 'c': hx(col), '.': (60, 64, 72, 255), 'g': (200, 170, 70, 255), 'k': (30, 30, 34, 255), 'y': (230, 200, 90, 255)}
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in cm: P(img, i, j, cm[ch])
    return img


# ------------------------------------------------------------------ MODELS (Java block models, 1/16 units)
def face(uv, texture, rot=0, cull=None, tint=None):
    f = {'uv': uv, 'texture': texture}
    if rot: f['rotation'] = rot
    if cull: f['cullface'] = cull
    return f


def pipe_models(kind, t):
    tid = TIERS[t][0]; s = TYPES[kind]['s']; lo = (16 - s) // 2; hi = lo + s; L = lo
    name = f'{tid}_{TYPES[kind]["suffix"]}'; base = f'block/transport/{name}'
    T = tex(base, pipe_texture(kind, t))
    cap = [0, 0, s, s]; band = [16 - L, 16 - s, 16, 16]
    core = {'parent': 'block/block', 'textures': {'pipe': T, 'particle': T}, 'render_type': TYPES[kind]['rt'],
            'elements': [{'from': [lo, lo, lo], 'to': [hi, hi, hi], 'faces': {d: face(cap, '#pipe') for d in ('north', 'south', 'east', 'west', 'up', 'down')}}]}
    arm = {'parent': 'block/block', 'textures': {'pipe': T, 'particle': T}, 'render_type': TYPES[kind]['rt'],
           'elements': [{'from': [lo, lo, 0], 'to': [hi, hi, lo], 'faces': {
               'north': face(cap, '#pipe', cull='north'), 'east': face(band, '#pipe'), 'west': face(band, '#pipe'),
               'up': face(band, '#pipe', rot=90), 'down': face(band, '#pipe', rot=90)}}]}
    MODELS[f'{base}_core'] = core; MODELS[f'{base}_arm'] = arm
    # item model: core + east/west arms, standard block display
    item = {'parent': 'block/block', 'textures': {'pipe': T, 'particle': T}, 'render_type': TYPES[kind]['rt'],
            'elements': core['elements'] + [
                {'from': [0, lo, lo], 'to': [lo, hi, hi], 'faces': {'west': face(cap, '#pipe'), 'north': face(band, '#pipe'), 'south': face(band, '#pipe'), 'up': face(band, '#pipe'), 'down': face(band, '#pipe')}},
                {'from': [hi, lo, lo], 'to': [16, hi, hi], 'faces': {'east': face(cap, '#pipe'), 'north': face(band, '#pipe'), 'south': face(band, '#pipe'), 'up': face(band, '#pipe'), 'down': face(band, '#pipe')}}],
            'display': {'gui': {'rotation': [30, 45, 0], 'scale': [0.8, 0.8, 0.8]}, 'fixed': {'scale': [0.75, 0.75, 0.75]}}}
    MODELS[f'item/{name}'] = item
    # blockstate: multipart, one property per side
    rot = {'north': {}, 'east': {'y': 90}, 'south': {'y': 180}, 'west': {'y': 270}, 'up': {'x': 270}, 'down': {'x': 90}}
    parts = [{'apply': {'model': f'{NS}:{base}_core'}}]
    for d, r in rot.items():
        parts.append({'when': {d: 'pipe|normal|push|pull'}, 'apply': dict({'model': f'{NS}:{base}_arm'}, **r)})
        for m in ('normal', 'push', 'pull'):
            parts.append({'when': {d: m}, 'apply': dict({'model': f'{NS}:block/transport/connector_{kind}_{m}'}, **r)})
    STATES[name] = {'multipart': parts}
    return name


def connector_models():
    for kind in TYPES:
        p0, p1 = TYPES[kind]['plate']
        for m in ('normal', 'push', 'pull'):
            T = tex(f'block/transport/connector_{kind}_{m}', connector_texture(kind, m))
            MODELS[f'block/transport/connector_{kind}_{m}'] = {'parent': 'block/block', 'textures': {'c': T, 'particle': T},
                'elements': [{'from': [p0, p0, 0], 'to': [p1, p1, 2], 'faces': {
                    'north': face([p0, p0, p1, p1], '#c', cull='north'), 'south': face([p0, p0, p1, p1], '#c'),
                    'east': face([p0, 0, p1, 2], '#c', rot=90), 'west': face([p0, 0, p1, 2], '#c', rot=90),
                    'up': face([p0, 0, p1, 2], '#c'), 'down': face([p0, 0, p1, 2], '#c')}}]}


def port_models():
    Tc = tex('block/transport/port_casing', casing())
    for kind in TYPES:
        name = f'{kind}_port'
        for m in ('input', 'output', 'both'):
            Tf = tex(f'block/transport/{kind}_port_{m}', port_face(kind, m))
            MODELS[f'block/transport/{name}_{m}'] = {'parent': 'block/orientable', 'textures': {'front': Tf, 'side': Tc, 'top': Tc}}
        STATES[name] = {'variants': {f'facing={f},mode={m}': dict({'model': f'{NS}:block/transport/{name}_{m}'}, **r)
                                     for f, r in (('north', {}), ('east', {'y': 90}), ('south', {'y': 180}), ('west', {'y': 270}))
                                     for m in ('input', 'output', 'both')}}
        MODELS[f'item/{name}'] = {'parent': f'{NS}:block/transport/{name}_both'}


def cell_models():
    for lv in range(9): tex(f'block/transport/energy_cell_gauge_{lv}', gauge(lv))
    for t, T in enumerate(TIERS):
        tid = T[0]; name = f'{tid}_energy_cell'
        Ts = tex(f'block/transport/{name}_side', cell_side(t)); Tt = tex(f'block/transport/{name}_top', cell_top(t))
        for lv in range(9):
            g = f'{NS}:block/transport/energy_cell_gauge_{lv}'
            MODELS[f'block/transport/{name}_{lv}'] = {'parent': 'block/block', 'textures': {'side': Ts, 'top': Tt, 'gauge': g, 'particle': Ts},
                'elements': [{'from': [0, 0, 0], 'to': [16, 16, 16], 'faces': dict({d: face([0, 0, 16, 16], '#side', cull=d) for d in ('north', 'south', 'east', 'west')},
                                                                                **{d: face([0, 0, 16, 16], '#top', cull=d) for d in ('up', 'down')})},
                             {'from': [-0.01, -0.01, -0.01], 'to': [16.01, 16.01, 16.01], 'faces': {d: face([0, 0, 16, 16], '#gauge', cull=d) for d in ('north', 'south', 'east', 'west')}}],
                'render_type': 'cutout'}
        STATES[name] = {'variants': {f'level={lv}': {'model': f'{NS}:block/transport/{name}_{lv}'} for lv in range(9)}}
        MODELS[f'item/{name}'] = {'parent': f'{NS}:block/transport/{name}_8'}


def misc_models():
    TEX['block/transport/null_link'] = null_link_frames()
    MODELS['block/transport/null_link'] = {'parent': 'block/cube_all', 'textures': {'all': f'{NS}:block/transport/null_link'}}
    STATES['null_link'] = {'variants': {'': {'model': f'{NS}:block/transport/null_link'}}}
    MODELS['item/null_link'] = {'parent': f'{NS}:block/transport/null_link'}
    for k, nm in (('wrench', 'flux_wrench'), ('item_filter', 'item_filter_card'), ('fluid_filter', 'fluid_filter_card'), ('frequency', 'null_frequency_card')):
        T = tex(f'item/{nm}', item_icon(k))
        MODELS[f'item/{nm}'] = {'parent': 'item/handheld' if k == 'wrench' else 'item/generated', 'textures': {'layer0': T}}


# ------------------------------------------------------------------ PREVIEW RENDERER (box elements, per-face samplers)
class Cam:
    def __init__(s, yaw=-35, pitch=28, scale=6):
        s.cy, s.sy, s.cp, s.sp, s.k = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), math.cos(math.radians(pitch)), math.sin(math.radians(pitch)), scale

    def tr(s, p):
        x, y, z = p; xr = x * s.cy - z * s.sy; zr = x * s.sy + z * s.cy
        return (xr * s.k, -(y * s.cp + zr * s.sp) * s.k, zr * s.cp - y * s.sp)


def render_scene(boxes, cam, size=None, bg=(235, 233, 243)):
    """boxes: list of (x0,y0,z0,x1,y1,z1, sampler(face, a, b) -> RGBA or None). Coordinates in pixels (16 per block)."""
    polys = []
    normals = {'north': (0, 0, -1), 'south': (0, 0, 1), 'west': (-1, 0, 0), 'east': (1, 0, 0), 'up': (0, 1, 0), 'down': (0, -1, 0)}
    light = {'up': 1.0, 'north': .82, 'south': .82, 'east': .68, 'west': .68, 'down': .5}
    for (x0, y0, z0, x1, y1, z1, smp) in boxes:
        for f, n in normals.items():
            nz = n[0] * cam.sy + n[2] * cam.cy
            if nz * cam.cp - n[1] * cam.sp >= 0: continue
            if f in ('north', 'south'):
                z = z0 if f == 'north' else z1; A, B = (x0, x1), (y0, y1)
                pt = lambda a, b, z=z: (a, b, z)
            elif f in ('west', 'east'):
                x = x0 if f == 'west' else x1; A, B = (z0, z1), (y0, y1)
                pt = lambda a, b, x=x: (x, b, a)
            else:
                y = y1 if f == 'up' else y0; A, B = (x0, x1), (z0, z1)
                pt = lambda a, b, y=y: (a, y, b)
            na, nb = max(1, int(round(A[1] - A[0]))), max(1, int(round(B[1] - B[0])))
            for i in range(na):
                for j in range(nb):
                    a0, a1 = A[0] + (A[1] - A[0]) * i / na, A[0] + (A[1] - A[0]) * (i + 1) / na
                    b0, b1 = B[0] + (B[1] - B[0]) * j / nb, B[0] + (B[1] - B[0]) * (j + 1) / nb
                    c = smp(f, (i + .5) / na, (j + .5) / nb)
                    if not c or c[3] < 6: continue
                    q = [cam.tr(pt(a0, b0)), cam.tr(pt(a1, b0)), cam.tr(pt(a1, b1)), cam.tr(pt(a0, b1))]
                    polys.append((sum(p[2] for p in q) / 4, [(p[0], p[1]) for p in q], sh(c, light[f], c[3])))
    xs = [p[0] for _, ps, _ in polys for p in ps]; ys = [p[1] for _, ps, _ in polys for p in ps]
    mx, my = min(xs) - 4, min(ys) - 4
    size = (int(max(xs) - mx) + 5, int(max(ys) - my) + 5)
    im = Image.new('RGB', size, bg); d = ImageDraw.Draw(im, 'RGBA')          # RGB canvas so translucent glass blends
    mask = Image.new('L', size, 0); dm = ImageDraw.Draw(mask)
    for _, ps, c in sorted(polys, key=lambda t: -t[0]):
        pp = [(x - mx, y - my) for x, y in ps]
        d.polygon(pp, fill=c); dm.polygon(pp, fill=255)
    out = im.convert('RGBA'); out.putalpha(mask)
    return out


def tex_sampler(img, region, axis_map):
    """region: (u0,v0,u1,v1) in px; axis_map(face, a, b) -> (u_frac, v_frac)"""
    u0, v0, u1, v1 = region
    def f(face, a, b):
        u, v = axis_map(face, a, b)
        x = int(u0 + (u1 - u0) * u - 1e-6); y = int(v0 + (v1 - v0) * v - 1e-6)
        return img.getpixel((min(img.width - 1, max(0, x)), min(img.height - 1, max(0, y))))
    return f


def pipe_boxes(kind, t, bx, by, bz, conns, contents=None):
    """conns: dict dir -> 'pipe'|'normal'|'push'|'pull'"""
    s = TYPES[kind]['s']; lo = (16 - s) // 2; hi = lo + s
    img = TEX[f'block/transport/{TIERS[t][0]}_{TYPES[kind]["suffix"]}']
    ox, oy, oz = bx * 16, by * 16, bz * 16
    out = []
    cap = tex_sampler(img, (0, 0, s, s), lambda f, a, b: (a, 1 - b if f not in ('up', 'down') else b))
    out.append((ox + lo, oy + lo, oz + lo, ox + hi, oy + hi, oz + hi, cap))
    D = {'north': (0, 0, -1), 'south': (0, 0, 1), 'west': (-1, 0, 0), 'east': (1, 0, 0), 'up': (0, 1, 0), 'down': (0, -1, 0)}
    for d, mode in conns.items():
        dx, dy, dz = D[d]
        rng = lambda c, lo=lo, hi=hi: (0, lo) if c < 0 else ((hi, 16) if c > 0 else (lo, hi))
        (x0, x1), (y0, y1), (z0, z1) = rng(dx), rng(dy), rng(dz)
        axis = 'x' if dx else ('y' if dy else 'z')
        def band(f, a, b, axis=axis):
            # along-pipe coordinate first
            if axis == 'x': along, across = a, (1 - b if f not in ('up', 'down') else b)
            elif axis == 'z': along, across = (a if f in ('west', 'east') else b), (1 - b if f in ('west', 'east') else a)
            else: along, across = 1 - b, a
            return along, across
        bs = tex_sampler(img, (16 - lo, 16 - s, 16, 16), band)
        out.append((ox + x0, oy + y0, oz + z0, ox + x1, oy + y1, oz + z1, bs))
        if mode in ('normal', 'push', 'pull'):
            p0, p1 = TYPES[kind]['plate']; ct = TEX[f'block/transport/connector_{kind}_{mode}']
            r2 = lambda c, p0=p0, p1=p1: (0, 2) if c < 0 else ((14, 16) if c > 0 else (p0, p1))
            (a0, a1), (b0, b1), (c0, c1) = r2(dx), r2(dy), r2(dz)
            def plate(f, a, b, ct=ct, p0=p0, p1=p1, dx=dx, dy=dy, dz=dz):
                facing_out = (f == 'north' and dz) or (f == 'south' and dz) or (f in ('west', 'east') and dx) or (f in ('up', 'down') and dy)
                if facing_out: return ct.getpixel((int(p0 + (p1 - p0) * a), int(p0 + (p1 - p0) * (1 - b))))
                return ct.getpixel((int(p0 + (p1 - p0) * a), 1))
            out.append((ox + a0, oy + b0, oz + c0, ox + a1, oy + b1, oz + c1, plate))
    if contents:
        col = contents
        m = lo + 1, hi - 1
        if kind == 'fluid':
            out.insert(0, (ox + m[0], oy + m[0], oz + m[0], ox + m[1], oy + m[0] + (s - 2) * .7, oz + m[1], lambda f, a, b, c=col: c))
            for d in conns:
                dx, dy, dz = D[d]
                rr = lambda c, m=m: (0, m[0]) if c < 0 else ((m[1], 16) if c > 0 else m)
                (x0, x1), (y0, y1), (z0, z1) = rr(dx), rr(dy), rr(dz)
                if not dy: y1 = y0 + (y1 - y0) * .7
                out.insert(0, (ox + x0, oy + y0, oz + z0, ox + x1, oy + y1, oz + z1, lambda f, a, b, c=col: c))
        elif kind == 'item':
            out.insert(0, (ox + 6, oy + 6, oz + 6, ox + 10, oy + 10, oz + 10, lambda f, a, b, c=col: c if (int(a * 4) + int(b * 4)) % 2 else sh(c, .7)))
    return out


def cube_box(bx, by, bz, img_side, img_top=None, front=None, front_dir=None):
    ox, oy, oz = bx * 16, by * 16, bz * 16
    def smp(f, a, b):
        im = img_top if f in ('up', 'down') and img_top else img_side
        if front is not None and f == front_dir: im = front
        u = a if f not in ('north', 'east') else 1 - a
        v = 1 - b if f not in ('up', 'down') else b
        return im.getpixel((min(15, int(u * 16)), min(15, int(v * 16))))
    return (ox, oy, oz, ox + 16, oy + 16, oz + 16, smp)


# ------------------------------------------------------------------ SHEETS
def scene(kind, t):
    """machine -> pull connector -> run -> corner -> push connector -> port"""
    casing_img = TEX['block/transport/port_casing']
    boxes = [cube_box(0, 0, 0, casing_img, front=TEX[f'block/transport/{kind}_port_output'], front_dir='east'),
             cube_box(1, 0, -2, casing_img, front=TEX[f'block/transport/{kind}_port_input'], front_dir='east')]
    fill = {'fluid': hx('#3fb3e0', 210), 'item': hx('#e9b23a'), 'energy': None}[kind]
    boxes += pipe_boxes(kind, t, 1, 0, 0, {'west': 'pull', 'east': 'pipe'}, fill)
    boxes += pipe_boxes(kind, t, 2, 0, 0, {'west': 'pipe', 'north': 'pipe'}, fill)
    boxes += pipe_boxes(kind, t, 2, 0, -1, {'south': 'pipe', 'north': 'pipe'}, fill)
    boxes += pipe_boxes(kind, t, 2, 0, -2, {'south': 'pipe', 'west': 'push'}, fill)
    return render_scene(boxes, Cam(-35, 28, 5))


def contact_sheet():
    keys = sorted(TEX)
    S = 6; cw, chh = 16 * S + 150, 16 * S + 34
    cols = 7; rows = (len(keys) + cols - 1) // cols
    W = 40 + cols * cw; H = 90 + rows * chh
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((28, 22), 'ZeroG Transport  -  all generated textures (16 x 16, shown x6; animated strip shows frame 1)', font=F(22, True), fill=INK)
    for i, k in enumerate(keys):
        x, y = 28 + (i % cols) * cw, 70 + (i // cols) * chh
        t = TEX[k].crop((0, 0, 16, 16)).resize((16 * S, 16 * S), Image.NEAREST)
        for yy in range(0, 16 * S, 12):
            for xx in range(0, 16 * S, 12):
                d.rectangle([x + xx, y + yy, x + xx + 11, y + yy + 11], fill=(225, 225, 225) if (xx // 12 + yy // 12) % 2 else (250, 250, 250))
        im.paste(t, (x, y), t)
        name = k.split('/')[-1]
        d.text((x, y + 16 * S + 4), name[:30], font=FM(11), fill=INK)
    return im


def preview_sheet():
    W = 2300
    rows = []
    for kind in TYPES:
        row = [scene(kind, t) for t in range(6)]
        rows.append((kind, row))
    rh = max(max(i.height for i in r) for _, r in rows) + 70
    H = 110 + rh * 3 + 420
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((28, 20), 'ZeroG Transport  -  in-world previews', font=F(30, True), fill=INK)
    d.text((28, 62), 'Each scene: output port -> PULL connector (orange) -> run with a corner -> PUSH connector (blue) -> input port. Fluid and item contents are drawn by the block entity renderer in game.', font=F(14), fill=SUB)
    y = 100
    for kind, row in rows:
        d.text((28, y), TYPES[kind]['name'] + ('  ·  ' + {'energy': '4 x 4 px, opaque', 'fluid': '6 x 6 px, glass', 'item': '8 x 8 px, glass'}[kind]), font=F(18, True), fill=INK)
        cw = (W - 56) // 6
        for t, r in enumerate(row):
            x = 28 + t * cw
            d.rounded_rectangle([x, y + 30, x + cw - 14, y + rh - 10], 10, fill=(235, 233, 243))
            im.paste(r, (x + (cw - 14 - r.width) // 2, y + 36), r)
            stat = {'energy': f'{FE[t]:,} FE/t', 'fluid': f'{MB[t]:,} mB/t', 'item': f'{ITEMS[t][0]} items / {ITEMS[t][1]} t, {ITEMS[t][2]} b/s'}[kind]
            d.text((x + 10, y + rh - 50), f'{TIERS[t][1]}', font=F(14, True), fill=INK)
            d.text((x + 10, y + rh - 30), stat, font=F(12), fill=SUB)
        y += rh
    # extra blocks row: ports, cells, null link, items
    d.text((28, y), 'Ports, Energy Cells, Null Link and tools', font=F(18, True), fill=INK); y += 34
    casing_img = TEX['block/transport/port_casing']; x = 28
    for kind in TYPES:
        for m in ('input', 'output', 'both'):
            r = render_scene([cube_box(0, 0, 0, casing_img, front=TEX[f'block/transport/{kind}_port_{m}'], front_dir='north')], Cam(-35, 28, 5), bg=BG)
            im.paste(r, (x, y), r); d.text((x, y + r.height + 2), f'{kind} {m}', font=F(11), fill=SUB); x += r.width + 14
    y2 = y + 150; x = 28
    for t in range(6):
        tid = TIERS[t][0]; lv = [2, 3, 4, 5, 6, 8][t]
        side = TEX[f'block/transport/{tid}_energy_cell_side'].copy(); side.alpha_composite(TEX[f'block/transport/energy_cell_gauge_{lv}'])
        r = render_scene([cube_box(0, 0, 0, side, TEX[f'block/transport/{tid}_energy_cell_top'])], Cam(-35, 28, 5), bg=BG)
        im.paste(r, (x, y2), r); d.text((x, y2 + r.height + 2), f'{TIERS[t][1]} cell', font=F(11), fill=SUB); x += r.width + 20
    nl = TEX['block/transport/null_link'].crop((0, 0, 16, 16))
    r = render_scene([cube_box(0, 0, 0, nl)], Cam(-35, 28, 5), bg=BG); im.paste(r, (x + 20, y2), r); d.text((x + 20, y2 + r.height + 2), 'Null Link', font=F(11), fill=SUB); x += r.width + 60
    for nm in ('flux_wrench', 'item_filter_card', 'fluid_filter_card', 'null_frequency_card'):
        ic = TEX[f'item/{nm}'].resize((96, 96), Image.NEAREST); im.paste(ic, (x, y2 + 10), ic); d.text((x, y2 + 112), nm, font=F(11), fill=SUB); x += 130
    return im


# ------------------------------------------------------------------ SPEC
def spec(names):
    o = []; w = o.append
    w('# ZeroG Transport: conduits, pipes, tubes and connection blocks\n')
    w('Mekanism-style transport (networks of thin pipes that connect to anything with a capability) with Powah-style energy cells, '
      'built on the ZeroG tier ladder so every upgrade comes from a planet. All three networks use NeoForge capabilities '
      '(`Capabilities.EnergyStorage.BLOCK`, `FluidHandler.BLOCK`, `ItemHandler.BLOCK`), so they also connect to Mekanism, Powah, Create and vanilla blocks.\n')
    w('Generated by `transport.py`: textures, models, blockstates and every number in this file come from the same data.\n')
    w('## 1. Families\n')
    w('| Family | Moves | Cross-section | Look | Render type |\n| --- | --- | --- | --- | --- |')
    w('| Energy Conduit | FE | 4 x 4 px | Dark insulated cable; tier-coloured rings; glowing line in the gaps | solid |')
    w('| Fluid Pipe | fluids | 6 x 6 px | Glass pipe with tier-metal clamps every 5 px; fluid shows inside | translucent |')
    w('| Item Tube | items | 8 x 8 px | Wide glass tube with tier-metal rings every 8 px; items ride through it | translucent |')
    w('| Energy Cell | stores FE | full block | Tier-metal corner brackets, glowing core window, 8-step gauge | cutout |')
    w('| Item / Fluid / Energy Port | connection point | full block | Casing with a typed front face; Input, Output or Both | solid |')
    w('| Null Link | all three, across dimensions | full block | Animated void swirl (8 frames) | solid |\n')
    w('The three sizes are deliberate: you can tell energy, fluid and item lines apart at a glance, even in the same colour tier.\n')
    w('## 2. Tiers\n')
    w('| Tier | Metal | Comes from | Energy Conduit | Fluid Pipe | Item Tube (items / pull, ticks between pulls, speed) | Energy Cell |\n| --- | --- | --- | --- | --- | --- | --- |')
    for t, T in enumerate(TIERS):
        w(f'| {t + 1} | {T[1]} | {T[2]} | {FE[t]:,} FE/t | {MB[t]:,} mB/t | {ITEMS[t][0]} / {ITEMS[t][1]} t, {ITEMS[t][2]} blocks/s | {CELL[t]:,} FE |')
    w('\nEach tier is 8x the last for energy, 4x for fluids. Tier 1 uses vanilla copper so players can move things before the first ZeroG ore. '
      'Tiers 3-6 match the machine casing ladder (Cyrrium, Tectium, Wraithsteel, Astrium).\n')
    w('**Fluid tier limits (lore):** some planet liquids need a pipe that can hold them. A lower-tier pipe refuses the fluid (it does not break or leak).\n')
    w('| Liquid | Lowest pipe tier |\n| --- | --- |')
    for f, tid in HOT_FLUIDS: w(f'| {f} | {[T[1] for T in TIERS if T[0] == tid][0]} |')
    w('\nWater, lava and honey work in every tier.\n')
    w('## 3. Block ids\n')
    w('All new. Nothing existing is renamed (`gate_energy_port` stays as it is).\n')
    w('| Block | Ids |\n| --- | --- |')
    for kind in TYPES: w(f'| {TYPES[kind]["name"]} | ' + ', '.join(f'`{T[0]}_{TYPES[kind]["suffix"]}`' for T in TIERS) + ' |')
    w('| Energy Cell | ' + ', '.join(f'`{T[0]}_energy_cell`' for T in TIERS) + ' |')
    w('| Ports | `item_port`, `fluid_port`, `energy_port` |')
    w('| Null Link | `null_link` |')
    w('| Items | `flux_wrench`, `item_filter_card`, `fluid_filter_card`, `null_frequency_card` |\n')
    w('## 4. Connections\n')
    w('Each pipe block has six side properties (`north`, `south`, `east`, `west`, `up`, `down`) with these values:\n')
    w('| Value | Drawn as | Meaning |\n| --- | --- | --- |')
    w('| `none` | nothing | No connection on this side. |')
    w('| `pipe` | arm | Joined to another pipe of the same family (any tier, same colour or uncoloured). |')
    w('| `normal` | arm + grey plate | Connected to a block with the capability; the network both inserts and (for energy) receives. Default. |')
    w('| `push` | arm + blue plate, arrows out | Network only inserts into that block. |')
    w('| `pull` | arm + orange plate, arrows in | Network actively extracts from that block (items and fluids need at least one pull side; energy sources push on their own). |\n')
    w('A player-disabled side stores `disabled` in the block entity and shows as `none`, so the pipe will not reconnect by itself.\n')
    w('**Flux Wrench** (`flux_wrench`):\n')
    w('- Right-click a pipe side: cycle normal > push > pull > disabled > normal. A chat line shows the new mode.')
    w('- Shift-right-click: pick the block up (pipes, ports, cells, Null Link keep their contents and settings).')
    w('- Right-click a port: cycle Input > Output > Both. Right-click a cell face: toggle that face between input and output.\n')
    w('**Pull side menu:** right-click a `pull` plate with an empty hand to open a small menu: filter card slot, redstone mode '
      '(ignore, high, low, never) and, for items, routing (nearest first, round robin, random). Push sides have a priority (-10 to 10) set in the same menu; higher priority fills first.\n')
    w('**Colours:** right-click a pipe with a dye to paint it (a tinted band in the texture). Painted pipes only join pipes of the same colour or unpainted ones, so parallel lines stay separate. Right-click with a water bottle to clean.\n')
    w('**Upgrading in place:** right-click a placed pipe with a higher-tier pipe of the same family: it swaps in place and drops the old one. Side settings are kept.\n')
    w('## 5. Network behaviour\n')
    w('- **Energy:** all connected conduits form one network with a shared buffer (sum of each conduit\'s rate). Producers push in, consumers are filled evenly. '
      'The network moves at most the rate of its lowest-tier conduit per tick, so mixed tiers work but bottleneck.')
    w('- **Fluids:** one fluid type per network. The network buffer is the sum of each pipe\'s rate; it fills push sides by priority then evenly. The first fluid in sets the network; empty the network to change it.')
    w('- **Items:** each pull side extracts a stack slice every N ticks (tier table). The item travels along the tube at the tier speed (rendered moving), takes the shortest route to a valid push or normal side that accepts it, and bounces back to the source (or drops if the source is gone) if nothing accepts it.')
    w('- Networks recalculate when a pipe is placed, broken or reconfigured, not every tick. Store networks per level in a `SavedData`, keyed by pipe positions.')
    w('- Breaking a pipe with contents: energy is lost; fluid in that pipe\'s share is lost; items inside drop.\n')
    w('## 6. Connection blocks\n')
    w('**Ports** (`item_port`, `fluid_port`, `energy_port`) are the connection points for multiblocks and machines that should not take pipes on every face '
      '(the gate, alveary tiers, large machines). Place them in the structure; pipes connect to their front face.\n')
    w('| Port | Buffer | Front face | Blockstate |\n| --- | --- | --- | --- |')
    w('| Item Port | 9 slots | Amber crate glyph | `facing` (4) x `mode` (input, output, both) |')
    w('| Fluid Port | 16,000 mB | Cyan drop glyph | same |')
    w('| Energy Port | 1,000,000 FE | Red bolt glyph | same |\n')
    w('Ring colour shows the mode: blue = input (arrows in), orange = output (arrows out), violet = both. Same colours as the pipe plates, so a blue plate always meets a blue ring.\n')
    w('**Energy Cells** (Powah-style): six tiers. Every face is configurable input or output with the wrench (default: all input, the face you place against is output). '
      'Blockstate `level` 0-8 drives the gauge overlay on all four sides. Output rate = the same tier\'s conduit rate. Cells keep their energy when picked up with the wrench.\n')
    w('**Null Link:** endgame (Astrium recipe). Bind two Null Links with a `null_frequency_card` (right-click one, then the other). '
      'They share a 9-slot item buffer, a 16,000 mB fluid tank and a 4,000,000 FE buffer across dimensions, each face set like a cell. '
      'Cost: 2 FE per item, 1 FE per mB, 1% of energy moved, doubled when the two links are in different dimensions. Lore: a sliver of the gate\'s rift, so the Concord could supply outposts.\n')
    w('**Filter cards:** `item_filter_card` (9 ghost slots; whitelist or blacklist; match tags and components toggles) and `fluid_filter_card` (3 ghost fluids). Right-click in the air to edit.\n')
    w('## 7. Models and blockstates\n')
    w('All models are generated; values in 1/16 block.\n')
    w('| Family | Core | North arm | Connector plate |\n| --- | --- | --- | --- |')
    for kind, T in TYPES.items():
        s = T['s']; lo = (16 - s) // 2; hi = lo + s; p0, p1 = T['plate']
        w(f'| {T["name"]} | [{lo},{lo},{lo}] to [{hi},{hi},{hi}] | [{lo},{lo},0] to [{hi},{hi},{lo}] | [{p0},{p0},0] to [{p1},{p1},2] |')
    w('\n- Blockstate is `multipart`: the core always; per side, the arm when the side is `pipe|normal|push|pull`, plus `connector_<family>_<mode>` for `normal|push|pull`. '
      'Arms and plates are authored for north and rotated: east y90, south y180, west y270, up x270, down x90.')
    w('- Arm long faces use the band region with `rotation: 90` on the up/down faces, so the band always runs along the pipe after rotation.')
    w('- Item models: core plus an east-west run, block display. Ports use `block/orientable`. Cells add a gauge overlay element 0.01 px outside the cube.')
    w('- Contents: fluids and moving items are drawn by a `BlockEntityRenderer` inside the glass (fluid fill height = network fill; items interpolate along their path).\n')
    w('## 8. Textures\n')
    w('Every texture is 16 x 16 (Null Link is a 16 x 128 animated strip with `null_link.png.mcmeta`, frametime 3).\n')
    w('**Pipe texture layout:** the bottom `s` rows are the band (the run seen from the side, read left to right along the pipe); the top-left `s x s` square is the end cap (core faces). '
      'The 3 x 3 swatch at the top right shows the tier colour for pack makers.\n')
    w('| Family | Band rows | Cap |\n| --- | --- | --- |')
    for kind, T in TYPES.items(): w(f'| {T["name"]} | {16 - T["s"]}-15 | 0-{T["s"] - 1} x 0-{T["s"] - 1} |')
    w('\n| Tier | Dark | Mid | Light | Glow |\n| --- | --- | --- | --- | --- |')
    for T in TIERS: w(f'| {T[1]} | {T[3]} | {T[4]} | {T[5]} | {T[6]} |')
    w('\nFamily colours (port glyphs and the dark ring in each plate): items #e9b23a, fluids #3fb3e0, energy #e2453a. '
      'Mode colours: normal #8b92a0, push / input #3f8fe0, pull / output #f08a2a, both #9a6ae0.\n')
    w('## 9. Recipes (starting point)\n')
    w('| Output | Recipe |\n| --- | --- |')
    w('| 8 x tier energy conduit | shaped `IRI` (tier ingot, redstone, tier ingot) on all three rows, yields 8 |')
    w('| 8 x tier fluid pipe | `IGI` (ingot, glass, ingot), yields 8 |')
    w('| 8 x tier item tube | `IGI` with a hopper in the middle row: `IGI` / `GHG` / `IGI`, yields 8 |')
    w('| Tier upgrade | 8 pipes of tier N around 1 tier N+1 ingot -> 8 pipes of tier N+1 |')
    w('| Energy cell | tier ingots around a redstone block with the previous tier\'s cell in the middle (copper uses a redstone block only) |')
    w('| Ports | port casing (iron + tier-1 ingot) with a chest / bucket / redstone block |')
    w('| Flux Wrench | 3 iron + 1 Nullifite nugget |')
    w('| Null Link | 2 Astrium blocks, 4 Nullifite ingots, 1 Ender Eye, 2 Null Fluid buckets |\n')
    w('## 10. Lang\n')
    w('`block.zerog_tweaks.<tier>_energy_conduit` = "<Tier> Energy Conduit", likewise for pipes, tubes and cells; tooltips '
      '`tooltip.zerog_tweaks.transport.rate` ("Moves up to %s"), `.mode.<normal|push|pull|disabled>`, `.fluid_too_hot` ("This pipe can\'t carry %s").\n')
    w('## 11. Generated files\n')
    w(f'- {len(TEX)} textures under `assets/{NS}/textures/block/transport/` and `textures/item/`.')
    w(f'- {len(MODELS)} models under `assets/{NS}/models/` and {len(STATES)} blockstates under `assets/{NS}/blockstates/`.')
    w('- `transport_textures.png` (contact sheet) and `transport_previews.png` (in-world renders) are for review, not shipped.\n')
    return '\n'.join(o)


if __name__ == '__main__':
    connector_models(); port_models(); cell_models(); misc_models()
    names = [pipe_models(k, t) for k in TYPES for t in range(6)]
    base = f'{OUT}/assets/{NS}'
    for p, im in TEX.items():
        fp = f'{base}/textures/{p}.png'; os.makedirs(os.path.dirname(fp), exist_ok=True); im.save(fp)
    json.dump({'animation': {'frametime': 3, 'interpolate': True}}, open(f'{base}/textures/block/transport/null_link.png.mcmeta', 'w'))
    for p, m in MODELS.items():
        fp = f'{base}/models/{p}.json'; os.makedirs(os.path.dirname(fp), exist_ok=True); json.dump(m, open(fp, 'w'), indent=1)
    for n, s in STATES.items():
        fp = f'{base}/blockstates/{n}.json'; os.makedirs(os.path.dirname(fp), exist_ok=True); json.dump(s, open(fp, 'w'), indent=1)
    contact_sheet().save(f'{OUT}/transport_textures.png'); preview_sheet().save(f'{OUT}/transport_previews.png')
    open(f'{OUT}/transport_spec.md', 'w').write(spec(names))
    print(len(TEX), 'textures', len(MODELS), 'models', len(STATES), 'blockstates')
