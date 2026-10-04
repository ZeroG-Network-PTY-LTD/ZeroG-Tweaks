"""Resource-only replacement of two user-owned addon models. Never modifies classes.
Writes a NEW candidate; installation/backups are a separate operation.
"""
import argparse,hashlib,json
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
p=argparse.ArgumentParser();p.add_argument('--addon',type=Path,required=True);p.add_argument('--design',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
assert not a.output.exists(),'Use a fresh candidate path; do not overwrite an unreviewed JAR'
base=a.design/'docs/single-block-machines-v1';manifest=json.loads((base/'manifest.json').read_text())
replacements={row['path']:(base/'source'/row['path']).read_bytes() for row in manifest['files'] if row['path'].startswith('assets/aeroapiary/')}
obsolete={
 'assets/aeroapiary/geo/machines/genetic_splicer.geo.json',
 'assets/aeroapiary/animations/genetic_splicer.animation.json',
 'assets/aeroapiary/textures/block/genetic_splicer_front.png',
 'assets/aeroapiary/textures/block/genetic_splicer_side.png',
 'assets/aeroapiary/textures/block/genetic_splicer_top.png',
 'assets/aeroapiary/textures/block/machines/genetic_splicer_hd.png',
 'assets/aeroapiary/textures/block/machines/genetic_splicer_hd_emissive.png',
 'assets/aeroapiary/textures/block/machines/genetic_splicer_hd_glowmask.png',
 'assets/aeroapiary/textures/block/other/geno_station.png',
 'assets/aeroapiary/textures/block/other/geno_station_emissive.png',
 'assets/aeroapiary/textures/block/other/geno_station_glowmask.png',
 'assets/aeroapiary/textures_emissive/block/machines/genetic_splicer_hd.png',
 'assets/aeroapiary/textures_emissive/block/other/geno_station.png',
}
with ZipFile(a.addon) as old:
 assert not any(n.upper().endswith(('.SF','.RSA','.DSA')) for n in old.namelist()),'Signed JAR must not be repacked'
 contents={n:old.read(n) for n in old.namelist() if not n.endswith('/')}
 assert obsolete.issubset(contents),'Unexpected baseline: inspect removed resources first'
 removed_refs={n.removeprefix('assets/aeroapiary/').removeprefix('textures/').removesuffix('.png') for n in obsolete if n.endswith('.png')}
 result={n:v for n,v in contents.items() if n not in obsolete};result.update(replacements)
 def texture_refs(obj):
  if isinstance(obj,dict):
   for key,value in obj.items():
    if key=='textures' and isinstance(value,dict):
     for v in value.values():
      if isinstance(v,str):yield v
    if key=='texture' and isinstance(value,str):yield value
    yield from texture_refs(value)
  elif isinstance(obj,list):
   for value in obj:yield from texture_refs(value)
 for name,data in result.items():
  if name.endswith('.json') and name.startswith('assets/aeroapiary/'):
   refs=set(texture_refs(json.loads(data)))
   for key in removed_refs:assert 'aeroapiary:'+key not in refs,f'{name} retains removed texture {key}'
 for name in contents:
  if name.endswith('.class') or name.startswith(('data/','META-INF/')):assert result[name]==contents[name],name
 a.output.parent.mkdir(parents=True,exist_ok=True)
 with ZipFile(a.output,'w',compression=ZIP_DEFLATED,compresslevel=9) as out:
  for name,data in sorted(result.items()):out.writestr(name,data)
with ZipFile(a.output) as candidate:
 assert not obsolete.intersection(candidate.namelist())
 for name,data in replacements.items():assert candidate.read(name)==data
report={'original_sha256':hashlib.sha256(a.addon.read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256(a.output.read_bytes()).hexdigest(),
 'removed':sorted(obsolete),'replaced_or_added':sorted(replacements),'classes_and_data_unchanged':True}
a.output.with_suffix('.receipt.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
