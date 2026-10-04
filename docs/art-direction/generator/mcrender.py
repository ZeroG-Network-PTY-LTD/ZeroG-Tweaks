"""Minimal software renderer for Minecraft Java block models (elements, per-face uv, face rotation, element rotation)."""
import json, math
from PIL import Image, ImageDraw


class Cam:
    def __init__(s, yaw=-35, pitch=28, scale=12):
        s.cy, s.sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
        s.cp, s.sp, s.k = math.cos(math.radians(pitch)), math.sin(math.radians(pitch)), scale

    def tr(s, p):
        x, y, z = p; xr = x * s.cy - z * s.sy; zr = x * s.sy + z * s.cy
        return (xr * s.k, -(y * s.cp + zr * s.sp) * s.k, zr * s.cp - y * s.sp)


def _auto_uv(f, a, b):
    x0, y0, z0 = a; x1, y1, z1 = b
    return {'north': [16 - x1, 16 - y1, 16 - x0, 16 - y0], 'south': [x0, 16 - y1, x1, 16 - y0], 'west': [z0, 16 - y1, z1, 16 - y0],
            'east': [16 - z1, 16 - y1, 16 - z0, 16 - y0], 'up': [x0, z0, x1, z1], 'down': [x0, 16 - z1, x1, 16 - z0]}[f]


def _rot(p, r):
    if not r: return p
    o = r.get('origin', [8, 8, 8]); a = math.radians(r['angle']); ax = r['axis']
    x, y, z = p[0] - o[0], p[1] - o[1], p[2] - o[2]
    c, s = math.cos(a), math.sin(a)
    if ax == 'x': y, z = y * c - z * s, y * s + z * c
    elif ax == 'y': x, z = x * c + z * s, -x * s + z * c
    else: x, y = x * c - y * s, x * s + y * c
    return (x + o[0], y + o[1], z + o[2])


NORM = {'north': (0, 0, -1), 'south': (0, 0, 1), 'west': (-1, 0, 0), 'east': (1, 0, 0), 'up': (0, 1, 0), 'down': (0, -1, 0)}
LIGHT = {'up': 1.0, 'north': .82, 'south': .82, 'east': .66, 'west': .66, 'down': .5}


def render(model, textures, cam, bg=(235, 233, 243), emissive=(), glow_full=True, extra_rot=0):
    """model: dict with 'elements'; textures: name -> PIL RGBA image (name without '#')."""
    polys = []
    for e in model['elements']:
        a, b = e['from'], e['to']; r = e.get('rotation')
        x0, y0, z0 = a; x1, y1, z1 = b
        for f, fd in e.get('faces', {}).items():
            tname = fd['texture'].lstrip('#'); img = textures.get(tname)
            if img is None: continue
            uv = fd.get('uv') or _auto_uv(f, a, b); fr = fd.get('rotation', 0)
            W, H = img.size
            if f == 'north': pt = lambda s, t: (x1 - s * (x1 - x0), y1 - t * (y1 - y0), z0); na, nb = x1 - x0, y1 - y0
            elif f == 'south': pt = lambda s, t: (x0 + s * (x1 - x0), y1 - t * (y1 - y0), z1); na, nb = x1 - x0, y1 - y0
            elif f == 'west': pt = lambda s, t: (x0, y1 - t * (y1 - y0), z0 + s * (z1 - z0)); na, nb = z1 - z0, y1 - y0
            elif f == 'east': pt = lambda s, t: (x1, y1 - t * (y1 - y0), z1 - s * (z1 - z0)); na, nb = z1 - z0, y1 - y0
            elif f == 'up': pt = lambda s, t: (x0 + s * (x1 - x0), y1, z0 + t * (z1 - z0)); na, nb = x1 - x0, z1 - z0
            else: pt = lambda s, t: (x0 + s * (x1 - x0), y0, z1 - t * (z1 - z0)); na, nb = x1 - x0, z1 - z0
            n = NORM[f]; n2 = _rot((8 + n[0], 8 + n[1], 8 + n[2]), r); o2 = _rot((8, 8, 8), r)
            nv = (n2[0] - o2[0], n2[1] - o2[1], n2[2] - o2[2])
            if extra_rot:
                nv = _rot((8 + nv[0], 8 + nv[1], 8 + nv[2]), {'axis': 'y', 'angle': extra_rot}); nv = (nv[0] - 8, nv[1] - 8, nv[2] - 8)
            nz = nv[0] * cam.sy + nv[2] * cam.cy
            if nz * cam.cp - nv[1] * cam.sp >= 0: continue
            # texel resolution of the uv region
            su = abs(uv[2] - uv[0]) / 16 * W; sv = abs(uv[3] - uv[1]) / 16 * H
            if fr in (90, 270): su, sv = sv, su
            NA = max(1, int(round(max(na, su)))); NB = max(1, int(round(max(nb, sv))))
            NA = min(NA, 64); NB = min(NB, 64)
            light = max(.45, min(1, .66 + .34 * (nv[1] * .8 + nv[0] * .45 - nv[2] * .4)))
            for i in range(NA):
                for j in range(NB):
                    s, t = (i + .5) / NA, (j + .5) / NB
                    if fr == 90: s2, t2 = t, 1 - s
                    elif fr == 180: s2, t2 = 1 - s, 1 - t
                    elif fr == 270: s2, t2 = 1 - t, s
                    else: s2, t2 = s, t
                    u = uv[0] + (uv[2] - uv[0]) * s2; v = uv[1] + (uv[3] - uv[1]) * t2
                    px = img.getpixel((min(W - 1, max(0, int(u / 16 * W))), min(H - 1, max(0, int(v / 16 * H)))))
                    if px[3] < 8: continue
                    k = 1 if (tname in emissive and glow_full) else light
                    q = []
                    for (ss, tt) in ((i / NA, j / NB), ((i + 1) / NA, j / NB), ((i + 1) / NA, (j + 1) / NB), (i / NA, (j + 1) / NB)):
                        p = _rot(pt(ss, tt), r)
                        if extra_rot: p = _rot(p, {'axis': 'y', 'angle': extra_rot})
                        q.append(cam.tr(p))
                    c = tuple(max(0, min(255, int(px[c_] * k))) for c_ in range(3)) + (px[3],)
                    polys.append((sum(p[2] for p in q) / 4 + (-.01 if tname in emissive else 0), [(p[0], p[1]) for p in q], c))
    xs = [p[0] for _, ps, _ in polys for p in ps]; ys = [p[1] for _, ps, _ in polys for p in ps]
    mx, my = min(xs) - 4, min(ys) - 4; size = (int(max(xs) - mx) + 5, int(max(ys) - my) + 5)
    im = Image.new('RGB', size, bg); d = ImageDraw.Draw(im, 'RGBA'); mask = Image.new('L', size, 0); dm = ImageDraw.Draw(mask)
    for _, ps, c in sorted(polys, key=lambda t: -t[0]):
        pp = [(x - mx, y - my) for x, y in ps]; d.polygon(pp, fill=c); dm.polygon(pp, fill=255)
    out = im.convert('RGBA'); out.putalpha(mask); return out
