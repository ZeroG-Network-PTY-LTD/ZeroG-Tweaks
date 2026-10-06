"""Export only a verified workshop region into a new copy of the player's hub."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import shutil
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, required=True)
parser.add_argument('--tested', type=Path, required=True)
parser.add_argument('--destination', type=Path, required=True)
parser.add_argument('--nbt-library', type=Path, required=True)
parser.add_argument('--verification-log', type=Path, required=True)
parser.add_argument('--report', type=Path, required=True)
args = parser.parse_args()
source, tested, destination = (p.resolve() for p in (args.source, args.tested, args.destination))
if destination.exists() or destination.parent != source.parent or destination.parent.name != 'saves':
    raise SystemExit('Only a new sibling save is permitted; existing saves are never overwritten.')
if not destination.name.startswith('ZeroG_Planet_Showcase_') or tested == source:
    raise SystemExit('Expected an isolated tested world and a named ZeroG showcase destination.')
verification = args.verification_log.read_text(encoding='utf-8')
if not re.search(r'All [1-9]\d* required tests passed', verification) or 'BUILD SUCCESSFUL' not in verification:
    raise SystemExit('The supplied verification log does not show a passing required-test run.')
sys.path.insert(0, str(args.nbt_library.resolve()))
import nbtlib

ledger_path = Path('data/zerog_planet_gates.dat')
source_ledger = nbtlib.load(source / ledger_path)
tested_ledger = nbtlib.load(tested / ledger_path)
if not tested_ledger['data'].get('workshopBuilt') or not source_ledger['data'].get('exhibitsBuilt'):
    raise SystemExit('Verified workshop / original hub exhibits are required.')
if int(source_ledger['data']['prepared']) != 34 or len(source_ledger['data']['gates']) != 68:
    raise SystemExit('Expected the complete 34-destination / 68-gate hub.')

def snapshot(root):
    return {str(p.relative_to(root)): hashlib.file_digest(p.open('rb'), 'sha256').hexdigest()
            for p in root.rglob('*') if p.is_file() and p.name != 'session.lock'}

before = snapshot(source)
# Preserve original terrain, inventories, entities, progression and mod metadata.
shutil.copytree(source, destination, ignore=shutil.ignore_patterns('session.lock'))
# The workshop occupies negative X/Z entirely inside this one region. Do not
# export distant GameTest regions or overwrite existing apiary/gallery chunks.
region = Path('region/r.-1.-1.mca')
shutil.copy2(tested / region, destination / region)
source_ledger['data']['workshopBuilt'] = nbtlib.Byte(1)
source_ledger.save(destination / ledger_path)
forced = nbtlib.load(destination / 'data/chunks.dat')
chunks = {int(n) for n in forced['data']['Forced']}
for cx in range(-7, 0):
    for cz in range(-7, 0):
        unsigned = (cx & 0xffffffff) | ((cz & 0xffffffff) << 32)
        chunks.add(unsigned if unsigned < 1 << 63 else unsigned - (1 << 64))
forced['data']['Forced'] = nbtlib.LongArray(sorted(chunks))
forced.save(destination / 'data/chunks.dat')
level = nbtlib.load(destination / 'level.dat')
level['Data']['LevelName'] = nbtlib.String('ZeroG Supplied Workshop 1.0.12 — Seed 0')
level['Data']['DayTime'] = nbtlib.Long(1000)  # Solar inspection starts in daylight.
level.save(destination / 'level.dat')
if before != snapshot(source):
    raise SystemExit('Original save changed during export; stop and inspect before delivery.')
report = {'source': str(source), 'destination': str(destination), 'original_unchanged': True,
          'copied_workshop_region': str(region), 'gate_count': 68, 'prepared_planets': 34,
          'original_player_data_preserved': True, 'distant_test_regions_excluded': True,
          'survival_recipes_changed': False, 'verification_log': str(args.verification_log)}
args.report.parent.mkdir(parents=True, exist_ok=True)
args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, indent=2))
