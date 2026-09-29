import random, math
from PIL import Image
from tex import hx, stone
import blocks as K
def N(): return Image.new('RGBA',(16,16),(0,0,0,0))
def noise(pal,seed,w=(.2,.5,.85)):
    r=random.Random(seed); im=N(); px=im.load()
    for y in range(16):
        for x in range(16):
            v=r.random(); px[x,y]=hx(pal[0] if v<w[0] else pal[1] if v<w[1] else pal[2] if v<w[2] else pal[3])
    return im
def sand(p,s): return noise(p,s,(.1,.4,.8))
def polished(p,s):
    im=noise([p[1],p[2],p[2],p[2]],s,(.05,.3,.95)); px=im.load()
    for i in range(16): px[i,0]=hx(p[3]); px[0,i]=hx(p[3]); px[i,15]=hx(p[0]); px[15,i]=hx(p[0])
    return im
def bricks(p,s):
    im=noise([p[1],p[2],p[2],p[3]],s,(.15,.5,.9)); px=im.load()
    for y in range(16):
        for x in range(16):
            if y%4==3 or ((x+(4 if (y//4)%2 else 0))%8==7): px[x,y]=hx(p[0])
            elif y%4==0: px[x,y]=hx(p[3])
    return im
def chiseled(p,s):
    im=polished(p,s); px=im.load()
    for i in range(3,13): px[i,3]=hx(p[0]); px[3,i]=hx(p[0]); px[i,12]=hx(p[3]); px[12,i]=hx(p[3])
    for (x,y) in [(7,6),(8,6),(6,7),(9,7),(6,8),(9,8),(7,9),(8,9)]: px[x,y]=hx(p[0])
    for (x,y) in [(7,7),(8,7),(7,8),(8,8)]: px[x,y]=hx(p[3])
    return im
def cracked(p,s,acc,n=5):
    im=stone(p,s); px=im.load(); r=random.Random(s)
    for _ in range(n):
        x,y=r.randrange(16),r.randrange(16)
        for _ in range(r.randrange(3,7)):
            px[x%16,y%16]=hx(acc); x+=r.choice([-1,0,1]); y+=r.choice([0,1])
    return im
def speck(base,s,cols,n=10):
    im=base.copy(); px=im.load(); r=random.Random(s)
    for _ in range(n): px[r.randrange(16),r.randrange(16)]=hx(r.choice(cols))
    return im
def ice(p,s):
    im=noise(p,s,(.1,.45,.85)); px=im.load()
    for d in (3,9,14):
        for i in range(16):
            x=(i+d)%16; y=15-i
            px[x,y]=hx(p[3])
    return im
def glass(frame,tint,s,alpha=90):
    im=N(); px=im.load(); t=hx(tint)
    for y in range(16):
        for x in range(16): px[x,y]=(t[0],t[1],t[2],alpha)
    for i in range(16):
        for q in [(i,0),(0,i),(i,15),(15,i)]: px[q]=hx(frame)
    for (x,y) in [(3,3),(4,4),(4,3),(11,9),(12,10)]: px[x,y]=(255,255,255,200)
    return im
def side_cover(dirt,top,s):
    im=stone(dirt,s); px=im.load(); r=random.Random(s)
    for x in range(16):
        h=r.choice([2,3,3,4])
        for y in range(h): px[x,y]=hx(top[1] if y==h-1 else top[2] if y else top[3])
    return im
def log_side(p,s):
    im=N(); px=im.load(); r=random.Random(s)
    for y in range(16):
        for x in range(16):
            c=p[1] if x%4==0 else p[2] if r.random()<.75 else p[3]
            if r.random()<.05: c=p[0]
            px[x,y]=hx(c)
    return im
def log_top(bark,ring,s):
    im=N(); px=im.load()
    for y in range(16):
        for x in range(16):
            d=math.hypot(x-7.5,y-7.5)
            px[x,y]=hx(bark[1] if d>6.6 else ring[1] if int(d)%2 else ring[2])
    return im
def planks(p,s):
    im=noise([p[1],p[2],p[2],p[3]],s,(.1,.4,.9)); px=im.load()
    for y in range(16):
        for x in range(16):
            if y%4==3: px[x,y]=hx(p[0])
            if (y//4)%2==0 and x==11 or (y//4)%2==1 and x==4: px[x,y]=hx(p[0])
    return im
def leaves(p,s,acc=None):
    im=N(); px=im.load(); r=random.Random(s)
    for y in range(16):
        for x in range(16):
            v=r.random()
            if v<.12: continue
            px[x,y]=hx(p[0] if v<.3 else p[1] if v<.65 else p[2] if v<.9 else p[3])
            if acc and r.random()<.05: px[x,y]=hx(acc)
    return im
def lamp(frame,glow,s):
    f=K.casing([frame[0],frame[1],frame[2],frame[3],frame[3]],s,glow[2]); f.r(3,3,12,12,frame[0]); 
    for y in range(4,12):
        for x in range(4,12):
            d=math.hypot(x-7.5,y-7.5); f.p(x,y,glow[2] if d<1.8 else glow[1] if d<3.2 else glow[0])
    return f.im
def plant(kind,p,acc,s):
    f=K.F()
    if kind=='flower':
        f.r(7,8,7,15,'#3a6a3a' if acc!='frost' else p[0]); f.p(6,11,p[0]); f.p(8,12,p[0])
        for (x,y) in [(7,4),(6,5),(8,5),(5,6),(9,6),(6,7),(8,7),(7,6)]: f.p(x,y,p[2])
        f.p(7,5,p[3]); f.p(7,6,p[3])
    elif kind=='bush':
        r=random.Random(s)
        for i in range(5):
            x,y=r.randrange(3,12),15
            for k in range(r.randrange(6,11)):
                f.p(x,y,p[1] if k%3 else p[2]); y-=1; x+=r.choice([-1,0,0,1])
                if k%3==2: f.p(x+1,y,p[3])
    elif kind=='fungus':
        f.r(7,9,8,15,p[0]); f.r(4,6,11,8,p[1]); f.r(5,5,10,5,p[2]); f.r(3,8,12,8,p[1])
        for q in [(5,6),(9,7),(7,5)]: f.p(*q,p[3])
    elif kind=='fern':
        for side in (-1,1):
            for i in range(6):
                x=7+side*(1+i//2); y=14-i*2; f.p(x,y,p[1]); f.p(x+side,y,p[2]); f.p(x+side*2,y-1,p[3])
        f.r(7,4,7,15,p[1])
    elif kind=='vine':
        r=random.Random(s)
        for x in (3,7,11):
            L=r.randrange(8,16)
            for y in range(L): f.p(x+(y//4)%2,y,p[1] if y%3 else p[2])
            f.p(x,L-1,p[3])
    elif kind=='crystal':
        for (x,y,h) in [(7,4,12),(5,8,8),(10,7,9),(3,11,5),(12,11,5)]:
            f.r(x,y,x,15,p[1]); f.r(x+1,y+1,x+1,15,p[2]); f.p(x,y,p[3])
    return f.im
