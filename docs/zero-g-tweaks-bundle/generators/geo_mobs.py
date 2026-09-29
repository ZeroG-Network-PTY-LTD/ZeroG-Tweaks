import os, json, math
from PIL import Image
from mobs_data import MOBS
from mobs_food import M2
import mob_sheet
from mob_sheet import tcol
from tex import hx
NS='zerog_tweaks'; A=f'out/assets/{NS}'
GEO=f'{A}/geckolib/models/entity'; ANI=f'{A}/geckolib/animations/entity'; TEX=f'{A}/textures/entity'
for p in (GEO,ANI,TEX): os.makedirs(p,exist_ok=True)
HEADW=('head','eye','snout','nose','jaw','ear','horn','antler','mandible','beak','crest','teeth','maw','mouth','visor','hat','crown','vael')
LEGW=('leg','hoove','paw','feet','hooves')
def kind(label):
    l=(label or '').lower()
    if any(w in l for w in LEGW) and 'wing' not in l: return 'leg'
    if 'wing' in l: return 'wing'
    if 'tail' in l or 'trail' in l: return 'tail'
    if any(w in l for w in HEADW): return 'head'
    if 'tendril' in l: return 'tendril'
    if 'shard' in l and 'orbit' in l: return 'orbit'
    if 'ray' in l and 'corona' in l: return 'orbit'
    return 'body'
def overlap(a,b):
    return a[1]<b[4]+.01 and b[1]<a[4]+.01 and a[3]<b[6]+.01 and b[3]<a[6]+.01
def build(key,m):
    boxes=[]; cur=None
    for b in m['boxes']:
        if b[0]: cur=b[0]
        boxes.append((cur,)+tuple(b[1:]))
    groups={'body':[],'head':[],'tail':[],'orbit':[]}; legs=[]; wings={-1:[],1:[]}; tendrils=[]
    for b in boxes:
        k=kind(b[0])
        if k=='leg':
            for L in legs:
                if any(overlap(b,x) for x in L): L.append(b); break
            else: legs.append([b])
        elif k=='wing': wings[-1 if (b[1]+b[4])<0 else 1].append(b)
        elif k=='tendril': tendrils.append([b])
        else: groups[k].append(b)
    # glowmask boxes & packing
    allb=[(b,'') for b in boxes]
    fp=[]
    for b in boxes:
        w,h,d=b[4]-b[1],b[5]-b[2],b[6]-b[3]; W_,H_,D_=max(1,math.ceil(w)),max(1,math.ceil(h)),max(1,math.ceil(d))
        fp.append((2*(D_+W_),D_+H_))
    tw=64
    while True:
        x=y=rowh=0; pos=[]; ok=True
        order=sorted(range(len(boxes)),key=lambda i:-fp[i][1])
        P={}
        for i in order:
            fw,fh=fp[i]
            if fw>tw: ok=False; break
            if x+fw>tw: x=0; y+=rowh; rowh=0
            P[i]=(x,y); x+=fw; rowh=max(rowh,fh)
        th=y+rowh
        if ok and th<=tw*2: break
        tw*=2
    th=1
    while th<y+rowh: th*=2
    th=max(th,tw//2) if th<tw//2 else th
    pal={k:hx(v) for k,v in m['pal'].items()}
    mob_sheet.CR=hx(next((m['pal'][c] for c in ('rift','ember','crust','core','glow','vent','ice') if c in m['pal']),'#ffb040'))
    tex=Image.new('RGBA',(tw,th),(0,0,0,0)); glow=Image.new('RGBA',(tw,th),(0,0,0,0)); tp=tex.load(); gp=glow.load()
    for i,b in enumerate(boxes):
        u,v=P[i]; w,h,d=b[4]-b[1],b[5]-b[2],b[6]-b[3]; W_,H_,D_=max(1,math.ceil(w)),max(1,math.ceil(h)),max(1,math.ceil(d))
        base=pal[b[7]]; pat=b[8]
        rects=[(u+D_,v,W_,D_,1.08),(u+D_+W_,v,W_,D_,.7),(u,v+D_,D_,H_,.86),(u+D_,v+D_,W_,H_,1.0),(u+D_+W_,v+D_,D_,H_,.86),(u+2*D_+W_,v+D_,W_,H_,.8)]
        for (x0,y0,ww,hh,f) in rects:
            for yy in range(hh):
                for xx in range(ww):
                    c=tcol(base,pat,i,xx,yy,f); tp[x0+xx,y0+yy]=c
                    if pat=='glow': gp[x0+xx,y0+yy]=c
        # dark 1px edge on side faces for readability
    tex.save(f'{TEX}/{key}.png')
    if any(b[8]=='glow' for b in boxes): glow.save(f'{TEX}/{key}_glowmask.png')
    idx={id(b):i for i,b in enumerate(boxes)}
    def cube(b):
        u,v=P[idx[id(b)]]; return {'origin':[round(b[1],3),round(b[2],3),round(b[3],3)],'size':[round(b[4]-b[1],3),round(b[5]-b[2],3),round(b[6]-b[3],3)],'uv':[u,v]}
    def bbox(bs): return (min(b[1] for b in bs),max(b[4] for b in bs),min(b[2] for b in bs),max(b[5] for b in bs),min(b[3] for b in bs),max(b[6] for b in bs))
    bones=[{'name':'root','pivot':[0,0,0]}]
    body=groups['body'] or boxes[:1]; bb=bbox(body)
    bones.append({'name':'body','parent':'root','pivot':[0,round((bb[2]+bb[3])/2,2),0],'cubes':[cube(b) for b in groups['body']]})
    anim_legs=[]; anim_wings=[]; extra={}
    if groups['head']:
        hb=bbox(groups['head']); bones.append({'name':'head','parent':'body','pivot':[0,round(hb[2],2),round(hb[5],2)],'cubes':[cube(b) for b in groups['head']]})
    if groups['tail']:
        tb=bbox(groups['tail']); bones.append({'name':'tail','parent':'body','pivot':[0,round((tb[2]+tb[3])/2,2),round(tb[4],2)],'cubes':[cube(b) for b in groups['tail']]})
    if groups['orbit']:
        bones.append({'name':'orbit','parent':'body','pivot':[0,round((bb[2]+bb[3])/2,2),0],'cubes':[cube(b) for b in groups['orbit']]})
    for n,L in enumerate(legs):
        lb=bbox(L); nm=f'leg{n}'; bones.append({'name':nm,'parent':'body','pivot':[round((lb[0]+lb[1])/2,2),round(lb[3],2),round((lb[4]+lb[5])/2,2)],'cubes':[cube(b) for b in L]})
        anim_legs.append((nm,(lb[0]+lb[1])/2,(lb[4]+lb[5])/2))
    for s,W_ in wings.items():
        if not W_: continue
        wb=bbox(W_); nm='wing_left' if s<0 else 'wing_right'; px=wb[1] if s<0 else wb[0]
        bones.append({'name':nm,'parent':'body','pivot':[round(px,2),round((wb[2]+wb[3])/2,2),round((wb[4]+wb[5])/2,2)],'cubes':[cube(b) for b in W_]}); anim_wings.append((nm,s))
    for n,T in enumerate(tendrils):
        tb=bbox(T); nm=f'tendril{n}'; bones.append({'name':nm,'parent':'body','pivot':[round((tb[0]+tb[1])/2,2),round(tb[3],2),round((tb[4]+tb[5])/2,2)],'cubes':[cube(b) for b in T]})
        extra[nm]=n
    X0,X1,Y0,Y1,Z0,Z1=bbox(boxes)
    geo={'format_version':'1.12.0','minecraft:geometry':[{'description':{'identifier':f'geometry.{NS}.{key}','texture_width':tw,'texture_height':th,
        'visible_bounds_width':round(max(X1-X0,Z1-Z0)/16+1,1),'visible_bounds_height':round((Y1-Y0)/16+1,1),'visible_bounds_offset':[0,round((Y1+Y0)/32,2),0]},'bones':bones}]}
    json.dump(geo,open(f'{GEO}/{key}.geo.json','w'),indent=1)
    # animations
    flying=Y0>=3
    idle={'body':{'position':{'0.0':[0,0,0],'1.0':[0,1.2 if flying else 0.25,0],'2.0':[0,0,0]}}}
    if groups['head']: idle['head']={'rotation':{'0.0':[0,0,0],'1.0':[-3,0,0],'2.0':[0,0,0]}}
    if groups['tail']: idle['tail']={'rotation':{'0.0':[0,-8,0],'1.0':[0,8,0],'2.0':[0,-8,0]}}
    if groups['orbit']: idle['orbit']={'rotation':{'0.0':[0,0,0],'4.0':[0,360,0]}}
    for nm,s in anim_wings: idle[nm]={'rotation':{'0.0':[0,0,0],'0.25':[0,0,-25*s],'0.5':[0,0,0]}}
    for nm,n in extra.items(): idle[nm]={'rotation':{'0.0':[0,0,-6+4*(n%3)],'1.0':[0,0,6-4*(n%3)],'2.0':[0,0,-6+4*(n%3)]}}
    walk={}
    for nm,x,z in anim_legs:
        ph=1 if (x<0)==(z<0) else -1
        walk[nm]={'rotation':{'0.0':[30*ph,0,0],'0.5':[-30*ph,0,0],'1.0':[30*ph,0,0]}}
    walk['body']={'position':{'0.0':[0,0,0],'0.25':[0,0.4,0],'0.5':[0,0,0],'0.75':[0,0.4,0],'1.0':[0,0,0]}}
    if groups['tail']: walk['tail']={'rotation':{'0.0':[0,-12,0],'0.5':[0,12,0],'1.0':[0,-12,0]}}
    for nm,s in anim_wings: walk[nm]={'rotation':{'0.0':[0,0,0],'0.125':[0,0,-35*s],'0.25':[0,0,0]}}
    if groups['orbit']: walk['orbit']=idle['orbit']
    ani={'format_version':'1.8.0','animations':{f'animation.{key}.idle':{'loop':True,'animation_length':4.0 if groups['orbit'] else 2.0,'bones':idle},
        f'animation.{key}.walk':{'loop':True,'animation_length':1.0,'bones':walk}}}
    json.dump(ani,open(f'{ANI}/{key}.animation.json','w'),indent=1)
    return dict(tw=tw,th=th,bones=len(bones),legs=len(anim_legs),glow=any(b[8]=='glow' for b in boxes))
res={}
for k,m in list(MOBS.items())+list(M2.items()): res[k]=build(k,m)
for k,v in res.items(): print(k,v)
