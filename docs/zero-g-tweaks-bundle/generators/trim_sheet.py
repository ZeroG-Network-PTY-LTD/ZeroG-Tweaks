"""Preview sheet for the ZeroG armor trims: every pattern on armor, recoloured by trim materials,
plus the 20 material palettes and the template items. Writes docs/zero-g-tweaks-bundle/sheets/gear/armor_trims.png"""
import os
from PIL import Image, ImageDraw, ImageFont

REPO = '/home/claude/zerog-tweaks'
T = f'{REPO}/src/main/resources/assets/zerog_tweaks/textures'
OUT = f'{REPO}/docs/zero-g-tweaks-bundle/sheets/gear'
F = lambda s, b=False: ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if b else ""}.ttf', s)
KEY = [p[:3] for p in Image.open(f'{T}/trims/color_palettes/trim_palette.png').convert('RGBA').getdata()]
PATTERNS = ['fracture', 'crater', 'olympus', 'geode', 'rift', 'hull', 'corona', 'surge', 'prism', 'meteor']
NAMES = {'fracture': 'Fracture', 'crater': 'Crater', 'olympus': 'Olympus', 'geode': 'Geode', 'rift': 'Rift', 'hull': 'Hull',
         'corona': 'Corona', 'surge': 'Surge', 'prism': 'Prism', 'meteor': 'Meteor'}
SETS = ['nullifite', 'ferrox', 'moonsteel', 'olympium', 'cobaltium', 'cyrrium', 'aurelion', 'cerulite', 'ruskite', 'tectium', 'pyrium',
        'skarnite', 'salvium', 'wraithsteel', 'palladine', 'eidolite', 'photium', 'astrium', 'radiantine', 'solvanite']
# which armor set shows each pattern (the world it comes from), and 3 materials to show it in
SHOW = {'fracture': 'nullifite', 'crater': 'moonsteel', 'olympus': 'olympium', 'geode': 'cerulite', 'rift': 'skarnite',
        'hull': 'wraithsteel', 'corona': 'solvanite', 'surge': 'cyrrium', 'prism': 'aurelion', 'meteor': 'astrium'}
MATS3 = [['solvanite', 'cerulite', 'radiantine'], ['nullifite', 'photium', 'cerulite'], ['palladine', 'cobaltium', 'aurelion'],
         ['solvanite', 'pyrium', 'moonsteel'], ['cerulite', 'radiantine', 'nullifite'], ['pyrium', 'eidolite', 'ferrox'],
         ['nullifite', 'cerulite', 'skarnite'], ['radiantine', 'palladine', 'skarnite'], ['astrium', 'ruskite', 'wraithsteel'],
         ['cerulite', 'solvanite', 'palladine']]
pal = {s: [p[:3] for p in Image.open(f'{T}/trims/color_palettes/{s}.png').convert('RGBA').getdata()] for s in SETS}

def recolor(im, p):
    im = im.convert('RGBA'); out = Image.new('RGBA', im.size)
    out.putdata([(p[KEY.index(c[:3])] + (255,)) if c[3] and c[:3] in KEY else (0, 0, 0, 0) for c in im.getdata()])
    return out

FRONT = [  # (layer, src rect, dest x, dest y) for a front-view figure 16 x 32 model pixels
    (1, (8, 8, 8, 8), 4, 0), (1, (20, 20, 8, 12), 4, 8), (1, (44, 20, 4, 12), 0, 8), (1, (44, 20, 4, 12), 12, 8),
    (2, (20, 20, 8, 12), 4, 8), (2, (4, 20, 4, 12), 4, 20), (2, (4, 20, 4, 12), 8, 20), (1, (4, 20, 4, 12), 4, 20), (1, (4, 20, 4, 12), 8, 20)]
def figure(armor, pattern, mat, s=7):
    l1 = Image.open(f'{T}/models/armor/{armor}_layer_1.png').convert('RGBA'); l2 = Image.open(f'{T}/models/armor/{armor}_layer_2.png').convert('RGBA')
    t1 = recolor(Image.open(f'{T}/trims/models/armor/{pattern}.png'), pal[mat]); t2 = recolor(Image.open(f'{T}/trims/models/armor/{pattern}_leggings.png'), pal[mat])
    fig = Image.new('RGBA', (16, 32), (0, 0, 0, 0))
    for layer, (x, y, w, h), dx, dy in FRONT:
        base, trim = (l1, t1) if layer == 1 else (l2, t2)
        part = base.crop((x, y, x + w, y + h)); part.alpha_composite(trim.crop((x, y, x + w, y + h)))
        fig.alpha_composite(part, (dx, dy))
    return fig.resize((16 * s, 32 * s), Image.NEAREST)

BG, INK, SUB, LINE = (26, 28, 34), (236, 240, 250), (170, 178, 196), (64, 70, 86)
cw, rh = 150, 290
W = 60 + 5 * 2 * cw + 40
img = Image.new('RGB', (W, 150 + 5 * rh + 260), BG); d = ImageDraw.Draw(img)
d.text((30, 22), 'ZeroG armor trims', font=F(40, True), fill=INK)
d.text((30, 76), '10 ZeroG trim patterns and 20 trim materials, one per ZeroG armor set. Vanilla patterns work with our materials and vice versa.', font=F(18), fill=SUB)
for n, pid in enumerate(PATTERNS):
    ox = 30 + (n % 2) * (5 * cw + 20); oy = 120 + (n // 2) * rh
    d.rounded_rectangle((ox, oy, ox + 5 * cw, oy + rh - 14), 12, outline=LINE, width=2)
    tpl = Image.open(f'{T}/item/{pid}_armor_trim_smithing_template.png').convert('RGBA').resize((64, 64), Image.NEAREST)
    img.paste(tpl, (ox + 14, oy + 14), tpl)
    d.text((ox + 14, oy + 90), NAMES[pid], font=F(22, True), fill=INK)
    d.text((ox + 14, oy + 120), f'on {SHOW[pid].capitalize()}', font=F(15), fill=SUB)
    for j, m in enumerate(MATS3[n]):
        f = figure(SHOW[pid], pid, m)
        img.paste(f, (ox + 160 + j * 190, oy + 14), f)
        d.text((ox + 160 + j * 190, oy + 246), m.capitalize(), font=F(14), fill=SUB)
oy = 130 + 5 * rh
d.text((30, oy), 'Trim material palettes', font=F(26, True), fill=INK)
for i, s in enumerate(SETS):
    x = 30 + (i % 10) * 150; y = oy + 44 + (i // 10) * 90
    for k, c in enumerate(pal[s]):
        d.rectangle((x + k * 14, y, x + k * 14 + 13, y + 30), fill=c)
    d.text((x, y + 36), s.capitalize(), font=F(15), fill=INK)
os.makedirs(OUT, exist_ok=True); img.save(f'{OUT}/armor_trims.png'); print(img.size)
