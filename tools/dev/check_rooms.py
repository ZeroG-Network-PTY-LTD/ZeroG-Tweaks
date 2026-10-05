"""Validate Concord Vault room templates against the vault brief (Design: briefs/concord_vault.md) and the mod's blocks.

usage: python tools/dev/check_rooms.py [ROOMS_DIR]
       default ROOMS_DIR: src/main/resources/data/zerog_tweaks/structure/concord_vault/rooms
       Needs one Gradle build first (vanilla block list comes from build/moddev/artifacts).
"""
import glob, os, re, sys, zipfile
import nbtlib

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
ROOT = os.path.join(REPO, 'src/main/resources/assets/zerog_tweaks/blockstates/')
ROOMS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'src/main/resources/data/zerog_tweaks/structure/concord_vault/rooms')
jars = glob.glob(os.path.join(REPO, 'build/moddev/artifacts/*client-extra*.jar'))
if not jars: raise SystemExit("No Minecraft resources jar in build/moddev/artifacts: run gradlew build once")
vanilla = zipfile.ZipFile(jars[0])
VANILLA = {n.split('/')[-1][:-5] for n in vanilla.namelist() if n.startswith('assets/minecraft/blockstates/')}
BANNED = [r'_ore$', r'^zerog_tweaks:(cerulite|starlite|lumenite|nebulite|pulsar_dust|[a-z]+ium|[a-z]+ite|[a-z]+ine)_block$',
          r'_gate_frame$', r'^zerog_tweaks:gate_', r'_casing$', r'^zerog_tweaks:crystal_cell$', r'^minecraft:torch$', r'^minecraft:wall_torch$',
          r'^zerog_tweaks:cerulite_cluster$', r'^zerog_tweaks:budding_cerulite$']
DOORS = {'N': ((8, 1, 0), 'north'), 'S': ((8, 1, 16), 'south'), 'W': ((0, 1, 8), 'west'), 'E': ((16, 1, 8), 'east')}
ok_all = True
for f in sorted(os.listdir(ROOMS)):
    n = nbtlib.load(os.path.join(ROOMS, f)); errs = []
    size = tuple(int(v) for v in n['size'])
    if size != (17, 9, 17): errs.append(f'size {size}')
    pal = n['palette']; names = [str(p['Name']) for p in pal]
    cells = {}
    for b in n['blocks']:
        pos = tuple(int(v) for v in b['pos']); st = int(b['state'])
        cells[pos] = (names[st], pal[st], b.get('nbt'))
    for nm in set(names):
        ns, path = nm.split(':')
        if ns == 'zerog_tweaks' and not os.path.exists(ROOT + path + '.json'): errs.append(f'unknown block {nm}')
        if ns == 'minecraft' and path not in VANILLA and path not in ('air', 'structure_void', 'cave_air'): errs.append(f'unknown vanilla block {nm}')
        if any(re.search(p, nm) for p in BANNED): errs.append(f'banned {nm}')
    doors = []
    for d, (pos, facing) in DOORS.items():
        c = cells.get(pos)
        if c and c[0] == 'minecraft:jigsaw':
            nb = c[2]; ori = str(c[1]['Properties']['orientation'])
            if not ori.startswith(facing): errs.append(f'{d} jigsaw faces {ori}')
            if str(nb['pool']) != 'zerog_tweaks:concord_vault/corridors' or str(nb['name']) != 'zerog_tweaks:door' or str(nb['target']) != 'zerog_tweaks:door':
                errs.append(f'{d} jigsaw settings {dict(nb)}')
            doors.append(d)
    jig = [p for p, c in cells.items() if c[0] == 'minecraft:jigsaw']
    if len(jig) != len(doors): errs.append(f'stray jigsaws {jig}')
    for x in range(7, 10):
        for z in range(7, 10):
            fl = cells.get((x, 0, z), ('minecraft:air',))[0]
            if fl in ('minecraft:air', 'minecraft:cave_air'): errs.append(f'no floor at centre {(x, z)}')
            for y in range(1, 4):
                c = cells.get((x, y, z))
                if c and c[0] not in ('minecraft:air', 'minecraft:cave_air'): errs.append(f'centre blocked {(x, y, z)} {c[0]}')
    chests = [(p, c) for p, c in cells.items() if c[0] in ('minecraft:chest', 'minecraft:barrel', 'minecraft:trapped_chest')]
    for p, c in chests:
        lt = str(c[2].get('LootTable', '')) if c[2] else ''
        if c[0] != 'minecraft:barrel' and not lt.startswith('zerog_tweaks:chests/concord_vault/'): errs.append(f'chest {p} loot {lt!r}')
        if c[2] and 'Items' in c[2] and len(c[2]['Items']): errs.append(f'container {p} has fixed items')
    ents = [str(e['nbt']['id']) for e in n['entities']]
    print(f"{'OK  ' if not errs else 'FAIL'} {f:22s} doors {''.join(sorted(doors)):4s} chests {sum(1 for _, c in chests if c[0] != 'minecraft:barrel')} "
          f"blocks {len(n['blocks'])} entities {ents}")
    for e in errs[:8]: print('      -', e)
    ok_all &= not errs
print('ALL OK' if ok_all else 'PROBLEMS FOUND')
