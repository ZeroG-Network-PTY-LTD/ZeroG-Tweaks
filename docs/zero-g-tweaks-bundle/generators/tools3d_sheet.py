import sys; sys.argv=['x','/dev/null']; sys.path.insert(0,'/home/claude/zg')
import json, os
from PIL import Image, ImageDraw, ImageFont
import tools3d as T
S='/tmp/claude-0/-home-claude-zerog-tweaks/23345d11-2ce7-53a5-9128-b35ae672adbe/scratchpad'
F=lambda s,b=False: ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if b else ""}.ttf', s)
M=lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', s)
BG,INK,SUB,LINE,DARK=(245,244,240),(30,32,38),(96,100,112),(205,205,215),(30,32,40)
tex=Image.open(f'{S}/t3d/textures/item/3d/moonsteel_tools.png').convert('RGBA')
rows=[]
for k,name,_ in T.TOOLS:
    m=json.load(open(f'{S}/t3d/models/item/moonsteel_{k}.json'))
    rows.append((k,name,m,[T.render_model(m,tex,y,p,scale=s) for y,p,s in [(0,0,14),(-38,-22,20),(-80,-10,20)]]))
cw=[260,300,420,420]; W=40+sum(cw)+3*20+380+40
RH=440; Hh=150+len(rows)*(RH+20)+460
img=Image.new('RGB',(W,Hh),BG); d=ImageDraw.Draw(img)
d.text((40,24),'Moonsteel tools · 3D models (Draconic Evolution style)',font=F(38,True),fill=INK)
d.text((40,78),'Real 3D item models built from cubes instead of a flat sprite: layered steel, honed edges, cord-wrapped grips and glowing moon-blue inlays.',font=F(17),fill=SUB)
d.text((40,104),'Glowing parts are full-bright in game (NeoForge per-element light). The soft halo in these renders is for the sheet only; add a shader or emissive mod for real bloom.',font=F(17),fill=SUB)
heads=['Now (flat sprite)','Inventory (3D)','Angled (3/4 view)','Side (thickness)']
for i,(k,name,m,(gui,ang,side)) in enumerate(rows):
    y=150+i*(RH+20); x=40
    d.text((x,y),f'Moonsteel {name}',font=F(24,True),fill=INK)
    d.text((x,y+32),f'{len(m["elements"])} cubes · models/item/moonsteel_{k}.json',font=M(13),fill=SUB)
    for j,(c,label) in enumerate(zip(cw,heads)):
        bx=x+sum(cw[:j])+20*j; by=y+64
        d.rounded_rectangle((bx,by,bx+c,by+RH-70),12,fill=DARK)
        d.text((bx+12,by+10),label,font=F(13,True),fill=(200,206,220))
        if j==0:
            sp=Image.open(f'{S}/ms/items/moonsteel_{k}.png').convert('RGBA').resize((192,192),Image.NEAREST); im=sp
        else:
            im=[gui,ang,side][j-1].copy(); im.thumbnail((c-20,RH-110))
        img.paste(im,(bx+(c-im.width)//2,by+34+(RH-110-im.height)//2),im)
# right column: parts legend
lx=40+sum(cw)+3*20+20; ly=150
d.text((lx,ly),'Parts',font=F(22,True),fill=INK)
parts=[('light','Blade / head steel'),('mid','Body steel'),('dark','Hammer / poll steel'),('edge','Honed edges (brightest)'),('grip','Grip (dark wrap)'),('wrap','Moon-blue cord bands'),('socket','Collar / ferrule'),('plate','Riveted striking face'),('glow','Glowing inlay (full-bright)'),('gem','Moon gem (pommel / cap)'),('core','Moon core disc (full-bright)'),('trim','Dark trim band')]
for n,(mat,label) in enumerate(parts):
    u,v=T.region(mat); sw=tex.crop((u*4,v*4,u*4+16,v*4+16)).resize((40,40),Image.NEAREST)
    yy=ly+44+n*52; img.paste(sw,(lx,yy),sw); d.rectangle((lx,yy,lx+40,yy+40),outline=LINE)
    d.text((lx+52,yy+10),label,font=F(15),fill=INK)
d.text((lx,ly+44+len(parts)*52+16),'Texture (64 x 64)',font=F(18,True),fill=INK)
tt=tex.resize((256,256),Image.NEAREST); img.paste(tt,(lx,ly+44+len(parts)*52+46),tt); d.rectangle((lx,ly+44+len(parts)*52+46,lx+256,ly+44+len(parts)*52+302),outline=LINE)
# notes
ny=150+len(rows)*(RH+20)+10
d.text((40,ny),'How it works (for the Blockbench / code side)',font=F(24,True),fill=INK)
notes=['Each model is a normal Java item model with "elements" (parent minecraft:item/handheld), so it opens in Blockbench as-is: File > Open Model, then the .json.',
 'Every cube is rotated -45 degrees on Z around the centre, so the tool lies on the same diagonal as the old sprite and the vanilla hand, GUI and ground poses still fit.',
 'One shared 64 x 64 texture (textures/item/3d/moonsteel_tools.png) holds 12 material swatches; each face maps to a swatch, so other sets can reuse the models with a recoloured texture.',
 'Glowing cubes carry "neoforge_data": {"block_light": 15, "sky_light": 15} and "shade": false. Blockbench may drop the neoforge_data block when it saves, so re-add it after editing.',
 'To install: copy models/item/*.json over src/main/resources/assets/zerog_tweaks/models/item/ and the texture into textures/item/3d/. No Java changes needed.',
 'Want the flat sprite in the inventory but 3D in hand (like some DE items)? Wrap it with the NeoForge "neoforge:separate_transforms" loader, using the sprite for the gui perspective.']
for n,t in enumerate(notes):
    d.text((40,ny+44+n*30),'• '+t,font=F(16),fill=SUB)
img=img.crop((0,0,W,ny+44+len(notes)*30+30))
img.save(f'{S}/t3d/moonsteel_tools_3d_sheet.png'); print(img.size)
