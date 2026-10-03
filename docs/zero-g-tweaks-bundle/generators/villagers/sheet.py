"""Reference sheet for one villager species, in the house style of sheets/mobs/."""
from vkit import *

PROF = [('Farmer', '#d8b13a'), ('Fisherman', '#3f7fb5'), ('Shepherd', '#e6e6e6'), ('Fletcher', '#8a6a3a'), ('Librarian', '#b0342c'),
        ('Cartographer', '#2f6d4f'), ('Cleric', '#7b3fa0'), ('Armorer', '#5a5f66'), ('Weaponsmith', '#2b2b2b'), ('Toolsmith', '#8a5a2a'),
        ('Butcher', '#c94a3a'), ('Leatherworker', '#7a4a2a'), ('Mason', '#9a9a8a')]
LEVELS = [('Novice', '#8b8b8b'), ('Apprentice', '#d8d8d8'), ('Journeyman', '#e9b23a'), ('Expert', '#3fbf5f'), ('Master', '#5fe3e8')]


def lum(c): return .3 * c[0] + .59 * c[1] + .11 * c[2]


def recolour(tex, colour, mask='accent'):
    """Profession overlay idea: repaint the species' accent pixels in the profession colour, keeping their shading."""
    t = Tex(*tex.img.size); t.img = tex.img.copy(); t.glow = set(tex.glow); t.masks = tex.masks
    px = sorted(tex.masks.get(mask, ()))
    if not px: return t
    base = max(lum(tex.img.getpixel(p)) for p in px) or 1
    c = hexc(colour)
    for p in px:
        k = 0.55 + 0.5 * lum(tex.img.getpixel(p)) / base
        t.img.putpixel(p, shade(c, k))
    return t


def overlay(tex, colour, mask='accent'):
    t = recolour(tex, colour, mask); o = Image.new('RGBA', tex.img.size, (0, 0, 0, 0))
    for p in tex.masks.get(mask, ()): o.putpixel(p, t.img.getpixel(p))
    return o


def grid_view(sh, d, sp, tex, cam, box, title, note, labels=(), axis='', dims=True, only_right=False):
    panel(d, box, title, 'same scale in all views')
    im, proj = render(sp, tex, cam, flat=True)
    x0, y0, x1, y1 = box
    ox = (x0 + x1) // 2 - im.width // 2; oy = y0 + 70 + (y1 - y0 - 140 - im.height) // 2
    P = lambda p: (proj(p)[0] + ox, proj(p)[1] + oy)
    s = cam.s
    # pixel grid behind the model (across the model's width and height)
    xs = [P((x, 0, 0))[0] for x in range(-12, 13)] if abs(cam.sy_) < .5 else [P((0, 0, z))[0] for z in range(-12, 13)]
    gx0, gx1 = min(xs), max(xs); gy1 = P((0, 0, 0))[1]; gy0 = P((0, 40, 0))[1]
    gx0, gx1 = max(gx0, x0 + 90), min(gx1, x1 - 90)
    for gx in xs:
        if gx0 <= gx <= gx1: d.line([(gx, gy0), (gx, gy1)], fill=(236, 235, 242))
    for yy in range(0, 41):
        gy = P((0, yy, 0))[1]; d.line([(gx0, gy), (gx1, gy)], fill=(236, 235, 242) if yy % 4 else (224, 222, 234))
    sh.alpha_composite(im, (int(ox), int(oy)))
    # ground and hitbox
    gy = P((0, 0, 0))[1]
    d.line([(gx0 - 30, gy), (gx1 + 30, gy)], fill=SUB, width=1); d.text((gx1 + 34, gy - 7), 'ground', font=FR(11), fill=SUB)
    hw = HITBOX[0] * 16 / RENDER_SCALE / 2; hh = HITBOX[1] * 16 / RENDER_SCALE
    hx0, hx1 = P((hw, 0, 0))[0], P((-hw, 0, 0))[0]
    if abs(cam.sy_) > .5: hx0, hx1 = P((0, 0, -hw))[0], P((0, 0, hw))[0]
    hx0, hx1 = min(hx0, hx1), max(hx0, hx1); hy = P((0, hh, 0))[1]
    for a in range(int(hx0), int(hx1), 8): d.line([(a, hy), (min(a + 4, hx1), hy)], fill=ACC, width=2)
    for a in range(int(hy), int(gy), 8):
        d.line([(hx0, a), (hx0, min(a + 4, gy))], fill=ACC, width=2); d.line([(hx1, a), (hx1, min(a + 4, gy))], fill=ACC, width=2)
    if dims:
        top = sp.height(); ty = P((0, top, 0))[1]; rx = gx0 - 14
        d.line([(rx, ty), (rx, gy)], fill=INK); d.line([(rx - 5, ty), (rx + 5, ty)], fill=INK); d.line([(rx - 5, gy), (rx + 5, gy)], fill=INK)
        t = f'{top:g} px = {top * RENDER_SCALE / 16:.2f} blocks'; d.text((rx - 10, ty - 30), t, font=FR(11), fill=INK)
        d.text((hx1 + 6, hy - 16), 'hitbox 0.6 x 1.95', font=FR(10), fill=ACC)
    d.text((x0 + 16, y1 - 22), axis, font=FR(10), fill=SUB)
    # labels
    if labels:
        cx = (x0 + x1) / 2; L, R = [], []
        for text, pt in labels:
            ax, ay = P(pt)
            (L if not only_right and (ax < cx - 4 or (abs(ax - cx) <= 4 and len(L) <= len(R))) else R).append((ay, ax, text))
        for side, items in (('L', L), ('R', R)):
            items.sort(); last = -1e9; placed = []
            for ay, ax, text in items:
                ty = max(ay, last + 24); placed.append((ty, ay, ax, text)); last = ty + 15 * (len(wrap(d, text, FR(12), 200)) - 1)
            over = (placed[-1][0] - (y1 - 40)) if placed else 0
            if over > 0: placed = [(t - over, a, b, c) for t, a, b, c in placed]
            for ty, ay, ax, text in placed:
                f = FR(12)
                if side == 'L':
                    lines = wrap(d, text, f, max(120, gx0 - 70 - (x0 + 16)))
                    for j, ln in enumerate(lines): d.text((x0 + 16, ty - 8 + j * 15), ln, font=f, fill=INK)
                    lx = x0 + 16 + d.textlength(lines[0], font=f) + 6
                else:
                    lines = wrap(d, text, f, max(120, (x1 - 16) - (gx1 + 40)))
                    for j, ln in enumerate(lines):
                        d.text((x1 - 16 - d.textlength(ln, font=f), ty - 8 + j * 15), ln, font=f, fill=INK)
                    lx = x1 - 16 - d.textlength(lines[0], font=f) - 6
                d.line([(lx, ty), (ax, ay)], fill=ACC, width=1); d.ellipse([ax - 3, ay - 3, ax + 3, ay + 3], fill=ACC)
    return P


def anchor(sp, c, face):
    (x, y, z), (w, h, dd) = c.origin, c.size; i = c.inflate
    p = {'north': (x + w / 2, y + h / 2, z - i), 'south': (x + w / 2, y + h / 2, z + dd + i)}[face]
    return world(sp, c, p)


def table(d, x, y, cols, rows, font=FM(12), head=FB(12), rh=21, zebra=True):
    cx = x
    for (title, w) in cols:
        d.text((cx, y), title, font=head, fill=INK); cx += w
    y += rh + 2; d.line([(x, y - 4), (cx, y - 4)], fill=LINE)
    for i, r in enumerate(rows):
        if zebra and i % 2: d.rectangle([x - 6, y - 3, cx, y + rh - 5], fill=(247, 246, 251))
        cx = x
        for (title, w), v in zip(cols, r):
            d.text((cx, y), str(v), font=font, fill=INK); cx += w
        y += rh
    return y


def build(sp, out_png):
    tex = sp.texture()
    W = 2240; H = 2800
    sh = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(sh)
    d.text((28, 20), f'{sp.name}  —  villager reference sheet', font=FB(32), fill=INK)
    d.text((28, 64), f'{sp.planet} ({sp.gravity:g} g) · planet villager species · entity zerog_tweaks:{sp.id} · hitbox 0.6 x 1.95 · '
                     f'model {sp.height():g} px tall, rendered at 0.9375 (vanilla villager scale) · texture {sp.W} x {sp.H} · ZeroG Tweaks',
           font=FR(14), fill=SUB)
    d.text((28, 86), f'"{sp.tag}"', font=FR(14), fill=ACC)

    S = 15; top = 118; bot = 930
    fl = [(c.label, anchor(sp, c, 'north')) for c in sp.cubes if c.label and c.origin[2] + c.size[2] / 2 <= 1.2]
    grid_view(sh, d, sp, tex, Cam(0, 0, S), (28, top, 812, bot), 'FRONT  (looking at its face)', None, fl, 'horizontal: X (model\'s right on the left)    vertical: Y up')
    grid_view(sh, d, sp, tex, Cam(90, 0, S), (828, top, 1268, bot), 'LEFT SIDE  (face points left)', None, (), 'horizontal: Z (front on the left)    vertical: Y up')
    bl = [(c.label.split(' (')[0], anchor(sp, c, 'south')) for c in sp.cubes if c.label and c.origin[2] + c.size[2] / 2 > 1.2][:5]
    grid_view(sh, d, sp, tex, Cam(180, 0, S), (1284, top, 1724, bot), 'BACK', None, [(t, p) for t, p in bl], 'horizontal: X (mirrored)    vertical: Y up', only_right=True)
    # 3D panel
    box = (1740, top, 2212, bot); panel(d, box, '3D VIEW')
    d.rounded_rectangle([box[0] + 14, box[1] + 46, box[2] - 14, box[3] - 14], 10, fill=(235, 233, 243))
    a, _ = render(sp, tex, Cam(-35, 22, 12.5)); b, _ = render(sp, tex, Cam(145, 22, 6.5))
    sh.alpha_composite(a, ((box[0] + box[2]) // 2 - a.width // 2, box[1] + 70))
    sh.alpha_composite(b, (box[2] - 30 - b.width, box[3] - 30 - b.height))
    d.text((box[0] + 26, box[3] - 40), 'front-right, and back-left (small)', font=FR(11), fill=SUB)

    # ---------------------------------------------------------- texture + tables
    y2 = bot + 18; y2b = y2 + 600
    tb = (28, y2, 812, y2b); panel(d, tb, f'TEXTURE  ({sp.W} x {sp.H}, box UV)', f'textures/entity/villager/{sp.id}.png')
    k = min((tb[2] - tb[0] - 40) // sp.W, (tb[3] - tb[1] - 110) // sp.H)
    tw, th = sp.W * k, sp.H * k; tx, ty = tb[0] + 20, tb[1] + 50
    for yy in range(0, th, 8):
        for xx in range(0, tw, 8):
            d.rectangle([tx + xx, ty + yy, tx + xx + 7, ty + yy + 7], fill=(238, 238, 238) if (xx // 8 + yy // 8) % 2 else (250, 250, 250))
    sh.alpha_composite(tex.img.resize((tw, th), Image.NEAREST), (tx, ty))
    for i, c in enumerate(sp.cubes):
        u, v = c.uv; iw, ih = island(c)
        d.rectangle([tx + u * k, ty + v * k, tx + (u + iw) * k - 1, ty + (v + ih) * k - 1], outline=ACC)
        lab = str(i + 1); lw = d.textlength(lab, font=FB(11))
        d.rectangle([tx + u * k + 1, ty + v * k + 1, tx + u * k + lw + 5, ty + v * k + 14], fill=ACC)
        d.text((tx + u * k + 3, ty + v * k + 1), lab, font=FB(11), fill=(255, 255, 255))
    gl = tex.glowmask()
    if sp.W == 64:
        gk = 3; gx, gy = tx + tw + 30, ty + 22
    else:
        gk = 2; gx, gy = tx, ty + th + 30
    d.text((gx, gy - 20), 'Glowmask (emissive layer)', font=FR(12), fill=SUB)
    d.rectangle([gx - 1, gy - 1, gx + sp.W * gk, gy + sp.H * gk], fill=(30, 30, 36))
    sh.alpha_composite(gl.resize((sp.W * gk, sp.H * gk), Image.NEAREST), (gx, gy))
    nx, ny = (gx, gy + sp.H * gk + 10) if sp.W == 64 else (gx + sp.W * gk + 16, gy)
    for j, ln in enumerate([f'{sp.id}_glowmask.png', 'Numbers match the cube table.', 'Box UV per cube: top and bottom', 'on the first row, then right side,', 'front, left side, back.']):
        d.text((nx, ny + j * 17), ln, font=FM(11) if j == 0 else FR(11), fill=SUB)

    cb = (828, y2, 2212, y2b); panel(d, cb, 'CUBES AND BONES', 'values exactly as in the .geo.json (Bedrock: X mirrored from Blockbench view)')
    rows = []
    for i, c in enumerate(sp.cubes):
        (x, y, z), (w, h, dd) = c.origin, c.size
        rows.append((i + 1, c.bone, c.name, f'[{r6(-(x + w))}, {r6(y)}, {r6(z)}]', f'[{w}, {h}, {dd}]', f'[{c.uv[0]}, {c.uv[1]}]', c.inflate or ''))
    table(d, cb[0] + 18, cb[1] + 50, [('#', 34), ('bone', 100), ('cube', 110), ('origin', 168), ('size', 108), ('uv', 84), ('inflate', 60)], rows, rh=max(18, min(26, 520 // max(1, len(rows)))))
    brows = [(b.name, b.parent or '-', f'[{r6(-b.pivot[0])}, {r6(b.pivot[1])}, {r6(b.pivot[2])}]', f'[{b.rot[0]}, {b.rot[1]}, {b.rot[2]}]' if any(b.rot) else '-') for b in sp.bones]
    bx = cb[0] + 720
    d.text((bx, cb[1] + 46 - 18), '', font=FR(1))
    yb = table(d, bx, cb[1] + 50, [('bone', 112), ('parent', 82), ('pivot', 176), ('rotation', 120)], brows, rh=24)
    yb += 14
    for ln in ['Bone names match the vanilla villager (head, nose, body,', 'arms, right_leg, left_leg) so its walk, look and head-shake', 'animations carry over. Extra bones are this species\' own.',
               '', 'Heights in px. In game: px x 0.9375 / 16 = blocks.']:
        d.text((bx, yb), ln, font=FR(12), fill=SUB); yb += 18

    # ---------------------------------------------------------- palette, variants, professions
    y3 = y2b + 18
    d.text((28, y3), 'Palette', font=FB(18), fill=INK)
    keys = list(sp.palette.items()); per = 11; sw = (W - 56) // per
    for i, (kname, hx) in enumerate(keys):
        cx = 28 + (i % per) * sw; cy = y3 + 32 + (i // per) * 46
        d.rectangle([cx, cy, cx + 30, cy + 30], fill=hexc(hx), outline=LINE)
        d.text((cx + 38, cy + 1), kname, font=FR(12), fill=INK); d.text((cx + 38, cy + 16), hx, font=FM(11), fill=SUB)
    y4 = y3 + 40 + ((len(keys) + per - 1) // per) * 46 + 8
    vb = (28, y4, 1100, y4 + 400); panel(d, vb, 'BIOME VARIANTS', 'one texture per planet biome (VillagerType)')
    n = len(sp.variants); cw = (vb[2] - vb[0] - 32) // n
    for i, (vid, vname, pal) in enumerate(sp.variants):
        t = sp.texture(pal); im, _ = render(sp, t, Cam(-35, 18, 7.2))
        cx = vb[0] + 16 + i * cw
        d.rounded_rectangle([cx, vb[1] + 46, cx + cw - 12, vb[3] - 16], 8, fill=(235, 233, 243))
        sh.alpha_composite(im, (cx + (cw - 12 - im.width) // 2, vb[1] + 58))
        d.text((cx + 10, vb[3] - 56), vname, font=FB(12), fill=INK)
        d.text((cx + 10, vb[3] - 38), f'{sp.id}.png' if i == 0 else f'{sp.id}_{vid}.png', font=FM(10), fill=SUB)
    pb = (1116, y4, 2212, y4 + 400); panel(d, pb, 'PROFESSION LOOK', f'overlay repaints {sp.badge}')
    sig = sp.signature[0]
    demo = [('No profession', None), ('Librarian', '#b0342c'), ('Farmer', '#d8b13a'), ('Cleric', '#7b3fa0'), (sig, sp.sig_colour)]
    cw = (pb[2] - pb[0] - 32) // len(demo)
    for i, (nm, col) in enumerate(demo):
        t = recolour(tex, col) if col else tex
        im, _ = render(sp, t, Cam(-25, 12, 6.2)); cx = pb[0] + 16 + i * cw
        d.rounded_rectangle([cx, pb[1] + 46, cx + cw - 10, pb[3] - 16], 8, fill=(235, 233, 243))
        sh.alpha_composite(im, (cx + (cw - 10 - im.width) // 2, pb[1] + 58))
        d.text((cx + 8, pb[3] - 50), nm, font=FB(12), fill=INK)
        if col: d.rectangle([cx + 8, pb[3] - 32, cx + 22, pb[3] - 20], fill=hexc(col)); d.text((cx + 28, pb[3] - 33), col, font=FM(10), fill=SUB)
    # ---------------------------------------------------------- text
    y5 = y4 + 418
    c1, c2, c3 = (28, 740), (800, 1520), (1560, 2212)
    d.text((c1[0], y5), 'Who they are', font=FB(18), fill=INK)
    yy = text_block(d, c1[0], y5 + 32, sp.lore, FR(13), c1[1] - c1[0], gap=5)
    d.text((c1[0], yy + 12), 'Behaviour', font=FB(18), fill=INK)
    yy = text_block(d, c1[0], yy + 44, sp.behaviour, FR(13), c1[1] - c1[0], gap=5)
    nm, job, trades = sp.signature
    d.text((c2[0], y5), f'Signature profession: {nm}', font=FB(18), fill=INK)
    d.text((c2[0], y5 + 30), f'Job site: zerog_tweaks:{job} (a new PoiType on that block). The vanilla professions also work.', font=FR(13), fill=SUB)
    yy = table(d, c2[0], y5 + 62, [('Level', 120), ('Buys from the player', 290), ('Sells', 300)], trades, font=FR(13), rh=26)
    d.text((c2[0], yy + 8), 'Prices are starting points; tune in playtesting. No trade sells an ingot above the planet\'s own tier.', font=FR(12), fill=SUB)
    d.text((c3[0], y5), 'Animations', font=FB(18), fill=INK)
    yy = y5 + 32
    for an, desc in sp.anims:
        d.text((c3[0], yy), f'animation.{sp.id}.{an}', font=FM(12), fill=ACC)
        yy = text_block(d, c3[0] + 14, yy + 18, desc, FR(12), c3[1] - c3[0] - 14, gap=3) + 6
    d.text((c3[0], yy + 8), 'Notes for the artist and code', font=FB(18), fill=INK)
    yy += 40
    for nt in sp.notes:
        d.text((c3[0], yy), '•', font=FR(13), fill=INK)
        yy = text_block(d, c3[0] + 14, yy, nt, FR(13), c3[1] - c3[0] - 14, gap=4) + 4
    fy = max(yy, y5 + 420) + 30
    d.text((28, fy), f'Files: blockbench/villagers/{sp.id}/{sp.id}.geo.json · {sp.id}.animation.json · {sp.id}.png (+ biome variants, glowmask, profession overlays) · '
                          f'generator generators/villagers/build_villagers.py', font=FR(12), fill=SUB)
    sh.crop((0, 0, W, fy + 40)).convert('RGB').save(out_png)
    return yy
