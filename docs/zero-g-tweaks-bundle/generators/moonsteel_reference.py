"""Moonsteel gear reference for Blockbench: (1) tools + armor icons as numbered 16x16 pixel grids with exact colours,
held/3D views and model info; (2) worn GeckoLib armor: cube table, labelled box-UV map, front/side/back renders.
Usage: python3 moonsteel_reference.py <geo.json> <geo_texture.png> <item_texture_dir> <out_dir>"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render3d import Scene

GEO, GTEX, ITEMS, OUT = sys.argv[1:5]
SET = 'moonsteel'
F = lambda s, b=False: ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if b else ""}.ttf', s)
M = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', s)
BG, INK, SUB, LINE, CARD, ACC = (245, 244, 240), (30, 32, 38), (96, 100, 112), (205, 205, 215), (255, 255, 255), (110, 80, 220)
TOOLS = [('sword', 'Sword', 'item/handheld', 'Broad blade, clipped tip, glowing fuller, bar guard, round pommel'),
         ('pickaxe', 'Pickaxe', 'item/handheld', 'Hammer-backed pick head on a steel handle'),
         ('axe', 'Axe', 'item/handheld', 'Classic axe head'),
         ('shovel', 'Shovel', 'item/handheld', 'Square blade'),
         ('hoe', 'Hoe', 'item/handheld', 'Straight blade with a back spike')]
ARMOR = [('helmet', 'Helmet'), ('chestplate', 'Chestplate'), ('leggings', 'Leggings'), ('boots', 'Boots')]

def palette_of(ims):
    cols = {}
    for im in ims:
        for c in im.getdata():
            if c[3] > 0: cols[c] = cols.get(c, 0) + 1
    order = sorted(cols, key=lambda c: (sum(c[:3])))
    keys = '123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
    return {c: keys[i] for i, c in enumerate(order)}

def grid(im, pal, cell=22):
    n = im.width; pad = 18
    g = Image.new('RGB', (n * cell + pad + 2, n * cell + pad + 2), (255, 255, 255)); d = ImageDraw.Draw(g)
    for y in range(n):
        for x in range(n):
            c = im.getpixel((x, y)); X, Y = pad + x * cell, pad + y * cell
            if c[3] == 0:
                for k in range(0, cell, 6):
                    d.rectangle((X, Y + k, X + cell, Y + k + 2), fill=(240, 240, 246))
            else:
                d.rectangle((X, Y, X + cell, Y + cell), fill=c[:3])
                lum = sum(c[:3]) / 3
                d.text((X + cell // 2, Y + cell // 2), pal[c], font=M(10), fill=(255, 255, 255) if lum < 120 else (20, 20, 30), anchor='mm')
    for i in range(n + 1):
        w = (150, 150, 165) if i % 4 == 0 else (215, 215, 225)
        d.line((pad + i * cell, pad, pad + i * cell, pad + n * cell), fill=w); d.line((pad, pad + i * cell, pad + n * cell, pad + i * cell), fill=w)
    for i in range(n):
        d.text((pad + i * cell + cell // 2, 8), str(i), font=M(9), fill=SUB, anchor='mm')
        d.text((8, pad + i * cell + cell // 2), str(i), font=M(9), fill=SUB, anchor='mm')
    return g

def held(im):
    s = Scene(yaw=-35, pitch=-20)
    s.extrude(im, (0, 0, 0), 1.0, 1.0)
    return s.render(9, pad=6)

# ---------------- sheet 1: items ----------------
items = {k: Image.open(f'{ITEMS}/{SET}_{k}.png').convert('RGBA') for k, *_ in TOOLS + ARMOR}
pal = palette_of(items.values())
cw, chh = 560, 600
W = 40 + 3 * (cw + 20) + 20
H = 150 + 3 * (chh + 20) + 280
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
d.text((40, 26), 'Moonsteel gear · item reference (Blockbench)', font=F(38, True), fill=INK)
d.text((40, 80), '16 x 16 item textures, pixel for pixel. Column/row numbers are texture coordinates (0,0 = top-left). '
       'Letters match the palette at the bottom; checkered cells are transparent.', font=F(17), fill=SUB)
d.text((40, 106), 'Tools use parent minecraft:item/handheld (held diagonally); armor icons use minecraft:item/generated. '
       'In Blockbench: File > New > Java Block/Item, then Generate from texture (1 px thick).', font=F(17), fill=SUB)
cells = [(k, n, p, desc) for k, n, p, desc in TOOLS] + [(k, n, 'item/generated', 'Inventory icon only; the worn model is on sheet 2') for k, n in ARMOR]
for i, (k, name, parent, desc) in enumerate(cells):
    x = 40 + (i % 3) * (cw + 20); y = 150 + (i // 3) * (chh + 20)
    d.rounded_rectangle((x, y, x + cw, y + chh), 14, fill=CARD, outline=LINE, width=2)
    d.text((x + 20, y + 16), f'Moonsteel {name}', font=F(22, True), fill=INK)
    d.text((x + 20, y + 46), f'zerog_tweaks:{SET}_{k}', font=M(13), fill=SUB)
    g = grid(items[k], pal); img.paste(g, (x + 20, y + 76))
    h = held(items[k]); h.thumbnail((150, 170)); img.paste(h, (x + cw - 20 - h.width, y + 90), h)
    d.text((x + cw - 20, y + 272), '3D (1 px thick)', font=F(12), fill=SUB, anchor='ra')
    ic = items[k].resize((64, 64), Image.NEAREST); img.paste(ic, (x + cw - 20 - 64, y + 300), ic)
    d.text((x + cw - 20, y + 370), 'icon 4x', font=F(12), fill=SUB, anchor='ra')
    ty = y + 76 + g.height + 12
    d.text((x + 20, ty), f'texture  textures/item/{SET}_{k}.png', font=M(12), fill=INK)
    d.text((x + 20, ty + 20), f'model    models/item/{SET}_{k}.json  (parent {parent})', font=M(12), fill=INK)
    d.text((x + 20, ty + 44), desc, font=F(14), fill=SUB)
# palette
py = 150 + 3 * (chh + 20) + 10
d.text((40, py), 'Palette (every colour used across the 9 textures)', font=F(22, True), fill=INK)
for i, (c, key) in enumerate(sorted(pal.items(), key=lambda kv: kv[1])):
    x = 40 + (i % 8) * 215; y = py + 44 + (i // 8) * 64
    d.rectangle((x, y, x + 44, y + 44), fill=c[:3], outline=LINE)
    d.text((x + 22, y + 22), key, font=M(14), fill=(255, 255, 255) if sum(c[:3]) / 3 < 120 else (20, 20, 30), anchor='mm')
    d.text((x + 54, y + 4), '#%02x%02x%02x' % c[:3], font=M(15), fill=INK)
    d.text((x + 54, y + 24), f'alpha {c[3]}' if c[3] < 255 else 'opaque', font=F(12), fill=SUB)
img = img.crop((0, 0, W, py + 44 + ((len(pal) + 7) // 8) * 64 + 20))
img.save(f'{OUT}/moonsteel_reference_items.png'); print('items', img.size, len(pal), 'colours')

# ---------------- sheet 2: worn armor ----------------
geo = json.load(open(GEO))['minecraft:geometry'][0]
tex = Image.open(GTEX).convert('RGBA'); TW, TH = geo['description']['texture_width'], geo['description']['texture_height']
cubes = []
for b in geo['bones']:
    for c in b.get('cubes', []):
        cubes.append((b['name'], b.get('parent'), b.get('pivot'), c))
NICE = {'armorHead': 'Helmet', 'armorBody': 'Chestplate body', 'armorRightArm': 'Chestplate sleeve R', 'armorLeftArm': 'Chestplate sleeve L',
        'armorRightLeg': 'Leggings R', 'armorLeftLeg': 'Leggings L', 'armorRightBoot': 'Boot R', 'armorLeftBoot': 'Boot L'}
COLS = [(230, 80, 80), (60, 140, 230), (40, 170, 110), (230, 150, 30), (150, 90, 220), (20, 170, 190), (220, 90, 170), (120, 120, 130), (90, 160, 40), (200, 120, 60)]

def render(yaw, pitch, scale=9):
    s = Scene(yaw=yaw, pitch=pitch)
    # faint player body for scale
    for o, sz in [((-4, 24, -4), (8, 8, 8)), ((-4, 12, -2), (8, 12, 4)), ((-8, 12, -2), (4, 12, 4)), ((4, 12, -2), (4, 12, 4)), ((-4, 0, -2), (4, 12, 4)), ((0, 0, -2), (4, 12, 4))]:
        s.solid(o, sz, (196, 160, 132), noise=.08, seed=sum(o))
    for name, parent, pivot, c in cubes:
        s.box_uv(tuple(c['origin']), tuple(c['size']), tuple(c['uv']), tex, inflate=c.get('inflate', 0) or 0, mirror=c.get('mirror', False))
    return s.render(scale, pad=10)

views = [('Front', render(0, -8)), ('Three-quarter', render(-35, -14)), ('Back', render(180, -8))]
uvs = 6
uvimg = tex.resize((TW * uvs, TH * uvs), Image.NEAREST)
uvbg = Image.new('RGBA', uvimg.size, (255, 255, 255, 255))
for yy in range(0, uvimg.height, 12):
    for xx in range(0, uvimg.width, 12):
        if (xx // 12 + yy // 12) % 2: ImageDraw.Draw(uvbg).rectangle((xx, yy, xx + 11, yy + 11), fill=(236, 236, 242, 255))
uvbg.alpha_composite(uvimg); ud = ImageDraw.Draw(uvbg)
seen = {}
for i, (name, parent, pivot, c) in enumerate(cubes):
    (u, v), (w, h, dd) = c['uv'], c['size']
    key = (u, v, w, h, dd)
    col = COLS[len(seen) % len(COLS)] if key not in seen else seen[key]
    if key not in seen:
        seen[key] = col
        ud.rectangle((u * uvs, v * uvs, (u + 2 * (dd + w)) * uvs - 1, (v + dd + h) * uvs - 1), outline=col + (255,), width=3)
        ud.text((u * uvs + 4, v * uvs + 2), f'{u},{v}', font=M(13), fill=col + (255,))

W2 = 1900
img2 = Image.new('RGB', (W2, 2000), BG); d = ImageDraw.Draw(img2)
d.text((40, 26), 'Moonsteel armor · worn model reference (GeckoLib / Blockbench)', font=F(36, True), fill=INK)
d.text((40, 78), f'Model geckolib/models/item/armor/{SET}.geo.json · texture textures/item/armor/{SET}.png ({TW} x {TH}, box UV) · '
       'Blockbench project type: GeckoLib Animated Model, "Armor".', font=F(17), fill=SUB)
x = 40
for title, im in views:
    im = im.copy(); im.thumbnail((380, 520))
    d.rounded_rectangle((x, 120, x + 400, 680), 14, fill=CARD, outline=LINE, width=2)
    d.text((x + 18, 134), title, font=F(20, True), fill=INK)
    img2.paste(im, (x + (400 - im.width) // 2, 170 + (500 - im.height) // 2), im); x += 420
d.text((x + 10, 140), 'Skin-coloured boxes are the player\nbody, shown only for scale.\nEverything grey/blue is armor.', font=F(15), fill=SUB)
d.text((x + 10, 220), 'Bone names must stay exactly as\nlisted (GeckoLib maps armorHead,\narmorBody, ... to the player).', font=F(15), fill=SUB)
# cube table
ty = 710
d.text((40, ty), 'Cubes (Blockbench values: origin = min corner, size, inflate, box-UV offset)', font=F(22, True), fill=INK)
hdr = ['#', 'Piece', 'Bone', 'Parent bone', 'Pivot', 'Origin (x,y,z)', 'Size (w,h,d)', 'Inflate', 'UV']
colx = [40, 80, 300, 480, 660, 820, 1040, 1220, 1320]
for cx, hname in zip(colx, hdr): d.text((cx, ty + 44), hname, font=F(15, True), fill=INK)
for i, (name, parent, pivot, c) in enumerate(cubes):
    y = ty + 74 + i * 30
    if i % 2 == 0: d.rectangle((36, y - 4, 1440, y + 24), fill=(236, 236, 240))
    key = (c['uv'][0], c['uv'][1], *c['size'])
    piece = NICE.get(name, name) + (' (pauldron)' if c['size'] == [6, 3, 6] else '')
    vals = [str(i + 1), piece, name, parent or '', str(pivot), str(c['origin']), str(c['size']), str(c.get('inflate', 0) or 0), str(c['uv'])]
    for cx, v in zip(colx, vals): d.text((cx, y), v, font=M(14) if cx > 280 else F(14), fill=INK)
    d.rectangle((1450, y, 1470, y + 20), fill=seen[key])
ny = ty + 74 + len(cubes) * 30 + 20
notes = ['Pauldrons are the only extra geometry: 6 x 3 x 6 boxes on each shoulder (not inflated).',
         'Helmet inflate 1.0, body 1.01, sleeves 1.0, leggings 0.5, boots 1.0, as vanilla armor, so the layers do not z-fight.',
         'Leggings and boots share the leg bones; boots sit on top with the larger inflate.',
         'The left and right pieces use the same UV island, so paint it once and both sides match.',
         'Sleeves are half-length on purpose: the arm island is painted only on its top 7 rows, so the forearm shows the player skin.',
         'Glass visor and accent band are painted on the helmet front face; rivets, knee plates and heavy soles are painted, not modelled.']
for k, n in enumerate(notes): d.text((40, ny + k * 26), '• ' + n, font=F(15), fill=SUB)
# uv map
uy = ny + len(notes) * 26 + 30
d.text((40, uy), f'Texture layout ({TW} x {TH}, shown {uvs}x). Each outline is one cube\'s box-UV island; the label is its UV offset.', font=F(22, True), fill=INK)
uvs_im = uvbg.convert('RGB'); img2.paste(uvs_im, (40, uy + 44))
lx = 40 + uvs_im.width + 30
d.text((lx, uy + 50), 'Box-UV island order (each cube):', font=F(15, True), fill=INK)
for k, t in enumerate(['top row: top face | bottom face', 'lower row: right | front | left | back',
                       'island width = 2 x (depth + width)', 'island height = depth + height']):
    d.text((lx, uy + 80 + k * 24), t, font=F(14), fill=SUB)
img2 = img2.crop((0, 0, W2, uy + 44 + uvs_im.height + 30))
img2.save(f'{OUT}/moonsteel_reference_armor.png'); print('armor', img2.size)
