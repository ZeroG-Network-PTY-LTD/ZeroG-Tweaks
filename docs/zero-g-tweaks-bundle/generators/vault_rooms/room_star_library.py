"""Concord Vault room 6/10: Star Library (doors N, E, W). Usage: python3 room_star_library.py <out_dir>"""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from room_kit import Room, Z, sheet, CENTRE

OUT = sys.argv[1]
r = Room('NEW', seed=66)
P = lambda n, **k: Z + n + ('[' + ','.join(f'{a}={b}' for a, b in k.items()) + ']' if k else '')
BB, BRK, CHIS, CBLK = P('polished_black_cerulean_stone_bricks'), P('cerulean_stone_bricks'), P('chiseled_cerulean_stone'), P('chiseled_polished_black_cerulean_stone')
PLANK, LOGY, LOGX, LOGZ = P('shardwood_planks'), P('stripped_shardwood_log', axis='y'), P('stripped_shardwood_log', axis='x'), P('stripped_shardwood_log', axis='z')
SLAB_T, SLAB_B, FENCE = P('shardwood_slab', type='top', waterlogged='false'), P('shardwood_slab', type='bottom', waterlogged='false'), P('shardwood_fence')
SHELF, LAMP, PULSAR, CHAIN = 'minecraft:bookshelf', P('spectral_lantern'), P('pulsar_lamp'), 'minecraft:chain[axis=y,waterlogged=false]'
STAIR = lambda f, h='bottom': P('shardwood_stairs', facing=f, half=h, shape='straight', waterlogged='false')

# ---------------------------------------------------------------- shell: dark-panelled walls, Shardwood floor
for x in range(17):
    for z in range(17):
        edge = x in (0, 16) or z in (0, 16)
        r.put(x, 0, z, BB if edge else PLANK)
        r.put(x, 8, z, P('polished_black_cerulean_stone'))
        if edge:
            for y in range(1, 8): r.put(x, y, z, BB if y in (1, 7) else BRK)
for a in (3, 13):
    for y in range(1, 8): r.put(a, y, 0, LOGY); r.put(0, y, a, LOGY); r.put(16, y, a, LOGY); r.put(a, y, 16, LOGY)
r.open_doors()
for cells in (lambda i: (i, 0), lambda i: (0, i), lambda i: (16, i)):
    for i in (5, 11):
        for y in range(1, 7): r.put(cells(i)[0], y, cells(i)[1], CBLK)
    for i in range(6, 11): r.put(cells(i)[0], 6, cells(i)[1], BB)
    r.put(cells(8)[0], 6, cells(8)[1], CHIS)

# ---------------------------------------------------------------- floor: a star chart inlaid around the medallion
for x in range(1, 16):
    for z in range(1, 12):
        dd = math.hypot(x - 8, z - 8)
        if 4.0 <= dd <= 4.9: r.put(x, 0, z, P('smooth_cerulean_stone'))
        elif dd < 4.0: r.put(x, 0, z, P('polished_cerulean_stone'))
for k in range(8):                                                     # eight "stars" on the ring
    a = k * math.pi / 4; x, z = round(8 + 4.5 * math.cos(a)), round(8 + 4.5 * math.sin(a))
    if z < 12: r.put(x, 0, z, CBLK)
for x in range(7, 10):
    for z in range(7, 10): r.put(x, 0, z, P('polished_black_cerulean_stone'))
r.put(8, 0, 8, CBLK)

# ---------------------------------------------------------------- bookshelf walls (floor to ceiling where there is no door)
def shelves(cells, y0=1, y1=6):
    for (x, z) in cells:
        for y in range(y0, y1 + 1): r.put(x, y, z, SHELF)
shelves([(x, 1) for x in (1, 2, 4)] + [(x, 1) for x in (12, 14, 15)])                       # north wall, beside the door
shelves([(1, z) for z in (2, 4)] + [(15, z) for z in (2, 4)])                               # east and west walls, north part
for (x, z) in ((3, 1), (13, 1), (1, 3), (15, 3)):                                           # posts between the shelves carry lamps
    for y in range(1, 7): r.put(x, y, z, LOGY)
    r.put(x, 5, z, LAMP)

# ---------------------------------------------------------------- the gallery: a balcony along the south wall (walk at y 4)
for x in range(1, 16):
    for z in range(12, 16): r.put(x, 3, z, SLAB_T)
for x in range(2, 16):
    r.put(x, 4, 12, FENCE)                                                                  # railing
for x in (4, 8, 12):
    for y in (1, 2): r.put(x, y, 12, LOGY)                                                  # posts holding the balcony up
    r.put(x, 3, 12, LOGX)
shelves([(x, 15) for x in range(1, 16)], 1, 2)                                              # under the balcony
shelves([(x, 15) for x in range(1, 16) if x != 8], 4, 7)                                    # above it, to the ceiling
shelves([(1, z) for z in (13, 14)] + [(15, z) for z in (13, 14)], 4, 6)
# stairs up to the gallery: three steps rising east along its front edge, arriving through a gap in the railing
for x, y in ((2, 1), (3, 2), (4, 3)):
    r.put(x, y, 11, STAIR('east'))
    for yy in range(1, y): r.put(x, yy, 11, PLANK)
r.put(4, 4, 12, 'minecraft:air'); r.put(5, 4, 12, 'minecraft:air')                       # gap in the railing
# gallery furniture: the chart alcove (lectern with a Concord log), a cartography table, the upstairs chest, an orrery lamp
book = {'id': 'minecraft:written_book', 'count': 1, 'components': {'minecraft:written_book_content': {
    'title': {'raw': 'Quiet Mines: Chart 7'}, 'author': 'Concord Archivist',
    'pages': [{'raw': json.dumps({'text': 'The sky over the Quiet Mines, as we chart it. Eleven bright stars, one dark one that moves.'})},
              {'raw': json.dumps({'text': 'The dark star is closer every season. Vael says it is nothing. The Sentinel was told to test anyone who comes after us.'})},
              {'raw': json.dumps({'text': 'If you are reading this, you found the Vault. Find the four keys. Answer the Sentinel truthfully.'})}]}}}
r.put(8, 4, 15, 'minecraft:lectern[facing=north,has_book=true,powered=false]',
      {'id': 'minecraft:lectern', 'Book': book, 'Page': 0}); r.notes[(8, 4, 15)] = 'lectern + Concord log'
r.put(8, 6, 15, PULSAR); r.put(8, 5, 15, 'minecraft:air'); r.put(8, 7, 15, CBLK)
r.put(5, 4, 14, 'minecraft:cartography_table')
r.chest(13, 4, 14, 'north', 'uncommon', "Archivist's chest (gallery)")
r.put(11, 4, 14, FENCE); r.put(11, 5, 14, LAMP)                                             # orrery-style lamp on a post

# ---------------------------------------------------------------- reading tables (north half) and a nook under the gallery
for cx in (3, 12):
    for x in (cx, cx + 1): r.put(x, 1, 6, SLAB_T); r.put(x, 1, 8, 'minecraft:air')
    r.put(cx, 1, 5, STAIR('north')); r.put(cx + 1, 1, 5, STAIR('north'))
    r.put(cx, 1, 7, STAIR('south')); r.put(cx + 1, 1, 7, STAIR('south'))
    r.put(cx, 2, 6, LAMP if cx == 3 else 'minecraft:air')
r.put(13, 2, 6, LAMP)
r.chest(14, 1, 14, 'north', 'common', 'Reading-nook chest (under the gallery)')
r.put(13, 1, 14, STAIR('east')); r.put(12, 1, 14, SLAB_T)

# ---------------------------------------------------------------- lights: a chandelier over the star chart, lamps in the ceiling like stars
for y in (6, 7): r.put(8, y, 8, CHAIN)
r.put(8, 5, 8, LAMP)
for x, z in ((8, 4), (5, 8), (11, 8), (4, 4), (12, 4), (8, 10)): r.put(x, 8, z, LAMP)
for x, z in ((4, 14), (12, 13), (2, 13)): r.put(x, 2, z, 'minecraft:air')
r.put(6, 8, 13, LAMP); r.put(10, 8, 13, LAMP)
for x in (6, 10): r.put(x, 2, 13, LAMP)                                                      # lamps under the gallery, lighting the nook

n = r.save(f'{OUT}/star_library.nbt')
meta = {
 'title': 'Concord Vault · Room 6 · Star Library',
 'subtitle': '17 x 9 x 17 · doors north, east and west · 1 common + 1 uncommon chest · lore lectern · can hold a Key Altar · template rooms/star_library.nbt',
 'story': ('The Concord charted Cerulon\'s sky from the Quiet Mines, and this is where they kept the charts: shelves to the ceiling, '
           'reading tables, a gallery along the south wall and a star map set into the floor. One chart is still open on the gallery '
           'lectern, and it is the first place in the Vault that tells the player what happened here: a dark star that moved, a leader '
           'who said it was nothing, and a Sentinel left to test whoever came after.'),
 'sections': [
  ('Zones', ['Star chart (floor): a stone circle around the black medallion with eight dark "stars" on its ring. The Key Altar appears '
             'in the middle; a chandelier hangs over it.',
             'Bookshelf walls: floor to ceiling beside the north door and on the east and west walls, split by Shardwood posts with lamps.',
             'Reading tables: two tables with stools on both sides, north half of the room, one with a reading lamp.',
             'Gallery (south): a balcony at walking height 4, reached by three steps rising east along its front (a gap in the railing at x 4-5), with posts and beams under it.',
             'On the gallery: the chart alcove (lectern with the Concord log under a pulsar lamp), a cartography table, an orrery lamp and the uncommon chest.',
             'Under the gallery: a reading nook with the common chest, lit by lamps set under the balcony.']),
  ('Loot and lore', ["Archivist's chest (13, 4, 14) on the gallery, faces north: chests/concord_vault/uncommon.",
                     'Reading-nook chest (14, 1, 14) under the gallery, faces north: common.',
                     'Lectern (8, 4, 15): a written book, "Quiet Mines: Chart 7" by the Concord Archivist, 3 pages of lore '
                     '(the moving dark star, Vael dismissing it, the Sentinel\'s orders and a hint about the four keys).',
                     'Bookshelves drop books, as in vanilla; that is fine (no valuable loot).']),
  ('Connectors', ['North door x 6-10, y 1-5 at z 0; jigsaw (8, 1, 0) facing north.',
                  'East door z 6-10, y 1-5 at x 16; jigsaw (16, 1, 8) facing east.',
                  'West door z 6-10, y 1-5 at x 0; jigsaw (0, 1, 8) facing west.',
                  'Jigsaws: name and target zerog_tweaks:door, pool zerog_tweaks:concord_vault/corridors, final state air, joint aligned.']),
  ('Gameplay', ['A story room: no spawner, no traps. The lectern is the reward as much as the chests.',
                'The gallery gives height; when it is a key room, players can fight the 3 Prismling guardians from the railing.',
                'The best chest is upstairs, so players who only sweep the floor miss it.']),
  ('Building it', ['The book is stored on the lectern as an item with the 1.21.1 written-book component (pages as JSON text). '
                   'Check it opens in game; if not, write the book in game and place it on the lectern before saving the structure.',
                   'The Book tag uses Echo-era lore; edit the pages in room_star_library.py to change it.',
                   'Generator: generators/vault_rooms/room_star_library.py.']),
 ]}
print(n, 'blocks;', sheet(r, meta, f'{OUT}/06_star_library.png'))
for t, ok in r.check(): print('PASS' if ok else 'FAIL', t)
