"""Static full-cube walking approximation, not native Minecraft collision."""
import collections,json
from pathlib import Path
from showcase_augment_lib import read_nbt

root=Path(__file__).resolve().parent.parent/'revision-candidates'
report=json.loads((root/'revision-report.json').read_text());results={}
for name,m in report.items():
    s=read_nbt(root/(name+'.nbt'))
    assert all(all(0<=v<s['size'][i] for i,v in enumerate(b['pos'])) for b in s['blocks'])
    assert len({tuple(b['pos']) for b in s['blocks']})==len(s['blocks'])
    assert not any('gate_' in state['Name'] for state in s['palette'])
    cells={tuple(v['pos']):s['palette'][v['state']]['Name'] for v in s['blocks']}
    def free(p):return cells.get(p,'minecraft:air')=='minecraft:air'
    def stand(p):
        x,y,z=p
        return free(p) and free((x,y+1,z)) and not free((x,y-1,z))
    start=tuple(m['entry']);seen={start};q=collections.deque([start])
    while q:
        x,y,z=q.popleft()
        for dx,dz in [(1,0),(-1,0),(0,1),(0,-1)]:
            for dy in [-1,0,1]:
                v=x+dx,y+dy,z+dz
                if v in seen or not all(0<=v[i]<s['size'][i] for i in range(3)):continue
                if stand(v):seen.add(v);q.append(v)
    reached=sum(any((x+dx,y,z+dz) in seen for dx,dz in [(1,0),(-1,0),(0,1),(0,-1)]) for x,y,z in m['loot_positions'])
    spawners=[p for p,v in cells.items() if v=='minecraft:spawner']
    assert len(spawners)==1
    assert len([v for v in cells.values() if v=='minecraft:chest'])==4
    spawn_floor_cells=0
    sx,sy,sz=spawners[0]
    for x in range(sx-4,sx+5):
        for z in range(sz-4,sz+5):
            if stand((x,sy,z)):spawn_floor_cells+=1
    results[name]={'entry_standing':stand(start),'reachable_loot_rooms':reached,
                   'bounds_and_unique_positions':True,'gate_blocks':0,
                   'spawner_nearby_standing_cells':spawn_floor_cells,
                   'walkable_cells':len(seen),'native_collision_verified':False}
print(json.dumps(results,indent=2))
(root/'static-route-report.json').write_text(json.dumps(results,indent=2)+'\n')
if not all(v['entry_standing'] and v['reachable_loot_rooms']==4 for v in results.values()):
    raise SystemExit('Route repair still required; do not install')
