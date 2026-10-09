"""Read bounded saved chunks of an isolated ordinary server; never player saves.

Reports observed ores, underground flora, mine loot and village anchors. Missing
features in a small sample do not establish rarity or absence across a planet.
"""
import argparse
import gzip
import json
import struct
import sys
import zlib
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools/dev'))
import worldscan


def saved_entities(path, x, z):
    region = path / 'entities' / f'r.{x >> 5}.{z >> 5}.mca'
    if not region.exists():
        return []
    raw = region.read_bytes()
    if not raw:
        return []  # Minecraft may create an empty region when no entities exist.
    if len(raw) < 8192:
        raise ValueError('Incomplete saved entity region header')
    entry = struct.unpack_from('>I', raw, 4 * ((x & 31) + (z & 31) * 32))[0]
    if not entry:
        return []
    offset = (entry >> 8) * 4096
    length = struct.unpack_from('>I', raw, offset)[0]
    kind, payload = raw[offset + 4], raw[offset + 5:offset + 4 + length]
    if kind == 1:
        payload = gzip.decompress(payload)
    elif kind == 2:
        payload = zlib.decompress(payload)
    elif kind != 3:
        raise ValueError('Unsupported entity region compression')
    nbt = worldscan._read(payload, 3 + struct.unpack_from('>H', payload, 1)[0], 10)[0]
    return [entity.get('id', 'unknown') for entity in nbt.get('Entities', [])]


def survey(run, dimension, cx, cz, radius):
    ns, name = dimension.split(':')
    if ns != 'zerog_tweaks' or not name.replace('_', '').isalnum():
        raise ValueError('Only a simple ZeroG dimension ID is accepted')
    path = run / 'world/dimensions' / ns / name
    blocks, underground, loot = Counter(), Counter(), Counter()
    entities = Counter()
    anchors, structures, heights, coordinates = [], [], [], []
    for x in range(cx - radius, cx + radius + 1):
        for z in range(cz - radius, cz + radius + 1):
            chunk = worldscan.chunk(str(path), x, z)
            if not chunk or chunk.get('Status') not in {'minecraft:full', 'full'}:
                continue
            coordinates.append([x, z])
            entities.update(saved_entities(path, x, z))
            surface = None
            for section in chunk.get('sections', []):
                for index, block, y in worldscan.section_blocks(section):
                    if index & 15 == 8 and (index >> 4) & 15 == 8 and block not in {'minecraft:air', 'minecraft:cave_air', 'minecraft:void_air'}:
                        surface = y if surface is None else max(surface, y)
                    if block.startswith('zerog_tweaks:'):
                        blocks[block] += 1
                        if y < 32 and any(part in block for part in ('vine', 'kelp', 'mushroom', 'dripstone', 'lichen')):
                            underground[block] += 1
            if surface is not None:
                heights.append(surface)
            for be in chunk.get('block_entities', []):
                table = be.get('LootTable', '')
                if table.startswith('zerog_tweaks:'):
                    loot[table] += 1
                if be.get('id') == 'zerog_tweaks:settlement_anchor':
                    anchors.append({k: be.get(k) for k in ('x', 'y', 'z', 'residents', 'speciesResidents')})
            for key, start in chunk.get('structures', {}).get('starts', {}).items():
                if start.get('id') != 'INVALID':
                    structures.append({'chunk': [x, z], 'structure': key, 'pieces': len(start.get('Children', []))})
    return {'dimension': dimension, 'centre_chunk': [cx, cz], 'radius': radius,
            'saved_full_chunks': len(coordinates), 'surface_height_range': [min(heights), max(heights)] if heights else [],
            'ores': {k: v for k, v in sorted(blocks.items()) if k.endswith('_ore')},
            'observed_flora_below_y32': dict(sorted(underground.items())),
            'wood_and_support_blocks': {k: v for k, v in sorted(blocks.items()) if any(s in k for s in ('_planks', '_fence', '_door'))},
            'unopened_loot_tables': dict(sorted(loot.items())), 'settlement_anchors': anchors,
            'observed_saved_entity_types': dict(sorted(entities.items())),
            'natural_structure_starts': structures}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--site', action='append', required=True, help='dimension,chunkX,chunkZ,radius; radius 0..9')
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    run = args.run.resolve()
    if run.parent != ROOT or not run.name.startswith('run-local-ordinary-'):
        raise ValueError('Only isolated ordinary-server worlds are accepted')
    raw = gzip.decompress((run / 'world/level.dat').read_bytes())
    metadata = worldscan._read(raw, 3 + struct.unpack_from('>H', raw, 1)[0], 10)[0]['Data']['WorldGenSettings']
    if not metadata['generate_features']:
        raise ValueError('Natural structures must be enabled')
    rows = []
    for site in args.site:
        dimension, x, z, radius = site.split(',')
        radius = int(radius)
        if not 0 <= radius <= 9:
            raise ValueError('Bounded radius 0..9 required')
        rows.append(survey(run, dimension, int(x), int(z), radius))
    report = {'seed': metadata['seed'], 'ordinary_server': True, 'structures_enabled': True,
              'scope': 'Saved FULL chunks only. No natural mob population, all-biome coverage or client appearance certification.',
              'sites': rows}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(args.report), 'sites': len(rows), 'saved_full_chunks': sum(r['saved_full_chunks'] for r in rows)}))


if __name__ == '__main__':
    main()
