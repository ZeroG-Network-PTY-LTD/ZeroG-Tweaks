"""Render authored food/material silhouettes with 64px detail and BB projects.

Original symbolic masks and color roles are retained. Sub-pixel shading,
material grain and edge highlights are drawn at the target resolution.
"""
import base64
import hashlib
import io
import json
import uuid
from pathlib import Path
from PIL import Image
from food_data import F, MAT, REW, MASK

ROOT=Path(__file__).resolve().parents[3]
ASSETS=ROOT/"src/main/resources/assets/zerog_tweaks"
PROJECTS=ROOT/"docs/zero-g-tweaks-bundle/blockbench/mob_drops"
REWARD_IDS={"star_map_fragment","heatproof_plating","cryo_core","neutralizer","stardust",
            "rust_shell","crystal_hide","cinder_pelt","frost_pelt","burrower_scale","solar_spark",
            "colossus_core","sentinel_prism","rift_heart","captains_lantern","heart_of_solvane",
            "galaxy_3_gate_key","galaxy_4_gate_key","galaxy_5_gate_key"}

def rgba(value):
    return (*bytes.fromhex(value.removeprefix("#")),255)

def render(item):
    rows=(MASK[item["mask"]]+[""]*16)[:16]
    pixels={(x,y):c for y,row in enumerate(rows) for x,c in enumerate(row[:16]) if c!="."}
    scale=4
    image=Image.new("RGBA",(64,64),(0,0,0,0))
    grill=item["G"]=="GRILL"
    colors={c:rgba(item[c] if c!="G" or not grill else item["H"]) for c in "HGAW"}
    seed=int(hashlib.sha256(item["k"].encode()).hexdigest()[:8],16)
    for x,y in pixels:
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            if (x+dx,y+dy) in pixels:continue
            for s in range(scale):
                px=x*scale+(scale if dx==1 else -1 if dx==-1 else s)
                py=y*scale+(scale if dy==1 else -1 if dy==-1 else s)
                if 0<=px<64 and 0<=py<64:
                    image.putpixel((px,py),tuple(int(v*.3) for v in colors[pixels[(x,y)]][:3])+(255,))
    for (x,y),role in pixels.items():
        base=colors[role]
        for sy in range(scale):
            for sx in range(scale):
                px,py=x*scale+sx,y*scale+sy
                edge_up=pixels.get((x,y-1))!=role and sy<2
                edge_left=pixels.get((x-1,y))!=role and sx<2
                edge_down=pixels.get((x,y+1))!=role and sy>=2
                edge_right=pixels.get((x+1,y))!=role and sx>=2
                value=1.0+.13*edge_up+.1*edge_left-.14*edge_down-.1*edge_right+(28-py)/450
                grain=((px*17+py*31+seed)%11-5)*.007
                if item["mask"] in ("hide","fluff","skin"):
                    grain+=.04 if (px//2+py//5)%5==0 else -.01
                if grill and role=="H" and (px+py)%16 in (0,1):value*=.65
                image.putpixel((px,py),tuple(max(0,min(255,round(c*(value+grain)))) for c in base[:3])+(255,))
    if item["mask"]=="fish":
        for y in range(20,23):
            for x in range(12,15):image.putpixel((x,y),(12,27,36,255))
    return image

def bbmodel(item,image):
    key=item["k"]
    cube_id=str(uuid.uuid5(uuid.NAMESPACE_URL,f"zerog_tweaks/item/{key}"))
    data=io.BytesIO();image.save(data,format="PNG")
    return {"meta":{"format_version":"4.10","model_format":"java_block","box_uv":False},
            "name":key,"model_identifier":f"zerog_tweaks:{key}","resolution":{"width":64,"height":64},
            "elements":[{"name":key,"type":"cube","uuid":cube_id,"from":[0,0,7.99],"to":[16,16,8.01],
                         "origin":[8,8,8],"box_uv":False,"faces":{
                             "north":{"uv":[0,0,64,64],"texture":0},"south":{"uv":[64,0,0,64],"texture":0}}}],
            "outliner":[cube_id],"textures":[{"name":f"{key}.png","id":"0","namespace":"zerog_tweaks",
                "folder":"item","mode":"bitmap","source":"data:image/png;base64,"+base64.b64encode(data.getvalue()).decode(),
                "uuid":str(uuid.uuid5(uuid.NAMESPACE_URL,f"zerog_tweaks/texture/{key}"))}],
            "display":{"thirdperson_righthand":{"rotation":[0,0,0],"translation":[0,3,1],"scale":[.55,.55,.55]},
                       "firstperson_righthand":{"rotation":[0,-90,25],"translation":[1.13,3.2,1.13],"scale":[.68,.68,.68]},
                       "ground":{"translation":[0,2,0],"scale":[.5,.5,.5]}}}

def main():
    specs={i["k"]:i for i in F if i["kind"] in ("raw","cooked") and i["k"] not in ("baked_tuber","lichen_crisps","roasted_solflower_seeds")}
    specs.update({i["k"]:i for i in F if i["k"] in ("frost_milk","blue_egg")})
    specs.update({i["k"]:i for i in MAT})
    specs.update({i["k"]:i for i in REW if i["k"] in REWARD_IDS})
    for key,color in (("crystal_shard","#3fc9e8"),("remnant_shard","#b8d8e8")):
        specs[key]={"k":key,"n":key.replace("_"," ").title(),"mask":"core","H":color,"A":"#f4ffff","G":color,"W":"#8a929e"}
    PROJECTS.mkdir(parents=True,exist_ok=True)
    design_only=[]
    for key,item in sorted(specs.items()):
        image=render(item)
        if (ASSETS/"models/item"/f"{key}.json").exists():
            image.save(ASSETS/"textures/item"/f"{key}.png")
        else:
            design_only.append(key)
            (PROJECTS/"textures").mkdir(exist_ok=True)
            image.save(PROJECTS/"textures"/f"{key}.png")
        (PROJECTS/f"{key}.bbmodel").write_text(json.dumps(bbmodel(item,image),indent=2)+"\n",encoding="utf-8")
    (PROJECTS/"manifest.json").write_text(json.dumps({"items":list(specs),"design_only":design_only,"resolution":64,"source":"food_data.py F/MAT/REW/MASK"},indent=2)+"\n",encoding="utf-8")
    print(f"Built {len(specs)} authored drop, cooked-food and reward sprites/models at 64x64.")

if __name__=="__main__":main()
