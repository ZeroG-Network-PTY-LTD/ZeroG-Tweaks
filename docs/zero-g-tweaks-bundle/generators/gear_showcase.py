"""3D gear showcase sheets: each armor set on an armor stand (current GeckoLib model and the recommended
chunky shell), the five tools as 3D extruded models, and modelling notes for armor and tools.
Writes docs/zero-g-tweaks-bundle/sheets/gear/showcase/<nn>_<set>.png and 00_all_sets.png"""
import json, os, re, sys, textwrap
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render3d import Scene
from data import M

REPO = '/home/claude/zerog-tweaks'
A = f'{REPO}/src/main/resources/assets/zerog_tweaks'
OUT = f'{REPO}/docs/zero-g-tweaks-bundle/sheets/gear/showcase'
os.makedirs(OUT, exist_ok=True)
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'armor_sheet.py')).read()
ns = {}
for name in ('PERK', 'STR', 'TIER'):
    m = re.search(rf'^{name}=\{{.*?\}}$', src, re.M | re.S); exec(m.group(0), ns)
PERK, STR, TIER = ns['PERK'], ns['STR'], ns['TIER']
SETS = ['nullifite', 'ferrox', 'moonsteel', 'olympium', 'cobaltium', 'cyrrium', 'aurelion', 'cerulite', 'ruskite', 'tectium', 'pyrium',
        'skarnite', 'salvium', 'wraithsteel', 'palladine', 'eidolite', 'photium', 'astrium', 'radiantine', 'solvanite']
WORLD = {**{k: 'Sol' for k in SETS[:4]}, **{k: 'Cerulon (Galaxy 2)' for k in SETS[4:8]}, **{k: 'Skarn (Galaxy 3)' for k in SETS[8:12]},
         **{k: 'Eidolon (Galaxy 4)' for k in SETS[12:16]}, **{k: 'Solvane (Galaxy 5)' for k in SETS[16:]}}
H = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
F = lambda s, b=False: ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if b else ""}.ttf', s)
WOOD, STONE = (170, 128, 82), (128, 128, 132)

def stand(s):
    s.solid((-6, -1, -6), (12, 1, 12), STONE, 0.18, 1)
    s.solid((-1, 0, -1), (2, 23, 2), WOOD, 0.12, 2)
    s.solid((-6, 20.5, -1.5), (12, 2, 3), WOOD, 0.12, 3)

def armor(s, k, chunky):
    g = json.load(open(f'{A}/geckolib/models/item/armor/{k}.geo.json'))['minecraft:geometry'][0]
    tex = Image.open(f'{A}/textures/item/armor/{k}.png').convert('RGBA')
    gp = f'{A}/textures/item/armor/{k}_glowmask.png'
    glow = Image.open(gp).convert('RGBA') if os.path.exists(gp) else None
    for b in g['bones']:
        for c in b.get('cubes', []):
            s.box_uv(c['origin'], c['size'], c['uv'], tex, c.get('inflate', 0) or 0, c.get('mirror', False), glow)
    if chunky:
        pal = [H(c) for c in M[k]['pal']]      # outline, dark, mid, light, highlight, accent
        dark, mid, light, hi, acc = pal[1], pal[2], pal[3], pal[4], pal[5]
        for sx in (-1, 1):                     # layered pauldrons over each shoulder
            x = -10.2 if sx < 0 else 4.2
            s.solid((x - (0.3 if sx < 0 else -0.3), 20.6, -3.5), (6.6, 2.6, 7), mid, .12, 11 + sx)    # pauldron base plate
            s.solid((x + (0.6 if sx < 0 else -0.6), 23.2, -2.8), (5.4, 1.8, 5.6), light, .12, 13 + sx)  # pauldron dome
            s.solid((-9.3 if sx < 0 else 2.7, 12.2, -3.3), (6.6, 3.0, 6.6), mid, .1, 15 + sx)           # bracers wrap the wrist
            s.solid((-3.6 if sx < 0 else -0.4, 5.2, -2.95), (4, 2.6, 1), light, .15, 17 + sx)         # knee plates
            s.solid((-4.4 if sx < 0 else -0.6, 2.6, -2.8), (5, 1.4, 5.6), mid, .15, 19 + sx)          # boot cuffs
        s.solid((-4.8, 15.2, -3.6), (9.6, 7.6, 1.2), mid, .2, 21)       # raised breastplate
        s.solid((-1.8, 17.6, -4.4), (3.6, 3.6, 1), acc, .1, 22)          # core gem (glows)
        s.solid((-1.1, 18.3, -4.9), (2.2, 2.2, 0.6), hi, .05, 23)
        s.solid((-5.0, 12.0, -3.0), (10, 1.6, 6), dark, .15, 24)         # belt
        s.solid((-4.8, 31.4, -4.8), (9.6, 1.6, 9.6), light, .15, 25)     # helmet crown ridge
        s.solid((-1, 33, -4.4), (2, 2.6, 8), acc, .1, 26)                # crest
        s.solid((-5.2, 26.4, -5.3), (10.4, 1.2, 1), light, .12, 27)      # brow / visor rim

def tool_voxels(s, k, tool, center, scale, rot):
    spr = Image.open(f'{A}/textures/item/{k}_{tool}.png').convert('RGBA')
    pal = [H(c) for c in M[k]['pal']]
    acc = pal[5]
    def thick(x, y, c):
        d = abs(x - (15 - y))                      # distance from the handle diagonal (bottom-left to top-right)
        t = (x + (15 - y)) / 30                    # position along it, 0 = butt, 1 = tip
        if sum((a - b) ** 2 for a, b in zip(c[:3], acc)) < 1800: return 3.0   # gems and accents stand out
        if t < 0.52 and d <= 1: return 1.4         # handle
        return 2.4                                 # head / blade
    s.extrude(spr, center, scale, 1.4, rot, thickness_fn=thick)

def fit(img, mw, mh):
    f = min(mw / img.width, mh / img.height, 1.0)
    return img if f >= 1 else img.resize((max(1, int(img.width * f)), max(1, int(img.height * f))), Image.LANCZOS)

def render_armor(k, chunky, yaw, scale=14):
    s = Scene(yaw=yaw, pitch=14); stand(s); armor(s, k, chunky); return s.render(scale)

def render_tool(k, tool, rot=0, yaw=-28):
    s = Scene(yaw=yaw, pitch=16)
    tool_voxels(s, k, tool, (0, 0, 0), 1.0, rot)
    return s.render(24, pad=4)

BG, PANEL, INK, SUB, LINE = (16, 16, 20), (26, 26, 32), (238, 240, 248), (168, 174, 192), (58, 60, 74)
ARMOR_NOTES = [
    'Chunky, layered look: every piece is the vanilla armor box plus extra shell cubes on top, so the armor reads as heavy plate, not painted skin.',
    'Helmet: inflate 1.0, plus a crown ridge, a brow rim over the visor and a crest in the set\'s accent colour.',
    'Chestplate: inflate 1.01, a raised breastplate, a glowing core gem in the centre, layered pauldrons (two stacked cubes per shoulder) and gauntlet cuffs.',
    'Leggings: inflate 0.5 with a belt and knee plates. Boots: inflate 1.0 with a flared cuff.',
    'The gem, visor and accent lines go on the glowmask so they light up in the dark.',
    'Keep every extra cube on the matching GeckoLib armor bone (armorHead, armorBody, armorRightArm ...) so it follows the player.',
]
TOOL_NOTES = [
    'Held tools are 3D models, not flat sprites: the 16x16 icon is extruded into voxels.',
    'Handle 1-1.5 px thick; head and blade 2-2.5 px; gems and accent pixels 3 px so they stand proud.',
    'Keep the flat 16x16 texture for the inventory (gui display) and use the 3D model in hand and on armor stands.',
    'Scale the in-hand model up about 1.5x (display "thirdperson_righthand" and "firstperson_righthand") so the weapons feel oversized, like the reference.',
    'The sword blade glows along its edge and the guard carries the set gem.',
]

def sheet(n, k):
    name = M[k]['name']
    a1 = render_armor(k, False, -30); a2 = render_armor(k, True, -30); a3 = render_armor(k, True, 150)
    tools = {t: render_tool(k, t) for t in ('axe', 'pickaxe', 'shovel', 'hoe')}
    sword = render_tool(k, 'sword', 0, -34).resize((460, 460), Image.NEAREST) if False else render_tool(k, 'sword', 0, -34)
    W = 1800; Hh = 1500
    im = Image.new('RGBA', (W, Hh), BG + (255,)); d = ImageDraw.Draw(im)
    d.text((40, 30), f'{name}  -  armor and tools in 3D', font=F(40, True), fill=INK)
    sub = f'{WORLD[k]}  ·  {TIER.get(k, "metal set")}  ·  strength: {STR[k]}  ·  full-set perk: {PERK[k]}'
    d.text((40, 84), sub, font=F(19), fill=SUB)
    # armor stands
    d.rounded_rectangle((30, 130, W - 30, 700), 16, fill=PANEL + (255,))
    labels = ['Current GeckoLib model', 'Recommended chunky shell', 'Chunky shell, back']
    for i, (img, lab) in enumerate(zip((a1, a2, a3), labels)):
        cx = 30 + (W - 60) * (i * 2 + 1) // 6
        img = fit(img, 520, 480)
        im.alpha_composite(img, (cx - img.width // 2, 640 - img.height))
        tw = d.textlength(lab, font=F(18, True)); d.text((cx - tw / 2, 655), lab, font=F(18, True), fill=INK if i else SUB)
    # tools
    d.rounded_rectangle((30, 720, 1080, 1470), 16, fill=PANEL + (255,))
    d.text((50, 735), 'Tools as 3D models', font=F(22, True), fill=INK)
    for i, t in enumerate(('axe', 'pickaxe', 'shovel', 'hoe')):
        img = fit(tools[t], 230, 230); cx = 160 + i * 250
        im.alpha_composite(img, (cx - img.width // 2, 1000 - img.height))
        tw = d.textlength(t.capitalize(), font=F(16, True)); d.text((cx - tw / 2, 1010), t.capitalize(), font=F(16, True), fill=SUB)
    big = fit(sword, 600, 390)
    im.alpha_composite(big, (555 - big.width // 2, 1440 - big.height))
    d.text((70, 1420), 'Sword', font=F(16, True), fill=SUB)
    # notes
    x0 = 1100; y = 740
    d.text((x0, y - 5), 'How to model the armor', font=F(22, True), fill=INK); y += 36
    for note in ARMOR_NOTES:
        for i, line in enumerate(textwrap.wrap(note, 58)):
            d.text((x0 + (0 if i == 0 else 16), y), ('• ' if i == 0 else '') + line, font=F(16), fill=SUB); y += 22
        y += 6
    y += 14
    d.text((x0, y), 'How to model the tools', font=F(22, True), fill=INK); y += 36
    for note in TOOL_NOTES:
        for i, line in enumerate(textwrap.wrap(note, 58)):
            d.text((x0 + (0 if i == 0 else 16), y), ('• ' if i == 0 else '') + line, font=F(16), fill=SUB); y += 22
        y += 6
    im.convert('RGB').save(f'{OUT}/{n:02d}_{k}.png')
    return a2

stands = []
for n, k in enumerate(SETS, 1):
    stands.append((k, sheet(n, k))); print('sheet', k)

# overview: every set on its stand, grouped by world, like a display row
cols = 10; cw = 170
W = 40 + cols * cw; Hh = 150 + 2 * 360
im = Image.new('RGBA', (W, Hh), BG + (255,)); d = ImageDraw.Draw(im)
d.text((30, 26), 'ZeroG armor sets on display (recommended chunky shell)', font=F(34, True), fill=INK)
d.text((30, 76), 'Sol · Cerulon · Skarn · Eidolon · Solvane, in progression order', font=F(18), fill=SUB)
for i, (k, img) in enumerate(stands):
    x = 20 + (i % cols) * cw + cw // 2; y = 130 + (i // cols) * 360
    sm = fit(img, 160, 290)
    im.alpha_composite(sm, (x - sm.width // 2, y + 300 - sm.height))
    nm = M[k]['name']; tw = d.textlength(nm, font=F(16, True)); d.text((x - tw / 2, y + 310), nm, font=F(16, True), fill=INK)
im.convert('RGB').save(f'{OUT}/00_all_sets.png')
print('done')
