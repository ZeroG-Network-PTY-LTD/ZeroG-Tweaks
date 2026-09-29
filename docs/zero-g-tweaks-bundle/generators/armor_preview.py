import json, os, math
from PIL import Image, ImageDraw, ImageFont
from gear_sets import S
from data import M
A='out/assets/zerog_tweaks'
def render(k,sc=7,front=True):
    g=json.load(open(f'{A}/geckolib/models/item/armor/{k}.geo.json'))['minecraft:geometry'][0]
    T=Image.open(f'{A}/textures/item/armor/{k}.png').convert('RGBA').load()
    cubes=[c for b in g['bones'] for c in b.get('cubes',[])]
    def box(c):
        (x0,y0,z0),(sw,sh,sd)=c['origin'],c['size']; i=c.get('inflate',0)
        return x0-i,y0-i,z0-i,sw+2*i,sh+2*i,sd+2*i
    X0,X1,Y1=-12,12,38
    im=Image.new('RGBA',((X1-X0)*sc,(Y1+2)*sc),(0,0,0,0)); d=ImageDraw.Draw(im)
    key=(lambda c:-(box(c)[2]+box(c)[5])) if front else (lambda c:(box(c)[2]))
    for c in sorted(cubes,key=key):
        x0,y0,z0,sw,sh,sd=box(c); u,v=c['uv']; Wd,Hd,Dd=[max(1,math.ceil(s_)) for s_ in c['size']]; mir=c.get('mirror',False)
        fu=u+Dd if front else u+2*Dd+Wd
        for iy in range(Hd):
            for ix in range(Wd):
                col=T[fu+ix,v+Dd+iy]
                if col[3]<20: continue
                # front view: viewer's left is the model's +x (entity faces the viewer)
                j=ix if not mir else Wd-1-ix
                if front: xa=x0+sw*(1-j/Wd); xb=x0+sw*(1-(j+1)/Wd)
                else: xa=x0+sw*j/Wd; xb=x0+sw*(j+1)/Wd
                sx0=( -xa if front else xa)-X0; sx1=( -xb if front else xb)-X0
                ya=Y1-(y0+sh*(1-iy/Hd)); yb=Y1-(y0+sh*(1-(iy+1)/Hd))
                d.rectangle([min(sx0,sx1)*sc,ya*sc,max(sx0,sx1)*sc-1,yb*sc-1],fill=col)
    return im.crop(im.getbbox())
Fp='/usr/share/fonts/truetype/dejavu/'; FB=lambda s:ImageFont.truetype(Fp+'DejaVuSans-Bold.ttf',s); FR=lambda s:ImageFont.truetype(Fp+'DejaVuSans.ttf',s)
keys=list(S); cols=5; cw,ch=300,330; W=56+cols*cw; H=110+((len(keys)+cols-1)//cols)*ch
sh=Image.new('RGBA',(W,H),(246,245,242,255)); d=ImageDraw.Draw(sh)
d.text((28,22),'GeckoLib armor models  —  3D extras included',font=FB(28),fill=(34,32,40))
d.text((28,60),'Rendered from each set’s .geo.json and texture: the base armor boxes use the worn layers, extras (horns, crests, halos, pauldrons, wings, fins, spikes) are real geometry.',font=FR(13),fill=(110,108,118))
for i,k in enumerate(keys):
    f=render(k,6,True); bk=render(k,6,False)
    x=28+(i%cols)*cw; y=100+(i//cols)*ch; d.rounded_rectangle([x,y,x+cw-14,y+ch-14],8,fill=(235,233,243))
    sh.alpha_composite(f,(x+8+(135-f.width)//2,y+14+(260-f.height))); sh.alpha_composite(bk,(x+143+(135-bk.width)//2,y+14+(260-bk.height)))
    d.text((x+12,y+ch-42),M[k]['name'],font=FB(13),fill=(34,32,40)); d.text((x+150,y+ch-40),'front \u00b7 back',font=FR(10),fill=(110,108,118))
sh.convert('RGB').save('sheets/29_armor_models.png'); print('ok')
