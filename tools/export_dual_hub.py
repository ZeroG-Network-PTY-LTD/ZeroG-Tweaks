"""Stage a verified fresh dual-gate hub and 50 FULL chunks per custom planet.

Only the explicitly named compact hub can be replaced, recoverably. Test players,
faraway GameTest regions, forced chunk data and vanilla dimensions never ship.
"""
import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('tested', 'saves', 'nbt-library', 'verification-log', 'report'):
        p.add_argument('--' + name, type=Path, required=True)
    p.add_argument('--install', action='store_true')
    a = p.parse_args()
    source, saves = a.tested.resolve(), a.saves.resolve()
    assert source.name == 'world' and source.parent.name.startswith('run-local-dual-hub-')
    assert saves.name == 'saves' and saves.is_dir() and not source.is_relative_to(saves)
    log = a.verification_log.read_text(encoding='utf-8')
    assert re.search(r'All [1-9]\d* required tests passed', log) and 'BUILD SUCCESSFUL' in log
    receipt = json.loads((source / 'zerog-pregen50.json').read_text())
    assert receipt['chunks_per_dimension'] == 50 and receipt['total_requested_chunks'] == 1700
    assert len(receipt['dimensions']) == 34 and not receipt['permanent_forced_chunks']
    sys.path.insert(0, str(a.nbt_library.resolve()))
    sys.path.insert(0, str(Path(__file__).parent / 'dev'))
    import nbtlib
    from worldscan import chunk
    level = nbtlib.load(source / 'level.dat')
    assert int(level['Data']['WorldGenSettings']['seed']) == 0
    assert len(level['Data']['WorldGenSettings']['dimensions']) == 37
    ledger = nbtlib.load(source / 'data/zerog_planet_gates.dat')
    data = ledger['data']
    assert all(data.get(k) for k in ('compactHub', 'hubBuilt', 'tieredHubBuilt', 'playerHubBuilt', 'exhibitsBuilt', 'workshopBuilt'))
    assert int(data['prepared']) == 0 and int(data['inspectionPrepared']) == 0 and not data['inspectionEnabled']
    ids = set()
    for entry in receipt['dimensions']:
        identifier = entry['id']
        assert re.fullmatch(r'zerog_tweaks:(moon|mars|cerulon|skarn|eidolon|solvane|g[2-5]_(p[1-6]|moons))', identifier)
        assert identifier not in ids and entry['chunks'] == 50 and entry['return_gates'] == 12
        ids.add(identifier)
        folder = source / 'dimensions/zerog_tweaks' / identifier.split(':')[1]
        checked = 0
        for x in range(entry['min_chunk_x'], entry['max_chunk_x'] + 1):
            for z in range(entry['min_chunk_z'], entry['max_chunk_z'] + 1):
                saved = chunk(str(folder), x, z)
                assert saved and saved.get('Status') in ('minecraft:full', 'full'), f'Not FULL: {identifier} {x},{z}'
                checked += 1
        assert checked == 50
        assert not (folder / 'data/chunks.dat').exists(), f'Unexpected forced-chunk data: {identifier}'
    final = saves / 'ZeroG_Planet_Showcase_1_0_12_Compact_Hub_Seed0'
    result = {'installed': False, 'destination': str(final), 'seed': 0, 'admin_gates': 6, 'player_gates': 6,
              'planet_dimensions': 34, 'requested_full_chunks_per_dimension': 50, 'requested_full_chunks': 1700,
              'vanilla_generation_margin': receipt['generation_margin_note'], 'forced_chunks_copied': False,
              'pregen_structure_starts_enabled': False, 'ordinary_future_structure_generation_enabled': True,
              'natural_structures_and_villages_in_pregen_sample_verified': False,
              'player_data_copied': False, 'unrelated_saves_changed': False, 'verification_log': str(a.verification_log)}
    if a.install:
        stamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-UTC')
        stage = saves.parent / 'zerog-hub-staging' / stamp / final.name
        stage.mkdir(parents=True, exist_ok=False)
        for folder in ('region', 'entities', 'poi'):
            for x in (-1, 0):
                for z in (-1, 0):
                    relative = Path(folder) / f'r.{x}.{z}.mca'
                    if (source / relative).exists():
                        (stage / folder).mkdir(exist_ok=True)
                        shutil.copy2(source / relative, stage / relative)
        assert len(list((stage / 'region').glob('*.mca'))) == 4
        (stage / 'data').mkdir()
        ledger.save(stage / 'data/zerog_planet_gates.dat')
        for identifier in sorted(ids):
            relative = Path('dimensions/zerog_tweaks') / identifier.split(':')[1]
            for folder in ('region', 'entities', 'poi'):
                source_folder = source / relative / folder
                if source_folder.exists():
                    # Only region files intersecting the requested 10x5 chunk rectangle.
                    for x in (0, 1):
                        for z in (1,):
                            file = source_folder / f'r.{x}.{z}.mca'
                            if file.exists():
                                target = stage / relative / folder
                                target.mkdir(parents=True, exist_ok=True)
                                shutil.copy2(file, target / file.name)
        d = level['Data']
        d['LevelName'] = nbtlib.String('ZeroG Compact Dual Gates — 50 chunks / planet — Seed 0')
        d['GameType'], d['allowCommands'] = nbtlib.Int(1), nbtlib.Byte(1)
        d['SpawnX'], d['SpawnY'], d['SpawnZ'] = map(nbtlib.Int, (0, 65, 0))
        d['DayTime'] = nbtlib.Long(1000)
        d['WorldGenSettings']['generate_features'] = nbtlib.Byte(1)
        d.pop('Player', None)
        for k, v in {'doDaylightCycle': 'true', 'doWeatherCycle': 'true', 'doMobSpawning': 'true',
                     'doMobLoot': 'true', 'doTileDrops': 'true', 'doFireTick': 'true', 'randomTickSpeed': '3'}.items():
            d['GameRules'][k] = nbtlib.String(v)
        level.save(stage / 'level.dat')
        shutil.copy2(source / 'zerog-pregen50.json', stage / 'zerog-pregen50.json')
        archive = saves.parent / 'zerog-hub-archives' / stamp / final.name
        if final.exists():
            archive.parent.mkdir(parents=True, exist_ok=False)
            shutil.move(str(final), str(archive))
        try:
            shutil.move(str(stage), str(final))
        except Exception:
            if archive.exists():
                shutil.move(str(archive), str(final))
            raise
        result.update(installed=True, archived_previous_hub=str(archive) if archive.exists() else None)
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
