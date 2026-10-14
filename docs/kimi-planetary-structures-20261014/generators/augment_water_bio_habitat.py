"""Water Bio Habitat: add the blueprint surface identity above the bunker.

Keeps: underground loot route + chests + drowned spawner.
Adds: crystalline purple spires (west), stepped bio-habitat towers with
glowing windows, centre energy core with conduit down, seabed flora ring.
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

# ---------- purpur spire cluster (west side, blueprint callout) ----------
def cspire(x0, z0, height, radius):
    for y in range(SURF + 1, SURF + 1 + height):
        t = (y - SURF) / height
        r = max(0.4, radius * (1 - t))
        for x in range(x0 - radius - 1, x0 + radius + 2):
            for z in range(z0 - radius - 1, z0 + radius + 2):
                if math.hypot(x - x0, z - z0) <= r:
                    put(x, y, z, M + 'prism_cluster' if (x + y + z) % 5 else A + 'purpur_block')

cspire(8, 18, 22, 3)
cspire(12, 14, 18, 2)
cspire(7, 27, 14, 2)
cspire(13, 22, 10, 1)

# ---------- stepped habitat towers (east side, blueprint callout) ----------
def tower(x0, z0, w, h):
    for y in range(SURF + 1, SURF + 1 + h):
        for x in range(x0, x0 + w):
            for z in range(z0, z0 + w):
                if not (x in (x0, x0 + w - 1) or z in (z0, z0 + w - 1)):
                    continue
                window = (y - SURF) % 3 == 1 and ((x * 5 + z * 3 + y) % 4 == 0)
                put(x, y, z, A + 'sea_lantern' if window else
                    (M + 'abyssal_stone_bricks' if (y + x) % 7 else A + 'dark_prismarine'))
    # stepped cap
    for x in range(x0 + 1, x0 + w - 1):
        for z in range(z0 + 1, z0 + w - 1):
            put(x, SURF + 1 + h, z, M + 'abyssal_stone_bricks')
    put(x0 + w // 2, SURF + 2 + h, z0 + w // 2, A + 'sea_lantern')

tower(31, 12, 7, 12)
tower(36, 22, 5, 15)
tower(28, 31, 5, 8)

# terraces between towers with teal flora
for x in range(30, 41):
    for z in range(15, 37):
        if (x + z) % 2 == 0:
            put(x, SURF + 1, z, M + 'tidesand')
        if (x * 3 + z) % 7 == 0:
            put(x, SURF + 1, z, M + 'azure_coral_bush')
        elif (x + z * 2) % 9 == 0:
            put(x, SURF + 1, z, M + 'solvane_glow_shrub')

# ---------- energy core (centre, orange glow + conduit legs) ----------
for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
        put(x, SURF + 1, z, A + 'magma_block' if (x + z) % 3 else M + 'budding_prism_crystal')
put(cx, SURF + 2, cz, M + 'fusion_lamp')
for dx, dz in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
    put(cx + dx, SURF + 2, cz + dz, M + 'solvane_glow_flower')
# conduit down-leg into the bunker central route (blueprint: conduit vertical)
for y in range(SURF - 2, SURF + 1):
    put(cx, y, cz, M + 'nullifite_energy_conduit')
# surface conduit arms (N/S/E/W)
for d in range(1, 5):
    put(cx + d, SURF + 1, cz, M + 'nullifite_energy_conduit')
    put(cx - d, SURF + 1, cz, M + 'nullifite_energy_conduit')
    put(cx, SURF + 1, cz + d, M + 'nullifite_energy_conduit')
    put(cx, SURF + 1, cz - d, M + 'nullifite_energy_conduit')
# vanilla conduit accent above the core
put(cx, SURF + 3, cz, A + 'conduit')

# ---------- seabed flora ring around the rim ----------
for i, (x, z) in enumerate([(6, 36), (10, 44), (41, 7), (36, 42), (17, 5), (42, 26), (5, 9), (24, 43), (38, 37), (12, 39)]):
    put(x, SURF + 1, z, A + 'seagrass' if i % 2 else A + 'kelp')

augment('water_bio_habitat', ADD)
