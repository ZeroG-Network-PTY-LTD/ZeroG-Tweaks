import os, math, hashlib
from PIL import Image, ImageDraw, ImageFont
from mobs_data import MOBS
from tex import hx
Fp='/usr/share/fonts/truetype/dejavu/'; FB=lambda s:ImageFont.truetype(Fp+'DejaVuSans-Bold.ttf',s); FR=lambda s:ImageFont.truetype(Fp+'DejaVuSans.ttf',s); FM=lambda s:ImageFont.truetype(Fp+'DejaVuSansMono.ttf',s)
BG=(246,245,242,255); INK=(34,32,40,255); SUB=(110,108,118,255); BORDER=(214,212,222,255); WH=(255,255,255,255); LINE=(124,92,220,255); GRID=(238,238,244,255)
def sh(c,f): return (max(0,min(255,int(c[0]*f))),max(0,min(255,int(c[1]*f))),max(0,min(255,int(c[2]*f))),255)
def h(*a): return int(hashlib.md5(repr(a).encode()).hexdigest()[:6],16)/0xffffff
CR=None
def tcol(base,pat,i,u,v,f):
    r=h(i,u,v)
    if pat=='glow': return sh(base,1.0 if r>.2 else 1.12)
    m=1.0
    if pat=='noise': m=.92+.16*r
    if pat=='stripes': m=(.8 if v%3==0 else 1.0)*(.95+.1*r)
    if pat=='fur': m=(.84 if (u+int(r*3))%3==0 else 1.0)
    if pat=='crystal': m=1.25 if (u+v)%4==0 else (.85 if (u-v)%5==0 else 1.0)
    if pat=='rivets': m=1.3 if (u%4==1 and v%4==1) else .95+.1*r
    if pat=='spots': m=1.35 if r>.86 else .95
    if pat=='cracks':
        if r>.9: return CR
        m=.92+.12*r
    return sh(base,m*f)
VIEWS={'front':('FRONT  (looking at its face)','x','y',lambda b:-b[3]),'side':('LEFT SIDE  (head points left)','z','y',lambda b:b[1]),
       'top':('TOP  (looking down, head at the top)','x','z',lambda b:b[2]),'bottom':('BOTTOM  (looking up, head at the top)','xm','z',lambda b:-b[5])}
def bounds(B):
    return (min(b[1] for b in B),max(b[4] for b in B),min(b[2] for b in B),max(b[5] for b in B),min(b[3] for b in B),max(b[6] for b in B))
def rng(b,ax):
    return {'x':(b[1],b[4]),'xm':(-b[4],-b[1]),'y':(b[2],b[5]),'z':(b[3],b[6])}[ax]
def render_view(m,view,sc):
    B=m['boxes']; pal={k:hx(v) for k,v in m['pal'].items()}; X0,X1,Y0,Y1,Z0,Z1=bounds(B)
    _,ha,va,key=VIEWS[view]
    hr={'x':(X0,X1),'xm':(-X1,-X0),'z':(Z0,Z1)}[ha]; vr={'y':(Y0,Y1),'z':(Z0,Z1)}[va]
    W=math.ceil((hr[1]-hr[0])*sc)+2; H=math.ceil((vr[1]-vr[0])*sc)+2
    im=Image.new('RGBA',(W,H),(0,0,0,0)); ids=[[None]*W for _ in range(H)]; d=ImageDraw.Draw(im)
    order=sorted(range(len(B)),key=lambda i:key(B[i]) if view!='side' else -B[i][1])
    if view=='side': order=sorted(range(len(B)),key=lambda i:-(B[i][1]+B[i][4]))
    if view=='front': order=sorted(range(len(B)),key=lambda i:-(B[i][3]+B[i][6]))
    if view=='top': order=sorted(range(len(B)),key=lambda i:(B[i][2]+B[i][5]))
    if view=='bottom': order=sorted(range(len(B)),key=lambda i:-(B[i][2]+B[i][5]))
    f={'front':1.0,'side':.86,'top':1.08,'bottom':.7}[view]
    for i in order:
        b=B[i]; a0,a1=rng(b,ha); c0,c1=rng(b,va); base=pal[b[7]]
        sx0=(a0-hr[0])*sc; sx1=(a1-hr[0])*sc
        if va=='y': sy0=(vr[1]-c1)*sc; sy1=(vr[1]-c0)*sc
        else: sy0=(c0-vr[0])*sc; sy1=(c1-vr[0])*sc
        nu=max(1,round(a1-a0)); nv=max(1,round(c1-c0))
        for iu in range(nu):
            for iv in range(nv):
                x0=sx0+(sx1-sx0)*iu/nu; x1=sx0+(sx1-sx0)*(iu+1)/nu; y0=sy0+(sy1-sy0)*iv/nv; y1=sy0+(sy1-sy0)*(iv+1)/nv
                d.rectangle([round(x0),round(y0),max(round(x0),round(x1)-1),max(round(y0),round(y1)-1)],fill=tcol(base,b[8],i,iu,iv,f))
        d.rectangle([round(sx0),round(sy0),max(round(sx0),round(sx1)-1),max(round(sy0),round(sy1)-1)],outline=sh(base,.45))
        for yy in range(max(0,round(sy0)),min(H,round(sy1))):
            for xx in range(max(0,round(sx0)),min(W,round(sx1))): ids[yy][xx]=i
    return im,ids,hr,vr
def iso(m,sc):
    B=m['boxes']; pal={k:hx(v) for k,v in m['pal'].items()}; X0,X1,Y0,Y1,Z0,Z1=bounds(B)
    w,hh=sc*.866,sc*.5
    def raw(x,y,z): return (x*w+z*w, x*hh-z*hh-y*sc)
    cs=[raw(x,y,z) for x in(X0,X1) for y in(Y0,Y1) for z in(Z0,Z1)]
    mx=min(c[0] for c in cs); my=min(c[1] for c in cs)
    W=int(max(c[0] for c in cs)-mx)+4; H=int(max(c[1] for c in cs)-my)+4
    PP=lambda x,y,z:(raw(x,y,z)[0]-mx+2,raw(x,y,z)[1]-my+2)
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    order=sorted(range(len(B)),key=lambda i:((B[i][1]+B[i][4])/2-(B[i][3]+B[i][6])/2+(B[i][2]+B[i][5])/2*.5))
    for i in order:
        x0,y0,z0,x1,y1,z1=B[i][1:7]; c=pal[B[i][7]]; o=sh(c,.4); g=B[i][8]=='glow'
        d.polygon([PP(x0,y1,z0),PP(x1,y1,z0),PP(x1,y1,z1),PP(x0,y1,z1)],fill=sh(c,1.1),outline=o)
        d.polygon([PP(x0,y1,z0),PP(x1,y1,z0),PP(x1,y0,z0),PP(x0,y0,z0)],fill=sh(c,1.0 if g else .9),outline=o)
        d.polygon([PP(x1,y1,z0),PP(x1,y1,z1),PP(x1,y0,z1),PP(x1,y0,z0)],fill=sh(c,.9 if g else .68),outline=o)
    return im
def wrap(s,f,w,d):
    out=[];line=''
    for word in s.split():
        t=(line+' '+word).strip()
        if d.textlength(t,font=f)>w: out.append(line); line=word
        else: line=t
    return out+[line]
PW,PH=760,560
def panel(m,view,sc):
    img,ids,hr,vr=render_view(m,view,sc); im=Image.new('RGBA',(PW,PH),WH); d=ImageDraw.Draw(im); d.rectangle([0,0,PW-1,PH-1],outline=BORDER)
    d.text((16,14),VIEWS[view][0],font=FB(14),fill=INK); d.text((PW-160,16),'same scale in all views',font=FR(10),fill=SUB)
    ox=(PW-img.width)//2; oy=60+(420-img.height)//2
    step=sc if sc>=6 else sc*2
    gx0,gy0=ox-2*sc,oy-2*sc; gx1,gy1=ox+img.width+2*sc,oy+img.height+2*sc
    x=gx0
    while x<=gx1: d.line([x,gy0,x,gy1],fill=GRID); x+=step
    y=gy0
    while y<=gy1: d.line([gx0,y,gx1,y],fill=GRID); y+=step
    im.alpha_composite(img,(ox,oy))
    if VIEWS[view][2]=='y':
        d.line([gx0-6,oy+img.height-1,gx1+6,oy+img.height-1],fill=(80,80,90,255)); d.text((gx1+10,oy+img.height-8),'ground',font=FR(10),fill=SUB)
    hpx=vr[1]-vr[0]; wpx=hr[1]-hr[0]; rx=gx0-14
    d.line([rx,oy,rx,oy+img.height],fill=INK); d.line([rx-4,oy,rx+4,oy],fill=INK); d.line([rx-4,oy+img.height,rx+4,oy+img.height],fill=INK)
    t=f'{hpx:g} px ({hpx/16:.2f} bl)'; d.text((rx-d.textlength(t,font=FR(10))/2,oy-18),t,font=FR(10),fill=INK)
    by=oy+img.height+18; d.line([ox,by,ox+img.width,by],fill=INK); d.line([ox,by-4,ox,by+4],fill=INK); d.line([ox+img.width,by-4,ox+img.width,by+4],fill=INK)
    t=f'{wpx:g} px ({wpx/16:.2f} blocks)'; d.text((ox+img.width/2-d.textlength(t,font=FR(11))/2,by+6),t,font=FR(11),fill=INK)
    # callouts
    pts={}
    for yy in range(0,img.height,max(1,sc//2)):
        for xx in range(0,img.width,max(1,sc//2)):
            i=ids[yy][xx]
            if i is not None and m['boxes'][i][0]: pts.setdefault(m['boxes'][i][0],[]).append((xx,yy))
    left=[];right=[]
    for lab,ps in pts.items():
        cx=sum(p[0] for p in ps)/len(ps); cy=sum(p[1] for p in ps)/len(ps)
        best=min(ps,key=lambda p:(p[0]-cx)**2+(p[1]-cy)**2); anchor=(ox+best[0],oy+best[1])
        (left if cx<img.width/2 else right).append((lab,anchor))
    for lst,side in ((left,'L'),(right,'R')):
        lst.sort(key=lambda a:a[1][1]); last=40
        for lab,(ax,ay) in lst:
            ly=max(ay,last+20); ly=min(ly,PH-40); last=ly
            if side=='L':
                tw=d.textlength(lab,font=FR(11)); d.text((14,ly-7),lab,font=FR(11),fill=INK); d.line([18+tw,ly,ax,ay],fill=LINE)
            else:
                tx=PW-14-d.textlength(lab,font=FR(11)); d.text((tx,ly-7),lab,font=FR(11),fill=INK); d.line([ax,ay,tx-4,ly],fill=LINE)
            d.ellipse([ax-3,ay-3,ax+3,ay+3],fill=LINE)
    ax_={'front':'horizontal: X    vertical: Y up','side':'horizontal: Z (front on the left)    vertical: Y up','top':'horizontal: X    vertical: Z (front at the top)','bottom':'horizontal: X (mirrored)    vertical: Z (front at the top)'}[view]
    d.text((16,PH-22),ax_,font=FR(10),fill=SUB)
    return im
def render_all(MB,start=1,only=None):
  os.makedirs('sheets/mobs',exist_ok=True)
  for n,(k,m) in enumerate(MB.items(),start=start):
      if only and k not in only: continue
      X0,X1,Y0,Y1,Z0,Z1=bounds(m['boxes']); md=max(X1-X0,Y1-Y0,Z1-Z0)
      sc=max(3,min(22,int(400/md)))
      globals()['CR']=hx(next((m['pal'][c] for c in ('rift','ember','crust','core','glow','vent','ice') if c in m['pal']),'#ffb040'))
      W=1596; H=2400; im=Image.new('RGBA',(W,H),BG); d=ImageDraw.Draw(im)
      d.text((28,22),f"{m['name']}  —  reference sheet",font=FB(30),fill=INK); d.text((28,64),m['info']+' · ZeroG Tweaks',font=FR(13),fill=SUB)
      for i,v in enumerate(['front','side','top','bottom']):
          im.alpha_composite(panel(m,v,sc),(28+(i%2)*(PW+20),100+(i//2)*(PH+20)))
      y=100+2*(PH+20)+10
      # iso + stats + notes
      box_=Image.new('RGBA',(500,420),WH); bd=ImageDraw.Draw(box_); bd.rectangle([0,0,499,419],outline=BORDER); bd.text((16,14),'3D VIEW',font=FB(14),fill=INK)
      bd.rounded_rectangle([14,40,485,405],10,fill=(235,233,243,255))
      iv=iso(m,max(2,int(sc*.8)))
      if iv.width>440 or iv.height>340: iv=iv.resize((int(iv.width*min(440/iv.width,340/iv.height)),int(iv.height*min(440/iv.width,340/iv.height))),Image.NEAREST)
      box_.alpha_composite(iv,(250-iv.width//2,222-iv.height//2)); im.alpha_composite(box_,(28,y))
      sx=548; d.text((sx,y),'Stats and behavior',font=FB(17),fill=INK); yy=y+32
      for a,b in m['stats']:
          d.text((sx,yy),a,font=FB(12),fill=INK)
          for ln in wrap(b,FR(12),380,d): d.text((sx+120,yy),ln,font=FR(12),fill=INK); yy+=17
          yy+=7
      nx=1090; d.text((nx,y),'Notes for the artist and code',font=FB(17),fill=INK); ny=y+32
      for t in m['notes']+[f"Texture: textures/entity/{k}.png (+ {k}_emissive.png); model built in Blockbench to these boxes.",'Proposed stats; tune in playtesting.']:
          for ln in wrap(t,FR(12),470,d): d.text((nx,ny),ln,font=FR(12),fill=INK); ny+=17
          ny+=7
      y=max(y+440,yy,ny)+10; d.text((28,y),'Palette',font=FB(17),fill=INK); y+=30
      for j,(kk,c) in enumerate(m['pal'].items()):
          x=28+(j%8)*190; yy=y+(j//8)*52
          d.rectangle([x,yy,x+32,yy+32],fill=hx(c),outline=(120,120,120,255)); d.text((x+40,yy+2),kk,font=FR(11),fill=INK); d.text((x+40,yy+17),c,font=FM(10),fill=SUB)
      y=yy+60
      im.crop((0,0,W,y)).convert('RGB').save(f'sheets/mobs/{n:02d}_{k}.png')

if __name__=='__main__': render_all(MOBS)
