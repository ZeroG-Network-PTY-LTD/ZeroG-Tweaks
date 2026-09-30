"""Tidewraith face redesign: 16x12 front-face textures (3 options) in the Blockbench build's teal palette,
rendered on a head box, plus a before/after sheet.
Writes docs/shattered-skies/textures/tidewraith_face_*.png and sheets/tidewraith_face_redesign.png"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from render3d import Scene

REPO = '/home/claude/zerog-tweaks'
OUTT = f'{REPO}/docs/shattered-skies/textures'
OUTS = f'{REPO}/docs/shattered-skies/sheets'
BEFORE = '/root/.claude/uploads/23345d11-2ce7-53a5-9128-b35ae672adbe/39c961ba-image.png'
F = lambda s, b=False: ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if b else ""}.ttf', s)

# colours sampled from the Blockbench screenshot, plus a few new shades
P = {
    '.': (18, 62, 66),     # skin
    ',': (37, 118, 113),   # skin speckle / manta spot
    'd': (11, 40, 46),     # skin shadow (edge bevel)
    'b': (6, 24, 29),      # brow / socket dark
    'k': (3, 12, 16),      # mouth interior
    'g': (113, 208, 178),  # eye glow (same as the build)
    'G': (200, 255, 238),  # eye hot core
    'h': (44, 120, 106),   # glow halo
    'r': (34, 78, 82),     # gill rakers (dark, so they don't read as teeth)
    'p': (138, 180, 176),  # pale underside
    'q': (104, 150, 148),  # pale underside shade
    'l': (84, 132, 134),   # light gill line
    'v': (201, 168, 255),  # splinter crack (violet, as on the rest of the mob)
    'V': (122, 92, 190),   # crack dim
    'c': (216, 106, 106),  # coral
    'C': (255, 194, 176),  # coral light
}
GLOW = set('gGvhC')  # pixels for the _glowmask (emissive) layer; h is dim glow

FACES = {
 'manta': ("A  Manta (recommended)",
  "Slanted slit eyes pushed to the outer corners, a wide filter-feeder mouth with gill rakers instead of teeth, pale chin like a ray's belly, and a violet splinter crack down the brow.",
  ["dd,.....v.....dd",
   "d.....,.V..,...d",
   "dbbb....v...bbbd",
   "dGgh...VV...hgGd",
   "d.gg,......,gg.d",
   "d..h.,....,.h..d",
   "d,............,d",
   "dd.kkkkkkkkkk.dd",
   "d.krkrkrrkrkrk.d",
   "d.krkrkrrkrkrk.d",
   "dqqkkkkkkkkkkqqd",
   "ddqppppppppppqdd"]),
 'wraith': ("B  Wraith",
  "Deep hollow sockets with a single pin-point pupil each, no teeth, and a ragged jaw that hangs open with a faint glow inside. Spookiest of the three.",
  ["dd....,..,....dd",
   "d..............d",
   "dbbbbb....bbbbbd",
   "dbkkkb.v..bkkkbd",
   "dbkGkb.V..bkGkbd",
   "dbkhkb....bkhkbd",
   "d.bbb..,,..bbb.d",
   "d..............d",
   "d.kkkkkkkkkkkk.d",
   "d.khkkkhhkkkhk.d",
   "d.k.kk.kk.kk.k.d",
   "dd.q.qq..qq.q.dd"]),
 'reef': ("C  Reef",
  "Calmer: round glowing eyes under a coral brow, a closed curved mouth line, and three gill slits on each cheek. Reads as a creature rather than a monster.",
  ["dd,cCc....cCc,dd",
   "d.ccccc..ccccc.d",
   "d..bbb....bbb..d",
   "d.bgGgb..bgGgb.d",
   "d.bhghb..bhghb.d",
   "d..bbb....bbb..d",
   "dl............ld",
   "d.l.kk....kk.l.d",
   "dl...kkkkkk...ld",
   "d.l..........l.d",
   "dqppppppppppppqd",
   "ddqqppppppppqqdd"]),
}

def tex(rows):
    assert len(rows) == 12 and all(len(r) == 16 for r in rows), [len(r) for r in rows]
    im = Image.new('RGBA', (16, 12)); gm = Image.new('RGBA', (16, 12), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            im.putpixel((x, y), P[ch] + (255,))
            if ch in GLOW: gm.putpixel((x, y), P[ch] + (255,))
    return im, gm

def skin_tex(w, h, seed):
    import random
    r = random.Random(seed); im = Image.new('RGBA', (w, h))
    for y in range(h):
        for x in range(w):
            c = P[',' if r.random() < .12 else '.']
            if x in (0, w - 1) or y in (0, h - 1): c = P['d']
            im.putpixel((x, y), c + (255,))
    return im

def head_render(face, scale=22):
    """head box 16 wide x 12 tall x 12 deep, face on the front (-z); small fins on top like the build."""
    s = Scene(yaw=-24, pitch=-12)
    W, H, D = 16, 12, 12
    x0, y0, z0 = -8, 0, -6
    x1, y1, z1 = x0 + W, y0 + H, z0 + D
    fp = face.load()
    s.face((x1, y1, z0), (-1, 0, 0), (0, -1, 0), W, H, lambda i, j: fp[W - 1 - i, j], (0, 0, -1),
           lambda i, j: FACE_GLOW[W - 1 - i, j][3] > 0)
    for key, P0, U, V, cols, rows, N in [
        ('e', (x1, y1, z1), (0, 0, -1), (0, -1, 0), D, H, (1, 0, 0)),
        ('w', (x0, y1, z0), (0, 0, 1), (0, -1, 0), D, H, (-1, 0, 0)),
        ('t', (x1, y1, z1), (-1, 0, 0), (0, 0, -1), W, D, (0, 1, 0))]:
        t = skin_tex(cols, rows, hash(key) & 255).load()
        s.face(P0, U, V, cols, rows, lambda i, j, t=t: t[i, j], N)
    for fx in (-7, 4):  # little fin nubs like the build
        s.solid((fx, y1, z0 + 1), (3, 2, 3), P[','], noise=.15, seed=fx)
    return s.render(scale, pad=16)

os.makedirs(OUTT, exist_ok=True)
renders = {}
for key, (title, desc, rows) in FACES.items():
    face, glow = tex(rows)
    face.save(f'{OUTT}/tidewraith_face_{key}.png'); glow.save(f'{OUTT}/tidewraith_face_{key}_glowmask.png')
    FACE_GLOW = glow.load()
    renders[key] = (title, desc, face, head_render(face))

# ---- sheet ----
BG, INK, SUB, LINE, CARD = (245, 244, 240), (30, 32, 38), (96, 100, 112), (205, 205, 215), (255, 255, 255)
before = Image.open(BEFORE).convert('RGB').crop((590, 160, 900, 420))
cw = 520
W =40 + 4 * (cw + 20) + 20
img = Image.new('RGB', (W, 1010), BG); d = ImageDraw.Draw(img)
d.text((40, 26), 'Tidewraith · face redesign', font=F(38, True), fill=INK)
d.text((40, 80), 'Front face of the head. 16 x 12 texture in the Blockbench build\'s teal palette, glowmask included. Pick one; A is the recommendation.',
       font=F(18), fill=SUB)

def cald(x, title, desc, big, small=None):
    d.rounded_rectangle((x, 130, x + cw, 980), 14, fill=CARD, outline=LINE, width=2)
    d.text((x + 20, 150), title, font=F(24, True), fill=INK)
    bw = cw - 40; bh = 420
    b = big.copy(); b.thumbnail((bw, bh), Image.NEAREST if big.width < 100 else Image.LANCZOS)
    dark = Image.new('RGB', (bw, bh), (190, 206, 214)); img.paste(dark, (x + 20, 195))
    img.paste(b, (x + 20 + (bw - b.width) // 2, 195 + (bh - b.height) // 2), b if b.mode == 'RGBA' else None)
    y = 635
    if small is not None:
        sm = small.resize((16 * 12, 12 * 12), Image.NEAREST)
        img.paste(sm, (x + 20, y)); d.rectangle((x + 20, y, x + 20 + sm.width, y + sm.height), outline=LINE)
        d.text((x + 230, y + 4), 'texture 16 x 12', font=F(15, True), fill=INK)
        d.text((x + 230, y + 26), '(12x zoom)', font=F(14), fill=SUB)
        y += sm.height + 20
    wolds, line, ly = desc.split(), '', y
    for w_ in wolds:
        if d.textlength(line + ' ' + w_, font=F(16)) > cw - 40:
            d.text((x + 20, ly), line.strip(), font=F(16), fill=SUB); ly += 24; line = ''
        line += ' ' + w_
    d.text((x + 20, ly), line.strip(), font=F(16), fill=SUB)

cald(40, 'Current', 'The goggle eyes and toothy grin read as a cartoon box face, not a ray. The whole front is one flat dark panel, so the head looks like a mask stuck on the body.', before)
for i, key in enumerate(['manta', 'wraith', 'reef']):
    t, desc, face, r = renders[key]
    cald(40 + (i + 1) * (cw + 20), t, desc, r, face)
img.save(f'{OUTS}/tidewraith_face_redesign.png'); print(img.size)

# ---- chosen face (A Manta) in each style's palette ----
def hx(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def mix(a, b, t): return tuple(int(x + (y - x) * t) for x, y in zip(a, b))
STYLES = {  # skin, speckle, eye glow, underside, crack
    'base':    dict(skin=P['.'], spot=P[','], glow=P['g'], pale=P['p'], crack=P['v']),
    'storm':   dict(skin=hx('#6b7682'), spot=hx('#8a9aa6'), glow=hx('#ffe066'), pale=hx('#e3e8ec'), crack=hx('#c9a8ff')),
    'abyssal': dict(skin=hx('#14233f'), spot=hx('#1f4f6a'), glow=hx('#6ff0ff'), pale=hx('#26395e'), crack=hx('#b58cff')),
    'pearl':   dict(skin=hx('#e4dfec'), spot=hx('#ffffff'), glow=hx('#f2a7c8'), pale=hx('#f6f3fa'), crack=hx('#b8e6f2'), dark=.6),
}
def style_pal(s):
    k = (0, 0, 0); f = s.get('dark', 1.0)   # pale styles use softer darks
    return {'.': s['skin'], ',': s['spot'], 'd': mix(s['skin'], k, .38 * f), 'b': mix(s['skin'], k, .65 * f), 'k': mix(s['skin'], k, .85 * f),
            'g': s['glow'], 'G': mix(s['glow'], (255, 255, 255), .6), 'h': mix(s['glow'], s['skin'], .6),
            'r': mix(s['skin'], k, .5 * f), 'p': s['pale'], 'q': mix(s['pale'], k, .22), 'v': s['crack'], 'V': mix(s['crack'], k, .4)}
rows = FACES['manta'][2]; strip = []
for name, s in STYLES.items():
    sp = style_pal(s)
    im = Image.new('RGBA', (16, 12)); gm = Image.new('RGBA', (16, 12), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            im.putpixel((x, y), sp[ch] + (255,))
            if ch in GLOW: gm.putpixel((x, y), sp[ch] + (255,))
    suffix = '' if name == 'base' else '_' + name
    im.save(f'{OUTT}/tidewraith{suffix}_face.png'); gm.save(f'{OUTT}/tidewraith{suffix}_face_glowmask.png')
    P_backup = dict(P); P.update(sp); FACE_GLOW = gm.load(); strip.append((name, im, head_render(im))); P.clear(); P.update(P_backup)
sh = Image.new('RGB', (40 + 4 * 420, 640), BG); d = ImageDraw.Draw(sh)
d.text((40, 24), 'Tidewraith face · Manta (chosen) in every style', font=F(32, True), fill=INK)
for i, (name, im, r) in enumerate(strip):
    x = 40 + i * 420
    r = r.copy(); r.thumbnail((380, 330), Image.LANCZOS)
    sh.paste(Image.new('RGB', (380, 330), (190, 206, 214)), (x, 90)); sh.paste(r, (x + (380 - r.width) // 2, 90 + (330 - r.height) // 2), r)
    sh.paste(im.resize((192, 144), Image.NEAREST), (x, 440))
    d.text((x + 210, 450), name.capitalize(), font=F(24, True), fill=INK)
    d.text((x + 210, 486), f"tidewraith{'' if name == 'base' else '_' + name}_face.png", font=F(13), fill=SUB)
sh.save(f'{OUTS}/tidewraith_face_styles.png'); print(sh.size)
