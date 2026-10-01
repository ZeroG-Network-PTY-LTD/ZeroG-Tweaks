import math
from PIL import Image
TB='out/assets/zerog_tweaks/textures/block'
def lum(c): return .3*c[0]+.59*c[1]+.11*c[2]
def pal_of(im):
    cols=sorted({im.getpixel((x,y))[:3] for x in range(16) for y in range(16)},key=lum)
    n=len(cols); return [cols[0],cols[n//3],cols[(2*n)//3],cols[-1]]
def ramp(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)+(255,)
for w in ['shardwood','charwood','hoarwood','gildwood']:
    log=Image.open(f'{TB}/{w}_log.png').convert('RGBA'); top=Image.open(f'{TB}/{w}_log_top.png').convert('RGBA'); pl=Image.open(f'{TB}/{w}_planks.png').convert('RGBA')
    P=pal_of(pl); base=P[2]
    # side: keep the log's vertical grain, recolored into the inner-wood palette
    lp=sorted({log.getpixel((x,y))[:3] for x in range(16) for y in range(16)},key=lum); rank={c:i/(max(1,len(lp)-1)) for i,c in enumerate(lp)}
    s=Image.new('RGBA',(16,16)); px=s.load()
    for y in range(16):
        for x in range(16):
            t=rank[log.getpixel((x,y))[:3]]
            px[x,y]=ramp(base,.72+ .5*t) if x%4 else ramp(base,.78)
    s.save(f'{TB}/stripped_{w}_log.png')
    # top: growth rings across the whole face, no bark
    t_=Image.new('RGBA',(16,16)); q=t_.load()
    for y in range(16):
        for x in range(16):
            d=math.hypot(x-7.5,y-7.5)
            q[x,y]=ramp(base,.8) if d>7.2 else (ramp(base,1.12) if int(d)%2 else ramp(base,.93))
    t_.save(f'{TB}/stripped_{w}_log_top.png')
print('ok')
