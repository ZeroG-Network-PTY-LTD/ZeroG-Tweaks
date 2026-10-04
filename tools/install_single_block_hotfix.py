"""Recoverable two-JAR installation; exact checksums, no saves/other mods touched."""
import argparse,datetime,hashlib,json,shutil
from pathlib import Path
from zipfile import ZipFile
p=argparse.ArgumentParser()
for key in ['instance','tweaks','addon']:p.add_argument('--'+key,type=Path,required=True)
for key in ['old-tweaks-sha','old-addon-sha','new-tweaks-sha','new-addon-sha']:p.add_argument('--'+key,required=True)
a=p.parse_args();digest=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
mods=a.instance/'mods';name1='zerog-tweaks-1.21.1-1.0.12-dev.jar';name2='zerog-binnie-expansion-1.21.1-1.0.0.jar'
rows=[(a.tweaks,mods/name1,a.old_tweaks_sha,a.new_tweaks_sha),(a.addon,mods/name2,a.old_addon_sha,a.new_addon_sha)]
assert list(mods.glob('zerog-tweaks*.jar'))==[mods/name1]
assert list(mods.glob('zerog-binnie-expansion*.jar'))==[mods/name2]
for source,target,old,new in rows:
 assert digest(source)==new and digest(target)==old,'Candidate or installed build changed; inspect before replacing'
 assert not target.with_suffix('.jar.pending').exists()
with ZipFile(a.tweaks) as jar:
 assert 'Implementation-Version: 1.0.12-dev' in jar.read('META-INF/MANIFEST.MF').decode()
 assert 'net/zerog/tweaks/client/MachineWorkbenchScreen.class' in jar.namelist()
 assert not any('/gametest/' in n and n.endswith('.class') for n in jar.namelist())
with ZipFile(a.addon) as jar:
 assert 'assets/aeroapiary/geo/machines/genetic_splicer.geo.json' not in jar.namelist()
 for id in ['genetic_splicer','geno_station']:
  model=json.loads(jar.read(f'assets/aeroapiary/models/block/other/{id}.json'))
  assert len(model['elements'])==1 and model['elements'][0]['to']==[16,16,16]
backup=a.instance/'zerog-mod-backups'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S-UTC-single-block-machines')
backup.mkdir(parents=True,exist_ok=False);staged=[];moved=[];installed=[]
try:
 for source,target,old,new in rows:
  pending=target.with_suffix('.jar.pending');shutil.copy2(source,pending);staged.append(pending);assert digest(pending)==new
 for source,target,old,new in rows:shutil.move(target,backup/target.name);moved.append(target)
 for source,target,old,new in rows:target.with_suffix('.jar.pending').rename(target);installed.append(target);assert digest(target)==new
except Exception:
 for target in installed:shutil.move(target,backup/('failed-new-'+target.name))
 for target in moved:shutil.move(backup/target.name,target)
 for pending in staged:
  if pending.exists():shutil.move(pending,backup/('failed-'+pending.name))
 raise
report={'backup':str(backup),'installed':[{'path':str(t),'sha256':digest(t)} for s,t,o,n in rows],'other_mods_and_saves_unchanged':True}
(backup/'installation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
