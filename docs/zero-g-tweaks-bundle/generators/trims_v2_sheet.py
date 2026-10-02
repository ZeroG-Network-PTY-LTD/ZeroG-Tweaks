import sys; sys.path.insert(0,'/home/claude/zg')
from PIL import Image, ImageDraw, ImageFont
from render3d import Scene
S='/tmp/claude-0/-home-claude-zerog-tweaks/23345d11-2ce7-53a5-9128-b35ae672adbe/scratchpad/trimv2'
F=lambda s,b=False: ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if b else ""}.ttf', s)
KEY=[p[:3] for p in Image.open(f'{S}/pal/trim_palette.png').convert('RGBA').getdata()]
def recolor(im,pal):
    o=Image.new('RGBA',im.size); o.putdata([(pal[KEY.index(c[:3])]+(255,)) if c[3] and c[:3] in KEY else (0,0,0,0) for c in im.getdata()]); return o
def helm(armor,trim,mat,yaw,pitch):
    pal=[p[:3] for p in Image.open(f'{S}/pal/{mat}.png').convert('RGBA').getdata()]
    t=Image.open(f'{S}/armor/{armor}.png').convert('RGBA'); t.alpha_composite(recolor(Image.open(trim).convert('RGBA'),pal))
    s=Scene(yaw=yaw,pitch=pitch); s.solid((-3.5,0.5,-3.5),(7,7,7),(196,160,132))
    s.box_uv((-4,0,-4),(8,8,8),(0,0),t,inflate=0.5); return s.render(13,pad=8)
P=['fracture','crater','olympus','geode','rift','hull','corona','surge','prism','meteor']
NAMES={p:p.capitalize() for p in P}
BG,INK,SUB,LINE,CARD,DARK=(245,244,240),(30,32,38),(96,100,112),(205,205,215),(255,255,255),(34,36,44)
cw,ch=680,330; W=40+2*(cw+20)+20; Hh=150+5*(ch+20)+30
img=Image.new('RGB',(W,Hh),BG); d=ImageDraw.Draw(img)
d.text((40,26),'Trim patterns v2 · helmets',font=F(38,True),fill=INK)
d.text((40,80),'Before and after on the Moonsteel helmet in Solvanite. New rules: a feature on the crown, a frame around the face that keeps the visor clear,',font=F(17),fill=SUB)
d.text((40,104),'matching sides and back, and lines that continue across the edges between faces.',font=F(17),fill=SUB)
for i,p in enumerate(P):
    x=40+(i%2)*(cw+20); y=150+(i//2)*(ch+20)
    d.rounded_rectangle((x,y,x+cw,y+ch),12,fill=CARD,outline=LINE,width=2)
    d.text((x+16,y+12),NAMES[p],font=F(22,True),fill=INK)
    for j,(lab,tdir) in enumerate([('before','old'),('after','new')]):
        bx=x+16+j*330
        d.rounded_rectangle((bx,y+48,bx+318,y+ch-14),10,fill=DARK)
        d.text((bx+10,y+56),lab,font=F(13,True),fill=(200,206,220) if j==0 else (150,220,170))
        for k,(yw,pt) in enumerate([(-35,-28),(145,-28)]):
            im=helm('moonsteel',f'{S}/{tdir}/{p}.png','solvanite',yw,pt); im.thumbnail((150,230))
            img.paste(im,(bx+8+k*155+(150-im.width)//2,y+80+(230-im.height)//2),im)
img.save(f'{S}/helmets_v2.png'); print(img.size)
