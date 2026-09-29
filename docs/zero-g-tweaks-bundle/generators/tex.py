import random
from PIL import Image

def hx(c):
    c=c.lstrip('#'); return tuple(int(c[i:i+2],16) for i in (0,2,4))+(255,)

T = {}
T['ingot']=["................","................","................","................","................",
"......oooooooo..","....oohhhhhhlmo.","..oohhllllllmmo.",".ohllllllllmmdo.",".ommlllllmmmddo.",
".odmmmmmmmmddo..",".oddddddddddo...","..oooooooooo....","................","................","................"]
T['nugget']=["................","................","................","................","................","................",
".......oooo.....","......ohhlmo....","...ooohllmdo....","..ohlmoomddooo..","..olmmdooooohlo.","..odmddo..olmdo.",
"...oooo...oddo..","...........oo...","................","................"]
T['raw']=["................","................","................","................","......oooo......","....oohhlmoo....",
"...ohhllmlmmo...","..ohllamllmmdo..","..olllmmlmmddo..",".oolmlmmaddmdoo.",".ohlmmdmmmddmddo",".olmmddmdddmddo.",
"..oddmddddddoo..","...ooodddooo....","......ooo.......","................"]
T['fuel']=["................","................","................",".......oooo.....",".....oolhlmoo...","....olllmmamdo..",
"...ollmmaamdddo.","..ollmmdmamddo..","..olmaddmmddddo.",".oolmmaaddmddo..",".olmdddmadddddo.",".oddmmddddaddo..",
"..odddddddddo...","...oooodddoo....",".......ooo......","................"]
T['dust']=["................","..h.........h...","........h.......","....h...........","...........h....",
".......oo.......","......ohlo......",".....ohllmo.....","....ohlhlmmo....","...ohllmlmmdo...","..ohllmhmlmddo..",
".ohllmmlmmmdddo.",".odmmdmmdmdmddo.",".oddddddddddddo.","..oooooooooooo..","................"]
T['orb']=["................","................",".....oooooo.....","....ohhlllmo....","...ohhllllmmo...",
"..ohhlllaallmo..","..ohllaallllmo..","..olllallmmmdo..","..ollllalammdo..","..olllllammmdo..",
"..omllllmmmddo..","...ommmmmmddo...","....ommmdddo....",".....oooooo.....","................","................"]
T['diamond']=["................","................","................","....oooooooo....","...ohhlhhllmo...",
"..ohhllhllmmdo..",".ohhlllhlmmmddo.",".oddddddddddddo.",".ohllllmmmmmddo.","..ohlllmmmmddo..",
"...ohllmmmddo...","....ohlmmddo....",".....ohmmdo.....","......ohdo......",".......oo.......","................"]
T['crystal']=["................","......oooo......",".....ohhlmo.....","....ohhllmmo....","....ohlllmmo....",
"....ohhllmdo....","....ohlllmdo....","....ohllmmdo....","....ohlllmdo....","....ohllmmdo....",
"....ohllmmdo....","....ohllmddo....","....oolmmddo....",".....olmmdo.....","......oooo......","................"]
for k,v in T.items():
    assert len(v)==16 and all(len(r)==16 for r in v),(k,[len(r) for r in v])

def item(tpl,pal,accent_emissive=False):
    im=Image.new('RGBA',(16,16),(0,0,0,0)); px=im.load()
    m={'o':pal[0],'d':pal[1],'m':pal[2],'l':pal[3],'h':pal[4],'a':pal[5]}
    for y,r in enumerate(T[tpl]):
        for x,c in enumerate(r):
            if c in m: px[x,y]=hx(m[c])
    return im

def stone(stp,seed):
    rnd=random.Random(seed); im=Image.new('RGBA',(16,16)); px=im.load()
    base=[[rnd.random() for _ in range(16)] for _ in range(16)]
    for y in range(16):
        for x in range(16):
            v=(base[y][x]*2+base[y][(x+1)%16]+base[(y+1)%16][x])/4
            i=min(3,int(v*4.4)); px[x,y]=hx(stp[i])
    # a few cracks
    for _ in range(3):
        x,y=rnd.randrange(16),rnd.randrange(16)
        for _ in range(rnd.randrange(2,5)):
            px[x%16,y%16]=hx(stp[0]); x+=rnd.choice([0,1]); y+=rnd.choice([0,1])
    return im

CL=[[(3,3),(4,3),(3,4),(4,4),(5,4)],[(10,2),(11,2),(11,3),(12,3)],[(2,10),(3,10),(3,11),(4,11),(3,12)],
    [(9,9),(10,9),(10,10),(11,10),(10,11),(12,11)],[(6,13),(7,13),(7,14)],[(13,13),(14,13)]]
def ore(stp,pal,seed):
    im=stone(stp,seed); px=im.load()
    for cl in CL:
        s=set(cl)
        for (x,y) in cl:
            for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                q=(x+dx,y+dy)
                if q not in s and 0<=q[0]<16 and 0<=q[1]<16: px[q]=hx(pal[0])
        for i,(x,y) in enumerate(cl):
            px[x,y]=hx([pal[4],pal[3],pal[2],pal[3],pal[2],pal[3]][i%6])
        x,y=cl[0]; px[x,y]=hx(pal[5])
    return im

def storage(pal,style,seed):
    rnd=random.Random(seed); im=Image.new('RGBA',(16,16)); px=im.load()
    for y in range(16):
        for x in range(16):
            if style=='metal':
                c=pal[3] if (x+y)%7 else pal[4]
                if y in (7,8): c=pal[2]
                if x in (7,8): c=pal[2]
            elif style=='gem':
                u,v=x%8,y%8
                c=pal[4] if u+v<5 else pal[3] if u+v<9 else pal[2] if u+v<12 else pal[1]
            else:
                r=rnd.random(); c=pal[1] if r<.25 else pal[2] if r<.65 else pal[3] if r<.9 else pal[4]
                if style=='fuel' and rnd.random()<.07: c=pal[5]
            px[x,y]=hx(c)
    for i in range(16):
        for q in [(i,0),(0,i)]: px[q]=hx(pal[4] if style!='grain' else pal[3])
        for q in [(i,15),(15,i)]: px[q]=hx(pal[0])
    if style=='metal':
        for q in [(2,2),(13,2),(2,13),(13,13)]: px[q]=hx(pal[5])
    return im
