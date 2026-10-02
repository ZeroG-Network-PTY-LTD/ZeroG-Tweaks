"""Vanilla-style 3D item models (1 px extrusion) for every ZeroG smithing template, for Blockbench.

Each opaque pixel row run becomes one 1 px thick element with front/back faces and edge faces, exactly like the
item Minecraft generates from a flat sprite, with the vanilla item/generated display transforms.
usage: python build_templates.py TEXTURE_DIR OUT_DIR
writes OUT_DIR/<template>.json and prints the list
"""
import json, sys
from pathlib import Path
from PIL import Image

TEX = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
DISPLAY = {
    "thirdperson_righthand": {"rotation": [0, 0, 0], "translation": [0, 3, 1], "scale": [0.55, 0.55, 0.55]},
    "firstperson_righthand": {"rotation": [0, -90, 25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
    "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.5, 0.5, 0.5]},
    "head": {"rotation": [0, 180, 0], "translation": [0, 13, 7], "scale": [1, 1, 1]},
    "fixed": {"rotation": [0, 180, 0], "scale": [1, 1, 1]},
}
names = sorted(p.stem for p in TEX.glob("*_smithing_template.png"))
for name in names:
    im = Image.open(TEX / f"{name}.png").convert("RGBA")
    elements = []
    for y in range(16):
        x = 0
        while x < 16:
            if im.getpixel((x, y))[3] == 0:
                x += 1
                continue
            x1 = x
            while x1 < 16 and im.getpixel((x1, y))[3]:
                x1 += 1
            run, left, right = [x, y, x1, y + 1], [x, y, x + 1, y + 1], [x1 - 1, y, x1, y + 1]
            elements.append({"from": [x, 15 - y, 7.5], "to": [x1, 16 - y, 8.5], "faces": {
                "south": {"uv": run, "texture": "#0"}, "north": {"uv": [x1, y, x, y + 1], "texture": "#0"},
                "up": {"uv": run, "texture": "#0"}, "down": {"uv": run, "texture": "#0"},
                "west": {"uv": left, "texture": "#0"}, "east": {"uv": right, "texture": "#0"}}})
            x = x1
    model = {"credit": "ZeroG Tweaks - smithing template item (1 px, vanilla style)", "gui_light": "front",
             "textures": {"0": f"zerog_tweaks:item/{name}", "particle": f"zerog_tweaks:item/{name}"},
             "elements": elements, "display": DISPLAY}
    (OUT / f"{name}.json").write_text(json.dumps(model, indent=1) + "\n", encoding="utf-8")
    print(f"{name:45s} elements={len(elements)}")
print(f"{len(names)} templates")
