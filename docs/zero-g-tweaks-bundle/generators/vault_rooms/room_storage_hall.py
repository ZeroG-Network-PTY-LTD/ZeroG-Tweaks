"""Concord Vault room 1/10: Storage Hall (doors N, S, E). Usage: python3 room_storage_hall.py <out_dir>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from room_kit import Room, Z, sheet

OUT = sys.argv[1]
r = Room('NSE', seed=11)
P = lambda n, **k: Z + n + ('[' + ','.join(f'{a}={b}' for a, b in k.items()) + ']' if k else '')
BB, BRK, CRK, CHIS = P('polished_black_cerulean_stone_bricks'), P('cerulean_stone_bricks'), P('cracked_cerulean_stone_bricks'), P('chiseled_cerulean_stone')
LOGY, LOGX, LOGZ, BEAMX = P('stripped_shardwood_log', axis='y'), P('stripped_shardwood_log', axis='x'), P('stripped_shardwood_log', axis='z'), P('stripped_shardwood_wood', axis='y')
PLANK, SLAB_T, SLAB_B = P('shardwood_planks'), P('shardwood_slab', type='top'), P('shardwood_slab', type='bottom')
BARREL = lambda f='up': f'minecraft:barrel[facing={f},open=false]'
CHAIN, LAMP, PULSAR = 'minecraft:chain[axis=y,waterlogged=false]', P('spectral_lantern'), P('pulsar_lamp')

# ---------------------------------------------------------------- shell
for x in range(17):
    for z in range(17):
        edge = x in (0, 16) or z in (0, 16)
        r.put(x, 0, z, BB if edge else PLANK)
        r.put(x, 8, z, P('cerulean_stone'))
        for y in range(1, 8):
            if not edge: continue
            r.put(x, y, z, BB if y == 1 else CHIS if y == 7 else (CRK if r.rng.random() < .16 else BRK))
# pilasters (Shardwood posts the beams rest on) and corner posts
for a in (3, 13):
    for y in range(1, 8):
        r.put(a, y, 0, LOGY); r.put(a, y, 16, LOGY); r.put(0, y, a, LOGY); r.put(16, y, a, LOGY)
for x, z in ((0, 0), (0, 16), (16, 0), (16, 16)):
    for y in range(1, 8): r.put(x, y, z, LOGY)
# ceiling beams at y7 resting on the pilasters, crossing at (3|13, 3|13)
for i in range(1, 16):
    r.put(i, 7, 3, LOGX); r.put(i, 7, 13, LOGX); r.put(3, 7, i, LOGZ); r.put(13, 7, i, LOGZ)
for x, z in ((3, 3), (3, 13), (13, 3), (13, 13)): r.put(x, 7, z, BEAMX)
# floor: stone aisles (N-S and to the east door) with smooth curbs, black medallion where the Key Altar goes
for z in range(1, 16):
    for x in range(6, 11): r.put(x, 0, z, P('smooth_cerulean_stone') if x in (6, 10) else P('polished_cerulean_stone'))
for x in range(11, 16):
    for z in range(6, 11): r.put(x, 0, z, P('smooth_cerulean_stone') if z in (6, 10) else P('polished_cerulean_stone'))
for x in range(7, 10):
    for z in range(7, 10): r.put(x, 0, z, P('polished_black_cerulean_stone'))
r.put(8, 0, 8, P('chiseled_polished_black_cerulean_stone'))
# door frames: black jambs, lintel and a chiseled keystone over each door
r.open_doors()
for d, cells in (('N', lambda i: (i, 0)), ('S', lambda i: (i, 16)), ('E', lambda i: (16, i))):
    for i in (5, 11):
        for y in range(1, 7): r.put(*((cells(i)[0], y, cells(i)[1])), BB)
    for i in range(6, 11): r.put(cells(i)[0], 6, cells(i)[1], BB)
    r.put(cells(8)[0], 6, cells(8)[1], P('chiseled_polished_black_cerulean_stone'))
# west wall lamp, framed
for y, z in ((3, 8), (5, 8), (4, 7), (4, 9)): r.put(0, y, z, P('chiseled_polished_black_cerulean_stone'))
r.put(0, 4, 8, PULSAR)

# ---------------------------------------------------------------- west racks (two tall shelving units)
def rack(z0, z1):
    for z in range(z0, z1 + 1):
        r.put(1, 1, z, BARREL('east')); r.put(1, 2, z, BARREL('east')); r.put(1, 3, z, SLAB_T); r.put(1, 4, z, BARREL('east'))
        r.put(1, 5, z, SLAB_B)
        end = z in (z0, z1)
        if end:
            for y in range(1, 5): r.put(2, y, z, P('shardwood_fence'))
            r.put(2, 5, z, SLAB_B)
        else:
            r.put(2, 3, z, SLAB_T)                                   # shelf deck, 2 deep
            if r.rng.random() < .45: r.put(2, 1, z, BARREL('up'))    # loose crates at the foot of the rack
            if r.rng.random() < .3: r.put(2, 4, z, P('potted_starbloom'))
rack(1, 6); rack(10, 15)
# quartermaster's desk between the racks
r.chest(1, 1, 7, 'east', 'common', 'Quartermaster')
r.put(1, 1, 8, 'minecraft:lectern[facing=east,has_book=false,powered=false]'); r.notes[(1, 1, 8)] = 'manifest lectern'
r.put(1, 1, 9, BARREL('east'))
r.put(1, 2, 7, 'minecraft:bookshelf'); r.put(1, 2, 9, 'minecraft:bookshelf')
for z in (7, 8, 9): r.put(1, 3, z, SLAB_B)
r.put(3, 1, 7, P('shardwood_stairs', facing='west', half='top', shape='straight'))
r.put(3, 1, 9, P('shardwood_stairs', facing='west', half='top', shape='straight'))
r.put(3, 2, 7, P('potted_starbloom'))
r.put(4, 1, 7, P('shardwood_stairs', facing='east', half='bottom', shape='straight'))      # stool

# ---------------------------------------------------------------- north and south wall shelves
for x in (4, 5, 11, 12):
    for z, f in ((1, 'south'), (15, 'north')):
        if z == 15 and x in (11, 12): continue
        r.put(x, 1, z, BARREL(f)); r.put(x, 2, z, SLAB_T); r.put(x, 3, z, BARREL(f)); r.put(x, 4, z, SLAB_B)

# ---------------------------------------------------------------- east loading bay
# north-east crate stack around the dock chest
for (x, y, z) in ((14, 1, 1), (15, 1, 1), (15, 2, 1), (15, 1, 2), (14, 2, 1), (15, 3, 1), (13, 1, 1), (15, 1, 4)):
    r.put(x, y, z, BARREL('up'))
r.chest(15, 1, 3, 'west', 'common', 'Dock (north)')
# south-east crates and a packing bench
for (x, y, z) in ((15, 1, 15), (14, 1, 15), (15, 2, 15), (13, 1, 15), (15, 1, 14), (15, 1, 11), (15, 2, 11)):
    r.put(x, y, z, BARREL('up'))
r.chest(15, 1, 13, 'west', 'common', 'Dock (south)')
r.put(12, 1, 14, P('shardwood_stairs', facing='south', half='top', shape='straight'))
r.put(11, 1, 14, P('shardwood_stairs', facing='south', half='top', shape='straight'))
r.put(11, 1, 13, P('shardwood_stairs', facing='north', half='bottom', shape='straight'))  # bench seat
# cart line from the east door to a buffer, with a chest minecart and a crate hanging from the hoist
for x in range(12, 16): r.put(x, 1, 8, 'minecraft:rail[shape=east_west,waterlogged=false]')
r.put(11, 1, 8, P('polished_black_cerulean_stone_stairs', facing='west', half='bottom', shape='straight'))
r.chest_minecart(13, 8, 1, 'common')
r.put(13, 6, 8, CHAIN); r.put(13, 5, 8, CHAIN); r.put(13, 4, 8, BARREL('up')); r.notes[(13, 4, 8)] = 'hoist crate'

# ---------------------------------------------------------------- south-west sorting corner
r.put(4, 1, 14, 'minecraft:crafting_table'); r.put(5, 1, 14, SLAB_T); r.put(5, 2, 14, BARREL('up'))
r.put(4, 1, 13, P('shardwood_stairs', facing='south', half='bottom', shape='straight'))

# ---------------------------------------------------------------- lights: three hanging lanterns over the aisle, ceiling lights over the bays
for z, drop in ((4, 6), (12, 6), (8, 5)):
    for y in range(drop + 1, 8): r.put(8, y, z, CHAIN)
    r.put(8, drop, z, LAMP)
for x, z in ((5, 5), (5, 11), (11, 5), (11, 11), (2, 2), (2, 14), (14, 2), (14, 14), (2, 8), (14, 11), (14, 5)): r.put(x, 8, z, LAMP)
# wall sconces: lanterns set into the north and south walls beside the doors
for x in (2, 14):
    r.put(x, 4, 0, LAMP); r.put(x, 4, 16, LAMP)

n = r.save(f'{OUT}/storage_hall.nbt')
meta = {
 'title': 'Concord Vault · Room 1 · Storage Hall',
 'subtitle': '17 x 9 x 17 · doors north, south and east · 3 common chests + 1 chest minecart · can hold a Key Altar · template rooms/storage_hall.nbt',
 'story': ('The Concord miners drew their rations, rope and lamp oil here. A quartermaster kept the manifests on the lectern by the west '
           'racks, crates came in on the cart line from the east tunnel, and a hoist lifted them off the cart. When the Vault was '
           'sealed the hall was left mid-shift: crates still stacked, a cart still loaded, one crate still hanging from the hoist. '
           'It should feel orderly and lived-in, the calmest room in the Vault, a place to breathe between fights.'),
 'sections': [
  ('Zones', ['Centre aisle (x 6-10, north to south door): polished cerulean with smooth curbs and a black medallion at the centre, '
             'which is where the Key Altar appears when this room is a key room. Three spectral lanterns hang over it on chains.',
             'West racks (x 1-2): two tall Shardwood shelving units (z 1-6 and 10-15). Barrels three high, a slab shelf deck two '
             'blocks deep, fence posts at the ends, a few potted Starblooms.',
             "Quartermaster's desk (x 1-4, z 7-9): chest, manifest lectern, barrel, bookshelves, a counter with a gap to walk in, a stool.",
             'East loading bay (x 11-15): a rail line from the east door to a stone buffer, a chest minecart on it, a crate hanging '
             'from a chain hoist off the ceiling beam, and crate stacks with the two dock chests in each corner.',
             'Sorting corner (south-west): crafting table, packing bench and a barrel.',
             'Structure: black-brick plinth, cerulean brick walls with cracked bricks, a chiseled band at the top, stripped Shardwood '
             'posts that carry a beam grid at y 7, and a framed pulsar lamp on the west wall.']),
  ('Loot', ["Quartermaster's chest (1, 1, 7), faces east: chests/concord_vault/common.",
            'Dock chest north (15, 1, 3) and south (15, 1, 13), face west: common.',
            'Chest minecart on the rail (13, 1, 8): common. It is an entity; leave it out if the brief should stay at exactly 3 chests.',
            'Every barrel is empty decoration. Turn any into loot with LootTable common if the room feels too thin.']),
  ('Connectors', ['North door x 6-10, y 1-5 at z 0; jigsaw (8, 1, 0) facing north.',
                  'South door x 6-10, y 1-5 at z 16; jigsaw (8, 1, 16) facing south.',
                  'East door z 6-10, y 1-5 at x 16; jigsaw (16, 1, 8) facing east.',
                  'All jigsaws: name and target zerog_tweaks:door, pool zerog_tweaks:concord_vault/corridors, final state air, joint aligned.',
                  'The rails stop at x 15, so the door cells stay clear for the corridor.']),
  ('Gameplay', ['No spawner and no traps: this is the breather room.',
                'When this is a key room, taking the key wakes 3 Prismling guardians. The open aisles (5 wide) and the bay give room '
                'to fight them; the racks and crates are cover.',
                'Sightlines: from every door you can see the centre medallion, so the Key Altar is obvious the moment you walk in.',
                'Three chests and a cart reward a thorough search: the dock chests sit behind crate stacks, not in plain view.']),
  ('Building it', ['Use the file as is: storage_hall.nbt in data/zerog_tweaks/structure/concord_vault/rooms/ (same name, so the pool needs no change).',
                   'Or rebuild it by hand from the layer plans: place the shell, then beams (y 7), floor (y 0), racks, bay, then lights.',
                   'Fence and wall connections are stored in the file, so they look right the moment the room is placed.',
                   'Generator: generators/vault_rooms/room_storage_hall.py (shared code in room_kit.py).']),
 ]}
print(n, 'blocks;', sheet(r, meta, f'{OUT}/01_storage_hall.png'))
for t, ok in r.check(): print('PASS' if ok else 'FAIL', t)
