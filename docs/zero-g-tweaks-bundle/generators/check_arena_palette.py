"""Check a boss-arena structure template against the arena rules (see briefs/prism_sentinel_arena.md).
Usage: python3 check_arena_palette.py <arena.nbt> [--max 48] [--min-height 30] [--headroom 18] [--radius 15]
Needs: pip install nbtlib"""
import sys, re, argparse, collections
import nbtlib

BANNED = [r'_ore$', r'^zerog_tweaks:(cerulite|starlite|lumenite|aresite|selenite|[a-z]+ium|[a-z]+ite|[a-z]+ine)_block$',
          r'_gate_frame$', r'^zerog_tweaks:gate_', r'_casing$', r'^zerog_tweaks:crystal_cell$',
          r'^minecraft:(amethyst_cluster|small_amethyst_bud|medium_amethyst_bud|large_amethyst_bud|sea_lantern|chest|barrel)$']
LIMITED = {r'prismstone': 20}            # pattern -> max count allowed (accents only)
AIRLIKE = {'minecraft:air', 'minecraft:cave_air', 'minecraft:structure_void', 'minecraft:light'}

a = argparse.ArgumentParser(); a.add_argument('nbt'); a.add_argument('--max', type=int, default=48)
a.add_argument('--min-height', type=int, default=30); a.add_argument('--headroom', type=int, default=18)
a.add_argument('--radius', type=int, default=15); o = a.parse_args()
n = nbtlib.load(o.nbt); r = n if 'size' in n else n['']
sx, sy, sz = (int(v) for v in r['size']); pal = r['palette'] if 'palette' in r else r['palettes'][0]
names = [str(p['Name']) for p in pal]
cnt = collections.Counter(names[int(b['state'])] for b in r['blocks'])
errs = []
if max(sx, sy, sz) > o.max: errs.append(f'size {sx}x{sy}x{sz} is over the {o.max}-block structure limit')
if sy < o.min_height: errs.append(f'height {sy} < {o.min_height}: not enough room for a 10.8-tall floating boss')
for nm, c in sorted(cnt.items()):
    if any(re.search(p, nm) for p in BANNED): errs.append(f'banned block {nm} x{c}')
for p, lim in LIMITED.items():
    tot = sum(c for nm, c in cnt.items() if re.search(p, nm))
    if tot > lim: errs.append(f'{p} family x{tot} (max {lim}, accents only)')
# headroom: within `radius` of the centre, find the floor (highest solid block in the lower third), require air above it
cx, cz = sx // 2, sz // 2; solid = collections.defaultdict(list)
for b in r['blocks']:
    nm = names[int(b['state'])]
    if nm in AIRLIKE: continue
    x, y, z = (int(v) for v in b['pos'])
    if (x - cx) ** 2 + (z - cz) ** 2 <= o.radius ** 2: solid[(x, z)].append(y)
floor_ys = [min(ys) for ys in solid.values() if ys]
if floor_ys:
    floor = sorted(floor_ys)[len(floor_ys) // 2]                 # median lowest-solid = floor level
    blocked = sorted({(x, z) for (x, z), ys in solid.items() if any(floor + 3 < y < floor + 3 + o.headroom for y in ys)})
    # the dais (r <= 4) and 4 pylons are allowed: ignore columns that are part of a contiguous 3x3 or the dais
    blocked = [(x, z) for x, z in blocked if (x - cx) ** 2 + (z - cz) ** 2 > 16]
    if len(blocked) > 4 * 9: errs.append(f'{len(blocked)} columns inside r{o.radius} block the headroom (only 4 pylons, 3x3 each, are allowed)')
be = sum(1 for b in r['blocks'] if 'nbt' in b)
if not any('concord_prism' in nm for nm in names): errs.append('no zerog_tweaks:concord_prism at the dais (nothing starts the fight)')
print(f'{o.nbt}: {sx}x{sy}x{sz}, {len(names)} block types, {be} block entities')
print('\n'.join('  FAIL ' + e for e in errs) if errs else 'OK')
sys.exit(1 if errs else 0)
