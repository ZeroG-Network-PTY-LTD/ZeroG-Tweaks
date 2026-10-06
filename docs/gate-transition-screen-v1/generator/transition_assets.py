"""Gate transition screen ("zoom from galaxy to planet") - native pixel-art assets.

Follows Design/docs/art-direction-lock.md: hue-shifted 6-tone ramps, shading by ramp steps
(light from the top-left front), clustered bands with no dithering, dark-hue outlines (never
pure black), emissive "C" accents that are never shaded, gray ramps for galaxy-tinted sprites.

Usage: python3 transition_assets.py <out_dir>
Writes <out_dir>/assets/zerog_tweaks/textures/gui/transition/*.png (+ .png.mcmeta for strips).
"""
import sys, os, math, json
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'art'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'art-direction', 'generator'))  # repo layout
from style_kit import RAMPS  # locked ramps

OUT = os.path.join(sys.argv[1] if len(sys.argv) > 1 else '.', 'assets/zerog_tweaks/textures/gui/transition')
os.makedirs(OUT, exist_ok=True)


def hx(h):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


R = {k: [hx(c) for c in v] for k, v in RAMPS.items()}
R.update({k: [hx(c) for c in v] for k, v in {
    # every ramp: dark -> light, shadows lean blue/violet (warm ones lean deep red-brown)
    'ocean':    ['#0a1030', '#12245a', '#1a3f8a', '#2a68b8', '#4f9ad8', '#a8dcf4'],
    'sand':     ['#1e1020', '#4a2a2a', '#7a4f36', '#a8794a', '#cfa66a', '#f0dca0'],
    'cloud':    ['#2a2f5a', '#5a6390', '#8e97bf', '#bcc4e0', '#e2e8f6', '#ffffff'],
    'moon':     ['#1a1a2c', '#34364a', '#555869', '#7d8193', '#aeb2c2', '#e2e4ee'],
    'mars':     ['#1c0a14', '#47161a', '#7e2a1e', '#b04a26', '#d8783e', '#f2b27a'],
    'ochre':    ['#20101a', '#4e2a1c', '#86501e', '#b8802c', '#ddb050', '#f6e09a'],
    'azure':    ['#071a2a', '#0f3550', '#1a5a7a', '#2a87a0', '#52b8c4', '#a6ecf0'],
    'charcoal': ['#0e0b14', '#1f1a22', '#342b30', '#4d3f3e', '#6e5a54', '#9a8274'],
    'marble':   ['#2a2432', '#4f4652', '#7d737a', '#aaa1a2', '#d4ccc8', '#f4efe8'],
    'ember':    ['#3a0c04', '#7a1c06', '#c43c0a', '#f07018', '#ffb040', '#fff0b0'],
    'ice':      ['#0c1428', '#1c3050', '#3a5e80', '#6a98b4', '#a8d0e0', '#eefaff'],
    'permafrost': ['#10142a', '#232c44', '#3c4a62', '#5c6e86', '#8a9cb2', '#c4d2e0'],
    'phantom':  ['#0a2a3a', '#145a6a', '#22a0aa', '#58dcd8', '#a8fff4', '#ffffff'],
    'crimson':  ['#1a0410', '#4a0a1c', '#8a1426', '#c42a2a', '#f05a34', '#ffb070'],
    'plasma':   ['#5a1a00', '#b84400', '#ff8a00', '#ffc840', '#fff0a0', '#ffffff'],
    'void':     ['#08060f', '#141026', '#241a3e', '#3a2a5e', '#5a4488', '#8a74c0'],
}.items()})
OUTLINE = hx('#0b0a1a')  # deep navy-violet space outline, never #000

# --------------------------------------------------------------------------- noise
_rng = np.random.default_rng(7)
_PERM = np.concatenate([_rng.permutation(256)] * 2)
_GRAD = _rng.random(256)


def _vnoise(x, y, z):
    xi, yi, zi = np.floor(x).astype(int), np.floor(y).astype(int), np.floor(z).astype(int)
    xf, yf, zf = x - xi, y - yi, z - zi
    u, v, w = (t * t * (3 - 2 * t) for t in (xf, yf, zf))
    xi, yi, zi = xi & 255, yi & 255, zi & 255

    def h(a, b, c): return _GRAD[_PERM[_PERM[_PERM[a] + b] + c]]
    x00 = h(xi, yi, zi) * (1 - u) + h(xi + 1, yi, zi) * u
    x10 = h(xi, yi + 1, zi) * (1 - u) + h(xi + 1, yi + 1, zi) * u
    x01 = h(xi, yi, zi + 1) * (1 - u) + h(xi + 1, yi, zi + 1) * u
    x11 = h(xi, yi + 1, zi + 1) * (1 - u) + h(xi + 1, yi + 1, zi + 1) * u
    return (x00 * (1 - v) + x10 * v) * (1 - w) + (x01 * (1 - v) + x11 * v) * w


def fbm(p, freq=2.0, oct=4, seed=0):
    x, y, z = p
    tot, amp, norm = 0, 1.0, 0
    for o in range(oct):
        f = freq * (2 ** o)
        tot = tot + amp * _vnoise(x * f + seed * 17.3, y * f + seed * 5.1, z * f + seed * 11.7)
        norm += amp; amp *= .5
    return tot / norm


# --------------------------------------------------------------------------- planets
SIZE, RAD = 128, 58
LIGHT = np.array([-.55, -.62, .56]); LIGHT = LIGHT / np.linalg.norm(LIGHT)  # screen: x right, y down, z to viewer
FRAMES = 16


def sphere_geometry(size=SIZE, rad=RAD):
    c = (size - 1) / 2
    yy, xx = np.mgrid[0:size, 0:size]
    nx, ny = (xx - c) / rad, (yy - c) / rad
    r2 = nx * nx + ny * ny
    inside = r2 <= 1.0
    nz = np.sqrt(np.clip(1 - r2, 0, 1))
    return nx, ny, nz, inside, r2


def light_shift(nx, ny, nz):
    d = nx * LIGHT[0] + ny * LIGHT[1] + nz * LIGHT[2]
    # ramp steps, not brightness: lit side +1/+2, terminator -2, night side -4 (clamped to tone 0/1)
    return np.clip(np.round((d - .38) * 3.4), -3, 1).astype(int), d


def surface_point(nx, ny, nz, rot):
    # world point on the unit sphere, spun about the vertical axis (y up in world)
    wx, wy, wz = nx, -ny, nz
    c, s = math.cos(rot), math.sin(rot)
    return (wx * c + wz * s, wy, -wx * s + wz * c)


def craters(p, n, seed, rmin=.05, rmax=.16):
    """returns (bowl mask, lit-rim mask) for n random craters on the sphere"""
    rng = np.random.default_rng(seed)
    bowl = np.zeros(p[0].shape, bool); rim = np.zeros(p[0].shape, bool)
    for _ in range(n):
        v = rng.normal(size=3); v /= np.linalg.norm(v); r = rng.uniform(rmin, rmax)
        dot = p[0] * v[0] + p[1] * v[1] + p[2] * v[2]
        ang = np.arccos(np.clip(dot, -1, 1))
        bowl |= ang < r * .78
        ring = (ang >= r * .78) & (ang < r)
        # the rim facing away from the bowl toward world "up-left" catches light
        rim |= ring & ((p[1] - v[1]) > -.02)
    return bowl, rim


def render_planet(spec, rot, glow_pulse=0):
    nx, ny, nz, inside, r2 = sphere_geometry()
    shift, d = light_shift(nx, ny, nz)
    p = surface_point(nx, ny, nz, rot)
    ramp_idx = np.zeros(nx.shape, int); ramp_key = np.empty(nx.shape, object)
    glow_key = np.full(nx.shape, None, object); glow_idx = np.zeros(nx.shape, int)
    spec['surface'](p, ramp_key, ramp_idx, glow_key, glow_idx)
    img = np.zeros((SIZE, SIZE, 4), np.uint8)
    lit = np.clip(ramp_idx + shift, 0, 5)
    if spec.get('spec_key'):  # small clustered ocean glint, light-side only
        m = (ramp_key == spec['spec_key']) & (d > .93)
        lit[m] = 5
    for key in set(ramp_key[inside].tolist()):
        m = inside & (ramp_key == key)
        cols = np.array(R[key], np.uint8)
        img[m, :3] = cols[lit[m]]
        img[m, 3] = 255
    gm = inside & (glow_key != None)  # noqa: E711 - emissive C accents ignore light
    for key in set(glow_key[gm].tolist()):
        m = gm & (glow_key == key)
        cols = np.array(R[key], np.uint8)
        img[m, :3] = cols[np.clip(glow_idx[m] + glow_pulse, 0, 5)]
    # atmosphere: 2 px rim, brighter on the lit side, translucent
    if spec.get('atmo'):
        ar = np.sqrt(r2) * RAD
        band = (ar > RAD) & (ar <= RAD + 2.6)
        lit_side = (nx * LIGHT[0] + ny * LIGHT[1]) > -.1
        col = np.array(R[spec['atmo']][4], np.uint8)
        a = np.where(lit_side, 120, 45) * (1 - (ar - RAD) / 2.8)
        mm = band
        img[mm, :3] = col; img[mm, 3] = np.clip(a[mm], 0, 255).astype(np.uint8)
        inner = inside & (np.sqrt(r2) > .955) & lit_side  # inner limb haze
        img[inner, :3] = (img[inner, :3] * .5 + col * .5).astype(np.uint8)
    # dark-hue outline one pixel outside the disc (on the shadow side it merges into space)
    disc = img[..., 3] == 255
    ring = np.zeros_like(disc)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ring |= np.roll(np.roll(disc, dy, 0), dx, 1)
    ring &= ~disc & (img[..., 3] < 120)
    img[ring, :3] = OUTLINE; img[ring, 3] = 255
    return Image.fromarray(img, 'RGBA')


def assign(ramp_key, ramp_idx, mask, key, idx):
    ramp_key[mask] = key; ramp_idx[mask] = idx if np.isscalar(idx) else idx[mask]


def S_earth(p, k, i, gk, gi):
    h = fbm(p, 1.6, 5, 1)
    ocean = h < .52
    assign(k, i, ocean, 'ocean', np.where(h < .42, 2, 3))
    land = ~ocean
    dry = land & (fbm(p, 3.0, 3, 9) > .56)
    assign(k, i, land & ~dry, 'leaf', np.where(h > .62, 4, 3))
    assign(k, i, dry, 'sand', 3)
    cap = np.abs(p[1]) > .86 - .06 * fbm(p, 4, 2, 3)
    assign(k, i, cap, 'cloud', 4)
    cl = fbm((p[0] * 1.3, p[1] * 2.4, p[2] * 1.3), 2.2, 4, 21) > .6
    assign(k, i, cl, 'cloud', 4)


def S_moon(p, k, i, gk, gi):
    h = fbm(p, 2.0, 4, 2)
    assign(k, i, np.ones(h.shape, bool), 'moon', np.where(h < .45, 2, 3))   # dark mare / bright highlands
    bowl, rim = craters(p, 38, 5)
    i[bowl] = np.clip(i[bowl] - 1, 0, 5); i[rim] = np.clip(i[rim] + 1, 0, 5)


def S_mars(p, k, i, gk, gi):
    h = fbm(p, 1.8, 5, 4)
    assign(k, i, np.ones(h.shape, bool), 'mars', np.where(h < .46, 2, 3))
    assign(k, i, h > .63, 'ochre', 3)
    cap = p[1] > .9 - .05 * fbm(p, 5, 2, 8)
    assign(k, i, cap, 'cloud', 4)
    bowl, rim = craters(p, 10, 6, .04, .1)
    i[bowl] = np.clip(i[bowl] - 1, 0, 5)


def S_cerulon(p, k, i, gk, gi):
    h = fbm(p, 1.7, 5, 11)
    sea = h < .5
    assign(k, i, sea, 'cerulite', np.where(h < .4, 2, 3))
    assign(k, i, ~sea, 'azure', np.where(h > .64, 4, 3))
    # C accent: geode fields glow cyan-white through the moss
    g = (~sea) & (fbm(p, 6.0, 2, 13) > .7)
    gk[g] = 'cerulite'; gi[g] = 4


def S_skarn(p, k, i, gk, gi):
    h = fbm(p, 2.1, 5, 14)
    assign(k, i, np.ones(h.shape, bool), 'charcoal', np.where(h < .5, 2, 3))
    assign(k, i, h > .64, 'marble', 3)
    # ember-orange fracture seams (C accent): thin bands where a second noise crosses its midline
    f = fbm(p, 3.4, 4, 15)
    seam = (np.abs(f - .5) < .022) & (h < .62)
    gk[seam] = 'ember'; gi[seam] = 3
    lava = h < .34
    gk[lava] = 'ember'; gi[lava] = 2


def S_eidolon(p, k, i, gk, gi):
    h = fbm(p, 1.9, 5, 17)
    assign(k, i, np.ones(h.shape, bool), 'ice', np.where(h < .48, 3, 4))
    assign(k, i, h < .4, 'permafrost', 3)
    cr = np.abs(fbm(p, 4.0, 3, 18) - .5) < .016
    i[cr] = np.clip(i[cr] - 2, 0, 5)
    ph = fbm(p, 7.0, 2, 19) > .74   # phantom ice glints
    gk[ph] = 'phantom'; gi[ph] = 3


def S_solvane(p, k, i, gk, gi):
    h = fbm(p, 1.8, 5, 23)
    assign(k, i, np.ones(h.shape, bool), 'solvanite', np.where(h < .5, 2, 3))
    assign(k, i, h < .38, 'crimson', 2)
    f = fbm(p, 2.8, 4, 24)
    flow = np.abs(f - .5) < .03
    gk[flow] = 'plasma'; gi[flow] = 3
    hot = h > .7
    gk[hot] = 'plasma'; gi[hot] = 2


def S_nullifite(p, k, i, gk, gi):
    """not a destination - used for the 'unknown / hidden world' placeholder"""
    h = fbm(p, 2.0, 4, 31)
    assign(k, i, np.ones(h.shape, bool), 'void', np.where(h < .5, 2, 3))
    cr = np.abs(fbm(p, 3.0, 4, 32) - .5) < .02
    gk[cr] = 'glow'; gi[cr] = 4


def W(pattern):
    """wasteland bases are drawn in the gray ramp only; the game tints them per galaxy"""
    def f(p, k, i, gk, gi):
        h = fbm(p, 1.9, 5, 40 + len(pattern))
        one = np.ones(h.shape, bool)
        if pattern == 'ocean':
            assign(k, i, one, 'tint_gray', np.where(h < .58, 2, 4))
            i[h < .44] = 1
        elif pattern == 'desert':
            d = np.sin((p[1] * 9 + fbm(p, 3, 2, 41) * 6)) > .3
            assign(k, i, one, 'tint_gray', np.where(d, 3, 2))
            i[h > .66] = 4
        elif pattern == 'volcanic':
            assign(k, i, one, 'tint_gray', np.where(h < .5, 1, 2))
            seam = np.abs(fbm(p, 3.2, 4, 42) - .5) < .024
            gk[seam] = 'ember'; gi[seam] = 3          # lava stays untinted (emissive)
        elif pattern == 'frozen':
            assign(k, i, one, 'tint_gray', np.where(h < .5, 4, 5))
            cr = np.abs(fbm(p, 4, 3, 43) - .5) < .015
            i[cr] = 3
        elif pattern == 'toxic':
            m = fbm(p, 4.5, 3, 44)
            assign(k, i, one, 'tint_gray', np.where(m < .45, 2, np.where(m < .6, 3, 1)))
        elif pattern == 'crystal':
            assign(k, i, one, 'tint_gray', np.where(h < .5, 2, 3))
            c = fbm(p, 8, 2, 45) > .72
            gk[c] = 'glow'; gi[c] = 3                 # crystal sparkle, untinted
        elif pattern == 'barren':
            assign(k, i, one, 'tint_gray', np.where(h < .5, 2, 3))
            bowl, rim = craters(p, 30, 46)
            i[bowl] = np.clip(i[bowl] - 1, 0, 5); i[rim] = np.clip(i[rim] + 1, 0, 5)
    return f


PLANETS = {
    'earth':   dict(surface=S_earth, atmo='ocean', spec_key='ocean'),
    'moon':    dict(surface=S_moon),
    'mars':    dict(surface=S_mars, atmo='mars'),
    'cerulon': dict(surface=S_cerulon, atmo='cerulite', spec_key='cerulite'),
    'skarn':   dict(surface=S_skarn, atmo='ember'),
    'eidolon': dict(surface=S_eidolon, atmo='ice'),
    'solvane': dict(surface=S_solvane, atmo='plasma'),
    'unknown': dict(surface=S_nullifite, atmo='glow'),
}
for w in ('ocean', 'desert', 'volcanic', 'frozen', 'toxic', 'crystal', 'barren'):
    PLANETS['wasteland_' + w] = dict(surface=W(w), atmo='tint_gray' if w in ('ocean', 'toxic', 'frozen') else None)


def strip(frames, name, frametime=2):
    w, h = frames[0].size
    im = Image.new('RGBA', (w, h * len(frames)))
    for n, f in enumerate(frames): im.paste(f, (0, n * h))
    im.save(f'{OUT}/{name}.png')
    with open(f'{OUT}/{name}.png.mcmeta', 'w') as fh:
        json.dump({'animation': {'frametime': frametime, 'interpolate': False}}, fh)
    return im


def build_planets():
    out = {}
    for name, spec in PLANETS.items():
        frames = [render_planet(spec, 2 * math.pi * f / FRAMES) for f in range(FRAMES)]
        strip(frames, 'planet_' + name, 3)
        out[name] = frames
    return out


# --------------------------------------------------------------------------- galaxies
GALAXY = {  # galaxy number -> (arm ramp, core ramp, arms, pitch)
    1: ('moonsteel', 'solvanite', 2, .32),   # Sol: Milky-Way silver with a warm core
    2: ('cerulite', 'ice', 2, .28),          # Cerulon blues
    3: ('ember', 'crimson', 3, .36),         # Skarn ember
    4: ('ice', 'phantom', 2, .26),           # Eidolon pale cyan
    5: ('solvanite', 'plasma', 4, .30),      # Solvane gold
}


def render_galaxy(n, size=192, spin=0.0):
    arm_r, core_r, arms, pitch = GALAXY[n]
    c = (size - 1) / 2
    yy, xx = np.mgrid[0:size, 0:size]
    tilt, ang = .56, math.radians(-18)
    dx, dy = xx - c, yy - c
    rx = dx * math.cos(ang) + dy * math.sin(ang)
    ry = (-dx * math.sin(ang) + dy * math.cos(ang)) / tilt
    r = np.sqrt(rx * rx + ry * ry) / (size * .44)
    th = np.arctan2(ry, rx) + spin
    dens = np.zeros(r.shape)
    for a in range(arms):
        arm_th = np.log(np.maximum(r, .03)) / math.tan(pitch) + a * 2 * math.pi / arms
        dth = np.angle(np.exp(1j * (th - arm_th)))
        dens = np.maximum(dens, np.exp(-(dth * (.9 + 1.6 * r)) ** 2 * 2.2))
    p = (rx / size * 6, ry / size * 6, np.full(r.shape, .3 * n))
    dust = fbm(p, 1.0, 4, 60 + n)
    dens = (dens * np.exp(-r * 1.5) + .22 * np.exp(-r * 2.6)) * (.6 + .7 * dust) * (r < 1.05)
    core = np.exp(-(r / .2) ** 2)
    img = np.zeros((size, size, 4), np.uint8)
    arm_cols, core_cols = np.array(R[arm_r], np.uint8), np.array(R[core_r], np.uint8)
    lev = np.digitize(dens, [.05, .09, .15, .23, .34, .5])  # 0 = empty
    m = lev > 0
    img[m, :3] = arm_cols[np.clip(lev[m] - 1, 0, 5)]
    img[m, 3] = np.array([0, 90, 150, 210, 255, 255, 255])[lev[m]]
    cl = np.digitize(core, [.15, .3, .5, .7, .88])
    m = cl > 0
    img[m, :3] = core_cols[np.clip(cl[m], 0, 5)]
    img[m, 3] = 255
    rng = np.random.default_rng(80 + n)  # clustered stars along the arms
    for _ in range(320):
        x, y = rng.integers(4, size - 4, 2)
        if dens[y, x] > .07:
            img[y, x] = (*arm_cols[5], 255)
            if rng.random() < .15:
                for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)): img[y + oy, x + ox] = (*arm_cols[4], 220)
    return Image.fromarray(img, 'RGBA')


def target_point(n, size=192):
    """where the destination system sits on each galaxy sprite (pixel coords), on an outer arm"""
    return {1: (126, 112), 2: (64, 76), 3: (132, 70), 4: (58, 118), 5: (130, 116)}[n]


# --------------------------------------------------------------------------- starfields
def starfield(seed, density, bright, size=256):
    rng = np.random.default_rng(seed)
    img = np.zeros((size, size, 4), np.uint8)
    pals = [R['moonsteel'], R['cerulite'], R['solvanite'], R['glow']]
    for _ in range(int(size * size * density)):
        x, y = rng.integers(0, size, 2); pal = pals[rng.integers(0, 4)]
        t = rng.integers(2, 6) if bright else rng.integers(1, 4)
        img[y, x] = (*pal[t], 255 if bright else 200)
        if bright and t == 5 and rng.random() < .35:  # plus-shaped bright star, wraps for tiling
            for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                img[(y + oy) % size, (x + ox) % size] = (*pal[3], 200)
    return Image.fromarray(img, 'RGBA')


def nebula(size=256):
    yy, xx = np.mgrid[0:size, 0:size]
    a, b = xx / size * 2 * math.pi, yy / size * 2 * math.pi
    p = (np.cos(a) * 1.0, np.sin(a) * 1.0 + np.cos(b), np.sin(b))  # torus mapping -> seamless tile
    v = fbm(p, .8, 4, 90)
    lev = np.digitize(v, [.6, .68, .76])
    img = np.zeros((size, size, 4), np.uint8)
    cols = np.array(R['void'], np.uint8)
    m = lev > 0
    img[m, :3] = cols[lev[m] + 1]; img[m, 3] = np.array([0, 40, 60, 80])[lev[m]]
    return Image.fromarray(img, 'RGBA')


# --------------------------------------------------------------------------- stars (system view)
STAR = {1: 'solvanite', 2: 'cerulite', 3: 'ember', 4: 'phantom', 5: 'plasma'}


def render_star(n, frame, size=48):
    cols = np.array(R[STAR[n]], np.uint8)
    c = (size - 1) / 2
    yy, xx = np.mgrid[0:size, 0:size]
    dx, dy = xx - c, yy - c
    r = np.sqrt(dx * dx + dy * dy)
    th = np.arctan2(dy, dx)
    img = np.zeros((size, size, 4), np.uint8)
    spike = (np.abs(np.sin(th * 4 + frame * .39)) < .07) & (r < 21 - (frame % 2) * 2)
    glow = r < 15.5 + (frame % 2)
    img[glow, :3] = cols[1]; img[glow, 3] = 110
    img[spike, :3] = cols[3]; img[spike, 3] = 210
    halo = r < 13.2
    img[halo, :3] = cols[3]; img[halo, 3] = 230
    disc = r < 11
    band = np.clip(5 - (r[disc] / 11 * 3).astype(int), 3, 5)   # emissive: white core, saturated rim
    img[disc, :3] = cols[band]; img[disc, 3] = 255
    return Image.fromarray(img, 'RGBA')


# --------------------------------------------------------------------------- UI
UI_DARK, UI_MID = hx('#141326'), hx('#2b2a4a')


def nameplate():
    """32x32 nine-slice (8 px borders): dark panel, moonsteel bevel, a glow accent line on top"""
    m = R['moonsteel']; g = R['glow']
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); px = im.load()
    for y in range(32):
        for x in range(32):
            edge = x in (0, 31) or y in (0, 31)
            corner = (x in (0, 31) and y in (0, 31))
            if corner: continue
            if edge: px[x, y] = (*m[0], 255)
            elif x == 1 or y == 1: px[x, y] = (*m[3], 255)           # lit bevel top-left
            elif x == 30 or y == 30: px[x, y] = (*m[1], 255)          # shadow bevel
            else: px[x, y] = (*UI_DARK, 236)
    for x in range(4, 28): px[x, 2] = (*g[3], 255)                    # C accent line
    for x in (4, 27): px[x, 2] = (*g[1], 255)
    return im


def progress_frame():
    m = R['moonsteel']
    im = Image.new('RGBA', (184, 9), (0, 0, 0, 0)); px = im.load()
    for x in range(184):
        for y in range(9):
            if (x in (0, 183) and y in (0, 8)): continue
            if x in (0, 183) or y in (0, 8): px[x, y] = (*m[0], 255)
            elif y == 1: px[x, y] = (*m[1], 255)
            else: px[x, y] = (*UI_DARK, 255)
    for x in range(6, 184, 12): px[x, 7] = (*m[2], 255)                # tick marks
    return im


def progress_fill():
    """180x5 emissive fill (glow ramp): white top line, saturated body, dark base"""
    g = R['glow']; im = Image.new('RGBA', (180, 5)); px = im.load()
    rows = [5, 4, 3, 3, 2]
    for y in range(5):
        for x in range(180):
            t = rows[y] if (x // 4) % 6 else min(5, rows[y] + 1)          # moving highlight segments
            px[x, y] = (*g[t], 255)
    return im


def reticle(frame):
    g = R['glow']; im = Image.new('RGBA', (24, 24), (0, 0, 0, 0)); px = im.load()
    o = (frame % 4)                                                       # brackets breathe 0..3 px
    L = 6
    for (cx, cy, sx, sy) in ((o, o, 1, 1), (23 - o, o, -1, 1), (o, 23 - o, 1, -1), (23 - o, 23 - o, -1, -1)):
        for k in range(L):
            px[cx + sx * k, cy] = (*g[4 if k < 2 else 3], 255)
            px[cx, cy + sy * k] = (*g[4 if k < 2 else 3], 255)
    px[11, 11] = px[12, 12] = px[11, 12] = px[12, 11] = (*g[5], 255)
    return im


ICONS = {  # 9x9, '.' empty, digits = ramp index, ramp chosen per icon (C accents)
    'gravity': ('moonsteel', ["....4....", "....4....", "....4....", "..4.4.4..", "...444...", "....4....",
                              ".........", "222222222", "111111111"]),
    'heat':    ('ember',     ["....4....", "...45....", "...354...", "..3454...", "..34543..", ".234543..",
                              ".2345432.", "..23332..", "...222..."]),
    'cold':    ('ice',       ["....5....", ".4..5..4.", "..4.5.4..", "...454...", "55554555.", "...454...",
                              "..4.5.4..", ".4..5..4.", "....5...."]),
    'acid':    ('leaf',      ["....4....", "....4....", "...454...", "...454...", "..45554..", "..45554..",
                              "..34443..", "...333...", "........."]),
    'storm':   ('ochre',     ["..44444..", ".4.....4.", "4..333..4", "4.3...3.4", "4.3.4.3.4", "4..3..3.4",
                              ".4..33.4.", "..4...4..", "...444..."]),
    'void':    ('glow',      ["2.......2", ".3.....3.", "..4...4..", "...4.4...", "....5....", "...4.4...",
                              "..3...4..", ".2.....3.", "2.......2"]),
    'safe':    ('leaf',      [".........", "........4", ".......4.", "......4..", "4....4...", ".4..4....",
                              "..44.....", "...4.....", "........."]),
}


def icons():
    im = Image.new('RGBA', (9 * len(ICONS), 9), (0, 0, 0, 0)); px = im.load()
    for n, (name, (ramp, rows)) in enumerate(ICONS.items()):
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch != '.': px[n * 9 + x, y] = (*R[ramp][int(ch)], 255)
    return im


def echo_wisp(frame):
    g = R['glow']; c = R['cerulite']
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); px = im.load()
    cx, cy = 7.5, 7.5 - frame * .5
    for y in range(16):
        for x in range(16):
            d = math.hypot(x - cx, y - cy)
            if d < 2.2: px[x, y] = (*g[5], 255)
            elif d < 3.6: px[x, y] = (*g[4], 255)
            elif d < 5.0: px[x, y] = (*g[2], 200)
            elif d < 6.2 and (x + y + frame) % 3 == 0: px[x, y] = (*c[4], 180)  # orbiting shard flecks
    return im


def main():
    planets = build_planets()
    for n in GALAXY:
        render_galaxy(n).save(f'{OUT}/galaxy_{n}.png')
        strip([render_star(n, f) for f in range(4)], f'star_{n}', 3)
    starfield(1, .010, False).save(f'{OUT}/starfield_far.png')
    starfield(2, .004, True).save(f'{OUT}/starfield_mid.png')
    starfield(3, .0012, True).save(f'{OUT}/starfield_near.png')
    nebula().save(f'{OUT}/nebula.png')
    nameplate().save(f'{OUT}/nameplate.png')
    progress_frame().save(f'{OUT}/progress_frame.png')
    progress_fill().save(f'{OUT}/progress_fill.png')
    strip([reticle(f) for f in range(4)], 'reticle', 3)
    icons().save(f'{OUT}/hazard_icons.png')
    strip([echo_wisp(f) for f in range(2)], 'echo_wisp', 8)
    print('assets ->', OUT, len(os.listdir(OUT)), 'files')
    return planets


if __name__ == '__main__':
    main()
