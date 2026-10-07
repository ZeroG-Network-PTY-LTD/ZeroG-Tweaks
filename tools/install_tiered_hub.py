"""Install only verified north-hub regions, six return regions and the gate ledger.

Dry run by default. Requires a stopped client; never replaces level.dat or players.
The source must be a tested copy of the SAME save, not a newly generated world.
"""
import argparse, hashlib, json, shutil, subprocess, tempfile
from datetime import datetime, timezone
from pathlib import Path
import sys

def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--save',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True);p.add_argument('--install',action='store_true')
    p.add_argument('--nbt-library',type=Path,required=True)
    a=p.parse_args();source=a.source.resolve();save=a.save.resolve()
    sys.path.insert(0,str(a.nbt_library.resolve()))
    import nbtlib
    assert source!=save and source.is_dir() and save.is_dir() and save.parent.name=='saves'
    ledger=nbtlib.load(source/'data/zerog_planet_gates.dat')
    assert int(ledger['data']['tieredHubBuilt'])==1,'Unverified tiered source ledger'
    assert int(nbtlib.load(source/'level.dat')['Data']['WorldGenSettings']['seed'])==int(nbtlib.load(save/'level.dat')['Data']['WorldGenSettings']['seed']), 'Source seed differs'
    # Do not copy test-server preparation counters or newly generated legacy routes.
    # Only migrate the existing save's north entries; its other routes remain exact.
    migrated=nbtlib.load(save/'data/zerog_planet_gates.dat')
    migrated['data']['tieredHubBuilt']=nbtlib.Byte(1)
    migrated['data']['gates']=nbtlib.List[nbtlib.Compound]([g for g in migrated['data']['gates'] if str(g['dimension'])!='minecraft:overworld'])
    with tempfile.NamedTemporaryFile(suffix='.dat',delete=False) as f:staged=Path(f.name)
    migrated.save(staged)
    protected=['level.dat','level.dat_old','playerdata','advancements','stats']
    original={str(f.relative_to(save)):sha(f) for name in protected for f in ([save/name] if (save/name).is_file() else (save/name).rglob('*')) if f.is_file()}
    paths=[Path('data/zerog_planet_gates.dat')]
    for kind in ['region','poi','entities']:
        for name in ['r.-1.-1.mca','r.0.-1.mca']:
            rel=Path(kind)/name
            if (source/rel).is_file():paths.append(rel)
        for dimension in ['moon','cerulon','skarn','eidolon','solvane','g5_moons']:
            rel=Path('dimensions/zerog_tweaks')/dimension/kind/'r.1.1.mca'
            if (source/rel).is_file():paths.append(rel)
    assert all((source/Path('dimensions/zerog_tweaks')/d/'region/r.1.1.mca').is_file() for d in ['moon','cerulon','skarn','eidolon','solvane','g5_moons'])
    backup=save.parent.parent/'zerog-hub-backups'/datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-UTC')
    report={'save':str(save),'source':str(source),'backup':str(backup),'installed':False,'files':[]}
    if a.install:
        proc=subprocess.run(['powershell.exe','-NoProfile','-Command','@(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq "javaw.exe" -and $_.CommandLine -match "Instances[\\/]+ZeroG" }).Count'],capture_output=True,text=True,check=True)
        assert proc.stdout.strip()=='0','Close the ZeroG client before installation'
        backup.mkdir(parents=True,exist_ok=False)
    for rel in paths:
        candidate=staged if rel==Path('data/zerog_planet_gates.dat') else source/rel
        target=save/rel; row={'file':rel.as_posix(),'before':sha(target) if target.exists() else None,'after':sha(candidate)}
        if a.install:
            if target.exists():
                saved=backup/rel;saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,saved)
            target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(candidate,target)
            assert sha(target)==row['after']
        report['files'].append(row)
    assert all(sha(save/rel)==value for rel,value in original.items()),'Player/global save data changed'
    staged.unlink()
    report['installed']=a.install;a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'installed':a.install,'files':len(paths),'backup':str(backup)},indent=2))

if __name__=='__main__':main()
