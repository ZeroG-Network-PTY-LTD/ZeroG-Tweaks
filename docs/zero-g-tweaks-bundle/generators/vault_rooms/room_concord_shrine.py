"""Concord Vault room 10/10: Concord Shrine (doors N, S, E, W). Usage: python3 room_concord_shrine.py <out_dir>"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from room_kit import Room, Z, sheet

OUT = sys.argv[1]
r = Room('NSEW', seed=1010)
P = lambda n, **k: Z + n + ('[' + ','.join(f'{a}={b}' for a, b in k.items()) + ']' if k else '')
BB, BRK, CHIS, CBLK = P('polished_black_cerulean_stone_bricks'), P('cerulean_stone_bricks'), P('chiseled_cerulean_stone'), P('chiseled_polished_black_cerulean_stone')
BLK, POL, SMOOTH = P('polished_black_cerulean_stone'), P('polished_cerulean_stone'), P('smooth_cerulean_stone')
LAMP, PULSAR, GLASS, CHAIN = P('spectral_lantern'), P('pulsar_lamp'), P('crystal_glass'), 'minecraft:chain[axis=y,waterlogged=false]'
BUD = lambda size, f='up': P(f'{size}_cerulite_bud', facing=f, waterlogged='false')
BSTAIR = lambda f, h='bottom': P('polished_black_cerulean_stone_brick_stairs', facing=f, half=h, shape='straight', waterlogged='false')
PSTAIR = lambda f, h='bottom': P('polished_cerulean_stone_stairs', facing=f, half=h, shape='straight', waterlogged='false')
d = lambda x, z: math.hypot(x - 8, z - 8)
aisle = lambda x, z: 6 <= x <= 10 or 6 <= z <= 10

# ---------------------------------------------------------------- shell: a solemn hall, all four doors framed alike
for x in range(17):
    for z in range(17):
        edge = x in (0, 16) or z in (0, 16)
        r.put(x, 0, z, BB if edge else (POL if aisle(x, z) else SMOOTH))
        r.put(x, 8, z, BB)
        if edge:
            for y in range(1, 8): r.put(x, y, z, BB if y in (1, 7) else BRK)
r.open_doors()
for cells in (lambda i: (i, 0), lambda i: (i, 16), lambda i: (0, i), lambda i: (16, i)):
    for i in (5, 11):
        for y in range(1, 7): r.put(cells(i)[0], y, cells(i)[1], CBLK)
    for i in range(6, 11): r.put(cells(i)[0], 6, cells(i)[1], BB)
    r.put(cells(8)[0], 6, cells(8)[1], CHIS)
# aisle borders and the lamp ring around the plinth
for x in range(1, 16):
    for z in range(1, 16):
        if aisle(x, z) and (x in (6, 10) and not 6 <= z <= 10 or z in (6, 10) and not 6 <= x <= 10): r.put(x, 0, z, BLK)
        if 2.6 <= d(x, z) <= 3.4: r.put(x, 0, z, PULSAR if (x + z) % 2 == 0 else BLK)
for x in range(7, 10):
    for z in range(7, 10): r.put(x, 0, z, BLK)
r.put(8, 0, 8, CBLK)
# vaulted ceiling: stepped ribs along both aisles, a ring of hanging lanterns around the centre
for i in range(1, 16):
    for (x, z, f) in ((5, i, 'east'), (11, i, 'west'), (i, 5, 'south'), (i, 11, 'north')):
        if r.get(x, 7, z) == 'minecraft:air': r.put(x, 7, z, BSTAIR(f, 'top'))
for x, z in ((8, 5), (8, 11), (5, 8), (11, 8)):
    r.put(x, 7, z, BB); r.put(x, 6, z, CHAIN); r.put(x, 5, z, LAMP)
r.put(8, 8, 8, GLASS)

# ---------------------------------------------------------------- four black pillars with crystal crowns, at the corners of the crossing
for x, z in ((5, 5), (11, 5), (5, 11), (11, 11)):
    for y in range(1, 6): r.put(x, y, z, BB)
    r.put(x, 1, z, CBLK); r.put(x, 6, z, LAMP); r.put(x, 7, z, BUD('large'))
    for (dx, dz), f in (((1, 0), 'east'), ((-1, 0), 'west'), ((0, 1), 'south'), ((0, -1), 'north')):
        if not aisle(x + dx, z + dz): r.put(x + dx, 5, z + dz, BUD('medium', f))       # buds sprouting below the lamp

# ---------------------------------------------------------------- corner chapels
def kneeler(x, z, f):
    r.put(x, 1, z, PSTAIR(f))
# NW: the wall of names (engraved stones), a kneeling bench, a lamp behind glass
for x in range(1, 5):
    for y in range(2, 6): r.put(x, y, 0, CHIS)
for z in range(1, 5):
    for y in range(2, 6): r.put(0, y, z, CHIS)
r.put(0, 3, 2, PULSAR); r.put(2, 3, 0, PULSAR)
kneeler(2, 3, 'south'); kneeler(3, 2, 'east'); r.notes[(2, 1, 3)] = 'kneeler'
# NE: the offering plinth with the rare chest
r.put(14, 1, 2, CBLK); r.put(13, 1, 2, BSTAIR('west')); r.put(15, 1, 2, BSTAIR('east'))
r.chest(14, 2, 2, 'south', 'rare', 'Offering (on the plinth)')
for x in (13, 15): r.put(x, 2, 2, BUD('small'))
r.put(14, 4, 0, PULSAR); r.put(14, 5, 0, CBLK); r.put(16, 4, 2, PULSAR)
kneeler(14, 4, 'north')
# SW: a small Sentinel effigy (crystal core, black shell, bud shards)
r.put(2, 1, 14, BB); r.put(2, 2, 14, GLASS); r.put(2, 3, 14, BB); r.put(2, 4, 14, BUD('large'))
for (x, z, f) in ((1, 14, 'west'), (3, 14, 'east'), (2, 13, 'north'), (2, 15, 'south')): r.put(x, 2, z, BUD('medium', f))
r.put(2, 1, 13, 'minecraft:air'); r.notes[(2, 2, 14)] = 'Sentinel effigy'
r.put(0, 4, 14, PULSAR); kneeler(4, 12, 'west')
# SE: a relief of the gate (a ring of crystal glass set in the walls) with a lamp at its heart
for (y, z) in ((2, 13), (3, 12), (4, 12), (5, 13), (5, 14), (4, 15), (3, 15), (2, 14)): r.put(16, y, z, GLASS)
r.put(16, 3, 13, BB); r.put(16, 4, 13, BB); r.put(16, 3, 14, PULSAR); r.put(16, 4, 14, BB)
for (x, y) in ((13, 2), (12, 3), (12, 4), (13, 5), (14, 5), (15, 4), (15, 3), (14, 2)): r.put(x, y, 16, GLASS)
r.put(13, 3, 16, BB); r.put(14, 4, 16, PULSAR); r.put(13, 4, 16, BB); r.put(14, 3, 16, BB)
kneeler(13, 13, 'east'); kneeler(13, 14, 'east')

n = r.save(f'{OUT}/concord_shrine.nbt')
meta = {
 'title': 'Concord Vault · Room 10 · Concord Shrine',
 'subtitle': '17 x 9 x 17 · doors north, south, east and west · 1 rare chest · can hold a Key Altar · template rooms/concord_shrine.nbt',
 'story': ('Where the tunnels cross, the Concord built a shrine. The four keys were blessed on the plinth at its heart before they '
           'were hidden, which is why a Key Altar looks at home here. Four black pillars hold up a vaulted ceiling, each crowned with '
           'crystal; the corners are small chapels: a wall of names for those who stayed behind, a crystal effigy of the Sentinel, '
           'a relief of the gate they hoped to open, and an offering that no one came back for.'),
 'cut_top': 7,
 'sections': [
  ('Zones', ['Crossing: polished aisles from all four doors, edged in black, meeting at the medallion where the Key Altar appears, '
             'ringed by pulsar lamps set in the floor.',
             'Pillars: four black pillars at the corners of the crossing, each with a lantern near the top, a large bud crown and '
             'medium buds sprouting toward the chapels.',
             'Ceiling: stepped black ribs over both aisles, a ring of four hanging lanterns around the centre and a crystal pane over the plinth.',
             'North-west chapel: the wall of names (engraved chiseled stone on both walls), two lamps set in the walls, two kneelers.',
             'North-east chapel: a black plinth with stair wings, the rare chest on top, small buds either side, a lamp above.',
             'South-west chapel: a small Sentinel effigy (crystal core in black shell, bud "shards" around it), a lamp and a kneeler.',
             'South-east chapel: a ring of crystal glass set into both walls like the gate, with a pulsar lamp at its heart, and two kneelers.']),
  ('Loot', ['Offering (14, 2, 2) on the plinth, faces south: chests/concord_vault/rare.',
            'The rest is memorial: no barrels, no extra chests, by design. This room is about the story.']),
  ('Connectors', ['North door x 6-10 at z 0; jigsaw (8, 1, 0) facing north.',
                  'South door x 6-10 at z 16; jigsaw (8, 1, 16) facing south.',
                  'West door z 6-10 at x 0; jigsaw (0, 1, 8) facing west.',
                  'East door z 6-10 at x 16; jigsaw (16, 1, 8) facing east.',
                  'All doors 5 x 5 (y 1-5). Jigsaws: name and target zerog_tweaks:door, pool zerog_tweaks:concord_vault/corridors, '
                  'final state air, joint aligned.']),
  ('Gameplay', ['A crossroads: with four doors it often sits in the middle of a branch, so players pass through it more than once.',
                'No spawner, no traps. When it is a key room, the open crossing is a good arena for the 3 Prismling guardians; '
                'the pillars are cover.',
                'The chapels reward a slow look: the names wall and the effigy are worth a screenshot, and the offering is a rare chest.']),
  ('Building it', ['Buds replace the placeholder\'s crystal clusters (clusters drop Cerulite gems).',
                   'The gate relief is crystal glass set into the wall itself, with black bricks and a pulsar lamp inside the ring.',
                   'Generator: generators/vault_rooms/room_concord_shrine.py.']),
 ]}
print(n, 'blocks;', sheet(r, meta, f'{OUT}/10_concord_shrine.png'))
for t, ok in r.check(): print('PASS' if ok else 'FAIL', t)
