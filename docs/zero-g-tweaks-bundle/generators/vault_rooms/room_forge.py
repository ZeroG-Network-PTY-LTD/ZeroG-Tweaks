"""Concord Vault room 8/10: Forge (doors N, E). Usage: python3 room_forge.py <out_dir>"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from room_kit import Room, Z, sheet

OUT = sys.argv[1]
r = Room('NE', seed=88)
P = lambda n, **k: Z + n + ('[' + ','.join(f'{a}={b}' for a, b in k.items()) + ']' if k else '')
BB, BRK, CRK, CHIS, CBLK = (P('polished_black_cerulean_stone_bricks'), P('cerulean_stone_bricks'), P('cracked_cerulean_stone_bricks'),
                            P('chiseled_cerulean_stone'), P('chiseled_polished_black_cerulean_stone'))
POL, SMOOTH, BLK = P('polished_cerulean_stone'), P('smooth_cerulean_stone'), P('polished_black_cerulean_stone')
LOGY, LOGX, LOGZ = P('stripped_shardwood_log', axis='y'), P('stripped_shardwood_log', axis='x'), P('stripped_shardwood_log', axis='z')
SLAB_T = P('shardwood_slab', type='top', waterlogged='false')
LAMP, CHAIN = P('spectral_lantern'), 'minecraft:chain[axis=y,waterlogged=false]'
BSTAIR = lambda f, h: P('polished_black_cerulean_stone_brick_stairs', facing=f, half=h, shape='straight', waterlogged='false')
FIRE = 'minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]'

# ---------------------------------------------------------------- shell: soot-dark lower walls, stone floor, black near the hearth
for x in range(17):
    for z in range(17):
        edge = x in (0, 16) or z in (0, 16)
        r.put(x, 0, z, BB if edge else (BLK if z >= 12 else SMOOTH if (x + z) % 3 == 0 else POL))
        r.put(x, 8, z, BRK)
        if edge:
            for y in range(1, 8): r.put(x, y, z, BB if y <= 2 else CHIS if y == 7 else (CRK if r.rng.random() < .15 else BRK))
for a in (4, 12):
    for y in range(1, 8): r.put(a, y, 0, LOGY); r.put(0, y, a, LOGY); r.put(16, y, a, LOGY)
for i in range(1, 16): r.put(i, 7, 4, LOGX); r.put(i, 7, 12, LOGX)                     # ceiling beams
r.open_doors()
for cells in (lambda i: (i, 0), lambda i: (16, i)):
    for i in (5, 11):
        for y in range(1, 7): r.put(cells(i)[0], y, cells(i)[1], CBLK)
    for i in range(6, 11): r.put(cells(i)[0], 6, cells(i)[1], BB)
    r.put(cells(8)[0], 6, cells(8)[1], CBLK)
# anvil floor: a black ring around the medallion where the Key Altar goes
for x in range(5, 12):
    for z in range(5, 12):
        dd = math.hypot(x - 8, z - 8)
        if 2.4 < dd <= 3.4: r.put(x, 0, z, BLK)
for x in range(7, 10):
    for z in range(7, 10): r.put(x, 0, z, BLK)
r.put(8, 0, 8, CBLK)

# ---------------------------------------------------------------- the great hearth (south wall): campfires behind a stone grate, under a hood and chimney
for x in range(6, 11):
    for y in range(1, 3): r.put(x, y, 15, BB)                                          # back of the hearth
for x in (7, 8, 9):
    r.put(x, 1, 15, FIRE); r.put(x, 2, 15, 'minecraft:air')
    r.put(x, 1, 14, P('cerulean_stone_brick_wall'))                                     # grate: nobody steps into the fire
for x in (6, 10):
    for y in range(1, 4): r.put(x, y, 14, BB); r.put(x, y, 15, BB)                       # hearth cheeks
for x in range(6, 11): r.put(x, 3, 14, BSTAIR('south', 'top')); r.put(x, 3, 15, BB)     # hood overhang
for x in range(7, 10): r.put(x, 4, 14, BSTAIR('south', 'bottom')); r.put(x, 4, 15, BB)
for x in range(7, 10):
    for y in range(5, 8): r.put(x, y, 15, BB)                                           # chimney
r.put(8, 5, 14, CBLK); r.put(8, 6, 14, CBLK)                                            # Concord mark on the chimney breast
# furnace banks either side of the hearth
for x in (4, 5): r.put(x, 1, 15, 'minecraft:blast_furnace[facing=north,lit=false]'); r.put(x, 2, 15, 'minecraft:blast_furnace[facing=north,lit=false]')
for x in (11, 12): r.put(x, 1, 15, 'minecraft:furnace[facing=north,lit=false]'); r.put(x, 2, 15, 'minecraft:furnace[facing=north,lit=false]')
for x in (4, 5, 11, 12): r.put(x, 3, 15, BSTAIR('north', 'bottom'))

# ---------------------------------------------------------------- west wall: the smith's line (smithing table, anvil, grindstone, quench trough)
r.put(1, 1, 3, 'minecraft:smithing_table')
r.put(3, 1, 5, 'minecraft:anvil[facing=north]'); r.notes[(3, 1, 5)] = 'anvil'
r.put(1, 1, 7, 'minecraft:grindstone[face=floor,facing=east]')
r.put(1, 1, 10, 'minecraft:water_cauldron[level=3]'); r.put(1, 1, 11, 'minecraft:water_cauldron[level=3]'); r.notes[(1, 1, 10)] = 'quench trough'
for z in range(2, 13):                                                                  # tool rack along the wall at y 3-4
    r.put(1, 3, z, SLAB_T if z % 3 else LOGZ)
r.put(1, 4, 5, P('shardwood_fence')); r.put(1, 4, 8, P('shardwood_fence'))
r.put(0, 4, 8, LAMP)

# ---------------------------------------------------------------- south-east: the smith's bench, key moulds and the chest
r.put(15, 1, 10, 'minecraft:crafting_table')
r.put(15, 1, 11, SLAB_T); r.put(15, 1, 12, SLAB_T); r.put(15, 2, 11, CBLK); r.notes[(15, 2, 11)] = 'key mould'
r.put(15, 2, 12, LAMP)
r.chest(15, 1, 14, 'west', 'uncommon', "Smith's chest")
r.put(14, 1, 11, P('shardwood_stairs', facing='west', half='bottom', shape='straight', waterlogged='false'))
for z in (13, 15): r.put(15, 1, z, 'minecraft:barrel[facing=up,open=false]')
# north-east: fuel store (barrels) and a bellows (stairs + fence)
for (x, y, z) in ((15, 1, 1), (14, 1, 1), (15, 2, 1), (15, 1, 2), (13, 1, 1)): r.put(x, y, z, 'minecraft:barrel[facing=up,open=false]')
r.put(2, 1, 14, P('shardwood_stairs', facing='east', half='top', shape='straight', waterlogged='false')); r.put(3, 1, 14, P('shardwood_fence'))
r.put(2, 2, 14, CHAIN); r.notes[(2, 1, 14)] = 'bellows'

# ---------------------------------------------------------------- lights: lanterns on chains from the beams, plus the fire
for x, z in ((4, 4), (12, 4), (4, 12), (12, 12)):
    r.put(x, 6, z, CHAIN); r.put(x, 5, z, LAMP)
r.put(8, 7, 8, CHAIN); r.put(8, 6, 8, LAMP)

n = r.save(f'{OUT}/forge.nbt')
meta = {
 'title': 'Concord Vault · Room 8 · Forge',
 'subtitle': '17 x 9 x 17 · doors north and east · 1 uncommon chest · can hold a Key Altar · template rooms/forge.nbt',
 'story': ('The Concord smiths made the Vault\'s tools here, and the four keys that build the Sentinel\'s chamber. The great hearth '
           'in the south wall still burns behind its grate, the furnaces stand cold on either side, and the smith\'s line along '
           'the west wall is laid out ready for work. On the bench by the east door the key moulds are still set in the stone.'),
 'cut_top': 7,
 'sections': [
  ('Zones', ['Great hearth (south wall): three lit campfires behind a low stone grate, black-brick cheeks, a stepped hood and a chimney '
             'to the ceiling with the Concord mark on its breast.',
             'Furnace banks: two blast furnaces stacked on the west of the hearth, two furnaces on the east, each capped with a stair.',
             "Smith's line (west wall): smithing table, anvil, grindstone and a two-cauldron quench trough, under a tool rack.",
             "Smith's bench (south-east): crafting table, a slab bench with the key moulds (a chiseled block) and a lamp, barrels, the chest.",
             'Fuel store (north-east): stacked barrels. Bellows (south-west corner): a stair and a fence with a chain.',
             'Anvil floor: a black ring around the medallion where the Key Altar appears; black stone under the hearth end.']),
  ('Loot', ["Smith's chest (15, 1, 14), faces west: chests/concord_vault/uncommon.",
            'The workstations are usable: players can repair and upgrade gear here (anvil, smithing table, grindstone), '
            'which matters because the Vault is far from home.']),
  ('Connectors', ['North door x 6-10, y 1-5 at z 0; jigsaw (8, 1, 0) facing north.',
                  'East door z 6-10, y 1-5 at x 16; jigsaw (16, 1, 8) facing east.',
                  'Jigsaws: name and target zerog_tweaks:door, pool zerog_tweaks:concord_vault/corridors, final state air, joint aligned.']),
  ('Gameplay', ['A workshop room: no spawner, no traps. The fire hurts if someone climbs the grate, which is fair.',
                'Useful mid-Vault: repair at the anvil, smith upgrades if players brought templates, drink from the cauldrons.',
                'When it is a key room, the Prismling guardians fight around the workstations; the hearth is a dead end to avoid.']),
  ('Building it', ['The hearth glow comes from lit campfires, which need no fuel. Lit furnaces would go dark on their first tick, so '
                   'the furnaces are stored unlit.',
                   'No lava: it would set the Shardwood beams and rack alight.',
                   'Generator: generators/vault_rooms/room_forge.py.']),
 ]}
print(n, 'blocks;', sheet(r, meta, f'{OUT}/08_forge.png'))
for t, ok in r.check(): print('PASS' if ok else 'FAIL', t)
