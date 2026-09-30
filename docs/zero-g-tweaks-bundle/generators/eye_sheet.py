"""Eye-style reference sheet: the four eye placements with front/side head diagrams, which mobs use each,
the Eye-of-Ender style eye recoloured per mob, and the guardian boss scale.
Writes docs/zero-g-tweaks-bundle/sheets/mobs/diagrams/eye_styles.png"""
import csv, json
from PIL import Image, ImageDraw, ImageFont

REPO = '/home/claude/zerog-tweaks'
M = f'{REPO}/docs/zero-g-tweaks-bundle/sheets/mobs'
F = lambda s, b=False: ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if b else ""}.ttf', s)
rows = list(csv.DictReader(open(f'{M}/data/mob_eye_styles.csv')))
eggs = {r['egg'].split(':')[1][:-10]: r for r in csv.DictReader(open(f'{REPO}/docs/zero-g-tweaks-bundle/data/spawn_eggs.csv'))}
H = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

BG, INK, SUB, LINE = (26, 28, 34), (236, 240, 250), (170, 178, 196), (70, 76, 92)
HEAD, HEAD_D, EYE, PUPIL = (120, 132, 150), (88, 98, 114), (240, 244, 250), (20, 22, 28)
W, Hh = 2000, 1560
img = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(img)
d.text((30, 22), 'Mob eye styles and boss scale', font=F(40, True), fill=INK)
d.text((30, 76), 'Where the eyes go on each mob. (SS) = Shattered Skies creature. Orange "proposed" = filled in to match the vanilla base; confirm before modelling.', font=F(20), fill=SUB)

def px(x, y, s, c, ox, oy):  # draw one "model pixel"
    d.rectangle((ox + x * s, oy + y * s, ox + x * s + s - 1, oy + y * s + s - 1), fill=c)

def head(style, ox, oy, s=10):
    """front view (left) and side view (right) of a 8x8 head with the style's eyes"""
    for view, dx in (('front', 0), ('side', 11)):
        for y in range(8):
            for x in range(8):
                px(dx + x, y + 3, s, HEAD if y < 7 else HEAD_D, ox, oy)
        if view == 'side':
            for y in range(4, 8): px(dx - 2, y + 2, s, HEAD_D, ox, oy); px(dx - 1, y + 2, s, HEAD_D, ox, oy)  # snout, facing left
        eyes = []
        if style == 'front' and view == 'front': eyes = [(1, 6), (5, 6)]
        if style == 'side' and view == 'side': eyes = [(3, 5)]
        if style == 'side' and view == 'front': eyes = [(0, 5), (7, 5)]  # just the edge of each eye
        if style == 'ender_eye' and view == 'front': eyes = [(3, 5)]
        if style == 'ender_eye' and view == 'side': eyes = []
        for ex, ey in eyes:
            w = 1 if (style == 'side' and view == 'front') else 2
            for a in range(w):
                for b in range(2): px(dx + ex + a, ey + b, s, EYE, ox, oy)
            px(dx + ex + (w - 1), ey + 1, s, PUPIL, ox, oy)
        if style == 'stalk':
            for sx in ((2, 5) if view == 'front' else (4,)):
                for y in range(0, 3): px(dx + sx, y, s, HEAD_D, ox, oy)
                px(dx + sx, -1, s, EYE, ox, oy); px(dx + sx - (0 if view == 'front' else 0), -2, s, EYE, ox, oy)
                px(dx + sx, -1, s, PUPIL, ox, oy)
        d.text((ox + dx * s, oy + 12 * s), view, font=F(15), fill=SUB)

TITLES = {'side': 'Side-set eyes', 'front': 'Front-facing eyes', 'ender_eye': 'Single Eye-of-Ender eye', 'stalk': 'Eyes on stalks above the head'}
RULES = {'side': 'Prey and grazer look (cow, horse, fish). One eye each side, set back from the snout.',
         'front': 'Predator and humanoid look (wolf, spider, illagers). Both eyes on the front face.',
         'ender_eye': 'One central eye styled on the vanilla Eye of Ender, recoloured per mob, emissive.',
         'stalk': 'Crab and snail look. Each stalk is its own bone and swivels in idle.'}
panel_w, panel_h = 960, 330
for n, style in enumerate(('side', 'front', 'ender_eye', 'stalk')):
    ox, oy = 30 + (n % 2) * (panel_w + 20), 120 + (n // 2) * (panel_h + 20)
    d.rounded_rectangle((ox, oy, ox + panel_w, oy + panel_h), 14, outline=LINE, width=2)
    d.text((ox + 20, oy + 14), TITLES[style], font=F(28, True), fill=INK)
    d.text((ox + 20, oy + 52), RULES[style], font=F(17), fill=SUB)
    head(style, ox + 40, oy + 110)
    names = [r for r in rows if r['eye_style'] == style]
    for j, r in enumerate(names):
        tag = ' (proposed)' if r['source'] == 'proposed' else ''
        mod = ' (SS)' if r['mod'] == 'shattered_skies' else ''
        cx, cy = ox + 290 + (j // 9) * 330, oy + 96 + (j % 9) * 24
        d.text((cx, cy), f"{r['name']}{mod}{tag}", font=F(17, not tag), fill=(255, 205, 140) if tag else INK)

# Eye of Ender style eyes, recoloured per mob (original pixel art in the style, not a copy of the vanilla texture)
oy = 820
d.text((30, oy), 'Eye-of-Ender style eye, recoloured per mob', font=F(28, True), fill=INK)
d.text((30, oy + 38), 'Round orb with a dark rim, a two-tone iris in the mob colour, a dark vertical slit pupil and one highlight. Goes on the glowmask.', font=F(17), fill=SUB)
ORB = ["....XXXX....", "..XXOOOOXX..", ".XOOIIIIOOX.", ".XOIIIIIIOX.", "XOIIHPIIIIOX", "XOIIIPIIIIOX", "XOIIIPIIIIOX", "XOIIIPIIIIOX",
       ".XOIIPIIIOX.", ".XOOIIIIOOX.", "..XXOOOOXX..", "....XXXX...."]
ender = [r for r in rows if r['eye_style'] == 'ender_eye']
for i, r in enumerate(ender):
    k = r['mob']
    if k in eggs: iris = H(eggs[k]['spots'])
    else: iris = H(json.load(open(f'{REPO}/docs/shattered-skies/models/{k}.json'))['palette'].get('splinter', '#c9a8ff'))
    outer = tuple(int(c * .55) for c in iris); rim = tuple(int(c * .25) for c in iris)
    cols = {'X': rim, 'O': outer, 'I': iris, 'P': (18, 16, 22), 'H': (255, 255, 255)}
    ox = 40 + i * 240; s = 14
    for y, line in enumerate(ORB):
        for x, c in enumerate(line):
            if c != '.':
                d.rectangle((ox + x * s, oy + 90 + y * s, ox + x * s + s - 1, oy + 90 + y * s + s - 1), fill=cols[c])
    d.text((ox, oy + 270), r['name'], font=F(17, True), fill=INK)
    if r['source'] == 'proposed': d.text((ox, oy + 292), 'proposed', font=F(15), fill=(255, 205, 140))

# boss scale
oy = 1160
d.text((30, oy), 'Guardian boss scale: 6x the player', font=F(28, True), fill=INK)
d.text((30, oy + 38), 'Prism Sentinel, Rift Tyrant, Eidolon Captain and The Dying Star are built at six times player size: 3.6 blocks wide, 10.8 blocks tall.', font=F(17), fill=SUB)
base_y = oy + 360; s = 18
def figure(x, w, h, col, label):
    d.rectangle((x, base_y - h * s, x + w * s, base_y), outline=col, width=3)
    d.text((x, base_y + 8), label, font=F(16, True), fill=INK)
figure(60, 0.6, 1.8, (140, 200, 255), 'Player')
figure(160, 3.6, 10.8, (200, 150, 255), 'Boss')
for k in range(0, 12, 2):
    y = base_y - k * s; d.line((40, y, 260, y), fill=LINE); d.text((12, y - 9), str(k), font=F(13), fill=SUB)
d.text((340, oy + 90), 'Tidewraith (Shattered Skies)', font=F(22, True), fill=INK)
d.text((340, oy + 122), 'Build it on the vanilla Phantom model: same rig and flight animations,', font=F(17), fill=SUB)
d.text((340, oy + 146), 'retextured with pixel scales and manta-ray gill slits on the underside.', font=F(17), fill=SUB)
d.text((340, oy + 200), 'Mini-bosses (Frost Warden, Sun Colossus) and the Shattered Skies bosses keep their own sizes.', font=F(17), fill=SUB)
img.save(f'{M}/diagrams/eye_styles.png'); print('ok')
