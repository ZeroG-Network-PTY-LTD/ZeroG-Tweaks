"""Hot Ring Monolith: add the blueprint surface identity above the bunker.

Keeps: underground loot route + chests + magma_cube spawner.
Adds: obsidian tower with two tilted gravity rings, spawning-hive mound with
glowing bulbs, quantum conduit line, sub-drill shafts, lava pools.
"""
import math
from showcase_augment_lib import augment

A = 'minecraft:'
M = 'zerog_tweaks:'
ADD = []

def put(x, y, z, name):
    ADD.append((x, y, z, name))

SURF = 13  # existing bunker surface baseline
cx = cz = 24

# ---------- central void tower (black, blueprint callout) ----------
for y in range(SURF + 1, SURF + 22):
    for dx, dz in ((0, 0), (1, 0), (0, 1), (1, 1)):
        put(cx + dx, y, cz + dz, A + 'obsidian' if (y + dx + dz) % 4 else A + 'crying_obsidian')
# portal glow ring at y=SURF+15 (blueprint: orange glow dots)
cy = SURF + 15
for a in range(16):
    ang = a * math.pi / 8
    x = int(round(cx + 0.5 + 3.6 * math.cos(ang)))
    z = int(round(cz + 0.5 + 3.6 * math.sin(ang)))
    put(x, cy, z, M + 'ember_spinel_block' if a % 2 == 0 else A + 'magma_block')

# ---------- gravity rings (two tilted rings around the tower) ----------
def ring(cxr, cyr, czr, radius, tilt=0.45, every=9):
    pts = set()
    for t in range(720):
        a = math.radians(t / 2)
        x = radius * math.cos(a)
        y = radius * math.sin(a) * math.cos(tilt)
        z = radius * math.sin(a) * math.sin(tilt)
        xi = int(round(cxr + x)); yi = int(round(cyr + y)); zi = int(round(czr + z))
        pts.add((xi, yi, zi, t // 90))
    for xi, yi, zi, q in pts:
        put(xi, yi, zi, A + 'blackstone' if (q % every) else M + 'ember_spinel_block')

ring(cx + 0.5, SURF + 16, cz + 0.5, 7.5, tilt=0.50)
ring(cx + 0.5, SURF + 18, cz + 0.5, 9.5, tilt=-0.35, every=11)

# ---------- spawning hive mound (west of tower, organic with orange bulbs) ----------
hx, hz = 8, 33
for x in range(hx - 4, hx + 5):
    for z in range(hz - 4, hz + 5):
        r = math.hypot(x - hx, z - hz)
        if r > 4.4:
            continue
        hh = int(round(4.4 * (1 - r / 4.4)))
        for y in range(SURF + 1, SURF + 1 + hh):
            put(x, y, z, A + 'crimson_nylium' if (x + y + z) % 3 else M + 'oxide_crust')
# glowing bulbs on stalks (blueprint: orange pods)
for dx, dy, dz in [(-3, 2, 0), (3, 3, 1), (0, 3, -3), (2, 4, 3), (-2, 3, 3), (0, 5, 0), (3, 1, -2)]:
    put(hx + dx, SURF + dy + 4, hz + dz, A + 'shroomlight')

# ---------- quantum conduit run (SE rim → tower) ----------
for i in range(0, 9):
    x, y, z = 33 - i, SURF, 37 - i
    put(x, y, z, A + 'blackstone' if i % 2 == 0 else M + 'nullifite_energy_conduit')
# pylon at the SE corner
px, pz = 33, 38
for y in range(SURF + 1, SURF + 8):
    put(px, y, pz, A + 'blackstone' if y % 2 else A + 'gold_block')
put(px, SURF + 8, pz, M + 'ember_spinel_block')
# down-leg into the tower base
for y in range(SURF - 2, SURF):
    put(cx, y, cz, M + 'nullifite_energy_conduit')

# ---------- sub-drills: 3 vertical shafts with emberite_ore cores ----------
for i, (dx, dz) in enumerate([(6, 6), (37, 6), (6, 40)]):
    put(dx, SURF + 1, dz, M + 'chiseled_mare_basalt')
    put(dx, SURF + 2, dz, M + 'chiseled_mare_basalt')
    for y in range(1, SURF + 1):
        put(dx, y, dz, M + 'emberite_ore' if y % 3 else M + 'emberite_block')
# lava collars at two drill mouths
put(6, SURF + 3, 7, A + 'lava')
put(37, SURF + 3, 7, A + 'lava')

# ---------- basalt bloom scatter ----------
for i, (x, z) in enumerate([(9, 15), (13, 11), (33, 9), (36, 22), (10, 43), (22, 42), (29, 38), (7, 30), (18, 43), (36, 29)]):
    put(x, SURF + 1, z, M + 'basalt_bloom' if i % 2 else M + 'spectral_lantern')

augment('hot_ring_monolith', ADD)
