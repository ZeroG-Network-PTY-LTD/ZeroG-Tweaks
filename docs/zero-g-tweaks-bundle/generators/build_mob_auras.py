"""Optional original aura overlays and combined Blockbench preview projects."""
import base64
import copy
import io
import json
import math
from pathlib import Path
from PIL import Image
from build_mob_models import ROOT, uid, keyframe, write_json

OUT=ROOT/"docs/zero-g-tweaks-bundle/blockbench/auras"
SELECTED={"frost_warden","flare_sprite","prism_sentinel","prismling","crater_drifter","rift_tyrant","eidolon_captain","dying_star","glimmerfish","ice_leech","scorch_wyrmling"}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    records=[]
    paths=list((ROOT/"docs/zero-g-tweaks-bundle/blockbench/mobs").glob("*.bbmodel"))+list((ROOT/"docs/shattered-skies/blockbench").glob("*.bbmodel"))
    for path in sorted(paths):
        source=json.loads(path.read_text())
        ns,key=source["model_identifier"].split(":")
        if ns!="shatteredskies" and key not in SELECTED:continue
        assets=ROOT/"src/main/resources/assets"/ns
        mask=assets/"textures/entity"/f"{key}_glowmask.png"
        if not mask.exists():continue
        colors=Image.open(mask).convert("RGBA").getcolors(16777216)
        visible=[(n,c) for n,c in colors if c[3]>0 and sum(c[:3])>220]
        color=max(visible,key=lambda p:p[0])[1][:3] if visible else (178,132,244)
        texture=Image.new("RGBA",(128,128))
        for y in range(128):
            for x in range(128):
                radius=math.hypot((x-63.5)/63.5,(y-63.5)/63.5)
                ring=max(0,1-abs(radius-.72)/.21)
                haze=max(0,1-radius)*.16
                alpha=round((ring*.055+haze*.65)*255/4)*4
                if radius>=1:alpha=0
                texture.putpixel((x,y),(*color,alpha))
        texture.save(assets/"textures/entity"/f"{key}_aura.png")
        atlas=source["resolution"]
        buff=io.BytesIO();texture.resize((atlas["width"],atlas["height"]),Image.Resampling.NEAREST).save(buff,format="PNG")
        preview=copy.deepcopy(source)
        preview["name"]=key+" with optional aura"
        preview["textures"].append({"name":f"{key}_aura.png","id":"1","uuid":uid(key,"aura_texture"),"mode":"bitmap","visible":True,"saved":True,"source":"data:image/png;base64,"+base64.b64encode(buff.getvalue()).decode(),"width":atlas["width"],"height":atlas["height"],"uv_width":atlas["width"],"uv_height":atlas["height"]})
        lo=[min(e["from"][a] for e in source["elements"]) for a in range(3)]
        hi=[max(e["to"][a] for e in source["elements"]) for a in range(3)]
        center=[(a+b)/2 for a,b in zip(lo,hi)]
        radius=max((hi[a]-lo[a])/2 for a in range(3))*1.2
        bone={"name":"aura","origin":center,"uuid":uid(key,"aura_bone"),"export":True,"visibility":True,"children":[]}
        cubes=[]
        for axis in range(3):
            a=[c-radius for c in center];b=[c+radius for c in center]
            a[axis]=b[axis]=center[axis]
            faces=(("east","west"),("up","down"),("north","south"))[axis]
            # Base texture atlas determines BB UV coordinate units for every texture.
            w,h=preview["resolution"]["width"],preview["resolution"]["height"]
            ident=uid(key,"aura_plane",axis)
            preview["elements"].append({"name":f"aura_plane_{axis}","type":"cube","uuid":ident,"from":a,"to":b,"origin":center,"rotation":[0,0,0],"box_uv":False,"light_emission":15,"faces":{f:{"uv":[0,0,w,h],"texture":1} for f in faces}})
            bone["children"].append(ident)
            cubes.append({"origin":a,"size":[v-u for u,v in zip(a,b)],"uv":{f:{"uv":[0,0],"uv_size":[128,128]} for f in faces}})
        preview["outliner"][0]["children"].append(bone)
        clip=f"animation.{ns}.{key}.aura_pulse"
        values=[(0,[1,1,1]),(1.5,[1.06,1.06,1.06]),(3,[1,1,1])]
        preview["animations"].append({"name":clip,"uuid":uid(key,"aura_pulse"),"length":3,"loop":"loop","override":False,"snapping":20,"animators":{bone["uuid"]:{"name":"aura","type":"bone","keyframes":[keyframe(t,"scale",v,clip) for t,v in values]}}})
        write_json(OUT/f"{key}.bbmodel",preview)
        geo={"format_version":"1.12.0","minecraft:geometry":[{"description":{"identifier":f"geometry.{ns}.{key}.aura","texture_width":128,"texture_height":128,"visible_bounds_width":radius/8+1,"visible_bounds_height":radius/8+1,"visible_bounds_offset":[c/16 for c in center]},"bones":[{"name":"aura","pivot":center,"cubes":cubes}]}]}
        write_json(assets/"geo"/f"{key}.aura.geo.json",geo)
        write_json(assets/"animations"/f"{key}.aura.animation.json",{"format_version":"1.8.0","animations":{clip:{"loop":True,"animation_length":3,"bones":{"aura":{"scale":{str(t):v for t,v in values}}}}}})
        records.append({"model":key,"namespace":ns,"color":color,"opacity_max":texture.getchannel("A").getextrema()[1],"render_requirement":"translucent emissive layer, separate aura texture and geometry; render with mob transform"})
    write_json(OUT/"manifest.json",{"auras":records,"runtime_wired":False})
    print(f"Built {len(records)} optional aura preview projects and overlay exports.")

if __name__=="__main__":main()
