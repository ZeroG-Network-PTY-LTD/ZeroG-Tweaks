"""Admit verified new far-away structure regions only; never overwrite exploration."""
import argparse,hashlib,json,re,shutil
from pathlib import Path

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--tested',type=Path,required=True);p.add_argument('--save',type=Path,required=True)
p.add_argument('--verification-log',type=Path,required=True);p.add_argument('--report',type=Path,required=True)
p.add_argument('--install',action='store_true');a=p.parse_args()
source=a.tested.resolve();target=a.save.resolve()
assert source.name=='world' and source.parent.name.startswith('run-local-kimi-sites-')
assert target.name=='ZeroG_Fresh_Workshop_20261014_Seed0' and target.parent.name=='saves'
assert (target/'level.dat').is_file() and not target.is_symlink()
log=a.verification_log.read_text();assert re.search(r'All [1-9]\d* required tests passed',log) and 'BUILD SUCCESSFUL' in log
receipt=json.loads((source/'zerog-kimi-sites.json').read_text());assert receipt['version']==1 and not receipt['natural_generation']
expected={'ice_spire_outpost':'eidolon','water_bio_habitat':'cerulon','hot_ring_monolith':'skarn'}
assert {s['name']:s['planet'] for s in receipt['sites']}==expected
copies=[]
for site in receipt['sites']:
    planet=site['planet'];x,y,z=site['origin'];assert 4096<=x<10000 and 4096<=z<10000
    relative=Path('dimensions/zerog_tweaks')/planet
    width=54 if site['name']=='ice_spire_outpost' else 48
    for rx in range(x//512,(x+width-1)//512+1):
        for rz in range(z//512,(z+width-1)//512+1):
            for folder in ('region','entities','poi'):
                path=relative/folder/f'r.{rx}.{rz}.mca'
                if (source/path).exists():copies.append(path)
    path=relative/'data/zerog_showcase_sites.dat';assert (source/path).is_file();copies.append(path)
copies=list(dict.fromkeys(copies));assert len(copies)<=39
for path in copies:
    assert not (target/path).exists(),f'Refuse existing explored region/site data: {path}'
    assert not (source/path).is_symlink()
report={'installed':False,'save':str(target),'sites':receipt['sites'],'overworld_untouched':True,'forced_chunks_copied':False,'files':{str(path):hashlib.sha256((source/path).read_bytes()).hexdigest() for path in copies}}
if a.install:
    for path in copies:(target/path).parent.mkdir(parents=True,exist_ok=True)
    staged=[];committed=[]
    try:
        for path in copies:
            tmp=(target/path).with_suffix('.zerog-site-staging');assert not tmp.exists();shutil.copyfile(source/path,tmp);staged.append((tmp,target/path))
            assert hashlib.sha256(tmp.read_bytes()).hexdigest()==report['files'][str(path)]
        for tmp,dest in staged:
            assert not dest.exists(),'Target appeared during staging; refuse overwrite'
            tmp.replace(dest);committed.append(dest)
        report['installed']=True
    except Exception:
        for dest in reversed(committed):
            key=str(dest.relative_to(target))
            if dest.is_file() and hashlib.sha256(dest.read_bytes()).hexdigest()==report['files'][key]:dest.unlink()
        raise
    finally:
        for tmp,dest in staged:
            if tmp.exists():tmp.unlink()
a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
