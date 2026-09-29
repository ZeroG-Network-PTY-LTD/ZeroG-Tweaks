"""Vanilla-counterpart plant textures (cave vines / kelp / glow lichen / dead bush style)."""
import random, os
from PIL import Image

OUT = '/home/claude/zerog-tweaks/src/main/resources/assets/zerog_tweaks/textures'
H = lambda s: tuple(int(s[i:i+2], 16) for i in (1, 3, 5)) + (255,)

def img(): return Image.new('RGBA', (16, 16), (0, 0, 0, 0))

def put(im, x, y, c):
    if 0 <= x < 16 and 0 <= y < 16: im.putpixel((x, y), c)

# ---------------------------------------------------------------- vines
def vine(seed, stalk, leaf, berry=None, head=False):
    """cave_vines-style: two wandering strands with alternating leaves.
    body tiles vertically (x at y=0 == x at y=16); head stops early and curls."""
    r = random.Random(seed)
    im = img()
    s_dark, s_mid, s_hi = stalk
    l_dark, l_mid, l_hi = leaf
    for sx in (4, 11):
        path, x = [], sx
        for y in range(16):
            path.append(x)
            if y < 15 and r.random() < .35: x += r.choice((-1, 1))
            x = max(sx - 2, min(sx + 2, x))
        # force seamless wrap for the body
        if not head:
            for y in range(12, 16):
                path[y] = path[y] + (sx - path[y]) * (y - 11) // 4
        end = 16 if not head else r.randint(10, 12)
        for y in range(end):
            x = path[y]
            put(im, x, y, s_mid if y % 4 else s_hi)
            if y % 5 == 2: put(im, x + 1, y, s_dark)
        # leaves alternate sides every 3-4 px
        side = r.choice((-1, 1))
        for y in range(1, end - 1, 3):
            x = path[y] + side
            put(im, x, y, l_mid); put(im, x + side, y - 1, l_hi); put(im, x, y + 1, l_dark)
            side = -side
        if head:  # curled tip like cave_vines.png
            x, y = path[end - 1], end
            put(im, x, y, s_mid); put(im, x - 1, y + 1, s_mid); put(im, x - 1, y + 2, s_hi)
        if berry:
            b_dark, b_mid, b_hi = berry
            y0 = r.randint(3, 6) if sx == 4 else r.randint(8, 11)
            bx = path[y0] + (1 if sx == 4 else -1)
            for dx, dy, c in ((-1,0,b_dark),(0,0,b_hi),(1,0,b_mid),(-1,1,b_mid),(0,1,b_mid),(1,1,b_dark),(-1,2,b_dark),(0,2,b_dark),(1,2,b_dark)):
                put(im, bx + dx, y0 + dy, c)
            put(im, bx, y0 - 1, s_dark)
    return im

# ---------------------------------------------------------------- kelp
def kelp(seed, stalk, leaf, glow, head=False):
    r = random.Random(seed)
    im = img()
    sd, sm, sh = stalk; ld, lm, lh = leaf
    x = 7
    top = 3 if head else 0
    xs = []
    for y in range(16):
        xs.append(x)
        if y % 4 == 3: x += 1 if (y // 4) % 2 == 0 else -1
    for y in range(top, 16):
        put(im, xs[y], y, sm); put(im, xs[y] + 1, y, sd)
    # broad wavy leaf blades, alternating, like kelp_plant
    for i, y in enumerate(range(top + 1, 16, 4)):
        side = 1 if i % 2 == 0 else -1
        bx = xs[y] + (2 if side > 0 else -1)
        for k in range(4):
            put(im, bx + side * k, y - k // 2, lm)
            put(im, bx + side * k, y - k // 2 + 1, ld)
        put(im, bx + side * 3, y - 2, lh)
        put(im, bx, y, glow)  # bioluminescent node
    if head:  # air-bladder bulb at the tip like kelp.png
        cx = xs[top]
        for dx, dy in ((0, -1), (1, -1), (0, -2), (1, -2)): put(im, cx + dx, top + dy, glow)
        put(im, cx, top - 3, lh)
    return im

# ---------------------------------------------------------------- lichen
def lichen(seed, cols, glow=None):
    """glow_lichen-style: patchy growth over the whole face with gaps."""
    r = random.Random(seed)
    im = img()
    d, m, h = cols
    cells = set()
    for _ in range(13):
        cx, cy = r.randint(1, 14), r.randint(1, 14)
        for _ in range(r.randint(14, 24)):
            cells.add((cx, cy))
            cx = max(0, min(15, cx + r.choice((-1, 0, 1))))
            cy = max(0, min(15, cy + r.choice((-1, 0, 1))))
    for (x, y) in cells:
        n = sum((x + dx, y + dy) in cells for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)))
        put(im, x, y, h if n >= 4 else m if n >= 2 else d)
    if glow:
        for (x, y) in r.sample(sorted(cells), 6): put(im, x, y, glow)
    return im

# ---------------------------------------------------------------- thorn bush
def thorn(seed, stem, tip):
    """dead_bush-style branching twigs with glowing ember thorn tips."""
    r = random.Random(seed)
    im = img()
    sd, sm = stem
    def branch(x, y, dx, n):
        for i in range(n):
            put(im, x, y, sm if i % 2 else sd)
            if r.random() < .3: put(im, x + (1 if dx > 0 else -1), y, sd)
            y -= 1
            if r.random() < .55: x += dx
            if i > 1 and r.random() < .3: branch(x, y, -dx, max(2, n - i - 2))
        put(im, x, y, tip)
    for dx, n in ((-1, 10), (1, 11), (0, 9)):
        branch(7 + (dx > 0), 15, dx if dx else r.choice((-1, 1)), n)
    return im

def save(im, rel):
    p = os.path.join(OUT, rel); im.save(p); print('wrote', rel)

if __name__ == '__main__':
    PY_STALK = (H('#5a1e0a'), H('#8a3412'), H('#c4600e'))
    PY_LEAF = (H('#a8400c'), H('#e0701a'), H('#ff9a30'))
    PY_BERRY = (H('#d05a10'), H('#ffb040'), H('#fff0a0'))
    save(vine(11, PY_STALK, PY_LEAF, head=True), 'block/pyrevine.png')
    save(vine(11, PY_STALK, PY_LEAF, PY_BERRY, head=True), 'block/pyrevine_lit.png')
    save(vine(23, PY_STALK, PY_LEAF), 'block/pyrevine_plant.png')
    save(vine(23, PY_STALK, PY_LEAF, PY_BERRY), 'block/pyrevine_plant_lit.png')

    GK_STALK = (H('#0c3a3a'), H('#12585a'), H('#1e8a86'))
    GK_LEAF = (H('#0f4c4a'), H('#1a7470'), H('#3cb8a8'))
    GK_GLOW = H('#8ffff0')
    save(kelp(5, GK_STALK, GK_LEAF, GK_GLOW, head=True), 'block/glowkelp.png')
    save(kelp(5, GK_STALK, GK_LEAF, GK_GLOW), 'block/glowkelp_plant.png')
    save(kelp(5, GK_STALK, GK_LEAF, GK_GLOW, head=True), 'item/glowkelp.png')

    save(lichen(7, (H('#6a7a6e'), H('#8a9a8a'), H('#a8b8a8')), H('#e8f4ff')), 'block/lunar_lichen.png')
    save(lichen(9, (H('#6a2a14'), H('#8a3a1e'), H('#b85a30'))), 'block/rust_lichen.png')

    save(thorn(3, (H('#4a2a18'), H('#6a3a20')), H('#ff8a2a')), 'block/emberthorn.png')
