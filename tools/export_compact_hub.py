"""Export a verified compact Overworld hub; planets generate on first visit.

Never copies GameTest regions, planetary terrain, forced chunks or test players.
Only the named former Cardinal Hub may be recoverably archived.
"""
import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--tested', type=Path, required=True)
p.add_argument('--saves', type=Path, required=True)
p.add_argument('--nbt-library', type=Path, required=True)
p.add_argument('--verification-log', type=Path, required=True)
p.add_argument('--report', type=Path, required=True)
p.add_argument('--archive-cardinal', action='store_true')
a = p.parse_args()
tested, saves = a.tested.resolve(), a.saves.resolve()
assert saves.is_dir() and saves.name == 'saves'
destination = saves / 'ZeroG_Planet_Showcase_1_0_12_Compact_Hub_Seed0'
assert not destination.exists(), 'Refuse to overwrite an existing save'
log = a.verification_log.read_text(encoding='utf-8')
assert re.search(r'All [2-9]\d* required tests passed', log) and 'BUILD SUCCESSFUL' in log
sys.path.insert(0, str(a.nbt_library.resolve()))
import nbtlib

ledger = nbtlib.load(tested / 'data/zerog_planet_gates.dat')
data = ledger['data']
assert all(data.get(key) for key in ('compactHub', 'hubBuilt', 'tieredHubBuilt', 'exhibitsBuilt', 'workshopBuilt'))
assert int(data['prepared']) == 0 and int(data['inspectionPrepared']) == 0
assert not data['inspectionEnabled']
level = nbtlib.load(tested / 'level.dat')
assert int(level['Data']['WorldGenSettings']['seed']) == 0
assert len(level['Data']['WorldGenSettings']['dimensions']) == 37
assert all((tested / 'region' / f'r.{x}.{z}.mca').is_file() for x in (-1,0) for z in (-1,0))

destination.mkdir()
copied = []
for folder in ('region', 'entities', 'poi'):
    for x in (-1, 0):
        for z in (-1, 0):
            relative = Path(folder) / f'r.{x}.{z}.mca'
            source = tested / relative
            if source.exists():
                (destination / folder).mkdir(exist_ok=True)
                shutil.copy2(source, destination / relative)
                copied.append(relative.as_posix())
assert len([v for v in copied if v.startswith('region/')]) == 4
(destination / 'data').mkdir()
ledger.save(destination / 'data/zerog_planet_gates.dat')
d = level['Data']
d['LevelName'] = nbtlib.String('ZeroG Compact Hub 1.0.12 — Seed 0')
d['GameType'] = nbtlib.Int(1)
d['allowCommands'] = nbtlib.Byte(1)
d['SpawnX'], d['SpawnY'], d['SpawnZ'] = map(nbtlib.Int, (0, 65, 0))
d['DayTime'] = nbtlib.Long(1000)
d.pop('Player', None)
for name, value in {'doDaylightCycle': 'true', 'doWeatherCycle': 'true', 'doMobSpawning': 'true', 'randomTickSpeed': '3'}.items():
    d['GameRules'][name] = nbtlib.String(value)
level.save(destination / 'level.dat')
assert not (destination / 'dimensions').exists()
assert not (destination / 'data/chunks.dat').exists()
archive = None
old = saves / 'ZeroG_Planet_Showcase_1_0_12_Cardinal_Hub_Seed0'
if a.archive_cardinal and old.exists():
    archive = saves.parent / 'zerog-hub-archives' / datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-UTC') / old.name
    archive.parent.mkdir(parents=True, exist_ok=False)
    shutil.move(str(old), str(archive))
report = {'installed': True, 'destination': str(destination), 'archived_cardinal': str(archive) if archive else None,
          'seed': 0, 'gate_tiers': list(range(1, 7)), 'admin_travel': True,
          'planetary_terrain_copied': False, 'planetary_generation': 'on first visit',
          'forced_chunks_copied': False, 'copied_overworld_files': copied,
          'save_changes': True, 'unrelated_saves_changed': False,
          'verification_log': str(a.verification_log),
          'files': {f.relative_to(destination).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest()
                    for f in destination.rglob('*') if f.is_file()}}
a.report.parent.mkdir(parents=True, exist_ok=True)
a.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, indent=2))
