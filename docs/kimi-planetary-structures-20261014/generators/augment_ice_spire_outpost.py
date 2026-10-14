"""Ice Spire Outpost: add the blueprint surface identity above the bunker.

Keeps: underground loot route + chests (14,4,14)/(34,4,14) + spawner (18,4,32).
Adds: back-row glacial spires, cryo-core crown (fusion lamp + pods), ice arch
over the courtyard, perimeter walls, flora scatter.
"""
import math
from showcase_augment_lib import augment

A = 'minecraft:'
M = 'zerog_tweaks:'
ADD = []

def put(x, y, z, name):
    ADD.append((x, y, z, name))

# surface heights (max y at each column of the existing bunker, measured)
# The bunker surface sits ~y=12-13 across the disc; everything we add goes on top.
SURF = 13  # baseline surface of the existing showcase

# ---------- back-row glacial spires (blueprint: tall packed cluster, north) ----------
def spire(x0, z0, height, radius):
    for y in range(SURF + 1, SURF + 1 + height):
        t = (y - SURF) / height
        r = max(0.0, radius * (1 - t * 0.85))
        for x in range(x0 - radius - 1, x0 + radius + 2):
            for z in range(z0 - radius - 1, z0 + radius + 2):
                d = math.hypot(x - x0, z - z0)
                if d <= r:
                    put(x, y, z, A + 'packed_ice' if (x + z + y) % 9 == 0 else A + 'blue_ice')

# cluster at the back of the disc (z small = north in the render)
spire(16, 10, 24, 3)
spire(21, 9, 28, 3)
spire(26, 10, 22, 3)
spire(31, 12, 18, 2)
spire(12, 13, 16, 2)
spire(36, 11, 12, 1)

# ---------- cryogenic core chamber crown (center of the disc) ----------
cx = cz = 24
# ring of phantom ice pillars at chamber corners (blueprint: glowing cyan heart)
for dx in (-3, 3):
    for dz in (-3, 3):
        for y in range(SURF + 1, SURF + 5):
            put(cx + dx, y, cz + dz, M + 'phantom_ice')
# fusion lamp heart inside the crown (blueprint callout)
put(cx, SURF + 1, cz, M + 'fusion_lamp')
put(cx, SURF + 2, cz, M + 'crystal_glass')
# cryo pods around the heart (blueprint: cryo pods ring)
put(cx - 2, SURF + 1, cz, M + 'cryo_pod')
put(cx + 2, SURF + 1, cz, M + 'cryo_pod')
put(cx, SURF + 1, cz - 2, M + 'cryo_pod')
put(cx, SURF + 1, cz + 2, M + 'cryo_pod')
# conduit run from the SE rim into the core (blueprint: energy conduit)
for i in range(11):
    x, z = 24 + i, 35 - i
    put(x, SURF, z, M + 'crystal_glass' if i % 2 == 0 else M + 'nullifite_energy_conduit')
# pylon at the SE rim
for y in range(SURF, SURF + 6):
    put(34, y, 26, M + 'chiseled_polished_black_frostrock' if y % 2 else M + 'crystal_glass')
put(34, SURF + 6, 26, M + 'fusion_lamp')

# ---------- perimeter ice arch over the courtyard (blueprint) ----------
# arch spanning the core from west to east
for t in range(25):
    a = math.pi * t / 24.0
    x = int(round(cx + 10 * math.cos(a)))
    y = int(round(SURF + 2 + 9 * math.sin(a)))
    for z in (cz - 1, cz):
        put(x, y, z, A + 'blue_ice')

# ---------- perimeter snow walls (low, broken) ----------
for a in range(0, 360, 3):
    ang = math.radians(a)
    x = int(round(cx + 21.5 * math.cos(ang)))
    z = int(round(cz + 21.5 * math.sin(ang)))
    if (a // 3) % 3 == 0:
        put(x, SURF + 1, z, A + 'snow_block')

# ---------- flora scatter (frost crystals + brine buds) ----------
for i, (x, z) in enumerate([(9, 18), (14, 30), (38, 9), (40, 22), (7, 28), (32, 39), (20, 41), (43, 30), (11, 36), (28, 6), (36, 38), (6, 15)]):
    put(x, SURF + 1, z, M + 'frost_crystal' if i % 3 == 0 else
        (M + 'medium_brine_bud' if i % 3 == 1 else
         {'Name': M + 'small_brine_bud', 'Properties': {'facing': 'up', 'waterlogged': 'false'}}))

augment('ice_spire_outpost', ADD)
