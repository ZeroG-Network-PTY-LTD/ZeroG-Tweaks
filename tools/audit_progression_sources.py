"""Read-only progression provenance: loot definitions are not worldgen proof.

Reports item sources, authored template bindings, configured structure pools,
and Java loot hooks separately. Never opens a player save or generates terrain.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--resources', type=Path, default=Path('src/main/resources'))
p.add_argument('--java', type=Path, default=Path('src/main/java'))
p.add_argument('--nbt-library', type=Path, required=True)
p.add_argument('--report', type=Path, required=True)
a = p.parse_args()
sys.path.insert(0, str(a.nbt_library.resolve()))
import nbtlib

root = a.resources / 'data/zerog_tweaks'
sources = defaultdict(list)
bindings = defaultdict(list)
structures = {}
hooks = []

def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)

for path in sorted((root / 'loot_table').rglob('*.json')):
    key = 'zerog_tweaks:' + path.relative_to(root / 'loot_table').with_suffix('').as_posix()
    for node in walk(json.loads(path.read_text())):
        name = node.get('name', '')
        if node.get('type') == 'minecraft:item' and ('upgrade_smithing_template' in name or 'gate_key' in name or 'concord_vault_key' in name):
            sources[name].append({'loot_table': key, 'weight': node.get('weight', 1),
                                  'entry_conditions': node.get('conditions', [])})

for path in sorted((root / 'structure').rglob('*.nbt')):
    template = nbtlib.load(path)
    key = 'zerog_tweaks:' + path.relative_to(root / 'structure').with_suffix('').as_posix()
    for block in template.get('blocks', []):
        loot = block.get('nbt', {}).get('LootTable')
        if loot:
            bindings[str(loot)].append(key)

for path in sorted((root / 'worldgen/structure').glob('*.json')):
    data = json.loads(path.read_text())
    structures[path.stem] = {'type': data['type'], 'start_pool': data.get('start_pool'),
                             'biomes': data.get('biomes')}

for path in sorted(a.java.rglob('*.java')):
    lines = path.read_text().splitlines()
    for number, line in enumerate(lines, 1):
        if 'chests/' in line:
            hooks.append({'file': path.relative_to(a.java).as_posix(), 'line': number,
                          'literal_tables': re.findall(r'"(chests/[^"\n]+)"', line),
                          'scope': 'Source reference only; review call site and placement conditions'})

rows = []
for item, entries in sorted(sources.items()):
    rows.append({'item': item, 'loot_sources': entries,
                 'authored_chest_bindings': {e['loot_table']: sorted(set(bindings[e['loot_table']])) for e in entries},
                 'natural_obtainability': 'Not established by this static audit; requires generated structure/entity gameplay checks'})

report = {'schema': 1, 'scope': 'Static shipped-source provenance, not natural generation or client approval',
          'items': rows, 'configured_structures': structures, 'java_chest_hooks': hooks,
          'unbound_chest_sources': sorted({e['loot_table'] for row in rows for e in row['loot_sources']
                                          if e['loot_table'].startswith('zerog_tweaks:chests/') and not bindings[e['loot_table']]}),
          'boundaries': ['Crafting/template duplication is not a first-acquisition source.',
                         'An authored chest template is not proof that its jigsaw pool generates.',
                         'Entity loot is not proof that the entity naturally spawns or can be defeated.',
                         'Nested loot-table references and datapack overrides require separate runtime inspection.']}
a.report.parent.mkdir(parents=True, exist_ok=True)
a.report.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'items': len(rows), 'configured_structures': len(structures),
                  'unbound_chest_sources': report['unbound_chest_sources'],
                  'report_sha256': hashlib.sha256(a.report.read_bytes()).hexdigest()}, indent=2))
