"""Tiny software renderer for Minecraft-style box models: textured GeckoLib/Bedrock cubes (box UV)
and extruded item sprites, drawn as shaded texel quads in a 3/4 orthographic view."""
import json, math
from PIL import Image, ImageDraw

class Scene:
    def __init__(self, yaw=-32, pitch=18, light=(-0.55, 0.75, -0.6)):
        self.quads = []  # (depth, [pts3d], color, normal, emissive)
        self.yaw, self.pitch = math.radians(yaw), math.radians(pitch)
        l = math.sqrt(sum(c * c for c in light)); self.L = tuple(c / l for c in light)

    def rot(self, p):
        x, y, z = p
        cy, sy = math.cos(self.yaw), math.sin(self.yaw)
        x, z = x * cy + z * sy, -x * sy + z * cy
        cp, sp = math.cos(self.pitch), math.sin(self.pitch)
        y, z = y * cp - z * sp, y * sp + z * cp
        return x, y, z

    def quad(self, pts, col, normal, emissive=False):
        if col[3] < 16: return
        n = self.rot(normal)
        if n[2] >= -1e-6: return                         # back-facing (camera looks along +z)
        r = [self.rot(p) for p in pts]
        depth = sum(p[2] for p in r) / 4
        shade = 1.0 if emissive else 0.66 + 0.46 * max(0.0, sum(a * b for a, b in zip(normal, self.L)))
        c = tuple(min(255, int(ch * shade)) for ch in col[:3])
        self.quads.append((depth, r, c))

    def face(self, P, U, V, cols, rows, sample, normal, emissive=None):
        """P origin corner, U/V vectors per texel; sample(i,j) -> rgba"""
        for j in range(rows):
            for i in range(cols):
                c = sample(i, j)
                if c is None or c[3] < 16: continue
                p0 = tuple(P[k] + U[k] * i + V[k] * j for k in range(3))
                pts = [p0, tuple(p0[k] + U[k] for k in range(3)), tuple(p0[k] + U[k] + V[k] for k in range(3)), tuple(p0[k] + V[k] for k in range(3))]
                self.quad(pts, c, normal, emissive(i, j) if emissive else False)

    def box_uv(self, origin, size, uv, tex, inflate=0.0, mirror=False, glow=None, offset=(0, 0, 0)):
        """Bedrock box-UV cube. tex/glow: PIL images."""
        (x0, y0, z0), (w, h, d) = origin, size
        x0 += offset[0]; y0 += offset[1]; z0 += offset[2]
        x0, y0, z0 = x0 - inflate, y0 - inflate, z0 - inflate
        W, H, D = w + 2 * inflate, h + 2 * inflate, d + 2 * inflate
        x1, y1, z1 = x0 + W, y0 + H, z0 + D
        tw, th, td = max(1, math.ceil(w)), max(1, math.ceil(h)), max(1, math.ceil(d))
        u, v = uv; T = tex.load(); G = glow.load() if glow else None
        def samp(tu, tv, flip):
            def f(i, j):
                ii = (tw if flip in ('w',) else td if flip == 'd' else tw) - 1 - i if mirror else i
                x, y = tu + ii, tv + j
                if 0 <= x < tex.width and 0 <= y < tex.height: return T[x, y]
                return None
            return f
        def emis(tu, tv):
            if not G: return None
            return lambda i, j: (0 <= tu + i < glow.width and 0 <= tv + j < glow.height and G[tu + i, tv + j][3] > 40)
        # faces: (texture rect origin, texel cols, rows, P, U, V, normal)
        F = [
            ((u + td, v + td), tw, th, (x1, y1, z0), (-W / tw, 0, 0), (0, -H / th, 0), (0, 0, -1), 'w'),       # north / front
            ((u + 2 * td + tw, v + td), tw, th, (x0, y1, z1), (W / tw, 0, 0), (0, -H / th, 0), (0, 0, 1), 'w'),  # south / back
            ((u, v + td), td, th, (x1, y1, z1), (0, 0, -D / td), (0, -H / th, 0), (1, 0, 0), 'd'),               # +x side
            ((u + td + tw, v + td), td, th, (x0, y1, z0), (0, 0, D / td), (0, -H / th, 0), (-1, 0, 0), 'd'),      # -x side
            ((u + td, v), tw, td, (x1, y1, z1), (-W / tw, 0, 0), (0, 0, -D / td), (0, 1, 0), 'w'),              # top
        ]
        for (tu, tv), cols, rows, P, U, V, N, fl in F:
            if mirror:
                P = tuple(P[k] + U[k] * cols for k in range(3)); U = tuple(-c for c in U)
                self.face(P, U, V, cols, rows, lambda i, j, tu=tu, tv=tv: T[tu + cols - 1 - i, tv + j] if tu + cols - 1 - i < tex.width and tv + j < tex.height else None,
                          N, (lambda i, j, tu=tu, tv=tv: G[tu + cols - 1 - i, tv + j][3] > 40) if G else None)
            else:
                self.face(P, U, V, cols, rows, lambda i, j, tu=tu, tv=tv: T[tu + i, tv + j] if tu + i < tex.width and tv + j < tex.height else None,
                          N, (lambda i, j, tu=tu, tv=tv: G[tu + i, tv + j][3] > 40) if G else None)

    def solid(self, origin, size, color, noise=0.0, seed=0):
        """untextured box (e.g. armor stand wood); per-unit noise for a plank look"""
        import random
        r = random.Random(seed)
        (x0, y0, z0), (w, h, d) = origin, size
        def c():
            k = 1 + (r.random() - .5) * noise
            return tuple(min(255, int(ch * k)) for ch in color) + (255,)
        cols = {}
        def sample(key):
            return lambda i, j: cols.setdefault((key, i, j), c())
        x1, y1, z1 = x0 + w, y0 + h, z0 + d
        W, H, D = max(1, round(w)), max(1, round(h)), max(1, round(d))
        self.face((x1, y1, z0), (-w / W, 0, 0), (0, -h / H, 0), W, H, sample('n'), (0, 0, -1))
        self.face((x0, y1, z1), (w / W, 0, 0), (0, -h / H, 0), W, H, sample('s'), (0, 0, 1))
        self.face((x1, y1, z1), (0, 0, -d / D), (0, -h / H, 0), D, H, sample('e'), (1, 0, 0))
        self.face((x0, y1, z0), (0, 0, d / D), (0, -h / H, 0), D, H, sample('w'), (-1, 0, 0))
        self.face((x1, y1, z1), (-w / W, 0, 0), (0, 0, -d / D), W, D, sample('t'), (0, 1, 0))

    def extrude(self, sprite, center, scale, thick, rotz=0.0, lift=0, thickness_fn=None):
        """16x16 item sprite -> voxels in the XY plane (z = depth). rotz rotates in plane (degrees)."""
        px = sprite.load(); n = sprite.width
        a = math.radians(rotz); ca, sa = math.cos(a), math.sin(a)
        def tr(x, y, z):
            x, y = x - n / 2, n / 2 - y
            x, y = x * ca - y * sa, x * sa + y * ca
            return (center[0] + x * scale, center[1] + y * scale, center[2] + z * scale)
        for y in range(n):
            for x in range(n):
                c = px[x, y]
                if c[3] < 40: continue
                t = thickness_fn(x, y, c) if thickness_fn else thick
                z0, z1 = -t / 2, t / 2
                corners = lambda X, Y, Z: tr(X, Y, Z)
                # front (-z), back (+z)
                self.quad([tr(x, y, z0), tr(x + 1, y, z0), tr(x + 1, y + 1, z0), tr(x, y + 1, z0)], c, (0, 0, -1))
                self.quad([tr(x + 1, y, z1), tr(x, y, z1), tr(x, y + 1, z1), tr(x + 1, y + 1, z1)], c, (0, 0, 1))
                # edges only where the neighbour is empty or thinner
                def empty(xx, yy):
                    return not (0 <= xx < n and 0 <= yy < n) or px[xx, yy][3] < 40
                dk = tuple(int(ch * .78) for ch in c[:3]) + (255,)
                nx = (ca, sa, 0); ny = (-sa, ca, 0)
                if empty(x, y - 1): self.quad([tr(x, y, z0), tr(x, y, z1), tr(x + 1, y, z1), tr(x + 1, y, z0)], dk, ny)
                if empty(x, y + 1): self.quad([tr(x + 1, y + 1, z0), tr(x + 1, y + 1, z1), tr(x, y + 1, z1), tr(x, y + 1, z0)], dk, tuple(-q for q in ny))
                if empty(x - 1, y): self.quad([tr(x, y + 1, z0), tr(x, y + 1, z1), tr(x, y, z1), tr(x, y, z0)], dk, tuple(-q for q in nx))
                if empty(x + 1, y): self.quad([tr(x + 1, y, z0), tr(x + 1, y, z1), tr(x + 1, y + 1, z1), tr(x + 1, y + 1, z0)], dk, nx)

    def render(self, scale, pad=10, bg=(0, 0, 0, 0)):
        if not self.quads: return Image.new('RGBA', (1, 1), bg)
        xs = [p[0] for q in self.quads for p in q[1]]; ys = [p[1] for q in self.quads for p in q[1]]
        X0, X1, Y0, Y1 = min(xs), max(xs), min(ys), max(ys)
        W, H = int((X1 - X0) * scale) + 2 * pad, int((Y1 - Y0) * scale) + 2 * pad
        im = Image.new('RGBA', (W, H), bg); d = ImageDraw.Draw(im)
        for depth, pts, c in sorted(self.quads, key=lambda q: -q[0]):
            poly = [((p[0] - X0) * scale + pad, (Y1 - p[1]) * scale + pad) for p in pts]
            d.polygon(poly, fill=c + (255,), outline=c + (255,))
        return im
