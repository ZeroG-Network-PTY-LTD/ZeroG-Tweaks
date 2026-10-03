"""Use the actual vanilla water-bucket base plus an original liquid-only overlay.

Reads installed Minecraft pixels only to locate blue liquid pixels. No Mojang
base PNG is copied to Design or runtime: item layer0 references minecraft:item/water_bucket.
"""
import argparse,hashlib,io,json
from pathlib import Path
from zipfile import ZipFile
from PIL import Image,ImageDraw
from planet_bees import FAMILIES,STYLES
from dimension_ecology import FLUIDS
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'docs/asset-collection-1.21.1/vanilla-liquid-buckets-v1'
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code-root',type=Path,required=True);a=p.parse_args();res=a.code_root/'src/main/resources'
    jars=list((a.code_root/'build/moddev/artifacts').glob('*client-extra*resources.jar'));assert len(jars)==1,'Build Minecraft resources first'
    with ZipFile(jars[0]) as z:
        source=Image.open(io.BytesIO(z.read('assets/minecraft/textures/item/water_bucket.png'))).convert('RGBA')
        empty=Image.open(io.BytesIO(z.read('assets/minecraft/textures/item/bucket.png'))).convert('RGBA')
    colours={key:tuple(bytes.fromhex(row[0][2])) for key,row in FLUIDS.items()};colours['liquid_starlight']=(125,224,246)
    colours.update({key+'_honey':STYLES[style][2] for key,style in FAMILIES.items()});records=[]
    preview=Image.new('RGBA',(1080,690),'#171d28');draw=ImageDraw.Draw(preview)
    draw.text((20,18),'Actual vanilla water-bucket base + ZeroG liquid overlay: all 18 filled buckets',fill='white')
    draw.text((20,40),'Offline preview composites reference installed Minecraft art; no standalone Mojang base texture is bundled',fill='#aebad0')
    for index,(key,base) in enumerate(colours.items()):
        overlay=Image.new('RGBA',source.size);count=0
        for y in range(source.height):
            for x in range(source.width):
                r,g,b,alpha=source.getpixel((x,y))
                if alpha and source.getpixel((x,y))!=empty.getpixel((x,y)):
                    factor=.55+.55*b/255
                    overlay.putpixel((x,y),tuple(min(255,round(c*factor)) for c in base)+(255,));count+=1
        assert count>8,'Missing liquid mask'
        name=key+'_bucket';relative='assets/zerog_tweaks/textures/item/'+name+'.png'
        for root in [res,OUT/'resource-source']:
            target=root/relative;target.parent.mkdir(parents=True,exist_ok=True);overlay.save(target)
            model=root/'assets/zerog_tweaks/models/item'/(name+'.json');model.parent.mkdir(parents=True,exist_ok=True)
            model.write_text(json.dumps({'parent':'minecraft:item/generated','textures':{'layer0':'minecraft:item/water_bucket','layer1':'zerog_tweaks:item/'+name}},indent=2)+'\n')
        target=OUT/'textures/item'/(name+'.png');target.parent.mkdir(parents=True,exist_ok=True);overlay.save(target)
        records.append({'path':'item/'+name+'.png','size':list(overlay.size),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'liquid_pixels':count})
        composed=source.copy();composed.alpha_composite(overlay)
        for y in range(source.height):
            for x in range(source.width):
                if source.getpixel((x,y))==empty.getpixel((x,y)):assert composed.getpixel((x,y))==source.getpixel((x,y)),'Metal body changed'
        x=20+(index%6)*175;y=80+(index//6)*200
        preview.alpha_composite(composed.resize((128,128),Image.Resampling.NEAREST),(x,y));draw.text((x,y+140),key,fill='white')
    preview.convert('RGB').save(OUT/'vanilla_bucket_reference.png')
    (OUT/'manifest.json').write_text(json.dumps({'schema':1,'base':'minecraft:item/water_bucket','mojang_png_copied':False,'textures':records},indent=2)+'\n')
    print(f'{len(records)} original liquid overlays; exact vanilla water-bucket base retained by resource reference')
if __name__=='__main__':main()
