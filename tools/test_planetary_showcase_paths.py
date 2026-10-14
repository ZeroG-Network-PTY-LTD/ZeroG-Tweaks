"""Bounded two-block-clearance path checks for native showcase templates.

Static full-cube approximation, NOT Minecraft pathfinding or natural placement.
"""
import gzip
import sys
import unittest
from collections import deque
from pathlib import Path

sys.path.insert(0,str(Path(__file__).parent/'dev'))
from worldscan import _read

ROOT=Path(__file__).resolve().parents[1]
NAMES=('water_bio_habitat','hot_ring_monolith','ice_spire_outpost')


def template(name):
    raw=gzip.decompress((ROOT/'src/main/resources/data/zerog_tweaks/structure/planetary_showcase'/f'{name}.nbt').read_bytes())
    data,end=_read(raw,3,10)
    assert end==len(raw)
    palette=data['palette']
    blocks={tuple(b['pos']):palette[b['state']]['Name'] for b in data['blocks']}
    return data,blocks


def reachable(blocks,start,size):
    def empty(p):return blocks.get(p,'minecraft:air')=='minecraft:air'
    def stand(p):
        x,y,z=p
        return (0<=x<size[0] and 1<=y<size[1]-1 and 0<=z<size[2]
                and empty(p) and empty((x,y+1,z)) and not empty((x,y-1,z)))
    if not stand(start):return set()
    seen={start};queue=deque([start])
    while queue:
        x,y,z=queue.popleft()
        for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
            for dy in (0,-1,1):
                candidate=(x+dx,y+dy,z+dz)
                if candidate in seen or not stand(candidate):continue
                # Stepping up/down must also clear the traversed upper cell.
                if dy==1 and not empty((x,y+2,z)):continue
                if dy==-1 and not empty((x+dx,y+1,z+dz)):continue
                seen.add(candidate);queue.append(candidate)
    return seen


class ShowcasePaths(unittest.TestCase):
    def test_surface_entrance_reaches_all_four_loot_rooms(self):
        for name in NAMES:
            with self.subTest(template=name):
                data,blocks=template(name)
                n=data['size'][0];c=n//2;depth=14 if name=='ice_spire_outpost' else 20 if name=='hot_ring_monolith' else 16
                seen=reachable(blocks,(c,depth+1,c+depth+1),data['size'])
                self.assertTrue(seen,'Blocked surface entrance')
                for target in ((x-1,2,z) for x in (8,n-9) for z in (8,n-9)):
                    self.assertTrue(target in seen,f'Gallery/loot access blocked: {name} {target}')

    def test_templates_keep_four_chests_and_one_hostile_spawner(self):
        for name in NAMES:
            data,blocks=template(name)
            self.assertEqual(sum(v=='minecraft:chest' for v in blocks.values()),4)
            self.assertEqual(sum(v=='minecraft:spawner' for v in blocks.values()),1)
            spawner=next(b['nbt'] for b in data['blocks'] if 'SpawnData' in b.get('nbt',{}))
            self.assertIn(spawner['SpawnData']['entity']['id'],('minecraft:spider','minecraft:husk','minecraft:stray'))


if __name__=='__main__':unittest.main()
