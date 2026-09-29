#!/usr/bin/env python3
# Regenerates every image in docs/images/ for the README + docs/HELP.md.
# Prerequisites (run once, any WSL/python3 with Pillow):
#   mkdir -p /tmp/zg/bees2/assets/aeroapiary
#   unzip -o -q "Desktop/ZeroG_Mods/zero-g-Orbital-Bee's/build/libs/zerog-binnie-expansion-1.21.1-1.0.0.jar" \
#       -d /tmp/zg/bees2 'assets/aeroapiary/textures/block/*' 'assets/aeroapiary/textures/item/*'
#   (ZeroG Tweaks textures are read from docs/zero-g-tweaks-bundle/resources/ inside this repo.)
# Then:  python3 docs/images/generate_images.py
"""Generate diagram + gallery images for the ZeroG Tweaks / ZeroG Bees README (v2)."""
import glob, os, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = "/mnt/c/Users/jakem/Desktop/ZeroG_Mods/ZeroG_Tweaks"
OUT = os.path.join(ROOT, "docs/images")
os.makedirs(OUT, exist_ok=True)
BEES_TEX = "/tmp/zg/bees2/assets/aeroapiary/textures"
ITEM_TEX = "/tmp/zg/bees2/assets/aeroapiary/textures/item"
TWK_TEX = os.path.join(ROOT, "docs/zero-g-tweaks-bundle/resources/assets/zerog_tweaks/textures")

BG      = (11, 14, 24)
PANEL   = (20, 26, 42)
PANEL2  = (27, 35, 56)
ACCENT  = (111, 216, 255)
ACCENT2 = (232, 154, 98)
ACCENT3 = (170, 130, 255)
TXT     = (232, 240, 255)
MUTED   = (138, 151, 181)
GOOD    = (120, 230, 160)
AIR     = (30, 38, 58)

def font(size, bold=False):
    cands = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/mnt/c/Windows/Fonts/arialbd.ttf" if bold else "/mnt/c/Windows/Fonts/arial.ttf",
    ]
    for c in cands:
        if os.path.exists(c):
            try: return ImageFont.truetype(c, size)
            except Exception: pass
    return ImageFont.load_default()

F = lambda s: font(s)
FB = lambda s: font(s, True)

def starfield(w, h, seed=7, n=None):
    import random
    r = random.Random(seed)
    im = Image.new("RGB", (w, h), BG)
    glow = Image.new("RGB", (w, h), BG)
    gd = ImageDraw.Draw(glow)
    for _ in range(6):
        x, y = r.randint(0, w), r.randint(0, h)
        rad = r.randint(h // 4, h // 2)
        col = r.choice([(24, 36, 66), (36, 24, 60), (16, 44, 60)])
        gd.ellipse([x - rad, y - rad, x + rad, y + rad], fill=col)
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    im = Image.blend(im, glow, 0.5)
    d = ImageDraw.Draw(im)
    n = n or int(w * h / 5200)
    for _ in range(n):
        x, y = r.randint(0, w - 1), r.randint(0, h - 1)
        b = r.choice([(70, 80, 105), (110, 120, 150), (170, 185, 215), (235, 245, 255)])
        d.point((x, y), fill=b)
    return im

def px(path, size):
    """load texture, resize longest side to `size` px (nearest). None if missing."""
    if not os.path.exists(path) and not os.path.exists(path + ".png"):
        return None
    if not os.path.exists(path):
        path += ".png"
    im = Image.open(path).convert("RGBA")
    w, h = im.width, im.height
    if w >= h:
        return im.resize((size, max(1, int(h * size / w))), Image.NEAREST)
    return im.resize((max(1, int(w * size / h)), size), Image.NEAREST)

def paste_centered(base, tile, cx, cy):
    base.paste(tile, (int(cx - tile.width / 2), int(cy - tile.height / 2)), tile)

def chip(d, x, y, w, h, fill=PANEL, outline=None, rad=10):
    d.rounded_rectangle([x, y, x + w, y + h], radius=rad, fill=fill, outline=outline, width=2 if outline else 0)

def badge(d, x, y, text, fg=ACCENT, fs=20):
    f = FB(fs)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + tw + 22, y + fs + 14], radius=(fs + 14) // 2,
                        fill=(fg[0] // 6 + 8, fg[1] // 6 + 10, fg[2] // 6 + 14), outline=fg, width=2)
    d.text((x + 11, y + 6), text, font=f, fill=fg)
    return tw + 22

def title_strip(d, x, y, title, subtitle, accent=ACCENT):
    d.rectangle([x, y, x + 8, y + 52], fill=accent)
    d.text((x + 26, y - 2), title, font=FB(40), fill=TXT)
    d.text((x + 26, y + 52), subtitle, font=F(20), fill=MUTED)

def arrow(d, p1, p2, color=ACCENT, w=4, head=12):
    import math
    d.line([p1, p2], fill=color, width=w)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    for da in (2.6, -2.6):
        d.line([p2, (p2[0] - head * math.cos(ang + da), p2[1] - head * math.sin(ang + da))],
               fill=color, width=max(2, w - 2))

# ============================================================
# 1. GALAXY PROGRESSION
# ============================================================
def img_galaxy():
    W, H = 1500, 1120
    im = starfield(W, H, seed=11)
    d = ImageDraw.Draw(im)
    title_strip(d, 70, 54, "Galaxy progression",
                "materials from galaxy N build the gate that reaches galaxy N+1", ACCENT)
    hops = [
        ("SOL", "Galaxy 1 · Earth, Moon, Mars (fixed)", "NULLIFITE",
         "rare deepslate ore · ancient cities", (150, 160, 185), ACCENT),
        ("CERULON", "Galaxy 2 · blue, crystalline", "CERULITE", None, (63, 201, 232), ACCENT),
        ("SKARN", "Galaxy 3 · fractured, hostile", "SKARNITE", None, (255, 138, 42), ACCENT2),
        ("EIDOLON", "Galaxy 4 · frozen, derelict", "EIDOLITE", None, (150, 216, 255), ACCENT),
        ("SOLVANE", "Galaxy 5 · stellar endgame, fading sun", "SOLVANITE", None, (255, 210, 110), ACCENT3),
    ]
    ty = 230; rowh = 138; lx = 150
    gates = ["T1 gate: built from overworld Nullifite", "T2 gate: built from Sol materials",
             "T3 gate: built from Cerulon ore", "T4 gate: built from Skarn materials",
             "T5 gate: built from Eidolon materials"]
    for i, (world, sub, ore, ore_note, col, acc) in enumerate(hops):
        y = ty + i * rowh
        chip(d, lx, y, 356, 104, PANEL, acc)
        d.text((lx + 20, y + 15), world, font=FB(33), fill=TXT)
        d.text((lx + 20, y + 62), sub, font=F(17), fill=MUTED)
        chip(d, lx + 422, y + 16, 300, 72, PANEL2, col)
        d.text((lx + 442, y + 26), ore, font=FB(25), fill=col)
        if ore_note:
            d.text((lx + 442, y + 58), ore_note, font=F(16), fill=MUTED)
        arrow(d, (lx - 40, y + 52), (lx - 8, y + 52), acc, 5)
        if i > 0:
            yc = y - 24
            arrow(d, (lx + 581, yc), (lx + 581, y + 10), ACCENT3, 4)
            d.text((lx + 601, yc - 4), gates[i - 1] if i > 1 else gates[0], font=F(16), fill=MUTED, anchor="lb")
    d.multiline_text((lx, H - 128),
        "Design: every wasteland hides one small reward — a plant, a mob drop or a ruin — so no planet is worth skipping.\n"
        "Resource-planet names are locked so ores, lore and wiki pages always match; wasteland and moon names roll per seed.",
        font=F(19), fill=MUTED, spacing=10)
    im.save(f"{OUT}/diagram_galaxy_progression.png")

# ============================================================
# 2. 5x5x5 ALVEARY
# ============================================================
def img_alveary():
    W, H = 1500, 1080
    im = starfield(W, H, seed=23)
    d = ImageDraw.Draw(im)
    title_strip(d, 70, 54, "Orbital Alveary — structure map",
                "Forestry-pattern multiblock: 5 wide × 5 deep × 5 tall = 125 cells, validated by AlvearyStructureValidator", ACCENT)
    tx = 500; ty = 205; cell = 72; gap = 6
    rows = [
        ("y+4  roof", "roof", ACCENT2),
        ("y+3  top ring", "part", ACCENT),
        ("y+2  ring", "open", ACCENT3),
        ("y+1  ring", "open", ACCENT3),
        ("y+0  floor", "floor", GOOD),
    ]
    for ri, (label, kind, acc) in enumerate(rows):
        y = ty + (4 - ri) * (cell + 30)
        d.text((tx - 16, y + cell // 2 - 11), label, font=FB(20), fill=TXT, anchor="rm")
        for ci in range(5):
            x = tx + ci * (cell + gap)
            center3 = 1 <= ci <= 3 and kind == "open"
            if center3:
                chip(d, x, y, cell, cell, AIR, MUTED, 6)
                d.text((x + cell // 2, y + cell // 2), "air", font=F(15), fill=MUTED, anchor="mm")
            elif kind == "roof":
                chip(d, x, y, cell, cell, (55, 46, 30), ACCENT2, 6)
                d.text((x + cell // 2, y + cell // 2), "roof", font=F(14), fill=ACCENT2, anchor="mm")
            elif kind == "floor" and ci == 2:
                chip(d, x, y, cell, cell, (26, 52, 40), GOOD, 6)
                d.multiline_text((x + cell // 2, y + cell // 2), "APIARY\nCONTROLLER", font=FB(13), fill=GOOD, anchor="mm", align="center", spacing=1)
            else:
                chip(d, x, y, cell, cell, PANEL2, acc, 6)
                d.text((x + cell // 2, y + cell // 2), "part", font=F(14), fill=MUTED, anchor="mm")
    ly = ty + 5 * (cell + 30) + 16; lx = tx - 160
    legend = [(GOOD, "controller (part of its tier's floor)"),
              (ACCENT, "tierN_* structure cells"),
              (ACCENT2, "tierN_roof top ring"),
              (MUTED, "air — core 3×3 of y+1, y+2")]
    for col, t in legend:
        d.ellipse([lx, ly + 4, lx + 22, ly + 26], fill=col)
        d.text((lx + 32, ly), t, font=F(18), fill=TXT)
        ly += 38
    rx = 940
    d.text((rx, ty - 6), "RULES", font=FB(24), fill=ACCENT)
    rules = [
        "• every structure cell must be an\n  aeroapiary block of its own tier",
        "• controller sits on the floor ring,\n  one step out from the (+x,+z) corner",
        "• core 3×3 of rings y+1/y+2 must\n  stay air — the working cavity",
        "• top ring is strictly tierN_roof —\n  a gap or foreign block refuses\n  the whole structure",
        "• at least ONE tierN_energy_port\n  required (more = faster charge)",
        "• tierN_frame_housing count is the\n  frame-modifier budget, reported in\n  the controller GUI",
    ]
    yy = ty + 52
    for t in rules:
        lines = t.count("\n") + 1
        d.multiline_text((rx, yy), t, font=F(20), fill=TXT, spacing=6)
        yy += lines * 30 + 18
    d.text((70, H - 104),
        "Status line on the controller GUI: green ALVEARY FORMED / red INCOMPLETE + exact reason. The production cycle resets while unformed.\n"
        "Formation re-checks every 20 ticks server-side; tier scales the cycle length, tier 1 → 7: 800 → 200 ticks.",
        font=F(20), fill=MUTED, spacing=8)
    im.save(f"{OUT}/diagram_5x5_alveary.png")

# ============================================================
# 3. PRODUCT FLOW
# ============================================================
def img_flow():
    W, H = 1660, 1180
    im = starfield(W, H, seed=5)
    d = ImageDraw.Draw(im)
    title_strip(d, 70, 54, "ZeroG bees — product flow",
                "space beekeeping built on Productive Bees: six custom bee species feed the alveary machines", ACCENT)
    bees = ["stardust", "void", "meteor", "nebula", "solar", "comet"]
    bx = 70
    d.text((bx, 172), "SPACE BEE SPECIES  (Productive Bees species JSONs — breeding, centrifuge recipes, comb dispatch)",
           font=FB(19), fill=MUTED)
    yy = 208
    for b in bees:
        t = badge(d, bx, yy, b + "_bee", ACCENT3, 21); bx += t + 14
    d.text((70, 292), "MACHINES  (right-click → manifest-driven GUI)", font=FB(19), fill=MUTED)
    machines = [
        ("zero_g_hive", "hive · queen + frames"),
        ("stardust_smelter", "→ stardust"),
        ("starmetal_smelter", "→ starmetal ingots"),
        ("silk_weaver", "→ woven silk"),
        ("gravitational_centrifuge", "→ comb products"),
        ("frame_assembler", "→ untreated frames"),
        ("frame_infusion_altar", "→ special frames"),
    ]
    my = 330; mx = 70
    for name, note in machines:
        chip(d, mx, my, 450, 76, PANEL, ACCENT)
        t_im = px(f"{BEES_TEX}/block/other/{name}_front.png", 48)
        if t_im: paste_centered(im, t_im, mx + 40, my + 38)
        d.text((mx + 92, my + 10), name, font=FB(22), fill=TXT)
        d.text((mx + 92, my + 44), note, font=F(17), fill=MUTED)
        my += 88
    d.text((735, 292), "PRODUCTS", font=FB(19), fill=MUTED)
    items = ["stardust_comb", "void_comb", "meteor_comb", "nebula_comb", "solar_comb", "comet_comb", "molten_comb",
             "honey_drop", "royal_jelly", "cosmic_jelly", "astro_honey", "silk_thread",
             "untreated_frame", "proven_frame", "impregnated_frame", "starmetal_frame", "starlit_frame", "frame_void"]
    for i, it in enumerate(items):
        c, r = i % 3, i // 3
        cx = 735 + c * 300; cy = 324 + r * 112
        t_im = px(f"{ITEM_TEX}/{it}.png", 60)
        chip(d, cx, cy, 276, 96, PANEL2, ACCENT3)
        if t_im: paste_centered(im, t_im, cx + 54, cy + 48)
        else: d.text((cx + 54, cy + 48), "?", font=FB(30), fill=MUTED, anchor="mm")
        nm = it.replace("_", " ")
        d.multiline_text((cx + 112, cy + 24), "\n".join(textwrap.wrap(nm, 14)), font=FB(19), fill=TXT, spacing=2)
    arrow(d, (536, 460), (726, 460), ACCENT, 5, 14)
    d.text((556, 484), "cycles", font=F(17), fill=MUTED)
    d.text((70, H - 88),
        "Alveary cycle (tier 1 → 7: 800 → 200 ticks) consumes frames + queen output; tierN_frame_housing count sets the frame budget.\n"
        "PB bridge: spawn-egg → our-hive item bridge, per-bee comb dispatch, PB breeding chains and centrifuge recipes under data/aeroapiary/productivebees/.",
        font=F(19), fill=MUTED, spacing=8)
    im.save(f"{OUT}/diagram_product_flow.png")

# ============================================================
# 4. PACK LAYOUT
# ============================================================
def img_pack():
    W, H = 1500, 1020
    im = starfield(W, H, seed=31)
    d = ImageDraw.Draw(im)
    title_strip(d, 70, 54, "Pack layout — dependencies + folder",
                "what goes in mods/, and the required-load-order chain (instance: CurseForge → ZeroG)", ACCENT)
    rows = [
        ("minecraft", "1.21.1", (245, 245, 245)),
        ("neoforge", "21.1.252", (247, 193, 84)),
        ("geckolib", "4.9.3", (150, 200, 255)),
        ("productivebees", "1.21.1-13.14.0", (255, 170, 90)),
        ("zerog-binnie-expansion\n(ZeroG Bees · aeroapiary)", "1.0.0", GOOD),
        ("zerog-tweaks", "1.0.0 · zero required deps", ACCENT),
    ]
    y = 220; arrow_rows = []
    for idx, (name, ver, col) in enumerate(rows):
        chip(d, 90, y, 640, 84, PANEL, col)
        head = name.split("\n")[0]
        head = head[:-1] if len(head) > 25 else head
        d.text((116, y + 16), head, font=FB(26), fill=TXT)
        if "\n" in name:
            d.text((560, y + 14), "ZeroG Bees", font=F(19), fill=GOOD)
        d.text((116, y + 52), ver, font=F(18), fill=MUTED)
        if idx in (2, 3, 4):
            arrow_rows.append(y + 42)
        y += 102
    pb_cy = 220 + 3 * 102 + 42
    for ay in arrow_rows:
        arrow(d, (744, ay), (744, pb_cy), ACCENT3, 3)
    d.multiline_text((760, pb_cy - 10), "required AFTER\n(PB's version string is\nMC-prefixed: [1.21.1-13.0,))",
                     font=F(16), fill=ACCENT3, spacing=4)
    fx = 1100
    d.text((fx, 190), "instance mods/ folder", font=FB(22), fill=ACCENT)
    files = ["productivebees-1.21.1-13.14.0.jar", "zerog-binnie-expansion-…1.0.0.jar",
             "zerog-tweaks-1.21.1-…1.0.0.jar", "geckolib-neoforge-…4.9.3.jar", "(…other pack mods)"]
    yy = 236
    for f in files:
        hl = f.startswith(("zerog", "productivebees"))
        if hl: d.rectangle([fx - 12, yy - 1, fx - 6, yy + 22], fill=ACCENT)
        d.text((fx, yy), f, font=FB(17) if hl else F(17), fill=TXT if hl else MUTED)
        yy += 44
    d.multiline_text((fx, yy + 30),
        "Release jars are committed in\nthis repo under docs/jars/\nwith SHA256SUMS.txt — copy\nthem straight into mods/.",
        font=F(19), fill=MUTED, spacing=8)
    d.text((70, H - 96),
        "ZeroG Tweaks ships with ZERO required dependencies — pure NeoForge; GeckoLib is only needed where other pack mods use it.\n"
        "ZeroG Bees requires Productive Bees + GeckoLib 4.9 and loads AFTER both.",
        font=F(20), fill=MUTED, spacing=8)
    im.save(f"{OUT}/diagram_pack_layout.png")

# ============================================================
# 5. LOGO
# ============================================================
def img_logo():
    W, H = 1200, 320
    im = starfield(W, H, seed=3, n=int(W * H / 3400))
    d = ImageDraw.Draw(im)
    d.text((80, 74), "ZERO", font=FB(94), fill=TXT)
    tw = d.textlength("ZERO", font=FB(94))
    d.text((84 + tw, 74), "G", font=FB(94), fill=ACCENT)
    tw2 = d.textlength("ZEROG", font=FB(94))
    d.rectangle([84, 176, 84 + tw2, 184], fill=ACCENT)
    d.text((84, 198), "TWEAKS  +  BEES", font=FB(40), fill=MUTED)
    badge(d, 700, 100, "NeoForge 1.21.1", ACCENT, 23)
    badge(d, 700, 160, "two jars · one pack", ACCENT3, 23)
    im.save(f"{OUT}/logo.png")

# ============================================================
# 6-7. BEES MACHINE + ITEM IMAGES
# ============================================================
BEES_STRIP = 150
def bees_machines_img():
    faces = [
        ("other/zero_g_hive_front", "Zero-G Hive"),
        ("other/stardust_smelter_front", "Stardust Smelter"),
        ("other/starmetal_smelter_front", "Starmetal Smelter"),
        ("other/silk_weaver_front", "Silk Weaver"),
        ("other/frame_assembler_front", "Frame Assembler"),
        ("other/infusion_altar_front", "Infusion Altar"),
        ("other/centrifuge_front", "Centrifuge"),
        ("other/meteor_comb_block_front", "Meteor Comb Block"),
    ]
    tl = 128; pad = 30; slotw = tl + 66
    cols = 4
    W = pad + cols * (slotw + pad) + 120
    rows = (len(faces) + cols - 1) // cols
    H = BEES_STRIP + 40 + rows * (tl + 62) + 20
    im = starfield(W, H, seed=9)
    d = ImageDraw.Draw(im)
    title_strip(d, 40, 36, "ZeroG Bees — machines and hive blocks",
                "block textures straight from the shipped jar, nearest-upscaled", ACCENT)
    for i, (tex, name) in enumerate(faces):
        r, c = divmod(i, cols)
        x = pad + c * (slotw + pad)
        y = BEES_STRIP + 30 + r * (tl + 62)
        chip(d, x, y, tl + 14, tl + 14, (28, 34, 52), ACCENT, 8)
        t_im = px(f"{BEES_TEX}/block/{tex}", tl - 6)
        if t_im: paste_centered(im, t_im, x + (tl + 14) / 2, y + (tl + 14) / 2)
        d.multiline_text((x + (tl + 14) / 2, y + tl + 22), "\n".join(textwrap.wrap(name, 14)),
                         font=F(19), fill=TXT, anchor="ma", align="center", spacing=2)
    im.save(f"{OUT}/bees_machines.png")

def bees_items_img():
    groups = [
        ("SPACE COMBS", ["stardust_comb", "void_comb", "meteor_comb", "nebula_comb", "solar_comb", "comet_comb", "molten_comb"]),
        ("FRAMES", ["untreated_frame", "proven_frame", "impregnated_frame", "starmetal_frame", "starlit_frame", "frame_void", "aero_frame", "aero_silk_frame"]),
        ("FOOD / METALS", ["honey_drop", "royal_jelly", "cosmic_jelly", "astro_honey", "silk_thread", "stardust", "starmetal_ingot", "aeronautic_alloy"]),
        ("APIARIST GEAR", ["basic_scoop", "magnetic_bee_scoop", "bee_smoker", "apiarist_wrench", "portable_beealyzer", "habitat_locator"]),
    ]
    tl = 100; cw = 60
    maxn = max(len(g[1]) for g in groups)
    W = 320 + maxn * (tl + cw) + 60
    H = BEES_STRIP + 50 + len(groups) * (tl + 92) + 30
    im = starfield(W, H, seed=13)
    d = ImageDraw.Draw(im)
    title_strip(d, 40, 36, "ZeroG Bees — items: combs, frames, gear",
                "icon textures from the shipped jar (64px sources; _hd and _inventory variants also included)", ACCENT3)
    yy = BEES_STRIP + 40
    for gname, group in groups:
        d.text((56, yy + tl // 2 - 12), gname, font=FB(23), fill=ACCENT3)
        cxx = 320
        for it in group:
            t_im = px(f"{ITEM_TEX}/{it}.png", tl - 4)
            chip(d, cxx, yy, tl + 4, tl + 4, (28, 34, 52), ACCENT3, 8)
            if t_im: paste_centered(im, t_im, cxx + (tl + 4) / 2, yy + (tl + 4) / 2)
            d.multiline_text((cxx + (tl + 4) / 2, yy + tl + 12), "\n".join(textwrap.wrap(it.replace("_", " "), 13)),
                             font=F(16), fill=MUTED, anchor="ma", align="center", spacing=2)
            cxx += tl + cw
        yy += tl + 92
    im.save(f"{OUT}/bees_items.png")

# ============================================================
# GALLERY (cropped sheets + title strip)
# ============================================================
STRIP = 150
def gallery(src, dst, title, sub, accent=ACCENT, max_h=1500):
    sheet = Image.open(src).convert("RGB")
    if sheet.height > max_h: sheet = sheet.crop((0, 0, sheet.width, max_h))
    W = max(sheet.width, 1200)
    H = STRIP + sheet.height
    im = starfield(W, H, seed=17)
    d = ImageDraw.Draw(im)
    title_strip(d, 40, 36, title, sub, accent)
    im.paste(sheet, ((W - sheet.width) // 2, STRIP))
    im.save(dst)

print("building…")
img_galaxy(); img_alveary(); img_flow(); img_pack(); img_logo()
bees_machines_img(); bees_items_img()
gal = [
    ("sheets/materials_and_blocks/07_machine_blocks.png", "gallery_machines.png", "Machines & gate blocks", "functional blocks + the galaxy gate family", ACCENT, 1500),
    ("sheets/materials_and_blocks/06_teleporter_blocks.png", "gallery_teleporter.png", "Teleporter / gate blocks", "the tiered galaxy teleporter family", ACCENT2, 1500),
    ("sheets/mobs/01_regolith_crawler.png", "gallery_mobs.png", "Mob sheets — sample", "28 mob + boss design sheets; ships as loot/interaction data", ACCENT3, 1500),
    ("sheets/gear/15_gear_sol.png", "gallery_gear.png", "Gear — Sol set", "9+ full tool + armor kits, one per world family", GOOD, 1500),
    ("sheets/armor/01_nullifite_armor.png", "gallery_armor.png", "Armor — Nullifite set", "worn armor reference, shown front + back", ACCENT, 1500),
    ("sheets/food_and_items/22_food_meats.png", "gallery_food.png", "Food & items", "65 food/util items: dishes, materials, templates, keys", ACCENT, 1900),
]
base = f"{ROOT}/docs/zero-g-tweaks-bundle"
for src, dst, t, s, a, mh in gal:
    gallery(f"{base}/{src}", f"{OUT}/{dst}", t, s, a, mh)
    print(dst, "ok")
for f in ["diagram_galaxy_progression.png", "diagram_5x5_alveary.png", "diagram_product_flow.png",
          "diagram_pack_layout.png", "logo.png", "bees_machines.png", "bees_items.png"]:
    print(f, "ok")
print("DONE")