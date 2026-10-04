"""Redesign of the Orbital-Bees Genetic Splicer and Geno Station.
Element data -> 128 x 128 texture atlas (2 px per model unit) -> block models, helix GeckoLib model + animation,
reference sheets, before/after and the spec. Usage: python3 gene_machines.py <out_dir> <old_jar_extract_dir>"""
import os, sys, json, math, random
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcrender import render, Cam

OUT = sys.argv[1]; OLD = sys.argv[2] if len(sys.argv) > 2 else None
NS = 'aeroapiary'; PX = 2; ATLAS = 128; U = 16 / ATLAS          # 1 atlas px = 0.125 uv units
FP = '/usr/share/fonts/truetype/dejavu/'
F = lambda s, b=False: ImageFont.truetype(FP + ('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'), s)
FM = lambda s: ImageFont.truetype(FP + 'DejaVuSansMono.ttf', s)
INK, SUB, ACC, BG = (34, 32, 40), (110, 108, 118), (124, 92, 230), (246, 245, 242)


def hx(h, a=255): h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def sh(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3],)


PAL = dict(steel=hx('#4a5060'), steel_l=hx('#6f788b'), steel_d=hx('#2a2e36'), brass=hx('#c99a3a'), brass_l=hx('#efc76c'), brass_d=hx('#8a6420'),
           copper=hx('#b8673c'), copper_l=hx('#e39a62'), glass=(196, 232, 242, 62), glass_e=(225, 246, 252, 150), honey=hx('#e8a82c'), honey_l=hx('#ffd27a'),
           comb=hx('#c98a1e'), screen=hx('#0e2a30'), cyan=hx('#5ff3ff'), violet=hx('#9c7ae0'), amber=hx('#ffb347'), green=hx('#7cf08a'), red=hx('#ff6a5a'))


# ------------------------------------------------------------------ face painters (img, x, y, w, h, rng, el, face)
def P(img, x, y, c):
    if 0 <= x < img.width and 0 <= y < img.height: img.putpixel((x, y), c)


def fill(img, x, y, w, h, c):
    for j in range(h):
        for i in range(w): P(img, x + i, y + j, c)


def m_steel(img, x, y, w, h, r, base='steel', rivets=True):
    b = PAL[base]
    for j in range(h):
        for i in range(w):
            n = r.randint(-5, 5); c = tuple(max(0, min(255, b[k] + n)) for k in range(3)) + (255,)
            if j == 0 or i == 0: c = sh(c, 1.35)
            if j == h - 1 or i == w - 1: c = sh(c, .62)
            P(img, x + i, y + j, c)
    if rivets and w >= 12 and h >= 10:
        for (i, j) in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)): P(img, x + i, y + j, PAL['steel_l']); P(img, x + i + 1, y + j + 1, PAL['steel_d'])


def m_steel_d(img, x, y, w, h, r): m_steel(img, x, y, w, h, r, 'steel_d', False)


def m_brass(img, x, y, w, h, r):
    for j in range(h):
        for i in range(w):
            t = j / max(1, h - 1); c = PAL['brass_l'] if j == 0 else (PAL['brass_d'] if j == h - 1 else (PAL['brass'] if t < .6 else sh(PAL['brass'], .88)))
            if (i + j) % 7 == 0 and 0 < j < h - 1: c = sh(c, 1.08)
            P(img, x + i, y + j, c)


def m_copper_coil(img, x, y, w, h, r):
    for j in range(h):
        for i in range(w):
            P(img, x + i, y + j, PAL['copper_l'] if (i + j) % 3 == 0 else PAL['copper'])


def m_glass(img, x, y, w, h, r):
    for j in range(h):
        for i in range(w):
            c = PAL['glass_e'] if (i in (0, w - 1) or j in (0, h - 1)) else PAL['glass']
            if 0 < i < w - 1 and 0 < j < h - 1 and (i - j) % 9 in (0, 1) and i < w * .6: c = (255, 255, 255, 110)
            P(img, x + i, y + j, c)


def m_honey_glass(img, x, y, w, h, r, level=.7):
    m_glass(img, x, y, w, h, r)
    for j in range(int(h * (1 - level)), h - 1):
        for i in range(1, w - 1):
            P(img, x + i, y + j, PAL['honey_l'] if j == int(h * (1 - level)) else (sh(PAL['honey'], .9 + .1 * ((i + j) % 3 == 0))))


def m_honeycomb(img, x, y, w, h, r):
    m_steel(img, x, y, w, h, r, 'steel_d', False)
    for j in range(2, h - 2):
        for i in range(2, w - 2):
            row = j // 3; off = 2 if row % 2 else 0
            edge = (i + off) % 4 == 0 or j % 3 == 0
            P(img, x + i, y + j, PAL['brass_d'] if edge else (PAL['comb'] if (i * 7 + j * 3) % 5 else PAL['honey_l']))
    fill(img, x + w // 2, y + 2, 1, h - 4, PAL['steel_d'])                                   # door split
    P(img, x + w // 2 - 2, y + h // 2, PAL['brass_l']); P(img, x + w // 2 + 2, y + h // 2, PAL['brass_l'])  # handles


def m_screen_genome(img, x, y, w, h, r):
    fill(img, x, y, w, h, PAL['steel_d'])
    fill(img, x + 1, y + 1, w - 2, h - 2, PAL['screen'])
    cols = [PAL['cyan'], PAL['amber'], PAL['green'], PAL['violet'], PAL['red']]
    for j in range(2, h - 2, 2):                                                             # genome bars: one row per chromosome
        L = r.randint(int((w - 4) * .3), w - 4)
        for i in range(2, 2 + L): P(img, x + i, y + j, cols[(j // 2) % 5] if i % 6 else sh(cols[(j // 2) % 5], .6))
    P(img, x + w - 3, y + 2, PAL['green'])


def m_screen_splice(img, x, y, w, h, r):
    fill(img, x, y, w, h, PAL['steel_d']); fill(img, x + 1, y + 1, w - 2, h - 2, PAL['screen'])
    for i in range(2, w - 2):                                                                # two strands crossing
        a = math.sin(i / max(1, (w - 4)) * math.pi * 2)
        y1 = int(round(y + h / 2 + a * (h / 2 - 2))); y2 = int(round(y + h / 2 - a * (h / 2 - 2)))
        P(img, x + i, min(y + h - 2, max(y + 1, y1)), PAL['cyan']); P(img, x + i, min(y + h - 2, max(y + 1, y2)), PAL['amber'])
    fill(img, x + 2, y + h - 2, max(1, (w - 4) * 2 // 3), 1, PAL['green'])                  # progress bar


def m_rung(img, x, y, w, h, r):
    for j in range(h):
        for i in range(w):
            t = i / max(1, w - 1)
            c = PAL['cyan'] if t < .35 else (PAL['amber'] if t > .65 else (240, 240, 255, 255))
            P(img, x + i, y + j, c)


def m_serum(col):
    def f(img, x, y, w, h, r):
        m_glass(img, x, y, w, h, r)
        i0, i1 = (1, w - 1) if w > 3 else (0, w)                                     # thin vials: liquid fills the whole face width
        for j in range(max(1, int(h * .15)), h - 1):
            for i in range(i0, i1): P(img, x + i, y + j, hx(col) if (i + j) % 4 else sh(hx(col), 1.25))
    return f


def m_coil_top(img, x, y, w, h, r):
    m_steel(img, x, y, w, h, r, 'steel', False)
    cx, cy = x + w / 2 - .5, y + h / 2 - .5
    for j in range(h):
        for i in range(w):
            dd = math.hypot(x + i - cx, y + j - cy)
            if dd <= 2.2: P(img, x + i, y + j, PAL['violet'] if (i + j) % 2 else (210, 190, 255, 255))
            elif dd <= 3.4: P(img, x + i, y + j, PAL['copper_l'])
            elif dd <= 4.4: P(img, x + i, y + j, PAL['copper'])


def m_lens(img, x, y, w, h, r):
    fill(img, x, y, w, h, PAL['steel_d'])
    for j in range(1, h - 1):
        for i in range(1, w - 1): P(img, x + i, y + j, PAL['violet'] if (i + j) % 2 else (210, 190, 255, 255))


def m_specimen(img, x, y, w, h, r):
    for j in range(h):
        for i in range(w): P(img, x + i, y + j, PAL['honey'] if (i // max(1, w // 3)) % 2 == 0 else (30, 26, 22, 255))


def m_keys(img, x, y, w, h, r):
    m_steel(img, x, y, w, h, r, 'steel_d', False)
    for j in range(1, h - 1, 2):
        for i in range(1, w - 1, 2): P(img, x + i, y + j, (170, 176, 190, 255) if (i + j) % 6 else PAL['amber'])


def m_needle(img, x, y, w, h, r):
    for j in range(h):
        for i in range(w): P(img, x + i, y + j, (200, 206, 216, 255) if j == 0 else (150, 156, 168, 255))


MATS = dict(coil_top=m_coil_top, steel=m_steel, steel_d=m_steel_d, brass=m_brass, coil=m_copper_coil, glass=m_glass, honey_glass=m_honey_glass, honeycomb=m_honeycomb,
            genome=m_screen_genome, splice=m_screen_splice, rung=m_rung, lens=m_lens, specimen=m_specimen, keys=m_keys, needle=m_needle,
            serum_cyan=m_serum('#5ff3ff'), serum_violet=m_serum('#9c7ae0'), serum_green=m_serum('#7cf08a'), serum_amber=m_serum('#ffb347'))
GLOW = {'coil_top', 'genome', 'splice', 'rung', 'lens', 'serum_cyan', 'serum_violet', 'serum_green', 'serum_amber'}


def E(name, a, b, mat='steel', faces=None, rot=None, label=None, hide=(), bone=None):
    return dict(name=name, a=a, b=b, mat=mat, faces=faces or {}, rot=rot, label=label, hide=set(hide), bone=bone)


# ------------------------------------------------------------------ the two machines (model faces north)
def splicer():
    rung = lambda i, y, ang: E(f'rung_{i}', [5.5, y, 8.5], [10.5, y + 1, 9.5], 'rung', rot={'origin': [8, y, 9], 'axis': 'y', 'angle': ang}, bone='helix',
                              label='DNA helix (spins, GeckoLib)' if i == 2 else None)
    return [
        E('base', [0, 0, 0], [16, 2, 16], 'steel', label='Steel plinth'),
        E('step', [1, 2, 1], [15, 3, 15], 'brass', label='Brass step'),
        E('console', [3, 3, 0.5], [13, 6, 4], 'steel', faces={'up': 'keys'}, label='Control console (keys on top)'),
        E('screen', [4, 5.2, 1.6], [12, 8.2, 2.4], 'steel_d', faces={'north': 'splice'}, rot={'origin': [8, 5.2, 2], 'axis': 'x', 'angle': 22.5}, label='Splice screen (glows)'),
        E('pedestal', [4, 3, 5], [12, 4, 13], 'brass'),
        E('chamber', [4, 4, 5], [12, 13, 13], 'glass', label='Glass gene chamber'),
        E('cap', [3, 13, 4], [13, 15, 14], 'steel', label='Chamber cap'),
        E('coil', [4, 15, 5], [12, 16, 13], 'coil', faces={'up': 'coil_top'}, label='Resonance coil (violet core glows)'),
        rung(0, 5, -45), rung(1, 6.5, -22.5), rung(2, 8, 0), rung(3, 9.5, 22.5), rung(4, 11, 45),
        E('arm_l_block', [0.5, 6, 7], [3, 9, 11], 'steel', label='Left injector'),
        E('needle_l', [3, 7, 8.5], [5, 8, 9.5], 'needle'),
        E('arm_r_block', [13, 6, 7], [15.5, 9, 11], 'steel', label='Right injector'),
        E('needle_r', [11, 7, 8.5], [13, 8, 9.5], 'needle'),
        E('vial_r', [13.5, 9, 8], [15, 13, 10], 'serum_cyan', label='Serum vial in use (glows)'),
        E('vial_cap', [13.25, 13, 7.75], [15.25, 13.75, 10.25], 'brass'),
        E('conduit', [6, 3, 13], [10, 12, 15], 'honey_glass', label='Royal-jelly feed (back)'),
        E('conduit_top', [5.5, 12, 12.5], [10.5, 13, 15.5], 'brass'),
    ]


def geno():
    return [
        E('plinth', [0, 0, 1], [16, 1, 16], 'steel_d'),
        E('cabinet', [1, 1, 2], [15, 9, 15], 'steel', faces={'north': 'honeycomb'}, label='Cabinet, honeycomb doors'),
        E('worktop', [0, 9, 1], [16, 10, 16], 'brass', label='Brass worktop'),
        E('keyboard', [3, 10, 2], [9, 10.5, 5], 'keys', label='Keyboard'),
        E('mon_stand', [5, 10, 12], [8, 12, 13], 'steel_d'),
        E('monitor', [1.5, 11.5, 11], [11.5, 16, 13], 'steel', faces={'north': 'genome'}, rot={'origin': [6.5, 11.5, 12], 'axis': 'x', 'angle': 22.5}, label='Genome monitor (glows)'),
        E('dish', [6, 10, 6.5], [10, 10.6, 10.5], 'glass', label='Specimen dish'),
        E('specimen', [7.3, 10.6, 8], [8.7, 11.4, 9.4], 'specimen', label='Bee specimen'),
        E('scan_post', [12.5, 10, 8.5], [13.5, 15, 9.5], 'steel'),
        E('scan_arm', [8, 14, 8.5], [13.5, 15, 9.5], 'steel'),
        E('scan_head', [7, 12.5, 8], [9, 14, 10], 'steel_d', faces={'down': 'lens'}, label='Scanner head (violet lens glows)'),
        E('rack', [0.5, 10, 6], [4.5, 11, 9], 'brass', label='Serum rack'),
        E('vial_1', [1, 11, 7], [2, 14, 8], 'serum_green'),
        E('vial_2', [2.25, 11, 7], [3.25, 14, 8], 'serum_violet'),
        E('vial_3', [3.5, 11, 7], [4.5, 14, 8], 'serum_amber', label='Trait serums (glow)'),
        E('tank', [12, 10, 11], [15.5, 15.5, 15], 'honey_glass', label='Honey reagent tank'),
        E('tank_cap', [11.75, 15.5, 10.75], [15.75, 16, 15.25], 'brass'),
    ]


# ------------------------------------------------------------------ atlas packing + model building
def face_dims(el, f):
    a, b = el['a'], el['b']; dx, dy, dz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    w, h = {'north': (dx, dy), 'south': (dx, dy), 'east': (dz, dy), 'west': (dz, dy), 'up': (dx, dz), 'down': (dx, dz)}[f]
    return max(1, math.ceil(w * PX - 1e-6)), max(1, math.ceil(h * PX - 1e-6))


def build(name, els):
    atlas = Image.new('RGBA', (ATLAS, ATLAS), (0, 0, 0, 0)); rects = []
    jobs = []
    for el in els:
        for f in ('north', 'south', 'east', 'west', 'up', 'down'):
            if f in el['hide']: continue
            w, h = face_dims(el, f); jobs.append((h, w, el, f))
    jobs.sort(key=lambda j: (-j[0], -j[1]))
    x = y = rowh = 0; place = {}
    for h, w, el, f in jobs:
        if x + w > ATLAS: x, y, rowh = 0, y + rowh, 0
        assert y + h <= ATLAS, f'{name}: atlas full'
        place[(el['name'], f)] = (x, y, w, h); x += w; rowh = max(rowh, h)
    for el in els:
        for f in ('north', 'south', 'east', 'west', 'up', 'down'):
            if (el['name'], f) not in place: continue
            x, y, w, h = place[(el['name'], f)]
            mat = el['faces'].get(f, el['mat'])
            MATS[mat](atlas, x, y, w, h, random.Random(name + el['name'] + f))
            rects.append((x, y, w, h, el['name'], f, mat))
    tex_id = f'{NS}:block/machines/{name}'
    model = {'parent': 'block/block', 'render_type': 'minecraft:translucent', 'textures': {'all': tex_id, 'particle': tex_id}, 'elements': []}
    for el in els:
        if el['bone'] == 'helix' and name == 'genetic_splicer_v2': pass
        e = {'name': el['name'], 'from': el['a'], 'to': el['b'], 'faces': {}}
        if el['rot']: e['rotation'] = el['rot']
        glow = el['mat'] in GLOW or any(m in GLOW for m in el['faces'].values())
        for f in ('north', 'south', 'east', 'west', 'up', 'down'):
            if (el['name'], f) not in place: continue
            x, y, w, h = place[(el['name'], f)]
            e['faces'][f] = {'uv': [round(x * U, 4), round(y * U, 4), round((x + w) * U, 4), round((y + h) * U, 4)], 'texture': '#all'}
        if glow and el['mat'] in GLOW: e['neoforge_data'] = {'block_light': 15, 'sky_light': 15}
        model['elements'].append(e)
    # glowing single faces (screens, lenses) on otherwise plain elements: split into an emissive overlay element
    for el in els:
        for f, mat in el['faces'].items():
            if mat in GLOW and el['mat'] not in GLOW:
                x, y, w, h = place[(el['name'], f)]
                a, b = list(el['a']), list(el['b']); d = .01
                axis = {'north': (2, -d), 'south': (2, d), 'west': (0, -d), 'east': (0, d), 'down': (1, -d), 'up': (1, d)}[f]
                i, s = axis
                if s < 0: b[i] = a[i]; a[i] = a[i] + s
                else: a[i] = b[i]; b[i] = b[i] + s
                ov = {'name': el['name'] + '_glow', 'from': [round(v, 3) for v in a], 'to': [round(v, 3) for v in b],
                      'faces': {f: {'uv': [round(x * U, 4), round(y * U, 4), round((x + w) * U, 4), round((y + h) * U, 4)], 'texture': '#all'}},
                      'neoforge_data': {'block_light': 15, 'sky_light': 15}}
                if el['rot']: ov['rotation'] = el['rot']
                model['elements'].append(ov)
    glowmask = Image.new('RGBA', atlas.size, (0, 0, 0, 0))
    for x, y, w, h, n, f, mat in rects:
        if mat in GLOW: glowmask.paste(atlas.crop((x, y, x + w, y + h)), (x, y))
    return model, atlas, glowmask, rects


def blockstate(name):
    return {'variants': {f'facing={f}': ({'model': f'{NS}:block/other/{name}'} | ({'y': r} if r else {}))
                         for f, r in (('north', 0), ('east', 90), ('south', 180), ('west', 270))}}


def helix_geo(els):
    """GeckoLib block model for the animated helix only (rendered by the block entity renderer; the static rungs are left out of the baked model)."""
    cubes = []
    for el in els:
        if el['bone'] != 'helix': continue
        (x0, y0, z0), (x1, y1, z1) = el['a'], el['b']
        cubes.append({'origin': [round(-(x1 - 8), 3), y0, round(z0 - 8, 3)], 'size': [x1 - x0, y1 - y0, z1 - z0], 'pivot': [0, y0 + .5, round(9 - 8, 3)],
                      'rotation': [0, -el['rot']['angle'], 0], 'uv': {f: {'uv': [0, 0], 'uv_size': [16, 2]} for f in ('north', 'south', 'east', 'west', 'up', 'down')}})
    return {'format_version': '1.12.0', 'minecraft:geometry': [{'description': {'identifier': 'geometry.aeroapiary.genetic_splicer_helix', 'texture_width': 16, 'texture_height': 16,
                                                                                   'visible_bounds_width': 2, 'visible_bounds_height': 2, 'visible_bounds_offset': [0, 0.5, 0]},
                                                                   'bones': [{'name': 'helix', 'pivot': [0, 8, 1], 'cubes': cubes}]}]}


def helix_anim():
    return {'format_version': '1.8.0', 'animations': {
        'animation.aeroapiary.genetic_splicer.idle': {'loop': True, 'animation_length': 8, 'bones': {'helix': {'rotation': {'0.0': [0, 0, 0], '8.0': [0, 360, 0]}}}},
        'animation.aeroapiary.genetic_splicer.working': {'loop': True, 'animation_length': 2, 'bones': {'helix': {
            'rotation': {'0.0': [0, 0, 0], '2.0': [0, 360, 0]}, 'position': {'0.0': [0, 0, 0], '1.0': [0, 0.5, 0], '2.0': [0, 0, 0]}}}}}}


def helix_tex():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    m_rung(im, 0, 0, 16, 2, None); return im


# ------------------------------------------------------------------ sheets
def ortho(model, tex, yaw, pitch, scale): return render(model, {'all': tex}, Cam(yaw, pitch, scale), bg=(255, 255, 255))


def wrap(d, text, font, width):
    out, cur = [], ''
    for wd in text.split(' '):
        t = (cur + ' ' + wd).strip()
        if d.textlength(t, font=font) <= width: cur = t
        else: out.append(cur); cur = wd
    out.append(cur); return out


def sheet(name, title, sub, els, model, atlas, glowmask, rects, text_blocks, path):
    W, H = 2240, 1980
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((28, 20), f'{title}  —  redesign reference sheet', font=F(32, True), fill=INK)
    d.text((28, 64), sub, font=F(14), fill=SUB)
    views = [('FRONT', 0, 0), ('RIGHT SIDE', -90, 0), ('BACK', 180, 0), ('TOP', 0, 89)]
    x = 28
    for t, yaw, pitch in views:
        box = (x, 100, x + 420, 560)
        d.rectangle(box, fill=(255, 255, 255), outline=(205, 203, 214)); d.text((box[0] + 14, box[1] + 12), t, font=F(15, True), fill=INK)
        r = ortho(model, atlas, yaw, pitch, 22)
        im.paste(r, (box[0] + (420 - r.width) // 2, box[1] + 40 + (420 - r.height) // 2), r); x += 436
    # 3D big
    box = (x, 100, W - 28, 560)
    d.rectangle(box, fill=(255, 255, 255), outline=(205, 203, 214)); d.text((box[0] + 14, box[1] + 12), '3D', font=F(15, True), fill=INK)
    r = render(model, {'all': atlas}, Cam(-35, 26, 15), bg=(255, 255, 255)); im.paste(r, (box[0] + (box[2] - box[0] - r.width) // 2, box[1] + 40), r)
    # labelled 3D
    lb = (28, 580, 1100, 1240); d.rectangle(lb, fill=(255, 255, 255), outline=(205, 203, 214)); d.text((lb[0] + 14, lb[1] + 12), 'PARTS', font=F(15, True), fill=INK)
    cam = Cam(-35, 26, 24); r = render(model, {'all': atlas}, cam, bg=(255, 255, 255))
    ox, oy = lb[0] + (lb[2] - lb[0] - r.width) // 2, lb[1] + 50; im.paste(r, (ox, oy), r)
    # projection offset: recompute bounds the same way render() does
    from mcrender import _rot
    pts = []
    for e in model['elements']:
        for xx in (e['from'][0], e['to'][0]):
            for yy in (e['from'][1], e['to'][1]):
                for zz in (e['from'][2], e['to'][2]): pts.append(cam.tr(_rot((xx, yy, zz), e.get('rotation'))))
    mx = min(p[0] for p in pts) - 4; my = min(p[1] for p in pts) - 4
    labs = []
    for el in els:
        if not el['label']: continue
        c = [(el['a'][i] + el['b'][i]) / 2 for i in range(3)]
        p = cam.tr(_rot(c, el['rot'])); labs.append((p[1] - my + oy, p[0] - mx + ox, el['label']))
    L = [l for l in labs if l[1] < (lb[0] + lb[2]) / 2]; R = [l for l in labs if l[1] >= (lb[0] + lb[2]) / 2]
    for side, items in (('L', sorted(L)), ('R', sorted(R))):
        last = lb[1] + 30
        for ay, ax, text in items:
            ty = max(ay, last + 22); last = ty; f = F(12)
            if side == 'L': tx = lb[0] + 14; d.text((tx, ty - 8), text, font=f, fill=INK); lx = tx + d.textlength(text, font=f) + 6
            else: tw = d.textlength(text, font=f); tx = lb[2] - 14 - tw; d.text((tx, ty - 8), text, font=f, fill=INK); lx = tx - 6
            d.line([(lx, ty), (ax, ay)], fill=ACC); d.ellipse([ax - 3, ay - 3, ax + 3, ay + 3], fill=ACC)
    # atlas
    ab = (1116, 580, W - 28, 1240); d.rectangle(ab, fill=(255, 255, 255), outline=(205, 203, 214))
    d.text((ab[0] + 14, ab[1] + 12), f'TEXTURE ATLAS  (128 x 128, 2 px per model pixel)   textures/block/machines/{name}.png', font=F(15, True), fill=INK)
    k = 4; tx, ty = ab[0] + 16, ab[1] + 44
    for yy in range(0, 128 * k, 8):
        for xx in range(0, 128 * k, 8): d.rectangle([tx + xx, ty + yy, tx + xx + 7, ty + yy + 7], fill=(236, 236, 236) if (xx // 8 + yy // 8) % 2 else (250, 250, 250))
    big = atlas.resize((128 * k, 128 * k), Image.NEAREST); im.paste(big, (tx, ty), big)
    for x0, y0, w, h, n, f, mat in rects:
        if w * k >= 10 and h * k >= 10: d.rectangle([tx + x0 * k, ty + y0 * k, tx + (x0 + w) * k - 1, ty + (y0 + h) * k - 1], outline=(124, 92, 230, 255))
    gx = tx + 128 * k + 20; d.text((gx, ty), 'Glowmask', font=F(12, True), fill=INK)
    d.rectangle([gx, ty + 18, gx + 256, ty + 18 + 256], fill=(24, 24, 28)); gm = glowmask.resize((256, 256), Image.NEAREST); im.paste(gm, (gx, ty + 18), gm)
    yy = ty + 290
    for ln in ['Every face has its own island; purple boxes', 'outline the larger ones. Glowing faces are', 'baked with neoforge_data light 15 (no extra', 'emissive texture needed).']:
        d.text((gx, yy), ln, font=F(12), fill=SUB); yy += 17
    # text blocks
    y = 1262; cw = (W - 56 - 40) // 3
    for i, (h, body) in enumerate(text_blocks):
        x = 28 + i * (cw + 20); d.text((x, y), h, font=F(18, True), fill=INK); yy = y + 34
        for para in body:
            bullet = para.startswith('- ')
            for j, ln in enumerate(wrap(d, para[2:] if bullet else para, F(13), cw - (16 if bullet else 0))):
                if bullet and j == 0: d.text((x, yy), '•', font=F(13), fill=INK)
                d.text((x + (16 if bullet else 0), yy), ln, font=F(13), fill=INK); yy += 19
            yy += 6
        ymax = max(locals().get('ymax', 0), yy)
    im.crop((0, 0, W, ymax + 30)).save(path)


def before_after(old_models, new_models, path):
    W = 2240; im = Image.new('RGB', (W, 760), BG); d = ImageDraw.Draw(im)
    d.text((28, 20), 'Genetic Splicer and Geno Station  —  before and after', font=F(30, True), fill=INK)
    x = 28
    for (lab, mdl, tex, glow), tag in zip(old_models + new_models, ['before', 'before', 'after', 'after']):
        box = (x, 80, x + 532, 730); d.rectangle(box, fill=(255, 255, 255), outline=(205, 203, 214))
        d.text((box[0] + 14, box[1] + 12), f'{lab}  ({tag})', font=F(16, True), fill=INK if tag == 'after' else SUB)
        r = render(mdl, tex, Cam(-35, 26, 20), bg=(255, 255, 255), emissive=glow)
        im.paste(r, (box[0] + (532 - r.width) // 2, box[1] + 60 + (560 - r.height) // 2), r); x += 548
    im.save(path)


# ------------------------------------------------------------------ spec
SPEC = """# Orbital-Bees genetics: Genetic Splicer and Geno Station (redesign)

Mod: ZeroG Orbital-Bees (`aeroapiary`), Productive Bees add-on. Block ids stay `aeroapiary:genetic_splicer` and `aeroapiary:geno_station`.

## What exists today (found in the repo)

- Shipped in `zerog-binnie-expansion-1.21.1-1.0.0.jar` (on `Docs`); design sources in `Design` `docs/asset-collection-1.21.1/bees/` and `docs/art-rollout-v3/`.
- Old models: Splicer = 12-cube grey cabinet with a 3-rung helix hidden inside; Geno Station = 15-cube console with a cyan screen. Textures are flat swatches.
- **Old behaviour is placeholder** (from `ZeroGMachines`):
  - Genetic Splicer: slots accept queen (0), drone (1), frame (2), but `tick` runs `processTwo(0, 1, 3, frameInfusionRecipe)`.
  - Geno Station: slot 0 accepts combs only, and `tick` runs `processTwo(0, 0, 1, stardustSmelterRecipe)`.
  - Neither touches genes. The redesign below gives both a real job.

## The genetics loop

1. **Geno Station (read and sample):** put in a bee and a blank Serum Vial; it analyses the bee and draws one chosen trait into the vial, giving a **Trait Serum** that names the trait and value (e.g. "Speed: Fast").
2. **Genetic Splicer (write):** put in a queen or princess and a Trait Serum; it writes that trait into both chromosomes of the bee.

This is the Gendustry sampler/imprinter idea (Binnie isolator/inoculator in the old packs), kept to two blocks.

## Geno Station

| Slot | Index | Accepts | Notes |
| --- | --- | --- | --- |
| Specimen | 0 | any Productive Bees bee item (queen, princess, drone) | Returned to slot 3 after analysis, unless sampling consumes it |
| Blank vial | 1 | `serum_vial` | One per sample |
| Reagent | 2 | `honey_drop` (or honey bottle) | 1 per analysis, 1 per sample |
| Specimen out | 3 | output | Analysed bee (genome now readable in tooltips) |
| Serum out | 4 | output | `trait_serum` with a `aeroapiary:trait` data component {gene, value} |

- Mode buttons: **Analyse** (reagent only; reveals the genome) or **Sample** (choose a gene from the list on the screen; consumes the vial and reagent).
- Sampling a **drone** never kills it; sampling a princess or queen has a 25% chance to lower its fertility by 1 (needs care).
- Power: 20 FE/t; Analyse 100 ticks, Sample 300 ticks. Works without power at quarter speed (old packs let you hand-crank; here it is just slow).
- Screen (the glowing monitor on the model) shows the genome bars; in the GUI it is the gene list.

## Genetic Splicer

| Slot | Index | Accepts | Notes |
| --- | --- | --- | --- |
| Bee | 0 | queen or princess | The target |
| Serum | 1 | `trait_serum` | Consumed; empty `serum_vial` returns to slot 3 |
| Catalyst | 2 | `royal_jelly` (normal), `cosmic_jelly` (double chance) | Consumed per attempt |
| Bee out | 3 | output | Spliced bee |
| Vial out | 4 | output | Empty vial |

- Success 75% with royal jelly, 100% with cosmic jelly. A failed attempt keeps the bee and wastes the serum.
- Power: 60 FE/t, 400 ticks. Royal jelly feed also comes in by pipe through the back conduit (fluid, 250 mB per attempt) when the pack has the Transport fluid pipes.
- Rules: one trait per serum; species cannot be spliced (keeps mutations meaningful); traits above the bee's tier cap need the Quantum Queen Chamber research (optional).

## Code fix

- Replace the two placeholder `tick` branches in `ZeroGMachines` with `GenoStationLogic.tick` and `GeneticSplicerLogic.tick`; give each its own slot rules in `mayPlaceIn` (tables above) and its own layout in `MachineSlotLayouts`.
- Add the data component `aeroapiary:trait` (codec: gene id + value) and make `trait_serum` show it in its name and tooltip.
- Read and write genes through the Productive Bees bee-data API (the gene keys it already uses), so serums stay compatible with its breeding.
- Splicer: a `GeoBlockRenderer` draws `genetic_splicer_helix.geo.json` (idle spin when powered, fast spin and bob while working). The baked block model has no rungs, so the helix is never drawn twice.

## Files

| File | Use |
| --- | --- |
| `models/block/other/genetic_splicer.json`, `geno_station.json` | New baked models (translucent render type; glowing parts use `neoforge_data` light 15) |
| `textures/block/machines/genetic_splicer.png`, `geno_station.png` | 128 x 128 atlases, 2 px per model pixel |
| `textures/block/machines/*_glowmask.png` | For shaders/emissive layers; the models already glow without them |
| `blockstates/genetic_splicer.json`, `geno_station.json` | Now with `facing` (north, east, south, west); the block needs `HORIZONTAL_FACING`, which `ZeroGMachineBlock` already has |
| `geo/machines/genetic_splicer_helix.geo.json`, `animations/genetic_splicer_helix.animation.json`, `textures/block/machines/genetic_splicer_helix.png` | Animated helix |
| `models/item/*.json` | Parent the block model |

Old textures (`genetic_splicer_hd*.png`, `other/geno_station*.png`) can stay in the jar; nothing points to them after this, and no ids change.
"""


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    A = f'{OUT}/assets/{NS}'
    built = {}
    for name, els, title, sub in (
            ('genetic_splicer', splicer(), 'Genetic Splicer', 'aeroapiary:genetic_splicer · writes a Trait Serum into a queen or princess · full block, 16 px tall · glass chamber with a spinning DNA helix'),
            ('geno_station', geno(), 'Geno Station', 'aeroapiary:geno_station · analyses bees and draws one trait into a Serum Vial · full block · analysis bench')):
        model, atlas, gm, rects = build(name, els)
        baked = dict(model); baked['elements'] = [e for e in model['elements'] if not e['name'].startswith('rung_')]
        for p, obj in ((f'{A}/models/block/other/{name}.json', baked), (f'{A}/blockstates/{name}.json', blockstate(name)),
                       (f'{A}/models/item/{name}.json', {'parent': f'{NS}:block/other/{name}_inventory' if name == 'genetic_splicer' else f'{NS}:block/other/{name}'})):
            os.makedirs(os.path.dirname(p), exist_ok=True); json.dump(obj, open(p, 'w'), indent=1)
        if name == 'genetic_splicer':                       # inventory model keeps the rungs so the item shows the helix
            json.dump(model, open(f'{A}/models/block/other/{name}_inventory.json', 'w'), indent=1)
        os.makedirs(f'{A}/textures/block/machines', exist_ok=True)
        atlas.save(f'{A}/textures/block/machines/{name}.png'); gm.save(f'{A}/textures/block/machines/{name}_glowmask.png')
        built[name] = (model, atlas, gm, rects, els, title, sub)
    os.makedirs(f'{A}/geo/machines', exist_ok=True); os.makedirs(f'{A}/animations', exist_ok=True)
    json.dump(helix_geo(splicer()), open(f'{A}/geo/machines/genetic_splicer_helix.geo.json', 'w'), indent=1)
    json.dump(helix_anim(), open(f'{A}/animations/genetic_splicer_helix.animation.json', 'w'), indent=1)
    helix_tex().save(f'{A}/textures/block/machines/genetic_splicer_helix.png')
    texts = {
        'genetic_splicer': [('What it does', ['Writes one trait into a bee. Bee (queen or princess) + Trait Serum + Royal Jelly in; spliced bee and an empty vial out.',
                                              '- 75% success with Royal Jelly, 100% with Cosmic Jelly; failure keeps the bee, loses the serum.', '- 60 FE/t, 400 ticks. Species can never be spliced.']),
                            ('Look', ['A lab apparatus, not a cabinet: the bee\'s genes are visibly worked on.', '- Glass chamber with a floating DNA helix (cyan and amber strands) that spins in game.',
                                      '- Two injector arms; the right one carries the serum vial in use (its colour = the trait family).', '- Copper resonance coil with a violet top; brass step and control console with a splice screen.',
                                      '- Royal-jelly feed tube on the back (fluid input).']),
                            ('Build notes', ['- Baked model without the rungs + GeckoLib helix (genetic_splicer_helix.geo.json) drawn by the block entity renderer.',
                                             '- Render type translucent for the glass; glowing elements use neoforge_data light 15.', '- Item model = block model with the rungs, so the inventory icon shows the helix.',
                                             '- Blockstate now has facing; model faces north.'])],
        'geno_station': [('What it does', ['Reads genes and samples them. Analyse a bee (honey drop) to reveal its genome, or Sample one chosen gene into a blank Serum Vial to make a Trait Serum.',
                                           '- Drones are never harmed; queens/princesses may lose 1 fertility (25%).', '- 20 FE/t; Analyse 100 ticks, Sample 300 ticks; quarter speed unpowered.']),
                         ('Look', ['An analysis bench: everything is on top, the cabinet is storage.', '- Genome monitor leaning back, showing one glowing bar per chromosome.',
                                   '- Scanner arm over a glass specimen dish with a bee; violet lens glows.', '- Rack of three trait serums (green, violet, amber) and a honey reagent tank.',
                                   '- Honeycomb cabinet doors, brass worktop, keyboard.']),
                         ('Build notes', ['- One baked model, 17 parts, translucent render type; no animation needed (optional: scanner head bob via a small GeckoLib bone later).',
                                          '- Blockstate gains facing; ZeroGMachineBlock already has HORIZONTAL_FACING.', '- The old geno_station textures can stay; nothing points to them.'])]}
    for i, (name, (model, atlas, gm, rects, els, title, sub)) in enumerate(built.items()):
        sheet(name, title, sub, els, model, atlas, gm, rects, texts[name], f'{OUT}/{i + 1:02d}_{name}_sheet.png')
    if OLD:
        J = f'{OLD}/assets/aeroapiary/'
        olds = []
        for nm, lab, tx in (('genetic_splicer', 'Genetic Splicer', {'base': 'textures/block/machines/genetic_splicer_hd.png', 'emissive': 'textures/block/machines/genetic_splicer_hd_emissive.png'}),
                            ('geno_station', 'Geno Station', {'base': 'textures/block/other/geno_station.png', 'emissive': 'textures/block/other/geno_station_emissive.png'})):
            olds.append((lab, json.load(open(J + f'models/block/other/{nm}.json')), {k: Image.open(J + v).convert('RGBA') for k, v in tx.items()}, {'emissive'}))
        news = [('Genetic Splicer', built['genetic_splicer'][0], {'all': built['genetic_splicer'][1]}, set()),
                ('Geno Station', built['geno_station'][0], {'all': built['geno_station'][1]}, set())]
        before_after(olds, news, f'{OUT}/00_before_after.png')
    open(f'{OUT}/genetics_machines_spec.md', 'w').write(SPEC)
    print('ok', {k: len(v[0]['elements']) for k, v in built.items()})
