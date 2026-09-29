"""In-game fix sheet: colleague's screenshots (left) vs the design-branch texture/model (right) + the rule.
Writes docs/zero-g-tweaks-bundle/sheets/fixes/ingame_fix_sheet.png"""
import os, textwrap
from PIL import Image, ImageDraw, ImageFont

REPO = '/home/claude/zerog-tweaks'
UP = '/root/.claude/uploads/23345d11-2ce7-53a5-9128-b35ae672adbe'
TEX = f'{REPO}/src/main/resources/assets/zerog_tweaks/textures/block'
OUT = f'{REPO}/docs/zero-g-tweaks-bundle/sheets/fixes'
os.makedirs(OUT, exist_ok=True)
F = lambda s, b=False: ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if b else ""}.ttf', s)

# same maths as client/ZGBlockColors.java
TYPE = {'ocean': 0x7C9CB8, 'frozen': 0xDDEAF2, 'crystal': 0xC6AEE6}
GAL = [0xFFFFFF, 0x9CB8F0, 0x9CB8F0, 0xF0A878, 0xC8E6F0, 0xF4D68C]
def mul(a, b): return tuple(((a >> s) & 255) * ((b >> s) & 255) // 255 for s in (16, 8, 0))
def tint(t, g):
    gal = GAL[g]; soft = ((gal & 0xFEFEFE) // 2) + 0x808080
    r, gg, b = mul(TYPE[t], soft); return (r << 16) | (gg << 8) | b
def tinted(name, t, g):
    im = Image.open(f'{TEX}/{name}.png').convert('RGBA'); c = tint(t, g)
    cr, cg, cb = (c >> 16) & 255, (c >> 8) & 255, c & 255
    px = [(r * cr // 255, gg * cg // 255, b * cb // 255, a) for r, gg, b, a in im.getdata()]
    o = Image.new('RGBA', im.size); o.putdata(px); return o
def tex(name): return Image.open(f'{TEX}/{name}.png').convert('RGBA')

ROWS = [
 ('cfc1c2e2', (760, 380, 1160, 720), 'Gildwood Sapling', 'OLD BUILD',
  'Old squiggle texture: the screenshot is from the 1.21.1-update branch, which does not have the new sapling art.',
  'Fixed on design/v1.2-assets: vanilla oak_sapling layout. 1-2 px stem from bottom centre, side twig, 3-tone leaf crown from the tree\'s own leaves/log palette. Model: block/cross, render_type cutout. Item: item/generated layer0 = block texture.',
  [tex('gildwood_sapling')]),
 ('5a0d54da', (700, 320, 1060, 680), 'Hoarwood Sapling', 'OLD BUILD',
  'Same as Gildwood: old texture from the 1.21.1-update build.',
  'Fixed on design branch: frosted drooping crown, white frost specks. Same cross model and cutout render type as every sapling.',
  [tex('hoarwood_sapling')]),
 ('9270781a', (840, 400, 1140, 720), 'Brine Crystal', 'GREY - NO TINT',
  'Grey on purpose-made grayscale art. The model is block/tinted_cross (tintindex 0) but no colour handler was registered, so Minecraft multiplies by white = raw grey. Same for the held item.',
  'Fixed now: client/ZGBlockColors.java moved into src. Tint = wasteland type x galaxy colour, read from the gN_pM dimension id; Overworld/planets fall back to Galaxy 2. Grey levels raised to 175-225 so the tint is not muddy. Right: Overworld, G3, G4, G5.',
  [tinted('brine_crystal', 'ocean', 2), tinted('brine_crystal', 'ocean', 3), tinted('brine_crystal', 'ocean', 4), tinted('brine_crystal', 'ocean', 5)]),
 ('21fca42c', (780, 340, 1180, 720), 'Prism Cluster', 'GREY - NO TINT',
  'Same cause as Brine Crystal: grayscale texture on tinted_cross, no colour handler.',
  'Fixed by the same ZGBlockColors wiring (crystal type, lavender). Also fixes Frost Crystal and all 307 grayscale wasteland blocks: stones, bricks, slabs, stairs, walls, sands, glass. Right: Overworld, G3, G4, G5.',
  [tinted('prism_cluster', 'crystal', 2), tinted('prism_cluster', 'crystal', 3), tinted('prism_cluster', 'crystal', 4), tinted('prism_cluster', 'crystal', 5)]),
 ('da0f19fc', (720, 340, 1060, 640), 'Cerulite Cluster', 'OK',
  'Correct: coloured texture on a plain block/cross, no tint needed. AmethystClusterBlock gives the thin hitbox and face placement.',
  'Rule for all 4 crystals: one 16x16 sprite of 3-5 spikes, transparent background, spikes rooted on the bottom row; X-billboard (cross) model; blockstate rotates by facing like amethyst_cluster.',
  [tex('cerulite_cluster')]),
 ('ab6b17ee', (720, 300, 1140, 700), 'Glowkelp', 'OLD BUILD',
  'Grey, standing on grass: old build. There it was a tinted grey plant that accepted any ground.',
  'Fixed on design branch: kelp counterpart. Must be placed in a full water source, grows upward. Two coloured textures (no tint): glowkelp = tip with glowing bulb, glowkelp_plant = seamless stem that tiles vertically. Both block/cross, cutout, light 8.',
  [tex('glowkelp'), tex('glowkelp_plant')]),
 ('c391ba44', (650, 220, 1200, 700), 'Pyrevine', 'OLD BUILD',
  'Old single texture, no berries, and the held item uses the vine art. Old build.',
  'Fixed on design branch: cave_vines counterpart. 4 textures: pyrevine / pyrevine_lit (tip, curl at the bottom) and pyrevine_plant / pyrevine_plant_lit (body, tiles vertically). The _lit versions add Pyrefruit berries and light 14. You plant it with Pyrefruit, like glow berries.',
  [tex('pyrevine'), tex('pyrevine_lit'), tex('pyrevine_plant'), tex('pyrevine_plant_lit')]),
 ('48cef392', (620, 260, 1220, 820), 'Lunar Lichen', 'OLD BUILD',
  'Standing X-shape in the middle of the block: the old cross model. Lichen should lie flat against faces.',
  'Fixed on design branch: glow_lichen counterpart (multiface). The texture is a full 16x16 patchy face texture drawn edge to edge. The model is one flat plane at z=0.1; the blockstate is multipart, rotated per face (north/south/east/west/up/down). Shears-only drops.',
  [tex('lunar_lichen'), tex('rust_lichen')]),
]

W, RH, PAD = 1900, 360, 24
img = Image.new('RGB', (W, 150 + RH * len(ROWS)), (24, 26, 32))
d = ImageDraw.Draw(img)
d.text((PAD, 24), 'ZeroG Tweaks - in-game fix sheet (plants and crystals)', font=F(40, True), fill=(235, 240, 255))
d.text((PAD, 80), 'Left: your screenshot.  Middle: what is wrong and why.  Right: the texture/model the design branch ships (tinted rows show the tint).',
       font=F(22), fill=(170, 180, 200))
TAG = {'OLD BUILD': (230, 150, 40), 'GREY - NO TINT': (220, 70, 70), 'OK': (70, 180, 110)}
for i, (uid, box, name, tag, why, fix, tiles) in enumerate(ROWS):
    y = 140 + i * RH
    d.rectangle((PAD - 8, y - 6, W - PAD + 8, y + RH - 20), outline=(60, 66, 80), width=2)
    shot = Image.open(f'{UP}/{uid}-image.png').convert('RGB').crop(box)
    shot.thumbnail((440, 320)); img.paste(shot, (PAD, y + 8))
    x = PAD + 460
    d.text((x, y + 6), name, font=F(30, True), fill=(240, 240, 250))
    tw = d.textlength(name, font=F(30, True))
    d.rounded_rectangle((x + tw + 16, y + 10, x + tw + 32 + d.textlength(tag, font=F(18, True)), y + 40), 8, fill=TAG[tag])
    d.text((x + tw + 24, y + 13), tag, font=F(18, True), fill=(20, 20, 20))
    ty = y + 52
    for head, body, col in (('Problem', why, (255, 190, 170)), ('Fix / model rule', fix, (180, 230, 200))):
        d.text((x, ty), head, font=F(19, True), fill=col); ty += 26
        for line in textwrap.wrap(body, 78):
            d.text((x, ty), line, font=F(18), fill=(215, 220, 232)); ty += 23
        ty += 8
    # tiles
    tx = W - PAD - 10
    size = 128 if len(tiles) <= 2 else 96
    for t in reversed(tiles):
        tx -= size + 10
        bg = Image.new('RGB', (size, size), (70, 76, 90))
        bd = ImageDraw.Draw(bg)
        for yy in range(0, size, size // 8):
            for xx in range(0, size, size // 8):
                if (xx + yy) // (size // 8) % 2: bd.rectangle((xx, yy, xx + size // 8 - 1, yy + size // 8 - 1), fill=(84, 90, 104))
        bg.paste(t.resize((size, size), Image.NEAREST), (0, 0), t.resize((size, size), Image.NEAREST))
        img.paste(bg, (tx, y + 60))
img.save(f'{OUT}/ingame_fix_sheet.png')
print('ok', img.size)
