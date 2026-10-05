"""Read-only survey of saved native block states in a completed isolated world.

Scans existing Anvil chunks, never generates terrain or opens the player's save.
"""
import argparse
from collections import Counter
import gzip
import io
import json
from pathlib import Path
import struct
import sys
import zlib

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--world',type=Path,required=True)
p.add_argument('--nbt-library',type=Path,required=True)
p.add_argument('--report',type=Path,required=True)
a=p.parse_args()
sys.path.insert(0,str(a.nbt_library.resolve()))
import nbtlib

def chunks(path):
    with path.open('rb') as stream:
        header=stream.read(4096)
        for index in range(1024):
            entry=int.from_bytes(header[index*4:index*4+4],'big')
            sector=entry>>8
            if not sector:continue
            stream.seek(sector*4096)
            length=struct.unpack('>I',stream.read(4))[0]
            kind=stream.read(1)[0]
            payload=stream.read(length-1)
            if kind==1:payload=gzip.decompress(payload)
            elif kind==2:payload=zlib.decompress(payload)
            elif kind!=3:raise ValueError(f'Unsupported Anvil compression {kind}: {path}')
            yield nbtlib.File.parse(io.BytesIO(payload))

def counts(section):
    states=section.get('block_states',{})
    palette=[str(v['Name']) for v in states.get('palette',[])]
    if not palette:return Counter()
    if len(palette)==1:return Counter({palette[0]:4096})
    bits=max(4,(len(palette)-1).bit_length());per_word=64//bits;mask=(1<<bits)-1
    result=Counter();data=states.get('data',[])
    for index in range(4096):
        number=(int(data[index//per_word])>>(index%per_word*bits))&mask
        result[palette[number]]+=1
    return result

entries=[]
for dimension in sorted((a.world/'dimensions/zerog_tweaks').iterdir()):
    if not dimension.is_dir():continue
    total=Counter();tree_chunks=[];number=0
    for region in sorted((dimension/'region').glob('*.mca')):
        for chunk in chunks(region):
            if str(chunk.get('Status','')) not in {'minecraft:full','full'}:continue
            number+=1;blocks=Counter()
            for section in chunk.get('sections',[]):blocks.update(counts(section))
            total.update(blocks)
            if any(v>0 and k.startswith('zerog_tweaks:') and k.endswith('_log') for k,v in blocks.items()):
                tree_chunks.append([int(chunk['xPos']),int(chunk['zPos'])])
    keys={k:v for k,v in total.items() if k.startswith('zerog_tweaks:') and
          (k.endswith('_log') or 'vine' in k or 'mushroom' in k or 'kelp' in k)}
    entries.append({'dimension':'zerog_tweaks:'+dimension.name,'saved_full_chunks':number,
                    'tree_chunks':tree_chunks,'observed_ecology_blocks':dict(sorted(keys.items()))})
report={'scope':'Already-saved full native chunks only; not natural-spawn or client visual approval',
        'dimensions':entries,'total_tree_chunks':sum(len(e['tree_chunks']) for e in entries)}
a.report.parent.mkdir(parents=True,exist_ok=True)
a.report.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'dimensions':len(entries),'tree_chunks':report['total_tree_chunks'],
                 'report':str(a.report)},indent=2))
