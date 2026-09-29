import random, math
from PIL import Image, ImageDraw
from tex import hx
from data import M
GUN=['#15171c','#2a2e36','#3e444f','#58606d','#7c8594']
VIO='#b48cff'; VIO2='#6e4ab0'; VHI='#e6dcff'
def new(): return Image.new('RGBA',(16,16),(0,0,0,0))
class F:
    def __init__(s,base=None): s.im=base.copy() if base else new(); s.px=s.im.load()
    def p(s,x,y,c):
        if 0<=x<16 and 0<=y<16: s.px[x,y]=hx(c)
    def r(s,x0,y0,x1,y1,c):
        for y in range(y0,y1+1):
            for x in range(x0,x1+1): s.p(x,y,c)
    def box(s,x0,y0,x1,y1,c):
        for x in range(x0,x1+1): s.p(x,y0,c); s.p(x,y1,c)
        for y in range(y0,y1+1): s.p(x0,y,c); s.p(x1,y,c)
    def circ(s,cx,cy,rad,c,fill=False):
        for y in range(16):
            for x in range(16):
                d=math.hypot(x+.5-cx,y+.5-cy)
                if (d<=rad) if fill else (rad-0.75<=d<=rad): s.p(x,y,c)
def casing(pal=GUN,seed=0,bolts='#9aa2ae'):
    f=F(); rnd=random.Random(seed)
    for y in range(16):
        for x in range(16): f.p(x,y,pal[2] if rnd.random()<.8 else pal[1] if rnd.random()<.5 else pal[3])
    f.box(0,0,15,15,pal[0])
    for i in range(1,15): f.p(i,1,pal[4]); f.p(1,i,pal[3]); f.p(i,14,pal[1]); f.p(14,i,pal[1])
    for q in [(2,2),(13,2),(2,13),(13,13)]: f.p(*q,bolts)
    return f
def plain(pal=GUN,seed=0,bolts='#9aa2ae'): return casing(pal,seed,bolts).im
def darker(seed=9): 
    f=casing(GUN,seed); f.r(2,2,13,13,GUN[1]); return f

B={}
# ---------------- Teleporter parts
def controller():
    s=casing(seed=1); s.r(3,5,12,10,GUN[1]); s.r(4,6,11,9,'#3a2a5a') # conduit window
    for x in range(4,12,2): s.p(x,7,VIO); s.p(x+1,8,VIO2)
    f=casing(seed=2); f.r(2,2,13,12,GUN[0]); f.r(3,3,12,11,'#0d0b1e')
    f.circ(7.5,7,4.2,'#3c2e70'); f.circ(7.5,7,2.3,'#5a44a0')
    for q in [(4,4),(10,5),(6,9),(11,10),(8,4),(5,7)]: f.p(*q,'#ffffff')
    f.p(8,7,VIO); f.p(7,6,VHI)  # target
    f.r(4,13,11,13,GUN[1]); 
    for x,c in [(5,'#4ade80'),(7,'#facc15'),(9,VIO)]: f.p(x,13,c)
    t=casing(seed=3); t.r(4,4,11,11,GUN[0]); t.r(5,5,10,10,'#2a1f44'); t.circ(8,8,2.5,VIO,True); t.circ(8,8,1.2,VHI,True)
    b=darker(4)
    return dict(top=t.im,front=f.im,side=s.im,bottom=b.im)
def pad():
    t=casing(seed=5); t.r(2,2,13,13,'#1d1830')
    t.circ(8,8,6,VIO2); t.circ(8,8,4,VIO); t.circ(8,8,2,VHI,True)
    for q in [(8,2),(8,13),(2,8),(13,8)]: t.p(*q,VIO)
    s=F(plain(seed=6)); s.r(1,5,14,6,VIO2); s.r(1,5,14,5,VIO)
    return dict(top=t.im,front=s.im,side=s.im,bottom=darker(7).im)
def frame(key,seed):
    p=M[key]['pal']; pal=[p[0],p[1],p[2],p[3],p[4]]
    f=casing(pal,seed,p[5]); f.r(3,3,12,12,p[1]); f.box(3,3,12,12,p[0])
    for i in range(4,12): f.p(i,i,p[3]); f.p(i+1,i,p[2])
    f.r(7,7,8,8,p[5])
    return dict(top=f.im,front=f.im,side=f.im,bottom=f.im)
def pylon():
    s=casing(seed=8); s.r(6,1,9,14,GUN[0]); s.r(7,2,8,13,'#2a1f44')
    for y in range(3,13,3): s.r(7,y,8,y,VIO)
    s.p(7,6,VHI)
    t=casing(seed=9); t.r(5,5,10,10,GUN[0]); t.r(6,6,9,9,VIO2); t.r(7,7,8,8,VHI)
    return dict(top=t.im,front=s.im,side=s.im,bottom=darker(10).im)
def port():
    s=casing(seed=11); s.r(4,4,11,11,GUN[0]); s.circ(8,8,3.5,'#0e4a5c',True); s.circ(8,8,3.5,'#3fd6f0'); s.circ(8,8,1.5,'#b8f6ff',True)
    for q in [(8,3),(8,12),(3,8),(12,8)]: s.p(*q,'#3fd6f0')
    return dict(top=plain(seed=12),front=s.im,side=s.im,bottom=plain(seed=13))
def lens():
    f=casing(seed=14); f.r(3,3,12,12,GUN[0]); f.circ(8,8,4.6,'#8f9ab8',True); f.circ(8,8,4.6,'#3a3f52')
    f.circ(8,8,3,'#c2cbe6',True); f.r(6,5,7,6,'#ffffff'); f.p(9,10,'#e2e8f7')
    for q in [(8,2),(8,13),(2,8),(13,8)]: f.p(*q,VIO)
    s=casing(seed=15); s.r(2,7,13,8,GUN[1]); s.r(3,7,12,7,VIO2)
    return dict(top=s.im,front=f.im,side=s.im,bottom=plain(seed=16))
def landing():
    t=casing(seed=17); t.r(2,2,13,13,'#2a2e36')
    t.circ(8,8,5.5,'#ffcc4a'); 
    for x in range(5,11): t.p(x,5,'#e6e8ec'); t.p(x,10,'#e6e8ec')
    t.r(5,5,5,10,'#e6e8ec'); t.r(10,5,10,10,'#e6e8ec'); t.r(7,7,8,8,VIO)
    s=F(plain(seed=18))
    for x in range(1,15): s.p(x,12,'#ffcc4a' if (x//2)%2 else GUN[0]); s.p(x,13,'#ffcc4a' if ((x+1)//2)%2 else GUN[0])
    s.r(2,4,13,4,VIO2); s.r(4,4,11,4,VIO)
    return dict(top=t.im,front=s.im,side=s.im,bottom=darker(19).im)
def cell():
    s=casing(seed=20); s.r(3,2,12,13,GUN[0]); s.r(4,3,11,12,'#1c2a3a')
    for (x,y,h) in [(6,6,6),(8,4,8),(10,7,5),(5,9,3)]:
        s.r(x,y,x,y+h-1,'#6fe0ff'); s.p(x,y,'#e8ffff')
    s.r(4,3,11,3,'#9aa8b8'); s.p(5,4,'#c9d6e4')
    t=casing(seed=21); t.r(5,5,10,10,GUN[0]); 
    for i in range(6,10,2): t.r(6,i,9,i,'#6fe0ff')
    return dict(top=t.im,front=s.im,side=s.im,bottom=darker(22).im)
# ---------------- Machines
def generator():
    f=casing(seed=30); f.r(3,5,12,12,GUN[0]); f.r(4,6,11,11,'#2a0e04')
    for x in range(4,12,2): f.r(x,6,x,11,GUN[1])
    for x,y,c in [(5,10,'#ff8a2a'),(7,9,'#ffb040'),(9,10,'#ff8a2a'),(7,11,'#ffd070'),(9,8,'#ff6a1a'),(5,8,'#e05a10'),(11,9,'#ffb040')]: f.p(x,y,c)
    f.r(4,3,11,3,GUN[1]); f.p(5,3,'#4ade80')
    t=casing(seed=31)
    for y in range(4,12,2): t.r(4,y,11,y,GUN[0])
    return dict(top=t.im,front=f.im,side=plain(seed=32),bottom=darker(33).im)
def solar():
    t=F(); t.r(0,0,15,15,'#9aa2ae'); t.box(0,0,15,15,GUN[0])
    for cy in (1,8):
        for cx in (1,8):
            t.r(cx,cy,cx+6,cy+6,'#1b3a7a'); t.r(cx,cy,cx+6,cy,'#3a6ad0'); t.p(cx+1,cy+1,'#8ab8ff'); t.p(cx+2,cy+1,'#5a8ae8')
            for i in range(2,7,2): t.r(cx+i,cy,cx+i,cy+6,'#2a4e9a')
    s=F(plain(seed=34)); s.r(2,2,13,4,'#1b3a7a'); s.r(2,2,13,2,'#3a6ad0')
    return dict(top=t.im,front=s.im,side=s.im,bottom=darker(35).im)
def fusion():
    f=casing(seed=36); f.circ(8,8,6.2,GUN[0],True); f.circ(8,8,6.2,'#ff7a1a'); f.circ(8,8,4.5,'#3a0a04',True)
    f.circ(8,8,3.2,'#ffa030',True); f.circ(8,8,1.8,'#fff0a0',True); f.p(7,7,'#ffffff')
    s=casing(seed=37)
    for y in range(3,13,2): s.r(3,y,12,y,'#b86a2a'); s.r(3,y+1,12,y+1,GUN[1])
    s.r(3,13,12,13,'#ffcc4a')
    t=casing(seed=38); t.circ(8,8,4,'#ff7a1a'); t.circ(8,8,2,'#fff0a0',True)
    return dict(top=t.im,front=f.im,side=s.im,bottom=darker(39).im)
def refinery():
    f=casing(seed=40); f.r(3,4,12,12,GUN[0]); f.r(4,5,11,11,'#202428')
    for x in range(4,12,2):
        f.p(x,5,'#b8c0cc'); f.p(x+1,6,'#b8c0cc'); f.p(x,11,'#b8c0cc'); f.p(x+1,10,'#b8c0cc')
    f.r(5,7,10,9,'#3f68a8'); f.p(6,8,'#b5d4f5'); f.p(9,8,'#e8661e')
    t=casing(seed=41); t.r(3,3,12,12,GUN[0]); t.r(5,5,10,10,'#101216'); t.box(4,4,11,11,GUN[1])
    return dict(top=t.im,front=f.im,side=plain(seed=42),bottom=darker(43).im)
def forge():
    f=casing(seed=44); f.r(3,6,12,12,GUN[0]); f.r(4,7,11,12,'#3a1a0e')
    f.r(5,9,10,11,'#6a3a1a'); f.r(6,9,9,10,'#ffb040'); f.p(7,9,'#fff4c8'); f.r(5,8,10,8,'#8a5a2a')
    f.r(4,4,11,4,GUN[1]); 
    t=casing(seed=45); t.r(5,5,10,10,GUN[0]); t.r(6,6,9,9,'#140a06'); t.p(7,7,'#ff8a2a')
    return dict(top=t.im,front=f.im,side=plain(seed=46),bottom=darker(47).im)
def growth():
    f=casing(seed=48); f.r(3,2,12,13,'#9aa8b8'); f.r(4,3,11,12,'#12303a')
    for (x,y,h,c) in [(7,5,7,'#3fc9e8'),(5,8,4,'#1592b8'),(9,7,5,'#3fc9e8'),(10,9,3,'#1592b8'),(6,10,2,'#b0f2ff')]:
        f.r(x,y,x,y+h-1,c); f.p(x,y,'#e8ffff')
    f.r(4,12,11,12,'#0d5f7c'); f.r(4,3,11,3,'#c9d6e4')
    t=casing(seed=49); t.r(4,4,11,11,'#9aa8b8'); t.r(5,5,10,10,'#12303a'); t.r(7,7,8,8,'#3fc9e8')
    return dict(top=t.im,front=f.im,side=plain(seed=50),bottom=darker(51).im)
def salvage():
    f=casing(seed=52); f.r(3,3,12,12,GUN[0]); f.circ(8,8,4.8,'#aab2bc',True); f.circ(8,8,4.8,'#6a7280')
    for a in range(8):
        x=8+4.6*math.cos(a*math.pi/4); y=8+4.6*math.sin(a*math.pi/4); f.p(int(x),int(y),'#e6eaee')
    f.circ(8,8,1.5,GUN[1],True); f.p(7,7,'#d49a5a'); f.p(10,11,'#d49a5a')
    t=casing(seed=53)
    for x in range(4,12,2): t.r(x,4,x,11,GUN[0])
    return dict(top=t.im,front=f.im,side=plain(seed=54),bottom=darker(55).im)
def casing_block(key,seed):
    p=M[key]['pal']; f=casing([p[0],p[1],p[2],p[3],p[4]],seed,p[5]); f.r(5,5,10,10,p[1]); f.box(5,5,10,10,p[0]); f.r(7,7,8,8,p[5])
    return dict(top=f.im,front=f.im,side=f.im,bottom=f.im)
