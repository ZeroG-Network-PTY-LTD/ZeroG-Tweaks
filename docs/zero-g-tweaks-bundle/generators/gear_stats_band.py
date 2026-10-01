"""Append an 'Exact stats' band to gear sheets, read straight from the design doc's
'Gear stats and abilities' table (single source of truth). Usage: python3 gear_stats_band.py <bundle_dir>"""
import re, sys, os, glob
from PIL import Image, ImageDraw, ImageFont

B = sys.argv[1]
DOC = open(f'{B}/ZeroG_Tweaks_Design_Doc.md').read()
F = lambda s, b=False: ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if b else ""}.ttf', s)
INK, SUB, LINE, CARD, ACC = (34, 32, 40), (110, 108, 118), (214, 212, 222), (255, 255, 255), (124, 92, 220)
DIA_ARMOR = (363, 528, 495, 429); DIA_TOOL = 1561   # vanilla diamond durability

def table(after):
    sec = DOC[DOC.index(after):]
    rows = []
    for ln in sec.splitlines()[1:]:
        if ln.startswith('|'):
            cells = [c.strip() for c in ln.strip('|').split('|')]
            if set(cells[0]) <= set('- '): continue
            rows.append(cells)
        elif rows: break
    return rows[0], rows[1:]
h, stats = table('**Gear stats and abilities')
STATS = {r[0].lower(): dict(zip(h, r)) for r in stats}
_, metal = table('**Metal gear sets**'); META = {r[0].lower(): r for r in metal}
_, main = table('## Gear'); MAIN = {r[0].lower(): r for r in main}
_, abil = table('**Tool and weapon abilities'); ABIL = {r[0].lower(): r for r in abil}
PRECIOUS = 'Precious sets' in DOC

def lines_for(k):
    s = STATS[k]; out = []
    arm = s['Armor (helm/chest/legs/boots)']; per = [int(x) for x in arm.split(' ')[0].split('/')]
    mult = float(s['Durability'].rstrip('×'))
    out.append(('Tier', s['Tier'] + (' set (main progression)' if s['Tier'].startswith('T') else ' set')))
    out.append(('Armor', f"helmet {per[0]} · chestplate {per[1]} · leggings {per[2]} · boots {per[3]}  =  {sum(per)} points  (diamond = 20)"))
    out.append(('Toughness', f"{s['Toughness']}  (diamond 2, netherite 3)"))
    out.append(('Knockback resist', s['Knockback resist'] + ('  (netherite 10%)' if s['Knockback resist'] != '0%' else '')))
    out.append(('Durability', f"{s['Durability']} diamond  →  tools ≈ {round(DIA_TOOL * mult)} uses; armor ≈ "
                + ' / '.join(str(round(v * mult)) for v in DIA_ARMOR) + ' (helm/chest/legs/boots)'))
    out.append(('Sword damage', f"{s['Sword damage']}  (diamond 7, netherite 8)"))
    if s['Tier'] == 'Precious': out.append(('Enchantability', '25, and mines and swings faster, like gold'))
    if k in META: out.append(('Full-set perk', META[k][4]))
    elif k in MAIN: out.append(('Set bonus', MAIN[k][3]))
    if k in ABIL:
        a = ABIL[k]; out.append(('Abilities', f"Pick/shovel: {a[1]} · Axe/hoe: {a[2]} · Sword: {a[3]}"))
    if s['Tier'].startswith('T'):
        out.append(('Mining level', "Mines the next planet's rare ore (needs_<tier>_tool tags)."))
    else:
        out.append(('Mining level', 'Not set in the design doc for metal sets yet. Decide it before the SimpleTier is coded.'))
    return out

def wrap(d, text, font, width):
    words, cur, res = text.split(' '), '', []
    for w in words:
        if d.textlength((cur + ' ' + w).strip(), font=font) > width: res.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    return res + [cur]

def band(width, k, scale=1.0):
    fs = lambda n: max(10, int(n * scale))
    rows = lines_for(k)
    tmp = Image.new('RGB', (width, 10)); d = ImageDraw.Draw(tmp)
    lab_w = int(190 * scale); txt_w = width - 56 - lab_w - 20
    hgt = int(60 * scale) + sum(len(wrap(d, v, F(fs(13)), txt_w)) * int(19 * scale) + int(8 * scale) for _, v in rows) + int(36 * scale)
    im = Image.new('RGB', (width, hgt), (246, 245, 242)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((28, 8, width - 28, hgt - 10), 12, fill=CARD, outline=LINE, width=2)
    d.text((48, 22), 'Exact stats', font=F(fs(18), True), fill=INK)
    d.text((48 + d.textlength('Exact stats', font=F(fs(18), True)) + 14, 26),
           'from the design doc (Gear stats and abilities, locked). Durability use counts are worked out from vanilla diamond.', font=F(fs(12)), fill=SUB)
    y = int(60 * scale)
    for lab, val in rows:
        d.text((48, y), lab, font=F(fs(13), True), fill=INK)
        for ln in wrap(d, val, F(fs(13)), txt_w):
            d.text((48 + lab_w, y), ln, font=F(fs(13)), fill=INK); y += int(19 * scale)
        y += int(8 * scale)
    return im

def append(path, k, scale=1.0):
    base = Image.open(path).convert('RGB')
    marker = (base.getpixel((5, base.height - 3)))
    b = band(base.width, k, scale)
    out = Image.new('RGB', (base.width, base.height + b.height), (246, 245, 242))
    out.paste(base, (0, 0)); out.paste(b, (0, base.height)); out.save(path)

if __name__ == '__main__':
    done = []
    for p in sorted(glob.glob(f'{B}/sheets/armor/*_armor.png')):
        k = re.match(r'\d+_(.+)_armor\.png', os.path.basename(p)).group(1); append(p, k); done.append(p)
    for p in sorted(glob.glob(f'{B}/sheets/gear/showcase/[0-9][0-9]_*.png')):
        k = re.match(r'\d+_(.+)\.png', os.path.basename(p)).group(1)
        if k in STATS: append(p, k, 1.15); done.append(p)
    for p in [f'{B}/sheets/gear/moonsteel_reference_items.png', f'{B}/sheets/gear/moonsteel_tools_3d.png']:
        append(p, 'moonsteel', 1.15); done.append(p)
    print(len(done), 'sheets updated'); print(lines_for('moonsteel'))
