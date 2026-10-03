"""Concord Vault room 2/10: Crystal Garden (doors N, W). Usage: python3 room_crystal_garden.py <out_dir>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from room_kit import Room, Z, sheet

OUT = sys.argv[1]
r = Room('NW', seed=22)
P = lambda n, **k: Z + n + ('[' + ','.join(f'{a}={b}' for a, b in k.items()) + ']' if k else '')
BB, BRK, CRK, CHIS = P('polished_black_cerulean_stone_bricks'), P('cerulean_stone_bricks'), P('cracked_cerulean_stone_bricks'), P('chiseled_cerulean_stone')
MOSS, SOIL, SHELL = P('azure_moss'), P('cerulean_soil'), P('cerulean_geode_shell')
LEAF = P('shardwood_leaves', distance='1', persistent='true', waterlogged='false')
LOGX, LOGZ, CORNER = P('stripped_shardwood_log', axis='x'), P('stripped_shardwood_log', axis='z'), P('stripped_shardwood_wood', axis='y')
LAMP, CHAIN, GLASS = P('spectral_lantern'), 'minecraft:chain[axis=y,waterlogged=false]', P('crystal_glass')
BUD = lambda size, f='up': P(f'{size}_cerulite_bud', facing=f, waterlogged='false')
WATER = 'minecraft:water[level=0]'

# ---------------------------------------------------------------- shell: walls with moss creeping up from the floor
for x in range(17):
    for z in range(17):
        edge = x in (0, 16) or z in (0, 16)
        r.put(x, 0, z, BB if edge else SOIL)
        r.put(x, 8, z, P('cerulean_stone'))
        if edge:
            for y in range(1, 8):
                b = BB if y == 1 else CHIS if y == 7 else (CRK if r.rng.random() < .14 else BRK)
                if 2 <= y <= 3 and r.rng.random() < .35 - .12 * (y - 2): b = MOSS          # moss creeping up the walls
                r.put(x, y, z, b)
for x, z in ((0, 0), (0, 16), (16, 0), (16, 16)):
    for y in range(1, 8): r.put(x, y, z, P('stripped_shardwood_log', axis='y'))
r.open_doors()
for d, cells in (('N', lambda i: (i, 0)), ('W', lambda i: (0, i))):
    for i in (5, 11):
        for y in range(1, 7): r.put(cells(i)[0], y, cells(i)[1], BB)
    for i in range(6, 11): r.put(cells(i)[0], 6, cells(i)[1], BB)
    r.put(cells(8)[0], 6, cells(8)[1], P('chiseled_polished_black_cerulean_stone'))

# ---------------------------------------------------------------- crystal ceiling: a glass lattice with lanterns, framed in Shardwood
for x in range(1, 16):
    for z in range(1, 16):
        if 3 <= x <= 13 and 3 <= z <= 13:
            r.put(x, 8, z, LOGX if z in (3, 8, 13) else LOGZ if x in (3, 8, 13) else GLASS)
for x in (3, 8, 13):
    for z in (3, 8, 13): r.put(x, 8, z, CORNER)
for x, z in ((5, 5), (11, 5), (5, 11), (11, 11)): r.put(x, 8, z, LAMP)                 # lanterns set in the glass

# ---------------------------------------------------------------- paths: from each door to a round plaza, Key Altar medallion in the middle
for z in range(1, 11):
    for x in range(6, 11): r.put(x, 0, z, P('smooth_cerulean_stone') if x in (6, 10) else P('polished_cerulean_stone'))
for x in range(1, 11):
    for z in range(6, 11): r.put(x, 0, z, P('smooth_cerulean_stone') if z in (6, 10) else P('polished_cerulean_stone'))
for x in range(5, 12):
    for z in range(5, 12):
        if (x - 8) ** 2 + (z - 8) ** 2 <= 10: r.put(x, 0, z, P('polished_cerulean_stone'))
for x in range(7, 10):
    for z in range(7, 10): r.put(x, 0, z, P('polished_black_cerulean_stone'))
r.put(8, 0, 8, P('chiseled_polished_black_cerulean_stone'))

# ---------------------------------------------------------------- raised planter beds (log rims, moss, Starblooms, leafy shrubs)
def bed(x0, z0, x1, z1, shrub):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            rim = x in (x0, x1) or z in (z0, z1)
            corner = x in (x0, x1) and z in (z0, z1)
            if rim: r.put(x, 1, z, CORNER if corner else (LOGX if z in (z0, z1) else LOGZ))
            else:
                r.put(x, 1, z, MOSS)
                if (x, z) == shrub: r.put(x, 2, z, LEAF); r.put(x, 3, z, LEAF)
                elif r.rng.random() < .7: r.put(x, 2, z, P('starbloom'))
bed(1, 1, 5, 5, (3, 3)); bed(11, 1, 15, 5, (13, 3)); bed(1, 11, 5, 15, (3, 13))
# lanterns hanging over the beds
for x, z in ((3, 3), (13, 3), (3, 13)):
    for y in range(6, 8): r.put(x, y, z, CHAIN)
    r.put(x, 5, z, LAMP)

# ---------------------------------------------------------------- trellis arches over both paths, grown over with leaves
for (a, b), (c, d) in (((6, 3), (10, 3)), ((3, 6), (3, 10))):
    for y in range(1, 4): r.put(a, y, b, P('shardwood_fence')); r.put(c, y, d, P('shardwood_fence'))
    if b == d:
        for x in range(a, c + 1): r.put(x, 4, b, LEAF)
    else:
        for z in range(b, d + 1): r.put(a, 4, z, LEAF)

# ---------------------------------------------------------------- south-east: still pond ringed by geode shell and growing buds
for x in range(11, 16):
    for z in range(11, 16):
        r.put(x, 0, z, WATER if (12 <= x <= 14 and 12 <= z <= 14) else SHELL)
for (x, z), size in (((11, 11), 'large'), ((15, 12), 'medium'), ((11, 14), 'small'), ((13, 15), 'large'), ((15, 15), 'medium'), ((12, 11), 'small')):
    r.put(x, 1, z, BUD(size))
for y in range(6, 8): r.put(13, y, 13, CHAIN)
r.put(13, 5, 13, LAMP)

# ---------------------------------------------------------------- south: crystal grotto in the wall, with a bench facing it
for x in range(5, 12):
    for y in range(1, 6): r.put(x, y, 16, SHELL)
for (x, y), size in (((6, 2), 'large'), ((8, 3), 'large'), ((10, 2), 'medium'), ((7, 4), 'small'), ((9, 1), 'medium'), ((11, 3), 'small')):
    r.put(x, y, 15, BUD(size, 'north'))
for x in (7, 9): r.put(x, 1, 12, P('shardwood_stairs', facing='north', half='bottom', shape='straight'))
r.put(8, 1, 12, P('shardwood_slab', type='bottom'))
for x in range(6, 11):
    for z in range(11, 15): r.put(x, 0, z, P('polished_cerulean_stone') if z == 11 else P('crystal_sand'))

# ---------------------------------------------------------------- east wall: the gardener's bench, with the chest
r.put(15, 1, 6, 'minecraft:composter[level=4]')
r.put(15, 1, 7, 'minecraft:barrel[facing=up,open=false]'); r.put(15, 2, 7, P('potted_starbloom'))
r.chest(15, 1, 8, 'west', 'uncommon', "Gardener's chest")
r.put(15, 1, 9, P('shardwood_stairs', facing='east', half='top', shape='straight')); r.put(15, 2, 9, P('potted_starbloom'))
r.put(15, 1, 10, 'minecraft:barrel[facing=up,open=false]')
for z in range(6, 11): r.put(15, 4, z, P('shardwood_slab', type='top'))               # shelf over the bench
r.put(15, 5, 7, P('potted_starbloom')); r.put(15, 5, 9, P('potted_starbloom'))
r.put(16, 3, 8, P('pulsar_lamp'))                                                       # lamp set in the wall over the bench
for x in range(11, 16):
    for z in range(6, 11): r.put(x, 0, z, P('polished_cerulean_stone') if x == 15 else MOSS if r.rng.random() < .6 else P('crystal_sand'))

# ---------------------------------------------------------------- north-east bed's corner: a crystal bleed through the wall
for (x, y, z) in ((16, 2, 2), (16, 3, 2), (16, 2, 3), (15, 6, 0), (14, 6, 0)): r.put(x, y, z, SHELL)
r.put(15, 3, 2, BUD('medium', 'west')); r.put(15, 2, 3, BUD('small', 'west'))

n = r.save(f'{OUT}/crystal_garden.nbt')
meta = {
 'title': 'Concord Vault · Room 2 · Crystal Garden',
 'subtitle': '17 x 9 x 17 · doors north and west · 1 uncommon chest · can hold a Key Altar · template rooms/crystal_garden.nbt',
 'story': ('The miners grew Starblooms here for dye and light, under a ceiling of crystal glass that glows like a night sky. '
           'When the Vault was sealed the garden kept going on its own: moss climbed the walls, leaves swallowed the trellis arches, '
           'and cerulite crystal started pushing through the south wall and around the old pond. It is the most beautiful room in '
           'the Vault, quiet and glowing, and the gardener\'s bench still has a few things worth taking.'),
 'sections': [
  ('Zones', ['Paths: from the north and west doors, stone paths with smooth curbs meet in a round plaza. The black medallion '
             'in the middle is where the Key Altar appears.',
             'Three raised beds (north-west, north-east, south-west): Shardwood log rims, Azure Moss, Starblooms, a leafy '
             'shrub in the middle, and a lantern hanging over each.',
             'Trellis arches: fence posts with a band of leaves over each path, 3 blocks clear underneath.',
             'Pond (south-east): a 3 x 3 still pond in a geode-shell rim with growing cerulite buds.',
             'Crystal grotto (south wall): geode shell breaking through the wall with buds, and a bench facing it on crystal sand.',
             "Gardener's bench (east wall): composter, barrels, potted Starblooms, a shelf, and the chest, lit by a lamp set in the wall.",
             'Ceiling: a 3 x 3 grid of crystal-glass panes in Shardwood frames, with four lanterns set in the glass.']),
  ('Loot', ["Gardener's chest (15, 1, 8), faces west: chests/concord_vault/uncommon.",
            'Everything else is decoration. Starblooms and buds can be picked (dye, decor), but the room has no gem-dropping '
            'clusters and no budding block, so it cannot be farmed for Cerulite.']),
  ('Connectors', ['North door x 6-10, y 1-5 at z 0; jigsaw (8, 1, 0) facing north.',
                  'West door z 6-10, y 1-5 at x 0; jigsaw (0, 1, 8) facing west.',
                  'Jigsaws: name and target zerog_tweaks:door, pool zerog_tweaks:concord_vault/corridors, final state air, joint aligned.']),
  ('Gameplay', ['A calm room: no spawner, no traps.',
                'When it is a key room, 3 Prismling guardians wake in a space full of low obstacles (bed rims, bench, pond). '
                'Players can use the beds as cover and the pond to slow down.',
                'Both doors lead straight to the plaza, so the altar is in view on entry.',
                'Light comes from lanterns, the glowing ceiling and the buds; the room glows blue, not white.']),
  ('Building it', ['Use crystal_garden.nbt as is (same name as the placeholder), or rebuild it by hand from the layer plans.',
                   'Leaves are stored with persistent=true so they never decay; keep that if you rebuild by hand (place them with shears-picked leaves).',
                   'Use Crystal Glass, not Shimmer Glass: Shimmer Glass is recoloured for the crystal wasteland.',
                   'Generator: generators/vault_rooms/room_crystal_garden.py.']),
 ]}
print(n, 'blocks;', sheet(r, meta, f'{OUT}/02_crystal_garden.png'))
for t, ok in r.check(): print('PASS' if ok else 'FAIL', t)
