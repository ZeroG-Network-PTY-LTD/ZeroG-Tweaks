"""Moonsteel 3D held tools from their 16x16 sprites (design sheet rules).

Handle 1.5 px thick, head/blade 2.5 px, gems/accents 3 px. Gem pixels (and the sword's
edge + fuller) are emissive. In hand: 3D model scaled 1.5x. In the inventory (gui): the
original flat sprite, via NeoForge's separate_transforms loader.

usage: python gen_tools.py ASSETS_DIR     (…/assets/zerog_tweaks)
"""
import json, sys
from pathlib import Path
from PIL import Image

ASSETS = Path(sys.argv[1])
NS = "zerog_tweaks"
TOOLS = ["sword", "pickaxe", "axe", "shovel", "hoe"]

HANDLE = {(0x14, 0x18, 0x20), (0x9E, 0xA8, 0xB4), (0x3A, 0x42, 0x50)}
GEM = {(0xA8, 0xD8, 0xFF), (0xEE, 0xF8, 0xFF), (0x5A, 0x8A, 0xB0)}
GLOW = {(0xA8, 0xD8, 0xFF), (0xEE, 0xF8, 0xFF)}
SWORD_EDGE = (0xEE, 0xF4, 0xFA)
THICK = {"handle": 1.5, "head": 2.5, "gem": 3.0}

# vanilla handheld transforms, in-hand scaled 1.5x as the sheet asks
S = 1.5
DISPLAY = {
    "thirdperson_righthand": {"rotation": [0, -90, 55], "translation": [0, 4.0, 0.5], "scale": [0.85 * S] * 3},
    "thirdperson_lefthand": {"rotation": [0, 90, -55], "translation": [0, 4.0, 0.5], "scale": [0.85 * S] * 3},
    "firstperson_righthand": {"rotation": [0, -90, 25], "translation": [1.13, 3.2, 1.13], "scale": [0.68 * S] * 3},
    "firstperson_lefthand": {"rotation": [0, 90, -25], "translation": [1.13, 3.2, 1.13], "scale": [0.68 * S] * 3},
    "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.5, 0.5, 0.5]},
    "head": {"rotation": [0, 180, 0], "translation": [0, 13, 7], "scale": [1, 1, 1]},
    "fixed": {"rotation": [0, 180, 0], "translation": [0, 0, 0], "scale": [1, 1, 1]},
}


def classify(tool, x, y, rgb):
    """Return (thickness class, emissive) for one opaque pixel."""
    if rgb in GEM:
        return "gem", rgb in GLOW
    if rgb in HANDLE or (x <= 4 and y >= 12):  # grip + pommel outline
        return "handle", False
    if tool == "sword" and rgb == SWORD_EDGE:
        return "head", True  # blade edge glows
    return "head", False


def build(tool):
    sprite = f"{NS}:item/moonsteel_{tool}"
    im = Image.open(ASSETS / "textures/item" / f"moonsteel_{tool}.png").convert("RGBA")
    elements = []
    for y in range(16):
        x = 0
        while x < 16:
            p = im.getpixel((x, y))
            if p[3] == 0:
                x += 1
                continue
            cls = classify(tool, x, y, p[:3])
            x1 = x + 1  # merge a horizontal run of the same class
            while x1 < 16 and im.getpixel((x1, y))[3] and classify(tool, x1, y, im.getpixel((x1, y))[:3]) == cls:
                x1 += 1
            half = THICK[cls[0]] / 2
            uv_run, uv_l, uv_r = [x, y, x1, y + 1], [x, y, x + 1, y + 1], [x1 - 1, y, x1, y + 1]
            el = {"from": [x, 15 - y, 8 - half], "to": [x1, 16 - y, 8 + half],
                  "faces": {"north": {"uv": uv_run, "texture": "#layer0"},
                            "south": {"uv": uv_run, "texture": "#layer0"},
                            "up": {"uv": uv_run, "texture": "#layer0"},
                            "down": {"uv": uv_run, "texture": "#layer0"},
                            "west": {"uv": uv_l, "texture": "#layer0"},
                            "east": {"uv": uv_r, "texture": "#layer0"}}}
            if cls[1]:
                el["neoforge_data"] = {"block_light": 15, "sky_light": 15}
            elements.append(el)
            x = x1
    model_3d = {"textures": {"layer0": sprite, "particle": sprite}, "elements": elements, "display": DISPLAY}
    item = {"loader": "neoforge:separate_transforms",
            "base": {"parent": f"{NS}:item/moonsteel_{tool}_3d"},
            "perspectives": {"gui": {"parent": "minecraft:item/handheld", "textures": {"layer0": sprite}}}}
    out = ASSETS / "models/item"
    (out / f"moonsteel_{tool}_3d.json").write_text(json.dumps(model_3d, indent=1) + "\n", encoding="utf-8")
    (out / f"moonsteel_{tool}.json").write_text(json.dumps(item, indent=2) + "\n", encoding="utf-8")
    return len(elements), sum(1 for e in elements if "neoforge_data" in e)


for t in TOOLS:
    n, g = build(t)
    print(f"{t:8s} elements={n:3d} emissive={g}")
