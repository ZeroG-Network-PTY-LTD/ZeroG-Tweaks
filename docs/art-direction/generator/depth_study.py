"""Study sheet: gradients, depth, 2D perspective and 3D model depth for ZeroG pixel art. Usage: python3 depth_study.py <out.png>"""
import sys, os, math, colorsys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcrender import render, Cam

FP = '/usr/share/fonts/truetype/dejavu/'
F = lambda s, b=False: ImageFont.truetype(FP + ('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'), s)
BG, INK, SUB, PANEL = (21, 20, 28), (233, 231, 242), (150, 146, 170), (30, 29, 40)
S = 8  # display scale for 32 px sprites


def hsv(h, s, v): r, g, b = colorsys.hsv_to_rgb((h % 360) / 360, max(0, min(1, s)), max(0, min(1, v))); return (int(r * 255), int(g * 255), int(b * 255), 255)


def ramp(base_h, n=6, shift_dark=40, shift_light=-25, sat=(.55, .45, .18), val=(.16, .97)):
    """Hue-shifted ramp, dark to light. Shadows rotate toward blue/violet (+), highlights toward warm (-)."""
    out = []
    for i in range(n):
        t = i / (n - 1)
        h = base_h + shift_dark * (1 - t) ** 1.3 + shift_light * t ** 2
        s = sat[0] * (1 - t) + sat[1] * (1 - abs(2 * t - 1)) * .6 + sat[2] * t if t > .5 else sat[0] * (1 - t * .5)
        v = val[0] + (val[1] - val[0]) * t ** .9
        out.append(hsv(h, s, v))
    return out


def flat_ramp(base_h, n=6):
    return [hsv(base_h, .25, .16 + .8 * i / (n - 1)) for i in range(n)]


def sprite(w=32, h=32): return Image.new('RGBA', (w, h), (0, 0, 0, 0))


def up(im, k=S): return im.resize((im.width * k, im.height * k), Image.NEAREST)


# ---------------------------------------------------------------- 1. gradients on a sphere
def sphere(r, mode):
    im = sprite(); L = (-.55, -.6, .58); n = math.sqrt(sum(v * v for v in L)); L = tuple(v / n for v in L)
    for y in range(32):
        for x in range(32):
            dx, dy = (x - 15.5) / 13, (y - 15.5) / 13; d2 = dx * dx + dy * dy
            if d2 > 1: continue
            dz = math.sqrt(1 - d2); lam = max(0, dx * L[0] + dy * L[1] + dz * L[2])
            if mode == 'flat': c = r[3]
            elif mode == 'smooth':                                    # banded/greyscale value gradient: no hue change
                g = int(40 + 200 * lam); c = (g, g, int(g * 1.05), 255)
            else:
                idx = min(len(r) - 2, int(lam * (len(r) - 1.2)) + 1)
                if d2 > .86: idx = max(1, idx - 1)                    # rim falls off one step
                c = r[idx]
            im.putpixel((x, y), c)
    if mode == 'ramp':                                                # dark-hue outline + specular cluster + bounce light
        for y in range(32):
            for x in range(32):
                if im.getpixel((x, y))[3] and any(not (0 <= x + a < 32 and 0 <= y + b < 32) or not im.getpixel((x + a, y + b))[3] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    im.putpixel((x, y), r[0])
        for (x, y) in ((10, 9), (11, 9), (10, 10), (12, 8)): im.putpixel((x, y), (255, 255, 255, 255))
        for x in range(13, 21): im.putpixel((x, 27), r[2])
    return im


# ---------------------------------------------------------------- 2. depth on an ingot (3/4 view)
def _inside(poly, x, y):
    """pixel-centre point-in-polygon, so faces tile with no stray edge pixels"""
    px, py = x + .5, y + .5; c = False; n = len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1: c = not c
    return c


INGOT = dict(top=[(5, 13), (20, 8), (28, 11), (13, 16)], end=[(5, 13), (13, 16), (13, 23), (5, 20)], front=[(13, 16), (28, 11), (28, 18), (13, 23)])


def ingot(stage, r, accent=((180, 120, 255, 255), (110, 230, 255, 255))):
    im = sprite(); face = {}
    for y in range(32):
        for x in range(32):
            for k in ('top', 'end', 'front'):
                if _inside(INGOT[k], x, y): face[(x, y)] = k; break
    tone = {'top': r[4], 'end': r[3], 'front': r[2]}
    shape = set(face)
    if stage == 0:
        for (x, y) in shape:
            if any((x + a, y + b) not in shape for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))): im.putpixel((x, y), r[1])
        return im
    for p, k in face.items(): im.putpixel(p, tone[k])
    if stage >= 2:
        for (x, y), k in face.items():
            if k == 'top' and (face.get((x, y + 1)) in ('end', 'front')): im.putpixel((x, y), r[5])        # lit bevel where the top turns down
            if k == 'end' and face.get((x + 1, y)) == 'front': im.putpixel((x, y), r[4])                     # lit vertical corner
            if k == 'front' and (x, y + 1) not in shape: im.putpixel((x, y), r[1])                          # shadowed bottom edge
        for x in range(32):
            for y in range(32):
                if (x, y) not in shape and any((x + a, y + b) in shape for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))): im.putpixel((x, y), r[0])
    if stage >= 3:
        for (x, y) in sorted(shape):
            g = (x + 1, y + 2)
            if g not in shape and 0 <= g[0] < 32 and 0 <= g[1] < 32 and im.getpixel(g)[3] == 0: im.putpixel(g, (0, 0, 0, 70))   # contact shadow
        for (x, y, c) in ((15, 12, 0), (19, 11, 1), (22, 10, 0), (18, 18, 1), (23, 16, 0)):                # flecks: bright core, dark lower pixel
            im.putpixel((x, y), (255, 255, 255, 255) if c == 0 and x == 15 else accent[c]); im.putpixel((x + 1, y), accent[c])
            im.putpixel((x, y + 1), tuple(int(v * .55) for v in accent[c][:3]) + (255,))
    return im


def sword(r, accent=(180, 120, 255, 255)):
    """blade on the 45 degree diagonal: tones by side of the axis, glowing fuller on the axis"""
    im = sprite(); cells = {}
    ax0, ay0, ax1, ay1 = 10, 21, 27, 4                        # blade axis, tip top-right
    for y in range(32):
        for x in range(32):
            t = ((x - ax0) * (ax1 - ax0) + (y - ay0) * (ay1 - ay0)) / ((ax1 - ax0) ** 2 + (ay1 - ay0) ** 2)
            if not 0 <= t <= 1: continue
            dx, dy = ax0 + t * (ax1 - ax0), ay0 + t * (ay1 - ay0)
            perp = ((x - dx) + (y - dy)) / math.sqrt(2)            # + toward bottom-right
            width = 1.6 if t < .88 else 1.6 * (1 - (t - .88) / .12) + .3
            if abs(perp) <= width: cells[(x, y)] = perp
    for (x, y), p in cells.items():
        im.putpixel((x, y), r[5] if p < -.9 else (r[4] if p < -.2 else (r[3] if p < .6 else r[2])))
    for i in range(3, 14): im.putpixel((ax0 + i, ay0 - i), accent if i % 4 else (230, 210, 255, 255))      # glowing fuller
    guard = [(7, 20), (8, 21), (9, 22), (10, 23), (11, 24), (8, 19), (12, 25)]
    for (x, y) in guard: im.putpixel((x, y), (214, 150, 80, 255))
    for (x, y) in ((8, 20), (9, 21), (10, 22)): im.putpixel((x, y), (250, 205, 130, 255))
    for i in range(4): im.putpixel((8 - i, 23 + i), (96, 66, 44, 255)); im.putpixel((9 - i, 23 + i), (70, 46, 30, 255))
    for (x, y) in ((3, 27), (4, 27), (3, 28), (4, 28)): im.putpixel((x, y), accent)
    im.putpixel((3, 27), (240, 225, 255, 255))
    shape = {(x, y) for x in range(32) for y in range(32) if im.getpixel((x, y))[3]}
    for x in range(32):
        for y in range(32):
            if (x, y) not in shape and any((x + a, y + b) in shape for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))): im.putpixel((x, y), r[0])
    return im


# ---------------------------------------------------------------- 3. 2D perspective
def views(r):
    out = []
    a = sprite(); d = ImageDraw.Draw(a); d.rectangle([5, 12, 26, 19], fill=r[3], outline=r[0]); d.line([(6, 13), (25, 13)], fill=r[5]); out.append(('Side-on: flat, no depth', a))
    out.append(('3/4 oblique: top + front + end', ingot(3, r)))
    c = sprite(); d = ImageDraw.Draw(c)
    T, Lf, Rf = [(16, 4), (28, 10), (16, 16), (4, 10)], [(4, 10), (16, 16), (16, 29), (4, 23)], [(16, 16), (28, 10), (28, 23), (16, 29)]
    d.polygon(T, fill=r[4]); d.polygon(Lf, fill=r[3]); d.polygon(Rf, fill=r[2])
    for poly in (T, Lf, Rf): d.polygon(poly, outline=r[0])
    d.line([(16, 17), (16, 28)], fill=r[4]); out.append(('Isometric block: 2:1 pixel lines', c))
    s = sword(r)
    out.append(('Tool: 45 degree diagonal, 1:1 steps', s))
    return out


# ---------------------------------------------------------------- 4. 3D model depth (Blockbench-style item made of cubes)
def blade_model():
    T = {'steel': None}
    els = []
    def E(a, b, tex): els.append({'from': a, 'to': b, 'faces': {f: {'uv': [0, 0, 16, 16], 'texture': '#' + tex} for f in ('north', 'south', 'east', 'west', 'up', 'down')}})
    E([7, 0, 7.5], [9, 4, 8.5], 'grip')                # grip: 1 px deep
    E([5, 4, 7], [11, 5, 9], 'guard')                  # guard: wider and 2 px deep, so it stands proud
    E([7, 5, 7.25], [9, 15, 8.75], 'steel')            # blade body 1.5 px deep
    E([7.6, 6, 7.0], [8.4, 14, 7.25], 'glow')          # fuller inlay raised 0.25 px on the front face
    E([7.5, 15, 7.5], [8.5, 16, 8.5], 'steel')         # tip
    E([7.25, -1, 7.25], [8.75, 0, 8.75], 'glow')       # pommel crystal
    return {'elements': els}


def solid(c):
    im = Image.new('RGBA', (16, 16), c)
    return im


def gradient_tex(r):
    im = Image.new('RGBA', (16, 16))
    for y in range(16):
        for x in range(16): im.putpixel((x, y), r[min(5, 1 + (15 - y) // 4 + (1 if x < 3 else 0))])
    return im


def sheet(out):
    steel = ramp(222, shift_dark=38, shift_light=-35)
    copper = ramp(22, shift_dark=-14, shift_light=18, sat=(.75, .55, .25))
    W, H = 2000, 1720
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((40, 26), 'Gradients, depth and perspective  —  ZeroG pixel-art study', font=F(30, True), fill=INK)
    d.text((40, 70), 'Light comes from the top-left front on every sprite and model. All sprites are native 32 x 32, shown x8.', font=F(15), fill=SUB)

    def panel(x, y, w, h, title):
        d.rounded_rectangle([x, y, x + w, y + h], 12, fill=PANEL); d.text((x + 20, y + 16), title, font=F(19, True), fill=INK)

    # 1 gradients
    panel(40, 110, 1920, 400, '1. Gradients: value alone vs a hue-shifted ramp')
    for i, (mode, cap) in enumerate((('flat', 'Flat fill: no form'), ('smooth', 'Smooth grey gradient: muddy, no colour'), ('ramp', 'Hue-shifted 6-tone ramp + outline + spec'))):
        sp = up(sphere(steel, mode)); x = 70 + i * 300; im.paste(sp, (x, 160), sp); d.text((x, 430), cap, font=F(13), fill=SUB)
    x0 = 1000; d.text((x0, 160), 'Steel ramp, dark to light', font=F(14, True), fill=INK)
    for i, c in enumerate(steel):
        d.rectangle([x0 + i * 70, 186, x0 + i * 70 + 62, 248], fill=c[:3])
        h, s_, v = colorsys.rgb_to_hsv(*[q / 255 for q in c[:3]]); d.text((x0 + i * 70, 252), f'H{int(h * 360)}', font=F(11), fill=SUB); d.text((x0 + i * 70, 266), f'S{int(s_ * 100)} V{int(v * 100)}', font=F(11), fill=SUB)
    d.text((x0, 296), 'Copper ramp (planet variant)', font=F(14, True), fill=INK)
    for i, c in enumerate(copper):
        d.rectangle([x0 + i * 70, 322, x0 + i * 70 + 62, 384], fill=c[:3])
        h, s_, v = colorsys.rgb_to_hsv(*[q / 255 for q in c[:3]]); d.text((x0 + i * 70, 388), f'H{int(h * 360)}', font=F(11), fill=SUB); d.text((x0 + i * 70, 402), f'S{int(s_ * 100)} V{int(v * 100)}', font=F(11), fill=SUB)
    rules = ['Value carries the form; hue and saturation carry the mood.', 'Shadows rotate toward blue/violet, highlights toward warm or white.',
             'Saturation peaks in the mid tones and drops at both ends.', 'Use 4-6 tones per material, placed in clusters, not dither noise.']
    for j, t in enumerate(rules): d.text((1440, 186 + j * 24), '• ' + t, font=F(13), fill=INK)

    # 2 depth in 2D
    panel(40, 530, 1920, 380, '2. Depth in a 2D sprite: build it in layers')
    caps = ['Silhouette only', '+ three faces, one tone each', '+ bevels and dark-hue outline', '+ contact shadow, glowing inlays']
    for i in range(4):
        sp = up(ingot(i, steel)); x = 70 + i * 300; im.paste(sp, (x, 575), sp); d.text((x, 845), caps[i], font=F(13), fill=SUB)
    for j, t in enumerate(['Each face of a form gets its own tone; the face toward the light is lightest.', 'A 1 px lighter line on edges that face the light reads as a bevel.',
                           'Outlines use the darkest tone of the material, never pure black.', 'A soft contact shadow sits the object on the ground.',
                           'Glow = light centre, mid ring, one darker rim pixel; only on parts that mean it.']):
        d.text((1300, 590 + j * 26), '• ' + t, font=F(13), fill=INK)

    # 3 2D perspective
    panel(40, 930, 1920, 380, '3. 2D perspective: how the sprite is "seen"')
    for i, (cap, sp) in enumerate(views(steel)):
        sp = up(sp); x = 70 + i * 300; im.paste(sp, (x, 975), sp); d.text((x, 1245), cap, font=F(13), fill=SUB)
    for j, t in enumerate(['Items: 3/4 oblique, so the top and one side show (ingots, ores, armour).', 'Blocks in inventory: isometric, edges on clean 2:1 pixel steps.',
                           'Tools and weapons: on the 45 degree diagonal, head top-right, 1:1 steps.', 'Keep one viewpoint per sprite; never mix a flat front with an angled top.',
                           'Foreshortened faces are shorter and darker; the face toward the viewer is widest.']):
        d.text((1300, 990 + j * 26), '• ' + t, font=F(13), fill=INK)

    # 4 3D depth
    panel(40, 1330, 1920, 360, '4. 3D model depth (Blockbench): thickness tells the eye what matters')
    model = blade_model()
    tex = {'steel': gradient_tex(steel), 'grip': solid((96, 66, 44, 255)), 'guard': gradient_tex(copper), 'glow': solid((180, 120, 255, 255))}
    for i, (yaw, pitch, cap) in enumerate(((-35, 20, '3/4 view: guard stands proud, inlay sits on top'), (-90, 0, 'Side: depths 1 / 1.5 / 2 px read as layers'), (0, 0, 'Front: same silhouette as the 2D sprite'))):
        r = render(model, tex, Cam(yaw, pitch, 14), bg=PANEL, emissive={'glow'}); x = 70 + i * 300
        im.paste(r, (x + (260 - r.width) // 2, 1375 + (250 - r.height) // 2), r); d.text((x, 1640), cap, font=F(13), fill=SUB)
    for j, t in enumerate(['Vary depth by role: grip 1 px, blade 1.5 px, guard 2 px, inlays +0.25 px.', 'Raised details catch light on their top and sides; recessed ones get a dark rim.',
                           'Paint the gradient on each face too: light at the top, dark toward the bottom.', 'In-hand display transforms must keep the lit side facing the camera.',
                           'Block icons use the gui transform [30, 225, 0] so they match the isometric 2D rule.']):
        d.text((1000, 1390 + j * 26), '• ' + t, font=F(13), fill=INK)
    im.save(out)


if __name__ == '__main__':
    sheet(sys.argv[1])
