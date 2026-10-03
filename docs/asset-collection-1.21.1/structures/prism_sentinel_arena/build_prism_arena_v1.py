"""Prism Sentinel arena ("Keeper's Proving Hall", Cerulon) as Minecraft commands.

Builds around (0, Y0, 0) inside a 47 x 22 x 47 box (fits one structure block). Writes C:/zt-tmp/arena_commands.txt
and prints counts. Blocks are ZeroG (zerog_tweaks:) plus vanilla accents.
"""
import math, random

Y0 = -61  # superflat grass layer: the floor replaces it
rng = random.Random(1337)
Z = "zerog_tweaks:"
B = {}


def put(x, y, z, block):
    B[(x, Y0 + y, z)] = block


def r_of(x, z):
    return math.hypot(x, z)


# ---- floor -----------------------------------------------------------------------------------------
for x in range(-21, 22):
    for z in range(-21, 22):
        r = r_of(x, z)
        if r > 20.6:
            continue
        b = Z + "polished_black_cerulean_stone_bricks"
        if r <= 16.6: b = Z + "polished_cerulean_stone"
        if 11 <= r <= 12.4: b = Z + "polished_black_prismstone"
        if r <= 5.6: b = Z + "polished_prismstone"
        if r <= 2.6: b = Z + "chiseled_prismstone"
        # 8 light channels feeding the dais (cardinal + diagonal), between the dais and the wall
        if 6 <= r <= 16.4 and (x == 0 or z == 0 or abs(x) == abs(z)):
            b = Z + "pulsar_lamp"
        put(x, 0, z, b)

# ---- walls with ore seams, windows and a chiseled band --------------------------------------------
ORES = [Z + "cerulite_ore", Z + "lumenite_ore", Z + "starlite_ore"]
for x in range(-21, 22):
    for z in range(-21, 22):
        r = r_of(x, z)
        if not 17.6 <= r <= 20.6:
            continue
        ang = (math.degrees(math.atan2(z, x)) + 360) % 360
        entrance = z > 0 and abs(x) <= 2
        for y in range(1, 8):
            if entrance and y <= 4:
                continue
            b = Z + "cerulean_stone_bricks"
            if y == 4: b = Z + "chiseled_cerulean_stone"
            if y == 7: b = Z + "polished_black_cerulean_stone_bricks"
            if y in (2, 3, 5, 6) and rng.random() < 0.07: b = rng.choice(ORES)
            # windows every 45 degrees (offset from the pillars), crystal glass outside, tinted inside
            if y in (5, 6) and (ang % 45) < 6 and r >= 18.6:
                b = Z + "crystal_glass" if r >= 19.6 else "minecraft:tinted_glass"
            put(x, y, z, b)

# raised inner walkway step around the wall
for x in range(-18, 19):
    for z in range(-18, 19):
        if 16.6 < r_of(x, z) < 17.6 and not (z > 0 and abs(x) <= 2):
            put(x, 1, z, Z + "polished_black_cerulean_stone_bricks")

# ---- entrance (south): gate frame arch, pylons, steps, Concord machinery ----------------------------
for y in range(1, 6):
    for x in (-3, 3):
        for z in range(17, 22):
            put(x, y, z, Z + "cerulite_gate_frame")
for x in range(-3, 4):
    for z in range(17, 22):
        put(x, 5, z, Z + "cerulite_gate_frame")
for x in (-4, 4):
    put(x, 1, 22, Z + "gate_pylon"); put(x, 2, 22, Z + "gate_pylon"); put(x, 3, 22, Z + "spectral_lantern")
    put(x, 1, 21, Z + "cyrrium_casing"); put(x, 2, 21, Z + "cyrrium_casing")
for x in range(-2, 3):
    put(x, 0, 22, Z + "polished_black_cerulean_stone_bricks")
    put(x, 0, 23, Z + "cerulean_stone_brick_slab")

# ---- central dais: the Sentinel's proving stone ------------------------------------------------------
for x in range(-5, 6):
    for z in range(-5, 6):
        r = r_of(x, z)
        if r <= 4.6: put(x, 1, z, Z + "polished_black_prismstone")
        if r <= 3.3: put(x, 2, z, Z + "polished_prismstone")
        if r <= 1.5: put(x, 3, z, Z + "chiseled_prismstone")
put(0, 3, 0, Z + "cerulite_block")
put(0, 4, 0, Z + "crystal_glass")
for x, z in ((4, 0), (-4, 0), (0, 4), (0, -4)):
    put(x, 2, z, Z + "prism_cluster")
for x, z in ((3, 3), (-3, 3), (3, -3), (-3, -3)):
    put(x, 2, z, "minecraft:amethyst_cluster")

# ---- 8 crystal pillars with lenses aimed at the dais -------------------------------------------------
tops = []
for k in range(8):
    a = math.radians(22.5 + 45 * k)
    cx, cz = round(14 * math.cos(a)), round(14 * math.sin(a))
    tops.append((cx, cz))
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            for y in range(1, 10):
                b = Z + "polished_black_prismstone_bricks"
                if y in (1, 9): b = Z + "chiseled_polished_black_prismstone"
                if y == 5: b = Z + "cerulite_block"
                if y == 7 and dx == 0 and dz == 0: b = "minecraft:sea_lantern"
                put(cx + dx, y, cz + dz, b)
    put(cx, 10, cz, Z + "crystal_glass")
    put(cx, 11, cz, Z + "prism_cluster")
    # lens on the inner face, facing the centre
    ix, iz = cx - round(math.cos(a) * 2), cz - round(math.sin(a) * 2)
    put(ix, 6, iz, Z + "gate_lens_housing")

# ---- dome: 8 ribs from the pillar tops up to a crystal oculus ---------------------------------------
for cx, cz in tops:
    for i in range(0, 41):
        t = i / 40
        x, z = round(cx * (1 - t * 0.82)), round(cz * (1 - t * 0.82))
        y = round(10 + 9 * math.sin(t * math.pi / 2))
        if (x, y, z) not in [(cx, 10, cz), (cx, 11, cz)]:
            put(x, y, z, Z + "polished_black_cerulean_stone_bricks")
for x in range(-4, 5):
    for z in range(-4, 5):
        r = r_of(x, z)
        if 2.4 <= r <= 3.6: put(x, 19, z, Z + "crystal_glass")
        if r < 2.4: put(x, 20, z, Z + "crystal_glass")
put(0, 21, 0, Z + "cerulite_block")
for y in range(15, 20):
    put(0, y, 0, "minecraft:chain")
put(0, 14, 0, "minecraft:lantern[hanging=true]")

# ---- outside: azure moss and stray crystal growth ----------------------------------------------------
for _ in range(140):
    x, z = rng.randint(-23, 23), rng.randint(-23, 23)
    if 20.8 <= r_of(x, z) <= 23.4:
        put(x, 0, z, Z + "azure_moss")
        if rng.random() < 0.18:
            put(x, 1, z, rng.choice([Z + "prism_cluster", Z + "cerulite_cluster", "minecraft:small_amethyst_bud"]))

# ---- commands: clear the box, then fill runs along x ------------------------------------------------
cmds = [f"fill -23 {Y0 + 1} -23 23 {Y0 + 21} 23 minecraft:air", f"fill -23 {Y0} -23 23 {Y0} 23 minecraft:grass_block"]
by_row = {}
for (x, y, z), b in B.items():
    by_row.setdefault((y, z), []).append((x, b))
for (y, z), cells in sorted(by_row.items()):
    cells.sort()
    i = 0
    while i < len(cells):
        x0, b = cells[i]
        j = i
        while j + 1 < len(cells) and cells[j + 1][0] == cells[j][0] + 1 and cells[j + 1][1] == b:
            j += 1
        x1 = cells[j][0]
        cmds.append(f"setblock {x0} {y} {z} {b}" if x0 == x1 else f"fill {x0} {y} {z} {x1} {y} {z} {b}")
        i = j + 1
open("C:/zt-tmp/arena_commands.txt", "w", encoding="utf-8").write("\n".join(cmds) + "\n")
used = {}
for b in B.values():
    used[b] = used.get(b, 0) + 1
print(f"blocks placed: {len(B)}  commands: {len(cmds)}  bounds y {min(k[1] for k in B)}..{max(k[1] for k in B)}")
print("block types:", len(used))
for b, n in sorted(used.items(), key=lambda kv: -kv[1]):
    print(f"  {n:5d}  {b}")
