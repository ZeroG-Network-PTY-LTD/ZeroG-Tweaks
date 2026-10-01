"""Mining ladder sheet: level staircase from netherite to Solvanite, with pick icons and the ores each level opens.
Usage: python3 mining_ladder_sheet.py <bundle_dir> <item_texture_dir> <out_png>"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mining_ladder as ML
B, ITEMS, OUT = sys.argv[1:4]
F = lambda s, b=False: ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if b else ""}.ttf', s)
BG, INK, SUB, LINE, CARD = (245, 244, 240), (30, 32, 38), (96, 100, 112), (205, 205, 215), (255, 255, 255)
WORLD_COL = {'Overworld': (120, 120, 130), 'Sol (Overworld)': (90, 80, 140), 'Mars': (196, 90, 60), 'Moon': (140, 160, 185),
             'Cerulon': (40, 150, 200), 'Skarn': (220, 110, 40), 'Eidolon': (110, 190, 210), 'Solvane': (230, 175, 40)}
rows = [(4, ['netherite'], 'Overworld', 'Vanilla. The entry ticket to space.')] + ML.LEVELS
RH = 92; W = 1800; H = 190 + len(rows) * RH + 60
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
d.text((40, 26), 'ZeroG mining ladder', font=F(40, True), fill=INK)
d.text((40, 82), 'Every ZeroG pickaxe out-mines netherite. Nullifite needs netherite; each later ore needs the pickaxe before it. '
       'Within a world: common metal, then standard metal, then the rare gem.', font=F(17), fill=SUB)
d.text((40, 108), 'Precious (gold-style) picks share their world\'s common level but mine faster. Fuels and energy dusts only need iron, so power is never blocked.',
       font=F(17), fill=SUB)
cols = [(40, 'Level'), (130, 'Pickaxe'), (520, 'World'), (680, 'Opens these ores'), (1180, 'Speed'), (1270, 'Lore')]
for x, t in cols: d.text((x, 150), t, font=F(15, True), fill=INK)
for i, (L, sets, world, lore) in enumerate(rows):
    y = 182 + i * RH
    d.rounded_rectangle((36, y, W - 36, y + RH - 10), 10, fill=CARD, outline=LINE)
    wc = WORLD_COL.get(world, (150, 150, 150))
    d.rectangle((36, y, 46, y + RH - 10), fill=wc)
    bw = 12 + 3 * (L - 4)                                         # staircase bar grows with level
    d.text((62, y + 14), str(L), font=F(26, True), fill=INK)
    d.rectangle((62, y + 54, 62 + bw, y + 62), fill=wc)
    x = 130
    for s in sets:
        p = f'{ITEMS}/{s}_pickaxe.png'
        if os.path.exists(p):
            ic = Image.open(p).convert('RGBA').resize((48, 48), Image.NEAREST); img.paste(ic, (x, y + 16), ic)

        nm = s.capitalize() + (' *' if s in ML.PRECIOUS else '')
        d.text((x + 56, y + 28), nm, font=F(17, True), fill=INK); x += int(56 + d.textlength(nm, font=F(17, True)) + 26)
    d.text((520, y + 28), world, font=F(15), fill=wc)
    ores = [o.replace('_ore', '').replace('deepslate_', '').replace('_', ' ').title() for o, (r, _) in ML.ORES.items() if r == L]
    d.text((680, y + 28), ', '.join(ores) if ores else ('everything' if L == 20 else '(nothing new)'), font=F(15), fill=INK)
    sp = ', '.join(f'{ML.mining_speed(s):g}' for s in sets) if L > 4 else '9'
    d.text((1180, y + 28), sp, font=F(15), fill=INK)
    words, line, ly = lore.split(), '', y + 18
    for w in words:
        if d.textlength(line + ' ' + w, font=F(14)) > W - 36 - 1290:
            d.text((1270, ly), line.strip(), font=F(14), fill=SUB); ly += 20; line = ''
        line += ' ' + w
    d.text((1270, ly), line.strip(), font=F(14), fill=SUB)
d.text((40, H - 46), '* gold-style precious set: same level as its world\'s common metal, +4 mining speed, enchantability 25, lower durability.  '
       'A level-N pick mines every ore listed at level N and below.', font=F(14), fill=SUB)
img.save(OUT); print(img.size)
