"""Original deterministic vine pixel art; native vine geometry, no borrowed pack art."""
import argparse, json, random, zipfile
from pathlib import Path
from PIL import Image, ImageDraw

parser=argparse.ArgumentParser()
parser.add_argument('--code-root',required=True,type=Path)
args=parser.parse_args()
root=args.code_root
assets=root/'src/main/resources/assets/zerog_tweaks'
data=root/'src/main/resources/data'
source=Path(__file__).resolve().parent
palettes={'moon':((91,83,146),(185,172,234)), 'mars':((111,67,44),(236,156,87)),
          'cerulon':((29,91,90),(92,220,206)), 'skarn':((88,46,55),(239,123,85)),
          'eidolon':((55,105,139),(156,223,245)), 'solvane':((126,103,40),(249,213,99))}
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
def shade(colour,amount):return tuple(max(0,min(255,c+amount)) for c in colour)+(255,)
def texture(theme,kind,ripe=False):
    dark,light=palettes[theme]
    if kind=='venom_ivy':light=(159,233,114)
    image=Image.new('RGBA',(32,32));draw=ImageDraw.Draw(image)
    rng=random.Random(theme+'/'+kind)
    for strand in range(4):
        x=3+strand*8
        for y in range(32):
            xx=(x+(1 if (y//6)%2 else 0))%32
            draw.point((xx,y),fill=shade(dark,4));draw.point(((xx+1)%32,y),fill=shade(light,-35))
        for y in range(strand%3,32,5):
            side=-1 if (y//5)%2 else 1
            leafx=(x+side*3)%32
            draw.polygon([(x,y),(leafx,y-2),(leafx+side*2,y),(leafx,y+3)],fill=shade(dark,12))
            draw.line([(x,y),(leafx,y)],fill=shade(light,-18))
            draw.point((leafx,y-1),fill=shade(light,14))
            if kind in ('glow_ivy','venom_ivy'):
                draw.point(((x+2)%32,(y+3)%32),fill=shade(light,25))
            if kind=='fruit_ivy' and ripe and rng.random()<.7:
                bx=(x+side*3)%32;by=min(28,y+2)
                draw.rectangle((bx-1,by,bx+2,by+3),fill=shade(light,-25))
                draw.point((bx,by),fill=shade(light,40));draw.point((bx+2,by+3),fill=shade(dark,-15))
    return image
with zipfile.ZipFile(root/'build/moddev/artifacts/neoforge-21.1.252-client-extra-aka-minecraft-resources.jar') as jar:
    template=json.loads(jar.read('assets/minecraft/blockstates/vine.json'))
manifest=[];preview=Image.new('RGBA',(32*4,32*6),(22,28,36,255))
langpath=assets/'lang/en_us.json';lang=json.loads(langpath.read_text(encoding='utf-8'))
climb=[]
for row,theme in enumerate(palettes):
    for column,kind in enumerate(('ivy','glow_ivy','venom_ivy','fruit_ivy')):
        id=theme+'_'+kind;climb.append('zerog_tweaks:'+id)
        label=theme.title()+' '+kind.replace('_',' ').title();lang['block.zerog_tweaks.'+id]=label
        for ripe in ([False,True] if kind=='fruit_ivy' else [False]):
            textureid=id+('_ripe' if ripe else '')
            art=texture(theme,kind,ripe)
            for folder in (assets/'textures/block',source/'textures'):
                folder.mkdir(parents=True,exist_ok=True);art.save(folder/(textureid+'.png'))
            if kind!='fruit_ivy' or ripe:preview.alpha_composite(art,(column*32,row*32))
            model={'render_type':'minecraft:cutout','ambientocclusion':False,
                   'textures':{'particle':'zerog_tweaks:block/'+textureid,'vine':'zerog_tweaks:block/'+textureid},
                   'elements':[{'from':[0,0,.8],'to':[16,16,.8],'shade':False,'faces':{
                       'north':{'uv':[16,0,0,16],'texture':'#vine'},
                       'south':{'uv':[0,0,16,16],'texture':'#vine'}}}]}
            write(assets/'models/block'/(textureid+'.json'),model)
        multipart=[]
        for entry in template['multipart']:
            variants=[False,True] if kind=='fruit_ivy' else [None]
            for ripe in variants:
                new=json.loads(json.dumps(entry));modelid=id+('_ripe' if ripe else '')
                new['apply']['model']='zerog_tweaks:block/'+modelid
                if ripe is not None:new.setdefault('when',{})['berries']=str(ripe).lower()
                multipart.append(new)
        write(assets/'blockstates'/(id+'.json'),{'multipart':multipart})
        write(assets/'models/item'/(id+'.json'),{'parent':'minecraft:item/generated','textures':{'layer0':'zerog_tweaks:block/'+id}})
        write(data/'zerog_tweaks/loot_table/blocks'/(id+'.json'),{'type':'minecraft:block','pools':[{'rolls':1,'entries':[{'type':'minecraft:item','name':'zerog_tweaks:'+id}],
            'conditions':[{'condition':'minecraft:match_tool','predicate':{'items':'minecraft:shears'}}]}]})
        manifest.append({'id':id,'resolution':[32,32],'model':'native vine planes, no biome tint','visual_poison_only':kind=='venom_ivy'})
    fruit=theme+'_vine_fruit';lang['item.zerog_tweaks.'+fruit]=theme.title()+' Vine Fruit'
    image=Image.new('RGBA',(16,16));draw=ImageDraw.Draw(image);dark,light=palettes[theme]
    draw.polygon([(4,5),(8,3),(12,5),(13,10),(10,13),(6,13),(3,9)],fill=shade(dark,5))
    draw.polygon([(4,6),(8,4),(11,6),(11,10),(7,11),(4,9)],fill=shade(light,-10))
    draw.line((5,6,7,5),fill=shade(light,35));draw.line((8,3,9,1),fill=(84,133,79,255))
    (assets/'textures/item').mkdir(parents=True,exist_ok=True);image.save(assets/'textures/item'/(fruit+'.png'))
    image.save(source/'textures'/(fruit+'.png'))
    write(assets/'models/item'/(fruit+'.json'),{'parent':'minecraft:item/generated','textures':{'layer0':'zerog_tweaks:item/'+fruit}})
    vent=theme+'_ambient_vent';lang['block.zerog_tweaks.'+vent]=theme.title()+' Ambient Vent'
    write(assets/'blockstates'/(vent+'.json'),{'variants':{'':{'model':'zerog_tweaks:block/'+theme+'_gas_vent'}}})
    write(assets/'models/item'/(vent+'.json'),{'parent':'zerog_tweaks:block/'+theme+'_gas_vent'})
    write(data/'zerog_tweaks/loot_table/blocks'/(vent+'.json'),{'type':'minecraft:block','pools':[{'rolls':1,'entries':[{'type':'minecraft:item','name':'zerog_tweaks:'+vent}],'conditions':[{'condition':'minecraft:survives_explosion'}]}]})
lang['item.zerog_tweaks.weather_tester']='Planetary Weather Tester'
write(langpath,lang)
tagpath=data/'minecraft/tags/block/climbable.json'
existing=json.loads(tagpath.read_text(encoding='utf-8')).get('values',[]) if tagpath.exists() else []
write(tagpath,{'replace':False,'values':list(dict.fromkeys(['zerog_tweaks:pyrevine','zerog_tweaks:pyrevine_plant']+existing+climb))})
# Dedicated tag, do not overwrite existing shared mining tags.
write(data/'zerog_tweaks/tags/block/alien_vines.json',{'replace':False,'values':climb})
tagpath=data/'minecraft/tags/block/mineable/pickaxe.json'
existing=json.loads(tagpath.read_text(encoding='utf-8')).get('values',[]) if tagpath.exists() else []
write(tagpath,{'replace':False,'values':list(dict.fromkeys(existing+['zerog_tweaks:'+theme+'_ambient_vent' for theme in palettes]))})
preview.save(source/'vine-palette-preview.png')
write(source/'manifest.json',{'original_art':True,'deterministic_generator':'generate_assets.py','vines':manifest,'palette_row_order':list(palettes),'column_order':['ivy','glow_ivy','venom_ivy','fruit_ivy']})
print('Generated 24 vines, 6 fruits, 6 non-damaging vents and preview sheet.')
