"""Concord Vault room 9/10: Observatory (door N only). Usage: python3 room_observatory.py <out_dir>"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from room_kit import Room, Z, sheet

OUT = sys.argv[1]
r = Room('N', seed=99)
P = lambda n, **k: Z + n + ('[' + ','.join(f'{a}={b}' for a, b in k.items()) + ']' if k else '')
BB, BRK, CHIS, CBLK = P('polished_black_cerulean_stone_bricks'), P('cerulean_stone_bricks'), P('chiseled_cerulean_stone'), P('chiseled_polished_black_cerulean_stone')
BLK, POL, SMOOTH = P('polished_black_cerulean_stone'), P('polished_cerulean_stone'), P('smooth_cerulean_stone')
LAMP, PULSAR, GLASS, CHAIN = P('spectral_lantern'), P('pulsar_lamp'), P('crystal_glass'), 'minecraft:chain[axis=y,waterlogged=false]'
BSTAIR = lambda f, h='bottom': P('polished_black_cerulean_stone_brick_stairs', facing=f, half=h, shape='straight', waterlogged='false')
PSTAIR = lambda f, h='bottom': P('polished_cerulean_stone_stairs', facing=f, half=h, shape='straight', waterlogged='false')
d = lambda x, z: math.hypot(x - 8, z - 8)

# ---------------------------------------------------------------- shell: a dark planetarium
for x in range(17):
    for z in range(17):
        edge = x in (0, 16) or z in (0, 16)
        r.put(x, 0, z, BB if edge else BLK)
        r.put(x, 8, z, BB)
        if edge:
            for y in range(1, 8): r.put(x, y, z, BB if y in (1, 7) else BRK)
r.open_doors()
for i in (5, 11):
    for y in range(1, 7): r.put(i, y, 0, CBLK)
for i in range(6, 11): r.put(i, 6, 0, BB)
r.put(8, 6, 0, CBLK)
# rounded ceiling: the corners step down so the room reads as a dome; crystal oculus in the middle
for x in range(1, 16):
    for z in range(1, 16):
        dd = d(x, z)
        if dd >= 8.2: r.put(x, 7, z, BB); r.put(x, 6, z, BSTAIR('north' if z < 8 else 'south', 'top') if abs(z - 8) > abs(x - 8) else BSTAIR('west' if x < 8 else 'east', 'top'))
        elif dd >= 7.0: r.put(x, 7, z, BSTAIR('north' if z < 8 else 'south', 'top') if abs(z - 8) >= abs(x - 8) else BSTAIR('west' if x < 8 else 'east', 'top'))
        if dd <= 2.3: r.put(x, 8, z, GLASS)
        elif dd <= 3.2: r.put(x, 8, z, CBLK)
# night-sky wall panels (east, west and south walls) with lantern constellations
for z in range(2, 15):
    for y in range(2, 6): r.put(0, y, z, BLK); r.put(16, y, z, BLK)
for x in range(2, 15):
    for y in range(4, 7): r.put(x, y, 16, BLK)
for (y, z) in ((5, 3), (4, 5), (5, 6), (3, 8), (4, 11), (2, 12), (5, 13)): r.put(0, y, z, LAMP)          # "the Miner" (west)
for (y, z) in ((3, 3), (4, 4), (2, 6), (5, 9), (4, 10), (3, 12)): r.put(16, y, z, LAMP)                 # "the Gate" (east)
for (x, y) in ((3, 5), (5, 6), (7, 4), (11, 6), (13, 5)): r.put(x, y, 16, LAMP)                          # over the telescope

# ---------------------------------------------------------------- floor: star-chart ring of pulsar lamps around the medallion
for x in range(1, 16):
    for z in range(1, 12):
        dd = d(x, z)
        if 4.5 <= dd <= 5.5: r.put(x, 0, z, PULSAR if (x + z) % 2 == 0 else SMOOTH)
        elif 2.5 <= dd < 4.5: r.put(x, 0, z, POL)
for x in range(7, 10):
    for z in range(7, 10): r.put(x, 0, z, BLK)
r.put(8, 0, 8, CBLK)

# ---------------------------------------------------------------- hanging orrery (all above head height; the 3 x 3 centre stays clear up to y 3)
r.put(8, 7, 8, CHAIN); r.put(8, 6, 8, CHAIN); r.put(8, 5, 8, PULSAR); r.notes[(8, 5, 8)] = 'orrery sun'
for (x, z, y) in ((11, 8, 5), (11, 10, 4), (5, 7, 5), (6, 5, 6), (10, 4, 4)):
    for yy in range(y + 1, 8):
        if r.get(x, yy, z) == 'minecraft:air': r.put(x, yy, z, CHAIN)
    r.put(x, y, z, LAMP)

# ---------------------------------------------------------------- seating facing the telescope (north side, either side of the door path)
for z in (2, 3):
    for x in list(range(2, 6)) + list(range(11, 15)):
        r.put(x, 1, z, PSTAIR('north'))

# ---------------------------------------------------------------- telescope platform (south): 2 high, steps at the front, railing
for x in range(4, 13):
    for z in range(12, 16):
        r.put(x, 1, z, BB); r.put(x, 2, z, BLK)
for x in range(7, 10):
    r.put(x, 1, 11, PSTAIR('south')); r.put(x, 2, 12, PSTAIR('south'))
for x in list(range(4, 7)) + list(range(10, 13)): r.put(x, 3, 12, P('polished_black_cerulean_stone_wall'))
# the telescope: tripod, eyepiece, a stepped tube rising north toward the oculus, crystal lens at the top
r.put(8, 3, 14, P('shardwood_fence')); r.put(7, 3, 15, P('shardwood_fence')); r.put(9, 3, 15, P('shardwood_fence'))
r.put(8, 4, 15, P('smooth_cerulean_stone_slab', type='bottom', waterlogged='false')); r.notes[(8, 4, 15)] = 'eyepiece'
r.put(8, 4, 14, BB); r.put(8, 5, 14, BB); r.put(8, 5, 13, BSTAIR('north', 'top')); r.put(8, 6, 13, BB)
r.put(8, 6, 12, BSTAIR('north', 'top')); r.put(8, 7, 12, BB); r.put(8, 7, 11, GLASS); r.notes[(8, 7, 11)] = 'lens'
# astronomer's corner: desk, stool, the chest
r.put(5, 3, 14, 'minecraft:cartography_table'); r.put(6, 3, 14, P('shardwood_stairs', facing='west', half='bottom', shape='straight', waterlogged='false'))
r.chest(11, 3, 14, 'west', 'rare', "Astronomer's chest (platform)")
r.put(12, 3, 15, LAMP); r.put(4, 3, 15, LAMP)

n = r.save(f'{OUT}/observatory.nbt')
meta = {
 'title': 'Concord Vault · Room 9 · Observatory',
 'subtitle': '17 x 9 x 17 · door north only (a dead end) · 1 rare chest · can hold a Key Altar · template rooms/observatory.nbt',
 'story': ('A planetarium at the end of a tunnel. The Concord could not see the sky from the Vault, so they built it here: '
           'constellations in lanterns on night-black walls, an orrery hanging under a rounded ceiling, a ring of lamps in the floor '
           'and a great telescope aimed at the crystal oculus. It was here they first saw the dark star move. Because it is a dead end, '
           'it is the reward at the end of a long branch, and the astronomer kept the best of what they had.'),
 'cut_top': 7,
 'sections': [
  ('Zones', ['Floor: black stone with a ring of pulsar lamps (alternating with smooth stone) around a polished circle and the '
             'black medallion where the Key Altar appears.',
             'Orrery: a pulsar "sun" hanging over the medallion at y 5 and five lantern "planets" on chains at different heights, '
             'all above y 3 so the altar spot stays clear.',
             'Walls: night-black panels on the east, west and south walls with lantern constellations ("the Miner", "the Gate").',
             'Ceiling: stepped black stairs round off the corners into a dome; a crystal-glass oculus with a black ring in the middle.',
             'Seating: two rows of stone seats either side of the door path, facing the telescope.',
             'Telescope platform (south): 2 high with steps at the front and a low wall railing; a fence tripod, an eyepiece and a '
             'stepped tube rising north to a crystal lens aimed at the oculus.',
             "Astronomer's corner: cartography table, stool, the rare chest, two lamps."]),
  ('Loot', ["Astronomer's chest (11, 3, 14) on the platform, faces west: chests/concord_vault/rare.",
            'Only one door, so the room is always at the end of a branch: the rare chest rewards players who explore all the way.']),
  ('Connectors', ['North door x 6-10, y 1-5 at z 0; jigsaw (8, 1, 0) facing north. No other doors.',
                  'Jigsaw: name and target zerog_tweaks:door, pool zerog_tweaks:concord_vault/corridors, final state air, joint aligned.']),
  ('Gameplay', ['A quiet room: no spawner, no traps.',
                'When it is a key room, it is a dead end: players fight the 3 Prismling guardians with their back to the telescope '
                'platform, and the only way out is the way they came. The platform gives height.',
                'The floor ring and constellations make it the most striking room after the Starlight Pool.']),
  ('Building it', ['Pulsar lamps in the floor are full blocks, so players walk on them.',
                   'The dome is made of polished black brick stairs (top half) on the corner cells; keep them when rebuilding by hand.',
                   'Generator: generators/vault_rooms/room_observatory.py.']),
 ]}
print(n, 'blocks;', sheet(r, meta, f'{OUT}/09_observatory.png'))
for t, ok in r.check(): print('PASS' if ok else 'FAIL', t)
