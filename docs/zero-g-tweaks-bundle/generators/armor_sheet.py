import os, zipfile, random
from PIL import Image, ImageDraw, ImageFont
import armor3d as A
from gear_sets import S, HAND
from data import M, PL
from tex import hx
Fp='/usr/share/fonts/truetype/dejavu/'; FB=lambda s:ImageFont.truetype(Fp+'DejaVuSans-Bold.ttf',s); FR=lambda s:ImageFont.truetype(Fp+'DejaVuSans.ttf',s); FM=lambda s:ImageFont.truetype(Fp+'DejaVuSansMono.ttf',s)
BG=(246,245,242,255); INK=(34,32,40,255); SUB=(110,108,118,255); BORDER=(214,212,222,255); WH=(255,255,255,255); LINE=(124,92,220,255)
PERK={'nullifite':'Null Step: no fall damage','moonsteel':'Lunar Stride: 50% less fall damage','ferrox':'Sturdy: +1 armor toughness','olympium':'Dust Shield: storm and dust immunity',
'cobaltium':'Quick Hands: +10% mining speed','cyrrium':'Tempered: +20% durability','aurelion':'Silver Tongue: better alien trader prices','cerulite':'Crystal Sight: night vision; nearby ores glow',
'ruskite':'Heat Scale: 25% less fire damage','tectium':'Anchored: knockback resistance','pyrium':'Kindled: tools auto-smelt ores 20% of the time','skarnite':'Ember Walk: fire immunity; safe on Ember Crust and lava',
'salvium':'Scrapper: extra Salvium from wreck blocks','wraithsteel':'Chill Guard: slowness immunity','palladine':'Lucky: +1 Fortune and Looting','eidolite':'Phantom Veil: freeze immunity; invisible while sneaking',
'photium':'Glow: lights the area around the player','astrium':'Star Forged: +2 max health','radiantine':'Radiant: +20% damage to undead and Splinter creatures','solvanite':'Starborne: creative flight; immune to every planet hazard'}
STR={'nullifite':'Around diamond','moonsteel':'Between iron and diamond','ferrox':'Iron+','olympium':'Between diamond and netherite','cobaltium':'Around diamond, lower durability',
'cyrrium':'Around diamond','aurelion':'Gold-style: fast, enchantable, fragile','cerulite':'Around netherite','ruskite':'Diamond+','tectium':'Around netherite','pyrium':'Gold-style: fast, enchantable, fragile',
'skarnite':'Above netherite','salvium':'Around netherite','wraithsteel':'Above netherite','palladine':'Gold-style: fast, enchantable, fragile','eidolite':'High','photium':'High','astrium':'Near endgame',
'radiantine':'Gold-style: fast, enchantable, fragile','solvanite':'Endgame'}
TIER={'nullifite':'T1','olympium':'T2','cerulite':'T3','skarnite':'T4','eidolite':'T5','solvanite':'T6'}
PREV={'olympium':'Nullifite','cerulite':'Olympium','skarnite':'Cerulite','eidolite':'Skarnite','solvanite':'Eidolite'}
WORLD={'nullifite':'Sol (Overworld)','moonsteel':'Sol (Moon)','ferrox':'Sol (Mars)','olympium':'Sol (Mars)'}
for pk,(pn,gal,_,lst) in PL.items():
    for x in lst: WORLD[x[0]]=f'{pn} ({gal})'
MOTIF={'cracks':'void cracks (emissive)','rivets':'rivets','facets':'crystal facets','rust':'rust flecks','frost':'frosted top edges','flame':'ember flecks (emissive)',
'filigree':'gold filigree','stars':'star pixels (emissive)','glow_edge':'glowing lower edges (emissive)','inlay':'gem inlay'}
def mat_item(k):
    r=M[k]['role']; return f"{M[k]['name']} {'Ingot' if r=='metal' else ''}".strip()
# ---------- descriptions from params
def desc(piece,P):
    if piece=='sword':
        span=P.get('w',(14,16)); n=span[1]-span[0]+1
        w={2:'Slim',3:'Standard',4:'Broad'}.get(n,'Great') if n>=2 else 'Slim'
        bits=[w+(' curved' if P.get('curve') else '')+(' wavy' if P.get('wave') else '')+' blade']
        bits.append({'point':'pointed tip','long':'long tapered tip','clipped':'clipped tip'}[P.get('tip','point')])
        if P.get('serrate'): bits.append(('one' if P['serrate']=='one' else 'both')+' edge serrated')
        if P.get('spikes'): bits.append('crystal spikes')
        if P.get('fuller'): bits.append('glowing fuller')
        bits.append({'bar':'bar guard','crescent':'crescent guard','wings':'winged guard','disc':'disc guard','sun':'sun guard','horns':'horned guard','block':'block guard'}[P.get('guard','bar')])
        return '; '.join(bits)+'.'
    if piece=='pickaxe':
        return ('Hammer-backed' if P.get('ends')=='hammer' else 'Double-pointed')+(' spiked' if P.get('spikes') else '')+(' long' if P.get('L',7)>=8 else '')+' pick head.'
    if piece=='axe': return {'std':'Classic axe head.','double':'Double-bit head.','crescent':'Crescent head.','cleaver':'Heavy cleaver head.','bearded':'Bearded head.'}[P.get('type','std')][:-1]+(' with a spike.' if P.get('spike') else '.')
    if piece=='shovel': return {'round':'Round','point':'Pointed','square':'Square','spade':'Shouldered spade'}[P.get('type','round')]+' blade.'
    if piece=='hoe': return {'bar':'Straight blade','hook':'Hooked blade','scythe':'Scythe blade','fork':'Forked tines'}[P.get('type','bar')]+(' with a back spike.' if P.get('back') else '.')
    if piece=='helmet':
        v={'slit':'glowing visor slit','glass':'glass visor','nose':'nose guard','mask':'full mask'}.get(P.get('visor'),'open face')
        return ', '.join([v]+[{'crest':'crest','horns':'horns','fins':'side fins','crown':'crown points','brim':'brim','wings':'side wings','hood':'hood','band':'accent band','halo':'halo'}[a] for a in P.get('add',[])]).capitalize()+'.'
    if piece=='chestplate':
        n={'round':'Round neck','v':'V-neck','collar':'High collar'}[P.get('neck','round')]
        return ', '.join([n]+[{'pauldron':'pauldrons','spikes':'shoulder spikes','belt':'belt','core':'core gem','ribs':'ribbed plates','wings':'back wings','waist':'tapered waist'}[a] for a in P.get('add',[])])+'.'
    if piece=='leggings':
        a=[{'knee':'knee plates','flare':'flared cuffs','fin':'hip fins','tasset':'tassets','belt':'belt','stripe':'side stripes'}[x] for x in P.get('add',[])]
        return ('Plated legs with '+', '.join(a) if a else 'Plain plated legs')+'.'
    if piece=='boots':
        a=[{'cuff':'cuffs','sole':'heavy soles','spike':'toe spikes','wing':'ankle wings','strap':'straps','heel':'heel fins'}[x] for x in P.get('add',[])]
        return ('Boots with '+', '.join(a) if a else 'Plain boots')+'.'
# ---------- figure rendering
S_=13
def face_img(L,part,f,mirror=False):
    x,y,w,h=A.faces(part)[f]; im=L.crop((x,y,x+w,y+h))
    return im.transpose(Image.FLIP_LEFT_RIGHT) if mirror else im
BASE=['#3a3a42','#5c5c66','#74747e','#8e8e98']
def mannequin(front):
    im=Image.new('RGBA',(16,32),(0,0,0,0)); d=ImageDraw.Draw(im)
    for (x0,y0,x1,y1) in [(4,0,11,7),(4,8,11,19),(0,8,3,19),(12,8,15,19),(4,20,7,31),(8,20,11,31)]:
        d.rectangle([x0,y0,x1,y1],fill=hx(BASE[2]),outline=hx(BASE[1]))
    if front: d.point([(6,4),(9,4)],fill=hx(BASE[0])); d.line([(6,6),(9,6)],fill=hx(BASE[1]))
    return im
def paste(canvas,img,x0,y0,x1,y1,ox,oy):
    W=round((x1-x0)*S_); H=round((y1-y0)*S_)
    canvas.alpha_composite(img.resize((W,H),Image.NEAREST),(ox+round(x0*S_),oy+round(y0*S_)))
def box(d,ox,oy,x0,y0,x1,y1,c,o='#101014'):
    d.rectangle([ox+x0*S_,oy+y0*S_,ox+x1*S_-1,oy+y1*S_-1],fill=hx(c),outline=hx(o))
def figure(k,cfg,L1,L2,front):
    pal=M[k]['pal']; acc=cfg['acc']; ox,oy=5*S_,5*S_
    cv=Image.new('RGBA',(26*S_,40*S_),(0,0,0,0)); d=ImageDraw.Draw(cv)
    cv.alpha_composite(mannequin(front).resize((16*S_,32*S_),Image.NEAREST),(ox,oy))
    f='front' if front else 'back'
    B=cfg['chestplate'].get('add',[]); H=cfg['helmet'].get('add',[]); G=cfg['leggings'].get('add',[]); Bt=cfg['boots'].get('add',[])
    if not front and 'wings' in B:
        for i,(x0,y0,x1,y1) in enumerate([(-3,9,3,11),(-4,11,2,13),(-3,13,3,15),(13,9,19,11),(14,11,20,13),(13,13,19,15)]): box(d,ox,oy,x0,y0,x1,y1,'#eef4fb','#8a96a8')
    # leggings
    paste(cv,face_img(L2,'body',f),3.5,7.5,12.5,20.5,ox,oy)
    for i,xs in enumerate([(3.5,8),(8,12.5)]):
        paste(cv,face_img(L2,'leg',f,mirror=(i==1)==front),xs[0],19.5,xs[1],32.5,ox,oy)
    for i,xs in enumerate([(3,8),(8,13)]):
        paste(cv,face_img(L1,'leg',f,mirror=(i==1)==front),xs[0],19,xs[1],33,ox,oy)
    paste(cv,face_img(L1,'body',f),3,7,13,21,ox,oy)
    for i,xs in enumerate([(-1,4),(12,17)]):
        paste(cv,face_img(L1,'arm',f,mirror=(i==1)==front),xs[0],7,xs[1],21,ox,oy)
    if 'pauldron' in B:
        box(d,ox,oy,-1.5,6,4.5,9,pal[3],pal[0]); box(d,ox,oy,11.5,6,17.5,9,pal[3],pal[0])
        box(d,ox,oy,-1.5,8,4.5,9,acc[1],pal[0]); box(d,ox,oy,11.5,8,17.5,9,acc[1],pal[0])
    if 'spikes' in B:
        for x in (0,2,13,15): box(d,ox,oy,x,4.5,x+1,6,acc[3],pal[0])
    paste(cv,face_img(L1,'head',f),3,-1,13,9,ox,oy)
    if 'crest' in H: box(d,ox,oy,7.4,-3.5,8.6,-1,pal[4],pal[0])
    if 'horns' in H:
        for (x,y) in [(2,0),(1,-1),(1,-2),(2,-3)]: box(d,ox,oy,x,y,x+1,y+1,HAND['bone'][3],HAND['bone'][0]); box(d,ox,oy,15-x,y,16-x,y+1,HAND['bone'][3],HAND['bone'][0])
    if 'fins' in H: box(d,ox,oy,1.8,1,3,5,acc[2],pal[0]); box(d,ox,oy,13,1,14.2,5,acc[2],pal[0])
    if 'wings' in H:
        for (x,y) in [(2,2),(1,1),(0,0),(0,-1)]: box(d,ox,oy,x,y,x+1,y+1,'#f4f8ff','#8a96a8'); box(d,ox,oy,15-x,y,16-x,y+1,'#f4f8ff','#8a96a8')
    if 'crown' in H:
        for x in (4,6.5,9,11.5): box(d,ox,oy,x,-2.2,x+.8,-1,acc[3],pal[0])
    if 'halo' in H: box(d,ox,oy,4,-4.5,12,-3.8,acc[2],acc[0])
    if 'hood' in H: box(d,ox,oy,6.5,-2.5,9.5,-1,pal[1],pal[0]); box(d,ox,oy,7.4,-3.5,8.6,-2.5,pal[1],pal[0])
    if 'fin' in G: box(d,ox,oy,2.2,21,3.2,24,acc[2],pal[0]); box(d,ox,oy,12.8,21,13.8,24,acc[2],pal[0])
    if 'wing' in Bt: box(d,ox,oy,1.8,27,3,29,'#f4f8ff','#8a96a8'); box(d,ox,oy,13,27,14.2,29,'#f4f8ff','#8a96a8')
    if 'spike' in Bt and front: box(d,ox,oy,5,32.4,6,33.2,acc[3],pal[0]); box(d,ox,oy,10,32.4,11,33.2,acc[3],pal[0])
    if 'heel' in Bt and not front: box(d,ox,oy,5,30,6,32,pal[3],pal[0]); box(d,ox,oy,10,30,11,32,pal[3],pal[0])
    return cv,(ox,oy)
def callouts(k,cfg,front):
    H=cfg['helmet']; C=cfg['chestplate']; G=cfg['leggings']; B=cfg['boots']; out=[]
    v={'slit':'Glowing visor slit','glass':'Glass visor','nose':'Nose guard','mask':'Full mask, glowing eyes'}.get(H.get('visor'),'Open face')
    if front: out.append((v,(8,4)))
    names={'crest':('Crest (3D)',(8,-2.5)),'horns':('Horns (3D)',(1.5,-1.5)),'fins':('Side fins (3D)',(2.4,3)),'crown':('Crown points (3D)',(11.8,-1.6)),
           'halo':('Halo (3D)',(8,-4.2)),'hood':('Hood peak (3D)',(8,-2.5)),'wings':('Helmet wings (3D)',(0.5,0)),'band':('Accent band',(12,2)),'brim':('Brim',(3.5,4))}
    for a in H.get('add',[]):
        if a in names: out.append(names[a])
    if front:
        out.append(({'round':'Round neckline','v':'V-neck','collar':'High collar'}[C.get('neck','round')],(8,7.5)))
    cn={'pauldron':('Pauldrons (3D)',(1.5,7)),'spikes':('Shoulder spikes (3D)',(14.5,5)),'core':('Core gem (emissive)',(8,12)),'ribs':('Ribbed plates',(6,14)),
        'belt':('Belt',(8,18.5)),'waist':('Tapered waist',(3.5,17)),'wings':('Back wings (3D)',(-2,12))}
    for a in C.get('add',[]):
        if a in cn and (front or a in('pauldron','spikes','wings')): 
            if a=='wings' and front: continue
            out.append(cn[a])
    gn={'knee':('Knee plates',(6,24.5)),'stripe':('Side stripes',(4,26)),'fin':('Hip fins (3D)',(2.7,22)),'tasset':('Tassets',(10,21)),'flare':('Flared cuffs',(4,29)),'belt':('Leggings belt',(8,19))}
    for a in G.get('add',[]):
        if a in gn and (front or a in('fin','tasset')): out.append(gn[a])
    bn={'cuff':('Boot cuffs',(10,28)),'sole':('Heavy soles',(6,32.5)),'strap':('Straps',(10,30)),'spike':('Toe spikes',(10.5,32.8)),'wing':('Ankle wings (3D)',(13.6,28)),'heel':('Heel fins (3D)',(10.5,31))}
    for a in B.get('add',[]):
        if a in bn and (front or a in('heel','wing','cuff')): 
            if a=='spike' and not front: continue
            if a=='heel' and front: continue
            out.append(bn[a])
    if cfg['motif']: out.append(('Surface: '+', '.join(MOTIF[m] for m in cfg['motif']),(6.5,11) if front else (9.5,11)))
    if not front: out.append(('Spine ridge',(8,15)))
    return out
def panel(k,cfg,L1,L2,front):
    W,H=760,640; im=Image.new('RGBA',(W,H),WH); d=ImageDraw.Draw(im); d.rectangle([0,0,W-1,H-1],outline=BORDER)
    d.text((16,14),'FRONT  (looking at its face)' if front else 'BACK  (from behind)',font=FB(14),fill=INK); d.text((W-170,16),'same scale in all views',font=FR(10),fill=SUB)
    fig,(ox,oy)=figure(k,cfg,L1,L2,front); fx=(W-fig.width)//2; fy=42
    gx0,gy0=fx+ox-2*S_,fy+oy-5*S_
    for i in range(0,21): d.line([gx0+i*S_,gy0,gx0+i*S_,gy0+39*S_],fill=(236,236,242,255))
    for j in range(0,40): d.line([gx0,gy0+j*S_,gx0+20*S_,gy0+j*S_],fill=(236,236,242,255))
    im.alpha_composite(fig,(fx,fy))
    gy=fy+oy+33*S_; d.line([gx0-10,gy,gx0+20*S_+10,gy],fill=(90,90,100,255)); d.text((gx0+20*S_+14,gy-7),'ground',font=FR(10),fill=SUB)
    rx=gx0-18; d.line([rx,fy+oy-S_,rx,gy],fill=INK); d.line([rx-4,fy+oy-S_,rx+4,fy+oy-S_],fill=INK); d.line([rx-4,gy,rx+4,gy],fill=INK)
    d.text((rx-30,gy+6),'34 px (2.1 bl)',font=FR(10),fill=INK)
    co=callouts(k,cfg,front); left=[c for c in co if c[1][0]<8]; right=[c for c in co if c[1][0]>=8]
    def place(lst,side):
        lst=sorted(lst,key=lambda c:c[1][1]); lasty=-99
        for lab,(tx,ty) in lst:
            px_=fx+ox+tx*S_; py_=fy+oy+ty*S_; ly=max(py_,lasty+22); lasty=ly
            if side=='L':
                lw=d.textlength(lab,font=FR(11)); x_text=14; d.text((x_text,ly-7),lab,font=FR(11),fill=INK)
                d.line([x_text+lw+4,ly,px_,py_],fill=LINE)
            else:
                x_text=W-14-d.textlength(lab,font=FR(11)); d.text((x_text,ly-7),lab,font=FR(11),fill=INK); d.line([px_,py_,x_text-4,ly],fill=LINE)
            d.ellipse([px_-3,py_-3,px_+3,py_+3],fill=LINE)
    place(left,'L'); place(right,'R')
    d.text((16,H-20),'horizontal: X    vertical: Y up    3D = extra geometry (GeckoLib armor model); the rest is painted on the layer',font=FR(10),fill=SUB)
    return im
def checker(n,c=8):
    im=Image.new('RGBA',(n,n),(250,250,252,255)); d=ImageDraw.Draw(im)
    for y in range(0,n,c):
        for x in range(0,n,c):
            if (x//c+y//c)%2: d.rectangle([x,y,x+c-1,y+c-1],fill=(238,236,244,255))
    return im
def wrap(s,f,w,d):
    out=[];line=''
    for word in s.split():
        t=(line+' '+word).strip()
        if d.textlength(t,font=f)>w: out.append(line); line=word
        else: line=t
    return out+[line]
PIECES=['sword','pickaxe','axe','shovel','hoe','helmet','chestplate','leggings','boots']
TYPE={'sword':'Weapon · sword','pickaxe':'Tool · pickaxe','axe':'Tool · axe','shovel':'Tool · shovel','hoe':'Tool · hoe','helmet':'Armor · helmet','chestplate':'Armor · chestplate','leggings':'Armor · leggings','boots':'Armor · boots'}
os.makedirs('sheets/armor',exist_ok=True)
for i,(k,cfg) in enumerate(S.items()):
    pal=M[k]['pal']; acc=cfg['acc']; L1,L2=A.build_layers(k,cfg,pal,acc,i*17); name=M[k]['name']
    W=1596; H=2000; im=Image.new('RGBA',(W,H),BG); d=ImageDraw.Draw(im)
    d.text((28,22),f'{name} — armor and gear set',font=FB(30),fill=INK)
    tier=TIER.get(k); role='gem set' if tier else M[k]['role']+' set'
    d.text((28,64),f"{WORLD[k]} · {(tier+' ' if tier else '')}{role} · strength: {STR[k]} · {'upgraded at the smithing table from '+PREV[k] if k in PREV else 'crafted from '+mat_item(k)+'s'}",font=FR(13),fill=SUB)
    cw=(W-56-8*8)//9
    for j,pc in enumerate(PIECES):
        x=28+j*(cw+8); y=100; d.rectangle([x,y,x+cw,y+300],fill=WH,outline=BORDER)
        ic=Image.open(f'out/assets/zerog_tweaks/textures/item/{k}_{pc}.png').convert('RGBA')
        c=checker(112); c.alpha_composite(ic.resize((112,112),Image.NEAREST)); im.alpha_composite(c,(x+10,y+10))
        for s_,(dx,dy) in zip((1,2),((126,20),(126,44))):
            cc=checker(16*s_,2); cc.alpha_composite(ic.resize((16*s_,16*s_),Image.NEAREST)); im.alpha_composite(cc,(x+dx,y+dy))
        d.text((x+10,y+130),f'{name} {pc.capitalize()}',font=FB(11),fill=INK); d.text((x+10,y+147),TYPE[pc],font=FR(10),fill=SUB)
        d.text((x+10,y+162),f'zerog_tweaks:{k}_{pc}',font=FM(8),fill=SUB)
        yy=y+182
        for ln in wrap(desc(pc,cfg[pc]),FR(10),cw-18,d)[:6]: d.text((x+10,yy),ln,font=FR(10),fill=INK); yy+=14
    im.alpha_composite(panel(k,cfg,L1,L2,True),(28,420)); im.alpha_composite(panel(k,cfg,L1,L2,False),(28+760+20,420))
    y=1080; d.text((28,y),'Set bonus and stats',font=FB(17),fill=INK); y+=32
    rows=[('Strength',STR[k]),('Full-set perk',PERK[k]),('Repair',mat_item(k)),('Mining tier','Can mine this world\'s rare gem' if not tier else f'{tier} set; mines the next planet\'s rare gem'),
          ('Made by','Smithing table: '+PREV[k]+' piece + '+mat_item(k)+' + tier template' if k in PREV else 'Crafting table, vanilla patterns with '+mat_item(k)+'s')]
    for a,b in rows:
        d.text((28,y),a,font=FB(12),fill=INK)
        for ln in wrap(b,FR(12),520,d): d.text((200,y),ln,font=FR(12),fill=INK); y+=18
        y+=8
    y2=1080; x2=820; d.text((x2,y2),'Notes for the artist and code',font=FB(17),fill=INK); y2+=32
    extras=[t for t,_ in callouts(k,cfg,True)+callouts(k,cfg,False) if '(3D)' in t]
    notes=[f'Worn textures: models/armor/{k}_layer_1.png (helmet, chestplate, boots) and {k}_layer_2.png (leggings), vanilla 64×32 layout.',
           'Painted on the layer: visor, neckline, belts, knee plates, cuffs, straps and the surface pattern.',
           ('3D extras need a GeckoLib armor model: '+', '.join(sorted(set(e.replace(' (3D)','') for e in extras)))+'. Without GeckoLib they fall back to the painted version.') if extras else 'No 3D extras; works with the vanilla armor model.',
           'Glowing pixels (accent colors) go on an emissive layer.']
    for n_ in notes:
        for ln in wrap(n_,FR(12),740,d): d.text((x2,y2),ln,font=FR(12),fill=INK); y2+=18
        y2+=8
    y2+=6; d.text((x2,y2),'Layer textures (3×)',font=FB(12),fill=INK); y2+=20
    for j,Lx in enumerate((L1,L2)):
        c=Image.new('RGBA',(192,96),(250,250,252,255)); c.alpha_composite(Lx.resize((192,96),Image.NEAREST)); im.alpha_composite(c,(x2+j*210,y2)); d.rectangle([x2+j*210,y2,x2+j*210+191,y2+95],outline=BORDER)
        d.text((x2+j*210,y2+100),f'layer_{j+1}',font=FM(10),fill=SUB)
    y=max(y,y2+130)+10
    sw=[('dark',pal[1]),('mid',pal[2]),('light',pal[3]),('highlight',pal[4]),('outline',pal[0]),('accent',acc[2]),('accent hi',acc[3]),('handle',HAND[cfg['hand']][2])]
    for j,(n_,c) in enumerate(sw):
        x=28+j*190; d.rectangle([x,y,x+32,y+32],fill=hx(c),outline=(120,120,120,255)); d.text((x+40,y+2),n_,font=FR(11),fill=INK); d.text((x+40,y+17),c,font=FM(10),fill=SUB)
    im=im.crop((0,0,W,y+56)); im.convert('RGB').save(f'sheets/armor/{i+1:02d}_{k}_armor.png')
with zipfile.ZipFile('zerog_tweaks_resources.zip','w') as z:
    for root,_,files in os.walk('out'):
        for f in files: z.write(os.path.join(root,f),os.path.relpath(os.path.join(root,f),'out'))
print('done')
