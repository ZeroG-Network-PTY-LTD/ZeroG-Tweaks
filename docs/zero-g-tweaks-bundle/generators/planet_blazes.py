"""Original 128x64 cosmic palettes on vanilla BlazeModel's 64x32 logical UVs."""
import argparse,base64,hashlib,io,json,math,random,re,uuid
from pathlib import Path
from PIL import Image,ImageDraw
from crystals_v2 import embedded_project
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'docs/asset-collection-1.21.1/planet-blazes-v1'
HOMES={'void':'moon','nova':'solvane','nebula':'cerulon','void_c':'skarn','pulsar':'mars','comet':'eidolon'}
PALETTES={'void':[(9,10,27),(23,24,57),(64,50,122),(83,143,204)],'nova':[(51,26,13),(153,83,29),(239,188,74),(255,253,204)],'nebula':[(21,39,44),(60,102,116),(95,83,164),(95,206,139)],'void_c':[(18,24,27),(39,54,65),(26,106,142),(104,214,244)],'pulsar':[(31,55,74),(70,124,156),(213,169,74),(190,245,255)],'comet':[(68,109,146),(124,175,208),(194,229,244),(242,255,255)]}
HEAD={'north':[8,8,16,16],'east':[0,8,8,16],'west':[16,8,24,16],'south':[24,8,32,16],'up':[8,0,16,8],'down':[16,0,24,8]}
ROD={'north':[2,18,4,26],'east':[0,18,2,26],'west':[4,18,6,26],'south':[6,18,8,26],'up':[2,16,4,18],'down':[4,16,6,18]}
def tile(style,w,h,tone,rod=False):
    pal=PALETTES[style];im=Image.new('RGBA',(w,h));rng=random.Random(882+tone);variation=[.85,1,1.13][tone]
    for y in range(h):
        for x in range(w):
            nx=(x-w/2)/max(w/2,1);ny=(y-h/2)/max(h/2,1);r=math.hypot(nx,ny);a=math.atan2(ny,nx)
            value=(math.sin(x*.41+y*.31)+math.sin(x*.21-y*.63))/4+.5
            if style in ('void','void_c'):value=max(0,1-r)*(math.sin(a*2+r*7)+1)/2
            elif style=='nova':value=max(0,1-r)+(.15 if rng.random()>.96 else 0)
            elif style=='comet':value=round(value*4)/4
            c=pal[max(0,min(3,int(value*4)))];im.putpixel((x,y),tuple(min(255,round(v*variation)) for v in c)+(255,))
    d=ImageDraw.Draw(im)
    if style=='pulsar':
        d.rectangle((0,0,w-1,h-1),outline=pal[2],width=1);d.line((w//2,1,w//2,h-2),fill=pal[3]);d.line((1,h//2,w-2,h//2),fill=pal[3])
    if rod:
        d.line((1,1,1,h-2),fill=pal[3]);d.point((w-2,h//2),fill=pal[3])
    return im
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code-root',type=Path,required=True);a=p.parse_args();res=a.code_root/'src/main/resources';records=[];models=[]
    def write(relative,obj):
        for root in [res,OUT/'resource-source']:
            target=root/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(obj,indent=2)+'\n')
    def tex(path,im):
        target=OUT/'textures'/path;target.parent.mkdir(parents=True,exist_ok=True);im.save(target);dst=res/'assets/zerog_tweaks/textures'/path;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(target.read_bytes());records.append({'path':path,'size':list(im.size),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    lang=json.loads((res/'assets/zerog_tweaks/lang/en_us.json').read_text());lore=json.loads((ROOT/'docs/zero-g-tweaks-bundle/data-manifest.json').read_text())
    preview=Image.new('RGBA',(1200,1120),'#171d28');pd=ImageDraw.Draw(preview);pd.text((20,20),'Cosmic Blazes - vanilla geometry/AI; 128x64 painted source, three persistent palette variants',fill='white');pd.text((20,45),'Offline UV and rod reference, not GPU rendering; rods/eyes have emissive masks, no dynamic world light',fill='#aebad0')
    for index,(style,home) in enumerate(HOMES.items()):
        for tone in range(3):
            skin=Image.new('RGBA',(128,64))
            for part,uvs in [(False,HEAD),(True,ROD)]:
                for face,(x,y,x2,y2) in uvs.items():skin.alpha_composite(tile(style,(x2-x)*2,(y2-y)*2,tone,part),(x*2,y*2))
            d=ImageDraw.Draw(skin);eye=(102,12,30) if style=='void_c' else PALETTES[style][3]
            for x in [18,26]:d.rectangle((x,23,x+3,25),fill=eye+(255,))
            d.line((22,29,25,29),fill=(14,19,27,255))
            tex(f'entity/{style}_blaze_{tone}.png',skin)
            mask=Image.new('RGBA',skin.size)
            for yy in range(64):
                for xx in range(128):
                    colour=skin.getpixel((xx,yy))
                    if colour[3] and (max(colour[:3])>=195 or (style=='void_c' and colour[:3]==eye)):mask.putpixel((xx,yy),colour)
            tex(f'entity/{style}_blaze_{tone}_glowmask.png',mask)
            elements=[]
            def cube(name,start,end,uvs):
                identity=str(uuid.uuid5(uuid.NAMESPACE_URL,style+str(tone)+name));elements.append({'name':name,'uuid':identity,'from':start,'to':end,'faces':{f:{'uv':uv,'texture':0} for f,uv in uvs.items()}});return identity
            cube('head',[-4,20,-4],[4,28,4],HEAD)
            for n in range(12):
                if n<4:angle=n;radius=9;y=-2+math.cos(n*2*.25)
                elif n<8:angle=math.pi/4+n-4;radius=7;y=2+math.cos(n*2*.25)
                else:angle=.47123894+n-8;radius=5;y=11+math.cos(n*1.5*.5)
                x,z=math.cos(angle)*radius,math.sin(angle)*radius;cube('rod_'+str(n),[x,24-y-8,z],[x+2,24-y,z+2],ROD)
            buf=io.BytesIO();skin.save(buf,format='PNG');name=style+'_blaze_'+str(tone)
            obj={'meta':{'format_version':'4.10','model_format':'bedrock','box_uv':False},'name':name,'model_identifier':'geometry.'+name,'resolution':{'width':64,'height':32},'elements':elements,'outliner':[e['uuid'] for e in elements],'textures':[{'id':'0','name':name+'.png','uuid':str(uuid.uuid5(uuid.NAMESPACE_URL,name)),'source':'data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode(),'width':128,'height':64,'uv_width':64,'uv_height':32,'mode':'bitmap'}],'animations':[]}
            target=OUT/'blockbench'/(name+'.bbmodel');target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(obj,indent=2)+'\n');models.append(name)
            preview.alpha_composite(skin.resize((256,128),Image.Resampling.NEAREST),(210+tone*280,85+index*170))
        pd.text((20,110+index*170),style.replace('_',' ').title(),fill='white');pd.text((20,133+index*170),home,fill='#aebad0')
        rod=Image.new('RGBA',(32,32));rd=ImageDraw.Draw(rod);pal=PALETTES[style];rd.polygon([(5,25),(23,5),(27,7),(27,11),(9,29),(5,28)],fill=pal[0]);rd.line((7,26,25,7),fill=pal[2],width=4);rd.line((8,25,24,8),fill=pal[3],width=1);tex('item/'+style+'_blaze_rod.png',rod)
        preview.alpha_composite(rod.resize((96,96),Image.Resampling.NEAREST),(1070,100+index*170))
        write('assets/zerog_tweaks/models/item/'+style+'_blaze_rod.json',{'parent':'minecraft:item/generated','textures':{'layer0':'zerog_tweaks:item/'+style+'_blaze_rod'}})
        write('assets/zerog_tweaks/models/item/'+style+'_blaze_spawn_egg.json',{'parent':'minecraft:item/template_spawn_egg'})
        write('data/zerog_tweaks/loot_table/entities/'+style+'_blaze.json',{'type':'minecraft:entity','pools':[{'rolls':1,'entries':[{'type':'minecraft:item','name':'zerog_tweaks:'+style+'_blaze_rod','functions':[{'function':'minecraft:set_count','count':{'type':'minecraft:uniform','min':0,'max':1}},{'function':'minecraft:enchanted_count_increase','enchantment':'minecraft:looting','count':{'type':'minecraft:uniform','min':0,'max':1}}]}],'conditions':[{'condition':'minecraft:killed_by_player'}]}]})
        biomes=lore['planets'][home]['biomes'];write('data/zerog_tweaks/neoforge/biome_modifier/'+style+'_blaze_spawns.json',{'type':'neoforge:add_spawns','biomes':['zerog_tweaks:'+b for b in biomes],'spawners':[{'type':'zerog_tweaks:'+style+'_blaze','weight':2,'minCount':1,'maxCount':1}]})
        for namespace,suffix in [('entity',''),('item','_spawn_egg'),('item','_rod')]:lang[namespace+'.zerog_tweaks.'+style+'_blaze'+suffix]=(style+'_blaze'+suffix).replace('_',' ').title()
    (res/'assets/zerog_tweaks/lang/en_us.json').write_text(json.dumps(lang,ensure_ascii=False,indent=2)+'\n')
    tabs=a.code_root/'src/main/java/net/zerog/tweaks/registry/ZGCreativeTabContents.java';text=tabs.read_text()
    for section,suffix in [('SPAWN_EGGS','_blaze_spawn_egg'),('INGREDIENTS','_blaze_rod')]:
        def add(m):
            extra=[k+suffix for k in HOMES if '"'+k+suffix+'"' not in m.group(2)];return m.group(0) if not extra else m.group(1)+m.group(2).rstrip()+',\n            '+', '.join(json.dumps(i) for i in extra)+m.group(3)
        text=re.sub(r'(public static final String\[\] '+section+r' = \{)(.*?)(\n    \};)',add,text,flags=re.S)
    tabs.write_text(text);preview.convert('RGB').save(OUT/'planet_blazes_reference.png');(OUT/'manifest.json').write_text(json.dumps({'schema':1,'homes':HOMES,'textures':records,'projects':models,'client_verified':False,'animation':'vanilla BlazeModel runtime orbit; Blockbench projects are bind-pose UV studies'},indent=2)+'\n');print('6 species / 18 palettes / 42 PNGs / 18 editable vanilla-geometry projects')
if __name__=='__main__':main()
