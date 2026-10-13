"""ZeroG Structure Workshop: deterministic Java 1.21.1 NBT, no services required.

This is a project-native structure compiler, NOT the game-dev asset CLI. It does
not generate artwork, install content, edit saves, or activate natural spawning.
"""
import argparse
import gzip
import hashlib
import json
import re
import struct
from pathlib import Path

VERSION = '0.1.0'
DATA_VERSION = 3955  # Java Minecraft 1.21.1
ID = re.compile(r'^[a-z0-9_.-]+:[a-z0-9_./-]+$')
FORBIDDEN_LOOT = {'dormant_wisp', 'concord_codex', 'broken_console'}


def valid_id(value):
    if not isinstance(value, str) or not ID.fullmatch(value):
        return False
    path = value.split(':', 1)[1]
    return all(part not in ('', '.', '..') for part in path.split('/'))


def validate(spec, assets=None):
    if spec.get('schema') != 1:
        raise ValueError('Expected structure specification schema 1')
    size = spec.get('size')
    if not isinstance(size, list) or len(size) != 3 or any(type(n) is not int or not 1 <= n <= 128 for n in size):
        raise ValueError('Size must contain three integers in 1..128')
    palette = spec.get('palette', [])
    if not palette or len(palette) > 1024:
        raise ValueError('Palette must contain 1..1024 states')
    for state in palette:
        name = state.get('Name', '')
        if not valid_id(name):
            raise ValueError(f'Invalid block identifier: {name}')
        props = state.get('Properties', {})
        if not isinstance(props, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in props.items()):
            raise ValueError('Block properties must be string pairs')
        if assets and name.startswith('zerog_tweaks:'):
            if not (Path(assets) / 'blockstates' / (name.split(':', 1)[1] + '.json')).is_file():
                raise ValueError(f'Unknown local block asset: {name}')
    seen = set()
    blocks = spec.get('blocks', [])
    if not isinstance(blocks, list) or not 1 <= len(blocks) <= 300000:
        raise ValueError('Expected 1..300000 explicitly authored blocks')
    for block in blocks:
        pos, state = block.get('pos'), block.get('state')
        if not isinstance(pos, list) or len(pos) != 3 or any(type(n) is not int or not 0 <= n < size[i] for i, n in enumerate(pos)):
            raise ValueError(f'Block outside structure bounds: {pos}')
        if tuple(pos) in seen:
            raise ValueError(f'Duplicate block coordinate: {pos}')
        seen.add(tuple(pos))
        if type(state) is not int or not 0 <= state < len(palette):
            raise ValueError(f'Invalid palette index at {pos}')
        tag = block.get('nbt', {})
        if not isinstance(tag, dict):
            raise ValueError('Block entity NBT must be an object')
        if tag:
            name = palette[state]['Name']
            if name in ('minecraft:chest', 'minecraft:barrel'):
                if set(tag) - {'LootTable'} or not valid_id(tag.get('LootTable', '')):
                    raise ValueError('Loot containers accept one approved LootTable only')
            elif name == 'minecraft:spawner':
                if set(tag) != {'mob'} or not valid_id(tag.get('mob', '')):
                    raise ValueError('Spawner requires exactly one mob identifier')
            else:
                raise ValueError('Only loot containers/spawners support authored block NBT')
    # Room/clearance volumes are explicit air blocks, not destructive fill commands.
    loot = spec.get('loot_tables', {})
    for name, table in loot.items():
        if not valid_id(name) or not isinstance(table, dict):
            raise ValueError('Invalid loot table')
        raw = json.dumps(table)
        if any(word in raw for word in FORBIDDEN_LOOT) or 'gate_key' in raw or 'smithing_template' in raw:
            raise ValueError('Story loot requires a separate approved reward contract')
        if table.get('type') != 'minecraft:chest' or not isinstance(table.get('pools'), list):
            raise ValueError('Expected a Minecraft chest loot table')
    for block in blocks:
        table = block.get('nbt', {}).get('LootTable')
        if table and table not in loot and table not in spec.get('existing_loot_tables', []):
            raise ValueError(f'Unresolved loot table: {table}')
    return {'size': size, 'blocks': len(blocks), 'palette_states': len(palette),
            'loot_containers': sum('LootTable' in b.get('nbt', {}) for b in blocks),
            'spawners': sum('mob' in b.get('nbt', {}) for b in blocks)}


def utf(value):
    raw = value.encode('utf-8')
    return struct.pack('>H', len(raw)) + raw


def payload(kind, value):
    if kind == 2:
        return struct.pack('>h', value)
    if kind == 3:
        return struct.pack('>i', value)
    if kind == 8:
        return utf(value)
    if kind == 9:
        subtype, values = value
        return bytes([subtype]) + struct.pack('>i', len(values)) + b''.join(payload(subtype, v) for v in values)
    if kind == 10:
        return b''.join(bytes([t]) + utf(k) + payload(t, v) for k, (t, v) in value.items()) + b'\0'
    raise ValueError(f'Unsupported NBT type: {kind}')


def nbt_bytes(spec):
    validate(spec)
    states = []
    for state in spec['palette']:
        entry = {'Name': (8, state['Name'])}
        if state.get('Properties'):
            entry['Properties'] = (10, {k: (8, v) for k, v in sorted(state['Properties'].items())})
        states.append(entry)
    blocks = []
    for block in sorted(spec['blocks'], key=lambda b: tuple(b['pos'])):
        entry = {'pos': (9, (3, block['pos'])), 'state': (3, block['state'])}
        tag = block.get('nbt', {})
        if 'LootTable' in tag:
            entry['nbt'] = (10, {'LootTable': (8, tag['LootTable'])})
        if 'mob' in tag:
            entry['nbt'] = (10, {
                'id': (8, 'minecraft:mob_spawner'), 'Delay': (2, 200),
                'MinSpawnDelay': (2, 400), 'MaxSpawnDelay': (2, 800),
                'SpawnCount': (2, 2), 'MaxNearbyEntities': (2, 4),
                'RequiredPlayerRange': (2, 16), 'SpawnRange': (2, 4),
                'SpawnData': (10, {'entity': (10, {'id': (8, tag['mob'])})})})
        blocks.append(entry)
    root = {'DataVersion': (3, DATA_VERSION), 'size': (9, (3, spec['size'])),
            'palette': (9, (10, states)), 'blocks': (9, (10, blocks)),
            'entities': (9, (10, []))}
    return gzip.compress(b'\x0a\x00\x00' + payload(10, root), mtime=0)


def build(spec, destination, assets=None):
    report = validate(spec, assets)
    destination = Path(destination)
    if destination.exists():
        raise ValueError('Output exists; choose a new versioned destination')
    # Validate/serialize before creating any destination.
    nbt = nbt_bytes(spec)
    destination.mkdir(parents=True)
    files = {'structure.nbt': nbt,
             'source.json': (json.dumps(spec, indent=2) + '\n').encode()}
    for name, table in spec.get('loot_tables', {}).items():
        namespace, path = name.split(':', 1)
        files[f'data/{namespace}/loot_table/{path}.json'] = (json.dumps(table, indent=2) + '\n').encode()
    for name, data in files.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    receipt = {'tool': 'zerog-structure-workshop', 'version': VERSION,
               'minecraft': '1.21.1', 'validation': report,
               'evidence': 'static NBT export only; not in-game placement or visual approval',
               'sha256': {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}}
    (destination / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version=VERSION)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor')
    for name in ('validate', 'build'):
        child = sub.add_parser(name)
        child.add_argument('source', type=Path)
        child.add_argument('--assets', type=Path)
        if name == 'build':
            child.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'doctor':
            result = {'tool': 'zerog-structure-workshop', 'version': VERSION,
                      'dependencies': 'Python standard library only',
                      'exports': ['Java 1.21.1 structure NBT', 'loot JSON', 'SHA256 receipt'],
                      'limitations': ['No image-to-geometry conversion', 'No asset CLI emulation',
                                      'No natural-generation activation', 'No live-save writes']}
        else:
            spec = json.loads(args.source.read_text(encoding='utf-8'))
            result = build(spec, args.output, args.assets) if args.command == 'build' else validate(spec, args.assets)
        print(json.dumps(result, indent=2))
    except (ValueError, OSError, KeyError) as error:
        parser.exit(2, f'{error}\n')


if __name__ == '__main__':
    main()
