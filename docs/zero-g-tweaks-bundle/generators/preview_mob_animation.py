"""Software keyframe playback for visual review; not a Minecraft/Blockbench test."""
import json, math
import numpy as np
from PIL import ImageDraw
from build_mob_models import ROOT
from review_mob_assets import render

def translate(v):
    m=np.eye(4);m[:3,3]=v;return m

def rotation(v):
    x,y,z=np.radians(v);cx,sx=math.cos(x),math.sin(x);cy,sy=math.cos(y),math.sin(y);cz,sz=math.cos(z),math.sin(z)
    rx=np.array([[1,0,0,0],[0,cx,-sx,0],[0,sx,cx,0],[0,0,0,1]])
    ry=np.array([[cy,0,sy,0],[0,1,0,0],[-sy,0,cy,0],[0,0,0,1]])
    rz=np.array([[cz,-sz,0,0],[sz,cz,0,0],[0,0,1,0],[0,0,0,1]])
    return rz@ry@rx

def sample(keys,t,default):
    if not keys:return np.array(default,dtype=float)
    keys=sorted(keys,key=lambda k:k['time'])
    def vec(k):return np.array([float(k['data_points'][0][a]) for a in ('x','y','z')])
    if t<=keys[0]['time']:return vec(keys[0])
    for first,last in zip(keys,keys[1:]):
        if t<=last['time']:
            weight=(t-first['time'])/(last['time']-first['time'])
            return vec(first)*(1-weight)+vec(last)*weight
    return vec(keys[-1])

def make(path,action):
    model=json.loads(path.read_text());clip=next(a for a in model['animations'] if a['name'].endswith('.'+action))
    bones={};members={}
    def walk(nodes,parent=None):
        for n in nodes:
            if isinstance(n,str):members[n]=parent
            else:bones[n['uuid']]={**n,'parent':parent};walk(n['children'],n['uuid'])
    walk(model['outliner'])
    frames=[]
    for frame in range(24):
        t=frame/24*clip['length'];matrices={}
        def matrix(key):
            if key is None:return np.eye(4)
            if key in matrices:return matrices[key]
            b=bones[key];kf=clip['animators'].get(key,{}).get('keyframes',[])
            pos=sample([k for k in kf if k['channel']=='position'],t,[0,0,0])
            rot=sample([k for k in kf if k['channel']=='rotation'],t,[0,0,0])+np.array(b.get('rotation',[0,0,0]))
            scale=sample([k for k in kf if k['channel']=='scale'],t,[1,1,1]);s=np.diag([*scale,1])
            pivot=np.array(b['origin']);m=matrix(b['parent'])@translate(pivot+pos)@rotation(rot)@s@translate(-pivot)
            assert np.isfinite(m).all();matrices[key]=m;return m
        def vertex(cube,p):return (matrix(members[cube['uuid']])@np.array([*p,1]))[:3].tolist()
        image=render(model,vertex_transform=vertex).convert('RGB')
        ImageDraw.Draw(image).text((12,12),path.stem.replace('_',' ').title()+' — '+action,fill='white')
        frames.append(image)
    output=ROOT/'docs/zero-g-tweaks-bundle/blockbench/previews'/f'{path.stem}_{action}.gif'
    frames[0].save(output,save_all=True,append_images=frames[1:],duration=round(clip['length']*1000/24),loop=0)
    print(output.name)

def main():
    zg=ROOT/'docs/zero-g-tweaks-bundle/blockbench/mobs'
    for key,action in [('dune_burrower','walk'),('moon_hopper','hop'),('frost_warden','blink')]:make(zg/(key+'.bbmodel'),action)
    make(ROOT/'docs/shattered-skies/blockbench/tidewraith.bbmodel','fly')

if __name__=='__main__':main()
