import os, json, math
from PIL import Image, ImageDraw
from gear_sets import S, HAND
from data import M
from tex import hx
NS='zerog_tweaks'; A=f'out/assets/{NS}'
GEO=f'{A}/geckolib/models/item/armor'; ANI=f'{A}/geckolib/animations/item/armor'; TEX=f'{A}/textures/item/armor'
for p in (GEO,ANI,TEX): os.makedirs(p,exist_ok=True)
def mirror(o,s): return [-(o[0]+s[0]),o[1],o[2]]
def extras(cfg,pal,acc):
    H=cfg['helmet'].get('add',[]); C=cfg['chestplate'].get('add',[]); G=cfg['leggings'].get('add',[]); B=cfg['boots'].get('add',[])
    bone_ivory=HAND['bone'][3]; white='#f4f8ff'
    out=[]  # (bone_right, bone_left or None, origin(right side or centered), size, color, glow)
    def pair(bR,bL,o,s,c,g=False): out.append((bR,o,s,c,g)); out.append((bL,mirror(o,s),s,c,g))
    def one(b,o,s,c,g=False): out.append((b,o,s,c,g))
    if 'crest' in H: one('armorHead',[-0.5,33,-4.5],[1,3,9],pal[4])
    if 'horns' in H:
        for o in ([-6.5,31,-1],[-7.5,32,-1],[-7.5,33,-1],[-6.5,34,-1]): pair('armorHead','armorHead',o,[1,1,1],bone_ivory)
    if 'fins' in H: pair('armorHead','armorHead',[-6,26,-3],[1,4,5],acc[2],True)
    if 'wings' in H:
        for o in ([-6,28,0],[-7,29,0],[-8,30,0],[-8,31,0]): pair('armorHead','armorHead',o,[1,1,3],white)
    if 'crown' in H:
        for x in (-3.5,-1.25,1,3.25): one('armorHead',[x,33,-4.6],[0.8,1.4,0.8],acc[3],True); one('armorHead',[x,33,3.8],[0.8,1.4,0.8],acc[3],True)
    if 'halo' in H:
        for o,s in (([-4.5,35.5,-4.5],[9,0.6,0.6]),([-4.5,35.5,3.9],[9,0.6,0.6]),([-4.5,35.5,-4.5],[0.6,0.6,9]),([3.9,35.5,-4.5],[0.6,0.6,9])): one('armorHead',o,s,acc[2],True)
    if 'hood' in H: one('armorHead',[-1.5,33,-1.5],[3,1.5,3],pal[1]); one('armorHead',[-0.5,34.5,-0.5],[1,1,1],pal[1])
    if 'pauldron' in C: pair('armorRightArm','armorLeftArm',[-9.5,21,-3],[6,3,6],pal[3])
    if 'spikes' in C:
        for x in (-8,-6): pair('armorRightArm','armorLeftArm',[x,24,-0.5],[1,1.5,1],acc[3])
    if 'wings' in C:
        for o,s in (([-9,19,2.5],[6,1.5,1]),([-10,17,2.5],[7,1.5,1]),([-9,15,2.5],[6,1.5,1])): pair('armorBody','armorBody',o,s,white)
    if 'fin' in G: pair('armorRightLeg','armorLeftLeg',[-5.4,7,-0.5],[1,3,1],acc[2],True)
    if 'wing' in B: pair('armorRightBoot','armorLeftBoot',[-5.4,2,-0.5],[1,2,2],white)
    if 'spike' in B: pair('armorRightBoot','armorLeftBoot',[-2.5,0,-4],[1,1,1],acc[3],True)
    if 'heel' in B: pair('armorRightBoot','armorLeftBoot',[-2.5,1,2.5],[1,2,1],pal[3])
    return out
def shade(c,f): t=hx(c); return (min(255,int(t[0]*f)),min(255,int(t[1]*f)),min(255,int(t[2]*f)),255)
def build(k,cfg):
    pal=M[k]['pal']; acc=cfg['acc']
    L1=Image.open(f'{A}/textures/models/armor/{k}_layer_1.png').convert('RGBA'); L2=Image.open(f'{A}/textures/models/armor/{k}_layer_2.png').convert('RGBA')
    tex=Image.new('RGBA',(128,64),(0,0,0,0)); tex.paste(L1,(0,0)); tex.paste(L2,(0,32)); glow=Image.new('RGBA',(128,64),(0,0,0,0))
    tp=tex.load(); gp=glow.load()
    X=[e for e in extras(cfg,pal,acc)]
    x=64; y=0; rowh=0; cubes={}
    for (bone,o,s,c,g) in X:
        w,h,d=[max(1,math.ceil(v)) for v in s]; fw,fh=2*(w+d),d+h
        if x+fw>128: x=64; y+=rowh; rowh=0
        assert y+fh<=64,(k,'texture overflow')
        u,v=x,y; x+=fw; rowh=max(rowh,fh)
        for (x0,y0,ww,hh,f) in [(u+d,v,w,d,1.15),(u+d+w,v,w,d,.7),(u,v+d,d,h,.85),(u+d,v+d,w,h,1.0),(u+d+w,v+d,d,h,.85),(u+2*d+w,v+d,w,h,.8)]:
            for yy in range(hh):
                for xx in range(ww):
                    col=shade(c,f*(1.1 if yy==0 else .9 if yy==hh-1 else 1.0)); tp[x0+xx,y0+yy]=col
                    if g: gp[x0+xx,y0+yy]=col
        cubes.setdefault(bone,[]).append({'origin':[round(v,3) for v in o],'size':s,'uv':[u,v]})
    base={'armorHead':([0,24,0],[{'origin':[-4,24,-4],'size':[8,8,8],'uv':[0,0],'inflate':1.0}]),
          'armorBody':([0,24,0],[{'origin':[-4,12,-2],'size':[8,12,4],'uv':[16,16],'inflate':1.01}]),
          'armorRightArm':([-5,22,0],[{'origin':[-8,12,-2],'size':[4,12,4],'uv':[40,16],'inflate':1.0}]),
          'armorLeftArm':([5,22,0],[{'origin':[4,12,-2],'size':[4,12,4],'uv':[40,16],'inflate':1.0,'mirror':True}]),
          'armorRightLeg':([-1.9,12,0],[{'origin':[-3.9,0,-2],'size':[4,12,4],'uv':[0,48],'inflate':0.5}]),
          'armorLeftLeg':([1.9,12,0],[{'origin':[-0.1,0,-2],'size':[4,12,4],'uv':[0,48],'inflate':0.5,'mirror':True}]),
          'armorRightBoot':([-1.9,12,0],[{'origin':[-3.9,0,-2],'size':[4,12,4],'uv':[0,16],'inflate':1.0}]),
          'armorLeftBoot':([1.9,12,0],[{'origin':[-0.1,0,-2],'size':[4,12,4],'uv':[0,16],'inflate':1.0,'mirror':True}])}
    parent={'armorRightLeg':None,'armorLeftLeg':None}
    bones=[{'name':'bipedHead','pivot':[0,24,0]},{'name':'bipedBody','pivot':[0,24,0]},{'name':'bipedRightArm','pivot':[-5,22,0]},{'name':'bipedLeftArm','pivot':[5,22,0]},
           {'name':'bipedRightLeg','pivot':[-1.9,12,0]},{'name':'bipedLeftLeg','pivot':[1.9,12,0]}]
    par={'armorHead':'bipedHead','armorBody':'bipedBody','armorRightArm':'bipedRightArm','armorLeftArm':'bipedLeftArm','armorRightLeg':'bipedRightLeg','armorLeftLeg':'bipedLeftLeg','armorRightBoot':'bipedRightLeg','armorLeftBoot':'bipedLeftLeg'}
    for b,(pv,cs) in base.items(): bones.append({'name':b,'parent':par[b],'pivot':pv,'cubes':cs+cubes.get(b,[])})
    geo={'format_version':'1.12.0','minecraft:geometry':[{'description':{'identifier':f'geometry.{NS}.armor.{k}','texture_width':128,'texture_height':64,'visible_bounds_width':3,'visible_bounds_height':3,'visible_bounds_offset':[0,1.5,0]},'bones':bones}]}
    json.dump(geo,open(f'{GEO}/{k}.geo.json','w'),indent=1); tex.save(f'{TEX}/{k}.png')
    if glow.getbbox(): glow.save(f'{TEX}/{k}_glowmask.png')
    json.dump({'format_version':'1.8.0','animations':{}},open(f'{ANI}/{k}.animation.json','w'))
    return len(X)
for k,cfg in S.items(): print(k,build(k,cfg),'extra cubes')
