"""Concord Vault room 3/10: Starlight Pool (doors N, S). Usage: python3 room_starlight_pool.py <out_dir>"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from room_kit import Room, Z, sheet

OUT = sys.argv[1]
r = Room('NS', seed=33)
P = lambda n, **k: Z + n + ('[' + ','.join(f'{a}={b}' for a, b in k.items()) + ']' if k else '')
BB, BRK, CRK, CHIS = P('polished_black_cerulean_stone_bricks'), P('cerulean_stone_bricks'), P('cracked_cerulean_stone_bricks'), P('chiseled_cerulean_stone')
CBLK, POL, SMOOTH, SHELL = P('chiseled_polished_black_cerulean_stone'), P('polished_cerulean_stone'), P('smooth_cerulean_stone'), P('cerulean_geode_shell')
RIM = P('polished_cerulean_stone_slab', type='bottom', waterlogged='false')
STAR = P('liquid_starlight', level='0')
LAMP, PULSAR, GLASS = P('spectral_lantern'), P('pulsar_lamp'), P('crystal_glass')
BUD = lambda size, f='up': P(f'{size}_cerulite_bud', facing=f, waterlogged='false')
d = lambda x, z: math.hypot(x - 8, z - 8)
BRIDGE = lambda x, z: 7 <= x <= 9 and (z <= 5 or z >= 11)          # north and south bridges to the island

# ---------------------------------------------------------------- shell
for x in range(17):
    for z in range(17):
        edge = x in (0, 16) or z in (0, 16)
        r.put(x, 0, z, BB if edge else POL)
        if edge:
            for y in range(1, 8): r.put(x, y, z, BB if y == 1 else CHIS if y == 7 else (CRK if r.rng.random() < .12 else BRK))
for x, z in ((0, 0), (0, 16), (16, 0), (16, 16)):
    for y in range(1, 8): r.put(x, y, z, CBLK)
r.open_doors()
for cells in (lambda i: (i, 0), lambda i: (i, 16)):
    for i in (5, 11):
        for y in range(1, 7): r.put(cells(i)[0], y, cells(i)[1], CBLK)
    for i in range(6, 11): r.put(cells(i)[0], 6, cells(i)[1], BB)
    r.put(cells(8)[0], 6, cells(8)[1], P('chiseled_polished_black_cerulean_stone'))

# ---------------------------------------------------------------- the ring pool: a raised basin around the island
#   island   d <= 2.6   (floor level, black medallion; the Key Altar goes here)
#   inner rim 2.6-3.6  bottom slabs at y1
#   pool     3.6-5.7   Liquid Starlight at y1 over a glowing geode-shell bed (lamps under the fluid)
#   outer rim 5.7-6.7  bottom slabs at y1
for x in range(1, 16):
    for z in range(1, 16):
        dd = d(x, z)
        if dd <= 2.6:
            r.put(x, 0, z, P('polished_black_cerulean_stone'))
        elif dd <= 3.6 or 5.7 < dd <= 6.7:
            r.put(x, 0, z, SMOOTH); r.put(x, 1, z, RIM)
        elif dd <= 5.7:
            r.put(x, 0, z, PULSAR if (x + 2 * z) % 5 == 0 else SHELL); r.put(x, 1, z, STAR)
        elif (x + z) % 2 == 0: r.put(x, 0, z, SMOOTH)                          # checkered outer walkway
        if BRIDGE(x, z) and 2.6 < dd <= 6.7:
            r.put(x, 0, z, SMOOTH); r.put(x, 1, z, P('polished_black_cerulean_stone_slab', type='bottom', waterlogged='false'))
r.put(8, 0, 8, P('chiseled_polished_black_cerulean_stone'))
# medium buds on the island's four outer points, facing up (the 3 x 3 centre stays clear)
for x, z in ((6, 8), (10, 8), (8, 6), (8, 10)):
    if (x, z) not in {(7, 7)}: r.put(x, 1, z, BUD('medium'))
for x, z in ((8, 6), (8, 10)): r.put(x, 1, z, 'minecraft:air')                 # keep the bridge ends clear

# ---------------------------------------------------------------- the rare chest rests on the pool bed, under the starlight
r.chest(13, 0, 8, 'west', 'rare', 'Sunken offering (under the fluid)')

# ---------------------------------------------------------------- colonnade: four black pillars with crystal crowns at the diagonals
for x, z in ((3, 3), (13, 3), (3, 13), (13, 13)):
    for y in range(1, 7): r.put(x, y, z, BB if y < 6 else CBLK)
    r.put(x, 7, z, LAMP)
    for (dx, dz), f in (((1, 0), 'east'), ((-1, 0), 'west'), ((0, 1), 'south'), ((0, -1), 'north')):
        if 1 <= x + dx <= 15 and 1 <= z + dz <= 15 and d(x + dx, z + dz) > 6.7: r.put(x + dx, 1, z + dz, BUD('small', f))
# east and west walls: starlight "spouts" (carved heads) over benches
for wx, f, bf in ((16, 'west', 'east'), (0, 'east', 'west')):
    sx = 15 if wx == 16 else 1
    r.put(wx, 4, 8, PULSAR); r.put(wx, 5, 8, CBLK); r.put(wx, 3, 8, CBLK)
    r.put(sx, 4, 8, P('polished_black_cerulean_stone_stairs', facing=bf, half='top', shape='straight'))
    for z in (6, 7, 9, 10): r.put(sx, 1, z, P('polished_cerulean_stone_stairs', facing=bf, half='bottom', shape='straight'))
    r.put(sx, 1, 8, P('polished_cerulean_stone_slab', type='bottom', waterlogged='false'))

# ---------------------------------------------------------------- ceiling: a star map of lanterns around a crystal oculus over the island
for x in range(1, 16):
    for z in range(1, 16):
        dd = d(x, z)
        r.put(x, 8, z, GLASS if dd <= 2.2 else CBLK if 2.2 < dd <= 3.2 else P('cerulean_stone'))
for x, z in ((2, 6), (5, 2), (11, 2), (14, 6), (14, 10), (11, 14), (5, 14), (2, 10), (6, 5), (10, 11), (4, 9), (12, 7)):
    r.put(x, 8, z, LAMP)
r.put(8, 8, 8, LAMP)

n = r.save(f'{OUT}/starlight_pool.nbt')
meta = {
 'title': 'Concord Vault · Room 3 · Starlight Pool',
 'subtitle': '17 x 9 x 17 · doors north and south · 1 rare chest (on the pool bed) · can hold a Key Altar · template rooms/starlight_pool.nbt',
 'story': ('Liquid Starlight seeps through Cerulon\'s crystal caves, and the Concord caught it here in a ring basin around a stone '
           'island. They harvested it for their growth chambers and, the old logs say, came here to think. The ceiling is a star map: '
           'the lanterns match the sky over the Quiet Mines. An offering still rests on the bed of the pool, under the glowing fluid.'),
 'sections': [
  ('Zones', ['Island (centre, floor level): black stone with the chiseled medallion where the Key Altar appears; '
             'medium buds on its east and west points.',
             'Ring pool: Liquid Starlight at y 1, held between two rims of bottom slabs, over a geode-shell bed with pulsar lamps '
             'set in it, so the pool glows from below.',
             'Bridges: black slab walkways cross the pool from the north and south doors straight to the island.',
             'Outer walkway: checkered polished and smooth stone, with four black pillars at the diagonals, each crowned with a '
             'lantern and ringed by small buds.',
             'East and west walls: a carved "spout" with a pulsar lamp over a stone bench.',
             'Ceiling: a crystal-glass oculus over the island, a black ring around it, and lanterns placed like a star map.']),
  ('Loot', ['Sunken offering (13, 0, 8), faces west: chests/concord_vault/rare. It sits on the pool bed, so the fluid is right on '
            'top of it; players reach it from the outer rim or by wading in.',
            'Wading in the Liquid Starlight gives Slow Falling and Night Vision, a little reward for exploring.']),
  ('Connectors', ['North door x 6-10, y 1-5 at z 0; jigsaw (8, 1, 0) facing north.',
                  'South door x 6-10, y 1-5 at z 16; jigsaw (8, 1, 16) facing south.',
                  'Jigsaws: name and target zerog_tweaks:door, pool zerog_tweaks:concord_vault/corridors, final state air, joint aligned.']),
  ('Gameplay', ['No spawner, no traps. The pool is the obstacle: only the two bridges reach the island without wading.',
                'When it is a key room, the 3 Prismling guardians fight around a ring; players can hold a bridge as a choke point.',
                'The room is the brightest in the Vault (the pool is light 12), a landmark players will remember.']),
  ('Building it', ['The fluid is held by slabs on both sides and has a solid floor under it, so it cannot leak into the rock or the corridors.',
                   'Place the fluid last, as source blocks (level 0), one cell at a time, after the rims and bridges are in.',
                   'Generator: generators/vault_rooms/room_starlight_pool.py.']),
 ]}
print(n, 'blocks;', sheet(r, meta, f'{OUT}/03_starlight_pool.png'))
for t, ok in r.check(): print('PASS' if ok else 'FAIL', t)
