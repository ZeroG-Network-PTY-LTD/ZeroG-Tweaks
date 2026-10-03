"""Concord Vault templates (owner 2026-10-03). Writes data/zerog_tweaks/structure/concord_vault/*.nbt:

  chamber.nbt               the Sentinel chamber shell (v3 arena layout with 4 doorways), Concord Lock at the prism spot
  chamber_stage_1..3.nbt    what each key builds: 1 lit floor, 2 dais + refractor pylons, 3 stands + rails + crystal dome
                            (only their own blocks, no air, so placing them adds to the shell)
  corridor_*.nbt            5 x 5 mine corridors (straight, turn, junction, crossing) and a dead-end cap
  entrance_shaft.nbt        tunnel + 46-block spiral stair up to a shrine on the surface
  rooms/<design>.nbt        the 10 room designs (17 x 9 x 17, doors 5 x 5 at side centres, centre 3x3 kept free for
                            the Key Altar the structure may put there), chests on concord_vault loot tables

Jigsaw convention: every connector is a minecraft:jigsaw on the doorway's floor+1 cell at the piece edge, facing out,
name = target = zerog_tweaks:door, final_state air. Chamber S/E/W -> corridors pool, chamber N -> entrance pool,
corridors -> branches pool (rooms + corridors), rooms -> corridors pool; fallback caps.
"""
import math, os, random, sys
import nbtlib
from nbtlib import Compound, List, Int, String, Double, Byte

OUT = sys.argv[1] if len(sys.argv) > 1 else 'C:/zt-tmp/w/src/main/resources/data/zerog_tweaks/structure/concord_vault/'
Z = 'zerog_tweaks:'
DATA_VERSION = 3955


def to_nbt(v):
    if isinstance(v, (Compound, List, Int, String, Double, Byte)): return v
    if isinstance(v, bool): return Byte(1 if v else 0)
    if isinstance(v, int): return Int(v)
    if isinstance(v, float): return Double(v)
    if isinstance(v, str): return String(v)
    if isinstance(v, dict): return Compound({k: to_nbt(x) for k, x in v.items()})
    if isinstance(v, list):
        items = [to_nbt(x) for x in v]
        return List[type(items[0])](items) if items else List[Compound]([])
    raise TypeError(v)


class Piece:
    def __init__(self, sx, sy, sz):
        self.size = (sx, sy, sz)
        self.blocks = {}   # (x, y, z) -> (state, nbt dict or None)
        self.entities = []

    def put(self, x, y, z, state, nbt=None):
        if 0 <= x < self.size[0] and 0 <= y < self.size[1] and 0 <= z < self.size[2]:
            self.blocks[(x, y, z)] = (state, nbt)

    def fill(self, x0, y0, z0, x1, y1, z1, state):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    self.put(x, y, z, state)

    def jigsaw(self, x, y, z, facing, pool):
        self.put(x, y, z, f'minecraft:jigsaw[orientation={facing}_up]', {
            'id': 'minecraft:jigsaw', 'name': Z + 'door', 'target': Z + 'door', 'pool': pool,
            'final_state': 'minecraft:air', 'joint': 'aligned', 'placement_priority': 0, 'selection_priority': 0})

    def chest(self, x, y, z, facing, table):
        self.put(x, y, z, f'minecraft:chest[facing={facing},type=single,waterlogged=false]',
                 {'id': 'minecraft:chest', 'LootTable': Z + 'chests/concord_vault/' + table})

    def save(self, path):
        palette, index, blocks = [], {}, []
        for (x, y, z), (state, nbt) in sorted(self.blocks.items(), key=lambda kv: (kv[0][1], kv[0][2], kv[0][0])):
            if state not in index:
                index[state] = len(palette); palette.append(state)
            b = {'pos': List[Int]([Int(x), Int(y), Int(z)]), 'state': Int(index[state])}
            if nbt: b['nbt'] = to_nbt(nbt)
            blocks.append(Compound(b))
        pal = []
        for state in palette:
            name, props = (state[:-1].split('[', 1) if '[' in state else (state, ''))
            c = {'Name': String(name)}
            if props:
                c['Properties'] = Compound({k: String(v) for k, v in (p.split('=') for p in props.split(','))})
            pal.append(Compound(c))
        ents = [Compound({'pos': List[Double]([Double(a) for a in pos]), 'blockPos': List[Int]([Int(a) for a in bpos]),
                          'nbt': to_nbt(nbt)}) for pos, bpos, nbt in self.entities]
        root = Compound({'DataVersion': Int(DATA_VERSION), 'size': List[Int]([Int(a) for a in self.size]),
                         'palette': List[Compound](pal), 'blocks': List[Compound](blocks), 'entities': List[Compound](ents)})
        os.makedirs(os.path.dirname(path), exist_ok=True)
        nbtlib.File(root, root_name='').save(path, gzipped=True)
        return len(blocks)


# =========================================================================================================================
# Chamber: run the v3 arena builder with 4 doorways, recording which stage each block belongs to
# =========================================================================================================================
src = open('C:/zt-tmp/build_prism_arena_v3.py', encoding='utf-8').read()
src = src[:src.index('# ---- NBT')]
src = src.replace('def entrance(dx, dz):\n    return dz > 0 and abs(dx) <= 3', 'def entrance(dx, dz):\n    return abs(dx) <= 3 or abs(dz) <= 3')
src = src.replace('    if k == 2:      # 90 degrees = south = entrance: the arch takes that spot', '    if k % 2 == 0:  # the four doorways')
src = src.replace('put(0, FLOOR + 3, 0, Z + "concord_prism[state=idle]")', '')
arch_start = src.index('# ---- entrance arch')
arch_end = src.index('# ---- dome')
arch = src[arch_start:arch_end]
arch_body = '\n'.join('    ' + line if line.strip() else line for line in arch.splitlines())
src = src[:arch_start] + '''# ---- four doorway arches (the v3 south arch, turned to each side) ---------------------------------------------------------
def _arch(put):
''' + arch_body + '''
    for dz in range(30, 34):
        for dx in range(-3, 4):
            for y in range(FLOOR + 1, FLOOR + 10):
                put(dx, y, dz, "minecraft:air")
_real_put = put
for _turn in range(4):
    def _rot_put(dx, y, dz, b, _t=_turn):
        for _ in range(_t):
            dx, dz = -dz, dx
        _real_put(dx, y, dz, b)
    _arch(_rot_put)

''' + src[arch_end:]
STAGE_AT = [('# ---- clear the inside', 0), ('# ---- foundation and fight floor', 0), ('# ---- dais', 2),
            ('# ---- 4 refractor pylons', 2), ('# ---- tiered stands', 3), ('# ---- outer wall', 0),
            ('CROWNS = []', 0), ('# ---- four doorway arches', 0), ('# ---- dome', 3)]
for marker, stage in STAGE_AT:
    i = src.index(marker)
    src = src[:i] + f'STAGE = {stage}\n' + src[i:]
src = src.replace('B = {}        # (x, y, z) -> block state string, template-local', 'B = {}\nWRITES = []\nSTAGE = 0')
src = src.replace('''def put(dx, y, dz, block):
    x, z = C + dx, C + dz
    if 0 <= x < SX and 0 <= y < SY and 0 <= z < SZ:
        B[(x, y, z)] = block''', '''def put(dx, y, dz, block):
    x, z = C + dx, C + dz
    if 0 <= x < SX and 0 <= y < SY and 0 <= z < SZ:
        B[(x, y, z)] = block
        WRITES.append(((x, y, z), block, STAGE))''')
assert 'WRITES.append' in src and 'WRITES = []' in src
g = {'__name__': 'v3', '__file__': 'build_prism_arena_v3.py'}
exec(compile(src, 'build_prism_arena_v3(vault)', 'exec'), g)
SX, SY, SZ, C, FLOOR = g['SX'], g['SY'], g['SZ'], g['C'], g['FLOOR']

shell = Piece(SX, SY, SZ)
stages = {1: Piece(SX, SY, SZ), 2: Piece(SX, SY, SZ), 3: Piece(SX, SY, SZ)}
FLOOR_DETAIL = {Z + 'pulsar_lamp', Z + 'smooth_cerulean_stone', Z + 'polished_black_cerulean_stone_bricks'}
for (x, y, z), block, stage in g['WRITES']:
    if stage == 0:
        r = math.hypot(x - C, z - C)
        if y == FLOOR and r <= 22.9 and block in FLOOR_DETAIL:
            shell.put(x, y, z, Z + 'polished_cerulean_stone')     # plain floor until the first key
            stages[1].put(x, y, z, block)
        else:
            shell.put(x, y, z, block)
    elif block != 'minecraft:air':
        stages[stage].put(x, y, z, block)
for ex, ey, ez, bx, by, bz in g['ENTITIES']:                     # rails and minecarts belong to the stands
    stages[3].entities.append(((ex, ey, ez), (bx, by, bz), {'id': 'minecraft:minecart', 'Pos': [ex, ey, ez]}))
shell.put(C, FLOOR + 1, C, Z + 'polished_black_cerulean_stone')   # the lock on a plinth where the prism will stand
shell.put(C, FLOOR + 2, C, Z + 'polished_black_cerulean_stone')
shell.put(C, FLOOR + 3, C, Z + 'concord_lock[facing=south,stage=0]')
shell.jigsaw(C, FLOOR + 1, SZ - 1, 'south', Z + 'concord_vault/corridors')
shell.jigsaw(SX - 1, FLOOR + 1, C, 'east', Z + 'concord_vault/corridors')
shell.jigsaw(0, FLOOR + 1, C, 'west', Z + 'concord_vault/corridors')
shell.jigsaw(C, FLOOR + 1, 0, 'north', Z + 'concord_vault/entrance')
counts = {'chamber': shell.save(OUT + 'chamber.nbt')}
for n, p in stages.items():
    counts[f'chamber_stage_{n}'] = p.save(OUT + f'chamber_stage_{n}.nbt')

# =========================================================================================================================
# Corridors: 7 wide (5 inside), 7 tall (5 inside), mine-style with Shardwood supports
# =========================================================================================================================
rng = random.Random(9071)
STONE = [Z + 'cerulean_stone'] * 6 + [Z + 'cobbled_cerulean_stone'] * 3 + [Z + 'cracked_cerulean_stone_bricks']
BRANCH = Z + 'concord_vault/branches'


def rock():
    return rng.choice(STONE)


def tunnel(p, cells):
    """cells: set of (x, z) floor cells of the 5-wide passage; wraps them in rock, clears 5 high, brick floor."""
    for (x, z) in cells:
        p.put(x, 0, z, rng.choice([Z + 'cerulean_stone_bricks', Z + 'cerulean_stone_bricks', Z + 'cracked_cerulean_stone_bricks']))
        for y in range(1, 6):
            p.put(x, y, z, 'minecraft:air')
        p.put(x, 6, z, rock())
    for (x, z) in cells:
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            n = (x + dx, z + dz)
            if n not in cells and 0 <= n[0] < p.size[0] and 0 <= n[1] < p.size[2] and (n[0], 1, n[1]) not in p.blocks:
                for y in range(0, 7):
                    p.put(n[0], y, n[1], rock())


def support(p, z, x0=1, x1=5):
    for y in range(1, 5):
        p.put(x0, y, z, Z + 'shardwood_log[axis=y]')
        p.put(x1, y, z, Z + 'shardwood_log[axis=y]')
    for x in range(x0, x1 + 1):
        p.put(x, 5, z, Z + 'shardwood_planks')
    p.put((x0 + x1) // 2, 4, z, Z + 'spectral_lantern')


def corridor(name, openings):
    if name == 'corridor_straight':
        p = Piece(7, 7, 13)
        tunnel(p, {(x, z) for x in range(1, 6) for z in range(0, 13)})
        for z in (2, 10):
            support(p, z)
        for z in range(0, 13):
            if z not in (2, 10):
                p.put(3, 1, z, 'minecraft:rail[shape=north_south,waterlogged=false]')
        p.jigsaw(3, 1, 0, 'north', BRANCH)
        p.jigsaw(3, 1, 12, 'south', BRANCH)
        return p
    p = Piece(7, 7, 7)
    cells = {(x, z) for x in range(1, 6) for z in range(1, 6)}
    ends = {'N': ((3, 0), 'north', [(x, 0) for x in range(1, 6)]), 'S': ((3, 6), 'south', [(x, 6) for x in range(1, 6)]),
            'E': ((6, 3), 'east', [(6, z) for z in range(1, 6)]), 'W': ((0, 3), 'west', [(0, z) for z in range(1, 6)])}
    for o in openings:
        cells |= set(ends[o][2])
    tunnel(p, cells)
    for x, z in ((1, 1), (5, 1), (1, 5), (5, 5)):
        for y in range(1, 6):
            p.put(x, y, z, Z + 'shardwood_log[axis=y]')
    p.put(3, 5, 3, Z + 'spectral_lantern')
    for o in openings:
        (jx, jz), facing, _ = ends[o]
        p.jigsaw(jx, 1, jz, facing, BRANCH)
    return p


for name, openings in (('corridor_straight', None), ('corridor_turn', 'NE'), ('corridor_junction', 'NEW'), ('corridor_crossing', 'NESW')):
    counts[name] = corridor(name, openings).save(OUT + f'{name}.nbt')

cap = Piece(7, 7, 3)
tunnel(cap, {(x, z) for x in range(1, 6) for z in range(0, 2)})
cap.fill(1, 1, 2, 5, 5, 2, Z + 'cerulean_stone_bricks')
cap.put(3, 3, 2, Z + 'spectral_lantern')
cap.put(1, 1, 1, Z + 'cobbled_cerulean_stone'); cap.put(5, 1, 1, Z + 'cobbled_cerulean_stone')
cap.jigsaw(3, 1, 0, 'north', 'minecraft:empty')
counts['corridor_cap'] = cap.save(OUT + 'corridor_cap.nbt')

# =========================================================================================================================
# Entrance shaft: tunnel, then a 7 x 7 stair tower spiralling 46 up to a shrine (chamber floor is 45 below the surface)
# =========================================================================================================================
H = 46
sh = Piece(9, H + 7, 16)
tunnel(sh, {(x, z) for x in range(2, 7) for z in range(0, 8)})
support(sh, 3, 2, 6)
sh.fill(0, 0, 8, 8, H + 5, 15, Z + 'cerulean_stone_bricks')              # tower shell
for x in range(0, 9):
    if x < 2 or x > 6:
        sh.fill(x, 0, 7, x, H + 5, 7, Z + 'cerulean_stone_bricks')
cx, cz = 4, 11
CORE = {(a, b) for a in range(3, 6) for b in range(10, 13)}
band = [(x, z) for x in range(1, 8) for z in range(8, 15) if (x, z) not in CORE]
start_angle = math.atan2(7 - cz, 4 - cx)   # stairs start beside the tunnel opening


def step_bin(x, z):
    return int(((math.atan2(z - cz, x - cx) - start_angle) % (2 * math.pi)) / (2 * math.pi) * 24)


for (x, z) in band:
    for y in range(1, H + 5):
        sh.put(x, y, z, 'minecraft:air')
for (x, z) in band:
    for loop in range(3):
        y = step_bin(x, z) + loop * 24
        if 0 <= y < H:
            sh.put(x, y, z, Z + 'polished_cerulean_stone')
for y in range(0, H + 5):                                                # the core, lit every 6
    for (x, z) in CORE:
        lamp = y % 6 == 3 and (x, z) != (cx, cz)
        sh.put(x, y, z, Z + ('spectral_lantern' if lamp else 'polished_black_cerulean_stone_bricks'))
for (x, z) in band:                                                       # landing, open above the last steps
    if not 18 <= step_bin(x, z) <= 21:
        sh.put(x, H, z, Z + 'polished_cerulean_stone')
for y in range(H + 1, H + 5):                                             # shrine: arches to all four sides
    for x in range(0, 9):
        for z in range(7, 16):
            edge = x in (0, 8) or z in (7, 15)
            door = (x in (0, 8) and 10 <= z <= 12) or (z in (7, 15) and 3 <= x <= 5)
            if edge:
                sh.put(x, y, z, 'minecraft:air' if door and y <= H + 3 else Z + 'polished_black_cerulean_stone_bricks')
            elif (x, z) not in CORE:
                sh.put(x, y, z, 'minecraft:air')
sh.fill(0, H + 5, 7, 8, H + 5, 15, Z + 'chiseled_polished_black_cerulean_stone')
sh.put(4, H + 5, 11, Z + 'pulsar_lamp')
for x, z in ((0, 7), (8, 7), (0, 15), (8, 15)):
    sh.put(x, H + 6, z, Z + 'cerulite_cluster[facing=up,waterlogged=false]')
sh.jigsaw(4, 1, 0, 'north', BRANCH)
counts['entrance_shaft'] = sh.save(OUT + 'entrance_shaft.nbt')

# =========================================================================================================================
# Rooms: 17 x 9 x 17, floor y 0, ceiling y 8, doors 5 wide x 5 tall at side centres
# =========================================================================================================================
CORR = Z + 'concord_vault/corridors'
DOORS = {'N': ('north', (8, 0), lambda i: (i, 0)), 'S': ('south', (8, 16), lambda i: (i, 16)),
         'W': ('west', (0, 8), lambda i: (0, i)), 'E': ('east', (16, 8), lambda i: (16, i))}
CENTRE = {(x, z) for x in range(7, 10) for z in range(7, 10)}


def room(doors, floor=Z + 'polished_cerulean_stone', wall=Z + 'cerulean_stone_bricks', ceiling=Z + 'cerulean_stone'):
    p = Piece(17, 9, 17)
    for x in range(17):
        for z in range(17):
            p.put(x, 0, z, floor)
            p.put(x, 8, z, ceiling)
            for y in range(1, 8):
                edge = x in (0, 16) or z in (0, 16)
                p.put(x, y, z, (rng.choice([wall, wall, wall, Z + 'cracked_cerulean_stone_bricks']) if edge else 'minecraft:air'))
    for d in doors:
        facing, (jx, jz), at = DOORS[d]
        for i in range(6, 11):
            x, z = at(i)
            for y in range(1, 6):
                p.put(x, y, z, 'minecraft:air')
        p.jigsaw(jx, 1, jz, facing, CORR)
    for x, z in ((4, 4), (12, 4), (4, 12), (12, 12)):
        p.put(x, 7, z, Z + 'spectral_lantern')
    return p


def free(x, z):
    return (x, z) not in CENTRE


def is_air(p, x, y, z):
    return p.blocks.get((x, y, z), ('minecraft:air',))[0] == 'minecraft:air'


def r_storage_hall():
    p = room('NSE', floor=Z + 'shardwood_planks')
    for z in range(2, 15, 3):
        for x in (1, 15):
            for y in (1, 2, 3):
                p.put(x, y, z, 'minecraft:barrel[facing=up,open=false]' if y < 3 else Z + 'shardwood_slab[type=bottom,waterlogged=false]')
    for x in range(3, 14, 4):
        p.put(x, 1, 14, Z + 'shardwood_planks'); p.put(x, 2, 14, Z + 'shardwood_planks')
    p.chest(2, 1, 14, 'north', 'common'); p.chest(14, 1, 2, 'west', 'common'); p.chest(2, 1, 2, 'east', 'common')
    return p


def r_crystal_garden():
    p = room('NW', floor=Z + 'azure_moss')
    for _ in range(40):
        x, z = rng.randint(2, 14), rng.randint(2, 14)
        if free(x, z) and is_air(p, x, 1, z):
            p.put(x, 1, z, rng.choice([Z + 'starbloom', Z + 'cerulite_cluster[facing=up,waterlogged=false]']))
    for x in range(2, 15, 3):
        for z in range(2, 15, 3):
            p.put(x, 8, z, Z + 'shimmer_glass'); p.put(x, 7, z, Z + 'cerulite_cluster[facing=down,waterlogged=false]')
    p.chest(14, 1, 14, 'north', 'uncommon')
    return p


def r_starlight_pool():
    p = room('NS', floor=Z + 'cerulean_geode_shell')
    for x in range(2, 15):
        for z in range(2, 15):
            r = math.hypot(x - 8, z - 8)
            if 2.6 < r <= 5.6:
                p.put(x, 0, z, Z + 'liquid_starlight[level=0]')
            elif 5.6 < r <= 6.4:
                p.put(x, 1, z, Z + 'smooth_cerulean_stone_slab[type=bottom,waterlogged=false]')
    p.chest(14, 1, 8, 'west', 'rare')
    return p


def r_collapsed_mine():
    p = room('NE', floor=Z + 'cobbled_cerulean_stone')
    for _ in range(14):                                               # rubble piles along the walls
        x, z = rng.choice([(rng.randint(1, 15), rng.choice([1, 2, 14, 15])), (rng.choice([1, 2, 14, 15]), rng.randint(1, 15))])
        if (x, z) in ((8, 1), (8, 2), (15, 8), (14, 8)):
            continue
        for y in range(1, rng.randint(2, 4)):
            p.put(x, y, z, rock())
    for x in range(3, 14):                                            # a fallen support beam
        if free(x, 12):
            p.put(x, 1, 12, Z + 'shardwood_log[axis=x]')
    for z in range(1, 16):
        if free(4, z) and z != 12:
            p.put(4, 1, z, 'minecraft:rail[shape=north_south,waterlogged=false]')
    p.entities.append(((4.5, 1.0625, 13.5), (4, 1, 13), {'id': 'minecraft:chest_minecart', 'Pos': [4.5, 1.0625, 13.5],
                                                         'LootTable': Z + 'chests/concord_vault/common'}))
    p.chest(14, 1, 3, 'west', 'common')
    return p


def r_prismling_nest():
    p = room('NSW', floor=Z + 'cobbled_cerulean_stone')
    for _ in range(30):
        x, z = rng.randint(2, 14), rng.randint(2, 14)
        if free(x, z) and not (6 <= x <= 10 or 6 <= z <= 10):         # keep the walkways between the doors clear
            h = rng.randint(1, 3)
            for y in range(1, h + 1):
                p.put(x, y, z, Z + 'cerulean_geode_shell')
            p.put(x, h + 1, z, Z + 'cerulite_cluster[facing=up,waterlogged=false]')
    p.put(13, 1, 13, 'minecraft:spawner', {'id': 'minecraft:mob_spawner', 'Delay': 20, 'MinSpawnDelay': 200,
                                           'MaxSpawnDelay': 600, 'SpawnCount': 2, 'MaxNearbyEntities': 5,
                                           'RequiredPlayerRange': 12, 'SpawnRange': 4,
                                           'SpawnData': {'entity': {'id': Z + 'prismling'}}})
    for y in range(2, 5):
        p.put(13, y, 13, 'minecraft:air')
    p.chest(2, 1, 14, 'north', 'uncommon')
    return p


def r_star_library():
    p = room('NEW', floor=Z + 'shardwood_planks')
    for z in range(1, 16):
        for x in (1, 15):
            if not (6 <= z <= 10):
                for y in range(1, 6):
                    p.put(x, y, z, 'minecraft:bookshelf')
    for x in range(2, 15):
        if not (6 <= x <= 10):
            for y in range(1, 6):
                p.put(x, y, 15, 'minecraft:bookshelf')
    p.put(8, 1, 13, 'minecraft:lectern[facing=north,has_book=false,powered=false]')
    p.put(4, 1, 4, Z + 'pulsar_lamp'); p.put(12, 1, 4, Z + 'pulsar_lamp')
    p.chest(3, 1, 13, 'north', 'common'); p.chest(13, 1, 13, 'north', 'uncommon')
    return p


def r_trap_hall():
    p = room('NS')
    for z in (4, 12):
        for x in (1, 15):
            facing = 'east' if x == 1 else 'west'
            p.put(x, 2, z, f'minecraft:dispenser[facing={facing},triggered=false]', {
                'id': 'minecraft:dispenser', 'Items': [{'Slot': Byte(0), 'id': 'minecraft:arrow', 'count': 16}]})
            p.put(x + (1 if x == 1 else -1), 1, z, 'minecraft:stone_pressure_plate[powered=false]')
    p.put(13, 1, 14, Z + 'chiseled_polished_black_cerulean_stone')
    p.chest(13, 2, 14, 'north', 'rare')
    return p


def r_forge():
    p = room('NE', floor=Z + 'smooth_cerulean_stone')
    for x in range(2, 7):
        p.put(x, 1, 15, 'minecraft:blast_furnace[facing=north,lit=false]' if x % 2 else 'minecraft:furnace[facing=north,lit=false]')
    p.put(12, 1, 13, 'minecraft:anvil[facing=west]'); p.put(13, 1, 13, 'minecraft:smithing_table')
    for z in range(2, 6):
        p.put(1, 1, z, Z + 'polished_black_cerulean_stone_bricks'); p.put(1, 2, z, 'minecraft:cauldron')
    p.put(14, 1, 3, Z + 'pulsar_lamp')
    p.chest(14, 1, 14, 'west', 'uncommon')
    return p


def r_observatory():
    p = room('N', floor=Z + 'polished_black_cerulean_stone')
    for x in range(1, 16):
        for z in range(1, 16):
            if 6.5 <= math.hypot(x - 8, z - 8) <= 7.3 and free(x, z):
                p.put(x, 0, z, Z + 'pulsar_lamp')                       # a star-chart ring in the floor
    for x, z in ((3, 3), (13, 3), (3, 13), (13, 13)):
        p.put(x, 0, z, Z + 'pulsar_lamp')
    for y in range(1, 5):
        p.put(13, y, 4, Z + 'shardwood_fence[east=false,north=false,south=false,west=false,waterlogged=false]')
    p.put(13, 5, 4, Z + 'crystal_glass'); p.put(12, 5, 4, Z + 'crystal_glass')   # the telescope
    for x in range(5, 12):
        for z in range(5, 12):
            p.put(x, 8, z, Z + 'crystal_glass')
    p.chest(3, 1, 14, 'east', 'rare')
    return p


def r_concord_shrine():
    p = room('NSEW', floor=Z + 'polished_cerulean_stone')
    for x, z in ((3, 3), (13, 3), (3, 13), (13, 13)):
        for y in range(1, 7):
            p.put(x, y, z, Z + ('chiseled_polished_black_cerulean_stone' if y in (1, 6) else 'polished_black_cerulean_stone_bricks'))
        p.put(x, 7, z, Z + 'cerulite_cluster[facing=up,waterlogged=false]')
    for x in range(2, 15):
        for z in range(2, 15):
            if abs(math.hypot(x - 8, z - 8) - 4.5) < 0.5 and free(x, z):
                p.put(x, 0, z, Z + 'pulsar_lamp')
    p.chest(3, 1, 2, 'south', 'rare')
    return p


ROOMS = {'storage_hall': r_storage_hall, 'crystal_garden': r_crystal_garden, 'starlight_pool': r_starlight_pool,
         'collapsed_mine': r_collapsed_mine, 'prismling_nest': r_prismling_nest, 'star_library': r_star_library,
         'trap_hall': r_trap_hall, 'forge': r_forge, 'observatory': r_observatory, 'concord_shrine': r_concord_shrine}
for name, make in ROOMS.items():
    p = make()
    for (x, z) in CENTRE:                                              # the Key Altar spot stays clear
        assert p.blocks[(x, 0, z)][0] != 'minecraft:air', name
        for y in range(1, 4):
            assert is_air(p, x, y, z), (name, x, y, z, p.blocks.get((x, y, z)))
    counts['rooms/' + name] = p.save(OUT + f'rooms/{name}.nbt')

for k, v in counts.items():
    print(f'{v:7d}  {k}')
