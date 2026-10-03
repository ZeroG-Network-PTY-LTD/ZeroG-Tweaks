"""Villager species kit: geometry in Blockbench space, box-UV packing, texture painting,
GeckoLib export and a software renderer for the reference sheets.

Coordinates: Blockbench space (three.js, right-handed, Y up). The model faces -Z (north).
+X is the model's RIGHT side (it appears on the viewer's left in a front view).
On export the Bedrock/GeckoLib file mirrors X (origin_x = -(x + w), pivot_x = -px), the same
conversion Blockbench does, so `right_leg` keeps vanilla's position in the file.
"""
import json, math, random, os
from PIL import Image, ImageDraw, ImageFont

FP = '/usr/share/fonts/truetype/dejavu/'
FB = lambda s: ImageFont.truetype(FP + 'DejaVuSans-Bold.ttf', s)
FR = lambda s: ImageFont.truetype(FP + 'DejaVuSans.ttf', s)
FM = lambda s: ImageFont.truetype(FP + 'DejaVuSansMono.ttf', s)
INK, SUB, LINE, BG, PANEL, ACC = (34, 32, 40), (110, 108, 118), (205, 203, 214), (246, 245, 242), (255, 255, 255), (124, 92, 230)
RENDER_SCALE = 0.9375          # same as VillagerRenderer, so a 34 px model stands ~2 blocks tall
HITBOX = (0.6, 1.95)           # vanilla villager: fits 1 x 2 doors


def hexc(h, a=255):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def shade(c, k):
    return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3] if len(c) > 3 else 255,)


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,)


class Bone:
    def __init__(self, name, parent=None, pivot=(0, 0, 0), rot=(0, 0, 0)):
        self.name, self.parent, self.pivot, self.rot = name, parent, pivot, rot


class Cube:
    def __init__(self, bone, name, origin, size, paint=None, inflate=0.0, label=None):
        self.bone, self.name, self.origin, self.size, self.paint, self.inflate, self.label = bone, name, origin, size, paint, inflate, label
        self.uv = None


def island(c):
    w, h, d = c.size
    return 2 * (w + d), d + h


def pack(cubes, sizes=((64, 64), (128, 64), (128, 128))):
    order = sorted(cubes, key=lambda c: (-island(c)[1], -island(c)[0]))
    for W, H in sizes:
        x = y = row = 0; ok = True; pos = {}
        for c in order:
            iw, ih = island(c)
            if x + iw > W: x, y, row = 0, y + row, 0
            if iw > W or y + ih > H: ok = False; break
            pos[c.name] = (x, y); x += iw; row = max(row, ih)
        if ok:
            for c in cubes: c.uv = pos[c.name]
            return W, H
    raise ValueError('cubes do not fit in 128 x 128')


def face_rects(c):
    u, v = c.uv; w, h, d = c.size
    return {'top': (u + d, v, w, d), 'bottom': (u + d + w, v, w, d), 'east': (u, v + d, d, h),
            'north': (u + d, v + d, w, h), 'west': (u + d + w, v + d, d, h), 'south': (u + 2 * d + w, v + d, w, h)}


class Painter:
    """Paints one cube's six faces. Face-local (col, row): col 0 is the texture's left edge.
    north: col 0 at +X (viewer's left from the front), row 0 at the top. south: col 0 at -X.
    east (+X, model's right): col 0 at the back (+Z). west (-X): col 0 at the front (-Z).
    top: col 0 at +X, last row at the front edge."""
    def __init__(self, tex, cube, rng):
        self.t, self.c, self.rng, self.R = tex, cube, rng, face_rects(cube)

    def size(self, f):
        return self.R[f][2], self.R[f][3]

    def faces(self, f):
        return list(self.R) if f == 'all' else ([f] if isinstance(f, str) else list(f))

    def fill(self, f, col, noise=5, grad=0.10, edge=0.0):
        for ff in self.faces(f):
            u, v, w, h = self.R[ff]
            for r in range(h):
                for cc in range(w):
                    k = 1 + grad * (0.5 - (r + .5) / max(1, h)) if ff not in ('top', 'bottom') else (1.06 if ff == 'top' else .82)
                    if edge and (cc in (0, w - 1) or r in (0, h - 1)) and ff not in ('top', 'bottom'): k *= 1 - edge
                    n = self.rng.randint(-noise, noise)
                    self.t.img.putpixel((u + cc, v + r), tuple(max(0, min(255, int(col[i] * k) + n)) for i in range(3)) + (col[3],))

    def px(self, f, cc, r, col, glow=False, mask=None):
        for ff in self.faces(f):
            u, v, w, h = self.R[ff]
            if 0 <= cc < w and 0 <= r < h:
                self.t.img.putpixel((u + cc, v + r), col)
                if glow: self.t.glow.add((u + cc, v + r))
                if mask: self.t.masks.setdefault(mask, set()).add((u + cc, v + r))

    def rect(self, f, c0, r0, c1, r1, col, glow=False, noise=0, mask=None):
        for ff in self.faces(f):
            w, h = self.size(ff)
            for r in range(max(0, r0), min(h - 1, r1) + 1):
                for cc in range(max(0, c0), min(w - 1, c1) + 1):
                    cl = col if not noise else tuple(max(0, min(255, col[i] + self.rng.randint(-noise, noise))) for i in range(3)) + (col[3],)
                    self.px(ff, cc, r, cl, glow, mask)

    def row(self, f, r, col, **k):
        for ff in self.faces(f): self.rect(ff, 0, r, self.size(ff)[0] - 1, r, col, **k)

    def col(self, f, cc, col, **k):
        for ff in self.faces(f): self.rect(ff, cc, 0, cc, self.size(ff)[1] - 1, col, **k)

    def clear(self, f, c0, r0, c1, r1):
        self.rect(f, c0, r0, c1, r1, (0, 0, 0, 0))

    def rows_from_bottom(self, f, n, col, **k):
        for ff in self.faces(f):
            h = self.size(ff)[1]
            for r in range(h - n, h): self.row(ff, r, col, **k)

    def glow_all(self, f='all'):
        for ff in self.faces(f):
            u, v, w, h = self.R[ff]
            for r in range(h):
                for cc in range(w):
                    if self.t.img.getpixel((u + cc, v + r))[3]: self.t.glow.add((u + cc, v + r))


class Tex:
    def __init__(self, W, H):
        self.img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); self.glow = set(); self.masks = {}

    def glowmask(self):
        g = Image.new('RGBA', self.img.size, (0, 0, 0, 0))
        for p in self.glow: g.putpixel(p, self.img.getpixel(p))
        return g


class Species:
    def __init__(self, **k):
        self.__dict__.update(k)
        self.bmap = {b.name: b for b in self.bones}
        self.W, self.H = pack(self.cubes)

    def texture(self, palette=None):
        pal = dict(self.palette); pal.update(palette or {})
        P = {k: hexc(v) for k, v in pal.items()}
        t = Tex(self.W, self.H)
        for c in self.cubes:
            p = Painter(t, c, random.Random(self.id + c.name))
            c.paint(p, P)
        return t

    # ------------------------------------------------------------- export
    def geo(self):
        bones = []
        for b in self.bones:
            e = {'name': b.name}
            if b.parent: e['parent'] = b.parent
            e['pivot'] = [r6(-b.pivot[0]), r6(b.pivot[1]), r6(b.pivot[2])]
            if any(b.rot): e['rotation'] = list(b.rot)
            cs = []
            for c in self.cubes:
                if c.bone != b.name: continue
                (x, y, z), (w, h, d) = c.origin, c.size
                ce = {'origin': [r6(-(x + w)), r6(y), r6(z)], 'size': [w, h, d], 'uv': list(c.uv)}
                if c.inflate: ce['inflate'] = c.inflate
                cs.append(ce)
            if cs: e['cubes'] = cs
            bones.append(e)
        return {'format_version': '1.12.0', 'minecraft:geometry': [{
            'description': {'identifier': f'geometry.zerog_tweaks.{self.id}', 'texture_width': self.W, 'texture_height': self.H,
                            'visible_bounds_width': 3, 'visible_bounds_height': 3.5, 'visible_bounds_offset': [0, 1.25, 0]},
            'bones': bones}]}

    def height(self):
        return max(c.origin[1] + c.size[1] + c.inflate for c in self.cubes)


def r6(v):
    v = round(v, 4); return int(v) if v == int(v) else v


# ------------------------------------------------------------- geometry + renderer
def bone_chain(sp, name):
    out = []
    while name:
        b = sp.bmap[name]; out.append(b); name = b.parent
    return out                                          # child first


def rot_point(p, pivot, rot):
    """rot = file rotation in degrees (Bedrock). three.js angle = -x, -y, +z (Blockbench convention)."""
    x, y, z = p[0] - pivot[0], p[1] - pivot[1], p[2] - pivot[2]
    ax, ay, az = math.radians(-rot[0]), math.radians(-rot[1]), math.radians(rot[2])
    if az: x, y = x * math.cos(az) - y * math.sin(az), x * math.sin(az) + y * math.cos(az)
    if ay: x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    if ax: y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    return (x + pivot[0], y + pivot[1], z + pivot[2])


def world(sp, c, p, pose=None):
    for b in bone_chain(sp, c.bone):
        r = (pose or {}).get(b.name, b.rot)
        if any(r): p = rot_point(p, b.pivot, r)
    return p


def cube_quads(sp, c, tex, pose=None):
    """Yields (corners[4] world, normal-ref point, colour, glow) for every texel of every face."""
    (x0, y0, z0), (w, h, d) = c.origin, c.size; i = c.inflate
    x0, y0, z0, x1, y1, z1 = x0 - i, y0 - i, z0 - i, x0 + w + i, y0 + h + i, z0 + d + i
    sx, sy, sz = (x1 - x0) / w, (y1 - y0) / h, (z1 - z0) / d
    R = face_rects(c); T = tex.img
    def emit(face, cc, r, quad, n):
        u, v, fw, fh = R[face]
        col = T.getpixel((u + cc, v + r))
        if col[3] < 8: return None
        q = [world(sp, c, p, pose) for p in quad]
        o = world(sp, c, (0, 0, 0), pose); nn = world(sp, c, n, pose); nv = (nn[0] - o[0], nn[1] - o[1], nn[2] - o[2])
        return q, nv, col, (u + cc, v + r) in tex.glow
    out = []
    for r in range(h):
        ya, yb = y1 - r * sy, y1 - (r + 1) * sy
        for cc in range(w):
            xa, xb = x1 - cc * sx, x1 - (cc + 1) * sx
            out.append(emit('north', cc, r, [(xa, ya, z0), (xb, ya, z0), (xb, yb, z0), (xa, yb, z0)], (0, 0, -1)))
            xa, xb = x0 + cc * sx, x0 + (cc + 1) * sx
            out.append(emit('south', cc, r, [(xa, ya, z1), (xb, ya, z1), (xb, yb, z1), (xa, yb, z1)], (0, 0, 1)))
        for cc in range(d):
            za, zb = z1 - cc * sz, z1 - (cc + 1) * sz
            out.append(emit('east', cc, r, [(x1, ya, za), (x1, ya, zb), (x1, yb, zb), (x1, yb, za)], (1, 0, 0)))
            za, zb = z0 + cc * sz, z0 + (cc + 1) * sz
            out.append(emit('west', cc, r, [(x0, ya, za), (x0, ya, zb), (x0, yb, zb), (x0, yb, za)], (-1, 0, 0)))
    for r in range(d):
        for cc in range(w):
            xa, xb = x1 - cc * sx, x1 - (cc + 1) * sx
            za, zb = z1 - r * sz, z1 - (r + 1) * sz
            out.append(emit('top', cc, r, [(xa, y1, za), (xb, y1, za), (xb, y1, zb), (xa, y1, zb)], (0, 1, 0)))
            za, zb = z0 + r * sz, z0 + (r + 1) * sz
            out.append(emit('bottom', cc, r, [(xa, y0, za), (xb, y0, za), (xb, y0, zb), (xa, y0, zb)], (0, -1, 0)))
    return [q for q in out if q]


class Cam:
    def __init__(self, yaw=0, pitch=0, scale=10):
        self.cy, self.sy_, self.cp, self.sp_, self.s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), math.cos(math.radians(pitch)), math.sin(math.radians(pitch)), scale

    def tr(self, p):
        x, y, z = p
        xr = x * self.cy - z * self.sy_; zr = x * self.sy_ + z * self.cy
        yr = y * self.cp + zr * self.sp_; dr = zr * self.cp - y * self.sp_
        return (-xr * self.s, -yr * self.s, dr)

    def facing(self, n):
        x, y, z = n; zr = x * self.sy_ + z * self.cy
        return zr * self.cp - y * self.sp_ < -1e-6

    def light(self, n):
        L = (0.45, 0.8, -0.4); m = math.sqrt(sum(v * v for v in n)) or 1
        return 0.66 + 0.34 * max(0, (n[0] * L[0] + n[1] * L[1] + n[2] * L[2]) / m)


def render(sp, tex, cam, pose=None, pad=4, flat=False):
    polys = []
    for c in sp.cubes:
        for q, n, col, g in cube_quads(sp, c, tex, pose):
            if not cam.facing(n): continue
            pts = [cam.tr(p) for p in q]
            k = 1 if (flat or g) else cam.light(n)
            polys.append((sum(p[2] for p in pts) / 4, [(p[0], p[1]) for p in pts], shade(col, k) if not g else col))
    xs = [p[0] for _, ps, _ in polys for p in ps]; ys = [p[1] for _, ps, _ in polys for p in ps]
    mx, my = min(xs), min(ys)
    W, H = int(max(xs) - mx) + 2 * pad + 1, int(max(ys) - my) + 2 * pad + 1
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for _, ps, col in sorted(polys, key=lambda t: -t[0]):
        pp = [(x - mx + pad, y - my + pad) for x, y in ps]
        d.polygon(pp, fill=col, outline=col)
    proj = lambda p: (cam.tr(p)[0] - mx + pad, cam.tr(p)[1] - my + pad)
    return im, proj


# ------------------------------------------------------------- sheet helpers
def wrap(d, text, font, width):
    lines = []
    for para in text.split('\n'):
        cur = ''
        for wd in para.split(' '):
            t = (cur + ' ' + wd).strip()
            if d.textlength(t, font=font) <= width: cur = t
            else: lines.append(cur); cur = wd
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, width, fill=INK, gap=4):
    for ln in wrap(d, text, font, width):
        d.text((x, y), ln, font=font, fill=fill); y += font.size + gap
    return y


def panel(d, box, title, note=None):
    d.rectangle(box, fill=PANEL, outline=LINE)
    d.text((box[0] + 16, box[1] + 14), title, font=FB(15), fill=INK)
    if note: d.text((box[2] - 16 - d.textlength(note, font=FR(11)), box[1] + 17), note, font=FR(11), fill=SUB)
