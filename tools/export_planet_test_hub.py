"""Export an isolated seed-0 hub as a NEW playable save; never modify the source."""
import argparse, json, re, shutil, sys
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--destination',type=Path,required=True)
    p.add_argument('--nbt-library',type=Path,required=True)
    p.add_argument('--export',action='store_true')
    p.add_argument('--verification-log',type=Path)
    p.add_argument('--label',default='ZeroG Planet Showcase 1.0.9 — Seed 0')
    a=p.parse_args();source=a.source.resolve();target=a.destination.resolve()
    assert (source/'level.dat').is_file() and (source/'zerog-hub-report.json').is_file()
    if a.verification_log:
        log=a.verification_log.read_text(encoding='utf-8')
        assert re.search(r'All [1-9]\d* required tests passed',log) and 'BUILD SUCCESSFUL' in log, 'Passing test transcript required'
    assert target.parent.name=='saves' and not target.exists(), 'Only a NEW save in saves/ is permitted'
    assert not target.is_relative_to(source) and not source.is_relative_to(target)
    sys.path.insert(0,str(a.nbt_library.resolve()))
    import nbtlib
    report=json.loads((source/'zerog-hub-report.json').read_text())
    level=nbtlib.load(source/'level.dat');d=level['Data']
    assert report['seed']==int(d['WorldGenSettings']['seed'])==0
    assert report['gate_count']==68 and len(report['planets'])==34
    assert len(d['WorldGenSettings']['dimensions'])==37
    assert str(d['WorldGenSettings']['dimensions']['minecraft:overworld']['generator']['settings']['biome'])=='zerog_tweaks:planet_test_hub'
    result={'source':str(source),'destination':str(target),'seed':0,'gates':68,
            'exported':False,'existing_saves_changed':False,
            'player_travel_tested':report.get('player_travel_tested',False),
            'demonstration_colonies':report.get('demonstration_colonies',True),
            'nearby_inspection_villages':report.get('nearby_inspection_villages',False),
            'inspection_village_count':sum(len(p.get('inspection_village_positions',[])) for p in report['planets']),
            'caveat':'Fresh independently seeded terrain; '+('1–2 terrain-grounded inspection villages near each planetary gate.' if report.get('nearby_inspection_villages',False) else ('34 demonstration colonies.' if report.get('demonstration_colonies',True) else 'No demonstration colonies; only rare natural village generation.'))+' Small samples do not certify complete ecology or client graphics.'}
    if a.export:
        target.parent.mkdir(parents=True,exist_ok=True)
        def ignore(directory,names):
            omitted=set(shutil.ignore_patterns('session.lock','playerdata','advancements','stats','level.dat_old')(directory,names))
            folder=Path(directory)
            if folder.parent==source and folder.name in ('region','entities','poi'):
                for name in names:
                    match=re.fullmatch(r'r\.(-?\d+)\.(-?\d+)\.mca',name)
                    if match and (abs(int(match[1]))>1 or abs(int(match[2]))>1):omitted.add(name)
            return omitted
        shutil.copytree(source,target,ignore=ignore)
        exported=nbtlib.load(target/'level.dat');data=exported['Data']
        data['LevelName']=nbtlib.String(a.label)
        data['DayTime']=nbtlib.Long(1000)
        data['GameType']=nbtlib.Int(1)
        data['allowCommands']=nbtlib.Byte(1)
        data['SpawnX']=nbtlib.Int(0);data['SpawnY']=nbtlib.Int(65);data['SpawnZ']=nbtlib.Int(0)
        data['WorldGenSettings']['generate_features']=nbtlib.Byte(1)
        for key in ['doMobSpawning','doDaylightCycle','doWeatherCycle','doMobLoot','doTileDrops']:
            data['GameRules'][key]=nbtlib.String('true')
        data['GameRules']['randomTickSpeed']=nbtlib.String('3')
        # The isolated fake player's data must not become the singleplayer avatar.
        data.pop('Player',None)
        exported.save()
        assert int(nbtlib.load(target/'level.dat')['Data']['WorldGenSettings']['seed'])==0
        result['exported']=True
        (target/'zerog-export-report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
