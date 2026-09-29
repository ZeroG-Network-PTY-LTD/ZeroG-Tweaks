import os, zipfile
from PIL import Image, ImageDraw, ImageFont
from tex import item, ore, storage, stone, hx
from data import M, PL, STONES
F='/usr/share/fonts/truetype/dejavu/'
def fnt(n,s): return ImageFont.truetype(F+n,s)
FB=lambda s:fnt('DejaVuSans-Bold.ttf',s); FR=lambda s:fnt('DejaVuSans.ttf',s); FM=lambda s:fnt('DejaVuSansMono.ttf',s)
NS='zerog_tweaks'; OUT='out/assets/'+NS+'/textures'
BG=(246,245,242,255); PANEL=(235,233,243,255); BORDER=(214,212,222,255); INK=(34,32,40,255); SUB=(110,108,118,255)

# ---------- texture generation
TEX={}
def put(kind,name,im): TEX[(kind,name)]=im
seed=1
for k,m in M.items():
    p=m['pal']; st=STONES[m['stone']]; r=m['role']; seed+=7
    oname=f'{k}_ore' if m['stone']!='deepslate' else f'deepslate_{k}_ore'
    put('block',oname,ore(st,p,seed))
    if r=='fuel': put('item',k,item('fuel',p)); put('block',k+'_block',storage(p,'fuel',seed))
    elif r=='metal':
        put('item','raw_'+k,item('raw',p)); put('item',k+'_ingot',item('ingot',p)); put('item',k+'_nugget',item('nugget',p))
        put('block',k+'_block',storage(p,'metal',seed)); put('block','raw_'+k+'_block',storage(p,'grain',seed+1))
    elif r=='dust': put('item',k,item('dust',p)); put('block',k+'_block',storage(p,'grain',seed))
    else: put('item',k,item(r,p)); put('block',k+'_block',storage(p,'gem',seed))
for i,(sk,sp) in enumerate(STONES.items()):
    if sk!='deepslate': put('block',sk,stone(sp,100+i))
for (kind,name),im in TEX.items():
    d=f'{OUT}/{kind}'; os.makedirs(d,exist_ok=True); im.save(f'{d}/{name}.png')

# ---------- drawing helpers
def checker(w,h,c=6):
    im=Image.new('RGBA',(w,h),(255,255,255,255)); d=ImageDraw.Draw(im)
    for y in range(0,h,c):
        for x in range(0,w,c):
            if (x//c+y//c)%2: d.rectangle([x,y,x+c-1,y+c-1],fill=(238,236,244,255))
    return im
def up(im,s): return im.resize((im.width*s,im.height*s),Image.NEAREST)
def shade(c,f): return (int(c[0]*f),int(c[1]*f),int(c[2]*f),c[3])
def extrude(tex,s=9,depth=2):
    W=16*s+depth*s+4; im=Image.new('RGBA',(W,W),(0,0,0,0)); px=tex.load(); d=ImageDraw.Draw(im)
    for k in range(depth*s,0,-1):
        for y in range(16):
            for x in range(16):
                c=px[x,y]
                if c[3] and any(0<=x+dx<16 and 0<=y+dy<16 and px[x+dx,y+dy][3] for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): d.rectangle([x*s+k,y*s+depth*s-k,x*s+k+s-1,y*s+depth*s-k+s-1],fill=shade(c,.55))
    im.alpha_composite(up(tex,s),(0,depth*s)); return im
def cube(top,left,right,s=6):
    w,h=s*0.866,s*0.5; W=int(32*w)+2; H=int(32*h+16*s)+2; im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    F0=(W/2,1); a=(w,h); b=(-w,h); dn=(0,s)
    def face(tex,O,U,V,f):
        px=tex.load()
        for y in range(16):
            for x in range(16):
                P=lambda u,v:(O[0]+u*U[0]+v*V[0],O[1]+u*U[1]+v*V[1])
                d.polygon([P(x,y),P(x+1,y),P(x+1,y+1),P(x,y+1)],fill=shade(px[x,y],f))
    face(top,F0,a,b,1.0)
    L=(F0[0]+16*b[0],F0[1]+16*b[1]); N=(F0[0],F0[1]+32*h)
    face(left,L,a,dn,.82); face(right,N,(w,-h),dn,.64); return im

def text(d,xy,s,f,c=INK): d.text(xy,s,font=f,fill=c)
def wrap(s,f,w,d):
    out=[];line=''
    for word in s.split():
        t=(line+' '+word).strip()
        if d.textlength(t,font=f)>w: out.append(line); line=word
        else: line=t
    return out+[line]

CW,CH=512,330
def card(kind,name,title,typ,desc):
    tex=TEX[(kind,name)]; im=Image.new('RGBA',(CW,CH),(255,255,255,255)); d=ImageDraw.Draw(im)
    d.rectangle([0,0,CW-1,CH-1],outline=BORDER)
    text(d,(12,10),title,FB(15)); text(d,(12,30),f"{'Block' if kind=='block' else 'Item'} · {typ}   ·   {NS}:{name}",FM(10),SUB)
    d.rounded_rectangle([10,50,215,272],8,fill=PANEL)
    if kind=='block':
        c=cube(tex,tex,tex); im.alpha_composite(c,(10+(205-c.width)//2,50+(222-c.height)//2-6))
        text(d,(16,258),'3D (block)',FR(9),SUB)
        for i,lab in enumerate(['TOP','FRONT','BOTTOM']):
            f=tex if lab!='BOTTOM' else Image.eval(tex,lambda v:v) ; x=230+i*72
            im.alpha_composite(up(f,4),(x,56)); d.rectangle([x,56,x+63,56+63],outline=INK)
            d.rectangle([x,56,x+6*len(lab)+4,66],fill=INK); text(d,(x+2,56),lab,FB(8),(255,255,255,255))
        y0=196
    else:
        e=extrude(tex); im.alpha_composite(e,(10+(205-e.width)//2,50+(222-e.height)//2))
        text(d,(16,258),'3D (extruded 2 px)',FR(9),SUB)
        im.alpha_composite(checker(128,128),(230,52)); im.alpha_composite(up(tex,8),(230,52)); d.rectangle([230,52,357,179],outline=BORDER)
        d.rectangle([230,52,262,62],fill=INK); text(d,(232,52),'FRONT',FB(8),(255,255,255,255))
        # side strip: leftmost opaque pixel per row
        px=tex.load(); d.rectangle([366,52,379,179],fill=(250,250,252,255),outline=BORDER)
        for y in range(16):
            for x in range(16):
                if px[x,y][3]:
                    q=px[min(15,x+1),y] if px[min(15,x+1),y][3] else px[x,y]
                    d.rectangle([367,52+y*8,378,59+y*8],fill=shade(q,.8)); break
        text(d,(362,184),'SIDE',FB(7),SUB); y0=196
    x=230
    for s in (1,2,4):
        cb=checker(16*s,16*s,3); cb.alpha_composite(up(tex,s)); im.alpha_composite(cb,(x,y0+64-16*s)); x+=16*s+10
    text(d,(230,y0+68),'in slot: 1x  2x  4x',FR(9),SUB)
    yy=282
    for ln in wrap(desc,FR(11),CW-24,d)[:3]: text(d,(12,yy),ln,FR(11)); yy+=15
    return im

def sheet(fname,title,subtitle,cards,rows):
    cols=3; gap=12; M0=28; top=96; nr=(len(cards)+2)//3
    th=40+28*(len(rows)+1)
    W=M0*2+cols*CW+(cols-1)*gap; H=top+nr*(CH+gap)+30+th+30
    im=Image.new('RGBA',(W,H),BG); d=ImageDraw.Draw(im)
    text(d,(M0,24),title,FB(30)); text(d,(M0,64),subtitle,FR(13),SUB)
    for i,c in enumerate(cards):
        im.alpha_composite(card(*c),(M0+(i%3)*(CW+gap),top+(i//3)*(CH+gap)))
    y=top+nr*(CH+gap)+18; text(d,(M0,y),'Recipes & uses',FB(18)); y+=36
    cx=[M0,M0+300,M0+860]; d.rectangle([M0,y,W-M0,y+26],fill=(232,230,240,255))
    for x,h in zip(cx,['Item','Comes from','Used for']): text(d,(x+8,y+6),h,FB(12))
    y+=26
    for j,(kind,name,label,src,use) in enumerate(rows):
        if j%2: d.rectangle([M0,y,W-M0,y+27],fill=(250,249,247,255))
        im.alpha_composite(TEX[(kind,name)],(M0+8,y+5)); text(d,(M0+30,y+6),label,FB(12))
        text(d,(cx[1]+8,y+7),src,FR(11)); text(d,(cx[2]+8,y+7),use,FR(11)); y+=28
    d.line([M0,y,W-M0,y],fill=BORDER)
    im.convert('RGB').save(fname)

os.makedirs('sheets',exist_ok=True)
RT={'fuel':'fuel','metal':'metal','dust':'dust','orb':'lore gem','diamond':'rare gem','crystal':'trade gem'}
def g(k,suffix=''): return M[k]
# ---- Sol sheet
c=[('block','deepslate_nullifite_ore','Deepslate Nullifite Ore','ore','Deepslate with rare veins of fractured void metal. Fracture pixels go on an emissive layer.'),
   ('item','raw_nullifite','Raw Nullifite','raw metal','Rough chunk of void metal with glowing fracture flecks.'),
   ('item','nullifite_ingot','Nullifite Ingot','metal','Near-black bar with a violet-white top edge.'),
   ('item','nullifite_nugget','Nullifite Nugget','metal','Small shards of void metal.'),
   ('block','nullifite_block','Block of Nullifite','storage','9 ingots; riveted plates with glowing violet studs.'),
   ('item','regolith','Regolith Dust','dust','Fine grey moon dust.'),
   ('item','moonsteel_ingot','Moonsteel Ingot','metal','Pale blue-grey steel with a cold sheen.'),
   ('item','selenite','Selenite','crystal','Milky pale crystal; the T2 focus lens.'),
   ('item','ferrox_ingot','Ferrox Ingot','metal','Rust-red iron-oxide bar.'),
   ('item','olympium_ingot','Olympium Ingot','metal','Dense bronze-red heavy metal bar.'),
   ('item','aresite','Aresite','rare gem','Deep red cut gem; the T2 core.'),
   ('block','aresite_ore','Aresite Ore','ore','Martian Stone with rare red gem clusters.')]
r=[('item','nullifite_ingot','Nullifite','Deepslate ore, Y -64 to -40','T1 teleporter, Nullifite gear'),
   ('item','regolith','Regolith Dust','Moon surface','Smelts into Lunar Glass'),
   ('item','moonsteel_ingot','Moonsteel','Moon ore, mid-depth','T2 frames; alloy for Olympium gear'),
   ('item','selenite','Selenite','Moon deep geodes','T2 focus lens, Selenite Lamp'),
   ('item','ferrox_ingot','Ferrox','Mars ore, common','Basic Mars parts'),
   ('item','olympium_ingot','Olympium','Mars ore, deep','Olympium gear, Olympium Plating'),
   ('item','aresite','Aresite','Mars ore, rare and deep','T2 core')]
sheet('sheets/01_sol_materials.png','Sol materials  —  icons with 3D view',
      'ZeroG Tweaks · Nullifite, Moon and Mars. Items: 3D extruded view, 16×16 front at 8×, side strip, in-slot previews. Blocks: 3D cube plus faces.',c,r)
# ---- planet sheets
for n,(pk,(pn,gal,st,lst)) in enumerate(PL.items(),start=2):
    ks=[x[0] for x in lst]; fuel,com,std,pre,dust,lore,rare,trade=ks
    N=lambda k:M[k]['name']
    c=[('item',fuel,N(fuel),'fuel',M[fuel]['desc']),('item','raw_'+com,'Raw '+N(com),'raw metal','Unsmelted '+N(com)+' chunk.'),
       ('item',com+'_ingot',N(com)+' Ingot','common metal',M[com]['desc']),('item',std+'_ingot',N(std)+' Ingot','standard metal',M[std]['desc']),
       ('item',pre+'_ingot',N(pre)+' Ingot','precious metal',M[pre]['desc']),('item',pre+'_nugget',N(pre)+' Nugget','precious metal','Small pieces of '+N(pre)+'.'),
       ('item',dust,N(dust),'energy dust',M[dust]['desc']),('item',lore,N(lore),'lore gem',M[lore]['desc']),
       ('item',rare,N(rare),'rare gem',M[rare]['desc']),('item',trade,N(trade),'trade gem',M[trade]['desc']),
       ('block',rare+'_ore',N(rare)+' Ore','ore',f'{st.replace("_"," ").title()} with rare {N(rare)} clusters.'),
       ('block',std+'_block','Block of '+N(std),'storage','9 ingots; riveted plates, the '+pn+' building metal.')]
    def ic(k): r=M[k]['role']; return ('item',k+'_ingot') if r=='metal' else ('item',k)
    r=[ic(k)+(N(k),M[k]['src'],M[k]['use']) for k in ks]
    sheet(f'sheets/0{n}_{pk}_materials.png',f'{pn} materials  —  icons with 3D view',
          f'ZeroG Tweaks · {gal} Resource planet · 8 ores in vanilla role order. Glowing accents go on an emissive layer.',c,r)
# ---- zip
with zipfile.ZipFile('zerog_tweaks_textures.zip','w') as z:
    for root,_,files in os.walk('out'):
        for f in files: z.write(os.path.join(root,f),os.path.relpath(os.path.join(root,f),'out'))
print(len(TEX),'textures')
