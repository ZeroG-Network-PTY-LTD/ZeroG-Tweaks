import json, os, math
from PIL import Image, ImageDraw, ImageFont
NS='zerog_tweaks'; A=f'out/assets/{NS}'
def load(key):
    g=json.load(open(f'{A}/geckolib/models/entity/{key}.geo.json'))['minecraft:geometry'][0]
    tex=Image.open(f'{A}/textures/entity/{key}.png').convert('RGBA')
    cubes=[c for b in g['bones'] for c in b.get('cubes',[])]
    tw,th=g['description']['texture_width'],g['description']['texture_height']
    for c in cubes:
        u,v=c['uv']; w,h,d=[max(1,math.ceil(s)) for s in c['size']]
        assert u+2*(w+d)<=tw and v+d+h<=th,(key,c)
    return cubes,tex
def render(key,sc):
    cubes,tex=load(key); T=tex.load()
    xs=[c['origin'][0] for c in cubes]+[c['origin'][0]+c['size'][0] for c in cubes]
    ys=[c['origin'][1] for c in cubes]+[c['origin'][1]+c['size'][1] for c in cubes]
    zs=[c['origin'][2] for c in cubes]+[c['origin'][2]+c['size'][2] for c in cubes]
    w,h=sc*.866,sc*.5
    raw=lambda x,y,z:(x*w+z*w,x*h-z*h-y*sc)
    pts=[raw(x,y,z) for x in(min(xs),max(xs)) for y in(min(ys),max(ys)) for z in(min(zs),max(zs))]
    mx=min(p[0] for p in pts); my=min(p[1] for p in pts)
    W=int(max(p[0] for p in pts)-mx)+4; H=int(max(p[1] for p in pts)-my)+4
    P=lambda x,y,z:(raw(x,y,z)[0]-mx+2,raw(x,y,z)[1]-my+2)
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    order=sorted(cubes,key=lambda c:(c['origin'][0]+c['size'][0]/2)-(c['origin'][2]+c['size'][2]/2)+(c['origin'][1]+c['size'][1]/2)*.5)
    for c in order:
        (x0,y0,z0),(sw,sh,sd)=c['origin'],c['size']; u,v=c['uv']; W_,H_,D_=[max(1,math.ceil(s)) for s in (sw,sh,sd)]
        x1,y1,z1=x0+sw,y0+sh,z0+sd
        # top: region (u+D, v) W x D
        for iz in range(D_):
            for ix in range(W_):
                a=x0+sw*ix/W_; b=x0+sw*(ix+1)/W_; e=z0+sd*iz/D_; f=z0+sd*(iz+1)/D_
                d.polygon([P(a,y1,e),P(b,y1,e),P(b,y1,f),P(a,y1,f)],fill=T[u+D_+ix,v+iz])
        for iy in range(H_):
            for ix in range(W_):
                a=x0+sw*ix/W_; b=x0+sw*(ix+1)/W_; t=y1-sh*iy/H_; bt=y1-sh*(iy+1)/H_
                d.polygon([P(a,t,z0),P(b,t,z0),P(b,bt,z0),P(a,bt,z0)],fill=T[u+D_+ix,v+D_+iy])
            for iz in range(D_):
                e=z0+sd*iz/D_; f=z0+sd*(iz+1)/D_; t=y1-sh*iy/H_; bt=y1-sh*(iy+1)/H_
                c_=T[u+D_+W_+iz,v+D_+iy]; c_=(int(c_[0]*.8),int(c_[1]*.8),int(c_[2]*.8),c_[3])
                d.polygon([P(x1,t,e),P(x1,t,f),P(x1,bt,f),P(x1,bt,e)],fill=c_)
    return im
keys=[f[:-9] for f in sorted(os.listdir(f'{A}/geckolib/models/entity'))]
Fp='/usr/share/fonts/truetype/dejavu/'; FB=lambda s:ImageFont.truetype(Fp+'DejaVuSans-Bold.ttf',s); FR=lambda s:ImageFont.truetype(Fp+'DejaVuSans.ttf',s)
cols=7; cw,chh=220,250; W=28*2+cols*cw; rows=(len(keys)+cols-1)//cols; H=110+rows*chh
sheet=Image.new('RGBA',(W,H),(246,245,242,255)); d=ImageDraw.Draw(sheet)
d.text((28,22),'Mob models  —  geckolib geo.json + textures',font=FB(28),fill=(34,32,40))
d.text((28,60),'Rendered straight from the exported .geo.json files and their generated textures (box UV). Open any of them in Blockbench (Bedrock or GeckoLib entity).',font=FR(13),fill=(110,108,118))
for i,k in enumerate(keys):
    im=render(k,4); s=min(1,190/im.width,190/im.height)
    if s<1: im=im.resize((int(im.width*s),int(im.height*s)),Image.NEAREST)
    x=28+(i%cols)*cw; y=100+(i//cols)*chh
    d.rounded_rectangle([x,y,x+cw-12,y+chh-14],8,fill=(235,233,243))
    sheet.alpha_composite(im,(x+(cw-12-im.width)//2,y+(200-im.height)//2+6)); d.text((x+10,y+chh-40),k.replace('_',' ').title(),font=FB(12),fill=(34,32,40))
sheet.convert('RGB').save('sheets/28_mob_models.png'); print('ok',len(keys))
