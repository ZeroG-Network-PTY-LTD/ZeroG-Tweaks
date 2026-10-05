"""Inspect mod IDs and recoverably install one verified ZeroG development jar.

Dry-run by default. Does not launch Minecraft or edit saves/configs/other mods.
"""
import argparse,hashlib,json,shutil,tempfile,tomllib
from datetime import datetime,timezone
from pathlib import Path
from zipfile import ZipFile

def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def mod_ids(path):
    with ZipFile(path) as jar:
        for name in ['META-INF/neoforge.mods.toml','META-INF/mods.toml']:
            if name in jar.namelist():return {m['modId'] for m in tomllib.loads(jar.read(name).decode()).get('mods',[])}
    return set()
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--jar',type=Path,required=True);p.add_argument('--mods',type=Path,required=True);p.add_argument('--sha256',required=True);p.add_argument('--install',action='store_true');p.add_argument('--report',type=Path);a=p.parse_args()
    def emit(report):
        payload=json.dumps(report,indent=2)
        if a.report:
            a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(payload+'\n')
        print(payload)
    source=a.jar.resolve();mods=a.mods.resolve();assert mods.is_dir() and mods.name=='mods','Existing exact mods directory required'
    assert source.is_file() and source.suffix=='.jar' and source.parent!=mods
    assert sha(source)==a.sha256,'Candidate hash changed';assert mod_ids(source)=={'zerog_tweaks'},'Unexpected candidate mod IDs'
    installed=list(mods.glob('*.jar'));duplicates=[];preserved=[]
    for path in installed:
        ids=mod_ids(path)
        if 'zerog_tweaks' in ids:
            assert ids=={'zerog_tweaks'},'Refuse to move a multi-mod jar';duplicates.append(path)
        elif ids.intersection({'aeroapiary','geckolib','productivebees'}):preserved.append({'name':path.name,'ids':sorted(ids),'sha256':sha(path)})
    target=mods/source.name;already=target.exists() and sha(target)==a.sha256
    obsolete=[path for path in duplicates if not (already and path==target)]
    report={'candidate':str(source),'target':str(target),'sha256':a.sha256,'installed':False,'conflicts':[path.name for path in obsolete],'preserved_dependencies':preserved}
    if not a.install:emit(report);return
    backup=mods.parent/'zerog-mod-backups'/datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-UTC')
    moved=[];temporary=None
    try:
        if not already:
            with tempfile.NamedTemporaryFile(prefix='zerog-install-',suffix='.tmp',dir=mods,delete=False) as stream:temporary=Path(stream.name)
            shutil.copyfile(source,temporary);assert sha(temporary)==a.sha256
        if obsolete:backup.mkdir(parents=True,exist_ok=False)
        for path in obsolete:
            destination=backup/path.name;assert not destination.exists();path.rename(destination);moved.append((path,destination))
        if not already:temporary.replace(target);temporary=None
        assert sha(target)==a.sha256
        remaining=[path for path in mods.glob('*.jar') if 'zerog_tweaks' in mod_ids(path)]
        assert remaining==[target],'Duplicate ZeroG Tweaks remains'
        for row in preserved:assert sha(mods/row['name'])==row['sha256'],'Dependency unexpectedly changed'
    except Exception:
        if temporary is not None and temporary.exists():temporary.unlink()
        if not already and target.exists() and sha(target)==a.sha256:
            backup.mkdir(parents=True,exist_ok=True);target.rename(backup/('failed-candidate-'+target.name))
        for original,saved in reversed(moved):
            if saved.exists() and not original.exists():saved.rename(original)
        raise
    report.update(installed=True,backup=str(backup) if obsolete else None,backed_up=[destination.name for _,destination in moved]);emit(report)
if __name__=='__main__':main()
