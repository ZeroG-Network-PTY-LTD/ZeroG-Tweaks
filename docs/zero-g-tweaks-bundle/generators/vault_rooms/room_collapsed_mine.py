"""Concord Vault room 4/10: Collapsed Mine (doors N, E). Usage: python3 room_collapsed_mine.py <out_dir>"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from room_kit import Room, Z, sheet, CENTRE

OUT = sys.argv[1]
r = Room('NE', seed=44)
P = lambda n, **k: Z + n + ('[' + ','.join(f'{a}={b}' for a, b in k.items()) + ']' if k else '')
STONE, COB, CBLK, BB = P('cerulean_stone'), P('cobbled_cerulean_stone'), P('chiseled_polished_black_cerulean_stone'), P('polished_black_cerulean_stone_bricks')
POST, PLANK, LOGX, LOGZ = P('shardwood_log', axis='y'), P('shardwood_planks'), P('stripped_shardwood_log', axis='x'), P('stripped_shardwood_log', axis='z')
LAMP, CHAIN = P('spectral_lantern'), 'minecraft:chain[axis=y,waterlogged=false]'
RAIL = lambda s: f'minecraft:rail[shape={s},waterlogged=false]'
rnd = r.rng
rough = lambda: COB if rnd.random() < .35 else STONE

# ---------------------------------------------------------------- shell: rough-cut rock, not bricks
for x in range(17):
    for z in range(17):
        edge = x in (0, 16) or z in (0, 16)
        r.put(x, 0, z, rough() if edge else (P('crystal_sand') if rnd.random() < .18 else COB if rnd.random() < .4 else STONE))
        r.put(x, 8, z, rough())
        if edge:
            for y in range(1, 8): r.put(x, y, z, rough())
# jagged walls and ceiling: rock bulging one block inward here and there
for x in range(1, 16):
    for z in range(1, 16):
        if x in (1, 15) or z in (1, 15):
            for y in range(3, 8):
                if rnd.random() < .18 + .06 * (y - 3): r.put(x, y, z, rough())
        if rnd.random() < .12: r.put(x, 7, z, rough())
r.open_doors()
# door frames: timber, like a mineshaft entrance
for cells in (lambda i: (i, 0), lambda i: (16, i)):
    for i in (5, 11):
        for y in range(1, 6): r.put(cells(i)[0], y, cells(i)[1], POST)
    for i in range(5, 12): r.put(cells(i)[0], 6, cells(i)[1], LOGX if cells(0)[1] == 0 else LOGZ)

# ---------------------------------------------------------------- mine frames (posts + cross beam), lanterns hung under the beams
def frame_x(z, x0, x1, top=5):                      # beam runs along x
    for y in range(1, top): r.put(x0, y, z, POST); r.put(x1, y, z, POST)
    for x in range(x0, x1 + 1): r.put(x, top, z, LOGX)
def frame_z(x, z0, z1, top=5):                      # beam runs along z
    for y in range(1, top): r.put(x, y, z0, POST); r.put(x, y, z1, POST)
    for z in range(z0, z1 + 1): r.put(x, top, z, LOGZ)
frame_x(3, 5, 11); frame_z(14, 5, 11)
for y in (6, 7): r.put(8, y, 3, PLANK)              # beam braced to the ceiling
for y in (6, 7): r.put(14, y, 8, PLANK)
r.put(8, 4, 3, LAMP); r.put(14, 4, 8, LAMP)

# ---------------------------------------------------------------- rail line: north door -> around the altar spot -> east door
track = {}
for z in range(1, 4): track[(8, z)] = 'north_south'
track[(8, 4)] = 'north_east'
for x in range(9, 12): track[(x, 4)] = 'east_west'
track[(12, 4)] = 'south_west'
for z in range(5, 8): track[(12, z)] = 'north_south'
track[(12, 8)] = 'north_east'
for x in range(13, 16): track[(x, 8)] = 'east_west'
for (x, z), s in track.items(): r.put(x, 1, z, RAIL(s)); r.put(x, 0, z, P('stripped_shardwood_wood', axis='y') if (x + z) % 2 else STONE)

# ---------------------------------------------------------------- the cave-in: a rubble slope rising into the south-west corner
for x in range(1, 9):
    for z in range(8, 16):
        dist = math.hypot(x - 1, z - 15)
        h = max(0, int(round(6.5 - dist * .95)))
        if (x, z) in CENTRE: h = 0
        for y in range(1, h + 1): r.put(x, y, z, rough())
        if 0 < h < 7 and rnd.random() < .55:                            # slopes: slabs and stairs on top of the heap
            r.put(x, h + 1, z, P('cobbled_cerulean_stone_slab', type='bottom', waterlogged='false'))
for x in range(1, 5):                                                    # the ceiling sagged over the heap
    for z in range(12, 16): r.put(x, 7, z, rough())
# fallen beam lying on the rubble, and the snapped post it came off
for x in range(4, 9): r.put(x, 3 if x < 6 else 2, 11, LOGX)
r.put(10, 1, 11, POST); r.put(10, 2, 11, P('shardwood_fence'))
# derailed chest minecart beside the heap, a lantern knocked to the floor
r.chest_minecart(10, 13, 1, 'common')
r.put(9, 1, 14, LAMP); r.notes[(9, 1, 14)] = 'fallen lantern'

# ---------------------------------------------------------------- north-west: miners' alcove with the chest
r.chest(1, 1, 2, 'east', 'common', "Miners' chest")
r.put(1, 1, 3, 'minecraft:barrel[facing=up,open=false]'); r.put(1, 2, 3, 'minecraft:barrel[facing=east,open=false]')
r.put(1, 1, 1, 'minecraft:barrel[facing=up,open=false]')
for z in (1, 2, 3, 4): r.put(1, 3, z, P('shardwood_slab', type='bottom', waterlogged='false'))
r.put(2, 1, 4, P('shardwood_stairs', facing='west', half='bottom', shape='straight'))
r.put(0, 3, 2, LAMP)                                                     # lamp cut into the wall over the alcove

# ---------------------------------------------------------------- south-east: a worked face (picked-out pockets), a spoil pile and a buffer
for z in range(12, 16):
    for y in range(1, 6):
        if rnd.random() < .5: r.put(15, y, z, rough())
for (x, y, z) in ((13, 1, 14), (14, 1, 14), (14, 1, 13), (14, 2, 14), (13, 1, 15), (14, 1, 15), (15, 1, 15)):
    r.put(x, y, z, COB)
r.put(14, 2, 15, P('cobbled_cerulean_stone_slab', type='bottom', waterlogged='false'))
r.put(15, 4, 13, LAMP)                                                   # work light in the face

# ---------------------------------------------------------------- lights over the open floor (ceiling lanterns on chains)
for x, z, drop in ((5, 8, 5), (11, 12, 5), (4, 5, 5)):
    for y in range(drop + 1, 8): r.put(x, y, z, CHAIN)
    r.put(x, drop, z, LAMP)
r.put(8, 7, 8, CHAIN); r.put(8, 6, 8, CHAIN); r.put(8, 5, 8, LAMP)      # over the Key Altar spot

n = r.save(f'{OUT}/collapsed_mine.nbt')
meta = {
 'title': 'Concord Vault · Room 4 · Collapsed Mine',
 'cut_top': 7, 'cut_depth': 2,
 'view_a_title': 'Cutaway from the south-west (ceiling, sagging rock and the two near walls cut away)',
 'view_b_title': 'Cutaway from the north-east (ceiling, sagging rock and the two near walls cut away)',
 'subtitle': '17 x 9 x 17 · doors north and east · 1 common chest + 1 chest minecart · can hold a Key Altar · template rooms/collapsed_mine.nbt',
 'story': ('A working face of the Quiet Mines, where the Concord cut stone for the Vault itself. Something made the ceiling give way '
           'in the south-west corner: the rubble buried half the room, snapped a support post and threw its beam across the heap. '
           'The cart line still curves through from the north tunnel to the east one, but one cart was knocked off the rails and lies '
           'where it stopped, still loaded. It is the roughest room in the Vault: bare rock, timber frames and dust.'),
 'sections': [
  ('Zones', ['Rail line: from the north door down x 8, then east along z 4, south along x 12 and out of the east door along z 8. '
             'It curves around the altar spot, so a Key Altar never sits on the track.',
             'Mine frames: two timber frames (posts and a stripped-log beam), one over the north entrance and one along the east side, '
             'each braced to the ceiling and carrying a lantern.',
             'Cave-in (south-west): a rubble slope that rises to 6 high in the corner, slabs on its surface, the ceiling sagging above it, '
             'a fallen beam lying across it and the snapped post it came from.',
             "Miners' alcove (north-west): chest, barrels, a plank shelf and a stool, lit by a lamp cut into the wall.",
             'Worked face (south-east): a picked-out rock face with a spoil pile and a work light.',
             'Walls and ceiling: rough cerulean and cobbled stone, bulging inward in places, with crystal-sand dust on the floor.']),
  ('Loot', ["Miners' chest (1, 1, 2), faces east: chests/concord_vault/common.",
            'Derailed chest minecart (10, 1, 13), beside the rubble: common. It is an entity, so it can sit off the rails.']),
  ('Connectors', ['North door x 6-10, y 1-5 at z 0; jigsaw (8, 1, 0) facing north.',
                  'East door z 6-10, y 1-5 at x 16; jigsaw (16, 1, 8) facing east.',
                  'Rails stop one block inside each door, so the door cells stay clear for the corridor.',
                  'Jigsaws: name and target zerog_tweaks:door, pool zerog_tweaks:concord_vault/corridors, final state air, joint aligned.']),
  ('Gameplay', ['No spawner, no traps: the danger is implied (it already fell in).',
                'The rubble slope is climbable and gives height; when it is a key room, players can fight the 3 Prismling guardians from it.',
                'The cart on the rails can be pushed along the track for fun; the derailed one holds the loot.']),
  ('Building it', ['Rails are stored with their shapes (straight runs and four curves), so the track is correct when the room is placed.',
                   'The rubble uses a random mix of cerulean and cobbled stone; when rebuilding by hand, keep the slope rising toward the corner.',
                   'Generator: generators/vault_rooms/room_collapsed_mine.py.']),
 ]}
print(n, 'blocks;', sheet(r, meta, f'{OUT}/04_collapsed_mine.png'))
for t, ok in r.check(): print('PASS' if ok else 'FAIL', t)
