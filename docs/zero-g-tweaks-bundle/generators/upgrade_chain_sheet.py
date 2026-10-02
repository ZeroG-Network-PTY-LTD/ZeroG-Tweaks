"""Upgrade chain sheet. Usage: python3 upgrade_chain_sheet.py <upgrade_out_dir> <out_png>"""
import sys, os, io, subprocess
from PIL import Image, ImageDraw, ImageFont
sys.argv = [sys.argv[0], '/dev/null'] + sys.argv[1:]  # keep upgrade_templates import quiet-safe
OUTDIR, PNG = sys.argv[2], sys.argv[3]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location('ut', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upgrade_templates.py'))
src = open(spec.origin).read().split('# 1. smithing upgrades')[0]   # only the tables, no file writing
ns = {'__file__': spec.origin}; sys.argv = ['x', '/dev/null']; exec(src, ns)
CHAIN, PLACE, mat, nice, git, R = ns['CHAIN'], ns['PLACE'], ns['mat'], ns['nice'], ns['git'], ns['R']
F = lambda s, b=False: ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if b else ""}.ttf', s)
BG, INK, SUB, LINE, CARD = (245, 244, 240), (30, 32, 38), (96, 100, 112), (205, 205, 215), (255, 255, 255)
def icon(name):
    p = f'{OUTDIR}/assets/zerog_tweaks/textures/item/{name}.png'
    try: return Image.open(p).convert('RGBA') if os.path.exists(p) else Image.open(io.BytesIO(git(f'{R}/assets/zerog_tweaks/textures/item/{name}.png', True))).convert('RGBA')
    except Exception: return None
rows = list(CHAIN.items()); RH = 74; W = 1700; H = 170 + (len(rows) + 1) * RH + 40
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
d.text((40, 24), 'Upgrade chain · netherite-style smithing templates', font=F(36, True), fill=INK)
d.text((40, 76), 'Smithing table: template + the previous set\'s piece + the new set\'s ingot or gem. Enchantments and trims carry over. '
       'Nullifite is crafted from ingots, like diamond.', font=F(16), fill=SUB)
d.text((40, 100), 'Copy a template (gives 2): 7 of the base set\'s material + the template + the stone of the place it\'s found. '
       'Precious sets (*) branch off their world\'s entry set.', font=F(16), fill=SUB)
cols = [(40, 'From'), (360, 'Template'), (488, 'Ingredient'), (640, 'Result'), (960, 'Template found in'), (1380, 'Copy: ring x7 + middle')]
for x, t in cols: d.text((x, 140), t, font=F(14, True), fill=INK)
for i, (s, (b, chest, stone)) in enumerate([('nullifite', (None, None, None))] + rows):
    y = 166 + i * RH
    d.rounded_rectangle((36, y, W - 36, y + RH - 8), 10, fill=CARD, outline=LINE)
    def put(name, x):
        im = icon(name)
        if im: img.paste(im.resize((48, 48), Image.NEAREST), (x, y + 9), im.resize((48, 48), Image.NEAREST))
    if b is None:
        put('nullifite_pickaxe', 640); d.text((700, y + 22), 'Nullifite (crafted from ingots)', font=F(16, True), fill=INK); continue
    put(f'{b}_pickaxe', 40); d.text((100, y + 22), b.capitalize(), font=F(16), fill=INK)
    d.text((300, y + 20), '+', font=F(22, True), fill=SUB)
    put(f'{s}_upgrade_smithing_template', 360)
    d.text((412, y + 20), '+', font=F(22, True), fill=SUB)
    put(mat(s).split(':')[1], 430); d.text((488, y + 22), nice(mat(s)), font=F(14), fill=INK)
    d.text((610, y + 20), '→', font=F(22, True), fill=SUB)
    put(f'{s}_pickaxe', 640)
    d.text((700, y + 22), s.capitalize() + (' *' if s in ('aurelion', 'pyrium', 'palladine', 'radiantine') else ''), font=F(16, True), fill=INK)
    d.text((960, y + 22), PLACE[chest], font=F(14), fill=INK)
    d.text((1380, y + 22), f'{nice(mat(b))} + {nice(stone)}', font=F(14), fill=INK)
img.save(PNG); print(img.size)
