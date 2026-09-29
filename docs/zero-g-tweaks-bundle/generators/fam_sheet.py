import pickle, os, zipfile
from PIL import Image, ImageDraw, ImageFont
Fp='/usr/share/fonts/truetype/dejavu/'; FB=lambda s:ImageFont.truetype(Fp+'DejaVuSans-Bold.ttf',s); FR=lambda s:ImageFont.truetype(Fp+'DejaVuSans.ttf',s); FM=lambda s:ImageFont.truetype(Fp+'DejaVuSansMono.ttf',s)
BG=(246,245,242,255); INK=(34,32,40,255); SUB=(110,108,118,255); BORDER=(214,212,222,255); PANEL=(235,233,243,255); WH=(255,255,255,255)
TX='out/assets/zerog_tweaks/textures/block'
def L(n): return Image.open(f'{TX}/{n}.png').convert('RGBA')
def sh(c,f): return (int(c[0]*f),int(c[1]*f),int(c[2]*f),c[3])
def render(boxes,tex,s=4,side=None):
    w,h=s*.866,s*.5; W=int(32*w)+4; H=int(32*h+16*s)+4; im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    O=(W/2,2); P=lambda x,y,z:(O[0]+x*w-z*w,O[1]+x*h+z*h+(16-y)*s)
    tp=tex.load(); sp=(side or tex).load()
    for (x0,y0,z0,x1,y1,z1) in boxes:
        for z in range(z0,z1):
            for x in range(x0,x1):
                d.polygon([P(x,y1,z),P(x+1,y1,z),P(x+1,y1,z+1),P(x,y1,z+1)],fill=sh(tp[x,z],1))
        for y in range(y0,y1):
            for x in range(x0,x1):
                c=sp[x,15-y]
                if c[3]: d.polygon([P(x,y+1,z1),P(x+1,y+1,z1),P(x+1,y,z1),P(x,y,z1)],fill=sh(c,.84))
            for z in range(z0,z1):
                c=sp[15-z,15-y]
                if c[3]: d.polygon([P(x1,y+1,z+1),P(x1,y+1,z),P(x1,y,z),P(x1,y,z+1)],fill=sh(c,.66))
    return im
CUBE=[(0,0,0,16,16,16)]; STAIR=[(0,0,0,16,8,16),(0,8,0,16,16,8)]; SLAB=[(0,0,0,16,8,16)]
WALL=[(0,0,5,4,14,11),(4,0,4,12,16,12),(12,0,5,16,14,11)]
F=pickle.load(open('fams.pkl','rb')); GL=pickle.load(open('glass.pkl','rb'))
SHORT=['Base','Cobbled','Smooth','Polished','Bricks','Cracked bricks','Chiseled','Polished black','Black bricks','Chiseled black']
def sheet(fname,title,sub,keys,extra=None):
    M0=28; CW=112; RH=230; W=M0*2+10*CW+3*CW+40; H=110+len(keys)*RH+(330 if extra else 0)
    im=Image.new('RGBA',(W,H),BG); d=ImageDraw.Draw(im)
    d.text((M0,24),title,font=FB(30),fill=INK); d.text((M0,64),sub,font=FR(13),fill=SUB)
    y=100
    for k in keys:
        name,full,names,shapes,tint=F[k]
        d.rounded_rectangle([M0,y,W-M0,y+RH-12],6,fill=WH,outline=BORDER)
        d.text((M0+12,y+10),name+' family',font=FB(15),fill=INK)
        d.text((M0+12+d.textlength(name+' family',font=FB(15))+10,y+13),f'{len(full)} blocks · {len(shapes)*3} stairs, slabs and walls'+(' · grayscale, tinted in game' if tint else ''),font=FR(11),fill=SUB)
        for i,(b,lab) in enumerate(zip(full,SHORT)):
            x=M0+12+i*CW; c=render(CUBE,L(b),s=3.4); im.alpha_composite(c,(x+(CW-c.width)//2-6,y+40))
            im.alpha_composite(L(b).resize((32,32),Image.NEAREST),(x+30,y+150))
            tw=d.textlength(lab,font=FR(10)); d.text((x+(CW-tw)//2-6,y+188),lab,font=FR(10),fill=INK)
        xs=M0+12+10*CW+20; d.line([xs-12,y+40,xs-12,y+200],fill=BORDER)
        br=L(f'{k}_bricks')
        for j,(bx,lab) in enumerate([(STAIR,'Stairs'),(SLAB,'Slab'),(WALL,'Wall')]):
            c=render(bx,br,s=3.4); x=xs+j*CW; im.alpha_composite(c,(x+(CW-c.width)//2-6,y+40))
            tw=d.textlength(lab,font=FR(10)); d.text((x+(CW-tw)//2-6,y+188),lab,font=FR(10),fill=INK)
        d.text((xs,y+206),'shown in bricks; all 10 variants get stairs, a slab and a wall',font=FR(9),fill=SUB)
        y+=RH
    if extra:
        d.text((M0,y+6),'Smelted glass and wood shapes',font=FB(18),fill=INK); y+=40
        d.rounded_rectangle([M0,y,W-M0,y+270],6,fill=WH,outline=BORDER)
        for i,(id,nm,src,_,_) in enumerate(GL):
            x=M0+12+i*CW*1.2; c=render(CUBE,L(id),s=3.4); im.alpha_composite(c,(int(x)+(CW-c.width)//2,y+14))
            d.text((int(x)+8,y+120),nm,font=FB(10),fill=INK); d.text((int(x)+8,y+134),'from '+src.replace('_',' '),font=FR(9),fill=SUB)
        for i,w in enumerate(['shardwood','charwood','hoarwood','gildwood']):
            pl=L(f'{w}_planks')
            for j,(bx,lab) in enumerate([(STAIR,'stairs'),(SLAB,'slab')]):
                x=M0+12+(i*2+j)*CW*1.05; c=render(bx,pl,s=3); im.alpha_composite(c,(int(x),y+160))
                d.text((int(x)+6,y+248),f'{w} {lab}',font=FR(9),fill=INK)
    im.convert('RGB').save(fname)
pk=['lunar_stone','mare_basalt','martian_stone','cerulean_stone','skarn_rock','scorched_marble','permafrost','solar_stone']
wk=[k for k in F if k not in pk]
sheet('sheets/20_stone_families_planets.png','Stone families  —  planet stones','Every stone gets cobbled, smooth (smelted), polished, bricks, cracked bricks (smelted), chiseled and a polished black line (8 polished + 1 Nullifite nugget). Every variant gets stairs, a slab and a wall.',pk)
sheet('sheets/21_stone_families_wastelands.png','Stone families  —  wasteland stones','Same family set in grayscale; the game tints each galaxy. Plus smelted glass from every sand and stairs and slabs for the four woods.',wk,extra=True)
with zipfile.ZipFile('zerog_tweaks_textures.zip','w') as z:
    for root,_,files in os.walk('out'):
        for f in files: z.write(os.path.join(root,f),os.path.relpath(os.path.join(root,f),'out'))
