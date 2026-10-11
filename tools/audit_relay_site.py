"""Read a saved natural Relay site: bounded water-cover and foundation samples, no save writes."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/dev'))
import worldscan
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--run',type=Path,required=True);p.add_argument('--chunk-x',type=int,required=True)
p.add_argument('--chunk-z',type=int,required=True);p.add_argument('--report',type=Path,required=True)
a=p.parse_args();run=a.run.resolve()
assert run.parent==ROOT and run.name.startswith('run-local-ordinary-'),'Disposable project world required'
dim=run/'world/dimensions/zerog_tweaks/g2_p1';cache={}
def chunk(x,z):
    k=x>>4,z>>4
    if k not in cache:cache[k]=worldscan.chunk(str(dim),*k)
    assert cache[k] and cache[k].get('Status')=='minecraft:full','Unsaved/incomplete sample chunk'
    return cache[k]
def state(x,y,z):
    c=chunk(x,z)
    for s in c['sections']:
        sy=((s['Y']+128)%256-128)*16
        if not sy<=y<sy+16:continue
        bs=s.get('block_states');assert bs,'Missing block states'
        pal=bs['palette']
        if len(pal)==1:return pal[0]
        i=(x&15)+(z&15)*16+(y&15)*256;bits=max(4,(len(pal)-1).bit_length());per=64//bits
        return pal[((bs['data'][i//per]&0xffffffffffffffff)>>((i%per)*bits))&((1<<bits)-1)]
    raise AssertionError('Missing sample section')
start=worldscan.chunk(str(dim),a.chunk_x,a.chunk_z)['structures']['starts']['zerog_tweaks:sunken_relay']
assert start['id']=='zerog_tweaks:sunken_relay' and len(start['Children'])==1
bb=start['Children'][0]['BB'];samples=[]
for ix in range(5):
    for iz in range(5):
        x=bb[0]+(bb[3]-bb[0])*ix//4;z=bb[2]+(bb[5]-bb[2])*iz//4
        top=state(x,bb[4]+1,z);below=state(x,bb[1]-1,z)
        water=top['Name']=='minecraft:water' or top.get('Properties',{}).get('waterlogged')=='true'
        support=below['Name'] not in {'minecraft:air','minecraft:cave_air','minecraft:void_air','minecraft:water','minecraft:lava'}
        samples.append({'x':x,'z':z,'above_bounds':top,'below_foundation':below,'water_cover':water,'non_air_nonfluid_support':support})
report={'scope':'One natural site;25 saved sample columns, not all-world/client or loot-roll proof',
    'dimension':'zerog_tweaks:g2_p1','chunk':[a.chunk_x,a.chunk_z],'piece_bounds':bb,'samples':samples,
    'all_water_covered':all(s['water_cover'] for s in samples),'all_samples_supported':all(s['non_air_nonfluid_support'] for s in samples)}
a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='samples'},indent=2))
assert report['all_water_covered'],'Natural Relay is not covered by water'
assert report['all_samples_supported'],'Natural Relay foundation has unsupported sample columns'
