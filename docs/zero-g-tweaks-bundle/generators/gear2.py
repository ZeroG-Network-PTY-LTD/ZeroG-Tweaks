import math, random
from PIL import Image
from tex import hx
from data import M
def dk(c,f):
    t=hx(c); return '#%02x%02x%02x'%tuple(min(255,int(t[i]*f)) for i in range(3))
# ---------- core: label grid -> shaded image
def shade(L,pal,hpal,acc,motif=None,seed=0):
    im=Image.new('RGBA',(16,16),(0,0,0,0)); px=im.load()
    inside=lambda x,y:(x,y) in L
    same=lambda x,y,m: L.get((x,y))==m
    for (x,y),m in L.items():
        p={'H':pal,'G':[pal[0],pal[1],pal[1],pal[2],pal[3]],'W':hpal,'A':[acc[0],acc[1],acc[1],acc[2],acc[3]]}[m]
        up=not same(x,y-1,m) or not same(x-1,y,m); dn=not same(x,y+1,m) or not same(x+1,y,m)
        dul=min([k for k in range(1,5) if not same(x-k,y-k,m)]+[5]); ddr=min([k for k in range(1,5) if not same(x+k,y+k,m)]+[5])
        c=p[4] if up and not dn else p[1] if dn and not up else (p[3] if dul<ddr else p[2])
        if up and dn: c=p[3] if dul<=ddr else p[2]
        px[x,y]=hx(c)
    for (x,y) in list(L):
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            q=(x+dx,y+dy)
            if 0<=q[0]<16 and 0<=q[1]<16 and q not in L: px[q]=hx(pal[0] if L[(x,y)]!='W' else hpal[0])
    if motif: apply_motif(px,L,motif,pal,acc,seed)
    return im
def apply_motif(px,L,motifs,pal,acc,seed):
    r=random.Random(seed); H=[k for k,v in L.items() if v=='H']
    Hs=set(H)
    interior=[k for k in H if all((k[0]+dx,k[1]+dy) in Hs for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
    for m in motifs:
        if m=='cracks' and interior:
            x,y=r.choice(interior)
            for _ in range(7):
                if (x,y) in Hs: px[x,y]=hx(acc[2])
                x+=r.choice([1,0,1]); y+=r.choice([-1,0,1])
        elif m=='rivets':
            for k in interior[::5][:4]: px[k]=hx(acc[3])
        elif m=='facets':
            for (x,y) in interior:
                if (x+2*y)%5==0: px[x,y]=hx(pal[4])
        elif m=='rust':
            for k in r.sample(H,min(6,len(H))): px[k]=hx(acc[1])
        elif m=='frost':
            for (x,y) in H:
                if (x,y-1) not in L and r.random()<.7: px[x,y]=hx('#f4fcff')
        elif m=='flame':
            for (x,y) in H:
                if (x+1,y-1) not in L and (x,y-1) not in L and r.random()<.6: px[x,y]=hx(acc[3] if r.random()<.5 else acc[2])
        elif m=='filigree':
            for (x,y) in interior:
                if (x+y)%4==0 and (x-y)%4==0: px[x,y]=hx(acc[3])
        elif m=='stars':
            for k in r.sample(interior,min(3,len(interior))): px[k]=hx('#fff6c0')
        elif m=='glow_edge':
            for (x,y) in H:
                if (x+1,y) not in L and (x,y+1) not in L: px[x,y]=hx(acc[2])
        elif m=='inlay':
            if interior:
                cx=sum(a for a,_ in interior)/len(interior); cy=sum(b for _,b in interior)/len(interior)
                k=min(interior,key=lambda q:(q[0]-cx)**2+(q[1]-cy)**2); px[k]=hx(acc[3])
                for d in((1,0),(0,1)):
                    q=(k[0]+d[0],k[1]+d[1])
                    if q in Hs: px[q]=hx(acc[2])
def put(L,x,y,m,over=True):
    if 0<=x<16 and 0<=y<16 and (over or (x,y) not in L): L[(x,y)]=m
# ---------- tools (u = x-y along the handle toward tip; v = x+y across)
VC=15
def handle(L,u0,u1,wrap=False,pom='round'):
    for x in range(16):
        for y in range(16):
            u,v=x-y,x+y
            if u0<=u<=u1 and v in (VC,VC+1): put(L,x,y,'W',False)
    ex,ey=(u0+VC)//2,(VC-u0)//2
    if pom=='round':
        for q in [(ex,ey),(ex-1,ey),(ex,ey+1),(ex-1,ey+1)]: put(L,*q,'A')
    elif pom=='spike': put(L,ex-1,ey+1,'A'); put(L,ex,ey,'A')
    elif pom=='gem': put(L,ex,ey,'A'); put(L,ex-1,ey+1,'A'); put(L,ex-1,ey,'A')
def sword(P):
    L={}; ug=P.get('ug',-4); ut=P.get('len',11); w=P.get('w',(14,16))
    for x in range(16):
        for y in range(16):
            u,v=x-y,x+y
            if not(ug+1<=u<=ut): continue
            t=(u-ug)/(ut-ug)
            off=round(P.get('curve',0)*(t*t)*6+P.get('wave',0)*math.sin(t*math.pi*3))
            lo,hi=w[0]+off,w[1]+off
            tip=P.get('tip','point')
            if tip=='point' and u>=ut-2: lo+= (u-(ut-2)); hi-= (u-(ut-2))
            if tip=='long' and u>=ut-4: lo+=(u-(ut-4))//2; hi-=(u-(ut-4))//2
            if tip=='clipped' and u>=ut-1: lo+=2
            if lo<=v<=hi:
                if P.get('serrate') in('one','both') and v==hi and u%3==0 and u<ut-1: continue
                if P.get('serrate')=='both' and v==lo and u%3==1 and u<ut-1: continue
                put(L,x,y,'H')
                if P.get('fuller') and v==(lo+hi)//2+ (1 if (lo+hi)%2 else 0) and ug+2<u<ut-2: L[(x,y)]='A'
            if P.get('spikes') and u%3==0 and ug+2<u<ut-1 and v in (hi+1,hi+2) and (u+v)%2==0: put(L,x,y,'H')
    g=P.get('guard','bar'); G=P.get('gw',3)
    for x in range(16):
        for y in range(16):
            u,v=x-y,x+y; dv=v-15.5
            if g=='bar' and u in(ug-1,ug) and abs(dv)<=2*G: put(L,x,y,'G')
            if g=='crescent' and ((u in(ug-1,ug) and abs(dv)<=2*G-2) or (u in(ug+1,ug+2) and 2*G-2<abs(dv)<=2*G+1)): put(L,x,y,'G')
            if g=='wings' and ((u in(ug-1,ug) and abs(dv)<=2*G) or (u in(ug-3,ug-2) and 2*G-1<=abs(dv)<=2*G+1)): put(L,x,y,'G')
            if g=='disc' and abs(u-ug+.5)+abs(dv)*.8<=2.6: put(L,x,y,'G')
            if g=='sun' and (abs(u-ug+.5)+abs(dv)*.8<=2.6 or (u in(ug-1,ug) and abs(dv)<=2*G+1)): put(L,x,y,'A' if abs(u-ug+.5)+abs(dv)<1.6 else 'G')
            if g=='horns' and ((u in(ug-1,ug) and abs(dv)<=4) or (u in(ug+1,ug+3) and 4<abs(dv)<=6)): put(L,x,y,'G')
            if g=='block' and u in(ug-2,ug-1,ug) and abs(dv)<=3: put(L,x,y,'G')
    handle(L,P.get('hu',-11),ug-2,pom=P.get('pom','round')); return L
def pickaxe(P):
    L={}; uh=P.get('uh',7); Lh=P.get('L',7)*1.45; c=P.get('c',.08)*.5; th=P.get('th',1.5)
    for x in range(16):
        for y in range(16):
            u,v=x-y,x+y; dv=v-15.5
            if abs(dv)>Lh: continue
            uc=uh-c*dv*dv; t=th*(1-.55*(abs(dv)/Lh)**2)
            end=P.get('ends','point')
            if end=='hammer' and dv<0: t=th+ (1 if abs(dv)>Lh-3 else 0)
            if abs(u-uc)<=t: put(L,x,y,'H')
            if P.get('spikes') and abs(dv)<Lh-1 and int(dv)%3==0 and 0<u-uc<=t+2: put(L,x,y,'H')
    handle(L,-11,uh-2,pom=P.get('pom','round'))
    if P.get('socket',True):
        for x in range(16):
            for y in range(16):
                u,v=x-y,x+y
                if u in(uh-2,uh-1) and v in(14,15,16,17): put(L,x,y,'G')
    return L
def axe(P):
    L={}; ua=P.get('ua',5); typ=P.get('type','std'); D=P.get('D',5)*.8; hw=P.get('hw',2.5)*.6
    for x in range(16):
        for y in range(16):
            u,v=x-y,x+y; du=(u-ua)/2
            for side in ((-1,1) if typ=='double' else (-1,)):
                dist=(15.5-v)/2 if side==-1 else (v-15.5)/2
                if dist<0 or dist>D: continue
                Dd=D if side==-1 else D*.75
                if dist>Dd: continue
                grow=.45 if typ!='cleaver' else .12
                w=hw+dist*grow
                lo,hi=-w,w
                if typ=='bearded': lo=-w-dist*.6; hi=w*.7
                if typ=='cleaver': lo=-w-1; hi=w+.5
                if typ=='crescent' and dist<Dd-1.2 and dist>1.2 and abs(du)>hw+.5: continue
                if lo<=du<=hi: put(L,x,y,'H')
            if P.get('spike') and -0.6<=du<=0.6 and 0<=(v-15.5)/2<=1.5 and typ!='double': put(L,x,y,'H')
    for x in range(16):
        for y in range(16):
            u,v=x-y,x+y
            if P.get('spike') and u>=ua+2*hw+1 and u<=ua+2*hw+4 and v in(15,16): put(L,x,y,'H')
    handle(L,-11,ua+2,pom=P.get('pom','round'))
    return L
def shovel(P):
    L={}; us=P.get('us',7); ru=P.get('ru',3)*1.5; rv=P.get('rv',2.6)*1.6; typ=P.get('type','round')
    for x in range(16):
        for y in range(16):
            u,v=x-y,x+y; du=u-us; dv=v-15.5
            if typ=='round' and (du/ru)**2+(dv/rv)**2<=1: put(L,x,y,'H')
            if typ=='point' and du>=-ru and abs(dv)<=rv*(1-max(0,du)/(ru+.5)): put(L,x,y,'H')
            if typ=='square' and -ru<=du<=ru-.5 and abs(dv)<=rv: put(L,x,y,'H')
            if typ=='spade' and -ru<=du<=ru and abs(dv)<=rv*(1-max(0,du)/(ru+1))+ (0.8 if du<-ru+1.5 else 0): put(L,x,y,'H')
    handle(L,-11,int(us-ru+1),pom=P.get('pom','round'))
    for x in range(16):
        for y in range(16):
            u,v=x-y,x+y
            if abs(u-(us-ru))<=0.5 and 14<=v<=17: put(L,x,y,'G')
    return L
def hoe(P):
    L={}; uh=P.get('uh',8); Lh=P.get('L',5); typ=P.get('type','bar')
    for x in range(16):
        for y in range(16):
            u,v=x-y,x+y; dv=15.5-v
            if 0<=dv<=Lh*1.5 and abs(u-uh)<=1.2: put(L,x,y,'H')
            if typ=='hook' and Lh-1.5<=dv<=Lh and uh-3<=u<=uh: put(L,x,y,'H')
            if typ=='scythe' and dv>=0 and abs(u-(uh-dv*dv*.12))<=.9 and dv<=Lh+1: put(L,x,y,'H')
            if typ=='fork' and 0<=dv<=Lh and abs(u-uh)<=.8 and (int(dv)%2==0 or dv<1.5): 
                put(L,x,y,'H')
                if int(dv)%2==0 and dv>1: put(L,x-1,y+1,'H')
            if P.get('back') and -2.5<=dv<0 and abs(u-uh)<=.8: put(L,x,y,'H')
    handle(L,-11,uh-1,pom=P.get('pom','round')); return L
# ---------- armor (mirrored, x 0..7 then mirror)
def mirror(half):
    L={}
    for (x,y),m in half.items(): L[(x,y)]=m; L[(15-x,y)]=m
    return L
def helmet(P):
    h={}; top=P.get('top',3); w=P.get('w',6)
    for y in range(top,top+5):
        for x in range(8-w,8):
            if y==top and x<8-w+1: continue
            put(h,x,y,'H')
    for y in range(top+5,top+8):
        for x in range(8-w,8-w+P.get('cheek',2)): put(h,x,y,'H')
    v=P.get('visor')
    if v=='slit':
        for x in range(8-w+2,8): put(h,x,top+5,'H'); put(h,x,top+6,'A' if x>8-w+2 else 'H'); put(h,x,top+7,'H')
    if v=='glass':
        for y in range(top+5,top+8):
            for x in range(8-w+2,8): put(h,x,y,'A')
    if v=='nose': put(h,7,top+5,'H'); put(h,7,top+6,'H')
    if v=='mask':
        for y in range(top+5,top+9):
            for x in range(8-w+1,8): put(h,x,y,'H')
        put(h,5,top+6,'A'); put(h,6,top+6,'A')
    for a in P.get('add',[]):
        if a=='crest':
            for y in range(top-2,top+1): put(h,7,y,'H')
            put(h,6,top-1,'H')
        if a=='horns': put(h,8-w,top,'H'); put(h,8-w-1,top-1,'H'); put(h,8-w-1,top-2,'H'); put(h,8-w,top-3,'H')
        if a=='fins': put(h,8-w-1,top+2,'H'); put(h,8-w-2,top+1,'H'); put(h,8-w-1,top+1,'H')
        if a=='crown':
            for x in range(8-w+1,8,2): put(h,x,top-1,'A')
            put(h,7,top-2,'A')
        if a=='brim':
            for x in range(8-w-1,8): put(h,x,top+4,'G')
        if a=='wings': put(h,8-w-1,top+1,'G'); put(h,8-w-2,top,'G'); put(h,8-w-2,top-1,'G'); put(h,8-w-3,top-2,'G'); put(h,8-w-1,top,'G')
        if a=='hood': put(h,7,top-1,'H'); put(h,6,top-1,'H'); put(h,7,top-2,'H')
        if a=='band':
            for x in range(8-w,8): put(h,x,top+3,'A')
        if a=='halo':
            for x in range(8-w,8): put(h,x,top-2,'A')
    return mirror(h)
def chest(P):
    h={}; neck=P.get('neck','round')
    for y in range(1,4):
        for x in range(0,8): put(h,x,y,'H')
    for y in range(4,13):
        for x in range(2,8): put(h,x,y,'H')
    for x in range(0,2): put(h,x,4,'H')
    if neck=='round':
        for q in [(6,1),(7,1),(7,2)]: h.pop(q,None)
    if neck=='v':
        for q in [(5,1),(6,1),(7,1),(6,2),(7,2),(7,3)]: h.pop(q,None)
    if neck=='collar':
        put(h,5,0,'G'); put(h,6,0,'G')
        for q in [(7,1),(7,2)]: h.pop(q,None)
    for a in P.get('add',[]):
        if a=='pauldron':
            for x in range(0,4): put(h,x,0,'G')
            for y in range(1,5): put(h,0,y,'G')
        if a=='spikes': put(h,0,0,'G'); put(h,1,-1 if False else 0,'G'); put(h,2,0,'G'); put(h,1,0,'A')
        if a=='belt':
            for x in range(2,8): put(h,x,11,'A')
        if a=='core': put(h,7,6,'A'); put(h,7,7,'A'); put(h,6,7,'A')
        if a=='ribs':
            for y in (6,8,10): put(h,4,y,'G'); put(h,5,y,'G')
        if a=='wings': put(h,0,5,'G'); put(h,1,6,'G'); put(h,0,6,'G'); put(h,1,5,'G')
        if a=='waist':
            for q in [(2,10),(2,11),(2,12)]: h.pop(q,None)
    return mirror(h)
def legs(P):
    h={}
    for y in range(2,4):
        for x in range(3,8): put(h,x,y,'H')
    lw=P.get('lw',4); bottom=P.get('bottom',12)
    for y in range(4,bottom+1):
        for x in range(3,3+lw): put(h,x,y,'H')
    for a in P.get('add',[]):
        if a=='knee':
            for x in range(3,3+lw): put(h,x,8,'A')
        if a=='flare':
            put(h,2,bottom,'H'); put(h,2,bottom-1,'H')
        if a=='fin': put(h,2,5,'G'); put(h,1,4,'G'); put(h,2,4,'G')
        if a=='tasset':
            for y in range(4,7):
                for x in range(3,8): put(h,x,y,'G')
        if a=='belt':
            for x in range(3,8): put(h,x,2,'A')
        if a=='stripe':
            for y in range(4,bottom): put(h,3,y,'A')
    return mirror(h)
def boots(P):
    h={}; top=P.get('top',8)
    for y in range(top,12):
        for x in range(2,5): put(h,x,y,'H')
    for y in (12,13):
        for x in range(1-P.get('toe',1),5): put(h,x,y,'H')
    for a in P.get('add',[]):
        if a=='cuff':
            for x in range(1,6): put(h,x,top,'G')
        if a=='sole':
            for x in range(0-P.get('toe',1)+1,5): put(h,x,14,'G')
        if a=='spike': put(h,0-P.get('toe',1)+0,13,'A') if P.get('toe',1)<2 else put(h,-1,13,'A'); put(h,1-P.get('toe',1)-1,12,'H')
        if a=='wing': put(h,1,top+1,'G'); put(h,0,top,'G'); put(h,1,top,'G'); put(h,0,top-1,'G')
        if a=='strap':
            for x in range(2,5): put(h,x,top+2,'A')
        if a=='heel': put(h,5,12,'H'); put(h,5,13,'H')
    return mirror(h)
PIECES={'sword':sword,'pickaxe':pickaxe,'axe':axe,'shovel':shovel,'hoe':hoe,'helmet':helmet,'chestplate':chest,'leggings':legs,'boots':boots}
