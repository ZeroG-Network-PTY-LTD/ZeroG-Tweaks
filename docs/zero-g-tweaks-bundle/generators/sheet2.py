import os, zipfile
from PIL import Image, ImageDraw, ImageFont
import blocks as K
F='/usr/share/fonts/truetype/dejavu/'
FB=lambda s:ImageFont.truetype(F+'DejaVuSans-Bold.ttf',s); FR=lambda s:ImageFont.truetype(F+'DejaVuSans.ttf',s); FM=lambda s:ImageFont.truetype(F+'DejaVuSansMono.ttf',s)
NS='zerog_tweaks'; OUT='out/assets/'+NS+'/textures/block'
BG=(246,245,242,255); PANEL=(235,233,243,255); BORDER=(214,212,222,255); INK=(34,32,40,255); SUB=(110,108,118,255); WH=(255,255,255,255)
def up(im,s): return im.resize((16*s,16*s),Image.NEAREST)
def shade(c,f): return (int(c[0]*f),int(c[1]*f),int(c[2]*f),c[3])
def cube(top,left,right,s=7):
    w,h=s*0.866,s*0.5; W=int(32*w)+2; H=int(32*h+16*s)+2; im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    F0=(W/2,1); a=(w,h); b=(-w,h); dn=(0,s)
    def face(tex,O,U,V,f):
        px=tex.load()
        for y in range(16):
            for x in range(16):
                P=lambda u,v:(O[0]+u*U[0]+v*V[0],O[1]+u*U[1]+v*V[1])
                if px[x,y][3]: d.polygon([P(x,y),P(x+1,y),P(x+1,y+1),P(x,y+1)],fill=shade(px[x,y],f))
    face(top,F0,a,b,1.0); L=(F0[0]+16*b[0],F0[1]+16*b[1]); N=(F0[0],F0[1]+32*h)
    face(left,L,a,dn,.84); face(right,N,(w,-h),dn,.66); return im
def T(d,xy,s,f,c=INK): d.text(xy,s,font=f,fill=c)
def wrap(s,f,w,d):
    out=[];line=''
    for word in s.split():
        t=(line+' '+word).strip()
        if d.textlength(t,font=f)>w: out.append(line); line=word
        else: line=t
    return out+[line]
CW,CH=770,350
def card(name,title,faces,desc,state,model):
    im=Image.new('RGBA',(CW,CH),WH); d=ImageDraw.Draw(im); d.rectangle([0,0,CW-1,CH-1],outline=BORDER)
    T(d,(14,12),title,FB(15)); T(d,(14,32),f'{NS}:{name}',FM(10),SUB)
    c=cube(faces['top'],faces['front'],faces['side'],s=6); im.alpha_composite(c,(14+(210-c.width)//2,54))
    ox,oy,S=250,52,64
    lay=[('TOP',1,0,'top'),('LEFT',0,1,'side'),('FRONT',1,1,'front'),('RIGHT',2,1,'side'),('BACK',3,1,'side'),('BOTTOM',1,2,'bottom')]
    for lab,cx,cy,k in lay:
        x,y=ox+cx*S,oy+cy*S; im.alpha_composite(up(faces[k],4),(x,y)); d.rectangle([x,y,x+S-1,y+S-1],outline=INK)
        d.rectangle([x,y,x+6*len(lab)+4,y+10],fill=INK); T(d,(x+2,y),lab,FB(8),WH)
    y=268
    for ln in wrap(desc,FR(12),CW-28,d)[:2]: T(d,(14,y),ln,FR(12)); y+=17
    yy=y+10
    if not state.startswith('model'): T(d,(14,yy),state,FM(10),SUB); yy+=15
    T(d,(14,yy),model,FM(10),SUB)
    return im
def save_faces(name,faces):
    os.makedirs(OUT,exist_ok=True); uniq={}
    for k,v in faces.items(): uniq.setdefault(id(v),(k,v))
    if len({id(v) for v in faces.values()})==1: faces['top'].save(f'{OUT}/{name}.png'); return f'…/block/{name}.png'
    names=[]
    for k in ('front','side','top','bottom'):
        faces[k].save(f'{OUT}/{name}_{k}.png'); names.append(k)
    return f'…/block/{name}_{{front,side,top,bottom}}.png'
def sheet(fname,title,sub,items,strip=None):
    cols=2; gap=12; M0=28; top=96; nr=(len(items)+1)//2; sh=270 if strip else 0
    W=M0*2+cols*CW+gap; H=top+nr*(CH+gap)+sh+30
    im=Image.new('RGBA',(W,H),BG); d=ImageDraw.Draw(im); T(d,(M0,24),title,FB(30)); T(d,(M0,64),sub,FR(13),SUB)
    for i,(name,ttl,faces,desc,state) in enumerate(items):
        path=save_faces(name,faces)
        model='model: orientable' if 'facing' in state else ('model: cube_all' if path.endswith(f'{name}.png') else 'model: cube_bottom_top')
        im.alpha_composite(card(name,ttl,faces,desc,state,model+'   '+path),(M0+(i%2)*(CW+gap),top+(i//2)*(CH+gap)))
    if strip:
        y=top+nr*(CH+gap)+10; st,lst=strip; T(d,(M0,y),st,FB(18)); x=M0; y+=40
        box=Image.new('RGBA',(W-2*M0,215),WH); bd=ImageDraw.Draw(box); bd.rectangle([0,0,box.width-1,214],outline=BORDER); im.alpha_composite(box,(M0,y))
        step=(W-2*M0)//len(lst)
        for i,(name,lab,sub2,faces) in enumerate(lst):
            save_faces(name,faces); c=cube(faces['top'],faces['front'],faces['side'],s=5)
            cx=M0+i*step+(step-c.width)//2; im.alpha_composite(c,(cx,y+10))
            tw=d.textlength(lab,font=FB(12)); T(d,(M0+i*step+(step-tw)//2,y+176),lab,FB(12))
            tw=d.textlength(sub2,font=FR(10)); T(d,(M0+i*step+(step-tw)//2,y+194),sub2,FR(10),SUB)
    im.convert('RGB').save(fname)

tele=[('gate_controller','Gate Controller',K.controller(),'Directional: star-chart screen with a violet target on the front; void conduit on the sides; glowing core vent on top.','blockstate: facing (horizontal), formed'),
 ('gate_pad_plate','Gate Pad Plate',K.pad(),'Glowing void rings on top where players stand; violet trim on the sides. Rings light up when the pad zone is occupied.','blockstate: lit'),
 ('gate_pylon','Gate Pylon',K.pylon(),'Corner tower block; the violet segments light up one by one while the gate charges.','blockstate: charge=0..4'),
 ('gate_energy_port','Gate Energy Port',K.port(),'Cyan FE socket on every side; top and bottom are plain casing. Cables connect to any side.','blockstate: none (all sides accept FE)'),
 ('gate_lens_housing','Gate Lens Housing',K.lens(),'Sits on the arch; holds the Selenite focus crystal (front). Lens flares when a jump fires.','blockstate: facing, lens=empty|selenite'),
 ('crystal_cell','Crystal Cell',K.cell(),'Slow charger for the Landing Platform: glowing crystal rods behind glass on all sides.','blockstate: charge=0..3'),
 ('landing_platform','Landing Platform',K.landing(),'Generated on first arrival; landing ring on top, hazard stripes on the sides. Sends everyone on it home.','blockstate: lit'),
 ('nullifite_gate_frame','Nullifite Gate Frame (T1)',K.frame('nullifite',60),'Innermost frame ring. Each tier adds a ring of its own metal around it.','model: cube_all')]
tiers=[('nullifite_gate_frame','T1','Nullifite',K.frame('nullifite',60)),('moonsteel_gate_frame','T2','Moonsteel',K.frame('moonsteel',61)),
 ('cerulite_gate_frame','T3','Cerulite',K.frame('cerulite',62)),('skarnite_gate_frame','T4','Skarnite',K.frame('skarnite',63)),
 ('eidolite_gate_frame','T5','Eidolite',K.frame('eidolite',64)),('solvanite_gate_frame','T6','Solvanite',K.frame('solvanite',65))]
sheet('sheets/06_teleporter_blocks.png','Teleporter blocks  —  every face','Each block as a 3D view plus an unfolded cube (top · left · front · right · back · bottom). 16×16 per face at 4×. Violet and cyan pixels go on the emissive layer.',tele,('Frame rings by tier',tiers))
mach=[('combustion_generator','Combustion Generator',K.generator(),'Directional: firebox grille with glowing embers on the front; vent slats on top. Burns planet fuels.','blockstate: facing, lit'),
 ('solar_array','Solar Array',K.solar(),'Four blue cells on top; output depends on the world it sits on.','blockstate: none'),
 ('fusion_reactor','Fusion Reactor',K.fusion(),'Directional: white-hot ringed core on the front; copper coils on the sides. Fed with Fusion Dust.','blockstate: facing, active'),
 ('ore_refinery','Ore Refinery',K.refinery(),'Directional: crusher teeth window on the front; hopper mouth on top. Doubles ore output.','blockstate: facing, active'),
 ('alloy_forge','Alloy Forge',K.forge(),'Directional: crucible of molten metal on the front; chimney on top.','blockstate: facing, lit'),
 ('crystal_growth_chamber','Crystal Growth Chamber',K.growth(),'Directional: glass chamber with growing crystals on the front; crystals grow with progress.','blockstate: facing, stage=0..3'),
 ('salvage_station','Salvage Station',K.salvage(),'Directional: saw blade on the front; grille on top. Breaks wreck blocks into Salvium.','blockstate: facing, active')]
cas=[('cyrrium_casing','Tier 1','Cyrrium casing',K.casing_block('cyrrium',70)),('tectium_casing','Tier 2','Tectium casing',K.casing_block('tectium',71)),
 ('wraithsteel_casing','Tier 3','Wraithsteel casing',K.casing_block('wraithsteel',72)),('astrium_casing','Tier 4','Astrium casing',K.casing_block('astrium',73))]
sheet('sheets/07_machine_blocks.png','Machine blocks  —  every face','Each machine as a 3D view plus an unfolded cube. 16×16 per face at 4×. Casing tier sets speed and efficiency.',mach,('Machine casing tiers',cas))
with zipfile.ZipFile('zerog_tweaks_textures.zip','w') as z:
    for root,_,files in os.walk('out'):
        for f in files: z.write(os.path.join(root,f),os.path.relpath(os.path.join(root,f),'out'))
print(sum(len(f) for _,_,f in os.walk('out')))
