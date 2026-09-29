from PIL import Image
from tex import hx
from food_data import MASK
def mixc(c,t,f):
    a=hx(c); b=hx(t); return tuple(int(a[i]*(1-f)+b[i]*f) for i in range(3))+(255,)
def ramp(c): return [mixc(c,'#000000',.72),mixc(c,'#000000',.32),hx(c),mixc(c,'#ffffff',.25),mixc(c,'#ffffff',.55)]
def render(item):
    rows=MASK[item['mask']]; rows=(rows+['']*16)[:16]; L={}
    for y,r in enumerate(rows):
        for x,c in enumerate(r.ljust(16,'.')[:16]):
            if c!='.': L[(x,y)]=c
    grill=item['G']=='GRILL'
    cols={'H':item['H'],'G':item['H'] if grill else item['G'],'A':item['A'],'W':item['W']}
    R={k:ramp(v) for k,v in cols.items()}
    im=Image.new('RGBA',(16,16),(0,0,0,0)); px=im.load()
    same=lambda x,y,m:L.get((x,y))==m
    for (x,y),m in L.items():
        p=R[m]
        if m=='A': px[x,y]=p[3] if not same(x,y+1,'A') else p[2]; continue
        up=not same(x,y-1,m) or not same(x-1,y,m); dn=not same(x,y+1,m) or not same(x+1,y,m)
        c=p[4] if up and not dn else p[1] if dn and not up else p[3] if (x+y)%5 else p[2]
        if up and dn: c=p[3]
        px[x,y]=c
    for (x,y),m in list(L.items()):
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            q=(x+dx,y+dy)
            if 0<=q[0]<16 and 0<=q[1]<16 and q not in L: px[q]=R[m][0] if m!='A' else R['H'][0]
    if grill:
        g=mixc(item['H'],'#000000',.45)
        for (x,y),m in L.items():
            if m=='H' and (x+y)%4==0 and all(L.get((x+dx,y+dy))=='H' for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): px[x,y]=g
    return im
