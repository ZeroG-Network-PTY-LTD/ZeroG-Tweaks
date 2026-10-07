"""Trace shipped jigsaw pools to authored chest rewards, without opening saves.

This is potential source reachability, not a natural-generation or loot-roll test.
Imperative Java placement, processors and datapack overrides need separate checks.
"""
import argparse
import gzip
import json
import struct
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'dev'))
from worldscan import _read


def read_template(path):
    raw = path.read_bytes()
    if raw[:2] == b'\x1f\x8b':
        raw = gzip.decompress(raw)
    assert raw[0] == 10, f'Not a compound template: {path.name}'
    return _read(raw, 3 + struct.unpack_from('>H', raw, 1)[0], 10)[0]


def elements(element):
    """Flatten list pool elements without pretending feature elements are templates."""
    if element.get('element_type') == 'minecraft:list_pool_element':
        for child in element.get('elements', []):
            yield from elements(child)
    else:
        yield element


def trace(start, pools, templates):
    pending = deque([start]); visited = set(); reached = set(); missing = set(); other = set()
    while pending:
        pool_id = pending.popleft()
        if pool_id == 'minecraft:empty' or pool_id in visited:
            continue
        visited.add(pool_id)
        if pool_id not in pools:
            missing.add(pool_id); continue
        pool = pools[pool_id]
        pending.append(pool.get('fallback', 'minecraft:empty'))
        for weighted in pool.get('elements', []):
            if weighted.get('weight', 0) <= 0:
                continue
            for element in elements(weighted['element']):
                kind = element.get('element_type')
                if kind == 'minecraft:empty_pool_element':
                    continue
                if kind not in {'minecraft:single_pool_element', 'minecraft:legacy_single_pool_element'}:
                    other.add(str(kind)); continue
                template_id = element['location']; reached.add(template_id)
                if template_id not in templates:
                    missing.add(template_id); continue
                pending.extend(templates[template_id]['outgoing_pools'])
    return {'potential_pools': sorted(visited), 'potential_templates': sorted(reached),
            'missing_references': sorted(missing), 'non_template_elements': sorted(other)}


def audit(resources):
    root = resources / 'data/zerog_tweaks'; templates = {}; pools = {}; routes = {}
    for path in sorted((root / 'structure').rglob('*.nbt')):
        data = read_template(path)
        palettes = data.get('palettes', [data.get('palette', [])])
        outgoing = set(); loot = set()
        for block in data.get('blocks', []):
            nbt = block.get('nbt', {})
            if nbt.get('LootTable'):
                loot.add(nbt['LootTable'])
            if any(palette[block['state']]['Name'] == 'minecraft:jigsaw' for palette in palettes):
                if nbt.get('pool'):
                    outgoing.add(nbt['pool'])
        key = 'zerog_tweaks:' + path.relative_to(root / 'structure').with_suffix('').as_posix()
        templates[key] = {'outgoing_pools': sorted(outgoing), 'chest_tables': sorted(loot)}
    for path in sorted((root / 'worldgen/template_pool').rglob('*.json')):
        key = 'zerog_tweaks:' + path.relative_to(root / 'worldgen/template_pool').with_suffix('').as_posix()
        pools[key] = json.loads(path.read_text())
    for path in sorted((root / 'worldgen/structure').rglob('*.json')):
        data = json.loads(path.read_text()); start = data.get('start_pool')
        if not start:
            continue
        route = trace(start, pools, templates)
        route['biomes'] = data.get('biomes')
        route['potential_chest_tables'] = sorted({table for key in route['potential_templates']
            for table in templates.get(key, {}).get('chest_tables', [])})
        routes['zerog_tweaks:' + path.relative_to(root / 'worldgen/structure').with_suffix('').as_posix()] = route
    rewards = sorted('zerog_tweaks:' + p.relative_to(root / 'loot_table').with_suffix('').as_posix()
                     for p in (root / 'loot_table/chests').rglob('*.json'))
    potential = {table for route in routes.values() for table in route['potential_chest_tables']}
    return {'schema': 1, 'scope': 'Shipped jigsaw source graph only; no save access or natural placement proof',
            'structure_routes': routes, 'authored_templates': templates,
            'chest_tables_without_jigsaw_route': [key for key in rewards if key not in potential],
            'boundaries': ['Possible reachability does not guarantee a selected room or successful placement.',
                'Java-placed Courier, mineshaft chests and chamber stages are outside this jigsaw-only graph.',
                'Loot chances, player access, processors, biome filters and datapack overrides need runtime checks.']}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--resources', type=Path, default=Path('src/main/resources'))
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args(); report = audit(a.resources)
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'structures': len(report['structure_routes']),
        'missing_references': {key: row['missing_references'] for key,row in report['structure_routes'].items() if row['missing_references']},
        'chest_tables_without_jigsaw_route': report['chest_tables_without_jigsaw_route']}, indent=2))
