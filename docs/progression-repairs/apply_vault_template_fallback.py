"""Apply the tracker-approved Cerulon knowledge fallback after loot generation.

Usage: python apply_vault_template_fallback.py CODE/src/main/resources
Keeps IDs, existing pools/rolls and other entries. Idempotently adds the three
Galaxy-2 templates to Concord Vault uncommon loot at their Prism Spire weight 3.
This is first-acquisition loot, not new crafting costs or an implemented Spire.
"""
import argparse
import json
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('resources', type=Path)
a = p.parse_args()
path = a.resources / 'data/zerog_tweaks/loot_table/chests/concord_vault/uncommon.json'
data = json.loads(path.read_text())
assert data['type'] == 'minecraft:chest' and len(data['pools']) == 1
entries = data['pools'][0]['entries']
assert any(e.get('name') == 'zerog_tweaks:cobaltium_ingot' for e in entries)
for metal in ('cobaltium', 'cyrrium', 'aurelion'):
    name = f'zerog_tweaks:{metal}_upgrade_smithing_template'
    if not any(e.get('name') == name for e in entries):
        entries.append({'type': 'minecraft:item', 'name': name, 'weight': 3})
path.write_text(json.dumps(data, indent=2) + '\n')
print('Concord Vault uncommon template fallback is current.')
