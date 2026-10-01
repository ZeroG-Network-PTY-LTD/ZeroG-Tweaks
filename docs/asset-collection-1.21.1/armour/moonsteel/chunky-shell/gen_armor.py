"""Moonsteel chunky-shell armour: GeckoLib geo + 128x128 texture + glowmask.

Follows the Moonsteel design sheet: every piece is the vanilla armour box plus
shell cubes on the matching GeckoLib armour bone. Box UV is packed automatically.

usage: python gen_armor.py OUT_DIR
writes OUT_DIR/moonsteel.geo.json, moonsteel.png, moonsteel_glowmask.png
"""
import json, math, random, sys
from pathlib import Path
from PIL import Image

OUT = Path(sys.argv[1])
TEX_W, TEX_H = 128, 128
rng = random.Random(7)

# palette sampled from the existing Moonsteel textures
DARK = (0x5B, 0x64, 0x70)
MID = (0x8A, 0x95, 0xA3)
LIGHT = (0xB8, 0xC3, 0xCF)
SHINE = (0xEE, 0xF4, 0xFA)
FROST = (0xD3, 0xE0, 0xEE)
ACCENT = (0xA8, 0xD8, 0xFF)
ACCENT_DEEP = (0x6F, 0xA3, 0xD0)
VISOR = (0x3E, 0x6A, 0x94)
VISOR_HI = (0x5B, 0x8C, 0xBC)
GEM_CORE = (0xEE, 0xF8, 0xFF)

# (bone, role, origin, size, inflate)
ARMOR = {
    "armorHead": dict(parent="bipedHead", pivot=[0, 24, 0], cubes=[
        ("helm", [-4, 24, -4], [8, 8, 8], 1.0),
        ("ridge", [-1, 33, -4], [2, 1, 8], 0.0),
        ("crest", [-1, 34, -2], [2, 2, 5], 0.0),
        ("brow", [-5.5, 30, -6], [11, 1, 1], 0.0),
    ]),
    "armorBody": dict(parent="bipedBody", pivot=[0, 24, 0], cubes=[
        ("plate", [-4, 12, -2], [8, 12, 4], 1.01),
        ("breast", [-3, 16, -4], [6, 7, 1], 0.0),
        ("gem", [-1.5, 18, -5], [3, 3, 1], 0.0),
        ("backplate", [-3, 15, 3], [6, 7, 1], 0.0),
        ("fauld", [-5.5, 11.7, -3.3], [11, 2, 7], 0.0),
    ]),
    "armorRightArm": dict(parent="bipedRightArm", pivot=[-5, 22, 0], cubes=[
        ("plate", [-8, 12, -2], [4, 12, 4], 1.0),
        ("pauldron", [-10.2, 20, -4], [7, 3, 8], 0.0),
        ("pauldron_top", [-9.5, 23, -3.5], [6, 3, 7], 0.0),
        ("cuff", [-9.5, 11.5, -3.5], [7, 2, 7], 0.0),
    ]),
    "armorLeftArm": dict(parent="bipedLeftArm", pivot=[5, 22, 0], cubes=[
        ("plate", [4, 12, -2], [4, 12, 4], 1.0),
        ("pauldron", [3.2, 20, -4], [7, 3, 8], 0.0),
        ("pauldron_top", [3.5, 23, -3.5], [6, 3, 7], 0.0),
        ("cuff", [2.5, 11.5, -3.5], [7, 2, 7], 0.0),
    ]),
    "armorRightLeg": dict(parent="bipedRightLeg", pivot=[-1.9, 12, 0], cubes=[
        ("leg", [-3.9, 0, -2], [4, 12, 4], 0.5),
        ("belt", [-4.5, 10, -3], [5, 2, 6], 0.0),
        ("knee", [-3.4, 8.2, -3.2], [3, 2, 1], 0.0),
    ]),
    "armorLeftLeg": dict(parent="bipedLeftLeg", pivot=[1.9, 12, 0], cubes=[
        ("leg", [-0.1, 0, -2], [4, 12, 4], 0.5),
        ("belt", [-0.5, 9.9, -3.5], [5, 2, 7], 0.0),
        ("knee", [0.4, 8.2, -3.2], [3, 2, 1], 0.0),
    ]),
    "armorRightBoot": dict(parent="bipedRightLeg", pivot=[-1.9, 12, 0], cubes=[
        ("boot", [-3.9, 0, -2], [4, 6, 4], 1.0),
        ("flare", [-5.4, 5, -3.5], [7, 3, 7], 0.0),
    ]),
    "armorLeftBoot": dict(parent="bipedLeftLeg", pivot=[1.9, 12, 0], cubes=[
        ("boot", [-0.1, 0, -2], [4, 6, 4], 1.0),
        ("flare", [-1.6, 4.9, -3.6], [7, 3, 7], 0.0),
    ]),
}
BIPEDS = {"bipedHead": [0, 24, 0], "bipedBody": [0, 24, 0], "bipedRightArm": [-5, 22, 0],
          "bipedLeftArm": [5, 22, 0], "bipedRightLeg": [-1.9, 12, 0], "bipedLeftLeg": [1.9, 12, 0]}

tex = Image.new("RGBA", (TEX_W, TEX_H), (0, 0, 0, 0))
glow = Image.new("RGBA", (TEX_W, TEX_H), (0, 0, 0, 0))


class Shelf:
    """Simple shelf packer for box-UV nets."""
    def __init__(self):
        self.x = self.y = self.row_h = 0

    def place(self, w, h):
        if self.x + w > TEX_W:
            self.x, self.y, self.row_h = 0, self.y + self.row_h, 0
        if self.y + h > TEX_H:
            raise SystemExit("texture atlas full")
        pos = (self.x, self.y)
        self.x += w
        self.row_h = max(self.row_h, h)
        return pos


def faces(u, v, w, h, d):
    """Box-UV face rectangles (x, y, width, height) keyed by direction."""
    return {
        "up": (u + d, v, w, d), "down": (u + d + w, v, w, d),
        "east": (u, v + d, d, h), "north": (u + d, v + d, w, h),
        "west": (u + d + w, v + d, d, h), "south": (u + 2 * d + w, v + d, w, h),
    }


def px(img, x, y, c, a=255):
    img.putpixel((x, y), (*c, a))


def metal(rect, base=MID, rim=DARK, top_light=True, speckle=0.18):
    """Frosty plate: 2x2 blotches like the design sheet, dark only on the bottom edge."""
    x0, y0, w, h = rect
    bright = base in (LIGHT, FROST)
    weights = [(FROST, 3), (LIGHT, 4), (MID, 3)] if bright else [(LIGHT, 4), (MID, 4), (FROST, 1), (DARK, 1)]
    cells = {}
    for y in range(h):
        for x in range(w):
            key = (x // 2, y // 2)
            if key not in cells:
                cells[key] = rng.choices([c for c, _ in weights], [n for _, n in weights])[0]
            c = cells[key]
            if y == h - 1 and h > 2:
                c = rim
            elif x in (0, w - 1) and w > 2 and c == FROST:
                c = LIGHT
            elif top_light and y == 0 and h > 2:
                c = FROST
            if rng.random() < speckle * 0.4:
                c = SHINE
            px(tex, x0 + x, y0 + y, c)


def fill(rect, c, img=None, a=255):
    x0, y0, w, h = rect
    for y in range(h):
        for x in range(w):
            px(img or tex, x0 + x, y0 + y, c, a)


def hline(rect, row, c, glow_too=False, x_from=0, x_to=None):
    x0, y0, w, h = rect
    for x in range(x_from, w if x_to is None else x_to):
        px(tex, x0 + x, y0 + row, c)
        if glow_too:
            px(glow, x0 + x, y0 + row, c)


def paint(role, f, size):
    w, h, d = size
    if role in ("helm",):
        for k in f: metal(f[k])
        fill(f["up"], FROST)
        for k in ("north", "east", "west", "south"): hline(f[k], 0, SHINE)
        # visor band across the face, eye slit glows
        fx, fy, fw, fh = f["north"]
        for y in range(2, 6):
            for x in range(1, fw - 1):
                px(tex, fx + x, fy + y, VISOR_HI if y == 2 else VISOR)
                px(glow, fx + x, fy + y, (*VISOR_HI,) if y == 2 else VISOR)
        for k in ("east", "west"):  # accent band around the brow line
            hline(f[k], 2, ACCENT, glow_too=True, x_from=1, x_to=f[k][2] - 1)
    elif role in ("ridge", "brow", "fauld", "belt", "pauldron_top"):
        for k in f: metal(f[k], base=LIGHT, rim=MID, top_light=False, speckle=0.12)
        if role in ("fauld", "belt"):
            for k in ("north", "east", "west", "south"):
                hline(f[k], 1 if f[k][3] > 1 else 0, ACCENT_DEEP, x_from=1, x_to=max(1, f[k][2] - 1))
    elif role == "crest":
        for k in f:
            fill(f[k], ACCENT, a=235); fill(f[k], ACCENT, img=glow)
            x0, y0, fw, fh = f[k]
            px(tex, x0, y0, GEM_CORE); px(glow, x0, y0, GEM_CORE)
    elif role == "gem":
        for k in f:
            fill(f[k], ACCENT); fill(f[k], ACCENT, img=glow)
        fx, fy, fw, fh = f["north"]
        for y in range(fh):
            for x in range(fw):
                c = GEM_CORE if (x, y) == (fw // 2, fh // 2) else (SHINE if x + y == 0 else ACCENT)
                px(tex, fx + x, fy + y, c); px(glow, fx + x, fy + y, c)
    elif role in ("breast", "backplate", "knee"):
        for k in f: metal(f[k], speckle=0.22)
        if role == "breast":
            fx, fy, fw, fh = f["north"]
            for y in range(1, fh - 1):  # accent seams either side of the gem
                for x in (1, fw - 2):
                    px(tex, fx + x, fy + y, ACCENT_DEEP)
    elif role in ("pauldron", "flare", "cuff"):
        for k in f: metal(f[k], base=LIGHT, rim=MID, speckle=0.15)
        hline(f["up"], 0, SHINE); hline(f["up"], f["up"][3] - 1, SHINE)
        if role != "flare":
            for k in ("north", "east", "west", "south"):
                hline(f[k], f[k][3] - 1, ACCENT, glow_too=True, x_from=0, x_to=f[k][2])
    elif role in ("plate", "leg", "boot"):
        for k in f: metal(f[k])
        if role == "plate" and w == 8:  # chest: vertical accent seams on the sides
            for k in ("east", "west"):
                x0, y0, fw, fh = f[k]
                for y in range(2, fh - 2):
                    px(tex, x0 + fw // 2, y0 + y, ACCENT); px(glow, x0 + fw // 2, y0 + y, ACCENT)
        if role == "leg":
            hline(f["north"], 6, ACCENT_DEEP, x_from=1, x_to=f["north"][2] - 1)
        if role == "boot":
            for k in ("north", "east", "west", "south"):
                hline(f[k], f[k][3] - 2, DARK)
    else:
        raise SystemExit(f"unknown role {role}")


shelf = Shelf()
bones = [{"name": n, "pivot": p} for n, p in BIPEDS.items()]
for name, spec in ARMOR.items():
    cubes = []
    for role, origin, size, inflate in spec["cubes"]:
        w, h, d = size
        net_w, net_h = 2 * (w + d), d + h
        u, v = shelf.place(net_w, net_h)
        paint(role, faces(u, v, w, h, d), size)
        cube = {"origin": origin, "size": size, "uv": [u, v]}
        if inflate:
            cube["inflate"] = inflate
        cubes.append(cube)
    bones.append({"name": name, "parent": spec["parent"], "pivot": spec["pivot"], "cubes": cubes})

geo = {"format_version": "1.12.0", "minecraft:geometry": [{
    "description": {"identifier": "geometry.zerog_tweaks.armor.moonsteel", "texture_width": TEX_W,
                    "texture_height": TEX_H, "visible_bounds_width": 3, "visible_bounds_height": 3,
                    "visible_bounds_offset": [0, 1.5, 0]},
    "bones": bones}]}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "moonsteel.geo.json").write_text(json.dumps(geo, indent=2) + "\n", encoding="utf-8")
tex.save(OUT / "moonsteel.png")
glow.save(OUT / "moonsteel_glowmask.png")
print(f"cubes={sum(len(b.get('cubes', [])) for b in bones)} atlas_rows_used={shelf.y + shelf.row_h}/{TEX_H}")
