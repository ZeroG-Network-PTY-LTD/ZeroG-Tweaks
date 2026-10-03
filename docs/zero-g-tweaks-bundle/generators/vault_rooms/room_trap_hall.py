"""Concord Vault room 7/10: Trap Hall (doors N, S). Usage: python3 room_trap_hall.py <out_dir>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from room_kit import Room, Z, sheet

OUT = sys.argv[1]
r = Room('NS', seed=77)
P = lambda n, **k: Z + n + ('[' + ','.join(f'{a}={b}' for a, b in k.items()) + ']' if k else '')
BB, BRK, CRK, CHIS, CBLK = (P('polished_black_cerulean_stone_bricks'), P('cerulean_stone_bricks'), P('cracked_cerulean_stone_bricks'),
                            P('chiseled_cerulean_stone'), P('chiseled_polished_black_cerulean_stone'))
STONE, POL, SMOOTH, PLANK = P('cerulean_stone'), P('polished_cerulean_stone'), P('smooth_cerulean_stone'), P('shardwood_planks')
PLATE, FENCE, LAMP = P('shardwood_pressure_plate', powered='false'), P('shardwood_fence'), P('spectral_lantern')
BUD = lambda size, f='up': P(f'{size}_cerulite_bud', facing=f, waterlogged='false')
traps = []

# ---------------------------------------------------------------- shell, then solid fill behind the two inner walls (the hall is x 5-11)
for x in range(17):
    for z in range(17):
        edge = x in (0, 16) or z in (0, 16)
        r.put(x, 0, z, BB if edge else (SMOOTH if x in (5, 11) else POL))
        r.put(x, 8, z, BRK)
        for y in range(1, 8):
            if edge or x <= 3 or x >= 13: r.put(x, y, z, BB if (edge and y == 1) else STONE if not edge else (CRK if r.rng.random() < .12 else BRK))
r.open_doors()
for cells in (lambda i: (i, 0), lambda i: (i, 16)):
    for i in (5, 11):
        for y in range(1, 7): r.put(cells(i)[0], y, cells(i)[1], CBLK)
    for i in range(6, 11): r.put(cells(i)[0], 6, cells(i)[1], BB)
    r.put(cells(8)[0], 6, cells(8)[1], CBLK)
# inner walls x 4 and x 12: black plinth, cerulean bricks, a chiseled band, glyph panels over every dart slot
for z in range(1, 16):
    for x in (4, 12):
        for y in range(1, 8): r.put(x, y, z, BB if y == 1 else CHIS if y == 7 else BRK)
# vaulted ceiling: stepped arch over the hall
for z in range(1, 16):
    for x in (5, 11): r.put(x, 7, z, P('cerulean_stone_brick_stairs', facing='east' if x == 5 else 'west', half='top', shape='straight', waterlogged='false'))
    for x in (6, 10): r.put(x, 8, z, BRK)

def dart_slot(wx, z, facing):
    """dispenser in the inner wall at y 1, its plate on the hall cell in front, a glyph panel above it"""
    r.dart(wx, 1, z, facing)
    px = wx + (1 if facing == 'east' else -1)
    r.put(px, 0, z, PLANK); r.put(px, 1, z, PLATE); r.notes[(px, 1, z)] = 'plate'
    r.put(wx, 2, z, CBLK)
    traps.append(((wx, 1, z), (px, 1, z)))

# ---------------------------------------------------------------- the gauntlet: two fence lines force players through the trapped side gaps
for zf in (4, 12):
    for x in range(6, 11): r.put(x, 1, zf, FENCE)
    r.put(8, 2, zf, FENCE); r.put(8, 3, zf, LAMP)                                       # a lamp post in the middle of each line
    dart_slot(4, zf, 'east'); dart_slot(12, zf, 'west')
    for dz in (-1, 1):                                                                  # one more plate before and after each gap
        dart_slot(4, zf + dz, 'east'); dart_slot(12, zf + dz, 'west')
# decoy-free middle: the plates are on wood tiles, so a careful player can see every one ("watch the floor")

# ---------------------------------------------------------------- the rare chest's vault, behind the east wall, entered through a trapped gap
for z in range(6, 11):
    for x in range(13, 16):
        for y in range(1, 5): r.put(x, y, z, 'minecraft:air')
        r.put(x, 0, z, P('polished_black_cerulean_stone')); r.put(x, 5, z, CBLK)
for y in range(1, 4): r.put(12, y, 8, 'minecraft:air')                                 # 1-wide, 3-tall gap
r.put(12, 0, 8, PLANK); r.put(12, 1, 8, PLATE); r.notes[(12, 1, 8)] = 'plate (vault gap)'
r.dart(12, 1, 7, 'south', label='dart into the gap'); r.dart(12, 1, 9, 'north', label='dart into the gap')
traps += [((12, 1, 7), (12, 1, 8)), ((12, 1, 9), (12, 1, 8))]
r.put(12, 4, 8, CBLK)                                                                  # glyph over the gap
r.chest(15, 1, 8, 'west', 'rare', 'Vault chest')
for z, f in ((6, 'south'), (10, 'north')): r.put(15, 1, z, BUD('large', 'up')); r.put(13, 4, z, BUD('medium', 'down'))
r.put(16, 3, 8, LAMP)

# ---------------------------------------------------------------- lights: lanterns high in the inner walls, between the dart slots
for z in (2, 8, 14):
    r.put(4, 5, z, LAMP); r.put(12, 5, z, LAMP)
for z in (6, 10): r.put(8, 8, z, LAMP)
r.put(8, 8, 8, LAMP)

# check every plate really sits next to its dispenser (a pressure plate powers adjacent mechanisms directly)
for (dx, dy, dz), (px, py, pz) in traps:
    assert abs(dx - px) + abs(dz - pz) == 1 and dy == py, (dx, dz, px, pz)

n = r.save(f'{OUT}/trap_hall.nbt')
meta = {
 'title': 'Concord Vault · Room 7 · Trap Hall',
 'subtitle': '17 x 9 x 17 · doors north and south · 1 rare chest · 14 dart traps · can hold a Key Altar · template rooms/trap_hall.nbt',
 'story': ('The Concord tested their own here. The hall is a gauntlet: two fence lines cross it, and the only ways through are the '
           'gaps beside the dart walls, where every floor tile that is wood instead of stone is a pressure plate. Above each dart slot '
           'a black glyph warns you, for anyone who knows to look. The test is not speed but attention. Behind the east wall, '
           'through one last trapped gap, is the vault and what the Concord kept for those who passed.'),
 'hide_a': lambda x, y, z: y >= 7 or (y >= 2 and (x <= 4 or z == 16)),
 'hide_b': lambda x, y, z: y >= 7 or (y >= 2 and (z == 0 or x == 16 or x == 12 or (x >= 13 and not (6 <= z <= 10 and y <= 4)))),
 'view_a_title': 'Cutaway from the south-west (ceiling, south wall and west side cut to the dart line)',
 'view_b_title': 'Cutaway from the north-east (ceiling, north wall and east dart wall cut; vault opened)',
 'sections': [
  ('Zones', ['The hall (x 5-11): a 7-wide stone hall from the north door to the south door under a stepped brick arch. '
             'The black medallion where the Key Altar appears is in the middle, between the two fence lines.',
             'Fence lines (z 4 and z 12): fences across x 6-10 with a lamp post in the middle. The way through is the 1-block gap at '
             'each side (x 5 and x 11).',
             'Dart walls (x 4 and x 12): a dispenser at foot height beside each gap and one block before and after it, '
             'each with a pressure plate on a wood tile in front of it and a black glyph panel above it.',
             'Vault (x 13-15, z 6-10): through a 1-wide gap in the east wall, guarded by two darts that fire into the gap; '
             'the rare chest, large buds and a lamp inside.',
             'Behind the dart walls: solid stone, so the dispensers cannot be reached from behind.']),
  ('Traps and loot', ['14 dart traps: 12 at the fence gaps (3 per gap, both sides) and 2 at the vault gap.',
                      'Each dispenser holds 16 arrows and fires straight at the plate in front of it, so the dart hits whoever steps on it.',
                      'No wiring: a pressure plate powers the dispenser right next to it, so the traps work as soon as the room is placed.',
                      'Vault chest (15, 1, 8), faces west: chests/concord_vault/rare.',
                      'Tells: every plate sits on a wood tile in a stone floor, and every dart slot has a black glyph over it.']),
  ('Connectors', ['North door x 6-10, y 1-5 at z 0; jigsaw (8, 1, 0) facing north.',
                  'South door x 6-10, y 1-5 at z 16; jigsaw (8, 1, 16) facing south.',
                  'Jigsaws: name and target zerog_tweaks:door, pool zerog_tweaks:concord_vault/corridors, final state air, joint aligned.']),
  ('Gameplay', ['Each gap is 1 wide with a plate in it, so walking through always fires one dart; the plates before and after punish '
                'rushing. Players can break a fence to make a safe gap, or sneak along in armour; both are fair answers.',
                'When it is a key room, the Key Altar is between the fence lines, so players must pass one line to reach it and the other to leave '
                'by the far door, with 3 Prismling guardians chasing them over the plates.',
                'Darts run out after 16 shots each, so the hall gets safer the more it is used.']),
  ('Building it', ['Dispensers store their arrows in the file ({Items:[{Slot:0b,id:"minecraft:arrow",count:16}]}).',
                   'Keep each plate directly in front of its dispenser; the generator checks this.',
                   'Generator: generators/vault_rooms/room_trap_hall.py.']),
 ]}
print(n, 'blocks;', len(traps), 'traps;', sheet(r, meta, f'{OUT}/07_trap_hall.png'))
for t, ok in r.check(): print('PASS' if ok else 'FAIL', t)
