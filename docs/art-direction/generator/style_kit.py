"""ZeroG art-style kit: hand-tuned hue-shifted ramps, index-mapped 32 px sprites, and a lit 3D renderer that shades by
moving along the ramp (so shadows shift hue instead of just darkening). Index maps: ints 0-5 = material ramp, ('a', i) = glow
accent ramp index (unlit), ('m', name, i) = second material ramp, None = transparent."""
import math, random
from PIL import Image, ImageDraw

# dark -> light, 6 tones each. Shadows lean blue/violet, highlights pale or warm; saturation peaks in the middle.
RAMPS = {
    'moonsteel': ['#141326', '#2b2a4a', '#454a78', '#6a7bb0', '#9fb6d8', '#e6f4ff'],
    'copper':    ['#1e0d0b', '#4a1f17', '#83391f', '#c0622c', '#eb9a52', '#ffd9a0'],
    'nullifite': ['#0b0712', '#231536', '#3f2766', '#6a45a8', '#a07ee0', '#e2d4ff'],
    'solvanite': ['#1f0e05', '#5a2b0a', '#a3570f', '#e09a1c', '#ffd04a', '#fff4c0'],
    'cerulite':  ['#06141f', '#0e3550', '#14648a', '#1fa2c4', '#5fe0f0', '#dcffff'],
    'leaf':      ['#0a1a1c', '#14383a', '#1f5e58', '#2f8a78', '#58b894', '#a8e6c0'],
    'glow':      ['#2a0e4a', '#5a22a0', '#9a4ef0', '#c48cff', '#e8ccff', '#ffffff'],
    'rock':      ['#121220', '#272838', '#3e4052', '#5c5f74', '#85899c', '#b9bccb'],
    'tint_gray': ['#161616', '#363636', '#5a5a5a', '#868686', '#b6b6b6', '#ececec'],
    'wood':      ['#1a0e0a', '#3c2216', '#5e3a24', '#875a36', '#b0824e', '#dcb27a'],
}


def hx(h, a=255): h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


R = {k: [hx(c) for c in v] for k, v in RAMPS.items()}


def blank(w=32, h=32): return [[None] * w for _ in range(h)]


def inside(poly, x, y):
    px, py = x + .5, y + .5; c = False; n = len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1: c = not c
    return c


def outline(m, idx=0, ramp=None):
    """dark-hue outline just outside the silhouette (4-neighbour)"""
    h, w = len(m), len(m[0]); add = []
    for y in range(h):
        for x in range(w):
            if m[y][x] is None and any(0 <= x + a < w and 0 <= y + b < h and m[y + b][x + a] is not None for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                add.append((x, y))
    for x, y in add: m[y][x] = idx if ramp is None else ('m', ramp, idx)
    return m


def colour(tok, mat, shift=0, glow_boost=0):
    if tok is None: return None
    if isinstance(tok, tuple):
        if tok[0] == 'a': return R['glow' if len(tok) < 3 else tok[2]][min(5, tok[1] + glow_boost)]
        if tok[0] == 'm': i = tok[2]; return R[tok[1]][i if i == 0 else max(1, min(5, i + shift))]
    return R[mat][tok if tok == 0 else max(1, min(5, tok + shift))]


def to_image(m, mat, shift=0, glow_boost=0):
    h, w = len(m), len(m[0]); im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            c = colour(m[y][x], mat, shift, glow_boost)
            if c: im.putpixel((x, y), c)
    return im


# ------------------------------------------------------------------ sprites (index maps, light from top-left)
def ingot():
    m = blank(); face = {}
    P = dict(top=[(5, 14), (20, 9), (28, 12), (13, 17)], end=[(5, 14), (13, 17), (13, 24), (5, 21)], front=[(13, 17), (28, 12), (28, 19), (13, 24)])
    for y in range(32):
        for x in range(32):
            for k in ('top', 'end', 'front'):
                if inside(P[k], x, y): face[(x, y)] = k; break
    base = {'top': 4, 'end': 3, 'front': 2}
    for (x, y), k in face.items():
        v = base[k]
        if k == 'top' and (x - 5) < 6: v = 5 if (x + y) % 7 else 4                         # top-left of the top face catches the most light
        if k == 'front' and y - (12 + (28 - x) * 5 / 15) > 4.5: v = 1                        # lower band of the front falls into shadow
        if k == 'top' and face.get((x, y + 1)) in ('end', 'front'): v = 5                    # bevel highlight
        if k == 'end' and face.get((x + 1, y)) == 'front': v = 4                             # lit corner
        if k == 'front' and (x, y + 1) not in face: v = 1
        m[y][x] = v
    for (x, y) in ((16, 13), (17, 13), (21, 11), (19, 19), (23, 17), (24, 17)): m[y][x] = ('a', 3)   # inlaid crystal flecks
    m[13][16] = ('a', 5); m[19][19] = ('a', 4)
    for (x, y) in ((16, 14), (21, 12), (19, 20), (23, 18)): m[y][x] = ('a', 1)
    return outline(m)


def raw_ore():
    m = blank(); rnd = random.Random(4)
    blobs = [(13, 20, 7.0), (20, 17, 6.4), (19, 24, 5.0), (9, 24, 4.4), (25, 22, 4.2)]
    L = _norm((-.6, -.75, .45))
    hmap = {}
    for y in range(32):
        for x in range(32):
            h = max((math.sqrt(max(0, r * r - (x - cx) ** 2 - (y - cy) ** 2)) for cx, cy, r in blobs), default=0)
            if h > .4: hmap[(x, y)] = h
    for (x, y), h in hmap.items():
        hx_ = hmap.get((x + 1, y), 0) - hmap.get((x - 1, y), 0); hy_ = hmap.get((x, y + 1), 0) - hmap.get((x, y - 1), 0)
        n = _norm((-hx_, -hy_, 1.6)); lam = max(0, sum(a * b for a, b in zip(n, L)))
        v = max(2, min(5, 2 + int(lam * 3.6)))
        if rnd.random() < .07: v = max(1, v - 1)
        m[y][x] = ('m', 'rock', v)
    def crystal(base, tip, w, ramp):
        bx, by = base; tx, ty = tip
        left = [(bx - w, by + .5), (tx - .5, ty), (bx, by + 1.5)]; right = [(bx, by + 1.5), (tx + .5, ty), (bx + w, by + .5)]
        for y in range(32):
            for x in range(32):
                if inside(left, x, y): m[y][x] = ('a', 4, ramp)
                elif inside(right, x, y): m[y][x] = ('a', 2, ramp)
        for k in range(3):                                                                    # bright ridge down the lit facet
            yy = ty + 1 + k * 2; xx = int(round(tx + (bx - tx) * (yy - ty) / max(1, by - ty))) - 1
            if 0 <= yy < 32 and 0 <= xx < 32 and m[yy][xx] is not None: m[yy][xx] = ('a', 5, ramp)
        m[ty][tx] = ('a', 5, ramp)
    crystal((12, 17), (9, 6), 3.6, 'cerulite'); crystal((19, 15), (21, 5), 3.2, 'glow'); crystal((23, 20), (27, 12), 2.8, 'cerulite')
    crystal((8, 23), (5, 16), 2.4, 'glow'); crystal((16, 22), (16, 15), 2.0, 'cerulite')
    return outline(m, 0, 'rock')


def dust():
    m = blank(); rnd = random.Random(9)
    peak = 15
    for x in range(3, 30):
        d = abs(x - peak) / (12.5 if x < peak else 13.5)
        top = 27 - 14 * max(0, 1 - d ** 1.25) + rnd.choice((0, 0, 0, 1))
        for y in range(int(top), 28):
            depth = (y - top) / max(1, 28 - top)
            lit = (x < peak + 2 and depth < .5)
            v = 4 if lit else (3 if depth < .55 else 2)
            if x < peak - 4 and depth < .25: v = 5
            if depth > .8: v = 1
            m[y][x] = v
    for _ in range(90):                                                                        # grain clusters: 1-2 px, one step lighter or darker
        x, y = rnd.randrange(4, 29), rnd.randrange(13, 27)
        if isinstance(m[y][x], int):
            d = rnd.choice((-1, 1, 1))
            m[y][x] = max(1, min(5, m[y][x] + d))
            if rnd.random() < .5 and x + 1 < 32 and isinstance(m[y][x + 1], int): m[y][x + 1] = max(1, min(5, m[y][x + 1] + d))
    for (x, y) in ((1, 27), (31, 27), (2, 26), (30, 26)): m[y][x] = 2                         # loose grains at the foot
    for (x, y) in ((11, 18), (16, 15), (20, 21), (8, 23), (14, 23), (24, 25)): m[y][x] = ('a', 5, 'cerulite')   # star glints
    return outline(m)


def sword():
    m = blank()
    ax0, ay0, ax1, ay1 = 11, 20, 27, 4
    for y in range(32):
        for x in range(32):
            t = ((x - ax0) * (ax1 - ax0) + (y - ay0) * (ay1 - ay0)) / ((ax1 - ax0) ** 2 + (ay1 - ay0) ** 2)
            if not 0 <= t <= 1: continue
            dx, dy = ax0 + t * (ax1 - ax0), ay0 + t * (ay1 - ay0)
            p = ((x - dx) + (y - dy)) / math.sqrt(2)
            wd = 1.7 if t < .86 else 1.7 * (1 - (t - .86) / .14) + .25
            if abs(p) <= wd: m[y][x] = 5 if p < -1 else (4 if p < -.3 else (3 if p < .5 else 2))
    for i in range(3, 13): m[ay0 - i][ax0 + i] = ('a', 3 if i % 4 else 5)
    for (x, y) in ((8, 19), (9, 20), (10, 21), (11, 22), (12, 23), (7, 18), (13, 24)): m[y][x] = ('m', 'copper', 3)
    for (x, y) in ((8, 19), (9, 20), (10, 21)): m[y][x] = ('m', 'copper', 5)
    for (x, y) in ((12, 23), (13, 24)): m[y][x] = ('m', 'copper', 2)
    for i in range(4): m[23 + i][9 - i] = ('m', 'wood', 3); m[23 + i][10 - i] = ('m', 'wood', 2)
    for (x, y) in ((4, 27), (5, 27), (4, 28), (5, 28)): m[y][x] = ('a', 3)
    m[27][4] = ('a', 5)
    return outline(m)


def block_texture(mat_inlay=True):
    """32 x 32 plated block face: four bevelled plates, rivets, a glowing cross inlay where the plates meet"""
    m = blank()
    for y in range(32):
        for x in range(32):
            px, py = x % 16, y % 16
            v = 3 if px + py < 18 else 2                                                        # diagonal light falloff across each plate
            if px + py < 8: v = 4
            if py == 0 or px == 0: v = 5 if (py == 0 and px < 15) or (px == 0 and py < 15) else 4
            if py == 15 or px == 15: v = 1
            if (px in (1, 2) and py in (14,)) or (py == 1 and px == 14): v = 2
            m[y][x] = v
    for (cx, cy) in ((3, 3), (12, 3), (3, 12), (12, 12)):
        for (ox, oy) in ((0, 0), (16, 0), (0, 16), (16, 16)):
            m[cy + oy][cx + ox] = 5; m[cy + oy + 1][cx + ox + 1] = 1
    if mat_inlay:
        for i in range(12, 20): m[15][i] = ('a', 3); m[16][i] = ('a', 2); m[i][15] = ('a', 3); m[i][16] = ('a', 2)
        for (x, y) in ((15, 15), (16, 15), (15, 16), (16, 16)): m[y][x] = ('a', 5)
    for i in range(32): m[0][i] = 5 if m[0][i] != 1 else 1
    return m


# ------------------------------------------------------------------ lit renderer: faces shade by stepping along the ramp
def _norm(v): n = math.sqrt(sum(a * a for a in v)) or 1; return tuple(a / n for a in v)


def ramp_shift(nrm, light, ambient=.35):
    lam = max(0.0, sum(a * b for a, b in zip(nrm, light)))
    v = ambient + (1 - ambient) * lam                                                           # 0.35 .. 1
    return int(round((v - .72) * 4.5))                                                          # about -2 .. +1 ramp steps


class Cam:
    def __init__(s, yaw, pitch, scale):
        s.cy, s.sy, s.cp, s.sp, s.k = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), math.cos(math.radians(pitch)), math.sin(math.radians(pitch)), scale

    def tr(s, p):
        x, y, z = p; xr = x * s.cy - z * s.sy; zr = x * s.sy + z * s.cy
        return (xr * s.k, -(y * s.cp + zr * s.sp) * s.k, zr * s.cp - y * s.sp)

    def faces(s, n):
        zr = n[0] * s.sy + n[2] * s.cy; return zr * s.cp - n[1] * s.sp < -1e-6


def rot_y(p, a):
    c, s_ = math.cos(a), math.sin(a); x, y, z = p; return (x * c + z * s_, y, -x * s_ + z * c)


def lit_cube(tex_map, mat, cam, light, size=1.0, center=(0, 0, 0), spin=0.0, glow_boost=0):
    """returns polygons for a cube whose six faces use the same 32 px index map"""
    h = size / 2; N = len(tex_map); polys = []
    faces = {'north': ((0, 0, -1), lambda a, b: (h - a * size, h - b * size, -h)), 'south': ((0, 0, 1), lambda a, b: (-h + a * size, h - b * size, h)),
             'east': ((1, 0, 0), lambda a, b: (h, h - b * size, h - a * size)), 'west': ((-1, 0, 0), lambda a, b: (-h, h - b * size, -h + a * size)),
             'up': ((0, 1, 0), lambda a, b: (-h + a * size, h, -h + b * size)), 'down': ((0, -1, 0), lambda a, b: (-h + a * size, -h, h - b * size))}
    for f, (n, pt) in faces.items():
        n2 = rot_y(n, spin)
        if not cam.faces(n2): continue
        sh_ = ramp_shift(n2, light)
        for j in range(N):
            for i in range(N):
                tok = tex_map[j][i]; c = colour(tok, mat, sh_, glow_boost)
                if not c: continue
                q = [rot_y(pt(a, b), spin) for a, b in ((i / N, j / N), ((i + 1) / N, j / N), ((i + 1) / N, (j + 1) / N), (i / N, (j + 1) / N))]
                q = [cam.tr((p[0] + center[0], p[1] + center[1], p[2] + center[2])) for p in q]
                polys.append((sum(p[2] for p in q) / 4, [(p[0], p[1]) for p in q], c))
    return polys


def extruded(sprite_map, mat, cam, light, spin, center, scale=1.0, thick=1 / 16, glow_boost=0):
    """Minecraft generated-item style: the sprite extruded 1 px deep, spinning around Y. Edge faces step darker along the ramp."""
    N = len(sprite_map); s = scale / N; polys = []
    solid = lambda x, y: 0 <= x < N and 0 <= y < N and sprite_map[y][x] is not None
    nf, nb = rot_y((0, 0, -1), spin), rot_y((0, 0, 1), spin)
    for y in range(N):
        for x in range(N):
            tok = sprite_map[y][x]
            if tok is None: continue
            x0, x1 = (x - N / 2) * s, (x + 1 - N / 2) * s; y0, y1 = (N / 2 - y - 1) * s, (N / 2 - y) * s; z0, z1 = -thick * scale / 2, thick * scale / 2
            quads = [(nf, [(x1, y1, z0), (x0, y1, z0), (x0, y0, z0), (x1, y0, z0)], 0), (nb, [(x0, y1, z1), (x1, y1, z1), (x1, y0, z1), (x0, y0, z1)], 0)]
            if not solid(x - 1, y): quads.append((rot_y((-1, 0, 0), spin), [(x0, y1, z0), (x0, y1, z1), (x0, y0, z1), (x0, y0, z0)], -1))
            if not solid(x + 1, y): quads.append((rot_y((1, 0, 0), spin), [(x1, y1, z1), (x1, y1, z0), (x1, y0, z0), (x1, y0, z1)], -1))
            if not solid(x, y - 1): quads.append((rot_y((0, 1, 0), spin), [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], 0))
            if not solid(x, y + 1): quads.append((rot_y((0, -1, 0), spin), [(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)], -2))
            for n, q, extra in quads:
                if not cam.faces(n): continue
                c = colour(tok, mat, ramp_shift(n, light) + extra, glow_boost)
                qq = [cam.tr(tuple(a + b for a, b in zip(rot_y(p, spin), center))) for p in q]
                polys.append((sum(p[2] for p in qq) / 4, [(p[0], p[1]) for p in qq], c))
    return polys


def draw(polys, size, bg, offset=(0, 0)):
    im = Image.new('RGB', size, bg); d = ImageDraw.Draw(im, 'RGBA')
    for _, ps, c in sorted(polys, key=lambda t: -t[0]):
        d.polygon([(x + offset[0], y + offset[1]) for x, y in ps], fill=c)
    return im
