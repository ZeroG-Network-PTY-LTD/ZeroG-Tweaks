"""Top view + south elevation of a structure template, coloured by each block's average texture colour."""
import sys, os, nbtlib
from PIL import Image, ImageDraw
TEX = "C:/zt-tmp/w/src/main/resources/assets/zerog_tweaks/textures/block/"
FALLBACK = {"minecraft:rail": (120, 100, 80)}
cache = {}
def colour(name):
    if name in cache: return cache[name]
    short = name.split(":")[1]
    for cand in (short, short + "_top", short + "_idle", short.replace("_bricks", "_brick"), short + "_side"):
        p = TEX + cand + ".png"
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA").resize((1, 1), Image.LANCZOS); c = im.getpixel((0, 0))[:3]; break
    else:
        c = FALLBACK.get(name, (150, 150, 150))
    cache[name] = c; return c
n = nbtlib.load(sys.argv[1]); pal = [str(p["Name"]) for p in n["palette"]]
sx, sy, sz = (int(v) for v in n["size"])
cells = {}
for b in n["blocks"]:
    nm = pal[int(b["state"])]
    if nm != "minecraft:air": cells[tuple(int(v) for v in b["pos"])] = nm
S = 10
top = Image.new("RGB", (sx * S, sz * S), (22, 26, 34)); d = ImageDraw.Draw(top)
for x in range(sx):
    for z in range(sz):
        ys = [y for y in range(sy) if (x, y, z) in cells]
        if ys:
            y = max(ys); c = colour(cells[(x, y, z)]); k = 0.55 + 0.45 * y / sy
            d.rectangle([x * S, z * S, x * S + S - 1, z * S + S - 1], fill=tuple(int(v * k) for v in c))
front = Image.new("RGB", (sx * S, sy * S), (22, 26, 34)); d = ImageDraw.Draw(front)
for x in range(sx):
    for y in range(sy):
        zs = [z for z in range(sz) if (x, y, z) in cells]
        if zs:
            z = max(zs); c = colour(cells[(x, y, z)]); k = 0.5 + 0.5 * z / sz
            d.rectangle([x * S, (sy - 1 - y) * S, x * S + S - 1, (sy - y) * S - 1], fill=tuple(int(v * k) for v in c))
out = Image.new("RGB", (sx * S * 2 + 30, max(sz, sy) * S + 50), (14, 16, 22)); dd = ImageDraw.Draw(out)
out.paste(top, (10, 40)); out.paste(front, (sx * S + 20, 40))
dd.text((10, 12), "Top view (north up)", fill=(220, 230, 240)); dd.text((sx * S + 20, 12), "South elevation (entrance)", fill=(220, 230, 240))
out.save(sys.argv[2]); print("wrote", sys.argv[2])
