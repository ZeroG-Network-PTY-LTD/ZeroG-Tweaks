"""Concord Vault room kit: build a 17x9x17 room block by block, check it against the vault rules
(briefs/concord_vault.md), export a drop-in .nbt, and draw a fully detailed design sheet
(cutaway 3D views, every layer's plan, materials, light map, loot and connectors).
Used by room_<name>.py files. Textures are read from TEX (cached from 1.21.x)."""
import math, os, random, collections, json
import nbtlib
from nbtlib import Compound, List, Int, String, Double, Byte
from PIL import Image, ImageDraw, ImageFont, ImageFilter

Z = 'zerog_tweaks:'
DATA_VERSION = 3955
SX, SY, SZ = 17, 9, 17
TEX = os.environ.get('ZG_TEX', '/tmp/claude-0/-home-claude-zerog-tweaks/23345d11-2ce7-53a5-9128-b35ae672adbe/scratchpad/rooms/tex')
DOORS = {'N': ('north', (8, 0), lambda i: (i, 0)), 'S': ('south', (8, 16), lambda i: (i, 16)),
         'W': ('west', (0, 8), lambda i: (0, i)), 'E': ('east', (16, 8), lambda i: (16, i))}
CENTRE = {(x, z) for x in range(7, 10) for z in range(7, 10)}
CORR = Z + 'concord_vault/corridors'
LIGHT = {Z + 'spectral_lantern': 15, Z + 'pulsar_lamp': 15, Z + 'cerulite_cluster': 5, Z + 'liquid_starlight': 12,
         Z + 'starbloom': 7, Z + 'potted_starbloom': 7}
BANNED = ['_ore', 'cerulite_block', 'starlite_block', 'lumenite_block', 'aresite_block', 'gate_', '_casing', 'crystal_cell',
          'minecraft:torch', 'minecraft:wall_torch', 'minecraft:lantern', 'sea_lantern']

# ------------------------------------------------------------------------------------------------ NBT helpers
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

def name_of(state): return state.split('[', 1)[0]
def props_of(state):
    if '[' not in state: return {}
    return dict(p.split('=') for p in state[:-1].split('[', 1)[1].split(','))

class Room:
    def __init__(self, doors, seed=1):
        self.doors = doors; self.blocks = {}; self.entities = []; self.rng = random.Random(seed)
        self.notes = {}                                   # (x,y,z) -> short label for the plans
    def put(self, x, y, z, state, nbt=None):
        if 0 <= x < SX and 0 <= y < SY and 0 <= z < SZ: self.blocks[(x, y, z)] = (state, nbt)
    def get(self, x, y, z): return self.blocks.get((x, y, z), ('minecraft:air', None))[0]
    def fill(self, x0, y0, z0, x1, y1, z1, state):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1): self.put(x, y, z, state)
    def chest(self, x, y, z, facing, table, label=None):
        self.put(x, y, z, f'minecraft:chest[facing={facing},type=single,waterlogged=false]',
                 {'id': 'minecraft:chest', 'LootTable': Z + 'chests/concord_vault/' + table})
        self.notes[(x, y, z)] = label or table
    def jigsaw(self, x, y, z, facing):
        self.put(x, y, z, f'minecraft:jigsaw[orientation={facing}_up]', {
            'id': 'minecraft:jigsaw', 'name': Z + 'door', 'target': Z + 'door', 'pool': CORR,
            'final_state': 'minecraft:air', 'joint': 'aligned', 'placement_priority': 0, 'selection_priority': 0})
    def chest_minecart(self, x, z, y, table):
        self.entities.append(((x + .5, y + .0625, z + .5), (x, y, z),
                              {'id': 'minecraft:chest_minecart', 'LootTable': Z + 'chests/concord_vault/' + table}))
        self.notes[(x, y, z)] = 'cart:' + table
    def open_doors(self):
        for d in self.doors:
            facing, (jx, jz), at = DOORS[d]
            for i in range(6, 11):
                x, z = at(i)
                for y in range(1, 6): self.put(x, y, z, 'minecraft:air')
            self.jigsaw(jx, 1, jz, facing)
    # ------------------------------------------------------------------ connect fences / walls / panes like the game does
    def connect(self):
        def solidish(st):
            n = name_of(st)
            return n != 'minecraft:air' and not any(k in n for k in ('rail', 'chain', 'potted', 'starbloom', 'cluster', 'carpet', 'pressure_plate', 'jigsaw', 'lectern', 'chest'))
        for (x, y, z), (st, nbt) in list(self.blocks.items()):
            n = name_of(st)
            if n.endswith('_fence'):
                pr = {}
                for d, (dx, dz) in (('north', (0, -1)), ('south', (0, 1)), ('west', (-1, 0)), ('east', (1, 0))):
                    pr[d] = 'true' if solidish(self.get(x + dx, y, z + dz)) else 'false'
                pr['waterlogged'] = 'false'
                self.blocks[(x, y, z)] = (n + '[' + ','.join(f'{k}={v}' for k, v in pr.items()) + ']', nbt)
            elif n.endswith('_wall'):
                pr = {}
                for d, (dx, dz) in (('north', (0, -1)), ('south', (0, 1)), ('west', (-1, 0)), ('east', (1, 0))):
                    pr[d] = 'low' if solidish(self.get(x + dx, y, z + dz)) else 'none'
                pr['up'] = 'true'; pr['waterlogged'] = 'false'
                self.blocks[(x, y, z)] = (n + '[' + ','.join(f'{k}={v}' for k, v in pr.items()) + ']', nbt)
    # ------------------------------------------------------------------ export
    def save(self, path):
        self.connect()
        full = {}
        for x in range(SX):
            for y in range(SY):
                for z in range(SZ): full[(x, y, z)] = self.blocks.get((x, y, z), ('minecraft:air', None))
        palette, index, blocks = [], {}, []
        for (x, y, z), (state, nbt) in sorted(full.items(), key=lambda kv: (kv[0][1], kv[0][2], kv[0][0])):
            if state not in index: index[state] = len(palette); palette.append(state)
            b = {'pos': List[Int]([Int(x), Int(y), Int(z)]), 'state': Int(index[state])}
            if nbt: b['nbt'] = to_nbt(nbt)
            blocks.append(Compound(b))
        pal = []
        for state in palette:
            c = {'Name': String(name_of(state))}
            if props_of(state): c['Properties'] = Compound({k: String(v) for k, v in props_of(state).items()})
            pal.append(Compound(c))
        ents = [Compound({'pos': List[Double]([Double(a) for a in pos]), 'blockPos': List[Int]([Int(a) for a in bpos]),
                          'nbt': to_nbt(nbt)}) for pos, bpos, nbt in self.entities]
        root = Compound({'DataVersion': Int(DATA_VERSION), 'size': List[Int]([Int(SX), Int(SY), Int(SZ)]),
                         'palette': List[Compound](pal), 'blocks': List[Compound](blocks), 'entities': List[Compound](ents)})
        os.makedirs(os.path.dirname(path), exist_ok=True)
        nbtlib.File(root, root_name='').save(path, gzipped=True)
        return len(blocks)
    # ------------------------------------------------------------------ rule checks (brief: Rules for a room design)
    def check(self):
        res = []
        res.append(('Size 17 x 9 x 17', True))
        for d in 'NSEW':
            facing, (jx, jz), at = DOORS[d]
            st = self.get(jx, 1, jz)
            if d in self.doors:
                ok = st.startswith('minecraft:jigsaw') and all(self.get(*((at(i)[0], y, at(i)[1]))) in ('minecraft:air',) or (at(i) == (jx, jz) and y == 1)
                                                            for i in range(6, 11) for y in range(1, 6))
                res.append((f'{facing.title()} door 5 x 5 open, jigsaw facing out', ok))
        cen = all(self.get(x, 0, z) != 'minecraft:air' for x, z in CENTRE) and \
              all(self.get(x, y, z) == 'minecraft:air' for x, z in CENTRE for y in range(1, 4))
        res.append(('Centre 3 x 3 free for the Key Altar (solid floor, air y1-3)', cen))
        chests = [nbt for (st, nbt) in self.blocks.values() if nbt and nbt.get('id') == 'minecraft:chest']
        res.append(('Every chest uses a concord_vault loot table', all('LootTable' in c for c in chests) and len(chests) > 0))
        bad = sorted({name_of(st) for st, _ in self.blocks.values() if any(b in name_of(st) for b in BANNED)})
        res.append(('No ores, storage blocks, gate/machine parts, torches' + (f' (found {bad})' if bad else ''), not bad))
        return res
    # ------------------------------------------------------------------ light (block light, flood fill like the game)
    def light(self):
        opaque = lambda st: self._shape(st) == 'full' and not any(k in st for k in ('glass', 'lantern', 'lamp', 'leaves'))
        L = {}; q = collections.deque()
        for p, (st, _) in self.blocks.items():
            lv = LIGHT.get(name_of(st))
            if lv: L[p] = lv; q.append(p)
        while q:
            x, y, z = q.popleft(); lv = L[(x, y, z)]
            for dx, dy, dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
                n = (x + dx, y + dy, z + dz)
                if not (0 <= n[0] < SX and 0 <= n[1] < SY and 0 <= n[2] < SZ): continue
                if opaque(self.get(*n)): continue
                if L.get(n, 0) < lv - 1: L[n] = lv - 1; q.append(n)
        return L
    # ------------------------------------------------------------------ geometry for rendering
    @staticmethod
    def _shape(st):
        n = name_of(st)
        if n == 'minecraft:air' or n.startswith('minecraft:jigsaw'): return None
        for k, v in (('_slab', 'slab'), ('_stairs', 'stairs'), ('_fence_gate', 'gate'), ('_fence', 'fence'), ('_wall', 'wall'),
                     ('chain', 'chain'), ('rail', 'rail'), ('_trapdoor', 'trapdoor'), ('lectern', 'lectern'), ('chest', 'chest'),
                     ('potted_', 'pot'), ('_pressure_plate', 'plate'), ('_carpet', 'plate'), ('starbloom', 'plant'),
                     ('cluster', 'plant'), ('_button', 'button')):
            if k in n: return v
        return 'full'

    def boxes(self, x, y, z, st):
        """-> list of (x0,y0,z0,x1,y1,z1) in block units for this block"""
        s = self._shape(st); pr = props_of(st)
        if s is None: return []
        if s == 'full': return [(0, 0, 0, 1, 1, 1)]
        if s == 'slab':
            return [(0, .5, 0, 1, 1, 1)] if pr.get('type') == 'top' else [(0, 0, 0, 1, 1, 1)] if pr.get('type') == 'double' else [(0, 0, 0, 1, .5, 1)]
        if s == 'stairs':
            top = pr.get('half') == 'top'
            base = (0, .5, 0, 1, 1, 1) if top else (0, 0, 0, 1, .5, 1)
            yy = (0, .5) if top else (.5, 1)
            f = pr.get('facing', 'north')
            half = {'north': (0, 0, 1, .5), 'south': (0, .5, 1, 1), 'west': (0, 0, .5, 1), 'east': (.5, 0, 1, 1)}[f]
            return [base, (half[0], yy[0], half[1], half[2], yy[1], half[3])]
        if s == 'fence':
            b = [(.375, 0, .375, .625, 1, .625)]
            if pr.get('north') == 'true': b.append((.4375, .375, 0, .5625, .9375, .375))
            if pr.get('south') == 'true': b.append((.4375, .375, .625, .5625, .9375, 1))
            if pr.get('west') == 'true': b.append((0, .375, .4375, .375, .9375, .5625))
            if pr.get('east') == 'true': b.append((.625, .375, .4375, 1, .9375, .5625))
            return b
        if s == 'wall':
            b = [(.25, 0, .25, .75, 1, .75)]
            for d, bx in (('north', (.3125, 0, 0, .6875, .875, .25)), ('south', (.3125, 0, .75, .6875, .875, 1)),
                          ('west', (0, 0, .3125, .25, .875, .6875)), ('east', (.75, 0, .3125, 1, .875, .6875))):
                if pr.get(d, 'none') != 'none': b.append(bx)
            return b
        if s == 'chain': return [(.44, 0, .44, .56, 1, .56)]
        if s == 'rail': return [(0, 0, 0, 1, .0625, 1)]
        if s == 'plate': return [(.0625, 0, .0625, .9375, .0625, .9375)]
        if s == 'trapdoor':
            if pr.get('open') == 'true':
                f = pr.get('facing', 'north')
                return [{'north': (0, 0, .8125, 1, 1, 1), 'south': (0, 0, 0, 1, 1, .1875), 'west': (.8125, 0, 0, 1, 1, 1), 'east': (0, 0, 0, .1875, 1, 1)}[f]]
            return [(0, .8125, 0, 1, 1, 1)] if pr.get('half') == 'top' else [(0, 0, 0, 1, .1875, 1)]
        if s == 'lectern': return [(0, 0, 0, 1, .125, 1), (.25, .125, .25, .75, .8, .75), (0, .8, 0, 1, .95, 1)]
        if s == 'chest': return [(.0625, 0, .0625, .9375, .875, .9375)]
        if s == 'pot': return [(.3125, 0, .3125, .6875, .375, .6875), (.42, .375, .42, .58, .85, .58)]
        if s == 'plant': return [(.3, 0, .3, .7, .7, .7)]
        if s == 'gate': return [(0, .375, .4375, 1, .9375, .5625)]
        if s == 'button': return [(.375, 0, .375, .625, .125, .625)]
        return [(0, 0, 0, 1, 1, 1)]

# ------------------------------------------------------------------------------------------------ textures
_TC = {}
def _load(n):
    p = os.path.join(TEX, n + '.png')
    if os.path.exists(p):
        im = Image.open(p).convert('RGBA')
        if im.height > im.width: im = im.crop((0, 0, im.width, im.width))
        return im.resize((16, 16), Image.NEAREST)
    return None
def _proc(kind):
    """procedural 16x16 textures for vanilla blocks (no vanilla assets in this repo)"""
    im = Image.new('RGBA', (16, 16)); p = im.load(); r = random.Random(kind)
    for y in range(16):
        for x in range(16):
            n = r.random() * 14 - 7
            if kind == 'barrel_side':
                c = (112 + n, 82 + n, 50 + n) if (x % 5) else (86, 62, 38); c = (58, 48, 40) if y in (2, 13) else c
            elif kind == 'barrel_top':
                d = math.hypot(x - 7.5, y - 7.5); c = (70, 54, 36) if d > 7 else (126 + n, 94 + n, 58 + n); c = (40, 32, 26) if 5.5 < d < 6.5 else c
            elif kind == 'chest':
                c = (150 + n, 104 + n, 46 + n); c = (64, 46, 26) if x in (0, 15) or y in (0, 15, 5) else c
                c = (205, 205, 205) if 6 <= x <= 9 and 4 <= y <= 7 else c
            elif kind == 'chain': c = (60, 66, 78) if (y % 4) < 2 else (96, 104, 118)
            elif kind == 'rail':
                c = (95 + n, 70 + n, 45 + n) if y % 4 == 1 else (0, 0, 0, 0)
                if x in (2, 3, 12, 13): c = (150, 150, 158)
            elif kind == 'lectern': c = (138 + n, 100 + n, 60 + n) if y % 4 else (100, 72, 44)
            elif kind == 'bookshelf':
                c = (130 + n, 96 + n, 58 + n) if y in (0, 7, 8, 15) else [(150, 40, 40), (40, 80, 150), (60, 120, 60), (170, 140, 60), (90, 60, 120)][(x // 2 + y // 8) % 5]
                if x in (0, 15): c = (110, 80, 50)
            elif kind == 'pot': c = (150 + n, 80 + n, 56 + n)
            elif kind == 'minecart': c = (110 + n, 114 + n, 122 + n) if x not in (0, 15) else (70, 74, 82)
            elif kind == 'crafting': c = (140 + n, 104 + n, 64 + n) if (x + y) % 6 else (90, 66, 40)
            else: c = (200, 0, 200)
            p[x, y] = tuple(int(max(0, min(255, v))) for v in c[:3]) + ((c[3],) if len(c) > 3 else (255,))
    return im
def tex_for(st, face):
    n = name_of(st).split(':')[1] if ':' in name_of(st) else name_of(st)
    ns = name_of(st).split(':')[0]
    key = (n, face)
    if key in _TC: return _TC[key]
    im = None
    if ns == 'minecraft':
        m = {'barrel': 'barrel_top' if face in ('up', 'down') else 'barrel_side', 'chest': 'chest', 'chain': 'chain', 'rail': 'rail',
             'lectern': 'lectern', 'bookshelf': 'lectern' if face in ('up', 'down') else 'bookshelf', 'crafting_table': 'crafting',
             'smithing_table': 'crafting', 'cartography_table': 'crafting'}.get(n, 'chest')
        im = _proc(m)
    else:
        base = n
        for suf in ('_slab', '_stairs', '_wall', '_fence_gate', '_fence', '_pressure_plate', '_button'):
            if base.endswith(suf): base = base[:-len(suf)]
        if base.startswith('potted_'): base = base[7:]
        cands = []
        if face in ('up', 'down'): cands += [base + '_top', base + '_log_top' if base.endswith('_wood') else '']
        if base.endswith('_brick') : base += 's'
        cands += [base, base.replace('_brick', '_bricks'), base + 's', base.replace('_wood', '_log'), base.replace('stripped_shardwood_wood', 'stripped_shardwood_log')]
        if base == 'shardwood' or (base.startswith('shardwood') and not base.endswith(('_log', '_wood', 'leaves', 'sapling', 'door', 'trapdoor'))): cands.append('shardwood_planks')
        for c in cands:
            if c and (im := _load(c)): break
        if im is None: im = _proc('x')
        glow = _load(base + '_emissive')
        if glow is not None:
            im = im.copy(); gl = glow; m = _load(base + '_glowmask')
            im.alpha_composite(gl if m is None else Image.composite(gl, Image.new('RGBA', (16, 16), (0, 0, 0, 0)), m.split()[0]))
    _TC[key] = im; return im
def avg_color(st):
    im = tex_for(st, 'up'); px = [p for p in im.getdata() if p[3] > 20]
    return tuple(sum(p[i] for p in px) // max(1, len(px)) for i in range(3)) if px else (200, 0, 200)

# ------------------------------------------------------------------------------------------------ 3D cutaway renderer
FACES = {
 'south': (lambda a, b: [(a[0], b[1], b[2]), (b[0], b[1], b[2]), (b[0], a[1], b[2]), (a[0], a[1], b[2])], (0, 0, 1), ('x', 'y')),
 'north': (lambda a, b: [(b[0], b[1], a[2]), (a[0], b[1], a[2]), (a[0], a[1], a[2]), (b[0], a[1], a[2])], (0, 0, -1), ('x', 'y')),
 'east':  (lambda a, b: [(b[0], b[1], b[2]), (b[0], b[1], a[2]), (b[0], a[1], a[2]), (b[0], a[1], b[2])], (1, 0, 0), ('z', 'y')),
 'west':  (lambda a, b: [(a[0], b[1], a[2]), (a[0], b[1], b[2]), (a[0], a[1], b[2]), (a[0], a[1], a[2])], (-1, 0, 0), ('z', 'y')),
 'up':    (lambda a, b: [(a[0], b[1], a[2]), (b[0], b[1], a[2]), (b[0], b[1], b[2]), (a[0], b[1], b[2])], (0, 1, 0), ('x', 'z')),
}
SUN = (-.35, .85, .45); _l = math.sqrt(sum(c * c for c in SUN)); SUN = tuple(c / _l for c in SUN)

def render(room, yaw, pitch=-32, scale=34, hide=lambda x, y, z: False, light=None, sub=4):
    cy, sy_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)); cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    def rot(p):
        x, y, z = p[0] - SX / 2, p[1] - SY / 2, p[2] - SZ / 2
        x, z = x * cy + z * sy_, -x * sy_ + z * cy
        y, z = y * cp - z * sp, y * sp + z * cp
        return x, y, z
    def rn(n):
        x, y, z = n; x, z = x * cy + z * sy_, -x * sy_ + z * cy; y, z = y * cp - z * sp, y * sp + z * cp; return x, y, z
    room.connect()
    vis = {p: st for p, (st, _) in room.blocks.items() if not hide(*p) and room._shape(st)}
    def full_at(p): st = vis.get(p); return st is not None and room._shape(st) == 'full' and 'glass' not in st
    polys = []
    for (x, y, z), st in vis.items():
        glow = LIGHT.get(name_of(st), 0) >= 12
        for (x0, y0, z0, x1, y1, z1) in room.boxes(x, y, z, st):
            a, b = (x + x0, y + y0, z + z0), (x + x1, y + y1, z + z1)
            for fname, (fn, n, axes) in FACES.items():
                vn = rn(n)
                if vn[2] <= 1e-6: continue
                # cull faces hidden by a full neighbour (only for faces on the block boundary)
                on_edge = {'south': z1 == 1, 'north': z0 == 0, 'east': x1 == 1, 'west': x0 == 0, 'up': y1 == 1}[fname]
                if on_edge and full_at((x + n[0], y + n[1], z + n[2])) and room._shape(st) == 'full': continue
                cs = fn(a, b); t = tex_for(st, 'up' if fname == 'up' else 'side').load()
                lv = 15 if light is None else max(light.get((x + n[0], y + n[1], z + n[2]), 0), light.get((x, y, z), 0))
                amb = .62 + .38 * (lv / 15) if light is not None else 1
                shade = 1.0 if glow else (.62 + .45 * max(0, sum(i * j for i, j in zip(n, SUN)))) * amb
                # texture window for this face (partial faces use the matching part of the texture)
                if fname in ('south', 'north'): u0, u1, v0, v1 = x0, x1, 1 - y1, 1 - y0
                elif fname in ('east', 'west'): u0, u1, v0, v1 = z0, z1, 1 - y1, 1 - y0
                else: u0, u1, v0, v1 = x0, x1, z0, z1
                nu = max(1, round((u1 - u0) * sub)); nv = max(1, round((v1 - v0) * sub))
                P0, P1, P3 = cs[0], cs[1], cs[3]
                for j in range(nv):
                    for i in range(nu):
                        def pt(ii, jj):
                            s_, t_ = ii / nu, jj / nv
                            return tuple(P0[k] + (P1[k] - P0[k]) * s_ + (P3[k] - P0[k]) * t_ for k in range(3))
                        tu = int((u0 + (u1 - u0) * (i + .5) / nu) * 16); tv = int((v0 + (v1 - v0) * (j + .5) / nv) * 16)
                        col = t[min(15, max(0, tu)), min(15, max(0, tv))]
                        if col[3] < 30: continue
                        q = [rot(pt(i, j)), rot(pt(i + 1, j)), rot(pt(i + 1, j + 1)), rot(pt(i, j + 1))]
                        polys.append((sum(p[2] for p in q) / 4, q, tuple(min(255, int(c * shade)) for c in col[:3]), glow))
    for (pos, bpos, nbt) in room.entities:               # chest minecart as a box
        x, y, z = pos; a, b = (x - .45, y, z - .4), (x + .45, y + .65, z + .4)
        for fname, (fn, n, axes) in FACES.items():
            vn = rn(n)
            if vn[2] <= 1e-6: continue
            q = [rot(c) for c in fn(a, b)]; sh = .62 + .45 * max(0, sum(i * j for i, j in zip(n, SUN)))
            polys.append((sum(p[2] for p in q) / 4, q, tuple(int(c * sh) for c in (112, 116, 126)), False))
    xs = [p[0] for _, q, _, _ in polys for p in q]; ys = [p[1] for _, q, _, _ in polys for p in q]
    X0, X1, Y0, Y1 = min(xs) - .6, max(xs) + .6, min(ys) - .6, max(ys) + .6
    W, H = int((X1 - X0) * scale), int((Y1 - Y0) * scale)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(gl)
    for depth, q, col, glow in sorted(polys, key=lambda p: p[0]):
        pts = [((p[0] - X0) * scale, (Y1 - p[1]) * scale) for p in q]
        d.polygon(pts, fill=col + (255,), outline=col + (255,))
        if glow: dg.polygon(pts, fill=(150, 220, 255, 255))
    b = gl.filter(ImageFilter.GaussianBlur(scale * .7)); b.putalpha(b.split()[3].point(lambda v: int(v * .55)))
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.alpha_composite(im); out.alpha_composite(b)
    return out

# ------------------------------------------------------------------------------------------------ sheet
F = lambda s, b=False: ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if b else ""}.ttf', s)
M = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', s)
BG, INK, SUB, LINE, CARD, DARK, ACC = (245, 244, 240), (30, 32, 38), (96, 100, 112), (205, 205, 215), (255, 255, 255), (24, 27, 36), (90, 70, 210)

def _wrap(d, text, font, width):
    out, cur = [], ''
    for w in text.split():
        if d.textlength((cur + ' ' + w).strip(), font=font) > width: out.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    return out + [cur]

def pretty(st):
    n = name_of(st).split(':')[1].replace('_', ' ')
    pr = props_of(st); extra = []
    if 'type' in pr and pr['type'] != 'single': extra.append(pr['type'])
    if 'half' in pr: extra.append(pr['half'])
    if 'axis' in pr: extra.append(pr['axis'])
    if 'facing' in pr and not n.endswith('chest'): extra.append('faces ' + pr['facing'])
    return n + (f' ({", ".join(extra)})' if extra else '')

def sheet(room, meta, out_png):
    room.connect()
    light = room.light()
    W = 2200
    # ---- legend: one glyph per distinct block (ignoring connection props)
    def key(st):
        pr = {k: v for k, v in props_of(st).items() if k not in ('north', 'south', 'east', 'west', 'up', 'waterlogged', 'open', 'powered', 'has_book', 'shape')}
        return name_of(st) + ('[' + ','.join(f'{k}={v}' for k, v in sorted(pr.items())) + ']' if pr else '')
    counts = collections.Counter(key(st) for st, _ in room.blocks.values() if room._shape(st))
    glyphs = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz@#$%&*+=?'
    order = sorted(counts, key=lambda k: (-counts[k], k))
    G = {k: glyphs[i] for i, k in enumerate(order)}
    # ---- page
    views = [(meta.get('view_a_title', 'Cutaway from the south-west (south and west walls cut away)'), render(room, 38, 34, 30, hide=lambda x, y, z: y == 8 or ((z == 16 or x == 0) and y >= 2), light=light)),
             (meta.get('view_b_title', 'Cutaway from the north-east (north and east walls cut away)'), render(room, 218, 34, 30, hide=lambda x, y, z: y == 8 or ((z == 0 or x == 16) and y >= 2), light=light))]
    H = 4200
    img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
    d.text((50, 34), meta['title'], font=F(46, True), fill=INK)
    d.text((50, 98), meta['subtitle'], font=F(20), fill=SUB)
    y = 140
    for ln in _wrap(d, meta['story'], F(18), W - 100): d.text((50, y), ln, font=F(18), fill=INK); y += 27
    y += 16
    # views
    vw = (W - 120) // 2
    for i, (t, im) in enumerate(views):
        x = 50 + i * (vw + 20)
        d.rounded_rectangle((x, y, x + vw, y + 700), 16, fill=DARK)
        d.text((x + 20, y + 16), t, font=F(18, True), fill=(210, 216, 230))
        im = im.copy(); im.thumbnail((vw - 40, 640), Image.LANCZOS)
        img.paste(im, (x + (vw - im.width) // 2, y + 46 + (640 - im.height) // 2), im)
    y += 730
    # ---- layer plans
    d.text((50, y), 'Layer by layer (top-down, north up). Cell = 1 block. Coordinates are template-local (x 0-16 west to east, z 0-16 north to south).', font=F(18, True), fill=INK)
    y += 36
    cell = 22; pw = 17 * cell + 30; ph = 17 * cell + 56
    layers = list(range(0, 9))
    for i, ly in enumerate(layers):
        px = 50 + (i % 5) * (pw + 18); py = y + (i // 5) * (ph + 16)
        d.rounded_rectangle((px, py, px + pw, py + ph), 10, fill=CARD, outline=LINE)
        d.text((px + 12, py + 8), f'y = {ly}' + {0: '  floor', 1: '  (Key Altar level)', 8: '  ceiling'}.get(ly, ''), font=F(15, True), fill=INK)
        ox, oy = px + 15, py + 36
        for z in range(17):
            for x in range(17):
                st = room.get(x, ly, z); X, Y = ox + x * cell, oy + z * cell
                if room._shape(st):
                    c = avg_color(st); d.rectangle((X, Y, X + cell - 1, Y + cell - 1), fill=c)
                    lum = sum(c) / 3
                    d.text((X + cell // 2, Y + cell // 2), G[key(st)], font=M(11), fill=(255, 255, 255) if lum < 110 else (15, 15, 20), anchor='mm')
                elif st.startswith('minecraft:jigsaw'):
                    d.rectangle((X, Y, X + cell - 1, Y + cell - 1), fill=(255, 210, 60)); d.text((X + cell // 2, Y + cell // 2), 'J', font=M(12), fill=INK, anchor='mm')
                else:
                    d.rectangle((X, Y, X + cell - 1, Y + cell - 1), fill=(248, 248, 250), outline=(232, 232, 238))
                if ly in (1,) and (x, z) in CENTRE: d.rectangle((X + 1, Y + 1, X + cell - 2, Y + cell - 2), outline=ACC, width=2)
                if (x, ly, z) in room.notes: d.ellipse((X + cell - 9, Y + 1, X + cell - 1, Y + 9), fill=(230, 60, 60))
        for (pos, bpos, nbt) in room.entities:
            if bpos[1] == ly:
                X, Y = ox + bpos[0] * cell, oy + bpos[2] * cell; d.rectangle((X + 3, Y + 3, X + cell - 4, Y + cell - 4), outline=(230, 60, 60), width=3)
    # light map in the 10th slot
    px = 50 + 4 * (pw + 18); py = y + (ph + 16)
    d.rounded_rectangle((px, py, px + pw, py + ph), 10, fill=CARD, outline=LINE)
    d.text((px + 12, py + 8), 'Light at y = 1 (what players stand in)', font=F(13, True), fill=INK)
    ox, oy = px + 15, py + 36; low = 0; lowest = 15
    for z in range(17):
        for x in range(17):
            st = room.get(x, 1, z); X, Y = ox + x * cell, oy + z * cell
            if room._shape(st) == 'full': d.rectangle((X, Y, X + cell - 1, Y + cell - 1), fill=(60, 62, 70)); continue
            lv = light.get((x, 1, z), 0); low += lv < 7 and 0 < x < 16 and 0 < z < 16
            if 0 < x < 16 and 0 < z < 16 and room._shape(st) is None: lowest = min(lowest, lv)
            t = lv / 15; d.rectangle((X, Y, X + cell - 1, Y + cell - 1), fill=(int(30 + 225 * t), int(30 + 200 * t), int(60 + 120 * t)))
            d.text((X + cell // 2, Y + cell // 2), str(lv), font=M(10), fill=(20, 20, 20) if t > .5 else (230, 230, 230), anchor='mm')
    y += 2 * (ph + 16) + 10
    # ---- legend + materials
    d.text((50, y), 'Block legend and quantities', font=F(22, True), fill=INK); y += 38
    colw = (W - 100) // 3
    for i, k in enumerate(order):
        cx = 50 + (i % 3) * colw; cy_ = y + (i // 3) * 30
        c = avg_color(k); d.rectangle((cx, cy_, cx + 24, cy_ + 24), fill=c, outline=LINE)
        d.text((cx + 12, cy_ + 12), G[k], font=M(12), fill=(255, 255, 255) if sum(c) / 3 < 110 else (15, 15, 20), anchor='mm')
        d.text((cx + 34, cy_ + 3), f'{counts[k]:>4}  {pretty(k)}', font=M(14), fill=INK)
    y += ((len(order) + 2) // 3) * 30 + 26
    # ---- right-hand info blocks (two columns)
    sections = meta['sections'] + [('Light', [f'Sources: {", ".join(sorted({pretty(st) for st, _ in room.blocks.values() if LIGHT.get(name_of(st))}))}.',
                                               (f'Lowest light on a walkable cell at y = 1: {lowest}. ' + ('Hostile mobs need block light 0 to spawn (1.21), so none spawn in this room.' if lowest > 0 else 'Some cells are at 0: hostile mobs can spawn there.'))])]
    sections.append(('Rule check (briefs/concord_vault.md)', [('PASS  ' if ok else 'FAIL  ') + t for t, ok in room.check()]))
    colx = [50, 50 + (W - 100) // 2 + 10]; cw = (W - 100) // 2 - 30; cys = [y, y]
    for title, lines in sections:
        c = 0 if cys[0] <= cys[1] else 1
        yy = cys[c]; d.text((colx[c], yy), title, font=F(20, True), fill=INK); yy += 32
        for ln in lines:
            bullet = not ln.startswith(('PASS', 'FAIL'))
            col = (30, 140, 70) if ln.startswith('PASS') else (200, 40, 40) if ln.startswith('FAIL') else INK
            for k, w in enumerate(_wrap(d, ln, F(16), cw - 20)):
                d.text((colx[c] + (18 if bullet and k else 0), yy), (('•  ' if bullet and k == 0 else '') + w), font=F(16), fill=col); yy += 24
            yy += 4
        cys[c] = yy + 22
    img = img.crop((0, 0, W, max(cys) + 30)); img.save(out_png); return img.size
