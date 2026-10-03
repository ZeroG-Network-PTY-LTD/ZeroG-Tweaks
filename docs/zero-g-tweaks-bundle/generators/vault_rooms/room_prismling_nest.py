"""Concord Vault room 5/10: Prismling Nest (doors N, S, W). Usage: python3 room_prismling_nest.py <out_dir>"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from room_kit import Room, Z, sheet, CENTRE

OUT = sys.argv[1]
r = Room('NSW', seed=55)
P = lambda n, **k: Z + n + ('[' + ','.join(f'{a}={b}' for a, b in k.items()) + ']' if k else '')
BRK, CRK, BB = P('cerulean_stone_bricks'), P('cracked_cerulean_stone_bricks'), P('polished_black_cerulean_stone_bricks')
SHELL, SAND, GLASS, POL = P('cerulean_geode_shell'), P('crystal_sand'), P('crystal_glass'), P('polished_cerulean_stone')
LAMP = P('spectral_lantern')
BUD = lambda size, f='up': P(f'{size}_cerulite_bud', facing=f, waterlogged='false')
rnd = r.rng
SIZES = ['small', 'small', 'medium', 'medium', 'large']
door_lane = lambda x, z: (6 <= x <= 10 and (z <= 6 or z >= 10)) or (6 <= z <= 10 and x <= 6)    # keep walking lanes clear

# ---------------------------------------------------------------- shell: brick room, then the geode grows over it
for x in range(17):
    for z in range(17):
        edge = x in (0, 16) or z in (0, 16)
        r.put(x, 0, z, BB if edge else (SAND if rnd.random() < .45 else SHELL))
        r.put(x, 8, z, SHELL if rnd.random() < .7 else BRK)
        if edge:
            for y in range(1, 8): r.put(x, y, z, SHELL if rnd.random() < .45 else (CRK if rnd.random() < .3 else BRK))
r.open_doors()
# geode lining one block inside the walls (thicker high up), never in front of a door
for x in range(1, 16):
    for z in range(1, 16):
        if not (x in (1, 15) or z in (1, 15)) or door_lane(x, z): continue
        for y in range(1, 8):
            if rnd.random() < .32 + .07 * y: r.put(x, y, z, SHELL)
# what is left of the old floor near the middle, and the medallion under the crystal dust
for x in range(5, 12):
    for z in range(5, 12):
        if math.hypot(x - 8, z - 8) <= 3.2: r.put(x, 0, z, POL if rnd.random() < .7 else SAND)
for x in range(7, 10):
    for z in range(7, 10): r.put(x, 0, z, P('polished_black_cerulean_stone'))
r.put(8, 0, 8, P('chiseled_polished_black_cerulean_stone'))

# ---------------------------------------------------------------- stalactites: geode shell hanging from the ceiling, buds pointing down
LAMPS = ((3, 8), (8, 3), (8, 13), (8, 1), (8, 15), (1, 8), (3, 3), (3, 13), (6, 6), (6, 10))
near_lamp = lambda x, z: any(abs(x - a) <= 1 and abs(z - b) <= 1 for a, b in LAMPS)
for x in range(2, 15):
    for z in range(2, 15):
        if (x, z) in CENTRE or near_lamp(x, z): continue
        if rnd.random() < .22:
            r.put(x, 7, z, SHELL)
            if rnd.random() < .5: r.put(x, 6, z, SHELL)
            low = 6 if r.get(x, 6, z) == SHELL else 7
            r.put(x, low - 1, z, BUD(rnd.choice(SIZES), 'down'))

# ---------------------------------------------------------------- floor mounds with upward spikes (off the walking lanes)
for x in range(2, 15):
    for z in range(2, 15):
        if (x, z) in CENTRE or door_lane(x, z) or 11 <= x: continue
        if rnd.random() < .25:
            r.put(x, 1, z, SHELL)
            if rnd.random() < .6: r.put(x, 2, z, BUD(rnd.choice(SIZES)))
        elif rnd.random() < .12: r.put(x, 1, z, BUD(rnd.choice(SIZES)))
# spikes growing out of the lining toward the room
for x in range(2, 15):
    for z in range(2, 15):
        for y in range(1, 6):
            if r.get(x, y, z) != 'minecraft:air' or rnd.random() > .2: continue
            for (dx, dz), f in (((-1, 0), 'east'), ((1, 0), 'west'), ((0, -1), 'south'), ((0, 1), 'north')):
                if r.get(x + dx, y, z + dz) == SHELL and not door_lane(x, z):
                    r.put(x, y, z, BUD(rnd.choice(SIZES), f)); break

# ---------------------------------------------------------------- egg clutches: crystal-glass "eggs" crowned with small buds
for cx, cz in ((3, 3), (3, 13), (12, 13), (12, 3)):
    for dx, dz in ((0, 0), (1, 0), (0, 1)):
        x, z = cx + dx, cz + dz
        if door_lane(x, z): continue
        r.put(x, 1, z, GLASS); r.put(x, 2, z, BUD('small'))
    r.notes[(cx, 1, cz)] = 'egg clutch'

# ---------------------------------------------------------------- the nest mound against the east wall: spawner in front, chest on top behind it
for x in range(11, 16):
    for z in range(4, 13):
        h = 1 + (x >= 12) + (x >= 13 and 6 <= z <= 10) + (x >= 14 and 7 <= z <= 9)
        for y in range(1, h + 1): r.put(x, y, z, SHELL)
        if rnd.random() < .5 and not (x == 13 and z == 8): r.put(x, h + 1, z, BUD(rnd.choice(SIZES)))
r.spawner(12, 3, 8, Z + 'prismling', 'Prismling spawner', count=3, max_nearby=5, player_range=12, range=3)
r.put(12, 2, 8, SHELL)
r.chest(14, 4, 8, 'west', 'uncommon', 'Nest hoard (on the mound)')
r.put(13, 4, 8, 'minecraft:air')
for z in (7, 9): r.put(14, 4, z, BUD('large'))

# ---------------------------------------------------------------- lights: dim on purpose (a spawner only works at block light 11 or lower)
for x, z in LAMPS: r.put(x, 8, z, LAMP)
for x, z in LAMPS:
    for y in (6, 7):
        if r.get(x, y, z) != 'minecraft:air' and 'bud' not in r.get(x, y, z): r.put(x, y, z, 'minecraft:air')

# fill any sealed pocket that would still be dark (no mob can spawn in a block)
_L = r.light()
for x in range(1, 16):
    for z in range(1, 16):
        for y in range(1, 7):
            if r._shape(r.get(x, y, z)) is None and r._shape(r.get(x, y - 1, z)) == 'full' and _L.get((x, y, z), 0) == 0:
                r.put(x, y, z, SHELL)
n = r.save(f'{OUT}/prismling_nest.nbt')
L = r.light()
spawn_light = max(L.get((12 + dx, 3 + dy, 8 + dz), 0) for dx in range(-3, 4) for dy in (-1, 0, 1) for dz in range(-3, 4))
meta = {
 'title': 'Concord Vault · Room 5 · Prismling Nest',
 'subtitle': '17 x 9 x 17 · doors north, south and west · 1 uncommon chest + Prismling spawner · can hold a Key Altar · template rooms/prismling_nest.nbt',
 'story': ('This was a storeroom once; you can still see brick behind the crystal. The Prismlings found it after the Vault was '
           'sealed and grew it into a geode: shell creeping over the walls, spikes on every surface, clutches of crystal eggs in the '
           'corners. Their nest mound fills the east wall, and whatever the Concord left behind they piled on top of it. It is the only '
           'room in the Vault that fights back on its own.'),
 'cut_top': 7, 'cut_depth': 2,
 'view_a_title': 'Cutaway from the south-west (ceiling, stalactites and the two near walls cut away)',
 'view_b_title': 'Cutaway from the north-east (ceiling, stalactites and the two near walls cut away)',
 'sections': [
  ('Zones', ['Walking lanes: from the north, south and west doors to the centre, kept clear of mounds and spikes.',
             'Centre clearing: what is left of the polished floor, with the black medallion where the Key Altar appears.',
             'Geode lining: shell one block inside the walls, thicker toward the ceiling, with buds growing out toward the room.',
             'Stalactites: shell hanging from the ceiling with buds pointing down.',
             'Floor mounds: small shell bumps with upward spikes, west half of the room.',
             'Egg clutches: crystal-glass "eggs" with small buds on top, in all four corners.',
             'Nest mound (east wall): stepped geode shell rising to 4 high, the Prismling spawner on its front step, the chest on top behind it.']),
  ('Loot and spawner', ['Nest hoard (14, 4, 8), faces west: chests/concord_vault/uncommon. Reach it by climbing the mound past the spawner.',
                        'Prismling spawner (12, 3, 8): 3 per wave, at most 5 nearby, wakes when a player is within 12 blocks, spawns within 3 blocks.',
                        f'Brightest block light around the spawner: {spawn_light}. Monster spawners need 11 or lower in 1.21, so it works; '
                        'do not add lights near the mound.',
                        'Break the spawner to stop the waves; it drops nothing, as in vanilla.']),
  ('Connectors', ['North door x 6-10, y 1-5 at z 0; jigsaw (8, 1, 0) facing north.',
                  'South door x 6-10, y 1-5 at z 16; jigsaw (8, 1, 16) facing south.',
                  'West door z 6-10, y 1-5 at x 0; jigsaw (0, 1, 8) facing west.',
                  'Jigsaws: name and target zerog_tweaks:door, pool zerog_tweaks:concord_vault/corridors, final state air, joint aligned.']),
  ('Gameplay', ['The fight room: Prismlings keep coming until the spawner is broken.',
                'When it is also a key room, taking the key wakes 3 more Prismling guardians on top of the spawner waves. That is intended: '
                'it is the hardest key in the Vault.',
                'Three doors make it easy to retreat and come back; the spikes and mounds slow movement on the sides, so players fight in the lanes.',
                'If the Prismling entity has its own spawn rules (light, block), check that the spawner can place it on geode shell.']),
  ('Building it', ['Buds only drop themselves, and there are no full clusters or budding blocks, so the nest cannot be farmed for Cerulite.',
                   'The spawner settings are stored in the file. To change them by hand: /data merge block 12 3 8 {SpawnCount:3,MaxNearbyEntities:5}.',
                   'Generator: generators/vault_rooms/room_prismling_nest.py.']),
 ]}
print(n, 'blocks; spawner light', spawn_light, ';', sheet(r, meta, f'{OUT}/05_prismling_nest.png'))
for t, ok in r.check(): print('PASS' if ok else 'FAIL', t)
