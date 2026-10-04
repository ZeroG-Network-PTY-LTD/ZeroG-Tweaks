"""Read only an isolated hub's saved entity regions; verify resident admission."""
import argparse,collections,gzip,io,json,struct,sys,zlib
from pathlib import Path
parser=argparse.ArgumentParser()
parser.add_argument('--world',type=Path,required=True)
parser.add_argument('--nbt-library',type=Path,required=True)
args=parser.parse_args()
sys.path.insert(0,str(args.nbt_library))
import nbtlib
report=json.loads((args.world/'zerog-hub-report.json').read_text())
species={'zerog_tweaks:'+s for s in ['lunari','rustborn','glintfolk','ashwright','hollow_kin','sunwarden']}
counts=collections.Counter();uuids=set()
for planet in report['planets']:
    namespace,name=planet['dimension'].split(':')
    local=collections.Counter()
    for path in (args.world/'dimensions'/namespace/name/'entities').glob('*.mca'):
        with path.open('rb') as region:
            header=region.read(4096)
            for i in range(1024):
                offset=int.from_bytes(header[i*4:i*4+3],'big')
                if not offset:continue
                region.seek(offset*4096);length=struct.unpack('>I',region.read(4))[0];codec=region.read(1)[0]
                assert not codec&128,'External entity payload not supported'
                data=region.read(length-1)
                data=zlib.decompress(data) if codec==2 else gzip.decompress(data) if codec==1 else data
                root=nbtlib.File.parse(io.BytesIO(data))
                for entity in root.get('Entities',[]):
                    kind=str(entity.get('id',''))
                    if kind in species or kind=='minecraft:villager':
                        uuid=tuple(int(v) for v in entity['UUID']);assert uuid not in uuids,'Duplicate resident UUID';uuids.add(uuid)
                        local[kind]+=1;counts[kind]+=1
                        if kind in species:assert 0<=int(entity['PlanetStyle'])<=2
    number=len(planet['inspection_village_positions'])
    assert local['minecraft:villager']==0,(name,'Old vanilla planetary residents remain',dict(local))
    assert sum(local[s] for s in species)==number*8,(name,'Planetary residents missing/duplicated',dict(local))
print(json.dumps({'saved_residents':dict(counts),'unique_uuids':len(uuids),'planets':len(report['planets']),
                 'inspection_villages':sum(len(p['inspection_village_positions']) for p in report['planets'])},indent=2))
