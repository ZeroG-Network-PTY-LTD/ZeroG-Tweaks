"""Augment planetary_showcase NBTs with blueprint surface features.

Preserves every underground anchor the GameTests and path tests lock in:
  chests (14,4,14) / (34,4,14), spawner (18,4,32), air (24,4,24)..(24,5,24),
  surface entry (24,13,40) route, loot tables, spawner mobs.
Adds the blueprint-visible surface identity: spires / ring tower / habitat
towers, core chamber crown, perimeter arches, flora.

Reads the existing .nbt, appends blocks, writes back. Idempotent: strips prior
augmentation layers first (tracked in a sidecar manifest next to the nbt).
"""
import gzip, json, math, struct, sys, os
from pathlib import Path

DATA_VERSION = 3955
SHOWCASE_PATH = str(Path(os.environ.get('ZEROG_SHOWCASE_TEMPLATE_DIR',str(Path(__file__).resolve().parent.parent/'templates'))) / '{}')


def read_nbt(path):
    raw = gzip.open(path, 'rb').read()
    pos = [0]
    def r1():
        v = raw[pos[0]]; pos[0] += 1; return v
    def r2():
        v = struct.unpack('>H', raw[pos[0]:pos[0] + 2])[0]; pos[0] += 2; return v
    def r4s():
        v = struct.unpack('>i', raw[pos[0]:pos[0] + 4])[0]; pos[0] += 4; return v
    def r2s():
        v = struct.unpack('>h', raw[pos[0]:pos[0] + 2])[0]; pos[0] += 2; return v
    def rstr():
        n = r2(); s = raw[pos[0]:pos[0] + n].decode(); pos[0] += n; return s
    def payload(t):
        if t == 2: return r2s()
        if t == 3: return r4s()
        if t == 8: return rstr()
        if t == 9:
            st = r1(); n = r4s()
            return [payload(st) for _ in range(n)]
        if t == 10:
            d = {}
            while True:
                tt = r1()
                if tt == 0:
                    break
                k = rstr(); d[k] = payload(tt)
            return d
        raise ValueError(t)
    r1(); rstr()
    return payload(10)


def utf(s):
    raw = s.encode('utf-8')
    return struct.pack('>H', len(raw)) + raw


def wr_payload(kind, value):
    if kind == 2: return struct.pack('>h', value)
    if kind == 3: return struct.pack('>i', value)
    if kind == 8: return utf(value)
    if kind == 9:
        subtype, values = value
        return bytes([subtype]) + struct.pack('>i', len(values)) + b''.join(wr_payload(subtype, v) for v in values)
    if kind == 10:
        return b''.join(bytes([t]) + utf(k) + wr_payload(t, v) for k, (t, v) in value.items()) + b'\0'
    raise ValueError(f'Unsupported NBT type: {kind}')


def write_nbt(path, spec):
    states = []
    for state in spec['palette']:
        entry = {'Name': (8, state['Name'])}
        if state.get('Properties'):
            entry['Properties'] = (10, {k: (8, v) for k, v in sorted(state['Properties'].items())})
        states.append(entry)
    out_blocks = []
    for bl in sorted(spec['blocks'], key=lambda b: tuple(b['pos'])):
        entry = {'pos': (9, (3, bl['pos'])), 'state': (3, bl['state'])}
        if 'nbt' in bl:
            tag = bl['nbt']
            if 'SpawnData' in tag:
                # preserve authored full spawner NBT (existing showcase format)
                entry['nbt'] = (10, {
                    'id': (8, tag.get('id', 'minecraft:mob_spawner')),
                    'Delay': (2, tag.get('Delay', 200)),
                    'MinSpawnDelay': (2, tag.get('MinSpawnDelay', 400)),
                    'MaxSpawnDelay': (2, tag.get('MaxSpawnDelay', 800)),
                    'SpawnCount': (2, tag.get('SpawnCount', 2)),
                    'MaxNearbyEntities': (2, tag.get('MaxNearbyEntities', 4)),
                    'RequiredPlayerRange': (2, tag.get('RequiredPlayerRange', 16)),
                    'SpawnRange': (2, tag.get('SpawnRange', 4)),
                    'SpawnData': (10, {'entity': (10, {'id': (8, tag['SpawnData']['entity']['id'])})}),
                })
            elif 'LootTable' in tag:
                entry['nbt'] = (10, {'LootTable': (8, tag['LootTable'])})
            elif 'mob' in tag:
                entry['nbt'] = (10, {
                    'id': (8, 'minecraft:mob_spawner'), 'Delay': (2, 200),
                    'MinSpawnDelay': (2, 400), 'MaxSpawnDelay': (2, 800),
                    'SpawnCount': (2, 2), 'MaxNearbyEntities': (2, 4),
                    'RequiredPlayerRange': (2, 16), 'SpawnRange': (2, 4),
                    'SpawnData': (10, {'entity': (10, {'id': (8, tag['mob'])})})})
        out_blocks.append(entry)
    root = {'DataVersion': (3, DATA_VERSION), 'size': (9, (3, spec['size'])),
            'palette': (9, (10, states)), 'blocks': (9, (10, out_blocks)),
            'entities': (9, (10, []))}
    Path(path).write_bytes(gzip.compress(b'\x0a\x00\x00' + wr_payload(10, root), mtime=0))


def augment(name, add_blocks):
    """add_blocks: list of (x, y, z, 'minecraft:id' or {'Name','Properties'})"""
    path = Path(SHOWCASE_PATH.format(f'{name}.nbt'))
    plain = read_nbt(path)
    palette = list(plain['palette'])
    key_to_idx = {}
    for i, s in enumerate(palette):
        key_to_idx[json.dumps(s, sort_keys=True)] = i
    blocks = list(plain['blocks'])
    occupied = {tuple(b['pos']) for b in blocks}
    manifest = path.with_suffix('.aug.json')
    if manifest.exists():
        prior = set(map(tuple, json.loads(manifest.read_text())))
        blocks = [b for b in blocks if tuple(b['pos']) not in prior]
        occupied = {tuple(b['pos']) for b in blocks}
    added = []
    for x, y, z, ref in add_blocks:
        state_ref = {'Name': ref} if isinstance(ref, str) else ref
        key = json.dumps(state_ref, sort_keys=True)
        if key not in key_to_idx:
            key_to_idx[key] = len(palette)
            palette.append(state_ref)
        si = key_to_idx[key]
        pos = (x, y, z)
        if pos in occupied:
            continue
        blocks.append({'pos': list(pos), 'state': si})
        occupied.add(pos)
        added.append(list(pos))
    new = {'size': plain['size'], 'palette': palette, 'blocks': blocks}
    write_nbt(path, new)
    manifest.write_text(json.dumps(added))
    print(f'{name}: +{len(added)} blocks (anchors untouched)')
