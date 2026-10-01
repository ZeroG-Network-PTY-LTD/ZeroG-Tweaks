import os, random, math
from PIL import Image, ImageDraw, ImageFont
from tex import hx
from data import M
from gear_sets import S, HAND
from gear2 import dk
OUTA='out/assets/zerog_tweaks/textures/models/armor'; os.makedirs(OUTA,exist_ok=True)
# ---------------- layer painting
def rgba(c,a=255): t=hx(c); return (t[0],t[1],t[2],a)
class Tex:
    def __init__(s): s.im=Image.new('RGBA',(64,32),(0,0,0,0)); s.px=s.im.load()
    def p(s,x,y,c,a=255):
        if 0<=x<64 and 0<=y<32: s.px[x,y]=rgba(c,a) if isinstance(c,str) else c
    def clr(s,x,y): 
        if 0<=x<64 and 0<=y<32: s.px[x,y]=(0,0,0,0)
def plate(T,x0,y0,w,h,pal,seed,edge=True,rows=None):
    r=random.Random(seed); ys=list(rows) if rows else list(range(h)); n=len(ys)
    for i,y in enumerate(ys):
        t=i/max(1,n-1)
        for x in range(w):
            c=pal[3] if t<.45 else pal[2]
            if r.random()<.12: c=pal[2] if c==pal[3] else pal[3]
            if edge:
                if i==0: c=pal[4]
                elif i==n-1: c=pal[1]
                elif x==0 or x==w-1: c=pal[2] if t<.45 else pal[1]
            T.p(x0+x,y0+y,c)
def motif(T,rect,m,pal,acc,seed):
    x0,y0,w,h=rect; r=random.Random(seed)
    pts=[(x0+x,y0+y) for x in range(1,w-1) for y in range(1,h-1) if T.px[x0+x,y0+y][3]]
    if not pts: return
    for k in m:
        if k=='cracks':
            x,y=r.choice(pts)
            for _ in range(6):
                if (x,y) in pts: T.p(x,y,acc[2])
                x+=r.choice([0,1,-1]); y+=1
        if k=='rivets':
            for (x,y) in pts:
                if (x-x0)%3==1 and (y-y0)%4==1: T.p(x,y,acc[3])
        if k=='facets':
            for (x,y) in pts:
                if (x-y)%4==0: T.p(x,y,pal[4])
        if k=='rust':
            for q in r.sample(pts,min(4,len(pts))): T.p(*q,acc[1])
        if k=='frost':
            for (x,y) in pts:
                if y==y0+1 and r.random()<.7: T.p(x,y,'#f4fcff')
        if k=='flame':
            for (x,y) in pts:
                if y>=y0+h-3 and r.random()<.35: T.p(x,y,acc[2] if r.random()<.5 else acc[3])
        if k=='filigree':
            for (x,y) in pts:
                if (x+y)%4==0 and (x-y)%4==0: T.p(x,y,acc[3])
        if k=='stars':
            for q in r.sample(pts,min(2,len(pts))): T.p(*q,'#fff6c0')
        if k=='glow_edge':
            for x in range(x0,x0+w):
                if T.px[x,y0+h-1][3]: T.p(x,y0+h-1,acc[2])
        if k=='inlay': pass
BOX={'head':(0,0,8,8,8),'body':(16,16,8,12,4),'arm':(40,16,4,12,4),'leg':(0,16,4,12,4)}
def faces(part):
    u,v,w,h,d=BOX[part]
    return {'top':(u+d,v,w,d),'bottom':(u+d+w,v,w,d),'right':(u,v+d,d,h),'front':(u+d,v+d,w,h),'left':(u+d+w,v+d,d,h),'back':(u+d+w+d,v+d,w,h)}
def build_layers(k,cfg,pal,acc,seed):
    L1,L2=Tex(),Tex(); m=cfg['motif']; H=cfg['helmet']; C=cfg['chestplate']; G=cfg['leggings']; B=cfg['boots']
    # helmet
    for f,(x,y,w,h) in faces('head').items():
        plate(L1,x,y,w,h,pal,seed+len(f)); motif(L1,(x,y,w,h),m,pal,acc,seed)
        if 'band' in H.get('add',[]) and f in('front','back','left','right'):
            for i in range(w): L1.p(x+i,y+2,acc[2])
    fx,fy,_,_=faces('head')['front']; v=H.get('visor'); ch=H.get('cheek',2)
    if v is None or v=='nose':
        for yy in range(3,8):
            for xx in range(min(ch,3),8-min(ch,3)): L1.clr(fx+xx,fy+yy)
        if v=='nose':
            for yy in range(3,6): L1.p(fx+3,fy+yy,pal[2]); L1.p(fx+4,fy+yy,pal[1])
    elif v=='slit':
        for xx in range(1,7): L1.p(fx+xx,fy+3,pal[0]); L1.p(fx+xx,fy+4,acc[2])
        for xx in range(2,6): L1.p(fx+xx,fy+6,pal[1])
    elif v=='glass':
        for yy in range(2,7):
            for xx in range(1,7): L1.p(fx+xx,fy+yy,acc[1] if yy>3 else acc[2],190)
        L1.p(fx+2,fy+3,'#ffffff',220); L1.p(fx+1,fy+2,'#ffffff',220)
    elif v=='mask':
        for xx in (2,5): L1.p(fx+xx,fy+4,acc[3]); L1.p(fx+xx,fy+3,acc[2])
        for xx in range(2,6): L1.p(fx+xx,fy+6,pal[0])
    tx,ty,_,_=faces('head')['top']
    if 'crest' in H.get('add',[]):
        for yy in range(8): L1.p(tx+3,ty+yy,pal[4]); L1.p(tx+4,ty+yy,pal[1])
    if 'crown' in H.get('add',[]) or 'halo' in H.get('add',[]):
        for f in ('front','back','left','right'):
            x,y,w,h=faces('head')[f]
            for i in range(0,w,2): L1.p(x+i,y,acc[3])
    if 'hood' in H.get('add',[]):
        for f in ('left','right','back'):
            x,y,w,h=faces('head')[f]
            for yy in range(h):
                for xx in range(w): 
                    if L1.px[x+xx,y+yy][3]: L1.p(x+xx,y+yy,dk(pal[1],.8) if (xx+yy)%3 else pal[1])
    for side in ('left','right'):
        x,y,w,h=faces('head')[side]
        if 'horns' in H.get('add',[]): 
            for q in [(2,1),(3,1),(3,2),(4,2),(4,3)]: L1.p(x+q[0],y+q[1],HAND['bone'][3])
        if 'fins' in H.get('add',[]):
            for yy in range(1,6): L1.p(x+3,y+yy,acc[2])
        if 'wings' in H.get('add',[]):
            for q in [(1,1),(2,1),(3,2),(4,2),(5,3),(2,3),(3,4)]: L1.p(x+q[0],y+q[1],'#f4f8ff')
    # chest body + arms
    for f,(x,y,w,h) in faces('body').items():
        plate(L1,x,y,w,h,pal,seed+7+len(f)); motif(L1,(x,y,w,h),m,pal,acc,seed+3)
    bx,by,_,_=faces('body')['front']; nk=C.get('neck','round'); a=C.get('add',[])
    if nk=='round': L1.clr(bx+3,by); L1.clr(bx+4,by)
    if nk=='v':
        for q in [(2,0),(3,0),(4,0),(5,0),(3,1),(4,1),(3,2) if False else (4,2)]: L1.clr(bx+q[0],by+q[1])
        L1.clr(bx+3,by+2)
    if nk=='collar':
        for i in range(8): L1.p(bx+i,by,pal[4] if i in(0,7) else acc[1])
    if 'core' in a:
        for q in [(3,4),(4,4),(3,5),(4,5)]: L1.p(bx+q[0],by+q[1],acc[2] if q!=(3,4) else acc[3])
    if 'ribs' in a:
        for yy in (5,7,9):
            for xx in range(1,7): 
                if (xx,yy) not in((3,4),(4,4)): L1.p(bx+xx,by+yy,pal[1])
    if 'belt' in a:
        for xx in range(8): L1.p(bx+xx,by+10,acc[1])
        L1.p(bx+3,by+10,acc[3]); L1.p(bx+4,by+10,acc[3])
    if 'waist' in a:
        for yy in range(7,12): L1.clr(bx,by+yy); L1.clr(bx+7,by+yy)
    kx,ky,_,_=faces('body')['back']
    for yy in range(1,11): L1.p(kx+3,ky+yy,pal[1]); L1.p(kx+4,ky+yy,pal[2])
    if 'wings' in a:
        for q in [(1,2),(2,3),(1,4),(2,5),(1,6),(6,2),(5,3),(6,4),(5,5),(6,6)]: L1.p(kx+q[0],ky+q[1],'#f4f8ff')
    for f,(x,y,w,h) in faces('arm').items():
        plate(L1,x,y,w,h,pal,seed+11+len(f),rows=range(0,7) if f not in('top','bottom') else None)
        motif(L1,(x,y,w,7 if f not in('top','bottom') else h),m,pal,acc,seed+5)
        if 'pauldron' in a and f not in('top','bottom'):
            for xx in range(w): L1.p(x+xx,y,pal[4]); L1.p(x+xx,y+3,acc[1])
        if 'spikes' in a and f=='top': L1.p(x+1,y+1,acc[3]); L1.p(x+2,y+2,acc[3])
    # boots on layer1 leg region lower rows
    for f,(x,y,w,h) in faces('leg').items():
        if f in('top',): continue
        rows=range(h-5,h) if f!='bottom' else range(0,h)
        plate(L1,x,y,w,h,pal,seed+13+len(f),rows=rows)
        if f!='bottom':
            if 'cuff' in B.get('add',[]):
                for xx in range(w): L1.p(x+xx,y+h-5,acc[1])
            if 'strap' in B.get('add',[]):
                for xx in range(w): L1.p(x+xx,y+h-3,acc[2])
            if 'sole' in B.get('add',[]):
                for xx in range(w): L1.p(x+xx,y+h-1,pal[0])
            if 'spike' in B.get('add',[]) and f=='front': L1.p(x+1,y+h-2,acc[3]); L1.p(x+2,y+h-2,acc[3])
            if 'wing' in B.get('add',[]) and f in('left','right'):
                for q in [(1,h-4),(2,h-5),(3,h-5)]: L1.p(x+q[0],y+q[1],'#f4f8ff')
    # leggings layer2: body belt rows + legs upper rows
    for f,(x,y,w,h) in faces('body').items():
        if f in('top','bottom'): continue
        plate(L2,x,y,w,h,pal,seed+17+len(f),rows=range(h-4,h))
        if 'belt' in G.get('add',[]):
            for xx in range(w): L2.p(x+xx,y+h-4,acc[1])
    for f,(x,y,w,h) in faces('leg').items():
        if f in('top',): continue
        rows=range(0,h-2) if f!='bottom' else range(0,h)
        plate(L2,x,y,w,h,pal,seed+19+len(f),rows=rows); motif(L2,(x,y,w,h-2),m,pal,acc,seed+9)
        if f=='bottom': continue
        ga=G.get('add',[])
        if 'knee' in ga and f=='front':
            for xx in range(w): L2.p(x+xx,y+4,acc[2])
        if 'stripe' in ga and f in('left','right'):
            for yy in range(0,h-2): L2.p(x+1,y+yy,acc[2])
        if 'tasset' in ga:
            for yy in range(0,3):
                for xx in range(w): L2.p(x+xx,y+yy,pal[1] if yy==2 else acc[1])
        if 'fin' in ga and f in('left','right'):
            for q in [(2,1),(2,2),(1,2),(2,3)]: L2.p(x+q[0],y+q[1],acc[2])
    L1.im.save(f'{OUTA}/{k}_layer_1.png'); L2.im.save(f'{OUTA}/{k}_layer_2.png')
    return L1.im,L2.im
