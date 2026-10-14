"""Source occupancy projection. Not Minecraft/GPU rendering or texture approval."""
import argparse,gzip,json,struct,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from showcase_augment_lib import read_nbt

def main():
 p=argparse.ArgumentParser();p.add_argument('--templates',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 names=['ice_spire_outpost','water_bio_habitat','hot_ring_monolith']
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
 colors={'minecraft:air':None,'minecraft:purpur_block':(166,113,175),'minecraft:packed_ice':(137,188,228),'minecraft:blue_ice':(104,151,208),'minecraft:snow_block':(227,238,246),'minecraft:dark_prismarine':(51,98,88),'minecraft:prismarine':(108,166,148),'minecraft:glass':(165,216,237),'minecraft:sea_lantern':(182,231,222),'minecraft:shroomlight':(255,165,77),'minecraft:obsidian':(34,26,45),'minecraft:crying_obsidian':(58,31,89),'minecraft:red_nether_bricks':(89,30,34),'minecraft:blackstone':(42,40,49),'minecraft:gold_block':(243,195,68),'minecraft:chest':(169,112,51),'minecraft:spawner':(42,59,72),'minecraft:crimson_nylium':(120,27,37),'minecraft:lava':(235,94,20),'minecraft:magma_block':(164,66,25)}
 sheet=Image.new('RGB',(2700,1700),(16,23,35))
 for column,name in enumerate(names):
  s=read_nbt(a.templates/(name+'.nbt'));pal=[v['Name'] for v in s['palette']]
  for row,cut in enumerate([False,True]):
   cells={tuple(v['pos']):pal[v['state']] for v in s['blocks'] if pal[v['state']]!='minecraft:air' and (not cut or v['pos'][2]>=24)}
   im=Image.new('RGB',(900,850),(16,23,35));d=ImageDraw.Draw(im)
   def point(x,y,z):return (140+(x+z)*6,600+(x-z)*3-y*6)
   for (x,y,z),block in sorted(cells.items(),key=lambda e:(e[0][0]+e[0][1]-e[0][2],e[0])):
    c=colors.get(block,(113,119,140))
    if block.startswith('zerog_tweaks:'):
     if 'cerulean' in block:c=(73,153,157)
     if 'skarn' in block:c=(58,43,48)
     if 'soil' in block:c=(61,83,77) if 'cerulon' in block else (97,64,56) if 'skarn' in block else (91,110,122)
     if 'grass_block' in block:c=(75,124,111) if 'cerulon' in block else (121,64,52) if 'skarn' in block else (162,192,202)
     if any(w in block for w in ['frost','ice','cryo','brine']):c=(129,192,215)
     elif any(w in block for w in ['ember','oxide','basalt']):c=(144,55,44)
     elif any(w in block for w in ['prism','cluster']):c=(140,110,191)
     elif any(w in block for w in ['coral','kelp','azure','tide']):c=(87,165,143)
     elif 'lamp' in block:c=(127,235,225)
     if 'polished_black' in block:c=tuple(int(v*.42) for v in c)
     if 'cracked_' in block:c=tuple(int(v*.72) for v in c)
     if 'glow_' in block:c=(106,211,174) if 'cerulon' in block else (238,134,74) if 'skarn' in block else (153,222,240)
    faces=[((x,y+1,z),[(x,y+1,z),(x+1,y+1,z),(x+1,y+1,z+1),(x,y+1,z+1)],1),((x+1,y,z),[(x+1,y,z),(x+1,y+1,z),(x+1,y+1,z+1),(x+1,y,z+1)],.65),((x,y,z-1),[(x,y,z),(x+1,y,z),(x+1,y+1,z),(x,y+1,z)],.82)]
    for neighbour,pts,f in faces:
     if neighbour in cells:continue
     shade=tuple(int(v*f) for v in c);d.polygon([point(*v) for v in pts],fill=shade,outline=tuple(int(v*.72) for v in shade))
   d.text((24,20),name.replace('_',' ').title(),font=font,fill='#e7f2ff');d.text((24,56),'Cutaway: front half removed' if cut else 'Revision candidate · actual voxel exterior',font=small,fill='#96cee0')
   dims=' × '.join(map(str,s['size']))
   d.text((24,750),dims+' · flat representative colours',font=small,fill='#cad5e4');d.text((24,783),'Schematic preview. Client visual review pending.',font=small,fill='#a2acbc')
   sheet.paste(im,(column*900,row*850))
 a.output.parent.mkdir(parents=True,exist_ok=True);sheet.save(a.output);print(a.output)
if __name__=='__main__':main()
