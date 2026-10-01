"""Oriented-box cross-joint clearance audit, not an in-game collision test."""
import json
import itertools
import numpy as np
from pathlib import Path
import check_armour_collection_02 as pose

def overlap(a,b,vertex):
    def box(e):
        cache=getattr(vertex,'_obb_cache',None)
        if cache is None:cache={};vertex._obb_cache=cache
        if e['uuid'] in cache:return cache[e['uuid']]
        lo=np.array(e['from']);hi=np.array(e['to']);center=np.array(vertex(e,(lo+hi)/2))
        edges=[np.array(vertex(e,lo+np.eye(3)[i]*(hi[i]-lo[i])))-vertex(e,lo) for i in range(3)]
        axes=[edge/max(np.linalg.norm(edge),1e-8) for edge in edges]
        radii=[np.linalg.norm(edge)/2 for edge in edges]
        corners=np.array([vertex(e,p) for p in itertools.product(*zip(lo,hi))])
        cache[e['uuid']]=(center,axes,radii,corners)
        return cache[e['uuid']]
    ca,aa,ra,va=box(a);cb,ab,rb,vb=box(b)
    if np.any(va.max(axis=0)<=vb.min(axis=0)+1e-6) or np.any(vb.max(axis=0)<=va.min(axis=0)+1e-6):return False
    for axis in aa+ab+[np.cross(x,y) for x in aa for y in ab]:
        norm=np.linalg.norm(axis)
        if norm<1e-8:continue
        axis=axis/norm
        extent=sum(r*abs(np.dot(axis,x)) for r,x in zip(ra,aa))+sum(r*abs(np.dot(axis,x)) for r,x in zip(rb,ab))
        if abs(np.dot(cb-ca,axis))>=extent-1e-6:return False
    return True

def audit(path):
    m=path if isinstance(path,dict) else json.loads(path.read_text());owners={}
    def walk(nodes,owner=None):
        for n in nodes:
            if isinstance(n,str):owners[n]=owner
            else:walk(n['children'],n['name'] if n['name'] in ['head','body','right_arm','left_arm'] else owner)
    walk(m['outliner'])
    elems=[e for e in m['elements'] if e.get('export',True) and all(z>a for a,z in zip(e['from'],e['to']))]
    torso=[e for e in elems if owners[e['uuid']]=='body']
    arms=[e for e in elems if owners[e['uuid']] in ['right_arm','left_arm']]
    hits={};headhits={};head=[e for e in elems if owners[e['uuid']]=='head']
    clips=[a for a in m['animations'] if a['name'].endswith(('walk_fit_check','head_fit_check'))]
    for clip in clips:
        for t in np.linspace(0,clip['length'],25):
            v=pose.transform(m,clip,float(t))
            if clip['name'].endswith('walk_fit_check'):
                for a,b in itertools.product(torso,arms):
                    if overlap(a,b,v):hits.setdefault(a['name']+' / '+b['name'],[]).append(round(float(t),3))
            for a,b in itertools.product(head,torso+arms):
                if overlap(a,b,v):headhits.setdefault(a['name']+' / '+b['name'],[]).append({'clip':clip['name'],'time':round(float(t),3)})
    return {'file':m['name'],'clips':[a['name'] for a in clips],'samples':50,'cross_joint_arm_chest_intersections':hits,
            'cross_joint_head_shoulder_intersections':headhits,
            'scope':'opaque armour volumes only, excludes same-bone joins and player skin; no all-game-pose guarantee'}

if __name__=='__main__':
    import sys
    print(json.dumps(audit(Path(sys.argv[1])),indent=2))
